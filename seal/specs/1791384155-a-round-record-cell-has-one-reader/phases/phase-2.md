# 1791384155-a-round-record-cell-has-one-reader — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 984e45c8 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

J2 of `spec.md`: a home reader and an issue reader in `chain_check.py`;
`rounds_rows`, `release_seal.py#chain_counts` and `round_record.py#fix_table`
read through them; the panel's own home reader with its two patterns, the
release seal's `findall` and the fix table's own prefix test leave.
`docs/review-chain-spec.md`'s paragraph *The vocabulary the exit needs*, one
sentence by replacement. The fourteen prose cases replaced by S2's. Verified
by S2, S3 and S4 red first, then the four modules green.

## What this phase found

- **The fix table needs the note as well as the home**, so the one reader is
  `deferred_parts` (home and note), and `deferred_home` is its first half.
  Writing the cut a second time inside `fix_table` would have been the copy
  this work exists to remove.
- **`EMPHASIS` cannot be the layer the home's text loses.** It removes every
  underscore, so `tests/test_x.py` read as `tests/testx.py` — the defect
  round 2 of #666 fixed on the panel. The word is still matched by
  `verdict_of` through `EMPHASIS`; the home's text loses `HOME_MARKS`, the
  panel's narrower pattern, moved into `chain_check.py`.
- **A bare `deferred` in the fix table takes its home from the third cell**,
  and that cell is now read through the same grammar, as if the word stood in
  front of it: `| 1 | deferred | #309 — the parity arm |` closes as
  `deferred #309`, where it used to write the whole third cell into the
  Verdict cell. No case pinned that branch; one does now.
- **S4's expected Grounds omitted the third cell.** The note the generator
  writes is what followed the dash in the verdict cell, then the third cell's
  reasoning, joined with ` — `: `#854 — the run is capped — why; executed`.
- The release seal's S10 fixture carried `**deferred** #13, #14`, which the
  new grammar reads as one home naming no issue. It became two cells, and the
  second carries a note naming `#15` that counts nothing.
- The panel still prints a home in ASCII. That is the panel's concern (the
  letter twin maps only the owner's characters), so the encoding stays in
  `rounds_rows` and not in the one reader.
- The re-read rows went through `--ledger` narrowed to the seven released
  files and the two fragments the phase drifted; three rows `--reverify`
  wrote or re-stamped for the release branch's own 33 drifted rows were put
  back by hand. C3 of 0.18.0 is false now and is a `Corrected ·` row.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the panel's home reader and its two patterns in `broad_gate.py` | `chain_check.deferred_parts`, `HOME_MARKS`, `HOME_END` |
| the release seal's `re.findall(r"#(\d+)", …)` over a whole verdict cell | `chain_check.issue_of` over `deferred_home` |
| `fix_table`'s own `deferred` prefix test and its whole-rest home | `chain_check.verdict_of` and `deferred_parts` |
| test_the_home_is_read_off_the_cell_after_the_word and test_a_deferrals_home_is_read_whole (fourteen prose shapes and six word shapes) | `test_a_deferrals_home_is_what_stands_after_the_word` and `test_the_panels_home_is_the_gates_home` |
