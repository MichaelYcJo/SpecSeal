# Survivors — the release seal is drawn in curves

`survivor-check --range origin/release/v0.20.0...HEAD` reported 20 places
still carrying wording this work item removed from `seal_stamp.py`. One was
a live comment, the test module's section heading over the letter cases, and
it is corrected in the same commit as this file. The rest stand, for the
reason in each row: a released ledger row is never edited and this work
item's fragment corrects it, a released work item's frame records what that
work item decided, a test docstring tells the history its case exists for,
and two places share only the phrase *half a cell*.

Phases 5–9 removed more: the sheet from `seal_stamp.py`, #717's row shapes
from `broad_gate.panel`, and the Pillow drawing from `release_seal.py`. At
e0aaf29 the check reported 33 places beyond the first 19 rows. One was live,
`bin/test`'s line saying Pillow draws the release seal, and it is corrected
and pinned at d6839f6. The other 32 are the rows after the first 19, and
they stand for the same reasons as above and for two more: a case that asserts a removed
sentence is absent has to carry it, and a comment that tells a row's history
says what was there before it says what came back.

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
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | Since #717 there is no blank row in it, no `chain` | a negative pin: the docstrings case asserts this sentence is NOT in `seal_stamp.py`, so the case carries it to hold the comment above `SAMPLE_ROWS` to its #832 wording |
| `tests/test_the_gate_names_every_step_ci_runs.py` | chain off, because a drawn panel is green by construction | the comment over `HISTORICAL_ROWS` tells the row's history, #717 taking `chain` off, and its next sentence says #832 put it back |
| `seal/releases/0.18.0.md` | Decoded, every half of every cell is the colour | R2, a released row, frozen; the fragment's `Corrected · R2` supersedes it |
| `seal/releases/0.18.0.md` | writes paint's operations as an RGBA PNG | the same released R2 and the same correction |
| `seal/releases/0.18.0.md` | The frame's check, *the darkest pixel is nearer the ink than the parchment* | the same released R2's notes and the same correction |
| `seal/releases/0.18.0.md` | lays each cell of seal_stamp.compose's letter as a background rectangle | R1, a released row, frozen; the fragment's `Corrected · R1` supersedes it |
| `seal/releases/0.12.2.md` | gives a value 23 columns and cuts with no | R5's notes, a released row, frozen; the fragment's `Corrected · R5` supersedes it |
| `seal/releases/0.17.0.md` | inner lines without the frame and without any blank | L1, released and frozen; the fragment's `Corrected · L1` supersedes it |
| `seal/releases/0.17.0.md` | The block form emits a colour only where it changes, keeps a painted trailing cell | L3, released and frozen; the fragment's `Corrected · L3` supersedes it |
| `seal/releases/0.17.0.md` | describes the letter and the twin's characters | L4, released and frozen; the fragment's `Corrected · L4` supersedes it |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/overview.md` | Measured with bin/mutation-check over rgb's cube levels | #718's closing memo, which shipped in 0.18.0; it records what #718 measured, and `settle --retire-process` retires the directory |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/overview.md` | that check passed with the ink's red and green swapped | the same released memo |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/overview.md` | the darkest pixel is nearer the cell's ink than | the same released memo, quoting its frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | the PNG is pinned against the terminal output | #718's frame, which shipped in 0.18.0; it records what #718 built |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | The PNG carries the terminal form's colours | the same released frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | Both are seen red by swapping two colours | the same released frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | the PNG's top and bottom halves have the colours | the same released frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | In every non-space text cell, the darkest pixel is nearer the cell's ink | the same released frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | A triple as is, a 256-colour code through xterm's cube and grey ramp | the same released frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | an ordered list of ("rect", x0, y0, x1, y1, rgb) | the same released frame |
| `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md` | Pillow may enter only as a test-and-release dependency | the same released frame: what #718 allowed Pillow to be |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | absent where the ref is the commit | #717's released frame: the panel's rows as #717 built them, which #832 re-shaped in `panel` |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | The blank rows go from the data because the chosen sheet draws none | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | its top line as .---. and its bottom as | the same released frame: the twin over #717's sheet |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | the SEALED title is 124, the ink 94, the sheet 230, the edge 187 | the same released frame: #717's four 256-colour codes |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | the twin's first non-blank line is the sheet's | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | the first and last lines of the sheet are blank parchment | the same released frame |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md` | the seal's lowest row is below the sheet's last line | the same released frame: #717's corner overhang |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/questions.md` | How the sheet reads on a light terminal background as well as a dark one | #717's released questions, a question its owner answered then |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/questions.md` | the sheet's width where the text and not the seal sets it | the same released questions |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/questions.md` | Whether the blank rows stay in the data | the same released questions: #717's answer, which #832's owner reversed |
| `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/plan.md` | is drawn on success alone, so every exit code on it is 0 | #666's released plan, a record of its reasoning; the sentence it shares with `panel`'s docstring is still true there |
| `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md` | L2 described the 14-cell disc of four colours | round 1's fix pass rewrote the pair case's docstring, which shared *the owner's 28-cell disc of 2026-10-07* with this note; the note records what `Corrected · L2` replaced, and the disc it names is still the shipped one |
| `docs/the-broad-gate.md` | That disc is most of a stamp's size, so one real run's stamp goes out per message | the pair case no longer says *even the smallest panel's pair is over the budget*, because that depends on the mark; this sentence is about a real run's pair, which is over the budget under the S and under the archived key alike (round 1's report, 🟡 3) |
| `skills/verify/scripts/seal_stamp.py` | the owner's disc of 2026-10-07 the disc is `DISC_CELLS` across | shares only *disc of 2026-10-07* with the pair case's old docstring; it is about the disc's one size, which holds |
