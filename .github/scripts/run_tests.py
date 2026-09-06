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
THIS repository's suite**, and `.github/scripts/` is where this repository's
own automation already lives. That location hides nothing: the plugin ships
from the repository root, so a user's cache holds `.github/scripts/` and
`tests/` beside `bin/` -- read at 0.5.0, 0.7.0, 0.8.0 and 0.8.1.

What keeps a plugin user out of this suite is that `test` is a shell builtin,
so PATH never offers `bin/test` however many copies are on it; reaching this
file means typing a path into a versioned cache directory on purpose. The
check below is for the other case, a copy of `bin/` taken on its own.

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
    """True when `venv` holds an interpreter and a pytest to run it with.

    Filesystem only, no subprocess: this runs on every warm call, and the
    whole point of the work item is that a warm call costs nothing.

    Whether that interpreter is new enough is a separate question and
    `ensure` asks it, by reading `pyvenv.cfg` rather than by starting
    anything. Both stay off the subprocess path.
    """
    scripts = venv / ("Scripts" if os.name == "nt" else "bin")
    return venv_python(venv).exists() and any(scripts.glob("pytest*"))


def venv_version(venv):
    """The Python version `venv` was built with, from `pyvenv.cfg`, or None.

    Both builders record it -- `uv venv` writes `version_info`, `python -m
    venv` writes `version` -- so the floor can be checked by reading a file
    rather than by starting an interpreter, which a warm call must not pay
    for.

    None means the file says nothing this can read, and None is NOT a
    refusal. A directory with no readable version is not evidence of an old
    interpreter, and refusing on silence turns one unknown into a suite
    nobody can run.
    """
    try:
        text = (venv / "pyvenv.cfg").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines():
        name, sep, value = line.partition("=")
        if not sep or name.strip() not in ("version", "version_info"):
            continue
        parts = []
        for chunk in value.strip().split("."):
            if not chunk.isdigit():
                break
            parts.append(int(chunk))
        return tuple(parts) if len(parts) >= 2 else None
    return None


def hide_from_git(venv):
    """Write the ignore that keeps the virtualenv out of `git status`.

    `uv venv` writes this itself; `python -m venv` does not (checked on
    3.12 -- no `.gitignore` at all). So the runner writes it whichever built
    the directory, rather than the ignore holding only for one of the two.

    Inside the directory rather than in the repository's own `.gitignore`:
    the thing being ignored carries its own ignore, so removing the
    virtualenv removes the rule with it.

    Called from `ensure`'s `finally`, and from `build`'s so that `build`
    keeps its own house in order for the directory it makes.

    NAMING the paths is what this used to do, and the enumeration came up
    short twice. Review round 1 added a build that failed partway and a
    `.venv` the runner merely adopts; round 2 found a third the list had
    missed -- the one adopted `.venv` the FLOOR refuses, which is also the
    one least likely to carry an ignore of its own, since every version that
    refusal rejects is older than the 3.13 where `python -m venv` began
    writing one -- and a probe for that one found a fourth beside it, a
    directory an earlier run left on a machine where neither builder can now
    finish. A list of paths goes short again the next time one is added.

    A guarantee stated over EXITS cannot, because `main` reaches a virtualenv
    through `ensure` and through nothing else: nothing returns from `ensure`
    leaving a `.venv` git can see. Doing nothing when the directory is absent
    is what makes that safe on the exits that never made one.
    """
    if not venv.is_dir():
        return
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
    # `finally`, and it opens here rather than at the top of the function: the
    # branch above returns a string for a path that never makes a directory,
    # and the ignore is owed by every path that does. The install step is the
    # one that fails on a machine with no network, and by then `uv venv` has
    # already made the directory -- so the run that ends in a sentence was the
    # run leaving a virtualenv in `git status`.
    try:
        for step in steps:
            if subprocess.run(step).returncode != 0:
                return (
                    "bin/test could not build the virtualenv at "
                    f"{venv}: the command above exited non-zero. Remove that "
                    "directory and run bin/test again, or build it by hand with "
                    "pytest in it."
                )
    finally:
        hide_from_git(venv)
    return None


def ensure(venv):
    """The interpreter to run pytest with, or None after saying why not.

    The floor is asked of an ADOPTED environment as well as of a built one.
    `build` holds it two ways -- `uv venv --python ">=3.12"`, and the refusal
    below it -- and neither runs on the warm path, so a `.venv` left by an
    older interpreter ran the suite on a version nothing here supports and
    said nothing about it.

    The `finally` is where the ignore is written, and it is the whole of the
    guarantee: this function is the only way `main` reaches a virtualenv, so
    every path that can leave one behind is an exit of this function. It
    covers the directory this call built and the one it merely found, on the
    exit that succeeds and on every exit that refuses -- including the refusal
    directly below, which returned one line above the ignore it owed. No
    count, deliberately: a number here is a list again, and the next `return`
    falsifies it. `hide_from_git` does nothing when there is no directory.
    """
    try:
        if has_pytest(venv):
            found = venv_version(venv)
            if found is not None and found[:2] < FLOOR:
                print(
                    f"bin/test: the virtualenv at {venv} was built with Python "
                    f"{'.'.join(str(part) for part in found)}, below the "
                    f"{FLOOR_TEXT} floor this repository supports. Remove that "
                    "directory and run bin/test again to build it afresh.",
                    file=sys.stderr,
                )
                return None
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
    finally:
        hide_from_git(venv)


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
