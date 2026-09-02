import atexit
import importlib.util
import json
import os
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


def declare_routing(
    repo, item="1787708604-a-work-item", review="through the review chain"
):
    """Write a routing declaration for the repo's current branch, and return
    the work-item directory the round records now live in.

    Everything that used to key on a pull request number keys on this: the
    declaration names its branch, and the checked-out branch looks it up.
    """
    branch = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    d = repo / "seal" / "specs" / item
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
