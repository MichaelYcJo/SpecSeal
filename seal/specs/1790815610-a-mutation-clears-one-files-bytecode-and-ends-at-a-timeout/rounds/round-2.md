# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — review round 2

| Field | Value |
|---|---|
| Target SHA | 8b8149b3af8f216e3a3121ee9d0c7ecb8dbc4d21 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 698 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `5365948145b2e2e74171b1f013098d1f3d17f07f..dbd71bca45ccbeb969966a33aed1a6870f02e013`, 4 commits |
| Contract changes | mutation_run → main; test_the_file_is_restored_from_the_bytes_held_before_the_write → pytest only; test_a_run_past_the_bound_is_timed_out_and_leaves_nothing_it_started → pytest only |
| New units | none |
| Needs a fix | yes — 🟡 9 (a read-only target reads `not restored` over its original bytes) and 🟡 10 (the baseline's bound is pinned by no case) |
| Loses a record or crashes | no |
<!-- New units: bin/mutation-check read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 2 is the verifying round. It targets `8b8149b3` and verifies round 1's fix range `d6ce226a..2d47fbbd`, four commits. It was asked to re-run round 1's own probes against each of its eight verdicts, with the class closed. It was also asked to review, as finding surfaces, the units those fixes created: the three new verdict constants, the four probe fixtures, `red_on`, `seen_runs`, `starts_a_child` and seven new cases. Last, it was asked whether the records state the baseline's doubled cost honestly.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding 1 is closed — a failure without the break is `no baseline`, exit 2, nothing written | `skills/verify/scripts/mutation_check.py:313-328` | confirmed | Executed: a `-k` selecting nothing, a missing module and an already failing case each printed `no baseline`, exit 2, file unchanged; M7 and M10 red |
| 🟢 | round 1's finding 2 is closed — a restore whose write raises, an interrupt inside it included, is `not restored`, exit 2 | `skills/verify/scripts/mutation_check.py:337-350` | confirmed | Executed: cases that lock the mutant gave `not restored … PermissionError`, exit 2; a substituted restore that wrote three bytes and raised `KeyboardInterrupt` gave `not restored`, exit 2, file `VAL`; M3 red. The class reaches 🟡 9 |
| 🟢 | round 1's finding 3 is closed — an unnamed exception is `could not run`, exit 2 | `skills/verify/scripts/mutation_check.py:428-438` | confirmed | Executed: a missing path and a directory each exit 2 with no traceback; M8 red |
| 🟢 | round 1's finding 4 is closed — cases that exit but leave a child on the output read at once | `skills/verify/scripts/mutation_check.py:196-267` | confirmed | Executed: `red` in 0.2 s under `--timeout 3`, child gone; escaped child: `red` in 0.4 s, child alive (the documented limit); M5 red |
| 🟢 | round 1's finding 5 is closed — the `not restored` word and the replaced decode are pinned | `skills/verify/scripts/mutation_check.py:116`, `:244` | confirmed | Executed: M11, M4 and M12 (the elapsed time) each red |
| 🟢 | round 1's note 6 is closed — Q1 names where `-p no:xdist` is written | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` | confirmed | Read: the Q1 cell and its `Corrected` note; `agents/smith.md:268-282` |
| 🟢 | round 1's note 7 is answered — the relative-prefix defect predates the branch | `skills/verify/scripts/arm_check.py:783-789` | confirmed | Read: `overview.md` §Not verified records it; `arm_check.py` is not edited in the range |
| 🟢 | round 1's note 8 is closed — the escape sentence names a limit, not an event | `skills/verify/SKILL.md` §*`mutation-check` asks condition 2 of one unit* | confirmed | Read: the SKILL paragraph and the module docstring |
| 🟢 | The group bound still reaches pytest and its xdist workers through `bin/test`, now in the baseline | `skills/verify/scripts/mutation_check.py#run_cases` | confirmed | Executed: 8 s bound, `-n auto` and `-p no:xdist`, `pgrep` empty, target unchanged |
| 🟢 | The one survivor is exempted on sound grounds | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/plan.md:164` | confirmed | Executed: `survivor-check` exit 1 without the table, exit 0 with it; Read: the plan quotes the claim as approved, still true of the mutated run |
| 🟢 | L5 says the baseline doubles a call's cost, and the figure holds | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L5 | confirmed | Executed: 1.01 s mean per call against 0.43 s for one run, on L5's setup |
| 🟡 9 | A target read-only before the command starts reads `not restored` and is told to be restored from a commit, though the break never reached it | `skills/verify/scripts/mutation_check.py:337-350` | **fixed** `d64a5184` | fixed at d64a5184; Executed: `chmod 400` before the run gave `not restored … PermissionError`, exit 2, file `VALUE = 1`; the proposed case red at the target, green with the fix |
| 🟡 10 | The baseline's bound is pinned by no case, and it is now the bound most hangs meet | `skills/verify/scripts/mutation_check.py:319` | **fixed** `d64a5184` | fixed at d64a5184; Executed: `timeout=None` on the baseline SURVIVED the module (M1); the proposed case red under M1 |
| ⬜ 11 | The smith's step list and the wrapper's comment omit the baseline and the bound per run | `agents/smith.md:271-276`, `bin/mutation-check:11-15` | **fixed** `3f8e021e` | fixed at 3f8e021e; Read: SKILL and the docstring were updated, these two were not; behaviour and verdict list stay right |
| ⬜ 12 | The baseline's verdict lines: `no baseline` drops the exit code and its *Nothing was written* is unpinned; `interrupted` in the baseline says the file was restored; the timeout suffix lands on the escape clause | `skills/verify/scripts/mutation_check.py:320-328`, `:418-427` | **fixed** `dbd71bca` | fixed at dbd71bca; Executed: M9 SURVIVED; Ctrl-C substituted into the baseline's wait printed *was restored from the bytes read before the write* |
| ⬜ 13 | correction: Q5 states the per-call command figures with no note that a call now runs the cases twice | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md:42` | answered | corrected at 3f8e021e; Q5 gains a `Corrected` note: a call runs the cases twice, with round 2's measured 1.01 s per call against 0.43 s for one run; Read; L5 carries the note, Q5 does not. Paperwork, outside `Needs a fix` |
| ⬜ 14 | correction: the ledger fragment's header lists L1–L6 and not L7 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-8` | **fixed** `3f8e021e` | fixed at 3f8e021e; Read. Paperwork, outside `Needs a fix` |
| ❓ | The Windows arm: `proc.kill()`, its text, the temporary-file output, and `bin/mutation-check.cmd` | `skills/verify/scripts/mutation_check.py:218-221`, `bin/mutation-check.cmd` | ❓ out of verified scope | No Windows machine here; carried from round 1. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request |

## Paste-ready fixes

```python
def _sha_on_disk(path: str) -> str | None:
    """The sha256 of what `path` holds now, or None when it cannot be read."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None
```
```python
    finally:
        try:
            # A write that never reached the file -- it was read-only before
            # the command started -- leaves nothing to put back, and a restore
            # tried anyway raises the same error and reads `not restored`
            # over a file that holds its original bytes (round 2, 🟡 9).
            if _sha_on_disk(path) != original_sha:
                restore(path, original, original_sha)
        except RuntimeError as exc:
```
```python
@pytest.mark.skipif(
    os.name != "nt" and os.geteuid() == 0, reason="root writes a read-only file"
)
def test_a_target_that_cannot_be_written_is_not_called_unrestored(tmp_path, capsys):
    """Round 2, 🟡 9. A target that is read-only before the command starts
    never takes the break and holds its original bytes, so `not restored`
    there tells a person to restore a file nothing changed."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    os.chmod(target, 0o444)
    try:
        code, out = run(
            [
                target,
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                red_on(tmp_path, target, "VALUE = 2"),
            ],
            capsys,
        )
    finally:
        os.chmod(target, 0o644)
    assert code == 2, out
    assert out.startswith("could not run:"), out
    assert "PermissionError" in out, f"the cause is not named: {out}"
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
```
```python
def test_a_baseline_past_the_bound_is_timed_out_and_writes_nothing(tmp_path, capsys):
    """Round 2, 🟡 10. A hang that does not depend on the break -- the common
    kind -- now happens in the baseline, before anything is written, so that
    run's bound is the one most hangs meet."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    log = tmp_path / "seen.txt"
    appends = SEES_FILE.replace('"w", encoding', '"a", encoding')
    assert appends != SEES_FILE, "the fixture did not change"
    body = appends + "import time\ntime.sleep(30)\n"
    started = time.monotonic()
    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, body), target, log),
            "--timeout",
            "1",
        ],
        capsys,
    )
    elapsed = time.monotonic() - started
    assert code == 2, out
    assert out.startswith("timed out after 1s"), out
    assert "before the mutation was written" in out, out
    assert elapsed < 10, f"the baseline was not bounded: {elapsed:.1f}s"
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
    assert log.read_text(encoding="utf-8") == "VALUE = 1\n"
```
```
   It refuses an `<old>` that does not occur exactly once, runs the cases
   against the file as it is and stops with `no baseline` if they already
   fail, writes the break, removes the mutated file's cached bytecode for
   every interpreter tag, runs the cases again, each run under a bound (300 s
   unless `--timeout` says otherwise), puts the file back from the bytes it
   read first and compares the hash, and prints `red`, `SURVIVED`, or a run
   that measured nothing.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the work item's module, `-q -p no:xdist`, at the target | exit 0; 36 passed |
| `mutation-check` on a scratch target, `--tests "bin/test tests/test_arm_check.py -q -p no:xdist -k <a name no case has>"` | `no baseline`, exit 2, file unchanged |
| The same with a module path that does not exist | `no baseline`, exit 2, file unchanged |
| The same with a planted test file whose one case fails | `no baseline`, exit 2, file unchanged; the file was removed afterwards |
| Cases that make the target read-only once it holds the mutant | `not restored … PermissionError`, exit 2, no traceback; file `VALUE = 2` |
| A target read-only before the command starts, cases red only on the mutant | `not restored … PermissionError`, exit 2; file `VALUE = 1` (🟡 9) |
| A missing path, and a directory | `could not run: FileNotFoundError` / `IsADirectoryError`, exit 2, both |
| Cases that exit 1 on the mutant leaving a same-group child on the output, `--timeout 3` | `red`, exit 0, 0.2 s; child gone |
| The same with the child in a session of its own | `red`, exit 0, 0.4 s; child alive, ended by hand |
| Cases that sleep whatever the file holds, `--timeout 2` | `timed out after 2s … before the mutation was written`, exit 2, 2.2 s; file unchanged |
| In process: `restore` substituted by one that writes three bytes and raises `KeyboardInterrupt` | `not restored … KeyboardInterrupt`, exit 2; file `VAL` |
| In process: `KeyboardInterrupt` raised from the baseline's wait | `interrupted … was restored from the bytes read before the write`, exit 2; file unchanged; nothing had been written (⬜ 12) |
| `bin/mutation-check` on `mutation_check.py`, whole module `-x -p no:xdist`: M1 the baseline's `timeout=None` | SURVIVED (🟡 10) |
| The same: M2 the removal between the write and the mutated run | red: the baseline-cache case |
| The same: M3 the restore's `except BaseException` arm | red: the restore-raises case |
| The same: M4 `errors="strict"` on the sink | red: the non-UTF-8 case |
| The same: M5 no group kill after a normal exit | red: the child-on-the-output case |
| The same: M6 the baseline suffix dropped | red: the cannot-start case |
| The same: M7 the baseline's propagation of a non-verdict | red: the cannot-start case |
| The same: M8 `main`'s `except Exception` arm | red: the unreadable-path case |
| The same: M9 *Nothing was written* dropped from the `no baseline` detail | SURVIVED (⬜ 12) |
| The same: M10 the removal before the baseline | red: S1 |
| The same: M11 `NOT_RESTORED` renamed | red: the restore-did-not-land case |
| The same: M12 the elapsed time dropped from the verdict line | red: the red-and-exit-zero case |
| `git status --porcelain` in the clone after the mutations | empty |
| `mutation-check --timeout 8` over `bin/test` running two 40 s cases, `-n auto` and `-p no:xdist` | `timed out after 8s … before the mutation was written`, exit 2, 8–9 s; `pgrep` empty, both |
| Five `mutation-check` calls on L5's setup, `-p no:xdist`, after one warm-up, interleaved with one bare `bin/test` run each | all red; 0.96–1.07 s per call, mean 1.01 s; one run 0.41–0.47 s |
| The two proposed cases at the target | the bound case passed; the read-only case failed (`not restored`) |
| The bound case under M1 | red: suffix missing, 31.0 s |
| The module with 🟡 9's fix and both cases applied in the clone | exit 0; 38 passed; reverted afterwards |
| `bin/evidence-check .`, unscoped | exit 0; 3195 ok, 0 drifted, 0 broken; records 1 work item read, 0 drifted |
| `bin/survivor-check --range d6ce226a..2d47fbbd`, without and with `--exempt survivors.md`; and `d6ce226a..8b8149b3` with it | exit 1 on `plan.md:164` alone; exit 0; exit 0 |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: nobody has run it on this branch. It is the sealer's once the rounds settle, and it is not due while 🟡 9 and 🟡 10 stand |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/mutation_check.py:255` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:302-306` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:355-383` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:190-192` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:107` | round 1's 🟡 5 — fixed |
| round-1 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` | round 1's ⬜ 6 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:783-789` | round 1's ⬜ 7 — answered |
| round-1 | `skills/verify/SKILL.md` §*`mutation-check` asks condition 2 of one unit* | round 1's ⬜ 8 — fixed |
| round-1 | `agents/`, `skills/`, `docs/`, `templates/` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_arm_check.py:1066-1131` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.6.0.md`, `0.8.1.md`, `0.9.5.md`, `0.12.0.md`, `0.15.1.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L5 | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/mutation_check.py#run_cases` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/mutation_check.py:207-208`, `bin/mutation-check.cmd` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/verify/scripts/arm_check.py`'s `run_arms` reads any non-zero exit as killed with no baseline: round 1's finding 1 class, in a file C2 keeps unedited (already deferred in round 1) | a new issue, beside #313 | the orchestrator, who files it when the pull request is opened |
