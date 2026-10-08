# 1791384154-a-records-finding-closes-once-at-the-runs-end — review round 1

| Field | Value |
|---|---|
| Target SHA | 7795f390014750b1a9917aa9d0e5dd0ff9ad0270 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 879 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `e10a7c3581fa657f42ea0802b158748b7549b046..38696bb019234f50bf1a011bcd23c1478f25e385`, 4 commits |
| Contract changes | none |
| New units | a_run_stopped_with_a_note (depth 1); test_the_redesign_waits_for_the_stopped_runs_notes (depth 1); test_notes_names_each_row_it_cannot_apply_and_writes_nothing (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (the rider re-stamp), 🟡 2 (the cutoff), 🟡 3 (a stopped run's notes become unclosable), 🟡 4 (the policy sentence), 🟡 5 (the unpinned refusals) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the build at 7795f390, against origin/release/v0.21.0, governed by the installed 0.20.0 rules. The spawn named six things to attack. First, the two divergences: the notes table keyed by round and id, and open notes left out of the landing computation. Second, notes' run's-end test shared with seal over capped, reframed, empty and superseded runs. Third, close refusing a ⬜ row, the deferred path, and records written before NOTES_FROM. Fourth, a sample of the 73 Re-read rows. Fifth, whether the carriers say one rule and pin it. Sixth, the round's own axes. Facts arrived labelled. Executed by the orchestrator: the fragment rename to the full work-item name at 7795f390, evidence-check --strict at exit 0, bin/test over five modules (326 passed) and ruff. Read from the smith: 30 mutations, the carried_notes sweep, the Q2 count and the re-read rows. The reviewer's session hit the account's usage limit after it had written the report in full. The orchestrator confirmed 🔴 1 independently from the PR's ubuntu log, where the rider module's two cases fail on agents/smith.md:87.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The ⬜ paragraph inserted into §*Phases* drifted the rider stamped on that section; two cases of the rider module fail and the PR's test legs are red | `agents/smith.md:87` | **fixed** `7706e367` | fixed at 7706e367 — the rider's three measurements re-run at the base and at the fix (one invocation alone, one with everything above, `_hides_a_commit` True: unchanged by the note paragraph), recorded in the rider, and the stamp re-taken with `rider_check.py --reverify --only agents/smith.md`; `rider_check.py` exit 0 and `tests/test_a_rider_reaches_its_file.py` 49 passed; executed: rider module 2 failed, 47 passed; `rider_check.py` exit 1, 1 drifted. Read: CI ubuntu and Windows group 1 fail on the same two cases |
| 🟡 2 | `NOTES_FROM` is this item's id, but the batch's siblings (1791384155 to 1791384162) run under 0.20.0's `close`, which demands and admits ⬜ `fixed`; #858's records already fail arm A three times | `skills/code-review/scripts/chain_check.py:856` | **fixed** `9a37a02d` | fixed at 9a37a02d — `NOTES_FROM = 1791384163`, one past the batch 1791384152–1791384162 whose rounds run under 0.20.0's `close`; the cutoff case moved with it and is red at the old value; the grounds' wording made version-free in `38696bb0` for `tests/test_release_hygiene.py`; executed: `carried_notes` over #858's branch at `4e4eeff` returns 3 errors at round-1.md:33-35. Read: CI checks the merge ref, and the release PR touches every sibling |
| 🟡 3 | A stopped run whose notes were not closed at the `second` leaves them open for good: `seal`, `carried_notes` and `carried_line` stop reading them, and `notes` refuses them as outside the run | `skills/code-review/scripts/round_record.py:4855` | **fixed** `9a37a02d` | fixed at 9a37a02d — `new` refuses the redesign's first record while the stopped run carries an open ⬜, naming it and `notes`; `test_the_redesign_waits_for_the_stopped_runs_notes`, red with the refusal removed; executed: `run_of_last` gives `[4]`, `open_notes` gives `[]`, `carried_notes` gives `([], [])`, `notes` exits 2 *outside the run*; round-1's ⬜ 1 still reads `open` |
| 🟡 4 | The policy document says a record-located finding closes in the fix table, which `close` now refuses; the overview says the document does not contradict the rule | `docs/review-chain-spec.md:246` | **fixed** `9a37a02d` | fixed at 9a37a02d — `docs/review-chain-spec.md` now says a ⬜ closes at the run's end through `notes` and a 🟡 in its fix table, in place, the document still at 999 lines; the overview's claim that it did not contradict is replaced; read: the sentence against `close`'s ⬜ refusal and `agents/warden.md`'s instruction to grade such a finding ⬜ |
| 🟡 5 | Five of `notes`' refusal sentences are unpinned, and a case's docstring claims the already-closed refusal it never asserts | `tests/test_a_note_closes_once_at_the_runs_end.py:450` | **fixed** `9a37a02d` | fixed at 9a37a02d — `test_notes_names_each_row_it_cannot_apply_and_writes_nothing` pins the five sentences, each red when changed; the docstring now names the case that asserts the already-closed refusal; executed: the five strings match `notes`' output, exit 2, records unchanged; read: no case asserts them |
| ⬜ 6 | `Re-read · S13` and `Re-read · S10` say the claim holds where `close` no longer ticks `Pass` over a carried note and a capped run with an open note no longer seals; `Corrected ·` rows were owed | `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:17` | answered | corrected at `0966de0e` — the two `Re-read ·` rows are replaced by `Corrected · S10` and `Corrected · S13` in this item's fragment; read: 0.10.0 S10 and S13 against `close` and `seal` at the target |
| ⬜ 7 | `agents/warden.md` asks for an answer to every earlier finding and also says a carried ⬜ is not re-reported | `agents/warden.md:348` | answered | corrected at `9a37a02d` — `agents/warden.md` excepts a ⬜ the run still carries from the answer every earlier finding needs; read: lines 161 and 348 |
| ⬜ 8 | The owner file keeps *corrected in passing or not at all* one sentence before the rule that a ⬜ closes once at the run's end | `skills/code-review/orchestration.md:196` | answered | corrected at `9a37a02d` — the owner file's rule-1 paragraph and the policy's both read *a ⬜ like any other* where they said *corrected in passing or not at all*; read |
| 🟢 | The landing leaves only open notes out: an open 🔴 or 🟡 still holds `nobody`, and `Pass` is derived from every word | `skills/code-review/scripts/round_record.py:2595` | confirmed | read: `build` and `close` filter by `carried_ids`, which takes only `note_rows`' open notes |
| 🟢 | No shipped run turns red under the two arms | `skills/code-review/scripts/chain_check.py:4610` | confirmed | executed: 7 items, 0 errors, 24 notices |
| 🟢 | `runs_of` and `run_of_last` cut the run alike, and every reader of a note goes through `note_rows` | `skills/code-review/scripts/chain_check.py:3867` | confirmed | read |
| ❓ | The merge with #860 and #866, which edit `close` and `chain_check.py` beside these lines | `skills/code-review/scripts/round_record.py:4401` | ❓ out of verified scope | neither sibling's diff was reviewed here; the orchestrator answers it when it integrates them |

## Paste-ready fixes

```
python3 .github/scripts/rider_check.py --reverify --only agents/smith.md
bin/test tests/test_a_rider_reaches_its_file.py
```
```python
# Where a note closed on a fix word becomes an error, as the unix second in a
# work item's directory name. NOT this item's own id, which is what the other
# cutoffs use: 0.21.0's items were framed in one sitting, 1791384154 through
# 1791384162, and every one after this one runs its rounds under the installed
# 0.20.0 `close`, which demands a fix-table row for a ⬜ and admits `fixed` --
# #858's round 1 closed three that way before this rule landed. One past the
# batch, so the first records held to it are written under it.
# Measured 2026-10-07: 35 ⬜ rows of 14 committed records closed `fixed`
# before it, and they print.
NOTES_FROM = 1791384163
```
```python
AT_THE_CUTOFF = "seal/specs/1791384163-an-item-under-the-rule"
BEFORE_THE_CUTOFF = "seal/specs/1791384162-an-item-before-the-rule"
```
```python
    # #837. The redesign's first record is where the stopped run's notes stop
    # being read: `seal`, `notes` and `chain_check.carried_notes` read the run
    # the LAST record belongs to. Refused here, while `notes` can still close
    # them, rather than left open on a run nothing reads again.
    if stopped is not None and previous_pair == stopped:
        left = open_notes(reader, run_of_last(reader, earlier))
        if left:
            raise Refused(
                f"round-{stopped[0]}.md ended its run at a "
                f"`{chain.FOF_SECOND}` with {named_notes(left)} still open. A "
                "note closes once, at the run's end, and the "
                f"`{chain.FOF_SECOND}` is that end: run `{NOTES_COMMAND}` "
                "before the redesign's first record, which would leave them on "
                "a run nothing reads again. "
                f"{chain.NOTES_OWNER}; nothing was written"
            )
```
```
At the run's end, in the notes table, such a row closes `answered` with
`corrected at <sha>` as its grounds, never `fixed`: `fixed` is a fix word, and
a fix word commissions the reader a correction does not owe.
```
```python
def test_notes_names_each_row_it_cannot_apply_and_writes_nothing(repo):
    """The refusals `notes` raises before the write, each pinned (§14): a
    round outside the run, an id no record holds, a `Round` cell that names
    no round, an `--at` that does not resolve, and a row for a note the
    record already closed. Seen red by deleting each sentence in turn."""
    at = two_rounds_with_a_note_each(repo)
    before = record(repo, 1), record(repo, 2)
    for row, said in (
        (
            "| round-3 | 1 | answered | it stands |\n",
            "names round 3, outside the run that ends at round-2.md",
        ),
        (
            "| round-1 | 9 | answered | it stands |\n",
            "names round-1's 9, which no verdict table of the run holds",
        ),
        (
            "| round-x | 1 | answered | it stands |\n",
            "Write `round-K`, the record the note stands in",
        ),
    ):
        code, out = run_notes(repo, notes_table(*BOTH_ROWS, row), at=at)
        assert code == 2 and said in out, out
        assert (record(repo, 1), record(repo, 2)) == before
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at="deadbeefdeadbeef")
    assert code == 2 and "--at deadbeefdeadbeef does not resolve" in out, out
    assert (record(repo, 1), record(repo, 2)) == before
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at=at)
    assert code == 0, out
    commit(repo, "the notes closed")
    closed = record(repo, 1)
    code, out = run_notes(
        repo, notes_table("| round-1 | 1 | answered | again |\n"), at=at
    )
    assert code == 2, out
    assert f"round-1's {NOTE} 1, already closed in its verdict table" in out, out
    assert record(repo, 1) == closed
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_rider_reaches_its_file.py -n 0` in the clone at `7795f390` | 2 failed (`test_every_rider_stamp_resolves_and_reproduces_its_hash`, `test_the_check_asks_git_for_nothing`), 47 passed |
| `python3 .github/scripts/rider_check.py` in the clone | exit 1; `DRIFTED agents/smith.md:87`; 19 ok, 1 drifted, 0 broken |
| probe P1: `carried_notes(strict=True)` over every work item with records in the clone | 7 items, 0 errors, 24 notices |
| probe P2: `carried_notes(strict=True)` over #858's branch at `4e4eeff`, cloned `--no-local` | 3 errors: ⬜ 6, ⬜ 7 and ⬜ 8 at round-1.md:33-35 *closes on `fixed`* |
| probe P3: a run stopped at round 3 with round 1's ⬜ 1 open, `notes` skipped, round 4 written by hand | `run_of_last` gives `[4]`; `open_notes` gives `[]`; `carried_notes` gives `([], [])`; `notes` exits 2 *outside the run that ends at round-4.md* |
| probe P4: `notes` given a round outside the run, an unknown id, a bad `Round` cell, an unresolvable `--at`, and a closed note | each exits 2 with the sentence the paste-ready case pins; records unchanged |
| `gh pr checks 879`, read and not run by this round | ubuntu: fail (2 rider cases, 12766 passed). Windows group 1: fail (same 2). Windows groups 2-4, lint, ledger, release, arm-check-grammar: pass. macOS: pending |
| the full suite, repository-wide lint and typecheck (the sealer's broad gate) | not yet — no run has happened at any SHA of this branch; the sealer answers it after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
