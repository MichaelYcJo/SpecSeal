# Review round 1 — `perf/641-129-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout`

Target SHA `6b01b184`, base `release/v0.17.0` (`cd24f516`), diff
`cd24f516..6b01b184`. I reviewed it in a `git clone --no-local` at the target,
which has since been deleted. This is a first round. The work item has no
`round-N.md`, so I carried no coordinates and inherited no verdicts. I read
the build's account (the spawn prompt, `overview.md`, the phase records,
`questions.md`) as claims and checked each one against the code.

How the findings relate:

```
the command's verdict is only as good as the exit code it reads
  ├ ① any non-zero exit reads `red`, with no baseline       (🔴 the false red: `-k` typo, wrong module, a case already failing)
  ├ ③ any uncaught exception exits 1, SURVIVED's code       (🟡 missing path, a directory, an OSError in the cache step)
  │    └ ② a restore that raises is not `not restored`      (🟡 the mutant stays on disk, traceback, exit 1)
  └ ④ the wait is on the pipe, not the process              (🟡 a finished red reads `timed out` after the whole bound)
⑤ `not restored` and the output decode survive mutation     (🟡 §14: a verdict word nothing pins)
⑥–⑧ paperwork and edges                                     (⬜)
```

## Spec compliance

Every scenario S1–S10 has its case, and the cases are green at the target
(executed, below). Constraints C1–C4 hold where I checked them. The
mechanism the spec asked for exists as specified: one replacement that must
land exactly once, the mutated file's bytecode cleared for every tag before
the run and after the restore, `PYTHONDONTWRITEBYTECODE=1`, a restore from
held bytes compared by sha256, and a process-group bound on POSIX.

**Where the spec itself is short.** Its *Failure direction* section says the
loop reports red for the wrong reason "in two ways": a stale cache and a
restore that did not land. There is a third, and it is the common one. The
cases may fail for a reason that has nothing to do with the mutation. Finding
1 is that gap, and the code inherited it from the spec. So I judged it
against the spec's own definition of red in S7 ("a `--tests` that fails
against the mutant"). That definition requires a case to fail *because of*
the mutation, and `run_cases` reads every non-zero exit as red.

### The attacks the prompt asked for

**1. False red / false SURVIVED.**
- **Same-length break within one second.** I planted a real timestamp `.pyc`
  by importing the target with the clone's 3.13 virtualenv. Then I ran
  `bin/mutation-check` under `python3` 3.14 with `VALUE = 15` → `25` and
  cases that load the file by `spec_from_file_location` and assert 15. The
  result was `red`, and no `.pyc` for the target was left (executed). This is M4's
  two-tag machine, run for real rather than with a hand-written foreign tag.
- **Absolute `PYTHONPYCACHEPREFIX`.** The same run with the prefix set in
  the environment was also `red`, with nothing left under the prefix
  (executed).
- **A relative prefix together with `--cwd`.** I did not run this. By
  reading, `clear_bytecode_cache` resolves the prefix against
  `mutation-check`'s own cwd while the cases resolve it against `--cwd`
  (⬜ 7).
- **The inherited `PYTHONDONTWRITEBYTECODE=1`.** Both modules pass with the
  variable set in the environment that runs them: 101 passed, 2 skipped
  (executed). `git grep` over `tests/` for `.pyc`, `cache_from_source`,
  `py_compile` and `sys.dont_write_bytecode` finds no third case that plants
  a cache by import and asserts on it (read). The class is closed.
- **The false red.** Finding 1.

**2. Restore.** Red, SURVIVED, timeout and interrupt all restore. I checked
this by reading and by the cases, and the probe target read `VALUE = 15`
after every run (executed). A refused substitution writes nothing (the S3
cases). Nothing restores from `HEAD`. Two paths break the promise. A restore
whose write raises leaves the mutant on disk and exits 1 with a traceback
(finding 2, executed). A Ctrl-C that lands inside the write-back prints *was
restored* over a file that may be truncated (finding 2, read).

**3. The bound.** Through `bin/test`, with xdist both on (`-n auto`) and off,
an 8 s bound ended the run in 8.1 s, and `pgrep` found no surviving pytest or
worker one second later (executed). The Windows text is truthful: it says
only the command's own process was ended (S6 pins it). A `timed out` is never
printed as red or SURVIVED. The reverse does happen: a run that exited `red`
in 0.1 s printed `timed out` because a child it left held the pipe (finding
4, executed).

**4. Exit codes.** 0, 1 and 2 are documented in `skills/verify/SKILL.md` and
pinned by the S7 cases and by the timeout, refusal and interrupt cases.
`agents/smith.md` names the verdicts and points at the skill for the codes,
and that is enough. The gap is that Python's own exit for an uncaught
exception is also 1 (finding 3), and that the `not restored` word is not
pinned (finding 5).

**5. The speed claim.** No added line in `agents/`, `skills/`, `bin/`,
`tests/` or the changelog fragment claims the command is faster (executed,
grep for *faster*, *recompil*, *142* and *speed* over the added lines). L5
states 0.76 s against 0.84 s and calls the target unmet. The overview records
the divergence from the spec's 142-module premise. On `-p no:xdist`: the
command runs any runner, so it cannot inject a pytest flag, and documenting
the flag is the right place. `SKILL.md`'s example carries it, and
`agents/smith.md` carries it as prose beside a runner-neutral example.
`questions.md` Q1 says the smith's *example* carries it, which is not what
the file holds (⬜ 6). If finding 1's baseline is adopted, each call runs the
cases twice. L5's figures then describe a command that no longer exists, and
Q4's grounds should be re-read.

**6. The ledger.** `evidence-check .`, unscoped, exited 0 with 3188 ok, 0
drifted and 0 broken; the records arm read 1 work item and found 0 drifted.
`rider_check.py` exited 0 with 20 ok (both executed in the clone). I read the
five re-read notes. Each names what changed under its anchor and why the
claim still holds. N1 says the waiver paragraph's `_hides_a_commit` was
re-taken at both ends. I did not re-run that. The note is dated and says who
ran it.

**7. The class.** `git grep` over the tracked tree, outside `seal/` and
`CHANGELOG.md`, finds no remaining instruction to clear `tests/__pycache__`
or any named cache directory, in `agents/warden.md`, the skills, `docs/` or
`templates/` (executed). The mentions that remain are the new prose that
explains why, and walk-skip lists.

## Quality

### 🔴 1 · Any non-zero exit reads `red`, so a `-k` typo makes every unit "watched"

`skills/verify/scripts/mutation_check.py:255` (`run_cases`): `if
proc.returncode != 0: return RED`. Nothing first runs the cases against the
unmutated file. Executed at the target, with a target file that no case
imports:

| `--tests` | Exit the cases gave | Verdict printed | Exit |
|---|---|---|---|
| `bin/test tests/test_arm_check.py -q -p no:xdist -k <a name no case has>` | 5 (no tests collected) | `red: the cases failed against the mutation (exit 5)` | 0 |
| `bin/test <a module path that does not exist> -q -p no:xdist` | 4 (usage error) | `red … (exit 4)` | 0 |
| a test file whose one case is `assert False` | 1 | `red … (exit 1)` | 0 |

Each of these says *a case watches this unit* about a file no case read. It
is the worst direction this command can fail in. The smith reads `red` as
permission to hand over, and a misspelled `-k` costs one keystroke and turns
every mutation in the loop red. Python's own exit for a mutant that breaks
collection is 2, and that is a real red. So the fix is not a list of pytest
codes: it is a baseline. The cases must pass against the file as it is
before a failure against the mutant means anything.

The cost is a second run per call: about 0.47 s becomes about 0.9 s on L5's
module. That is the price of a verdict that cannot be faked by the command
line. The baseline is skipped for nothing, because the smith types the
command once per break and has no other place to learn that the cases did
not run.

The cases are affected. Every case that uses the `FAILS` probe (`sys.exit(1)`
whatever the file holds) would read `no baseline` after the fix. They need a
probe that fails only on the mutant, given in the fix block below.

Class (§12): `skills/verify/scripts/arm_check.py#run_arms` has the same rule
(`by_operator[operator] = run.returncode != 0`) and no baseline, so it can
record `killed` for an arm no case ran against. This branch does not edit
`arm_check.py` (C2), and the defect is not this branch's. I listed it under
*Deferred*.

### 🟡 2 · A restore whose write raises leaves the mutant on disk, prints a traceback and exits 1

`skills/verify/scripts/mutation_check.py:302-306`: the `finally` turns only
`RuntimeError`, the hash mismatch, into `NotRestored`. Executed: cases that
run `chmod 444` on the target. The restore's `open(path, "wb")` raised
`PermissionError`, the run printed a traceback and no verdict line, the exit
was **1** (SURVIVED's code), and the file held `VALUE = 25`. The same happens
when the cases remove the file's directory. A Ctrl-C that lands inside the
write-back raises `KeyboardInterrupt` past the same arm. `main` then prints
`interrupted: … was restored from the bytes read before the write` over a
file that may be half written (read, not timed).

This is the one promise the command exists to keep, and it is the outcome
the `not restored` verdict was written for.

### 🟡 3 · Any other exception exits 1, which is SURVIVED's code

`skills/verify/scripts/mutation_check.py:355-383`: `main` catches `Refused`,
`NotRestored` and `KeyboardInterrupt`, and nothing else. Executed: a path
that does not exist (`FileNotFoundError`) and a directory
(`IsADirectoryError`) each print a traceback and exit **1**. By reading, the
same holds for an `OSError` from `clear_bytecode_cache` on a read-only
`__pycache__`, before or after the run, and for a `UnicodeDecodeError` from
output the cases print if the `errors="replace"` decode ever goes (finding 5
shows nothing pins it).

The module's docstring and `SKILL.md` both say "exit 2 for every run that
measured nothing". A script that branches on the code, or a person reading
`echo $?` per contract §1, reads a mistyped path as *nothing watches this
unit*. A `&&` chain still stops, so the cost is the record and not the
chain.

### 🟡 4 · The wait is on the pipe, so a finished run reads `timed out` after the whole bound

`skills/verify/scripts/mutation_check.py:190-192` and `:248`: `_wait` is
`proc.communicate(timeout=…)`, which returns only when every holder of the
output pipe has closed it. Executed: cases that start a background process in
the same group and then `sys.exit(1)`. The cases exited at once. The verdict
was `timed out after 3s: no verdict`, exit 2, at the 3 s bound. At the
default bound that is 300 s per mutation, and a red that was measured is
reported as one that never returned.

`REAP_TIMEOUT` handles the same hazard after the kill. The cause is one step · NAME NOT IN TREE
earlier: waiting on the pipe instead of on the process. With the output sent
to a temporary file, the wait is on the process, nothing can hold it open,
and `REAP_TIMEOUT` and its escaped-session case have nothing left to guard. · NAME NOT IN TREE
Ending the group after a normal exit as well keeps the docstring's promise
that nothing the run started outlives the verdict.

### 🟡 5 · The `not restored` verdict word and the output decode survive mutation

Executed with the command itself, against the new module (`bin/test
tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py -q
-p no:xdist`):

| Unit | Mutation | Verdict |
|---|---|---|
| `NOT_RESTORED` (`mutation_check.py:107`) | `"not restored"` → `"restored"` | SURVIVED |
| `errors="replace",` (`mutation_check.py:242`) | deleted | SURVIVED |
| `proc.stdout.close()` in `_end` (`:212-213`) | deleted | SURVIVED |
| the elapsed time in the verdict line (`:388`) | dropped | SURVIVED |

The first two matter. `not restored:` is the line that tells a person the
file holds a mutant and to restore it from their commit, and the restore
case passes on the phrase *was not restored*, which the fake's exception
message supplies. If someone renamed the label to `restored:`, every case
would stay green (§14). Without `errors="replace"`, a case that prints a
non-UTF-8 byte crashes the run after the restore (finding 3's exit 1). The
build's account says 31 code mutations went red and every unit was mutated.
These four were not among them. The last two are ⬜-weight: the close is
redundant after a kill, and the elapsed time is cosmetic.

### ⬜ 6 · `questions.md` Q1 says the smith's example carries `-p no:xdist`

`seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md`,
Q1's status: "so the example carries `-p no:xdist`". The example in
`agents/smith.md:268-270` is `--tests "<the runner> <module> -k <cases>"`,
and the flag sits in the prose under it. `SKILL.md`'s example does carry it.
This is a paperwork correction: say *the prose beside the example*, or name
`SKILL.md`. It is not counted in `Needs a fix`.

### ⬜ 7 · A relative `PYTHONPYCACHEPREFIX` with `--cwd` is cleared in the wrong place (read)

`skills/verify/scripts/arm_check.py:783-789` joins the prefix as given.
CPython resolves a relative prefix against the importing process's cwd, and
the cases run in `--cwd`, while `clear_bytecode_cache` runs in
`mutation-check`'s cwd. The two mirrors differ, and the stale `.pyc` stays
where the cases read it. Not executed. It needs a relative prefix and a
`--cwd` that is not the shell's directory together. A
`os.path.abspath(prefix)` taken in the cases' cwd closes it, but it lives in
`arm_check.py`, which C2 keeps unedited.

### ⬜ 8 · "the verdict says so" for an escaped process overstates

`skills/verify/SKILL.md` ("A process that put itself in yet another session
is outside the group, and the verdict says so") and the module docstring
(`mutation_check.py:47-50`, "the verdict names the exception"). The verdict
always says "unless it put itself in a session of its own". It names the
possibility and cannot tell whether one did. After finding 4's fix the
sentence should say what it does: the escape is named as a limit, and the
output stops waiting on it.

### Not judged

The `8a03922c` commit shape (`cd …; git -C … commit`) is a fact about a
command line, and the tree does not hold it. The orchestrator reported it,
and I have no verdict on it.

## Executed and read, kept apart

- **Executed** (in the clone at `6b01b184`): the two narrow modules (twice,
  once under `PYTHONDONTWRITEBYTECODE=1`); `evidence-check .`;
  `.github/scripts/rider_check.py`; the probes in the table below; four
  mutations of the script with `bin/mutation-check`; the class greps.
- **Read**: the whole of `mutation_check.py`, the new test module,
  `arm_check.py#clear_bytecode_cache`, `#restore` and `#run_arms`, the spec,
  the questions, the overview, phase 4, the changelog fragment, the ledger
  row L5 and the five re-read notes, the `agents/smith.md` and `SKILL.md`
  hunks, and both `.cmd` wrappers (they differ only in name and path).
- **Unverified**: the Windows arm (❓ row); the full suite, repository-wide
  lint and the broad gate, which belong to the sealer once the rounds settle.

## Regression tests to plant

All go in
`tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`.
The proposed names do not exist yet (NAME NOT IN TREE).

- For finding 1: a `-k` that selects nothing, and cases that fail without
  the mutation, each give `no baseline`, exit 2, and a byte-identical file.
  Seen red at `6b01b184` by the probe above (`red`, exit 0).
- For finding 2: cases that `chmod 444` the target give `not restored:` and
  exit 2, and no traceback. Seen red at the target (exit 1, traceback).
- For finding 3: a missing path gives exit 2 and a verdict line, not exit 1.
  Seen red at the target.
- For finding 4: cases that exit 1 and leave a background child on the pipe
  give `red` well inside the bound. Seen red at the target (`timed out`).
- For finding 5: the restore case asserts the output starts with `not
  restored:`, and a case prints a non-UTF-8 byte and still gets a verdict.

## Facts for the evidence ledger

These are executed at `6b01b184`, on macOS with `python3` 3.14.4 and the
clone's `.venv` at 3.13.9. They corroborate L1 and L2 if those rows are
re-stamped after the fixes:

- A same-length break of a file that the 3.13 interpreter had cached by
  import, run by `mutation-check` under 3.14 with cases that load the file
  by `spec_from_file_location`, reads `red` and leaves no `.pyc`. So does the
  same run with an absolute `PYTHONPYCACHEPREFIX`.
- Through `bin/test`, with xdist on and off, an 8 s bound leaves no pytest
  process and no worker alive one second after the verdict.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | Any non-zero exit reads `red` and nothing runs the cases unmutated first, so a `-k` that selects nothing (exit 5), a mistyped module (exit 4) or a case already failing reads `red`, exit 0, for a file no case read | `skills/verify/scripts/mutation_check.py:255` | open | Executed: all three probes printed `red` and exited 0 against a target no case imports. The spec's *Failure direction* omits this third way |
| 🟡 2 | A restore whose write raises (`PermissionError`, a missing directory, a Ctrl-C inside the write) escapes the `NotRestored` arm: the mutant stays on disk, a traceback is printed, exit 1; on an interrupt, `interrupted` claims the file was restored | `skills/verify/scripts/mutation_check.py:302-306` | open | Executed: cases that `chmod 444` the target left `VALUE = 25` on disk with exit 1. The interrupt path is read |
| 🟡 3 | Any exception `main` does not name exits 1, SURVIVED's code: a missing path, a directory, an `OSError` from the cache step, an output decode error | `skills/verify/scripts/mutation_check.py:355-383` | open | Executed: a missing path and a directory each exited 1 with a traceback. The docstring and `SKILL.md` promise exit 2 for every run that measured nothing |
| 🟡 4 | The wait is on the output pipe, so cases that exit but leave a process holding it read `timed out` after the whole bound | `skills/verify/scripts/mutation_check.py:190-192` | open | Executed: cases that exited 1 at once printed `timed out after 3s`, exit 2, at the 3 s bound; at the default that is 300 s per mutation |
| 🟡 5 | The `not restored` verdict word and the `errors="replace"` output decode survive mutation, so a renamed verdict or a crash on non-UTF-8 output would go unseen (§14) | `skills/verify/scripts/mutation_check.py:107` | open | Executed with `bin/mutation-check`: both SURVIVED against the new module, and so did two cosmetic units (`:212-213`, `:388`) |
| ⬜ 6 | `questions.md` Q1 says the smith's example carries `-p no:xdist`; the example in `agents/smith.md` does not, and the prose beside it does | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` | open | Read `agents/smith.md:268-280`. A paperwork correction, outside `Needs a fix` |
| ⬜ 7 | A relative `PYTHONPYCACHEPREFIX` with a `--cwd` other than the shell's is cleared under the wrong mirror | `skills/verify/scripts/arm_check.py:783-789` | open | Read only. It lives in `arm_check.py`, which C2 keeps unedited |
| ⬜ 8 | "the verdict says so" / "the verdict names the exception" for an escaped process: the verdict names the possibility, never the event | `skills/verify/SKILL.md` §*`mutation-check` asks condition 2 of one unit* | open | Read: `timed_out_detail` prints the same sentence whether or not anything escaped |
| 🟢 | The class §12 names is closed: no shipped file still tells an agent to clear `tests/__pycache__` or any named cache directory | `agents/`, `skills/`, `docs/`, `templates/` | confirmed | Executed: `git grep` over the tracked tree outside `seal/` and `CHANGELOG.md` |
| 🟢 | The inherited `PYTHONDONTWRITEBYTECODE=1` class is closed in `tests/test_arm_check.py` and the new module | `tests/test_arm_check.py:1066-1131` | confirmed | Executed: both modules pass with the variable set, 101 passed, 2 skipped; grep finds no third import-planted cache |
| 🟢 | The five release rows and the rider are re-read and re-stamped, and the notes say what changed | `seal/releases/0.6.0.md`, `0.8.1.md`, `0.9.5.md`, `0.12.0.md`, `0.15.1.md` | confirmed | Executed: `evidence-check .` 3188 ok, 0 drifted; `rider_check.py` 20 ok. Notes read |
| 🟢 | No shipped document or record claims the command is faster; L5 says the target was not met | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L5 | confirmed | Executed: grep over the added lines; L5 and phase 4 read |
| 🟢 | The POSIX bound reaches pytest and its xdist workers through `bin/test` | `skills/verify/scripts/mutation_check.py#run_cases` | confirmed | Executed: 8 s bound, both xdist settings, `pgrep` empty afterwards |
| ❓ | The Windows arm: `proc.kill()` on expiry, the text it prints, and `bin/mutation-check.cmd` reaching the script | `skills/verify/scripts/mutation_check.py:207-208`, `bin/mutation-check.cmd` | ❓ out of verified scope | No Windows machine here. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request, which runs S6 but times nothing out |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `arm_check.py#run_arms` reads any non-zero exit as `killed` with no baseline, so an arm no case ran against can be recorded as watched: finding 1's class, in a file C2 keeps unedited | a new issue, beside #313 (which already asks for `run_arms`' bound to be decided) | the orchestrator, who files it when the pull request is opened |

## Paste-ready fixes

### 🔴 1 — a baseline before the write (`skills/verify/scripts/mutation_check.py`)

```python
NO_BASELINE = "no baseline"
```

In `mutation_run`, after `after = mutated(text, old, new, path)` and the two
`env` lines, before the `try`:

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

A probe for the cases that used `FAILS` and must now fail only on the
mutant:

```python
# Fails only when the file it is handed holds the mutation, so the baseline
# run passes and the mutated run is red.
FAILS_ON_THE_MUTANT = """\
import sys
with open(sys.argv[1], encoding="utf-8") as f:
    sys.exit(1 if "VALUE = 2" in f.read() else 0)
"""
```

`skills/verify/SKILL.md`, the exit-2 bullet:

```
- exit 2 for every run that measured nothing: `no baseline` (the cases fail
  without the break, so nothing was written), `timed out`, `could not
  start`, `could not run`, `refused` (nothing was written), `not restored`
  (the file may still hold the break; restore it from your commit), and
  `interrupted`.
```

### 🟡 2 — every failed write-back is `not restored` (`mutation_check.py:302-307`)

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

### 🟡 3 — nothing measured exits 2 (`mutation_check.py`, `main`)

```python
COULD_NOT_RUN = "could not run"
```

After the `except KeyboardInterrupt:` arm in `main`:

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

### 🟡 4 — wait on the process, with output in a file (`mutation_check.py:190-250`)

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

`REAP_TIMEOUT` goes. `test_a_process_outside_the_group_does_not_hold_the_verdict_back` · NAME NOT IN TREE
keeps its assertions and drops its `monkeypatch.setattr(mc, "REAP_TIMEOUT", 0.5)`.
`test_a_group_that_ended_on_its_own_at_the_bound_is_not_an_error` asserts
`mc._end(proc, mc.GROUP) is None`.

### 🟡 5 — pin the verdict word and the decode (new module)

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

Needs a fix: yes — 🔴 1 (a baseline before the write, so a red means a case failed because of the mutation), and 🟡 2, 🟡 3, 🟡 4, 🟡 5
Loses a record or crashes: yes — 🟡 2 leaves the mutant on disk with a traceback and exit 1, and 🟡 3 crashes with a traceback and exit 1 on a missing path

The broad gate has not come due: this round leaves 🔴 1 and four 🟡 open,
so the next act is the fix pass and a verifying round, not the sealer.

## Proof block

Files opened this round, all in the clone at `6b01b184` unless noted:

- `skills/verify/scripts/mutation_check.py` (whole)
- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` (whole)
- `skills/verify/scripts/arm_check.py` (`clear_bytecode_cache`, `restore`, `run_arms`)
- `bin/mutation-check`, `bin/mutation-check.cmd`, `bin/arm-check.cmd`, `bin/test`
- `agents/smith.md` (the diff, and lines 255-300 and 383-401)
- `skills/verify/SKILL.md` (the diff)
- `tests/test_arm_check.py` (the diff, and lines 1190-1230)
- `tests/test_chain_hooks.py` (lines 488-540), `tests/test_a_record_states_what_the_tree_has.py` (lines 305-330)
- `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/spec.md`, `questions.md`, `overview.md`, `changelog.md`, `phases/phase-4.md`, `routing.md` (lines 1-40)
- `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` (L1, L5, and the header comment)
- `seal/releases/0.6.0.md`, `0.8.1.md`, `0.9.5.md`, `0.12.0.md`, `0.15.1.md` (the changed rows, through the diff)
- `seal/config.md` in the worktree (for `Record language`; the row is absent, so the record is in English)
