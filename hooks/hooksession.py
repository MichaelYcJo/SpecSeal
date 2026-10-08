"""Which Claude session a git hook runs under, or none (#692).

A git hook is spawned by git, not by the harness, so no payload names the
session. Two routes answer it, in order:

  1. **The environment.** The harness exports `CLAUDE_CODE_SESSION_ID` to every
     Bash child, and a child git hands it to the hook it spawns (phase 1's M4,
     executed in this harness). The value is the session's id, the same one
     its lease file and transcript are named by.
  2. **The lease** (`hooks/session-lease.py`), for a harness that exports no
     variable, or a command that emptied the environment (`env -i git commit`,
     M6). The hook walks up its own process ancestry to the nearest process
     named `claude`, the way the lease writer finds the owner it records, and
     takes the lease whose recorded `pid` is that process. Leases sit under
     each worktree's own git directory, so every worktree of the clone is
     read. Two leases naming one pid is a question nobody can settle from
     here, and the answer is no session (W3).

Contract §13 is why the second route exists: the variable is a platform
guarantee, and a defence resting on one is verified only with it removed.

**No session is an answer, and it is a person's** (`questions.md` P2, answer
(a)): a commit at someone's own terminal, with no `claude` above it, is theirs
and is not judged.

**This module is the one reader of which process and which variable are the
session's** (#868). The lease writer (`hooks/session-lease.py`) records
`claude_pid`, the lease route here reads it back, and the worktree guard's
count of other sessions tests a process's name with `is_claude`, so all three
find the same process. The writer used to take any process whose name held
`claude`, at a different depth, so a `claude-host` ancestor was recorded and
no reader ever matched that lease. `claude_pid` reads `CLAUDE_PID` first, a
value the harness exports beside `SESSION_VARIABLE` to every Bash child
(measured: it is the pid the walk finds), and walks only where it is absent.
The walk stays under the variable for §13's reason. The stub's short-cut
(`hooks/githooks.py`) and `hooks/tokens.py#steps_around_hooks` name
`SESSION_VARIABLE` and nothing else, because nothing here reads another name.
"""

import json
import os
import subprocess

LEASES = "specseal-leases"

# The one variable the harness exports that names the session, read here, in
# the stub's short-cut and in `steps_around_hooks`.
SESSION_VARIABLE = "CLAUDE_CODE_SESSION_ID"

# The variable the harness exports beside it that names the session's own
# `claude` process (executed in a Bash child on 2026-10-07 and 2026-10-08).
PID_VARIABLE = "CLAUDE_PID"


def _clean(value):
    """`value` as a file name, or "" where it cannot be one."""
    part = os.path.basename(str(value or "").strip())
    return "" if part in ("", ".", "..") else part


def is_claude(comm):
    """Whether a process whose `ps` comm is COMM is a Claude Code session:
    its executable's basename is `claude`, nothing more and nothing less.
    `claude-host` and `xclaude` are not; `/x/bin/claude` is."""
    return os.path.basename(str(comm or "").strip()) == "claude"


def claude_pid(environ=None):
    """The pid of the session's `claude` process, or None.

    `CLAUDE_PID` where the environment carries a pid above 1, an observed
    value; else the nearest ancestor `claude_ancestor` finds. None is a real
    answer: an extension host whose process is not named `claude`, and which
    exports no variable, must not be mistaken for a session that exited."""
    environ = os.environ if environ is None else environ
    value = str(environ.get(PID_VARIABLE) or "").strip()
    if value.isdigit() and int(value) > 1:
        return int(value)
    return claude_ancestor()


def claude_ancestor(start=None, depth=20):
    """The pid of the nearest ancestor process named `claude`, or None."""
    pid = os.getppid() if start is None else start
    for _ in range(depth):
        if pid is None or pid <= 1:
            return None
        try:
            out = subprocess.run(
                ["ps", "-o", "ppid=,comm=", "-p", str(pid)],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None
        if not out:
            return None
        parent, _, comm = out.partition(" ")
        if is_claude(comm):
            return pid
        try:
            pid = int(parent)
        except ValueError:
            return None
    return None


def _ps(pid, fields):
    try:
        return subprocess.run(
            ["ps", "-ww", "-o", fields, "-p", str(pid)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def call_args(start=None, depth=20):
    """The argv of every process between the hook and the nearest `claude`
    above it, nearest first; [] where no `claude` is found.

    The Bash tool's shell is one of them, and it carries the command it runs
    in its argv, so `hooks/answers.py#given` can tell which Bash call a
    commit came from (round 1 of #692, 🟡 9).
    """
    pid = os.getppid() if start is None else start
    found = []
    for _ in range(depth):
        if pid is None or pid <= 1:
            return []
        parent, _, comm = _ps(pid, "ppid=,comm=").partition(" ")
        if is_claude(comm):
            return found
        found.append(_ps(pid, "args="))
        try:
            pid = int(parent)
        except ValueError:
            return []
    return []


def lease_dirs(common):
    """Every `specseal-leases` directory of the clone at `common`."""
    found = [os.path.join(common, LEASES)]
    worktrees = os.path.join(common, "worktrees")
    try:
        names = sorted(os.listdir(worktrees))
    except OSError:
        names = []
    found += [os.path.join(worktrees, n, LEASES) for n in names]
    return [d for d in found if os.path.isdir(d)]


def from_lease(common, pid):
    """The one session whose lease in the clone records `pid`, or ""."""
    if pid is None or not common:
        return ""
    holders = set()
    for directory in lease_dirs(common):
        try:
            names = os.listdir(directory)
        except OSError:
            continue
        for name in names:
            try:
                with open(os.path.join(directory, name), encoding="utf-8") as f:
                    record = json.load(f)
            except (OSError, ValueError):
                continue
            if isinstance(record, dict) and record.get("pid") == pid:
                holders.add(_clean(name))
    holders.discard("")
    return holders.pop() if len(holders) == 1 else ""


def session(common, environ=None):
    """(session id, route) for the hook running now; ("", "") for none."""
    environ = os.environ if environ is None else environ
    sid = _clean(environ.get(SESSION_VARIABLE))
    if sid:
        return sid, "environment"
    sid = from_lease(common, claude_pid(environ))
    if sid:
        return sid, "lease"
    return "", ""
