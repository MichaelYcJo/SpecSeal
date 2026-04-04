#!/usr/bin/env python3
"""PreToolUse gate: a commit needs a review in its cycle.

The code-review skill marks a completed review by writing the reviewed HEAD
into <git-dir>/claude-preset-reviewed. A commit closes that cycle (HEAD moves),
so the next commit needs a fresh review mark.

Opt-in per repository: the gate is active only where the preset workflow is in
use, detected by an `_ai/` directory at the repo root. Everywhere else this
hook stays silent — a globally installed plugin must not nag unrelated repos.

Decisions:
  - not a git commit, repo not opted in, or `[no-review]` in the command → allow
  - review mark matches current HEAD → allow
  - otherwise → ask (the user approving the prompt IS the waiver — no
    separate bypass mechanism to maintain)
"""

import json
import re
import subprocess
import sys

COMMIT_RE = re.compile(r"\bgit(\s+-[^\s]+)*\s+commit\b")


def git(args, cwd):
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd or None, capture_output=True, text=True, timeout=5
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    if payload.get("tool_name") != "Bash":
        return
    command = (payload.get("tool_input") or {}).get("command", "")
    if not COMMIT_RE.search(command) or "[no-review]" in command:
        return

    cwd = payload.get("cwd", "")
    top = git(["rev-parse", "--show-toplevel"], cwd)
    if not top:
        return

    import os

    if not os.path.isdir(os.path.join(top, "_ai")):
        return  # repo has not opted into the preset workflow

    head = git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd)
    git_dir = git(["rev-parse", "--git-dir"], cwd)
    mark_path = os.path.join(cwd or ".", git_dir, "claude-preset-reviewed") if git_dir else ""

    marked = ""
    if mark_path and os.path.isfile(mark_path):
        try:
            with open(mark_path) as f:
                marked = f.read().strip()
        except OSError:
            pass

    if head and marked == head:
        return  # reviewed in this cycle

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        "No review is recorded for this cycle (the code-review "
                        "skill writes the reviewed HEAD to "
                        ".git/claude-preset-reviewed). Approve to commit anyway, "
                        "or run the review chain first. `[no-review]` in the "
                        "command also skips this gate."
                    ),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
