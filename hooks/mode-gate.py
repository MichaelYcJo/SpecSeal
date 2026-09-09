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
existence IS the declaration, `skills/implement/orchestration.md` §Bootstrap
says the mode question is asked there and nowhere else, and the preset block in
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

**The budget, stated because `CONTRIBUTING.md` asks for it.** Two prompts per
session per repository and no more: one deny, then one `ask` that approving
gets past, then silence for every command after them. Zero once the row
exists, which `seal mode` writes and which `skills/implement/orchestration.md`
§Bootstrap now writes when it creates the root -- so a repository that went
through the bootstrap is never asked here, and this gate sees only the roots
that did not.

**Per session per REPOSITORY, and a local root is one repository.** The two
markers are keyed to the folder the question is about rather than to the work
tree the command came from, because a local root is one folder every worktree
of the clone shares -- `marker_dir` below owns that, and asking twice about
one folder is what it was measured doing.

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
# The session's SECOND and last prompt: the approvable retry the deny tells
# the model to make. Its own directory, because the deny and the ask are two
# different questions and each is spent once.
RETRY_DIR = "specseal-mode-retry"


def already_asked(git_dir, session, choice_dir=CHOICE_DIR):
    """True when this session was already offered `choice_dir`'s prompt here.

    Records it when it was not. A marker that cannot be written counts as
    already asked: one missed question beats a deny the session cannot get
    past, and in a run with nobody at the keyboard that deny is an outage
    rather than a cost. The same rule as `hooks/commit-review-gate.py`, and
    not the same marker.

    `git_dir` is absolute, which `git_dir_of` guarantees by resolving git's
    answer against the root. The sibling this was copied from takes a `cwd`
    first argument because it is handed a RELATIVE git directory and the join
    is what places the marker; here that argument only ever discarded itself,
    since `os.path.join` drops everything before an absolute path -- so it is
    gone rather than kept as a no-op somebody would later read as a guard.
    What replaces it is `git_dir_of`'s own resolution, which is the thing that
    has to hold: `--git-common-dir` answers `.git` from a main work tree,
    measured 2026-09-08, so a resolution left to this join would have written
    the marker relative to whatever directory this process happened to be in.

    The id names a file, so a separator in a malformed one must not become a
    path escape -- measured on a sibling guard, where `../../escaped` put an
    empty file at the repository root.
    """
    session = os.path.basename(str(session or ""))
    if not git_dir or not session or session in (".", ".."):
        return True
    path = os.path.join(git_dir, choice_dir, session)
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return True
    return False


def undeclared(root, common=None):
    """`root`'s seal root when nobody recorded a mode for it, else "".

    Both halves are read where they live: the folder through `optin.home_at`,
    which is the opt-in signal and the only thing that says a repository runs
    this workflow, and the row through `config.declared_mode`, which is what
    `seal mode` writes. Nothing here infers one from the other -- a gate that
    trusted the row would go looking in a place with no folder.

    `unknown` -- a row naming something that is not a mode -- counts as
    undeclared, which is the direction `seal mode` already takes: a claim
    nobody can act on is not an answer somebody gave.

    A file that cannot be OPENED is the one case that goes the other way; see
    `unreadable` below for why the gate and the writer part company there.

    `common` is `main`'s already-resolved common git directory, handed down so
    this invocation asks git for it once; see `marker_dir` below.
    """
    home = optin.home_at(root, common)
    if not home:
        return ""
    if unreadable(repo_config.config_path(home)):
        return ""
    kind, _value = repo_config.declared_mode(home)
    return "" if kind == "mode" else home


def unreadable(path):
    """True when `path` is there and this process cannot read it as text.

    `hooks/config.py#declared_mode` folds no file, no row, an empty value and
    a file that will not open into one answer, and that is right for the
    WRITER: `seal mode` goes on to write the row either way. For a GATE the
    fourth is different in kind. A file that exists and cannot be opened -- a
    directory of that name, a permission this process does not have, bytes
    this locale cannot decode -- is not a repository that failed to answer. It
    is one whose answer could not be read, and this module's docstring says
    what to do then: say nothing, the way `hooks/optin.py` does.

    Not exotic, and it compounds. `hooks/optin.py#repo_root` already records a
    repository under a path a cp949 console cannot decode; a `Record language`
    row hand-edited in a non-UTF-8 locale puts those bytes in this file. The
    escape is `seal mode`, and the row it would write is in the file nothing
    can parse.
    """
    if not os.path.lexists(path):
        return False
    try:
        with open(path, encoding="utf-8") as handle:
            handle.read()
    except (OSError, ValueError):
        return True
    return False


def git_dir_of(root, which="--absolute-git-dir"):
    """`root`'s git directory as an absolute path, or "".

    Absolute always, resolved against `root` the way `optin.git_common_dir`
    resolves its own answer -- because git's is not. `--absolute-git-dir` is,
    but `--git-common-dir` answers `.git` from a main work tree and an
    absolute path from a linked one (measured 2026-09-08), and a marker path
    that is relative to whatever directory this process was started in is a
    question asked again in the same session.

    `which` picks WHOSE git directory, and that follows the ROOT rather than
    the tree -- see `marker_dir`.
    """
    try:
        done = subprocess.run(
            ["git", "-C", root, "rev-parse", which],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if done.returncode != 0:
        return ""
    out = (done.stdout or "").strip()
    return os.path.normpath(os.path.join(root, out)) if out else ""


def marker_dir(root, home, common=None):
    """The git directory this root's answer is recorded in.

    Per work tree for a SHARED root, which one tree owns: each work tree has
    its own `<repo>/seal/`, so each is a separate unanswered root and each
    deserves its own question.

    Per CLONE for a LOCAL one. There is one root under the common git
    directory serving every work tree, `undeclared()` reads that same folder
    from all of them, and `README.md`'s gate row says once per session per
    repository -- so keying it to the tree asks twice about one folder,
    measured 2026-09-08: one session, one clone, one local root, two denies.

    `common` is the caller's already-resolved common git directory, and it is
    the answer for a local root -- `git_dir_of(root, "--git-common-dir")` asks
    git the question `optin.git_common_dir` has already answered. Without it
    this invocation ran that same `rev-parse` twice more, once through
    `home_paths` and once here, which from a linked worktree, where `.git` is
    a file and `optin.py`'s fast path does not apply, was four `git` processes
    on every Bash call against a main work tree's two (measured 2026-09-08
    with a logging `git` on `PATH`).
    """
    shared, _local = optin.home_paths(root, common)
    if shared and os.path.realpath(home) == os.path.realpath(shared):
        return git_dir_of(root)
    return os.path.normpath(common) if common else git_dir_of(root, "--git-common-dir")


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
    # Resolved once, here, and handed to both readers below. Three units
    # wanted the common git directory and each asked git for itself.
    common = optin.git_common_dir(root)
    home = undeclared(root, common)
    if not home:
        return

    session = payload.get("session_id")
    # Two prompts, each spent once, then silence for the rest of the session.
    #
    # The ask is spent too, and that is the half this gate got wrong. It fires
    # on every Bash call rather than on a commit, so an `ask` that stands for
    # the rest of the session is a permission prompt on every command --
    # measured 2026-09-08, one deny and NINE asks over ten ordinary calls,
    # where the sibling gate was silent on nine of the same ten because it
    # returns early for a command that is not a commit. This has no such early
    # return by design, so the budget has to be spent rather than bounded by
    # what the command happens to be.
    #
    # The way out is `seal mode`, which is itself a Bash call. A run that
    # cannot answer an `ask` therefore could not reach the command that ends
    # the asking, and every command it tried was stopped rather than one --
    # the outage the docstring above says this cannot become.
    #
    # No session id means no way to record either prompt, so both count as
    # already spent and the gate says nothing. That is the direction
    # everything here is documented to fail in.
    git_dir = marker_dir(root, home, common)
    if session and not already_asked(git_dir, session, CHOICE_DIR):
        decide("deny", question_reason(root, home))
    elif session and not already_asked(git_dir, session, RETRY_DIR):
        decide("ask", ask_reason(root, home))


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind this line.
    console.to_utf8()
    main()
