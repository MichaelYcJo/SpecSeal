# Feature Specification: the seal's emblem is one vector source, and both forms rasterise it (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Raised by the owner looking at the 0.18.3 release note: the seal image is
the terminal stamp blown up cell for cell, so every edge is a staircase and
the emblem is a block mosaic. The owner's decisions, in order:

1. (#832 comment, 2026-10-06) The lily traced from the #717 chart into
   curves. **Withdrawn the same day**, through the orchestrator: the lily
   reads badly at 0.90 and has no tie to the project.
2. (2026-10-06, through the orchestrator) **The emblem is reopened.** A mark
   that means SpecSeal is being chosen from candidate renderings, and the
   orchestrator supplies it. The emblem is **one vector source**, and the
   terminal block stamp and the release PNG both rasterise it at their own
   resolution. The disc sits **inside** the parchment sheet, like a seal
   pressed on paper, in **both forms**.

So this frame fixes the mechanism and treats the emblem as an input it does
not fix (`questions.md` Q1). The file names below are coordinates in the tree
as it stands at `release/v0.20.0`, read 2026-10-06.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Nothing here stops to ask mid-run. The one owner decision (the emblem) is an input the orchestrator supplies; every other judgment is made from the tree and written where a reviewer can open it |
| `CONTRIBUTING.md` §*Running the checks* (*the gates themselves are stdlib-only Python and import nothing the suite installs*; Pillow is *test-and-release-only*) | The vector source and the sampler that rasterises it for the terminal live in `skills/verify/scripts/seal_stamp.py` and are stdlib-only, because `broad_gate.py`, `hooks/sealer-stamp.py` and `bin/seal-stamp` load that file. Pillow is imported in `.github/scripts/release_seal.py` alone, inside the function that writes the PNG, as today. **No new dependency of any kind** — not an SVG library, not cairo, not matplotlib, not numpy. `questions.md` says why curves and not an SDF under this constraint |
| `docs/the-broad-gate.md` §*Where the stamp is drawn*, the #717 paragraph (`MESSAGE_LIMIT`, the ladder, *a seal keeps its disc*) | The hook's message stays under `MESSAGE_BUDGET` at the first rung the ladder allows. Moving the disc inside the sheet adds parchment cells, so the measured sizes in that paragraph and in 0.17.0's L1 row are re-measured, not assumed (S5, `questions.md` Q3) |
| `docs/branch-and-release.md` §*Every act the release performs once it reaches `main`*, the bullet *Then the release's seal is attached* (#718) | The seal is still a second act that never fails the release. The bullet's description of the drawing (*from the broad gate's letter*) is amended to say the image is drawn from the same rows and the same emblem, not rasterised from cells |
| `docs/release-checklist.md` §6, the box *A GitHub Release exists at `vX.Y.Z`* | `DRY_RUN=1 python3 .github/scripts/release_seal.py` keeps drawing one by hand; the box stays true and gains nothing but the new look |
| `.github/scripts/publish_release_note.py`, module docstring (*The summary adds no way to fail*) and `release_seal.py`'s (*Any failure leaves the note as it was published*) | A draw that raises, a font that will not load, an emblem that will not parse — each is one log line and one `::warning::` with exit 0 |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `CONTRIBUTING.md` (*Python 3.12 is the supported floor*) | New code in `release_seal.py` uses no `zip(..., strict=)` and no `*.UTC`, or carries the guard block. `seal_stamp.py` already carries `FLOOR` and `below_floor` |
| `CLAUDE.md` §*a change writes fragments, never the shared file*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* (`Ledger frozen from` is declared in `seal/config.md`) | Changelog in `seal/specs/1791270164-…/changelog.md`. New rows in `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`. Released rows this work makes false are **corrected by a citing row in the fragment**, never edited where they live: `seal/releases/0.10.0.md` S2 (*the disc is computed from the 29×32 chart*), `seal/releases/0.17.0.md` L1 (the corner layout and the 6,277 / 7,249 sizes) and L2 (`shrink(ART, scale)`), `seal/releases/0.18.0.md` R1 and R2 (`paint`, `size`, the cell-for-cell pixel pin) |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures keep `example/repo`, `example.com`, `/Users/x/` |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is *every place the chart or the corner layout is described or pinned*, enumerated in S8. Every changed line a person reads is pinned in the same commit. Every new case is seen red first and the hand-back says how |

## Scope

### In

1. **One vector source for the emblem**, held in `seal_stamp.py` where the
   chart was its only copy, replacing `ART` and `shrink`. The source is a set
   of closed paths in a fixed frame; the emblem itself is the orchestrator's
   input (Q1), and a case-only fixture emblem proves the mechanism until it
   lands.
2. **One sampler, two resolutions.** The terminal form samples the source at
   cell centres through a stdlib point-in-shape test; the release PNG fills
   the same flattened paths with Pillow at a supersampled resolution. The
   lighting rule (lit from the upper left) is one definition both apply.
3. **The disc inside the sheet, both forms.** `compose` lays the sheet so the
   disc stands wholly within its edge; the block form, the letter twin and
   the PNG all follow, because all three read `compose`.
4. **The release PNG drawn as an image**: a computed circle, the emblem as
   filled curves, the sheet's text set in a real monospace face, everything
   supersampled and downscaled with a filter, written at 2× the display size
   and shown through `<img … width="…">` at the display size.
5. **The pins that follow the change** and the documents that describe the
   drawing (S8).

### Out

- **Which mark is the emblem.** Open, owner's, supplied by the orchestrator
  (Q1). The frame fixes the frame it is authored in and the sampler it is
  drawn by, nothing about its shape.
- **Redrawing 0.18.0–0.19.0's release images.** Nothing in the tree can do
  it unattended: a redraw needs the suite's counts at that tag, which the
  `seal` job's run supplied once. `DRY_RUN=1` from a checkout at the tag is
  the by-hand path and stays as it is (Q2).
- **The rows, the colours, the ladder, the budget.** `release_rows`,
  `LABELS`, `DISC_COLOURS`, the four sheet codes, `SCALE_LADDER`,
  `MESSAGE_LIMIT`, `MESSAGE_RESERVE` are unchanged. The disc's five colours
  stay the owner's #717 triples; the mark is pressed into the wax in the
  one colour, lit from the upper left, as the lily was.
- **A fleur-de-lis**, standard or traced. Decision 1 above is withdrawn.
- **The `seal-stamp` command line**, `--scale`'s band and its refusals keep
  their shape; only the sentence that says *the chart is one cell per
  stitch* loses its reason and is reworded (S8).
- **Pillow's version**, `run_tests.py#PACKAGES`, the workflow's install
  line. Pinned where they are; the holding cases stay green untouched.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · one source | Given `seal_stamp.EMBLEM` is a tuple of closed paths, each a sequence of straight and cubic Bézier segments in a frame whose origin is the disc's centre and whose unit circle is the field's edge (`FIELD_EDGE` of the radius), filled even-odd. When `flatten(EMBLEM, n)` is asked, then it returns polygons; when `inside(x, y)` is asked, then it answers from those polygons with no third-party import. A path string in SVG `d` syntax (absolute `M L C Q Z`, in a 1000×1000 viewBox centred on 500,500 with the field's edge at radius 500) is parsed into that form by one function, so the orchestrator's answer is data | `tests/test_the_seal_is_taken_once_by_the_sealer.py`: a fixture emblem (a square with a square hole) is inside at its ring and outside at its hole and beyond; the SVG parser round-trips a hand-written `d`; `seal_stamp` imports with `PIL` blocked in `sys.modules` |
| S2 · the terminal samples it | Given a scale in the band, when `build(scale)` is asked, then it returns `(w, h, px)` with **the footprint each rung has today** — `(w, h)` = (43, 44) at 1.0, (39, 40) at 0.90, (35, 36) at 0.80, (33, 34) at 0.75 — and `px(x, y)` is `None` past `WAX_EDGE`, `WAX_M` from `FIELD_EDGE`, else the emblem's colour where `inside` says so at the cell's centre and `FIELD` where not. The emblem's colour is `LILY_LIGHT` where the point one cell up-left is outside the emblem, `LILY_SHADOW` where the point one cell down-right is outside (and up-left is not), `LILY_FACE` otherwise — `shade(inside, point, delta)`, with `delta` one cell. `ART` and `shrink` are gone | `test_the_disc_draws_the_same_bytes_in_every_process` and `test_the_disc_is_symmetric_because_it_is_computed` stay green; a new case pins the four footprints; `test_the_lily_is_lit_from_the_upper_left` is rewritten against `inside` and `shade` and keeps asserting all three colours appear; a case asserts the twin's emblem letters (`G Y y`) cover between 85 % and 115 % of the area `flatten` encloses, at every rung, so a thin stroke a cell centre misses is red (Q1's authoring constraint) |
| S3 · the disc inside the sheet | Given rows and a scale, when `compose(rows, scale)` is asked, then every disc cell lies strictly inside the sheet's edge cells on all four sides, with `GAP` (2) clear parchment cells after every text line's last character where the disc stands further along that line, the sheet one blank line taller than the taller of the text and the disc, and the disc vertically centred in the sheet (half-row rounding allowed). `Letter` gains a fourth field, `disc`: `(left, top, w, h)` in cells and half-rows, or `None` with no disc. The block form and the twin have one footprint at every rung and with no disc, and the twin's first and last lines are still `.---.` and `'---'` | `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text` is replaced by `test_the_disc_is_pressed_inside_the_sheet_two_clear_cells_from_the_text`; `test_the_twin_and_the_block_form_have_equal_width_and_height`, `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`, `test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame` re-read and kept or amended; `test_not_sealed_carries_no_disc_and_names_every_failure` green |
| S4 · the budget still holds | Given `full_values()` and the widest panel the cases build, when the hook draws through `dispatch.py stop`, then the message is under `MESSAGE_BUDGET` at the first rung `admitted` allows, the ladder steps as before, and the oversized record is still the sheet alone | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` A2–A4 cases green unchanged; the sizes they print at 0.90 are written into the ledger fragment's correction of 0.17.0 L1 (Q3) |
| S5 · the PNG is drawn, not rasterised from cells | Given `compose`'s letter, when `draw(letter)` is asked, then it returns an RGBA image whose display metrics are `CELL_W` × `CELL_H` per cell (14 × 28) and `FONT_SIZE` 22, drawn at `SUPERSAMPLE` (4) × `DENSITY` (2) and downscaled with `Image.Resampling.LANCZOS` to `DENSITY` × the display size: the sheet as one parchment rectangle with its edge as a band, the text in `font()`'s face at the scaled size with the title bold, the disc as two filled circles (`WAX_M` to `WAX_EDGE`·r, `FIELD` to `FIELD_EDGE`·r) centred on `letter.disc`, the emblem as `flatten`'s polygons filled through masks offset by one cell up-left and down-right so `shade`'s rule holds, in the same five triples. `paint` and `size` are removed; `rgb`, `font`, `FACES` stay; Pillow is imported inside the drawing function alone | New pixel case: the disc's centre pixel is exactly `FIELD`; the pixel at 0.81·r on the equator is exactly `WAX_M`; a pixel inside the sheet away from everything is exactly `PARCHMENT`'s triple; across the equator from parchment into wax at least one pixel is **neither** colour (antialiased, the staircase is gone); `image.size` is `DENSITY` × the cell metrics; every title glyph cell holds a pixel of exactly `TITLE`'s triple. `test_the_seal_module_imports_without_pillow` keeps its shape with the new names |
| S6 · the two forms agree | Given the same letter at `DEFAULT_SCALE`, when the terminal's `build` says a disc cell's centre is emblem face (all eight neighbours emblem too), then the PNG's pixel at that cell's centre is one of the three emblem triples exactly; where `build` says `FIELD` with all eight neighbours `FIELD`, the pixel is exactly `FIELD` | The pixel case above walks `letter.disc`'s cells against `build`'s `px` |
| S7 · the note shows it at display size | Given the PNG at 2× and the published note, when `sealed_glance` writes the block, then the image line is `<img src="<url>" alt="<alt>" width="<display width>">` — `width` the PNG's width over `DENSITY` — and the counts line follows as today; `alt_text` is unchanged | `tests/test_a_release_publishes_its_note.py`, the `sealed_glance` case amended; a measurement that GitHub's sanitiser keeps `width` on `<img>` is Q4 |
| S8 · the documents and pins follow (§12's class) | Every place that describes the chart, the lily or the corner layout says what the code now does: `seal_stamp.py`'s module docstring and the comments over `DISC_COLOURS`, `SCALE_FLOOR`, `DEFAULT_SCALE`; `SCALE_REFUSED` and `SCALE_TOO_LARGE`'s wording (no *stitch*, no *lily*); `release_seal.py`'s docstring; `run_tests.py`'s docstring sentence *pins that drawing against the terminal form*; `docs/the-broad-gate.md`'s #717 paragraph where it names the corner; `docs/branch-and-release.md`'s bullet; the twin's `KEY` comment (`G Y y` are the emblem's letters) | `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`, `test_the_policy_states_the_budget_and_names_its_case`, `test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it` green; `grep -n "stitch\|29x32\|29×32\|lower right corner\|hangs" skills/verify/scripts/seal_stamp.py .github/scripts/release_seal.py docs/*.md` returns only history (round records, changelogs, ledger rows) |
| S9 · failure still costs the image alone | Given an emblem that will not parse, a face that will not load, or Pillow missing, when `seal_release` runs, then the log says why on one `::warning::` line, exit 0, nothing uploaded or edited | `test_any_failure_leaves_the_note_as_it_was_published` with `draw` as the broken unit |

## Data & interfaces

- `seal_stamp.EMBLEM`: `tuple[tuple[Segment, ...], ...]` — a path is a tuple
  of segments, each `("L", x, y)` or `("C", x1, y1, x2, y2, x, y)` from the
  previous point, the path closed to its first point. Frame: origin at the
  disc's centre, the field's edge at radius 1.0, **the emblem within radius
  0.95** (the lily reached 0.74/0.78 ≈ 0.95 of the field). `y` grows
  downward, as cells do.
- `seal_stamp.svg_path(d: str) -> path` parses absolute `M L C Q Z` in the
  1000-unit viewBox described in S1 (a `Q` is raised to a `C`). Relative
  commands, arcs and `H`/`V` are refused with a sentence naming the command,
  so an answer that uses them fails at the case, not at the tag.
- `seal_stamp.flatten(paths, n=16) -> list[list[(x, y)]]`: each cubic as
  `n` chords; `seal_stamp.inside(polygons, x, y) -> bool` even-odd.
- `seal_stamp.shade(inside, x, y, delta) -> colour | None`: `None` outside,
  else `LILY_LIGHT` / `LILY_SHADOW` / `LILY_FACE` by the rule in S2.
- `seal_stamp.build(scale) -> (w, h, px)` as today; the radius in cells is a
  named constant times `scale`, chosen so the four footprints in S2 hold.
- `seal_stamp.Letter(cells, width, height, disc)`; `disc` is
  `(left, top, w, h)` or `None`.
- `release_seal.DENSITY = 2`, `SUPERSAMPLE = 4`, `draw(letter) -> PIL.Image`,
  `png(image, path) -> font name`; `sealed_glance(image_url, alt, width, …)`
  gains the display width.
- Ledger fragment `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`:
  new rows for S1–S8 and the citing rows that correct 0.10.0 S2, 0.17.0 L1
  and L2, 0.18.0 R1 and R2, written with `evidence-check --reverify --into
  … --checked <date>` where a hash moved and by hand where a claim is false.

## Open questions → questions.md

Q1 (the emblem, the owner's, supplied by the orchestrator) is the one row a
person answers. Q2 is a person's but blocks nothing. Q3, Q4, Q6 are
measurements; Q5 is the work's.

Framed 2026-10-06 by framer, before the build.
