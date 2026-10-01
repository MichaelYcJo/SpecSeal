# 1790815610 — review round 3 report (verifying, the run's last)

Target SHA `15aecc780c1b117ddd9e01150048689d3bce35a0`. Verified range: round 2's
fix range `5365948145b2e2e74171b1f013098d1f3d17f07f..dbd71bca45ccbeb969966a33aed1a6870f02e013`,
four commits. Worked in a `git clone --no-local` at
`<scratchpad>/1790815610/round-3/clone`. Round 2 used the one reopening, so this
round is capped: what it finds below is reported at the severity found, and
where it goes is the orchestrator's ladder.

## Summary

Five of round 2's six verdicts are closed with their class, and each new
parameter fails on the defect it pins. Two things stay open, both inside
round 2's note 12:

1. **The interrupt sentence is still false in one case.** It now says what the
   file holds. On the baseline path nothing checks that, so when the cases
   write the target themselves during the baseline, the line says the file
   holds its first bytes while it holds the cases' bytes (🟡 15).
2. **The baseline suffix's new sentence boundary is pinned by no case.** Put
   the round 2 clause form back and the module passes (⬜ 16).

Separately, there is one paperwork correction to L2's new note (⬜ 17).

## Round 2's verdicts, answered

**Finding 9: a read-only target.** Closed, class included. Run through the
wrapper, a target made `0o400` before the command starts gives
`could not run: PermissionError … No verdict.`, exit 2. Its bytes and its mode
are unchanged. The guard at `skills/verify/scripts/mutation_check.py:354-360`
restores only when the bytes differ. Every exit of the `try` passes through
it, so no other path tries a restore over bytes the break never reached.
Under mutation, the `[read-only]` parameter of
`test_a_path_that_cannot_be_read_measures_nothing_and_exits_two` goes red when
the guard is removed (M1). The `[removed]` parameter of
`test_the_file_is_restored_from_the_bytes_held_before_the_write` goes red when
an unreadable file counts as matching (M2). So both halves of the guard are held.

**Finding 10: the baseline's bound.** Closed. With `timeout=None` on the
baseline call alone (M3), the `[baseline]` parameter of
`test_a_run_past_the_bound_is_timed_out_and_leaves_nothing_it_started` goes
red, and the run takes 37.0 s. A direct baseline hang under `--timeout 1`
prints `timed out after 1s … This was the run against the file as it is,
before the mutation was written`, exit 2, and the file is unchanged.

**Note 11: the step list and the wrapper comment.** Closed. Read:
`agents/smith.md:272-278` and `bin/mutation-check:11-16` now name the
baseline, the `no baseline` stop and the bound per run, and both match
`mutation_run`.

**Note 12: the baseline's verdict lines.** Partly closed.

- `no baseline (exit N)` is true and held. Real pytest runs gave `(exit 5)`,
  `(exit 4)` and `(exit 1)` for a `-k` that selects nothing, a missing module
  and a failing case, and nothing was written. M4, which drops the exit, and
  M8, which fixes it at 1, each go red.
- *Nothing was written* is held. M5 goes red.
- The suffix is now a sentence of its own, but no case notices if it goes
  back. That is ⬜ 16.
- The interrupt sentence is true for a file the cases leave alone. Probe P4
  interrupted the baseline and the file was unchanged. It is false for a file
  the cases write. That is 🟡 15.

**Note 13: Q5's figures.** Answered as round 2 recorded. Read: Q5 now carries
a `Corrected 2026-10-01` note. It says a call runs the cases twice and gives
1.01 s per call against 0.43 s for one run.

**Note 14: the ledger header.** Closed. Read: the header names L7 and says
where it sits.

**L2's new re-read note.** True. `dbd71bca` touches the test module only
(three added lines, one assertion and its comment). It changes nothing in the
bound, the group kill or the restore order. The note's punctuation is ⬜ 17.

**`evidence-check .`, unscoped:** exit 0, with 3223 ok, 0 drifted and 0 broken.

## Findings from execution

### 🟡 15 — an interrupt in the baseline says the file holds its first bytes, and nothing made that true

`skills/verify/scripts/mutation_check.py:318-338` (the baseline, outside the
`try`) and `:443-449` (the sentence).

`d64a5184` changed the interrupt line from *was restored from the bytes read
before the write* to *holds the bytes it held before the command started*.
That is true on the mutated path, where the `finally` compares the hash and
restores. The baseline runs before the `try` opens, so an interrupt there
reaches `main` with nothing compared.

The cases can write the target themselves. The module's `REWRITES` fixture
exists because they can, and it rewrites the file on every run, the baseline
included. Probe P5 used cases that write `VALUE = 99` to the target, with the
Ctrl-C landing in the baseline. The line said the file *holds the bytes it
held before the command started*, but the file held `VALUE = 99`. The same
cases interrupted in the mutated run end with the file restored.

**Why it matters.** The line tells a person the file is as it was, so they
have no reason to look. The command was holding the original bytes and could
have put them back. This is round 2's note 12 class (the interrupt sentence
states something about the file that the baseline path never made true). The
fix moved it from a claim about a mechanism to a claim about the file's
content, which a person acts on directly.

**The fix is general rather than a special case.** Open the `try` before the
baseline. The guard added for finding 9 restores only bytes that differ, so a
baseline that leaves the file alone still writes nothing, and every exit of
the baseline (`no baseline`, a timed-out or unstartable baseline, an
interrupt) leaves the file as it was. Executed in the clone: the proposed case
is red at the target and green with the fix. With the fix, the module passed
40 cases, and the read-only, removed and restore cases were among them.

One thing changes with the fix. In a `no baseline` run whose cases rewrote
the file, the restore now puts the bytes back. *Nothing was written* then
stays true of the break but not of the restore. If that sentence should be
exact, *the break was never written* is the narrower wording. The SKILL's
`no baseline` parenthesis would follow it, along with the assertion in
`test_cases_that_fail_without_the_mutation_measure_nothing`.

### ⬜ 16 — the baseline suffix's sentence boundary is pinned by no case

`tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:804`
and `:1100`. Both assertions read `"before the mutation was written" in out`.
Round 2's clause form, `{detail}, before the mutation was written`, carries
that substring too. M6 put the clause form back, and the whole module passed
(SURVIVED). Contract §14 asks a changed line to be pinned, and this one is
not. The behaviour and the fact are both right, so this is ⬜. Executed in
the clone: with the assertions widened to include `. This was the run against
the file as it is`, M6 goes red in both cases.

### ⬜ 17 — correction: L2's orchestrator note is joined to the previous one with no full stop

`seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md`
L2, Notes cell. The text reads *… and the claim holds Re-read 2026-10-01 by
the orchestrator …*. The earlier notes in the cell end in a full stop and
open in bold. This one does neither. Paperwork, outside `Needs a fix`.

## Findings from reading

None beyond the answers above.

## Regression tests to plant

- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`,
  after the interrupt case: the baseline-interrupt case in the 🟡 15 fence.
  Seen red at the target and green with the fix.
- The same module, `:804` and `:1100`: the widened assertions in the ⬜ 16
  fence. Seen red under M6.

## Facts for the evidence ledger

- L3 or L7, once 🟡 15 is fixed: the restore's reach includes the baseline,
  so every exit of a call (an interrupt in the baseline included) leaves the
  target holding the bytes read first, or reads `not restored`.
- L7's note says *the baseline's suffix is now a sentence of its own (⬜ 12)*.
  That is true at the target, but until ⬜ 16 is planted no anchor holds it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 9 is closed — a target read-only before the command starts is `could not run`, exit 2, left unchanged, and the restore is tried only over bytes that differ | `skills/verify/scripts/mutation_check.py:347-370` | confirmed | Executed: P1 `could not run: PermissionError`, exit 2, bytes and mode `0o400` unchanged; M1 red on `[read-only]`, M2 red on `[removed]`; every exit of the `try` passes the guard |
| 🟢 | round 2's finding 10 is closed — the baseline's bound is held by a case | `skills/verify/scripts/mutation_check.py:319` | confirmed | Executed: M3 (`timeout=None` on the baseline) red on the bound case's `[baseline]` parameter, 37.0 s; P3 `timed out after 1s`, exit 2, file unchanged |
| 🟢 | round 2's note 11 is closed — the step list and the wrapper comment name the baseline and the bound per run | `agents/smith.md:272-278`, `bin/mutation-check:11-16` | confirmed | Read: both match `mutation_run` at the target |
| 🟢 | round 2's note 12 is closed in two of its clauses — `no baseline` carries the baseline's exit and *Nothing was written*, both held | `skills/verify/scripts/mutation_check.py:320-329` | confirmed | Executed: P2 printed `(exit 5)`, `(exit 4)`, `(exit 1)`, nothing written; M4, M5 and M8 each red. The other two clauses are 15 and 16 below |
| 🟡 15 | An interrupt in the baseline prints that the file holds the bytes it held before the command started, and nothing compared them: cases that wrote the target leave it changed under that line | `skills/verify/scripts/mutation_check.py:318-338`, `:443-449` | open | Executed: P5, cases writing `VALUE = 99` with the Ctrl-C in the baseline, printed *holds the bytes it held*, file `VALUE = 99`; the proposed case red at the target, green with the fix; module 40 passed with it. Round 2's note 12 class, not closed |
| ⬜ 16 | The baseline suffix's sentence boundary is pinned by no case: both assertions read a substring round 2's clause form also carries | `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:804`, `:1100` | open | Executed: M6 (the clause form put back) SURVIVED the whole module; red in both cases with the widened assertions. Behaviour and fact stay right |
| 🟢 | round 2's note 13 is answered — Q5 says a call runs the cases twice, with the measured figures | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` Q5 | confirmed | Read: the `Corrected 2026-10-01` note in the Q5 cell |
| 🟢 | round 2's note 14 is closed — the fragment's header names L7 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-9` | confirmed | Read |
| 🟢 | L2's re-read note after `dbd71bca` is true | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | confirmed | Read: `dbd71bca` adds one assertion and its comment to the interrupt case and touches no code; the bound, the group kill and the restore order are as L2 states |
| ⬜ 17 | correction: L2's orchestrator note is joined to the note before it with no full stop and no bold opening | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | open | Read. Paperwork, outside `Needs a fix` |
| 🟢 | The ledger holds unscoped | the whole tree | confirmed | Executed: `bin/evidence-check .` exit 0, 3223 ok, 0 drifted, 0 broken |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/verify/scripts/arm_check.py`'s `run_arms` reads any non-zero exit as killed with no baseline: round 1's finding 1 class, in a file C2 keeps unedited (already deferred in round 1, carried in round 2) | a new issue, beside #313 | the orchestrator, who files it when the pull request is opened |

## Paste-ready fixes

### 🟡 15

`skills/verify/scripts/mutation_check.py`, in `mutation_run`: open the `try` before the baseline, so the `finally` (restore only over bytes that differ) covers every exit.

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

`tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`, after the interrupt case:

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

### ⬜ 16

The same module, `:804` (the cannot-start case) and `:1100` (the bound case's `[baseline]` branch), each:

```python
    assert (
        ". This was the run against the file as it is, before the mutation was written"
        in out
    ), out
```

Needs a fix: yes — 🟡 15 (an interrupt in the baseline says the file holds its first bytes over a file the cases changed)
Loses a record or crashes: no

## Proof block

Files opened this round (at the target, in the clone):

- `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/rounds/round-2.md`
- `skills/verify/scripts/mutation_check.py` (lines 90-470)
- `skills/verify/scripts/arm_check.py` (`restore`)
- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` (the cases the fix range touched, the fixtures they use, and the interrupt case)
- `skills/verify/SKILL.md` (lines 140-175)
- `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` (header, L2, L3, L7)
- `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` (Q5)
- the fix range's diff for `agents/smith.md`, `bin/mutation-check`, `seal/`, and `15aecc78`'s diff

The suite is `unverified`: the broad gate has not run, and it belongs to the sealer.
