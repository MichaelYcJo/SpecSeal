# 1790655302-every-reader-ends-a-line-where-gfm-does — phase 6

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-6.md -->

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 0fded909 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The milestone 49 orchestrator added this phase mid-run, once work item F
(#672) had merged into `release/v0.16.0` at `3fc0c5bd`. It asked for three
things. First, merge `origin/release/v0.16.0` into this branch after phases
1–5, resolving every conflict hunk by hunk under `CLAUDE.md`'s ledger rule.
Then build, as a phase, the two `rider_check.py` items #664 still owns:
- `#inferred_anchor` compares `splitlines` numbering with `ast`'s, which the
  frame named as waiting for F.
- F's round 3, 🟡 3: a rider whose marker follows a mid-paragraph U+2028 or
  form feed is read by `#riders_in`, and `#region_lines`, on GFM lines since
  #668, never cuts it. So the rider's own stamp is hashed, and it can never
  read ok after `--reverify`. `seal/releases/0.9.1.md` S2 carries a
  `Corrected` note naming #664.

Stay out of `hooks/blocks.py`'s inline-HTML handling and
`tests/commonmark_oracle.py`, which are work item H's (#673). See each case
red first and kill one mutant per changed branch.

## What this phase found

- **The merge conflicted in two ledger files, and nowhere else.** In
  `seal/ledger/1790635413-…md`, G1 and G2 were this branch's alone. C1 and
  M1 took both sides' notes, with each anchor's hash from the side that
  edited its unit: `correction_check.py#rows` and `heading_starts` from
  here, `CASES` from F. `seal/releases/0.15.3.md` P1-4 was the same, with
  `readable` from here and `fence_opener` from F. `evidence-check` read 0
  drifted after the resolution, and `correction-check` over the merge found
  no correction dropped.
- **F renamed a unit the class case names.** `broad_gate.py#fenced_row_at`
  became `#hidden_row_at`. The case went red on the merged tree, naming the
  new unit, which is what it is for, and the merge commit renames it.
- **A rider had drifted since phase 1, and no module this item ran
  covered it.** `round_record.py#inherited_rows` carries a rider, and phase
  1's split moved the unit's hash. `tests/test_a_rider_reaches_its_file.py`
  found it after the merge. The rider is about hiders blanking a row in an
  earlier record, which the split does not touch. It was re-read and
  re-stamped by hand, and `rider_check.py` reads 19 ok.
- **The fix is a mapping, not a second rule.** `gfm_places` reads every
  `str.splitlines` line of a text on GFM's numbering: the GFM line it starts
  in, and whether it starts it. `comment_blocks` steps over a marker line
  that does not start its GFM line, and `inferred_anchor` moves a rider's
  lines onto `ast`'s numbering. The reader keeps F's `str.splitlines` lines.
- **It applies to every file type.** In Python a form feed or U+2028 is no
  line end to `ast` either, so a `#` rider after one had the same defect.
  The consequence is that a `.py` file carrying a marker now loads
  `hooks/blocks.py` for its splitter, where only markdown did before. F's
  P5-1 said other file types read as before, so it now carries a
  `Corrected` note.
- **`inferred_anchor`'s defect needs two breaks to show.** One form feed
  above a rider puts it one line late. That is onto the unit directly
  below, which is the answer anyway. Two breaks put it on the unit after
  that. The gap case and the last-piece case pin the mapping's other two
  branches, and each was seen red against its mutant.
- **S17 holds F's copy now.** `hooks/blocks.py#gfm_lines` and its pattern
  are equal to the reader's. The test reads the module and does not edit
  it.
- **Not taken: F's round 3, ⬜ 4.** It asks for the old region half of F's
  break case to be restored in `tests/test_a_rider_reaches_its_file.py`.
  The spawn named two items, and that finding is F's round's own.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
