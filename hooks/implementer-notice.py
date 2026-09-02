#!/usr/bin/env python3
"""PostToolUse reminder: the declaration said `smith`, and `smith` never ran.

The third routing axis records who implements the work. This is what makes the
record worth writing: after a commit, where the declaration in force says
`smith` and no mark stands for this branch, the session is told once. Where the
mark stands, nothing is said at all.

**Why here and not at the commit gate.** A `PreToolUse` gate that allows
produces no output — allowing IS silence, and there is no spelling for "let
this through and also say something". A notice emitted from there would be a
notice nobody sees. `PostToolUse` is the nearest site whose output is read, and
it cannot block, which is exactly the standing the plan gave this axis: notice,
never denial.

**Once per repository per session.** The grain is written down because `once`
has meant four different things in this tree. A marker under the git dir
records that this session has been told here; a second commit says nothing, and
an unwritable marker counts as already told — one missed reminder beats a line
printed after every commit for the rest of a session.

**Which repository.** The session's own, resolved from `cwd`, the same key
`review-history-guard.py` uses. A commit aimed at another repository with
`git -C` is not judged here: following it would mean re-deriving every target
the commit gate derives, to decide whether to print one line.

Reminder-only (PostToolUse cannot block). Active only in repositories with
`seal/` at the root.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import implementer
import optin
import routing
from cmdline import drop_comments, drop_heredoc_bodies, parse_git, split_segments

NOTICE_DIR = "specseal-implementer-notice"


def commits(command):
    """True when some segment of the command actually invokes `git commit`.

    Borrowed from `cmdline` rather than matched with a regex, so that a
    heredoc line or a comment mentioning `git commit` does not produce a
    reminder about work nobody committed. The deeper forms the commit gate
    chases — an `eval` argument, a body an interpreter runs from stdin — are
    deliberately not chased here: missing one costs a reminder, and the gate
    that has to be right about them is the one that can stop a commit.
    """
    segments, _clean = split_segments(drop_heredoc_bodies(drop_comments(command)))
    for tokens in segments:
        parsed = parse_git(tokens)
        if parsed and parsed[0] == "commit":
            return True
    return False


def already_told(cwd, session):
    """True when this session has already been told here; records it if not.

    A failure to write reads as already told, for the reason
    `review-skill-gate.py` gives for the same shape: the alternative is a line
    that never stops. The id names a file, so a separator in a malformed one
    must not become a path escape.
    """
    gd = implementer.git_dir(cwd)
    session = os.path.basename(str(session or ""))
    if not gd or not session or session in (".", ".."):
        return True
    path = os.path.join(gd, NOTICE_DIR, session)
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return True
    return False


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if payload.get("tool_name") != "Bash":
        return
    command = (payload.get("tool_input") or {}).get("command", "")
    if not command or not commits(command):
        return

    cwd = payload.get("cwd") or "."
    top = optin.repo_root(cwd)
    if not top or not optin.opted_in(cwd):
        return

    branch = routing.current_branch(cwd)
    declared = routing.for_branch(top, branch)
    if not declared or declared.get("implementation") != routing.BY_SMITH:
        return
    if implementer.stands(cwd, branch):
        return
    if already_told(cwd, payload.get("session_id")):
        return

    # The path a person has to recognise, spelled the way their platform
    # spells it — `os.path.join`, not a literal `/`, for the reason
    # `review-history-guard.py` gives: half of one path in each dialect.
    item = routing.item_dir(top, branch)
    where = (
        os.path.join(os.path.relpath(item, top), routing.FILENAME)
        if item
        else "the routing declaration"
    )
    print(
        f"[specseal] {where} answers `Implementation` with `smith`, and no "
        f"smith was spawned on this branch. Either spawn it for the rest of the "
        f"work, or change the row to `the session` so the declaration says "
        f"what actually happened. Nothing was blocked, and this is said once "
        f"per session."
    )


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
