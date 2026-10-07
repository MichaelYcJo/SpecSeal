# 1791270164-the-release-seal-is-drawn-in-curves — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 35277597 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 3 row, as reframed on 2026-10-07 and approved at `7c18ca9b`: the 14-cell disc and the hand-drawn chart with its four colours (`DISC_CELLS`, `DISC_LINES`, `EDGE_INSET`, `RING_INSET`, `CHART`, `MARK`, `MARK_SHADOW`, the four-colour `DISC_COLOURS` and `KEY`); `build`, `compose` and `letter_row` rewritten; the sampler and its constants retired; the sentence pins and the policy paragraph corrected; Q3 measured.

The spawn added: a case that pins the drawn cells against the reference layout for the `full_values()` shape; each new case seen red at `7c18ca9b` first and then green; `bin/mutation-check` on each new or changed unit; only the stamp modules and the slices touched run; `bin/evidence-check --strict .` may stay red only for the released rows phase 6 owes, listed; `plan.md`'s Status filled; as the last act, `fitted`'s real message for one `full_values()` block written to `specseal-stamp-14.ans` in the session's scratchpad. Do not start phase 5.

## What this phase found

**`spec.md` S3's clash rule does not draw the owner's reference, and the reference won.** S3 says the sheet widens until *no cell inside the circle stands on a character*. Variant 2 of the reference was drawn by `sheet_mock.py` over exactly `FULL_ROWS`' text — the frame's note that its text differs from `full_values()`'s is not so, line for line — and its rule is *no character under the disc's square*. Over `FULL_ROWS` the circle rule gives a sheet 51 wide with the disc at column 36. The square rule gives 54 and column 39, which is the reference cell for cell. `compose` takes the square, because the owner chose the picture and S3 names it as its source. `test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell` carries the reference transcribed from the `.ans` file's half-cells: the twin's 16 lines and the disc's 14 half-rows. The S3 case rebuilds the square rule in its own body.

**The square's right end never decides anything.** The search starts at the bare width, where the square's last column is the longest line's last character plus one, so no character stands right of it. `bin/mutation-check` showed `< left + n` survive, so the bound was dropped and the clash test reads the square's first column alone. The guard that keeps the square inside the left edge is reached only by a panel with no text at all, which no gate writes; the S3 case pins it over `[]` so its break goes red.

**Q3: one real run is 3,055 units, so two real runs share a message, not three.** Sizes are UTF-16 units at 0.90, label included, through `seal_stamp.stamp`, read by a `test_tmp_` probe that was deleted after one run:

| Panel | Sheet with the disc | Bare sheet | One | Two | Three | Sheet alone | Per message |
|---|---|---|---|---|---|---|---|
| `full_values()` (`FULL_ROWS`) | 54 × 16, disc at (39, 16) | 38 × 16 | 3,055 | 6,112 | 9,169 | 1,526 | 2 |
| the cases' `ROWS` | 51 × 14 | 35 × 14 | 2,720 | 5,442 | 8,164 | 1,223 | 3 |
| `SAMPLE_ROWS` | 52 × 14 | 36 × 14 | 2,734 | 5,470 | 8,206 | 1,237 | 3 |
| `SMALL_ROWS`, four rows | 38 × 9 | 22 × 6 | 2,078 | 4,158 | 6,238 | 481 | 4 |
| the widest panel the tree can produce | 54 × 22 | 38 × 22 | 3,696 | 7,394 | 11,092 | 2,071 | 2 |

The frame's probe had one real run at 2,901 and three to a message. The built stamp is 154 units larger. The square rule widens the sheet three columns past the circle rule, which is 48 more parchment cells over 16 lines, by arithmetic rather than by a run. The other 106 are not attributed by measurement; the frame's probe used a stand-in label "of about the real length". Three real runs are 169 units over `MESSAGE_BUDGET` (9,000), so the third waits for the next `Stop`. Every panel fits alone with its disc; the widest has 5,304 units to spare.

**Two of the cases `plan.md` lists as green unchanged could not stay unchanged.**
- `test_the_ladder_steps_down_in_order_and_ends_with_no_disc` asserted three distinct sizes over 1.0, 0.90 and no disc, and that a file at 1.0 steps to 0.90. With one disc size, 1.0 and 0.90 draw the same bytes. The case now asserts that they do, and that a file at 1.0 that does not fit is the sheet alone.
- `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it` planted sixty deferral homes, and sixty now fit with the disc (8,187 units). The case adds homes one at a time until the stamp does not fit, as `test_two_files_in_one_turn_are_under_the_budget_together` already does, and asserts its premise.

**The colour-sequence bound is per row again for the letter, and two per cell for the disc alone.** S4a asked for *every row of the block form* under one sequence per cell, and that holds. A row of the disc printed alone, where the disc's mark changes colour at almost every cell, reaches 14 sequences in 14 cells at 1.0, so the disc-alone loop keeps the two-per-cell bound it had.

**Each new or re-aimed case was seen red** (§15). All seventeen failed together at `7c18ca9b`'s drawing with the new cases in place. They were then broken one unit at a time with `bin/mutation-check`, and every verdict below is `red`. The tree was clean after each.

| Unit broken | Case that went red |
|---|---|
| `RING_INSET = 1.0`; separately `EDGE_INSET = 0.0` | `test_the_disc_is_fourteen_cells_of_exactly_four_colours` |
| the shadow taken from `on(x + 1, y + 1)` | `test_the_emblem_is_lit_from_the_upper_left` |
| one cell of `CHART`; separately the column offset without `+ 1` | `test_the_mark_is_the_owners_hand_drawn_chart` |
| `KEY[MARK_SHADOW] = "Y"`; separately `letter_row` reading the bottom half first | `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame` (and the reference case for the second) |
| `MARK_SHADOW` left out of `DISC_COLOURS`; separately `MARK` back to (226, 82, 74) | `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours` |
| the disc one column left; the disc's top line one up; the square's clash test from its fourth column | `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text` and `test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell` |
| `GAP - 1`; the short sheet's height not raised; the right edge painted parchment; the square's left-edge guard removed | `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text` |
| the floor sentence's *one size* reworded; separately the two refusals swapped | `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence` |
| `--scale`'s help reworded | the same case |
| the module docstring's twin letters reworded | `test_the_docstrings_describe_the_letter_and_the_rows_it_carries` |
| `DEFAULT_SCALE`'s comment reworded | `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it` |
| the policy's ladder sentence put back to *the § fragment on a disc smaller than 0.90's 24 cells* | `test_the_policy_states_the_budget_and_names_its_case` |
| `admitted` laying one block per message | `test_several_files_come_out_as_one_message_oldest_first` |
| `admitted` drawing a lone oversized block at the rung instead of as the sheet | `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it` |
| the disc two cells wider at 1.0 | `test_the_ladder_steps_down_in_order_and_ends_with_no_disc` |
| `colour_row` writing the background on every cell | `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` |

Three breaks survived on the first pass, and each was answered. *`admitted`'s floor at half the budget* left the small pair fitting, so the break was replaced by one block per message, which is phase 2's behaviour and what the case exists to refuse. *The two refusals swapped* passed because both sentences name both bounds; the floor case now pins which side of the band each names. *The square's right end narrowed* is the bound above that was dropped.

**What was looked at.** `fitted`'s message for one `full_values()` block is `specseal-stamp-14.ans` in the orchestrating session's scratchpad, 3,055 units. Its letters were printed with the colour codes stripped, and its twin was read against the reference: the same 54 × 16 sheet and the same disc. A terminal's rendering of the block form was not seen by this phase; the owner's look is phase 4.

**Ledger consequences for phase 6.** `bin/evidence-check --strict .` exits 2 at `35277597`: 6,605 ok, 31 drifted, 4 broken. Every row it names is a released row, plus one in another work item's unreleased fragment, all drifted or broken by this work item's code:
- **Broken (4):** `seal_stamp.py#shrink` (0.10.0, phase 1); `test_the_lily_is_lit_from_the_upper_left` (0.17.0, phase 1's rename); `test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame` (0.17.0, now `_four_letters_`); `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text` (0.17.0, now `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text`). <!-- NAME NOT IN TREE -->
- **Drifted (31):** `seal_stamp.py` `build`, `letter_row`, `main` (0.10.0); `main`, `docs/the-broad-gate.md` §*Where the stamp is drawn*, `test_several_files_come_out_as_one_message_oldest_first`, `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it` (0.15.7); `test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` (0.16.0, and twice in `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md`; phase 2 already listed it drifted); `SCALE_LADDER`, `admitted`, `stamp`, `compose`, `GAP`, `build`, `DISC_COLOURS`, `letter_row`, `KEY`, §*Where the stamp is drawn* and ten cases (0.17.0); `admitted` (0.18.0).
- `test_several_files_come_out_as_one_message_oldest_first`, which phase 2 broke by renaming it, is found again under its own name and is drifted rather than broken. 0.15.7 N7 and 0.17.0 B2 cite it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `EMBLEM_D`, `svg_path`, `SVG_REFUSED`, `SVG_TOKEN`, `SVG_ARITY`, `flatten`, `inside`, `shade`, `EMBLEM`, `EMBLEM_POLYGONS`, `crossings`, `smoothstep` | none — the owner refused the § by area (`spec.md` decision 4); `CHART` carries the disc's mark <!-- NAME NOT IN TREE --> |
| `GAMMA`, `linear`, `srgb`, `nearest`, `cube`, `CUBE_LEVELS` (in `seal_stamp.py`; `release_seal.py` keeps its own until phase 5) | none — every disc cell is one palette colour, so nothing is blended or matched; `letter_row` is a lookup |
| `RIM_LIGHT`, `RIM_DARK`, `RIM_WIDTH`, `RIM_LIT_AT`, `FIT_OFFSET`, `FIT_SCALE`, `SAMPLES`, `TIGHT_LOW`, `TIGHT_SPAN`, `SHADOW_OFFSET`, `WAX_EDGE`, `FIELD_EDGE`, the 24-cell `DISC_CELLS`, `build`'s `disc_cells` keyword and `px`'s `under` | `DISC_CELLS = 14`, `DISC_LINES`, `EDGE_INSET`, `RING_INSET`, `CHART` <!-- NAME NOT IN TREE --> |
| `LILY_LIGHT`, `LILY_SHADOW` by name | `MARK` (240, 130, 118) and `MARK_SHADOW` (96, 10, 14); phase 6 corrects the rows that cite the old names |
| `KEY`'s `M` and `n` | none — the rim gradient is gone |
| `compose`'s corner overhang, its per-line `GAP` of two, its blended edge and its trailing-cell trim | `compose`'s square rule, `GAP = 3`; nothing stands past the sheet now |
| `test_the_disc_is_twenty_four_cells_across_at_the_default_rung`, `test_the_emblem_is_the_owners_section_sign_inside_the_field`, `test_the_emblem_fills_even_odd_from_an_svg_path`, `test_shade_lights_the_mark_and_casts_its_shadow_down_right`, `test_the_terminal_draws_the_area_the_emblem_encloses`, `test_a_cell_is_the_mean_of_its_samples_in_linear_light`, `test_the_mark_reads_at_the_default_rung_and_fragments_below_it` | `test_the_disc_is_fourteen_cells_of_exactly_four_colours` and `test_the_mark_is_the_owners_hand_drawn_chart`; phase 6 corrects any released row that cites them <!-- NAME NOT IN TREE --> |
| `test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text` | `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text`; 0.17.0 cites the old name |
| `test_the_twin_writes_the_discs_six_letters_over_the_sheets_frame` | `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame`; no released row cites the *six* name <!-- NAME NOT IN TREE --> |
| `test_several_files_come_out_one_stop_each_oldest_first` | `test_several_files_come_out_as_one_message_oldest_first`, #717's name back; no released row cites phase 2's name <!-- NAME NOT IN TREE --> |
| the sentence *the owner saw the § fragment on a disc smaller than 0.90's 24 cells* in `docs/the-broad-gate.md` | the same paragraph: *the owner's disc is drawn 14 cells across at every scale, so there is no smaller disc to step to* |
