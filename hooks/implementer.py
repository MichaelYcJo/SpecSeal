"""Shared address: was the agent the declaration named actually used?

The routing declaration has two axes nobody can gate on -- `Planning`, who
draws the frame, and `Implementation`, who writes the code -- and an axis
nobody can check is a note rather than a decision. This module owns the one
place either answer leaves a trace: a mark in the repository's git dir, written
when the agent is spawned and read after a commit.

A module rather than a copy in each gate, for the reason `optin.py` gives for
existing at all -- the mark is written by one hook and read by another, and two
spellings of one path is a mark that is written and never found.

**One module for BOTH axes**, for that same reason one storey up. A second
module beside this one would hold a `git_dir`, a `write` and a `stands` that
differ from these by a constant, and a near-identical copy is the failure
contract §11 and §16 each record having already been paid for -- each of them a
rule that sat in two definitions in near-identical words while a third carried
none. So the axis is an ARGUMENT here, never a second file: two constants, and
one reader that walks them.

**What a mark is worth, stated plainly.** Every mark this plugin writes can be
written by hand, `specseal-reviewed` included. These catch a session that
declared an agent and then did that agent's work itself, which is a session
forgetting its own answer, not an adversary defeating a check. Nothing blocks
on them and CI never sees them -- a git dir does not travel.

Everything here fails toward "no mark". A git dir that cannot be resolved, an
unwritable directory, an unreadable file: each ends as a false reminder rather
than a false silence. That direction is deliberate. A mark is written by a
`pre-agent` gate, and `dispatch.py` renders a gate that fails to load as an
allow with no output -- so a gate that quietly stops running would turn the
notice OFF, and nobody would learn that it had. Firing on *an agent declared
AND no mark* means a dead gate produces a line somebody reads.

Branch-scoped, because the declaration is. A mark names the branch it was
written on, and a mark for another branch does not answer for this one --
otherwise one `smith` spawned once in a repository would silence the notice for
every work item after it, forever. **Axis-scoped for the same reason**, one
level over: the two marks share a directory, so a `smith` spawned on this
branch must not answer for a `framer` that never was.
"""

import os
import subprocess

# Named for the AXIS rather than for the agent: what a mark records is that the
# declared agent for that axis was used, and the agent's name is only how a
# spawn happens to spell it. The file names are frozen -- an existing mark
# under somebody's git dir is found by this string and by nothing else.
IMPLEMENTATION_MARK = "specseal-implementer"
PLANNING_MARK = "specseal-planner"

# Which spawn writes which mark. The one place the two are paired, so a reader
# asking "does this spawn leave a trace" has one table to open.
AGENT_MARKS = (("framer", PLANNING_MARK), ("smith", IMPLEMENTATION_MARK))


def git_dir(cwd):
    """The git dir holding this tree's marks, or "" when there is none.

    Asked of git as an ABSOLUTE path, the way `session-lease.py` asks. In a
    linked worktree `<root>/.git` is a FILE, so a built path is unwritable
    there -- and an unwritable mark is a notice that fires forever in every
    worktree.
    """
    if not cwd or not os.path.isdir(cwd):
        return ""
    try:
        out = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--absolute-git-dir"],
            capture_output=True,
            # Named, not `text=True`: git answers UTF-8 and a repository under
            # a path this locale cannot decode otherwise leaves `stdout` as
            # None, which is an `AttributeError` neither clause below catches.
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return (out.stdout or "").strip() if out.returncode == 0 else ""


def write(cwd, branch, mark):
    """Record that `mark`'s declared agent ran on `branch`. Never raises.

    `mark` is named at every call site rather than defaulted, because a default
    here would be a wrong axis written silently -- and a mark under the wrong
    name is the false silence this module refuses, not a missing one.
    """
    gd = git_dir(cwd)
    if not gd or not branch or not mark:
        return False
    try:
        with open(os.path.join(gd, mark), "w", encoding="utf-8") as f:
            f.write(branch + "\n")
    except OSError:
        return False
    return True


def stands(cwd, branch, mark):
    """True when `mark` stands for `branch`.

    Two coordinates, for one reason each. The branch, because a declaration is
    per branch. The axis, because the two marks share a directory and `smith`
    is spawned on nearly every work item -- one mark answering for both is a
    silence in exactly the state the notice exists to report.
    """
    gd = git_dir(cwd)
    if not gd or not branch or not mark:
        return False
    try:
        with open(os.path.join(gd, mark), encoding="utf-8", errors="replace") as f:
            return f.read().strip() == branch
    except OSError:
        return False


def mark_for(subagent_type):
    """The mark a spawn of this agent writes, or "" when it writes none.

    The harness spells a plugin's agent `specseal:smith` and a project-local
    one `smith`, so the qualifier is dropped before comparing. Nothing looser:
    a substring test would read `smith-helper` -- or a prompt mentioning smith
    -- as the agent itself, and a mark written for the wrong spawn is exactly
    the false silence the module docstring refuses.

    One comparison over `AGENT_MARKS`, never one predicate per agent. The
    reasoning above is the whole value of this function, and a second agent
    that copied the `rsplit` would be a second place for it to be relaxed back
    into a substring test -- which is how it was nearly written the first time.
    """
    name = str(subagent_type or "").strip().rsplit(":", 1)[-1]
    for agent, mark in AGENT_MARKS:
        if name == agent:
            return mark
    return ""
