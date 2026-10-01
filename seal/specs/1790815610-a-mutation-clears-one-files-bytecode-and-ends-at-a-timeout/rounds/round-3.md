# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — review round 3

| Field | Value |
|---|---|
| Target SHA | 15aecc780c1b117ddd9e01150048689d3bce35a0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 698 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `db15439f629ba387423900385cad04b6f6247af2..37b3646f8b7f9a69d516adfac3b36791560937bb`, 2 commits |
| Contract changes | test_an_interrupt_ends_the_run_it_started_and_restores_the_file → pytest only |
| New units | none |
| Needs a fix | yes — 🟡 15 (an interrupt in the baseline says the file holds its first bytes over a file the cases changed) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is the verifying round after the run's one reopening, so it is the run's last. It targets `15aecc78` and verifies round 2's fix range `53659481..dbd71bca`, four commits. It was asked whether round 2's six verdicts are closed with their class: the read-only target, the baseline's bound held by a case, and the baseline's verdict lines. It was also asked whether each extended case fails on the defect it pins, and whether L2's new re-read note is true.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 9 is closed — a target read-only before the command starts is `could not run`, exit 2, left unchanged, and the restore is tried only over bytes that differ | `skills/verify/scripts/mutation_check.py:347-370` | confirmed | Executed: P1 `could not run: PermissionError`, exit 2, bytes and mode `0o400` unchanged; M1 red on `[read-only]`, M2 red on `[removed]`; every exit of the `try` passes the guard |
| 🟢 | round 2's finding 10 is closed — the baseline's bound is held by a case | `skills/verify/scripts/mutation_check.py:319` | confirmed | Executed: M3 (`timeout=None` on the baseline) red on the bound case's `[baseline]` parameter, 37.0 s; P3 `timed out after 1s`, exit 2, file unchanged |
| 🟢 | round 2's note 11 is closed — the step list and the wrapper comment name the baseline and the bound per run | `agents/smith.md:272-278`, `bin/mutation-check:11-16` | confirmed | Read: both match `mutation_run` at the target |
| 🟢 | round 2's note 12 is closed in two of its clauses — `no baseline` carries the baseline's exit and *Nothing was written*, both held | `skills/verify/scripts/mutation_check.py:320-329` | confirmed | Executed: P2 printed `(exit 5)`, `(exit 4)`, `(exit 1)`, nothing written; M4, M5 and M8 each red. The other two clauses are 15 and 16 below |
| 🟡 15 | An interrupt in the baseline prints that the file holds the bytes it held before the command started, and nothing compared them: cases that wrote the target leave it changed under that line | `skills/verify/scripts/mutation_check.py:318-338`, `:443-449` | **fixed** `647c3395` | fixed at 647c3395; Executed: P5, cases writing `VALUE = 99` with the Ctrl-C in the baseline, printed *holds the bytes it held*, file `VALUE = 99`; the proposed case red at the target, green with the fix; module 40 passed with it. Round 2's note 12 class, not closed |
| ⬜ 16 | The baseline suffix's sentence boundary is pinned by no case: both assertions read a substring round 2's clause form also carries | `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:804`, `:1100` | **fixed** `647c3395` | fixed at 647c3395; Executed: M6 (the clause form put back) SURVIVED the whole module; red in both cases with the widened assertions. Behaviour and fact stay right |
| 🟢 | round 2's note 13 is answered — Q5 says a call runs the cases twice, with the measured figures | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` Q5 | confirmed | Read: the `Corrected 2026-10-01` note in the Q5 cell |
| 🟢 | round 2's note 14 is closed — the fragment's header names L7 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-9` | confirmed | Read |
| 🟢 | L2's re-read note after `dbd71bca` is true | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | confirmed | Read: `dbd71bca` adds one assertion and its comment to the interrupt case and touches no code; the bound, the group kill and the restore order are as L2 states |
| ⬜ 17 | correction: L2's orchestrator note is joined to the note before it with no full stop and no bold opening | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | answered | corrected at 37b3646f; L2's note has its full stop back, with a round 3 re-read note; Read. Paperwork, outside `Needs a fix` |
| 🟢 | The ledger holds unscoped | the whole tree | confirmed | Executed: `bin/evidence-check .` exit 0, 3223 ok, 0 drifted, 0 broken |

## Paste-ready fixes

```python
    clear_bytecode_cache(path)
    # The restore's reach starts here, not at the write: the cases may write
    # the file themselves, and an interrupt in the baseline is reported as
    # the file holding its first bytes (round 3).
    try:
        before, detail, output = run_cases(command, cwd=cwd, env=env, timeout=timeout)
        if before == RED:
            # The baseline's own exit, `(exit N)` from `run_cases`' red detail:
            # pytest's 5 and 4 are what tell a mistyped `-k` from a failing case.
            exited = detail[detail.rfind("(exit ") :]
            return (
                NO_BASELINE,
                f"the cases fail against the file as it is {exited}, so a failure "
                f"under the mutation would say nothing about it. Nothing was written",
                output,
            )
        if before != SURVIVED:
            # A sentence of its own, so it reads as the verdict's and not as the
            # last clause of the detail's (round 2, ⬜ 12).
            return (
                before,
                f"{detail}. This was the run against the file as it is, before "
                f"the mutation was written",
                output,
            )
        with open(path, "wb") as f:
            f.write(after.encode("utf-8"))
        # Again after the write: the baseline's cases may have written the
        # original's `.pyc`, which a same-length break matches.
        clear_bytecode_cache(path)
        return run_cases(command, cwd=cwd, env=env, timeout=timeout)
    finally:
        # unchanged
```
```python
def test_an_interrupt_in_the_baseline_leaves_the_file_as_the_line_says(
    tmp_path, capsys, monkeypatch
):
    """Round 3: the interrupt line says the file holds the bytes it held
    before the command started. The cases can write the file during the
    baseline, before any break exists, and the line has to be true then too."""
    target = tmp_path / "under_test.py"
    original = b"VALUE = 1\n"
    target.write_bytes(original)
    rewrites = probe(
        tmp_path,
        "import sys\nopen(sys.argv[1], 'w').write('VALUE = 99\\n')\n",
    )
    mc = module()

    def interrupted(proc, timeout):
        # The cases finish what they write, then the Ctrl-C lands: the first
        # wait is the baseline's.
        proc.wait()
        raise KeyboardInterrupt

    monkeypatch.setattr(mc, "_wait", interrupted)
    code = mc.main(
        [
            str(target),
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(rewrites, target),
        ]
    )
    out = capsys.readouterr().out
    assert code == 2, out
    assert "holds the bytes it held before the command started" in out, out
    assert target.read_bytes() == original
```
```python
    assert (
        ". This was the run against the file as it is, before the mutation was written"
        in out
    ), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the module, `-q -p no:xdist`, at the target | exit 0; 39 passed |
| `bin/test tests/test_a_rider_reaches_its_file.py -q -p no:xdist` (the rider stamp `3f8e021e` moved) | exit 0; 49 passed |
| P1: the wrapper on a target made `0o400` before the command starts, cases that pass | `could not run: PermissionError … No verdict.`, exit 2; bytes `VALUE = 1`, mode `0o400` |
| P2: the wrapper with real pytest cases: a `-k` selecting nothing, a missing module, a failing case | `no baseline: … (exit 5)` / `(exit 4)` / `(exit 1)`, each `Nothing was written`, exit 2; file unchanged |
| P3: the wrapper, cases that sleep 30 s, `--timeout 1` | `timed out after 1s … This was the run against the file as it is, before the mutation was written`, exit 2, 1.0 s; file unchanged |
| P4: in process, the first `_wait` interrupted, cases that touch nothing | `interrupted … holds the bytes it held before the command started.`, exit 2; file unchanged |
| P5: in process, the first `_wait` interrupted after cases that write `VALUE = 99` to the target | the same line, exit 2; file `VALUE = 99` (🟡 15) |
| `bin/mutation-check` on `mutation_check.py`, whole module `-q -x -p no:xdist`: M1 the restore tried whatever the bytes | red: `[read-only]` |
| The same: M2 an unreadable file counted as matching | red: `[removed]` |
| The same: M3 `timeout=None` on the baseline call | red: the bound case `[baseline]`, 37.0 s |
| The same: M4 the baseline's exit dropped from `no baseline` | red: the no-baseline case `[failing]` |
| The same: M5 *Nothing was written* dropped | red: the no-baseline case `[failing]` |
| The same: M6 the suffix back to round 2's clause form | SURVIVED (⬜ 16) |
| The same: M7 the interrupt sentence back to round 2's | red: the interrupt case |
| The same: M8 the baseline's exit fixed at `(exit 1)` | red: the no-baseline case `[nothing-selected]` |
| `git status --porcelain` in the clone after the mutations | empty |
| The 🟡 15 fix and the three test changes applied in the clone | exit 0; 40 passed |
| The test changes at the target's source | exit 1; the proposed baseline-interrupt case alone failed |
| M6 under the widened assertions, `-k 'past_the_bound or cannot_start'` | red: the cannot-start case and the bound case `[baseline]` |
| The clone after the scratch patches | reverted; `git status --porcelain` empty |
| `bin/evidence-check .`, unscoped | exit 0; 3223 ok, 0 drifted, 0 broken; records 2 work items read, 0 drifted |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: nobody has run it on this branch. It is the sealer's once the rounds settle, and it is not due while 🟡 15 stands open or until the orchestrator rules on it |

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
| round-2 | `skills/verify/scripts/mutation_check.py:313-328` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:337-350` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:428-438` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:196-267` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:116`, `:244` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/plan.md:164` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:319` | round 2's 🟡 10 — fixed |
| round-2 | `agents/smith.md:271-276`, `bin/mutation-check:11-15` | round 2's ⬜ 11 — fixed |
| round-2 | `skills/verify/scripts/mutation_check.py:320-328`, `:418-427` | round 2's ⬜ 12 — fixed |
| round-2 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md:42` | round 2's ⬜ 13 — answered |
| round-2 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-8` | round 2's ⬜ 14 — fixed |
| round-2 | `skills/verify/scripts/mutation_check.py:218-221`, `bin/mutation-check.cmd` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/verify/scripts/arm_check.py`'s `run_arms` reads any non-zero exit as killed with no baseline: round 1's finding 1 class, in a file C2 keeps unedited (already deferred in round 1, carried in round 2) | a new issue, beside #313 | the orchestrator, who files it when the pull request is opened |
