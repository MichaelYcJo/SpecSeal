#!/usr/bin/env python3
"""PostToolUse: declare "this session is working on this tree" — a lease.

The worktree guard's process/tty/transcript heuristics cannot see every
session: extension-hosted sessions aren't named `claude`, and a session whose
cwd is elsewhere can still edit this tree through absolute paths (both
observed live). Heuristics infer; leases DECLARE. Every tool call that
touches a repo refreshes `<git-dir>/claude-preset-leases/<session-id>`, and
the guard treats a fresh lease as a live work stream — no inference needed.

Repo resolution: Write/Edit/NotebookEdit lease the repo containing the edited
file (cwd may be elsewhere); Bash leases the repo of its cwd. Leases older
than a day are pruned opportunistically. Failure is always silent — a lease
is a safety net, never a blocker.
"""

import json
import os
import subprocess
import sys
import time


def git_dir(path):
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=path, capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    session = payload.get("session_id", "") or f"pid-{os.getppid()}"

    if tool in ("Write", "Edit", "NotebookEdit"):
        target = os.path.dirname(tool_input.get("file_path", "") or "") or None
    elif tool == "Bash":
        target = payload.get("cwd") or None
    else:
        return
    if not target or not os.path.isdir(target):
        return

    gd = git_dir(target)
    if not gd:
        return
    leases = os.path.join(gd, "claude-preset-leases")
    try:
        os.makedirs(leases, exist_ok=True)
        with open(os.path.join(leases, session), "w") as f:
            f.write(str(int(time.time())))
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
    main()
