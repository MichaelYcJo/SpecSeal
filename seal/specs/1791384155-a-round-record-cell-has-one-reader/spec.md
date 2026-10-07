# Feature Specification: a round-record cell has one reader (#866)

<!-- seal/specs/1791384155-a-round-record-cell-has-one-reader/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Every coordinate below is at 5623d728 (0.20.0 as shipped), which is this
branch's base plus one routing commit. Names written without a code span are
units this work adds or removes: the ledger's records arm reads a backticked
name in a live work item's records as a claim that the tree holds it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #834 `spec.md` §*What the table found besides* (branch `chore/834-every-reader-and-record-is-inventoried`), with `inventory/3-review-chain.md` rows 47, 61, 92, 98, 109–112, 126–128 and `inventory/5-verify-bin-ci.md` rows 19, 36, 38 | the five judgments this work gives one reader, and the copies of each as the inventory found them. A row's claim is the inventory agent's reading; every copy below was re-read in the code |
| `docs/round-record-spec.md`, opening paragraph | the pull-request check is the authority for how a record's rows are read, and `round_record.py` is the generator that writes them. That ordering is why the one reader lives in `chain_check.py` and the generator imports it |
| `docs/round-record-spec.md` §*`Pass` has to be checked, and a draft is the way to open one that is not* | a state the check cannot see is judged **ready**, deliberately; an override flag for the local case was considered and rejected. The generator's fake draft payload is that override without the name, and it goes |
| `docs/review-chain-spec.md` §*`Needs a fix` — the row the bound above rests on*, and the bare-`yes` paragraph under it | one reader, `chain_check.says_reopened`, says what the cell means; a bare `yes` is refused at both ends and reads as no reopening. The broad gate's panel is the third reader of that cell and it goes through the same one |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*, and its paragraph *The vocabulary the exit needs* | `deferred <home>` is the closing word, `deferred #N` where the home is an issue, and a bare `deferred` stays open. The home is what stands after the word; nothing says a reader may search the rest of the cell for one |
| `docs/round-record-spec.md` §*A fix of a fix — `Fix of a fix`*; `skills/code-review/orchestration.md` §*A fix of a fix twice sends the work item back to its framer*; `agents/warden.md` §*Role*, the `.py` path sentence (:152) | a place is read from a `Location` only as a whole-token `.py` path form, and a name with no path lands nowhere: *it reads no prose to decide which name in a cell is the place*. The depth walk reads the same cell for the same question and takes the same answer |
| `docs/round-record-spec.md` §*The depth in `New units`* | the depth refusal's direction: a wrong deny costs a prompt and a wrong allow ships a unit read by nobody. Kept; what changes is which cell reading feeds it |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | every phase below states its test seen red, its failure direction, its prompt budget (zero throughout) and its platform honesty |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | between a reader that asks `gh` and one that assumes, the observed source wins; between a reader that guesses a home out of prose and one that reads the written shape, the owned shape wins |
| `skills/agent-contract/SKILL.md` §12 | the class is *a cell read by two scripts*, enumerated from the issue's table and the inventory, not from the finding that opened the issue |
| `docs/the-record-layout.md` §*F1* (the cut of `docs/commit-review-gate-spec.md`) | the precedent for cutting a document at its own headings when it meets the ceiling, which two of the documents this work edits sit one line under |

## Scope

**In.** Five judgments about a round record, each read today by two to four
scripts, each given one reader in `chain_check.py` that the other scripts
import. The issue's table names them; the inventory's rows are the coordinates.

| Judgment | Readers today | Where the one reader lives after this work |
|---|---|---|
| what `Needs a fix` says | `chain_check.py#says_reopened` (:2572), `round_record.py#terminal_value` (:1427, the writer's refusal through `chain.yes_or_no`), `broad_gate.py#rounds_rows` (:2895, `.startswith("yes")`) | `says_reopened`, unchanged; the panel reads through it |
| the home of a `deferred` verdict | `chain_check.py#verdict_of` (:1653, home present or not), `round_record.py#fix_table` (:3738, the rest of the cell or the third cell), `broad_gate.py#deferred_home` (:2828, an issue or a path anywhere after the word), `.github/scripts/release_seal.py#chain_counts` (:358, every `#N` in the cell) | a new function deferred_home beside `verdict_of`, and issue_of over its answer |
| where a `Location` places a finding | `round_record.py#path_forms` (:4026, through `landings` :2360) and `round_record.py#location_units` (:3986, through `depth_two` :4094) | `path_forms`; the wide reading leaves |
| the pull request's state | `chain_check.py#pull_request_state` (:1183, unknown → ready), `round_record.py#pull_request_is_ready` (:1006, unknown → draft, then `run_check` :2664 writes a draft payload), `broad_gate.py#draft_env` (:1793, writes the same payload) | `pull_request_state`, which gains the generator's `gh` question as its second source; the two payload writers leave |
| the floor's two walks · the run cut · the premature-gate test · a doubled close · duplicate rows and boxes | `chain_check.py#stopping_floor` (:3527) and `round_record.py#floor_and_fixes` (:1969) · `chain_check.py#runs_of` (:3819) and `round_record.py#current_run` (:2264) · `chain_check.py#broad_gate` (:4205) and `round_record.py#seal` (:4956) · `chain_check.py#doubled_grounds` (:2021) and `round_record.py#close` (:4440) · `chain_check.py#field` (:1230) and `#pass_checked` (:2219) against `round_record.py#field_index` (:4229), `#close` (:4516) and `#seal` (:4862) | one pure function per judgment in `chain_check.py`, fed the record's cells; both callers keep their names and call it |

In scope too: the documents whose sentence would be false after the change,
corrected by replacement (§*Data & interfaces*); the tests that pin a reading
this work removes, replaced by cases for the one reading; the `Re-read ·`
rows the edits owe (§*Operational impact* in `plan.md`).

**Out.**

- A verdict word, a severity rule, or what a ⬜ commissions — #837's.
- How a fix range is read across a merge (`round_record.py#touched`,
  `chain_check.py#walk_tip`) — #860's. This work touches neither unit.
- The broad gate's suite counts, the recorder, and the panel's other rows —
  #869's. This work touches `rounds_rows` and the chain arm's environment only.
- A registry of readers and their classes — #835's. This work lists the
  input class of every reader it adds or changes (§*Data & interfaces*) so the
  registry can take them, and adds no mechanism of its own for it.
- `survivor_check.py`'s copies of `BLOCK` and the changelog shapes (part 3
  rows 6, 9, 10). Those are copies across script roots that cannot import
  each other, which the inventory names and this issue does not.
- An owned `Unit` column in the verdict table. Rejected in `plan.md`'s
  Alternatives table.
- Cutting `docs/round-record-spec.md` or `docs/review-chain-spec.md` into two
  files. Each phase edits those documents by replacement and measures the line
  count; a cut is the fallback `questions.md` W1 names, and it is taken only
  where a replacement does not fit.

## The five judgments, decided

### J1 — `Needs a fix`: the panel reads through `says_reopened`

Today `rounds_rows` reads `visible(needs).strip().lower().startswith("yes")`
and prints ` · capped`. `says_reopened` reads the same cell for the gate and
for the generator's printed bound (`floor_and_fixes` :2068), and
`terminal_value` refuses a bare `yes` before the record exists. The three
disagree on exactly these cells:

| The cell | `says_reopened` | the panel today | the panel after |
|---|---|---|---|
| `yes — <what>` | True | ` · capped` | ` · capped` |
| `**yes — <what>**`, `` `yes` — <what> `` | True (emphasis off first) | not capped (begins `*` or `` ` ``) | ` · capped` |
| `yes` alone | None — refused at the gate above `NEEDS_FROM`, printed below it | ` · capped` | `<R>` alone |
| `yesterday's finding …`, any word outside the vocabulary, an empty cell | None | ` · capped` for the first, not capped for the rest | `<R>` alone |
| `no`, `no — <why>` | False | not capped | not capped |

**A cell the gate refuses is a record that cannot answer**, and
`rounds_rows` already prints `<R>` alone for a record that cannot answer both
of its questions (no `Needs a fix` row, no readable `## Verdicts`). A bare
`yes` joins that set rather than being read a third way. What leaves:
the `startswith("yes")` line and nothing else in that function.

Failure direction: the panel claims `capped` on fewer cells, and claims
nothing on a cell the check refuses. Measured: the tree's 22 records carry 18
`yes — …` cells and 4 `no`; none is bare, so no committed panel changes.

### J2 — a deferred finding's home: one grammar, the writer's

`round_record.py close` writes the verdict cell as `deferred <home>` (:4412)
where `<home>` is what `fix_table` read after the word in the smith's table,
and `new` writes `deferred the frame` at a `second`. So the written shape is
`deferred` + separator + the home, and a note, where the smith wrote one, is
joined with ` — ` into the Grounds cell. The four readers then read that cell
four ways: `verdict_of` asks only whether anything follows the word;
`fix_table` takes the whole rest of the cell (so `deferred #854 — the run is
capped` carries a home of `#854 — the run is capped`); the panel's
`deferred_home` searches the rest for the first `#N` or path and otherwise
takes words up to a dash; the release seal counts every `#N` anywhere in the
cell, so a note mentioning a second issue counts twice.

**The one reader is a function deferred_home beside `verdict_of`, with the
same two layers taken off** (`EMPHASIS`, a trailing stop) and the word matched
as `verdict_of` matches it. The home is the text after the word and its
separators, cut at the first ` — ` (space, em dash, space — `DASH`, the join
`close` and the generator's prose use) or the end of the cell, with the case
the writer gave it. A function issue_of over that answer gives `N` where the
home is exactly `#N`, and None otherwise. `verdict_of` keeps deciding open
against closed and is not changed.

| The cell | home | issue |
|---|---|---|
| `deferred #664`, `**deferred** #664.`, `deferred — #664` | `#664` | 664 |
| `deferred #854 — the run is capped; two spellings` | `#854` | 854 |
| `deferred seal/follow-up.md`, `` deferred `seal/follow-up.md` `` | `seal/follow-up.md` | None |
| `deferred the frame`, `deferred a new issue` | `the frame`, `a new issue` | None |
| `deferred to #664`, `deferred → #664`, `deferred — issue #97 already holds this axis` | `to #664`, `→ #664`, `issue #97 already holds this axis` | None |
| `deferred`, `deferred —` | None (`verdict_of` says `deferred (no home)`) | None |
| `fixed abc1234` | None | None |

The fifth row is the reading this work removes: the panel used to find the
issue inside those three, and `tests/test_the_seal_is_taken_once_by_the_sealer.py`
pins fourteen such cells (`test_the_home_is_read_off_the_cell_after_the_word`
and the parametrized case under it). They were written from shapes a person
might type, not from shapes the tree writes: measured over the 22 records in
the tree, every one of the 20 `deferred` cells begins `deferred #N` (14),
`deferred the frame` (5) or `deferred a new issue` (1), and no writer in
`agents/`, `skills/` or `templates/` emits `deferred to`, `deferred →` or
`deferred — issue`. A home a person wrote as prose prints as that prose on the
panel and names no issue to the release seal, which is what the cell says.

Who consumes it: `rounds_rows` (the distinct homes after `→`, as today);
`release_seal.py#chain_counts` (the distinct issues, through issue_of);
`fix_table` (the home, with everything after the cut going to the note the
third cell already carries). What leaves: `broad_gate.py`'s `HOME_TOKEN`,
`HOME_END` and its `deferred_home`; the `re.findall(r"#(\d+)", …)` in
`release_seal.py`; `fix_table`'s own `deferred` prefix test, which spelled the
separators differently from `verdict_of` (`deferred—#12`, with no space,
closes in the fix table and stays open at the gate).

Failure direction: the release seal and the panel count and name fewer homes
where a cell departs from the written shape, and never more. The generator
refuses nothing new: a `deferred` with no home was refused before.

### J3 — `Location`: the depth walk reads path forms, and the wide reading leaves

#823 narrowed `landings` to `path_forms` — a token that is wholly `path:line`,
`path#unit` or `path::unit` with a `.py` path — and left `location_units`'
wide reading in place for `depth_two` because *nothing in the three rounds
found it wrong* (that work item's `spec.md` §*What round 3 moved*). This work
overturns that half, on three grounds that were not on the table then:

- The inventory's finding is the two readers of one cell, not a wrong answer
  from either (part 3 rows 109–111, 126). One cell read two ways in one
  subcommand family is the shape #834 names.
- Measured on the 22 records in the tree: 61 `fixed` verdict rows, 44 with a
  `.py` path form, 17 with a path that is not `.py` (`templates/config.md:334`,
  `.github/workflows/test.yml:105`, an `overview.md` line), and **none** that
  names a unit by a backticked or bare identifier alone. #823's own count found
  none in 179 fix-owing rows at three tags. The wide reading has read nothing
  the narrow one would not, on every record the tree holds.
- `agents/warden.md` already tells the reviewer to carry the `.py` path, and
  `skills/code-review/orchestration.md` says the path *is* the place.

So `depth_two` resolves each `fixed` finding's `Location` through
`path_forms`, every pair it gets carries its file, and the branch that resolved
a path-less name against every file the range touched goes with the reading
that produced such names. What leaves `round_record.py`: location_units and
its five patterns LOCATION_UNIT_RE, LOCATION_LINE_RE, FRAGMENT_RE,
IDENTIFIER_RE and BARE_IDENTIFIER_RE; `resolve_path` and `tracked_at` stay,
because `path_forms` reads through them. The sentence in `depth_two`'s
docstring and in `docs/round-record-spec.md` §*The depth in `New units`* that
describes resolving a name with no file is replaced by the path-form sentence
§*A fix of a fix* already carries.

Failure direction: the depth-2 refusal fires on fewer shapes — a finding
located by a bare name no longer reaches it — which is the permissive side,
chosen for the reason #823 chose it for `landings`: a miss costs what today
costs, and reading prose to find the place is the enumeration
`docs/round-record-spec.md` declines. An owned column instead is rejected in
`plan.md`.

### J4 — the pull request's state: observed twice, assumed never

`pull_request_state` reads the event payload and judges `unknown` as ready,
and the policy table says why. `run_check` then writes
`{"pull_request": {"draft": true}}` into a temporary file and points
`GITHUB_EVENT_PATH` at it whenever `pull_request_is_ready` returns False —
which it does when `gh` is absent, fails, or says draft — and `draft_env` does
the same for the broad gate's chain arm. The inventory calls the first *writer
of a payload the next reader trusts* (part 5 row 19): on a machine without
`gh`, every local run is a draft, and a draft excuses the unchecked `Pass`, the
empty `rounds/`, the `nobody`-beside-`Pass` pair and the `Broad gate` cell.

**The one reader gains the generator's question as its second source and
keeps its direction.** `pull_request_state` reads, in order: the payload
(observed, unchanged); where there is none, `gh pr view --json isDraft` in the
repository (observed — the exact call `pull_request_is_ready` makes today,
with its timeout); where that is absent, fails, or does not answer the
question, `unknown`, judged **ready** and printed with which source was tried,
as the policy table requires. The generator's `run_check` and the gate's chain
arm call the check and write nothing into the environment. What leaves:
`round_record.py`'s pull_request_is_ready and the payload in `run_check`;
`broad_gate.py`'s draft_env.

**The gate's chain arm runs before `round_record.py seal` writes the cell it
checks, and that is a parameter of the one reader, said out loud.** The arm
passes `--sealing`, under which the `Broad gate` arm of the last record
prints its state and does not fail, because the caller is the run that writes
that cell; every other arm is judged by the state read. The output names the
flag beside the state line. CI's workflow passes no flag. `seal`'s own check,
after the write, runs plain.

| The caller | The state today | The state after |
|---|---|---|
| CI (`hygiene.yml`), payload present | the payload | the payload |
| `new`, `close`, `seal`; `gh` says draft | draft | draft (observed by `gh`) |
| `new`, `close`, `seal`; `gh` says ready | ready | ready |
| `new`, `close`, `seal`; no `gh`, or `gh` fails | draft (assumed) | ready (unknown; printed) |
| the broad gate's chain arm; `gh` says draft | draft (assumed, whatever `gh` says) | draft; the `Broad gate` cell excused under `--sealing` |
| the broad gate's chain arm; `gh` says ready | draft (assumed) | ready; the `Broad gate` cell excused under `--sealing`; an unchecked `Pass` or `nobody` beside `Pass` fails here, where `seal` refused them one arm later |
| the broad gate's chain arm; no `gh` | draft (assumed) | ready (unknown; printed); the cell excused |

Failure direction: blocks more, in one population — a machine with no
pull-request payload and no `gh` that can answer. There `new` and `close`
exit 1 on the record they just wrote, saying which state was assumed and why,
and the record is written all the same; today they exit 0 by assuming. That
is the policy table's third row applied where it was being quietly
overridden. Prompt budget: zero; nothing asks. Platform honesty: `gh` is
invoked by name and its absence is one of the shapes a case pins.

### J5 — the five doubled judgments become one function each

Each pair below is one judgment written twice, and the inventory's observation
is that they are *argued equivalent by construction* in a docstring
(`floor_and_fixes` :1982–2047) rather than being one function. The repair is
the same for all five: a pure function in `chain_check.py` over the record's
cells, which `chain_check.py` feeds from `HEAD` and `round_record.py` feeds
from disk. The text source is the parameter; the judgment is not.

| Judgment | The one function (proposed) | What it takes | Who calls it |
|---|---|---|---|
| a record's three facts for the floor | record_facts | a record's readable lines → (floor met, run reopened, closed on a fix), through `yes_or_no`, `says_reopened`, `closed_with_a_fix` | `stopping_floor` for each later record at `HEAD`; `floor_and_fixes` for each earlier record on disk |
| the two walks after a floor record | floor_walks | the facts of one run in round order → for every floor record, the fix-closing records after it and the count walk's spent count and whether it stopped | `stopping_floor` (errors and notices), `floor_and_fixes` (the printed bound) |
| where a run is cut | cut_runs | the `Fix of a fix` counts in round order → the runs, cut after a `second` its run counted | `runs_of` over `fof_of`; `current_run` over `fof_count_of` |
| the gate ran before the round it seals | gate_before_review | the resolved gate commit and the `Target SHA` cell → premature at `<sha>`, divergent at `<sha>`, or neither | the `broad_gate` arm (premature fails, divergent prints); `seal` (premature refused) |
| the close prefixes a Grounds cell carries | close_prefixes | a Grounds cell → the commits of the `fixed at <hex>` segments at the head of the cell, in the order `close` joined them with `; ` | `doubled_grounds` (two or more fails); `close` (one or more refuses the re-close) |
| the one row with a label; the one `Pass` box | fields and pass_boxes | the record's rows → every row carrying the label; the lines → every `Pass` box | `field` (the value when exactly one, None otherwise), `pass_checked` (None when not exactly one), `check_round` (an error naming the count when a label or the box appears more than once), `field_index`, `close`, `seal` (refuse as today, through the same count) |

What the disagreements resolve to, stated per pair:

- **A doubled close is read at the head of the cell, where `close` writes
  it.** `doubled_grounds` searched the whole Grounds cell with `findall`, so a
  reviewer's grounds quoting *fixed at abc1234 in round 1* counted as a close.
  The generator writes `fixed at <sha>[ — <note>]` and joins a re-close in
  front with `; `, so the prefixes are the leading `; `-separated segments that
  begin `fixed at <hex>`, and prose later in the cell is prose. `close` keeps
  its other half, `old.startswith(grounds)`: that is the writer comparing the
  cell with what it is about to write, which is not a reading of the record's
  vocabulary.
- **A duplicated row or box fails the record at the pull request.** `field`
  took the first `| label |` row and `pass_checked` the first box, silently;
  the generator refused anything but one. The strict reading wins at both
  ends, in one new sentence per record: *the record carries `| X |` N times*
  or *N `Pass` boxes*, as an error, and `field` answers None for a label it
  cannot answer for. Measured: no record in the tree carries a duplicate label
  or a second box, so no committed record changes verdict.
- **The walks, the cut and the premature test resolve to no new answer**;
  each pair agrees today by construction, and the function is what keeps
  them agreeing. The generator's printed bound and the gate's error read the
  same walk, so #218's class — the line a session reads and the gate it then
  meets disagreeing about one cell — has one fewer way to reopen.

Failure direction: blocks more for duplicates, reads fewer cells as a doubled
close, and is otherwise unchanged in verdict. Prompt budget: zero.

## User scenarios & acceptance *(mandatory)*

One row per scenario; these are the review's stage-1 checklist and the
regression tests' skeleton. Each case named is seen red first (§15): against
the two-reader code, or with the one reader's call replaced by the old copy.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 — the panel's `capped` is the gate's reopening | Given a last record whose `Needs a fix` reads `**yes — 🟡 1**`, when the panel's `rounds` row is drawn, then it reads `<R> · capped`; given `yes` alone or `yesterday …`, then it reads `<R>` with no second row; given `yes — …` as before, unchanged | parametrized cases beside `test_rounds_says_capped_and_counts_what_was_deferred`, each asserting `rounds_rows` against `chain_check.says_reopened` on the same cell; red with `startswith` restored |
| S2 — one home, read once | Given a verdict cell in each row of J2's table, when deferred_home and issue_of read it, then the home and the issue are the table's | a parametrized case in `tests/test_chain_check_at_the_pull_request.py` (the reader's own module), and `rounds_rows`' and `chain_counts`' cases asserting through it; the fourteen prose cases are replaced, not kept |
| S3 — the release seal counts issues, not mentions | Given a record with `deferred #854 — fixed in 0.20.0 as #858` and `deferred #854`, when `chain_counts` counts, then `deferred` is 1 | a case in `tests/test_the_release_seal_is_drawn.py`; red with the `findall` restored |
| S4 — the fix table's home ends at the dash | Given a fix row `\| 3 \| deferred #854 — the run is capped \| why \|`, when `close` applies it, then the verdict cell reads `deferred #854` and the Grounds cell `#854 — the run is capped; <reviewer's grounds>` | a case in `tests/test_the_fixes_close_the_record.py`; red against today's `fix_table`, which writes `deferred #854 — the run is capped` into the verdict cell |
| S5 — the depth walk reads path forms | Given round 1's fixes added `u` in `mod.py`, round 2's finding sits at `` `mod.py#u` `` and its fix adds `v` in `mod.py`, when `close` runs, then it refuses depth 2 as today; given the same finding located by `` `u` `` alone, then `close` writes the record and `New units` carries `v (depth 1)` | the existing depth-2 cases in `tests/test_the_fixes_close_the_record.py` with their `Location` as a path form, and one case for the bare name; the bare-name case is red against today's `depth_two` |
| S6 — `location_units` is gone and nothing reads a name without a path | Given `round_record.py`, when it is read, then location_units and its five patterns are absent and `depth_two` calls `path_forms` | a grep-level case; `tests/test_a_fix_of_a_fix_is_counted.py`'s docstring at :176 names the function and is reworded |
| S7 — the check asks `gh` where it has no payload | Given no `GITHUB_EVENT_PATH` and a `gh` on `PATH` that answers `{"isDraft": true}`, when `chain_check` runs, then the state line says draft and names `gh`; given one answering `false`, ready; given one that exits non-zero, or none on `PATH`, then unknown, judged ready, naming what was tried | subprocess cases in `tests/test_chain_check_at_the_pull_request.py` with a stub `gh` script placed first on `PATH`; red against today's reader, which never asks |
| S8 — the generator writes no payload | Given `round_record.py`, when its writers are walked, then `write_record` is the only one | `test_the_record_is_generated.py`'s writers case, with `run_check` removed from the expected set; red before the edit |
| S9 — `--sealing` excuses one cell and says so | Given a last record whose `Broad gate` reads `not yet` on a ready pull request, when `chain_check --sealing` runs, then that arm prints and the exit is 0, the output names the flag; when it runs without the flag, exit 1 as today; given the same record with `Pass` unchecked, then `--sealing` still exits 1 | cases in `tests/test_chain_check_at_the_pull_request.py`; the broad gate's chain-arm case in `tests/test_the_seal_is_taken_once_by_the_sealer.py` asserts the flag in the kept `chain.txt` command line, replacing the `draft-event.json` assertion |
| S10 — the walks are one function | Given a run of records whose floor row, `Needs a fix` and verdicts take each combination the two docstrings enumerate (floor met then quiet then quiet; met then fix-closing then fix-closing; met then reopened without fixes; two floor records), when `stopping_floor` is asked at the gate and `bound_line` at the generator, then the gate's error and the printed bound name the same record and the same count | the existing cases in `tests/test_the_reopening_is_one.py`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` and `tests/test_the_record_is_generated.py` keep passing, and one new case asserts both answers from one fixture; red with either caller's old loop restored |
| S11 — a doubled close is read at the head | Given a Grounds cell `the reviewer wrote: fixed at abc1234 held in round 1` under a `fixed` verdict closed once, when `chain_check` runs, then no doubled-close error; given `fixed at def5678; fixed at abc1234 — note; grounds`, then the error as today | cases beside `doubled_grounds`'s; the first is red against `findall` |
| S12 — a duplicated row fails the record | Given a record with two `\| Needs a fix \|` rows, or two `Pass` boxes, when `chain_check` runs on a ready pull request, then it fails naming the label or the box and the count; given one of each, unchanged | cases in `tests/test_chain_check_at_the_pull_request.py`; red against first-wins |
| S13 — the documents say what the code does | Given each document sentence §*Data & interfaces* lists, when it is read, then it states the one reader's rule and no longer the removed one; the documents stay under the ceiling | `fold-check` in the suite; the prose pins in `tests/test_the_rules_have_one_owner.py` and `tests/test_the_reopening_is_one.py` |
| S14 — a script copied alone still exits 2 | Given each of the four scripts copied without its siblings, when it runs, then exit 2 and the refusal names what is missing, as before | `tests/test_a_script_copied_alone_exits_2.py`, unchanged: no new sibling is added |

## Data & interfaces

**One module, no new file.** `round_record.py` loads `chain_check.py` at
import (`load(CHAIN, …)` :264, exit 2 with a sentence when absent);
`broad_gate.py` loads it by path through its `load` (:357, `Refused`);
`release_seal.py` loads it lazily through `module(…)` (:272) and runs only in
this repository's release workflow. All three already hold the one reader's
module, so every function below is added to `chain_check.py` and nothing is
added to the sibling list `tests/test_a_script_copied_alone_exits_2.py`
enumerates.

**Added to `chain_check.py`** (names proposed; the build may rename, the
docstring of each states its class):

| Name | Reads | Class |
|---|---|---|
| deferred_home, issue_of | a verdict cell as `close` and `new` write it | owned |
| record_facts, floor_walks, cut_runs | a record's cells through the readers that exist | owned |
| gate_before_review | the `Broad gate` and `Target SHA` cells, and `git merge-base --is-ancestor` | owned over observed |
| close_prefixes | a Grounds cell as `close` joins it | owned |
| fields, pass_boxes | the field table and the `Pass` line | owned |
| the second source in `pull_request_state` | `gh pr view --json isDraft` | observed; absent or failing → unknown |
| `--sealing` | a flag on `main` | owned; printed in the state line |

**Removed:** `broad_gate.py`'s deferred_home, HOME_TOKEN, HOME_END and
draft_env; `round_record.py`'s location_units, LOCATION_UNIT_RE,
LOCATION_LINE_RE, FRAGMENT_RE, IDENTIFIER_RE, BARE_IDENTIFIER_RE,
pull_request_is_ready, and the payload branch of `run_check`; the two loops
in `stopping_floor` and the `seen` walk in `floor_and_fixes`; the loop in
`current_run`; the ancestry loop in `seal` (:4956–4969); the `findall` in
`doubled_grounds` and the `CLOSE_PREFIX_RE.match` half of `close`'s guard;
the `startswith("yes")` in `rounds_rows`; the `findall` in `chain_counts`.

**Tests that move.** The fourteen prose-home cells in
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (two cases) are replaced
by S2's; its `draft-event.json` assertion by S9's; the writers set in
`tests/test_the_record_is_generated.py` by S8's; the environment-leak case at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:9425` keeps its purpose
(a runner's payload must not reach a fixture) and re-pins what the leak now
does, which under `--sealing` is no longer a failure on `not yet`; the
docstring at `tests/test_a_fix_of_a_fix_is_counted.py:176` stops naming
location_units.

**Documents, by replacement.** `docs/round-record-spec.md` opening paragraph:
one sentence saying the check is the one reader of every cell and the
generator, the broad gate's panel and the release seal read a cell through it.
§*`Pass` has to be checked* table, third row's text: *not visible to the check
at all, and `gh` cannot say* — and the paragraph under it names `gh` as the
second source, keeps the override sentence, now true of the generator too,
and names `--sealing` as the one excuse the broad gate's chain arm carries.
§*The depth in `New units`*: the name-with-no-file sentence replaced by the
path-form one. `docs/review-chain-spec.md`, the paragraph *The vocabulary the
exit needs*: one sentence on where the home ends. `agents/sealer.md` (:123):
the `rounds` row reads `capped` where `says_reopened` says the run reopened.
`templates/sdd-round.md` `Fix of a fix` row (:44): unchanged, it already says
path forms. Each document is measured after its phase's edit; W1 holds the
fallback.

**Ledger rows that drift.** 172 released rows anchor on the 23 units this
work edits, counted by `grep` over `seal/ledger.md` and `seal/releases/*.md`:
`broad_gate.py#gate` 63 (the chain arm's command and environment sit inside
it), `chain_check.py#main` 27 (the flag), `round_record.py#close` 21,
`round_record.py#seal` 15, `chain_check.py#stopping_floor` 7,
`round_record.py#floor_and_fixes` 5, four each on `fix_table`, `depth_two`,
`current_run`, `chain_check.py#broad_gate` and `broad_gate.py#main`, and 18
across the other twelve. The three largest are drifted in this release by the
siblings too — #869 edits `gate`, #837 and #860 edit `main` and `close` — and
#836 is framing what a re-read costs. Each phase re-reads the rows its edit
drifts with `evidence-check --reverify --into seal/ledger/<this item>.md
--checked <date>`, and corrects the claim first where the edit made it false
(the rows on location_units, pull_request_is_ready and draft_env, and any row
that states the panel reads `startswith`).

## Open questions → questions.md

No row needs a person. `questions.md` holds the judgments the issue left open
that the tree answered, two measurements and three rows for the work.

Framed 2026-10-07 by framer, before the build.
