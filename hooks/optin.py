"""Shared opt-in: does this repository run the specseal workflow?

Imported by the gates rather than copied into each, because the answer moved
once already and four divergent copies is how half of them keep the old answer.

The signal is `seal/` — the root the plugin maintains, whose existence is the
declaration — at the first of two places that has it: `<repo>/seal/`, which
shared mode commits, then `<git-common-dir>/seal/`, where local mode keeps
it (#80). One root, read one way, and no
config key (`docs/one-root-by-lifetime.md`, "The opt-in signal is the root
itself"). `.specseal/` opts nothing in any more: the only reader left of that
name is `hooks/root-migrate.py`, which moves it.

`<git-common-dir>/specseal-scratch` takes that declaration back. A repository
that exists for thirty seconds — a fixture built by hand to reproduce a gate
decision, which is what developing these gates consists of — carries the same
`seal/` as a repository under review, and the gates cannot tell them apart:
every probe stopped for a prompt about a repository that would be deleted
before the answer meant anything. The marker is written once, by a person, in
the repository being thrown away. It lives under the git directory rather
than inside the root because the root is committed: `.specseal/scratch` was a
file in a committed directory, and one committed there silenced every gate in
every clone with nothing in the diff that read as the workflow being switched
off. Nothing under `.git/` can be committed, and a linked worktree shares the
common directory, so it shares the opt-out. `seal/README.md` says so too.

Everything here fails toward "not opted in": a gate that cannot tell should do
nothing rather than act on a guess.
"""

import os
import subprocess

HOME = "seal"
# The sub-directory of the root that holds the work items. Readers that
# classify repository-relative paths — the commit gate's `DOC_ROOTS`, the CI
# scripts' globs, `chain_check.py`'s prefix — spell `seal/` as a string,
# because a path in a diff or a tree listing is only ever the shared root;
# every hook that opens a file joins this under `home()` instead, so #80
# changes where the folder is created and nothing that reads it.
WORK_ITEMS = "specs"
# An empty FILE under the common git directory; its existence is the whole
# signal, read the way the root is read. It is not an entry inside an existing
# file because every gate would then parse one to answer what is a directory
# test. A directory of this name is not the marker — see `home_at()` below.
SCRATCH = "specseal-scratch"


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


def git_common_dir(root):
    """The common git directory of the repository at `root`, or "".

    `.git` at the toplevel, when it is a directory, IS the repository's git
    directory, and for a main worktree the common directory is that same
    place — so that case is answered without a process. Every gated command
    in every opted-in repository reaches this through `home_at()`, and the
    rider on `repo_root` counts what one more `git` per call costs. A `.git`
    that is a file (a linked worktree, a submodule) or absent is asked of git,
    which answers relative to the directory it ran in unless the path is
    absolute; `os.path.join` handles both spellings.
    """
    if not root:
        return ""
    dotgit = os.path.join(root, ".git")
    if os.path.isdir(dotgit):
        return dotgit
    try:
        out = subprocess.run(
            ["git", "-C", root, "rev-parse", "--git-common-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return ""
    out = (out or "").strip()
    return os.path.normpath(os.path.join(root, out)) if out else ""


def home_at(root):
    """The `seal/` of the repository at `root`, or "" — for a caller that has
    already resolved the root and should not pay for a second `git` call.

    The two places are read in order, `<root>/seal/` then
    `<git-common-dir>/seal/`, and whichever exists first is the answer;
    nothing else is read. The opt-out is read once, here, so it cannot be
    honoured by one arm of a gate and missed by the other — the migration
    config sits inside the root the marker takes back, and a repository
    nobody reviews has nothing to compare against an original either.
    """
    if not root:
        return ""
    common = None
    found = os.path.join(root, HOME)
    if not os.path.isdir(found):
        common = git_common_dir(root)
        found = os.path.join(common, HOME) if common else ""
        if not found or not os.path.isdir(found):
            return ""
    if common is None:
        common = git_common_dir(root)
    # A FILE, which is what this module and `seal/README.md` both say the
    # signal is. `os.path.exists` also accepted a DIRECTORY of that name, and
    # the marker used to sit in a committed directory — so `.specseal/scratch/`
    # created once turned every gate off in every clone, with nothing in the
    # diff that reads as the workflow being switched off.
    if common and os.path.isfile(os.path.join(common, SCRATCH)):
        return ""
    return found


def home(cwd):
    """This repository's `seal/`, or "" when it does not run the workflow."""
    return home_at(repo_root(cwd))


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
