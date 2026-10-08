"""The bare words of a command, read for consent tokens and for the words that
step around git's hooks, and nothing else (#692).

`questions.md` P3, answer (a), keeps the old waiver and answer spellings --
`: '[no-review]'; git commit …` -- working beside the git-native
`git -c specseal.waive=review` form. A shell drops those words before git
runs, so a git hook never sees them; this reads them out of the command and
`hooks/answers.py` hands them to the hook.

It is the one text read the redesign keeps, and its failure direction is why
it may: a token it cannot read costs one refusal naming the git-native
spelling, and a token it reads has exactly the standing tokens always had --
`docs/worktree-guard-spec.md` §*Choice sites* calls it an audit trail, not an
authorization. `steps_around_hooks` fails the same way round: a word it reads
that meant nothing costs one judgment by the reading git's hooks replace.
Nothing here names a directory or decides where an action lands.

The rules are the two consent reads 0.16.0 had, joined:

  * **a bare word, never a substring** -- inside a quoted message it is prose
    (`git commit -m "drop [no-review] later"`), which `has_marker` and
    `has_token` both refused to read as consent;
  * **comments are read** -- the documented form writes the token in one;
  * **a here-document body reads nothing** (#773) -- a waiver is typed in
    front of a command, and a body is text the command only carries, so a
    token inside one silenced a commit nobody waived. `without_bodies` is the
    text a consent read reads, and a token counts only where the command as
    written carries it too, so leaving the bodies out can only refuse. A new
    consent read starts here, and the commit gate's `has_marker` and, since
    #780, the worktree guard's `has_token` already do;
  * **a parenthesis riding on a word is not part of it** --
    `(git worktree add ../wt f [worktree-ok])` (the guard's `has_token`);
  * **a quote that never closes reads nothing from where it opens** -- the
    words read before the split fails are read, and none after it. A word
    inside an unclosed quote is prose a shell would refuse to run, so the
    commit gate's substring fallback, which read it, is gone: reading
    loosely is the direction that waives without anybody asking. The words
    before it are kept because the documented comment form carries an
    English apostrophe after the token often enough to count
    (`# [shared-tree-ok] the release's own tree`): the comment is a comment
    to the shell, which runs the command, and this splitter, which reads
    comments on purpose, reads its apostrophe as a quote. Over the recorded
    runs that kept four of the guard's tokens and read none the base's reads
    did not (work item 1791384157, `phases/phase-1.md`).
    A quote this splitter cannot close is not always one bash refuses, and
    ANSI-C quoting is the known disagreement, in both directions: `$'it\\'s'`
    is one closed word to bash, while shlex closes the quote at `\\'` and
    reads the rest as a quote that never closes. So a waiver typed after
    `git commit -m $'it\\'s'` is refused although bash runs the command, and
    a token inside `echo $'it\\'s [shared-tree-ok] x'` is read although bash
    quotes it, as every base read did too (round 1 of work item 1791384157,
    white 6). The waiver typed in front is the way on in the first.

**This is the one reader of a consent token** (#868). The commit gate's
`has_marker`, the worktree guard's `has_token` and the old spelling handed to
the git hooks (`hooks/answer-write.py`) all answer `token in given(command)`.
"""

import re
import shlex

import hooksession

KNOWN = ("[no-review]", "[no-parity]", "[worktree-ok]", "[shared-tree-ok]")

# A backslash escape, a single-quoted span and a double-quoted span: what a
# text read takes out to see what the shell leaves unquoted. `is_plain` reads
# a subshell or a group through it, and the worktree guard reads a brace
# expansion through it (#856), so the two agree on what a quote is.
QUOTED_SPANS = re.compile(r"\\.|'[^']*'|\"(?:\\.|[^\"\\])*\"")


def words(command):
    """Every bare word of `command`, comments included; () for one that does
    not split."""
    lexer = shlex.shlex(command or "", posix=True, punctuation_chars=";&|<>")
    lexer.commenters = ""
    lexer.whitespace_split = True
    try:
        return tuple(lexer)
    except ValueError:
        return ()


def without_bodies(command):
    """`command` with its here-document bodies taken out and its comments kept:
    the text a consent read reads beside the command as written (#773).

    The bodies are the ones the commit gate already finds, by the two readers
    it already has. Where `hooks/one_heredoc.py` matches the one shape byte
    for byte, its reduced text, which holds no `<<`; everywhere else
    `hooks/cmdline.py#drop_heredoc_bodies`, which copies a comment through and
    opens no body inside one. No reader here decides where a body is.

    It is never read alone. Taking a body out can make a split succeed that
    failed on the raw text, and a token that split reads would be one the
    command as written never offered, so each caller ANDs this read with its
    read of the raw command.
    """
    import one_heredoc
    from cmdline import drop_heredoc_bodies

    command = command or ""
    reduced = one_heredoc.reduce(command)
    return drop_heredoc_bodies(command if reduced is None else reduced)


def _read_words(text):
    """The bare words of TEXT, comments included, up to where its split fails:
    a quote that never closes ends the read, and nothing from inside it is a
    word."""
    lexer = shlex.shlex(text or "", posix=True, punctuation_chars=";&|<>")
    lexer.commenters = ""
    lexer.whitespace_split = True
    read = []
    try:
        for word in lexer:
            read.append(word)
    except ValueError:
        pass
    return read


def _bare(text):
    return {w.strip("()") for w in _read_words(text)}


def given(command, fallback=None):
    """The known tokens `command` carries as bare words outside its
    here-document bodies, in `KNOWN`'s order -- read in the command as written
    AND in `without_bodies`, so a token in a body counts nowhere (#773).

    FALLBACK is the body reader to use where `without_bodies` raises,
    `hooks/cmdline.py` failing to load among the causes. The worktree guard
    hands the frozen reader's `drop_heredoc_bodies`, so a broken wider reader
    still finds the bodies and the single-stream creation deny keeps its way
    past (released row T1 of 0.18.3). It is an argument rather than an import
    because the frozen reader is the guard's and the consent writer's alone
    (`tests/test_the_frozen_reading_never_grows.py`). Without one the error
    propagates, which is the commit gate's direction: a gate that raises is
    reported by `hooks/dispatch.py`."""
    try:
        bodiless = without_bodies(command)
    except (Exception, SystemExit):
        if fallback is None:
            raise
        bodiless = fallback(command or "")
    found = _bare(command) & _bare(bodiless)
    return tuple(t for t in KNOWN if t in found)


def _empties_the_environment(word, after):
    if word.strip("(").rsplit("/", 1)[-1] != "env":
        return False
    return after in ("-", "--ignore-environment") or (
        after.startswith("-") and not after.startswith("--") and "i" in after
    )


def steps_around_hooks(command):
    """True when `command` carries a word that can keep this plugin's git hooks
    from judging it, so the PreToolUse reading must not stand aside for it
    (round 1 of #692, 🟡 2 and 🟡 8; `questions.md` P6's commit half).

    The kinds, each living in the one command where the installer, which runs
    before it, cannot see them: `core.hooksPath` in any spelling (`-c`,
    `--config-env`, `git config`, a `GIT_CONFIG_*` value), a config file that
    can carry it (`include.path`, `includeIf.<condition>.path`, `HOME=`,
    `XDG_CONFIG_HOME=`), any `GIT_CONFIG*` assignment, `env` emptying the
    environment, and a word naming the session variable
    (`hooksession.SESSION_VARIABLE`, `CLAUDE_CODE_SESSION_ID`) whole, which
    leaves the stub no session variable. `CLAUDECODE` left the list with
    #868, because the stub no longer reads it. A command that does not split
    is read as one of them.
    The direction is the refusal's: a word read here that meant nothing costs
    the reading's judgment of one command, which is 0.16.0's.
    """
    split = words(command)
    if not split:
        return bool((command or "").strip())
    for i, word in enumerate(split):
        if "hookspath" in word.lower():
            return True
        if word.lstrip("(").startswith("GIT_CONFIG") and "=" in word:
            return True
        after = split[i + 1] if i + 1 < len(split) else ""
        if _empties_the_environment(word, after):
            return True
        # The stub's P2 short-cut reads one session name, so a command that
        # empties, unsets or reassigns it leaves the stub no session where no
        # lease stands: `NAME= git commit`, `env -u NAME`, `env -uNAME`,
        # `env --unset=NAME`, `unset NAME` (round 2 of #692, 🟡 1, executed).
        # 0.16.0's reading stopped each. The name is compared whole, so
        # `$CLAUDE_CODE_SESSION_ID` or a message that mentions it is not one.
        name, eq, value = word.strip("()").partition("=")
        session = name
        if name == "--unset":
            session = value
        elif name.startswith("-u"):
            session = name[2:]
        if session == hooksession.SESSION_VARIABLE:
            return True
        # A config file the command names can carry core.hooksPath where no
        # word does: `include.path` or `includeIf.<condition>.path`, set by
        # `-c`, `--config-env` or `git config`, and HOME or XDG_CONFIG_HOME
        # pointing git at another global config (round 2 of #692, 🟡 2,
        # executed). 0.16.0's reading stopped each. The key and the name are
        # compared whole, so `$HOME/x` as an argument is not one.
        key = value.partition("=")[0] if name == "--config-env" else name
        key = key.lower()
        if key == "include.path" or key.startswith("includeif."):
            return True
        if eq and name in ("HOME", "XDG_CONFIG_HOME"):
            return True
    return False


# The programs a plain command may run, measured rather than guessed: the
# program word of every simple command in the 2,337 distinct Bash commands
# that ran `git … commit` across this repository's 478 recorded transcripts
# (2026-10-02, round 3's fix pass of #692). Kept are the ones that run no
# other program, change no environment and write no file by themselves:
# echo 1393, cd 785, grep 560, tail 511, cat 322, head 235, cut 156, wc 64,
# `:` 35, printf 22, `[` 8, and `true` and `test`, which cost nothing.
PLAIN_PROGRAMS = frozenset(
    {"git", "cd", "true", ":", "echo", "printf", "test", "["}
    | {"cat", "head", "tail", "grep", "wc", "cut"}
)

# The git subcommands a plain command may run, from the same count: commit
# 2023, add 1449, log 1243, rev-parse 337, status 330, diff 92, show 48.
PLAIN_GIT = frozenset({"commit", "add", "log", "rev-parse", "status", "diff", "show"})

# The keys a plain `git -c` may set, from the same count (commit.gpgsign 40,
# user.email 9, user.name 4) and the plugin's own git-native answers.
PLAIN_CONFIG = frozenset(
    {"commit.gpgsign", "user.email", "user.name", "specseal.waive", "specseal.answer"}
)


def is_plain(command):
    """True only when `command`'s shape is known plain, which is the one case
    the PreToolUse reading stands aside for in a clone where git decides
    (`questions.md` P7, the owner's answer of 2026-10-02).

    The rule is positive on purpose. Three review rounds of #692 each found
    spellings a list of hook-bypassing words missed, so the condition was
    flipped: instead of judging only what a list names, the reading judges
    everything except a shape this function recognises. Anything it does not
    recognise gets 0.16.0's reading, and a misread costs one refusal (P6).

    Plain means all of:
      * it splits, comments and quoted heredoc bodies aside;
      * every simple command's program is a bare word in `PLAIN_PROGRAMS`,
        and no assignment stands in a program's place;
      * a `git` passes only `-C <dir>` and `-c <key>=…` with a key in
        `PLAIN_CONFIG` before a subcommand in `PLAIN_GIT`;
      * no word is an `--output` option, which writes a file;
      * a `printf` takes no option, since `-v` assigns a variable;
      * output is redirected only to `/dev/null` or to another descriptor;
      * nothing re-parses: no `$( … )`, backtick or process substitution, no
        `( … )` or `{ … }`, no `${ … = … }`, and no heredoc body holding a
        substitution behind an unquoted delimiter;
      * `steps_around_hooks` finds none of its words.
    """
    from cmdline import (
        drop_comments,
        drop_heredoc_bodies,
        heredoc_bodies,
        substitution_bodies,
    )

    if not (command or "").strip() or steps_around_hooks(command):
        return False
    text = drop_heredoc_bodies(drop_comments(command))
    if substitution_bodies(text):
        return False
    # A subshell, a group or a function body, outside every quoted span.
    bare = QUOTED_SPANS.sub("", text)
    if any(ch in bare for ch in "(){}"):
        return False
    if any("$(" in b or "`" in b for b in heredoc_bodies(drop_comments(command))):
        markers = re.findall(r"(?<!<)<<(?!<)-?[ \t]*(\S)", text)
        if not markers or any(m not in "'\"\\" for m in markers):
            return False
    lexer = shlex.shlex(text, posix=True, punctuation_chars=";&|<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        split = list(lexer)
    except ValueError:
        return False
    program, git_at, k = None, None, 0
    while k < len(split):
        word = split[k]
        k += 1
        if set(word) <= set(";&|\n"):
            if git_at is not None:
                return False
            program = None
            continue
        if set(word) <= set("<>&|"):
            # Every redirection takes the next word: a file, a descriptor or
            # a heredoc's delimiter. Output goes to /dev/null or a descriptor.
            target = split[k] if k < len(split) else ""
            k += 1
            if ">" in word:
                if word.endswith("&"):
                    if not (target.isdigit() or target == "-"):
                        return False
                elif target != "/dev/null":
                    return False
            continue
        if re.search(r"\$\{[^}]*=", word):
            return False
        if program is None:
            if word not in PLAIN_PROGRAMS:
                return False
            program, git_at = word, (k if word == "git" else None)
            if word == "printf" and k < len(split) and split[k].startswith("-"):
                return False
            continue
        if word.startswith("--output"):
            return False
        if git_at is None:
            continue
        if word == "-C":
            k += 1
        elif word == "-c":
            key = split[k].partition("=")[0].lower() if k < len(split) else ""
            if key not in PLAIN_CONFIG:
                return False
            k += 1
        elif word in PLAIN_GIT:
            git_at = None
        else:
            return False
    return git_at is None
