#!/usr/bin/env python3
"""PreToolUse gate: a commit needs a review in its cycle.

The code-review skill marks a completed review by writing the reviewed HEAD
into <git-dir>/specseal-reviewed. A commit closes that cycle (HEAD moves),
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
import os
import shlex
import subprocess
import sys

WRAPPERS = {"command", "env", "nohup", "time", "sudo"}


def split_segments(command):
    """Split into pipeline/list segments while respecting quotes.

    A regex split on `;`/`&&`/newline breaks inside quoted strings, so the
    heredoc commit form Claude Code itself uses (`git commit -m "$(cat
    <<'EOF' ...)"`) fell apart mid-quote and slipped past the gate.
    shlex with punctuation_chars keeps quoted arguments whole and emits
    the separators as their own tokens.

    Unquoted newlines separate commands just like `;`; newlines inside
    quotes belong to an argument and must not split it. shlex alone treats
    every newline as plain whitespace, so a small quote-aware scan converts
    only the unquoted ones first.

    Returns (segments, parsed_cleanly)."""
    out, quote, esc = [], None, False
    for ch in command:
        if esc:
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
        out.append(";" if ch == "\n" and quote is None else ch)
    command = "".join(out)

    lex = shlex.shlex(command, posix=True, punctuation_chars=";|&")
    lex.whitespace_split = True
    lex.commenters = ""
    segments, current = [], []
    try:
        for tok in lex:
            if tok and set(tok) <= set(";|&"):
                if current:
                    segments.append(current)
                current = []
            else:
                current.append(tok)
    except ValueError:
        if current:
            segments.append(current)
        return segments, False
    if current:
        segments.append(current)
    return segments, True


def is_git_commit(command):
    """True only when some segment's COMMAND WORD is git with subcommand
    commit — a prose mention (echo "git commit", heredoc lines) must not
    gate. Same lesson the worktree guard learned; applied here too.

    When the command cannot be tokenized at all, a fail-open pass would
    exempt exactly the commands too gnarly to parse — so an unparseable
    command that mentions both `git` and `commit` gates anyway (the gate
    only asks; a false positive costs one approval click)."""
    segments, clean = split_segments(command)
    if not clean and "git" in command and "commit" in command:
        return True
    for toks in segments:
        i = 0
        while i < len(toks) and (
            ("=" in toks[i] and not toks[i].startswith("-"))
            or os.path.basename(toks[i]) in WRAPPERS
        ):
            i += 1
        if i >= len(toks) or os.path.basename(toks[i]) != "git":
            continue
        rest, j = toks[i + 1 :], 0
        takes = {"-C", "-c", "--git-dir", "--work-tree"}
        while j < len(rest):
            if rest[j] in takes:
                j += 2
                continue
            if rest[j].startswith("-"):
                j += 1
                continue
            break
        if j < len(rest) and rest[j] == "commit":
            return True
    return False


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
    if not is_git_commit(command) or "[no-review]" in command:
        return

    cwd = payload.get("cwd", "")
    top = git(["rev-parse", "--show-toplevel"], cwd)
    if not top:
        return

    if not os.path.isdir(os.path.join(top, "_ai")):
        return  # repo has not opted into the preset workflow

    head = git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd)
    git_dir = git(["rev-parse", "--git-dir"], cwd)
    mark_path = (
        os.path.join(cwd or ".", git_dir, "specseal-reviewed") if git_dir else ""
    )

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
                        ".git/specseal-reviewed). Approve to commit anyway, "
                        "or run the review chain first. `[no-review]` in the "
                        "command also skips this gate."
                    ),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
