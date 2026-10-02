# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 188c59fe |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`seal_stamp.py`: the four disc colours and the four 256-colour codes named;
`ROPE_L`, `ROPE_D`, `WAX_L` and `GOLD` removed; `build`'s `px` with nothing
past 0.84, `WAX_M` from 0.78, the field and the lily's three colours from
`shrink(ART, scale)` and the two neighbour tests; `sgr` taking an int; one
compositor from `letter(rows)`'s inner lines to cells — the sheet one blank
line above and below the text, the text three cells in, the disc's centre
line on the sheet's last line and the sheet's right edge at its centre column
where the disc sets the width, two clear parchment cells between every text
line's last character and the wax, no text cell covered — and two writers
over the cells, painted trailing cells kept; `KEY` for the twin's disc
letters and `|`, `.---.`, `'---'` for the sheet; `stamp` returning the
letter's lines; `beside` retired unless something still calls it. The
contrast measurement. The module docstring, `docs/the-broad-gate.md`'s
unchecked paragraph, `bin/seal-stamp` only if a sentence went false. Ledger:
`0.10.0` S2 corrected, S3 re-read; `0.15.7` N3, N5, N6 re-read, N7
corrected; new rows in the fragment. `changelog.md` and `overview.md`. The
S3 gap is the frame's judgement the owner did not see: build it as specced
and name the row it moves.

## What this phase found

**The frame holds for this phase.** The prototype is ported, not copied:
`narrow.py#sheet(scale=0.90, narrow=True, rw=trimmed(True))`'s geometry,
`env3.py#sealf`'s disc and `envelope.py#encode`'s writer, read as one
program through their `exec` chain. Over #702's values, trimmed the way
`panel` now trims them, the tree's letter is the prototype's cell for cell
with the disc two columns further right, and nothing else differs.

**The two-cell gap moves one row's spacing, the `suite` row's.** The
prototype checked its gap with the disc's column 0, which is outside the
disc on every row but the equator, so on the owner's rendering the wax
touched `6621 passed, 11 skipped` with no cell between. The tree checks every
text cell and the `GAP` cells after each line's last character, on both
halves of every line. The disc moves as a whole, so every disc row is two
columns right of the prototype's; the `suite` row is the one text line whose
distance to the wax changes, from zero cells to two, and every other text
line already had more. It costs 40 characters over #702's values.

**Sizes, measured 2026-10-02**, each the hook's message for one file: label,
then the block form, no final newline.

| Values | 0.90 | 0.80 | 0.75 | no disc |
|---|---|---|---|---|
| #702's seal, rows as `panel` now writes them | 6,277 (21 lines, 66 columns) | 5,440 | 4,677 | 1,263 |
| #702's seal, its own file as #666 wrote it (`chain`, `exit`, `drifted`, blanks) | 6,513 | 5,692 | 4,923 | 1,521 |
| A5's widest panel (`test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung`) | 7,249 (30 lines, 70 columns) | | | 2,071 |

Before #717 the same #702 file drew 10,171 at 0.90. The widest panel's
figure was read once by a `test_tmp_` probe beside that case, which was then
deleted.

**Contrast, computed 2026-10-02** with the WCAG 2 relative luminance over the
256-colour cube's RGB (`spec.md` S6, A17):

| Code | RGB | Against black | Against white |
|---|---|---|---|
| 230, parchment | (255, 255, 215) | 20.54 | 1.02 |
| 187, the sheet's edge | (215, 215, 175) | 14.23 | 1.48 |
| 94, ink | (135, 95, 0) | 3.67 | 5.73 |
| 124, the title | (175, 0, 0) | 2.82 | 7.44 |

On the parchment itself the ink is 5.60 and the title 7.28; the edge against
the parchment is 1.44. On a white terminal the sheet and its edge are close
to the background, which is the reading `overview.md` names the owner for.

**Q4, the build's answers.** The compositor is `compose(rows, scale)`,
returning `Letter(cells, width, height)` — the sheet's own width and
height — with `sheet_text(rows)` the lines it writes; the writers are
`colour_row(cells)` and `letter_row(cells)`, and `disc_cells(px, w, y)` is a
line of the disc alone for the two cases that read the disc by itself. The
twin's disc letters are `m` the wax's edge, `.` the field, `G` the lily's
face, `Y` its highlight and `y` its shadow. Where the text and not the disc
sets the width, the edge stands two cells past the longest line — one of
parchment, then the edge — which is the prototype's.

**`scale` None draws the sheet with no disc.** `fitted`'s last rung was the
old panel in phase 1; it is `compose` with no disc now, so the last rung is
the same letter without its wax.

**Two empty lines are dropped.** The disc's grid keeps the size #30's rope
gave it, and its last rows below the wax are empty; the prototype's output
ended with them. `compose` drops trailing lines that carry nothing, in both
forms alike.

**A9's *every sheet line has the same visible width* is read as: a line is
the sheet's width exactly, or wider where the disc carries it past the
edge.** A line beside the disc is longer than the sheet by construction, so
the literal reading cannot hold of the chosen layout; the case asserts the
reading above, and that a line's last painted cell is kept.

**A9 over `SAMPLE_ROWS`, A10 over `ROWS`.** The sealer test's `ROWS` moved to
the shape `panel` returns now, and the one case that reads a `None` row
through `letter` plants its own. The hook's cases keep the older shape in
`FULL_ROWS`, which is A13's file.

**`beside` and `GOLD` are gone**; nothing else called `beside`.
`strip_ansi` stays, because two cases call it.

**A case the frame's list missed.**
`tests/test_the_gate_asks_the_range_ci_will_ask.py#test_the_panel_names_the_ref_the_base_came_from`
read the ref off the twin with a `\|` after the commit; the sheet's edge on
that line may be the disc's. It reads the next line's value in the commit's
column now, as the plan expected.

**Red, as shown.** Against the rope-and-gold drawing as it stood at
`f74897df`, the cases written first were run before any drawing code: all
fifteen selected were red, the widest-panel case on size — 10,369 characters
against the 9,000 budget — once its own fixture's 25-character home, which
`fit` elided, was shortened. The cases added at `853b34ac` for the centre,
the trailing cells, the lily's light and the twin's letters came after the
drawing; each was seen red by the mutations below.
Mutations through `bin/mutation-check` are listed below.

Twenty-five mutations through `bin/mutation-check`, each red: `GAP` 0;
`TEXT_LEFT` 4; the wax's edge at 0.90; the highlight's neighbour taken
up-right, the shadow's taken right; a highlight returned as a shadow; the
title in ink; `PARCHMENT` 231; `SHEET_EDGE` 230; the 256-colour form written
as truecolour; a painted space written as a half-block; the final reset
dropped; the trailing-cell trim removed; the trailing-line drop removed; the
twin's bottom half read before its top; the bottom corner written `.`; the
text-set width one cell short; the disc-set width the whole disc; the disc's
top two lines higher; one leading space no longer dropped; blank lines kept;
the highlight given the face's letter; the docstring's *pressed over*
reworded; `panel`'s bold sentence reworded; and the disc drawn only where it
is off the sheet. That last one SURVIVED the first run — nothing asserted
that the disc covers sheet cells at all — and is red against
`test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`'s
*pressed over it rather than tucked under* assertion, added at `abd740e4`.
One planned break was refused by `mutation-check` because its old and new
text were the same (a typo in the script), and was not counted.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The rope ring (`ROPE_L`, `ROPE_D`), the outer red band (`WAX_L`) and the golds (`GOLD`) | none: the owner's drawing has none of them; `0.10.0` S2 is corrected for the rope |
| `beside`, which set the disc and the panel side by side | `compose`, which writes the text on the sheet and presses the disc over its corner |
| The panel's frame on the drawing (`.---.`, `|`) | the sheet's edge in colour, and the same characters in the twin |
| The prototype's two empty trailing lines | none |
