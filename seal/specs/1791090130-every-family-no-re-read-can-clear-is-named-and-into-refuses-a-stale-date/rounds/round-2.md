# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — review round 2

| Field | Value |
|---|---|
| Target SHA | bfa78c8522a1cda016c0235b6bfc5a10ef79b42c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #771 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `538f7e6ef37ec888f45f6195f0c5bbf1dcd8f696..080a03a33a64892ab7242ccae0a1d840b9707ca2`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 5, docs/the-pact.md names a moved hash or a BROKEN coordinate as the whole trigger for a pact change, and a row --into refuses for a stale date is now recorded with neither |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item `1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date` (#746, PR #771). It is the verifying round for round 1's fixes, `1640bf9a..2df48401`.

For each round-1 verdict, open the fix and judge whether it is closed:
- 🟡 2: the refusal branch now puts each moved coordinate of a refused row into `moves`, so its pact change is recorded. The row still gets no `Re-read ·` row and no ledger write, is named on its `LEFT` line, and makes the run exit 1. This reverses the frame's S1 and S6 and #756's W9 "records nothing", by the orchestrator's decision that a pact change is never lost.
- 🟡 1: the `LEFT` line and its five copies now say what is true.
- ⬜ 3 and ⬜ 4.

Check that #756's record-first order (W1) and its single-record property (W4) hold for a refused row's moves under a killed run. Then check that the new usage wording does not collide with #756's "left whole" meaning.

The new units the fixes created are a finding surface: `_frozen_released_o1` and the renamed A5.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 5 | `docs/the-pact.md` names a moved hash or a BROKEN coordinate as *the whole trigger* for a pact change, while a row `--into` refuses for a stale `--checked` is now recorded with its hash unmoved and no `Re-read ·` row | `docs/the-pact.md:115` | **fixed** `080a03a3` | fixed at 080a03a3; read against `evidence_check.py:3602-3612`; executed, P4: the refused row's move is recorded and its ledger is not written; `skills/evidence-check/SKILL.md:324-329` and the usage are true but incomplete, same class |
| ⬜ 6 | A coordinate that is OK but outranked by a newer reading holding other content is recorded as a move from its hash to the same hash, in the refusal arm the fix added as in the written arm | `skills/evidence-check/scripts/evidence_check.py:3602` | deferred to a new issue against #756's record writer | executed, P3: both arms record `57f678c6` → `@57f678c6` where the move was `7069baf7` → `57f678c6`; the written arm does the same at `edee5ca2`; W4 calls over-recording the safe direction |
| ⬜ 7 | The pact module's section comment for the refused-row cases still says the row records nothing | `tests/test_a_signatory_records_a_pact_change.py:1585` | **fixed** `080a03a3` | fixed at 080a03a3; read; a sixth copy of round 1's yellow 1 class, in a comment only |
| 🟢 | round 1's yellow finding 2 is closed — a refused row's moves reach the record, including the after-today arm whose repair no later re-read reaches | `skills/evidence-check/scripts/evidence_check.py:3602` | confirmed | executed: the two modules pass at the target (439); the three new pact cases fail with `1640bf9a`'s checker; read: the row stays out of `rows` and the plan |
| 🟢 | round 1's yellow finding 1 is closed — the `LEFT` line and its five copies say no `Re-read ·` row was written and the moves are recorded | `skills/evidence-check/scripts/evidence_check.py:3496` | confirmed | executed: the eight refusal cells, the after-today case and the usage pin fail with `1640bf9a`'s checker; read: the ledger home, `changelog.md:8`, F1 and the L4 correction |
| 🟢 | round 1's ⬜ 3 and ⬜ 4 are closed — the changelog names the fifth family's modes and the overview lists the sibling cases | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/changelog.md:21` | confirmed | read at `d481638f`, against the two cases round 1 named |
| 🟢 | #756's W1 and W4 hold for a refused row's moves under a killed run | `skills/evidence-check/scripts/evidence_check.py:5108` | confirmed | executed, P4: killed after the record, the next run leaves the record byte for byte and re-stamps; P5: killed before, nothing written, then one record and none twice |
| 🟢 | The usage's new wording does not call the refused row *left whole*, so it does not collide with #756 C1's *a row left whole … records nothing* | `skills/evidence-check/scripts/evidence_check.py:67` | confirmed | read: `git grep` finds *left whole* only for #387's row with no date cell and in C1; C1's hash-only re-stamp still holds |
| 🟢 | The new units `_frozen_released_o1` and the renamed A5 do what their docstrings say | `tests/test_a_signatory_records_a_pact_change.py:1588` | confirmed | read; executed: both pass at the target, and A5 fails with `1640bf9a`'s checker |

## Paste-ready fixes

```text
docs/the-pact.md, §A signatory records a pact change, replace the paragraph's
opening, from "**When a signatory's" through "one row per ledger row. `Pact",
with:

**When a signatory's `evidence-check --reverify` moves the hash of a ledger
row that cites a clause of a pact its `Pact` row declares, finds the code
under such a row moved where `--into` refuses it a `Re-read ·` row for a
stale `--checked`, or leaves a coordinate of one BROKEN, the same command
records a pact change, and that test is the whole trigger.** It needs no
judgment: a row carrying a pact anchor and a local coordinate is the link,
and a re-read is the one act at which a session says code under a row
moved. The record is written in both of the re-read's forms, a re-stamp in
place and a `Re-read ·` row under `--into`, before the hash it read is gone,
one row per ledger row. A row `--into` refuses is recorded by the run that
refuses it, because its repair may be a `Corrected ·` row that no later
re-read reaches (#746). `Pact
```
```text
skills/evidence-check/SKILL.md, the "In a signatory" paragraph, replace

`--into` — cites one of its clauses as a pact anchor, or a coordinate of such
a row is BROKEN, one row per ledger row is appended to

with

`--into` — cites one of its clauses as a pact anchor, or a coordinate of such
a row is BROKEN, or `--into` refuses such a row a `Re-read ·` row for a stale
`--checked` while the code under it moved, one row per ledger row is
appended to
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py,
# test_the_home_and_the_usage_say_a_stale_row_is_left: append to the list
        (
            "docs/the-pact.md",
            "finds the code under such a row moved where `--into` refuses it a "
            "`Re-read ·` row for a stale `--checked`, or leaves a coordinate of "
            "one BROKEN, the same command records a pact change, and that test "
            "is the whole trigger.",
        ),
# and to ids:
    ids=["the home: the refusal", "the home: after today", "the usage", "the pact's trigger"],
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_a_signatory_records_a_pact_change.py -q` in the round's clone at `bfa78c85` | exit 0, 439 passed |
| The same two modules, `-k` on the refusal, after-today, usage-pin and three new pact cases, with `1640bf9a`'s `evidence_check.py` checked out in the clone, then restored | exit 1, 13 failed and 2 passed; the two that passed are the docs-file pins, whose files were not swapped |
| `bin/evidence-check --strict --ledger` this item's fragment, then #756's fragment | this item's: exit 0, 76 ok; #756's: exit 2, 3 DRIFTED, the chore's units as in round 1 |
| P3, a probe case: an outranked-OK coordinate, narrowed, stale and written arms | stale: exit 1, record row `@57f678c6` → `@57f678c6`; written: exit 0, the same row; written arm with `edee5ca2`'s checker: the same row |
| P4, a probe case: a refused row plus a re-stamped row, killed after the record | exit 137, two record rows, fragment untouched; next run exit 1, record byte for byte, fragment re-stamped |
| P5, a probe case: the same tree, killed before the record | exit 137, no record, fragment untouched; next run records two rows; third run, still two |
| The broad gate (full suite, repository lint, typecheck) | not yet; the sealer's, after the rounds settle |

```python
# tests/test_tmp_746_r2_probe.py in the round's clone, run once, deleted.
# Helpers imported from tests/test_a_signatory_records_a_pact_change.py.
# P3: freeze; released O1 dated 2026-09-01 at serialize@h1; another item's
#     fragment seal/ledger/3000000003-the-newer-re-read.md holds
#     | Re-read · O1 ... | `<citation_for O1>`, `src/orders.py#serialize@h2` | read | 2026-09-10 | ... |
#     code reverted to h1; run --ledger seal/releases/0.1.0.md --into FRAGMENT
#     with --checked 2026-09-04 (stale) and 2026-09-12 (written); print record_rows.
# P4: freeze; released O1 dated 2026-09-10 at serialize@h1, and FRAGMENT row
#     F1 dated 2026-09-01 at serialize@h1, both citing CLAUSE; serialize moved;
#     a wrapper runs main() with record_pact_changes replaced by
#     real(*a); os._exit(137); then the plain run again; compare record bytes.
# P5: the same tree; the wrapper's replacement calls os._exit(137) before the
#     real call; then the plain run twice; count record rows.
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3645` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3591` | round 1's 🟡 2 — fixed |
| round-1 | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/changelog.md:21` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/overview.md:18` | round 1's ⬜ 4 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3506` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2924` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-evidence-ledger.md:178` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:4` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_signatory_records_a_pact_change.py:74` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 6: the record's old hash is the released member's, so an outranked-OK coordinate is recorded as a move to its own hash, in both of `reverify_into`'s arms and at the base | proposed: a new issue against #756's record writer; the fix is to take the old hash from the newest reading and skip a move whose two hashes agree | the orchestrator, who decides whether to file it |
| Without the freeze, one `--reverify` over every ledger moves the line a fragment's citing rows cite (round 1's deferral) | `overview.md` §*Not done*; already deferred in round 1 | the orchestrator, who decides whether to file it |
