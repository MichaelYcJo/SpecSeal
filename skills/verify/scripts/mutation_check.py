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
run. It runs the command once against the file as it is, and goes on only if
that passes: a red means a case failed BECAUSE of the break, never because
the command selected nothing or a case was already failing. Then it writes
the break, removes the mutated file's cached bytecode for every interpreter
tag, runs the command with `PYTHONDONTWRITEBYTECODE=1` under a bound, puts
the file back from the bytes it read first and compares their sha256,
removes the bytecode again, and prints one verdict line, then the command's
own output. The bound applies to each of the two runs.

  red              exit 0   a case failed against the mutation
  SURVIVED         exit 1   the cases passed, so nothing they run watches it
  no baseline      exit 2   the cases fail without the break; nothing written
  timed out        exit 2   the bound was reached; no verdict
  could not start  exit 2   the command could not be spawned; no verdict
  could not run    exit 2   anything else went wrong; no verdict
  refused          exit 2   nothing was written
  not restored     exit 2   the file on disk may still hold the mutation
  interrupted      exit 2   Ctrl-C; the run was ended and the file restored

Exit 2 is everything that measured nothing, so `mutation-check ... &&
mutation-check ...` stops at the first unit nothing watches or the first run
that could not say.

**The bound ends what the run started, not only the process it spawned.**
`subprocess.run`'s timeout kills the direct child, and `bin/test` execs a
runner that starts pytest as a child of its own, so a run bounded that way
leaves the suite running past the verdict -- #313 measured it on `arm-check`,
and the case for S5 re-measures it here. On POSIX the command runs in a
session of its own and a timed-out run's whole process group is killed; so
is the group of a run that exited, which ends whatever the cases left
behind. The wait is on the process and the output goes to a temporary file,
so nothing the cases leave can hold the wait open. Two consequences come with
the session. A process that puts itself in yet another session is outside
the group and outlives the kill; the verdict names that as the bound's
limit, without being able to tell whether it happened. And the terminal's
Ctrl-C now reaches this process alone, so the `KeyboardInterrupt` it raises
here is what ends the group, before the restore. On Windows the direct child
is ended, and the verdict says that anything it started was not: a group
kill there needs a job object, and nobody runs this on Windows to show one
works (#313's third option).

**The cache that matters is the mutated file's, and only that one.** CPython
reads a `.pyc` instead of the source whenever the size and the whole-second
mtime it recorded still match, and a same-length mutation written inside one
second is that match. An importer's bytecode is valid for its unchanged
source and is never stale, so clearing `tests/__pycache__` removed caches
that were right and missed the one that was not. The removal is
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
import signal
import subprocess
import sys
import tempfile
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
INTERRUPTED = "interrupted"
NO_BASELINE = "no baseline"
COULD_NOT_RUN = "could not run"

EXIT = {RED: 0, SURVIVED: 1}

# What the bound ends. `strategy` picks one per platform.
GROUP = "process group"
CHILD = "direct child"


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


def strategy(os_name: str) -> str:
    """What the bound ends on this platform. Takes the platform as an
    argument so the Windows half is pinned from any machine (contract §13)."""
    return CHILD if os_name == "nt" else GROUP


def timed_out_detail(timeout: float, how: str) -> str:
    """The verdict's text for a run the bound ended, saying what it ended."""
    if how == GROUP:
        return (
            f"after {timeout:g}s: no verdict. The command's whole process group "
            f"was ended, so nothing it started outlives this line unless it "
            f"put itself in a session of its own"
        )
    return (
        f"after {timeout:g}s: no verdict. Only the command's own process was "
        f"ended; anything it started was not ended and may still be running"
    )


def _wait(proc: subprocess.Popen, timeout: float | None):
    """The one wait, a function of its own so a case can interrupt it.

    On the process and not on a pipe. A process the cases started can hold a
    pipe open after they exit, and a wait on the pipe then read a run that
    finished red at once as one that never returned (round 1, 🟡 4)."""
    return proc.wait(timeout=timeout)


def _end(proc: subprocess.Popen, how: str) -> None:
    """End what the run started and reap it.

    The group on POSIX: `bin/test` execs a runner that starts pytest as a
    child of its own, so ending the direct child alone leaves the suite
    running past the verdict (#313). Called after a normal exit too, so what
    the cases left in the group goes with them. A group already gone is not
    an error: the command can finish between the bound and the kill."""
    if how == GROUP:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:
        # A no-op once the process has been reaped: `Popen.send_signal`
        # checks `returncode` first.
        proc.kill()
    proc.wait()


def run_cases(
    command: list[str],
    *,
    cwd: str,
    env: dict,
    timeout: float | None,
    how: str | None = None,
):
    """Run the cases once. `(verdict, detail, output)`.

    On POSIX the command runs in a session of its own, which is what lets the
    bound end everything it started. It also takes the command out of the
    terminal's process group, so a Ctrl-C reaches this process alone; the
    `KeyboardInterrupt` arm below is what passes it on, before the restore.

    The output goes to a temporary file rather than a pipe, so nothing the
    cases leave behind can hold this process's wait open. It is decoded with
    `errors="replace"`: the cases' output is shown, not trusted to be UTF-8."""
    how = how or strategy(os.name)
    with tempfile.TemporaryFile("w+", encoding="utf-8", errors="replace") as sink:
        try:
            proc = subprocess.Popen(
                command,
                cwd=cwd,
                env=env,
                stdout=sink,
                stderr=subprocess.STDOUT,
                start_new_session=how == GROUP,
            )
        except OSError as exc:
            return COULD_NOT_START, f"{type(exc).__name__}: {exc}", ""
        try:
            _wait(proc, timeout)
        except subprocess.TimeoutExpired:
            _end(proc, how)
            sink.seek(0)
            return TIMED_OUT, timed_out_detail(timeout, how), sink.read()
        except KeyboardInterrupt:
            _end(proc, how)
            raise
        _end(proc, how)
        sink.seek(0)
        output = sink.read()
    if proc.returncode != 0:
        return (
            RED,
            f"the cases failed against the mutation (exit {proc.returncode})",
            output,
        )
    return (
        SURVIVED,
        "the cases passed against the mutation, so nothing they run watches this unit",
        output,
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
    """Run the cases against the file as it is, then write one mutation, run
    them again, and restore. `(verdict, detail, output)`.

    `Refused` before any run; `NO_BASELINE` when the cases fail before the
    write; `NotRestored` when the restore did not land, which replaces
    whatever the run said."""
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

    # The cases must pass against the file as it is first. Otherwise a failure
    # under the mutation says nothing about the mutation: a `-k` that selects
    # nothing exits 5, a mistyped module exits 4, a case already failing exits
    # 1, and each read `red` -- *a case watches this unit* -- for a unit no
    # case ran against (round 1, 🔴 1).
    clear_bytecode_cache(path)
    before, detail, output = run_cases(command, cwd=cwd, env=env, timeout=timeout)
    if before == RED:
        return (
            NO_BASELINE,
            "the cases fail against the file as it is, so a failure under the "
            "mutation would say nothing about it. Nothing was written",
            output,
        )
    if before != SURVIVED:
        return before, f"{detail}, before the mutation was written", output

    try:
        with open(path, "wb") as f:
            f.write(after.encode("utf-8"))
        # Again after the write: the baseline's cases may have written the
        # original's `.pyc`, which a same-length break matches.
        clear_bytecode_cache(path)
        return run_cases(command, cwd=cwd, env=env, timeout=timeout)
    finally:
        try:
            restore(path, original, original_sha)
        except RuntimeError as exc:
            raise NotRestored(str(exc)) from exc
        except BaseException as exc:
            # A write that raised -- the cases made the file read-only or
            # removed its directory, or a second Ctrl-C landed inside the
            # write -- is a restore that did not land as surely as a hash
            # that differs (round 1, 🟡 2).
            raise NotRestored(
                f"{path} was not restored: writing it back raised "
                f"{type(exc).__name__}: {exc}."
            ) from exc
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
    except KeyboardInterrupt:
        # Reached only after `run_cases` ended what it started and
        # `mutation_run`'s `finally` restored the file -- a failed restore
        # raises `NotRestored` instead, and is reported above.
        print(
            f"{INTERRUPTED}: no verdict. What the run started was ended, and "
            f"{args.path} was restored from the bytes read before the write.",
            flush=True,
        )
        return 2
    except Exception as exc:
        # Anything else measured nothing. Left to Python, an uncaught
        # exception exits 1, which is SURVIVED's code, so a mistyped path or
        # a cache that could not be removed read as "nothing watches this
        # unit" (round 1, 🟡 3). The file was restored on the way out, or
        # `NotRestored` above would have been raised instead.
        print(
            f"{COULD_NOT_RUN}: {type(exc).__name__}: {exc}. No verdict.",
            flush=True,
        )
        return 2
    elapsed = time.monotonic() - started
    # `timed out after 300s: ...` reads as one phrase; the others are a word
    # and what it means.
    joint = " " if verdict == TIMED_OUT else ": "
    print(f"{verdict}{joint}{detail} ({elapsed:.1f}s)", flush=True)
    if output.strip():
        print(output.rstrip("\n"), flush=True)
    return EXIT.get(verdict, 2)


if __name__ == "__main__":
    sys.exit(main())
