# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 124cd1a6 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

This item's records (`spec.md` D8): the fragment's test rows for S1–S13; a
citing row for every released row phases 1–4 drifted, per row the
`Corrected ·` test row or the `Re-read ·` row, chosen by reading
(`questions.md` Q3); `changelog.md` and `overview.md`. The orchestrator
added: rows go in
`seal/ledger/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it.md`;
a released row is re-read with `--reverify --into <that file> --checked
2026-10-08`, a sibling's fragment row still under `seal/ledger/` is
re-stamped in place; the owner answered Q1 (a) — no bulk pass.

## What this phase found

**The drift was 106 findings over the frame's estimate, almost all of them
`reverify`.** `bin/evidence-check --strict .` at aae8f2bd read 114 drifted
coordinates. The frame counted the rows citing `malformed_rows`,
`grounds_cells`, `malformed_remedy`, `check_ledger`, `reverify_into`,
`target_problem` and the two skill sections; phase 1 also edited `reverify`
(S8's `LEFT` line), which 106 coordinates in the ledgers cite, and phase 2
edited `hooks/evidence-advisor.py#FROZEN_REPAIR` (Q4). Measured before
writing: a dry run of `--into` over an archive of the head in the scratchpad
said 38 citing rows and 9 in-place re-stamps were owed.

**Eight of the 114 were the base's, not this branch's.** At 863d7f80, before
any edit, `--strict` read 8 drifted, all `agents/warden.md#"## Report"`: #837
and #867 each re-read that section on their own branch, #837 at its new text
and #867 at its new heading reading, and the merged section is a third
content neither recorded. The same 8 stand at `origin/release/v0.21.0`'s head
(b6c81a83), beside 22 others this branch does not carry (an archive of that
head, read in the scratchpad: 30 drifted). Read for this phase: #837's diff
to §*Report* adds two sentences on a ⬜ note's grading and closing, and #867
changed no word of it; the six sibling rows that cite it — `S3`, the wrap
rule, `A6`, `A7`, `R7` and `1791384154`'s `S3` — claim the report and record
split, the wrap paragraph, the skeleton, the subheadings and the three
tables, none of which those sentences touch. So the in-place re-stamp of
those six, which the `--into` run makes with the rest, is a reading and not
a guess.

**Q3, answered per row by reading.** Each of the 38 released rows was read
against the diff of this branch; the fragment's citations name each one. Five
take a `Corrected ·` test row, because a test the row already cites holds
the whole claim:

| Released row | Test that holds it |
|---|---|
| `0.15.4.md`, *a `Code grounds` cell holding a coordinate …* | its seven cases and T1's; the claim is also corrected: a cell naming a test is no longer *citing none* |
| `0.15.4.md`, *`--reverify` names each `MALFORMED` row …* | `test_reverify_names_a_malformed_row_and_leaves_it`; the claim drops *and the remedy*, which no case holds |
| `0.15.5.md`, `S6` | `test_the_skill_states_the_grading_exit_code_returns_for_malformed` |
| `0.18.0.md`, `L10` | the two advisor cases it cites and `test_a_moved_released_row_is_told_its_correction_carries_every_coordinate` |
| `0.18.3.md`, `A2` | `test_the_documents_say_a_held_reading_is_left_alone`, parametrised over the four places the claim names |

The other 33 cite a test as one ground among several, or none, and take the
`Re-read ·` row `--into` wrote, which is Q3's default. Every one of those
claims reads true against the diff: `reverify` gained a list of test rows it
leaves and their `LEFT` lines, `check_ledger` one arm, `malformed_rows` a
test-aware branch, `reverify_into` one summary line, `target_problem` a
different resolver for the same answer, and the two skill sections added
paragraphs and changed none.

**The run wrote what the dry run said, less the five.** `--reverify --into
… --checked 2026-10-08` re-stamped nine sibling rows in place (six on
`agents/warden.md`, `1791384156`'s `C1` on `reverify` and `reverify_into`,
its `F1` on `target_problem`) and wrote 33 `Re-read ·` rows, exit 0; it
printed `INTO_HELD` once, as S9 says.

**The records arm read this item for the first time** once the fragment
existed, and refused two names: python_classes in `spec.md` §*Out*, which
is pytest's configuration key and no name of this tree, now marked `NAME NOT
IN TREE` on its line; and a name in `phases/phase-1.md` written in a code
span, now plain text.

**`survivor-check` named four places**, each a released row of
`seal/releases/0.19.0.md` still carrying `reverify` and `reverify_into` at
the hashes a sibling's row was re-stamped from. No sentence was removed.
Each is in `survivors.md` with the citation it opens with as the quote.

Executed at this phase's head, output read: `bin/evidence-check --strict .`
exit 0, `total: 7498 ok · 0 drifted · 0 broken · 0 external · 0 old-format ·
0 malformed · 0 overflow`, records `0 refused · 0 drifted`;
`bin/survivor-check --range origin/release/v0.21.0...HEAD --exempt …`, exit
0, four exempt; `bin/correction-check --range origin/release/v0.21.0...HEAD`,
exit 0, no correction dropped and no released ledger file changed; the
eight modules the orchestrator named, 437 passed; the 13 cases the five
`Corrected ·` rows name, green.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
