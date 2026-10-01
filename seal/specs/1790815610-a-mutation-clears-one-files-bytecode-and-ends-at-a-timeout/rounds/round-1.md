# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — review round 1

| Field | Value |
|---|---|
| Target SHA | 6b01b1840e05233492a3dc6a0cfb48244f46ff67 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 698 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `d6ce226a5a771b2f7d08aed094c3f29871f765e2..2d47fbbd46e886bd4152845153801341a408e336`, 4 commits |
| Contract changes | _end → round-1-report.md, round-1.md, run_cases, pytest; mutation_run → main; test_a_process_outside_the_group_does_not_hold_the_verdict_back → pytest only |
| New units | NO_BASELINE (depth 1); COULD_NOT_RUN (depth 1); FAILS_ON_THE_MUTANT (depth 1); red_on (depth 1); seen_runs (depth 1); test_bytecode_the_baseline_wrote_is_gone_before_the_mutated_run (depth 1); LOCKS_THE_MUTANT (depth 1); test_a_restore_whose_write_raises_is_not_restored_and_exits_two (depth 1); test_cases_that_fail_without_the_mutation_measure_nothing (depth 1); test_a_path_that_cannot_be_read_measures_nothing_and_exits_two (depth 1); LEAVES_A_CHILD_ON_THE_OUTPUT (depth 1); test_cases_that_exit_but_leave_a_child_on_the_output_read_red_at_once (depth 1); PRINTS_NOT_UTF8 (depth 1); test_output_that_is_not_utf8_does_not_cost_the_verdict (depth 1); starts_a_child (depth 1) |
| Needs a fix | yes — 🔴 1 (a baseline before the write, so a red means a case failed because of the mutation), and 🟡 2, 🟡 3, 🟡 4, 🟡 5 |
| Loses a record or crashes | yes — 🟡 2 leaves the mutant on disk with a traceback and exit 1, and 🟡 3 crashes with a traceback and exit 1 on a missing path |

- [x] Pass

## What this round was asked

Round 1 targets `6b01b184` and the diff `cd24f516..6b01b184`, the whole build. A false `red` is the worst defect a mutation command can have, so the round was asked to attack seven things:
1. False red and false SURVIVED: same-length mutations inside one second, a module loaded by path from outside `tests/`, a cache under another interpreter tag, `PYTHONPYCACHEPREFIX`, and the inherited `PYTHONDONTWRITEBYTECODE=1`.
2. That every exit path restores from kept bytes and checks sha256.
3. That the bound ends a grandchild on POSIX, that the reap is bounded, and that the Windows verdict is truthful.
4. That the exit codes and verdict lines are documented and pinned.
5. That nothing still claims the command is faster, and whether `-p no:xdist` should be the default.
6. The five re-stamped ledger rows and the `agents/smith.md` rider.
7. The class: every other place telling an agent to clear only `tests/__pycache__`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | Any non-zero exit reads `red` and nothing runs the cases unmutated first, so a `-k` that selects nothing (exit 5), a mistyped module (exit 4) or a case already failing reads `red`, exit 0, for a file no case read | `skills/verify/scripts/mutation_check.py:255` | **fixed** `a4ab9dc0` | fixed at a4ab9dc0; Executed: all three probes printed `red` and exited 0 against a target no case imports. The spec's *Failure direction* omits this third way |
| 🟡 2 | A restore whose write raises (`PermissionError`, a missing directory, a Ctrl-C inside the write) escapes the `NotRestored` arm: the mutant stays on disk, a traceback is printed, exit 1; on an interrupt, `interrupted` claims the file was restored | `skills/verify/scripts/mutation_check.py:302-306` | **fixed** `a4ab9dc0` | fixed at a4ab9dc0; Executed: cases that `chmod 444` the target left `VALUE = 25` on disk with exit 1. The interrupt path is read |
| 🟡 3 | Any exception `main` does not name exits 1, SURVIVED's code: a missing path, a directory, an `OSError` from the cache step, an output decode error | `skills/verify/scripts/mutation_check.py:355-383` | **fixed** `a4ab9dc0` | fixed at a4ab9dc0; Executed: a missing path and a directory each exited 1 with a traceback. The docstring and `SKILL.md` promise exit 2 for every run that measured nothing |
| 🟡 4 | The wait is on the output pipe, so cases that exit but leave a process holding it read `timed out` after the whole bound | `skills/verify/scripts/mutation_check.py:190-192` | **fixed** `a4ab9dc0` | fixed at a4ab9dc0; Executed: cases that exited 1 at once printed `timed out after 3s`, exit 2, at the 3 s bound; at the default that is 300 s per mutation |
| 🟡 5 | The `not restored` verdict word and the `errors="replace"` output decode survive mutation, so a renamed verdict or a crash on non-UTF-8 output would go unseen (§14) | `skills/verify/scripts/mutation_check.py:107` | **fixed** `a4ab9dc0` | fixed at a4ab9dc0; Executed with `bin/mutation-check`: both SURVIVED against the new module, and so did two cosmetic units (`:212-213`, `:388`) |
| ⬜ 6 | `questions.md` Q1 says the smith's example carries `-p no:xdist`; the example in `agents/smith.md` does not, and the prose beside it does | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` | answered | corrected at f0bce32e; Q1's cell now names where `-p no:xdist` is written, with a `Corrected` note; Read `agents/smith.md:268-280`. A paperwork correction, outside `Needs a fix` |
| ⬜ 7 | A relative `PYTHONPYCACHEPREFIX` with a `--cwd` other than the shell's is cleared under the wrong mirror | `skills/verify/scripts/arm_check.py:783-789` | answered | The defect is in `arm_check.py#clear_bytecode_cache`, which this branch reuses unedited and `arm-check --cwd` reaches the same way, so it predates the branch. Recorded in `overview.md` §Not done beside the `run_arms` baseline row, for the repository owner; Read only. It lives in `arm_check.py`, which C2 keeps unedited |
| ⬜ 8 | "the verdict says so" / "the verdict names the exception" for an escaped process: the verdict names the possibility, never the event | `skills/verify/SKILL.md` §*`mutation-check` asks condition 2 of one unit* | **fixed** `a4ab9dc0` | fixed at a4ab9dc0; Read: `timed_out_detail` prints the same sentence whether or not anything escaped |
| 🟢 | The class §12 names is closed: no shipped file still tells an agent to clear `tests/__pycache__` or any named cache directory | `agents/`, `skills/`, `docs/`, `templates/` | confirmed | Executed: `git grep` over the tracked tree outside `seal/` and `CHANGELOG.md` |
| 🟢 | The inherited `PYTHONDONTWRITEBYTECODE=1` class is closed in `tests/test_arm_check.py` and the new module | `tests/test_arm_check.py:1066-1131` | confirmed | Executed: both modules pass with the variable set, 101 passed, 2 skipped; grep finds no third import-planted cache |
| 🟢 | The five release rows and the rider are re-read and re-stamped, and the notes say what changed | `seal/releases/0.6.0.md`, `0.8.1.md`, `0.9.5.md`, `0.12.0.md`, `0.15.1.md` | confirmed | Executed: `evidence-check .` 3188 ok, 0 drifted; `rider_check.py` 20 ok. Notes read |
| 🟢 | No shipped document or record claims the command is faster; L5 says the target was not met | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L5 | confirmed | Executed: grep over the added lines; L5 and phase 4 read |
| 🟢 | The POSIX bound reaches pytest and its xdist workers through `bin/test` | `skills/verify/scripts/mutation_check.py#run_cases` | confirmed | Executed: 8 s bound, both xdist settings, `pgrep` empty afterwards |
| ❓ | The Windows arm: `proc.kill()` on expiry, the text it prints, and `bin/mutation-check.cmd` reaching the script | `skills/verify/scripts/mutation_check.py:207-208`, `bin/mutation-check.cmd` | ❓ out of verified scope | No Windows machine here. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request, which runs S6 but times nothing out |

## Paste-ready fixes

```python
NO_BASELINE = "no baseline"
```
```python
    # The cases must pass against the file as it is first. Otherwise a failure
    # under the mutation says nothing about the mutation: a `-k` that selects
    # nothing exits 5, a mistyped module exits 4, a case already failing exits
    # 1, and each read `red` -- *a case watches this unit* -- for a unit no
    # case ran against.
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
```
```python
# Fails only when the file it is handed holds the mutation, so the baseline
# run passes and the mutated run is red.
FAILS_ON_THE_MUTANT = """\
import sys
with open(sys.argv[1], encoding="utf-8") as f:
    sys.exit(1 if "VALUE = 2" in f.read() else 0)
"""
```
```
- exit 2 for every run that measured nothing: `no baseline` (the cases fail
  without the break, so nothing was written), `timed out`, `could not
  start`, `could not run`, `refused` (nothing was written), `not restored`
  (the file may still hold the break; restore it from your commit), and
  `interrupted`.
```
```python
    finally:
        try:
            restore(path, original, original_sha)
        except RuntimeError as exc:
            raise NotRestored(str(exc)) from exc
        except BaseException as exc:
            # A write that raised -- the cases made the file read-only or
            # removed its directory, or a second Ctrl-C landed inside the
            # write -- is a restore that did not land as surely as a hash
            # that differs.
            raise NotRestored(
                f"{path} was not restored: writing it back raised "
                f"{type(exc).__name__}: {exc}."
            ) from exc
        clear_bytecode_cache(path)
```
```python
COULD_NOT_RUN = "could not run"
```
```python
    except Exception as exc:
        # Anything else measured nothing. Left to Python, an uncaught
        # exception exits 1, which is SURVIVED's code, so a mistyped path or
        # a cache that could not be removed read as "nothing watches this
        # unit". The file was restored on the way out, or `NotRestored`
        # above would have been raised instead.
        print(
            f"{COULD_NOT_RUN}: {type(exc).__name__}: {exc}. No verdict.",
            flush=True,
        )
        return 2
```
```python
import tempfile


def _wait(proc: subprocess.Popen, timeout: float | None):
    """The one wait, a function of its own so a case can interrupt it.

    On the process and not on a pipe: a process the cases started can hold a
    pipe open after they exit, and a wait on the pipe then reads a finished
    run as one that never returned."""
    return proc.wait(timeout=timeout)


def _end(proc: subprocess.Popen, how: str) -> None:
    """End what the run started and reap it. The group on POSIX, because
    `bin/test` execs a runner that starts pytest as a child of its own
    (#313); the direct child elsewhere."""
    if how == GROUP:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif proc.poll() is None:
        proc.kill()
    proc.wait()


def run_cases(command, *, cwd, env, timeout, how=None):
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
        # The cases have exited; whatever they left in the group goes with
        # them, so nothing the run started outlives the verdict.
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
```
```python
    # in test_a_restore_that_did_not_land_stops_the_run_and_says_so, after the
    # existing asserts:
    assert text.startswith("not restored:"), (
        f"the line that says the file still holds a mutation lost its verdict word: {text}"
    )


# Prints bytes that are not UTF-8, then fails only on the mutant.
PRINTS_NOT_UTF8 = """\
import sys
sys.stdout.buffer.write(b"\\xff\\xfe\\n")
sys.stdout.flush()
with open(sys.argv[1], encoding="utf-8") as f:
    sys.exit(1 if "VALUE = 2" in f.read() else 0)
"""


def test_output_that_is_not_utf8_does_not_cost_the_verdict(tmp_path, capsys):
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, PRINTS_NOT_UTF8), target),
        ],
        capsys,
    )
    assert code == 0 and out.startswith("red"), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the new module and `tests/test_arm_check.py`, `-q -p no:xdist`, at `6b01b184` | exit 0; 101 passed, 2 skipped |
| The same with `PYTHONDONTWRITEBYTECODE=1` in the environment | exit 0; 101 passed, 2 skipped |
| `bin/evidence-check .`, unscoped | exit 0; 3188 ok, 0 drifted, 0 broken; records 1 work item read, 0 drifted |
| `python3 .github/scripts/rider_check.py` | exit 0; 20 ok, 0 drifted, 0 broken |
| `mutation-check` with `--tests "bin/test tests/test_arm_check.py -q -p no:xdist -k <a name no case has>"` on a file no case imports | `red … (exit 5)`, exit 0 |
| The same with a module path that does not exist | `red … (exit 4)`, exit 0 |
| The same with a test file whose one case fails unmutated | `red … (exit 1)`, exit 0 |
| `mutation-check` on a missing path, and on a directory | traceback, exit 1, both |
| `mutation-check` whose cases `chmod 444` the target | traceback (`PermissionError`), exit 1, file left as `VALUE = 25` |
| Same-length break over a 3.13 import-written `.pyc`, runner 3.14, cases loading by `spec_from_file_location`; and with an absolute `PYTHONPYCACHEPREFIX` | `red`, exit 0, no `.pyc` left, both |
| `--timeout 8` over `bin/test` running a 40 s case, `-n auto` and `-p no:xdist` | `timed out after 8s`, exit 2, 8.1 s; `pgrep` found nothing, both |
| Cases that start a same-group background child and exit 1, `--timeout 3` | `timed out after 3s`, exit 2, after 3.1 s |
| `bin/mutation-check` on four units of `mutation_check.py`, against the new module | all four SURVIVED (finding 5's table); `git status --porcelain` empty afterwards |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: nobody has run it on this branch, and it is the sealer's once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `arm_check.py#run_arms` reads any non-zero exit as `killed` with no baseline, so an arm no case ran against can be recorded as watched: finding 1's class, in a file C2 keeps unedited | a new issue, beside #313 (which already asks for `run_arms`' bound to be decided) | the orchestrator, who files it when the pull request is opened |
