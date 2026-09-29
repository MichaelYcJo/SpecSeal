# follow-up names are checked, and a re-read is dated — questions for the planner

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row below needs a person, and none blocks the build.** The owner
answered #387's one question before this frame. #508 and #387 left the
following judgments open. The tree answered them, and the grounds are in
`plan.md`'s Alternatives table and in `spec.md` (M1–M8). They are listed here
so nobody reopens them as questions:

- **How `path#name` is checked where the path resolves.** By token, in the
  named file. The unit rule refused two nested functions the file does define
  (M4).
- **What happens where the path does not resolve.** The name half is read as a
  bare name. 356 of 367 such spans are bare file names (M4).
- **Whether the underscore narrowing applies to the coordinate form.** It
  does not, where the path resolves (M4: all 140 underscore-free names
  resolve).
- **Whether `seal/follow-up.md` stays in the name corpus.** It comes out.
  Otherwise the red direction #508 asks for cannot be shown.
- **Whether the follow-up read waits for a live work item.** It does not: the
  file is permanent and its rows are live.
- **How a follow-up refusal is graded.** Exit 2, as `NOT-IN-TREE` is
  everywhere.
- **Whether this repository's build goes red when the arm widens.** Not at
  `1f218ae6`. `seal/follow-up.md` yields 0 refusals under both halves (M2,
  M3), and no work item is live (M1). Q1 re-measures after the rebase.
- **What `--checked` writes.** ` · D` appended to the date cell; D into an
  empty cell; nothing where the cell already ends in D (M5).
- **Which cell is the date cell.** `Checked`, else `Date`, else the fourth of
  a five-cell row under no header (M6).
- **Which dates are refused.** Anything that is not `YYYY-MM-DD`, is not a
  calendar date, or is later than the local date. Also `--checked` without
  `--reverify`.
- **A moved row with no date cell, under the flag.** Left whole, named, exit
  1.
- **Whether a heal (`identical content`) is dated.** Yes. Its hash moves, and
  the owner's rule is *every row whose hash it moved*.
- **The RIDER on `reverify`.** Deleted, since its question is answered.
- **`seal/follow-up.md` row 69.** Narrowed with a dated note (D3). Its open
  options stay the owner's.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | After the rebase onto A's squash (and whatever of B and D has landed by then), does this repository's tree still read 0 refused under both halves? That means every live work item's records, A's and this one's included, plus `seal/follow-up.md` | a measurement: run the widened arm over the rebased tree at the end of phase 1 and again at the end of phase 2, and record the counts in each `phases/phase-N.md` | 0 refused: nothing to correct. Any refusal: a `seal/follow-up.md` row is corrected in place there (an edit, not an append); a live record's line is corrected in its own work item's directory, or marked `NAME NOT IN TREE` where the record means a name the tree does not have. Another work item's record is corrected on this branch only where the record is plainly wrong; otherwise it is named in `overview.md` for its owner | 0 refused, as measured at `1f218ae6` (M1–M3) | ✅ Measured. Phase 1, at `18ac24e9`: 0 refused, `seal/follow-up.md` contributing 8 names. Phase 2, at `4f22852e`: 1 refused, this work item's own `plan.md` naming a test helper A's squash removed; corrected in place in that commit, and the tree reads 0 refused with 26 coordinate-form names read. `phases/phase-1.md` and `phases/phase-2.md` carry the counts |
| Q2 | Does A's overflow-cell arm add a header or row reader that the date-cell finder can use instead of a second one beside `grounds_cells`? | the work: phase 3, after reading A's squashed diff in phase 1 | Reuse: one reader for the table shape. A sibling: two readers that have to agree on the header and five-column rules | a sibling of `grounds_cells`, following its header rule | ✅ Reuse. A's squash moved the walk into `ledger_table_rows`, which yields `(line_number, header, cells)` with `header` None under no header; the date-cell finder reads it, and its line number is the splice's line (phase 1, read at `56e53c90`) |
| Q3 | The exact wording of every new line of output: the records heading and summary line (F7), the coordinate-form refusal detail (P1), the naming block and the dated lines of `--reverify` (R1, R3), and the `LEFT` line (R4) | the work: phases 1–3, each pinned by its case (§14) | Any wording carrying what `spec.md` requires of that line | the requirement in `spec.md`, rows F7, P1, R1, R3, R4 | ⬜ |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
