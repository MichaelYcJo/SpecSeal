# Survivors — the release seal is drawn in curves

`survivor-check --range origin/release/v0.20.0...HEAD` reported 20 places
still carrying wording this work item removed from `seal_stamp.py`. One was
a live comment, the test module's section heading over the letter cases, and
it is corrected in the same commit as this file. The rest stand, for the
reason in each row: a released ledger row is never edited and this work
item's fragment corrects it, a released work item's frame records what that
work item decided, a test docstring tells the history its case exists for,
and two places share only the phrase *half a cell*.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.17.0.md` | the sheet's right edge at the disc's centre column, or two cells past the longest line where the text is wider; | L1, a released row, frozen; `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`'s `Corrected · L1` supersedes it |
| `seal/releases/0.17.0.md` | the disc's centre line on the sheet's last line, standing as far left as it can with no text cell covered | the same released L1 and the same correction |
| `seal/releases/0.17.0.md` | L2 · `build(scale)` is the disc with nothing past `WAX_EDGE` (0.84 of its radius) | L2, a released row, frozen; the fragment's `Corrected · L2` supersedes it |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | It stands as far left as it can without covering a text cell | #717's frame, which shipped in 0.17.0; it records what #717 built, and `settle --retire-process` retires the directory |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | highlight edge `(226, 82, 74)` where the chart cell up-left of a lily cell is field; | the same released frame: the lily's palette as #717 drew it |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | The lily is pressed into the wax in one colour, lit from the upper left: field `(120, 16, 20)`; | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | shadow edge `(96, 10, 14)` where the cell down-right is field; | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | The disc is `build`'s circle with the rope and `WAX_L` removed | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | The seal's centre line is the sheet's last line, so half of it hangs below the sheet; | the same released frame: #717's corner overhang, which #832 replaced |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | the sheet's right edge is at the seal's centre column where the seal, not the text, sets the width | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | The design, the scale, the palette's four disc colours and the four 256-colour codes. | the same released frame: what #717's owner chose then |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/plan.md` | one compositor from `letter(rows)`'s inner lines and `build` to cells | #717's released plan, a record of its phases |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/plan.md` | Enforce the gap only where the prototype did (the disc's equator) | #717's released plan, an alternative it rejected |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/plan.md` | two clear cells on every text line, the prototype's own intent | the same alternatives row of #717's released plan |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/overview.md` | The prototype's output ends with two empty lines, the rows of #30's rope-sized grid below the wax | #717's released closing memo, a divergence it recorded |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | `shrink` resolved a tie between two chart colours with `max(set(ink), key=ink.count)` | the docstring of `test_the_disc_draws_the_same_bytes_in_every_process` tells, in the past tense, the defect the case was written for (round 1's 🟡 6 of #30); the case still holds the property for the 14-cell disc |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | A calculated circle that is not reproducible gives that argument back at every scale but 1.0 | the same docstring's reason for the case, which holds for any computed disc |
| `skills/evidence-check/scripts/evidence_check.py` | # half a cell and the report stays per-row readable. | shares only *half a cell* with the removed comment on `build`'s sample grid; it is about a ledger row's cells |
| `tests/test_a_row_points_by_content.py` | a partial rewrite would strand half a cell in each format | shares only *half a cell*; it is about a ledger row's cells |
