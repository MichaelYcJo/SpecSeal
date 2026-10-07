# Implementation Plan: the terminal seal is a hand-drawn chart on a computed disc, and the release PNG is the owner's SVG (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.
Approved 2026-10-07 by the orchestrating session under the owner's `automation` answer and their seal decision of that day, when `smith` was spawned for the reframe.

## Summary

The terminal stamp's disc is 14 cells across and 7 lines, computed from
`DISC_CELLS` so it is symmetric and reproducible, and every cell is exactly
one of four colours: the ring, the field, the mark, the mark's one-cell
shadow. The mark is the owner's hand-drawn 7 × 10 chart of the §, placed by
two computed offsets. The sheet keeps its height, widens to the right until
no cell of the circle stands on a character and then three columns more,
and the disc sits inside it against the right edge, its last line on the
sheet's second-to-last. The twin keeps four letters. The hook's ladder keeps
its one rung, and because a stamp is about 2,900 UTF-16 units now rather
than 7,180, several stamps share a message again. The release PNG is the
owner's own 32 × 32 SVG — radial-gradient wax, a rim, a pressed groove, a
Georgia Bold § with a shadow and a highlight — copied into the tree with its
text turned to paths and rasterised by `rsvg-convert` at 2× in the `seal`
job; the note shows it at display width.

This frame was drawn by `framer` on Fable 5.1 (fce42e0d), revised on
2026-10-06 to fold in the owner's answer to Q1 (b7a13d47), and **reframed on
2026-10-07** by `framer` on Fable 5.1 after the owner compared renders in
their own terminal and rejected the 24-cell area-averaged § for the
terminal. No review round has begun, so the `Reframed` line under the
`Framed` mark names the owner's look rather than a round. Phases 1 and 2
keep their commits; phases 3–6 below are the redrawn ones, and §*What of
phases 1–2 stands, and what phase 3 retires* says which of their cases the
smith re-aims rather than discovers.

**On wall time.** Phase 3 is mostly deletion and re-aiming: the sampler and
its constants go, `build` becomes about thirty lines, `compose` changes its
layout rule, and about fifteen cases move. Phase 5 is a new short script
path and a one-time text-to-path conversion. A reasonable expectation for
phases 3, 5 and 6 together is **two to three hours of smith wall time**;
phase 4 is the owner's and takes what it takes.

## Technical context

**What the code does at e90dbaed** (phase 2 closed, `origin/release/v0.20.0`
merged, read 2026-10-07).

- `skills/verify/scripts/seal_stamp.py` (1,337 lines, stdlib-only, loaded
  by path from `broad_gate.py#STAMP`, `hooks/sealer-stamp.py`,
  `bin/seal-stamp` and `release_seal.py#stamp()`):
  - the § as `EMBLEM_D`, parsed by `svg_path`, flattened by `flatten`, <!-- NAME NOT IN TREE -->
    tested by `inside`/`crossings`, shaded by `shade`; `build(scale,
    disc_cells=DISC_CELLS)` samples 6 × 6 points per cell in linear light
    with the rim's angular mix, the 0.7-cell shadow, the grid fit and the
    smoothstep tightening; `(w, h) = (26, 26)` at 0.90.
  - `compose(rows, scale)` → `Letter(cells, width, height, disc)`: the #717
    corner — `disc_top = height − disc_lines // 2 − 1`, `left` slid right
    until no text cell is covered and `GAP` (2) clear parchment cells hold on
    every line, `width = max(TEXT_LEFT + longest + 2, left + dw // 2)`, so
    the disc hangs below and right of the sheet, its edge blended into the
    parchment where the sheet is beneath (`under`, `cube`).
  - `letter_row` takes the nearest palette colour (`nearest`) for a blended
    cell; `KEY` has six letters.
  - `SCALE_LADDER = (0.90,)`, `admitted`, `fitted`, the budget constants,
    the band and `check_scale`; `main` with `--shape`, `--scale`, `--from`.
- `.github/scripts/release_seal.py` (610 lines): `paint(letter)` → one
  rectangle per half-cell at 14 × 28 px, `png` with Pillow imported inside,
  `font`/`FACES`, `rgb`; `seal_release` composes at `DEFAULT_SCALE` and
  writes `ASSET` `seal.png`; `release_rows`, `alt_text`, `suite_counts`,
  `chain_counts`, `readers` do not touch `stamp()`.
- `.github/scripts/publish_release_note.py#sealed_glance` writes
  `![alt](url)`.
- `.github/workflows/publish-release.yml`'s `seal` job: checkout, Python
  3.12, `pip install … pillow==12.3.0 …`, the suite at the tag, then
  `python3 .github/scripts/release_seal.py`; every step `continue-on-error`.

**What the owner's reference is, and what the frame measured.** The owner
chose variant 2 of `~/Desktop/specseal-sheet-seal-right.ans` on their machine,
drawn by the orchestrating session's `sheet_mock.py` as `sheet(14, hand(14,
BOLD_10, PINK), grow="right", extra=3)` (`read`, 2026-10-07): a 16-line
sheet of 14 text lines, 54 columns wide, the disc's 14 columns ending one
column inside the right margin, its 7 lines ending on the last text line
with the blank line under it; eight truecolour triples in the file, four of
them the disc's. The mock colours its sheet in triples where the hook uses
256-colour codes, and its text differs from `full_values()`'s, so the case
cannot compare bytes with the file; it rebuilds the rule (`spec.md` S3).

The frame's probe (`executed`, 2026-10-07, one script in the scratchpad over
this tree's `compose(rows, None)`, `sheet_text` and `colour_row`, laying the
hand-drawn disc by the owner's rule; deleted after; units UTF-16, a
stand-in label of about the real length):

| Rows | Bare sheet | With the 14-cell disc | One stamp today (24-cell §) | One stamp, 14 cells | Two | Three |
|---|---|---|---|---|---|---|
| `FULL_ROWS` (`full_values()`) | 38 × 16 | 51 × 16, disc at column 36, top line 8 | 7,074 | **2,901** | 5,804 | 8,707 |
| `ROWS` | 35 × 14 | 51 × 14 | 6,886 | 2,703 | 5,408 | 8,111 |
| `SAMPLE_ROWS` | 36 × 14 | 52 × 14 | 6,846 | 2,717 | 5,436 | 8,153 |
| `SMALL_ROWS` (four rows) | 22 × 6 | 38 × **9** (the sheet grows: 6 lines hold no 7-line disc) | 6,046 | about 1,490 | about 2,982 | — |

So one real run is under a third of `MESSAGE_BUDGET` (9,000), two and three
share a message, four do not; `test_several_files_come_out_one_stop_each_oldest_first`'s <!-- NAME NOT IN TREE -->
premise (*two stamps never share a message*) is false again and the case
goes back to #717's shape. The `SMALL_ROWS` row is the frame's one finding
the owner's rule did not cover: a sheet shorter than the disc plus a line.
No gate writes one — a real run has twelve rows or more — but a case does,
so S3 says the sheet takes the lines the disc needs there, and only there.

**`rsvg-convert` and the fonts, checked 2026-10-07** (`read` from
`actions/runner-images`' `Ubuntu2404-Readme.md`, `executed` on this
machine): the runner image lists neither `librsvg2-bin`, nor cairo, nor
Inkscape, nor ImageMagick, nor any Microsoft font — only
`fonts-noto-color-emoji`. This machine has `rsvg-convert 2.58.4`
(`/opt/homebrew/bin`) and `Georgia Bold.ttf` under
`/System/Library/Fonts/Supplemental/`. `rsvg-convert -w 320 -h 320` drew the
owner's SVG here with exit 0. So on the runner the SVG's `font-family:
Georgia` would fall back to whatever serif the image has and the § would not
be the one the owner looked at — which is why the tree's copy carries the
glyph as paths, and why the job installs `librsvg2-bin` with `apt-get`
(ubuntu-latest has `sudo` and apt; the step is `continue-on-error` like
every other, and a missing binary is one `::warning::`). Phase 5 verifies
the install at the first tag that runs the job (Q10); until then the
install line is `read`.

- Tests that pin the current drawing and will move, by phase:
  phase 3 — in `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `test_the_emblem_is_lit_from_the_upper_left`,
  `test_the_disc_is_twenty_four_cells_across_at_the_default_rung`, <!-- NAME NOT IN TREE -->
  `test_the_emblem_is_the_owners_section_sign_inside_the_field`, <!-- NAME NOT IN TREE -->
  `test_the_emblem_fills_even_odd_from_an_svg_path`, <!-- NAME NOT IN TREE -->
  `test_shade_lights_the_mark_and_casts_its_shadow_down_right`, <!-- NAME NOT IN TREE -->
  `test_the_terminal_draws_the_area_the_emblem_encloses`, <!-- NAME NOT IN TREE -->
  `test_a_cell_is_the_mean_of_its_samples_in_linear_light`, <!-- NAME NOT IN TREE -->
  `test_the_mark_reads_at_the_default_rung_and_fragments_below_it`, <!-- NAME NOT IN TREE -->
  `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`,
  `test_the_twin_writes_the_discs_six_letters_over_the_sheets_frame`, <!-- NAME NOT IN TREE -->
  `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours`,
  `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`,
  `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`,
  `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence`;
  in `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`,
  `test_several_files_come_out_one_stop_each_oldest_first`, <!-- NAME NOT IN TREE -->
  `test_the_policy_states_the_budget_and_names_its_case`,
  `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it`;
  phase 5 — in `tests/test_the_release_seal_is_drawn.py`,
  `test_rgb_is_xterms_table_and_a_triple_passes_through`,
  `test_paint_lays_every_cell_in_the_colours_block_gives_it`,
  `test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`,
  `test_the_seal_module_imports_without_pillow`,
  `test_any_failure_leaves_the_note_as_it_was_published` (its cases),
  `test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it`;
  in `tests/test_a_release_publishes_its_note.py`, the `sealed_glance`
  case. Tests that must stay green unchanged:
  `test_the_disc_draws_the_same_bytes_in_every_process`,
  `test_the_disc_is_symmetric_because_it_is_computed`,
  `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`,
  `test_the_twin_and_the_block_form_have_equal_width_and_height`,
  `test_the_stamp_module_imports_with_pillow_blocked`,
  `test_not_sealed_carries_no_disc_and_names_every_failure`,
  `test_the_budget_is_named_and_derived_from_the_measured_limit`,
  `test_the_hooks_message_is_under_the_budget_for_one_file`,
  `test_two_files_in_one_turn_are_under_the_budget_together`,
  `test_seals_past_what_one_message_carries_wait_for_the_next_turn`,
  `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it`,
  `test_the_ladder_steps_down_in_order_and_ends_with_no_disc`,
  `test_a_character_outside_the_bmp_is_counted_as_two`,
  `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung`,
  `test_the_publishing_workflow_installs_the_pins_the_runner_holds`,
  `test_the_alt_text_is_one_sentence_carrying_every_value`.
  `tests/test_the_gate_names_every_step_ci_runs.py` reads `hygiene.yml`
  only, so a new step in the `seal` job is not a row of `PARTITION`.

**Constraints.**

1. `seal_stamp.py` stays stdlib-only and importable on Python 3.12 without
   Pillow.
2. No new Python package anywhere. `rsvg-convert` is a system package of the
   `seal` job alone, installed by a workflow step, and nothing under
   `hooks/`, `skills/` or `tests/` requires it: the one case that runs it
   skips where it is absent.
3. The hook's message stays under `MESSAGE_BUDGET` at 0.90 for a real run's
   values, with the one-rung ladder. Measured by phase 3, recorded in the
   fragment (Q3).
4. Any failure in the release path is a `::warning::` and exit 0.
5. New code in `release_seal.py` avoids `zip(..., strict=)` and `*.UTC`.
6. Every comment over the disc's colours and chart says whose mark
   (*the disc's mark*): phase 1 met the one-word check on a bare *the mark*.

**What breaks in six months.**

- Somebody edits `CHART` by hand: S1 compares the ten strings verbatim and
  S2 pins the five counts, so one changed character is red twice.
- A terminal with a different cell aspect: a half-block grid is 1:2 by
  construction and the chart was drawn on it; a terminal whose cells are not
  shows the § a little stretched, as every half-block drawing is.
- GitHub's sanitiser drops `width` on `<img>`: the image shows at 320 px
  (too large, not broken); Q4 measures it before the first tag.
- The runner image or apt changes `librsvg2-bin`'s availability: the seal
  is skipped with a `::warning::` naming the call, and `DRY_RUN=1` by hand
  from a machine that has it is the path the checklist already names.
- The harness moves `MESSAGE_LIMIT`: with stamps at about 2,900 units the
  hook has room to lose two thirds of its budget before a real run comes
  out as the sheet alone.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The § by area on a 24-cell disc** (decision 3, phase 2's stamp) | The owner compared renders in their own terminal on 2026-10-07 and rejected it for the terminal: mid tones and a soft edge on a half-block grid | rejected by the owner; the mechanism is retired, not kept beside |
| **Finishing passes with a highlight and mid tones on the hand chart** | Seen and rejected by the owner the same day | not taken; four colours, no blend |
| **A smaller hand chart (12 cells, `BOLD_8`) as a lower rung** | The owner chose 14 from the mock's set; nobody drew a chart the owner accepted at another size, and a stamp of 2,900 units needs no lower rung to fit | rejected; the ladder stays one rung <!-- NAME NOT IN TREE --> |
| **Scale the chart with `scale`** | A 7 × 10 chart has one size; nearest-neighbour scaling of it is the staircase the ticket opened on | rejected; `build(scale)` draws 14 cells at every scale in the band |
| **Retire `--scale` and the band now that the disc has one size** | Fifteen parametrised cases, `main`'s flag, the values files' `scale` field and `admitted`'s `min(scale, rung)` all read it; nothing the owner looks at changes | out of scope; a work item of its own if anyone wants it. Here the refusal sentences stop giving a disc size as their reason (§14) |
| **Keep `GAP` as *two clear parchment cells on every line*** | The owner's rule is global: widen past the first clash-free width by three columns. On the tightest line that is three cells; on others, more | rejected; `GAP = 3` with the owner's meaning |
| **Grow the sheet downward when the text is shorter than the disc** | That is the mock's `grow="down"`, which the owner did not pick; but a 6-line sheet cannot hold a 7-line disc at all | taken only where the sheet is shorter than the disc plus a line, which no gate writes (`SMALL_ROWS` is a fixture); a real run's sheet keeps its height |
| **Let the disc overhang the right edge a little** (the mock's variant 4) | The owner chose variant 2 | rejected |
| **Blend the circle's edge cell into the parchment** | The owner rejected mid tones; the hard edge is the reference's | rejected |
| **Keep `nearest` for the twin** | Every cell is one palette colour, so `nearest` has nothing to decide and its case cannot fail | retired; `letter_row` is a lookup |
| **Keep `LILY_LIGHT` / `LILY_SHADOW` as names** | The lily left two phases ago, the mark's triple changes, and the comment keeping the names said they were kept for readers that now go | renamed `MARK` / `MARK_SHADOW`; the fragment corrects the rows that cite the old names |
| **Draw the release PNG with Pillow from the terminal rule** (phase 3 as framed on 2026-10-06) | The owner offered their own SVG, and a Pillow rendering of the hand chart is the staircase again | not taken; the PNG is the SVG (Q9) |
| **Render the SVG with CairoSVG** | A pip package that needs the cairo shared library, and its text path goes through the same missing font | rejected; `rsvg-convert` is one apt package, draws gradients, gradient strokes and opacity in C, and the runner has apt |
| **Keep `<text>` in the SVG and install Georgia on the runner** | `ttf-mscorefonts-installer` needs a debconf EULA answer and downloads from SourceForge at install time | rejected; the glyph becomes paths once, on the owner's machine, and the runner looks up no font |
| **Keep `<text>` and accept the runner's fallback serif** | The § the owner looked at is Georgia Bold's; a fallback is a different mark | rejected |
| **Rasterise the SVG at display size, `![alt](url)`** | Blurry on a high-density screen, which the ticket names as a goal | rejected; 2× and `<img width>`, as the earlier frame decided |
| **Put the SVG under `assets/` or the repository root** | The release script is the one reader; a file beside it is found by `HERE` and nothing else has to know the path | rejected; `.github/scripts/release-seal.svg` |
| **Keep Pillow out of the suite now that the script does not import it** | The suite reads the PNG's pixels with it, and the pin case holds the install line | kept where it is (`spec.md` Out) |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The vector source and the terminal sampler.** `EMBLEM`, `svg_path`, `flatten`, `inside`, `shade` in `seal_stamp.py`; `build` samples them at cell centres; `ART`, `shrink` removed; `SCALE_REFUSED` / `SCALE_TOO_LARGE` reworded; the chart's registry entry gone | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -p no:xdist`; each new case shown red <!-- NAME NOT IN TREE --> | 88070eac |
| 2 | **The owner's § by area on a 24-cell disc.** `EMBLEM_D` the §, the six-colour palette, the area sampler, `compose` blending the edge and filling `Letter.disc`, `nearest`, `SCALE_LADDER = (0.90,)` with the policy paragraph; Q3 and Q6 measured | the same two files; the half-cells looked at as a picture; the sizes and the draw time in `phases/phase-2.md` | 108f549c |
| 3 | **The owner's terminal seal.** `DISC_CELLS = 14`, `DISC_LINES`, `EDGE_INSET`, `RING_INSET`, `CHART`, `MARK`, `MARK_SHADOW`, the four-colour `DISC_COLOURS` and `KEY`; `build(scale)` by the rule in `spec.md` §*Data & interfaces*, `(14, 14, px)` at every scale; `compose` by S3 (`GAP = 3`, the sheet keeping its height, the disc inside against the right edge, `Letter.disc` filled); `letter_row` a lookup; the refusal sentences, `DEFAULT_SCALE`'s, `SCALE_FLOOR`'s, `SCALE_LADDER`'s and `admitted`'s comments and the module docstring reworded (S8); `docs/the-broad-gate.md`'s #717 sentence amended in the same commit (§14); everything §*Scope › What phases 1–2 built that decision 4 retires* lists under `seal_stamp.py` deleted after a grep for each name. The cases in §*Technical context* re-aimed as §*What of phases 1–2 stands* says, each new or re-aimed case seen red; the hook's message re-measured over `FULL_ROWS`, `ROWS`, `SMALL_ROWS` and the widest panel and recorded for the fragment (Q3). **Last act:** the message `fitted` prints for one `full_values()` block written to `<scratchpad>/specseal-stamp-14.ans`, the path in the hand-back <!-- NAME NOT IN TREE --> | the same two test files with `-p no:xdist`, plus `tests/test_one_word_one_meaning.py`, `tests/test_every_reader_ends_a_line_where_gfm_does.py`, `tests/test_a_script_says_which_interpreter_it_needs.py`; `bin/seal-stamp --shape` read once; the sizes written in `phases/phase-3.md` | 35277597 |
| 4 | **The owner's look (the orchestrator's act, not a smith's).** The orchestrator copies phase 3's `.ans` to `~/Desktop/specseal-stamp-14.ans` and asks the owner to `! cat` it in their terminal; the owner's word — accepted, or what to change — is written into `questions.md` Q8 by the orchestrator. Accepted: phase 5 starts. Changed: the chart, a colour or the layout is the owner's new decision, folded into `spec.md` by the orchestrator (a value, not a reframe) and phase 3 is re-spawned against it | the owner's word in Q8's Status cell; the commit that records it closes this row | |
| 5 | **The release PNG is the owner's SVG.** `.github/scripts/release-seal.svg` — the owner's file with its three `<text>` layers as `<path>`s of Georgia Bold's §, converted once with `uvx --from fonttools` over `/System/Library/Fonts/Supplemental/Georgia Bold.ttf` and compared against the text version through `rsvg-convert` here before committing; `SVG`, `SEAL_PX`, `DENSITY`, `rasterise(svg, png)` in `release_seal.py`, `seal_release` wired to it, `stamp()`, `paint`, `size`, `png`, `font`, `FACES`, `rgb`, `CELL_W`, `CELL_H`, `FONT_SIZE`, `CUBE_LEVELS` removed, the module docstring rewritten; `sealed_glance` writes `<img … width>`; the `seal` job gains `sudo apt-get install -y --no-install-recommends librsvg2-bin` as a `continue-on-error` step with a comment saying why, before the draw; `docs/branch-and-release.md`'s bullet and `run_tests.py`'s sentence amended; the cases of S6, S7, S9 planted and the retired ones removed; Q4 measured with `gh api /markdown` | `bin/test tests/test_the_release_seal_is_drawn.py tests/test_a_release_publishes_its_note.py tests/test_the_gate_names_every_step_ci_runs.py -p no:xdist`; `DRY_RUN=1 SEAL_PNG=… python3 .github/scripts/release_seal.py` with a JUnit fixture, the PNG opened and looked at once; the text-vs-path comparison's result in `phases/phase-5.md` <!-- NAME NOT IN TREE --> | |
| 6 | **The records close.** `changelog.md`; the ledger fragment with S1–S9 rows and the citing corrections of 0.10.0 S2, 0.17.0 L1/L2, 0.18.0 R1/R2 and the re-reads `phases/phase-1.md` and `phases/phase-2.md` list, plus what phases 3 and 5 moved; `overview.md` closed, its divergence rows about `R0_CELLS`, the centroid rule, the area count and `Letter`'s paths brought up to date (those rules are gone); `handoff.md` retired or rewritten; `survivor-check --range a9d7b0e5...HEAD` at zero | `evidence-check --strict .` exits 0 — it reads this item's three frame files once the fragment exists, so a name only the build can write carries `NAME NOT IN TREE` on its line; `survivor-check` reports no place; the `grep` from S8 returns only history | |

### What of phases 1–2 stands, and what phase 3 retires

Phase 1 and phase 2 keep their commits because four things they built or
measured still hold, and the rest is what the owner looked at and rejected:

- **Stands.** The disc is computed and symmetric (`test_the_disc_is_symmetric_because_it_is_computed`,
  `test_the_disc_draws_the_same_bytes_in_every_process`); the sheet's four
  codes and `sheet_text`; `Letter`'s fourth field; `admitted`, `fitted`, the
  budget constants and the one-rung ladder with the one-per-`Stop` claim
  rule; the way the hook's message is measured (UTF-16 units through
  `stamp`, phase 2's table in `phases/phase-2.md` is the method phase 3
  repeats); `SCALE_REFUSED` and `SCALE_TOO_LARGE` as sentences a case pins,
  though their reason changes.
- **Retires.** The § path and everything that rendered it by area; the rim
  gradient; the blended edge and `cube`; the corner overhang and the
  per-line `GAP`; `nearest` and the six letters; the 24-cell footprint rule.

The smith re-aims each of these on purpose, in phase 3, rather than meeting
it red:

- **The footprint** `test_the_disc_is_twenty_four_cells_across_at_the_default_rung` <!-- NAME NOT IN TREE -->
  → `test_the_disc_is_fourteen_cells_of_exactly_four_colours` (S2), the
  five counts and `(14, 14)` at every scale.
- **The § cases** `test_the_emblem_is_the_owners_section_sign_inside_the_field`, <!-- NAME NOT IN TREE -->
  `test_the_emblem_fills_even_odd_from_an_svg_path`, <!-- NAME NOT IN TREE -->
  `test_a_cell_is_the_mean_of_its_samples_in_linear_light`, <!-- NAME NOT IN TREE -->
  `test_the_terminal_draws_the_area_the_emblem_encloses`, <!-- NAME NOT IN TREE -->
  `test_the_mark_reads_at_the_default_rung_and_fragments_below_it`, <!-- NAME NOT IN TREE -->
  `test_shade_lights_the_mark_and_casts_its_shadow_down_right` — retired <!-- NAME NOT IN TREE -->
  with the units they pinned; `test_the_mark_is_the_owners_hand_drawn_chart`
  (S1) takes their place.
- **The lighting case** `test_the_emblem_is_lit_from_the_upper_left` — the
  one-cell neighbour rule (S2a).
- **The corner case** `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text`
  → `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text`
  (S3), the layout rebuilt in the case and compared cell for cell.
- **The twin's six letters** and **the five colours on the wire** — four of
  each (S4, S4a); the sequence-per-row bound back to every row.
- **The budget pair** — `test_several_files_come_out_one_stop_each_oldest_first` <!-- NAME NOT IN TREE -->
  back to `test_several_files_come_out_as_one_message_oldest_first` with
  its premise (two fit) asserted; `test_two_files_in_one_turn_are_under_the_budget_together`
  derives its homes and stays green.
- **The sentence pins** — the docstring case, the policy case, the default
  scale case and the floor case, each to the new sentences, each seen red by
  the old sentence put back.

This table is also where the work records how far it got. **Status is
empty, or the commit that closed the phase.** Re-read the column after any
rebase.

## Operational impact

- **One release-only system dependency.** `librsvg2-bin` (`rsvg-convert`) is installed by a step of the `seal` job on `ubuntu-latest`; nothing under `hooks/` or `skills/` needs it, and the suite skips its one real-render case where it is absent. Pillow stays pinned where it is, read by the suite alone.
- **The hook's `Stop` message shrinks.** A real-run stamp is about 2,900 UTF-16 units at 0.90 (the frame's probe; phase 3 measures the built drawing), so several stamps share a message again and the ladder's step to the sheet alone is reached only by a panel wider than the tree can produce. `docs/the-broad-gate.md` says so.
- **The terminal stamp changes shape** for every installed session at the next plugin update: a 14-cell disc inside the sheet against its right edge, the sheet wider and no taller, four flat colours.
- **Release notes from 0.20.0 on** show the owner's seal as a 320-px PNG through `<img … width="160">`, transparent outside the circle. Earlier notes keep their cell-for-cell PNGs (Q2).
- **No migration, no env var, no compatibility break.** `DRY_RUN=1` and `SEAL_PNG` work as before where `rsvg-convert` is installed; a pending values file from an older gate draws at its own 0.90, which draws the same 14 cells as every scale in the band.
