# Feature Specification: the terminal seal is a 28-cell frame holding one replaceable mark beside an open text block, and the release PNG is the owner's SVG with the same mark (#832)

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
4. (2026-10-07, after comparing renders in their own terminal) **The owner
   rejected the 24-cell area-averaged § for the terminal.** A 14-cell disc,
   a hand-drawn 7 × 10 chart of the § in one light red with a one-cell
   shadow, four flat colours, the disc inside the parchment sheet against
   its right edge. Phase 3 built it (closed at 35277597), and the owner
   printed the real stamp and accepted it, keeping its mark colour (Q8,
   200fedf1).
5. (2026-10-07, later the same day, through the orchestrator) **The disc's
   frame is final and the mark is a placeholder.** The owner looked at
   marks from 14 to 32 cells — the §, the light-red § of decision 4, the
   lily redrawn per size, a shield with a check, a page, a crown, a star, a
   padlock, a key — and kept none as the mark, but settled every rule of
   the disc around it:
   - **The frame.** A 28-cell disc, 14 lines. From the outside in: a
     one-cell wax edge; a two-cell raised rim lit from the upper left in
     three steps; a one-cell groove lit the other way; the field. No mid
     tones anywhere: every cell is exactly one of nine colours.
   - **The mark's tones.** The red lily's three — a face, a highlight where
     the cell up-left is field, an inner shadow where the cell down-right is
     field — and a drop shadow on the field cell down-right of the mark.
   - **The mark is a placeholder S** (Georgia Bold, fitted to the grid),
     held as **one replaceable 28 × 28 dot chart**. Changing the mark later
     is changing that chart alone. The mark's design is **#857** (0.21.0).
   - **The § and the key at 28 cells are archived candidates, not shipped**,
     each as its chart, its `.ans` and a PNG preview, in the seal gallery
     with the 14-cell light-red § of decision 4.
   - **The release PNG follows the mark**: the owner's SVG, its § path
     replaced by the Georgia Bold S as a path — a default the session
     proposed and the owner has not answered (Q9); it does not block.
   - **The gallery's home is `assets/seals/`**, not `docs/seals/`: `assets/`
     is where the READMEs' images already live (`assets/demo.gif`) and no
     check reads it; `docs/` is policy prose under the docs hygiene checks,
     which is why the gallery's README had to join the line-wrap list at
     6d0096b0.
6. (2026-10-07, last, through the orchestrator — **the final decision on
   the stamp; nobody is asked again**) **The whole layout: the parchment
   sheet goes.** The owner chose design 3 of the orchestrating session's
   `frames.py` (`design_open`), whose output is
   `~/Desktop/specseal-frame-3-open.ans`: no parchment, no sheet edge, no
   background colour anywhere outside the disc. The disc stands at the
   left; three columns right of it the text block — a bold title in the
   seal's red with a dim `─` rule after it, a blank line, then the rows,
   each label padded to seven columns — in the terminal's own foreground,
   labels and the rule dim (SGR 2), a green ✓ (SGR 32) on a result row that
   passed. Text and disc are each centred on the taller one's height. The
   rows join what used to wrap: `base` shows commit and ref on one line,
   `suite ✓ <n> passed · <m> skipped`, `ledger ✓ <ok> ok · <d> drifted · <b>
   broken`, `chain ✓ exit 0`; a row that is not a pass gets a dim `·`. The
   encoding stays lean. The letter twin follows the same layout in letters.

So this frame fixes decisions 5 and 6 together. Phases 1–4 keep their
commits; §*Scope › What phase 3 built that decisions 5–6 keep, and what
they replace* says which of phase 3's units stand. Decisions 5 and 6 are
owner's value changes and not a review reframe: no review round has run,
and the sentence above the mark at the foot of this file records the
2026-10-07 redraw after the owner's look at phase 2's stamp, in prose,
because a `Reframed` line names the review round that sent the work item
back and no round did. The file names
below are coordinates in the tree as it stands at 9fef49cf, read
2026-10-07.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Nothing here stops to ask. Decision 6 closed the last open point of the stamp, and the owner said nobody is to be asked again. Every other judgment is made from the tree and written where a reviewer can open it |
| `CONTRIBUTING.md` §*Running the checks* (*the gates themselves are stdlib-only Python and import nothing the suite installs*; Pillow is *test-and-release-only*) | `skills/verify/scripts/seal_stamp.py` stays stdlib-only, because `broad_gate.py`, `hooks/sealer-stamp.py` and `bin/seal-stamp` load it; the chart it reads is a text file beside it, opened with the standard library. The release PNG is rasterised by `rsvg-convert` (`librsvg2-bin`, a system package the `seal` job installs with `apt-get`), **a release-only dependency, never a plugin one**; `release_seal.py` imports no Pillow any more, and Pillow stays pinned where it is because the suite reads the PNG with it. No Python package is added anywhere |
| `docs/the-broad-gate.md` §*Where the stamp is drawn*, the #717 paragraph (`MESSAGE_LIMIT`, the ladder, *a seal keeps its disc*) and the paragraph *What the person's screen shows is not checked* | The hook's message stays under `MESSAGE_BUDGET`. The ladder keeps its one rung (S5): the disc has one size, so there is nothing below 0.90 to step to, and the step after it is still the text block alone. The budget paragraph's sentence *the owner's disc is drawn 14 cells across at every scale* is amended to 28, and the screen paragraph's sentences about the parchment's contrast on white and black (*1.02 and 1.48 to 1 … 20.5 and 14.2*) are amended to say nothing outside the disc is painted, so the stamp reads in the terminal's own theme and the owner still reads the first real seal on each background — both in the commit that changes the drawing (§14), each `Enforced by:` line kept |
| `docs/branch-and-release.md` §*Every act the release performs once it reaches `main`*, the bullet *Then the release's seal is attached* (#718) | The seal is still a second act that never fails the release. The bullet's *draws one seal for the release from the broad gate's letter* is amended to say the image is the owner's SVG rasterised, and the counts stay on the line under it |
| `docs/release-checklist.md` §6, the box *A GitHub Release exists at `vX.Y.Z`* | `DRY_RUN=1 python3 .github/scripts/release_seal.py` keeps drawing one by hand where `rsvg-convert` is installed; the box stays true and gains nothing but the new look |
| `skills/verify/SKILL.md` §*A seal says what it did not answer* and `agents/sealer.md`, which name the `CI also` row and its *<n> more steps* reading (pinned by `test_the_documents_name_the_ci_also_row`) | The row keeps its label — seven columns already, the owner's own wording from #717, named in two instructing documents — and gains the dim `·` the owner's design puts on a row that is not a pass (S5a). The mock's `flow` renamed the fixture's `workflow`, which the real panel has not carried since #717; the reason the owner gave for the rename, the seven-column label, is met by `CI also` as it stands. Overturning this is one word in `panel`, two documents and one case |
| `.github/scripts/publish_release_note.py`, module docstring (*The summary adds no way to fail*) and `release_seal.py`'s (*Any failure leaves the note as it was published*) | A missing `rsvg-convert`, a nonzero exit from it, a missing or unreadable SVG — each is one log line and one `::warning::` with exit 0 (S9) |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `CONTRIBUTING.md` (*Python 3.12 is the supported floor*) | New code in `release_seal.py` uses no `zip(..., strict=)` and no `*.UTC`, or carries the guard block. `seal_stamp.py` already carries `FLOOR` and `below_floor` |
| Work item 1791076830 (*every file the plugin reads or writes names its encoding*, shipped in 0.19.0) and its checker | The chart file is opened with `encoding="utf-8"` named, like every other file `seal_stamp.py` opens |
| `CLAUDE.md` §*a change writes fragments, never the shared file*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* (`Ledger frozen from` is declared in `seal/config.md`) | Changelog in `seal/specs/1791270164-…/changelog.md`, both entries rewritten. Rows in `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`: its `Corrected · L1`, `L2`, `L3`, `S2`, `B1`, `B2` and `D2` rows describe the 14-cell disc on the parchment sheet and are **rewritten in place** — the fragment is this work item's own unreleased file — and the released rows they correct stay corrected by them; the released rows about the sheet, the frame and `letter` that this work makes false (0.17.0's letter rows, 0.15.7's panel rows, 0.10.0's) gain citing corrections |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures keep `example/repo`, `example.com`, `/Users/x/`; the gallery README names the owner's machine as `~` |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* and `tests/test_one_word_one_meaning.py` | Every comment over the disc's colours and chart says *the disc's mark* or *the seal's mark*, never a bare *the mark*: phase 1 met `test_no_instructing_document_leaves_an_instance_anonymous` on exactly that word |
| `broad_gate.panel`'s docstring (*Separators are ASCII — ` . ` and `->` — because the letter twin exists for a console that is not UTF-8, where `·` and `→` print as `?`*) | The owner's design uses `·`, `✓` and `─`. The rows carry the owner's characters, and the **twin** maps the four to ASCII (`·` → `.`, `✓` → `+`, `─` → `-`, `→` → `>`) where it writes them, so the console the twin exists for still gets a printable line (S4). The docstring's sentence is amended to say so |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is *every place the parchment sheet, its four 256-colour codes, its edge and frame, the 14-cell disc, its four colours, its 7 × 10 chart, the square-clash layout, the bottom-right placement, the wrapped or ASCII-separated rows, the § as the mark, or `docs/seals/` is described or pinned*, enumerated in S8 and S10. Every changed line a person reads is pinned in the same commit. Every new case is seen red first and the hand-back says how |

## Scope

### In

1. **The disc is 28 cells across, 14 lines, computed.** `DISC_CELLS = 28`;
   `c = (n − 1) / 2`, `r = n / 2`; a cell at `(x, y)` with `dx = x − c`,
   `dy = y − c`, `d = hypot(dx, dy)` and `lit = (dx + dy) / (|dx| + |dy|)`
   (−1 at the upper left, +1 at the lower right) is, from the outside in:
   **outside** if `d > r − EDGE_INSET` (0.2); the **wax edge** `WAX_EDGE` if
   `d > r − WAX_INSET` (1.2); the **rim** if `d > r − RIM_INSET` (3.2) —
   `RIM_LIT` where `lit < −LIT_AT` (0.35), `RIM_DARK` where `lit > LIT_AT`,
   else `RIM_MID`; the **groove** if `d > r − GROOVE_INSET` (4.2) —
   `RIM_DARK` where `lit < 0`, else `RIM_LIT`; else the **field**, where the
   disc's mark is pressed (2). Every cell is exactly one of nine triples.
2. **The mark is one chart file, read as data.** `skills/verify/scripts/seal-mark.txt`,
   28 lines of 28 characters over the alphabet `.M`, is the owner's
   placeholder S (`chart28-S.txt` as the orchestrating session drew it,
   copied character for character). `read_chart(path)` reads it with its
   encoding named and refuses, with a sentence naming the path and the
   fault, a file that is not 28 lines of 28 over `.M`; `CHART` is its
   lines. A field cell under an `M` is `LIGHT` where the cell up-left is
   not under one, else `INNER` where the cell down-right is not under one,
   else `FACE`; a field cell not under an `M` whose up-left neighbour is
   under one is `DROP`; every other field cell is `FIELD`. **Changing the
   mark is changing that file alone**: no case pins the S's shape, and
   every case that touches the mark reads the chart as data (S1, S2).
3. **The stamp is the disc at the left and an open text block at the
   right; nothing else is drawn.** No parchment, no edge, no frame, no
   background colour on any cell outside the disc. The text block begins
   `GAP` (3) columns right of the disc's last column: its first line is the
   title — `SEALED ` in bold (SGR 1) and the seal's red `TITLE_RED`
   (196, 40, 44), then a dim (SGR 2) rule of `─` to the block's width — its
   second line blank, then one line per row: the label padded to
   `LABEL_WIDTH` (7) columns and a space, dim, then the value in the
   terminal's own foreground, a leading `✓` in green (SGR 32) and a leading
   `·` dim. A `None` row is a blank line. The block's width is its longest
   line; the stamp's height is `max(text lines, DISC_LINES)`, and the disc
   and the text block are each centred on it (`top_disc = (height −
   DISC_LINES) // 2`, `top_text = (height − text lines) // 2`). No line
   carries a trailing blank cell beyond the block's width or the disc's.
   The reference is `~/Desktop/specseal-frame-3-open.ans` on the owner's
   machine: 14 lines, 77 columns, 5,119 characters, drawn over `frames.py`'s
   `ROWS` (S3).
4. **The panel's rows take the owner's shape, in `broad_gate.panel`**, the
   one place that owns them (S5a): `base` joins commit and ref; a `None`
   row separates the identity rows from the result rows; the suite's
   counts join with ` · ` behind a `✓`; the ledger's row is `✓ <ok> ok ·
   <d> drifted · <b> broken`; a `chain ✓ exit <code>` row returns; `CI
   also` takes a dim `·`; the separators `.` and `->` become `·` and `→`;
   `PANEL_VALUE_WIDTH` becomes the width that keeps the stamp's widest line
   inside 80 columns. `wrapped` and `fit` stay for a value that is still too
   long.
5. **The encoding is lean** (S11): the block form's writer emits a code only
   where the foreground, the background or the style changed, puts every
   part in one SGR, writes no reset inside a line, and ends a line that
   holds a code with `\x1b[0m`. The sheet's four 256-colour codes retire
   with the parchment; the disc's nine triples are the only colours set.
6. **The twin writes nine letters for the disc's colours and the text as
   itself**, the three non-ASCII characters mapped (S4), with the same
   footprint as the block form and no frame.
7. **The release PNG is the owner's SVG with the S as its mark** (S6, S7,
   S9), the held phase-5 work kept where it does not depend on the mark:
   `rasterise`, `SVG`, `SEAL_PX`, `DENSITY`, `sealed_glance`'s `<img width>`
   with its escaping, the removal of the Pillow units, the rewritten
   docstrings, the cases of S6, S7 and S9, and Q4's answer.
8. **The hook's message re-measured** (Q3): one stamp per message, as in
   the lily's day, pinned under the budget by the real `fitted` message
   (S5).
9. **The seal gallery moves to `assets/seals/`** and gains `candidates/`
   with the § and the key at 28 cells and the light-red § at 14 — the last
   with a note that it was built on the parchment sheet — each as its
   chart, its `.ans` and a PNG preview, named in the README as candidates
   for #857 (S10). `docs/seals/` leaves the tree and its README leaves
   `tests/test_docs_line_wrap.py#COVERED`.
10. **The pins that follow** and the documents that describe the drawing
    (S8).

### Out

- **The mark's design.** The S is a placeholder by the owner's decision,
  and what replaces it is #857 (0.21.0). Nothing here chooses a mark.
- **Redrawing 0.18.0–0.19.0's release images.** Nothing in the tree can do
  it unattended (Q2). `DRY_RUN=1` from a checkout at the tag is the by-hand
  path and stays.
- **The budget constants, the default, the band, the release rows.**
  `release_rows`, `LABELS`, `MESSAGE_LIMIT`, `MESSAGE_RESERVE`,
  `MESSAGE_BUDGET`, `DEFAULT_SCALE` (0.90), `SCALE_FLOOR` (0.75),
  `SCALE_CEILING` (1.0), `SCALE_LADDER` (`(0.90,)`) are unchanged.
- **What `scale` does to the drawing: nothing**, as phase 3 left it;
  `check_scale` and the two refusal sentences stay. Retiring `--scale` and
  the band is a work item of its own (`plan.md` §Alternatives).
- **The failure form.** `not_sealed` is unchanged: words, no drawing.
- **The hook's label line** above the block (`label`), the values files'
  schema, `write_values`, `read_values`, `pending`, `claim`, `pick_shape`,
  `is_terminal`.
- **`Letter.disc`** stays, `(left, 2 · top_disc, 28, 28)`: the layout case
  reads it (S3).
- **Pillow's version**, `run_tests.py#PACKAGES`, the `seal` job's `pip
  install` line.
- **A fleur-de-lis**, the **area-averaged §**, the **24-cell disc**, the
  **blended edge**, the **corner overhang**, the **cell-for-cell PNG**, the
  **14-cell light-red §** as the shipped mark, and now the **parchment
  sheet** with its edge, its frame, its 256-colour codes and its widening
  rule: decisions 1–6 as the owner has closed them.
- **The `seal-stamp` command line.** `--shape`, `--scale`, `--from` keep
  their shape and their help.
- **A gallery entry for the shipped stamp.** `assets/seals/README.md`'s
  *The next entry* paragraph already says an entry is added when its
  release is tagged; 0.20.0's entry is the release's act.
- **Older values files.** A file an older gate wrote carries the old row
  shapes (`suite 768 passed, 1 skipped` on continuation rows, `base` and its
  ref on two rows, no `None`); the hook draws whatever rows the file
  carries, in the new layout, and nothing converts them.

### What phase 3 built that decisions 5–6 keep, and what they replace

**Keeps** (every one of these stands at 35277597 and is re-aimed by no
case): `admitted`, `fitted`, the budget constants, the one-rung ladder with
the one-per-`Stop` claim rule and the way the hook's message is measured
(UTF-16 units through `stamp`); `check_scale`, `SCALE_REFUSED` and
`SCALE_TOO_LARGE` as phase 3 reworded them; `DEFAULT_SCALE`'s,
`SCALE_FLOOR`'s and `SCALE_LADDER`'s comments where they say the disc is
one size; `letter_row` as a lookup; the disc computed from `hypot` with
`EDGE_INSET` (`test_the_disc_is_symmetric_because_it_is_computed`,
`test_the_disc_draws_the_same_bytes_in_every_process`);
`test_the_ladder_steps_down_in_order_and_ends_with_no_disc` and
`test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it` as phase 3
left them; `test_two_files_in_one_turn_are_under_the_budget_together`;
`Letter`'s four fields; `not_sealed`, the values files and the hook.

**Replaces** (the smith greps before each change):

- `DISC_CELLS` 14 → 28, `DISC_LINES` 7 → 14; `RING_INSET` → `WAX_INSET`,
  `RIM_INSET`, `GROOVE_INSET`, `LIT_AT`; the `CHART` tuple → `read_chart`
  over `seal-mark.txt`; `WAX_M`, `FIELD` (its triple), `MARK`,
  `MARK_SHADOW`, the four-colour `DISC_COLOURS` → the nine; `KEY` → nine
  letters;
- `PARCHMENT`, `SHEET_EDGE`, `INK`, `TITLE`, `TEXT_LEFT`, `PANEL_WIDTH`,
  `letter`, `sheet_text`, `compose`'s sheet, square-clash search and edge,
  `block`'s painted-space and parchment rules, `colour_row`'s per-side
  codes and resets, `sgr`'s 256-colour branch → the open layout of (3),
  `text_lines`, `TITLE_RED`, `LABEL_WIDTH`, a four-field cell and the lean
  writer of (5); `GAP` keeps its name and value with the new meaning;
- in `broad_gate.py`: `PANEL_VALUE_WIDTH` 23 → 41, `panel`'s rows as (4),
  `item_value`'s and `rounds_rows`'s separators, `SAMPLE_ROWS` and the
  tests' `FULL_ROWS` and `ROWS` to the new shape;
- the module docstring's and `build`'s, `compose`'s and `admitted`'s
  docstrings' sentences about the sheet, 14 cells, four colours and the
  right edge; `panel`'s docstring's row table and its *Separators are
  ASCII* and *No row is `None` since #717* paragraphs;
- `docs/the-broad-gate.md`'s sentence *14 cells across* and its parchment
  contrast sentences;
- the cases `test_the_mark_is_the_owners_hand_drawn_chart`, <!-- NAME NOT IN TREE -->
  `test_the_disc_is_fourteen_cells_of_exactly_four_colours`, <!-- NAME NOT IN TREE -->
  `test_the_emblem_is_lit_from_the_upper_left`, <!-- NAME NOT IN TREE -->
  `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text`, <!-- NAME NOT IN TREE -->
  `test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell`,
  `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`,
  `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame`, <!-- NAME NOT IN TREE -->
  `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours`,
  `test_a_coloured_row_carries_fewer_colour_sequences_than_cells`,
  `test_several_files_come_out_as_one_message_oldest_first`,
  `test_the_suite_carries_its_counts_and_nothing_under_them`,
  `test_the_ledger_carries_its_ok_count_and_nothing_beneath`,
  `test_a_base_that_is_its_own_commit_has_no_ref_row_under_it`,
  `test_a_list_too_long_for_its_row_continues_beneath_it`,
  `test_the_sample_carries_every_row_the_panel_can`,
  `test_the_values_file_holds_this_runs_panel`, the panel-width case, and
  the docstring, policy and floor sentence pins — as S1–S5a and S8 say;
- the changelog fragment's two entries and the ledger fragment's seven
  corrected rows, which describe the 14-cell disc on the parchment sheet.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the mark is one chart file | Given `skills/verify/scripts/seal-mark.txt`, when the module imports, then `CHART` is its 28 lines of 28 over `.M`, read through `read_chart` with `encoding="utf-8"`; every `M` lies inside the groove (`d ≤ r − GROOVE_INSET`), so no mark cell is ever a rim cell; `read_chart` over a file of 27 lines, of a 29-character line, or carrying a character outside `.M` raises `ValueError` with `CHART_MALFORMED` naming the path and the fault. Nothing asserts which letter the chart draws | `test_the_disc_mark_is_one_chart_file_read_as_data`: the file re-read in the case and compared to `CHART`, the groove bound over every `M`, the three malformed files under `tmp_path`; seen red by one `M` moved onto the rim in a copy handed to `read_chart`, and by the shape check removed <!-- NAME NOT IN TREE --> |
| S2 · the frame is computed, every cell one colour | Given a scale in the band, when `build(scale)` is asked, then it returns `(28, 28, px)` at every scale, and over the 784 cells `px` is `None` for 176, `WAX_EDGE` for 84, `RIM_LIT` for 98, `RIM_MID` for 30 and `RIM_DARK` for 96 — the frame's counts, which no chart moves — and one of `FIELD`, `FACE`, `LIGHT`, `INNER`, `DROP` for the 300 inside the groove, split by the rule of *Data & interfaces* over `CHART` (the case rebuilds the rule in its own body from the chart and the nine triples and compares cell for cell); `set(px values) − {None} == set(DISC_COLOURS)` | `test_the_disc_is_twenty_eight_cells_in_the_frames_nine_colours` (replacing `test_the_disc_is_fourteen_cells_of_exactly_four_colours`): the five frame counts, the 300, the cell-for-cell comparison at 0.75, 0.90 and 1.0; seen red by `RIM_INSET = 3.0` and separately by `LIT_AT = 0.5`. `test_the_disc_draws_the_same_bytes_in_every_process` and `test_the_disc_is_symmetric_because_it_is_computed` green unchanged <!-- NAME NOT IN TREE --> |
| S2a · lit from the upper left | Given `build`, when the rim and the groove are read, then every rim cell with `lit < −LIT_AT` is `RIM_LIT` and with `lit > LIT_AT` is `RIM_DARK`, every groove cell with `lit < 0` is `RIM_DARK` and otherwise `RIM_LIT`; and over the field, every `LIGHT` cell's up-left neighbour is not under the chart, every `INNER` cell's up-left is and its down-right is not, every `DROP` cell is not under the chart and its up-left is | `test_the_disc_is_lit_from_the_upper_left` (renamed from `test_the_emblem_is_lit_from_the_upper_left`); seen red by the groove's test flipped (`lit > 0`) and separately by the drop shadow taken from `on(x + 1, y + 1)` <!-- NAME NOT IN TREE --> |
| S3 · the disc at the left, the open text block at the right, nothing else | Given rows and a scale, when `compose(rows, scale)` is asked, then `lines = text_lines(rows)` (S3a), `height = max(len(lines), DISC_LINES)` (with the disc; `len(lines)` without), `top_disc = (height − DISC_LINES) // 2`, `top_text = (height − len(lines)) // 2`, `Letter.disc = (0, 2 · top_disc, 28, 28)`; a cell inside the circle is its `px` colour on both halves as the disc's row pair gives them; every other cell in the disc's 28 columns is empty (no character, no colour); the text block's cells begin at column `DISC_CELLS + GAP` and carry `text_lines`' characters with their styles; no cell anywhere outside the circle has a background; `width` is `DISC_CELLS + GAP + the block's width`, and no line is longer than its own content (a line with no text ends at the disc's last painted cell, a line past the disc at its last character). `scale` None leaves the disc off and the block begins at column 0 — the last rung `fitted` steps down to | `test_the_disc_stands_left_of_the_open_text_block_each_centred` (replacing `test_the_disc_sits_inside_the_sheet_against_its_right_edge_three_clear_of_the_text` and `test_the_text_is_written_on_a_sheet_one_blank_line_inside_it`): over `FULL_ROWS`, `SAMPLE_ROWS`, `SMALL_ROWS` (height 14, the text's top at 5) and `[]`, the case rebuilds the rule in its own body and asserts every cell of `compose` equal to it, no background outside the circle, and that with `GAP` set to 0 the block begins at column 28; seen red by the disc placed one line down and separately by the text one column left. **And** `test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell` re-transcribed from `~/Desktop/specseal-frame-3-open.ans` over `frames.py`'s `ROWS` as its fixture (the mock's rows, which carry the owner's shapes and a `flow` label the real panel does not — a fixture is data): the 14 lines of the twin's letters compared cell for cell, and the block form's plain text (codes stripped) equal to the file's; seen red by the chart's first `M` moved <!-- NAME NOT IN TREE --> |
| S3a · the text lines | Given rows, when `text_lines(rows)` is asked, then the first line is `("SEALED ", bold, TITLE_RED)` followed by `("─" × k, dim)` where `k` makes the title line as wide as the widest row line (and at least `RULE_MIN` (30), the mock's width, where every row is shorter); the second is blank; then one line per row — a `None` row blank; a row's label padded to `LABEL_WIDTH` (7) and a space, dim; its value in the default foreground, except a leading `✓ ` whose `✓` is green and a leading `· ` whose `·` is dim; a `""` label is seven spaces and a space, so a continuation row's value stands under the row above it. The title row `("SEALED", "")` that `panel` returns first is what makes the title; rows without it draw no title | `test_the_text_lines_are_a_red_title_a_rule_and_the_rows_under_it`: over `SAMPLE_ROWS` and `frames.py`'s `ROWS`, every line's characters and styles; seen red by the rule one short and separately by the label width 8 <!-- NAME NOT IN TREE --> |
| S4 · the twin's letters | Given a cell, when `letter_row` writes it, then a disc cell is `KEY[top]`, else `KEY[bottom]`; a text cell is its character, with `·` → `.`, `✓` → `+`, `─` → `-`, `→` → `>`; an empty cell is a space; the twin's lines have the block form's footprint | `test_the_twin_writes_the_discs_nine_letters_and_the_text_in_ascii` (replacing `test_the_twin_writes_the_discs_four_letters_over_the_sheets_frame`): `KEY` is exactly the nine pairs of *Data & interfaces*, every twin character over a disc cell is its colour's letter, every twin line is ASCII, and `test_the_twin_and_the_block_form_have_equal_width_and_height` green unchanged; seen red by two letters made equal and separately by the `✓` mapping removed <!-- NAME NOT IN TREE --> |
| S4a · the colours on the wire | Given the block form at 0.90, when its SGR sequences are read, then the only colour parts are `38;2;…`/`48;2;…` over exactly the nine triples of `DISC_COLOURS` and `38;2;196;40;44` for the title, the only other parts are `1`, `2`, `22`, `32`, `39`, `49` and the line-end `0`; no `;5;` (256-colour) part is left, and nothing of the rope, the gold, the 24-cell rim's two ends, the lily's (226, 82, 74) or the 14-cell disc's (168, 26, 30), (120, 16, 20), (240, 130, 118) | `test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours` re-aimed: the set of triples equals `set(DISC_COLOURS) ∪ {TITLE_RED}`, the set of non-colour parts is exactly `{1, 2, 22, 32, 39, 49, 0}`, no `;5;`, the old exclusions kept and the three 14-cell triples added; the name still says *four codes and five colours*, because a released ledger row cites it, and its docstring says why |
| S5 · the budget: one stamp per message | Given `SCALE_LADDER` is `(0.90,)`, when `admitted` lays blocks, then it carries as many of the oldest as fit together with their disc, and one block alone that does not fit is the text block with no disc — the rule as it stands. The reference is 5,119 characters for the mock's rows at 77 columns (`read`); the real panel's rows are of the same length, so one real run per message, as in the lily's day, and no two blocks of any fixture share one (two of the reference are 10,240). Phase 6 measures the built `fitted` message through `stamp` over `FULL_ROWS`, `ROWS`, `SAMPLE_ROWS`, `SMALL_ROWS` and the widest panel, and the fragment records it (Q3) | `test_several_files_come_out_as_one_message_oldest_first` back to phase 2's shape and name, `test_several_files_come_out_one_stop_each_oldest_first`: the pair of `SMALL_ROWS` blocks is over the budget together (premise asserted) and comes out one per `Stop`, oldest first, each with its disc, the broken file left pending. `test_the_hooks_message_is_under_the_budget_for_one_file` pins one real-size stamp under `MESSAGE_BUDGET` through the real hook; `test_two_files_in_one_turn_are_under_the_budget_together`, `test_seals_past_what_one_message_carries_wait_for_the_next_turn`, `test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it`, `test_the_ladder_steps_down_in_order_and_ends_with_no_disc`, `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` green (Q14) <!-- NAME NOT IN TREE --> |
| S5a · the panel's rows, in the one place that owns them | Given a sealed run's inputs, when `panel` is asked, then its rows are, in order: `("SEALED", "")`; `("tree", <tree>)`; `("", <branch>)` where there is one; `("base", "<commit>  <ref>")` — two spaces, the ref `fit` to its tail — or `("base", <commit>)` where the ref is the commit; `("item", "#<pr> · <id>")` or `<id>`; `("gate", <copy>)` where there is one; `None`; `("suite", "✓ <counts joined by ' · '>")` on `wrapped` rows where `exit 0`, else `("suite", "exit <n>")`; `("ledger", "✓ <ok> ok · <d> drifted · <b> broken")` where the total line was read, else `exit <n>`; `("chain", "✓ exit <code>")`; `("CI also", "· <n> more steps")` where the repository has the workflow; the `rounds` rows with ` · capped` and `→`. `PANEL_VALUE_WIDTH` is 41 (80 − 28 − 3 − 8: the widest value that keeps the stamp's widest line inside 80 columns), and every value still passes `fit` | `test_the_suite_carries_its_counts_and_nothing_under_them`, `test_the_ledger_carries_its_ok_count_and_nothing_beneath` (renamed `test_the_ledger_carries_its_three_counts_on_one_row`), `test_a_base_that_is_its_own_commit_has_no_ref_row_under_it` (re-aimed: joined where there is a ref, alone where not), `test_a_list_too_long_for_its_row_continues_beneath_it` (over 41), `test_the_sample_carries_every_row_the_panel_can` (`SAMPLE_ROWS` in the new shape), `test_the_values_file_holds_this_runs_panel`, `test_the_documents_name_the_ci_also_row` (the dim `·` added to the documented reading), the panel-width case re-aimed to *the stamp's widest line is at most 80 columns with a value of `PANEL_VALUE_WIDTH`*, and a new `test_the_result_rows_carry_a_tick_and_a_blank_row_stands_before_them`; each seen red by the old shape put back <!-- NAME NOT IN TREE --> |
| S6 · the PNG is the SVG with the S | Given `.github/scripts/release-seal.svg`, when `seal_release` runs, then `rasterise(svg, png)` runs `rsvg-convert -w <SEAL_PX·DENSITY> -h <SEAL_PX·DENSITY> <svg> -o <png>` through `subprocess.run` and the PNG is attached as `seal.png`; the SVG parses as XML with `viewBox="0 0 32 32"`, the radial gradient `sealBg` with its three stops, the linear gradient `rimShade`, the two circles, and three `<path>` elements carrying the fills and opacities the owner's three `<text>` layers had (`#380709` at 0.9, `#c42830`, `#e65a61` at 0.5) at their anchors `(16.5, 21.5)`, `(16, 21)`, `(15.7, 20.7)` — one outline, Georgia Bold's **S** at font-size 20, each layer the same points moved by the offset between anchors, every point inside the groove — and **no `<text>` element**. Where `rsvg-convert` is on `PATH`, the PNG it writes is RGBA, `SEAL_PX·DENSITY` square, alpha 0 at its corners and 255 at its centre, a pixel within 8 per channel of `#c42830` somewhere in it, and the wax darker at the lower right than at the upper left | The held cases as written: `test_the_release_seal_svg_is_the_owners_with_its_text_as_paths` (its docstring says the glyph is the S since decision 5), `test_the_rasteriser_runs_rsvg_convert_at_two_times_the_display_size`, `test_rsvg_convert_draws_the_seal_transparent_round_and_in_its_colours` (skips with the reason where `shutil.which("rsvg-convert")` is None). The text-version-vs-path-version comparison for the S goes in `phases/phase-8.md`. `test_paint_lays_every_cell_in_the_colours_block_gives_it`, `test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted`, `test_rgb_is_xterms_table_and_a_triple_passes_through`, `test_the_seal_module_imports_without_pillow` retired with the units they pinned <!-- NAME NOT IN TREE --> |
| S7 · the note shows it at display size | Given the PNG at `DENSITY` (2) × `SEAL_PX` (160) and the published note, when `sealed_glance` writes the block, then the image line is `<img src="<url>" alt="<alt>" width="160">` with the URL and the alt escaped for their attributes, and the counts line follows as today; `alt_text` is unchanged | `tests/test_a_release_publishes_its_note.py`, the `sealed_glance` case as the held patch amended it, plus `test_the_seal_job_installs_rsvg_convert_before_the_suite_and_the_draw` and the step count six; GitHub's sanitiser keeps `width` (Q4, measured) <!-- NAME NOT IN TREE --> |
| S8 · the documents and pins follow (§12's class) | Every place that describes the parchment sheet, its codes, edge or frame, the 14-cell disc, its four colours, its chart, the square-clash layout, the bottom-right placement, the wrapped or ASCII-separated rows, the § as the terminal's mark, the area sampler, the corner overhang or the cell-for-cell PNG says what the code now does: `seal_stamp.py`'s module docstring and the comments over the palette, `KEY`, `DISC_CELLS` and the insets, `GAP`, `build`'s, `compose`'s, `text_lines`', the writers' and `admitted`'s docstrings; `broad_gate.panel`'s docstring and `PANEL_VALUE_WIDTH`'s comment; `docs/the-broad-gate.md`'s two paragraphs; `docs/branch-and-release.md`'s bullet; `skills/verify/SKILL.md`'s and `agents/sealer.md`'s `CI also` sentences (the dim `·`); `release_seal.py`'s docstring; `run_tests.py`'s sentence *pins that drawing against the terminal form*; `.github/workflows/publish-release.yml`'s comments over the `seal` job; `tests/test_the_seal_is_taken_once_by_the_sealer.py`'s heading over the letter cases | `test_the_docstrings_describe_the_letter_and_the_rows_it_carries`, `test_the_policy_states_the_budget_and_names_its_case`, `test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it`, `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it`, `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence`, `test_the_documents_name_the_ci_also_row` re-aimed to the new sentences and green; `grep -n "parchment\|sheet\|14 cells\|four colours\|seven cells\|ten rows\|MARK_SHADOW\|WAX_M\b\|RING_INSET\|PARCHMENT\|SHEET_EDGE\|TEXT_LEFT\|against its right edge\|by area\|24 cells\|cell-for-cell\|docs/seals" skills/verify/scripts/seal_stamp.py skills/verify/scripts/broad_gate.py .github/scripts/release_seal.py .github/workflows/publish-release.yml docs/*.md skills/verify/SKILL.md agents/sealer.md tests/test_docs_line_wrap.py assets/seals/README.md` returns only history (round records, changelogs, ledger rows, the gallery's account of earlier emblems, `panel`'s history paragraphs) |
| S9 · failure still costs the image alone | Given `rsvg-convert` missing from `PATH`, or exiting nonzero, or the SVG missing, when `seal_release` runs, then the log says why on one `::warning::` line, exit 0, nothing uploaded or edited | `test_any_failure_leaves_the_note_as_it_was_published` with the held patch's three cases replacing *Pillow does not import*, *compose raises*, *compose exits* and *the PNG writer exits* |
| S10 · the gallery moves and names its candidates | Given the tree, when it is read, then `docs/seals/` is gone and `assets/seals/` holds `README.md`, `gold-lily.ans`/`.png`, `red-lily.ans`/`.png` byte for byte as 6d0096b0 committed them, and `candidates/` with `section-28.txt`/`.ans`/`.png`, `key-28.txt`/`.ans`/`.png` and `section-14-light-red.txt`/`.ans`/`.png`; the README's gallery paragraphs are as they were, with a *Candidates for #857* section that says what each is, that the two 28-cell ones were drawn by the orchestrating session's reference renderer over a sample panel on the parchment sheet and not by `seal_stamp.py`, that a 28-cell chart becomes the shipped mark by replacing `skills/verify/scripts/seal-mark.txt` with it, and that the 14-cell one was the shipped stamp between 35277597 and this work's next commit to the drawing **and was built on the parchment sheet, which decision 6 retired**; `tests/test_docs_line_wrap.py#COVERED` no longer names `docs/seals/README.md`; no code reads any file under `assets/seals/` | `read`: `git ls-files docs/seals` prints nothing and `git ls-files assets/seals` prints the fourteen files; `cmp` of each moved file against `git show 6d0096b0:docs/seals/<name>`; `bin/test tests/test_docs_line_wrap.py` green with the entry removed (the list is opt-in and only `README_PAIR` constrains it, read 2026-10-07); the README read once by the reviewer. No case is added: the gallery is documentation no code path reaches |
| S11 · the encoding is lean | Given any line of the block form, when its bytes are read, then every SGR is written where the foreground, the background or the style of the next cell differs from the running state and nowhere else; the parts of one change are in one SGR (`\x1b[…;…m`), so no two SGRs are adjacent; `\x1b[0m` appears only at the end of a line that holds a code; a blank cell with no background writes no code and leaves the running state; a cell's foreground is written only where the cell has a visible character or a half-block | `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` re-aimed to `test_a_line_writes_one_sgr_per_change_and_no_reset_inside_it`: over the real-run block and the disc alone, no `m\x1b[`, no `\x1b[0m` before a line's last character, the count of SGRs equal to the count of state changes the case computes from `compose`'s cells, and the real-run block under 5,500 units with the label (the reference's 5,119 plus the label's length and the real rows' difference); seen red by the parts split into two SGRs, and separately by a reset written at every colour change <!-- NAME NOT IN TREE --> |

## Data & interfaces

- **The disc's palette** (truecolour triples), the owner's as `seal28.py`
  holds them: `WAX_EDGE` (150, 24, 28); `RIM_LIT` (208, 68, 64), `RIM_MID`
  (160, 30, 34), `RIM_DARK` (96, 10, 14); `FIELD` (112, 16, 20); `FACE`
  (186, 38, 42), `LIGHT` (222, 86, 78), `INNER` (90, 8, 12); `DROP`
  (84, 8, 12). `DISC_COLOURS` is these nine, in this order. **The text's
  colours**: `TITLE_RED` (196, 40, 44) for the title, as `frames.py`'s
  `RED`; everything else is the terminal's own — SGR 39 for a value, SGR 2
  for a label, the rule and a leading `·`, SGR 32 for a leading `✓`, SGR 1
  for the title. The four 256-colour sheet codes are gone. <!-- NAME NOT IN TREE -->
- **The disc's numbers**: `DISC_CELLS = 28`; `DISC_LINES = DISC_CELLS // 2`
  (14); `EDGE_INSET = 0.2`, `WAX_INSET = 1.2`, `RIM_INSET = 3.2`,
  `GROOVE_INSET = 4.2`, in cells; `LIT_AT = 0.35`. <!-- NAME NOT IN TREE -->
- **A disc cell's colour**, for `(x, y)` in `0 ≤ x, y < 28`, `c = 13.5`,
  `r = 14`, `dx = x − c`, `dy = y − c`, `d = hypot(dx, dy)`, `lit = (dx +
  dy) / (|dx| + |dy|)` (guarded against zero as `seal28.py` does), `on(x,
  y)` true where `CHART[y][x]` is `M`:
  - `d > r − EDGE_INSET`: `None` (outside);
  - `d > r − WAX_INSET`: `WAX_EDGE`;
  - `d > r − RIM_INSET`: `RIM_LIT` if `lit < −LIT_AT`, `RIM_DARK` if
    `lit > LIT_AT`, else `RIM_MID`;
  - `d > r − GROOVE_INSET`: `RIM_DARK` if `lit < 0`, else `RIM_LIT`;
  - `on(x, y)`: `LIGHT` if not `on(x − 1, y − 1)`, else `INNER` if not
    `on(x + 1, y + 1)`, else `FACE`;
  - `on(x − 1, y − 1)`: `DROP`;
  - else `FIELD`.
  Frame counts over the 784 cells, which no chart moves: 176 outside, 84
  wax edge, 98 `RIM_LIT`, 30 `RIM_MID`, 96 `RIM_DARK`, 300 inside the
  groove. With the S chart the 300 split 185 / 37 / 31 / 16 / 31 over
  `FIELD` / `FACE` / `LIGHT` / `INNER` / `DROP` (measured by the framer,
  2026-10-07; no case pins the split, because the split is the chart's).
- **The chart file**, `skills/verify/scripts/seal-mark.txt`: 28 lines of 28
  characters over `.M`, a trailing newline, UTF-8, the placeholder S copied
  from `<scratchpad>/chart28-S.txt` (84 `M` cells over 14 rows).
  `read_chart(path) -> tuple[str, ...]` opens it with `encoding="utf-8"`
  and raises `ValueError` with `CHART_MALFORMED` — *seal-stamp: the disc's
  mark chart {path} is not {n} lines of {n} characters over `.M` ({fault}).
  Nothing was drawn.* — for any other shape; `CHART = read_chart(CHART_PATH)`
  at import, where `CHART_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
  "seal-mark.txt")`. <!-- NAME NOT IN TREE -->
- `seal_stamp.build(scale) -> (w, h, px)`, `w = h = DISC_CELLS` at every
  scale in the band, `px(x, y)` the rule above; `check_scale` still refuses
  outside the band.
- **A cell** is `(char, fg, bg, style)`: the character or `None` for an
  empty cell; `fg` a triple or `None` for the terminal's own; `bg` a triple
  or `None`; `style` one of `None`, `"dim"`, `"bold"`, `"green"`. A disc
  cell is `("▀", top, bottom, None)` for two colours, `("▀", top, None,
  None)` or `("▄", bottom, None, None)` for one, and empty for none — never
  a painted space, because nothing outside the disc has a background to
  paint. `Letter = namedtuple("Letter", "cells width height disc")` as
  today.
- `seal_stamp.text_lines(rows) -> list[list[cell]]`, S3a: `LABEL_WIDTH = 7`,
  `RULE_MIN = 30`, `TITLE_RED`; `GAP = 3`, *the clear columns between the
  disc's last column and the text block's first*. <!-- NAME NOT IN TREE -->
- `seal_stamp.compose(rows, scale) -> Letter`, the layout rule of S3; no
  `letter`, no `sheet_text`, no `TEXT_LEFT`, no `PANEL_WIDTH`.
- **The writers.** `colour_row(cells)` is S11's lean writer, after
  `frames.py#encode`: the running state `(fg, bg, style)`, one SGR per
  change holding, in order, `22;39` where a style ends then the new
  style's code (`1`, `2`, `32`), `38;2;r;g;b` or `39` where the foreground
  changes (not written for a green cell, whose colour is the style), `48;2;r;g;b`
  or `49` where the background changes; `\x1b[0m` at the end of a line
  that wrote a code. `letter_row(cells)` is S4's: `KEY` for a disc half,
  the character with `TWIN_ASCII = {"·": ".", "✓": "+", "─": "-", "→":
  ">"}` applied — one character for one, so the twin keeps the block
  form's footprint on every row, `SAMPLE_ROWS`' `deferred →` row included —
  a space for an empty cell. `block` and `sgr` retire. <!-- NAME NOT IN TREE -->
- `seal_stamp.KEY`, the twin's nine letters — the framer's choice, since
  the twin is for a console that cannot draw half-blocks and nobody chose
  it: `WAX_EDGE: "m"`, `RIM_LIT: "M"`, `RIM_MID: "n"`, `RIM_DARK: "N"`,
  `FIELD: "."`, `FACE: "X"`, `LIGHT: "Y"`, `INNER: "x"`, `DROP: "y"`.
  Capitals are lit, lower case is shadow; `m`/`.` are #30's letters for the
  wax and the field; `Y`/`y` are #717's for the lit and shadowed mark. <!-- NAME NOT IN TREE -->
- `seal_stamp.SCALE_LADDER = (0.90,)`; `admitted` as today over it;
  `stamp(rows, scale, shape)` as today.
- **`broad_gate.panel`** (S5a): `PANEL_VALUE_WIDTH = 41`; `SEP = " · "`,
  `ARROW = "→"`, `TICK = "✓ "`, `DOT = "· "` named once each; `item_value`
  → `#<pr> · <id>`; `rounds_rows` → ` · capped`, `<k> deferred → <homes>`;
  the row list as S5a. `wrapped(label, pieces)` unchanged in rule, the
  suite's pieces `["✓ 6621 passed", " · 11 skipped", …]`. `SAMPLE_ROWS` in
  `seal_stamp.py` and `FULL_ROWS`, `ROWS`, `SMALL_ROWS` in the hook's test
  module re-shaped to what `panel` returns (`SMALL_ROWS` keeps four rows). <!-- NAME NOT IN TREE -->
- `release_seal.SVG = os.path.join(HERE, "release-seal.svg")`,
  `SEAL_PX = 160`, `DENSITY = 2`, `rasterise(svg, png) -> None`;
  `sealed_glance(image_url, alt, width, …)` — all as the held patch wrote
  them. <!-- NAME NOT IN TREE -->
- **The SVG in the tree**: the held `p5-held/release-seal.svg` with each
  of its three `<path>` layers of the § replaced by a `<path>` of Georgia
  Bold's **S** at font-size 20, anchored where the owner's `<text>` layers
  were (`(16.5, 21.5)`, `(16, 21)`, `(15.7, 20.7)`), the same fills and
  opacities; the outline taken once with `fonttools` through `uvx` from
  `/System/Library/Fonts/Supplemental/Georgia Bold.ttf`, compared against
  a `<text>S</text>` version through `rsvg-convert` before committing; the
  file's comment names the placeholder and #857.
- **The gallery**: `assets/seals/README.md`, `gold-lily.ans`, `gold-lily.png`,
  `red-lily.ans`, `red-lily.png` moved with `git mv`; `assets/seals/candidates/`
  with `section-28.txt` (`chart28-section.txt`), `section-28.ans`
  (`~/Desktop/specseal-28-section.ans`, its caption line dropped),
  `section-28.png`; `key-28.txt` (`chart28-key.txt`), `key-28.ans`
  (`~/Desktop/specseal-28-key-big.ans`, caption dropped), `key-28.png`;
  `section-14-light-red.txt` (the 14 × 14 grid the 7 × 10 `CHART` of
  35277597 occupies at its offsets `(2, 4)`), `section-14-light-red.ans`
  (`~/Desktop/specseal-stamp-14.ans`, its label line dropped),
  `section-14-light-red.png`. Each PNG drawn as the gallery's others were
  — 12 × 24 pixels a cell, a half-block as its two halves, nothing painted
  transparent — by a scratch script over the `.ans` file with Pillow from
  the suite's environment. The README's *Candidates for #857* section says
  the two 28-cell ones and the 14-cell one all stand on the parchment sheet
  decision 6 retired, so only their discs are candidates.
- Ledger fragment `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`:
  rows for S1–S11 and the citing rows that correct 0.10.0 S2, 0.17.0 L1,
  L2, L3 and L4, 0.15.7's panel rows (N5, N7 where their claims name the
  sheet or the separators), 0.18.0 B1, B2 and D2, written with
  `evidence-check --reverify --into … --checked <date>` where a hash moved
  and by hand where a claim is false; the fragment's existing corrected
  rows rewritten in place for the open layout.

## Open questions → questions.md

Q1 and Q8 are history (the owner's decisions 3–6 supersede each other in
turn); Q3 is re-opened as a measurement; Q4 is measured; Q5, Q6 and Q7 are
moot. Q2 and Q9 are a person's and block nothing — Q9 records the PNG
default as a default the session proposed and the owner has not answered.
Q10 and Q14 are measurements, Q11 and Q13 are the work's, Q12 is the
mark's design (#857), and Q15 is the `CI also` label, decided from the
tree and open to one word from the owner.

The frame was redrawn on 2026-10-07 by framer, after the owner's look at
phase 2's stamp.

Framed 2026-10-06 by framer, before the build.
