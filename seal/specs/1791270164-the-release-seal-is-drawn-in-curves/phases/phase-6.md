# 1791270164-the-release-seal-is-drawn-in-curves — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 32e257f7 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 6 row as re-planned at `62f1b47d` and approved at `c85be7af`: the 28-cell frame with the disc's mark as a chart file (`seal-mark.txt`, `read_chart`, `CHART_MALFORMED`); the nine colours and `TITLE_RED`; `build` by the rule in `spec.md` §*Data & interfaces*; the four-field cell; `text_lines`; `compose` in the open layout, the disc at the left and the text block at the right; the lean writer after `frames.py#encode`; the twin with nine letters and `TWIN_ASCII`; the sheet's units deleted; `docs/the-broad-gate.md`'s two paragraphs; the cases of S1–S4a, S5 and S11 re-aimed and `REFERENCE_TWIN` re-transcribed from `~/Desktop/specseal-frame-3-open.ans` over `frames.py`'s `ROWS`.

The spawn added: Q3 measured through the real `fitted` message against the 9,000 budget, with a case that pins it; every new case seen red at `c85be7af` first; `bin/mutation-check` on each new or changed unit; only the stamp, panel and doc slices; and, as the last act, the real `fitted` message for one `full_values()` block written to `specseal-stamp-28.ans` in the orchestrating session's scratchpad. Do not start phase 7.

## What this phase found

**Four places where the frame and the owner's reference disagree, and which won.** The reference is the owner's picture, so what a person sees follows it; what nobody sees follows the spec.
- **The rule's length — the reference won.** `spec.md` S3a makes the rule *as wide as the widest row line, and at least 30*. Over `frames.py`'s rows that is 39 `─`, and the reference has 30 beside a 46-column row. `RULE_WIDTH = 30`, a fixed length; the spec's `RULE_MIN` does not exist. <!-- NAME NOT IN TREE -->
- **Trailing blanks — the spec won.** The reference pads every line with no text to 31 columns, the disc's 28 and the gap. `spec.md` S3 says no line runs past its own content, so the built lines stop at their last visible cell, and the reference case compares lines without their trailing blanks. Nothing on a screen differs.
- **The dim `·` — the spec won.** Decision 6 says a row that is not a pass *gets a dim `·`*, and S3a pins it; the reference draws the `flow` row's `·` in the full foreground. The block form dims it. It is the one difference in what a person sees.
- **A blank after the disc — the reference's encoder won.** `spec.md` S11 says a blank with no background *writes no code and leaves the running state*. Written that way, the disc's last background stays set and paints every blank up to the text: the first build did exactly that, and only a byte comparison with the reference showed it. `frames.py#encode` keeps the foreground and the style across a blank and ends the background with `49`, and `colour_row` does the same. The S11 case now reads each line the way a terminal would and requires a blank to paint nothing.

With those three named differences taken out of the reference — its trailing blanks, its plain `·`, and one redundant `39` it writes after `22;39` — the block form over `frames.py`'s rows is the reference byte for byte, all 14 lines (a scratch comparison, `executed`, deleted).

**`lit` needs no guard.** `spec.md` says `lit` is *guarded against zero as `seal28.py` does*, with `+ 1e-9`. `build` reads `lit` only past the groove's inner edge, where the distance from the centre is never 0, so it divides by `|dx| + |dy|` as the rule writes it. The counts are the framer's: 176 outside, 84 wax edge, 98 / 30 / 96 lit, mid and dark, and with the S 185 / 37 / 31 / 16 / 31 over field, face, highlight, inner shadow and drop.

**`read_chart` refuses an `M` outside the field.** S1 asserts that every `M` lies inside the groove as a fact about the chart. A chart with an `M` on the rim would lose that cell under the rim and nobody would see it go, so the loader refuses it with the same sentence, naming the line and the column.

**Cases the plan listed as green unchanged that could not stay unchanged.**
- `test_the_twin_and_the_block_form_have_equal_width_and_height` asserted the sheet's `.---.` top; those two assertions went with the sheet.
- `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` unpacked every row as a pair; it skips `None` now (phase 5).
- `test_the_ladder_steps_down_in_order_and_ends_with_no_disc` read rows at `{label:<8}`; the open layout pads to seven.
- `test_a_values_file_from_an_older_gate_draws_every_row_and_skips_its_blanks` <!-- NAME NOT IN TREE --> said an older file's blanks draw no line, which the sheet did. The open layout draws a `None` row blank, so the case is `test_a_values_file_from_an_older_gate_draws_every_row_in_the_new_layout`, over the older shape kept as `OLD_ROWS`. 0.17.0 cites the old name.
- `test_the_panel_renders_its_rows_and_its_blanks` <!-- NAME NOT IN TREE --> pinned `letter`, which is gone; S3a's case covers each of its claims, and no ledger row cites it.
- `test_the_title_is_the_sheets_first_line_whatever_a_value_says` keeps its name, because 0.17.0 cites it, and pins `text_lines`' title now.

**`release_seal.py` still paints with `block`, which this phase retired.** Thirteen cases of `tests/test_the_release_seal_is_drawn.py` are red at this commit, every one with `module 'specseal_seal_stamp' has no attribute 'block'`. Phase 8 replaces that path with the owner's SVG and `rasterise`; until it lands the release's seal would be skipped with a `::warning::`, as its own failure rule says. The plan put `block`'s removal here and the release's change there, and the two do not stand apart.

**Q3: one real run is 5,254 units, so one stamp goes out per message.** UTF-16 units at 0.90, label included, through `seal_stamp.fitted` and `stamp`, read by a `test_tmp_` probe run once and deleted:

| Panel | With the disc | Block alone | One | Two | Text block alone | Per message |
|---|---|---|---|---|---|---|
| `full_values()` (`FULL_ROWS`) | 80 x 14 | 5,084 | 5,254 | 10,510 | 696 (49 x 13) | 1 |
| the reference's rows | 77 x 14 | 5,088 | 5,258 | 10,518 | 700 (46 x 13) | 1 |
| the hook's `ROWS` | 68 x 14 | 4,931 | 5,012 | 10,026 | 467 (37 x 11) | 1 |
| `SAMPLE_ROWS` | 70 x 14 | 5,101 | 5,271 | 10,544 | 698 (39 x 14) | 1 |
| `SMALL_ROWS`, four rows | 68 x 14 | 4,662 | 4,743 | 9,488 | 225 (37 x 5) | 1 |
| the widest panel the tree can produce | 80 x 18 | 5,419 | 5,618 | 11,238 | 925 (49 x 18) | 1 |

The owner's reference file is 5,119 characters; the block over its own rows is 5,088 here, 31 fewer for the trailing blanks and the one `39`. Every panel fits alone with its disc, the widest with 3,382 to spare, and no two share a message — even the smallest pair is 488 over. `test_several_files_come_out_one_stop_each_oldest_first` pins that, its premise asserted; `test_the_hooks_message_is_under_the_budget_for_one_file` pins one real run under the budget through the real hook, and `test_a_line_writes_one_sgr_per_change_and_no_reset_inside_it` holds a real run's block with its label under 5,500.

**Q14: the widest panel is 5,618 units and its widest line is 80 columns**, `28 + 3 + 8 + 41`; `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` is green. `test_the_panel_value_width_is_what_the_stamp_actually_gives` now draws a value of `PANEL_VALUE_WIDTH` and requires the stamp's widest line to be exactly 80, in both forms.

**Q13: nothing enumerates the files under `skills/verify/scripts/`.** `seal_stamp.py` as a literal appears in no file of `.claude-plugin/`, `hooks/*.json` or a test that lists the directory; the plugin ships its tree whole, so `seal-mark.txt` joins nothing. One registry did need the new reader: `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` names `read_chart`'s `splitlines`, with the reason.

**What was looked at.** `bin/seal-stamp --shape` read once: the disc's letters at the left, the rows at column 31, the owner's characters in ASCII. The block form was written to `specseal-stamp-28.ans` (5,255 characters, the 5,254-unit message and a newline) and its twin read; no terminal's rendering of the block form was seen by this phase. The owner's look is the orchestrator's, before phase 7.

**Each new or re-aimed case was seen red** at the drawing of `c85be7af` — the phase-5 commit's `seal_stamp.py`, which differs from `c85be7af`'s only in `PANEL_WIDTH` and `SAMPLE_ROWS`, with `docs/the-broad-gate.md` as it stood — by setting those two files aside with `git stash` and running the 27 selected cases: 21 failed. The six that passed are the twin-footprint case at five scales, which lost two assertions and gained none, and the long-ref case, whose change was phase 5's. Then every new or changed unit was broken once with `bin/mutation-check`; the tree was clean after each:

| Unit broken | Verdict |
|---|---|
| `RIM_INSET` 3.0, `LIT_AT` 0.5, `WAX_INSET` 1.0, `GROOVE_INSET` 4.0, `EDGE_INSET` 0.0, `DISC_CELLS` 26 | red |
| the groove's test flipped; the rim's lit side at `+LIT_AT`; its dark side at 0; the groove's inner edge moved | red |
| the drop shadow taken from `on(x + 1, y + 1)`; `INNER` and `LIGHT` broken; the chart read transposed; `DROP` left out of `DISC_COLOURS` | red |
| `read_chart` accepting any count, any length, any character, an `M` on the rim, or raising nothing | red |
| `disc_cell` swapping its halves, or drawing `▄` as `▀` | red |
| the parts split into two SGRs; a reset at every change; a blank keeping the disc's background; `shown` not cleared after `22;39`; the reset written on a line with no code; `49` written as `39`; green as `33` | red |
| `22;39` written as `22` | **survived**, then red once the S11 case read each line as a terminal would |
| `letter_row` reading the background; `✓` missing from `TWIN_ASCII`; two letters made equal; `TITLE_RED` moved | red |
| `RULE_WIDTH` 29; `LABEL_WIDTH` 8; a mark with no space after it; `·` not dim; the title keyed on the label alone; the blank after the title gone; a `None` row drawn as nothing | red |
| the disc one line down; the text from line 0; the gap one short; the line's trim gone; `GAP` 4 | red |
| the gap kept with no disc; `Letter.disc` in lines rather than half-rows | **survived**, then red once the S3 case drew the bare block before moving `GAP` and an older panel taller than the disc |
| `RIM_MID` moved and the chart reversed, under the reference and the budget cases | red |

Three guards no cell can reach were removed before the breaks rather than left to survive them (`ac421623`): a blank's background test in `colour_row` and in `compose`'s trim, `colour_row`'s `if parts`, and its green-foreground skip.

`bin/test` over the two stamp modules, the range and steps modules and the line and word hygiene modules at the last commit: 733 passed, then the strengthened cases again; the hygiene modules, `ruff check` and `ruff format --check` clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `WAX_M`, `MARK`, `MARK_SHADOW` and the 14-cell `FIELD`; the four-colour `DISC_COLOURS` and `KEY` | the nine colours, `DISC_COLOURS` and `KEY` of nine; phase 9 corrects the rows that cite the old names |
| `RING_INSET`, the 14-cell `DISC_CELLS`, the `CHART` tuple and its placing offsets | `WAX_INSET`, `RIM_INSET`, `GROOVE_INSET`, `LIT_AT`, `DISC_CELLS = 28`, `seal-mark.txt` read by `read_chart` |
| `PARCHMENT`, `SHEET_EDGE`, `INK`, `TITLE`, `TEXT_LEFT`, `PANEL_WIDTH`, `letter`, `sheet_text`, `block`, `sgr`, and `compose`'s sheet, square-clash search and edge | the open layout: `text_lines`, `compose`, `disc_cell`, `colour_code`, `STYLE_CODES`, `TWIN_ASCII`, `TITLE_RED`, `LABEL_WIDTH`, `RULE_WIDTH`, `TITLE_ROW`, `VALUE_MARKS`; `release_seal.py`'s use of `block` is phase 8's |
| `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`, `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`, `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text`, `test_the_emblem_is_lit_from_the_upper_left`, `test_the_disc_is_fourteen_cells_of_exactly_four_colours`, `test_the_mark_is_the_owners_hand_drawn_chart`, `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame`, `test_the_panel_renders_its_rows_and_its_blanks`, `test_several_files_come_out_as_one_message_oldest_first`, `test_a_values_file_from_an_older_gate_draws_every_row_and_skips_its_blanks` <!-- NAME NOT IN TREE --> | `test_a_line_writes_one_sgr_per_change_and_no_reset_inside_it`, `test_the_disc_stands_left_of_the_open_text_block_each_centred`, `test_the_disc_is_lit_from_the_upper_left`, `test_the_disc_is_twenty_eight_cells_in_the_frames_nine_colours`, `test_the_disc_mark_is_one_chart_file_read_as_data`, `test_the_twin_writes_the_discs_nine_letters_and_the_text_in_ascii`, `test_the_text_lines_are_a_red_title_a_rule_and_the_rows_under_it`, `test_several_files_come_out_one_stop_each_oldest_first`, `test_a_values_file_from_an_older_gate_draws_every_row_in_the_new_layout`; phase 9 corrects the released rows that cite the old names |
| the policy's *14 cells across* and the parchment's contrast figures | `docs/the-broad-gate.md`'s same two paragraphs: 28 cells, one real run per message, nothing outside the disc painted |
