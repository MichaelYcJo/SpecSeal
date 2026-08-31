#!/usr/bin/env python3
"""PreToolUse gate: two skills answer to "review", so let the user pick.

Claude Code ships a skill named `code-review`, and this plugin ships
`specseal:code-review`. Their descriptions overlap on "review a PR or diff",
so a request that meant one can land on the other. The wrong direction is not
symmetric: the built-in runs a bug-and-cleanup sweep, and the user learns it
was the wrong review only after paying for a whole one.

A yes/no permission prompt is the wrong shape for a choice between two
things — approving is clear but rejecting leaves the user to retype the call
they wanted. So the gate denies instead, and the reason tells the model to put
the two options to the user directly. Measured against Claude Code 2.1.241:
the model reaches for AskUserQuestion on that reason.

Denying every time would trap the user who picks the built-in — their retry
would be denied again. So the gate fires once per session per working tree
and then steps aside, which is also what "a choice already made is not
re-litigated" means here. Per tree, not per repository: the marker lives in
the git dir, and a linked worktree has its own — so a session working a main
tree and a worktree of it is asked in each. The two trees hold different
branches and different diffs, so it is not the same choice being re-asked.
Without a session id it cannot dedupe, so it falls back to `ask`, where
approving is itself the way through.

The two names differ by the plugin prefix, so telling them apart is exact
string comparison — no substring matching, which would swallow an unrelated
`acme:code-review`.

This gate only ever sees a skill the MODEL chose. A user typing
`/code-review` does not route through the Skill tool at all (measured), so a
decision already made is never second-guessed.

Opt-in per repository, by the `.specseal/` directory the other gates use: a
globally installed plugin must not nag repos that do not run this workflow.

Failure direction: this gate interrupts more. A wrong interruption costs one
question; a wrong pass costs the full built-in review that the question
existed to prevent. Anything unexpected — malformed payload, no cwd, no git
repo, an unwritable git dir — lets the call through, since a gate that
crashes must not wedge the session. That silence belongs to states that are
genuinely broken, which is why the git dir is resolved by git and never
constructed: a path this hook builds wrong is indistinguishable from a
repository it cannot write, and it takes the silent exit on every call rather
than on the rare one.
"""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import optin

BUILTIN = "code-review"
OURS = "specseal:code-review"
MARKER_DIR = "specseal-review-choice"

REASON = f"""\
`{BUILTIN}` is Claude Code's built-in skill, not this plugin's, and this repo \
carries both. Do not choose for the user.

Ask with the AskUserQuestion tool, offering exactly these two options:

  1. "Built-in review" — /{BUILTIN}: bugs, duplication, and cleanup
     across the diff.
  2. "SpecSeal review" — /{OURS}: spec compliance first, then
     quality, inheriting the verdicts of earlier review rounds.

Then run the one they pick; retrying the built-in will go through. \
The user may also prefer `@agent-specseal:warden`, which runs the SpecSeal \
review as a subagent."""


def git(args, cwd):
    """Run a git command in `cwd`; "" on any failure.

    The same helper the sibling gate carries (`commit-review-gate.py`), so
    the two hooks reach a git dir by one route instead of two."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def git_dir(cwd):
    """The git dir holding this tree's markers, or "" when there is no repo.

    Asked of git rather than built as `<repo-root>/.git`. In a linked worktree
    that path is a FILE pointing at `<main>/.git/worktrees/<name>`, so every
    write beneath it raises and `already_asked` reads the failure as "already
    asked" -- which took this gate silent on every call made from a worktree.

    `rev-parse --git-dir` answers relative from a main tree (`.git`) and
    absolute from a linked worktree, so the result is joined onto `cwd`;
    joining an absolute path discards the prefix, which is why one line covers
    both. The sibling gate joins at its use site for the same reason.
    """
    gd = git(["rev-parse", "--git-dir"], cwd)
    return os.path.join(cwd or ".", gd) if gd else ""


def already_asked(cwd, session):
    """True if this session already got the question here; records it if not.

    A failure to write means the marker cannot be trusted, so the caller is
    told the question was already asked — one missed question beats a loop
    the user cannot escape."""
    gd = git_dir(cwd)
    if not gd or not session:
        return True
    # RIDER: the id is joined raw, without `os.path.basename`. Executed: an id
    # of `../../../../wt/sub/deep/f.txt` left an empty file and its parent
    # directories in the working tree. It comes from the harness rather than
    # from prose, and an existing marker is never overwritten because of the
    # `os.path.exists` return below -- so this is a stray write, not a
    # bypass. `hooks/commit-review-gate.py:already_asked` guards its own id
    # and is the shape to copy. Verified 2026-08-31 at 9829412.
    path = os.path.join(gd, MARKER_DIR, str(session))
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return True
    return False


def decide(decision, reason):
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


def main():
    try:
        event = json.load(sys.stdin)
        skill = (event.get("tool_input") or {}).get("skill")
        cwd = event.get("cwd")
        session = event.get("session_id")
    except (ValueError, AttributeError):
        return

    if skill != BUILTIN or not cwd or not os.path.isdir(cwd):
        return
    if not optin.opted_in(cwd):
        return

    # No session id means no way to record that the question was asked, so a
    # deny would repeat forever. `ask` cannot loop: approving is the way out.
    if not session:
        decide("ask", REASON)
        return

    if already_asked(cwd, session):
        return
    decide("deny", REASON)


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
