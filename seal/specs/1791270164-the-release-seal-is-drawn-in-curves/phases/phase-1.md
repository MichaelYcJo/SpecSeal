# 1791270164-the-release-seal-is-drawn-in-curves — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 88070eac |
| Ran by | smith on Opus 5.5 for the segment that stopped at `de5f8fcb`, as `handoff.md` records it; smith on Opus 5.5 for the closing segment, on the next machine (filled by the orchestrating session; the spawn prompt named neither) |

## What this phase was asked

`plan.md`'s phase 1 row: the vector source (`EMBLEM`, `svg_path`, `flatten`, `inside`, `shade`) in `seal_stamp.py`; `build` sampling it at cell centres with `R0_CELLS · scale`; `ART` and `shrink` removed; `SCALE_REFUSED` and `SCALE_TOO_LARGE` reworded; the `KEY` comment and the module docstring following; the lighting case rewritten; the fixture-emblem, area-fidelity and footprint cases planted. <!-- NAME NOT IN TREE -->

The closing segment was handed the phase at `de5f8fcb`, committed `wip` and not green, with four steps: read which rungs `admitted` picks for two `SMALL_ROWS` blocks and confirm or refute the suspicion that the narrower 0.90 disc caused the red case; re-run the two modules without `-x`; show each new case red; finish S8's sweep and write this record. It was told to keep `EMBLEM_D` as the labelled interim ring and `build`'s `r0_cells` keyword at its default, to pick no emblem and shrink no disc, and to say here which pins move when the owner's emblem and a smaller disc drop in. <!-- NAME NOT IN TREE -->

## What this phase found

**The red case was the emblem, not the disc's width.** The suspicion was refuted by measurement. The interim ring changes colour far less often per row than #717's lily did, so every block form is shorter. Sizes in UTF-16 units, `python3` over `seal_stamp.stamp` and `admitted`, 2026-10-06:

| Drawing | `SMALL_ROWS` at 0.90 / 0.80 / 0.75 | `admitted` picks for two | Real run (`FULL_ROWS`) at 0.90 / 0.80 / 0.75 | Two real runs |
|---|---|---|---|---|
| base (the lily, 0.90 disc 40 × 40) | 5,420 / 4,615 / 3,813 | 0.80, 0.75 | 6,516 / 5,695 / 4,926 | one drawn, one waits |
| interim ring (0.90 disc 39 × 40) | 4,201 / 3,673 / 3,374 | 0.90, 0.90 | 5,304 / 4,821 / 4,487 | both drawn at 0.75 (8,976 of 9,000) |
| interim ring, 0.90 forced to 40 × 40 | 4,174 / 3,673 / 3,374 | 0.90, 0.90 | — | — |

The last row is the refutation: with the 0.90 footprint put back, the picks do not move.

**Two neighbouring hygiene cases were red against phase 1 as well**, outside the two modules the plan names, and the closing commit fixes both. `test_one_word_one_meaning.py::test_no_instructing_document_leaves_an_instance_anonymous` refused `EMBLEM_D`'s comment for *which mark the seal carries* with no owner; it now says *the disc*. `test_every_reader_ends_a_line_where_gfm_does.py::test_every_splitlines_call_left_is_named_with_its_reason` still registered `seal_stamp.py`'s module-level `splitlines`, the call that parsed `ART`; the entry is gone. Both were seen red against `915fbc5c` and green after.

**A second case was red behind `-x`.** `test_two_files_in_one_turn_are_under_the_budget_together` asserts that two real runs do not share a message; under the ring they do, by 24 units. The first full run without `-x` showed both reds and 510 passing. At the closing commit the two modules and the five that read `seal_stamp.py` beside them (`test_the_release_seal_is_drawn.py`, `test_a_script_says_which_interpreter_it_needs.py`, `test_one_word_one_meaning.py`, `test_every_reader_ends_a_line_where_gfm_does.py`, `test_release_hygiene.py`) ran together with `-p no:xdist`: 804 passed.

**`spec.md` S4's "A2–A4 green unchanged" cannot hold as written.** Those cases pinned sizes, and the sizes are a property of the emblem, which the frame leaves open. Shrinking `R0_CELLS` to restore the lily's sizes was not available: the disc's size is the owner's. So the two cases now derive what the drawing decides instead of writing it in: <!-- NAME NOT IN TREE -->

- `test_several_files_come_out_as_one_message_oldest_first` computes the older block's rung (the highest that leaves the newer room at 0.75) and the newer's (the highest left) from the blocks' sizes under `MESSAGE_BUDGET`, and asserts the precondition that two fit at 0.75. Under the ring both are 0.90, so this case no longer exercises two different rungs through the hook; `test_the_ladder_steps_down_in_order_and_ends_with_no_disc` still does at budgets it picks.
- `test_two_files_in_one_turn_are_under_the_budget_together` gives the second run deferral homes, one at a time, until the pair does not fit at 0.75, and asserts the second still fits at 0.90 alone. Under the lily it adds none, so the case is the one #717 wrote; under the ring it adds one (the pair at 0.75 is then 9,047).

**Each new case was seen red** (§15), each by one `mutation-check` against `seal_stamp.py`, every verdict `red` and every file restored:

| Case | Break |
|---|---|
| `test_the_emblem_is_lit_from_the_upper_left` | `build` samples `shade` 0.05 to the right of the cell centre — red on the new field-cell check (a cell `LILY_LIGHT` where `shade` says field) |
| `test_each_rung_keeps_the_disc_height_the_chart_gave_it` | `R0_CELLS = 15.5 / 0.73` <!-- NAME NOT IN TREE --> |
| `test_the_emblem_fills_even_odd_from_an_svg_path` | four breaks, each red: `inside` sets instead of toggling; `Q` raised with 1/2 instead of 2/3; the viewBox divided by 400; lowercase commands let past the refusal <!-- NAME NOT IN TREE --> |
| `test_shade_lights_the_upper_left_edge_and_shadows_the_lower_right` | the highlight probe taken down-right <!-- NAME NOT IN TREE --> |
| `test_the_terminal_draws_the_area_the_emblem_encloses` | the emblem's frame scaled by 1.3 (drawn 512 cells against 343 enclosed) <!-- NAME NOT IN TREE --> |
| `test_the_stamp_module_imports_with_pillow_blocked` | `import PIL` at the module's head |
| `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence` | `SCALE_REFUSED` saying *stitches*; separately `SCALE_TOO_LARGE` saying *measured past it* |
| `test_the_docstrings_describe_the_letter_and_the_rows_it_carries` (the new #832 lines) | three breaks, each red: *the lily's face* back; the `EMBLEM_D` sentence removed; *a fleur-de-lis* back |
| `test_several_files_come_out_as_one_message_oldest_first` | `admitted` never takes a higher rung |
| `test_two_files_in_one_turn_are_under_the_budget_together` | `admitted`'s floor pass lets a block in up to twice the budget |

**The twin was read once at 0.90** (`bin/seal-stamp --shape --scale 0.9`): the ring sits inside the field with its highlight on the upper-left arc and its shadow on the lower-right, and every margin is even. The block form on a terminal was not looked at by this segment.

**Ledger consequences for phase 4.** Phase 1 moved anchors that released rows cite, and none of them is corrected here, because the citing rows belong with phase 4's corrections. The rename of `test_the_lily_is_lit_from_the_upper_left` removes an anchor that `seal/releases/0.17.0.md` L2 cites, so L2's `Corrected ·` row must cite `test_the_emblem_is_lit_from_the_upper_left`. The two amended hook cases move anchors that `seal/releases/0.15.7.md` N7 and `seal/releases/0.17.0.md` B2 cite (`@3bde6bd1`, `@34e5bc28`), so those take a re-read in the fragment.

### What the emblem answer and a smaller disc will touch

The mechanism does not change for either. `EMBLEM_D` is parsed by `svg_path` at import and flattened once into `EMBLEM_POLYGONS`; `build`'s radius is `r0_cells · scale` with `R0_CELLS` as the default. <!-- NAME NOT IN TREE -->

**The owner's emblem** replaces the string `EMBLEM_D` and the INTERIM paragraph of the comment above it, and nothing else in code. Then:

- Must stay green, and are the emblem's acceptance: `test_the_terminal_draws_the_area_the_emblem_encloses` (85–115 % at every rung — a stroke under about 50 viewBox units fails here), `test_the_emblem_is_lit_from_the_upper_left` (all three colours must appear at 0.90, 0.80 and 0.75), `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` (a busier mark adds colour changes per row), `test_the_disc_draws_the_same_bytes_in_every_process`, `test_the_disc_is_symmetric_because_it_is_computed`. A `svg_path` refusal names the command to convert. <!-- NAME NOT IN TREE -->
- Re-measured, not edited: every hook budget case in `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`. The two amended above follow the sizes by construction. `test_the_hooks_message_is_under_the_budget_for_one_file`, `test_a_values_file_from_an_older_gate_draws_every_row_and_skips_its_blanks` and `test_the_main_sessions_stop_draws_each_undrawn_file_once` assume a real run fits at 0.90; the lily was 6,516 there, so only a mark much busier than the lily moves them.
- The words that name the interim mark: `EMBLEM_D`'s comment, this record, `overview.md`'s Not verified row, and the twin above.

**A smaller disc** is a new value of `R0_CELLS` (or a scale band that maps to it). Then: <!-- NAME NOT IN TREE -->

- `test_each_rung_keeps_the_disc_height_the_chart_gave_it` moves wholly: its four `(w, h)` pairs, and its name and docstring, which say the chart's heights are kept. <!-- NAME NOT IN TREE -->
- `R0_CELLS`'s comment (*keeps that radius, so the four rungs keep the heights they had (44, 40, 36, 34)*), and the `DEFAULT_SCALE` comment's *the disc is 20 lines against the panel's 16* and *the disc (17 lines)*. <!-- NAME NOT IN TREE -->
- The authoring limit in `questions.md` Q1 and `EMBLEM_D`'s comment, *no stroke thinner than about 50 units*, scales by 15.5 / 0.74 over the new value: a smaller disc puts fewer cells under each stroke, and the area case is what says so.
- Every hook size above shrinks; the same budget cases are re-measured, and phase 2's sheet layout cases are drawn against the new size.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `ART`, the 29 × 32 chart of the lily, and `shrink`, its majority vote | none — the owner withdrew the lily (`spec.md` decision 1); `seal/releases/0.10.0.md` S2 and `0.17.0.md` L2 still describe them and take `Corrected ·` rows in phase 4 |
| `build`'s `margin` keyword | none — only the chart's reach used it; the radius is `R0_CELLS` now (`overview.md` divergence row) <!-- NAME NOT IN TREE --> |
| `test_the_lily_is_lit_from_the_upper_left`, by its name | `test_the_emblem_is_lit_from_the_upper_left`, same body; 0.17.0 L2's correction cites the new name |
| `seal_stamp.py`'s module-level entry in the `splitlines` registry of `tests/test_every_reader_ends_a_line_where_gfm_does.py` | none — its one call parsed `ART` |
| The fixed rungs (0.80, 0.75) and the fixed premise (two real runs never share a message) of two hook cases | derived in the cases themselves; the lily's figures are in the table above |
