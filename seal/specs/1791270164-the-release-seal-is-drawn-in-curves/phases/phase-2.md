# 1791270164-the-release-seal-is-drawn-in-curves — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 108f549c |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 2 row, after the framer folded the owner's answer to Q1 into the frame at `b7a13d47`: `EMBLEM_D` is the § from `spec.md` and the INTERIM paragraph goes; the palette gains `RIM_LIGHT` and `RIM_DARK` and loses `LILY_FACE`; `DISC_CELLS`, `RIM_WIDTH`, `SHADOW_OFFSET`, `FIT_OFFSET`, `FIT_SCALE`, `SAMPLES`; `build(scale, disc_cells=…)` by the footprint rule, with `px(x, y, under=None)` by area in linear light and the tightening; `shade` with two answers; `compose` passing `under` where the sheet is beneath, counting a touched cell for `GAP`, and filling `Letter.disc`; `nearest` and the six-letter `KEY`; `SCALE_LADDER = (0.90,)` with `admitted`'s docstring and `docs/the-broad-gate.md`'s #717 paragraph in the same commit. <!-- NAME NOT IN TREE -->

The spawn added: re-aim the phase-1 pins `plan.md` §*What phase 1 pinned that the answer moves* names rather than discover them, and see each new or re-aimed case red; record Q3 (the hook's message at 0.90) and Q6 (drawing time); report `bin/evidence-check --strict .`'s count rather than fix it, since that is phase 4's fragment; run the touched modules with seven named hygiene modules; render one real-size stamp at 0.90 in the block form into a file for the owner. Do not start phase 3.

## What this phase found

**The rendering matches the owner's reference cell for cell where the frame measured it.** At 0.90, `build` gives 77 cells exactly `LILY_LIGHT`, 3 exactly `LILY_SHADOW` and 139 exactly `FIELD`. The framer's probe over the owner's reference gave 77 / 3 / 139 (`plan.md` §*Technical context*). At 0.75 it is 46 `LILY_LIGHT`, so the reading the owner gave of the 20-cell disc holds in numbers too.

**Q6: no scanline fill was needed beyond reading each row's crossings once.** Asking `inside` per point over the § costs 33 µs a call against 1,026 edges, about 1.6 s per disc for its 48,000 field probes. `build` instead sorts each sample row's crossings once, through `crossings`, which repeats `inside`'s edge test and arithmetic, and reads a point's parity with `bisect`. Medians of five over `build`: 0.045 s at 1.0, 0.036 s at 0.90, 0.029 s at 0.80, 0.027 s at 0.75. A whole real-run stamp at 0.90 takes 0.044 s. `test_a_cell_is_the_mean_of_its_samples_in_linear_light` asks `inside` per point and asserts every cell equal, with nothing beneath and with the parchment beneath, at 0.90 and 0.75. <!-- NAME NOT IN TREE -->

**Q3: one real run fits with its disc at 0.90, and two never share a message.** Sizes are in UTF-16 units, label included, through `seal_stamp.stamp`:

| Panel | 0.90 | 0.80 | 0.75 | sheet alone |
|---|---|---|---|---|
| `full_values()`, a real run (`FULL_ROWS`) | 7,180 | 6,178 | 6,008 | 1,526 |
| the cases' `ROWS` | 6,903 | 5,923 | 5,735 | 1,223 |
| `SMALL_ROWS`, four lines | 6,063 | 5,092 | 4,891 | 481 |
| the widest panel the tree can produce | 7,885 | — | — | — |

The widest panel was read off `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` through a `test_tmp_` probe, since deleted. Everything fits `MESSAGE_BUDGET` (9,000) with its disc at 0.90. The margin for the widest panel is 1,115 units.

**`spec.md` S4 does not hold for one of its cases: no two stamps share a message any more.** The disc adds about 5,600 units to its sheet at 0.90, so even the four-line `SMALL_ROWS` pair is 12,128. The pair would still be 9,784 at 0.75, a rung the hook no longer draws. `test_several_files_come_out_as_one_message_oldest_first` could not keep deriving its premise, as the frame expected. It is renamed `test_several_files_come_out_one_stop_each_oldest_first` and pins what happens now: the first `Stop` draws the older alone, the newer and the broken file stay pending, and the next `Stop` draws the newer. It asserts that the pair is over the budget, so it says so if that ever changes. `admitted` still lays several blocks into one message at a budget a case picks, and the ladder case pins that. <!-- NAME NOT IN TREE -->

**`spec.md` S2a's centroid rule is false on the §.** It asks for the shadow's centroid below and right of the mark's. Measured over the cells wholly in the field, the shadow's centroid is right of the mark's at every scale, by about 2.2 cells. It is above it, by 1.0 to 1.9 cells, because the shadow falls mostly into the upper counter. This is the rule working on this shape, not a defect. The lighting case pins the rule itself, cell by cell. Each cell's shadow weight is paired with the mark weight of the cell one up-left of it, and separately with that of the cell one down-right. The first sum is 6.6–11.7 and the second 0.04–0.55. The case asserts the first is over four times the second. The rim's lightest cell is upper-left and its darkest lower-right, as S2a asks.

**`spec.md` S2b needs the rim kept out of the count.** The rim's light end is nearer `LILY_LIGHT` than `FIELD`, so counting every disc cell nearer the mark read the upper-left rim as mark. That gave 1.28 of the enclosed area. Over cells whose centre is inside the rim, the ratio is 1.014, 1.014, 0.935 and 0.991 at 1.0, 0.90, 0.80 and 0.75.

**`compose` asks `px` with the parchment beneath to decide `GAP`.** A cell the disc touches at all is then a blend different from the parchment, which is what *a touched cell counts* needs, and no second grid is computed. `px` returns `under` itself for a cell the disc does not reach, so the sheet keeps its 256-colour code there. Each cell's 36 points are classified once in `build`, and the two `under` answers are means over the same sums.

**The edge assertions hold as S3 wrote them.** At 0.90, 0.80 and 0.75, every rim half of the disc over the sheet is strictly between `WAX_M` and the parchment in every channel. Every one off the sheet is within the palette's range. `Letter.disc` bounds every triple, and the touched cells reach its inner border.

**Each new or re-aimed case was seen red** (§15), each by one `mutation-check` that came back `red`; the tree was clean after:

| Case | Break |
|---|---|
| `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` | `colour_row` writes the background on every cell |
| `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text` | nothing beneath a disc cell over the sheet (the edge goes hard); separately `Letter.disc`'s top in lines rather than half-rows |
| `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours` | `RIM_DARK` left out of `DISC_COLOURS` |
| `test_the_emblem_is_lit_from_the_upper_left` | `shade`'s shadow probe taken down-right; separately the rim lit from 45° |
| `test_the_disc_is_twenty_four_cells_across_at_the_default_rung` | `DISC_CELLS = 20` <!-- NAME NOT IN TREE --> |
| `test_the_emblem_is_the_owners_section_sign_inside_the_field` | one coordinate of `EMBLEM_D` changed <!-- NAME NOT IN TREE --> |
| `test_shade_lights_the_mark_and_casts_its_shadow_down_right` | `shade`'s shadow probe taken down-right <!-- NAME NOT IN TREE --> |
| `test_the_terminal_draws_the_area_the_emblem_encloses` | `FIT_SCALE = 1.3` <!-- NAME NOT IN TREE --> |
| `test_a_cell_is_the_mean_of_its_samples_in_linear_light` | three breaks, each red: `GAMMA = 2.0`; `crossings` unsorted; `TIGHT_LOW = 0.2` <!-- NAME NOT IN TREE --> |
| `test_the_mark_reads_at_the_default_rung_and_fragments_below_it` | the diameter left unscaled, so 0.75 draws 0.90's disc <!-- NAME NOT IN TREE --> |
| `test_the_twin_writes_the_discs_six_letters_over_the_sheets_frame` | `RIM_DARK`'s letter made `m`; separately `nearest` never answering the parchment <!-- NAME NOT IN TREE --> |
| `test_the_docstrings_describe_the_letter_and_the_rows_it_carries` (the #832 lines) | the rim's letters' sentence cut |
| `test_the_budget_is_named_and_derived_from_the_measured_limit`, `test_the_ladder_steps_down_in_order_and_ends_with_no_disc`, `test_a_character_outside_the_bmp_is_counted_as_two` | each red alone against the three-rung ladder put back |
| `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it` | the lone oversized block drawn at the last rung instead of as the sheet |
| `test_several_files_come_out_one_stop_each_oldest_first`, `test_two_files_in_one_turn_are_under_the_budget_together` | each red alone with `admitted`'s floor pass allowing twice the budget <!-- NAME NOT IN TREE --> |
| `test_the_policy_states_the_budget_and_names_its_case` (the #832 lines) | the policy paragraph's ladder sentence put back to *0.90, 0.80 and 0.75* |

**What was looked at.** A real-run stamp at 0.90, the label and the block form exactly as the hook prints it, is at `stamp-0.90.ans` in the orchestrating session's scratchpad (7,180 units; it equals `fitted`'s message). I drew its half-cells as a picture on a dark and on a light ground and looked at both once. The § reads as a § on both. The rim is light at the upper left and dark at the lower right. The disc's edge blends into the parchment where it lies on the sheet, and its edge off the sheet is hard on both grounds. The twin was printed at 0.90 and 0.75 and read. A terminal's own rendering of the block form was not seen by this phase; the owner's look at the file is the one that counts.

**Ledger consequences for phase 4.** `bin/evidence-check --strict .` exits 2 at `108f549c`: 6,379 ok, 25 drifted, 5 broken.
- **Broken (5):** `seal_stamp.py#shrink` (phase 1), `test_the_lily_is_lit_from_the_upper_left` (phase 1's rename), `test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame` (renamed to *six* here, as `spec.md` S3a asks), and `test_several_files_come_out_as_one_message_oldest_first`, cited twice, by 0.15.7 N7 and 0.17.0 B2 (renamed here).
- **Drifted (25):** `seal_stamp.py` `build`, `compose`, `letter_row`, `main`, `admitted`, `KEY`, `DISC_COLOURS`, `SCALE_LADDER`; `docs/the-broad-gate.md` §*Where the stamp is drawn*; `test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS`; and the re-aimed cases above.
- Each is phase 4's `Corrected ·` or re-read row in the fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The interim ring in `EMBLEM_D` and its INTERIM paragraph | none — the owner's § replaced it (`spec.md` decision 3) |
| `LILY_FACE` and the three-colour neighbour rule of `shade` | none — the owner's rendering has one mark colour and a shadow; `spec.md` S2 |
| `R0_CELLS` and `build`'s `r0_cells` keyword | `DISC_CELLS` and `build`'s `disc_cells`; phase 1's divergence rows in `overview.md` say so <!-- NAME NOT IN TREE --> |
| `SCALE_LADDER`'s 0.80 and 0.75 | none — the sheet alone is the step after 0.90; `docs/the-broad-gate.md`'s #717 paragraph |
| `test_each_rung_keeps_the_disc_height_the_chart_gave_it` | `test_the_disc_is_twenty_four_cells_across_at_the_default_rung`; no released row cites the old name <!-- NAME NOT IN TREE --> |
| `test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame`, by its name | `test_the_twin_writes_the_discs_six_letters_over_the_sheets_frame`; phase 4 corrects the released row that cites the old name <!-- NAME NOT IN TREE --> |
| `test_several_files_come_out_as_one_message_oldest_first`, by its name and its premise | `test_several_files_come_out_one_stop_each_oldest_first`; phase 4 corrects 0.15.7 N7 and 0.17.0 B2 <!-- NAME NOT IN TREE --> |
| `test_shade_lights_the_upper_left_edge_and_shadows_the_lower_right`, by its name | `test_shade_lights_the_mark_and_casts_its_shadow_down_right`; phase 1 added it, no released row cites it <!-- NAME NOT IN TREE --> |
