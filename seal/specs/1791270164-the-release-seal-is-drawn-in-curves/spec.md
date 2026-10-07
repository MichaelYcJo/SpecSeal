# Feature Specification: the terminal seal is a hand-drawn chart on a computed disc, and the release PNG is the owner's SVG (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Raised by the owner looking at the 0.18.3 release note: the seal image is
the terminal stamp blown up cell for cell, so every edge is a staircase and
the emblem is a block mosaic. The owner's decisions, in order:

1. (#832 comment, 2026-10-06) The lily traced from the #717 chart into
   curves. **Withdrawn the same day**, through the orchestrator: the lily
   reads badly at 0.90 and has no tie to the project.
2. (2026-10-06, through the orchestrator) **The emblem is reopened.** One
   vector source, rasterised by the terminal and by the release PNG at their
   own resolution. Phase 1 built that mechanism against an interim ring
   (closed at 88070eac).
3. (2026-10-06, the owner's answer to Q1) **The mark is §**, Georgia Bold's
   outline, rendered by area on a 24-cell disc pressed over the sheet's
   corner. Phase 2 built it (closed at 108f549c).
4. (2026-10-07, after comparing renders in their own terminal, every point
   decided) **The owner rejected the 24-cell area-averaged § for the
   terminal.** The terminal disc is **14 cells across, 7 lines**, computed,
   every cell exactly one colour; the mark is a **hand-drawn 7 × 10 chart**
   of the § with a one-cell shadow, **no highlight and no mid tones** (the
   owner saw finishing passes with both and rejected them); the **sheet
   keeps its height and widens to the right**, the disc on it, not over its
   corner; the **release PNG is drawn from the owner's own SVG**, a 32 × 32
   seal with gradients and Georgia Bold §, which the session proposed and
   nobody objected to.

So this frame fixes decision 4. Phases 1 and 2 keep their commits for what
still holds of them — the disc is computed and symmetric, the sheet's
colours, `admitted` with its budget and one-per-`Stop` rule, and the hook's
message measurement — and §*Scope* says what they built that this decision
retires. The file names below are coordinates in the tree as it stands at
e90dbaed (phase 2 closed, `origin/release/v0.20.0` merged), read 2026-10-07.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Nothing here stops to ask mid-run except the one stop the owner asked for: their look at the real stamp before the PNG phase (`plan.md` phase 4, `questions.md` Q8). Every other judgment is made from the tree and written where a reviewer can open it |
| `CONTRIBUTING.md` §*Running the checks* (*the gates themselves are stdlib-only Python and import nothing the suite installs*; Pillow is *test-and-release-only*) | `skills/verify/scripts/seal_stamp.py` stays stdlib-only, because `broad_gate.py`, `hooks/sealer-stamp.py` and `bin/seal-stamp` load it. The release PNG is rasterised by `rsvg-convert` (`librsvg2-bin`, a system package the `seal` job installs with `apt-get`), **a release-only dependency, never a plugin one**; `release_seal.py` imports no Pillow any more, and Pillow stays pinned where it is because the suite reads the PNG with it. No Python package is added anywhere |
| `docs/the-broad-gate.md` §*Where the stamp is drawn*, the #717 paragraph (`MESSAGE_LIMIT`, the ladder, *a seal keeps its disc*) | The hook's message stays under `MESSAGE_BUDGET`. The ladder keeps its one rung (S5): the disc has one size now, so there is nothing below 0.90 to step to, and the step after it is still the sheet alone. The paragraph's sentence *then 0.90, the one rung with a disc since #832 — the owner saw the § fragment on a disc smaller than 0.90's 24 cells* is amended in the commit that changes the drawing (§14), its `Enforced by:` line kept. The sizes are re-measured, not assumed (S5, Q3) |
| `docs/branch-and-release.md` §*Every act the release performs once it reaches `main`*, the bullet *Then the release's seal is attached* (#718) | The seal is still a second act that never fails the release. The bullet's *draws one seal for the release from the broad gate's letter* is amended to say the image is the owner's SVG rasterised, and the counts stay on the line under it |
| `docs/release-checklist.md` §6, the box *A GitHub Release exists at `vX.Y.Z`* | `DRY_RUN=1 python3 .github/scripts/release_seal.py` keeps drawing one by hand where `rsvg-convert` is installed; the box stays true and gains nothing but the new look |
| `.github/scripts/publish_release_note.py`, module docstring (*The summary adds no way to fail*) and `release_seal.py`'s (*Any failure leaves the note as it was published*) | A missing `rsvg-convert`, a nonzero exit from it, a missing or unreadable SVG — each is one log line and one `::warning::` with exit 0 (S9) |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `CONTRIBUTING.md` (*Python 3.12 is the supported floor*) | New code in `release_seal.py` uses no `zip(..., strict=)` and no `*.UTC`, or carries the guard block. `seal_stamp.py` already carries `FLOOR` and `below_floor` |
| `CLAUDE.md` §*a change writes fragments, never the shared file*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* (`Ledger frozen from` is declared in `seal/config.md`) | Changelog in `seal/specs/1791270164-…/changelog.md`. New rows in `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`. Released rows this work makes false are **corrected by a citing row in the fragment**, never edited where they live: `seal/releases/0.10.0.md` S2, `seal/releases/0.17.0.md` L1 and L2, `seal/releases/0.18.0.md` R1 and R2, and the re-reads `phases/phase-1.md` and `phases/phase-2.md` list (25 drifted, 5 broken at 108f549c) |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures keep `example/repo`, `example.com`, `/Users/x/` |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* and `tests/test_one_word_one_meaning.py` | Every comment over the disc's colours and chart says *the disc's mark* or *the seal's mark*, never a bare *the mark*: phase 1 met `test_no_instructing_document_leaves_an_instance_anonymous` on exactly that word |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is *every place the 24-cell disc, the area sampler, the § path, the rim gradient, the blended edge, the corner overhang, the six letters or the cell-for-cell PNG is described or pinned*, enumerated in S8. Every changed line a person reads is pinned in the same commit. Every new case is seen red first and the hand-back says how |

## Scope

### In

1. **The disc is 14 cells across, 7 lines, computed.** `DISC_CELLS = 14`; <!-- NAME NOT IN TREE -->
   `c = (n − 1) / 2`, `r = n / 2`; a cell at `(x, y)` with `d = hypot(x − c,
   y − c)` is **outside** if `d > r − EDGE_INSET` (0.2), the **ring** <!-- NAME NOT IN TREE -->
   `WAX_M` if `d > r − RING_INSET` (1.2), else in the **field**. Nothing is <!-- NAME NOT IN TREE -->
   area-averaged; every cell is exactly one of four triples.
2. **The mark is the hand-drawn chart**, `CHART`, the ten strings in <!-- NAME NOT IN TREE -->
   *Data & interfaces* verbatim, placed at row offset `(n − 10) // 2` (2)
   and column offset `(n − 7 + 1) // 2` (4). A field cell under an `M` is
   `MARK` (240, 130, 118); a field cell whose up-left neighbour `(x − 1, <!-- NAME NOT IN TREE -->
   y − 1)` is under an `M` is `MARK_SHADOW` (96, 10, 14); every other field <!-- NAME NOT IN TREE -->
   cell is `FIELD`. No highlight, no rim gradient, no mid tones.
3. **The sheet keeps its height and widens to the right.** One blank line
   under the text as today, no line added for the disc; the disc's last
   line is the sheet's second-to-last line and its last column is the
   column before the right edge; the sheet widens until no cell inside the
   circle stands on a character, then `GAP` (3) columns more, the disc
   moving with the right edge. A cell of the disc's square outside the
   circle is the sheet's own cell beneath it (parchment, or a character
   where one reaches under a corner). The reference is variant 2 of
   `/Users/michael/Desktop/specseal-sheet-seal-right.ans` (S3).
4. **The twin keeps its letters for the four colours**: `m` the ring, `.`
   the field, `Y` the mark, `y` its shadow (S4). Every cell is exactly one
   palette colour or the sheet's, so a letter is a lookup again.
5. **The release PNG is the owner's SVG rasterised.** The SVG is copied into
   the tree as `.github/scripts/release-seal.svg`, its three `<text>` layers
   converted once to `<path>` outlines of Georgia Bold's § so no font is
   looked up on the runner, and `rsvg-convert` draws it at `SEAL_PX` × <!-- NAME NOT IN TREE -->
   `DENSITY` pixels; the note shows it through `<img … width="<SEAL_PX>">` <!-- NAME NOT IN TREE -->
   (S6, S7).
6. **The hook's message re-measured at the new size** (Q3), and the two
   cases that pinned *two stamps never share a message* re-aimed to what
   `admitted` does again: several stamps per message, oldest first (S5).
7. **The pins that follow the change** and the documents that describe the
   drawing (S8), including the hook-policy sentence the one-size disc moves.

### Out

- **Redrawing 0.18.0–0.19.0's release images.** Nothing in the tree can do
  it unattended (Q2). `DRY_RUN=1` from a checkout at the tag is the by-hand
  path and stays.
- **The rows, the sheet's colours, the budget constants, the default, the
  band.** `release_rows`, `LABELS`, the four sheet codes (`PARCHMENT`,
  `SHEET_EDGE`, `INK`, `TITLE`), `MESSAGE_LIMIT`, `MESSAGE_RESERVE`,
  `MESSAGE_BUDGET`, `DEFAULT_SCALE` (0.90), `SCALE_FLOOR` (0.75),
  `SCALE_CEILING` (1.0), `SCALE_LADDER` (`(0.90,)`) are unchanged.
- **What `scale` does to the drawing: nothing, from now on.** A hand-drawn
  chart has one size, so `build(scale)` draws 14 cells at every scale in
  the band. `scale` stays what the values files carry and what `admitted`
  compares (`min(scale, rung)`), `check_scale` still refuses a file or a
  `--scale` outside the band, and the two refusal sentences are reworded
  so neither gives a disc size as its reason (§14). Retiring `--scale` and
  the band is a work item of its own (`plan.md` §Alternatives): fifteen
  parametrised cases and the files' schema, for a knob that stops nobody.
- **`Letter.disc`** stays, `(left, top, 14, 14)`: the layout case reads it
  (S3), and it costs nothing.
- **Pillow's version**, `run_tests.py#PACKAGES`, the `seal` job's `pip
  install` line. Pinned where they are; the suite reads the PNG with
  Pillow, and `test_the_publishing_workflow_installs_the_pins_the_runner_holds`
  stays green untouched.
- **A fleur-de-lis**, the **area-averaged §**, the **24-cell disc**, the
  **rim gradient**, the **blended edge**, the **corner overhang** and the
  **cell-for-cell PNG**: decisions 1–3 as the owner has now closed them.
- **The `seal-stamp` command line.** `--shape`, `--scale`, `--from` keep
  their shape; `--scale`'s help says the disc is one size.

### What phases 1–2 built that decision 4 retires

Where nothing else needs them (the smith greps before each delete; the
frame found no user outside `seal_stamp.py` on 2026-10-07):

- `EMBLEM_D`, `svg_path`, `SVG_REFUSED`, `SVG_TOKEN`, `SVG_ARITY`, <!-- NAME NOT IN TREE -->
  `flatten`, `inside`, `shade`, `EMBLEM`, `EMBLEM_POLYGONS`, `crossings`, <!-- NAME NOT IN TREE -->
  `smoothstep`, `GAMMA`, `linear`, `srgb`, `nearest`, `cube`, `CUBE_LEVELS`;
- `RIM_LIGHT`, `RIM_DARK`, `RIM_WIDTH`, `RIM_LIT_AT`, `FIT_OFFSET`, <!-- NAME NOT IN TREE -->
  `FIT_SCALE`, `SAMPLES`, `TIGHT_LOW`, `TIGHT_SPAN`, `SHADOW_OFFSET`, <!-- NAME NOT IN TREE -->
  `WAX_EDGE`, `FIELD_EDGE`, the 24-cell `DISC_CELLS`;
- `LILY_LIGHT` and `LILY_SHADOW` by name (the colours they held: the mark's
  triple changes, the shadow's does not);
- in `release_seal.py`: `stamp()`, `CELL_W`, `CELL_H`, `FONT_SIZE`,
  `CUBE_LEVELS`, `rgb`, `size`, `paint`, `FACES`, `font`, `png`;
- the cases named in S8 that pinned them.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the chart is the mark | Given `CHART` is the ten strings in *Data & interfaces*, when the module imports, then `CHART` has ten rows of seven characters over the alphabet `.M`, forty `M` cells, and `build` places it at row offset `(DISC_CELLS − 10) // 2` and column offset `(DISC_CELLS − 7 + 1) // 2` | `test_the_mark_is_the_owners_hand_drawn_chart`: the ten strings compared verbatim, the count 40, and `px` at every chart cell's position equals `MARK`; seen red by one character of the chart changed <!-- NAME NOT IN TREE --> |
| S2 · the disc is computed, every cell one colour | Given a scale in the band, when `build(scale)` is asked, then it returns `(14, 14, px)` at every scale, and `px(x, y)` is: `None` for the 48 cells outside, `WAX_M` for the 36 ring cells, `MARK` for the 40 mark cells, `MARK_SHADOW` for the 21 shadow cells, `FIELD` for the 51 field cells — by the rule in *Data & interfaces*, with no other value. Every row has a cell, and the widest row has 14 | `test_the_disc_is_fourteen_cells_of_exactly_four_colours`: the five counts, `set(px values) − {None} == set(DISC_COLOURS)`, and `(w, h) == (14, 14)` at 0.75, 0.90 and 1.0 (replacing `test_the_disc_is_twenty_four_cells_across_at_the_default_rung`); seen red by `RING_INSET = 1.0`. `test_the_disc_draws_the_same_bytes_in_every_process` and `test_the_disc_is_symmetric_because_it_is_computed` green unchanged <!-- NAME NOT IN TREE --> |
| S2a · lit from the upper left, by one cell | Given `build`, when the shadow cells are read, then each has a mark cell as its up-left neighbour, no shadow cell has a mark cell as its down-right neighbour unless that cell is also under the chart, and no ring cell is ever a shadow | `test_the_emblem_is_lit_from_the_upper_left` re-aimed to the neighbour rule; seen red by taking the shadow down-right (`on(x + 1, y + 1)`) |
| S3 · the sheet keeps its height and widens right | Given rows and a scale, when `compose(rows, scale)` is asked, then `height = max(lines + 2, DISC_LINES + 2)` where `DISC_LINES = 7` and `lines` is the text's line count (a real run's sheet keeps its height; a sheet shorter than the disc, which no gate writes, takes the lines the disc needs); the disc's grid is `Letter.disc = (width − 1 − 14, 2 · (height − 1 − 7), 14, 14)`, so its last line is the sheet's second-to-last and its last column is the column before the right edge; `width` is the first width from the bare sheet's (`TEXT_LEFT + longest + 2`) upward at which no cell inside the circle stands on a non-space character, plus `GAP` (3); a disc cell inside the circle is its `px` colour on both halves as the disc's row pair gives them; a cell of the square outside the circle, and every cell off the square, is the sheet's as today. Nothing stands below or right of the sheet | `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text` (replacing `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`): over `full_values()`'s rows from `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` (`FULL_ROWS`) and over `SAMPLE_ROWS`, the case rebuilds the owner's layout rule in its own body from `CHART` and the four triples, asserts every cell of `compose` equal to it, `height` equal to `compose(rows, None).height`, no circle cell on a character, every line the sheet's width (no cell past the edge, no line past `height`), and that with `GAP` set to 0 the width is exactly `GAP` smaller; with `SMALL_ROWS` (four rows) the height is 9 and the disc's top line is 1. `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it` green unchanged. Seen red by the disc placed one column left <!-- NAME NOT IN TREE --> |
| S4 · the twin's four letters | Given a cell, when `letter_row` writes it, then the letter is `KEY[top]`, else `KEY[bottom]`, else the sheet's own character, else a space — a lookup, since every disc cell is one palette colour | `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame` (renamed from *six*): `KEY` is exactly `{WAX_M: "m", FIELD: ".", MARK: "Y", MARK_SHADOW: "y"}`, and every twin character over a disc cell is its colour's letter; seen red by `KEY[MARK_SHADOW] = "Y"` <!-- NAME NOT IN TREE --> |
| S4a · the colours on the wire | Given the block form at 0.90, when its truecolour triples are read, then they are exactly the four of `DISC_COLOURS`, the sheet's four codes are as before, and nothing of the rope, the gold, the rim's two ends or the old mark colour (226, 82, 74) is left | `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours` re-aimed: the set of triples equals `set(DISC_COLOURS)` (four), the old exclusions kept and `(226, 82, 74)`, `(214, 70, 66)`, `(104, 12, 16)` added to them; the name still says five, because a released ledger row cites it. `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` back to its per-row bound: every row of the block form carries fewer sequences than cells |
| S5 · the budget at one rung, several stamps per message | Given `SCALE_LADDER` is `(0.90,)`, when `admitted` lays blocks, then it carries as many of the oldest as fit together with their disc, and one block alone that does not fit is the sheet with no disc — the rule as it stands. The frame's probe (`plan.md` §*Technical context*) puts one real run at about 2,900 units, so two and three real runs share a message again; phase 3 measures the built drawing and the fragment records it (Q3) | `test_several_files_come_out_one_stop_each_oldest_first` re-aimed back to #717's shape and name, `test_several_files_come_out_as_one_message_oldest_first`: two `SMALL_ROWS` blocks come out in one message, oldest first, each with its disc, the broken file left pending; its premise (the pair fits) asserted. `test_two_files_in_one_turn_are_under_the_budget_together` derives its homes as phase 1 left it and stays green. `test_the_hooks_message_is_under_the_budget_for_one_file`, `test_seals_past_what_one_message_carries_wait_for_the_next_turn`, `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it`, `test_the_ladder_steps_down_in_order_and_ends_with_no_disc`, `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` green. The sizes at 0.90 are written into the fragment's correction of 0.17.0 L1 <!-- NAME NOT IN TREE --> |
| S6 · the PNG is the SVG | Given `.github/scripts/release-seal.svg`, when `seal_release` runs, then `rasterise(svg, png)` runs `rsvg-convert -w <SEAL_PX·DENSITY> -h <SEAL_PX·DENSITY> <svg> -o <png>` through `subprocess.run` and the PNG is attached as `seal.png`; the SVG parses as XML with `viewBox="0 0 32 32"`, the radial gradient `sealBg` with its three stops, the linear gradient `rimShade`, the two circles, and three `<path>` elements carrying the fills and opacities the owner's three `<text>` layers had (`#380709` at 0.9, `#c42830`, `#e65a61` at 0.5) at their offsets — and **no `<text>` element**, so the runner looks up no font. Where `rsvg-convert` is on `PATH`, the PNG it writes is RGBA, `SEAL_PX·DENSITY` square, alpha 0 at its corners and 255 at its centre, a pixel within 8 per channel of `#c42830` somewhere in it, and the wax darker at the lower right than at the upper left | `test_the_release_seal_svg_is_the_owners_with_its_text_as_paths` (XML, no Pillow, no binary); `test_the_rasteriser_runs_rsvg_convert_at_two_times_the_display_size` (a fake `subprocess.run` pins the argv); `test_rsvg_convert_draws_the_seal_transparent_round_and_in_its_colours` (skips with the reason where `shutil.which("rsvg-convert")` is None; Pillow reads the pixels). `test_paint_lays_every_cell_in_the_colours_block_gives_it`, `test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`, `test_rgb_is_xterms_table_and_a_triple_passes_through`, `test_the_seal_module_imports_without_pillow` retired with the units they pinned <!-- NAME NOT IN TREE --> |
| S7 · the note shows it at display size | Given the PNG at `DENSITY` (2) × `SEAL_PX` (160) and the published note, when `sealed_glance` writes the block, then the image line is `<img src="<url>" alt="<alt>" width="160">` and the counts line follows as today; `alt_text` is unchanged | `tests/test_a_release_publishes_its_note.py`, the `sealed_glance` case amended; whether GitHub's sanitiser keeps `width` is Q4 <!-- NAME NOT IN TREE --> |
| S8 · the documents and pins follow (§12's class) | Every place that describes the 24-cell disc, the area sampler, the § path, the rim gradient, the blended edge, the corner overhang, the six letters or the cell-for-cell PNG says what the code now does: `seal_stamp.py`'s module docstring (*one vector source held below as data*, *renders it by area*, *`M n` the rim's*), the comments over the palette, `KEY`, `DISC_CELLS`, `GAP`, `DEFAULT_SCALE` (*24 cells across (`DISC_CELLS`), 13 lines*; its *0.75 was the other candidate … passed over* sentence stays, pinned), `SCALE_FLOOR` (*accepted nothing below 24*), `SCALE_LADDER` (*a disc smaller than 24 cells*), `SCALE_REFUSED` (*too few cells for its emblem*), `SCALE_TOO_LARGE`, `build`'s and `compose`'s and `admitted`'s docstrings; `docs/the-broad-gate.md`'s #717 paragraph; `docs/branch-and-release.md`'s bullet; `release_seal.py`'s docstring; `run_tests.py`'s sentence *pins that drawing against the terminal form*; `.github/workflows/publish-release.yml`'s comments over the `seal` job | `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`, `test_the_policy_states_the_budget_and_names_its_case`, `test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it`, `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it`, `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence` re-aimed to the new sentences and green; `grep -n "by area\|24 cells\|EMBLEM_D\|RIM_\|half on and half off\|hangs\|cell-for-cell\|LILY_" skills/verify/scripts/seal_stamp.py .github/scripts/release_seal.py .github/workflows/publish-release.yml docs/*.md` returns only history (round records, changelogs, ledger rows) |
| S9 · failure still costs the image alone | Given `rsvg-convert` missing from `PATH`, or exiting nonzero, or the SVG missing, when `seal_release` runs, then the log says why on one `::warning::` line, exit 0, nothing uploaded or edited | `test_any_failure_leaves_the_note_as_it_was_published` with three new cases (*rsvg-convert is not installed* → `FileNotFoundError`, *rsvg-convert fails* → returncode 1 with stderr in the reason, *the SVG is not there*) replacing *Pillow does not import*, *compose raises*, *compose exits* and *the PNG writer exits* |

## Data & interfaces

- **The palette** (truecolour triples): `WAX_M` (168, 26, 30) — the ring,
  `FIELD` (120, 16, 20), `MARK` (240, 130, 118) — the disc's mark, <!-- NAME NOT IN TREE -->
  `MARK_SHADOW` (96, 10, 14) — its shadow. `DISC_COLOURS` is these four. <!-- NAME NOT IN TREE -->
  The sheet's four 256-colour codes are unchanged.
- **The disc's numbers**: `DISC_CELLS = 14`; `DISC_LINES = DISC_CELLS // 2` <!-- NAME NOT IN TREE -->
  (7); `EDGE_INSET = 0.2` and `RING_INSET = 1.2`, in cells. The chart's <!-- NAME NOT IN TREE -->
  offsets are computed from `DISC_CELLS` and the chart's shape, not named.
- **A cell's colour**, for `(x, y)` in `0 ≤ x, y < 14`, `c = 6.5`, `r = 7`,
  `d = hypot(x − c, y − c)`, `on(x, y)` true where `CHART[y − 2][x − 4]`
  exists and is `M`:
  - `d > r − EDGE_INSET`: `None` (outside);
  - `d > r − RING_INSET`: `WAX_M`;
  - `on(x, y)`: `MARK`;
  - `on(x − 1, y − 1)`: `MARK_SHADOW`;
  - else `FIELD`.
  Counts over the 196 cells: 48 / 36 / 40 / 21 / 51 (measured by the
  framer, 2026-10-07, from the rule above; the reference file carries the
  same drawing).
- **`CHART`**, the owner's hand-drawn § for 14 cells, ten rows of seven: <!-- NAME NOT IN TREE -->

```
.MMMMM.
MM...MM
MM.....
.MMMMM.
MM...MM
MM...MM
.MMMMM.
.....MM
MM...MM
.MMMMM.
```

- `seal_stamp.build(scale) -> (w, h, px)`, `w = h = DISC_CELLS` at every
  scale in the band, `px(x, y)` the rule above; `check_scale` still refuses
  outside the band.
- `seal_stamp.compose(rows, scale) -> Letter(cells, width, height, disc)`,
  the layout rule of S3; `GAP = 3` with its comment rewritten: *columns the
  sheet is widened past the first width at which no cell inside the circle
  stands on a character; the disc moves with the right edge*.
- `seal_stamp.KEY`: the four letters of S4. `letter_row` is a lookup.
- `seal_stamp.SCALE_LADDER = (0.90,)`; `admitted` as today over it.
- `release_seal.SVG = os.path.join(HERE, "release-seal.svg")`, <!-- NAME NOT IN TREE -->
  `SEAL_PX = 160`, `DENSITY = 2`, `rasterise(svg, png) -> None` (raises <!-- NAME NOT IN TREE -->
  `Refused` naming the call where `rsvg-convert` is missing or fails);
  `sealed_glance(image_url, alt, width, …)` gains the display width.
- **The SVG in the tree**: the owner's file with each `<text>` replaced by a
  `<path d="…" fill="…" opacity="…">` of Georgia Bold's § at font-size 20,
  anchored at its middle on `x` and its baseline on `y` as the text was
  (`(16.5, 21.5)`, `(16, 21)`, `(15.7, 20.7)`). The outline is taken once
  from `/System/Library/Fonts/Supplemental/Georgia Bold.ttf` on the owner's
  machine with `fonttools` run through `uvx` (a tool used once, not a
  dependency), and the smith renders the text version and the path version
  with `rsvg-convert` here and compares them before committing the path
  version — the probe's result goes in `phases/phase-5.md`.
- Ledger fragment `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`:
  new rows for S1–S9 and the citing rows that correct 0.10.0 S2, 0.17.0 L1
  and L2, 0.18.0 R1 and R2, written with `evidence-check --reverify --into
  … --checked <date>` where a hash moved and by hand where a claim is false.

## Open questions → questions.md

Q1 and Q3 (as phase 2 measured it) and Q6 are history; Q5 and Q7 are moot
with the PNG drawn from the SVG. Q2 is a person's and blocks nothing. **Q8 is
the owner's look at the real 14-cell stamp, which blocks the PNG phase by
the owner's own instruction**; Q9 records the PNG default as the owner's
offer. Q3 is re-opened as a measurement, Q4 and Q10 are measurements, Q11 is
the work's.

Framed 2026-10-06 by framer, before the build.
Reframed 2026-10-07 by framer, after the owner's look at phase 2's stamp.
