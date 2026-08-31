#!/usr/bin/env python3
"""PostToolUse: declare "this session is working on this tree" — a lease.

The worktree guard's process/tty/transcript heuristics cannot see every
session: extension-hosted sessions aren't named `claude`, and a session whose
cwd is elsewhere can still edit this tree through absolute paths (both
observed live). Heuristics infer; leases DECLARE. Every tool call that
touches a repo refreshes `<git-dir>/specseal-leases/<session-id>`, and
the guard treats a fresh lease as a live work stream — no inference needed.

Repo resolution: Write/Edit/NotebookEdit lease the repo containing the edited
file (cwd may be elsewhere); Bash leases the repo of its cwd. Leases older
than a day are pruned opportunistically. Failure is always silent — a lease
is a safety net, never a blocker.

The record carries WHO holds it, not just when. A lease is stamped on every
tool call and never removed at session end, so a closed session's lease went
on reading as live work for the whole idle window and hard-denied other
sessions' branch switches (measured: two conversations ended minutes apart,
and a third could not switch). Writing the owning pid lets the guard ask
whether that session still exists instead of assuming it does.

The pid is the `claude` process found by walking up from this hook, NOT
`getppid()` — measured here, the immediate parent is the shell that spawned
the hook (`/bin/zsh`), which dies constantly. Treating that as the owner
would retire live leases. When no `claude` ancestor is found the record omits
`pid` entirely, and the guard reads that as unattributable — a question for
the user rather than either assumption.
"""

import json
import os
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console


def git_dir(path):
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=path,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def owner_pid():
    """The `claude` process this hook hangs off, or None if it cannot be seen.

    None is a real answer and is recorded as such: an extension host whose
    process is not named `claude` must not be mistaken for a session that has
    exited.
    """
    cur = os.getppid()
    for _ in range(15):
        try:
            r = subprocess.run(
                ["ps", "-o", "ppid=,comm=", "-p", str(cur)],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
            out = r.stdout.strip()
            if not out:
                return None
            ppid_s, _, comm = out.partition(" ")
            if "claude" in comm:
                return cur
            cur = int(ppid_s)
        except Exception:
            return None
        if cur <= 1:
            return None
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    # basename: the id names a file under specseal-leases/ — a separator in
    # a hostile or malformed id must not become a path escape.
    session = os.path.basename(payload.get("session_id", "")) or f"pid-{os.getppid()}"

    if tool in ("Write", "Edit", "NotebookEdit"):
        edited = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        target = os.path.dirname(edited) or None
    elif tool == "Bash":
        target = payload.get("cwd") or None
    else:
        return
    if not target or not os.path.isdir(target):
        return

    gd = git_dir(target)
    if not gd:
        return
    leases = os.path.join(gd, "specseal-leases")
    record = {"ts": int(time.time()), "host": socket.gethostname()}
    pid = owner_pid()
    if pid is not None:
        record["pid"] = pid
    try:
        os.makedirs(leases, exist_ok=True)
        with open(os.path.join(leases, session), "w") as f:
            json.dump(record, f)
        cutoff = time.time() - 86400
        for name in os.listdir(leases):
            p = os.path.join(leases, name)
            try:
                if os.stat(p).st_mtime < cutoff:
                    os.unlink(p)
            except OSError:
                pass
    except OSError:
        pass


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
