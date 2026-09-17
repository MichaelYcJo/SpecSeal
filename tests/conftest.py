import atexit
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

import pytest


def _build_repo(d):
    """`git init` a repo at `d`, with one committed file and a feature branch."""
    git = lambda *a: subprocess.run(
        ["git", "-C", str(d), *a],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (d / "f.txt").write_text("one\ntwo\nthree\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    git("branch", "feature/x")


def build_tracked_tree(d, files, deleted=()):
    """A repository at `d` holding `files`, with `deleted` removed from disk.

    `files` is `{relative path: text}`; every one of them is committed, and
    each entry of `deleted` is then unlinked WITHOUT staging the removal, so
    it stays in the index and leaves the working tree. That is the state the
    documented release sequence produces at step 3 of
    `docs/release-checklist.md`, and the state `on_disk` below is about.

    A real `git init` rather than a directory of files, for the reason
    `tests/test_the_pull_request_language_is_the_repositorys.py#test_the_templates_check_reads_prose_only_and_descends`
    already records: a fixture git never sees would report nothing and the
    case would pass having exercised nothing. `GIT_TEMPLATE_DIR` is emptied
    above, so the `git init` costs almost nothing.
    """
    d = pathlib.Path(d)
    d.mkdir(parents=True, exist_ok=True)
    git = lambda *a: subprocess.run(
        ["git", "-C", str(d), *a],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    for rel, text in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "base")
    for rel in deleted:
        (d / rel).unlink()
    return d


def on_disk(root, listed):
    """Split a git path listing into what is on disk and what is not.

    `git ls-files` lists the INDEX, so a tracked file the working tree has
    deleted is on the list with nothing behind it. A walk that opens every
    listed path ends there with a `FileNotFoundError`, no file after it is
    read, and the rule the walk holds reports nothing at all (#432, #282).

    **The missing half is returned rather than dropped.** A sweep that judges
    what it finds is strictly better off for the skip -- on this tree it used
    to report nothing about any file. A case that reads the corpus to prove an
    entry is still ALIVE is not: to it a skipped file and a deleted entry are
    the same evidence, so a silent skip buys it a false alarm. Those callers
    hand the missing list to `decline_if_shrunken`; a positive sweep judges
    what remains and ignores it.
    """
    present, missing = [], []
    for rel in listed:
        (present if os.path.isfile(os.path.join(root, rel)) else missing).append(rel)
    return present, missing


def shrunken_corpus(missing, what):
    """The reason a case gives when its verdict needs the whole corpus.

    Every path by name rather than a count. A claim removed from a corpus
    without a word is the direction `seal/follow-up.md`'s first row calls the
    one a checker of claims must not fail in, and a bare number is that
    silence with a digit in front of it -- the reader cannot tell which entry
    went unjudged, which is the one thing they need in order to judge it by
    hand.
    """
    return (
        f"{len(missing)} tracked path(s) are listed by git and not on disk, so "
        f"{what} cannot tell a file this run skipped from an entry that is "
        "really gone, and is not judging. Missing: " + ", ".join(sorted(missing))
    )


def decline_if_shrunken(missing, what):
    """`pytest.skip` with `shrunken_corpus`'s reason when anything is missing."""
    if missing:
        pytest.skip(shrunken_corpus(missing, what))


HOOKS = os.path.join(os.path.dirname(__file__), "..", "hooks")

# Default-locale determinism: the suite owns its locale. A plain setdefault
# is not enough — the author's machine exports SPECSEAL_LANG=ko session-wide
# (measured), which would flip every default-language assertion. Tests that
# need Korean monkeypatch the env and fresh-load the module.
os.environ["SPECSEAL_LANG"] = "en"

# One run of this suite calls `git init` 403 times, and each call copies the
# default template into the new repository: 18 files where 2 are enough, 14 of
# them sample hooks that nothing in this suite runs or reads. That is roughly
# 6,400 files created and never opened again -- free on a filesystem that
# creates files cheaply, and not free on windows, where the virus scanner
# opens each one as it appears.
#
# Set here rather than at the fifteen `git init` call sites, because `git`
# reads the template location from the environment and the tests should not
# each have to remember. An empty template still leaves a complete repository:
# `config`, `HEAD`, `objects/` and `refs/` are `git init`'s own work, not the
# template's.
_EMPTY_GIT_TEMPLATE = tempfile.mkdtemp(prefix="specseal-empty-git-template-")
os.environ["GIT_TEMPLATE_DIR"] = _EMPTY_GIT_TEMPLATE
atexit.register(shutil.rmtree, _EMPTY_GIT_TEMPLATE, True)

# `git commit` forks a detached `git maintenance run --auto` when
# maintenance.auto is on (the default), which keeps touching
# `.git/objects/` -- creating and removing `maintenance.lock` -- after the
# `commit` call has already returned. Several fixtures in this suite build
# one repository and `shutil.copytree` it into many tests, so that detached
# process racing a copy is no longer a one-in-many-runs coincidence: it read
# `.git/objects/maintenance.lock`'s directory entry, then found the file gone
# by the time it opened it, and failed the copy (observed on ubuntu CI).
# Disabled through the environment, not a global git config write, so a
# developer's own `maintenance.auto` setting is untouched.
os.environ["GIT_CONFIG_COUNT"] = "1"
os.environ["GIT_CONFIG_KEY_0"] = "maintenance.auto"
os.environ["GIT_CONFIG_VALUE_0"] = "false"


def load_hook_module(filename, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HOOKS, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_hook(filename, payload, env=None):
    """Feed a hook the stdin JSON the harness would send; return its stdout."""
    r = subprocess.run(
        [sys.executable, os.path.join(HOOKS, filename)],
        input=json.dumps(payload),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        env={**os.environ, **(env or {})},
    )
    return r.stdout


def decision_of(stdout):
    """'silent' when a hook allowed by staying quiet, else its decision."""
    if not stdout.strip():
        return "silent"
    return json.loads(stdout)["hookSpecificOutput"]["permissionDecision"]


def fired(stdout):
    """True when a gate stopped the call at all.

    A gate with two ways on denies the FIRST time a session meets it in a
    repository — spending the reason on the question — and asks on every
    attempt after that. Detection tests care that the gate saw the command,
    not which of the two prompts it produced; the shape has tests of its own.
    """
    return decision_of(stdout) in ("deny", "ask")


# Told apart by `shell_probe` below, and the caller is expected to act on the
# difference: one is a name that was never a shell, the other is a shell whose
# environment ate the answer.
NOT_A_SHELL = "not a shell here"
ATE_THE_PROBE = "its environment ate the probe"


def shell_probe(name):
    """Why `name` on PATH is not usable as a shell here, or None if it is.

    `shutil.which` was the whole question once, and on a `windows-latest`
    runner it resolves `bash` to `C:/Windows/System32/bash.exe` -- the WSL
    launcher, with no distribution installed. That is not a shell: it exits
    non-zero and prints an install notice in UTF-16, which arrives here as a
    string full of NUL bytes.

    The two ways to fail are not the same failure, and a caller that cannot
    tell them apart either fails on a name that was never a shell or stays
    quiet when a real one drops out:

      - a non-zero exit is a name that is not a shell at all, and the runner's
        `bash` is exactly that;
      - a zero exit with the wrong answer is a working shell whose environment
        wrote to stdout first. `zsh` sources `.zshenv` even non-interactively,
        so one `echo` in a developer's own removes it from the run.
    """
    try:
        r = subprocess.run(
            [name, "-c", "printf ok"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return f"did not run ({type(e).__name__}) -- {NOT_A_SHELL}"
    if r.returncode != 0:
        return f"exited {r.returncode} -- {NOT_A_SHELL}"
    if r.stdout.strip() != "ok":
        return f"answered {r.stdout.strip()!r}, not 'ok' -- {ATE_THE_PROBE}"
    return None


def symlink_or_skip(target, link):
    """`os.symlink(target, link)`, or skip the test where it is not permitted.

    Windows needs SeCreateSymbolicLinkPrivilege -- Developer Mode, or an
    elevated shell. A GitHub `windows-latest` runner has it and an ordinary
    developer machine does not, so `skipif(os.name == "nt")` and a bare
    `os.symlink` are both wrong in one direction each: the first drops the
    coverage where the privilege IS held, the second turns a missing
    privilege into a red suite for code nobody touched.

    Asked by attempting the call, because that is the only thing that answers
    it. Nothing is inferred from the platform.
    """
    # A missing parent is a fixture bug, and every one of its errors is an
    # `OSError` too -- so without this the skip would swallow it and the case
    # would read as "no privilege here" on a machine that has one.
    parent = os.path.dirname(os.path.abspath(str(link)))
    assert os.path.isdir(parent), f"the link's parent does not exist: {parent}"
    try:
        os.symlink(target, link)
    except OSError as exc:
        pytest.skip(f"symbolic links are not available here ({exc})")


def fifo_or_skip(path):
    """`os.mkfifo(path)`, or skip the test where it is not available.

    Asked by attempting the call, for the reason `symlink_or_skip` gives:
    `os.mkfifo` does not exist on Windows at all, and on a POSIX filesystem
    that has no named pipes it raises. Nothing is inferred from the platform.
    """
    parent = os.path.dirname(os.path.abspath(str(path)))
    assert os.path.isdir(parent), f"the fifo's parent does not exist: {parent}"
    maker = getattr(os, "mkfifo", None)
    if maker is None:
        pytest.skip("named pipes are not available here (no os.mkfifo)")
    try:
        maker(path)
    except OSError as exc:
        pytest.skip(f"named pipes are not available here ({exc})")


# What a POSIX shell answers, and what `cmd.exe` prints back verbatim.
POSIX_ROW_PROBE = "echo one; echo $(echo two)"


def posix_row_shell_or_skip():
    """Skip unless the shell behind `shell=True` here separates commands with
    `;` and substitutes `$(…)` — the two things a `Broad gate` row's fixture
    can be ABOUT.

    `broad_gate.run` hands the row to `subprocess(shell=True)`, which is
    `/bin/sh` on POSIX and `%COMSPEC%` — normally `cmd.exe` — on Windows.
    `cmd.exe` has neither: `echo a; echo b` is one `echo` that succeeds, and
    `$(echo x)` is a literal argument. So a fixture row written to fail, or
    to substitute, does neither there — and a case built on one is not
    failing to reproduce a defect, it has no defect to reproduce.

    **This is `symlink_or_skip`'s rule followed, not excepted.** That rule is
    *ask by attempting*, and the thing to attempt here is exactly which shell
    will run the row — asked through the same call the gate makes, so the
    answer is the gate's own shell rather than a guess from `os.name`.
    `skipif(os.name == "nt")` would be wrong in both of the directions that
    rule names: it drops the coverage on a Windows machine whose `COMSPEC` is
    a POSIX shell, and it keeps asserting on a POSIX machine whose `/bin/sh`
    is something nobody expected.

    A case that only reads a REFUSAL needs none of this. `not_as_written` is
    a string test that reaches no shell, and the refusal is right on both
    platforms — `templates/config.md` names what each shell does with the
    forms it lists.
    """
    try:
        r = subprocess.run(
            POSIX_ROW_PROBE,
            shell=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        pytest.skip(f"the shell behind `shell=True` could not be probed ({exc})")
    if r.returncode != 0 or r.stdout.split() != ["one", "two"]:
        pytest.skip(
            f"`shell=True` here is not a POSIX shell: {POSIX_ROW_PROBE!r} "
            f"answered {r.stdout.strip()!r} (exit {r.returncode}). A `;` "
            "separator and `$(…)` substitution are what this case's row is "
            "made of, and this shell has neither"
        )


def local_home(repo):
    """Create `<git-common-dir>/seal/` for `repo` and return its path.

    The local-mode root (#80). Asked of git rather than spelled `.git/seal`,
    because in a linked worktree `.git` is a FILE and the root belongs to
    the main tree's common directory, which is what the hooks read.
    """
    common = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-common-dir"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    home = pathlib.Path(os.path.normpath(os.path.join(str(repo), common))) / "seal"
    home.mkdir(parents=True, exist_ok=True)
    return home


def declare_routing(
    repo, item="1787708604-a-work-item", review="through the review chain", home=None
):
    """Write a routing declaration for the repo's current branch, and return
    the work-item directory the round records now live in.

    Everything that used to key on a pull request number keys on this: the
    declaration names its branch, and the checked-out branch looks it up.

    `home` is the root to write under when it is not `<repo>/seal/` -- the
    path `local_home` returned, for a local-mode fixture.
    """
    branch = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    d = (pathlib.Path(home) if home else repo / "seal") / "specs" / item
    d.mkdir(parents=True, exist_ok=True)
    (d / "routing.md").write_text(
        f"# {item} -- routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {review} |\n"
        "| Destination | open the pull request |\n"
        f"| Branch | {branch} |\n",
        encoding="utf-8",
    )
    return d


def rounds_dir(item):
    """`<item>/rounds/`, created. Where the round records live.

    A helper rather than `item / "rounds"` at each call site: the tests that
    write a record are the ones that would keep the old flat path alive, and
    one spelling is what makes moving it again a single edit.
    """
    d = item / "rounds"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def _repo_template(tmp_path_factory):
    """One built repo, shared for the session; `repo` copies it per test."""
    d = tmp_path_factory.mktemp("repo-template")
    _build_repo(d)
    return d


@pytest.fixture
def repo(tmp_path, _repo_template):
    """A git repo with one committed file and a feature branch to switch to."""
    d = tmp_path / "repo"
    shutil.copytree(_repo_template, d)
    return d
