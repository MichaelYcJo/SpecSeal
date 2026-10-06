# Implementation Plan: the seal's emblem is one vector source, and both forms rasterise it (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

The emblem is the § as one set of closed curves in `seal_stamp.py`,
rendered by area for the terminal — a 6 × 6 grid of samples per half-block
cell averaged in linear light, the mark in one light colour with a shadow
0.7 cell up-left, the rim lit by angle, the disc's edge blended into the
sheet — and filled by Pillow at a supersampled resolution for the release
PNG. The disc is 24 cells across at its wax edge, pressed over the sheet's
lower right corner as #717 laid it, in both forms. The hook's ladder keeps
one rung with a disc and then the sheet alone, because a smaller disc breaks
the mark. The PNG is drawn as an image — circle, ring, curves, a real face,
antialiased, at 2× — and the note shows it at display width.

This frame was drawn by `framer` on Fable 5.1 (fce42e0d), and revised by
`framer` on Fable 5.1 on 2026-10-06, after phase 1 closed at 88070eac, to
fold in the owner's answer to `questions.md` Q1 — the mark, its rendering,
its size and its placement — which arrived after phase 1. The `Framed` mark
at the foot of `spec.md` is unchanged: a `Reframed … after round <N>.` line
names a stop in a review run, and none has begun. Phase 1 keeps its commit;
phases 2–4 below are the redrawn ones, and §*What phase 1 pinned that the
answer moves* says which of its cases the smith re-aims rather than
discovers.

**On wall time.** The original ticket (one renderer, nothing in
`seal_stamp.py` changing) might have fitted 45 minutes. It does not now:
phase 2 replaces the terminal sampler and re-aims about a dozen cases in two
files, phase 3 is the renderer the ticket asked for, phase 4 is the records.
A reasonable expectation for phases 2–4 is **two to three hours of smith
wall time**, most of it in phase 2.

## Technical context

**What the code does at 88070eac** (phase 1 closed, read 2026-10-06).

- `skills/verify/scripts/seal_stamp.py` (1,133 lines, stdlib-only, loaded
  by path from `broad_gate.py#STAMP`, `hooks/sealer-stamp.py`,
  `bin/seal-stamp` and `release_seal.py#stamp()`):
  - `EMBLEM_D`, an interim ring labelled INTERIM in its comment; `svg_path`
    (absolute `M L C Q Z`, a `Q` raised to a `C`, anything else refused by
    name), `flatten(paths, n=16)`, `inside` (even-odd), `shade` with three
    answers (`LILY_LIGHT`, `LILY_SHADOW`, `LILY_FACE`) from one-cell <!-- NAME NOT IN TREE -->
    neighbour probes; `EMBLEM_POLYGONS` flattened once at import.
  - `build(scale, r0_cells=R0_CELLS)` samples at cell centres, `R0_CELLS = <!-- NAME NOT IN TREE -->
    15.5 / 0.74`, `w = int(2·r0) + 2`, `h` even; footprints (43, 44),
    (39, 40), (35, 36), (33, 34) at 1.0 / 0.90 / 0.80 / 0.75.
  - `compose(rows, scale)` → `Letter(cells, width, height)`: the #717
    corner — `disc_top = height − disc_lines // 2 − 1`, `left` slid right
    until no text cell is covered and `GAP` (2) holds on every line, `width
    = max(TEXT_LEFT + longest + 2, left + dw // 2)`. **This is the placement
    the owner chose on 2026-10-06; `compose` keeps it.**
  - `block`, `colour_row` (a colour sequence only where it changes, 19 units
    each for a triple), `letter_row` (`KEY[top]`, else `KEY[bottom]`, else
    the frame), `KEY` (`m . G Y y`), `admitted`, `fitted`, `SCALE_LADDER`
    (0.90, 0.80, 0.75), `SCALE_FLOOR` 0.75, `SCALE_CEILING` 1.0,
    `DEFAULT_SCALE` 0.90, `MESSAGE_BUDGET` 9,000.
- `.github/scripts/release_seal.py` (610 lines): `paint(letter)` → one
  rectangle per half-cell at `CELL_W, CELL_H = 14, 28`, `png(ops, size,
  path)` with Pillow imported inside, RGBA and transparent where nothing is
  laid; `font(ImageFont)` chains DejaVu Sans Mono / Menlo / Consolas /
  Pillow's default at `FONT_SIZE` 22; `rgb` through xterm's cube;
  `seal_release` composes at `DEFAULT_SCALE` and writes `ASSET` `seal.png`.
- `.github/scripts/publish_release_note.py#sealed_glance` writes
  `![alt](url)` — a Markdown image carries no width, which is why S7 moves
  to `<img>`.
- Pillow 12.3.0 is the only non-stdlib package the renderer may use. It
  fills polygons (`ImageDraw.polygon`, non-zero, so a counter is cut by
  drawing each contour into an `L` mask and XORing them), composites through
  masks (`Image.paste(colour, mask=…)`, `ImageChops.logical_xor`), draws
  arcs with a width (`ImageDraw.arc`), and resamples with
  `Image.Resampling.LANCZOS` (support three output pixels at 4×, so a pixel
  three or more display pixels from an edge is exact after the downscale).
  It has no Bézier primitive and no angular gradient, which is why the
  source is flattened to chords before either rasteriser sees it and the
  rim is drawn as arcs or per pixel (Q7).

**The owner's reference, and what it measured.** The rendering the owner
chose was drawn by the orchestrating session's scripts `term3.py#make` (the
disc, `make(True, True, True, True, 0, 0.375, 1.04, n=6)`) and `corner.py`
(the disc on a sheet) in that session's scratchpad — **not in the tree, and
gone with the session**. `spec.md` §*Data & interfaces* writes the whole
rule out so nothing depends on them; the smith builds from the spec, and the
reference is named here only so a reader knows where the numbers below came
from. Measured by the framer on 2026-10-06 (`executed`: one probe in the
scratchpad over that reference and this tree's `colour_row`, deleted after;
units are UTF-16, the count `admitted` uses):

| Drawing | Grid | Cost, edge hard | Cost, edge blended | Cells exactly `LILY_LIGHT` / `LILY_SHADOW` / `FIELD` | Distinct colours |
|---|---|---|---|---|---|
| the § at 24 cells (the owner's choice) | 26 × 26 | 5,337 | 6,610 | 77 / 3 / 139 | 127 |
| the § at 20 cells (seen to fragment) | 22 × 22 | 4,144 | 5,116 | 49 / 2 / 84 | 107 |
| today's interim ring at 0.90 | 39 × 40 | 3,909 | — | — | — |

A sheet alone of a real run's shape (13 text lines) is 1,270 units, and
`admitted`'s docstring records 2,071 for the widest panel the tree can
produce. So one real-run stamp at 0.90 is **about 7,300–7,600 units** with
the disc half on and half off — under `MESSAGE_BUDGET`, with a margin of
about 1,400; two real runs do not share a message, which is the rule #717
wrote and the interim ring had relaxed. The disc costs more than the lily's
despite a third of the cells, because nearly every cell on an edge is its
own colour and `colour_row` emits two sequences for it. The reference's
sampler — 36 point tests per cell through `inside` over 32 chords per
cubic — took **0.95 s per disc** on this machine, which is over the bar
phase 1 set (Q6); see the constraints.

- Tests that pin the current drawing and layout and will move, by phase:
  phase 2 — in `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `test_the_emblem_is_lit_from_the_upper_left`,
  `test_each_rung_keeps_the_disc_height_the_chart_gave_it`, <!-- NAME NOT IN TREE -->
  `test_shade_lights_the_upper_left_edge_and_shadows_the_lower_right`,
  `test_the_terminal_draws_the_area_the_emblem_encloses`,
  `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`,
  `test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame`,
  `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours`,
  `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`,
  `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`; in
  `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`,
  `test_the_budget_is_named_and_derived_from_the_measured_limit`,
  `test_the_ladder_steps_down_in_order_and_ends_with_no_disc`,
  `test_a_character_outside_the_bmp_is_counted_as_two`,
  `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it`, and the
  docstring of `test_two_files_in_one_turn_are_under_the_budget_together`;
  phase 3 — in `tests/test_the_release_seal_is_drawn.py`,
  `test_paint_lays_every_cell_in_the_colours_block_gives_it`,
  `test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`
  (both parametrisations), `test_the_seal_module_imports_without_pillow`;
  in `tests/test_a_release_publishes_its_note.py`, the `sealed_glance`
  case. Tests that must stay green unchanged:
  `test_the_disc_draws_the_same_bytes_in_every_process`,
  `test_the_disc_is_symmetric_because_it_is_computed`,
  `test_the_emblem_fills_even_odd_from_an_svg_path`,
  `test_the_stamp_module_imports_with_pillow_blocked`,
  `test_the_twin_and_the_block_form_have_equal_width_and_height`,
  `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`,
  `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it`,
  `test_the_hooks_message_is_under_the_budget_for_one_file`,
  `test_seals_past_what_one_message_carries_wait_for_the_next_turn`,
  `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung`.

**Constraints the renderer must respect.**

1. `seal_stamp.py` stays stdlib-only and importable on Python 3.12 without
   Pillow: the point-in-polygon test, the flattening and the area sampler
   are pure Python.
2. No new package anywhere. Pillow stays pinned at 12.3.0, imported inside
   the drawing function, test-and-release only.
3. **The terminal draw stays fast enough for a `Stop` hook that may draw
   several stamps: under 0.5 s per disc** (Q6, re-opened). The reference's
   per-point `inside` over 32 chords took 0.95 s; at `flatten`'s 16 chords
   and with each cell's 36 points classified once and shared between the
   `under` answers, expect about half that. If the measurement is still over
   the bar, the fast path is a **scanline fill**: each contour's crossings
   per sample row give spans, the mark's bitmap at 6 points per cell is
   filled once and the shadow's once more at the 0.7-cell shift, and a cell
   reads its 36 bits from the two. Same points, same answers;
   `test_a_cell_is_the_mean_of_its_samples_in_linear_light` is what holds <!-- NAME NOT IN TREE -->
   the fast path to the point rule, and a cache of the finished grid as data
   in the module is not an option (a second source).
4. The hook's message stays under `MESSAGE_BUDGET` at 0.90 for a real run's
   values (A3), with the one-rung ladder.
5. Any failure in the release path is a `::warning::` and exit 0.
6. New code in `release_seal.py` avoids `zip(..., strict=)` and `*.UTC`.

**What breaks in six months.**

- Somebody edits `EMBLEM_D` by hand and a stroke goes thinner than a cell:
  `test_the_mark_reads_at_the_default_rung_and_fragments_below_it` counts <!-- NAME NOT IN TREE -->
  the pure-mark cells at 0.90 and is red under 60.
- A terminal with a different cell aspect: the half-block grid is square by
  construction (one column by one half-row), and the fit was searched on
  it, so a terminal whose cells are not 1:2 shows the mark a little
  stretched, as every half-block drawing is. Nothing to pin.
- Pillow changes `LANCZOS` or `load_default`. The pin holds the version.
- GitHub's sanitiser drops `width` on `<img>`. The image shows at 2× (too
  large, not broken), the alt text and the counts line still carry every
  number, and Q4 measures the sanitiser before the first tag.
- The harness moves `MESSAGE_LIMIT`. With one rung the ladder has one step
  to give, so a budget cut below about 7,600 draws every real run as the
  sheet alone; `MESSAGE_LIMIT`'s comment already says how to re-measure it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Trace the #717 lily into curves** (decision 1) | Withdrawn by the owner 2026-10-06: it reads badly at 0.90 and means nothing about the project | not taken |
| **A standard fleur-de-lis** | Not the owner's mark either | rejected |
| **Emblem as an SDF** | Pillow cannot fill an SDF; the PNG would need a per-pixel Python loop at 4 × 2 × (40 cells × 14 px)² ≈ 20 M samples. Curves flatten to polygons Pillow fills in C, and the same polygons answer the terminal's samples | **curves chosen** |
| **Emblem in a sibling module** | Four loaders reach `seal_stamp.py` by path; a sibling needs a second path in each | rejected; `seal_stamp.py` holds it |
| **Keep the chart for the terminal, curves for the PNG only** | Two sources drift, and the majority vote is what mangled the mark at 0.90 | rejected by the owner's update |
| **Centre sampling in three colours** (phase 1's sampler, built against the interim ring) | The owner saw it break the § into fragments at 24 cells and chose the area rendering to fix that | replaced by the owner's choice; nothing of it is kept beside the new sampler |
| **Area averaging in sRGB** (not linear light) | The mark's thin strokes read darker than the light they are drawn in, because the mean of two sRGB values sits below the mean of their intensities; the owner's reference averages in linear light | rejected |
| **The disc inside the sheet** (decision 2's placement) | Compared by the owner with the corner on 2026-10-06; the corner was chosen | rejected; `compose`'s #717 placement stays |
| **Shrink the disc on the lower rungs** (keep 0.80 and 0.75 at 21 and 20 cells) | The owner saw 20 cells fragment the mark and accepted nothing below 24; a rung nobody accepted is a rung the hook must never draw | rejected |
| **The ladder is one rung, then the sheet alone** | A real run that does not fit with its disc — measured at about 7,300–7,600 of 9,000 — loses the disc rather than shrinking it; the widest panel the tree can produce fits at the first rung (its case stays green) | **chosen**; `SCALE_LADDER = (0.90,)` |
| **Raise the band's floor to 0.90** | `--scale 0.75` by hand is a person's own choice, and about twenty parametrised cases walk the three scales; the floor's refusal sentence is already true of the § | rejected; the band stays, the hook never steps below 0.90 |
| **`DEFAULT_SCALE = 1.0` with 24 cells at 1.0** | A values file an older gate wrote carries `0.9`, and `admitted` never draws above a file's own scale, so every pending file would draw at 21.6 cells — the size the owner refused | rejected; 0.90 stays the rung and `DISC_CELLS` is its diameter <!-- NAME NOT IN TREE --> |
| **A smaller sample grid** (3 × 3 or 4 × 4 per cell) | The owner chose the rendering at `n = 6`; the grid fit was searched at 3 × 3 and confirmed at 6 × 6, and a coarser grid moves which cells read pure | rejected; `SAMPLES = 6` |
| **Quantise the blended colours to shorten the message** | Not needed: one real run fits at 0.90 with 1,400 units to spare, and quantising changes the rendering the owner looked at | not taken |
| **Per-cell classes carried beside the colours for the twin** | Every reader of a cell (`block`, `colour_row`, `letter_row`, `compose.colour`, the PNG) would take a wider cell for the twin's benefit alone | rejected; the twin's letter is the nearest palette colour's (`nearest`), one pure function of the colour <!-- NAME NOT IN TREE --> |
| **A cached raster of the mark as data in the module** | A second source the first can drift from, which is the thing the owner ended | rejected; a scanline fill is the fast path if one is needed (constraint 3) |
| **The shadow through offset masks** (the old plan's three-colour composite) | More masks than the rule needs: with two colours, drawing the shadow's polygons first and the mark's over them gives *shifted and not mark* by painter's order | rejected; painter's order, with even-odd through XORed contour masks |
| **PNG by sampling the terminal rule per pixel** | The 20 M-sample loop above | rejected; Pillow fills the same polygons |
| **Draw the PNG at display size, no supersample** | Pillow's polygon and ellipse fills are not antialiased; the staircase returns | rejected; 4× then `LANCZOS` |
| **Keep `![alt](url)` and write the PNG at display size** | Blurry on a high-density screen, which the ticket names as a goal | rejected; `<img width>` at 2× |
| **Read the disc's position off `compose`'s cells** (keep `Letter` three-field) | The radius has to be re-derived and a one-cell error moves the circle off the terminal's; `compose` already knows `left` and `disc_top` | rejected; `Letter.disc` added |
| **An opaque image the size of the sheet** | The disc hangs off the sheet's corner, so the image has to be transparent where neither is — as 0.19.0's is today | rejected; RGBA, transparent outside sheet and disc |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The vector source and the terminal sampler.** `EMBLEM`, `svg_path`, `flatten`, `inside`, `shade` in `seal_stamp.py`; `build` samples them at cell centres with `R0_CELLS · scale`, footprints pinned to today's four; `ART`, `shrink` removed; `SCALE_REFUSED` / `SCALE_TOO_LARGE` reworded; `KEY` comment and module docstring follow. `EMBLEM` holds an interim ring labelled as such in a comment. The lily lighting case rewritten; a fixture-emblem case for even-odd, shading and `svg_path`'s refusals; the area-fidelity case; the four footprints pinned <!-- NAME NOT IN TREE --> | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -p no:xdist`; each new case shown red by deleting the sentence it pins; `seal-stamp` run on a terminal and its `--shape` twin compared by eye once | 88070eac |
| 2 | **The owner's rendering in the terminal.** `EMBLEM_D` is the § from `spec.md` (the INTERIM paragraph goes); the palette gains `RIM_LIGHT` and `RIM_DARK` and loses `LILY_FACE`; `DISC_CELLS`, `RIM_WIDTH`, `SHADOW_OFFSET`, `FIT_OFFSET`, `FIT_SCALE`, `SAMPLES`; `build(scale, disc_cells=…)` with the footprint rule and `px(x, y, under=None)` by area in linear light with the tightening (S2), `shade` with two answers; `compose` passes `under` where the sheet is beneath, counts a touched cell for `GAP`, and fills `Letter.disc`; `nearest` and the six-letter `KEY` for the twin (S3a); `SCALE_LADDER = (0.90,)` with `admitted`'s docstring and `docs/the-broad-gate.md`'s #717 paragraph amended in the same commit (§14); the comments S8 names in `seal_stamp.py`. The phase-1 cases re-aimed as §*What phase 1 pinned that the answer moves* says, each new or re-aimed case seen red; the hook cases re-measured and the A3 sizes at 0.90 recorded for the ledger (Q3); the draw time measured (Q6) and the scanline fill built only if it is over 0.5 s <!-- NAME NOT IN TREE --> | the same two test files with `-p no:xdist`; `bin/seal-stamp --scale 0.9` looked at on a dark and a light background and said so in `phases/phase-2.md`, with `--shape` beside it; the sizes and the draw time written in the record | 108f549c |
| 3 | **The release PNG drawn as an image.** `draw(letter)` with `DENSITY`, `SUPERSAMPLE`, the circle, the rim ring by angle (Q7), the § as shadow polygons then mark polygons through XORed contour masks, in `FIT_OFFSET` and `FIT_SCALE` at the PNG's cell size, the real face, `LANCZOS`, transparent outside sheet and disc; `png(image, path)`; `paint`, `size` removed; `seal_release` wired; `sealed_glance` writes `<img … width>`; the pixel case replaced (S5, S6), the imports-without-Pillow case renamed, the broken-unit failure case points at `draw`; Q4 measured with `gh api /markdown`; the edge band's width decided (Q5) <!-- NAME NOT IN TREE --> | `bin/test tests/test_the_release_seal_is_drawn.py tests/test_a_release_publishes_its_note.py -p no:xdist`; `DRY_RUN=1 SEAL_PNG=… python3 .github/scripts/release_seal.py` with a JUnit fixture, the PNG opened and looked at once | |
| 4 | **The records close.** Docs amended (`docs/branch-and-release.md`'s bullet, `run_tests.py` and `release_seal.py` docstrings; the #717 paragraph if phase 2 left any of it); `changelog.md`; the ledger fragment with S1–S8 rows and the citing corrections of 0.10.0 S2, 0.17.0 L1/L2, 0.18.0 R1/R2 and the re-reads `phases/phase-1.md` lists; `overview.md` closed, its phase-1 divergence rows about the 0.90 footprint and `r0_cells` brought up to date with the new rule | the document cases named in S8; the `grep` from S8 returns only history; `evidence-check --strict .` exits 0 — it reads this item's three frame files once the fragment exists, so a name only the build can write carries `NAME NOT IN TREE` on its line | |

### What phase 1 pinned that the answer moves

`phases/phase-1.md` §*What the emblem answer and a smaller disc will touch*
listed these before the answer came; the answer touches more than it
expected, because the rendering changed and not only the mark and the size.
The smith re-aims each on purpose, in phase 2, rather than meeting it red:

- **The lighting case** `test_the_emblem_is_lit_from_the_upper_left` —
  built on three colours and a one-cell neighbour walk. Both go: the mark
  has one colour and a 0.7-cell shadow, and a cell is a blend. Rewritten to
  the centroid rule (S2a).
- **Area fidelity** `test_the_terminal_draws_the_area_the_emblem_encloses`
  — counted cells in one of three colours over the enclosed area. By area
  sampling the sum of coverage equals the area by construction, so the case
  is re-aimed to *cells nearer the mark than the field* (S2b), which still
  catches a mis-scaled frame.
- **The footprints** `test_each_rung_keeps_the_disc_height_the_chart_gave_it` <!-- NAME NOT IN TREE -->
  — pinned the chart's four heights, which the owner's 24-cell disc ends.
  Replaced by the footprint-rule case (S2); its name goes with it, and no
  released row cites it.
- **The shade fixture** `test_shade_lights_the_upper_left_edge_and_shadows_the_lower_right`
  — asserts a face. Two answers now (S2a).
- **The twin's five letters** and **the five colours on the wire** — six
  of each (S3a, S3b), with `G` gone.
- **Sequences per row** — a blended row has nearly one colour per cell; the
  bound moves to the sheet's lines and to the block form as a whole (S3b).
- **The budget cases** — the two phase 1 derived keep deriving; the three
  that name 0.80 or 0.75 move to the one-rung ladder (S4), and
  `test_the_budget_is_named_and_derived_from_the_measured_limit` pins the
  new tuple.
- **The corner case** `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`
  — stays, which the earlier frame had replaced; it gains the edge
  assertions (S3).
- **The docstring case** — the #832 sentences it pins say *cell's centre*
  and name the ring; they say *by area* and the § now.

The emblem's authoring constraint phase 1 wrote (*no stroke thinner than
about 50 units*) is discharged: the § is the mark, and
`test_the_mark_reads_at_the_default_rung_and_fragments_below_it` is what <!-- NAME NOT IN TREE -->
says it reads.

This table is also where the work records how far it got. **Status is
empty, or the commit that closed the phase.** Re-read the column after any
rebase.

## Operational impact

- **No new dependency.** Pillow 12.3.0 stays the one non-stdlib package, test-and-release only, pinned where it is. Nothing under `hooks/` or `skills/` imports it.
- **The hook's `Stop` message changes size and the ladder changes shape.** A real-run stamp is about 7,300–7,600 units at 0.90 (measured on the owner's reference, re-measured by phase 2); two real runs no longer share a message, and a stamp that does not fit with its disc is drawn as the sheet alone rather than at 0.80 or 0.75. `docs/the-broad-gate.md` says so. The budget constants do not move.
- **The terminal stamp changes shape** for every installed session at the next plugin update: a 24-cell disc on the corner, the § by area, with blended edges and more colour sequences per row. The draw costs under 0.5 s per disc (Q6).
- **Release notes from 0.20.0 on** show `<img … width>` at 2× density, transparent around the sheet and the disc as today. Earlier notes keep their cell-for-cell PNGs (Q2).
- **No migration, no env var, no compatibility break.** `DRY_RUN=1` and `SEAL_PNG` work as before; a pending values file from an older gate draws at its own 0.90.
