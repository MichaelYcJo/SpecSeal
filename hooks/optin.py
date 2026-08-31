"""Shared opt-in: does this repository run the specseal workflow?

Imported by the gates rather than copied into each, because the answer moved
once already and four divergent copies is how half of them keep the old answer.

The signal is `.specseal/` at the repository root — the directory the plugin
maintains, whose existence is the declaration. One address, read one way.

`.specseal/scratch` beside it takes that declaration back. A repository that
exists for thirty seconds — a fixture built by hand to reproduce a gate
decision, which is what developing these gates consists of — carries the same
`.specseal/` as a repository under review, and the gates cannot tell them
apart: every probe stopped for a prompt about a repository that would be
deleted before the answer meant anything. The marker is written
once, by a person, in the repository being thrown away. It is an opt-out and
it is not for a repository anyone reviews; `.specseal/README.md` says so.

Everything here fails toward "not opted in": a gate that cannot tell should do
nothing rather than act on a guess.
"""

import os
import subprocess

HOME = ".specseal"
# An empty FILE; its existence is the whole signal, read the way the home
# directory beside it is read. It is not an entry inside an existing file
# because every gate would then parse one to answer what is a directory test.
# A directory of this name is not the marker — see `home()` below.
SCRATCH = "scratch"


def repo_root(cwd):
    """The repository root containing cwd, or "" when there is none."""
    # RIDER: every caller of this module resolves the root again. Counted with
    # a logging `git` on PATH: one gated command costs five `git` calls per
    # target and three of them are `rev-parse --show-toplevel` -- the commit
    # gate's own `root_of`, then `opted_in` and `parity_config` below. Fixing
    # it means passing the root in or memoising here, and three gates import
    # this module, so it is a change to all of them at once.
    # Verified 2026-08-31 at 9829412.
    if not cwd or not os.path.isdir(cwd):
        return ""
    try:
        out = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            capture_output=True,
            # Named, and the `.stdout or ""` below is the second half of the
            # same defect. `text=True` alone decodes with whatever locale the
            # parent had; git answers UTF-8, so a repository under a path this
            # locale cannot decode kills subprocess's reader thread -- and that
            # exception DOES NOT PROPAGATE. The call returns with `stdout` set
            # to None, and `.strip()` then raised `AttributeError`, which is
            # neither of the classes caught here.
            #
            # Measured on a cp949 console against a repository under a Korean
            # path: the gate exited 1 with no decision, and a PreToolUse hook
            # exiting non-zero is a non-blocking error -- so the commit went
            # through unjudged. Everything in this module is documented to fail
            # toward "not opted in", and that is silence, not a crash.
            encoding="utf-8",
            errors="replace",
            timeout=5,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return ""
    out = (out or "").strip()
    # Spelled the way this platform spells a path, because that is what every
    # caller does with it: `os.path.join` below, and the gates print it to
    # someone who has to recognise their own repository in it. git answers
    # with forward slashes on every platform, so on Windows the root arrived
    # in one dialect and was joined in another -- `C:/proj` and then
    # `C:/proj\.specseal\parity.md`. Both halves work; neither
    # equals a path the caller built, and the address is the whole point of a
    # module named for having ONE.
    #
    # A no-op where the two dialects already agree, so nothing about the POSIX
    # path changes and `normpath` is not asked to guess anything: git has
    # already resolved this to an absolute, existing directory.
    return os.path.normpath(out) if out else ""


def home(cwd):
    """This repository's `.specseal/`, or "" when it does not run the workflow.

    Both reads below go through here, so the opt-out is read once and cannot
    be honoured by one arm and missed by the other — the migration config sits
    inside the directory the marker takes back, and a repository nobody
    reviews has nothing to compare against an original either.
    """
    root = repo_root(cwd)
    if not root:
        return ""
    path = os.path.join(root, HOME)
    if not os.path.isdir(path):
        return ""
    # A FILE, which is what this module and `.specseal/README.md` both say the
    # signal is. `os.path.exists` also accepted a DIRECTORY of that name, and
    # `.specseal/` is committed by design — so `.specseal/scratch/` created
    # once turned every gate off in every clone, with nothing in the diff that
    # reads as the workflow being switched off.
    return "" if os.path.isfile(os.path.join(path, SCRATCH)) else path


def opted_in(cwd):
    """True when this repository runs the workflow."""
    return bool(home(cwd))


def parity_config(cwd):
    """Path to the migration config, or "" when there is none."""
    root = home(cwd)
    if not root:
        return ""
    path = os.path.join(root, "parity.md")
    return path if os.path.isfile(path) else ""
