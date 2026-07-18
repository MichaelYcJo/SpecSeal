#!/usr/bin/env python3
"""PostToolUse reminder: keep _ai/review-history flowing in both directions.

Two branches with OPPOSITE conditions — the failure modes differ:

  posting a review  → the record directory MISSING is the problem
                      (this is the only moment the session still holds its
                      verdicts and probe results; remind it to write
                      round-N.md / tests-todo.md / evidence-todo.md)

  reading a review  → the record directory EXISTING but unread is the problem
                      (inline comments may not contain the todo lists at all;
                      remind the fixer to open them)

Reminder-only (PostToolUse cannot block). Active only in repos with `_ai/`
at the root — a globally installed plugin must not nag unrelated repos.
"""

import json
import os
import re
import subprocess
import sys

POST_RE = re.compile(
    r"\bgh\s+pr\s+(review|comment)\b"
    r"|\bgh\s+api\b(?=.*-X\s+POST)(?=.*/pulls/\d+/(reviews|comments))"
)
READ_RE = re.compile(
    r"\bgh\s+pr\s+view\b(?=.*--json\s+\S*comments)"
    r"|\bgh\s+api\b(?!.*-X\s+POST)(?=.*/pulls/\d+/(comments|reviews))"
)
PR_NUM_RE = re.compile(r"\bgh\s+pr\s+(?:review|comment|view)\s+(\d+)|/pulls/(\d+)/")


SEG_RE = re.compile(r"&&|\|\||[;\n|]")
WRAPPERS = {"command", "env", "nohup", "time", "sudo"}


def gh_segments(command):
    """Segments whose command word is gh — prose mentions never remind."""
    import shlex
    out = []
    for seg in SEG_RE.split(command):
        try:
            toks = shlex.split(seg)
        except ValueError:
            continue
        i = 0
        while i < len(toks) and (("=" in toks[i] and not toks[i].startswith("-"))
                                 or os.path.basename(toks[i]) in WRAPPERS):
            i += 1
        if i < len(toks) and os.path.basename(toks[i]) == "gh":
            out.append(" ".join(toks[i:]))
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if payload.get("tool_name") != "Bash":
        return
    raw = (payload.get("tool_input") or {}).get("command", "")
    segs = gh_segments(raw)
    if not segs:
        return
    command = "\n".join(segs)
    cwd = payload.get("cwd", "") or "."

    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except Exception:
        return
    if not top or not os.path.isdir(os.path.join(top, "_ai")):
        return

    m = PR_NUM_RE.search(command)
    pr = next((g for g in (m.groups() if m else ()) if g), None)
    pr_dir = os.path.join(top, "_ai", "review-history", f"PR-{pr}") if pr else None

    if POST_RE.search(command):
        if pr_dir and not os.path.isdir(pr_dir):
            print(
                f"[specseal] A review was just posted but "
                f"_ai/review-history/PR-{pr}/ does not exist. Write round-N.md "
                f"(target SHA, verdicts, probe results), tests-todo.md, and "
                f"evidence-todo.md now — after this session ends, nobody can."
            )
    elif READ_RE.search(command):
        if pr_dir and os.path.isdir(pr_dir):
            print(
                f"[specseal] _ai/review-history/PR-{pr}/ exists. Read it "
                f"before acting on inline comments — tests-todo.md and "
                f"evidence-todo.md are implementer-owned lists that the "
                f"comments may not contain."
            )


if __name__ == "__main__":
    main()
