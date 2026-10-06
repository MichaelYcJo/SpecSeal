# Feature Specification: the seal's emblem is one vector source, and both forms rasterise it (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Raised by the owner looking at the 0.18.3 release note: the seal image is
the terminal stamp blown up cell for cell, so every edge is a staircase and
the emblem is a block mosaic. The owner's decisions, in order:

1. (#832 comment, 2026-10-06) The lily traced from the #717 chart into
   curves. **Withdrawn the same day**, through the orchestrator: the lily
   reads badly at 0.90 and has no tie to the project.
2. (2026-10-06, through the orchestrator) **The emblem is reopened.** The
   emblem is **one vector source**, and the terminal block stamp and the
   release PNG both rasterise it at their own resolution. Phase 1 built that
   mechanism against an interim ring (closed at 88070eac).
3. (2026-10-06, after phase 1, the owner's answer to `questions.md` Q1,
   chosen from renderings drawn on the orchestrator's machine and looked at
   in the owner's own terminal) **The mark is §**, the section sign, in the
   outline of Georgia Bold scaled to 820 units in the 1000-unit frame. **It
   is rendered by area**: each half-block cell is the average of a 6 × 6
   grid of samples taken in linear light, the mark in one light colour with
   a shadow 0.7 cell up-left of it, the field's inner rim lit continuously
   from the upper left, the disc's edge blended into the parchment where the
   sheet is under it. **The disc is 24 cells across at its wax edge** at the
   default rung; the owner saw 20 fragment the mark, and accepted nothing
   smaller. **It is pressed over the sheet's lower right corner, half on and
   half off** — the #717 placement, chosen over the disc inside the sheet
   that decision 2 had asked for. The release PNG follows the same placement.

So this frame fixes the mechanism and the mark. The file names below are
coordinates in the tree as it stands at 88070eac (phase 1 closed), read
2026-10-06.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Nothing here stops to ask mid-run. The one owner decision (the emblem, its rendering, its size and its placement) is answered and written in below; every other judgment is made from the tree and written where a reviewer can open it |
| `CONTRIBUTING.md` §*Running the checks* (*the gates themselves are stdlib-only Python and import nothing the suite installs*; Pillow is *test-and-release-only*) | The vector source and the sampler that rasterises it for the terminal live in `skills/verify/scripts/seal_stamp.py` and are stdlib-only, because `broad_gate.py`, `hooks/sealer-stamp.py` and `bin/seal-stamp` load that file. Pillow is imported in `.github/scripts/release_seal.py` alone, inside the function that writes the PNG, as today. **No new dependency of any kind** — not an SVG library, not cairo, not matplotlib, not numpy. `questions.md` says why curves and not an SDF under this constraint |
| `docs/the-broad-gate.md` §*Where the stamp is drawn*, the #717 paragraph (`MESSAGE_LIMIT`, the ladder, *a seal keeps its disc*) | The hook's message stays under `MESSAGE_BUDGET`. The ladder loses its two lower rungs (S4): a disc smaller than 24 cells breaks the mark, so the step after 0.90 is the sheet alone, which the ladder already ends in. The paragraph's sentence *its file's own scale, then 0.90, 0.80 and 0.75* and its *does not fit at 0.75 by itself* are amended in the commit that changes the ladder (§14), with the `Enforced by:` line under it kept. The sizes are re-measured, not assumed (S4, `questions.md` Q3) |
| `docs/branch-and-release.md` §*Every act the release performs once it reaches `main`*, the bullet *Then the release's seal is attached* (#718) | The seal is still a second act that never fails the release. The bullet's description of the drawing (*from the broad gate's letter*) is amended to say the image is drawn from the same rows and the same emblem, not rasterised from cells |
| `docs/release-checklist.md` §6, the box *A GitHub Release exists at `vX.Y.Z`* | `DRY_RUN=1 python3 .github/scripts/release_seal.py` keeps drawing one by hand; the box stays true and gains nothing but the new look |
| `.github/scripts/publish_release_note.py`, module docstring (*The summary adds no way to fail*) and `release_seal.py`'s (*Any failure leaves the note as it was published*) | A draw that raises, a font that will not load, an emblem that will not parse — each is one log line and one `::warning::` with exit 0 |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `CONTRIBUTING.md` (*Python 3.12 is the supported floor*) | New code in `release_seal.py` uses no `zip(..., strict=)` and no `*.UTC`, or carries the guard block. `seal_stamp.py` already carries `FLOOR` and `below_floor` |
| `CLAUDE.md` §*a change writes fragments, never the shared file*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* (`Ledger frozen from` is declared in `seal/config.md`) | Changelog in `seal/specs/1791270164-…/changelog.md`. New rows in `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`. Released rows this work makes false are **corrected by a citing row in the fragment**, never edited where they live: `seal/releases/0.10.0.md` S2 (*the disc is computed from the 29×32 chart*), `seal/releases/0.17.0.md` L1 (the 6,277 / 7,249 sizes, and the ladder's three rungs) and L2 (`shrink(ART, scale)`), `seal/releases/0.18.0.md` R1 and R2 (`paint`, `size`, the cell-for-cell pixel pin); and the re-reads `phases/phase-1.md` lists (0.15.7 N7, 0.17.0 B2) |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures keep `example/repo`, `example.com`, `/Users/x/` |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is *every place the chart, the lily, the centre-sampled three-colour mark, the three-rung ladder or the 20-line disc is described or pinned*, enumerated in S8. Every changed line a person reads is pinned in the same commit. Every new case is seen red first and the hand-back says how |

## Scope

### In

1. **One vector source, and it is the §.** `EMBLEM_D` holds the path
   string in *Data & interfaces* verbatim, in the frame phase 1 built
   (`svg_path`, `flatten`, `inside`); the interim ring and the INTERIM
   paragraph over it go.
2. **One sampler by area, two resolutions.** The terminal form averages a
   6 × 6 grid of samples per cell in linear light over three layers — the
   disc (wax, lit rim, field), the mark, its shadow — and tightens a cell
   wholly inside the field through a smoothstep; the release PNG fills the
   same layers with Pillow at a supersampled resolution. Phase 1's
   centre-sampled, three-colour `shade` is replaced, not kept beside.
3. **The disc on the sheet's lower right corner, half on and half off**, as
   #717 laid it and as `compose` lays it today. New: the disc's edge is
   blended into the sheet's colour where the sheet is under a cell and left
   hard where the disc hangs off it, and `Letter` says where the disc is, so
   the PNG draws its circles at the terminal's coordinates.
4. **The disc is 24 cells across at its wax edge at `DEFAULT_SCALE`**, and
   the hook's ladder has one rung with a disc. `DISC_CELLS` names the <!-- NAME NOT IN TREE -->
   owner's number; `R0_CELLS`, phase 1's radius parameter, goes with the <!-- NAME NOT IN TREE -->
   chart's heights it kept.
5. **The release PNG drawn as an image**: a computed circle, the rim as a
   lit ring, the § as filled curves with its shadow, the sheet's text set in
   a real monospace face, everything supersampled and downscaled with a
   filter, written at 2× the display size and shown through
   `<img … width="…">` at the display size.
6. **The pins that follow the change** and the documents that describe the
   drawing (S8), including the two hook-policy sentences the ladder change
   moves.

### Out

- **Redrawing 0.18.0–0.19.0's release images.** Nothing in the tree can do
  it unattended: a redraw needs the suite's counts at that tag, which the
  `seal` job's run supplied once. `DRY_RUN=1` from a checkout at the tag is
  the by-hand path and stays as it is (Q2).
- **The rows, the sheet's colours, the budget, the default, the band.**
  `release_rows`, `LABELS`, the four sheet codes, `MESSAGE_LIMIT`,
  `MESSAGE_RESERVE`, `MESSAGE_BUDGET`, `DEFAULT_SCALE` (0.90), `SCALE_FLOOR`
  (0.75) and `SCALE_CEILING` (1.0) are unchanged. `seal-stamp --scale` below
  0.90 draws a disc the owner saw fragment, by that person's own choice; the
  hook never steps there (S4).
- **The disc's colours as the owner chose them in #717**: `WAX_M`, `FIELD`,
  `LILY_LIGHT`, `LILY_SHADOW` keep their triples and their names. What
  changes is the palette's membership: `LILY_FACE` leaves with the <!-- NAME NOT IN TREE -->
  three-colour rule, and the rim's two ends join it (S2).
- **A fleur-de-lis**, standard or traced. Decision 1 is withdrawn.
- **The disc inside the sheet.** Decision 2 asked for it; the owner compared
  it with the corner on 2026-10-06 and chose the corner (decision 3).
- **The `seal-stamp` command line**, `--scale`'s band and its refusals keep
  their shape; the floor's refusal sentence stays true (*too few cells for
  its emblem to be read*) and gains nothing.
- **Pillow's version**, `run_tests.py#PACKAGES`, the workflow's install
  line. Pinned where they are; the holding cases stay green untouched.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · one source, the § | Given `EMBLEM_D` is the path string in *Data & interfaces*, when the module imports, then `svg_path` reads it into two paths (the outline and its counter), `flatten` makes them polygons, every vertex lies within radius 0.95 of the field's edge (the farthest is at 0.834, read from the string), and `inside` answers even-odd from them with no third-party import. The frame is phase 1's: origin at the disc's centre, the field's edge at radius 1.0, `y` down | `test_the_emblem_fills_even_odd_from_an_svg_path` and `test_the_stamp_module_imports_with_pillow_blocked` green unchanged; a new case reads `EMBLEM_D` back through `svg_path`, counts two paths, and asserts the farthest vertex is under 0.95 and over 0.80 (so a frame scaled by accident is red either way) |
| S2 · the terminal samples it by area | Given a scale in the band, when `build(scale)` is asked, then it returns `(w, h, px)` with `diameter = round(DISC_CELLS · scale / DEFAULT_SCALE)` — 24 at 0.90, 27 at 1.0, 21 at 0.80, 20 at 0.75 — `w = diameter + 2`, `h = w + w % 2` (so (26, 26), (29, 30), (23, 24), (22, 22)), and the disc's radius `diameter / 2 / WAX_EDGE` cells. `px(x, y, under=None)` is the cell's colour: the mean, in linear light, over `SAMPLES` × `SAMPLES` (6 × 6) points placed at the centres of the cell's equal sub-squares, of each point's colour by the rule in *Data & interfaces* (`under` outside the disc; `WAX_M` on the wax; the rim's mix by angle; and in the field `LILY_LIGHT` on the mark, `LILY_SHADOW` on its shadow, `FIELD` else). With `under` None a point outside the disc is dropped, and a cell with half or fewer of its points inside the disc is `None`. A cell whose every point is field, mark or shadow is **tightened**: the mark's share and the shadow's share are each put through `t = smoothstep(clamp((share − 0.15) / 0.7))`, and the cell is `FIELD` mixed toward `LILY_SHADOW` by `t_shadow · (1 − t_mark)`, then toward `LILY_LIGHT` by `t_mark`, in linear light. The mark is placed in its frame scaled by `FIT_SCALE` (1.04) and shifted by `FIT_OFFSET` (0, +0.375) cells <!-- NAME NOT IN TREE --> | The footprint case re-aimed: `test_the_disc_is_twenty_four_cells_across_at_the_default_rung` pins the four footprints above and the radius 12 / 0.84 at 0.90 (replacing `test_each_rung_keeps_the_disc_height_the_chart_gave_it`, which pinned the chart's heights). `test_a_cell_is_the_mean_of_its_samples_in_linear_light`: for every cell of `build(0.90)` and of `build(0.75)`, the case re-samples the same 36 points through `inside` and the layer rule written in the case itself and asserts `px` equal, so a faster rasteriser (`plan.md`) is held to the point test. `test_the_mark_reads_at_the_default_rung_and_fragments_below_it`: at 0.90 at least 60 cells are exactly `LILY_LIGHT` (77 measured on the owner's reference, `plan.md`) and at least 100 exactly `FIELD` (139 measured); at 0.75 strictly fewer cells are exactly `LILY_LIGHT` than at 0.90 — the owner's reading, in numbers. `test_the_disc_draws_the_same_bytes_in_every_process` and `test_the_disc_is_symmetric_because_it_is_computed` stay green <!-- NAME NOT IN TREE --> |
| S2a · lit from the upper left | Given `build(scale)` at every rung of the band's three tested scales, when the field's cells are read, then the centroid of the cells' shadow weight (how far each is toward `LILY_SHADOW` from `FIELD`, in linear light) lies below and to the right of the centroid of their mark weight (toward `LILY_LIGHT`), both weights are non-zero, the rim's lightest cell is in the upper-left quadrant and its darkest in the lower-right, and `shade` on the fixture square gives the highlight at every inside point, the shadow 0.7 up-left-inside-only, and nothing in the hole | `test_the_emblem_is_lit_from_the_upper_left` rewritten to the centroid rule (the three-colour neighbour walk is gone with `LILY_FACE`); `test_shade_lights_the_upper_left_edge_and_shadows_the_lower_right` re-aimed to two classes. Each seen red by taking the shadow probe down-right <!-- NAME NOT IN TREE --> |
| S2b · the mark's area | Given `build(scale)` at every rung, when the field's cells nearer `LILY_LIGHT` than `FIELD` in linear light are counted, then they cover between 85 % and 115 % of the area the polygons enclose, scaled by the fitted field radius squared | `test_the_terminal_draws_the_area_the_emblem_encloses` re-aimed from *cells in one of three colours* to *cells nearer the mark than the field*; seen red by scaling the frame by 1.3 as phase 1 did |
| S3 · the disc on the corner, its edge on the sheet | Given rows and a scale, when `compose(rows, scale)` is asked, then the disc stands as #717 laid it (centre line on the sheet's last line, centre column on its right edge where the disc sets the width, pushed right until every text line keeps `GAP` clear parchment cells before the first cell the disc touches, blended or not); a cell over the sheet is `px(x, y, under)` with `under` the sheet colour beneath it as a triple (`PARCHMENT` or `SHEET_EDGE` through xterm's cube) and a cell off the sheet is `px(x, y)`; `Letter` gains a fourth field, `disc`: `(left, top, w, h)` in cells and half-rows, or `None` with no disc. The twin keeps one footprint with the block form | `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text` kept and extended: an edge cell over the sheet is a blend strictly between `WAX_M` and the parchment per channel, an edge cell off the sheet is a disc colour or `None`, and `letter.disc` names exactly the cells carrying a triple; `test_the_twin_and_the_block_form_have_equal_width_and_height`, `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`, `test_not_sealed_carries_no_disc_and_names_every_failure` green |
| S3a · the twin's letters | Given a cell whose colour is a blend, when `letter_row` writes it, then the letter is `KEY`'s for the palette colour nearest it in linear light — `m` wax, `.` field, `Y` the mark, `y` its shadow, `M` the rim's light end, `n` its dark end — or the sheet's own character where the parchment's triple is nearer than any of the six | `test_the_twin_writes_the_discs_six_letters_over_the_sheets_frame` (renamed from *five*): `KEY` has six distinct letters over exactly the palette, `.` for `FIELD`, and a blended cell's letter is the nearest palette member's <!-- NAME NOT IN TREE --> |
| S3b · the colours on the wire | Given the block form at 0.90, when its truecolour triples are read, then `FIELD` and `LILY_LIGHT` each appear exactly, every triple lies within the per-channel range of the palette plus the parchment, nothing of the rope, the outer red band or the gold is left, and the sheet's four codes are as before | `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours` re-aimed: the palette is the six triples in *Data & interfaces*, the per-channel bound replaces *every triple is one of five*, and the old-colour exclusions stay. `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` re-aimed: a blended disc row carries up to two sequences per cell, so the per-row bound holds for the sheet's lines outside the disc and the whole block form carries fewer sequences than twice its cells |
| S4 · the budget holds at one rung | Given `SCALE_LADDER` is `(0.90,)`, when `admitted` lays blocks, then it carries as many of the oldest as fit together with their disc at 0.90 (each at its own scale where that is lower), and one block alone that does not fit with its disc is the sheet with no disc; `full_values()` through `dispatch.py stop` is under `MESSAGE_BUDGET` with its disc at 0.90, and the widest panel the tree can produce fits at the first rung | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`: `test_the_budget_is_named_and_derived_from_the_measured_limit` pins the one-rung tuple; `test_the_ladder_steps_down_in_order_and_ends_with_no_disc` rewritten for two rungs (0.90, then the sheet) and two blocks where the newer waits rather than shrinks; `test_a_character_outside_the_bmp_is_counted_as_two` steps to the sheet instead of 0.80; `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it` reads `SCALE_LADDER[-1]`; `test_two_files_in_one_turn_are_under_the_budget_together` and `test_several_files_come_out_as_one_message_oldest_first` derive their premise as phase 1 left them; `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` green; `test_the_policy_states_the_budget_and_names_its_case` green over the amended paragraph. The sizes at 0.90 are written into the ledger fragment's correction of 0.17.0 L1 (Q3) |
| S5 · the PNG is drawn, not rasterised from cells | Given `compose`'s letter, when `draw(letter)` is asked, then it returns an RGBA image whose display metrics are `CELL_W` × `CELL_H` per cell (14 × 28) and `FONT_SIZE` 22, drawn at `SUPERSAMPLE` (4) × `DENSITY` (2) and downscaled with `Image.Resampling.LANCZOS` to `DENSITY` × the display size, transparent where neither sheet nor disc is: the sheet as one parchment rectangle with its edge as a band, the text in `font()`'s face at the scaled size with the title bold, the disc centred on `letter.disc` as a `WAX_M` circle to `WAX_EDGE`·r, the rim ring from `(FIELD_EDGE − RIM_WIDTH / r0)`·r to `FIELD_EDGE`·r in the angle mix of S2, `FIELD` inside, then the § as `LILY_SHADOW` polygons shifted 0.7 cell up-left and `LILY_LIGHT` polygons over them (painter's order gives shadow = shifted ∧ ¬mark), even-odd, in the same `FIT_SCALE` and `FIT_OFFSET`. `paint` and `size` are removed; `rgb`, `font`, `FACES` stay; Pillow is imported inside the drawing function alone <!-- NAME NOT IN TREE --> | New pixel case: the disc's centre pixel is exactly `FIELD`; the pixel at 0.81·r on the equator is exactly `WAX_M`; the pixel at the rim's middle radius at 225° is within 1 unit per channel of `RIM_LIGHT` and at 45° of `RIM_DARK`; a pixel inside the sheet away from everything is exactly `PARCHMENT`'s triple; a pixel outside both sheet and disc has alpha 0; across the equator from parchment into wax at least one pixel is **neither** colour (antialiased, the staircase is gone); `image.size` is `DENSITY` × the cell metrics; every title glyph cell holds a pixel of exactly `TITLE`'s triple. `test_the_seal_module_imports_without_pillow` keeps its shape with the new names <!-- NAME NOT IN TREE --> |
| S6 · the two forms agree | Given the same letter at `DEFAULT_SCALE`, when the terminal's `build` says a cell is exactly `FIELD` with all eight neighbours exactly `FIELD`, then the PNG's pixel at that cell's centre is exactly `FIELD`; where a cell is exactly `LILY_LIGHT`, the pixel at its centre is nearer `LILY_LIGHT` than `FIELD` in linear light; where a cell is exactly `FIELD`, nearer `FIELD` than `LILY_LIGHT` | The pixel case above walks `letter.disc`'s cells against `build`'s `px`; the case asserts the interior-field set is non-empty and the two nearer-than sets each hold at least 50 cells |
| S7 · the note shows it at display size | Given the PNG at 2× and the published note, when `sealed_glance` writes the block, then the image line is `<img src="<url>" alt="<alt>" width="<display width>">` — `width` the PNG's width over `DENSITY` — and the counts line follows as today; `alt_text` is unchanged | `tests/test_a_release_publishes_its_note.py`, the `sealed_glance` case amended; a measurement that GitHub's sanitiser keeps `width` on `<img>` is Q4 |
| S8 · the documents and pins follow (§12's class) | Every place that describes the chart, the lily, the centre-sampled three-colour mark, the three-rung ladder or the 20-line disc says what the code now does: `seal_stamp.py`'s module docstring (*samples it at each cell's centre*) and the comments over `EMBLEM_D` (the INTERIM paragraph), the colours (*in one colour, lit … its face*), `KEY` (`G Y y`), `SCALE_FLOOR` (the lily's floor, now also the owner's 20-cell reading), `DEFAULT_SCALE` (*20 lines against the panel's 16*, *17 lines*; its *0.75 was the other candidate … passed over* sentence stays, pinned), `SCALE_LADDER` (*the rungs a block steps down*), the radius constant; `admitted`'s docstring (*each at 0.75*, *does not fit at 0.75*); `docs/the-broad-gate.md`'s #717 paragraph (*then 0.90, 0.80 and 0.75*, *at 0.75 by itself*); `docs/branch-and-release.md`'s bullet; `release_seal.py`'s docstring; `run_tests.py`'s docstring sentence *pins that drawing against the terminal form* | `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`, `test_the_policy_states_the_budget_and_names_its_case`, `test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it`, `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it` green; `grep -n "stitch\|29x32\|29×32\|INTERIM\|interim ring\|0\.80 and 0\.75\|cell's centre\|LILY_FACE" skills/verify/scripts/seal_stamp.py .github/scripts/release_seal.py docs/*.md` returns only history (round records, changelogs, ledger rows) |
| S9 · failure still costs the image alone | Given an emblem that will not parse, a face that will not load, or Pillow missing, when `seal_release` runs, then the log says why on one `::warning::` line, exit 0, nothing uploaded or edited | `test_any_failure_leaves_the_note_as_it_was_published` with `draw` as the broken unit |

## Data & interfaces

- **The palette** (truecolour triples; the first four are #717's, the
  rim's two the owner's of 2026-10-06): `WAX_M` (168, 26, 30), `FIELD`
  (120, 16, 20), `LILY_LIGHT` (226, 82, 74) — the mark, `LILY_SHADOW`
  (96, 10, 14) — its shadow, `RIM_LIGHT` (214, 70, 66), `RIM_DARK` <!-- NAME NOT IN TREE -->
  (104, 12, 16). `DISC_COLOURS` is these six; `LILY_FACE` is gone. <!-- NAME NOT IN TREE -->
- **The disc's numbers**: `WAX_EDGE` 0.84 and `FIELD_EDGE` 0.78 of the
  radius as today; `DISC_CELLS = 24`, the diameter at the wax edge in cells <!-- NAME NOT IN TREE -->
  at `DEFAULT_SCALE`; `RIM_WIDTH = 1.15` cells, the lit ring inside the <!-- NAME NOT IN TREE -->
  field's edge; `SHADOW_OFFSET = 0.7` cells, up-left; `FIT_OFFSET = (0, 0.375)` <!-- NAME NOT IN TREE -->
  cells and `FIT_SCALE = 1.04`, the grid fit the orchestrator searched over <!-- NAME NOT IN TREE -->
  offsets in eighths of a cell and scales 0.96 / 1.0 / 1.04 at 24 cells,
  maximising how many field cells read clearly mark or clearly field;
  `SAMPLES = 6` per side. All in cell units at the terminal's grid, where a
  cell is one column by one half-row; the PNG multiplies by its cell size.
- **A point's colour** (the layer rule S2 and S5 both apply), for a point
  at `(dx, dy)` cells from the disc's centre, `r = hypot(dx, dy) / r0`,
  `θ = atan2(dy, dx)` with `y` down:
  - `r > WAX_EDGE`: `under` (the colour beneath, or dropped where `under`
    is `None`);
  - `FIELD_EDGE < r ≤ WAX_EDGE`: `WAX_M`;
  - `FIELD_EDGE − RIM_WIDTH / r0 < r ≤ FIELD_EDGE`: the sRGB mix of
    `RIM_DARK` toward `RIM_LIGHT` by `smoothstep((1 + cos(θ − 225°)) / 2)`, <!-- NAME NOT IN TREE -->
    so the ring is lightest at the upper left and darkest at the lower
    right, with no seam;
  - else, with `(u, v) = ((dx − FIT_OFFSET.x) / (field · FIT_SCALE), (dy −
    FIT_OFFSET.y) / (field · FIT_SCALE))` and `field = FIELD_EDGE · r0`:
    `LILY_LIGHT` where `inside(u, v)`; `LILY_SHADOW` where not, and
    `inside(u − δ, v − δ)` with `δ = SHADOW_OFFSET / (field · FIT_SCALE)`;
    `FIELD` otherwise. `shade(filled, u, v, δ)` is this last rule, kept
    under its name with two answers instead of three.
  `smoothstep(t) = 3t² − 2t³` on `t` clamped to [0, 1]. Linear light is
  `(c / 255)^2.2` per channel and back with the inverse, rounded.
- `seal_stamp.build(scale, disc_cells=DISC_CELLS) -> (w, h, px)`, `px(x, y, <!-- NAME NOT IN TREE -->
  under=None)`, as S2. The 36 points of a cell are sampled once per cell
  and shared between the two `under` answers, or the module keeps a faster
  equivalent (`plan.md` §*Technical context*, the hook's draw time) that
  `test_a_cell_is_the_mean_of_its_samples_in_linear_light` holds to the <!-- NAME NOT IN TREE -->
  point rule.
- `seal_stamp.Letter(cells, width, height, disc)`; `disc` is
  `(left, top, w, h)` or `None`.
- `seal_stamp.KEY`: six letters over the six palette colours (S3a);
  `seal_stamp.nearest(colour) -> palette colour | None` in linear light, <!-- NAME NOT IN TREE -->
  `None` where the parchment's triple is nearer than every palette member.
- `seal_stamp.SCALE_LADDER = (0.90,)`; `admitted` as today over it.
- `release_seal.DENSITY = 2`, `SUPERSAMPLE = 4`, `draw(letter) -> PIL.Image`,
  `png(image, path) -> font name`; `sealed_glance(image_url, alt, width, …)`
  gains the display width.
- Ledger fragment `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`:
  new rows for S1–S8 and the citing rows that correct 0.10.0 S2, 0.17.0 L1
  and L2, 0.18.0 R1 and R2, written with `evidence-check --reverify --into
  … --checked <date>` where a hash moved and by hand where a claim is false.
- **`EMBLEM_D`**, the owner's choice, verbatim. The outline of Georgia Bold's
  § scaled to 820 units tall in the 1000 × 1000 frame, centred on
  (500, 500); two subpaths, the outline and its counter; its farthest point
  from the centre at radius about 417. The string the orchestrator handed
  over is the one below, and the build copies it character for character:

```
M 721.8 484.0 Q 721.8 535.5 687.5 572.0 Q 653.2 608.5 595.8 627.4 Q 645.4 647.9 670.7 681.9 Q 696.0 715.9 696.0 756.8 Q 696.0 822.5 635.0 866.2 Q 573.9 910.0 467.9 910.0 Q 417.3 910.0 383.8 900.5 Q 350.2 891.0 329.8 876.4 Q 309.3 861.9 300.8 844.6 Q 292.3 827.3 292.3 812.2 Q 292.3 785.5 308.1 768.2 Q 323.9 751.0 354.1 751.0 Q 375.5 751.0 391.1 762.1 Q 406.6 773.3 417.3 791.3 Q 427.5 808.4 434.6 827.6 Q 441.6 846.8 449.4 868.7 Q 451.9 869.1 456.2 869.6 Q 460.6 870.1 463.0 870.1 Q 508.8 870.1 538.7 852.6 Q 568.6 835.1 568.6 796.2 Q 568.6 772.8 558.8 756.8 Q 549.1 740.7 530.2 728.1 Q 511.7 715.0 481.0 702.1 Q 450.4 689.2 420.2 677.0 Q 346.8 647.4 312.5 609.7 Q 278.2 572.0 278.2 516.0 Q 278.2 468.4 305.9 433.4 Q 333.7 398.4 404.2 372.6 Q 349.7 350.2 324.9 315.9 Q 300.1 281.6 300.1 238.3 Q 300.1 174.6 363.3 132.3 Q 426.6 90.0 527.2 90.0 Q 575.4 90.0 609.9 99.2 Q 644.4 108.5 665.4 123.6 Q 685.3 137.7 694.1 154.9 Q 702.8 172.2 702.8 187.8 Q 702.8 213.5 688.0 231.3 Q 673.1 249.0 641.0 249.0 Q 618.7 249.0 603.8 237.9 Q 589.0 226.7 577.8 208.7 Q 568.6 194.1 560.1 170.5 Q 551.6 146.9 545.7 131.3 Q 542.3 130.4 538.4 130.1 Q 534.5 129.9 532.1 129.9 Q 486.4 129.9 457.0 148.1 Q 427.5 166.4 427.5 203.8 Q 427.5 228.1 437.5 243.7 Q 447.5 259.3 467.9 272.4 Q 488.3 285.5 518.0 297.7 Q 547.7 309.8 579.8 323.0 Q 652.7 352.1 687.2 389.1 Q 721.8 426.1 721.8 484.0 Z M 597.8 516.5 Q 597.8 491.2 586.6 473.5 Q 575.4 455.7 554.5 441.6 Q 535.5 428.5 501.7 413.9 Q 467.9 399.3 443.6 388.6 Q 425.6 404.2 413.9 431.7 Q 402.2 459.1 402.2 483.5 Q 402.2 509.2 414.4 527.5 Q 426.6 545.7 447.0 559.3 Q 469.4 573.9 498.3 586.3 Q 527.2 598.7 556.4 611.4 Q 580.2 590.5 589.0 566.6 Q 597.8 542.8 597.8 516.5 Z
```

## Open questions → questions.md

Q1 (the emblem, its rendering, its size and its placement) is answered by
the owner, 2026-10-06, and is written in above. Q2 is a person's but blocks
nothing. Q3, Q4, Q6 are measurements, two of them re-opened by the answer;
Q5 and Q7 are the work's.

Framed 2026-10-06 by framer, before the build.
