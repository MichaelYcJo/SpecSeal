#!/usr/bin/env python3
"""PreToolUse guard: keep worktrees tied to genuinely CONCURRENT work.

Reads the Claude Code hook JSON on stdin and guards both directions of the same
rule, using one signal -- how many work streams are actually live on this tree.

A) Branch switching (Bash: `git switch`, and every git shape not known to
   leave the branch where it is)

  Each git segment is one of three shapes, read from the frozen reading's
  words alone (#826): LISTED -- its subcommand is in `LEAVES_THE_TREE`, or it
  is a `checkout` with a path after `--` -- which is silent in every tree and
  spawns nothing; a `git switch`, which takes the rows below; and
  UNRECOGNISED, every other git (a `checkout` without `-- <path>`, an
  unlisted subcommand, git in a string handed to a shell, in a substitution
  body whose git is not all listed, behind a redirection or a zsh precommand
  word, or in a command that would not tokenize). An unrecognised shape stops
  only where one of the first four rows below would speak: a `deny` to the
  model naming the plain spelling where the person pressed `automation` or
  another session is ACTIVE, an `ask` otherwise (`stop_unrecognised`).

  - ACTIVE Claude session inside THIS working tree -> deny, steer to a worktree
  - only IDLE sessions (no terminal input for a while) -> CHOICE: switch here,
    or split into a worktree -- they are usually forgotten tabs, and the user
    can tell
  - cannot tell (process inspection unusable)       -> the same CHOICE
  - tracked changes present (dirty)                 -> ask the user first; this
    one really is yes/no (the branch is the same either way, and the only
    question is whether the uncommitted changes ride along)
  - otherwise (single work stream, clean)           -> allow the plain switch

  A command that also creates a worktree is judged by these rows, whichever of
  the two is written first, and the creation is judged where they would let the
  command run (docs/worktree-guard-spec.md §Creation consent).

B) Worktree creation, whichever path it takes:
     - Bash: `git worktree add ...`
     - Agent/Task tool with `isolation: "worktree"` (harness-managed, lands in
       `<repo>/.claude/worktrees/<name>` and never goes through Bash)

  - consent: this session already created one in this clone, or its person
    pressed `automation` on the routing question    -> allow (Bash, where the
    command is worktree creation and nothing else), silent (Bash, where it
    does more, and Agent/Task). Read FIRST, above every row below it:
    each of them asks something a person has already answered. The record is
    written by hooks/worktree_consent.py AFTER a creation ran, and the routing
    answer by the harness from the person's click, which is why both are
    evidence where `[worktree-ok]` is not -- that file holds the whole
    argument, and the budget they buy is one prompt per SESSION rather than
    one per worktree, and none for a session whose person pressed `automation`
  - another Claude session inside THIS working tree -> ask (concurrent:
    justified; declining leads only to "use that session's worktree or wait",
    which is not a command this session issues, so there is no choice to offer)
  - cannot tell                                     -> CHOICE: create it, or
    switch in the shared tree
  - `[worktree-ok]` given                           -> ask. NOT a choice: the
    token is what a completed confirmation looks like coming back through the
    guard, and declining it withdraws the token, which is the other way on.
    Still true, and still not consent for the NEXT creation: the token is
    written before the question and the record after the answer
  - otherwise (single work stream)                  -> deny, steer to `git switch`

  The rows after the consent row are the Bash path's. The Agent/Task path
  counts no sessions: the agent runs beside this session, so the call is
  concurrent work by construction, and a subagent has no session id the count
  could see. It is silent under consent and asks once otherwise (#8).

CHOICE sites: a hook decision renders as approve/decline and the model never
gets the turn, so where declining has TWO destinations the user sees neither
and has to retype the command they wanted. Those sites deny instead, and spend
the reason on an AskUserQuestion instruction naming both -- the shape measured
in hooks/review-skill-gate.py. Once per session per DIRECTION
(<git-dir>/specseal-worktree-choice/{create,switch}/<session-id>); every
attempt after that gets the decision the site made before, so a session with
nobody to answer (headless) pays one extra round trip and then behaves as it
always did. Direction, not site: within one direction the sites are mutually
exclusive on tree state, while one budget for the whole guard let a creation
question spend the answer a later switch needed.

Creation consent is a SECOND session-scoped record and deliberately not part
of that budget: `<git-common-dir>/specseal-worktree-consent/<session-id>`,
written only by hooks/worktree_consent.py on PostToolUse. The choice marker
above says "the question was put" and is written before the answer; this one
says "a creation ran" and is written after it, so one file could not carry
both without the guard reading its own question back as consent. They also
fail in opposite directions -- an unwritable choice marker counts as already
asked, an unwritable consent record counts as no consent.

Retry tokens, one per direction, both matched as BARE WORDS of the command
(has_token) -- a substring test read `echo 'we documented [shared-tree-ok]'`
as consent and turned the guard off -- and never inside a heredoc body, which
is text a command only carries (#780). `[worktree-ok]` carries the creation
answer (that site asks -- creating a worktree always takes one confirmation)
and `[shared-tree-ok]` carries the shared-tree answer, which passes the switch
straight through at the two cannot-tell sites. `[shared-tree-ok]` is ignored
where another session is ACTIVE, and where the tree is dirty: neither is the
question it answers.

Session activity: a session counts as ACTIVE when, within
WORKTREE_GUARD_IDLE_MIN minutes (default 5; env-overridable), EITHER its
terminal saw input or output OR its project's transcript files
(session .jsonl files and session subdirs incl. background-agent
transcripts, excluding this session's own) were written. The transcript signal is what makes 5 minutes safe: an autonomous
turn types nothing for long stretches but writes its transcript every few
seconds, while a forgotten tab goes quiet on both signals. Sessions where
neither signal can be read are conservatively treated as active.

Command matching: only segments whose FIRST word (after env assignments and
wrappers like `command`/`nohup`) is `git` are classified. Mentions of
"git switch" inside echo arguments or heredoc prose no longer trigger the
guard -- including a heredoc line that IS exactly a git command, which was a
residual here until the judgment read learned to drop heredoc bodies the way
it already dropped comments (`_judgment_text` below).

Note: sessions living in a linked worktree are already isolated and are NOT
counted -- switching the shared tree cannot affect them. `git checkout --
<path>` (with or without a name before the `--`) and `git restore` are always
allowed, as is every non-`add` worktree subcommand (`list`, `remove`,
`prune`). A `git checkout <name>` is no longer looked up to tell a branch from
a file: it is unrecognised, and its stop names `git switch` and `git checkout
-- <path>`, which the model can tell apart and the guard could not (#826).
"""

import json
import os
import re
import shlex
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reading a command line is neither gate's property; `hooks/cmdline.py` owns
# it. A plain filename means `sys.modules` deduplicates the import, which is
# what the two gates loading each other by path could not do — see that
# module's docstring for the 496 executions per hook event it cost.
#
# This guard reads through `hooks/cmdline_base.py`, the reader frozen at
# `86256492`, and never chooses a segment or a tree through `cmdline.py` (#689;
# the one question about kinds it asks that module is below, and `has_token`
# has it take heredoc bodies out, #780): the splitter, `parse_git`,
# `adds_a_worktree`, the walk and `Unresolved` all come from there, so what it
# recognises and where it judges are the release base's by construction.
# Since #826 nothing is read past the base's words: a segment is listed, a
# switch, a creation or unrecognised by its subcommand and, for `checkout`,
# `worktree` and `stash`, the word that decides it (`shape_of`). The name
# `cmdline` is kept so the rest of this file reads as it did.
# `worktree_consent` imports the same module, so the two share one `Unresolved`.
import cmdline_base as cmdline
import console

# The commit gate's wider reader, under a name of its own so the binding above
# keeps meaning the frozen one. Since #826 it reads what the frozen reading
# does not: the string a shell is handed, an `eval`'s argument, a substitution
# body, and a git behind a redirection or a zsh precommand word (`shape_of`,
# `_command_findings`). It never takes the first slot (#689), and it names a
# tree in one place: the `-C` of a git only it reads, composed onto the
# directory the frozen walk placed that segment in (`_finding_tree`). A
# string handed to a shell is not read for one. The import is guarded because
# this guard's own rows do not need it:
# a broken `hooks/cmdline.py` must not take the ACTIVE deny down with the
# commit gate, so where it fails to load the bare word `git` in such a place
# is the finding (`_BARE_GIT`) -- a broken reader costs a stop where the tree
# matters, never a silence -- and the commit gate's own failure still names
# the module.
# `SystemExit` beside `Exception`, as `hooks/dispatch.py` catches a module
# body that exits (round 1 of 1790993140, white 5).
try:
    import cmdline as wide
except (Exception, SystemExit):
    wide = None

# The one consent-token reader, shared with the commit gate (#773, #780,
# #868): `has_token` is `tokens.given`, and the brace reading takes its quoted
# spans (#856). Guarded like the import above, because this guard's rows do
# not need it: where it cannot load, no token is read and every brace reads
# as unquoted, each costing a prompt and never a silence.
try:
    import tokens
except (Exception, SystemExit):
    tokens = None

# The AFTER half of this guard: it owns the consent record, and this file reads
# it. A plain filename again -- and the reason that file's name carries an
# underscore where every other gate here carries a hyphen.
#
# `hooksession` beside it: which process is a Claude session is one test,
# `hooksession.is_claude`, shared with the lease writer and the commit gate's
# lease route (#868).
import hooksession
import worktree_consent
from cmdline_base import apply_chdir, parse_git


def _idle_min():
    """A typo in the override must not disable the guard: an unparseable or
    non-positive value falls back to the default rather than raising at
    import time, where the crash would read as a silent allow."""
    try:
        v = int(os.environ.get("WORKTREE_GUARD_IDLE_MIN", "5"))
    except ValueError:
        return 5
    return v if v > 0 else 5


IDLE_MIN = _idle_min()


def _lang():
    """SPECSEAL_LANG wins; otherwise the system locale; default English."""
    v = os.environ.get("SPECSEAL_LANG", "")
    if v:
        return "ko" if v.lower().startswith("ko") else "en"
    sys_locale = os.environ.get("LC_ALL") or os.environ.get("LANG") or ""
    return "ko" if sys_locale.lower().startswith("ko") else "en"


LANG = _lang()


def tr(en, ko):
    return ko if LANG == "ko" else en


# One marker file per session per repository. Empty; its existence is the fact.
CHOICE_DIR = "specseal-worktree-choice"


def load_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


# The tokenizing adapter and the placement live in `hooks/worktree_consent.py`
# since #868, beside the consent writer that reads the same command, so the
# directory a creation is filed under is the one this guard judged.
_tokenize_with_separators = worktree_consent.split_with_separators
segment_cwd = worktree_consent.segment_cwd


def _tokenize(command: str, windows=None):
    """The same read, without the operators — `(segments, parsed_cleanly)`."""
    items, clean = _tokenize_with_separators(command, windows)
    return [tokens for _, tokens in items], clean


def _judgment_text(command: str) -> str:
    """The command with everything the shell will not EXECUTE taken out.

    Comments and heredoc bodies are both data, and a judgment read drops both
    for the same reason. The residual this file used to record — "a heredoc
    line that IS exactly a git command still matches" — is what the second one
    closes. A CONSENT read keeps the comments, because a retry token is
    written in a comment on purpose: `parses_cleanly` reads the command as
    written, and `has_token` reads it both as written and with its heredoc
    bodies taken out (#780), so a token counts only outside a body.
    """
    return cmdline.drop_heredoc_bodies(cmdline.drop_comments(command))


def walk_command(command: str, cwd: str, windows=None):
    """[(tokens, wheres)] — each segment to JUDGE, and where the shell is in it.

    `split_command` answers what the segments are; this answers where each one
    runs, which the guard used to take from the session's `cwd` for all of
    them. A `cd` in front of a `git switch` therefore moved the shell and not
    the verdict — and this guard is the reason a session is in that shape at
    all: it refuses a switch and tells the user to work in a separate
    worktree, so the session stays where it was while the commands do not.

    `wheres` can hold more than one directory (a `||` leaves the shell in two
    possible places) and can hold one the reader could not compute. The caller
    decides what to do with that; see `main`.

    The walk is `hooks/cmdline_base.py`'s, the reader frozen at `86256492`,
    and never the commit gate's wider one (#689). `main` judges the first
    switch and the first creation, each in the first directory of its
    segment, so both which segments are git and the order of their
    directories pick the tree, and every way of ordering the wider reading
    for this guard met a new command. An unrecognised shape is judged in its
    own segment's tree (#826). The cost is that a `cd` behind a redirection (`2>/dev/null
    cd W`) does not move the tree judged here, and a git behind one
    (`2>/dev/null git switch x`) is not read as git, both as at `86256492`,
    while the commit gate reads both. Since #826 the second is an
    unrecognised shape (`shape_of`), stopped where the tree matters; the
    first stays a known limit (#686).
    """
    items, _clean = _tokenize_with_separators(_judgment_text(command), windows)
    return cmdline.walk_directories(items, cwd)


# RIDER: no production caller reaches this any more. `main` reads the command
# through `walk_command` above, which needs the operator between segments and
# the directory each one runs in; this returns the segments alone. Sixteen test
# call sites still target it, and they are targeting the tokenization seam
# rather than this function, so deleting it means rewriting them onto
# `walk_command` and deciding whether a tokenization-only entry point is worth
# keeping for tests. Left because that is a judgment about the test surface,
# not a cleanup.
# Verified 2026-08-31 against split_command@7e3ba403.
def split_command(command: str, windows=None):
    """The segments to JUDGE: comments dropped, quoting respected.

    Returns `(segments, parsed_cleanly)`; each segment is a list of tokens.
    `parsed_cleanly` here is the lexer's verdict on the comment-free text, so
    it answers "could this be classified" and NOT "was a retry token
    readable" -- `parses_cleanly` below answers that one, from the original.

    The splitter is `hooks/cmdline.py`, owned by neither gate. This guard
    learned the answer the expensive way twice: a regex that cut on `;` and
    `|` inside quotes as well turned `echo "step 1; git switch feature/x"`
    into a branch switch and denied an ordinary commit, and the same cut hid a
    `[worktree-ok]` the user really had given, at the one verdict with no
    `ask` behind it. The splitter it moved to had the same shape as the commit
    gate's because it WAS the commit gate's, loaded from it -- which put the
    two gates in a mutual import that ran their module bodies 496 times per
    hook event once both halves met on one branch (measured). A neutral module
    ends that.

    Comments are dropped because a shell drops them. The splitter clears
    `commenters` so a `[worktree-ok]` written in one stays readable, and the
    price of that is an apostrophe in a comment reading as an opening quote:
    `git status  # don't forget` on the first line swallowed every line after
    it, and the `git worktree add` on line two got no verdict at all while
    bash ran it. `cmdline.drop_comments` is quote-aware and word-aware -- `git
    switch feat#1` keeps its branch name.
    """
    return _tokenize(_judgment_text(command), windows)


def parses_cleanly(command: str, windows=None) -> bool:
    """Whether the lexer got through the command AS THE USER WROTE IT.

    Read from the original text, comments and all, because the one place this
    is consulted asks whether a retry token could have been READ -- and
    `has_token` reads the original, beside its body-free text. Asking the
    comment-free text instead would put "this command has an unbalanced
    quote" on commands whose only unbalanced quote was in a comment that no
    longer matters.
    """
    return _tokenize(command, windows)[1]


def has_token(command: str, token: str) -> bool:
    """True when `token` appears as a BARE WORD of the command.

    A substring test cannot tell a waiver from a sentence about one. Measured:
    `git switch x && echo 'we documented [shared-tree-ok] today'` carried the
    token as prose and turned the guard off outright. The commit gate learned
    this about `[no-review]`, and it costs more here — that marker skips one
    check the user is being asked about anyway, while `[shared-tree-ok]`
    silences the guard.

    The splitter keeps a quoted string whole, so that sentence arrives as
    ONE token and no bare-word comparison matches it. Unquoted prose is a
    different matter and still passes — measured:
    `git switch x && echo the [shared-tree-ok] token is documented` goes
    silent. Shell prose is usually quoted, so the residual is narrow, but it
    is a residual and not a property.

    **No substring fallback for a command that does not parse cleanly**: a
    quote that never closes ends the read, and nothing inside it is a word.
    Measured: `git worktree add ../wt f && echo "we agreed on [worktree-ok]
    yesterday` carries the token as a substring and gives no consent. Since
    #868 the commit gate's `has_marker` reads the same way.

    **Comments are NOT dropped here**, and that is the one way this read
    differs from the judgment read `split_command` does. A retry token is
    written in a comment on purpose — `git worktree add ../wt f
    # [worktree-ok]` is the documented form — so dropping comments first would
    throw away the only place the token is ever written. A parenthesis riding
    on a word is not part of it, so `(git worktree add ../wt f
    [worktree-ok])` carries the token: creation is the one verdict in this
    guard with no `ask` behind it, which turns an unreadable token into a loop
    with no way out.

    **A here-document body is not read** (#780). A token counts only where
    the command as written AND the command with its bodies taken out both
    carry it. A body is text a command only carries, so a `[shared-tree-ok]`
    written in one passed a switch nobody answered, and a `[worktree-ok]`
    there lowered the single-stream deny to an ask.

    Every one of those rules is `hooks/tokens.py#given`'s, the one reader of
    a consent token (#868): this guard, the commit gate and the old spelling
    handed to the git hooks split a command one way. Where `hooks/cmdline.py`
    cannot load, or the body read raises for any other reason, the frozen
    reader's `drop_heredoc_bodies` finds the bodies instead, handed to
    `given` as its fallback: falling back to the command as written would
    bring #780 back whenever that module is broken, and reading no token at
    all would leave the single-stream creation deny with no way past (`plan.md`
    G and H of work item 1791163981). Where `hooks/tokens.py` itself did not
    load, no token is read, and the cost is the prompt the token would have
    spared.
    """
    if tokens is None:
        return False
    return token in tokens.given(command, cmdline.drop_heredoc_bodies)


# The characters that make ONE segment do something besides run its command
# word. The splitter has already taken `;`, `|`, `&` and the newline apart into
# segments of their own, and `cmdline.understood` refuses a subshell, a brace
# group, an `eval` and the reserved words, so what is left inside a single
# segment is these four:
#
#   `$`   a parameter expansion, or a command substitution the shell runs
#         BEFORE git is invoked. Executed: `git worktree add ../wt f $(touch
#         <marker>)` created the marker under an `allow` that covered the whole
#         tool call.
#   `` ` ``  the older spelling of that substitution.
#   `>`   a redirection writing a file the allow was never about. Executed:
#         `git worktree add ../wt f > <file>` left a file that held
#         `important` holding `''`. `2>`, `>>` and `&>` all carry this
#         character, so one test covers the family.
#   `<`   the input side, the `<<EOF` whose body the judgment read discards,
#         and `<(…)` process substitution, which runs a command.
#
# A glob and a `~` are deliberately absent. Both expand and neither runs
# anything, and a `~` is the form a person is most likely to type for a
# worktree path -- refusing it would spend a prompt on the common case to buy
# nothing. A glob or a `~` in the COMMAND WORD is refused one line below
# instead, where `git` has to be the word itself. That sentence was written
# while the line below compared BASENAMES, which made it false: executed,
# `*/git worktree add …` and `~/git worktree add …` both answered `allow`.
ELSEWHERE = "$`<>"


def only_creates_a_worktree(command: str, cwd: str, windows=None) -> bool:
    """True when EVERY segment of `command` is a `git worktree add`.

    The bound on the allow, and the reason there is one.
    `permissionDecision: "allow"` bypasses the user's own permission settings
    for the WHOLE tool call, and a creation is routinely written as one segment
    of a compound. What consent establishes -- the record, or the person's
    `automation` answer -- is that this session may create worktrees, so the
    guard may speak for a command that is worktree creation and nothing else;
    for anything more it stays silent, which leaves the rest of the command
    line to the harness's own permission flow rather than denying the
    worktree.

    A command the lexer gave up on is not vouched for either -- what it could
    not read is exactly what the allow would be covering. That is the opposite
    call from `has_token`, which widens on an unreadable command, and the
    asymmetry is the same one that file states: widening a CONSENT read costs
    one prompt, widening a permission decision costs whatever else was on the
    line.

    Judged from `walk_command`, so a creation written inside a quoted string or
    a heredoc body is read here the way the guard already reads it -- neither
    is executed, so neither makes a command anything but what its real segments
    say.

    **A segment is more than its command word, and asking only "is this a
    creation" was not the bound this docstring claims.** Executed at `d82a02c`,
    with a consent record present, eleven shapes answered `allow` -- a command
    substitution, backticks, `>`, `>>`, `<`, a subshell, a heredoc, `sudo`,
    `env VAR=…`, a bare `VAR=…` and a trailing `&`. Two of them were run in a
    real shell and did what the shell says they do: the substitution created
    its marker and the redirection truncated a file. So the two tests below are
    the bound:

      1. the segment's command word is the WORD `git` -- not a path whose last
         component is spelled that way. `cmdline.parse_git` reads PAST
         `WRAPPERS` and leading `VAR=val` on purpose: the question IT answers
         is "is this a git invocation", and this one is "is this nothing but a
         creation". `sudo git worktree add …` is not, and a user's own
         `permissions.deny` on `Bash(sudo:*)` must not be spoken over by a
         hook that was reasoning about worktrees.

         **`os.path.basename` was this test and a basename is not an
         identity.** Executed at `62b2d2e` with a consent record present:
         `./git`, `../git`, `bin/git`, `/tmp/evil/git`, `~/git` and `*/git`
         all answered `allow`, which covers the whole tool call -- so a
         session that had ONE creation approved could then run any executable
         on the machine by giving it a filename of `git`. The reason this test
         exists does not stop at `sudo`: a hook must not sign for a binary it
         did not identify.

         So the test is exact equality, and the boundary it draws is *a
         command word carrying no separator, resolved on `PATH` the way the
         shell resolves it*. Anything with a `/` in it names a FILE rather
         than the command, and this function cannot tell whose file it is.
         `\\git` and `'git'` still pass -- the lexer hands both back as the
         word `git`, and both run exactly what `git` runs. `GIT` does not, and
         `git/` does not.

         What it costs is the allow on `/usr/bin/git worktree add …`, which is
         a legitimate command a person may type. With consent the guard is
         silent there, not asking -- the caller passes `silent` for anything
         this refuses -- so the user's own permission settings decide it.
         That is the trade this whole docstring already makes for `$` and
         `>`: a wrong silence leaves the call to the user's settings, a wrong
         allow signs for an arbitrary binary.
         `test_the_command_word_class_is_what_the_allow_covers` pins members
         of each verdict group.
      2. no `ELSEWHERE` character in any token, which is the expansion and
         redirection family the first test does not reach.

    `cmdline.understood` and an `Unresolved` in `wheres` were in this loop and
    are not, because a check nothing can make false is a check no case can pin
    -- the rule `guard_worktree_creation` states about its own missing
    `session_id and`. Mutation-tested one at a time: deleting either left every
    case green, while deleting the command-word test or `ELSEWHERE` turned one
    red. Test 1 subsumes them and is strictly stronger than `understood` --
    executed, `understood` answers True for `time git worktree add ../wt f`
    (`time` is a prefix it reads past) where test 1 answers False; a subshell
    arrives as the token `(git`, which is not `git`; and `Unresolved` cannot
    occur at all, because a segment that would produce one is not a creation
    and fails `adds_a_worktree` first.

    A lone trailing `&` is the one shape from that list left allowed, and it is
    a decision rather than an oversight: it backgrounds the creation and runs
    nothing else, so it is inside this docstring's bound. `git worktree add …
    & rm -rf <path>` is two segments and the second one fails the very first
    test.
    """
    if not parses_cleanly(command, windows):
        return False
    seen = False
    for tokens, _wheres in walk_command(command, cwd, windows):
        if not tokens:
            continue
        if not cmdline.adds_a_worktree(tokens):
            return False
        if tokens[0] != "git":
            return False
        if any(ch in tok for tok in tokens for ch in ELSEWHERE):
            return False
        seen = True
    return seen


def ancestors(pid: int):
    """Pids of this process and everything above it (so we never count ourselves)."""
    seen = {pid}
    cur = pid
    for _ in range(20):
        try:
            r = subprocess.run(
                ["ps", "-o", "ppid=", "-p", str(cur)],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            ppid = int(r.stdout.strip())
        except Exception:
            break
        if ppid <= 1:
            break
        seen.add(ppid)
        cur = ppid
    return seen


def proc_cwd(pid: int):
    """Working directory of another process, or None if it cannot be read.

    /proc first: it is free, and lsof is not installed by default on server
    and container Linux — where its absence used to make every other session
    invisible, which is the fail-open direction (the guard then reports a
    single stream and allows a switch that yanks someone else's branch).
    lsof remains the path on macOS, which has no /proc.
    """
    try:
        return os.readlink(f"/proc/{pid}/cwd")
    except OSError:
        pass
    try:
        r = subprocess.run(
            ["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        for line in r.stdout.splitlines():
            if line.startswith("n"):
                return line[1:]
    except Exception:
        pass
    return None


SHELLS = {
    "zsh",
    "bash",
    "sh",
    "fish",
    "login",
    "tmux",
    "screen",
    "claude",
    "-zsh",
    "-bash",
}
APP_LABELS = [
    ("Code Helper", "VS Code"),
    ("Visual Studio Code", "VS Code"),
    ("Cursor", "Cursor"),
    ("iTerm", "iTerm2"),
    ("Terminal", "Terminal"),
    ("WezTerm", "WezTerm"),
    ("Warp", "Warp"),
    ("kitty", "kitty"),
    ("Alacritty", "Alacritty"),
]


def host_app(pid: int):
    """Which application's terminal hosts this session — from the ANCESTOR
    chain, never from sibling processes (an MCP server's --app flag next to a
    session led to a wrong 'Cursor' attribution in practice)."""
    cur = pid
    for _ in range(15):
        try:
            r = subprocess.run(
                ["ps", "-o", "ppid=,comm=", "-p", str(cur)],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            out = r.stdout.strip()
            if not out:
                return None
            ppid_s, _, comm = out.partition(" ")
            ppid = int(ppid_s)
        except Exception:
            return None
        for needle, label in APP_LABELS:
            if needle in comm:
                return label
        if ppid <= 1:
            name = os.path.basename(comm.strip())
            return name if name not in SHELLS else None
        cur = ppid
    return None


def last_user_snippet(cwd: str, own_session_id: str):
    """(session-id-prefix, ts, text) of the newest OTHER session's last user
    message in this project — so a blocking prompt lets the human recognize
    WHICH forgotten conversation is being protected."""
    proj = os.path.expanduser(os.path.join("~/.claude/projects", project_slug(cwd)))
    best = None
    try:
        for name in os.listdir(proj):
            if not name.endswith(".jsonl"):
                continue
            if own_session_id and name == f"{own_session_id}.jsonl":
                continue
            path = os.path.join(proj, name)
            try:
                m = os.stat(path).st_mtime
            except OSError:
                continue
            if best is None or m > best[0]:
                best = (m, path, name)
    except OSError:
        return None
    if not best:
        return None
    _, path, name = best
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - 131072))
            tail = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    snippet = None
    # A JSON Lines record ends at LF alone. JSON permits a raw U+2028 inside
    # a string, and `str.splitlines` cut such a record into two halves that
    # each failed to parse, so the snippet was an earlier message's (#664).
    for line in tail.split("\n"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") != "user":
            continue
        content = (d.get("message") or {}).get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = " ".join(
                x.get("text", "")
                for x in content
                if isinstance(x, dict) and x.get("type") == "text"
            )
        else:
            continue
        text = " ".join(text.split())
        if text:
            snippet = (name.split(".")[0][:8], d.get("timestamp", "")[:16], text[:80])
    return snippet


def tty_idle_minutes(pid: int):
    """Minutes since the terminal hosting `pid` last saw input OR output.

    None when the pid has no tty or it cannot be checked -- callers treat
    that conservatively (active). atime is bumped by keystrokes (human
    present), mtime by writes to the screen -- a session streaming its
    progress repaints constantly, while an idle Claude Code prompt does not
    repaint at all (verified), so the fresher of the two is the signal.
    """
    try:
        r = subprocess.run(
            ["ps", "-o", "tty=", "-p", str(pid)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        tty = r.stdout.strip()
        if not tty or tty == "??":
            return None
        st = os.stat(f"/dev/{tty}")
        return max(0.0, (time.time() - max(st.st_atime, st.st_mtime)) / 60)
    except Exception:
        return None


def project_slug(path: str) -> str:
    """~/.claude/projects encodes a cwd by replacing non-alphanumerics with '-'."""
    return re.sub(r"[^A-Za-z0-9-]", "-", path)


ACTIVE_EVENT_TYPES = {"user", "assistant", "tool_use", "tool_result", "progress"}


def last_active_event_epoch(path: str):
    """Epoch of the newest ACTIVE event in a transcript's tail, else None.

    File mtime alone over-reports activity: idle sessions still receive
    passive appends (type "attachment" -- e.g. file-changed notices when some
    OTHER session edits a file they had read), observed live. So when the
    mtime looks fresh, confirm by scanning the last 64KB for events that mean
    someone is actually driving: user/assistant/tool traffic.
    """
    import datetime

    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - 65536))
            tail = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    # At LF alone, as `last_user_snippet` splits its tail and as every other
    # transcript reader here iterates the file (#664).
    for line in reversed(tail.split("\n")):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") not in ACTIVE_EVENT_TYPES:
            continue
        ts = d.get("timestamp")
        if not isinstance(ts, str):
            continue
        try:
            return datetime.datetime.fromisoformat(
                ts.replace("Z", "+00:00")
            ).timestamp()
        except ValueError:
            continue
    return None


def file_activity_epoch(path: str, stale_before: float):
    """Epoch of a transcript file's last real activity.

    Stale mtime is trusted as-is (mtime bounds every event, and passive
    appends only ever make it look FRESHER); a fresh mtime must be confirmed
    against the tail's active events.
    """
    try:
        m = os.stat(path).st_mtime
    except OSError:
        return None
    if m < stale_before:
        return m
    return last_active_event_epoch(path)


def transcript_idle_minutes(cwd: str, own_session_id: str, dead_ids=frozenset()):
    """Minutes since any OTHER session's transcript in `cwd`'s project dir was
    written -- top-level <session-id>.jsonl files AND session subdirectories,
    where background-agent transcripts live (<session-id>/subagents/*.jsonl).
    None when there is no readable transcript to judge by.

    A session running an autonomous turn appends its transcript every few
    seconds even though the keyboard is silent, and a background agent does
    the same in the session's subagents directory -- these signals keep
    working sessions out of the "forgotten tab" bucket. Per-project, not
    per-pid: if ANY other session of this project is writing, treat the tree
    as actively worked on.

    `dead_ids` names sessions a lease proves have EXITED (dead_session_ids).
    Their transcripts are skipped: a file an ended session left behind reads
    fresh for the whole idle window, and counting it is how the guard denied a
    switch naming a session that was already gone. Empty by default, so a
    caller that cannot supply the evidence gets exactly the old behaviour.
    """
    proj = os.path.expanduser(os.path.join("~/.claude/projects", project_slug(cwd)))
    newest = None
    threshold = time.time() - IDLE_MIN * 60
    try:
        entries = os.listdir(proj)
    except OSError:
        return None
    for name in entries:
        path = os.path.join(proj, name)
        if name.endswith(".jsonl"):
            if own_session_id and name == f"{own_session_id}.jsonl":
                continue
            if name[: -len(".jsonl")] in dead_ids:
                continue
            m = file_activity_epoch(path, threshold)
            if m is not None and (newest is None or m > newest):
                newest = m
        elif os.path.isdir(path):
            # Session subdirectories hold background-agent transcripts
            # (<session-id>/subagents/agent-*.jsonl). A session whose
            # foreground sits quiet while a background agent grinds for 30+
            # minutes is only visible here. Skip our own session's dir.
            if own_session_id and name == own_session_id:
                continue
            # A background agent runs inside its session's process, so when
            # the lease proves that process gone its subagents went with it.
            if name in dead_ids:
                continue
            for root, _dirs, files in os.walk(path):
                for f in files:
                    if not f.endswith(".jsonl"):
                        continue
                    m = file_activity_epoch(os.path.join(root, f), threshold)
                    if m is not None and (newest is None or m > newest):
                        newest = m
                if newest is not None and newest >= threshold:
                    break  # already fresh enough -- no need to walk further
            if newest is not None and newest >= threshold:
                break
    if newest is None:
        return None
    return max(0.0, (time.time() - newest) / 60)


def lease_owner_alive(pid: int):
    """True / False / None — alive, gone, or not answerable.

    `os.kill(pid, 0)` is the cheap probe on POSIX: the kernel special-cases
    signal 0 to mean "check only, deliver nothing." Windows has no such
    case -- signal 0 there collides with CTRL_C_EVENT, so os.kill(pid, 0)
    can deliver an actual Ctrl+C instead of just answering the question,
    including to this process if pid happens to be our own. `tasklist`
    answers without touching the target process at all.
    """
    if sys.platform == "win32":
        try:
            r = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True,
                # The one reader in this tree whose source is NOT UTF-8:
                # `tasklist` answers in the OEM codepage, and a missing pid
                # returns a localized message. `replace` is what keeps this
                # readable, and the verdict survives it because the
                # discriminator is the ASCII pid column -- a replacement
                # character can never become a digit. A second OEM reader
                # should name `encoding="oem"` rather than inherit this.
                #
                # `text=True` alone was worse than wrong here: the reader
                # thread died on cp949 and its exception did not propagate, so
                # `r.stdout` came back None and `.splitlines()` raised outside
                # the `try`. That is the only process probe Windows has -- no
                # `ps`, no `/proc` -- so the worktree guard went blind on the
                # console most likely to have a non-UTF-8 codepage.
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
        except Exception:
            return None
        rows = (line.split() for line in (r.stdout or "").splitlines() if line.strip())
        return any(len(cols) >= 2 and cols[1] == str(pid) for cols in rows)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        return None


def lease_dir(top: str):
    """<git-dir>/specseal-leases for the tree at `top`, or None if there is
    none to read. In a linked worktree --absolute-git-dir resolves to
    .git/worktrees/<name>, which is deliberate: a lease belongs to the tree
    its session is working in, not to the whole clone."""
    try:
        gd = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=top or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return None
    if gd.returncode != 0:
        return None
    d = os.path.join(gd.stdout.strip(), "specseal-leases")
    return d if os.path.isdir(d) else None


def dead_session_ids(top: str):
    """Session ids a lease PROVES have exited.

    A transcript is evidence that a session wrote something, never that it is
    still running. Those two readings diverge for exactly IDLE_MIN minutes
    after a session ends, and that window is where the guard was wrong: it
    denied a branch switch naming a session whose lease `fresh_leases` had
    already retired on positive evidence its pid was gone. One arm buried the
    session and the next read its transcript and put it back.

    So the same evidence is offered to the transcript scan. This set only ever
    REMOVES liveness, and only on the rule `fresh_leases` states for itself:
    this host, a recorded pid, and that pid no longer running. A lease from
    another host, one with no pid, one that will not parse, an owner that
    cannot be probed, or no lease at all -- none of them land here, so the
    transcript stays counted exactly as it is counted today. Every unreadable
    answer therefore falls toward active, which is the direction `proc_cwd`'s
    docstring argues for: a wrong deny costs a prompt, a wrong allow can move
    someone else's branch under them.

    What this is NOT is a liveness test on the transcript itself. Two were
    measured and both are false: no live `claude` holds its transcript file
    open (so an open-fd probe would answer "not held" for every session and
    collapse the arm to always-idle), and no record type marks the tail of an
    exited transcript.
    """
    d = lease_dir(top)
    if not d:
        return frozenset()
    this_host = socket.gethostname()
    dead = set()
    try:
        names = os.listdir(d)
    except OSError:
        return frozenset()
    for name in names:
        record = {}
        try:
            with open(os.path.join(d, name), encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                record = loaded
        except Exception:
            continue
        # Mirrors fresh_leases' own reading of the same file, so the two
        # cannot drift into disagreeing about one lease.
        host = record.get("host")
        if host and host != this_host:
            continue
        pid = record.get("pid")
        if not isinstance(pid, int):
            continue
        if lease_owner_alive(pid) is False:
            dead.add(name)
    return frozenset(dead)


def fresh_leases(top: str, own_session_id: str = "", scanned_pids=frozenset()):
    """DECLARED work streams — leases beat every heuristic. The session-lease
    hook stamps <git-dir>/specseal-leases/<session-id> on each tool call
    touching this tree, which catches what process scanning cannot:
    extension-hosted sessions (comm != claude) and sessions editing this tree
    from another cwd (both observed live).

    Returns (live, unattributable). The split exists because a lease outlives
    its session: nothing removes the file at session end, so a closed session
    kept denying branch switches for the whole idle window (measured — two
    conversations ended minutes apart and a third could not switch, with no
    prompt offered because every lease landed in the deny path).

    A lease is dropped ONLY on positive evidence that its owner is gone: this
    host, a recorded pid, and that pid no longer running. Everything else —
    a lease from another host, one written before the record carried a pid,
    one whose owner could not be probed — is `unattributable` and becomes a
    question rather than a refusal. The direction matters: the cost of asking
    is a prompt, the cost of a wrong drop is someone else's branch moving
    under them.

    Liveness and the idle window answer different questions — whether the
    session EXISTS, and whether it is WORKING — so neither replaces the other.
    A lease quiet past the window whose owner is still running is a forgotten
    tab, which the process scan already answers with a question rather than a
    pass; dropping it here gave one state two answers depending on which
    signal saw it. `scanned_pids` keeps that fix from doubling prompts: a pid
    the scan already reports is classified there, and the lease steps aside.
    """
    entries = []
    unattributable = []
    this_host = socket.gethostname()
    leases = lease_dir(top)
    if leases:
        for name in os.listdir(leases):
            if own_session_id and name == own_session_id:
                continue
            path = os.path.join(leases, name)
            try:
                age = (time.time() - os.stat(path).st_mtime) / 60
            except OSError:
                continue
            # Pre-upgrade format is a bare timestamp: no owner to ask about,
            # which leaves the record empty and the lease unattributable.
            record = {}
            try:
                with open(path, encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    record = loaded
            except Exception:
                pass
            pid = record.get("pid")
            host = record.get("host")

            # Without an owner to probe, age is the only filter there is.
            if host and host != this_host:
                if age < IDLE_MIN:
                    entries.append(
                        (
                            None,
                            f"{top}  [lease: {name[:8]}… on {host}]",
                            None,
                            age,
                            None,
                        )
                    )
                continue
            if not isinstance(pid, int):
                if age < IDLE_MIN:
                    unattributable.append(
                        (
                            None,
                            f"{top}  [lease: {name[:8]}… owner unknown]",
                            None,
                            age,
                            None,
                        )
                    )
                continue

            alive = lease_owner_alive(pid)
            if alive is False:
                continue  # gone: the only case that retires a lease outright

            if age < IDLE_MIN:
                label = f"pid {pid}" if alive else f"pid {pid} unprobeable"
                entries.append(
                    (None, f"{top}  [lease: {name[:8]}… {label}]", None, age, None)
                )
            elif alive is True and pid not in scanned_pids:
                # Quiet but running, and invisible to the process scan — the
                # forgotten-tab shape, which the scan itself turns into a
                # question rather than a pass. A pid the scan already reports
                # is deliberately skipped: it is classified there on its own
                # signals, and counting one session twice only multiplies
                # prompts. An unprobeable owner is not escalated either — that
                # is an absence of evidence, not evidence of a live session.
                unattributable.append(
                    (
                        None,
                        f"{top}  [lease: {name[:8]}… pid {pid} alive, quiet]",
                        None,
                        age,
                        None,
                    )
                )
    return entries, unattributable


def sessions_in_tree(top: str, own_session_id: str = ""):
    """Other Claude sessions whose cwd sits inside `top`.

    Returns (active, idle, reliable). A session is idle when BOTH signals are
    quiet for IDLE_MIN minutes: no terminal input AND no transcript writes in
    its project -- alive, but nobody (human or autonomous turn) is driving it.
    `reliable` is False when detection cannot be trusted -- notably when we
    cannot even spot our own process -- and the caller then falls back to the
    conservative behaviour.
    """
    # `pgrep -x claude` was observed to silently miss live sessions on macOS,
    # so enumerate with ps and match the executable basename ourselves, by
    # the one test the lease writer and the commit gate's lease route use
    # (`hooksession.is_claude`, #868).
    try:
        r = subprocess.run(
            ["ps", "-axo", "pid=,comm="],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        pids = set()
        for line in r.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            num, _, comm = line.partition(" ")
            if hooksession.is_claude(comm):
                pids.add(int(num))
    except Exception:
        return [], [], False
    if not pids:
        return [], [], False

    mine = ancestors(os.getpid())
    if not (pids & mine):
        return [], [], False  # our own session is invisible -> detection is unusable

    # Read once, then offered to every transcript scan below: the sessions a
    # lease proves have exited. Both scans ask the same question -- "is
    # anybody writing here" -- and a file left behind by an ended session is
    # not an answer to it.
    dead_ids = dead_session_ids(top)

    active, idle = [], []
    for p in sorted(pids - mine):
        d = proc_cwd(p)
        if d and (d == top or d.startswith(top + os.sep)):
            tty_idle = tty_idle_minutes(p)
            tr_idle = transcript_idle_minutes(d, own_session_id, dead_ids)
            signals = [v for v in (tty_idle, tr_idle) if v is not None]
            # Idle only when every readable signal is quiet; no signals at all
            # -> conservative (active).
            entry = (p, d, tty_idle, tr_idle, host_app(p))
            if signals and min(signals) >= IDLE_MIN:
                idle.append(entry)
            else:
                active.append(entry)

    # Sessions the scan already classified, so a lease naming one of them does
    # not raise a second prompt for a single session.
    scanned_pids = frozenset(e[0] for e in active + idle if e[0] is not None)
    lease_live, lease_unattributable = fresh_leases(top, own_session_id, scanned_pids)
    active.extend(lease_live)
    idle.extend(lease_unattributable)

    # Sessions whose process is NOT named claude (VS Code extension panels,
    # embedded hosts) are invisible to the scan above — but they still write
    # this project's transcripts. Fresh active events with no process to pin
    # them on = an unattached live session; measured live when a background
    # agent kept working after its terminal pid died from the scan's view.
    #
    # `dead_ids` is what keeps that reading from also catching a session that
    # simply ENDED. Its two inputs -- no process, a fresh transcript -- are
    # equally the inputs of a session that exited inside the idle window, and
    # nothing in the arm separated them, so the tree read as concurrent for
    # IDLE_MIN minutes after every session in the project closed. The lease
    # separates them exactly, and it keeps the case this arm exists for: a
    # live panel session's lease owner is alive, and one that has not written
    # a lease at all is not proved dead either, so both still count.
    if not active:
        tr_idle = transcript_idle_minutes(top, own_session_id, dead_ids)
        if tr_idle is not None and tr_idle < IDLE_MIN:
            active.append((None, top, None, tr_idle, None))
    return active, idle, True


def _age(minutes):
    if minutes is None:
        return tr("unknown", "확인 불가")
    if minutes >= 60:
        return tr(f"{minutes / 60:.1f}h ago", f"{minutes / 60:.1f}시간 전")
    return tr(f"{minutes:.0f}m ago", f"{minutes:.0f}분 전")


def fmt_sessions(entries):
    """Per-session line with DISAGGREGATED signals and host app. "마지막 활동
    1분 전" alone proved undiagnosable in practice — the reader could not tell
    a keystroke from an autonomous turn's transcript write, and app guesses
    made from sibling MCP processes misattributed a VS Code tab to Cursor."""
    lines = []
    for p, d, tty_idle, tr_idle, app in entries:
        if p is None:
            kind = (
                tr("lease declaration", "lease 선언")
                if "[lease:" in d
                else tr("transcript activity", "작업 기록(트랜스크립트)")
            )
            lines.append(
                tr(
                    f"    (unidentified session — extension panel or a session in another cwd)  {d}\n"
                    f"        {kind} {_age(tr_idle)} — working on this tree right now",
                    f"    (프로세스 미확인 세션 — VS Code 확장 패널·다른 cwd 의 세션 등)  {d}\n"
                    f"        {kind} {_age(tr_idle)} — 지금 이 트리에서 작업 중",
                )
            )
            continue
        where = (tr(f" ({app} terminal)", f" ({app} 터미널)")) if app else ""
        lines.append(
            tr(
                f"    pid {p}{where}  {d}\n"
                f"        terminal in/out {_age(tty_idle)} · transcript activity {_age(tr_idle)}",
                f"    pid {p}{where}  {d}\n"
                f"        터미널 입력/출력 {_age(tty_idle)} · 작업 기록(트랜스크립트) {_age(tr_idle)}",
            )
        )
    return "\n".join(lines)


def fmt_snippet(cwd, own_session_id):
    s = last_user_snippet(cwd, own_session_id)
    if not s:
        return ""
    sid, ts, text = s
    quoted = chr(34) + text + chr(34)
    return tr(
        f"\nNewest other-session record for this tree [{sid}… {ts}], last user message:\n"
        f"    {quoted}\n",
        f"\n이 트리의 가장 최근 다른 세션 기록 [{sid}… {ts}] 마지막 사용자 메시지:\n"
        f"    {quoted}\n",
    )


def tracked_changes(cwd: str) -> list[tuple[str, str]]:
    """(XY, path) entries of staged+unstaged changes to TRACKED files.

    Untracked files are excluded on purpose: they stay put across a switch and
    do not get carried onto the other branch.
    """
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        return [(line[:2], line[3:]) for line in r.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def phantom_entries(entries: list[tuple[str, str]], cwd: str) -> list[tuple[str, str]]:
    """Dirt invisible in the working tree: index-only entries (AD) and
    force-added paths that .gitignore hides from a plain directory view.
    """
    phantoms = []
    for xy, path in entries:
        if xy == "AD":
            phantoms.append(
                (
                    path,
                    tr(
                        "exists only in the index (added, then deleted in the worktree)",
                        "index에만 존재 (add 후 워크트리에서 삭제됨)",
                    ),
                )
            )
        # --no-index: check-ignore never flags indexed paths without it, and a
        # force-added file is by definition in the index.
        elif (
            xy[0] != " "
            and subprocess.run(
                ["git", "check-ignore", "-q", "--no-index", path],
                cwd=cwd or None,
                capture_output=True,
            ).returncode
            == 0
        ):
            phantoms.append(
                (
                    path,
                    tr(
                        "gitignored path force-staged into the index",
                        ".gitignore 경로인데 강제 스테이징됨",
                    ),
                )
            )
    return phantoms


def respond(decision: str, reason: str):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def repo_paths(cwd: str):
    """Return (toplevel, suggested worktree root) for the repo containing cwd."""
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            # The same bound `hooks/optin.py` puts on the same species of
            # call. This one runs once per candidate directory and the reader
            # can hand it several, so an unresponsive path is a hook that
            # never decides — and a hook that never decides is a command that
            # never runs. Read from the two call sites, not reproduced: no
            # unresponsive mount was mounted.
            timeout=5,
        ).stdout.strip()
    except Exception:
        top = ""
    if not top:
        return "", "../<repo>-worktrees"
    # git answers with forward slashes on Windows (`C:/proj/repo`) while the
    # OS and every other path in this module use the native separator. One
    # spelling, so the containment test in sessions_in_tree() compares like
    # with like.
    top = os.path.normpath(top)
    return top, os.path.join(os.path.dirname(top), f"{os.path.basename(top)}-worktrees")


def git_at(top: str, cwd: str) -> str:
    """The command word for a command a reason tells the person to run.

    `git` where the shell already stands in `top`'s tree, and `git -C <top>`
    where it does not: a `git -C <repo>` or a `cd <repo>` in the judged command
    names a tree the shell never moved to, so an unqualified `git fetch` or
    `git worktree add` in the advice ran in the shell's own repository, or
    failed where the shell had none (round 2 of work item 1790550712, finding
    1). A subdirectory of `top` is the same tree, and none of these commands
    takes a path relative to the root, so the text there is what it was.
    """
    here = repo_paths(cwd)[0] if cwd else ""
    if here and os.path.normcase(here) == os.path.normcase(top):
        return "git"
    return f"git -C {shlex.quote(top)}"


def steer_to_switch(git: str = "git") -> str:
    return tr(
        f"  {git} fetch origin\n"
        f"  {git} switch -c <branch> origin/main   # new branch\n"
        f"  {git} switch <branch>                  # existing branch\n\n"
        "If this genuinely is concurrent work needing separation, state why and get the "
        "user's confirmation first (if the user already asked for a worktree, retry with "
        "[worktree-ok] in the command).",
        f"  {git} fetch origin\n"
        f"  {git} switch -c <branch> origin/main   # 새 브랜치\n"
        f"  {git} switch <branch>                  # 기존 브랜치\n\n"
        "정말 동시 작업이라 분리가 필요하면 그 이유를 밝히고 사용자 확인을 먼저 받으세요 "
        "(사용자가 이미 워크트리를 지시했다면 명령에 [worktree-ok] 를 붙여 다시 시도).",
    )


def steer_to_shared(git: str = "git") -> str:
    """The retry for the answer "switch in the shared tree".

    `[worktree-ok]` gave the worktree answer a way to come back through the
    guard; the shared-tree answer had none, so a user who chose it met the
    mirror question one command later. The token is that missing half.

    Both branch forms are named. A single `-c` form told a user heading for a
    branch that already has commits on it to create it again, which git
    refuses outright.

    Translated, because naming both forms turned a bare command line into a
    sentence — and that sentence sat untranslated in the middle of a Korean
    option.
    """
    return tr(
        f"`{git} switch <branch>  # [shared-tree-ok]` for an existing branch, or "
        f"`{git} switch -c <branch> origin/main  # [shared-tree-ok]` for a new one",
        f"기존 브랜치면 `{git} switch <branch>  # [shared-tree-ok]`, 새 브랜치면 "
        f"`{git} switch -c <branch> origin/main  # [shared-tree-ok]`",
    )


def git_dir(cwd: str) -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        ).stdout.strip()
    except Exception:
        return ""


def already_asked(top: str, session: str, scope: str) -> bool:
    """True when this session was already offered a choice in this direction.

    Records it when it was not. An unwritable marker counts as already asked:
    one missed question beats a deny the session cannot get past. The same
    rule as hooks/review-skill-gate.py, though not the same code — that one
    builds its git-dir as `<root>/.git`, which is a FILE in a linked worktree.

    `scope` is the direction the question belongs to ("create" or "switch"),
    not the individual site. Within one direction the sites are mutually
    exclusive on tree state, so splitting further buys nothing; what it would
    cost is a second question when the model retries with a token and lands on
    a neighbouring site — the same question, one command later. One budget for
    the whole guard was worse still: answering at the creation sites left a
    later switch with the two-button prompt this work exists to replace.

    The id names a file, so a separator in a malformed one must not become a
    path escape — measured: `../../escaped` put an empty file at the
    repository root. `hooks/session-lease.py` guards its own id the same way.
    """
    gd = git_dir(top)
    session = os.path.basename(str(session or ""))
    if not gd or not session or session in (".", ".."):
        return True
    path = os.path.join(gd, CHOICE_DIR, scope, session)
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").close()
    except OSError:
        return True
    return False


def choose(
    top, session_id, scope, situation, question, options, fallback, before_ask=None
):
    """Deny once and hand the user the two options; ask on every attempt after.

    A hook decision renders as approve/decline, and the model never gets the
    turn — so where declining has TWO destinations the user sees neither and
    has to retype the command they wanted. Denying gives the model the turn
    back, and the reason spends it on AskUserQuestion.

    The fallback is this site's own pre-change decision, which is what keeps
    the deny from becoming a trap: a session with nobody to answer (headless),
    or one that has already been asked here, meets the prompt it always met.

    **`before_ask` runs on the fallback path only, and it exists because the
    two branches of this function have opposite standing for a command that
    carries more than the site is asking about.** The deny stops the WHOLE
    command line, so anything else written on it is stopped too. The ask does
    not: approving it runs every segment, while its own text asks about one of
    them. `main`'s switch ladder read "the three rows above the creation all
    deny" off two sites that are this one -- true of the first attempt and
    false of every attempt after, so the second `git switch feature/x && git
    worktree add ../wt f` in a session was answered *Approve — switch branches
    in this shared tree*, and approving created the worktree with the creation
    question never put. Executed at `62b2d2e`, both the idle and the
    detection-unusable states: `deny` then `ask`, the creation question on
    neither.

    Passing the creation's own judgment here rather than reordering the ladder
    is what keeps the deny branch intact: the first attempt still puts the
    switch's two options, naming the sessions it found, and only the branch
    that would have let the command through yields.
    """
    if session_id and not already_asked(top, session_id, scope):
        lines = [
            situation.rstrip("\n"),
            "",
            tr(
                "Do not choose for the user. Ask with the AskUserQuestion tool, "
                "offering exactly these two options:",
                "사용자 대신 고르지 마세요. AskUserQuestion 툴로 아래 두 선택지를 "
                "그대로 물어보세요:",
            ),
            "",
            f"  {question}",
        ]
        for label, detail in options:
            lines.append(f"    {label} — {detail}")
        lines.append("")
        lines.append(
            tr(
                "Then run what they picked. Re-issuing this command before they "
                "answer reaches the ordinary confirmation prompt instead.",
                "고른 쪽을 실행하세요. 답을 받기 전에 같은 명령을 다시 내면 "
                "일반 확인창이 뜹니다.",
            )
        )
        respond("deny", "\n".join(lines))
    if before_ask is not None:
        before_ask()
    respond("ask", situation + fallback)


def guard_worktree_creation(
    top: str,
    cwd: str,
    origin: str,
    user_ok: bool,
    session_id: str = "",
    consented="silent",
    transcript_path="",
):
    """Worktrees are for CONCURRENT work only -- block the single-stream case.

    The Bash path's creation ladder. The Agent/Task path used to come through
    here as well, with its own `single_stream` verdict and its own wording for
    the shared-tree option; it is judged in `main` now, by a rule that counts
    no sessions (#8), so those three parameters went with it.
    """
    # Same reason as the switch path: without a repository there is no tree to
    # separate, and standing `cwd` in for one makes every session under it look
    # like concurrent work in it.
    if not top:
        return

    # 0) 이 세션이 이 클론에서 이미 worktree 를 만들었거나, 사용자가 라우팅 질문에
    #    `automation` 을 눌렀다면, 아래 모든 자리는 사용자가 이미 답한 질문을
    #    다시 내는 것이다.
    #
    # This row goes ABOVE every other one, including the ACTIVE-session row.
    # Each of them asks something the consent has already answered: the ACTIVE
    # row asks for a confirmation, the two choice rows ask which way to go, and
    # the `[worktree-ok]` row asks whether the token was meant. A session that
    # created a worktree with a person's answer has settled all four, and so
    # has a person who pressed `automation`, whose description says nothing
    # stops to ask again.
    #
    # And it answers the `[worktree-ok]` docstring rather than stepping around
    # it. That site is right that the TOKEN is not evidence -- it is written
    # into the command by whoever issues it, so the model can write it on the
    # first attempt. This record is written by a PostToolUse hook AFTER the
    # call ran, and a `git worktree add` runs only if the deny did not fire and
    # the ask was answered yes. What changes is the invariant "creating a
    # worktree always takes one confirmation", which becomes "the FIRST
    # creation of a session takes one". That is the whole behaviour change.
    #
    # The routing answer is the second source, for the one creation the record
    # cannot cover: the first, which in an automation run comes before any
    # creation has run. The harness writes that answer into this session's
    # transcript from the person's click, and the model never writes which
    # option was pressed -- so it has the record's standing, not the token's.
    # `worktree_consent.consent` reads both, record first, and holds the rules.
    #
    # `consented` is the bound on the allow, computed by the caller from the
    # command. `hooks/worktree_consent.py` holds the record, the answer and the
    # rest of the reasoning.
    # No `session_id and` in front of it: `consent_path` and `transcript_for`
    # already answer "" for a missing or separator-only id, so a second test
    # here would be a
    # condition nothing could make false — which is a condition no case can
    # pin.
    # WHY `silent` AND NOT `ask` FOR A COMPOUND — the argument both entry
    # points rest on, kept here because a reader of the Bash path will not go
    # looking at the Agent block in `main` for it.
    #
    # A call that is a creation PLUS something else -- an agent with a prompt,
    # a pipe, a `cd`, a redirection -- is two questions, and the consent
    # answers only the first. Silence is the guard WITHDRAWING ITS OBJECTION,
    # which is the whole of what either consent establishes; whatever the harness
    # wants to ask about the rest of the command line is not the guard's to
    # remove, and it is equally not the guard's to ASK. `silent` grants
    # nothing: this function returns without responding, and the harness's own
    # permission flow then judges the call on its own terms, so a user's
    # `permissions.deny` on `Bash(sudo:*)` still fires -- it is simply not a
    # worktree guard that fires it.
    #
    # That is why the bound on the ALLOW is untouched by this. `allow` speaks
    # FOR the whole tool call and needs `only_creates_a_worktree` behind it;
    # `silent` speaks for none of it. The eleven shapes measured at `d82a02c`
    # are what an unbounded allow signs for, and every one of them still
    # fails that test and still reaches the harness rather than this guard.
    #
    # Measured on this repository's 0.9.2 release run: of five worktrees
    # created, two confirmations were paid here, both because the command
    # carried a pipe or a `cd` -- shapes the repository's own CLAUDE.md asks
    # sessions to write, by telling them to batch independent runs into one
    # call. The rule that shapes the command and the arm that stayed quiet for
    # it disagreed, and the session paid a stop for following the rule.
    #
    # #237's invariant holds for every session whose person did not press
    # `automation`: its FIRST creation is still a question, because without
    # that answer this arm is reached only once a record exists.
    #
    # `consented` is `allow` or `silent` and nothing else. It used to default
    # to `ask`, and an `ask` tail no production caller could reach sat under a
    # rider; both went when the routing answer joined this row, because a
    # message no caller can reach is a message nobody maintains.
    source = worktree_consent.consent(top, session_id, transcript_path)
    if source:
        if consented != "allow":
            return
        respond(
            "allow",
            f"{origin}\n"
            + (
                tr(
                    "A worktree creation already ran in this repository this session, "
                    "which means the user answered for it -- the harness only runs a "
                    "call that was permitted. It is the same decision, so it is not "
                    "put again.\n",
                    "이 세션에서 이 저장소에 worktree 생성이 이미 실행되었습니다. "
                    "허용된 호출만 실행되므로 사용자가 이미 답한 것입니다. 같은 "
                    "결정이라 다시 묻지 않습니다.\n",
                )
                if source == "record"
                else tr(
                    "The user pressed `automation` on this session's routing question, "
                    "whose answer says nothing stops to ask again. The harness wrote "
                    "that answer into this session's transcript, so the creation is "
                    "not put to them.\n",
                    "사용자가 이 세션의 라우팅 질문에서 `automation` 을 눌렀고, 그 답은 "
                    "더는 멈춰서 묻지 않는다는 뜻입니다. 이 답은 하네스가 이 세션의 "
                    "작업 기록에 적었으므로 생성을 다시 묻지 않습니다.\n",
                )
            ),
        )

    active, idle, reliable = sessions_in_tree(top, session_id)
    # The command word for every command this ladder hands back: `-C <top>`
    # where the shell is not in the creation's tree (`git_at`).
    git = git_at(top, cwd)

    # 두 방향의 목적지는 어느 자리에서 물어도 같다 — worktree 를 만들거나,
    # 공용 트리에서 `git switch` 로 그대로 진행하거나.
    create_or_switch = (
        (
            tr('1. "Create the worktree"', '1. "worktree 를 만든다"'),
            tr(
                "retry it and approve at the prompt — creating a worktree always "
                "takes a confirmation, so the retry asks once.",
                "그대로 다시 시도하고 확인창에서 승인하세요 — worktree 생성은 항상 "
                "확인을 한 번 거치므로 재시도 때 한 번 물어봅니다.",
            ),
        ),
        (
            tr(
                '2. "Switch in the shared tree"',
                '2. "공용 트리에서 브랜치만 전환한다"',
            ),
            tr(
                f"run {steer_to_shared(git)} instead. The token carries this "
                "answer, so the switch is not questioned again.",
                f"대신 {steer_to_shared(git)} 중 하나를 실행하세요. 이 토큰이 지금 "
                "고른 답을 담고 있어 전환할 때 다시 묻지 않습니다.",
            ),
        ),
    )

    # 1) 같은 트리에서 다른 세션이 동시에 작업 중 -> 분리가 타당. 확인만 받는다.
    if active:
        respond(
            "ask",
            (
                f"{origin}\n"
                + tr(
                    "Another Claude session is actively working in this tree, so a worktree "
                    "split looks justified. Worktree creation still needs the user's confirmation.\n",
                    "이 작업 트리에서 다른 Claude 세션이 동시에 작업 중이라 worktree 분리가 "
                    "타당해 보입니다. 다만 룰상 worktree 생성은 사용자 확인이 필요합니다.\n",
                )
                + f"{fmt_sessions(active)}\n"
                + f"{fmt_snippet(top, session_id)}\n"
                + tr(
                    "Confirm to proceed. Declining cancels this — use the worktree already "
                    "open for that session, or wait for it to finish.",
                    "진행할지 확인해 주세요. 거부하면 이번 생성은 취소됩니다 — 그 세션이 이미 "
                    "열어 둔 worktree를 쓰거나, 세션이 끝날 때까지 기다리세요.",
                )
            ),
        )

    # 2) 단건 작업이라도 [worktree-ok] 가 있으면 확인만 받는다. 이 검사가 선택지
    #    자리들보다 먼저 오는 것이 핵심이다 — 뒤에 두면 판정 불가 환경에서
    #    토큰을 달고 와도 선택지 자리가 먼저 잡아, 방금 답한 질문을 또 낸다.
    #
    # NOT a choice site, and the one place where that was tried and taken back.
    # `[worktree-ok]` is what a completed confirmation looks like coming back
    # through the guard (steer_to_switch says so in as many words), so putting
    # the same question again asks something the user has already answered.
    # It also closed a ring: a user who chose "split into a worktree" at a
    # SWITCH site retries with the token, lands here, and gets asked whether
    # they meant it. The `ask` below is not a weaker check — creating a
    # worktree always takes one confirmation, and declining it withdraws the
    # token, which is the second option spelled out.
    if user_ok:
        respond(
            "ask",
            (
                f"{origin}\n"
                # Reached before the choice rows, detection-unusable included,
                # so the count is named only where one was taken. And above
                # the idle row too, so *can be shown to be working*: a count
                # that found only idle sessions found nobody shown working,
                # and did not find nobody (#624).
                + (
                    tr(
                        "No other Claude session can be shown to be working in "
                        "this tree, but ",
                        "이 트리에서 작업 중임이 확인되는 다른 Claude 세션은 없지만 ",
                    )
                    if reliable
                    else ""
                )
                + tr(
                    "[worktree-ok] was given — treating this as the user's explicit "
                    "intent. Confirm the worktree creation. Declining withdraws "
                    "[worktree-ok] and proceeds in the shared tree instead:\n",
                    "[worktree-ok] 가 지정되어 사용자 의사로 판단합니다. worktree 를 "
                    "생성할지 확인해 주세요. 거부하면 [worktree-ok] 선언을 철회하고 공유 "
                    "트리에서 그대로 진행합니다:\n",
                )
                + steer_to_switch(git)
            ),
        )

    # 3) 살아 있긴 하나 한동안 입력이 없는 세션뿐 -> 잊힌 탭일 가능성. 사용자가 안다.
    if idle:
        choose(
            top,
            session_id,
            "create",
            (
                f"{origin}\n"
                + tr(
                    f"The only other sessions here have shown no activity (input or transcript) "
                    f"for {IDLE_MIN}+ minutes — if they are forgotten tabs this is effectively "
                    f"single-stream work and plain `git switch` beats a worktree.\n",
                    f"이 트리의 다른 세션은 {IDLE_MIN}분 이상 활동(키 입력·작업 기록)이 없는 것뿐입니다 — "
                    f"잊힌 탭이면 사실상 단건 작업이라 worktree 없이 `git switch` 가 낫습니다.\n",
                )
                + f"{fmt_sessions(idle)}\n"
                + f"{fmt_snippet(top, session_id)}\n"
            ),
            tr(
                "Only idle sessions here — split into a worktree, or switch in "
                "the shared tree?",
                "여기엔 멈춰 있는 세션뿐입니다 — worktree 로 분리할까요, 공용 트리에서 "
                "전환할까요?",
            ),
            create_or_switch,
            tr(
                "Still split into a worktree? Declining switches to plain `git switch` "
                "in the shared tree instead:\n",
                "그래도 worktree 로 분리할지 확인해 주세요. 거부하면 공유 트리에서 "
                "`git switch` 로 전환합니다:\n",
            )
            + steer_to_switch(git),
        )

    # 4) 동시 세션 판정 불가 -> 자동으로 만들지 말고 물어본다.
    if not reliable:
        choose(
            top,
            session_id,
            "create",
            (
                f"{origin}\n"
                + tr(
                    "Cannot determine whether other sessions are working here (ps/lsof "
                    "unavailable), so no automatic verdict.\n",
                    "동시 세션 여부를 확인할 수 없어(ps/lsof 사용 불가) 자동 판정을 못 합니다.\n",
                )
            ),
            tr(
                "No verdict is possible here — split into a worktree, or switch "
                "in the shared tree?",
                "여기서는 자동 판정이 불가능합니다 — worktree 로 분리할까요, 공용 "
                "트리에서 전환할까요?",
            ),
            create_or_switch,
            tr(
                "Confirm if this really is concurrent work; if single-stream, cancel and "
                "use `git switch`.",
                "정말 동시 작업이면 확인해 주시고, 단건이면 취소하고 `git switch` 로 진행하세요.",
            ),
        )

    # A Bash command can carry `[worktree-ok]` and come back through the block
    # above, so this deny has a documented way past it.
    respond(
        "deny",
        (
            f"{origin}\n"
            + tr(
                "No other session is working in this tree (= single-stream). Rule: for "
                "single-stream work, don't create a worktree — just switch branches in the "
                "shared tree. Everything stays visible in one editor window, and half-used "
                "worktree folders don't pile up.\n\n",
                "이 트리에서 동시에 작업 중인 다른 세션이 없습니다(= 단건 작업). "
                "룰: 단건이면 worktree를 만들지 말고 공유 트리에서 브랜치만 갈아끼웁니다 "
                "— 에디터 한 창에서 다 보여 코드 파악이 빠르고, 쓰다 만 worktree 폴더가 "
                "쌓이지 않습니다.\n\n",
            )
            + steer_to_switch(git)
        ),
    )


def judge_creation(
    command: str, cwd: str, top: str, session_id: str, transcript_path: str = ""
):
    """Put the creation question for a `git worktree add` in `command`.

    Extracted because more than one site reaches it, and the second one is
    why. `main` classified only the FIRST segment it could read, while
    `hooks/worktree_consent.py` records for a creation ANYWHERE in a command
    that RAN -- its docstring says so on purpose. Those two readings disagreed,
    and the gap between them was writable by whoever composed the command.
    `main` now reads up to its first switch and its first creation, in either
    order, and its own comment on the walk says why.

    Executed at `d82a02c`, clean single-stream tree, no consent record:

        git worktree add ../wt f                        deny
        git status && git worktree add ../wt f          deny
        git switch feature/x && git worktree add ../wt f   SILENT, record written
        git switch feature/x ;  git worktree add ../wt f   SILENT, record written
        git checkout feature/x && git worktree add ../wt f SILENT, record written

    `git status` classifies to nothing so the walk moved on and the creation
    ladder did run, which is the safe half of the class and the only half
    `phases/phase-2.md` named. The class is any first segment whose OWN verdict
    is not `None`: the walk stopped there, the creation ladder never ran, the
    shell created the worktree, and `PostToolUse` minted session-wide consent
    for a question nobody was asked. That falsified `spec.md`'s *a `git
    worktree add` runs only if the guard's `deny` did not fire and its `ask`
    was answered yes*, and the "Forgeable by the model: no" row resting on it.

    What is NOT done here is making the creation outrank the earlier verdict.
    That closes the same hole and costs a protection this branch must not move:
    `git switch feature/x && git worktree add ../wt f` in a tree another
    session is ACTIVE in denies today as a switch, and would become an `ask`
    about the creation -- the branch would still be taken out from under the
    other session, one approval later. The switch ladder keeps every verdict it
    has, and the creation is judged at the places where that ladder would
    otherwise let the command run: its two choice rows' `ask`, and above its
    tracked-changes row and its silent exit. The same holds whichever of the
    two segments is written first.

    `top` is the creation's own repository, which is not always the switch's --
    `git switch x && git -C /other worktree add ../wt f` acts on two. A `top`
    of "" is passed straight through; `guard_worktree_creation` refuses that
    case for the reason its own first lines give.
    """
    # A command the lexer gave up on may carry a `[worktree-ok]` in the part it
    # never reached. Single-stream is the one verdict in this guard with no
    # budget and no `ask` behind it, and its way past is "append
    # [worktree-ok]": without this note the user appends a token that is
    # already there, meets the same deny, and the loop ends only when the
    # command itself is rewritten.
    #
    # The verdict is left alone -- softening deny to ask would hand every
    # command a bypass costing one apostrophe -- and the instruction is made
    # followable instead, by naming the quote as the obstacle.
    user_ok = has_token(command, "[worktree-ok]")
    origin = tr(
        "Attempting to create a worktree with `git worktree add`.",
        "`git worktree add` 로 worktree를 만들려 합니다.",
    )
    if not user_ok and not parses_cleanly(command):
        origin += tr(
            " No [worktree-ok] was read, and this command has an unbalanced "
            "quote -- an apostrophe in a comment is enough. Everything "
            "after the quote opens is unread, so a token written there is "
            "invisible to a bare-word match. If you already appended one, "
            "close or drop the quote and re-issue.",
            " [worktree-ok] 를 읽어내지 못했습니다. 이 명령에는 닫히지 않은 "
            "따옴표가 있습니다(주석의 아포스트로피 하나면 충분합니다). 따옴표가 "
            "열린 뒤로는 읽지 못하므로, 그 뒤에 적은 토큰은 낱말로 잡히지 "
            "않습니다. 이미 붙이셨다면 따옴표를 닫거나 지우고 다시 실행하세요.",
        )
    guard_worktree_creation(
        top,
        cwd,
        origin,
        user_ok=user_ok,
        session_id=session_id,
        # The bound on the allow, computed from the command rather than from
        # the verdict: the verdict says a creation is in here somewhere, and
        # the allow needs to know there is nothing else.
        # `cwd`, not the creation's directory: this reads the command from
        # where the SHELL started, which is what the `walk_command` in `main`
        # was given too. Where the classified segment LANDED is not a starting
        # point -- handing it back would walk the same `cd` twice.
        #
        # `silent` on the else arm, not `ask`: see the `granted` block in
        # `guard_worktree_creation`, which holds the argument both entry
        # points now rest on. The bound on the ALLOW is unchanged -- a
        # compound still never earns one.
        consented=("allow" if only_creates_a_worktree(command, cwd) else "silent"),
        # Where the routing answer is read from; `worktree_consent` falls back
        # to this session's own file by id when the path names another one.
        transcript_path=transcript_path,
    )


# --- three shapes, and the stop for the third (#826) -----------------------
#
# Work item 1791270162. The switch arm used to answer *does this command
# switch a branch?* from the command's text, and four readings grew on that
# question without the findings converging (the option table, the name
# lookups, the guesses, candidate C). It now answers *is this command known
# to leave the branch where it is?* from the frozen reading's own words, and
# treats everything else as a possible switch, judged only where a switch
# would matter: another session ACTIVE or IDLE in the tree, detection
# unusable, or tracked changes (`docs/worktree-guard-spec.md` §A rows 1-4).
# Phase 3 of the work item removed the four readings and `classify` with
# them; nothing in this file looks a name up any more.

# Every git subcommand the recorded runs hold whose plain invocation leaves
# HEAD's branch where it was. The count beside each is the distinct (command,
# directory) pairs holding it in cut 1 / cut 2 of phase 1 of work item
# 1791270162 (`phases/phase-1.md` §M1: Bash tool uses before
# 2026-10-03T11:06:22+09:00 / to 2026-10-06), the way `hooks/tokens.py`'s
# `PLAIN_GIT` carries its counts. A subcommand the corpus never recorded is
# not here, on the owner's answer P1 (a): the list grows by a measured row,
# never by a reading. Which ones leave the branch was read off what each
# does (`spec.md` In 5), and one form of each row is run against git by
# `test_no_listed_form_moves_head_under_git`, which found `rebase`'s
# branch-naming form in round 1 of work item 1791270162.
#
# Not here, on purpose: `switch` (the ladder's), `checkout` (listed only with
# a path after `--`, `_restores`), `worktree` (listed unless it adds one,
# which is a creation, or a redirection hides its `add`, `_hidden_mover`),
# `update-ref` 13/13 and `symbolic-ref` 1/1 (both can
# move HEAD, owner's answer P3 (a)), and `bisect` and `stash branch`, which
# were recorded 0 times. Content moved on the same branch -- `reset`,
# `stash`, `rebase`, `merge`, `pull` -- is not the guard's subject (§Premise).
LEAVES_THE_TREE = frozenset(
    {
        "log",  # 2858/3064
        "status",  # 2609/2848
        "commit",  # 2014/2149
        "diff",  # 2028/2127
        "add",  # 1842/1947
        "rev-parse",  # 893/961
        "show",  # 651/756
        "push",  # 573/607
        "grep",  # 385/454
        "fetch",  # 252/276
        "clone",  # 223/243
        "branch",  # 223/236, `-m` renames HEAD's branch, same line of history
        "merge-base",  # 98/104
        "config",  # 84/100
        "stash",  # 95/99, `stash branch` excepted
        "ls-tree",  # 55/73
        "tag",  # 46/60
        "ls-files",  # 56/58
        "merge",  # 52/55
        "ls-remote",  # 44/47
        "archive",  # 43/47
        "pull",  # 43/44
        "cat-file",  # 38/41
        "for-each-ref",  # 26/40
        "describe",  # 26/27
        "rev-list",  # 23/24
        "reset",  # 23/23
        "remote",  # 17/19
        "init",  # 17/17
        "merge-tree",  # 7/11
        "apply",  # 8/11
        "check-ignore",  # 10/10
        "restore",  # 6/7
        "clean",  # 5/6
        "reflog",  # 6/6
        "revert",  # 6/6
        "blame",  # 3/5
        "rm",  # 5/5
        "cherry-pick",  # 4/4
        "mv",  # 1/2
        "show-ref",  # 2/2
        "rebase",  # 2/2, naming no branch: `_rebase_names_a_branch`
        "diff-tree",  # 1/2
        "gc",  # 1/1
        "format-patch",  # 0/1
        "count-objects",  # 0/1
        "update-index",  # 1/1
        "help",  # 1/1
        "shortlog",  # 1/1
    }
)

# The bare word `git` in text the frozen reading does not read as a git
# segment: a string handed to a shell, a substitution body, a command it
# could not tokenize. `/usr/bin/git` and `$(git` hold it, `gitlab`, `.git/`
# and `git-lfs` do not. This is also the whole test where `hooks/cmdline.py`
# fails to load, so a broken reader costs a stop and never a silence.
_BARE_GIT = re.compile(r"(?<![\w.\-])git(?![\w.\-/])")

# How deep a substitution body inside a body is read before the reading
# counts as one it could not finish, which stops: the bound the commit gate
# puts on the same walk (`NESTING_READ` in `hooks/commit-review-gate.py`).
BODY_DEPTH = 32

# The openers of a substitution, for the text test alone.
_OPENERS = ("$(", "`", "<(", ">(")

# A brace expansion bash and zsh perform before the command runs (#856), read
# so that it errs toward stopping: an unquoted `{` followed later in the same
# word by a `}`, with a `,` or a `..` between them. Nothing about what is
# between is read, so a signed sequence (`{+1..3}`), a nested brace and a
# brace bash would refuse all count. Round 4 of work item 1791384157 found the
# narrower test (`{a,b}` with no brace inside, sequences of digits or single
# letters) missing what bash expands, and the direction is the guard's:
# a brace it cannot tell about is a stop where the tree matters.
#
# This is the test on a command's text with its quoted spans and escapes
# taken out (`_unquoted_brace`), so a quoted brace, an escaped one (`\{a,b\}`)
# and a heredoc body are silent by the shell's own quoting, and a word ends at
# whitespace, so `{a, b}`, which the shell makes two words of, is silent too.
# A `$` directly before the `{` there is a parameter expansion (`${HOME}`,
# `${a,}`), which the shell's grammar makes no brace expansion, and an
# escaped `\$` is gone with the escape, so `\${a,b}` (`$a $b` to bash) stops.
# `{}`, `{a}`, `find`'s `{}` and `@{-1}..HEAD` hold no `,` or `..` before a
# `}` in their word.
_BRACE = re.compile(r"(?<!\$)\{\S*?(?:,|\.\.)\S*?\}")

# The same test on a word the frozen splitter made, asked only where the
# command's text holds one (`_unquoted_brace`). The splitter has taken the
# quotes and escapes off, so whitespace inside the braces was quoted (`{"a
# b",c}` is two words to bash) and a `$` before them may have been escaped:
# neither is read as an exception here.
_BRACE_IN_WORD = re.compile(r"\{.*?(?:,|\.\.).*?\}", re.S)


def _unquoted_brace(text) -> bool:
    """Whether TEXT, a judgment text, holds a brace expansion outside every
    quoted span and escape, which is where the shell expands one.

    The frozen splitter has taken the quotes off a word before the guard reads
    it, so `git commit -m '{a,b}'` and `git rebase {a,b}` arrive as the same
    words, and the quoting is read off the text instead, by the spans
    `hooks/tokens.py#is_plain` takes out (`tokens.QUOTED_SPANS`). The question
    is the command's, not a segment's: a quoted brace in one git segment and
    an unquoted one anywhere else on the line read as unquoted in both, which
    costs a stop where the tree matters. Where `hooks/tokens.py` did not load,
    every brace reads as unquoted, so a broken reader costs a stop and never a
    silence."""
    if tokens is None:
        return bool(_BRACE.search(text or ""))
    return bool(_BRACE.search(tokens.QUOTED_SPANS.sub("", text or "")))


class Finding(tuple):
    """One unrecognised shape: (kind, words, detail).

    KIND names the plain spelling the stop offers (`_described`); WORDS are
    the shape as read, quoted back in the stop; DETAIL is the subcommand for
    `unlisted` and `redirection`, the inner finding for `body`, and empty
    otherwise."""

    __slots__ = ()

    def __new__(cls, kind, words, detail=""):
        return super().__new__(cls, (kind, words, detail))

    kind = property(lambda self: self[0])
    words = property(lambda self: self[1])
    detail = property(lambda self: self[2])


def _holds_git(text) -> bool:
    return bool(_BARE_GIT.search(text or ""))


def _spoken(tokens) -> str:
    """TOKENS as the stop quotes them back: a word holding a space is put
    back in quotes, so `sh -c 'git switch y'` does not read as five words."""
    return " ".join(
        shlex.quote(t) if any(c.isspace() for c in t) else t for t in tokens
    )


# The redirection operators `hooks/cmdline.py`'s `_REDIRECTION` names, from
# their first `<` or `>` on (`&>` and `&>>` lose the `&` that `_plain_words`
# reads as a head). A word ending in one of these takes the next word as its
# target; any other text after the first `<` or `>` is a target glued on.
# `<&` and `>&` are not here: the splitter cuts a word at its `&`, and
# `merged_view` glues the next word on, so neither ends a word this reads (a
# spaced `>& 1` arrives as `>&1`, and `_redirections` places it).
_OPERATORS = frozenset({"<<<", "<<-", "<<", "<>", ">>!", ">>", ">|", ">!", ">", "<"})


def _plain_words(words):
    """WORDS as bash hands them to git once its redirections are off: a word
    holding `<` or `>` goes, with the word after it where the word ends in
    the operator itself (a target written apart), and text glued in front of
    the operator stays as a word of its own (`add>/dev/null` hands git
    `add`). A number or a `{name}` there is the operator's descriptor and an
    `&` is `&>`'s, so neither stays. Whatever follows the operator in the
    same word is its target, so `2>&-`, `>&1-`, `>-` and `>out-` take no
    next word: `<<-`'s `-` is part of the operator, a closed or moved
    descriptor's is not (round 1 of work item 1791270162, red 2). The frozen
    splitter has taken the quotes off, so a quoted `>` reads as an operator
    too, and the cost is a stop: a path quoted as `"> f"` after `--` is no
    path here."""
    out, skip = [], False
    for word in words:
        if skip:
            skip = False
        elif "<" in word or ">" in word:
            at = min(word.find(c) for c in "<>" if c in word)
            head = word[:at]
            head = head[:-1] if head.endswith("&") else head
            if head and not head.isdigit() and not head.startswith("{"):
                out.append(head)
            skip = word[at:] in _OPERATORS
        else:
            out.append(word)
    return out


def _restores(args) -> bool:
    """Whether a `checkout`'s words carry a `--` with a path after it.

    A restore by construction (`git checkout -- f`, `git checkout x -- f`):
    git reads every word after `--` as a path and moves no branch. A `--`
    with nothing after it says only that the name before it is no file, and
    git switches to it, so it does not count, and neither does a redirection
    after it: `git checkout x -- >/dev/null` hands git `x --`. A redirection
    written apart from its target takes the next word with it."""
    return "--" in args and bool(_plain_words(args[args.index("--") + 1 :]))


# The subcommands whose listing rests on the first word after them, and the
# word that moves a branch or adds a worktree there.
_DECIDED_BY = {"worktree": "add", "stash": "branch"}


def _hidden_mover(sub, args) -> str:
    """The redirection that hides `worktree add` or `stash branch` from the
    frozen reading, or "" where none does.

    The frozen reading takes the first word that is no option as the one
    that decides, and a redirection can stand there: `git worktree
    2>/dev/null add` and `git worktree add>/dev/null` create a worktree under
    bash, and `git stash 2>/dev/null branch x` takes a branch. So where the
    first word bash hands git is the deciding word and the frozen first word
    is not, the redirection hid it. `git worktree list>/dev/null` and `git
    stash 2>/dev/null` hide nothing. An `&`-led operator cuts the segment
    before it reaches here, and `_merged_findings` reads that group whole."""
    moving = _DECIDED_BY.get(sub)
    if moving is None:
        return ""
    frozen = [a for a in args if not a.startswith("-")][:1]
    handed = [w for w in _plain_words(args) if not w.startswith("-")][:1]
    if handed != [moving] or frozen == [moving]:
        return ""
    return next((w for w in args if "<" in w or ">" in w), moving)


def _rebase_names_a_branch(args) -> bool:
    """Whether a `rebase`'s words can name the branch it switches to first.

    `git rebase <upstream> <branch>`, `git rebase --onto <a> <b> <branch>`
    and `git rebase --root <branch>` run `git switch <branch>` before
    anything else, and HEAD stays there (git-rebase(1); executed on git
    2.50.1 in round 1 of work item 1791270162, red 3). Read without an
    option table, so an option's value counts as a word, and the cost lands
    on the side of a stop: `git rebase --onto main x` stops too.

    A word is dropped only where git reads it as an option. A lone `-` is
    `@{-1}`, and every word after a `--` is a revision whatever it starts
    with, so `git rebase - feature/x` and `git rebase -- main -x` each switch
    and count two words (git 2.50.1; round 2 of work item 1791270162, red
    1). `@{-1}` starts with no `-` and always counted.

    git has a second word that ends its options, `--end-of-options`, which it
    takes only spelled whole, and it takes any unambiguous prefix of a long
    option: `--ro` and `--roo` are `--root`, while `--r` is ambiguous and git
    refuses it. `--root` is the one option of `git rebase -h` that changes how
    many words name a branch, and it is read off the words once their
    redirections are off (`_plain_words`), so `--root>/dev/null` is `--root`
    too. Those are the words bash hands git except where a word holds a brace
    expansion, which bash makes other words of first (`--ro{,}` is `--ro
    --ro`); such a segment is unrecognised before this is asked (#856). An
    option taking a value counts its value as a word, as above (git 2.50.1;
    #854, round 3 of work item 1791270162, yellow 1)."""
    words = _plain_words(args)
    end = next(
        (i for i, w in enumerate(words) if w in ("--", "--end-of-options")),
        len(words),
    )
    plain = [w for w in words[:end] if w == "-" or not w.startswith("-")]
    plain += words[end + 1 :]
    root = any(w.startswith("--ro") and "--root".startswith(w) for w in words[:end])
    return len(plain) >= (1 if root else 2)


def _git_finding(tokens, parsed, braced=False):
    """(shape, finding) for a segment the frozen reading reads as git.

    BRACED is whether the command the segment comes from holds an unquoted
    brace expansion (`_unquoted_brace`). Where it does and one of the
    segment's words holds one, the words the frozen reading read are not the
    words git reads, so the segment is unrecognised whatever it reads as
    (#856, the owner's answer (c) of 2026-10-08): `git rebase
    {main,feature/x}` is `git rebase main feature/x` to git, and `git
    worktree {add,} ../wt f` a creation. A switch and a creation keep their
    own rules."""
    sub, args, _chdirs = parsed
    words = _spoken(tokens)
    if cmdline.adds_a_worktree(tokens):
        return "creation", None
    if sub == "switch":
        return "switch", None
    if braced and any(_BRACE_IN_WORD.search(t) for t in tokens):
        return "unrecognised", Finding("brace", words)
    hidden = _hidden_mover(sub, args)
    if hidden:
        return "unrecognised", Finding("redirection", words, hidden)
    if sub == "worktree":
        return "listed", None
    if sub == "checkout":
        if _restores(args):
            return "listed", None
        return "unrecognised", Finding("checkout", words)
    if sub == "stash" and [a for a in args if not a.startswith("-")][:1] == ["branch"]:
        return "unrecognised", Finding("unlisted", words, "stash branch")
    if sub == "rebase" and _rebase_names_a_branch(args):
        return "unrecognised", Finding("rebase", words)
    if sub in LEAVES_THE_TREE:
        return "listed", None
    # W3 of the work item: the frozen reading takes a redirection written
    # after `git` for the subcommand (`git 2>/dev/null status`, `git
    # switch>/dev/null x`), so it reaches here as one no list holds. Its
    # plain spelling is the redirection moved to the end.
    if "<" in sub or ">" in sub:
        return "unrecognised", Finding("redirection", words, sub)
    return "unrecognised", Finding("unlisted", words, sub)


def _eval_text(tokens) -> str:
    """The text `eval` would run, or "" where TOKENS is no `eval`.

    `hooks/cmdline.py#command_strings` returns no string for `eval "git
    switch x"` (W3 of work item 1791270162), so the word is found the way the
    commit gate's `_eval_argument` finds it: `command_word`, past a
    redirection on the second reading, and past `builtin`."""
    for redirections in (False, True):
        word, _unplaced = wide.command_word(list(tokens), "eval", redirections)
        while word and os.path.basename(word[0]) == "builtin":
            word = word[1:]
        if word and word[0] == "eval":
            return " ".join(word[1:])
    return ""


def _wide_git(tokens):
    """The wider reader's git reading of TOKENS, or of TOKENS with a
    redirection glued to a word's end cut off, or None."""
    return wide.parse_git(tokens) or wide.parse_git(wide.unglued(tokens) or [])


def _hidden_in(tokens):
    """The finding in a segment the frozen reading does NOT read as git.

    A string handed to a shell holding the bare word `git` (`sh -c`, `bash
    -c`, `eval`, `env -S`, the class #732 names), or a git the wider reader
    reads and the frozen one does not, which is a git behind a redirection or
    a zsh precommand word (the class candidate C read). A program that runs
    git from inside itself (`python3 -c`, `make`, a script) is not read, as
    it never was. Where the wider reader did not load, or raises, the bare
    word alone is the finding."""
    if not _holds_git(" ".join(tokens)):
        return None
    words = _spoken(tokens)
    if wide is None:
        return Finding("unread", words)
    try:
        if any(_holds_git(t) for t in wide.reparsed_texts(tokens)) or _holds_git(
            _eval_text(tokens)
        ):
            return Finding("string", words)
        if _wide_git(tokens):
            return Finding("hidden", words)
    except (Exception, SystemExit):
        return Finding("unread", words)
    return None


def _segment_finding(tokens, braced=False):
    """(shape, finding) for one segment; (None, None) where there is none.

    A brace in any word of a segment the frozen reading reads as no git is
    the brace shape too, on the test `_git_finding` uses for a git segment
    (the reframe of work item 1791384157 after round 3). Nothing about the
    brace is read: not what bash makes of it, and not where it stands. Rounds
    1-3 each read a little more of that (the command word's alternatives,
    every word up to the command word, a runner's operand) and each round
    found the next spelling bash builds `git` from (`{env,} git switch x`,
    `2>&1 {git,} switch x`), so the guard stops on the brace instead, as on
    every shape it does not recognise."""
    parsed = parse_git(tokens)
    if parsed:
        return _git_finding(tokens, parsed, braced)
    if braced and any(_BRACE_IN_WORD.search(t) for t in tokens):
        return "unrecognised", Finding("brace", _spoken(tokens))
    finding = _hidden_in(tokens)
    return ("unrecognised", finding) if finding else (None, None)


def shape_of(tokens, braced=False):
    """ "listed", "switch", "creation", "unrecognised" or None for one segment
    of the frozen walk (`spec.md` In 1 of work item 1791270162).

    A segment the frozen reading reads as git is listed where its subcommand
    is in `LEAVES_THE_TREE`, or is a `checkout` with a path after `--`, or a
    `worktree` that adds none; a switch where its subcommand is `switch`; a
    creation where it adds a worktree; and unrecognised otherwise, or where
    BRACED and one of its words holds a brace expansion (#856). A segment it
    does not read as git is unrecognised where it hands a shell a string
    holding `git` or hides a git from the frozen reading, and None otherwise.
    A substitution body is read at the command's level, where its quoting is
    still there to read (`_command_findings`)."""
    return _segment_finding(tokens, braced)[0]


def _merged_findings(items, braced=False):
    """[(first, finding, tokens)] for a git a redirection's `&` cut out of its
    own segment (`2>&1 git switch x`), read whole by `merged_view`.

    FIRST is the index of the group's first part and TOKENS its glued words:
    the group is one command, run where its first part runs, so its tree is
    the one its own `-C` names from there, wherever the cut fell. The last
    part's tokens carry no `-C` (`2>&1 git -C W switch x` ends `1 git -C W
    switch x`, which neither reading reads as git, and `git -C W worktree
    &>/dev/null add ../wt b` ends `>/dev/null add ../wt b`), and placing a
    group by them judged it in the tree it was typed from (round 2 of work
    item 1791270162, red 2).

    A group with a part the frozen reading reads as git is that part's where
    the part is a switch, a creation or unrecognised: `git checkout .
    &>/dev/null` is the frozen `checkout`'s finding. Where every such part is
    listed, the group is read again whole through the same shapes, because
    the cut can take the word the listing rests on: `git worktree &>/dev/null
    add ../wt b` is `git worktree` to the frozen reading and a creation to
    bash. `git status &>/dev/null` is listed either way.

    BRACED is the command's `_unquoted_brace`, as `_git_finding` reads it.

    Where `hooks/cmdline.py` did not load, or a reader in it raises, the cut
    is the finding (`_cut_unread`)."""
    if wide is None:
        return _cut_unread(items)
    out = []
    try:
        for parts, toks in wide.merged_view(items):
            frozen = [(p, parse_git(items[p][1])) for p in parts]
            frozen = [(p, parsed) for p, parsed in frozen if parsed]
            if frozen:
                if any(
                    _git_finding(items[p][1], f, braced)[0] != "listed"
                    for p, f in frozen
                ):
                    continue
                # The group's subcommand is the listed part's own, so the
                # whole can only differ by the word the cut took: a switch or
                # a creation would have been one before the cut too.
                parsed = wide.parse_git(toks)
                finding = _git_finding(toks, parsed, braced)[1] if parsed else None
                if finding is not None:
                    out.append((parts[0], finding, toks))
                continue
            if _wide_git(toks):
                out.append((parts[0], Finding("hidden", _spoken(toks)), toks))
    except (Exception, SystemExit):
        return _cut_unread(items)
    return out


def _cut_unread(items):
    """[(index, finding, tokens)], `_merged_findings`' shape, where the reader
    that glues an `&` cut back is missing or raises: each cut with the bare
    word `git` on either side of it is a finding, so a broken reader costs a
    stop where the tree matters and never a silence
    (`docs/worktree-guard-spec.md` §*Which tree*; round 1 of work item
    1791270162, yellow 4). A background `&` beside a git command stops too
    while the reader is broken, which is the cheaper mistake.

    Each cut is placed by the part before it, which is where it runs and
    where the frozen reading finds a `-C` (`git -C W worktree 2>&1 add …` is
    judged in `W`). A `-C` after the cut (`2>&1 git -C W switch x`) only the
    broken reader could read, so that cut is judged in the tree it was typed
    from: a named limit (§*Known limits*; round 2 of work item 1791270162,
    yellow 3)."""
    out = []
    for index, (sep, tokens) in enumerate(items):
        if index and sep == "&":
            before = items[index - 1][1]
            text = " ".join([*before, "&", *tokens])
            if _holds_git(text):
                out.append((index - 1, Finding("unread", text), before))
    return out


def _command_findings(text, clean, depth=0):
    """The findings TEXT holds as a whole command: a substitution body, read
    through the same shapes (owner's answer P2 (a)), and an untokenizable
    command holding `git` (P4 (a)). TEXT is already a judgment text.

    Where the wider reader did not load, a substitution holding the bare word
    `git` after its opener is the finding, which is the text test."""
    found = []
    if wide is None:
        openers = [text.find(o) for o in _OPENERS if o in text]
        if openers and _holds_git(text[min(openers) :]):
            found.append(Finding("unread", " ".join(text.split())))
    else:
        try:
            bodies = wide.substitution_bodies(text)
        except (Exception, SystemExit):
            bodies = None
            if _holds_git(text):
                found.append(Finding("unread", " ".join(text.split())))
        for body in bodies or ():
            inner = _first_finding_in(body, depth + 1)
            if inner is not None:
                found.append(Finding("body", " ".join(body.split()), inner))
                break
    # A brace counts there too, read off the raw text: the quoting the
    # splitter could not close is the quoting `_unquoted_brace` reads, so an
    # ANSI-C `$'…\'…'` beside `{g..g}it switch x` hid the brace (round 4 of
    # work item 1791384157, white 4).
    if not clean and (_holds_git(text) or _BRACE.search(text)):
        found.append(Finding("untokenizable", " ".join(text.split())))
    return found


def _first_finding_in(body, depth):
    """The first finding a substitution body holds read as a command, or None.

    A body of listed git holds none. A switch or a creation in a body is a
    finding of its own kind, because neither the ladder nor the creation
    rules read it there."""
    if depth > BODY_DEPTH:
        return Finding("unread", " ".join(body.split()))
    text = _judgment_text(body)
    items, clean = _tokenize_with_separators(text)
    # The body's own quoting decides its braces (#856): a body is read where
    # its quotes are still there to read.
    braced = _unquoted_brace(text)
    for _sep, tokens in items:
        shape, finding = _segment_finding(tokens, braced)
        if shape in ("switch", "creation"):
            return Finding(shape, _spoken(tokens))
        if finding is not None:
            return finding
    for _first, finding, _tokens in _merged_findings(items, braced):
        return finding
    for finding in _command_findings(text, clean, depth):
        return finding
    return None


def _finding_tree(tokens, wheres, cwd):
    """The directory an unrecognised shape's verdict is about.

    `worktree_consent.place`'s, which places the segment at the first of the
    frozen walk's directories WHERES and composes the segment's own `-C` as
    the frozen reading reads it. A git only the wider reader reads (`2>/dev/null git -C
    W switch x`) carries a `-C` the frozen reading cannot see, so the wider
    reading's is composed the same way: the shape is judged in `W`, where it
    runs, not in the tree it was typed from. A body or an untokenizable
    command (TOKENS None) is judged in the session's own tree. A string
    handed to a shell (`sh -c 'git -C W switch x'`) is no git to either
    reading, so its own `-C` and `cd` are not read and it is judged in the
    tree it was typed from: a named limit (`docs/worktree-guard-spec.md`
    §*Known limits*; round 1 of work item 1791270162, yellow 5)."""
    if tokens is None:
        return cwd
    here, target = worktree_consent.place(tokens, wheres, cwd)
    if parse_git(tokens) is None and wide is not None:
        try:
            parsed = _wide_git(tokens)
        except (Exception, SystemExit):
            parsed = None
        if parsed and parsed[2]:
            return apply_chdir(here, parsed[2])
    return target


def _finding_trees(finding, tokens, wheres, cwd):
    """Every directory an unrecognised shape's verdict is about.

    `_finding_tree`'s one, and for a brace segment also every tree its `-C
    <dir>` word pairs name: each pair alone, and the pairs composed in order
    as git composes them, onto the directory the segment is placed in.
    `{git,} -C W switch x`, `{env,} git -C W switch x` and `git {,} -C W
    switch x` are judged in the session's tree AND in `W`, and `{git,} -C ..
    -C W switch x` in `../W`, because which word bash makes the command or
    the subcommand of is the thing the guard does not read, in a segment the
    frozen reading reads as git or not (the reframe of work item 1791384157,
    In 5, S20; round 4, yellow 1: `git {,} -C W` is git to the frozen reading
    with `{,}` for its subcommand, so its `-C` was never composed). More
    trees is the stopping direction. The pair is two plain words, `-C` and
    the word after it, the way `cmdline_base.parse_git` reads a git
    segment's `-C`; a glued `-C<dir>` is read by neither. A `-C` a brace
    hides (`{git,} {-C,} W switch x`) is not read, the named limit a string
    handed to a shell already has."""
    trees = [_finding_tree(tokens, wheres, cwd)]
    if tokens is None or getattr(finding, "kind", None) != "brace":
        return trees
    here, _target = worktree_consent.place(tokens, wheres, cwd)
    chdirs = []
    for at, word in enumerate(tokens[:-1]):
        if word == "-C":
            chdirs.append(tokens[at + 1])
            trees.append(apply_chdir(here, [tokens[at + 1]]))
            trees.append(apply_chdir(here, list(chdirs)))
    return trees


def _sessions(top, session_id, seen):
    """`sessions_in_tree(top)`, read once per command (W2)."""
    key = ("sessions", top)
    if key not in seen:
        seen[key] = sessions_in_tree(top, session_id)
    return seen[key]


def _changes(eff_cwd, seen):
    """`tracked_changes(eff_cwd)`, read once per command (W2)."""
    key = ("changes", eff_cwd)
    if key not in seen:
        seen[key] = tracked_changes(eff_cwd)
    return seen[key]


def tree_matters(top, session_id, eff_cwd, seen=None):
    """(matters, active, idle, reliable, entries) for the tree at TOP.

    It matters where §A rows 1-4 would speak about a switch: another session
    ACTIVE or IDLE, detection unusable, or tracked changes at EFF_CWD. The
    changes are read only where the sessions did not already decide it, and
    ENTRIES is None where they were not read. SEEN carries both reads to the
    ladder, so a command holding an unrecognised shape and a switch in one
    tree reads each once (W2)."""
    seen = {} if seen is None else seen
    active, idle, reliable = _sessions(top, session_id, seen)
    if active or idle or not reliable:
        return True, active, idle, reliable, None
    entries = _changes(eff_cwd, seen)
    return bool(entries), active, idle, reliable, entries


def automation_pressed(top, session, transcript_path):
    """True when this session's person pressed `automation`, read from TOP.

    The reader and its wrapping are the commit gate's
    (`hooks/commit-review-gate.py#automation_pressed`): `top` is the root of
    the session's OWN directory, because the question is whether anybody is
    at the keyboard, and every way of not reading the press is False, which
    costs an `ask` where the opposite would cost a deny nobody can answer.
    The consent RECORD is not read: a creation having run says nothing about
    who is at the keyboard (`spec.md` In 3, S7)."""
    if not session or not top:
        return False
    try:
        return (
            worktree_consent.automation_answered(top, session, transcript_path or "")
            is True
        )
    except Exception:
        return False


def _described(finding):
    """(what, plain) for FINDING in this session's language: what the guard
    read, and the plain spelling it reads instead (`spec.md` In 3, W1)."""
    kind, detail = finding.kind, finding.detail
    if kind == "checkout":
        return (
            tr(
                "a `git checkout` with no `-- <path>`, which can switch a branch "
                "as well as restore a file",
                "`-- <path>` 가 없는 `git checkout` 이라, 파일을 되돌릴 수도 있지만 "
                "브랜치를 전환할 수도 있습니다",
            ),
            tr(
                "For a switch, write `git switch <branch>` or `git switch --detach "
                "<rev>`; for a restore, `git checkout -- <path>` or `git restore "
                "<path>`.",
                "전환이라면 `git switch <branch>` 나 `git switch --detach <rev>` 로, "
                "파일 되돌리기라면 `git checkout -- <path>` 나 `git restore <path>` "
                "로 쓰세요.",
            ),
        )
    if kind == "rebase":
        return (
            tr(
                "a `git rebase` naming a branch, which git switches to before it "
                "rebases",
                "브랜치를 지정한 `git rebase` 이며, git 은 리베이스하기 전에 그 "
                "브랜치로 전환합니다",
            ),
            tr(
                "Write `git switch <branch>` first, then `git rebase <upstream>`.",
                "먼저 `git switch <branch>` 를 실행한 뒤 `git rebase <upstream>` 을 "
                "쓰세요.",
            ),
        )
    if kind == "unlisted":
        return (
            tr(
                f"`git {detail}` is not on the list of subcommands known to leave "
                f"the branch where it is",
                f"`git {detail}` 는 브랜치를 그대로 둔다고 확인된 하위 명령 목록에 "
                f"없습니다",
            ),
            tr(
                "Nothing spells it more plainly, so run it in another clone with "
                "`git -C <scratch clone>`, or after the other session ends and the "
                "changes are committed.",
                "더 평범하게 쓸 방법이 없는 명령이므로 `git -C <scratch clone>` 으로 "
                "다른 클론에서 실행하거나, 다른 세션이 끝나고 변경을 커밋한 뒤에 "
                "실행하세요.",
            ),
        )
    if kind == "redirection":
        return (
            tr(
                f"a redirection (`{detail}`) written where git reads its subcommand",
                f"git 이 하위 명령을 읽는 자리에 리다이렉션(`{detail}`)이 있습니다",
            ),
            tr(
                "Write it after the command's own words, as in `git <subcommand> … "
                "2>/dev/null`.",
                "리다이렉션은 명령의 단어들 뒤에 쓰세요. 예: `git <subcommand> … "
                "2>/dev/null`.",
            ),
        )
    if kind == "brace":
        return (
            tr(
                "a word holding a brace expansion (`{a,b}`, `{1..3}`), which the "
                "shell turns into other words before the command runs, so this "
                "guard cannot tell which command that is",
                "중괄호 확장(`{a,b}`, `{1..3}`)이 든 단어이며, 셸은 명령이 실행되기 "
                "전에 이를 다른 단어들로 바꾸므로 이 guard 는 어떤 명령인지 알 수 "
                "없습니다",
            ),
            tr(
                "Write the words out as the shell would make them, as in `git "
                "rebase main feature/x` for `git rebase {main,feature/x}`, or quote "
                "the braces where they are meant literally.",
                "셸이 만들 단어를 직접 풀어 쓰세요. 예: `git rebase {main,feature/x}` "
                "대신 `git rebase main feature/x`. 중괄호를 글자 그대로 쓰려면 "
                "따옴표로 감싸세요.",
            ),
        )
    if kind == "string":
        return (
            tr(
                "a git command inside a string handed to a shell (`sh -c`, `bash "
                "-c`, `eval`, `env -S`)",
                "셸에 문자열로 넘긴 git 명령입니다(`sh -c`, `bash -c`, `eval`, "
                "`env -S`)",
            ),
            tr(
                "Run the git command itself rather than as a string: `git switch "
                "<branch>`, not `sh -c 'git switch <branch>'`.",
                "문자열로 넘기지 말고 git 명령을 직접 실행하세요. `sh -c 'git switch "
                "<branch>'` 가 아니라 `git switch <branch>` 입니다.",
            ),
        )
    if kind == "hidden":
        return (
            tr(
                "a git command behind a redirection or a zsh precommand word "
                "(`2>/dev/null git …`, `noglob git …`, `repeat N git …`)",
                "리다이렉션이나 zsh 가 명령 앞에 붙이는 단어(`noglob`, `repeat N` 등) 뒤에 놓인 "
                "git 명령입니다(`2>/dev/null git …`, `noglob git …`)",
            ),
            tr(
                "Write `git` first and any redirection last, as in `git switch "
                "<branch> 2>/dev/null`.",
                "`git` 을 맨 앞에, 리다이렉션은 맨 뒤에 쓰세요. 예: `git switch "
                "<branch> 2>/dev/null`.",
            ),
        )
    if kind == "untokenizable":
        return (
            tr(
                "a command this guard could not split into words, such as one with "
                "an unclosed quote or here-document",
                "따옴표나 here-document 가 닫히지 않아 이 guard 가 단어로 나누지 못한 "
                "명령입니다",
            ),
            tr(
                "Split it into commands that each read on their own, and write a "
                "commit message to a file and pass it with `git commit -F <file>`.",
                "각각 따로 읽히는 명령으로 나누고, 커밋 메시지는 파일에 써서 "
                "`git commit -F <file>` 로 넘기세요.",
            ),
        )
    if kind == "switch":
        return (
            tr(
                "a `git switch`, which the branch-switch rules read only where it "
                "is a command of its own",
                "`git switch` 이며, 브랜치 전환 규칙은 그 자체로 실행되는 명령만 "
                "읽습니다",
            ),
            tr("Run `git switch …` on its own.", "`git switch …` 만 따로 실행하세요."),
        )
    if kind == "creation":
        return (
            tr(
                "a `git worktree add`, which the worktree rules read only where it "
                "is a command of its own",
                "`git worktree add` 이며, worktree 규칙은 그 자체로 실행되는 명령만 "
                "읽습니다",
            ),
            tr(
                "Run `git worktree add …` on its own.",
                "`git worktree add …` 만 따로 실행하세요.",
            ),
        )
    return (
        tr(
            "a git command in a place only this guard's wider reader reads (a "
            "string handed to a shell, a substitution, or behind a redirection), "
            "and that reader could not run",
            "이 guard 의 넓은 읽기만 읽는 자리(셸에 넘긴 문자열, 치환, 리다이렉션 "
            "뒤)에 있는 git 명령인데, 그 읽기가 실행되지 못했습니다",
        ),
        tr(
            "Write each git command plainly, as a command of its own.",
            "git 명령을 하나씩 그 자체로 평범하게 쓰세요.",
        ),
    )


def _item(finding):
    """One line of the stop: the shape read, what it is, its plain spelling.

    A body names the innermost shape it holds, with that shape's own plain
    spelling, and says to run it outside the substitution (P2 (a))."""
    inside = False
    while finding.kind == "body":
        finding, inside = finding.detail, True
    what, plain = _described(finding)
    words = finding.words if len(finding.words) <= 120 else finding.words[:117] + "..."
    if inside:
        what = (
            tr(
                "inside a `$( … )`, backtick or `<( … )` body, ",
                "`$( … )`·백틱·`<( … )` 안에서 실행되는 명령으로, ",
            )
            + what
        )
        plain += tr(
            " Run it on its own, outside the substitution.",
            " 치환 밖에서 그 명령만 따로 실행하세요.",
        )
    return f"  · `{words}` — {what}. {plain}"


# How many shapes one stop lists before it counts the rest.
STOP_ITEMS = 5


def stop_unrecognised(findings, trees, pressed, before_ask=None, switch_on_line=False):
    """Stop on FINDINGS -- the unrecognised shapes, first one first -- where
    TREES, `[(top, (active, idle, reliable, entries))]`, are the trees on the
    line that matter, each once, first one first.

    The reason describes each of them, because approving the `ask` runs the
    line in every one: a second tree's IDLE sessions or unusable detection
    is shown beside the first tree's changes, not hidden behind them (round
    2 of work item 1791270162, yellow 4). Where one is ACTIVE the stop is a
    `deny` that nobody approves, and the reason describes the ACTIVE trees
    alone. Where one tree is described, the reason calls it "this tree" and
    reads as it did before.

    One reason text with two readers (`spec.md` In 3): a `deny` to the model
    where the person pressed `automation`, which rewrites in the plain
    spelling and meets today's rows on the retry, and an `ask` otherwise. In
    a tree another session is ACTIVE in it is a `deny` either way:
    `docs/worktree-guard-spec.md` §A row 1 denies a branch-form `checkout`
    there with nobody asked, and an `ask` would let one approval take the
    branch out from under that session. Every shape on the line is listed,
    so one rewrite answers all of them.

    BEFORE_ASK runs on the `ask` path only, for the reason `choose` gives
    its own: the deny stops the whole line, while approving an ask runs every
    segment of it, so a creation on the same line is judged first
    (`test_the_guard_is_never_silent_where_the_writer_records`). A
    `git switch` on the line (SWITCH_ON_LINE) makes the stop a `deny` for
    the same reason: approving would run the switch past §A's rows, in a
    tree this reason does not describe (round 1 of work item 1791270162,
    red 1), and the reason says to run the switch on its own."""
    held = [tree for tree in trees if tree[1][0]]
    described = held or trees
    active = bool(held)
    whys = []
    for top, (busy, idle, reliable, entries) in described:
        if busy:
            why = (
                tr(
                    "another Claude session is actively working here.\n",
                    "다른 Claude 세션이 이 트리에서 작업 중입니다.\n",
                )
                + fmt_sessions(busy)
                + "\n"
            )
        elif idle:
            why = (
                tr(
                    "other Claude sessions may be here, and none of them can be "
                    "shown to be working.\n",
                    "이 트리에 다른 Claude 세션이 있을 수 있고, 작업 중인지 확인되지 "
                    "않습니다.\n",
                )
                + fmt_sessions(idle)
                + "\n"
            )
        elif not reliable:
            why = tr(
                "whether another session works here cannot be told in this "
                "environment (process inspection is unavailable).\n",
                "이 환경에서는 프로세스를 조회할 수 없어, 다른 세션이 이 트리에서 "
                "작업 중인지 확인할 수 없습니다.\n",
            )
        else:
            n = len(entries or ())
            why = tr(
                f"it has {n} uncommitted tracked changes, which a switch would "
                f"carry onto the other branch.\n",
                f"커밋되지 않은 추적 파일 변경이 {n}건 있고, 전환하면 이 변경이 "
                f"다른 브랜치로 따라갑니다.\n",
            )
        whys.append((top, why))
    if len(whys) == 1:
        where = tr(
            "in this tree a branch switch would matter: ",
            "이 트리에서는 브랜치 전환이 문제가 됩니다. ",
        )
        why = whys[0][1]
    else:
        where = tr(
            "in each of these trees a branch switch would matter:\n",
            "아래 트리마다 브랜치 전환이 문제가 됩니다.\n",
        )
        why = "".join(f"  `{top}`: {why}" for top, why in whys)
    lines, listed = [], set()
    for finding in findings:
        line = _item(finding)
        if line not in listed:
            listed.add(line)
            lines.append(line)
    shown = lines[:STOP_ITEMS]
    if len(lines) > len(shown):
        more = len(lines) - len(shown)
        shown.append(tr(f"  · and {more} more", f"  · 그 밖에 {more}개"))
    decision = "deny" if pressed or active or switch_on_line else "ask"
    if decision == "ask" and before_ask is not None:
        before_ask()
    ending = (
        tr(
            "Re-issue the command in a plain spelling.",
            "평범한 표기로 다시 실행하세요.",
        )
        + (
            tr(
                " Run the `git switch` as a command of its own, so the "
                "branch-switch rules judge its tree.",
                " `git switch` 는 따로 실행해 브랜치 전환 규칙이 그 트리를 "
                "판단하게 하세요.",
            )
            if switch_on_line
            else ""
        )
        if decision == "deny"
        else tr(
            "Approve to run it as written, or decline and re-issue it in a plain "
            "spelling.",
            "그대로 실행하려면 승인하고, 아니면 거부한 뒤 평범한 표기로 다시 "
            "실행하세요.",
        )
    )
    respond(
        decision,
        tr(
            "This command holds a git command this guard does not know to leave "
            "the branch where it is, and ",
            "이 명령에는 브랜치를 그대로 둔다고 이 guard 가 확인하지 못한 git "
            "명령이 있고, ",
        )
        + where
        + why
        + "\n"
        + "\n".join(shown)
        + "\n\n"
        + tr(
            "The plain spellings are what this guard reads: a `git switch` then "
            "meets the branch-switch rules, and a git subcommand on the list "
            "passes. Name another tree with `git -C <dir>`. The list is "
            "`LEAVES_THE_TREE` in hooks/worktree-guard.py. ",
            "이 guard 는 위의 평범한 표기를 읽습니다. `git switch` 는 브랜치 전환 "
            "규칙으로 판단하고, 목록에 있는 git 하위 명령은 그대로 통과합니다. "
            "다른 트리는 `git -C <dir>` 로 지정하세요. 목록은 "
            "hooks/worktree-guard.py 의 `LEAVES_THE_TREE` 입니다. ",
        )
        + ending,
    )


def main():
    data = load_input()
    tool = data.get("tool_name", "")
    cwd = data.get("cwd") or os.getcwd()
    tool_input = data.get("tool_input", {}) or {}

    # 하네스가 관리하는 worktree(Agent/Task `isolation: "worktree"`)는 Bash를 거치지
    # 않고 <repo>/.claude/worktrees/<name> 에 바로 생성되므로 툴 호출에서 잡는다.
    #
    # This path counts nothing (#8). An isolated agent runs BESIDE this
    # session while this session's tree stays where it is, so the call is two
    # work streams by construction -- the concurrency
    # `docs/worktree-guard-spec.md` §Premise counts. Counting Claude sessions
    # cannot see it: a subagent's tool call renews its PARENT's lease and has
    # no id of its own (measured), so an agent in a one-session tree read as
    # single-stream. The verdict that reading produced told the model to call
    # the Agent again without isolation, which puts the agent in the parent's
    # tree while the parent works there -- the mixing this guard exists to
    # stop. So there is no `sessions_in_tree` call and no choice site here.
    #
    # Two outcomes. Consent -- the record or the routing answer -- is silence,
    # for the reason the `granted` block in `guard_worktree_creation` gives
    # for a compound: this call is a creation PLUS an agent with a prompt, and
    # consent answers the first half only. Otherwise one confirmation, which is
    # #237's floor for the first creation of a session, unmoved.
    #
    # No token is read, deliberately. The Agent's prompt is prose, and prose
    # cannot separate "the user asked for a worktree" from a sentence that
    # merely mentions the token -- a prompt discussing it switched the guard
    # off, and one apostrophe in a prompt that DID carry it dropped the call
    # onto a deny telling it to add the token it already had. The answer here
    # is an `ask` either way, so the token would buy nothing.
    if tool in ("Agent", "Task"):
        if str(tool_input.get("isolation", "")).lower() != "worktree":
            sys.exit(0)
        top, _ = repo_paths(cwd)
        # The same refusal `guard_worktree_creation` opens with: no repository,
        # no tree to separate.
        if not top:
            sys.exit(0)
        if worktree_consent.consent(
            top, data.get("session_id", ""), data.get("transcript_path", "") or ""
        ):
            sys.exit(0)
        respond(
            "ask",
            tr(
                'The Agent tool was called with isolation: "worktree" (the harness '
                "creates a worktree at <repo>/.claude/worktrees/<name>). The agent "
                "runs beside this session, so it is concurrent work and a separate "
                "tree is the right shape for it. Creating a worktree still takes "
                "the user's confirmation once per session. Declining cancels this "
                "spawn.",
                'Agent 툴을 isolation: "worktree" 로 호출했습니다(하네스가 '
                "<repo>/.claude/worktrees/<name> 에 worktree 를 만듭니다). 이 agent 는 "
                "이 세션과 나란히 돌기 때문에 동시 작업이고, 별도 트리가 맞는 "
                "모양입니다. 다만 worktree 생성은 세션마다 한 번 사용자 확인을 "
                "거칩니다. 거부하면 이번 호출이 취소됩니다.",
            ),
        )

    if tool != "Bash":
        sys.exit(0)
    command = tool_input.get("command", "") or ""
    # Hoisted above the walk: both silent exits below now have a creation to
    # judge before they take, and each of them needs it.
    session_id = data.get("session_id", "")
    transcript_path = data.get("transcript_path", "") or ""

    # The FIRST switch-kind segment and the FIRST creation, in whichever order
    # they are written. A command carrying both is judged by the switch
    # ladder, with the creation hooked in where that ladder already takes it
    # (`choose`'s `before_ask`, and the `judge_creation` call above row 3).
    #
    # Keeping the first verdict of either kind was the walk before #620, and
    # it was two defects of one cause. A creation written BEHIND a switch got
    # no verdict, while `hooks/worktree_consent.py` reads every segment and
    # recorded consent for it anyway -- `judge_creation` holds that
    # measurement. A switch written behind a creation got none either: the
    # creation took the verdict, consent made it silent for a compound, and
    # `git worktree add ../x -b x && git switch y` ran the switch over a tree
    # another session was ACTIVE in. `docs/worktree-guard-spec.md`
    # §*Creation consent* says consent never reaches the switch direction.
    #
    # Only the first of each kind, which is what the writer records for a
    # creation. A switch in a second tree or a creation in a second clone is
    # still judged on the first (#630).
    #
    # Since #826 the walk keeps a third kind beside them, the first
    # unrecognised shape and the tree its segment names, and every other
    # unrecognised shape on the line for the stop's text (`shape_of`). Each
    # kind is read from the frozen reading's words alone, so a listed shape
    # costs no spawn: the tree is read for the first of a kind, in its
    # segment's first directory, as the switch's always was. Whether the
    # command holds an unquoted brace expansion is read once, off its text,
    # because the frozen words carry no quotes (#856, `_unquoted_brace`).
    judged = _judgment_text(command)
    items, clean = _tokenize_with_separators(judged)
    walked = cmdline.walk_directories(items, cwd)
    braced = _unquoted_brace(judged)
    switch_at = None
    creation_at = None
    unrecognised = []
    for index, (tokens, wheres) in enumerate(walked):
        shape, finding = _segment_finding(tokens, braced)
        if shape not in ("switch", "creation") and finding is None:
            continue
        # Placed by `worktree_consent.place`, the one placement the consent
        # writer files a creation by (#868).
        if shape == "switch":
            if switch_at is None:
                switch_at = worktree_consent.place(tokens, wheres, cwd)[1]
        elif shape == "creation":
            if creation_at is None:
                creation_at = worktree_consent.place(tokens, wheres, cwd)[1]
        else:
            unrecognised.append((index, finding, tokens, wheres))
    # A cut group is placed by its own words, from the directory its first
    # part runs in (`_merged_findings`).
    for first, finding, tokens in _merged_findings(items, braced):
        unrecognised.append((first, finding, tokens, walked[first][1]))
    # A substitution body and an untokenizable command belong to no one
    # segment, so they are judged in the session's own tree: the fallback
    # #686 gives a directory the walk cannot place, and the stand-in the
    # commit gate judges a body's commit against (`_unresolved_base`).
    unrecognised += [
        (len(walked), finding, None, ()) for finding in _command_findings(judged, clean)
    ]
    unrecognised.sort(key=lambda found: found[0])

    # The stop of `spec.md` In 3, taken before the ladder because it stops
    # the whole line. Only where the tree an unrecognised shape names
    # matters: in a clean tree nobody else is in, §A row 5 says nothing of a
    # switch, and nothing here says more of a shape that might be one. Each
    # shape is judged in the tree its own segment names, first one first, so
    # one in a clean tree takes no stop away from one behind it in a dirty
    # tree (`git checkout README.md && 2>/dev/null git -C W switch x`); each
    # tree is read once, and the stop lists every shape on the line.
    #
    # Every tree is read before the stop is taken, not only the first that
    # matters: approving an `ask` runs every shape on the line, so a shape in
    # a tree another session is ACTIVE in makes the stop a `deny`, as it
    # would be alone (round 1 of work item 1791270162, red 1). Each tree that
    # matters is kept once, and the reason describes every one of them, or
    # the ACTIVE ones where there are any (round 2, yellow 4).
    seen = {}
    placed = set()
    trees = []
    # A brace segment that is not git is judged in more than one tree
    # (`_finding_trees`); the finding is listed once, and each tree is looked
    # up once like any other.
    for _index, found, tokens, wheres in unrecognised:
        for at in _finding_trees(found, tokens, wheres, cwd):
            if at in placed:
                continue
            placed.add(at)
            at_top = repo_paths(at)[0]
            if at_top and at_top not in [top for top, _state in trees]:
                matters, active, idle, reliable, entries = tree_matters(
                    at_top, session_id, at, seen
                )
                if matters:
                    trees.append((at_top, (active, idle, reliable, entries)))
    if trees:
        stop_unrecognised(
            [found[1] for found in unrecognised],
            trees,
            automation_pressed(repo_paths(cwd)[0], session_id, transcript_path),
            before_ask=(
                (
                    lambda: judge_creation(
                        command,
                        cwd,
                        repo_paths(creation_at)[0],
                        session_id,
                        transcript_path,
                    )
                )
                if creation_at
                else None
            ),
            switch_on_line=switch_at is not None,
        )

    # Candidate C's question used to be asked at each silent exit below
    # (#678). The stop above is what replaced it: a git behind a redirection
    # or a zsh precommand word is an unrecognised shape now, judged where the
    # tree matters and silent where it does not, like every other one.
    if switch_at is None and creation_at is None:
        sys.exit(0)
    reason = "switch" if switch_at is not None else "worktree-add"
    eff_cwd = switch_at if switch_at is not None else creation_at

    top, wt_root = repo_paths(eff_cwd)
    # No repository at the effective directory means there is no tree to keep
    # two sessions out of, and git itself will refuse the command. Falling back
    # to `cwd` here was the second half of the measured false deny: with cwd at
    # `$HOME`, the containment test in sessions_in_tree() matches every session
    # on the machine.
    if not top:
        # The guard's OTHER silent exit, and it hides the same escape as the
        # one at the end of the switch ladder. `worktree_consent.place` falls back
        # to the session's own directory, so `top` is empty only when the
        # SHELL is outside any repository -- and a `git -C <repo> worktree
        # add` later in the same command is not. Executed: with the shell in
        # an empty directory, `git switch feature/x && git -C <repo> worktree
        # add ../wt f` was silent here and `hooks/worktree_consent.py`
        # recorded session-wide consent for it, because the writer resolves
        # the creation's OWN directory and finds a repository there.
        if creation_at:
            judge_creation(
                command, cwd, repo_paths(creation_at)[0], session_id, transcript_path
            )
        sys.exit(0)

    if reason == "worktree-add":
        judge_creation(command, cwd, top, session_id, transcript_path)
        sys.exit(0)

    # Read once: the stop's question above may already have read this tree.
    active, idle, reliable = _sessions(top, session_id, seen)
    # The command word for every command this ladder hands back: `-C <top>`
    # where the shell is not in the switch's tree (`git_at`).
    git = git_at(top, cwd)

    # The mirror of [worktree-ok]: the user has just chosen the shared tree,
    # and the token carries that answer back through the guard. Honoured only
    # where the guard's own verdict is "cannot tell" — never over an ACTIVE
    # session (that deny protects a tree this session does not own), and never
    # over the dirty-tree question (which asks something else entirely).
    shared_ok = has_token(command, "[shared-tree-ok]")

    steer = tr(
        f"  # check an existing branch out into a worktree\n"
        f"  {git} worktree add {wt_root}/<branch> <branch>\n\n"
        f"  # or create a new branch off the latest origin/main\n"
        f"  {git} fetch origin\n"
        f"  {git} worktree add {wt_root}/<name> -b <branch> origin/main\n\n"
        "Then work in that folder from a separate Claude Code session. "
        "`git worktree list` shows worktrees.",
        f"  # 기존 브랜치를 worktree로 꺼내기\n"
        f"  {git} worktree add {wt_root}/<branch> <branch>\n\n"
        f"  # 새 브랜치를 최신 origin/main 기준으로 생성 (저장소 정책)\n"
        f"  {git} fetch origin\n"
        f"  {git} worktree add {wt_root}/<name> -b <branch> origin/main\n\n"
        "그런 다음 그 폴더에서 별도의 Claude Code 세션으로 작업하세요. "
        "worktree 목록은 `git worktree list`.",
    )

    switch_or_split = (
        (
            tr('1. "Switch in this shared tree"', '1. "이 공용 트리에서 전환한다"'),
            tr(
                "right when those are forgotten tabs or sessions that have "
                "already ended. Re-issue the SAME command with the token "
                "appended (`… # [shared-tree-ok]`); it carries this answer, so "
                "the switch goes straight through.",
                "잊힌 탭이거나 이미 끝난 세션이면 이쪽이 맞습니다. 같은 명령 뒤에 "
                "토큰을 붙여(`… # [shared-tree-ok]`) 다시 실행하세요. 이 토큰이 "
                "지금 고른 답을 담고 있어 전환이 그대로 통과합니다.",
            ),
        ),
        (
            tr('2. "Split into a worktree"', '2. "worktree 로 분리한다"'),
            tr(
                f"keeps the branch of a session that IS still working. Run "
                f"`{git} worktree add {wt_root}/<branch> <branch>  # [worktree-ok]` "
                f"for a branch that already exists, or "
                f"`{git} worktree add {wt_root}/<name> -b <branch> origin/main  "
                f"# [worktree-ok]` for a new one, then work there from a "
                f"separate session. The token carries this answer, so creating "
                f"it is confirmed rather than questioned again.",
                f"아직 작업 중인 세션의 브랜치를 보존합니다. 이미 있는 브랜치면 "
                f"`{git} worktree add {wt_root}/<branch> <branch>  # [worktree-ok]`, "
                f"새로 만들 브랜치면 `{git} worktree add {wt_root}/<name> -b "
                f"<branch> origin/main  # [worktree-ok]` 를 실행하고, 그 폴더에서 "
                f"별도 세션으로 작업하세요. 이 토큰이 지금 고른 답을 담고 있어 "
                f"생성할 때 다시 묻지 않고 확인만 받습니다.",
            ),
        ),
    )

    # What the two `choose` rows below hand their FALLBACK to, when this
    # command also creates a worktree. `choose` denies once per session per
    # direction and asks on every attempt after; the deny stops the creation
    # with the rest of the line and needs nothing, and the ask is where the
    # creation used to go unjudged. `choose`'s own docstring holds the
    # measurement.
    judge_the_creation = (
        (
            lambda: judge_creation(
                command, cwd, repo_paths(creation_at)[0], session_id, transcript_path
            )
        )
        if creation_at
        else None
    )

    # 1) 같은 작업 트리에서 다른 세션이 '지금' 일하는 중 -> 진짜 다중작업. 차단.
    if active:
        respond(
            "deny",
            (
                tr(
                    "Blocking this branch switch: another Claude session is actively working in "
                    "this tree (switching would land its next edits on an unintended branch).\n",
                    "이 작업 트리에서 다른 Claude 세션이 동시에 작업 중이라 브랜치 전환을 차단합니다 "
                    "(전환하면 상대 세션의 다음 편집이 의도치 않은 브랜치에 떨어집니다).\n",
                )
                + f"{fmt_sessions(active)}\n"
                + f"{fmt_snippet(top, session_id)}\n"
                + tr(
                    "This is concurrent work — take this branch to a separate worktree:\n\n",
                    "다중작업이므로 이 브랜치는 별도 worktree에서 진행하세요:\n\n",
                )
                + steer
            ),
        )

    # 1-b) 살아 있으나 입력이 끊긴 세션뿐 -> 잊힌 탭일 공산. 차단 대신 사용자 판단.
    if idle and not shared_ok:
        choose(
            top,
            session_id,
            "switch",
            (
                tr(
                    f"Other Claude sessions may exist in this tree, but none of them can be "
                    f"shown to be working: no input or transcript for {IDLE_MIN}+ minutes, or "
                    f"a lease whose owning session cannot be identified.\n",
                    f"이 트리에 다른 Claude 세션이 있을 수 있으나, 작업 중임을 확인할 수 있는 것은 "
                    f"없습니다 — {IDLE_MIN}분 이상 활동(키 입력·작업 기록)이 없거나, lease 를 남긴 "
                    f"세션이 누구인지 확인되지 않습니다.\n",
                )
                + f"{fmt_sessions(idle)}\n"
                + f"{fmt_snippet(top, session_id)}\n"
            ),
            tr(
                "No session here can be shown to be working — switch in this "
                "shared tree, or split into a worktree?",
                "작업 중임이 확인되는 세션이 없습니다 — 이 공용 트리에서 전환할까요, "
                "worktree 로 분리할까요?",
            ),
            switch_or_split,
            tr(
                "Your call:\n"
                "  · Approve — switch branches in this shared tree (right when those are "
                "forgotten tabs or sessions that have already ended).\n"
                "  · Deny — the switch is cancelled; split into a worktree instead so a "
                "session that IS still working keeps its branch:\n\n",
                "선택해 주세요:\n"
                "  · 승인 — 이 공용 트리에서 그대로 브랜치를 전환합니다(잊힌 탭이거나 이미 끝난 "
                "세션이면 이쪽이 맞습니다).\n"
                "  · 거부 — 전환을 취소하고 worktree 로 분리해, 아직 작업 중인 세션의 브랜치를 "
                "보존합니다:\n\n",
            )
            + steer,
            before_ask=judge_the_creation,
        )

    # 2) 세션 감지 자체가 불가능하면 사용자에게 확인. deny 였으나 확장 호스트처럼
    #    조상 프로세스가 `claude` 로 보이지 않는 환경에서 모든 전환이 막혔다 —
    #    판정 불가의 비용은 사용자가 한 번 확인하는 것으로 충분하다.
    if not reliable and not shared_ok:
        choose(
            top,
            session_id,
            "switch",
            tr(
                "Cannot determine whether other sessions are working in this tree "
                "(process inspection unavailable in this environment).\n",
                "이 트리에서 다른 세션이 작업 중인지 확인할 수 없습니다(이 환경에서는 "
                "프로세스 조회가 불가능합니다).\n",
            ),
            tr(
                "No verdict is possible here — switch in this shared tree, or "
                "split into a worktree?",
                "여기서는 자동 판정이 불가능합니다 — 이 공용 트리에서 전환할까요, "
                "worktree 로 분리할까요?",
            ),
            switch_or_split,
            tr(
                "Your call:\n"
                "  · Approve — switch branches in this shared tree (safe when no "
                "other session is active here).\n"
                "  · Deny — the switch is cancelled; split into a worktree instead "
                "so any concurrent session keeps its branch:\n\n",
                "선택해 주세요:\n"
                "  · 승인 — 이 공용 트리에서 그대로 브랜치를 전환합니다(다른 활성 세션이 "
                "없다면 안전합니다).\n"
                "  · 거부 — 전환을 취소하고 worktree 로 분리해, 동시 세션의 브랜치를 "
                "보존합니다:\n\n",
            )
            + steer,
            before_ask=judge_the_creation,
        )

    # A creation later in the same command has not been judged yet, and this is
    # where it gets its verdict. The three rows above keep their precedence
    # because they ARE the concurrency protections: a switch denied under an
    # ACTIVE session must stay denied, and making a creation outrank it would
    # turn that deny into an `ask` about the creation while the branch is still
    # taken out from under the other session, one approval later.
    #
    # **Only one of those three denies unconditionally.** Rows 1-b and 2 are
    # `choose` sites, whose deny is spent once per session per direction, and
    # their fallback is an `ask` whose approval runs the whole command line --
    # so reaching this line at all was a property of the FIRST attempt. Those
    # two hand their fallback `judge_the_creation` above, which is why they
    # still keep their deny and no longer keep the creation from being judged.
    # `choose`'s docstring holds the measurement; this line is what the two
    # rows below, and a session that never met either `choose`, still reach.
    #
    # The two rows BELOW yield, and neither of them protects a tree. Row 4 says
    # nothing at all, which is where `git switch feature/x && git worktree add
    # ../wt f` ran unjudged on a clean tree and `hooks/worktree_consent.py`
    # minted session-wide consent for it. Row 3 asks about uncommitted changes
    # riding along and its own text says the switch is ALLOWED -- so approving
    # it created the worktree too, and whether the creation was questioned at
    # all came down to whether the tree happened to be dirty. Executed: the
    # same command denied on a clean tree and asked about the changes on a
    # dirty one.
    #
    # The creation's own repository, not this switch's: they are not always the
    # same tree, and `guard_worktree_creation` refuses an empty one.
    if creation_at:
        judge_creation(
            command, cwd, repo_paths(creation_at)[0], session_id, transcript_path
        )

    # 3) 단건이지만 추적 중인 변경이 있으면 사용자에게 확인.
    #
    # Reached in three states, and only the first is a count. Single stream is
    # nothing idle with detection reliable; the other two are only-idle and
    # detection-unusable under `[shared-tree-ok]`, where the choice rows above
    # stood aside because the token carried the user's answer. The lead says
    # which of the two made the switch allowable, and nothing else moves (#624).
    #
    # Read from the tree the switch acts on, the one every row above judged,
    # not from where the shell started: `git -C <repo> switch x` or `cd <repo>
    # && git switch x` from elsewhere carries <repo>'s changes, not the session
    # directory's. Reading `cwd` here left a dirty <repo> silent and asked a
    # clean one about changes that were not going anywhere. The force-staged
    # check runs at that tree's root, `top`, not at `eff_cwd`: porcelain names
    # each path from the root and `check-ignore` reads one from where it runs,
    # so from a subdirectory an anchored pattern named nothing.
    entries = _changes(eff_cwd, seen)
    if entries:
        single_stream = not idle and reliable
        listing = "\n".join(f"    {xy}  {path}" for xy, path in entries)
        phantoms = phantom_entries(entries, top)
        note = ""
        if phantoms:
            why = "\n".join(f"    {p} — {r}" for p, r in phantoms)
            # Always the root, unlike `git_at`: porcelain names each path from
            # the tree's root, so from a subdirectory of the same tree a bare
            # `git restore <path>` names a different file (round 2 of work item
            # 1790550712, finding 1). `git restore` can overwrite a working
            # copy, which is why this one is not left to the shell's position.
            at = f"git -C {shlex.quote(top)}"
            fixes = "\n".join(
                f"    {at} restore --staged {shlex.quote(p)}" for p, _ in phantoms
            )
            note = tr(
                f"\nIndex-only residue invisible in the working tree:\n{why}\n"
                f"These commands clean the tree (run `{at} restore <path>` first to keep "
                f"index-only content):\n{fixes}\n",
                f"\n이 중 워크트리에서는 보이지 않는 index 잔재:\n{why}\n"
                f"아래 명령으로 정리하면 트리가 clean이 됩니다 "
                f"(index에만 존재하는 내용을 살리려면 `{at} restore <path>` 를 먼저 실행):\n{fixes}\n",
            )
        lead = (
            tr("Single-stream tree", "이 트리는 단건 작업이라")
            if single_stream
            else tr(
                "[shared-tree-ok] carries the user's answer to switch in this "
                "shared tree",
                "[shared-tree-ok] 가 공용 트리에서 전환한다는 사용자의 답을 담고 있어",
            )
        )
        respond(
            "ask",
            (
                tr(
                    f"{lead}, so the switch is allowed — but there are "
                    f"{len(entries)} uncommitted tracked changes:\n{listing}\n{note}"
                    f"They will follow you onto the target branch. Confirm to proceed "
                    f"(commit/stash first is recommended).",
                    f"{lead} 브랜치 전환을 허용할 수 있지만, "
                    f"커밋되지 않은 변경 {len(entries)}건이 있습니다:\n{listing}\n{note}"
                    f"전환하면 이 변경이 대상 브랜치로 따라갑니다. 진행할지 확인해 주세요 "
                    f"(커밋/스태시 후 전환을 권장).",
                )
            ),
        )

    # 4) 단건 + clean -> 워크트리 없이 그냥 전환.
    sys.exit(0)


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
