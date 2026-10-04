# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — review round 2 report

| Field | Value |
|---|---|
| Round | 2 |
| Target SHA | `bfa78c85` |
| Base | `release/v0.18.1` at `edee5ca2` |
| Fix range verified | `1640bf9a..2df48401`, and the closing commit `bfa78c85` |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at the target, under the session's scratchpad; nothing was written in the worktree but this file |

## What this round was asked

Round 2 of work item `1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date` (#746, PR #771). It is the verifying round for round 1's fixes, `1640bf9a..2df48401`.

For each round-1 verdict, open the fix and judge whether it is closed:
- yellow 2: the refusal branch now puts each moved coordinate of a refused row into `moves`, so its pact change is recorded. The row still gets no `Re-read ·` row and no ledger write, is named on its `LEFT` line, and makes the run exit 1. This reverses the frame's S1 and S6 and #756's W9 "records nothing", by the orchestrator's decision that a pact change is never lost.
- yellow 1: the `LEFT` line and its five copies now say what is true.
- ⬜ 3 and ⬜ 4.

Check that #756's record-first order (W1) and its single-record property (W4) hold for a refused row's moves under a killed run. Then check that the new usage wording does not collide with #756's "left whole" meaning.

The new units the fixes created are a finding surface: `_frozen_released_o1` and the renamed A5.

## What this round found

Every round-1 verdict is closed, and the record-first order holds for a
refused row under a kill. One finding needs a fix. The fix made a refused row
a new reason to record a pact change, and the pact's own policy document
still names the old reasons as the whole list.

- **🟡 5 — `docs/the-pact.md` says the trigger is a moved hash or a BROKEN
  coordinate, "and that test is the whole trigger", but a refused row is now
  recorded with neither.** `docs/the-pact.md:115-122` says a record is
  written when `--reverify` *moves the hash of a ledger row* that cites a
  clause, or leaves a coordinate of one BROKEN. It then says *that test is
  the whole trigger* and *the record is written in both of the re-read's
  forms, a re-stamp in place and a `Re-read ·` row under `--into`*. Since
  `4834f19e`, a released row `--into` refuses for a stale `--checked` gets
  neither form. Its hash is not moved, yet its move is recorded
  (`skills/evidence-check/scripts/evidence_check.py:3602-3612`; P4 below,
  executed). The page states its own rank in the same file: *it outranks the
  SDD set*. A pact reviewer at the pact's repository may receive a record row
  for a ledger row that no run re-stamped, and the policy page tells them
  that cannot happen. The ledger home was corrected for the refusal
  (`docs/the-evidence-ledger.md:148-154`). The pact's home was not, because
  round 1's yellow 1 listed the sentences that say *nothing is recorded*.
  This sentence says *only these record*, so it was not on that list.

  **The class, enumerated** by searching the tree for the statements of what
  makes a run record. Only `docs/the-pact.md` says its list is exhaustive.
  The others are conditionals that stay true, but they are incomplete in the
  same way, and the fix below adds the refused row to the one a person
  running the command reads:
  - `docs/the-pact.md:115`: *the whole trigger*. False. This is the 🟡.
  - `skills/evidence-check/SKILL.md:324-329`: *where … a row whose hash this
    moves … one row per ledger row is appended*. True, but incomplete.
  - `skills/evidence-check/scripts/evidence_check.py:73-77`, the usage:
    *appends one row per re-read ledger row citing a clause*. True, but
    incomplete.
  - The comment above the pact-change section
    (`evidence_check.py:3702-3711`) and the docstring of
    `tests/test_a_signatory_records_a_pact_change.py`. Both are sufficient
    conditions, and both are true.
  - `PACT_CHANGE_INTRO`: *one row per ledger row whose code moved under a
    pact clause it cites*. Already true of a refused row.

- **⬜ 6 — where a coordinate's newest reading is outranked rather than
  drifted, the record gets a move from a hash to the same hash.** The fix
  copied the loop's append, and with it the loop's choice of old hash.
  `released_drift` keeps the released member's match even where that reading
  is OK and only outranked by a newer reading holding other content
  (`evidence_check.py:3454-3480`). The append then records
  `m.group("hash")` against `current_hash`, which are the same hash. Probe
  P3, executed: a released row read on 2026-09-01 at `57f678c6`; another
  item's fragment re-reads it on 2026-09-10 at `7069baf7`; then the code
  goes back to `57f678c6`. `--ledger` is narrowed to the release file. A
  refused run (`--checked 2026-09-04`) records
  `serialize@57f678c6` → `@57f678c6`. The move that happened was
  `7069baf7` → `57f678c6`. The written arm (`--checked 2026-09-12`) records
  the same no-op row at `bfa78c85`, and it does so at `edee5ca2` too. So the
  defect predates this branch and lives in #756's writer. The fix only
  reaches it by one more door. W4 calls over-recording *the safe direction*,
  and the row still names the right ledger row and clause. That makes this a
  ⬜, deferred below.

- **⬜ 7 — a section comment in the pact module still says the refused row
  records nothing.** `tests/test_a_signatory_records_a_pact_change.py:1585`
  reads `# --- #746: a row --into refuses for a stale date records nothing`,
  above the three cases that now show it records. Round 1's yellow 1 class
  has a sixth copy. It is a comment, so no behaviour or pinned fact depends
  on it.

**Round 1's verdicts, each checked against the fix.**

- **yellow 2, closed.** Read: the stale branch at `evidence_check.py:3602`
  appends each coordinate of `drifted[key]` with the same tuple shape the
  written loop uses, before the `LEFT` line is built. The row still reaches
  neither `rows` nor the plan. Executed: the two modules pass at the target
  (439). With `1640bf9a`'s checker in the clone, the renamed A5, the
  after-today case and the BROKEN case each fail, so all three were seen
  red. P2's shape is now
  `test_a_row_dated_after_today_has_its_move_recorded_before_its_correction`,
  and the record holds the move after run 1.
- **yellow 1, closed.** `STALE_NOTHING` now reads *no `Re-read ·` row was
  written for this row*, which is true in both arms. The five copies round 1
  named say the moves are recorded: the ledger home, `changelog.md:8-11`, F1
  and the L4 correction in this item's fragment, and the usage. The pins
  `test_into_refuses_a_row_its_checked_date_cannot_make_count` (eight
  cells), `test_a_reading_dated_after_today_is_named_with_a_correction` and
  the usage entry of `test_the_home_and_the_usage_say_a_stale_row_is_left`
  fail with `1640bf9a`'s checker. ⬜ 7 is a sixth copy that is only a
  comment. `phases/phase-1.md:46-49` still quotes the old line. That is a
  phase record of what phase 1 measured, so it is history and not a
  statement about the code.
- **⬜ 3, closed.** `changelog.md:21-25` now says the first four hold in
  every mode, narrowed or not, and gives the fifth its two modes. This
  matches the two cases round 1 named.
- **⬜ 4, closed.** `overview.md` has a divergence row for A8 and A10 that
  names both siblings and the reason.

**#756's W1 and W4 for a refused row's moves, executed.**

- Killed after the record (P4): one run holds a refused released row and a
  fragment row it re-stamps, both citing the clause. `record_pact_changes`
  is wrapped to exit 137 after it returns. The record holds both rows,
  written in one replace, and the fragment is untouched. The next run exits
  1 with the same `LEFT` line, leaves the record byte for byte, and
  re-stamps the fragment.
- Killed before the record (P5): the same tree, with the wrapper exiting
  before the real call. No record and no fragment change. The next run
  records both rows once, and a third run adds none.
- Read: a refused row adds nothing to the plan, so step 3 has nothing of it
  to apply. Its moves exist only in `moves`, which step 2 writes in one
  atomic replace beside the written rows'. W1's table holds as written.
  W4's last-word key is `(old, new)` per clause, row and coordinate. The
  move a refused run records is the one the repaired run plans later, from
  the same released match, so the repair records nothing twice.

**The usage wording against #756's "left whole", read.** In this tree,
*left whole* means a row written back with nothing changed. That is #387's
row with no date cell under `--checked` (`evidence_check.py:3006`,
`skills/evidence-check/SKILL.md`). #756's C1 also uses it: *a row left whole
moved nothing and records nothing*. The usage used to call the refused row
*left whole*, and under the fix that row records, so the old wording would
have contradicted C1. The new wording, *gets no Re-read row, is named*, uses
neither phrase. No sentence in the tree calls the refused row *left whole*
any more. `git grep` finds the phrase only in #387's rows, its work item,
the pact case at `tests/test_a_signatory_records_a_pact_change.py:381`, and
C1. C1's hash-only re-stamp to `reverify_into@2e8a336c` holds, because C1
says what a re-read records and what a row left whole records, and the
refused row is neither. Narrowed `--strict` over #756's fragment still
reads only the chore's three units DRIFTED, as in round 1. I carried that
result rather than re-deriving its cause.

**The new units.** `_frozen_released_o1` writes the freeze, one released row
with the given date and Code grounds, and an empty fragment, which it
returns. Its docstring says exactly that. The renamed A5 asserts the `LEFT`
line, no `Re-read · O1`, the one record row and byte equality across two
runs. That is W4 for the refused arm. The two other new cases assert what
their names say. One gap is not a defect: none of them kills a run. P4 and
P5 cover the kill window, and a case is offered below.

**Carried, not re-derived:** the ledger coordinates round 1 opened, and its
result that C1 and W8 moved by hash alone. This item's fragment checks
clean under narrowed `--strict` (76 ok).

## Regression tests to plant

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: one entry in
  `test_the_home_and_the_usage_say_a_stale_row_is_left`, under **Paste-ready
  fixes**. It is red at the target because the sentence is not there yet.
- Optional, not a finding: P4's shape as a case in
  `tests/test_a_signatory_records_a_pact_change.py`, beside
  `test_a_run_killed_after_its_record_is_finished_by_the_next`. A refused
  row and a re-stamped row are killed after the record, and the next run
  leaves the record byte for byte. Today only the probe holds W2 for the
  refused arm.

## Facts for the evidence ledger

- A refused row's moves are written in the same record replace as the run's
  written rows, before any ledger file. A run killed on either side of the
  record is finished by the next with nothing recorded twice (executed, P4
  and P5).
- The record's old hash is the hash a released member of the family
  recorded, not the newest reading's. An outranked-but-OK coordinate is
  therefore recorded as a move to its own hash, at the base and at the
  target (executed, P3).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 5 | `docs/the-pact.md` names a moved hash or a BROKEN coordinate as *the whole trigger* for a pact change, while a row `--into` refuses for a stale `--checked` is now recorded with its hash unmoved and no `Re-read ·` row | `docs/the-pact.md:115` | open | read against `evidence_check.py:3602-3612`; executed, P4: the refused row's move is recorded and its ledger is not written; `skills/evidence-check/SKILL.md:324-329` and the usage are true but incomplete, same class |
| ⬜ 6 | A coordinate that is OK but outranked by a newer reading holding other content is recorded as a move from its hash to the same hash, in the refusal arm the fix added as in the written arm | `skills/evidence-check/scripts/evidence_check.py:3602` | deferred to a new issue against #756's record writer | executed, P3: both arms record `57f678c6` → `@57f678c6` where the move was `7069baf7` → `57f678c6`; the written arm does the same at `edee5ca2`; W4 calls over-recording the safe direction |
| ⬜ 7 | The pact module's section comment for the refused-row cases still says the row records nothing | `tests/test_a_signatory_records_a_pact_change.py:1585` | open | read; a sixth copy of round 1's yellow 1 class, in a comment only |
| 🟢 | round 1's yellow finding 2 is closed — a refused row's moves reach the record, including the after-today arm whose repair no later re-read reaches | `skills/evidence-check/scripts/evidence_check.py:3602` | confirmed | executed: the two modules pass at the target (439); the three new pact cases fail with `1640bf9a`'s checker; read: the row stays out of `rows` and the plan |
| 🟢 | round 1's yellow finding 1 is closed — the `LEFT` line and its five copies say no `Re-read ·` row was written and the moves are recorded | `skills/evidence-check/scripts/evidence_check.py:3496` | confirmed | executed: the eight refusal cells, the after-today case and the usage pin fail with `1640bf9a`'s checker; read: the ledger home, `changelog.md:8`, F1 and the L4 correction |
| 🟢 | round 1's ⬜ 3 and ⬜ 4 are closed — the changelog names the fifth family's modes and the overview lists the sibling cases | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/changelog.md:21` | confirmed | read at `d481638f`, against the two cases round 1 named |
| 🟢 | #756's W1 and W4 hold for a refused row's moves under a killed run | `skills/evidence-check/scripts/evidence_check.py:5108` | confirmed | executed, P4: killed after the record, the next run leaves the record byte for byte and re-stamps; P5: killed before, nothing written, then one record and none twice |
| 🟢 | The usage's new wording does not call the refused row *left whole*, so it does not collide with #756 C1's *a row left whole … records nothing* | `skills/evidence-check/scripts/evidence_check.py:67` | confirmed | read: `git grep` finds *left whole* only for #387's row with no date cell and in C1; C1's hash-only re-stamp still holds |
| 🟢 | The new units `_frozen_released_o1` and the renamed A5 do what their docstrings say | `tests/test_a_signatory_records_a_pact_change.py:1588` | confirmed | read; executed: both pass at the target, and A5 fails with `1640bf9a`'s checker |

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

### P3 to P5

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 6: the record's old hash is the released member's, so an outranked-OK coordinate is recorded as a move to its own hash, in both of `reverify_into`'s arms and at the base | proposed: a new issue against #756's record writer; the fix is to take the old hash from the newest reading and skip a move whose two hashes agree | the orchestrator, who decides whether to file it |
| Without the freeze, one `--reverify` over every ledger moves the line a fragment's citing rows cite (round 1's deferral) | `overview.md` §*Not done*; already deferred in round 1 | the orchestrator, who decides whether to file it |

## Paste-ready fixes

### 🟡 5

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

Needs a fix: yes — 🟡 5, docs/the-pact.md names a moved hash or a BROKEN coordinate as the whole trigger for a pact change, and a row --into refuses for a stale date is now recorded with neither

Loses a record or crashes: no

## Proof block

Opened at `bfa78c85` in the round's clone, or with `git -C` against the
worktree:

- `skills/evidence-check/scripts/evidence_check.py`: the usage (40–110),
  `put` through `write_atomic` (1055–1145), `current_hash`,
  `released_drift`, `later_reading` and `reverify_into` (3379–3680), the
  pact-change section and `record_pact_changes` (3700–3990), and `main`'s
  `--reverify` branch (5090–5215); the fix diff `1640bf9a..2df48401`
- `tests/test_a_signatory_records_a_pact_change.py`: 1–130, 835–877,
  1580–1680 and the fix diff
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the fix diff,
  and 1978–2012
- `docs/the-evidence-ledger.md`: the fix diff
- `docs/the-pact.md`: 112–165
- `skills/evidence-check/SKILL.md`: 300–345
- `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md`: W1–W10 (145–262)
- `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md`: C1, and the fix's word diff
- `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md`: every row's claim, and the fix's word diff
- this item's `changelog.md` (1–30), and the fix's word diff of `spec.md`, `overview.md` and `survivors.md`
- `rounds/round-1-report.md` and `rounds/round-1.md`, whole
- the round's own paragraph, as the orchestrator handed it
