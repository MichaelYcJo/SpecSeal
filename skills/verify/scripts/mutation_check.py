#!/usr/bin/env python3
"""Run one mutation of one unit, and say whether a case noticed.

#641, with #129. `agents/smith.md` asks the implementer to break every unit it
added, one at a time, and watch a case go red. Typed by hand that is three
acts per mutation -- an edit, a run, an edit back -- and every one of them
has gone wrong in this repository's history:

  the break      a pattern that missed by two spaces wrote nothing, and the
                 run recorded a verdict for a mutation never applied
  the run        a stale `.pyc` beside the mutated file made the interpreter
                 run the previous mutation instead of this one (#89, #370),
                 and nothing bounded a run that hung -- one did, for 32
                 minutes (#577)
  the edit back  `git checkout -- <file>` restores the committed state and
                 takes every uncommitted fix in the file with it

So this is the loop as one command:

    mutation-check <file> --replace OLD NEW --tests "<command>" [--timeout S]

It refuses a replacement that does not land exactly once, before anything is
written. It writes the break, removes the mutated file's cached bytecode for
every interpreter tag, runs the command with `PYTHONDONTWRITEBYTECODE=1` under
a bound, puts the file back from the bytes it read first and compares their
sha256, removes the bytecode again, and prints one verdict line, then the
command's own output.

  red              exit 0   a case failed against the mutation
  SURVIVED         exit 1   the cases passed, so nothing they run watches it
  timed out        exit 2   the bound was reached; no verdict
  could not start  exit 2   the command could not be spawned; no verdict
  refused          exit 2   nothing was written
  not restored     exit 2   the file on disk may still hold the mutation

Exit 2 is everything that measured nothing, so `mutation-check ... &&
mutation-check ...` stops at the first unit nothing watches or the first run
that could not say.

**The cache that matters is the mutated file's, and only that one.** CPython
reads a `.pyc` instead of the source whenever the size and the whole-second
mtime it recorded still match, and a same-length mutation written inside one
second is that match. An importer's bytecode is valid for its unchanged
source and is never stale, so clearing `tests/__pycache__` recompiled every
test module per run and missed the cache that was. The removal is
`arm_check.clear_bytecode_cache`, which takes `<stem>.*.pyc` rather than the
one name `importlib.util.cache_from_source` gives: that name is the calling
interpreter's tag, and on the machine this was built on `python3` is 3.14
while `bin/test`'s virtualenv reads 3.13.

**`arm_check.py` is reached by path, not through `sys.path`.** Both
functions this uses are its own, ledgered there, and a second copy is how two
loops come to disagree. A bare `from arm_check import ...` would resolve only
while this file is run by its path with `PYTHONSAFEPATH` unset, and a case
loading this file by an `importlib` spec meets neither condition. Every other
shipped script that reaches another file does it this way.

**What it does not protect.** The original is held in this process's memory
for the length of one run and nowhere else, so a `SIGKILL` delivered between
the write and the restore leaves the mutation on disk. `agents/smith.md`'s
*commit before you mutate* is what bounds that loss; a copy on disk is #312.

Nothing is read from or written to git.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import shlex
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ARM_CHECK = os.path.join(HERE, "arm_check.py")

# Seconds the command is waited for. `questions.md` Q4 of work item
# 1790815610 holds the grounds: about twice the slowest legitimate mutated run
# the flow logs record (158 s), and a sixth of the hang that cost 32 minutes.
DEFAULT_TIMEOUT = 300.0

RED = "red"
SURVIVED = "SURVIVED"
TIMED_OUT = "timed out"
COULD_NOT_START = "could not start"
REFUSED = "refused"
NOT_RESTORED = "not restored"

EXIT = {RED: 0, SURVIVED: 1}


def _sibling(name: str, path: str):
    """A script beside this one, loaded by path and registered first.

    Registered before it executes because `arm_check.py` uses `from
    __future__ import annotations` with dataclasses, and `dataclasses`
    resolves a string annotation through `sys.modules[cls.__module__]`."""
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


_ARM_CHECK = _sibling("specseal_arm_check_for_mutation_check", ARM_CHECK)
clear_bytecode_cache = _ARM_CHECK.clear_bytecode_cache
restore = _ARM_CHECK.restore


class Refused(Exception):
    """The mutation was not written, and why."""


class NotRestored(Exception):
    """The restore did not land, so the file may still hold the mutation."""


def mutated(text: str, old: str, new: str, path: str) -> str:
    """`text` with `old` replaced by `new`, or `Refused` before any write.

    Exactly once. A pattern that lands nowhere is the edit that silently did
    not happen, and one that lands twice breaks two units at once, so the
    verdict cannot say which of them a case caught."""
    if not old:
        raise Refused("OLD is empty, so there is nothing to replace")
    if old == new:
        raise Refused(
            "NEW is identical to OLD, so the file would not change and every "
            "run would read SURVIVED for a mutation nobody made"
        )
    count = text.count(old)
    if count != 1:
        raise Refused(
            f"OLD occurs {count} times in {path}; it must occur exactly once. "
            f"Nothing was written. Widen OLD until it names one place."
        )
    return text.replace(old, new, 1)


def run_cases(command: list[str], *, cwd: str, env: dict, timeout: float | None):
    """Run the cases once. `(verdict, detail, output)`."""
    try:
        done = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.output or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", "replace")
        return TIMED_OUT, f"after {timeout:g}s: no verdict", output
    except OSError as exc:
        return COULD_NOT_START, f"{type(exc).__name__}: {exc}", ""
    if done.returncode != 0:
        return (
            RED,
            f"the cases failed against the mutation (exit {done.returncode})",
            done.stdout,
        )
    return (
        SURVIVED,
        "the cases passed against the mutation, so nothing they run watches this unit",
        done.stdout,
    )


def mutation_run(
    path: str,
    old: str,
    new: str,
    command: list[str],
    *,
    cwd: str,
    timeout: float | None = DEFAULT_TIMEOUT,
):
    """Write one mutation, run the cases, restore. `(verdict, detail, output)`.

    `Refused` before any write; `NotRestored` when the restore did not land,
    which replaces whatever the run said."""
    with open(path, "rb") as f:
        original = f.read()
    original_sha = hashlib.sha256(original).hexdigest()
    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refused(f"{path} is not UTF-8 text ({exc}); nothing was written") from exc
    after = mutated(text, old, new, path)

    # Both halves of the bytecode step, as `arm_check.run_arms` has them: the
    # removal takes what was there before the run, and the variable stops the
    # run writing more. The removal is repeated after the restore for a
    # command that builds its own environment and writes the mutant's `.pyc`
    # anyway.
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        with open(path, "wb") as f:
            f.write(after.encode("utf-8"))
        clear_bytecode_cache(path)
        return run_cases(command, cwd=cwd, env=env, timeout=timeout)
    finally:
        try:
            restore(path, original, original_sha)
        except RuntimeError as exc:
            raise NotRestored(str(exc)) from exc
        clear_bytecode_cache(path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="mutation-check",
        description=(
            "Run one mutation of one unit: write it, run the cases, restore "
            "the file from held bytes, and say whether a case noticed."
        ),
    )
    parser.add_argument("path", help="the file to mutate; any UTF-8 text file")
    parser.add_argument(
        "--replace",
        nargs=2,
        metavar=("OLD", "NEW"),
        required=True,
        help=(
            "literal text, no regex. OLD must occur exactly once or nothing "
            "is written; NEW may be empty"
        ),
    )
    parser.add_argument(
        "--tests",
        required=True,
        help='the command the cases run as, e.g. --tests "bin/test tests/test_x.py -q -k y"',
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=(
            f"seconds the command is waited for before the run is a `timed "
            f"out` with no verdict; default {DEFAULT_TIMEOUT:g}, 0 removes the bound"
        ),
    )
    parser.add_argument("--cwd", default=None, help="working directory for --tests")
    args = parser.parse_args(argv)
    if args.timeout < 0:
        parser.error(
            "--timeout takes a non-negative number of seconds, and 0 removes "
            "the bound. A negative value ends every run before it starts."
        )
    command = shlex.split(args.tests)
    if not command:
        parser.error("--tests names no command")

    started = time.monotonic()
    try:
        verdict, detail, output = mutation_run(
            args.path,
            args.replace[0],
            args.replace[1],
            command,
            cwd=args.cwd or os.getcwd(),
            timeout=args.timeout or None,
        )
    except Refused as exc:
        print(f"{REFUSED}: {exc}", flush=True)
        return 2
    except NotRestored as exc:
        print(
            f"{NOT_RESTORED}: {exc} Restore it from your own commit before "
            f"anything else reads it.",
            flush=True,
        )
        return 2
    elapsed = time.monotonic() - started
    print(f"{verdict}: {detail} ({elapsed:.1f}s)", flush=True)
    if output.strip():
        print(output.rstrip("\n"), flush=True)
    return EXIT.get(verdict, 2)


if __name__ == "__main__":
    sys.exit(main())
