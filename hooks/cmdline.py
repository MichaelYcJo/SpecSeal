#!/usr/bin/env python3
"""Reading a shell command line: where one invocation ends, and what git it is.

Two gates ask the same three questions of the string the harness hands them.
`hooks/commit-review-gate.py` asks where one invocation ends so a heredoc
commit body is not mistaken for a second command; `hooks/worktree-guard.py`
asks the same, then asks which repository a `git -C` names. Neither owns the
answer, so it lives here.

`hooks/optin.py` states the rule this module follows: "the answer moved once
already, and four divergent copies is how half of them keep the old answer."
Copying was not what went wrong here — the two gates imported each other
instead, and that is worse. The commit gate loaded the guard for `parse_git`
and `apply_chdir`; the guard loaded the commit gate for `split_segments`;
`importlib.util.module_from_spec` does not consult `sys.modules`, so neither
load was deduplicated and the pair recursed. Measured on a merge tree built
with `git merge-file` from the two branches that each held one half: 496
executions of the two module bodies per hook event instead of two, and one
`dispatch.py pre-bash` call going from 25.7ms to 100.8ms (median of fifteen).
The verdicts were still right. The cost was the defect.

A plain filename with no hyphen is the whole fix: `import cmdline` goes
through `sys.modules` and runs once, the way `import optin` already does in
four gates.

There is no load fallback here and none is wanted. A gate that cannot read a
command line has no verdict to give, so a soft failure and a hard one are the
same silence — the difference would only be which line it happens on.
`hooks/dispatch.py:72` (`except Exception: return ""`) is what turns either
into silence, and that is the place to fix it; a `try` around the import here
would only make the silence look deliberate.
"""

import os
import shlex

WRAPPERS = {"command", "env", "nohup", "time", "sudo"}

# Characters after which a `#` starts a comment. A shell ends a word at these,
# and `#` opens a comment only at the start of a word: `git switch feat#1`
# names a branch, and dropping from that `#` would leave `git switch feat`.
#
# `(` and `)` are NOT here, and the reason is that neither answer is right for
# both of them. A `)` that closes `$(…)` leaves the word running — executed,
# `bash -c 'echo $(echo a)#foo && echo X'` prints `a#foo` and then `X`, so
# that `#` opens nothing — while a `)` that closes a SUBSHELL ends the word
# and the `#` after it IS a comment: `bash -c '(echo a)#x' $'\n' echo REACHED`
# prints `a` and reaches the next line.
#
# Treating every `)` as a word end deleted a command; treating none as one
# left a real comment in place, and an apostrophe inside it then opened a
# quote that never closes, which took every LATER line out of the segment
# list — the failure this function's own docstring exists to describe, and a
# commit two lines down went unseen. Both directions were measured against the
# gate, one round apart. So the loop below tracks which kind each `)` closes
# and this constant holds only the characters where there is nothing to tell
# apart.
#
# WHICH KIND, precisely. NINE openers make the `(` part of a word: `$(` (and
# `$((`), the `<(` and `>(` of a process substitution, the `(` of an array
# assignment `name=(`, and extglob's five — `@(`, `!(`, `*(`, `+(`, `?(`. Two
# close a COMMAND: a subshell's `(` and an arithmetic command's `((`.
#
# Round 4 enumerated four and declared the list closed; round 5 generated 1,815
# inputs and found the other five. The extglob half is a fail-OPEN and it hides
# from the obvious check: `bash -n` calls `ls -d @(a|b)#x ; git commit` a syntax
# error, and running it really commits, because `extglob` is a RUNTIME shopt the
# parse check cannot see. Measure this family with `bash -O extglob`, never with
# `bash -n`. Read as a command paren, the `)` ended the word, the `#` after it
# opened a comment bash does not, and the commit behind it was deleted — both
# gates silent. `release/v0.22.0` is silent too, by a different route, so it is
# not a regression; the line below is this branch's, so it is this branch's to
# get right. Reading a process
# substitution's or an array assignment's `)` as a subshell's put a comment
# where bash opens none and deleted the commit behind it — six forms, each of
# which really commits, measured under bash 3.2.57 against a scratch
# repository, silent at the revision before this one and denied after it.
# `f()` is a function definition rather than an assignment, which is why the
# preceding CHARACTER decides and not the preceding word.
WORD_BREAK = " \t\r\n;|&<>"


def drop_comments(command: str) -> str:
    """`command` with its shell comments removed, quotes respected.

    A JUDGMENT read has to do this and a CONSENT read must not; the two
    callers are `split_segments` for the first and the gates' own bare-word
    scans for the second.

    Why judgment needs it: `#` opens a comment and `\\n` closes it, so bash
    runs the next line. `shlex` with `commenters=""` — which is what keeps a
    `[worktree-ok]` written inside a comment readable — sees no comment at
    all, and an apostrophe in one is an opening quote to it. Everything after
    that point is swallowed into a string that never closes, the lexer raises,
    and every LATER line is gone from the segment list. Measured: `git status
    # don't forget` followed by `git worktree add ../wt f` runs both lines in
    bash and produced no verdict at all in the guard, while the same two lines
    without the apostrophe denied.

    Why consent must not: a retry token is written in a comment on purpose
    (`git worktree add ../wt f  # [worktree-ok]`). Dropping comments before
    looking for it would throw away the only place users put it.

    A comment ends at the newline and the newline stays, because
    `split_segments` needs it to end the segment. Escaping and quoting follow
    the same rules as the splitter below, so the two agree about which `#`
    characters are inside a string.
    """
    out, quote, esc, comment, word_start = [], None, False, False, True
    # One entry per open `(`, True when the `(` is part of a WORD rather than
    # the start of a command. See `WORD_BREAK` above for the four openers that
    # make it a word, the two that make it a command, and what each answer
    # costs.
    #
    # `braces` is how deep inside a `${…}` parameter expansion this is, and
    # `dollar` is what opens one -- the `$` immediately before the `{`, asked
    # for on its own because `word_part` is also true after `<>=!@*+?` and
    # `A={a,b}` is a brace expansion rather than an expansion of a name.
    #
    # A measured finding says this function is ignorant of `${…}` and pays nothing for
    # it, measured on six `${x:-((}#zzz` shapes. The `#` after a BLANK inside
    # one was never measured and is a fail-OPEN: bash prints `a #b` for
    # `echo ${x:-a #b} ; echo REACHED` and reaches the next command, while
    # this function returned `echo ${x:-a ` and DELETED the `git commit`
    # behind it -- both gates silent. So the state goes in for a reason of its
    # own here, and not only to keep the two paren models saying one thing.
    parens, word_part, braces, dollar = [], False, 0, False
    for ch in command:
        if comment:
            if ch == "\n":
                comment, word_start = False, True
                out.append(ch)
            continue
        if esc:
            out.append(ch)
            esc, word_start, word_part, dollar = False, False, False, False
            continue
        if quote != "'" and ch == "\\":
            out.append(ch)
            esc, word_start, word_part, dollar = True, False, False, False
            continue
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
            word_start, word_part, dollar = False, False, False
            continue
        if ch in "'\"":
            quote = ch
            out.append(ch)
            word_start, word_part, dollar = False, False, False
            continue
        if ch == "#" and word_start and not braces:
            comment = True
            continue
        out.append(ch)
        if ch == "{" and dollar:
            braces += 1
        elif ch == "}" and braces:
            braces -= 1
        if ch == "(":
            # Inside a `${…}` the parenthesis is text the expansion carries,
            # so the word runs on through the `)` that closes it. An
            # unbalanced `{` leaves this true to the end of the input, which
            # leaves a real comment standing -- the fail-CLOSED direction, and
            # the one this function's own docstring already takes.
            parens.append(word_part or bool(braces))
            word_start = True
        elif ch == ")":
            # An unbalanced `)` is not something this reader can place, and
            # ending the word is the answer that keeps a comment readable.
            # `else False` is what ENDS it. Round 4 found this fallback written
            # the other way round, against its own comment: a `case` pattern's
            # `)` — the place an unbalanced one actually occurs — left the word
            # running, the `#` after it read as no comment, and an apostrophe
            # inside that comment opened a quote that never closes. Measured:
            # bash DOES open a comment there, and the segment list came back
            # `clean=False`, which is the exact failure this function's
            # docstring exists to describe.
            word_start = not (parens.pop() if parens else False)
        else:
            word_start = ch in WORD_BREAK
        word_part = ch in "$<>=!@*+?"
        dollar = ch == "$"
    return "".join(out)


def _closes(command, i):
    """True when the `${` at `i` has a `}` that closes it.

    Round 2 asked for `not braces` on the two heredoc openers and the answer
    could not simply be added: an unbalanced `${` would then hold the count
    open to the end of the input, hide every heredoc opener after it, and
    read a heredoc BODY as commands -- the fail-OPEN direction, and the
    opposite of what the count was added for.
    `tests/test_what_the_reader_understands.py` pins `echo ${x <<EOF`, which
    is exactly that shape.

    So an expansion counts only if the shell would accept it. Quotes are
    tracked because a `}` inside one closes nothing.
    """
    depth, j, n, quote = 0, i, len(command), None
    while j < n:
        ch = command[j]
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif command.startswith("${", j):
            depth += 1
            j += 2
            continue
        elif ch == "}":
            depth -= 1
            if not depth:
                return True
        j += 1
    return False


def _heredoc_word(command, i):
    """(delimiter, index after it) for the word a `<<` redirect names.

    The delimiter may be quoted (`<<'EOF'`, `<<"EOF"`) or bare, and quoting is
    what decides whether the SHELL expands the body — which this reader does
    not care about, because it drops the body either way. What it does decide
    here is where the word ends.
    """
    out, quote, n = [], None, len(command)
    while i < n:
        ch = command[i]
        if quote:
            if ch == quote:
                quote = None
            else:
                out.append(ch)
            i += 1
            continue
        if ch in "'\"":
            quote = ch
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            out.append(command[i + 1])
            i += 2
            continue
        if ch in " \t\n;|&<>()":
            break
        out.append(ch)
        i += 1
    return "".join(out), i


def drop_heredoc_bodies(command: str) -> str:
    """`command` with heredoc BODIES removed, quotes and comments respected.

    A heredoc body is data. The shell feeds it to a command on stdin and never
    executes it, so a JUDGMENT read has to drop it — the same rule, and the
    same reason, as `drop_comments` above. Writing a script and then committing
    it is ordinary:

        cat > run.sh <<'EOF'
        cd /somewhere/else
        make
        EOF
        git add -A && git commit -m x

    Every newline was a segment separator, so the `cd` on the second line moved
    the reader's shell and the commit two lines later was judged against a
    repository the shell never entered. The session's own directory was not
    among the candidates at all: not over-collecting and missing, but
    confidently wrong. `hooks/worktree-guard.py` recorded the same residual for
    its own splitter.

    What it does NOT do, deliberately: it does not track which command owns
    which redirect, so two heredocs opened on one line have their bodies read
    off in the order the delimiters appeared, which is what a shell does. A
    `<<` inside a comment opens nothing, because a comment is not a redirect —
    without that, `echo hi # cat <<EOF` would swallow every command after it,
    which is the fail-open direction. `<<<` is a herestring and opens no body.

    Neither does `$((…))`, and that one was a defect rather than a decision.
    The `<<` in `n=$((1<<2))` is an arithmetic left shift; reading it as a
    redirect took `2))` for a delimiter and dropped every line after it until
    one matched — which no line does, so a `git commit` on the next line was
    not merely misjudged, it was gone from the segment list entirely and
    neither gate had anything to say. Arithmetic is copied through to its
    matching `))`, which is also why a `<<` inside one opens nothing.

    An unterminated body runs to the end of the input, which is what the shell
    does with one.
    """
    stripped, _bodies = _heredoc_split(command)
    return stripped


def heredoc_bodies(command: str) -> list:
    """The text of every heredoc body `drop_heredoc_bodies` removes, in order.

    Same reach and the same blind spots — two on one line come back in
    delimiter order, one inside quotes or a subshell is invisible here exactly
    as it is to the opener scan `drop_heredoc_bodies` runs. Measured: a body
    is data only where nothing ever reads it back as commands. `bash <<EOF`
    hands its body to a shell that executes it, so a caller checking whether a
    dropped body hides a `git commit` needs the text this drops, not just the
    command with it gone.
    """
    _stripped, bodies = _heredoc_split(command)
    return bodies


def _heredoc_split(command: str):
    """(stripped, bodies) -- `drop_heredoc_bodies` and `heredoc_bodies` share one pass."""
    out, i, n = [], 0, len(command)
    bodies = []
    quote, esc, comment, word_start, pending = None, False, False, True, []
    # How deep inside a `${…}` parameter expansion this is. The `((` below is
    # arithmetic everywhere except in here, where it is text the expansion
    # carries -- see the branch for what that costs and what it buys.
    braces = 0
    while i < n:
        ch = command[i]
        if esc:
            out.append(ch)
            esc, word_start = False, False
            i += 1
            continue
        if not comment and quote != "'" and ch == "\\":
            out.append(ch)
            esc, word_start = True, False
            i += 1
            continue
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
            word_start = False
            i += 1
            continue
        if not comment and ch in "'\"":
            quote = ch
            out.append(ch)
            word_start = False
            i += 1
            continue
        if not comment and ch == "#" and word_start and not braces:
            # `and not braces` is the same guard `drop_comments` carries, and
            # it was added there and not here. Round 1 measured what that
            # cost: `${x:-a #b}` opened a comment that swallowed the closing
            # `}`, so `braces` stayed 1 to the end of the input, every `((`
            # after it stopped being an arithmetic region, and a `<<` inside
            # one opened a heredoc that ate the rest of the command. The
            # `git worktree add` below such a line left the segment list
            # entirely and the worktree guard went silent on a command bash
            # really runs. Two models of one question have to answer it the
            # same way, which is the whole subject of that finding.
            comment = True
            out.append(ch)
            i += 1
            continue
        if not comment and command.startswith("${", i) and _closes(command, i):
            # A parameter expansion. Counted rather than matched, so
            # `${x:-${y}}` closes where the shell closes it, and only `${`
            # opens one: a bare `{` is a brace expansion or a group, and
            # counting it would hold this open past the `}` that ends it.
            #
            # An unbalanced `${` leaves this open to the end of the input,
            # which is the direction that can HIDE a real `((` region and let
            # a `<<` inside it open a body. That is the fail-open direction,
            # and what bounds it is that only `${` reaches here at all --
            # quotes, escapes and comments are handled by the branches above.
            braces += 1
            out.append(command[i : i + 2])
            word_start = False
            i += 2
            continue
        if not comment and ch == "}" and braces:
            braces -= 1
            out.append(ch)
            word_start = False
            i += 1
            continue
        if not comment and (
            command.startswith("$((", i)
            or command.startswith("$[", i)
            or (not braces and command.startswith("((", i))
        ):
            # `((` needs no preceding blank, and requiring one was a
            # fail-open. `(` is a bash metacharacter, so a reserved word ENDS
            # at it: `do((`, `then((`, `else((`, `!((` and `{((` are arithmetic
            # commands to bash and were heredoc redirects to this reader, which
            # took the `<<`'s delimiter out of the expression and swallowed
            # every line after it — the `git commit` included. Measured under
            # bash 3.2.57: all five really create a commit and both gates
            # stayed silent, while the same command with ONE space was read
            # correctly. bash DOES re-parse `((` as nested subshells when
            # the arithmetic parse fails — `bash -c '((echo a) )'` prints `a`,
            # measured. Those forms are paren-balanced so stepping over them
            # changes no answer, but the sentence that stood here said no such
            # form exists and that was simply false.
            #
            # WHAT DROPPING THE BLANK COST, AND WHY `braces` IS HERE. Round 4
            # measured eight shapes by hand and reported two, both supposedly
            # rejected by `bash -n`. Round 5 generated 1,815 inputs: the real
            # number was 51, every one a `((` written inside a `${…}`
            # parameter expansion, reproduced by all seventeen operators that
            # take a WORD, and bash accepts them all. `${x:-((}` has no
            # closing paren, so the region ran to the end of the input, the
            # `<<` below was never seen as a redirect, and the heredoc body
            # stayed in as commands. (`!((<<E … ))` passes `bash -n` too, so
            # "both are rejected" was wrong twice over.)
            #
            # That family was accepted as rare and pinned by test, and a later
            # finding is what reopened it: `echo ${x:-((} <<EOF / cd <path> / EOF
            # / git commit` makes one commit in bash and never leaves its
            # directory — executed, 1 -> 2 in a scratch repository, `pwd`
            # unmoved — while the gate answered for a path that exists only in
            # the heredoc body and DENIED a commit that had already been
            # reviewed. `braces` above is that fix: a bare `((` inside `${…}`
            # is the text bash treats it as, and `$((` and `$[` stay
            # arithmetic in there because they are unambiguous.
            #
            # Skipping the region is still fail-CLOSED, for the reason below —
            # it is copied through verbatim, so widening it can only skip a
            # heredoc DELETION. NARROWING it, which `braces` does, is the
            # direction that can delete one, so `${` alone opens the count and
            # every `}` closes it: an unbalanced `{` therefore leaves this
            # reader where it already was rather than one step further.
            #
            # Quotes and comments are handled by the branches above this one,
            # so `echo '((' <<EOF` is untouched. Trading a fail-open on five
            # valid forms for a fail-closed on this family is the direction
            # this repository takes everywhere else.
            #
            # Arithmetic, not a subshell and not a redirect. Copied through to
            # the bracket that closes it: this reader has no use for the
            # value, and stepping over the region is what keeps a `<<` inside
            # it from opening a body. Nesting is counted rather than matched
            # on the first close, so `$(( (1<<2) + 3 ))` ends where the shell
            # ends it. One that never closes runs to the end of the input,
            # which is the same thing the shell's own parser does with it.
            #
            # `$[1<<2]` is the same construct in bash's older spelling, and it
            # closes on ONE bracket. Left out, it swallowed the commit below
            # it exactly as `$((1<<2))` did — executed, with the commit really
            # created and the reader's segment list holding no commit at all.
            #
            # Quotes are tracked inside the region, because the depth count is
            # otherwise fooled by a parenthesis in a string: one `(` inside
            # `'…'` stretched the region to the end of the input and raised a
            # following heredoc body as commands.
            bracket = "[" if command.startswith("$[", i) else "("
            closer = "]" if bracket == "[" else ")"
            j = i + (2 if bracket == "[" else (3 if command[i] == "$" else 2))
            depth = 1 if bracket == "[" else 2
            inner = None
            while j < n and depth:
                c = command[j]
                if inner:
                    if c == inner:
                        inner = None
                elif c in "'\"":
                    inner = c
                elif c == bracket:
                    depth += 1
                elif c == closer:
                    depth -= 1
                j += 1
            out.append(command[i:j])
            word_start = False
            i = j
            continue
        if not comment and not braces and command.startswith("<<<", i):
            # A herestring feeds one word and opens no body. Stepping over all
            # THREE characters is what keeps the `<<` inside it from being read
            # as a redirect on the next pass — which swallowed every command
            # after `cat <<<hello`.
            out.append(command[i : i + 3])
            word_start = False
            i += 3
            continue
        if not comment and not braces and ch == "<" and command.startswith("<<", i):
            j = i + 2
            dashed = j < n and command[j] == "-"
            if dashed:
                j += 1
            while j < n and command[j] in " \t":
                j += 1
            delim, j = _heredoc_word(command, j)
            if delim:
                pending.append((delim, dashed))
                out.append(command[i:j])
                word_start = False
                i = j
                continue
        if ch == "\n":
            out.append(ch)
            i += 1
            comment, word_start = False, True
            for delim, dashed in pending:
                body_lines = []
                while i < n:
                    end = command.find("\n", i)
                    line = command[i:] if end == -1 else command[i:end]
                    i = n if end == -1 else end + 1
                    if (line.lstrip("\t") if dashed else line).rstrip("\r") == delim:
                        break
                    body_lines.append(line.rstrip("\r"))
                bodies.append("\n".join(body_lines))
            pending = []
            continue
        out.append(ch)
        comment = comment and ch != "\n"
        word_start = ch in WORD_BREAK
        i += 1
    return "".join(out), bodies


def split_segments(command):
    """Split into pipeline/list segments while respecting quotes.

    A regex split on `;`/`&&`/newline breaks inside quoted strings, so the
    heredoc commit form Claude Code itself uses (`git commit -m "$(cat
    <<'EOF' ...)"`) fell apart mid-quote and slipped past the commit gate.
    shlex with punctuation_chars keeps quoted arguments whole and emits
    the separators as their own tokens.

    Unquoted newlines separate commands just like `;`; newlines inside
    quotes belong to an argument and must not split it. shlex alone treats
    every newline as plain whitespace, so a small quote-aware scan converts
    only the unquoted ones first.

    `commenters` is cleared: a `#` has to survive as an ordinary character so
    that a retry token written in a comment can still be matched as a bare
    word. Callers judging what a command DOES run it through `drop_comments`
    first — see that docstring for what clearing this costs otherwise.

    Returns (segments, parsed_cleanly)."""
    items, clean = split_segments_with_separators(command)
    return [tokens for _, tokens in items], clean


def split_segments_with_separators(command):
    """The same split, keeping the operator that joined each segment.

    Returns ([(separator, tokens), ...], parsed_cleanly). `separator` is the
    operator that joined this segment to the one before it, "" for the first.

    The separator used to be emitted as a token and dropped, so `&&`, `;` and
    `||` were indistinguishable downstream — measured on all three forms of
    `cd /tmp/x <sep> git commit`, which returned the same two segments. In a
    shell the last of those is the opposite of the first: `&&` runs the commit
    where the `cd` arrived, `||` runs it only if the `cd` failed, which is
    where the shell already was. Without the operator, a reader following the
    `cd` judges the wrong repository with confidence on `||`, and a reader
    judging every reachable directory keeps asking about the session's own on
    `&&` — the prompt volume this exists to reduce.

    It arrives beside the tuple rather than inside it because three call sites
    read `split_segments`' two elements (`hooks/commit-review-gate.py`,
    `hooks/worktree-guard.py`, and that guard's consent read), and a third
    element in the middle of a fix for silent misjudgment is a change to every
    one of them.
    """
    out, quote, esc = [], None, False
    for ch in command:
        if esc:
            # A backslash-newline is a line continuation: the shell removes
            # BOTH characters and the command is one line. Keeping them turned
            # `cd /B \<newline> && git commit` into a two-argument `cd`, which
            # reads as a destination that cannot be computed — so a command
            # that passes on one line was stopped for being wrapped.
            if ch == "\n":
                out.pop()
            else:
                out.append(ch)
            esc = False
            continue
        if quote != "'" and ch == "\\":
            out.append(ch)
            esc = True
            continue
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        # Spaced, because shlex groups a RUN of punctuation into ONE token:
        # `cd /B ||` followed by a newline became the single token `||;`,
        # which is neither a branching operator nor a plain `;`. Writing the
        # operator at the end of the line is how a long command is normally
        # written, so this was the common form and not a constructed one, and
        # it went silent where the release before this work stopped it.
        # Measured tokens before the spaces: `||;`, `|;`, `&;`.
        out.append(" ; " if ch == "\n" and quote is None else ch)
    command = "".join(out)

    lex = shlex.shlex(command, posix=True, punctuation_chars=";|&")
    lex.whitespace_split = True
    lex.commenters = ""
    items, current, sep = [], [], ""
    try:
        for tok in lex:
            if tok and set(tok) <= set(";|&"):
                if current:
                    items.append((sep, current))
                    current, sep = [], tok
                # Two operators with nothing between them — `cd x ||` and then
                # a newline, which arrives here as its own `;`. The FIRST one
                # is the one that binds the segments; the second is the line
                # ending, and letting it win turned a multi-line `||` into a
                # `;` and dropped the session's own directory from the answer.
                elif not sep:
                    sep = tok
            else:
                current.append(tok)
    except ValueError:
        if current:
            items.append((sep, current))
        return items, False
    if current:
        items.append((sep, current))
    return items, True


# Operators that make a segment's effect, or the segment itself, uncertain.
#
# `||` runs its right side only when the left FAILED, so a `cd` in front of one
# leaves the shell in two possible places — and the segment after a `||` may be
# skipped entirely, which is the other half: `cd N || cd B && git commit`
# commits in N when the first `cd` works and in B when it does not.
#
# The other three are subshell boundaries. `&` runs the left side in the
# background, and both sides of a pipeline run in subshells, so a `cd` there
# does not move the shell the next command runs in — executed: `bash -c 'cd
# <B> | pwd'` prints the directory it started in. `|` and `|&` were missing
# here while `&` was present, which is the same property answered two ways:
# `cd <B> | git commit` was judged as landing in B while the commit landed
# where the shell already was, and a routing declaration in B then silenced it.
#
# Both directions are read, because a shell can also be told to run a
# pipeline's last stage in the current shell (`shopt -s lastpipe`), and this
# process cannot see which shell will run the string or how it is configured.
BRANCHING = ("||", "|", "|&", "&")

# The three that open a subshell, where the `cd` does not reach the parent
# shell at all. Told apart from `||` because they say something different
# about the segment: `||` may not RUN it, while these run it somewhere the
# parent cannot see.
SUBSHELL = ("|", "|&", "&")

# How many landing places one command may have before the reader gives up and
# says so. This is CONTAINMENT, not a fix: exclusive branches no longer
# compose (see `walk_directories`), which is what removed the measured
# explosion, and what is left is every shape whose REACHABLE directories
# genuinely multiply. Measured at this cap, counting the `cd` segments in
# front of the commit: a chain of pipe stages reaches it at seven, because
# each stage keeps the moved directory beside the unmoved one — six when the
# commit is joined by `;` rather than `&&`, since that parks a branch at every
# stage as well; a chain of `;`-joined `cd`s at seven, where before that change
# it did not multiply at all; a chain alternating `&&` and `||` at nine or
# ten, depending on which of the two starts it. No set is phantom —
# every directory in it is somewhere the command can really commit — so the
# cap is a limit on how much answering the reader will do, not a correction.
# Past it the command reads as a directory that could not be computed, which
# is this module's existing failure direction: a stop, never a guess.
STATE_CAP = 64

# Characters that make a `cd` destination something other than the path it
# looks like. The command is read BEFORE the shell expands it — the same fact
# that makes `git -C "$WT"` unresolvable — so `$` and a backtick
# name a value this process cannot see, and the glob and brace characters name
# a set of paths rather than one. A backslash is deliberately NOT here: it is
# the path separator on Windows, and `hooks/worktree-guard.py` hands the
# splitter a command whose backslashes are doubled precisely so the value
# survives.
EXPANDS = "$`*?[]{}"

# `cd` accepts these before its operand; they change how symlinks resolve and
# not where the shell lands.
CD_FLAGS = ("-L", "-P", "-e", "-@")

# The characters a shell name is made of. ASCII by hand rather than
# `str.isalnum`, which answers yes for every letter in Unicode and would read
# a name the shell will not accept.
_NAME_HEAD = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
_NAME_TAIL = _NAME_HEAD | frozenset("0123456789")


# THE NAMES A COMMAND WRITES FOR ITSELF.
#
# `SB=/abs/path; git -C "$SB" commit` names its destination twice. Once as an
# assignment three separate readers step past and throw away — `understood`,
# `_cd_target` and `parse_git` each hold the same three lines — and once as a
# `$SB` the `EXPANDS` test above calls unresolvable. The value is in the
# string both times, and an earlier round is what throwing it away costs: a review
# agent's scratch-repo probes reached a user who was not driving the session
# as permission prompts, twice inside five minutes, and stopping the agent
# cost the review round.
#
# What is filled in is exactly what the COMMAND STRING says. Nothing is read
# from this process's environment: `git -C "$WT"` with no assignment in the
# string stays unresolvable, which is the whole of that defect and the
# confident-wrong answer `understood`'s docstring exists to end. A hook's
# environment is not the shell's, and answering from it would be silently
# wrong exactly where the two differ.
#
# Three bounds keep this narrow, and each is load bearing.
#
# - Only `$NAME` and `${NAME}` are filled. `${x:-y}`, `$(pwd)`, `$((n+1))`,
#   `$1` and `$@` are left standing, so the `$` survives into the `EXPANDS`
#   test and the operand is unresolvable exactly as before.
# - The filling happens IN FRONT of that test and never replaces it. What
#   cannot be filled lands on the same `Unresolved` it landed on before —
#   `$SB/r$n` from a loop resolves its `$SB` and keeps its `$n`, so the text
#   the prompt prints names the part that could not be read rather than the
#   part that could.
# - Only a segment `understood` accepts contributes a name, and never one
#   bash runs in a subshell. `for … do SB=/x; done` and `SB=/x | cat` both
#   leave the parent shell's `SB` alone; so do they here.
#
# WHAT IT COSTS, measured. A SINGLE-quoted operand expands nothing in bash,
# and this reader cannot tell one from a double-quoted one: `shlex` runs in
# posix mode and takes both kinds of quote off, so `git -C '$SB'` and
# `git -C "$SB"` arrive here as the same token. bash operates on a directory
# literally named `$SB` and this reader now says `/x`, where before it said
# `<cwd>/$SB` and was right. That is the fail-OPEN direction — a target the
# command never reaches, judged instead of the one it does — and it is
# accepted rather than closed: it needs a directory literally named `$SB`,
# single-quoted, in a command that also assigns `SB`. Closing it means
# carrying quote provenance out of the splitter, which changes how every
# argument in every command tokenizes. Pinned by test so it stays a decision.
def _name_at(text, i):
    """(name, index past it) for a shell name starting at `i`, else (None, i)."""
    if i < len(text) and text[i] in _NAME_HEAD:
        j = i + 1
        while j < len(text) and text[j] in _NAME_TAIL:
            j += 1
        return text[i:j], j
    return None, i


def _substitute(operand, env):
    """`operand` with the names `env` holds filled in, left to right.

    One pass, and what a substitution writes is never rescanned: a value
    holding a `$` of its own cannot expand again, so nothing here loops and
    every `$` left in the result is one this reader could not fill.
    """
    if not env or "$" not in operand:
        return operand
    out, i, n = [], 0, len(operand)
    while i < n:
        if operand[i] != "$":
            out.append(operand[i])
            i += 1
            continue
        braced = i + 1 < n and operand[i + 1] == "{"
        name, end = _name_at(operand, i + 2 if braced else i + 1)
        if braced and not (name and end < n and operand[end] == "}"):
            # `${x:-y}`, `${#x}`, `${x[0]}` — an operator this reader does not
            # model, so the whole expansion stays as written and the `$` in it
            # is what makes the operand unresolvable.
            name = None
        if name is None or name not in env:
            out.append("$")
            i += 1
            continue
        out.append(env[name])
        i = end + 1 if braced else end
    return "".join(out)


# Builtins that write a shell name whose token carries no `=`. Their operands
# are bare names, so a segment running one of these leaves every name it
# mentions in a state this reader cannot state.
NAME_WRITERS = frozenset(
    {"read", "mapfile", "readarray", "getopts", "let", "printf", "unset"}
)


def _forget(env, tokens):
    """`env` without the names this segment may have written and did not bind.

    The mirror of `_bind`, and it is not symmetric with it on purpose: `_bind`
    is strict about what it will take, because a wrong name answers with
    confidence, and this is permissive about what it will drop, for the same
    reason. A name whose segment merely LOOKS like it assigns is forgotten,
    because forgetting costs a prompt and keeping costs a repository nobody
    reviewed.

    What it looks for is a bare `NAME` followed by `=`, `+=` or `[`, anywhere
    in the segment: `export SB=/x`, `declare -g SB=/x`, `readonly SB=/x`, and
    a plain `SB=/x` that `_bind` refused because the segment it sits in is a
    loop body or a conditional branch.

    A second family writes a name with no `=` in the token at all -- `read SB`
    is the common one, and `mapfile`, `readarray`, `getopts`, `let` and
    `printf -v` do the same. `unset` is here too: it does not write a name,
    it removes one, and to this reader the effect is the same -- the earlier
    value must not survive. Their operands are bare names, so every bare name
    in such a segment is forgotten. `read SB` leaked past the first version of
    this, answering with the value from before the read, and `IFS= read -r SB`
    leaked past the second because only the first token was examined.

    Round 1 of the re-application added three writers with no `=` at the
    start of a word. `((SB=3))` arrives as one token behind two parens, so the
    parens come off before the name is read; `let "SB = 3"` writes the name at
    the start of EVERY operand, blank or not, so `let` forgets the leading
    name of each rather than the bare ones; and `${SB:=/x}` or `${SB=/x}`
    writes `SB` from any argument position at all, so every token is scanned
    for that operator.
    """
    for tok in tokens:
        head = tok.lstrip("(")
        name, end = _name_at(head, 0)
        if name and end < len(head) and head[end] in "=+[":
            env.pop(name, None)
        at = tok.find("${")
        while at != -1:
            name, end = _name_at(tok, at + 2)
            if name and (tok.startswith("=", end) or tok.startswith(":=", end)):
                env.pop(name, None)
            at = tok.find("${", at + 2)
    words = [tok for tok in tokens if not tok.startswith("-")]
    # Round 2: this read the segment's FIRST token, so anything in front of
    # the builtin hid it. `IFS= read -r SB` is the canonical shell idiom for
    # reading a line, and `command read SB` and `builtin read SB` are the two
    # spellings that reach past a function of the same name -- all three kept
    # the value from before the read. `_bind` already steps past assignment
    # prefixes to find the word that RUNS; this is the same walk.
    while words and (
        ("=" in words[0] and not words[0].startswith("-"))
        or os.path.basename(words[0]) in PREFIXES
    ):
        words.pop(0)
    if words and os.path.basename(words[0]) in NAME_WRITERS:
        bare = os.path.basename(words[0]) != "let"
        for tok in words[1:]:
            name, end = _name_at(tok, 0)
            if name and (end == len(tok) or not bare):
                env.pop(name, None)
    return env


# Words a refused segment can run that reach text this reader never sees. An
# `eval`, a sourced script and an `exec` run commands that are not in this
# string at all, and a `trap` runs them later; whatever names they write, this
# scan cannot name, so a segment holding one of these empties the environment
# rather than forgetting a list. `pushd`, `popd` and `alias` are the members
# of `RELOCATORS` deliberately NOT here: each moves the shell or rewrites a
# word, and none of them writes a shell name.
OPAQUE = frozenset({".", "source", "eval", "exec", "trap", "coproc"})

# The two reserved words whose OPERAND is a name they write, once per
# iteration. `for SB in /two /three` leaves `SB` at `/three`, which is not a
# value this reader can state, and no `=` appears in the segment for `_forget`
# to find.
LOOP_WORDS = frozenset({"for", "select"})


def _runs(tokens):
    """The word a refused segment actually runs, or None when it names none.

    `understood` refuses a segment for a reason, and the reason decides what
    the segment can have done to a NAME. This finds the word to ask that of:
    the compound-command structure in front of it -- a reserved word, a
    subshell or brace-group opener, a function definition's `f()` -- is not
    what runs, and neither are the assignment prefixes and wrappers `_forget`
    already steps past.
    """
    toks, _ = strip_subshell(tokens)
    opened = None
    while toks and (
        (toks[0] in RESERVED and toks[0] not in CONDITIONS and toks[0] not in PREFIXES)
        or toks[0].endswith("()")
        or toks[0] in ("(", "{", "((")
    ):
        opened = toks.pop(0)
    if opened == "case":
        # `case WORD in` -- the word is data being matched, not a command, so
        # an unreadable one says nothing about what ran.
        return None
    while toks and (
        ("=" in toks[0] and not toks[0].startswith("-"))
        or os.path.basename(toks[0]) in PREFIXES
    ):
        toks.pop(0)
    return toks[0] if toks else None


def _unseen(env, tokens):
    """`env` after a segment `understood` refused to read.

    The wide reset this replaces -- every name dropped, whatever the segment
    was -- is correct and was measured so: round 1 found `eval`, a sourced
    script and a loop body each answering with a path bash had left, and
    emptying the environment is what closed that. What it also did was empty
    it for segments that CANNOT write a name at all. `if [ -d <x> ]`,
    `then echo hi`, `fi`, `( echo hi )`, `{ echo hi; }`, `pushd <x>` and
    `case x in` each carry no name, and six shapes that answered `/one` at
    before the change prompted after it for that reason alone -- in a work item
    that exists to stop asking. `if …; then … fi` is the commonest shape in a
    script, so the reset is aimed rather than removed.

    Aimed in three steps, and every one of them errs toward forgetting:

    * A segment reaching text this reader never sees empties the environment
      exactly as before -- `OPAQUE` above, asked of every word rather than of
      the first, because `then eval "$x"` and `f() { eval "$x"` put it second
      -- and so does one whose command word this process cannot read before
      expansion, which is the same refusal `understood` makes for `$cmd`.
    * `for` and `select` forget the name they iterate.
    * Everything else forgets what it NAMES, by `_forget`, plus the bare names
      of any segment mentioning a `NAME_WRITERS` builtin ANYWHERE. `_forget`
      asks that of the word that runs, which is right where the reader knows
      what runs; here it does not, and `f() { read SB; }` and
      `while read -r SB` both hide the `read` behind structure. The cost of
      asking it blindly is a forgotten name where `echo read` was written --
      a prompt, which is what this branch gave for everything.
    """
    words = [tok for tok in tokens if not tok.startswith("-")]
    if any(os.path.basename(token) in OPAQUE for token in words):
        return {}
    word = _runs(tokens)
    if (
        word is not None
        and word != "["
        and word not in CONDITIONS
        and any(ch in word for ch in EXPANDS)
    ):
        # `[` and `[[` hold characters `EXPANDS` lists and are conditionals
        # rather than globs -- the same exception `understood` writes out, and
        # without it `if [ -d <x> ]` empties the environment again.
        return {}
    for at, token in enumerate(words):
        if token not in LOOP_WORDS:
            continue
        # `(` is stripped because the arithmetic head arrives as one token,
        # `for ((SB=0`, and `_name_at` reads a name from the start of a word.
        head = words[at + 1].lstrip("(") if at + 1 < len(words) else ""
        name, _ = _name_at(head, 0)
        if name is not None:
            env.pop(name, None)
        # A head no name can be read out of gets no branch of its own. The
        # loop word IS what `_runs` returns for a `for` segment, so the
        # `EXPANDS` test above has already emptied the environment for
        # `for $v in …`, and a branch nothing reaches is a finding round 2
        # wrote against this same walk.
    env = _forget(env, tokens)
    if any(os.path.basename(token) in NAME_WRITERS for token in words):
        # `let` writes the leading name of every operand, blank or not, so
        # where it is mentioned the bare-name rule is not enough.
        bare = "let" not in words
        for tok in words:
            name, end = _name_at(tok, 0)
            if name and (end == len(tok) or not bare):
                env.pop(name, None)
    return env


# The words that open a compound command's body, and for each closer the
# openers it may close. `then`, `do`, `else`, `elif` and `in` are deliberately
# absent: each sits INSIDE a body the opener already counted, and counting them
# would leave a body open for the rest of the string.
OPENERS = frozenset({"if", "while", "until", "for", "select", "case", "{", "("})
CLOSES = {
    "fi": frozenset({"if"}),
    "done": frozenset({"while", "until", "for", "select"}),
    "esac": frozenset({"case"}),
    "}": frozenset({"{"}),
    ")": frozenset({"("}),
}
CLOSERS = frozenset(CLOSES)


def _leads(tokens, at):
    """Whether `tokens[at]` stands in command position.

    Every word before it is one bash reads past to reach the command -- a
    reserved word, a prefix, an opener, a function definition's `f()`, or the
    NAME after `function`. A `case` pattern `x)` is none of those, and
    neither is an ordinary command word, so `git commit -m "(wip) x"` and
    `grep -c '(' f` open nothing.
    """
    return all(
        tok in RESERVED
        or os.path.basename(tok) in PREFIXES
        or tok.endswith("()")
        or (before > 0 and tokens[before - 1] == "function")
        for before, tok in enumerate(tokens[:at])
    )


def _nesting(tokens, stack):
    """`stack` -- the bodies still open -- after this segment.

    `walk_directories` threads it beside the name environment, and while it is
    not empty an assignment is forgotten rather than bound. Round 1 of the
    re-application replaced an integer count with this stack, because a count
    cannot say WHICH body a closer closes: a multi-line `case` puts its arm
    pattern on a line of its own, `a )`, and that `)` -- last in its segment,
    exactly where a subshell's closer stands -- brought the count to zero
    before the arm body, so the arm's assignment bound. bash: `/one`; the
    reader: `/three`. Here `)` pops only when `(` is on top, and every closer
    pops only the openers `CLOSES` names for it, so a `)` or a quoted `")"`
    inside a `case` closes nothing.

    The two directions of error do not cost the same. A body opened and never
    closed forgets every assignment after it, which is a prompt; a body closed
    early binds what a body wrote, which is the confident wrong answer this
    whole mechanism is bounded to avoid. So every opener and every closer is
    read in COMMAND POSITION only (`_leads`), where bash itself reads them:
    `echo fi` inside a body closed the count early and the assignment after it
    bound, and `git commit -m "(wip) x"` opened a body that never closed and
    prompted for the rest of the string. A `)` may also stand last, because
    that is where a subshell's closer is. `f(){` -- the glued spelling -- opens
    a `{` body; the spaced `f() {` opens it through the bare `{`.

    An opener read in command position and popped only by its own closer is
    what makes an UNCOUNTED opener safe: `y) if true; then :; fi` inside a
    `case` counts neither the `if` nor the `fi`, and the `case` stays open
    until `esac`. The cost is that a `case` arm that DOES match prompts too,
    because the reader cannot tell which arm bash took.

    Two costs remain, and both are prompts. A closer glued to its last word
    is not counted -- `(cd <x> && make)` arrives as `(cd` … `make)`, and only
    the opener is read, the rule `strip_subshell` applies -- because a `case`
    pattern `x)` closes nothing and nothing in the token tells the two apart.
    And `shlex` is posix-mode, so a `"fi"` written as a command inside a body
    closes it; telling the two apart means carrying quote provenance out of
    the splitter, which the single-quoted operand already declined to do.

    `((` is arithmetic, not a subshell: `for ((SB=0` arrives as `for` `((SB=0`,
    the `for` opens and the head does not, and `k++))` closes nothing either.
    """
    stack = list(stack)
    last = len(tokens) - 1
    for at, tok in enumerate(tokens):
        if tok.endswith("(){"):
            stack.append("{")
        elif tok in OPENERS and _leads(tokens, at):
            stack.append(tok)
        elif tok.startswith("(") and not tok.startswith("((") and _leads(tokens, at):
            stack.append("(")
        elif tok in CLOSERS and (at == 0 or (tok == ")" and at == last)):
            if stack and stack[-1] in CLOSES[tok]:
                stack.pop()
    return stack


def _definitions(tokens):
    """The names of the functions this segment defines.

    `f()`, the spaced `f ()`, the glued `f(){`, and `function f`. A name this
    reader has seen defined is a word it can see, so when it later arrives in
    command position the call empties the environment the way `OPAQUE` does --
    the body may have written any name, and which one is not something the
    reader can follow.
    """
    names = set()
    for at, tok in enumerate(tokens):
        if tok.endswith("(){"):
            names.add(tok[:-3])
        elif tok.endswith("()") and len(tok) > 2:
            names.add(tok[:-2])
        elif tok == "()" and at:
            names.add(tokens[at - 1])
        elif tok == "function" and at + 1 < len(tokens):
            names.add(tokens[at + 1].rstrip("{"))
    names.discard("")
    return names


def _bind(env, tokens):
    """`env` updated with this segment's leading `VAR=value` assignments.

    The value goes through `_substitute` first, so `B=$A/y` records what `$A`
    already resolved to, and one that cannot be resolved records the `$` — the
    `EXPANDS` test then catches it at the operand with the unfillable part
    still in the text a prompt can print.

    A name is UNBOUND rather than left alone when the assignment is one this
    reader does not model: `A+=x` appends, `a[0]=x` writes an element, and
    `A=(x)` makes an array whose `$A` is its first element, not the text
    between the parens -- round 1 measured `SB=(/three); git -C "$SB"`
    composing `(/three)` onto the session directory where bash has `/three`.
    An earlier `A=/one` left standing through any of them would answer
    confidently with a path the shell never reaches. That is the single
    failure mode this whole mechanism has, so the unmodelled shapes empty the
    name instead of keeping it.

    Nothing is taken from a segment that also RUNS something. An assignment in
    front of a command is that command's environment and not the shell's --
    measured, `A=1 true; echo "$A"` prints an empty line -- so the shapes this
    reads are exactly the ones `understood` calls "assignments alone", and
    `SB=/x make; git -C "$SB"` keeps the prompt it has today. Where a segment
    is refused, whatever it NAMES is forgotten rather than left: round 1
    measured `export SB=/two` answering `/one`, which is the same confident
    wrong answer the paragraph above refuses for `A+=x`.
    """
    toks, opened = strip_subshell(tokens)
    if opened:
        return _forget(env, tokens)
    assignments = []
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        assignments.append(toks.pop(0))
    if toks:
        # Something else runs here, so this is not the shell's name. Refusing
        # to TAKE it is only half: `export SB=/two` and `declare SB=/two`
        # land in exactly this branch, and an earlier `SB=/one` left standing
        # answers with a path the shell is not in. Measured: `export` gave
        # `/one` where bash has `/two`.
        return _forget(env, tokens)
    while assignments:
        raw, _, value = assignments.pop(0).partition("=")
        name, end = _name_at(raw, 0)
        if name is None:
            continue
        if end == len(raw) and not value.startswith("("):
            env[name] = _substitute(value, env)
        else:
            env.pop(name, None)
    return env


def _expanded(tokens, env):
    """`tokens` with `env` filled into the operands that name a DIRECTORY.

    A `cd` destination and a `git -C` value, and nothing else. Two call sites
    read one of those (`_cd_target`, `parse_git`) and both are reached through
    the token list rather than through a new argument, so every consumer of
    `walk_directories` — both gates and the worktree guard — reads the filled
    operand without being changed.

    The command WORD is deliberately left alone. `CMD=git; $CMD commit` stays
    a word this process cannot read before expansion, which is what
    `understood`'s last line refuses; filling it in here would widen the
    reader by a construct nobody asked for and do it invisibly.
    """
    if not env:
        return tokens
    out = list(tokens)
    shift = 0
    while shift < len(out) and out[shift] in ("(", "((", "{"):
        shift += 1
    body = list(out[shift:])
    if body and body[0].startswith("("):
        body[0] = body[0].lstrip("(")
    # `cd` — the assignment prefix only, which is exactly what `_cd_target`
    # steps past. A wrapper in front of a `cd` is a segment `understood`
    # already refuses, so reading past one here would answer for a shell whose
    # landing place nothing computes.
    at = 0
    while at < len(body) and "=" in body[at] and not body[at].startswith("-"):
        at += 1
    if at < len(body) and body[at] == "cd":
        for k in range(at + 1, len(body)):
            if body[k] not in CD_FLAGS:
                out[shift + k] = _substitute(body[k], env)
        return out
    # `git` — assignments and wrappers both, which is what `parse_git` does.
    at = 0
    while at < len(body):
        tok = body[at]
        if ("=" in tok and not tok.startswith("-")) or os.path.basename(
            tok
        ) in WRAPPERS:
            at += 1
            continue
        break
    if at >= len(body) or os.path.basename(body[at]) != "git":
        return out
    start = at + 1
    _sub_at, chdir_at = _git_options(body[start:])
    for k in chdir_at:
        out[shift + start + k] = _substitute(body[start + k], env)
    return out


# The shell's reserved words. This set is what makes the reader's answer
# honest rather than merely wider: reserved words are a CLOSED, documented
# part of the grammar, while "constructs that move a shell" is the open list
# `specs/1787785858-the-repository-the-command-reaches/plan.md` refused to
# chase. A segment beginning with one of these is a compound command, and
# where its body leaves the shell is not something this reader computes.
RESERVED = frozenset(
    {
        "!",
        "[[",
        "]]",
        "case",
        "coproc",
        "do",
        "done",
        "elif",
        "else",
        "esac",
        "fi",
        "for",
        "function",
        "if",
        "in",
        "select",
        "then",
        "time",
        "until",
        "while",
        "{",
        "}",
    }
)

# Reserved words that open a CONDITIONAL EXPRESSION rather than a scope
# holding commands. Nothing inside `[[ … ]]` is a command, so it cannot leave
# the shell anywhere at all — the same reason `time` and `!` sit with the
# prefixes below. Read as scope openers they stopped
# `[[ -f f.py ]] && git commit`, which was silent at `release/v0.22.0`.
CONDITIONS = frozenset({"[[", "]]"})

# Builtins that relocate the shell, or run text this process cannot see.
# `cd` is deliberately absent: it is the one the reader DOES model, and
# `_cd_target` above is that model.
#
# `alias` and `shopt` are here for a narrower reason than the rest, and it is
# worth writing down because they buy only half a defence. An alias on `cd`
# leaves BOTH words in the command exactly as written — `alias cd='cd <B>'`
# and then `cd <X>` reads as a `cd` to X and lands in B — so this is a
# directory the reader got confidently wrong, not a command it never saw.
# Executed: bash stands in B while the reader answered `['/X', '/S']`, with B
# in neither the candidates nor as unreadable. It leaks only in the
# newline-separated form, because bash does not expand an alias defined
# earlier on the SAME line, and a multi-line command is the shape Claude Code
# sends.
#
# What it does not close: an alias set by `BASH_ENV` or a profile, which never
# appears in the command string at all. This process cannot see it and no
# enumeration reaches it. `shopt` was here for one round on the grounds that
# `expand_aliases` is what turns the feature on in a non-interactive shell,
# and it was taken back out: an alias WRITTEN in the command is caught by the
# line above, one set outside it is caught by nothing, so `shopt` closed no
# door and cost a stop on `shopt -s globstar && git commit` — silent at
# `release/v0.22.0`.
RELOCATORS = frozenset(
    {".", "source", "eval", "exec", "pushd", "popd", "trap", "alias"}
)

# Words that stand in FRONT of another command. The reader reads past them,
# and stops outright when what they wrap is a `cd`: whether the wrapper forks
# is what decides whether that `cd` reaches this shell, and it differs per
# word. Executed: `bash -c 'command cd /tmp; pwd'` prints `/tmp` and
# `bash -c 'sudo cd /tmp; pwd'` does not, because `sudo` looks for a binary.
# Keeping which is which would be one more enumeration, so the pair reads as
# one answer, and it is the stopping one.
#
# `time` and `!` are reserved words that stand in front of a command rather
# than opening a scope, so they belong here and not with the scope openers.
# Read as openers they stopped `time make && git commit` and
# `! grep -q zzz f && git commit`, both ordinary and both silent before.
PREFIXES = frozenset(WRAPPERS | {"builtin", "time", "!"})


def understood(tokens):
    """True when the reader can say where the shell is after this segment.

    This is the inversion that change asked for. The reader used to answer
    "nothing moved" for every construct it did not implement, which is a
    CONFIDENT answer, and it was wrong for five of the seven commands that
    issue measured — a `cd` inside a function body, a sourced script, an
    `eval`, a `pushd`, and a loop each left the shell somewhere the reader
    reported as the session's own directory. That answer is a stop where the
    session's directory needs review and a silence where it is declared, so
    one line of behavior produced both a false positive and the leak.

    What is enumerated here is what the reader UNDERSTANDS. A segment passes
    when it is a simple command — a literal command word and its arguments —
    and `walk_directories` turns everything else into `Unresolved`, which
    `docs/review-chain-spec.md` already treats as a stop rather than a pass.

    The direction of the remaining error is what matters: a construct nobody
    added to `RESERVED` reads as not understood, and stops. The old default
    failed the other way.
    """
    toks, opened = strip_subshell(tokens)
    if opened:
        # `(` and `{` open a scope whose end this reader does not find --
        # `_cd_target` already refused a `cd` inside one for that reason, and
        # this is the same refusal for every other command in there.
        return False
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        toks.pop(0)
    if not toks:
        # Assignments alone, or an empty segment. Neither moves the shell.
        return True
    word = toks[0]
    if (
        word in RESERVED and word not in PREFIXES and word not in CONDITIONS
    ) or word in RELOCATORS:
        return False
    # `f() { cd <path>; }` -- shlex ends a word at neither parenthesis, so the
    # definition arrives as the single token `f()`. The spaced form `f ()`
    # arrives as two.
    if word.endswith("()") or (len(toks) > 1 and toks[1] == "()"):
        return False
    # Read PAST the prefixes and their own options to the word that actually
    # runs. Stopping at the first option read `command -p cd <path>` and
    # `command -- cd <path>` as ordinary commands that moved nothing, and both
    # move this shell -- executed under bash 3.2.57 and `/bin/sh`. `command`
    # and `builtin` are complete under this rule because neither takes an
    # option that consumes the next word; `sudo -u alice cd <path>` still
    # walks through, and `sudo` cannot move the shell anyway.
    at = 0
    while at < len(toks):
        tok = toks[at]
        if os.path.basename(tok) in PREFIXES or (at and tok.startswith("-")):
            at += 1
            continue
        break
    if at >= len(toks):
        # Prefixes with nothing after them. `time` alone moves nothing.
        return True
    if (toks[at] in RESERVED and toks[at] not in CONDITIONS) or toks[at] in RELOCATORS:
        # The refusal the FIRST word met, asked again of the word that runs.
        # `! for SB in /two /three` and `time pushd <x>` put a reserved word
        # or a relocator behind a prefix, and reading only the first word
        # accepted both as simple commands. For a name that was a fail-open:
        # the loop reached `_bind` as something that runs, `_forget` found no
        # `=` in it, and the value from before the loop stood -- measured,
        # `/one` where bash has `/three`. The wide reset hid it by accident,
        # because the `do :` a segment later emptied the environment whole.
        return False
    if toks[at] == "cd":
        # A bare `cd` is the one construct this reader DOES model. Behind a
        # prefix it is the pair above, and unreadable.
        return at == 0
    if toks[at] == "[" or toks[at] in CONDITIONS:
        # A conditional, not a glob. The check below asks whether this process
        # can read the command word before expansion, and here that word IS
        # the conditional -- `EXPANDS` holds `[`, so both `[` and `[[` read as
        # globs and stopped `[ -f f.py ] && git commit` while
        # `test -f f.py && git commit`, the same condition in a third
        # spelling, stayed silent.
        return True
    # A command word this process cannot read before expansion -- `$cmd`, a
    # glob. The same fact that makes a `cd` operand unresolvable, and it is
    # asked of the word that RUNS: `command $C <path>` hid behind the wrapper
    # when only the segment's first token was checked.
    return not any(ch in toks[at] for ch in EXPANDS)


class Unresolved(str):
    """A directory the reader could not identify, carrying the text it read.

    It is a `str` so the prompt can print it — a target that cannot be named
    is one the user cannot go and look at — and it is a distinct type so that
    nothing judges a repository against it by accident. `docs/review-chain-spec.md`
    gives it the treatment an unresolvable `git -C` already had: not silence,
    which is indistinguishable from a repository checked and found clean, but
    a stop in a session whose own repository opted in.

    `why` says which of two things happened, because the way out differs and
    a prompt that offers the wrong one leaves the user with no way out at all.

    - `VALUE` — the command named a destination this process cannot expand,
      `git -C "$WT"` or `cd "$WT"`. The text carried IS that value, and
      writing the path out is a real instruction.
    - `CONSTRUCT` — the command contains something the reader cannot read as
      a simple command, so the shell's location is unknown from there on. The
      text carried is the last directory the reader could name, which is
      usually the session's own. There is no value to replace, so telling the
      user to write the path out is an instruction they cannot follow, and
      the waiver becomes the only way past. Measured: `eval 'cd <T>' && git
      commit` denied with the session's own path named as unresolvable.
    """

    __slots__ = ("why",)

    VALUE = "value"
    CONSTRUCT = "construct"

    def __new__(cls, text, why=VALUE):
        self = super().__new__(cls, text)
        self.why = why
        return self


def strip_subshell(tokens):
    """(tokens, opened) with a leading subshell opener taken off the word.

    A shell ends a word at `(` and `)`; shlex here is told only about `;`, `|`
    and `&`, so `(cd /tmp/x && git commit)` arrives as `(cd` … `commit)` and
    BOTH readers missed it — the `cd` was not a `cd` and the `git` was not a
    `git`. One parenthesis reproduced the whole fail-open this work item
    exists to close.

    Whether the parenthesis is worth reading is a separate question from
    whether the shell moves. It is not added to the splitter's punctuation
    because that changes how every quoted argument in every command tokenizes,
    which is a wider change than the two words it would fix.
    """
    out, opened = list(tokens), False
    while out and out[0] in ("(", "((", "{"):
        out.pop(0)
        opened = True
    if out and out[0].startswith("("):
        out[0] = out[0].lstrip("(")
        opened = True
    return out, opened


def _cd_target(tokens):
    """(kind, operand) when this segment is a `cd`, else None.

    `kind` is "path" when the destination is written out, "home" for a bare
    `cd`, "previous" for `cd -`, and "unknown" when the shell would arrive
    somewhere this process cannot compute.

    A subshell is "unknown" whatever it contains, even though the `cd` inside
    one is now readable: the closing parenthesis decides whether what follows
    runs inside the subshell or after it, and finding that reliably is the
    shell parser this module is not.
    """
    toks, subshell = strip_subshell(tokens)
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        toks.pop(0)
    if not toks or toks[0] != "cd":
        return None
    args = [t for t in toks[1:] if t not in CD_FLAGS]
    operand = args[0] if args else ""
    if subshell or len(args) > 1 or any(ch in operand for ch in EXPANDS):
        return "unknown", operand
    if not args:
        return "home", ""
    if operand == "-":
        return "previous", operand
    if os.path.expanduser(operand).startswith("~"):
        return "unknown", operand
    return "path", operand


def _dedup(states):
    """States in order, keeping a readable directory apart from an unreadable
    one that happens to spell the same path.

    Which branch a shell arrived by is not part of the identity any more: the
    two live in separate lists, so a state cannot be in both at once.
    """
    seen, out = set(), []
    for here, prev in states:
        key = (getattr(here, "why", None), str(here), str(prev))
        if key not in seen:
            seen.add(key)
            out.append((here, prev))
    return out


def _directories(states):
    """The distinct directories in `states`, in order.

    Two shells that arrived at one directory by different routes are one
    candidate, not two: `cd N || cd B` reaches B from both branches and
    differs only in where it came FROM, which nothing downstream asks about.
    Reporting it twice announced one repository as two.
    """
    seen, out = set(), []
    for here, _prev in states:
        key = (getattr(here, "why", None), str(here))
        if key not in seen:
            seen.add(key)
            out.append(here)
    return tuple(out)


def _step(here, operand):
    """`here` after a `cd` to `operand`, as `git -C` would resolve it.

    The same `apply_chdir` a `-C` value goes through, which is what carries
    the Windows path handling: the guard doubles backslashes before the
    splitter sees them and `normpath` (`ntpath` there) collapses what is left,
    and a `cd` argument is the same kind of value arriving the same way.
    """
    landed = apply_chdir(here, [operand])
    if isinstance(here, Unresolved) and not os.path.isabs(os.path.expanduser(operand)):
        return Unresolved(landed, here.why)
    return landed


def _land(here, prev, target):
    """Where a `cd` puts a shell that was in `here`, having come from `prev`."""
    kind, operand = target
    if kind == "unknown":
        return Unresolved(apply_chdir(here, [operand or "."]))
    if kind == "previous":
        # An unreadable `here` makes the shell's HISTORY unreadable too: a
        # segment the reader could not follow may have moved the shell any
        # number of times, so the directory it came from is not the one this
        # reader recorded. Returning `prev` there washed the answer clean --
        # `eval 'cd /A; cd /B' && cd - && git commit` answered the session's
        # own directory with nothing marked unreadable, while bash stood in
        # /A.
        if isinstance(here, Unresolved):
            return Unresolved(str(prev if prev is not None else here), here.why)
        # No previous directory to return to. `cd -` FAILS there and the shell
        # stays put, so the answer is this directory and not a path built out
        # of the operand -- `<cwd>/-` exists nowhere and was reported as a
        # target the user never typed.
        # CONSTRUCT rather than VALUE: the text carried is a directory the
        # reader named ITSELF, so there is no unexpanded value for the user to
        # write out, and offering that is the arm that leaves the waiver as
        # the only way past.
        return prev if prev is not None else Unresolved(str(here), Unresolved.CONSTRUCT)
    if kind == "home":
        return _step(here, "~")
    return _step(here, operand)


def compose(base, chdirs):
    """`apply_chdir`, keeping an unreadable base unreadable.

    A `git -C sub` inside a directory the reader could not identify still
    lands somewhere it cannot identify. An absolute `-C` does not depend on
    where the shell is, so it recovers the answer outright.
    """
    if not chdirs:
        return base
    landed = apply_chdir(base, chdirs)
    if isinstance(base, Unresolved) and not os.path.isabs(
        os.path.expanduser(chdirs[0])
    ):
        return Unresolved(landed, base.why)
    return landed


def walk_directories(items, cwd):
    """[(tokens, wheres)] — the directories each segment may run in.

    `items` comes from `split_segments_with_separators`. `wheres` is a tuple
    because one command can leave the shell in more than one place: after
    `cd X || …`, and equally after `cd X ; …`, the shell is in X if the `cd`
    worked and where it started if it did not, and the gate has to answer for
    both. An `Unresolved` entry is
    a directory that could not be computed at all.

    This is the state the segments used to be independent of. `apply_chdir`
    answers for one invocation and takes nothing from the one before it, so a
    command that walked to another repository first was read as if it had
    stayed put — measured wrong in both directions, and in the one that
    matters it let a routing declaration found in the session's own repository
    silence a commit landing in a repository that never gave that answer.

    What is deliberately NOT implemented is the rest of the shell. Functions,
    `exec`, `trap` and a subshell's scope all resolve to "unknown" rather than
    to a confident guess, because a hook that follows a construct it only half
    understands goes back to being silently wrong. Where every directory a
    command reaches sits in one repository the operator does not matter at
    all, and that is the common `cd src && git commit` — the caller collapses
    those by repository root and the verdict is unchanged.
    """
    # `states` are the shells a segment runs in when everything before it
    # worked. `parked` are the ones a command before it FAILED in — they wait,
    # because only a `||` runs anything from them, and it may be several
    # segments away. Reading just the operator immediately after a segment
    # dropped them: `cd <B> && make || git commit` commits where the shell is
    # when the `cd` fails, and one segment between the two was enough to lose
    # that directory entirely.
    # `env` is the third thread, beside `states` and `parked`: the names this
    # command string has written for itself so far. It is read when an operand
    # is judged and written only by a segment `understood` accepts, so a `cd`
    # and a `$SB` are refused on the same grounds rather than on two.
    # `stack` is the fourth, and it exists because of what the third cannot
    # see on its own. A compound command's body is split on `;` like any other
    # text, so its FIRST statement arrives with the structure word in front of
    # it -- `then SB=/two` -- and is refused, while its SECOND arrives as a
    # segment of its own, indistinguishable from a top-level assignment.
    # `if false; then echo hi; SB=/three; fi; git -C "$SB"` answered `/three`
    # where bash has `/one`, and so did a `while false` body, an empty `for`,
    # a `case` arm that does not match, a function defined and never called,
    # and a subshell -- 80 shapes in one differential run. The wide reset had
    # hidden every one of them by accident: the closer emptied the
    # environment, and a closer carries no name, so the aimed reset keeps it.
    # While a body is open an assignment is FORGOTTEN rather than bound, which
    # is the answer this reader gives for a body it cannot say ran. `_nesting`
    # says what opens and closes one and what its costs are.
    # `defined` is the fifth: the functions this string has defined so far, so
    # that a call to one -- a plain word `understood` accepts -- empties the
    # environment instead of keeping a value the body may have rewritten.
    states, parked, walked, env = [(cwd, None)], [], [], {}
    stack, defined = [], set()
    for index, (joined, tokens) in enumerate(items):
        following = items[index + 1][0] if index + 1 < len(items) else ""
        tokens = _expanded(tokens, env)

        if joined == "||" and parked:
            # Only the failure branch runs a `||`. The live shells skip it —
            # and are still REPORTED, because `cd X || git commit` is judged
            # for X as well as for the directory the shell was in, which is
            # what spec.md S3 pins. What S3 does not ask for is the mirror of
            # that: a failure branch no consumer ever reaches is not reported,
            # which is what keeps `cd <repo> && git commit` costing nothing.
            running, skipped, parked = parked, states, []
        elif joined == ";" and parked:
            # `;` — and a newline, which arrives here as one — runs what
            # follows whether the command before it succeeded or not, so BOTH
            # branches run this segment and neither is skipped. `cd <B> ; git
            # commit` commits in B when the `cd` works and in the directory
            # the shell was already in when it does not, and the reader
            # offered only the first. Executed: `bash -c 'cd /no/such/dir ;
            # pwd'` prints the directory it started in.
            #
            # The two branches merge here rather than staying apart, because
            # past this point nothing tells them apart: each is a live shell
            # whose own failure gets parked again by the segment it runs.
            running, skipped, parked = _dedup(list(states) + list(parked)), [], []
        else:
            running, skipped = states, []

        walked.append((tokens, _directories(running + skipped)))

        target = _cd_target(tokens)
        moved = [
            (here if target is None else _land(here, prev, target), here)
            for here, prev in running
        ]

        # A construct the reader does not understand leaves the shell
        # somewhere it cannot name -- in BOTH directions, because whether such
        # a segment "succeeded" says nothing about whether it moved. A
        # function whose body cds can fail on its last line having already
        # moved the shell.
        known = understood(tokens)
        if not known:
            moved = [
                (Unresolved(str(here), Unresolved.CONSTRUCT), prev)
                for here, prev in moved
            ]

        # Park this segment's own failure, but only while something that
        # CONSUMES one is still coming: with no `||` and no `;` left, nothing
        # would ever run from it and carrying it would double the states for
        # no answer. That is what keeps `cd <repo> && git commit` — the common
        # cross-repository form, and the prompt volume this exists to
        # reduce — answering for the target alone.
        if any(sep in ("||", ";") for sep, _ in items[index + 1 :]):
            failed = (
                running
                if known
                else [(Unresolved(str(h), Unresolved.CONSTRUCT), p) for h, p in running]
            )
            parked = _dedup(parked + list(failed))

        carried = list(moved)
        # A subshell on either side leaves the parent shell where it was. The
        # moved state is kept beside it because a shell can be told to run a
        # pipeline's last stage in the current shell (`shopt -s lastpipe`).
        if joined in SUBSHELL or following in SUBSHELL:
            carried = list(running) + carried
        carried += skipped
        states = _dedup(carried)

        if len(states) + len(parked) > STATE_CAP:
            here, prev = (states or parked)[0]
            # CONSTRUCT when the collapse is what made this unreadable: the
            # command reached more directories than the reader will answer
            # for, and that is not a value anyone can write out either.
            states, parked = (
                [(Unresolved(here, getattr(here, "why", Unresolved.CONSTRUCT)), prev)],
                [],
            )

        # The names this segment leaves behind, for the segments after it.
        # `understood` is the same acceptance test the directory half uses: a
        # construct whose effect on the shell this reader cannot state cannot
        # state its effect on a name either, so an assignment inside a
        # function body, a subshell or a loop never arrives here.
        #
        # A pipeline stage and a background job are excluded on top of that.
        # bash runs each in a subshell, so `A=1 | true; echo $A` prints
        # nothing and the parent's name is untouched — the same fact
        # `SUBSHELL` already carries above, where it keeps the parent shell's
        # DIRECTORY from moving.
        if _runs(tokens) in defined:
            # A call to a function this string defined. `f` is a command word
            # like any other, so `understood` accepts it and `_forget` finds
            # nothing in it to drop -- and the body it runs may have rewritten
            # any name. Round 1 measured `f() { SB=/three; }; SB=/one; f;
            # git -C "$SB"` answering `/one` where bash has `/three`. The
            # reader has seen the definition, so the call empties the
            # environment the way `OPAQUE` does.
            env = {}
        elif joined in ("&&", "||") and known:
            # This segment may not have run at all -- `states` and `parked`
            # model that for the DIRECTORY and nothing models it for a name.
            # Binding it answered `/two` where bash has `/one`, on
            # `SB=/one; [ -d /nope ] && SB=/two; git -C "$SB" commit`, which
            # is an ordinary shape in a script. Forgetting returns the name
            # to `Unresolved`, which is the answer this reader gives for
            # anything it cannot state.
            env = _forget(env, tokens)
        elif known and joined not in SUBSHELL and following not in SUBSHELL:
            # Inside a body -- `stack` above -- the segment is a statement of
            # a compound command whose running this reader cannot state, so it
            # is forgotten the way a `&&` branch is. `_forget` drops every
            # shape `_bind` would have taken or unbound, so nothing a body
            # writes survives it, and nothing it does not write is touched.
            env = _bind(env, tokens) if not stack else _forget(env, tokens)
        elif known:
            # A pipeline stage or a background job -- what is left once the
            # two branches above have taken the joins they name. The comment
            # above says bash runs each in a subshell and leaves the parent's
            # name untouched, and that is why `_bind` may not take one here.
            # It is not why the name is FORGOTTEN: `shopt -s lastpipe` runs a
            # pipeline's last stage in the current shell, so `true |
            # SB=/two` writes the parent's `SB` under a setting this process
            # cannot see, and `SB=/two | true` does not. Which of the two a
            # segment is depends on a shell option, so the answer is the one
            # this reader gives for anything it cannot state.
            #
            # The cost is one prompt on `SB=/one; SB=/two | true; git -C
            # "$SB"`, where bash has `/one`. The other direction is a commit
            # judged against a repository nobody reviewed.
            env = _forget(env, tokens)
        else:
            # A segment `understood` refused. `eval`, a sourced script, a loop
            # body, a conditional's structure words, a subshell. What such a
            # segment did to a name is decided by WHICH of those it is, and
            # `_unseen` is that judgment: the ones reaching text this scan
            # never sees empty the environment, and the ones carrying no name
            # at all leave it standing. Emptying it for every refusal was
            # measured too -- it cost six shapes their answer, `if …; then …
            # fi` among them.
            #
            # A function CALL is not in this branch and never was: `myfunc`
            # is a command word like any other, so `understood` accepts it.
            # Where the definition is in this string, `defined` above empties
            # the environment at the call; the body's own statements arrive
            # here as segments and are forgotten under `stack`, never bound.
            # What remains open is a function or an alias defined OUTSIDE the
            # string -- in a sourced rc file, an earlier tool call -- whose
            # name arrives as an ordinary word this reader has no reason to
            # doubt. That is the same edge `RELOCATORS` records for `alias`,
            # and no reading of this string can close it.
            env = _unseen(env, tokens)
        stack = _nesting(tokens, stack)
        defined |= _definitions(tokens)
    return walked


def _git_options(rest):
    """(index of the subcommand, indices of the `-C` VALUES) within `rest`.

    `rest` is what follows the `git` word. One scan, read twice: `parse_git`
    takes the values and `_expanded` fills their names in beforehand. Written
    twice they would drift about which token a `-C` names, and the two answers
    would then disagree about which repository the command reaches.
    """
    # RIDER: `--git-dir` and `--work-tree` are in this set so the SUBCOMMAND
    # is still found, and their values are then thrown away -- so
    # `git --git-dir=/elsewhere/.git --work-tree=/elsewhere commit` is judged
    # against the shell's cwd by both gates. It is narrower than `-C`, which
    # is what a session driving another repository actually types, and that is
    # why it was left: closing it means `chdirs` stops being one list of
    # composing paths and becomes a resolved (git-dir, work-tree) pair, which
    # `apply_chdir` below cannot express. The rider is here rather than on the
    # guard because this is the file the fix is in.
    # Verified 2026-08-31 at 9829412.
    takes_value = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
    i, chdirs = 0, []
    while i < len(rest):
        t = rest[i]
        if t in takes_value:
            if t == "-C" and i + 1 < len(rest):
                chdirs.append(i + 1)
            i += 2
            continue
        if t.startswith("-") and t != "-":
            i += 1
            continue
        break
    return i, chdirs


def parse_git(tokens):
    """Return (subcommand, args, chdirs) if this segment IS a git invocation.

    `git` must be the segment's command word -- leading VAR=val assignments and
    common wrappers are skipped, anything else (echo, cat, prose) disqualifies
    the segment. Then git's own global options (-C <path>, -c k=v, ...) are
    skipped to find the subcommand.

    `chdirs` are the `-C <path>` values in order. Skipping them was enough to
    FIND the subcommand and not enough to know which repository it acts on,
    which is the whole question the worktree guard answers.
    """
    tokens, _opened = strip_subshell(tokens)
    # RIDER: a reserved word in front of `git` is not read past, so a commit
    # that is the FIRST command in a loop or conditional body is invisible to
    # both gates. `for f in *; do git commit -m x; done` splits into a segment
    # whose tokens are `["do", "git", "commit", …]`, this loop stops at `do`,
    # no invocation is found, and the gate is silent -- executed against the
    # commit gate in an opted-in repository, `do git commit -m x; done`
    # returned nothing at all. It is a fail-OPEN and it is not this branch's:
    # the parser answered `None` for the same tokens before this branch.
    # Left because reading past `do` means deciding where the body LEAVES the
    # shell, which is the whole thing `understood` refuses to guess at -- the
    # segment would still need a directory, and `Unresolved(CONSTRUCT)` is the
    # only honest one. That is a change to what the gate stops, not a parse
    # fix, and it wants its own work item.
    # Verified 2026-08-31 at 9829412.
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if ("=" in t and not t.startswith("-")) or os.path.basename(t) in WRAPPERS:
            i += 1
            continue
        break
    if i >= len(tokens) or os.path.basename(tokens[i]) != "git":
        return None
    rest = tokens[i + 1 :]
    at, chdir_at = _git_options(rest)
    chdirs = [rest[k] for k in chdir_at]
    if at >= len(rest):
        return None
    # A closing parenthesis rides on the last word of the segment, which for
    # `(git commit)` is the SUBCOMMAND: it read as `commit)`, matched nothing,
    # and the gate returned before any of this module's walking was used. The
    # `-m x` form hides it, because the paren attaches to the argument
    # instead. No git subcommand ends in `)`, so taking it off costs nothing;
    # arguments are left alone, where a `)` can be part of a commit message.
    subcommand = rest[at].rstrip(")")
    # `( git )` leaves nothing behind, and the empty string is not a
    # subcommand — this function documents None for that, and a caller
    # testing the result for identity would read `''` as one.
    return (subcommand, rest[at + 1 :], chdirs) if subcommand else None


def apply_chdir(cwd: str, chdirs) -> str:
    """The directory a git invocation actually operates in.

    `git -C <path>` moves git without moving the shell, and repeats compose --
    each value is relative to the one before it. A guard that resolves the
    repository from the session's cwd therefore judges a tree the command
    never touches.

    Measured: `git -C ~/repo switch -c <branch> origin/next` typed from a
    session whose cwd was `$HOME` was denied, because `$HOME` stood in for the
    tree root and every Claude session on the machine sits underneath it.
    """
    base = cwd or os.getcwd()
    for path in chdirs:
        base = os.path.join(base, os.path.expanduser(path))
    return os.path.normpath(base)
