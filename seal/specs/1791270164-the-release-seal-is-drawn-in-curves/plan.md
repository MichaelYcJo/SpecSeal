# Implementation Plan: the seal's emblem is one vector source, and both forms rasterise it (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

The emblem becomes one set of closed curves in `seal_stamp.py`, sampled at
cell centres for the terminal and filled by Pillow at a supersampled
resolution for the release PNG. `compose` lays the disc inside the sheet.
The PNG is drawn as an image — circle, curves, a real face, antialiased, at
2× — and the note shows it at display width. The emblem's shape is the
orchestrator's input and is not fixed here.

**On the 45 minutes the spawn prompt asked for: this cannot be built in
about 45 minutes of wall time, and the plan does not pretend to.** The
original ticket (one renderer, nothing in `seal_stamp.py` changing) might
have been. The owner's update of 2026-10-06 adds two things to the terminal
stamp — the chart's replacement by a vector source in a stdlib-only file,
and a new sheet layout that every existing stamp case pins — on top of the
image renderer. Four phases below; a reasonable expectation is **two to
three hours of smith wall time**, most of it in phases 1 and 2, where
roughly a dozen existing cases in two test files have to be re-read and some
rewritten, and the hook's message budget has to be re-measured. Phase 3 is
the part the ticket originally asked for and is the one that could fit the
45 minutes on its own.

## Technical context

**What the code does today** (read 2026-10-06 at `release/v0.20.0`).

- `skills/verify/scripts/seal_stamp.py` (1,069 lines, stdlib-only, loaded by
  path from `broad_gate.py#STAMP`, `hooks/sealer-stamp.py`, `bin/seal-stamp`
  and `release_seal.py#stamp()`):
  - `ART` (29 × 32 chart), `shrink(art, f)` (majority vote per output cell),
    `build(scale, margin=0.74)` — radius `r0 = reach / margin` where `reach`
    is the shrunk chart's farthest stitch from its centre; `w = int(2·r0) + 2`,
    `h` even; `px(x, y)` sampled at cell centres, `None` past `WAX_EDGE`
    (0.84), `WAX_M` from `FIELD_EDGE` (0.78), lily colours by the up-left /
    down-right neighbour rule, `FIELD` else.
  - `compose(rows, scale)` → `Letter(cells, width, height)`: the disc's
    centre line on the sheet's last line, its centre column at the sheet's
    right edge, half hanging below and over; `left` found by sliding right
    until no text cell is covered and `GAP` holds on every line.
  - `block`, `colour_row`, `letter_row`, `KEY` (`m . G Y y`), `admitted`,
    `fitted`, `SCALE_LADDER` (0.90, 0.80, 0.75), `MESSAGE_BUDGET` 9,000.
  - The footprints `build` gives today, derived from the chart's rounding:
    (43, 44) at 1.0, (39, 40) at 0.90, (35, 36) at 0.80, (33, 34) at 0.75
    (`reach` 15.5, 14, 12.5, 11.5 over 0.74). A constant
    `R0_CELLS = 15.5 / 0.74` with `r0 = R0_CELLS · scale` reproduces all four
    (20.95 → 43; 18.85 → 39; 16.76 → 35; 15.71 → 33). The smith verifies
    this by running `build` before the change and pinning the four pairs
    first (§15: the pin is red against nothing, so it is planted against
    today's code and must stay green after).
- `.github/scripts/release_seal.py` (610 lines): `paint(letter)` → one
  rectangle per half-cell at `CELL_W, CELL_H = 14, 28`, `png(ops, size,
  path)` with Pillow imported inside; `font(ImageFont)` chains DejaVu Sans
  Mono / Menlo / Consolas / Pillow's default at `FONT_SIZE` 22; `rgb`
  through xterm's cube; `seal_release` composes at `DEFAULT_SCALE` and
  writes `ASSET` `seal.png`. 0.19.0's PNG is 826 × 532 (measured from the
  downloaded asset).
- `.github/scripts/publish_release_note.py#sealed_glance` writes
  `![alt](url)` — a Markdown image carries no width, which is why S7 moves
  to `<img>`.
- Pillow 12.3.0 is the only non-stdlib package the renderer may use
  (`run_tests.py#PILLOW`, the workflow's install line,
  `test_the_publishing_workflow_installs_the_pins_the_runner_holds`). It
  fills polygons (`ImageDraw.polygon`), composites through `L` masks
  (`Image.paste(colour, mask=…)`, `ImageChops`), offsets (`ImageChops.offset`
  wraps; a paste at an offset does not), and resamples with
  `Image.Resampling.LANCZOS`. It has no Bézier primitive, which is why the
  source is flattened to chords before either rasteriser sees it.
- Tests that pin the current drawing and layout and will move:
  `tests/test_the_seal_is_taken_once_by_the_sealer.py` —
  `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`,
  `test_the_lily_is_lit_from_the_upper_left`,
  `test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame`,
  `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`,
  `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`;
  `tests/test_the_release_seal_is_drawn.py` —
  `test_paint_lays_every_cell_in_the_colours_block_gives_it`,
  `test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`
  (both parametrisations), `test_the_seal_module_imports_without_pillow`;
  `tests/test_a_release_publishes_its_note.py` — the `sealed_glance` case.
  Tests that must stay green unchanged: the budget cases A2–A4 in
  `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`,
  `test_the_disc_draws_the_same_bytes_in_every_process`,
  `test_the_disc_is_symmetric_because_it_is_computed`,
  `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`,
  `test_the_twin_and_the_block_form_have_equal_width_and_height`.

**Constraints the renderer must respect.**

1. `seal_stamp.py` stays stdlib-only and importable on Python 3.12 without
   Pillow: the point-in-polygon test and the flattening are pure Python.
2. No new package anywhere. Pillow stays pinned at 12.3.0, imported inside
   the drawing function, test-and-release only.
3. The terminal draw stays fast enough for a `Stop` hook that may draw
   several stamps: `inside` is asked ~1,500 times per disc (plus two shade
   probes each) against `flatten`'s chords. At `n = 16` chords per cubic and
   an emblem of a few dozen segments this is under a second in CPython; the
   smith measures it (Q6) and lowers `n` for the terminal or caches per
   scale if it is not.
4. The hook's message stays under `MESSAGE_BUDGET` at 0.90 for a real run's
   values (A3), and the ladder's behaviour is unchanged.
5. Any failure in the release path is a `::warning::` and exit 0.
6. New code in `release_seal.py` avoids `zip(..., strict=)` and `*.UTC`.

**What breaks in six months.**

- The orchestrator's emblem uses an SVG feature `svg_path` refuses (arcs,
  relative commands). It fails at the case with the command named, so the
  answer is converted, not the parser widened in a fix pass.
- A new emblem has a stroke thinner than a cell at 0.75, so the terminal
  loses it while the PNG keeps it. S2's area-fidelity case (85–115 %) is
  what says so at the case rather than on the owner's screen.
- Pillow changes `LANCZOS` or `load_default`. The pin holds the version.
- GitHub's sanitiser drops `width` on `<img>`. The image shows at 2× (too
  large, not broken), the alt text and the counts line still carry every
  number, and Q4 measures the sanitiser before the first tag.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Trace the #717 lily into curves** (decision 1) | Withdrawn by the owner 2026-10-06: it reads badly at 0.90 and means nothing about the project | not taken |
| **A standard fleur-de-lis** | Not the owner's mark either; the owner is choosing a mark that means SpecSeal | rejected |
| **Emblem as an SDF** (a signed-distance function of primitives) | Pillow cannot fill an SDF; the PNG would need a per-pixel Python loop at 4 × 2 × (40 cells × 14 px)² ≈ 20 M samples, which is minutes. Curves flatten to polygons Pillow fills in C, and the same polygons answer `inside` for the terminal's 1,500 samples. One source either way; curves are the one both rasterisers can take without a new dependency | **curves chosen** |
| **Emblem in a sibling module** `skills/verify/scripts/seal_emblem.py` | Four loaders (`broad_gate`, `sealer-stamp`, `bin/seal-stamp`, `release_seal`) reach `seal_stamp.py` by path; a sibling needs a second path in each, and the chart was already *the only copy* in this file | rejected; `seal_stamp.py` holds it |
| **Keep the chart for the terminal, curves for the PNG only** (the ticket's original shape) | Two sources drift, and the majority vote is exactly what the owner says mangles the mark at 0.90 | rejected by the owner's update |
| **Terminal rasterises by coverage** (n × n subsamples per cell, majority) | Reintroduces a vote; thin strokes are still lost or fattened by the vote's threshold, and it costs n² the samples | rejected; centre sampling plus the area-fidelity case and an authoring constraint on stroke width (Q1) |
| **Keep the disc on the corner** | The owner asked for the disc inside the sheet, both forms | rejected |
| **PNG by sampling `inside` per pixel** (one rasteriser literally) | The 20 M-sample loop above | rejected; Pillow fills the same polygons |
| **Draw the PNG at display size, no supersample** | Pillow's polygon and ellipse fills are not antialiased; the staircase returns at the curve's edge | rejected; 4× then `LANCZOS` |
| **Keep `![alt](url)` and write the PNG at display size** | Blurry on a high-density screen, which the ticket names as a goal | rejected; `<img width>` at 2× |
| **Read the disc's position off `compose`'s cells** (keep `Letter` three-field) | Works for the bounding box, but the radius has to be re-derived and a one-cell margin error moves the circle off the terminal's; `compose` already knows `left` and `disc_top` | rejected; `Letter.disc` added |
| **Transparent image with the disc hanging past the sheet** | The owner moved the disc inside; the image is the sheet, so no transparency is needed and none is pinned | superseded |
| **Hand-author the production emblem in this work item** | Not the smith's call; the owner is choosing from renderings now. A placeholder would be an answer nobody gave | the production `EMBLEM` is written from the orchestrator's answer (phase 4); until it lands the constant holds an openly labelled interim geometric ring and the hand-back says so |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The vector source and the terminal sampler.** `EMBLEM`, `svg_path`, `flatten`, `inside`, `shade` in `seal_stamp.py`; `build` samples them at cell centres with `R0_CELLS · scale`, footprints pinned to today's four; `ART`, `shrink` removed; `SCALE_REFUSED` / `SCALE_TOO_LARGE` reworded; `KEY` comment and module docstring follow. `EMBLEM` holds an interim ring labelled as such in a comment unless Q1's answer has arrived. The lily lighting case rewritten; a fixture-emblem case for even-odd, shading and `svg_path`'s refusals; the area-fidelity case; the four footprints pinned (planted green against today's `build` first, then kept) | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -p no:xdist`; each new case shown red by deleting the sentence it pins (hand-back says how); `seal-stamp` run on a terminal and its `--shape` twin compared by eye once | 88070eac |
| 2 | **The disc inside the sheet.** `compose` lays the disc within the edge, `GAP` on every line, sheet height `max(text, disc) + 2`, disc vertically centred; `Letter.disc`; the corner case replaced; the sheet cases re-read; `admitted`'s docstring sizes and the budget cases re-measured (Q3) | the same two test files; A3's printed sizes recorded for the ledger; a `seal-stamp` rendering at 0.90 and 0.75 looked at on a dark and a light background and said so in `phases/phase-2.md` | |
| 3 | **The release PNG drawn as an image.** `draw(letter)` with `DENSITY`, `SUPERSAMPLE`, circle, polygons through offset masks, real face, `LANCZOS`; `png(image, path)`; `paint`, `size` removed; `seal_release` wired; `sealed_glance` writes `<img … width>`; the pixel case replaced (S5, S6), the imports-without-Pillow case renamed, the broken-unit failure case points at `draw`; Q4 measured with `gh api /markdown` | `bin/test tests/test_the_release_seal_is_drawn.py tests/test_a_release_publishes_its_note.py -p no:xdist`; `DRY_RUN=1 SEAL_PNG=… python3 .github/scripts/release_seal.py` with a JUnit fixture, the PNG opened and looked at once | |
| 4 | **The emblem lands and the records close.** `EMBLEM` written from the orchestrator's answer through `svg_path` (if not already in phase 1); docs amended (`docs/the-broad-gate.md` #717 paragraph, `docs/branch-and-release.md` bullet, `run_tests.py` and `release_seal.py` docstrings); `changelog.md`; the ledger fragment with S1–S8 rows and the citing corrections of 0.10.0 S2, 0.17.0 L1/L2, 0.18.0 R1/R2; `overview.md` | the document cases named in S8; `grep` from S8 returns only history; `evidence-check` lenient over the fragment exits 0 | |

The emblem's arrival governs only the **look**: phases 1–3 build and verify
the mechanism against the fixture emblem and the interim constant, so the
smith does not wait on Q1 to start. If the answer arrives during phase 1, it
goes in there and phase 4 loses that row.

This table is also where the work records how far it got. **Status is
empty, or the commit that closed the phase.** Re-read the column after any
rebase.

## Operational impact

- **No new dependency.** Pillow 12.3.0 stays the one non-stdlib package, test-and-release only, pinned where it is. Nothing under `hooks/` or `skills/` imports it.
- **The hook's `Stop` message changes size.** The disc inside the sheet adds parchment cells; A3 measures the new sizes and the ladder absorbs an overflow by stepping down. The budget constants do not move.
- **The terminal stamp changes shape** for every installed session at the next plugin update: the disc inside the sheet, a new emblem. `docs/the-broad-gate.md` says so.
- **Release notes from 0.20.0 on** show `<img … width>` at 2× density. Earlier notes keep their cell-for-cell PNGs (Q2).
- **No migration, no env var, no compatibility break.** `DRY_RUN=1` and `SEAL_PNG` work as before.
