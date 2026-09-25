# 1790260565-a-ledger-row-carries-two-readings-in-one — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | f834eb2e |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#501: `tests/test_release_hygiene.py#overwide_rows` counts a row with no
header above it against a width its caller supplies, and the corpus case
supplies the ledger row's width, read from `templates/ledger.md`. A new unit
case gives a headerless six-cell row and expects it named against five, seen
red against the header-only function first. The corpus case's docstring
states what it now counts, with the instrument and the date.
`docs/the-evidence-ledger.md`'s escaped-pipe paragraph takes the plan's
paste-ready text. C2 (`seal/releases/0.15.1.md`) gets a `Corrected` note and
its "Three of the 22" is corrected. The fragment gains one row, and D1, E1
and C2 are re-read wherever their anchors drift. `survivor-check` answers Q4.

## What this phase found

- **The paste-ready policy text carried a miscount, and the paragraph says
  three.** It said the eleven-modules row's Notes cell was "split in two". At
  `31937b9f` the row has seven unescaped pipes and no closing pipe, so it has
  seven cells, and its Notes cell is split in three. The frame counted six
  by subtracting a closing pipe the row does not have. The policy paragraph
  and C2's corrected note both say three.
- **Seen red (§15).** Before the fix, the new case ran against
  `overwide_rows` with `width` added to its signature and ignored. It failed
  with `assert [] == [(1, 5, 6)]`.
- **The corpus count is now executed rather than read.** A `test_tmp_*`
  script walked the function's header logic over the shared file and every
  release file. It found 767 table body rows, 25 of them under no header
  (5 in `0.15.0.md`, 20 in `0.15.1.md`), all five cells wide, and no
  overwide row with the width applied. That is the frame's read figure,
  reproduced. `seal/ledger/` did not exist until this phase wrote its
  fragment.
- **A unit the plan did not name, `ledger_overwide`, closes a mutation
  survivor.** With the width argument removed from the corpus case, the
  corpus case stayed green, because no row in the tree is overwide. Both
  cases now call `ledger_overwide`, and the unit case asserts on it. The
  mutations were run from a Python script, each file restored from bytes it
  had read and `tests/__pycache__` cleared between runs. All five went red:
  `header` reset to `None` off a table (1 red); `header` starting at `None`
  (1); the template width misread by one (2); the helper passing no width
  (1); the closing pipe not subtracted (3). A six-cell row planted in the
  real fragment also turned the corpus case red. The planted row with the corpus
  call rewritten to bypass the helper stayed green. That is a case being
  rewritten, not a unit breaking, and nothing pins a call site against it.
- **`cell_count` moved to module level** so that `ledger_row_width` counts
  the template's header the same way `overwide_rows` counts a row. It is the
  same body.
- **Drift was D1, E1 and C2, as the plan predicted, and nothing else.** The
  lenient run over `0.15.1.md` named the policy section and the two
  hygiene anchors. `--reverify` over that file changed those three rows and
  nothing more (`git diff -U0`). The unscoped lenient run named no drift
  outside `0.15.1.md` and the fragment.
- **Q4 is answered: nothing survives.** `bin/survivor-check --range
  1c95c1dd..2263f5ae` examined 350 files against 8 removed sentences:
  "no removed wording is still standing". This work item writes no
  `survivors.md`.
- **The date is 2026-09-25 from this phase on.** The local clock passed
  midnight (`+0900`) after phase 1 closed. The re-reads are dated when they
  were made.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the nested `cells` inside `overwide_rows` | `cell_count`, at module level in the same file, with the same body |
| the policy's "three of them a second date-and-notes pair" | the same paragraph, as two pairs and one Notes cell split in three |
