"""Shared address: was the implementer the declaration named actually used?

The routing declaration has a third axis, `Implementation`, and an axis nobody
can check is a note rather than a decision. This module owns the one place the
answer leaves a trace: a mark in the repository's git dir, written when `smith`
is spawned and read after a commit.

A module rather than a copy in each gate, for the reason `optin.py` gives for
existing at all -- the mark is written by one hook and read by another, and two
spellings of one path is a mark that is written and never found.

**What the mark is worth, stated plainly.** Every mark this plugin writes can
be written by hand, `specseal-reviewed` included. This one catches a session
that declared `smith` and then implemented the work itself, which is a session
forgetting its own answer, not an adversary defeating a check. Nothing blocks
on it and CI never sees it -- a git dir does not travel.

Everything here fails toward "no mark". A git dir that cannot be resolved, an
unwritable directory, an unreadable file: each ends as a false reminder rather
than a false silence. That direction is deliberate. The mark is written by a
`pre-agent` gate, and `dispatch.py` renders a gate that fails to load as an
allow with no output -- so a gate that quietly stops running would turn the
notice OFF, and nobody would learn that it had. Firing on *declared `smith` AND
no mark* means a dead gate produces a line somebody reads.

Branch-scoped, because the declaration is. The mark names the branch it was
written on, and a mark for another branch does not answer for this one --
otherwise one `smith` spawned once in a repository would silence the notice for
every work item after it, forever.
"""

import os
import subprocess

# Named for the axis rather than for the agent: what the mark records is that
# the declared implementer was used, and `smith` is today's only answer that
# leaves a trace.
MARK = "specseal-implementer"


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


def write(cwd, branch):
    """Record that the declared implementer ran on `branch`. Never raises."""
    gd = git_dir(cwd)
    if not gd or not branch:
        return False
    try:
        with open(os.path.join(gd, MARK), "w", encoding="utf-8") as f:
            f.write(branch + "\n")
    except OSError:
        return False
    return True


def stands(cwd, branch):
    """True when a mark for `branch` is there."""
    gd = git_dir(cwd)
    if not gd or not branch:
        return False
    try:
        with open(os.path.join(gd, MARK), encoding="utf-8", errors="replace") as f:
            return f.read().strip() == branch
    except OSError:
        return False


def is_smith(subagent_type):
    """True when a spawn names the `smith` agent.

    The harness spells a plugin's agent `specseal:smith` and a project-local
    one `smith`, so the qualifier is dropped before comparing. Nothing looser:
    a substring test would read `smith-helper` -- or a prompt mentioning smith
    -- as the agent itself, and a mark written for the wrong spawn is exactly
    the false silence the module docstring refuses.
    """
    name = str(subagent_type or "").strip()
    return name.rsplit(":", 1)[-1] == "smith"
