#!/usr/bin/env python3
"""PreToolUse gate: a root exists that nobody chose a mode for.

Creating `seal/` is what opts a repository in, and the mode that creation
lands in decides something a person should have been asked about. Shared mode
COMMITS the root, so every clone carries this repository's review records;
local mode keeps it under the common git directory and no clone does. A
monorepo that would not have wanted its records committed has them committed,
and the way back is a documented sequence rather than a setting.

**Nothing observed it.** #151, reported from a repository's first work item
under SpecSeal: the session created `seal/` and started working, and no
question was asked. Three files each said something correct and the three
together left no route to the question -- `hooks/optin.py` says the root's
existence IS the declaration, `skills/implement/SKILL.md` §Bootstrap says the
mode question is asked there and nowhere else, and the preset block in
`CLAUDE.md` (which `install.sh` copies into `~/.claude/CLAUDE.md`, so it loads
in every project on the machine) tells a session to write
`seal/specs/<id>/routing.md` before the first edit. That write creates the
root. The question lived in a skill the session had no reason to load.

So this names the state rather than hoping a document is read. A root with no
`Mode` row in `config.md` is exactly *nobody was asked*, and `seal mode`
answers it in one command -- either by recording where the folder already is,
or by moving it.

**Which repository, and why it is the session's.** The one the session is
working in, read from the payload's `cwd`. Its sibling gate resolves the
repository a COMMIT lands in, because a verdict about a change has to be about
the repository that change reaches; this is not a verdict about a change. It
is a fact about the workspace the session is sitting in -- that workspace has
a root, and nothing says which mode it is in -- and `git -C <elsewhere>` does
not move the session's workspace.

**When, and why not at the commit.** On any Bash call, which means the first
one of the session. Scoping it to a commit was the first design here and the
budget is what argued it down: `skills/implement/SKILL.md` §1 says the cost of
a question is not its difficulty but WHEN it arrives, and at the commit this
question lands beside the review arm's, at minute thirty, on a session that may
have nobody at the keyboard. On the first Bash call it lands in the batch a
session collects before it starts, which is where this project wants questions.
The number of interruptions is the same either way -- one -- because the budget
below is per session, not per command.

**The budget, stated because `CONTRIBUTING.md` asks for it.** One deny per
session per repository, then `ask`, which approving gets past. Zero once the
row exists, which `seal mode` writes and which
`skills/implement/SKILL.md` §Bootstrap now writes when it creates the root --
so a repository that went through the bootstrap is never asked here, and this
gate sees only the roots that did not.

**No waiver token.** The two arms of the commit gate each carry one because
each is about whether a CHANGE was checked, and a change can honestly be
exempt. This is about setup, the way on takes one command, and a token would
build exactly the standing exemption `docs/review-chain-spec.md` refuses.
`ask` is the escape hatch, and it is one an unattended run can take.

Everything here fails toward silence, the way `hooks/optin.py` does: a
repository this cannot read is one it says nothing about.
"""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as repo_config
import console
import optin

# One marker file per session per repository, and NOT the commit gate's
# directory. Sharing it would make answering one question silence the other,
# and the two are different questions that can arrive in the same session.
CHOICE_DIR = "specseal-mode-choice"


def already_asked(cwd, git_dir, session):
    """True when this session was already offered the question in this repo.

    Records it when it was not. A marker that cannot be written counts as
    already asked: one missed question beats a deny the session cannot get
    past, and in a run with nobody at the keyboard that deny is an outage
    rather than a cost. The same rule as `hooks/commit-review-gate.py`, and
    not the same marker.

    The id names a file, so a separator in a malformed one must not become a
    path escape -- measured on a sibling guard, where `../../escaped` put an
    empty file at the repository root.
    """
    session = os.path.basename(str(session or ""))
    if not git_dir or not session or session in (".", ".."):
        return True
    path = os.path.join(cwd or ".", git_dir, CHOICE_DIR, session)
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return True
    return False


def undeclared(root):
    """`root`'s seal root when nobody recorded a mode for it, else "".

    Both halves are read where they live: the folder through `optin.home_at`,
    which is the opt-in signal and the only thing that says a repository runs
    this workflow, and the row through `config.declared_mode`, which is what
    `seal mode` writes. Nothing here infers one from the other -- a gate that
    trusted the row would go looking in a place with no folder.

    `unknown` -- a row naming something that is not a mode -- counts as
    undeclared, which is the direction `seal mode` already takes: a claim
    nobody can act on is not an answer somebody gave.
    """
    home = optin.home_at(root)
    if not home:
        return ""
    kind, _value = repo_config.declared_mode(home)
    return "" if kind == "mode" else home


def git_dir_of(root):
    """`root`'s git directory as an absolute path, or "".

    Absolute, so a linked worktree's marker lands in that worktree's own git
    directory rather than beside the main tree's -- and so the join in
    `already_asked` does not depend on which directory this process is in.
    """
    try:
        done = subprocess.run(
            ["git", "-C", root, "rev-parse", "--absolute-git-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return (done.stdout or "").strip() if done.returncode == 0 else ""


def question_reason(root, home):
    """The first prompt: a deny whose reason hands the choice to the user."""
    return (
        f"{root} runs the SpecSeal workflow — its root is at {home} — and "
        "nothing records which mode that root is in. Creating the root is "
        "what opts a repository in, and the mode it landed in decides "
        "something nobody was asked: shared mode COMMITS the root, so every "
        "clone carries this repository's review records, and local mode keeps "
        "it under the git directory, where no clone does.\n\n"
        "Do not choose for the user. Ask with the AskUserQuestion tool, "
        "offering exactly these three options:\n\n"
        "  This repository's root has no recorded mode. Which one is it in?\n"
        '    1. "Keep it where it is" — run `seal mode`. It records the mode '
        f"from where the folder already is ({home}) and moves nothing. This "
        "is the answer whenever the current layout is the intended one, and "
        "it is the cheapest of the three.\n"
        '    2. "Shared" — run `seal mode shared`. The root moves into the '
        "tree at <repo>/seal/, the move is staged, and the pull-request "
        "checks are installed. Choose it when the records should travel with "
        "the repository.\n"
        '    3. "Local" — run `seal mode local`. The root moves under the '
        "common git directory, the workflow file is removed, and nothing "
        "about this repository is committed. Choose it when the records "
        "should not leave this machine — CI cannot run the checks in this "
        "mode.\n\n"
        "Then run what they picked. Re-issuing the command instead reaches "
        "the ordinary approval prompt, where approving proceeds and records "
        "nothing."
    )


def ask_reason(root, home):
    """The plain prompt, for the attempts after the first in a session."""
    return (
        f"{root} runs the SpecSeal workflow — root at {home} — and nothing "
        "records which mode that root is in, so `seal mode` has not been run "
        "here.\n\n"
        "Approving proceeds and records nothing: the state stays as it is and "
        "the question comes back in the next session. Declining cancels the "
        "command. The way past it for good is one command — `seal mode` "
        "records the mode from where the folder already is, and `seal mode "
        "shared` / `seal mode local` move the folder and record it."
    )


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
        payload = json.load(sys.stdin)
    except Exception:
        return

    if payload.get("tool_name") != "Bash":
        return
    cwd = payload.get("cwd", "")
    root = optin.repo_root(cwd)
    if not root:
        return
    home = undeclared(root)
    if not home:
        return

    session = payload.get("session_id")
    # No session id means no way to record that the question was asked, so a
    # deny would repeat forever. `ask` cannot loop: approving is the way out.
    if session and not already_asked(root, git_dir_of(root), session):
        decide("deny", question_reason(root, home))
    else:
        decide("ask", ask_reason(root, home))


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind this line.
    console.to_utf8()
    main()
