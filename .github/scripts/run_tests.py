#!/usr/bin/env python3
"""Run this repository's own suite from a virtualenv that is built once.

Issue #156. `CONTRIBUTING.md` already named a command --
`uvx --with pytest python3 -m pytest tests/ -q` -- so nothing was missing.
What was missing is a command that is cheap the second time it runs: that
form resolves and installs its environment on every call, 55-58 seconds each,
paid on all seventeen test calls of one measured segment (#133).

So the environment is built once, at `.venv` in the repository root, and
reused afterwards. The first call pays for it; every call after it pays for
Python's startup and nothing else.

**This lives under `.github/` rather than under `skills/` because it runs
THIS repository's suite.** `bin/` is on the Bash tool's PATH while the plugin
is enabled, so everything under `bin/`, `skills/` and `tests/` reaches a
user's machine -- and `.github/` does not. A user's copy of `bin/test`
therefore finds no runner beside it and says so, instead of spending five
minutes running a stranger's test suite.

Every failure here is a sentence rather than a traceback. This command writes
to the working tree the first time it runs, and half-building a virtualenv on
a machine with neither `uv` nor a new enough Python is the failure to design
against.

pytest runs with the repository root as its working directory, so a path
argument is read relative to the root from whichever directory the command
was typed in.

The full suite takes about five minutes and is the orchestrator's, run once
after the review rounds settle: `skills/agent-contract/SKILL.md` forbids it
to smith and warden, which is why naming one module is the ordinary use.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# CONTRIBUTING.md's stated floor, and the version CI runs the suite at. Named
# once, so raising it is one edit -- and so the comparison below is against a
# constant rather than a literal ruff would read as always-false at py312.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)


def repo_root():
    """The repository this file belongs to: `.github/scripts/` up two."""
    return Path(__file__).resolve().parent.parent.parent


def venv_python(venv):
    """The interpreter inside `venv`, wherever this platform puts it."""
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def has_pytest(venv):
    """True when `venv` is already an environment the suite can run in.

    Filesystem only, no subprocess: this runs on every warm call, and the
    whole point of the work item is that a warm call costs nothing.
    """
    scripts = venv / ("Scripts" if os.name == "nt" else "bin")
    return venv_python(venv).exists() and any(scripts.glob("pytest*"))


def hide_from_git(venv):
    """Write the ignore that keeps the virtualenv out of `git status`.

    `uv venv` writes this itself; `python -m venv` does not (checked on
    3.12 -- no `.gitignore` at all). So the runner writes it whichever built
    the directory, rather than the ignore holding only for one of the two.

    Inside the directory rather than in the repository's own `.gitignore`:
    the thing being ignored carries its own ignore, so removing the
    virtualenv removes the rule with it.
    """
    ignore = venv / ".gitignore"
    if not ignore.exists():
        ignore.write_text("*\n", encoding="utf-8")


def build(venv):
    """Create `venv` with pytest in it. Returns a sentence, or None on success.

    Two strategies, in the order of what the repository already assumes: `uv`
    where it is on PATH, and the standard library where it is not. Neither is
    silent -- the tools print what they are doing, because a first call that
    pauses for a minute with no output reads as a hang.
    """
    uv = shutil.which("uv")
    if uv:
        how = "uv"
        steps = [
            [uv, "venv", "--python", ">=" + FLOOR_TEXT, str(venv)],
            [uv, "pip", "install", "--python", str(venv_python(venv)), "pytest"],
        ]
    elif sys.version_info[:2] >= FLOOR:
        how = "python -m venv"
        steps = [
            [sys.executable, "-m", "venv", str(venv)],
            [str(venv_python(venv)), "-m", "pip", "install", "--quiet", "pytest"],
        ]
    else:
        return (
            "bin/test builds a virtualenv to run the suite in, and needs uv "
            f"or a Python {FLOOR_TEXT}-or-newer interpreter to build it with. "
            f"Found no uv on PATH, and this is Python "
            f"{sys.version.split()[0]}. Install uv, or run bin/test with "
            f"python{FLOOR_TEXT} or newer."
        )
    # After the strategy is chosen, never before it: a note that a build is
    # starting is a lie on the path that cannot build one.
    print(
        f"bin/test: building {venv} with {how}. The first run pays for it; "
        "every run after it reuses it.",
        file=sys.stderr,
    )
    for step in steps:
        if subprocess.run(step).returncode != 0:
            return (
                "bin/test could not build the virtualenv at "
                f"{venv}: the command above exited non-zero. Remove that "
                "directory and run bin/test again, or build it by hand with "
                "pytest in it."
            )
    hide_from_git(venv)
    return None


def ensure(venv):
    """The interpreter to run pytest with, or None after saying why not."""
    if has_pytest(venv):
        return venv_python(venv)
    problem = build(venv)
    if problem:
        print(problem, file=sys.stderr)
        return None
    if not has_pytest(venv):
        print(
            f"bin/test: built {venv} and pytest is still not in it. "
            "Remove that directory and run bin/test again.",
            file=sys.stderr,
        )
        return None
    return venv_python(venv)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = repo_root()
    if not (root / "tests").is_dir():
        print(
            "bin/test runs SpecSeal's own test suite, and there is no tests "
            f"directory at {root}. Run it from a clone of the SpecSeal "
            "repository.",
            file=sys.stderr,
        )
        return 2
    python = ensure(root / ".venv")
    if python is None:
        return 2
    print(f"bin/test: {python}", file=sys.stderr)
    # No `-n auto`: pytest-xdist is installed by `.github/workflows/test.yml`,
    # not by this virtualenv, so passing it would fail on every fresh build.
    # Arguments pass through, so add xdist and pass it yourself if you want it.
    command = [str(python), "-m", "pytest", *(argv or ["tests"])]
    return subprocess.run(command, cwd=str(root)).returncode


if __name__ == "__main__":
    raise SystemExit(main())
