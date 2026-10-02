# Feature Specification: the seal stamp is a letter with the seal on its corner

<!-- seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #717, release 0.17.0. Every seal drawn since #666 reached the owner as
a 2 KB preview of a persisted file: the harness persists a hook's
`systemMessage` past roughly 10,000 characters, and #666 lengthened the
label and the panel by about 200 visible characters, which crossed the line.
#666 is unreleased, so 0.17.0 would ship the stamp unreadable. The owner
chose the replacement on 2026-10-02 from rendered prototypes, and the
issue's body records the choice; §*What the owner decided* below restates it
only to anchor the clauses, and nothing in this file reopens it.

**What this is, in one line.** The hook holds every message it prints under
a budget named in the code, stepping the seal down and then leaving it off
rather than handing the harness anything it would persist; the panel loses
the rows a `SEALED` stamp cannot say anything with; and the drawing becomes
a letter on parchment with the seal pressed over its corner, at 6,239
characters against 10,090 for the same values.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-broad-gate.md` §*Where the stamp is drawn* — *"The stamp is drawn once, where a person sees it, and only over a run that earned it"*, and the second paragraph: *"What the person's screen shows is not checked … the owner reads it on the first real run after a change to this surface"* | The property this work restores is the first sentence's *where a person sees it*: a persisted preview is not seen. The budget is what makes it hold against a size the harness decides, and the second paragraph is why the dark-and-light reading (S6) is the owner's and no case's. One new paragraph joins this section under this item's marker, with an `Enforced by:` line naming the budget case |
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true* — *"Every step CI runs is either mirrored by a named arm or excluded with a written reason"* | The count on the panel stays a reading of `PARTITION` over `steps_for`; only its label and wording change (`CI also  <n> more steps`). The stderr line that names the steps is untouched |
| `skills/verify/SKILL.md` §*Every agent seals what it verified, and one of them is final*, the **Form** bullet — *"The sealer's is the only one drawn, and only over a run that earned it"* | The drawing changes and the property does not: the values are still written on the gate's own success path and drawn from nothing else. A `SEALED` stamp therefore already says what `chain exit 0`, `exit 0` under `suite` and `0 drifted . 0 broken` said, which is the owner's ground for removing them (S2) |
| `skills/verify/SKILL.md` §*A seal says what it did not answer* — *"the panel carries a `workflow` row — <n> of <total> not answered"* | This sentence becomes false and is corrected in the same work item, together with its example `4 of 9` (S7). The reason the count sits on the panel — *a panel value is 23 columns and a step name is a sentence* — is unchanged, and `PANEL_VALUE_WIDTH` stays 23 |
| `docs/the-broad-gate.md` §*A document that its own work item's fixes disproved is corrected in the same work item* | Six documents and two scripts describe the rope, the gold lily, the `workflow` row or the rows this work removes; each is corrected here (S7) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `hooks/sealer-stamp.py` is a hook. Direction: it blocks nothing and allows nothing it did not; what moves is the size of what it prints, and the failure it can now have is a stamp drawn smaller or without its seal, never one not drawn. Prompt budget: zero. A test seen red: every case in §*Acceptance* against the tree at `5180b89e` first |
| `CLAUDE.md` §*The goal a design is chosen against* | The threshold is a measurement for the builder and not a question for the owner; the step-down is decided by the code at draw time and asks nobody; the one reading only a screen can give is carried as an unverified row with the owner named, not as a stop |
| `CLAUDE.md` *Repo rule — a change writes fragments, never the shared file*, and the paragraph after it | New rows go in `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md`. The release rows this work drifts or makes false are handled in the files that hold them (§*Data & interfaces*, *Ledger rows this work drifts*) |
| `CLAUDE.md` *Repo rule — a thing more than one party can have is named with whose* | New prose says *the sealer's stamp*, *the panel*, *the sheet*, *the seal pressed on it*, never a bare *the seal* for the drawing. `seal_stamp.py` and `broad_gate.py` are members of `tests/test_one_word_one_meaning.py`'s sweep |
| `CLAUDE.md` *Repo rule — no real identifiers in examples or fixtures* | Every path this work writes into a record or a case is `/Users/x/…`; the prototype directory is named by its layout, never by its absolute path |
| `hooks/console.py`'s docstring, and `seal_stamp.pick_shape` | The letter twin exists for a console that is not UTF-8. Keeping the twin at the new design's footprint (S4) is what keeps that console a reader of the stamp rather than of mojibake |
| `agent-contract` §14, §15 | Every rendered line this work changes is documented and pinned in the same commit, and every pin is seen red first; `plan.md`'s Verified-by column names the file each pin lives in |
| `skills/implement/SKILL.md` §3's ladder | Text and a drawing a person reads change at every seal, and a size somebody is limited by gains a name: top rung, so `spec.md`, `plan.md`, then the build |

## What the owner decided (2026-10-02, from rendered prototypes; not reopened here)

The issue's body §*The design the owner chose* is the record. In this file's
vocabulary:

- **The sheet.** The panel's text is written on a parchment sheet. The sheet
  starts one blank line above the text and ends one blank line under it, so
  no blank paper is painted beyond that.
- **The seal.** The disc is at `DEFAULT_SCALE`, 0.90. It sits beside the
  last lines of the text and hangs over the sheet's bottom edge and its
  right edge, the way a seal is pressed onto a letter's corner.
- **The disc.** The rope ring (`ROPE_L`, `ROPE_D`) is removed, and so is the
  outer light-red band (`WAX_L`); `WAX_M` becomes the wax's edge. The lily
  is pressed into the wax in one colour, lit from the upper left: field
  `(120, 16, 20)`; highlight edge `(226, 82, 74)` where the chart cell
  up-left of a lily cell is field; shadow edge `(96, 10, 14)` where the cell
  down-right is field; face `(186, 34, 38)` everywhere else on the lily.
- **Colour codes.** The disc keeps 24-bit colour. Parchment and ink use
  256-colour codes: parchment 230, sheet edge 187, ink 94, the `SEALED`
  title 124.
- **Panel rows on a `SEALED` stamp.** `chain  exit 0`, the suite's `exit 0`
  continuation and the ledger's `0 drifted . 0 broken` continuation go,
  because `SEALED` implies each. The counts stay.
  `workflow  <n> of <m> not answered` becomes `CI also  <n> more steps`.
  The `NOT SEALED` form keeps the arms' exit codes.
- **The reference.** `narrow.py#sheet(scale=0.90, narrow=True, rw=trimmed(True))`
  in the orchestrating session's scratchpad, `stamp/` directory, with
  `envelope.py#encode`, `env3.py#sealf` and `rows.py#trimmed`; its output is
  `letter-090.txt` there, 6,239 characters over #702's values file. The
  scripts are throwaway and read-only: ported, never copied.
- **Release.** 0.17.0.

## What was measured before the frame, and by whom

| Fact | Label | Where |
|---|---|---|
| The current stamp over #702's values (`3e9af52c against 5180b89e`) is 10,091 characters, 11,260 bytes, 24 lines, 83 columns, 505 SGR sequences; the chosen prototype's output is 6,240 characters, 6,546 bytes, 24 lines (label included), 325 SGR sequences. The issue's 10,090 and 6,239 count the same strings without the trailing newline | executed 2026-10-02 by the framer, `len()` over `now-truecolor.txt` and `letter-090.txt` in the scratchpad | this file |
| **The threshold is bracketed by what the harness has already done.** Over three sessions of this project, 23 stamp messages of 9,886 to 9,919 characters and two #400 probe messages of 9,692 were drawn with no persisted file, and 7 messages of 10,090 to 10,270 characters each left a file `hook-<uuid>-2-systemMessage.txt` under `/Users/x/.claude/projects/<project>/<session>/tool-results/`. So the limit is above 9,919 and at or below 10,090 characters, counted as Python `str` length. The same bracket in bytes is 11,088 to 11,259, so this data alone does not say which unit the harness counts; the issue's *9.9KB* label does — 10,090 / 1024 is 9.85, 11,259 / 1024 is 11.0 | executed 2026-10-02 by the framer, decoding every `Stop` hook's recorded stdout in the three transcripts and listing the `tool-results` directories | this file; the issue's own table |
| The transcript records a `Stop` hook's whole stdout (`hook_success`, `stdout`) whether or not the message was persisted; the persisted copy is a second file beside it. So *was it persisted* is read off the `tool-results` directory, not off the transcript | executed 2026-10-02 by the framer, the same decode | this file; `hook_success` is a field of the harness's transcript, NAME NOT IN TREE (noted by the build, phase 2) |
| In the prototype's chosen rendering the wax touches the text on one row — `6621 passed, 11 skipped▀` — although `sheet()` takes `gap=2`. Its collision test reads the disc's column 0 for a cell inside the gap, which is outside the disc on every row but the equator, so the gap is enforced only there | read 2026-10-02, `narrow.py#sheet` (`collides`) and the stripped `letter-090.txt` | this file |
| `envelope.py#encode` strips a line's trailing spaces only where the last cell has no background (`if bg is None: s = s.rstrip()`); an earlier version stripped painted ones | read 2026-10-02; the spawn prompt named the defect and the file shows the repair | this file |
| The chosen layout drops every blank row: `sheet()` keeps only `letter()` lines with text, so the groups the panel's `None` rows separated are gone from the sheet | read 2026-10-02, `narrow.py#sheet` (`text = [t for t in text if t.strip()]`) and `letter-090.txt` | this file |
| The hook's message is assembled in two places: `hooks/sealer-stamp.py#drawings` builds one block per values file (label, then `stamp.stamp(rows, scale, shape=False)`), `main` joins the blocks with a blank line, and `hooks/dispatch.py#report` then PREPENDS the session's gate-failure report to the same `systemMessage` — `LABEL`, one line per failed gate capped at `MESSAGE_CAP` 200 characters of exception text, `CLOSING` — where one is pending. The hook cannot see that prefix | read 2026-10-02, `hooks/sealer-stamp.py` 96–150, `hooks/dispatch.py` 49–67, 484–525 | this file |
| `panel`'s values are bounded at `PANEL_VALUE_WIDTH` by `fit`, so the sheet's width is bounded; its height is not: `wrapped` continues the suite's counts and `rounds_rows`' deferred homes on as many rows as they need. Every other row is one of eleven | read 2026-10-02, `broad_gate.py#panel`, `#fit`, `#wrapped`, `#rounds_rows` | this file |
| The installed plugin is 0.16.0 and its `hooks/sealer-stamp.py` is byte-identical to the tree's; its `seal_stamp.py` is the pre-#666 module (old `not_sealed`, old `label`, `lint clean` in the sample). The hook loads the `seal_stamp.py` beside itself, so a values file this branch's gate writes is drawn by the 0.16.0 module's rope-and-gold design under the 0.16.0 label until 0.17.0 is installed | read 2026-10-02, `diff` of the two files against the plugin cache; `hooks/sealer-stamp.py#STAMP` | this file |
| Tests that pin today's rows or drawing: `tests/test_the_seal_is_taken_once_by_the_sealer.py` (`ROWS` 46–61; the twin, colour, symmetry, panel and floor cases 143–326; `test_the_command_piped_prints_the_twin` 437; `crown_of` 742; A5 `test_the_values_file_holds_this_runs_panel` 2504; the width case 2854–2918; `test_the_suite_carries_its_exit_under_its_counts` 2950; `test_the_ledger_carries_drifted_beside_broken_on_the_row_beneath` 2975; `test_the_sample_carries_every_row_the_panel_can` 3107); `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` (`ROWS` 26–42; S3 `lines[1:] == mod.stamp(ROWS, 0.9, shape=False)` 272 and 323, 341; `test_both_commands_draw_at_the_default_scale_when_given_none` 579); `tests/test_the_gate_names_every_step_ci_runs.py` (A6 `1 of 2 not answered` 587; `HISTORICAL_ROWS` 712; `4 of 9 not answered` 1184; `8 of 11 not answered` 1203); `tests/test_the_gate_asks_the_range_ci_will_ask.py` (the rendered regex with the `\|` frame 569–571; `test_the_panel_value_width_is_what_the_stamp_actually_gives` 1041; `test_a_ref_too_long_for_the_panel_says_it_was_cut` 1068); `tests/test_a_gate_that_fails_says_so.py` S9 (`STAMP_VALUES` 590, the stamp unchanged beside the report 602–631) | read 2026-10-02, `grep` then the regions opened | this file; the suite and ledger cases were renamed by the build's phase 2 to `test_the_suite_carries_its_counts_and_nothing_under_them` and `test_the_ledger_carries_its_ok_count_and_nothing_beneath`, so the two names above are the frame's, NAME NOT IN TREE |
| Documents that describe the drawing or name a row this work changes: `skills/verify/scripts/seal_stamp.py` docstring (4–19: *wax disc with a fleur-de-lis … parchment panel beside it*, the twin's letters `o O l m G W y Y`), `skills/verify/scripts/broad_gate.py` docstring (68–82: *the chain's exit* and *the exit code the repository's row came back with*), `#panel`'s docstring (the row diagram), `skills/verify/SKILL.md` §*A seal says what it did not answer* (the `workflow` row and `4 of 9`), `agents/sealer.md` lines 97–100 (*the `workflow` count*), `bin/seal-stamp`'s comment (unchanged: it names the scale and the commands only), `README.md`/`README.ko.md` (the hook table row names no row and no drawing: unchanged) | read 2026-10-02 | this file |

## Scope

### In

**S1 — A budget, named in the code, and a step-down ladder under it.**
`seal_stamp.py` names the harness's limit and what one hook message is held
under:

- `MESSAGE_LIMIT` — the number of characters past which the harness
  persists a `Stop` hook's `systemMessage`, counted as Python `str` length.
  Its value is what the build measures (`questions.md` Q1); its comment
  carries the measurement's date, the two probe sizes and their outcomes,
  and the bracket above as the fallback where the probe cannot run.
- `MESSAGE_BUDGET` — what the hook holds its WHOLE message under: every
  block, every label, the blank lines between blocks. It is `MESSAGE_LIMIT`
  less a reserve of at least 1,000 characters, and the comment says what the
  reserve is for: `hooks/dispatch.py#report` prepends the gate-failure
  report to this same message, the hook cannot see it, and one such report
  is about 500 characters for one gate.
- `SCALE_LADDER` — `(0.90, 0.80, 0.75)`, then the sheet without the seal.
  Every rung is inside `check_scale`'s band, so no rung can be refused.

One function in `seal_stamp.py` takes the rendered message at each rung in
order and returns the first that fits the budget, the last rung being the
sheet alone; the budget is a parameter so a case can drive the ladder at any
size. `hooks/sealer-stamp.py#drawings` renders every pending block at the
file's own scale as today, and `main` asks that function for the message it
prints: one rung for the whole message, chosen as the highest at which every
block fits together. A message with two stamps is two stamps at one scale.
`seal-stamp`, `seal-stamp --from` and the gate's own terminal drawing are not
budgeted: a terminal and a pipe are not the harness's message.

**The last rung fits every panel the tree can produce**, and that is a bound
stated rather than a mechanism: the sheet's width is fixed by
`PANEL_VALUE_WIDTH`, its height by eleven rows plus the continuation rows of
the suite's counts and the deferred homes, and a sheet without its seal costs
about 60 characters a row, so a message over the budget with no seal is a
record with more deferral homes than any work item here has had. A case
(A5) renders the widest panel the tree can produce and asserts it fits at
the FIRST rung; a second (A4) drives the ladder at a small budget and asserts
every rung in order.

**S2 — The panel says only what a `SEALED` stamp can say.**
`broad_gate.py#panel` returns, in this order (a row in brackets is
conditional, and every condition is today's):

```
SEALED
tree      <tree>
          <branch>                      [absent on a detached HEAD]
base      <base commit>
          <Base.ref>                    [absent where the ref is the commit]
item      #<pr> . <id>                  [absent without --record]
gate      tree <version>                [only where gate_copy says so]
suite     <pytest counts, or exit N where there are none>
          <more counts>                 [wrapped, as today]
ledger    <N> ok                        [exit N where there is no total line]
CI also   <n> more steps                [absent without a hygiene workflow]
rounds    <R>[ . capped]                [absent without --record]
          <k> deferred -> <homes>       [only where k > 0, wrapped as today]
```

- **Gone:** `chain  exit <N>`, the `exit <N>` row under `suite`'s counts,
  the `<D> drifted . <B> broken` row under `ledger`, and every blank row.
  Each is implied by `SEALED` on a drawn panel — `panel` runs on success
  alone, every exit is 0 and under `--strict` so are the two counts
  (`seal/specs/1790815615-…/spec.md` §*What was measured*). The blank rows
  go from the data because the chosen sheet draws none, and a row nothing
  draws is a row the values file should not claim (`tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_values_file_holds_this_runs_panel`:
  *the drawing is these values*). `read_values` keeps accepting `null`
  rows, and both forms skip one, because a file written by an older gate
  may still be pending.
- **Renamed:** `workflow  <n> of <m> not answered` is `CI also  <n> more
  steps`, `<n>` being `len(unanswered(workflow, base.given))` as today; the
  denominator leaves the panel and stays on the stderr coverage line, which
  does not change. Where `<n>` is 0 the row still prints — a row that goes
  quiet is indistinguishable from a gate that stopped looking
  (`tests/test_the_gate_names_every_step_ci_runs.py#test_a_seal_that_answers_every_step_says_so`'s
  reason) — and its wording at 0 is the work's (`questions.md` Q4).
- **Unchanged:** `fit`, `wrapped`, `PANEL_VALUE_WIDTH`, `ledger_counts`
  (still read; only `ok` is printed), `suite_counts`, `rounds_rows`,
  `item_value`, `gate_copy`, the `NOT SEALED` form (`failure_lines` keeps
  `exit <N>` as every entry's first line and the ledger's `total:` line as
  its last), and `broad_gate.py#gate`, whose terminal branch calls
  `stamp.stamp(rows, args.scale, shape)` with the same arguments.
- `SAMPLE_ROWS` mirrors the new sequence, as N8 of #666's fragment requires.

**S3 — The drawing is a letter with the seal pressed over its corner.** One
compositor in `seal_stamp.py` lays the panel's text on a sheet and presses
the seal over it, cell by cell, and two writers encode the same cells: the
block form in colour, and the letter twin (S4). The geometry is the chosen
prototype's:

- The text lines are `letter(rows)`'s inner lines with the frame removed —
  which keeps `letter` as the one place the value width is decided
  (`test_the_panel_value_width_is_what_the_stamp_actually_gives`) — laid
  from the sheet's second line, three cells in from its left edge. The
  `SEALED` row is the title, in 124; every other row is ink, 94; the sheet
  is 230 with a one-cell edge of 187 on each side. The sheet's top and
  bottom are its first and last lines, one blank line above the text and one
  below.
- The seal's centre line is the sheet's last line, so half of it hangs below
  the sheet; the sheet's right edge is at the seal's centre column where the
  seal, not the text, sets the width, so half of it hangs over the right
  edge. It stands as far left as it can without covering a text cell and
  while leaving **two clear parchment cells** between the last character of
  every text line and the wax on that line. The prototype asked for two and
  enforced it on the equator alone (§*What was measured*); the owner saw
  zero on one row. Two is the prototype's own intent and costs under 50
  characters, and the owner can overturn it when the plan is read.
- The disc is `build`'s circle with the rope and `WAX_L` removed: outside
  the wax's edge at `r > 0.84` is outside the disc, `WAX_M` from 0.78, the
  field inside, and the lily pressed as the four colours of §*What the owner
  decided*, decided from `shrink(ART, scale)` by the two neighbour tests.
  `ROPE_L`, `ROPE_D`, `WAX_L` and `GOLD` leave the module; `ART`, `shrink`,
  `check_scale`, `SCALE_FLOOR`, `SCALE_CEILING` and `DEFAULT_SCALE` stay.
- Colour is emitted at transitions only, as today, and `sgr` learns the
  256-colour form (`38;5;N`, `48;5;N`) beside the 24-bit one. A cell inside
  the sheet and outside the seal is a space on a painted background; a cell
  the seal covers top and bottom in two colours is `▀` with the bottom
  colour as background; a cell with one half outside everything is `▀` or
  `▄` with no background, as `colour_row` does today. **Trailing spaces
  painted with a background are kept**: a line ends with a reset only, and
  the rendering of a sheet row is the same width as every other row of the
  sheet. The prototype once stripped them and the fixed `encode` does not;
  a case pins it (A9).
- At `DEFAULT_SCALE` over #702's values the result is the prototype's size
  to within the gap's cost: about 6,300 characters, 22 lines, 67 to 69
  columns. A case pins the budget, not the bytes; the bytes are pinned the
  way they are today, by `test_the_disc_draws_the_same_bytes_in_every_process`.

**S4 — The letter twin keeps the block form's footprint.** `pick_shape` and
`is_terminal` do not change, and neither does what the twin is for: a console
that is not UTF-8 (`seal-stamp` or the gate's terminal path on cp949), and
`seal-stamp` on a pipe. The twin is the same cells written as characters:
the sheet's edge as `|`, its top line as `.---.` and its bottom as `'---'`,
exactly where the block form paints the 187 edge and the blank first and
last parchment lines; the text as itself; the seal's four disc colours and
the wax edge as five distinct characters in `KEY`, chosen by the work
(`questions.md` Q4), the field keeping `.`; a cell outside everything as a
space. A seal cell overrides a frame character where it covers one, as it
does in colour. So `test_the_twin_and_the_block_form_have_equal_width_and_height`
holds at every rung, `test_the_disc_is_symmetric_because_it_is_computed` holds
over `letter_row`, and no twin line carries an SGR sequence or a half-block.
The hook never draws the twin (`drawings` passes `shape=False`), so the
budget is measured over the block form alone.

**S5 — The hook keeps its role; only what it prints changes.**
`hooks/sealer-stamp.py` still answers the main session's `Stop` alone, finds
the session's directory under the common dir, builds every block whole before
claiming its file, claims before printing, prints one JSON `systemMessage`
whose first line is `label(values)`, and stays silent on every failure. What
changes: the message handed to `print` is the budgeted one (S1), so a stamp
may be drawn at a lower rung than the file's `scale` says, or without its
seal. A file's `scale` is not rewritten; `seal-stamp --from <drawn file>`
still refuses, as today. **Until 0.17.0 is installed the installed hook draws
this gate's files with its own 0.16.0 renderer** — rope and gold over the
new rows, under the pre-#666 label — and whether that message clears the
limit is `questions.md` Q3; the recovery named on every `SEALED` line,
`seal-stamp --from`, runs the installed copy too, so a person who wants the
letter runs the tree's `skills/verify/scripts/seal_stamp.py --from` by path.

**S6 — Dark and light backgrounds.** The parchment is a painted background,
so on a light terminal the sheet is a cream rectangle on white and its edge
(187, which is `(215, 215, 175)`) may be hard to see. No case, hook or
workflow can observe a screen (Grounding, row 1). The build does two things
and claims nothing more: it computes the contrast ratio of each 256-colour
pair the sheet uses against pure black and pure white, writes the eight
figures into its phase record, and names the owner's reading of the first
real seal on each background as an `overview.md` `## Not verified` row with
the owner as answerer. A palette change, should the reading call for one, is
one constant each and a follow-up, not this work item's.

**S7 — Every document and pin that describes the old drawing or the removed
rows moves with the code**, each pin seen red first: the two module
docstrings and `panel`'s row diagram; `skills/verify/SKILL.md` §*A seal says
what it did not answer* (the `workflow` row's name and wording, the `4 of 9`
example); `agents/sealer.md`'s *the `workflow` count* sentence;
`docs/the-broad-gate.md` §*Where the stamp is drawn* gains one paragraph under
this item's marker stating the budget rule and its `Enforced by:` line, and
one sentence in the unchecked paragraph saying the screen's background is
read by the owner; the comment above `SAMPLE_ROWS`; the cases listed in
§*What was measured*, last-but-one row. The changelog fragment is this
directory's `changelog.md`.

### Out, and why

- **The design, the scale, the palette's four disc colours and the four
  256-colour codes.** Chosen by the owner from renderings; this file carries
  them and does not weigh them.
- **The label line** (`seal_stamp.label`): unchanged, 165 characters on
  #702's values, inside every count above.
- **The `NOT SEALED` form, `failure_lines`, the `SEALED` line, the
  commit-the-cell line, the values file's keys, `write_values`,
  `read_values`'s acceptance, `claim`, `pending`, `drawn_from`.** None of
  them is about size or about the drawing's shape. `read_values` is touched
  only if the build finds it must be, and S2 says it keeps accepting `null`
  rows.
- **`broad_gate.py#gate`, `#signal`, `#main`.** The terminal branch's call
  and the values written are unchanged, so the fifteen ledger rows anchored
  on `gate` do not drift for this work. If a phase finds it must touch `gate`
  it says so in its record and re-reads those rows.
- **A budget on `seal-stamp` or on the gate's terminal drawing.** Neither is
  a `systemMessage`.
- **Making `dispatch.py` size-aware.** It assembles the final message but
  cannot re-render a stamp; the reserve in `MESSAGE_BUDGET` is the cheaper
  answer and the one with no second renderer.
- **Rewriting a values file's `scale` when the hook steps down.** The file
  records what the gate asked for; the drawn rung is the hook's and is said
  nowhere, by the same reasoning that lets a terminal draw at `--scale`
  without recording it. A reader who wants the figure runs
  `seal-stamp --from` on a copy.
- **A `COLORFGBG`-style reading of the terminal's background to pick a
  palette.** No reliable signal reaches a `Stop` hook, and a palette that
  switches on a guess is two drawings for the owner to approve rather than
  one.
- **Pruning drawn values files.** Named as a cost by #400 and unchanged.
- **The READMEs.** Both hook-table rows describe what the hook does and
  where, not what the stamp looks like (`test_both_readmes_list_the_stamp_hook`
  holds its sentences; none name a row or the rope).

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The threshold is measured | Given a scratch directory with a `Stop` hook that prints a `systemMessage` of exactly 9,990 characters, when a one-turn session ends there, then the scratch project's `tool-results/` holds no `hook-*-systemMessage.txt`; given the same hook at 10,010 characters, then it holds one. `MESSAGE_LIMIT`'s comment carries both outcomes and the date | **a measurement**, `questions.md` Q1, taken in phase 1 and recorded in `phases/phase-1.md`; where the nested session cannot run, the bracket above is the value's ground and the comment says so, labelled read |
| A2 | The budget is named and derived | `seal_stamp.MESSAGE_BUDGET <= seal_stamp.MESSAGE_LIMIT - 1000`, `MESSAGE_LIMIT <= 10090`, and `SCALE_LADDER == (0.90, 0.80, 0.75)` with every rung accepted by `check_scale` | a case reading the three constants |
| A3 | The hook's message is under the budget | Given any set of pending values files for a session, when the main session's `Stop` arrives, then `len(systemMessage) <= MESSAGE_BUDGET`, and each block still opens with its label | a hook case through `dispatch.py stop` over one file and over two, measuring the printed JSON's `systemMessage` |
| A4 | The ladder steps down in order | Given blocks whose rendering at 0.90 exceeds a budget passed to the fitting function, then the function returns the rendering at 0.80; given 0.80 exceeds it too, 0.75; given 0.75 exceeds it, the sheet with no seal — half-block-free and still carrying every text row; given 0.90 fits, 0.90 unchanged. One rung for every block in the message | a unit case over the function with a small budget argument, asserting the rung by the disc's row count and the no-seal form by the absence of half-blocks |
| A5 | The widest panel the tree can produce fits at the first rung | Given `panel` over a 73-character branch, a `refs/remotes/other/release/v1.2.3-hotfix` ref, five-digit counts in three parts (`12345 passed, 67890 skipped, 12 xfailed`), an item with a pull request, a `gate` row, a hygiene workflow, and a capped record whose verdicts defer to eight distinct homes, when the message (label and block form at `DEFAULT_SCALE`) is measured, then it is at most `MESSAGE_BUDGET` and the fitting function chose 0.90 | a case in the sealer test beside `test_no_value_on_the_panel_is_wider_than_the_frame_gives`, reusing its inputs and `capped_record`; seen red against the tree at `5180b89e`, whose rendering of the same rows is over 10,000 |
| A6 | The panel's rows | Given a sealer's green recorded run, then the values file's rows are exactly S2's sequence for that run — `SEALED`, `tree`, `""`, `base`, `""`, `item`, [`gate`], `suite`[, `""`…], `ledger`, [`CI also`], `rounds`[, `""`…] — with no `None`, no `chain`, no `exit` continuation and no `drifted` row | `test_the_values_file_holds_this_runs_panel` rewritten, positively; `HISTORICAL_ROWS` moved |
| A7 | `CI also` | Given this repository's `hygiene.yml` and a feature base, then the row reads `CI also  4 more steps`; given `main`, `8 more steps`; given the A6 fixture workflow, `1 more steps` on the rendered twin; given a repository with no workflow, no such row; the stderr coverage line is unchanged in every case | `tests/test_the_gate_names_every_step_ci_runs.py` A6, A11, A12 cases moved; the coverage-line assertions untouched and green |
| A8 | `suite` and `ledger` carry their counts and nothing under them | Given pytest counts, then `suite` is the counts, wrapped as today, and the row after the last counts row is not `exit 0`; given no counts, `suite` is `exit N`. Given a `total:` line, `ledger` is `<N> ok` and the next row is not a `drifted` row; given none, `exit N` | the two sealer cases rewritten to assert the absence positively (the row after is the next label) |
| A9 | The sheet and the seal | Given S3's compositor over `SAMPLE_ROWS` at 0.90, then: the first and last lines of the sheet are blank parchment; the text starts on the second line, three cells in; every sheet line has the same visible width, and a line whose last cell is painted ends with that cell and a reset rather than being stripped; no text cell is covered by a seal cell; on every text line at least two cells between the text's last character and the first wax cell are parchment; the seal's lowest row is below the sheet's last line and its rightmost column is right of the sheet's edge; the `SEALED` title is 124, the ink 94, the sheet 230, the edge 187, as `38;5;`/`48;5;` codes; every disc colour is a `;2;` code and is one of the four or `WAX_M`; no `ROPE_L`, `ROPE_D`, `WAX_L` or gold value appears | new cases in the sealer test's Part 1 over the cells and the encoded lines |
| A10 | The twin is the block form's footprint | At every rung, `stamp(rows, scale, shape=True)` has the same number of lines as the block form and each line the same visible width; no SGR sequence and no half-block in the twin; the twin's first non-blank line is the sheet's `.---.` top; the disc is left-right symmetric over `letter_row` | `test_the_twin_and_the_block_form_have_equal_width_and_height` parametrised over the ladder; `test_the_disc_is_symmetric_because_it_is_computed`; `crown_of` still names a line present in a stamp and nothing else the gate prints |
| A11 | Colour at transitions, and the same bytes everywhere | Every block-form line carries fewer SGR sequences than cells; the stamp at 0.75, 0.80 and 0.90 draws identical bytes under five `PYTHONHASHSEED`s | `test_a_coloured_row_carries_fewer_colour_sequences_than_cells` over the new writer; `test_the_disc_draws_the_same_bytes_in_every_process` unchanged |
| A12 | The hand command | `seal-stamp` on a pipe prints the twin with `SEALED` and `rounds` on it and equals `seal-stamp --shape`; `--scale 0.5` is refused with the floor named; `--from <file>` draws once at the file's scale and then refuses; `seal-stamp` and `broad-gate --help` agree on `DEFAULT_SCALE` | the existing cases, green over the new drawing |
| A13 | A values file from an older gate | Given a pending file whose rows carry `null` blanks, `chain`, `exit 0` and `drifted` rows, when the hook draws it, then every row is drawn as text on the sheet and the `null` rows are skipped; the label is `label(values)`'s | a hook case over `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`'s old `ROWS` shape |
| A14 | The report still goes first and the stamp is unchanged beside it | Given a pending gate-failure record and a pending values file for one session, then the `systemMessage` is the report, a blank line, then exactly the message the hook prints with no record pending | `tests/test_a_gate_that_fails_says_so.py#test_the_report_goes_before_the_stamp_and_the_stamp_is_unchanged`, green unchanged |
| A15 | Nothing else about the hook changed | A subagent's end, another session's file, a repository not opted in, a malformed later file, a subdirectory `cwd`, the sealer's worktree: each case of `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` holds, with its `mod.stamp(ROWS, 0.9, shape=False)` comparisons made against the budgeted message (which at `ROWS`' size is the 0.90 rendering) | those cases, moved where they compare bytes |
| A16 | The gate is untouched | `broad_gate.py#gate`, `#signal`, `#main` carry no diff; the terminal case still sees one `SEALED`, half-blocks and the commit-the-cell line; a piped recorded run still writes the values file and draws nothing; `NOT SEALED` still carries `exit N` per check | `git diff 5180b89e -- skills/verify/scripts/broad_gate.py` read in review; `test_a_person_at_a_terminal_sees_the_stamp_drawn_once`, `test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing`, the `chain  exit 1` assertions at 3714 and 4546, all green unchanged |
| A17 | Contrast is measured | The phase record carries the contrast ratio of 230, 187, 94 and 124 against black and against white, computed from the 256-colour cube's RGB | **a measurement**, phase 3; and `overview.md` `## Not verified` names the owner's reading of the first real seal on each background |
| A18 | The documents say what the code draws | Each sentence S7 names is replaced, and a pin reads the new one; `docs/the-broad-gate.md` carries this item's marker twice (the rule, and the sentence in the unchecked paragraph), with `Enforced by:` naming A3's case | document-pin cases, each seen red with its sentence deleted |
| A19 | The sample follows the panel | `seal-stamp`'s `SAMPLE_ROWS` labels, in order, are `panel`'s for a run with every conditional row present | `test_the_sample_carries_every_row_the_panel_can`, moved with the sequence |
| A20 | The ledger is left true | Every release row this work drifts is re-read and re-stamped with the date; the rows it makes false are corrected in place with a `Corrected <date>` note and their new claim written in this item's fragment | `evidence-check --strict .` names the set after each phase; the fragment's rows each name the phase |

## Data & interfaces

**Constants** (`skills/verify/scripts/seal_stamp.py`): `MESSAGE_LIMIT`,
`MESSAGE_BUDGET`, `SCALE_LADDER`; the four disc colours and the four
256-colour codes, named; `KEY` for the twin. Removed: `ROPE_L`, `ROPE_D`,
`WAX_L`, `GOLD`. Kept: `ART`, `WAX_M`, `FIELD` (renamed or revalued to the
chosen field colour is the work's), `SCALE_FLOOR`, `SCALE_CEILING`,
`DEFAULT_SCALE`, `PANEL_WIDTH`, `SAMPLE_ROWS`.

**Functions** (`seal_stamp.py`): `stamp(rows, scale, shape)` keeps its
signature and returns the letter's lines; `build(scale)` keeps `(w, h, px)`
with the new `px`; one compositor behind `stamp` producing cells, and two
writers over the cells; one fitting function taking the pending blocks'
renderer and a budget and returning the message that fits; `sgr` taking an
int or a triple. The names are the work's, pinned by the cases that read
them. `letter(rows)` stays and still decides the value width.

**The hook** (`hooks/sealer-stamp.py`): `drawings` keeps its contract —
blocks built whole, claimed before print — and `main` prints the fitted
message. A rung is chosen once per message.

**The panel** (`skills/verify/scripts/broad_gate.py#panel`): S2's sequence;
`CI also` is the label, in the `"  {label:<8} "` column `letter` already
gives. No signature change.

**The values file**: unchanged keys; `rows` is S2's sequence; `scale` is what
the gate was asked for.

**Ledger rows this work drifts or makes false** (read 2026-10-02; the set
after the edit is what `evidence-check` names):

- `seal/releases/0.10.0.md` S2 — *the top and bottom rope rows come out
  equal* and *the letter twin has the same width and height … at every
  accepted scale*. The rope half goes false; corrected in place with a
  `Corrected <date>` note (the symmetry claim stands over the wax's edge),
  anchors `build`, `letter_row` re-read.
- `seal/releases/0.10.0.md` S3 — `pick_shape`, `main` anchors; the claim
  holds; re-read.
- `seal/releases/0.15.7.md` N3, N5, N6 — `is_terminal`, `DEFAULT_SCALE`,
  `main`, `read_values`, `drawn_from` anchors; the claims hold; re-read where
  the hash moves.
- `seal/releases/0.15.7.md` N7 — *then the block form at the file's scale*.
  False once the hook may step down; corrected in place, the new claim in
  this item's fragment; anchors `sealer-stamp.py#main`, `#drawings`,
  `seal_stamp.py#label`.
- `seal/releases/0.12.2.md` R5 and G6 — `panel` anchor; the claims hold
  (the ref is still on the row under `base`; the count is still on the
  panel); re-read, G6's wording *the count on the panel* read against
  `CI also`.
- `seal/ledger/1790815615-….md` N5 — *`chain`, then `workflow` … `suite`
  with `exit N` beneath … `<D> drifted . <B> broken` beneath*. False;
  corrected in place, the new sequence a row of this item's fragment.
- `seal/ledger/1790815615-….md` N8 — the sample mirrors the panel; holds;
  `SAMPLE_ROWS` anchor re-read.
- `seal/ledger/1790815615-….md` N10 — *a feature seal reads `4 of 9 not
  answered` and a release seal `8 of 11`*. False on the panel; corrected in
  place (the stderr line's clause still holds), the `CI also` row in this
  item's fragment.
- `seal/releases/0.16.0.md` G4 and `seal/ledger/1790815611-….md` P1–P6 —
  `sealer-stamp.py#toplevel` and `broad_gate.py#gate`; untouched by this
  work and expected not to drift.

## What cannot be checked, stated so nobody mistakes it for enforced

- **Whether the stamp is seen unfolded.** The cases prove the message is
  under a number the code names; the owner's screen proves the number. The
  bracket in §*What was measured* is 170 characters wide, and a probe that
  cannot run leaves the value inside it, labelled read.
- **How the sheet reads on a light background.** Contrast figures are
  arithmetic; legibility is the owner's eye (S6).
- **What the installed 0.16.0 hook draws over this gate's files during this
  very release run.** Its renderer is in the plugin cache, outside the tree
  and outside any case; the first real seal of this branch is the reading
  (`questions.md` Q3).

## Open questions → questions.md

Every judgment the issue left open that the tree could answer is answered
above and listed at the head of `questions.md` so nobody reopens it. No row
there needs a person before the build; three are measurements, two are the
work's.

Framed 2026-10-02 by framer, before the build.
