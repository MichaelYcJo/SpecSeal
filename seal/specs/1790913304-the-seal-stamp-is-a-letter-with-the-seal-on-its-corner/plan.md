# Implementation Plan: the seal stamp is a letter with the seal on its corner

<!-- seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-10-02 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

Three vertical slices over two scripts, one hook and the documents that
describe them. Each slice changes what one surface prints, pins the new text
in the same commit after seeing the pin red, and moves the prose that named
the old text. `broad_gate.py#gate`, `#signal` and `#main`, the values file's
keys, the `NOT SEALED` form and every exit code are untouched throughout.

1. **The budget and the ladder.** The threshold is measured and named; the
   hook holds its whole message under a budget, stepping the seal down and
   then off. This slice ends the truncation on its own, over today's
   drawing, before anything is redrawn.
2. **The panel's rows.** `panel` drops `chain`, the `exit` and `drifted`
   continuations and the blank rows, and `workflow` becomes `CI also`; the
   sample, the cases and the two documents that name the rows follow.
3. **The drawing.** One compositor lays the text on a parchment sheet and
   presses the rope-less seal over its corner; two writers encode it, the
   block form in colour and the letter twin at the same footprint; the
   policy paragraph, the docstrings, the ledger corrections and the
   changelog fragment close the item.

Phase 1 goes first because it is the fix that holds whatever the design, and
because it gives phase 3 the number it is measured against. Phase 2 goes
before 3 because the drawing's size is a function of its rows, and the rows'
change is small.

## Technical context

**Where the text and the drawing are made** (all read 2026-10-02 at
`5180b89e`):

- `skills/verify/scripts/seal_stamp.py`: `ART` (104), `GOLD` (139),
  `ROPE_L`/`ROPE_D` (145), `WAX_L`/`WAX_M`/`FIELD` (146), `KEY` (149),
  `SCALE_FLOOR`/`SCALE_CEILING` (165–166), `DEFAULT_SCALE` (179),
  `check_scale` (198), `shrink` (216), `build` (252; the bands at 285–293,
  the chart lookup at 296–299), `sgr` (311), `colour_row` (318),
  `letter_row` (351), `PANEL_WIDTH` (363), `letter` (366), `strip_ansi`
  (387), `beside` (391), `stamp` (409), `pick_shape` (484), `is_terminal`
  (498), `read_values` (581; `null` rows accepted at 600–608), `label`
  (655), `SAMPLE_ROWS` (687), `main` (710), `drawn_from` (754).
- `hooks/sealer-stamp.py`: `STAMP` (63, the module beside the hook),
  `drawings` (96; `stamp.stamp(values["rows"], values["scale"],
  shape=False)` at 115), `main` (126; the one `print` at 150).
- `hooks/dispatch.py`: `MESSAGE_CAP` (53), `LABEL`/`CLOSING` (63–67),
  `GROUPS["stop"]` (92), `beside` (484), `report` (501; the prepend at
  513–521).
- `skills/verify/scripts/broad_gate.py`: `PANEL_VALUE_WIDTH`/`ELISION`
  (246–247), `fit` (250), `wrapped` (266), `ledger_counts` (2319),
  `rounds_rows` and `deferred_home` (phase 3 of #666), `panel` (2529–2660;
  the `chain` row at 2640, the `workflow` row at 2656, the blanks at 2622,
  2655, 2658), `failure_lines` (2663), the terminal branch of `gate`
  (2970–2984), `signal` (3080), `main` (3131), the module docstring's stamp
  paragraph (68–82).
- The prototype, in the orchestrating session's scratchpad under `stamp/`
  (the spawn prompt carries the absolute path): `narrow.py#sheet` is the
  layout, `env3.py#sealf` the disc (`outer=0.84`, the two neighbour tests),
  `envelope.py#encode` the writer (the fixed one, keeping painted trailing
  spaces), `envelope.py#code` the two SGR forms, `rows.py#trimmed` the row
  trim, `letter.py` the four 256-colour codes. Throwaway: ported, not
  copied. One script depends on the next by `exec`, so read them as one
  program.
- Tests: `tests/test_the_seal_is_taken_once_by_the_sealer.py` (Part 1,
  143–450; `ROWS` 46–61; `crown_of` 742; `checks_with` 2835; the width case
  2854–2918; `capped_record`/`record_of` 3136–3154; A5 2504; the suite and
  ledger row cases 2950–2990; the sample case 3107),
  `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` (`ROWS`
  26–42; `values()` 56; `stop()` 239; `message()` 256; the S3–S6 cases
  261–389; the scale cases 566–596),
  `tests/test_the_gate_names_every_step_ci_runs.py` (`FIXTURE_WORKFLOW`
  509; `panel_rows` 533; A6 556–608; `HISTORICAL_ROWS` 712; the real-workflow
  cases 1163–1210), `tests/test_the_gate_asks_the_range_ci_will_ask.py`
  (549–571; 1041–1069), `tests/test_a_gate_that_fails_says_so.py` (S9,
  588–631).

**Constraints the design is chosen under.**

- The limit is the harness's, counted in characters, bracketed at
  9,919 < limit ≤ 10,090 by what the harness has already drawn and
  persisted (`spec.md` §*What was measured*), and most likely 10,000.
- `hooks/dispatch.py#report` prepends text to the same message after the
  hook has printed; the hook cannot measure it, so the budget carries a
  reserve.
- The sheet's width is bounded by `PANEL_VALUE_WIDTH`; its height is not,
  because two lists wrap onto continuation rows.
- The twin and the block form walk one set of cells
  (`seal_stamp.py` 304–308, *one footprint*), and three cases hold them to
  it.
- A values file written by the tree's gate is drawn by the installed hook
  (0.16.0 today), and a file written by an older gate may still be pending
  when the new hook draws it; both directions must stay drawable.
- `letter` decides the value width and a case in another module measures
  it by rendering (`test_the_panel_value_width_is_what_the_stamp_actually_gives`).
- `seal_stamp.py` and `broad_gate.py` are swept by
  `tests/test_one_word_one_meaning.py`: a bare *the seal* for the drawing is
  refused.

**What breaks in six months.** The harness moves its limit: a lower one
truncates again, and the only sign is the owner's screen — `MESSAGE_LIMIT`'s
comment names the probe so the next measurement is one scratch hook away;
a higher one costs nothing. A twelfth labelled row is added to `panel` and
the widest-panel case is not extended: A5 still measures what it measures,
and the ladder catches the overflow at draw time rather than in the suite —
named, not closed. A terminal theme whose default background is the sheet's
cream makes the sheet vanish; nothing reads the background and S6 says so.
`dispatch.py` grows a longer report than the reserve: a stamp beside a
multi-gate failure report could persist again, and the reserve's comment is
where the next reader finds the two numbers to compare.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Measure the budget per block and step each stamp down on its own | Two seals in one turn come out at two scales, and a third pushes the message over while each block alone fits | Rejected; one rung per message, chosen as the highest at which every block fits together |
| Apply the budget in `dispatch.py`, which assembles the final message | It would need a second renderer to step a stamp down, and a `systemMessage` it cannot shrink it could only drop | Rejected; a reserve inside `MESSAGE_BUDGET` covers what `report` prepends, with the reason written beside it |
| Leave a file pending when its block does not fit, and draw it next turn | The same block is the same size next turn, so it is never drawn and never claimed; a file pending forever is drawn by nobody | Rejected; the last rung has no seal and fits every panel the tree can produce, which is stated as a bound (S1) rather than guarded by a mechanism |
| Truncate the sheet's continuation rows to fit at the last rung | Cuts the deferred homes, which are the one list a reader acts on, to save a case nobody has produced | Rejected; named as the bound's edge |
| Rewrite the values file's `scale` to the rung drawn | Two writers of one file, and the file records what the gate asked for; a terminal draws at `--scale` without recording it either | Rejected |
| Set `MESSAGE_LIMIT` to 10,000 by reading the bracket and skip the probe | Leaves 90 characters of the bracket unexplained, and a definition that says *measured* over a number nobody measured is the counterfeit `CONTRIBUTING.md` refuses | Rejected as the first choice; kept as the fallback, labelled read, where the nested session cannot run |
| Drop the letter twin and give a non-UTF-8 console the sheet alone, with no seal | Loses the drawing for the console the twin exists for and for `seal-stamp` on a pipe, makes `0.10.0` S2's footprint claim false, and moves `crown_of` and every case that renders through `shape=True` — for no saving, since the hook never draws the twin | Rejected; the twin keeps the footprint (S4) |
| Keep the panel's blank rows in the data and skip them in the renderer | The values file claims rows nothing draws, against the sentence the A5 case rests on (*the drawing is these values*); the `SEALED` message is 50 characters a blank heavier for no reader | Rejected; `panel` emits none, and the renderer skips a `null` an older file carries |
| Keep `chain exit 0` on the panel as #666 did | #666 kept it because the ticket kept it and dropping it unasked was a question for the owner; the owner has now answered it | Superseded by the owner's decision |
| `CI also  <n> of <m>` — keep the denominator | The owner chose `<n> more steps`; the denominator stays on the stderr line beside the names, where a reader who wants it already looks | Rejected; the owner's wording |
| Leave the row out where `<n>` is 0 | A run that answers every step must not go quiet on the panel either; silence reads as a gate that stopped looking (`test_a_seal_that_answers_every_step_says_so`'s reason) | Rejected; the row prints, its wording at 0 is Q4 |
| Enforce the gap only where the prototype did (the disc's equator) | The owner's rendering shows the wax touching `skipped` on one row; the prototype asked for two clear cells and its collision test missed the disc's curve | Rejected; two clear cells on every text line, the prototype's own intent, costing under 50 characters |
| A new compositor module beside `seal_stamp.py` | Splits the one drawing over two files for the hook to load, and `hooks/sealer-stamp.py#STAMP` names one module | Rejected; the compositor lives in `seal_stamp.py`, where `build`, `letter` and the writers already are |
| Pin the drawing's bytes with a golden file | A golden file is a case that cannot say what went wrong, and the owner may still move a colour; what must hold is the budget, the footprint, the gap and the colours, each pinned on its own | Rejected; `test_the_disc_draws_the_same_bytes_in_every_process` keeps reproducibility pinned without a golden |
| Read `COLORFGBG` or query the terminal to pick a light or dark palette | No reliable signal reaches a `Stop` hook, and two palettes are two drawings for the owner to approve | Rejected; one palette, contrast measured, the owner reads the screen (S6) |
| Carry the threshold probe as a case in the suite | A case cannot start a Claude Code session, and one that could would run on every machine's harness | Rejected; the probe is `test_tmp_*`-shaped, run once in phase 1, deleted, and recorded in the phase record and the constant's comment |

## Phases

Vertical slices — each phase ends with something runnable and verified.
Each phase drafts its ledger rows and writes them to
`seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md`
at its boundary, with its `phases/phase-N.md`, and each pin is seen red
before it is committed (contract §15; say in the phase record how). The
narrow runs are `bin/test <module> -q` over the modules each row names; the
broad gate is the sealer's.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The hook never hands the harness a message it would persist** (S1, S5). The measurement first: a scratch directory outside the tree with `.claude/settings.json` registering a `Stop` hook that prints `{"systemMessage": <N characters>}`, driven by a one-turn headless session (`claude -p`, `CLAUDECODE` unset for the child) at `N = 9990` and then `N = 10010`; the outcome is whether `/Users/x/.claude/projects/<scratch project>/<session>/tool-results/` gains a `hook-*-systemMessage.txt`, read after each run; everything the probe made is deleted (§7). Then `seal_stamp.py` gains `MESSAGE_LIMIT` (the measured value, or 10,000 labelled read with the bracket where the session cannot run), `MESSAGE_BUDGET` (`MESSAGE_LIMIT` less a reserve of at least 1,000, the reserve's reason in the comment), `SCALE_LADDER`, and one fitting function over a block renderer and a budget; `hooks/sealer-stamp.py#main` prints the fitted message, `drawings` unchanged in contract. Docs: `hooks/sealer-stamp.py`'s docstring gains the budget paragraph; `docs/the-broad-gate.md` §*Where the stamp is drawn* gains the rule under this item's marker with its `Enforced by:` line | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`: A2 (the constants), A3 (one file and two files through `dispatch.py stop`, `len(systemMessage) <= MESSAGE_BUDGET` — **red against `5180b89e` over a values file carrying #666's full row set**, whose 0.90 rendering with its label is over 10,000), A4 (the ladder at a small budget), A15 (the existing byte comparisons made against the fitted message); the policy pin (A18's first half); `tests/test_a_gate_that_fails_says_so.py` S9 green unchanged. `phases/phase-1.md` records the probe's two outcomes, the session's `tool-results` listing, and that the scratch directory, its project directory under `/Users/x/.claude/projects/` and its transcript were removed | e81b6138 |
| 2 | **The panel says only what a `SEALED` stamp can say** (S2, S7 for the rows). `broad_gate.py#panel`: no `None` rows, no `chain`, no `exit` continuation under `suite`, no `drifted` continuation under `ledger`, `("CI also", f"{n} more steps")` in `workflow`'s place; the docstring's row diagram and the module docstring's stamp paragraph (68–82) follow; `ledger_counts` kept. `seal_stamp.py`: `SAMPLE_ROWS` mirrors the sequence, its comment follows; both forms skip a `None` row. Docs: `skills/verify/SKILL.md` §*A seal says what it did not answer* (the row's name and wording, `4 of 9` → the `CI also` reading), `agents/sealer.md` lines 97–100. Ledger: `1790815615` N5 and N10 corrected in place with `Corrected <date>` notes, N8 re-read; `0.12.2` R5 and G6 re-read; the new rows in this item's fragment | `tests/test_the_seal_is_taken_once_by_the_sealer.py`: A6 (`test_the_values_file_holds_this_runs_panel` rewritten to S2's sequence, positively), A8 (the suite and ledger row cases rewritten to assert the next label), A19 (`test_the_sample_carries_every_row_the_panel_can`), the width case's `values` list still every value ≤ `PANEL_VALUE_WIDTH`; `tests/test_the_gate_names_every_step_ci_runs.py`: A7 (`1 more steps` on the rendered twin at 587, `4 more steps` at 1184, `8 more steps` at 1203, `HISTORICAL_ROWS` without `chain`), the coverage-line assertions untouched; `tests/test_the_gate_asks_the_range_ci_will_ask.py` 549–571 green over the row under `base` (the frame regex moves in phase 3 if the seal covers that row's edge); document pins for the two sentences, red with the sentence deleted. Each pin red against `5180b89e` first | f74897df |
| 3 | **The drawing is a letter with the seal pressed over its corner** (S3, S4, S6, S7 for the drawing). `seal_stamp.py`: the four disc colours and the four 256-colour codes named; `ROPE_L`, `ROPE_D`, `WAX_L`, `GOLD` removed; `build`'s `px` with the wax edge at 0.84, `WAX_M` from 0.78, the field and the lily's four colours from `shrink(ART, scale)` and the two neighbour tests; `sgr` taking an int; one compositor from `letter(rows)`'s inner lines and `build` to cells — the sheet one blank line above and below the text, the text three cells in, the seal's centre line on the sheet's last line and the sheet's right edge at the seal's centre column where the seal sets the width, two clear parchment cells between every text line's last character and the wax, no text cell covered — and two writers over the cells, painted trailing cells kept; `KEY` for the twin's five seal characters, `|`, `.---.`, `'---'` for the sheet; `stamp(rows, scale, shape)` returning the letter's lines; `beside` retired or kept only if something still calls it. The contrast measurement (A17) in the phase record. Docs: `seal_stamp.py`'s module docstring (the drawing, the twin's letters, the usage), `docs/the-broad-gate.md`'s unchecked paragraph (one sentence on the background), `bin/seal-stamp` only if a sentence went false. Ledger: `0.10.0` S2 corrected in place, S3 re-read; `0.15.7` N3, N5, N6 re-read, N7 corrected in place; the new rows in this item's fragment. `changelog.md` and `overview.md` (the Not-verified rows for the owner's two readings and Q3) close the item | `tests/test_the_seal_is_taken_once_by_the_sealer.py` Part 1: A9 (the sheet, the gap, the overhang, the kept trailing cells, the colour codes, the absent rope and gold — new cases, red against `5180b89e`), A10 (`test_the_twin_and_the_block_form_have_equal_width_and_height` parametrised over `SCALE_LADDER`, `test_the_disc_is_symmetric_because_it_is_computed`, `crown_of`'s line present in a stamp and nothing else), A11 (`test_a_coloured_row_carries_fewer_colour_sequences_than_cells` over the new writer, `test_the_disc_draws_the_same_bytes_in_every_process` unchanged), A5 (the widest panel fits at 0.90 — red against `5180b89e`), A12 (the hand-command cases green), A13 (an older file's `null`, `chain`, `exit` and `drifted` rows drawn as text, the blanks skipped), A16 (`git diff 5180b89e -- skills/verify/scripts/broad_gate.py` carries no hunk in `gate`, `signal` or `main`; the terminal, pipe and `NOT SEALED` cases green unchanged); `tests/test_the_gate_asks_the_range_ci_will_ask.py` 569–571's frame regex moved to read the row under `base` off the twin without the `\|`, and 1041–1069 green (`letter` unchanged); `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` S3 and `test_several_files_come_out_as_one_message_oldest_first` still comparing against the fitted message; A18's remaining pins | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **No migration, no new dependency, no new environment variable.** Three
  constants and one function in a stdlib-only module; the hook's
  registration, group and event are unchanged.
- **Failure direction and prompt budget** (`CONTRIBUTING.md`): the hook
  blocks nothing and allows nothing it did not; what can now go wrong is a
  stamp drawn at a lower rung or without its seal, never one not drawn, and
  never one persisted. Zero questions reach a person.
- **The install boundary, in both directions.** A values file this gate
  writes is drawn by the installed 0.16.0 hook with the 0.16.0 renderer
  until 0.17.0 is installed — rope and gold over the new rows, under the
  pre-#666 label — and its size is `questions.md` Q3; the first real seal of
  this branch is where the owner reads it. A file written by an older gate,
  still pending when 0.17.0's hook draws it, is drawn as the letter with its
  `null`, `chain`, `exit` and `drifted` rows as text and its blanks skipped
  (A13).
- **`seal-stamp --from` on PATH runs the installed copy.** A person who
  wants the letter before 0.17.0 is installed runs the tree's
  `skills/verify/scripts/seal_stamp.py --from <file>` by path; the hook's
  docstring and `docs/the-broad-gate.md`'s unchecked paragraph already send a
  reader to `--from`, and neither needs a second sentence for a window one
  release wide.
- **The sealer's report does not change.** The `SEALED` line, the
  commit-the-cell line and the `NOT SEALED` form are untouched, so
  `agents/sealer.md` §*The command* keeps its three outcomes as written;
  only its *the `workflow` count* sentence moves.
- **Sibling 0.17.0 branches.** `broad_gate.py` is edited in `panel` and its
  docstrings only; `seal_stamp.py` and `hooks/sealer-stamp.py` have no
  other open branch on them at `5180b89e`. Whichever branch squashes second
  merges `origin/release/v0.17.0` in — never a rebase (`docs/release-checklist.md`
  §0) — and re-takes its seal.
- **The changelog fragment** goes in this directory's `changelog.md`: what a
  person now sees on the stamp, the budget and the ladder, and the rows
  that left, in that order. It names the installed-hook window as a cost.
