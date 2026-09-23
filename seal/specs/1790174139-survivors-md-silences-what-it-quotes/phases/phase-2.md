# 1790174139-survivors-md-silences-what-it-quotes — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e88cdebc |
| Ran by | unknown — the spawn prompt handed over no agent or model name; the orchestrating session fills this row |

## What this phase was asked

Put a phase record in the class the exemption file joined in phase 1 (#460):
the predicate names everything under a work item's `phases/`, on both sides.
Cases S6 (three) and S9 (second extension), each seen red first; the
docstring paragraph; a `seal/follow-up.md` row naming the repository owner
for what this gives up (Q5, default *no checker*). Re-run S5, because the
three items' phase records leave the pool, and write the numbers here beside
phase 1's.

## What this phase found

**Seen red, executed at `c1311c53` with the phase-1 predicate**, four cases
in one run (`4 failed, 63 deselected`):

- `test_a_phase_record_the_range_added_does_not_subtract_the_survivor_it_quotes`
  — `the phase record quoting that wording is what silenced it; exit 0`.
- `test_a_phase_record_the_range_edited_does_not_become_a_source` — `the
  check read that edit as a correction somebody has to chase into guide.md;
  exit 1`.
- `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` —
  `guide.md's copy went unreported; exit 0`. The direction differs from the
  one `spec.md` S6 named (*a phase record reported as a survivor*): with the
  record in a four-file pool the phrase it quotes has two carriers, its
  weight halves, and nothing clears the floor at all — #308's arithmetic
  rather than #460's report. The case's second assertion, that the report
  names `guide.md` and nothing else, is what refuses the reported-record
  direction; both are pinned.
- `test_the_docstring_names_both_sides_of_the_round_record_exclusion` —
  `**A phase record.** is no longer an exclusion stated`.

After the edit: `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q`
→ `67 passed` (64 after phase 1), exit 0 read directly; `uvx ruff check` and
`uvx ruff format --check` on the two files, both exit 0.

**S5 at `e88cdebc`**, the same script as phase 1, the exemption file deleted
at the tip in a scratch clone for the probe columns:

| Pull request | Range, sentences removed | Rows | with `--exempt` | without | file deleted at the tip, without | file deleted, with |
|---|---|---|---|---|---|---|
| #525 | `f8f1c9d..edd022a`, 162 | 29 | exit 0, **14** exempt | exit 1, **14** standing | exit 1, **14** standing | exit 0, **14** exempt |
| #528 | `c626382..24ea206`, 5 | 4 | exit 0, 0 | exit 0, 0 | exit 0, 0 | exit 0, 0 |
| #527 | `edd022a..c626382`, 8 | 3 | exit 0, 0 | exit 0, 0 | exit 0, 0 | exit 0, 0 |

Unchanged from phase 1, coordinate for coordinate: the three items' phase
records leaving the pool moves no candidate across the floor on these
ranges. Q2 is therefore unchanged too — 14 of 29, 0 of 4, 0 of 3 consulted.

**Q3, re-measured, and the instrument corrected.** The phase-1 script
compared candidates as (coordinate, score) pairs, so a coordinate whose
score merely moved when the pool shrank read as new; compared on
coordinates alone, #525 still shows the same **five** places that appear
only when its `overview.md`, `changelog.md` and ledger fragment leave both
sides — `docs/review-chain-spec.md:392`, `:845`,
`skills/code-review/SKILL.md:210`, `skills/code-review/orchestration.md:263`,
`tests/test_the_last_rounds_fixes_are_checked.py:8` — and #528 and #527 none.
Phase 1's five were checked against the fourteen `exempt` coordinates and
none overlaps, so its record stands as written.

**Q5's default is taken.** No checker; the loss is written as a
`seal/follow-up.md` row under *Schedulable items with nowhere else to go*,
answerer the repository owner, with the two options.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
