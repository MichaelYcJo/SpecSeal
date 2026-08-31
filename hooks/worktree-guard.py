#!/usr/bin/env python3
"""PreToolUse guard: keep worktrees tied to genuinely CONCURRENT work.

Reads the Claude Code hook JSON on stdin and guards both directions of the same
rule, using one signal -- how many work streams are actually live on this tree.

A) Branch switching (Bash: git checkout/switch of a branch, or a -b/-c variant)

  - ACTIVE Claude session inside THIS working tree -> deny, steer to a worktree
  - only IDLE sessions (no terminal input for a while) -> CHOICE: switch here,
    or split into a worktree -- they are usually forgotten tabs, and the user
    can tell
  - cannot tell (process inspection unusable)       -> the same CHOICE
  - tracked changes present (dirty)                 -> ask the user first; this
    one really is yes/no (the branch is the same either way, and the only
    question is whether the uncommitted changes ride along)
  - otherwise (single work stream, clean)           -> allow the plain switch

B) Worktree creation, whichever path it takes:
     - Bash: `git worktree add ...`
     - Agent/Task tool with `isolation: "worktree"` (harness-managed, lands in
       `<repo>/.claude/worktrees/<name>` and never goes through Bash)

  - another Claude session inside THIS working tree -> ask (concurrent:
    justified; declining leads only to "use that session's worktree or wait",
    which is not a command this session issues, so there is no choice to offer)
  - cannot tell                                     -> CHOICE: create it, or
    switch in the shared tree
  - `[worktree-ok]` given                           -> ask. NOT a choice: the
    token is what a completed confirmation looks like coming back through the
    guard, and declining it withdraws the token, which is the other way on
  - otherwise (single work stream)                  -> deny, steer to `git switch`

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

Retry tokens, one per direction, both matched as BARE WORDS of the command
(has_token) -- a substring test read `echo 'we documented [shared-tree-ok]'`
as consent and turned the guard off. `[worktree-ok]` carries the creation
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
counted -- switching the shared tree cannot affect them. File-restore forms of
`git checkout` (and `git restore`) are always allowed, as is every non-`add`
worktree subcommand (`list`, `remove`, `prune`). `git switch -`/`checkout -`
count as switches (they are). A `git checkout <name>` that would DWIM a
remote-only branch is also a switch.
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
import cmdline
import console
from cmdline import apply_chdir, parse_git


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


def _tokenize_with_separators(command: str, windows=None):
    """`cmdline.split_segments_with_separators`, Windows separators carried across.

    Returns `([(operator, tokens), ...], parsed_cleanly)`. The operator is what
    joined each segment to the one before it, and reading a `cd` needs it: `&&`
    runs what follows where the `cd` arrived, `||` runs it only if the `cd`
    failed, which is where the shell already was.

    On Windows `\\` is the path separator, and POSIX-mode shlex reads it as an
    escape: `git -C C:\\proj\\repo switch topic` tokenizes to `C:projrepo` and
    the value naming the repository is gone. Doubling the backslashes first
    hands them back. The one form that comes out still doubled is a
    single-quoted path, where shlex unescapes nothing, and `apply_chdir`
    collapses those with `os.path.normpath` -- which is `ntpath` on Windows
    (measured).

    `windows` is overridable so the branch can be exercised from any platform:
    the failure it guards is invisible on the machines most sessions run on,
    and the value it destroys is the one that decides WHICH repository the
    command acts on.

    A `cd` argument is the same kind of value as a `-C` one, arrives the same
    way, and goes through this same doubling — which is the whole of what the
    adapter has to say about it, since both then reach `apply_chdir` and its
    `normpath`.
    """
    # RIDER: a UNC path in SINGLE quotes still loses the repository.
    # `git -C '\\\\server\\share\\repo' switch x` reaches `apply_chdir` with the
    # leading pair doubled: the line below doubles every backslash, shlex
    # unescapes nothing inside single quotes, and `ntpath.normpath` collapses
    # interior runs but not the leading pair that names the host. The guard
    # then finds no repository there and exits silently. The base hook handled
    # this form, so this one place went backwards; every other Windows form
    # (bare, double-quoted, relative) was compared against base and matches.
    # Verified 2026-08-31 at 0000000.
    #
    # A `cd` operand goes through this same doubling since that fix, so the
    # single-quoted UNC form loses the repository there too and the rider now
    # covers both. Read, not run: there is no Windows runner here.
    if windows is None:
        windows = os.name == "nt"
    if windows:
        command = command.replace("\\", "\\\\")
    return cmdline.split_segments_with_separators(command)


def _tokenize(command: str, windows=None):
    """The same read, without the operators — `(segments, parsed_cleanly)`."""
    items, clean = _tokenize_with_separators(command, windows)
    return [tokens for _, tokens in items], clean


def _judgment_text(command: str) -> str:
    """The command with everything the shell will not EXECUTE taken out.

    Comments and heredoc bodies are both data, and a judgment read drops both
    for the same reason. The residual this file used to record — "a heredoc
    line that IS exactly a git command still matches" — is what the second one
    closes. A CONSENT read (`has_token`, `parses_cleanly`) still reads the
    command as written, because a retry token is written in a comment on
    purpose.
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
# Verified 2026-08-31 at 0000000.
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
    `has_token` reads the original. Asking the comment-free text instead would
    put "this command has an unbalanced quote" on commands whose only
    unbalanced quote was in a comment that no longer matters.
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

    **No substring fallback for a command that does not parse cleanly**, and
    that is where this parts company with the commit gate's `has_marker`,
    which does fall back. The asymmetry above is the reason: reading a marker
    loosely costs one skipped check the user is being asked about anyway,
    while reading this token loosely turns the guard off with nobody asked.
    Measured: `git worktree add ../wt f && echo "we agreed on [worktree-ok]
    yesterday` carries the token as a substring and gives no consent.

    **Comments are NOT dropped here**, and that is the one way this read
    differs from the judgment read `split_command` does. A retry token is
    written in a comment on purpose — `git worktree add ../wt f
    # [worktree-ok]` is the documented form — so dropping comments first would
    throw away the only place the token is ever written.
    """
    segments, _clean = _tokenize(command)
    # A closing parenthesis rides on the last word of a segment, so a token
    # written at the end of `(git worktree add ../wt f [worktree-ok])` arrived
    # here with a `)` on it and matched nothing. The judgment read strips a
    # subshell opener, so that command now classifies — and creation is the
    # one verdict in this guard with no `ask` behind it, which turns an
    # unreadable token into a loop with no way out rather than one more
    # prompt. Widening a CONSENT read is the safe direction; the judgment
    # read is where a stray parenthesis must not decide anything.
    return any(
        tok == token or tok.strip("()") == token for toks in segments for tok in toks
    )


def judgeable(tokens, where: str, cwd: str):
    """(shell directory, git directory) this segment's verdict is about.

    Two destinations fall back to the session's own directory, which is this
    guard's answer from before it could read a `cd` at all:

      - one the reader could not compute (a variable, a glob, a subshell);
      - one that reads cleanly and holds no repository.

    The second was missed, and it is the more common of the two. `cd
    /no/such/dir ; git switch x` leaves the shell exactly where it started —
    `;` runs what follows whether the `cd` worked or not — so the switch
    happens in the session's own tree, which is the tree another session may
    be sitting in. Judging the destination sent the guard to `if not top:
    sys.exit(0)` and it said nothing at all.

    The commit gate STOPS on a target like this (`names_a_directory` in
    `hooks/commit-review-gate.py`) and this guard falls back instead. The two
    protect different things: a commit nobody judged is a commit nobody
    reviewed, while a guard that goes silent leaves a shared tree unguarded,
    and `worktree-guard-spec.md` §Unknowns resolve conservatively puts the
    cost of a wrong deny at one prompt against a wrong allow breaking another
    session's tree.

    A `git -C` that names no repository is NOT this case and keeps today's
    silence: git refuses that command itself, so no tree is touched.

    Which is why the segment's own `-C` is composed BEFORE the fallback is
    considered, and not after. Deciding first threw the destination away and
    then resolved a RELATIVE `-C` against the session directory instead:
    `cd ~/projects && git -C myrepo switch main` turned a real target
    repository into a path that does not exist, and the guard exited at
    `if not top` having said nothing. Returning both directories is what lets
    the caller classify against the tree it is about to judge.
    """
    here = cwd if isinstance(where, cmdline.Unresolved) else where
    target = segment_cwd(tokens, here)
    if here == cwd or repo_paths(target)[0]:
        return here, target
    return cwd, segment_cwd(tokens, cwd)


def segment_cwd(tokens, cwd: str) -> str:
    """`cwd` with this segment's own `git -C` applied, or `cwd` unchanged.

    Takes the token list `split_command` produced -- the same one `classify`
    judged. `main()` asks this for the `-C` target of the segment it just
    classified, so reading both from one tokenization is what keeps the
    verdict and the tree it is about in agreement.
    """
    parsed = parse_git(tokens)
    if not parsed:
        return cwd
    return apply_chdir(cwd, parsed[2])


def is_ref(name: str, cwd: str) -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{name}^{{commit}}"],
            cwd=cwd or None,
            capture_output=True,
        )
        return r.returncode == 0
    except Exception:
        return False


def classify(tokens, cwd: str):
    """Return a reason string if this segment switches branch or adds a worktree.

    Takes one segment's token list from `split_command`. Quoting is settled
    there: a quoted sentence is a single token, so it can never present itself
    here as a command word, and a command the lexer gave up on contributes the
    tokens it did read rather than nothing at all.
    """
    parsed = parse_git(tokens)
    if not parsed:
        return None
    sub, args, chdirs = parsed
    # `-C` moves the repository this segment reads, so the ref lookups and the
    # path-exists test below have to follow it.
    cwd = apply_chdir(cwd, chdirs)

    if sub == "worktree":
        # Only creation is guarded; list/remove/prune are how you clean up.
        positionals = [a for a in args if not a.startswith("-")]
        if positionals and positionals[0] == "add":
            return "worktree-add"
        return None

    if sub == "switch":
        # git switch <branch> / -c <branch> / `-` (previous)  => switches tree
        creating = any(a in ("-c", "-C") for a in args)
        has_target = any(a == "-" or not a.startswith("-") for a in args)
        if creating or has_target:
            return "create+switch" if creating else "switch"
        return None

    if sub == "checkout":
        if any(a in ("-b", "-B") for a in args):
            return "create+switch"
        if "--" in args:
            return None  # explicit path restore
        if "-" in args:
            return "switch"  # previous branch
        positionals = [a for a in args if not a.startswith("-")]
        if not positionals:
            return None
        first = positionals[0]
        if (
            first == "."
            or os.path.exists(os.path.join(cwd or ".", first))
            or os.path.exists(first)
        ):
            return None  # restoring a file/dir, not switching branch
        if is_ref(first, cwd):
            return "switch"
        if is_ref(f"origin/{first}", cwd):
            return "switch"  # DWIM checkout of a remote-only branch
        # `(git checkout topic)` puts the closing parenthesis on the BRANCH
        # NAME, so the lookups above ask about `topic)` and find nothing.
        # Retried only after the name AS WRITTEN has already failed, which is
        # what keeps a branch that genuinely ends in `)` answering first.
        # Peeled ONE at a time, longest name first. Stripping every trailing
        # parenthesis at once took a character off a branch really called
        # `weird)` as soon as it appeared inside a subshell, so the property
        # round 2 asked for held only outside one.
        bare = first
        while bare.endswith(")"):
            bare = bare[:-1]
            if is_ref(bare, cwd) or is_ref(f"origin/{bare}", cwd):
                return "switch"
        return None

    return None


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
    for line in tail.splitlines():
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
    for line in reversed(tail.splitlines()):
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


def transcript_idle_minutes(cwd: str, own_session_id: str):
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
    try:
        gd = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=top or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        leases = (
            os.path.join(gd.stdout.strip(), "specseal-leases")
            if gd.returncode == 0
            else None
        )
    except Exception:
        leases = None
    if leases and os.path.isdir(leases):
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
                with open(path) as f:
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
    # so enumerate with ps and match the executable basename ourselves.
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
            if os.path.basename(comm.strip()) == "claude":
                pids.add(int(num))
    except Exception:
        return [], [], False
    if not pids:
        return [], [], False

    mine = ancestors(os.getpid())
    if not (pids & mine):
        return [], [], False  # our own session is invisible -> detection is unusable

    active, idle = [], []
    for p in sorted(pids - mine):
        d = proc_cwd(p)
        if d and (d == top or d.startswith(top + os.sep)):
            tty_idle = tty_idle_minutes(p)
            tr_idle = transcript_idle_minutes(d, own_session_id)
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
    if not active:
        tr_idle = transcript_idle_minutes(top, own_session_id)
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


def steer_to_switch() -> str:
    return tr(
        "  git fetch origin\n"
        "  git switch -c <branch> origin/main   # new branch\n"
        "  git switch <branch>                  # existing branch\n\n"
        "If this genuinely is concurrent work needing separation, state why and get the "
        "user's confirmation first (if the user already asked for a worktree, retry with "
        "[worktree-ok] in the command).",
        "  git fetch origin\n"
        "  git switch -c <branch> origin/main   # 새 브랜치\n"
        "  git switch <branch>                  # 기존 브랜치\n\n"
        "정말 동시 작업이라 분리가 필요하면 그 이유를 밝히고 사용자 확인을 먼저 받으세요 "
        "(사용자가 이미 워크트리를 지시했다면 명령에 [worktree-ok] 를 붙여 다시 시도).",
    )


def steer_to_shared() -> str:
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
        "`git switch <branch>  # [shared-tree-ok]` for an existing branch, or "
        "`git switch -c <branch> origin/main  # [shared-tree-ok]` for a new one",
        "기존 브랜치면 `git switch <branch>  # [shared-tree-ok]`, 새 브랜치면 "
        "`git switch -c <branch> origin/main  # [shared-tree-ok]`",
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
        open(path, "w").close()
    except OSError:
        return True
    return False


def choose(top, session_id, scope, situation, question, options, fallback):
    """Deny once and hand the user the two options; ask on every attempt after.

    A hook decision renders as approve/decline, and the model never gets the
    turn — so where declining has TWO destinations the user sees neither and
    has to retype the command they wanted. Denying gives the model the turn
    back, and the reason spends it on AskUserQuestion.

    The fallback is this site's own pre-change decision, which is what keeps
    the deny from becoming a trap: a session with nobody to answer (headless),
    or one that has already been asked here, meets the prompt it always met.
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
    respond("ask", situation + fallback)


def guard_worktree_creation(
    top: str,
    cwd: str,
    origin: str,
    user_ok: bool,
    session_id: str = "",
    shared_option=None,
    shared_steer=None,
    single_stream="deny",
):
    """Worktrees are for CONCURRENT work only -- block the single-stream case."""
    # Same reason as the switch path: without a repository there is no tree to
    # separate, and standing `cwd` in for one makes every session under it look
    # like concurrent work in it.
    if not top:
        return
    active, idle, reliable = sessions_in_tree(top, session_id)

    # 두 방향의 목적지는 어느 자리에서 물어도 같다 — worktree 를 만들거나,
    # 공용 트리에서 그대로 진행하거나. 다만 "그대로 진행"이 어떤 명령인지는
    # 진입점마다 다르므로(Bash 는 git switch, Agent 는 isolation 없는 재호출)
    # 호출부가 준다.
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
        shared_option
        or (
            tr(
                '2. "Switch in the shared tree"',
                '2. "공용 트리에서 브랜치만 전환한다"',
            ),
            tr(
                f"run {steer_to_shared()} instead. The token carries this "
                "answer, so the switch is not questioned again.",
                f"대신 {steer_to_shared()} 중 하나를 실행하세요. 이 토큰이 지금 "
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
                + tr(
                    "Single-stream work, but [worktree-ok] was given — treating this as the "
                    "user's explicit intent. Confirm the worktree creation. Declining "
                    "withdraws [worktree-ok] and proceeds in the shared tree instead:\n",
                    "단건 작업이지만 [worktree-ok] 가 지정되어 사용자 의사로 판단합니다. "
                    "worktree 를 생성할지 확인해 주세요. 거부하면 [worktree-ok] 선언을 "
                    "철회하고 공유 트리에서 그대로 진행합니다:\n",
                )
                # Only the Bash path reaches here: `user_ok` comes from a
                # command line, and the Agent path no longer derives one.
                + steer_to_switch()
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
            + steer_to_switch(),
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

    # `single_stream` differs by entry point. A Bash command can carry
    # `[worktree-ok]` and come back through the block above, so the deny has a
    # documented way past it. An Agent call has no command line to carry one,
    # and reading the token out of its prompt was tried and taken back: the
    # prompt is prose, so "mentioning" and "instructing" cannot be told apart,
    # and one apostrophe in it decided the verdict. Both paths end at a human
    # either way, so the token only ever bought deny -> ask; the Agent path
    # takes that step directly instead.
    respond(
        single_stream,
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
            # The Bash path can be told to run `git switch`; the Agent path
            # cannot, and printing that here buried the one way on its own
            # first line already names.
            + (shared_steer or steer_to_switch())
        ),
    )


def main():
    data = load_input()
    tool = data.get("tool_name", "")
    cwd = data.get("cwd") or os.getcwd()
    tool_input = data.get("tool_input", {}) or {}

    # 하네스가 관리하는 worktree(Agent/Task `isolation: "worktree"`)는 Bash를 거치지
    # 않고 <repo>/.claude/worktrees/<name> 에 바로 생성되므로 툴 호출에서 잡는다.
    #
    # RIDER: an Agent with isolation: "worktree" may be concurrent work this
    # guard cannot see. It counts Claude sessions in the tree, and a subagent
    # is not one -- measured: a subagent's tool call renews the PARENT's lease
    # and creates no id of its own. So an Agent worktree in a single-stream
    # tree reads as single-stream, even though the agent runs alongside its
    # parent, which is this guard's own definition of concurrent. Nothing is
    # blocked by it: `single_stream="ask"` below means the path asks. What is
    # open is whether the Agent path should be judged by a different rule than
    # counting sessions. Reading a token out of the Agent's prompt was tried
    # and taken back for the reason the comment below gives.
    # Verified 2026-08-31 at 0000000.
    if tool in ("Agent", "Task"):
        if str(tool_input.get("isolation", "")).lower() != "worktree":
            sys.exit(0)
        top, _ = repo_paths(cwd)
        guard_worktree_creation(
            top,
            cwd,
            tr(
                'The Agent tool was called with isolation: "worktree" (the harness creates a '
                "worktree at <repo>/.claude/worktrees/<name>). Re-invoking without isolation "
                "proceeds in the shared tree.",
                'Agent 툴을 isolation: "worktree" 로 호출했습니다 '
                "(하네스가 <repo>/.claude/worktrees/<name> 에 worktree를 만듭니다). "
                "isolation 없이 다시 호출하면 공유 트리에서 그대로 진행됩니다.",
            ),
            # No token is read here, deliberately. The Agent's prompt is prose,
            # and prose cannot separate "the user asked for a worktree" from a
            # sentence that merely mentions the token — a prompt discussing it
            # switched the guard off, and one apostrophe in a prompt that DID
            # carry it dropped the call onto a deny telling it to add the token
            # it already had. Both paths end at a human anyway, so the token
            # only ever bought deny -> ask, and `single_stream="ask"` below
            # takes that step without the guessing.
            user_ok=False,
            session_id=data.get("session_id", ""),
            single_stream="ask",
            # No command to re-issue and nowhere to put a token: the way on
            # here is the one the origin line already names, and an option
            # telling the model to run `git switch` would bury it.
            shared_option=(
                tr(
                    '2. "Run it in the shared tree"',
                    '2. "공용 트리에서 그대로 진행한다"',
                ),
                tr(
                    'call the Agent again WITHOUT isolation: "worktree". It then '
                    "works in this tree, and no token is involved.",
                    'isolation: "worktree" 없이 Agent 를 다시 호출하세요. 그러면 이 '
                    "트리에서 그대로 작업하며, 토큰도 필요 없습니다.",
                ),
            ),
            # No `[worktree-ok]` guidance here: there is no such path on this
            # entry point, and naming one sends the model knocking on a door
            # that does not exist.
            shared_steer=tr(
                '  Call the Agent again without isolation: "worktree" — it then '
                "works in this tree.\n\n"
                "Approving this prompt creates the worktree anyway. On this path "
                "the confirmation IS the decision; there is no token for it.",
                '  isolation: "worktree" 없이 Agent 를 다시 호출하면 이 트리에서 '
                "그대로 작업합니다.\n\n"
                "이 확인창을 승인하면 worktree 를 그대로 만듭니다. 이 경로에서는 "
                "확인 자체가 결정이며, 따로 붙일 토큰은 없습니다.",
            ),
        )
        sys.exit(0)

    if tool != "Bash":
        sys.exit(0)
    command = tool_input.get("command", "") or ""

    reason = None
    eff_cwd = cwd
    for tokens, wheres in walk_command(command, cwd):
        for where in wheres:
            here, target = judgeable(tokens, where, cwd)
            reason = classify(tokens, here)
            if reason:
                eff_cwd = target
                break
        if reason:
            break
    if not reason:
        sys.exit(0)

    top, wt_root = repo_paths(eff_cwd)
    # No repository at the effective directory means there is no tree to keep
    # two sessions out of, and git itself will refuse the command. Falling back
    # to `cwd` here was the second half of the measured false deny: with cwd at
    # `$HOME`, the containment test in sessions_in_tree() matches every session
    # on the machine.
    if not top:
        sys.exit(0)

    if reason == "worktree-add":
        # A command the lexer gave up on may carry a `[worktree-ok]` in the
        # part it never reached. Single-stream is the one verdict in this
        # guard with no budget and no `ask` behind it, and its way past is
        # "append [worktree-ok]": without this note the user appends a token
        # that is already there, meets the same deny, and the loop ends only
        # when the command itself is rewritten.
        #
        # The verdict is left alone -- softening deny to ask would hand every
        # command a bypass costing one apostrophe -- and the instruction is
        # made followable instead, by naming the quote as the obstacle.
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
            session_id=data.get("session_id", ""),
        )
        sys.exit(0)

    session_id = data.get("session_id", "")
    active, idle, reliable = sessions_in_tree(top, session_id)

    # The mirror of [worktree-ok]: the user has just chosen the shared tree,
    # and the token carries that answer back through the guard. Honoured only
    # where the guard's own verdict is "cannot tell" — never over an ACTIVE
    # session (that deny protects a tree this session does not own), and never
    # over the dirty-tree question (which asks something else entirely).
    shared_ok = has_token(command, "[shared-tree-ok]")

    steer = tr(
        f"  # check an existing branch out into a worktree\n"
        f"  git worktree add {wt_root}/<branch> <branch>\n\n"
        f"  # or create a new branch off the latest origin/main\n"
        f"  git fetch origin\n"
        f"  git worktree add {wt_root}/<name> -b <branch> origin/main\n\n"
        "Then work in that folder from a separate Claude Code session. "
        "`git worktree list` shows worktrees.",
        f"  # 기존 브랜치를 worktree로 꺼내기\n"
        f"  git worktree add {wt_root}/<branch> <branch>\n\n"
        f"  # 새 브랜치를 최신 origin/main 기준으로 생성 (저장소 정책)\n"
        f"  git fetch origin\n"
        f"  git worktree add {wt_root}/<name> -b <branch> origin/main\n\n"
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
                f"`git worktree add {wt_root}/<branch> <branch>  # [worktree-ok]` "
                f"for a branch that already exists, or "
                f"`git worktree add {wt_root}/<name> -b <branch> origin/main  "
                f"# [worktree-ok]` for a new one, then work there from a "
                f"separate session. The token carries this answer, so creating "
                f"it is confirmed rather than questioned again.",
                f"아직 작업 중인 세션의 브랜치를 보존합니다. 이미 있는 브랜치면 "
                f"`git worktree add {wt_root}/<branch> <branch>  # [worktree-ok]`, "
                f"새로 만들 브랜치면 `git worktree add {wt_root}/<name> -b "
                f"<branch> origin/main  # [worktree-ok]` 를 실행하고, 그 폴더에서 "
                f"별도 세션으로 작업하세요. 이 토큰이 지금 고른 답을 담고 있어 "
                f"생성할 때 다시 묻지 않고 확인만 받습니다.",
            ),
        ),
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
        )

    # 3) 단건이지만 추적 중인 변경이 있으면 사용자에게 확인.
    entries = tracked_changes(cwd)
    if entries:
        listing = "\n".join(f"    {xy}  {path}" for xy, path in entries)
        phantoms = phantom_entries(entries, cwd)
        note = ""
        if phantoms:
            why = "\n".join(f"    {p} — {r}" for p, r in phantoms)
            fixes = "\n".join(
                f"    git restore --staged {shlex.quote(p)}" for p, _ in phantoms
            )
            note = tr(
                f"\nIndex-only residue invisible in the working tree:\n{why}\n"
                f"These commands clean the tree (run `git restore <path>` first to keep "
                f"index-only content):\n{fixes}\n",
                f"\n이 중 워크트리에서는 보이지 않는 index 잔재:\n{why}\n"
                f"아래 명령으로 정리하면 트리가 clean이 됩니다 "
                f"(index에만 존재하는 내용을 살리려면 `git restore <path>` 를 먼저 실행):\n{fixes}\n",
            )
        respond(
            "ask",
            (
                tr(
                    f"Single-stream tree, so the switch is allowed — but there are "
                    f"{len(entries)} uncommitted tracked changes:\n{listing}\n{note}"
                    f"They will follow you onto the target branch. Confirm to proceed "
                    f"(commit/stash first is recommended).",
                    f"이 트리는 단건 작업이라 브랜치 전환을 허용할 수 있지만, "
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
