# Implementation Plan: the terminal seal is a 28-cell frame holding one replaceable mark beside an open text block, and the release PNG is the owner's SVG with the same mark (#832)

<!-- seal/specs/1791270164-the-release-seal-is-drawn-in-curves/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.
Approved 2026-10-07 by the orchestrating session under the owner's `automation` answer and their seal decision of that day, when `smith` was spawned for the reframe.
Approved 2026-10-07 by the orchestrating session under the owner's `automation` answer and their final seal and layout decisions of that day, when `smith` was spawned for phases 5–9.

## Summary

The terminal stamp is two things side by side on the terminal's own
background and nothing else: at the left a 28-cell disc, 14 lines,
computed from `DISC_CELLS` so it is symmetric and reproducible, every cell
exactly one of nine colours — a wax edge, a rim lit from the upper left in
three steps, a groove lit the other way, the field, and the disc's mark in
the red lily's three tones with a drop shadow; three columns right of it an
open text block — a bold red `SEALED` with a dim rule, a blank line, the
rows with dim seven-column labels and a green ✓ on a result row — each
centred on the taller one's height. The mark is a placeholder S held as one
28 × 28 dot chart in a text file beside the module, read as data, so the
mark the owner eventually chooses (#857) replaces one file and nothing
else. The rows take the owner's joined shape in `broad_gate.panel`, the one
place that owns them. The twin writes nine letters and ASCII text. The
block form's writer is lean: one SGR per change, no reset inside a line,
no 256-colour code anywhere. The hook's ladder keeps its one rung, and one
stamp goes out per message, as in the lily's day. The seal gallery moves
from `docs/seals/` to `assets/seals/` and gains three archived candidates.
The release PNG is the owner's 32 × 32 SVG with the same placeholder S as
paths, rasterised by `rsvg-convert` at 2× in the `seal` job; the note shows
it at display width.

This frame was drawn by `framer` on Fable 5.1 (fce42e0d), revised on
2026-10-06 to fold in the owner's answer to Q1 (b7a13d47), reframed on
2026-10-07 after the owner's look at phase 2's stamp (27a4f321), and
**re-planned later on 2026-10-07** by `framer` on Fable 5.1 from phase 3's
closed commit, to fold in the owner's final seal decisions (`spec.md`
decisions 5 and 6, which arrived an hour apart through the orchestrator).
**That re-plan is an owner's value change, not a review reframe**: no
review round has run, the review chain sent nothing back, and so no
`Reframed` line is added under the mark. The earlier reframe is recorded
in a sentence above the mark rather than as a `Reframed` line, because that
line names a review round and none sent it. Phases 1–4 keep their commits; phases 5–9 below are the new ones,
and `spec.md` §*What phase 3 built that decisions 5–6 keep, and what they
replace* says which of phase 3's units the smith re-aims rather than
discovers.

**On wall time.** Phase 5 is a dozen lines in `panel` and six cases moved;
phase 6 is the palette, the chart loader, a thirty-line `build`, a new
`text_lines`, a shorter `compose`, two rewritten writers and about fourteen
cases re-aimed; phase 7 is a `git mv`, nine new files and a README section;
phase 8 is the held patch re-applied with one glyph swapped; phase 9 is
records. A reasonable expectation for the five together is **four to five
hours of smith wall time**.

## Technical context

**What the code does at 9fef49cf** (phase 3 closed at 35277597, Q8 recorded
at 200fedf1, the ledger and changelog fragments written for the 14-cell
disc; read 2026-10-07).

- `skills/verify/scripts/broad_gate.py#panel` (line 2867): rows `SEALED`,
  `tree`, `""` branch, `base`, `""` ref, `item` (`#<pr> . <id>`), `gate`,
  `suite` (pytest's counts split on `, ` and `wrapped` onto `""` rows),
  `ledger` (`<ok> ok`), `CI also <n> more steps`, `rounds` (` . capped`,
  `<k> deferred -> <homes>`). No `None` row since #717, no `chain` row, no
  `exit 0` under the suite and no drifted/broken counts under the ledger
  (#717 took them off as saying what `SEALED` says). `PANEL_VALUE_WIDTH =
  23` is measured against `seal_stamp.letter`'s 36-column frame; `fit`
  elides a value past it, `wrapped` continues a list. Separators are ASCII
  on purpose, for the twin's non-UTF-8 console.
- `skills/verify/scripts/seal_stamp.py` (1,042 lines, stdlib-only, loaded
  by path from `broad_gate.py#STAMP`, `hooks/sealer-stamp.py`,
  `bin/seal-stamp` and `release_seal.py#stamp()`):
  - `DISC_CELLS = 14`, `CHART` of ten strings, four colours, `KEY` of four.
  - `letter(rows)` frames the rows in `.---.`/`|` at `PANEL_WIDTH` 36;
    `sheet_text` strips the frame and the blank lines; `compose` writes the
    text on a parchment sheet (`PARCHMENT` 230, `SHEET_EDGE` 187, `INK` 94,
    `TITLE` 124 — 256-colour codes) with the disc inside it against its
    right edge after a square-clash search; a cell is `(top, bottom, text,
    frame)`.
  - `block` paints a two-halves-one-colour cell as a space with a
    background; `colour_row` emits a colour per changed side as separate
    SGRs, resets over a cell nothing covers and at a line's end; `sgr` has
    a 256-colour branch; `letter_row` is a `KEY` lookup falling back to the
    frame character.
  - `SCALE_LADDER = (0.90,)`, `admitted`, `fitted`, the budget constants,
    the band and `check_scale`; `main` with `--shape`, `--scale`, `--from`;
    `SAMPLE_ROWS` in the old row shape.
- `.github/scripts/release_seal.py` (610 lines) still paints the terminal
  stamp cell for cell with Pillow; `publish_release_note.py#sealed_glance`
  writes `![alt](url)`. The held phase-5 work — `rasterise`, `SVG`,
  `SEAL_PX`, `DENSITY`, `<img width>` with escaping, the new and retired
  cases — is a patch of four tracked files plus the converted SVG at
  `<scratchpad>/p5-held/`, none of it committed; its SVG holds the § as
  three `<path>` layers.
- `docs/seals/` holds the gallery (6d0096b0); `tests/test_docs_line_wrap.py#COVERED`
  names its README. Nothing else in the tree reads `docs/seals`.
- `seal/ledger/1791270164-….md` (17 rows) corrects seven released rows for
  the 14-cell disc on the parchment sheet; `changelog.md` carries two
  entries for it.

**What the owner's references are, and what the frame read and measured.**

- The disc: `<scratchpad>/seal28.py`'s `seal()` is the geometry and colour
  rule, `chart28-S.txt` the mark (`read`). Frame counts over the 784 cells,
  from the rule: 176 outside, 84 wax edge, 98 / 30 / 96 rim lit / mid /
  dark (the groove's cells counted with the rim's by colour), 300 inside
  the groove; with the S chart 185 field, 37 face, 31 highlight, 16 inner
  shadow, 31 drop (`executed`, 2026-10-07, the framer's probe, deleted).
- The layout: `<scratchpad>/frames.py`'s `design_open` and `encode`, and
  their output `~/Desktop/specseal-frame-3-open.ans` (`read`): 14 lines,
  77 columns, 5,119 characters (UTF-16 units the same, every character in
  the BMP), 15 lines with the trailing newline; the disc on columns 0–27,
  the text from column 31; the title `SEALED ` bold in (196, 40, 44) then
  thirty `─` dim; a blank line; eleven rows over `frames.py`'s `ROWS`
  (`tree`, `""` branch, `base <commit>  <ref>`, `item #12 · 1799000000`,
  `gate`, `None`, `suite ✓ 6621 passed · 11 skipped`, `ledger ✓ 3451 ok · 0
  drifted · 0 broken`, `chain ✓ exit 0`, `flow · 4 of 9 not answered`,
  `rounds 2`); text 13 lines against the disc's 14, so the text starts on
  the disc's first line. The SGR parts in the file are exactly `0`,
  `1;38;2;196;40;44`, `2;39`, `22;39`, `22;39;2;39`, `22;39;32`, `39`, `49`
  and `38;2;…`/`48;2;…` over the nine disc triples, sometimes both in one
  SGR — no `;5;` anywhere.
- `frames.py`'s `ROWS` are the hook test module's `FULL_ROWS` re-shaped by
  hand, not what `panel` returns: the real panel carries `CI also <n> more
  steps` and no `chain` or `flow` row, and has carried no `None`, no
  `exit 0` and no drifted/broken counts since #717. Phase 5 is what makes
  `panel` return the owner's shape; the reference case uses the mock's rows
  as a fixture, because a fixture is data and the owner's picture was drawn
  over them.
- The budget: the frame's earlier probe over the parchment layout (5,699
  for one real run through the tree's `colour_row`) is history with the
  sheet. The open layout's reference is 5,119 for rows of the same length
  as a real run's, so one real run per message with about 3,800 units to
  spare, two (10,240) over the budget. Phase 6 measures the real `fitted`
  message through `stamp` (Q3). The orchestrating session's 10,361 for the
  parchment layout was the mock renderer's `ansi()`, which resets and
  rewrites both sides at every change; neither that encoding nor the
  tree's current `colour_row` survives this work — the lean writer of S11
  is `frames.py#encode`'s rule.

**`rsvg-convert` and the fonts, checked 2026-10-07** (`read` from
`actions/runner-images`' `Ubuntu2404-Readme.md`, `executed` on this
machine by the earlier reframe): the runner image lists neither
`librsvg2-bin`, nor cairo, nor Inkscape, nor ImageMagick, nor any Microsoft
font. This machine has `rsvg-convert 2.58.4` (`/opt/homebrew/bin`) and
`Georgia Bold.ttf` under `/System/Library/Fonts/Supplemental/`. The held
work drew the §'s text and path versions at 320 px and found one pixel
differing by 9 in one channel against a Helvetica control of 7,661 pixels.
So the tree's copy carries the glyph as paths, and the `seal` job installs
`librsvg2-bin` with `apt-get`. Phase 8 verifies the install at the first
tag that runs the job (Q10); until then the install line is `read`.

- Tests that pin the current drawing and will move, by phase:
  phase 5 — in `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `test_the_suite_carries_its_counts_and_nothing_under_them`,
  `test_the_ledger_carries_its_ok_count_and_nothing_beneath`,
  `test_a_base_that_is_its_own_commit_has_no_ref_row_under_it`,
  `test_a_list_too_long_for_its_row_continues_beneath_it`,
  `test_the_sample_carries_every_row_the_panel_can`,
  `test_the_values_file_holds_this_runs_panel`,
  `test_the_documents_name_the_ci_also_row`, the panel-width case (the
  smith finds it by `PANEL_VALUE_WIDTH`), and every case that reads a row's
  text (`item`'s ` . `, `rounds`' ` . capped` and `->`; the smith greps the
  two stamp test modules and `tests/test_the_mode_is_a_row_and_a_command.py`,
  `tests/test_routing_is_recorded.py`, `tests/test_the_implementer_is_recorded.py`,
  `tests/test_waiver_decided_at_start.py` for the separators, since those
  modules name a `workflow` word for other reasons);
  phase 6 — in the sealer module,
  `test_the_mark_is_the_owners_hand_drawn_chart`, <!-- NAME NOT IN TREE -->
  `test_the_disc_is_fourteen_cells_of_exactly_four_colours`, <!-- NAME NOT IN TREE -->
  `test_the_emblem_is_lit_from_the_upper_left`, <!-- NAME NOT IN TREE -->
  `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text`, <!-- NAME NOT IN TREE -->
  `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`,
  `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame`, <!-- NAME NOT IN TREE -->
  `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours`,
  `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`,
  `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`,
  `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence`
  (only where a sentence names 14); in the hook module,
  `test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell`
  (`REFERENCE_TWIN`), `test_several_files_come_out_as_one_message_oldest_first`,
  `test_the_policy_states_the_budget_and_names_its_case`,
  `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it`
  (only where a sentence names 14), and `FULL_ROWS`, `ROWS`, `SMALL_ROWS`;
  phase 7 — `tests/test_docs_line_wrap.py#COVERED`, one entry removed;
  phase 8 — in `tests/test_the_release_seal_is_drawn.py` and
  `tests/test_a_release_publishes_its_note.py`, exactly what the held patch
  changes. Tests that must stay green unchanged:
  `test_the_disc_draws_the_same_bytes_in_every_process`,
  `test_the_disc_is_symmetric_because_it_is_computed`,
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
  `test_the_alt_text_is_one_sentence_carrying_every_value`,
  `test_the_command_piped_prints_the_twin`.
  `tests/test_the_gate_names_every_step_ci_runs.py` reads `hygiene.yml`
  only, so a new step in the `seal` job is not a row of `PARTITION`.

**Constraints.**

1. `seal_stamp.py` stays stdlib-only and importable on Python 3.12 without
   Pillow; the chart file is opened with `encoding="utf-8"`.
2. No new Python package anywhere. `rsvg-convert` is a system package of the
   `seal` job alone, installed by a workflow step, and nothing under
   `hooks/`, `skills/` or `tests/` requires it: the one case that runs it
   skips where it is absent.
3. The hook's message stays under `MESSAGE_BUDGET` at 0.90 for a real run's
   values, with the one-rung ladder. Measured by phase 6 through the real
   `fitted` message, recorded in the fragment (Q3), pinned by
   `test_the_hooks_message_is_under_the_budget_for_one_file`.
4. Any failure in the release path is a `::warning::` and exit 0.
5. New code in `release_seal.py` avoids `zip(..., strict=)` and `*.UTC`.
6. Every comment over the disc's colours and chart says whose mark
   (*the disc's mark*): phase 1 met the one-word check on a bare *the mark*.
7. **No case pins the S's shape.** Every case that touches the mark reads
   `CHART` as data and derives what it asserts from it, so #857's chart
   replaces `seal-mark.txt` and nothing else goes red but the reference
   case (which is the owner's picture and is re-transcribed then).
8. **Nothing outside the disc has a background colour**, and nothing is
   drawn but the disc and the text: no sheet, no edge, no frame. The stamp
   reads in the terminal's own theme.
9. **The rows change in `panel` and nowhere else.** `seal_stamp` formats
   whatever rows it is given and never joins, renames or re-spells one; an
   older values file draws its old rows in the new layout.
10. **The stamp's widest line stays inside 80 columns** for the widest
    panel the tree can produce: `PANEL_VALUE_WIDTH` is 41 because `28 + 3 +
    8 + 41 = 80`, and the widest-panel case measures it.

**What breaks in six months.**

- Somebody edits `seal-mark.txt` by hand into a shape `read_chart` refuses:
  the gate's import of `seal_stamp.py` raises with the sentence, and the
  suite is red at S1 — before any gate loads it, because the suite imports
  the module on every run.
- Somebody edits the chart into a legal shape nobody chose: nothing in the
  tree can tell, by design (constraint 7); the reference case goes red
  because the owner's picture no longer matches, and that is the one case
  #857 re-transcribes on purpose.
- A terminal theme whose default foreground is red, or whose green is
  faint: the title and the ✓ are the terminal's own choices now, as every
  CLI's are; the owner reads the first real seal on a light and a dark
  background, as `docs/the-broad-gate.md` already says.
- A terminal without SGR 2 (dim): labels and the rule render in the full
  foreground; nothing is lost but the hierarchy.
- A value past 41 columns: `fit` elides it with `...`, as it did at 23.
- A terminal with a different cell aspect: a half-block grid is 1:2 by
  construction and the chart was fitted on it.
- GitHub's sanitiser drops `width` on `<img>`: the image shows at 320 px
  (too large, not broken); Q4 measured that it keeps it.
- The runner image or apt changes `librsvg2-bin`'s availability: the seal
  is skipped with a `::warning::` naming the call, and `DRY_RUN=1` by hand
  from a machine that has it is the path the checklist already names.
- The harness moves `MESSAGE_LIMIT`: with a stamp at about 5,200 units the
  hook can lose about 40 % of its budget before a real run comes out as the
  text block alone; a second real run already waits for the next `Stop`.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The 14-cell light-red § on the parchment sheet** (decision 4, phase 3's stamp, Q8 accepted) | The owner compared it with marks from 14 to 32 cells and settled the 28-cell frame (decision 5), then chose a layout with no sheet at all (decision 6) | superseded; archived as a candidate in `assets/seals/candidates/` with a note that it stood on the parchment sheet |
| **The 28-cell disc inside the parchment sheet, right of the text** (decision 5 alone, as this plan stood for an hour on 2026-10-07) | The owner chose `frames.py`'s design 3: no parchment, no edge, no background, the disc at the left | superseded by decision 6 the same day; its probe figures (5,699 for one real run) are history |
| **A framed letter (`frames.py`'s design 1) or an envelope with the disc half outside (design 2)** | The owner saw all three and chose design 3 | rejected by the owner |
| **Keep `CHART` as a tuple in the module and change the mark by editing it** | One edit in one place either way; but a tuple in a 1,000-line module is not a thing a candidate's chart can be dropped over, and the gallery's candidates are charts in the same `.M` text | rejected; the mark is `seal-mark.txt` beside the module, read by `read_chart`, and a candidate becomes the mark by replacing the file |
| **Pin the S's cell counts or its rows in a case** | #857 replaces the chart and every such case goes red for a reason nobody has to re-judge | rejected (constraint 7); the cases pin the frame's counts, which no chart moves, and derive the mark's cells from `CHART` |
| **Fit the S from the font at import, as `seal28.py#fit` does** | Pillow in the gate's module, and a fit that can move with a Pillow version; the owner's decision is a chart, not a fitting | rejected; the chart is the fitted output, copied once |
| **A smaller chart as a lower rung** | #857's own lesson: a chart scaled by ratio smears below about 24 cells and a mark has to be drawn for its grid; and one real run fits with about 3,800 to spare | rejected; the ladder stays one rung |
| **Join and re-spell the rows in `seal_stamp` (a formatter between `panel` and the drawing)** | Two places would say what a row is, and the values file — which is `panel`'s rows, read by an older or newer hook — would claim rows nothing draws or draw rows nothing claimed | rejected; the rows change in `panel` (constraint 9), the drawing formats what it is given |
| **Rename `CI also` to `flow`, as the mock did** | The real panel has no `workflow` row to rename; `CI also` is seven columns already and the owner's own wording from #717, pinned in `skills/verify/SKILL.md` and `agents/sealer.md` by `test_the_documents_name_the_ci_also_row`. The reason the owner gave — the label has to fit seven columns — is met | not taken (Q15); the row gains the dim `·`. Overturning this is one word in `panel`, two documents and one case, and it is the owner's to say |
| **Leave `chain`, the ledger's drifted/broken counts and the suite's ✓ off, as #717 did (they say what `SEALED` says)** | The owner's design of 2026-10-07 shows `suite ✓`, `ledger ✓ … · 0 drifted · 0 broken` and `chain ✓ exit 0`, and both removals were the owner's choice then; the newer choice wins | the rows return, the ✓ marking exit 0; `panel`'s docstring says #717 took them off and decision 6 put them back |
| **Keep the separators ASCII in `panel` and let the colour writer render `·` and `✓`** | The values are data; a writer that rewrites `.` into `·` cannot tell a separator from a dot in a branch name | rejected; `panel` writes the owner's characters and the **twin** maps the three to ASCII where it writes them (S4), which is the one place the non-UTF-8 console is served |
| **Keep `PANEL_VALUE_WIDTH` at 23** | The owner's reference carries a 38-character branch on its own line and a 31-character joined `base`; 23 would elide both. With no frame the bound is the terminal, and 80 columns is the floor the stamp has to fit | 41, by `28 + 3 + 8 + 41 = 80`; `fit` and `wrapped` stay for values past it |
| **Drop `fit` and `wrapped` now that there is no frame** | A branch name has no bound, and the budget does; a 200-character branch would cost 200 units a line and run off an 80-column terminal | kept at the new width |
| **Emit the blank line between the groups in the drawing rather than as a `None` row** | The drawing would have to know which label starts the result rows, which is `panel`'s knowledge | `panel` returns `None` between the groups again; `text_lines` draws a `None` row blank; an older file without one draws without the blank |
| **Keep `colour_row`'s per-side SGRs and resets** | On the open layout a reset inside a line would also drop the dim and bold styles, so every text cell would re-set them; the owner asked for the lean encoding and the reference's bytes are its measure | replaced by S11's writer after `frames.py#encode` |
| **Reset and rewrite both sides at every change (the mock's `ansi()`)** | 10,361 units for one real run on the old sheet, over the budget | never the tree's encoding |
| **Paint the text block's background in the terminal's own background (SGR 49) explicitly** | Nothing to paint it over; a code with no effect on every line | no background code is written anywhere outside the disc (constraint 8) |
| **Letters for the twin's nine colours chosen by the owner** | The twin is for a console that cannot draw half-blocks; nobody has looked at it and no decision names it | the framer chose them (`spec.md` §*Data & interfaces*) |
| **Keep the gallery under `docs/seals/`** | `docs/` is policy prose under the docs hygiene checks; `assets/` is where the READMEs' images live and no check reads it | rejected by the owner (decision 5); moved with `git mv` so the lily files keep their history |
| **Keep the gallery README in `tests/test_docs_line_wrap.py#COVERED` at its new path** | The list is opt-in and only `README_PAIR` constrains it; keeping it would make `assets/` a place the docs checks read, which is the thing the move avoids | removed (phase 7) |
| **Archive the candidates as PNGs alone** | A PNG cannot be dropped in as the mark; the chart is the thing #857 starts from | each candidate is its chart, its `.ans` and a PNG |
| **Draw the release PNG with Pillow from the terminal rule** | The owner offered their own SVG, and a Pillow rendering of the chart is the staircase again | not taken; the PNG is the SVG (Q9) |
| **Keep the § in the SVG while the terminal shows an S** | *The release PNG follows the mark* is the owner's rule | rejected; the three layers become the S |
| **Render the SVG with CairoSVG** · **install Georgia on the runner** · **rasterise at display size** | As the earlier frame weighed them: a pip package over a C library; a debconf EULA and a SourceForge download; a blurry image on a dense screen | rejected; `rsvg-convert`, paths, 2× and `<img width>` kept from the held work |
| **Retire `--scale` and the band now that the disc has one size** | Fifteen parametrised cases, `main`'s flag, the values files' `scale` field and `admitted`'s `min(scale, rung)` all read it; nothing the owner looks at changes | out of scope; a work item of its own if anyone wants it |
| **Rewrite the ledger fragment's seven corrected rows as fresh corrections of the 14-cell rows** | The fragment is this work item's own unreleased file; a correction of a row that never shipped is a row nobody can cite | rewritten in place, each still correcting the released row it names |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The vector source and the terminal sampler.** `EMBLEM`, `svg_path`, `flatten`, `inside`, `shade` in `seal_stamp.py`; `build` samples them at cell centres; `ART`, `shrink` removed; `SCALE_REFUSED` / `SCALE_TOO_LARGE` reworded; the chart's registry entry gone | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -p no:xdist`; each new case shown red <!-- NAME NOT IN TREE --> | 88070eac |
| 2 | **The owner's § by area on a 24-cell disc.** `EMBLEM_D` the §, the six-colour palette, the area sampler, `compose` blending the edge and filling `Letter.disc`, `nearest`, `SCALE_LADDER = (0.90,)` with the policy paragraph; Q3 and Q6 measured | the same two files; the half-cells looked at as a picture; the sizes and the draw time in `phases/phase-2.md` | 108f549c |
| 3 | **The owner's 14-cell terminal seal on the parchment sheet.** `DISC_CELLS = 14`, `CHART` of ten rows, four colours, `compose` by the square rule, the disc inside the sheet against its right edge; Q3 measured; the real stamp written for the owner's look | the same two files with `-p no:xdist` and the hygiene modules beside them; the sizes in `phases/phase-3.md` | 35277597 |
| 4 | **The owner's look.** The owner printed `~/Desktop/specseal-stamp-14.ans` and accepted the 14-cell stamp, keeping its mark colour over the lily's tones (Q8) — superseded the same day by decisions 5 and 6, which this plan folds in | the owner's word in Q8's Status cell | 200fedf1 |
| 5 | **The panel's rows take the owner's shape, in `broad_gate.panel`.** `PANEL_VALUE_WIDTH = 41` with its comment rewritten (80 − 28 − 3 − 8); `SEP`, `ARROW`, `TICK`, `DOT`; `base` joined with its ref (`fit` to the tail, two spaces), `item_value` and `rounds_rows` on `·` and `→`, a `None` row before the result rows, the suite's pieces behind `✓` joined by ` · `, `ledger ✓ <ok> ok · <d> drifted · <b> broken`, `chain ✓ exit <code>` from `checks[CHAIN_NAME]`, `CI also · <n> more steps`; `panel`'s docstring's row table and its *No row is `None` since #717*, *A drawn panel says only what a `SEALED` stamp can say* and *Separators are ASCII* paragraphs rewritten to say what moved and why (decision 6 put back what #717 took off; the twin maps the three characters); `SAMPLE_ROWS`, `FULL_ROWS`, `ROWS`, `SMALL_ROWS` re-shaped; `skills/verify/SKILL.md`'s and `agents/sealer.md`'s `CI also` sentences gain the dim `·`. The old sheet still draws the new rows, so this phase stands alone. The cases of S5a re-aimed and `test_the_result_rows_carry_a_tick_and_a_blank_row_stands_before_them` planted, each seen red by the old shape put back | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py tests/test_the_mode_is_a_row_and_a_command.py tests/test_routing_is_recorded.py tests/test_the_implementer_is_recorded.py tests/test_waiver_decided_at_start.py -p no:xdist`; `bin/mutation-check` per changed unit; `bin/seal-stamp --shape` read once <!-- NAME NOT IN TREE --> | 21089fa7 |
| 6 | **The 28-cell frame beside the open text block, lean on the wire.** `skills/verify/scripts/seal-mark.txt` (the S chart, copied from `<scratchpad>/chart28-S.txt`), `CHART_PATH`, `CHART_MALFORMED`, `read_chart`, `CHART`; the nine triples, `DISC_COLOURS`, `TITLE_RED`; `DISC_CELLS = 28`, `DISC_LINES`, `WAX_INSET`, `RIM_INSET`, `GROOVE_INSET`, `LIT_AT`; `build(scale)` by the rule in `spec.md` §*Data & interfaces*; the four-field cell; `text_lines` with `LABEL_WIDTH`, `RULE_MIN`; `compose` by S3 (the disc at column 0, the block at `DISC_CELLS + GAP`, each centred, no sheet, `Letter.disc` filled); `colour_row` as S11's lean writer after `frames.py#encode`; `letter_row` with `KEY` of nine and `TWIN_ASCII`; `PARCHMENT`, `SHEET_EDGE`, `INK`, `TITLE`, `TEXT_LEFT`, `PANEL_WIDTH`, `letter`, `sheet_text`, `block`, `sgr`, `RING_INSET`, `WAX_M`, `MARK`, `MARK_SHADOW` gone after a grep for each; the module docstring and every docstring and comment S8 names in `seal_stamp.py` reworded; `docs/the-broad-gate.md`'s two paragraphs amended in the same commit (§14). The cases in §*Technical context* re-aimed as `spec.md` S1–S4a, S5 and S11 say, `REFERENCE_TWIN` re-transcribed from `~/Desktop/specseal-frame-3-open.ans` over `frames.py`'s `ROWS`, each new or re-aimed case seen red; the hook's message measured through `stamp` over `FULL_ROWS`, `ROWS`, `SAMPLE_ROWS`, `SMALL_ROWS` and the widest panel, the real `fitted` message for one `full_values()` block written to `<scratchpad>/specseal-stamp-28-open.ans` and its size recorded for the fragment (Q3, Q14) | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -p no:xdist`, plus `tests/test_one_word_one_meaning.py`, `tests/test_every_reader_ends_a_line_where_gfm_does.py`, `tests/test_a_script_says_which_interpreter_it_needs.py` and the encoding checker's module; `bin/mutation-check` per new or changed unit; `bin/seal-stamp` and `bin/seal-stamp --shape` read once each, the block form on a dark and a light terminal if the smith has one, else said so; the sizes written in `phases/phase-6.md` <!-- NAME NOT IN TREE --> | 32e257f7 |
| 7 | **The gallery moves to `assets/seals/` and names its candidates.** `git mv docs/seals assets/seals`; `candidates/` with `section-28.txt`/`.ans`/`.png`, `key-28.txt`/`.ans`/`.png`, `section-14-light-red.txt`/`.ans`/`.png` as `spec.md` §*Data & interfaces › The gallery* says; the README's *Candidates for #857* section (S10), saying all three stand on the parchment sheet decision 6 retired; `docs/seals/README.md` out of `tests/test_docs_line_wrap.py#COVERED`; `overview.md` gains a divergence row naming the move (the frame at 6d0096b0 said `docs/seals/`; the owner moved it) | `read`: `git ls-files docs/seals` empty, `git ls-files assets/seals` fourteen files, `cmp` on each moved file against `git show 6d0096b0:docs/seals/<name>`; `bin/test tests/test_docs_line_wrap.py tests/test_release_hygiene.py -p no:xdist`; the three PNGs opened and looked at once; the README read once | 6d73664f |
| 8 | **The release PNG is the owner's SVG with the S.** The held patch applied from `<scratchpad>/p5-held/phase5-tracked.patch` (`rasterise`, `SVG`, `SEAL_PX`, `DENSITY`, `sealed_glance`'s `<img width>` with escaping, the retired Pillow units, the cases of S6, S7, S9), then `.github/scripts/release-seal.svg` from `p5-held/release-seal.svg` with its three § paths replaced by Georgia Bold's S at the same anchors, fills and opacities — converted with `uvx --from fonttools` over `/System/Library/Fonts/Supplemental/Georgia Bold.ttf` and compared against a `<text>S</text>` version through `rsvg-convert` here before committing; the file's comment names the placeholder and #857; the `seal` job's `sudo apt-get install -y --no-install-recommends librsvg2-bin` step, `continue-on-error`, before the suite, with a comment saying why; `docs/branch-and-release.md`'s bullet and `run_tests.py`'s sentence amended; `release_seal.py`'s and the test module's docstrings say the S | `bin/test tests/test_the_release_seal_is_drawn.py tests/test_a_release_publishes_its_note.py tests/test_the_gate_names_every_step_ci_runs.py -p no:xdist`; `DRY_RUN=1 SEAL_PNG=… python3 .github/scripts/release_seal.py` with a JUnit fixture, the PNG opened and looked at once; the text-vs-path comparison's result in `phases/phase-8.md` <!-- NAME NOT IN TREE --> | 2753ce1d |
| 9 | **The records close.** `changelog.md`'s two entries rewritten for the open layout, the 28-cell frame and the placeholder S (naming #857), a third for the release PNG, and one for the gallery if it is to be named; the ledger fragment's seven corrected rows rewritten, rows for S1–S11 added, the released rows about the sheet, `letter` and the separators corrected, and the re-reads phases 5–8 moved; `overview.md` closed — its purpose line, the divergence rows about `R0_CELLS`, the centroid rule and `Letter`'s paths brought up to date, the gallery's move and the frame's and layout's changes as divergence rows, `## Not verified` drained or named; `handoff.md` retired; `survivors.md` brought up to date or retired; `survivor-check --range origin/release/v0.20.0...HEAD` at zero live places | `evidence-check --strict .` exits 0; `survivor-check` reports no live place; the `grep` from S8 returns only history <!-- NAME NOT IN TREE --> | 14c24b95 |

### What of phases 1–4 stands, and what phases 5–6 re-aim

`spec.md` §*What phase 3 built that decisions 5–6 keep, and what they
replace* is the list. The smith re-aims each of these on purpose rather
than meeting it red:

- **Phase 5, the rows:** `test_the_suite_carries_its_counts_and_nothing_under_them`
  (the ✓ and ` · `), `test_the_ledger_carries_its_ok_count_and_nothing_beneath`
  → `test_the_ledger_carries_its_three_counts_on_one_row`,
  `test_a_base_that_is_its_own_commit_has_no_ref_row_under_it` (joined
  where there is a ref), `test_a_list_too_long_for_its_row_continues_beneath_it`
  (over 41), `test_the_sample_carries_every_row_the_panel_can`,
  `test_the_values_file_holds_this_runs_panel`,
  `test_the_documents_name_the_ci_also_row`, the panel-width case, and
  `test_the_result_rows_carry_a_tick_and_a_blank_row_stands_before_them`
  planted (S5a).
- **Phase 6, the chart case** `test_the_mark_is_the_owners_hand_drawn_chart` <!-- NAME NOT IN TREE -->
  → `test_the_disc_mark_is_one_chart_file_read_as_data` (S1).
- **The footprint** `test_the_disc_is_fourteen_cells_of_exactly_four_colours` <!-- NAME NOT IN TREE -->
  → `test_the_disc_is_twenty_eight_cells_in_the_frames_nine_colours` (S2).
- **The lighting case** `test_the_emblem_is_lit_from_the_upper_left` → <!-- NAME NOT IN TREE -->
  `test_the_disc_is_lit_from_the_upper_left` (S2a).
- **The layout cases** `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text` <!-- NAME NOT IN TREE -->
  and `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it` →
  `test_the_disc_stands_left_of_the_open_text_block_each_centred` (S3) and
  `test_the_text_lines_are_a_red_title_a_rule_and_the_rows_under_it` (S3a);
  `test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell` keeps its
  name with the open-layout reference transcribed.
- **The twin's letters** → `test_the_twin_writes_the_discs_nine_letters_and_the_text_in_ascii`
  (S4); **the colours on the wire** re-aimed to nine triples, the title's
  red and the style parts (S4a).
- **The encoding** `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`
  → `test_a_line_writes_one_sgr_per_change_and_no_reset_inside_it` (S11).
- **The budget pair** — `test_several_files_come_out_as_one_message_oldest_first`
  back to `test_several_files_come_out_one_stop_each_oldest_first` with its
  premise (the pair does not fit) asserted; the rest green as phase 3 left
  them.
- **The sentence pins** — the docstring case, the policy case, the default
  scale case and the floor case, each to the new sentences where a sentence
  names 14 or the sheet, each seen red by the old sentence put back.

This table is also where the work records how far it got. **Status is
empty, or the commit that closed the phase.** Re-read the column after any
rebase.

## Operational impact

- **The terminal stamp changes shape and loses its sheet** for every installed session at the next plugin update: a 28-cell disc at the left, an open text block at the right in the terminal's own colours, no parchment and no frame, nine flat disc colours, a placeholder S until #857. The stamp reads in the terminal's theme, light or dark.
- **The panel's rows change shape in the values file too**: `base` on one row with its ref, a `None` row between the groups, `✓` on the result rows, `·` and `→` as separators, `chain` back. A values file an older gate wrote still draws, in its old row shape, in the new layout; a values file the new gate writes is drawn by an older hook on its parchment sheet — a plugin half-updated mid-session, which the next `Stop` after the update ends.
- **The hook's `Stop` message grows back to one stamp per message.** A real-run stamp is about 5,100–5,300 UTF-16 units at 0.90 (the owner's reference is 5,119; phase 6 measures the built drawing), so one real run goes out per `Stop` and a second waits for the next turn, as in the lily's day; the ladder's step to the text block alone is reached only by a panel wider than the tree can produce. `docs/the-broad-gate.md` says so.
- **One release-only system dependency.** `librsvg2-bin` (`rsvg-convert`) is installed by a step of the `seal` job on `ubuntu-latest`; nothing under `hooks/` or `skills/` needs it, and the suite skips its one real-render case where it is absent. Pillow stays pinned where it is, read by the suite alone.
- **The plugin ships one new data file**, `skills/verify/scripts/seal-mark.txt`, beside the module that reads it.
- **The seal gallery is at `assets/seals/`**, with three candidates under it; a link to `docs/seals/` anywhere outside the tree (none found inside it; #857's body names `docs/seals/` and is the orchestrator's to amend) is stale.
- **Release notes from 0.20.0 on** show the owner's seal with the placeholder S as a 320-px PNG through `<img … width="160">`, transparent outside the circle. Earlier notes keep their cell-for-cell PNGs (Q2).
- **No migration, no env var, no compatibility break.** `DRY_RUN=1` and `SEAL_PNG` work as before where `rsvg-convert` is installed; a pending values file from an older gate draws at its own 0.90, which draws the same 28 cells as every scale in the band.
