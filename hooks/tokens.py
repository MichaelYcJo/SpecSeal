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
  * **a parenthesis riding on a word is not part of it** --
    `(git worktree add ../wt f [worktree-ok])` (the guard's `has_token`);
  * **an unbalanced quote reads nothing** -- the guard's choice over the
    commit gate's substring fallback, because reading loosely is the
    direction that waives without anybody asking, and here the cost of the
    other direction is one refusal.
"""

import collections
import re
import shlex

KNOWN = ("[no-review]", "[no-parity]", "[worktree-ok]", "[shared-tree-ok]")


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


def given(command):
    """The known tokens `command` carries as bare words, in `KNOWN`'s order."""
    found = {w.strip("()") for w in words(command)}
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
    environment, and a word naming
    `CLAUDECODE` or `CLAUDE_CODE_SESSION_ID` whole -- the last two leave the
    stub no session variable. A command that does not split is read as one of
    them.
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
        # The stub's P2 short-cut reads two session names, so a command that
        # empties, unsets or reassigns either leaves the stub no session where
        # no lease stands: `NAME= git commit`, `env -u NAME`, `env -uNAME`,
        # `env --unset=NAME`, `unset NAME` (round 2 of #692, 🟡 1, executed).
        # 0.16.0's reading stopped each. The name is compared whole, so
        # `$CLAUDECODE` or a message that mentions it is not one.
        name, eq, value = word.strip("()").partition("=")
        session = name
        if name == "--unset":
            session = value
        elif name.startswith("-u"):
            session = name[2:]
        if session in ("CLAUDECODE", "CLAUDE_CODE_SESSION_ID"):
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
    import re

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
    bare = re.sub(r"\\.|'[^']*'|\"(?:\\.|[^\"\\])*\"", "", text)
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


# --- which here-document bodies nothing on the line can run (#739) ----------
#
# The commit gate reads every heredoc body back as shell to ask whether it
# commits, because `bash <<'EOF'` runs its body. The rule below names the few
# shapes where nothing can, the way `is_plain` names a plain command: a
# positive shape, and everything outside it keeps the reading that stops.
# `seal/specs/1791076831-a-here-document-body-is-data-to-the-commit-gate/
# spec.md` §*The rule (R)* is the contract; R2a to R2f below are its clauses.

# The programs such a line may run: the plain ones, a sink, `gh`, and a Python
# program read from stdin.
DATA_PROGRAMS = PLAIN_PROGRAMS | {"tee", "gh", "python3", "python"}

# A body these own is the text of their output (R2e).
SINKS = frozenset({"cat", "tee"})

# A body these own is a Python program, the class `python3 script.py` already
# belongs to: the shell reading of one finds only shell-shaped text (R2e).
STDIN_PROGRAMS = frozenset({"python3", "python"})

# The `gh` subcommands that run no local git, read from `gh <group> <sub>
# --help` at gh 2.100.0 (`questions.md` Q4). Left out, because each runs git
# here and git runs hooks: `pr create` (pushes a branch that is not pushed),
# `pr checkout`, `pr merge` and `pr close` (`--delete-branch` deletes and
# switches the local branch), `issue develop` (`--checkout`), and `release
# create` (it fetches a tag for `--notes-from-tag`). `api` has no subcommand.
GH_REMOTE = {
    "pr": frozenset(
        {"checks", "comment", "diff", "edit", "list", "lock", "ready"}
        | {"reopen", "revert", "review", "status", "unlock", "update-branch", "view"}
    ),
    "issue": frozenset(
        {"close", "comment", "create", "delete", "edit", "list", "lock", "pin"}
        | {"reopen", "status", "transfer", "unlock", "unpin", "view"}
    ),
    "release": frozenset(
        {"delete", "delete-asset", "download", "edit", "list", "upload"}
        | {"verify", "verify-asset", "view"}
    ),
}

# Marks a word that held quoting, which `shlex` would otherwise remove: a
# quoted or escaped program word is no bare literal (R2c).
_QUOTED = "\x01"

_SEPARATORS = ("", ";", "&&", "||")
_REDIRECTIONS = frozenset({"<", ">", ">>", ">|", "<<", "<<<", ">&", "<&"})
_WRITES = frozenset({">", ">>", ">|"})

# A simple command as the rule reads it. `pipeline` numbers the pipeline it
# stands in, so a body is followed to every stage its output reaches.
_Command = collections.namedtuple(
    "_Command", "program args redirections openers pipeline"
)


def _marked(text):
    """`text` with `_QUOTED` in front of every quote or escape that opens
    quoting outside one, read the way `shlex` reads it in POSIX mode."""
    out, quote, i, n = [], None, 0, len(text)
    while i < n:
        ch = text[i]
        if quote == "'":
            quote = None if ch == "'" else quote
            out.append(ch)
            i += 1
        elif quote == '"':
            if ch == "\\":
                out.append(text[i : i + 2])
                i += 2
                continue
            quote = None if ch == '"' else quote
            out.append(ch)
            i += 1
        elif ch == "\\":
            out.append(_QUOTED + text[i : i + 2])
            i += 2
        elif ch in "'\"":
            out.append(_QUOTED + ch)
            quote = ch
            i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _commands(line):
    """The simple commands of `line`, or None when it is not the plain line
    R2c and R2d describe. `line` has its comments and bodies dropped."""
    if _QUOTED in line or "`" in line or steps_around_hooks(line):
        return None
    # A `$` names a parameter and nothing else: `$(`, `${`, `$[`, `$((`,
    # `$'…'` and `$"…"` all fail here, inside quotes or out.
    if re.search(r"\$(?![A-Za-z0-9_])", line):
        return None
    bare = re.sub(r"\\.|'[^']*'|\"(?:\\.|[^\"\\])*\"", "", line)
    if any(ch in bare for ch in "(){}"):
        return None
    lexer = shlex.shlex(_marked(line), posix=True, punctuation_chars=";&|<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        split = list(lexer)
    except ValueError:
        return None
    commands, current, pipeline, k = [], None, 0, 0
    while k < len(split):
        word = split[k]
        k += 1
        if word and set(word) <= set(";&|<>\n"):
            core = word.replace("\n", "")
            if core in _SEPARATORS or core == "|":
                if current is None and core:
                    return None
                if current is not None:
                    commands.append(current)
                current = None
                pipeline += core != "|"
                continue
            if core not in _REDIRECTIONS or current is None:
                return None
            target = split[k] if k < len(split) else ""
            k += 1
            if not target or set(target) <= set(";&|<>\n"):
                return None
            if core.endswith("&") and not (target.isdigit() or target == "-"):
                return None
            if core == "<<":
                # R2d: the opener is on the default descriptor.
                before = (current.args or [current.program])[-1]
                if before.isdigit():
                    return None
                current.openers.append(target.replace(_QUOTED, ""))
            current.redirections.append((core, target.replace(_QUOTED, "")))
            continue
        if current is None:
            if word not in DATA_PROGRAMS:
                return None
            current = _Command(word, [], [], [], pipeline)
            continue
        current.args.append(word.replace(_QUOTED, ""))
    if current is not None:
        commands.append(current)
    return commands if all(map(_plain_on_a_data_line, commands)) else None


def _plain_on_a_data_line(command):
    """R2c for one simple command, past the program word itself.

    It carries every word guard of `is_plain`, so the line stays that
    construction (round 1 of #739): an `--output` option writes a file no
    redirection names (`git diff --no-index --output=<f> -` puts a body
    there), and `printf -v` assigns a variable, `PATH` included.
    """
    program, args = command.program, command.args
    if any(word.startswith("--output") for word in args):
        return False
    if program == "printf" and args and args[0].startswith("-"):
        return False
    if program == "git":
        k = 0
        while k < len(args):
            if args[k] == "-C":
                k += 2
            elif args[k] == "-c":
                key = args[k + 1].partition("=")[0].lower() if k + 1 < len(args) else ""
                if key not in PLAIN_CONFIG:
                    return False
                k += 2
            else:
                return args[k] in PLAIN_GIT
        return False
    if program == "gh":
        return bool(args) and args[0] in ("pr", "issue", "release", "api")
    if program in STDIN_PROGRAMS:
        # R2e's second kind, and the only place a Python program may stand:
        # it owns a body and reads its program from stdin.
        return bool(command.openers) and (not args or args[0] == "-")
    return True


def _runs_what_it_reaches(command):
    """True when `command` can run a file this line wrote (R2f): a Python
    program can, and git runs hooks, which a file the line wrote may be."""
    if command.program in STDIN_PROGRAMS or command.program == "git":
        return True
    if command.program != "gh" or command.args[:1] == ["api"]:
        return False
    remote = GH_REMOTE.get(command.args[0] if command.args else "", ())
    return len(command.args) < 2 or command.args[1] not in remote


def _writes_a_file(command):
    if command.program == "tee" and command.args:
        return True
    return any(op in _WRITES and t != "/dev/null" for op, t in command.redirections)


def heredoc_data(command):
    """One answer per body `cmdline.heredocs(drop_comments(command))` returns:
    True where nothing on the line can run that body, so the commit gate does
    not read it back as commands (#739, `spec.md` R2).

    A body is data when all of these hold, and is read as today otherwise:
      * its delimiter is quoted and its terminator arrived (R2a, R2b);
      * the line, with comments and bodies dropped, is plain in the sense
        above: every program a bare word in `DATA_PROGRAMS`, nothing a shell
        parses again, no `&` but `&&` and a descriptor's, no subshell or
        group, and `steps_around_hooks` finds nothing (R2c);
      * the line's openers are the bodies' openers, one for one, each on the
        default descriptor (R2d);
      * the command owning it is `cat` or `tee`, or `python3` or `python`
        whose first word is `-` or absent (R2e);
      * for a sink, when its pipeline writes a file, nothing on the line can
        run that file (R2f).
    """
    from cmdline import drop_comments, drop_heredoc_bodies, heredocs

    text = drop_comments(command or "")
    records = heredocs(text)
    unread = [False] * len(records)
    commands = _commands(drop_heredoc_bodies(text)) if records else None
    # A body behind an unquoted delimiter is expanded by the outer shell, so
    # no body on its line is data: `cat <<B` holding `$(sh f.sh)` runs the file
    # another body was written to, and a backslash-newline the shell removes
    # first splits the `$(` past any test of the text (rounds 1 and 2 of #739;
    # the owner's structural rule, 2026-10-04).
    if commands is None or not all(r.quoted for r in records):
        return unread
    owners = [(c, word) for c in commands for word in c.openers]
    # The lengths are compared first, so `zip` pairs every opener and record.
    if len(owners) != len(records) or any(
        word != ("-" if r.dashed else "") + r.delimiter
        for (_c, word), r in zip(owners, records)  # noqa: B905
    ):
        return unread
    runs = any(map(_runs_what_it_reaches, commands))
    answers = []
    for (owner, _word), record in zip(owners, records):  # noqa: B905
        data = record.quoted and record.terminated
        data = data and (owner.program in SINKS or owner.program in STDIN_PROGRAMS)
        if data and owner.program in SINKS and runs:
            stages = [c for c in commands if c.pipeline == owner.pipeline]
            data = not any(map(_writes_a_file, stages))
        answers.append(data)
    return answers
