#!/usr/bin/env python3
"""PreToolUse gate: a commit needs a review in its cycle.

The code-review skill marks a completed review by writing the reviewed HEAD
into <git-dir>/specseal-reviewed. A commit closes that cycle (HEAD moves),
so the next commit needs a fresh review mark.

Opt-in per repository: the gate is active only where the preset workflow is in
use, detected by an `_ai/` directory at the repo root. Everywhere else this
hook stays silent — a globally installed plugin must not nag unrelated repos.

A repo that declares `docs/parity.md` opts into a second check: ported
behavior follows the original where policy is silent, so a commit touching
code should carry a record that the original was consulted. The legacy-parity
skill writes the compared HEAD to <git-dir>/specseal-parity.

Both opt-ins are independent — a repo may declare either, both, or neither.

Decisions:
  - not a git commit, or no opt-in applies → allow
  - each applicable mark matches current HEAD → allow
  - otherwise → ask, naming every missing mark at once (the user approving
    the prompt IS the waiver — no separate bypass mechanism to maintain)
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


def read_mark(cwd, git_dir, name):
    """Contents of a <git-dir> mark file, or "" when absent/unreadable."""
    if not git_dir:
        return ""
    path = os.path.join(cwd or ".", git_dir, name)
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return ""


def touches_code(cwd):
    """True when the staged change is not confined to the document roots.

    A commit that only moves docs/, specs/ or _ai/ has nothing to compare
    against an original, and asking there would train people to click through
    the prompt — which costs more than the check is worth.
    """
    staged = git(["diff", "--cached", "--name-only"], cwd)
    if not staged:
        return False
    doc_roots = ("docs/", "specs/", "_ai/")
    return any(not path.startswith(doc_roots) for path in staged.splitlines() if path)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    if payload.get("tool_name") != "Bash":
        return
    command = (payload.get("tool_input") or {}).get("command", "")
    if not is_git_commit(command):
        return

    cwd = payload.get("cwd", "")
    top = git(["rev-parse", "--show-toplevel"], cwd)
    if not top:
        return

    head = git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd)
    git_dir = git(["rev-parse", "--git-dir"], cwd)

    # Two independent opt-ins. A repo can declare either, both, or neither,
    # so each is checked on its own rather than nested behind the other.
    missing = []

    if os.path.isdir(os.path.join(top, "_ai")) and "[no-review]" not in command:
        if not head or read_mark(cwd, git_dir, "specseal-reviewed") != head:
            missing.append(
                "No review is recorded for this cycle (the code-review skill "
                "writes the reviewed HEAD to .git/specseal-reviewed). "
                "`[no-review]` in the command skips this."
            )

    if os.path.isfile(os.path.join(top, "docs", "parity.md")) \
            and "[no-parity]" not in command and touches_code(cwd):
        if not head or read_mark(cwd, git_dir, "specseal-parity") != head:
            missing.append(
                "This repo declares docs/parity.md, so behavior here is ported "
                "and the original decides where policy is silent — but nothing "
                "records that the original was consulted for this change (the "
                "legacy-parity skill writes the compared HEAD to "
                ".git/specseal-parity). `[no-parity]` in the command skips this."
            )

    if not missing:
        return

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        "\n\n".join(missing)
                        + "\n\nApproving is the waiver — the commit proceeds."
                    ),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
