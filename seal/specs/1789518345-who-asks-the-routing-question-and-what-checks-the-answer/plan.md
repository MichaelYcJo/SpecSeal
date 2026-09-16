# Implementation Plan: who asks the routing question, and what checks the answer

<!-- seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-16 by the repository owner, when `smith` was spawned.

## Summary

Seven phases. Four change documents, two change code that reads those
documents, and the last writes the work item's own records.

**The order is documents before the check that reads them**, and inside the
documents it is the vocabulary before the question that uses it, then the party
that picks the act up before the party that puts it down. The two code phases
come last because each reads something the four before them settled: phase 5
reads the `Review` row, phase 6 reads the `Planning` row and the mark phase 3
introduces.

Nothing is renamed. Every vocabulary this work touches gains a value or a row;
no existing string changes, because 84 committed declarations parse under the
current ones and the commit gate goes back to asking for every declaration it
can no longer read.

## Technical context

| What | Coordinate | What it does today |
|---|---|---|
| the declaration reader | `hooks/routing.py#parse` | strict on `Review` and `Destination`, lenient on `Planning` and `Implementation` — a value outside either vocabulary reads as unanswered rather than taking the declaration down |
| the row walker | `hooks/routing.py#table_rows` | returns every two-cell row, unknown labels included, so a new axis needs no change here. The fourth axis arrived on that promise and needed none |
| the mark store | `hooks/implementer.py#write`, `hooks/implementer.py#stands` | writes and reads a per-axis, per-branch mark **in the git dir**. It does not travel, so CI never sees it |
| the notice | `hooks/implementer-notice.py#unfulfilled` | one line after a commit where a declared agent left no mark. Reminder-only, once per repository per session |
| the seal writer | `round_record.py#seal`, via `round_record.py#last_record` | sets the last round record's `Broad gate` cell. `last_record` **raises** when `rounds/` holds no `round-N.md` |
| the seal reader | `chain_check.py#broad_gate` | four states on the last record's cell. Reached only after the per-item walk passes the `straight to the PR` arm, which returns first |
| the broad run | `skills/verify/scripts/broad_gate.py#seal_record` | runs `round_record.py seal` on a green run and reads the word `sealed` out of its output |
| the question's home | `skills/implement/orchestration.md` §*Orchestrator: how the work is routed* | three checkboxes, one `multiSelect`, plus a fourth axis stated to be a record and not a box |
| the question's pins | `tests/test_waiver_decided_at_start.py` | seventeen cases over the template, the parser and the orchestration document |
| the design gate `smith` claims | `agents/smith.md`, phase 2, lines 53–72 | twenty lines asking a person, naming the three axes, and writing `routing.md` |
| the unsound inference | `agents/smith.md`, line 125 | *Where no frame was drawn, the ladder put the work below the rung that calls for one* |

### Five facts opened rather than taken from the tickets

- **0 of 84 work items carry a framer mark in `spec.md`.** One file matches a
  mark-shaped search and it is a scenario row in a spec *about* the notice, not
  a mark. #399's figure holds. *(executed — a grep over `seal/specs/*/spec.md`,
  then the one hit read)*
- **61 of 71 `plan.md` files carry the unfilled approval-line placeholder**, and
  3 of the 11 work items declaring `Planning | framer` are among them. This is
  what moves the approval-line arm from a refusal to a notice. *(executed — a
  script over every `plan.md` in the tree)*
- **The seal's two halves both fail on the no-rounds path, for two separate
  causes.** `chain_check.py` returns at the `straight to the PR` arm before it
  reaches `broad_gate`, and `last_record` raises rather than returning. Neither
  repairs the other. *(read)*
- **11 of 84 declarations answer `Planning | framer`; 16 answer `straight to the
  PR`; 68 answer `through the review chain`.** So the frame arm has a live
  corpus and the seal arm has one nearly as large. *(executed)*
- **`test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox` is named for
  `Planning` and this work adds a fifth axis that *is* a checkbox.** The case
  is about `Planning` and stays true; its name and its assertions both have to
  be read before phase 1 lands, or the suite reports a contradiction that is
  only in the naming. *(read)*
- **10 of the 11 work items declaring `Planning | framer` carry no mark**, the
  eleventh being this one. A release pull request carries every work item the
  release adds, so an arm with no cutoff refuses the next release into `main`
  for every framer-declared item in it — none of which could have written a
  mark that did not exist. `chain_check.py` already carries the mechanism: a
  constant read against the work item's own directory name, with everything
  below it printing instead of failing. The frame arm takes the same shape with
  its own constant, set to this work item's id. *(executed — the eleven
  directories read for a mark line)*
- **The waiver example at `agents/smith.md` lines 68–72 is not one of the three
  acts that go.** `tests/test_a_moved_rule_leaves_its_definition.py`'s docstring
  names it among the applications #107's phases 3 and 4 kept deliberately —
  *the smith's own waiver example as the patch §9's gate reads a commit out of*
  — so removing it would turn that module's stated carve-out into a lie. The
  span is named by **content**, not by the line range: the design gate, the
  routing batch and the `routing.md` write go, and the waiver paragraph with
  its `# RIDER:` stays where it is. *(read)*

### The failure scenario of the chosen approach, in six months

**The check compares two things the framer wrote.** The `Planning` row and the
mark in `spec.md` are both the framer's writes, so the arm catches a framer
that forgot one of them and nothing else. The day somebody reads a green
chain-check as evidence that a framer ran, they will be wrong, and the
disclosure list is the only thing standing between that reading and them.

The mitigation is that the list is in the module rather than in a ticket, and
S20 pins it. What it cannot mitigate is a reader who does not open the module.
That is the trade, stated rather than left to be found: the arm is worth having
because a declared framer with no frame at all is the reported failure and this
catches it, not because it proves a framer ran.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The question** — one `multiSelect` with four boxes and no question 1 | The answer given most often is four ticks, which is #88's complaint with one more tick on it. And the exit — *this change does not get the apparatus* — has nowhere to live, because it is not a party that does or does not run | **Rejected** |
| **The question** — #88's own two presets plus three axes | Five options in one question, which the four-option cap refuses. This is the wall #88 measured | **Rejected**, and it is why the shape below is two questions |
| **The question** — two questions in one call, question 1 offering *as a work item* / *straight in* | *End to end without stopping* is unsayable for anybody choosing per-axis: *smith and warden but no pull request, and do not come back* has no expression | **Rejected.** The box moved into question 2, which is what brings that question to exactly four |
| **The question** — two questions in one call: `automation` · `per axis` · `no work item`, and question 2's four boxes | The cap is spent at question 2 and a fifth box breaks it. Stated in `spec.md` §*The ceiling* rather than left to be discovered | **Chosen.** The answer given most often is one click, the axes are still visible under `per axis`, and the exit is a peer of neither |
| **Option 3's label** — `no skill`, the owner's word | `skills/` is a live concept in this repository and what the option declines is the apparatus, not a skill. `tests/test_one_word_one_meaning.py` exists for exactly this | **Rejected**, and it is a naming call the owner can overturn at this approval |
| **Option 3's label** — `no work item` | Names what does not happen, in the repository's own word, and its description names the five things that do not run | **Chosen** |
| **Option 2's label** — `some of it` | Names a quantity, and ticking all four boxes under it produces what `automation` produces. It describes neither what runs nor what is decided | **Rejected** |
| **Option 2's label** — `per axis` | Names what the option does: it hands the decision to the boxes. #88's own word for this option | **Chosen** |
| **Option order** — the exit second, as the owner sketched it | The exit is the least-verified path and one click. `skills/implement/orchestration.md` already warns that a preset makes that path the cheapest to press, and second is where a reader's eye lands after the first | **Rejected** |
| **Option order** — the exit last | Cheapest to press is not made cheaper by position, and the cost is in the description either way | **Chosen.** It is the smaller of two defences and it costs nothing |
| **The fourth box's row name** — `Automation` | Reads as *turn everything on*, which is what the three party boxes already say, and it collapses into them | **Rejected** |
| **The fourth box's row name** — `Unattended` | Names the property but not in words that answer a reader's question. The value would have to carry all of it | **Rejected** |
| **The fourth box's row name** — `Attendance`, values `nobody at the keyboard` · `somebody may be asked` | Names neither a party nor an agent, and the value answers what a reader six months later actually asks | **Chosen by the frame, OVERTURNED by the owner at the approval** (`questions.md` Q1). `Attendance` reads as a school register before it reads as *was anybody at the keyboard*, which is what `templates/config.md`'s naming rule refuses |
| **The fourth box's row name** — `Automation`, values `yes` · `no` | Reads as *turn everything on* where the row sits alone — but it does not sit alone: question 1's first option is labelled `automation`, so the button pressed and the row recorded are one word, which is what #88 asks for one level down. The word's 40 occurrences in this tree are all the ordinary English noun, so nothing in the vocabulary collides | **Chosen, at the approval.** The values give up carrying their own meaning — `no` is *this run may stop to ask*, not *a person did it by hand* — and that half moves into the template comment |
| **The fourth row** — required in `hooks/routing.py#parse` | 84 committed declarations carry no such row, and each becomes "not a declaration" — which re-opens the commit gate on every branch that already answered | **Rejected** |
| **The fourth row** — optional, absent reads as unanswered | A question that is asked always writes one of the two values, so an absent row means the question was never asked. That is the three-state reading `Implementation` already has | **Chosen.** It is also what keeps a chosen `no` from being byte-identical to an unread question |
| **Renaming `straight to the PR`** to name what does not run | 16 declarations stop parsing, the commit gate goes back to asking on each, and `chain_check.py` reports them as unreadable rather than as declarations | **Rejected.** The measured defect is in the question's label, and that is where the repair lands |
| **The mark** — a new file, `seal/specs/<id>/framed.md` | A fourth file in the set, whose only content is one line, for a fact that belongs to `spec.md` | **Rejected** |
| **The mark** — a line at the foot of `spec.md` | `routing.md` and `plan.md` already end with a line of exactly this shape, so three feet-lines share one convention rather than becoming three | **Chosen** |
| **The seal's home** — invent a round record for a run with no `warden` | Records a review that did not happen, and it is #241's problem taken on without #241 | **Rejected** |
| **The seal's home** — a cell in `routing.md` | Turns a declaration given before the first edit into a running log, and `hooks/routing.py#parse` would have to tolerate a row written at the end | **Rejected** |
| **The seal's home** — `seal/specs/<id>/broad-gate.md` where no round record exists | Named for the command that writes it and the cell it holds, so no new word enters the vocabulary. One writer picks the home from what exists; one reader does the same | **Chosen** |
| **The check's home** — a refusal inside `hooks/implementer-notice.py` | A `PostToolUse` hook cannot block by design, it reads a git-dir mark that never travels, and a refusal there is a fourth thing that can stop a session | **Rejected** |
| **The check's home** — a new step in `.github/workflows/hygiene.yml` | #420 thins that workflow next release, and a CI-only check reaches nobody working in a repository that never installed it | **Rejected** |
| **The check's home** — an arm in `chain_check.py` | The walk over every declaration the pull request adds or changes already exists, and so do both callers, one local and one in CI | **Chosen** |
| **The approval-line arm** — a refusal, as #399's *Done when* asks | 61 of 71 `plan.md` files in this tree carry the unfilled placeholder. A refusal that goes red for nearly every honest branch teaches people to write none, which is the reasoning `chain_check.py`'s own docstring gives for `unverified_check.py` | **Rejected**, on a measurement the ticket did not have |
| **The approval-line arm** — a notice | The gap is reported on every run and nothing honest is stopped. Promotion to a refusal becomes a ticket once the notice has been seen on a few releases | **Chosen** |
| **Recording the `no work item` exit** — a shared file every branch appends to | `CLAUDE.md`'s fragment rule forbids it, and the conflict arrives after the broad gate has run | **Rejected**, and it is why the record is a ticket rather than a phase |

## How this branch avoids breaking the machinery it edits

This branch edits the reader of its own `routing.md`, the definition of the
agent that framed it, the definition of the agent that will build it, the
checker that will judge its pull request, and the subcommand that will seal it.
Four rules keep the repair from landing in the middle of the machinery that
judges it.

**1 — This work item's own `routing.md` is not rewritten.** It is committed, it
parses under the current reader, and phase 1 adds only **optional** rows — so a
declaration without them stays a declaration. That is what keeps this branch's
own file valid through its own change, and it is measured rather than hoped:
84 declarations gained the fourth axis with no edit to any of them, and
`hooks/routing.py#table_rows` needed no change at all.

**2 — The framer's definition changes after the framer has run.**
`agents/framer.md` is read at spawn time, so phase 3's edit cannot reach the
session that wrote these documents. One consequence has to be written down
rather than discovered: **this work item's `Framed` line is added by `smith`,
not by the framer it names.** The line records a true fact — the framer did
frame this — and it is the one instance where the party that writes the mark is
not the party it names. Every work item after this one has the framer write it.

**3 — No phase runs `round-record` against this work item's own `rounds/`.**
Phase 5 changes where `seal` writes when no rounds exist. This work item
declares `through the review chain` and will have rounds, so `seal` takes the
round-record path here and phase 5's new path is exercised only in throwaway
clones, through the fixtures the existing cases already use. The one directory
the generator must not be pointed at during the build is this work item's own.

**4 — Phase 6's arm judges this branch's own pull request, on purpose.** This
work item declares `Planning | framer` and will carry all three documents and
the mark, so the arm's passing side is exercised by the branch that adds it. If
phase 6 is wrong, the cheapest place to find out is a pull request whose author
is still holding the diff. The risk is named rather than avoided, because
avoiding it means shipping the arm unexercised.

A fix pass during the rounds may repair any of these files. Rule 3 is the only
line it must not cross.

## Phases

Vertical slices — each phase ends with something runnable and verified. **Every
`Verified by` cell names its command and the mutation that makes the new case
red** (`agent-contract` §15). Exit codes are read directly, never through a pipe
(§1): `cmd >/dev/null 2>&1; echo $?`.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The vocabulary.** `hooks/routing.py` gains the `Automation` row with its two answers and the row recording which answer was pressed, both optional and both lenient, on the terms `Planning` has. `templates/sdd-routing.md` gains both rows with the comment a session follows. `test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox` is read first and reworded where it names `Planning` by position rather than by name | `bin/test tests/test_waiver_decided_at_start.py tests/test_routing_is_recorded.py`. **Red-first:** put the new answers into the strict branch of the reader, so a value outside the vocabulary takes the declaration down — the case asserting an unknown `Automation` value still parses as a declaration goes red. **Second direction, equally required:** a case parsing all 84 committed declarations, none of which carries the row, stays green; delete the row's default and it goes red | `2f302790` |
| 2 | **The question.** `skills/implement/orchestration.md` §*Orchestrator: how the work is routed* rewritten: two questions in one call, question 1's three options with their descriptions in the order `spec.md` fixes, question 2's four boxes with their checked **and unchecked** meanings, the sentence that the order is the specification, and the sentence that the cap is spent and a fifth box breaks the shape. The owner's personal-instructions paragraph is named as owing the same change and left to the owner | `bin/test tests/test_waiver_decided_at_start.py`. **Red-first:** swap question 2's first two rows — the case reading the row order out of the table goes red naming the property-of-the-run box's position. **Second mutation:** delete the unchecked clause from the `review with warden` box — the case asserting `nothing reviews` goes red, which is what pins the measured instance's repair rather than its statement | `4b01553b` |
| 3 | **The framer picks the acts up.** `agents/framer.md`: the acts become gather, judge, plan; the routing batch is the framer's, written and committed from the template in a command of its own, before its own three files; `questions.md` becomes the residue and each row owes a reason the tree could not answer it; the framer writes the `Framed` line. `templates/sdd-spec.md` gains that line at its foot | `bin/test tests/test_waiver_decided_at_start.py tests/test_the_set_a_work_item_always_has.py`. **Red-first:** delete the separate-command clause from the framer's routing paragraph — the case asserting it goes red. That clause is the one whose absence costs a lost file rather than a lost sentence: the commit gate denies the whole call, so `write && git add && git commit` writes nothing. **Second mutation:** remove `judge` from the three acts — the persona case goes red | `e049f3b9` |
| 4 | **`smith` puts them down.** Three acts removed from `agents/smith.md`'s phase 2 — the design gate, the routing batch, the `routing.md` write — replaced by the sentence that phase 2 is the caller's spawn. **The waiver paragraph and its `# RIDER:` stay**, for the reason above: the span is content, not the line range. Line 125's inference removed and not rewritten elsewhere. Added: where `routing.md` declares a framer and no `spec.md` exists, `smith` stops and says so rather than building | `bin/test tests/test_a_moved_rule_leaves_its_definition.py tests/test_the_rules_have_one_owner.py`. **Red-first:** paste the design-gate paragraph back under a new heading — the absence case goes red naming `agents/smith.md` and the span. That is the mutation this module was built for and the one a presence-only check cannot catch. **Second mutation:** delete the stop instruction — the case asserting `smith` refuses an absent declared frame goes red. **Third, the opposite direction:** delete the waiver example — the case that keeps it as smith's own application goes red, which is what stops the removal from over-reaching | `72edbd49` |
| 5 | **The seal's home where no round record exists.** `round_record.py seal` writes `seal/specs/<id>/broad-gate.md` when `rounds/` holds no record, and the last-record path is unchanged where one does. `chain_check.py`'s `straight to the PR` arm reads that cell instead of printing *nothing required* and returning | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_chain_check_at_the_pull_request.py`. **Red-first:** restore the raise in the no-rounds path — the case asserting `seal` writes the file rather than refusing goes red at exit 2. **Second mutation, the reader's half:** restore the early return in the direct arm — the case asserting a ready pull request with no cell exits non-zero goes red at exit 0, which is the exact silence this phase removes. **Third:** a work item **with** rounds still seals onto its last record, byte-identical to today | `d177df33` |
| 6 | **The check reads the declaration against the frame.** A new arm in `chain_check.py`: `Planning \| framer` owes `spec.md`, `plan.md` and the framer's mark, each refused by name; a mark reading `the session` beside a row reading `framer` refused as a disagreement; an unfilled approval line reported and not refused; everything below the cutoff printed rather than failed, on the mechanism the broad-gate arm already uses, with the constant set to this work item's id. The six things it cannot see written in the module beside it | `bin/test tests/test_chain_check_at_the_pull_request.py`. **Red-first:** empty the arm's failure collection before it is returned — every new refusal case goes red at exit 0, which is #142's class and the one mutation a presence-only suite misses. **Second mutation:** make the approval-line branch append to the errors list rather than the notices list — the case asserting exit 0 with the notice present goes red, which pins the measured 61-of-71 decision rather than restating it. **Third mutation:** drop the cutoff comparison so every item is judged — the case for a work item below the constant goes red at a non-zero exit, which is the retroactive red the 10-of-11 measurement forecloses. **Fourth:** delete one line of the disclosure — S20 goes red | |
| 7 | **The work item's own records.** `changelog.md` and `seal/ledger/1789518345-….md` in this repository's fragment convention, and `overview.md` carrying every divergence, what was not verified with who answers it, and the two tickets this work opens. The `Framed` line added to this `spec.md`, with rule 2's exception recorded in `overview.md` | `bin/evidence-check --strict .`, exit 0 read directly. **Red-first:** change one character of one new row's hash — the run reports that row drifted and the exit is non-zero, which is what shows the rows are anchored to content rather than accepted on sight. Then `bin/unverified-check --baseline origin/release/v0.12.0` | |

This table is also where the work records how far it got. There is no separate
task list. **Status is empty, or the commit that closed the phase** — a tick is
refused and so is `done`.

What a phase discovers and the next phase needs goes to
`seal/specs/1789518345-…/phases/phase-N.md`, from `templates/sdd-phase.md`, when
the phase closes.

## Operational impact

| Item | What a deployer must not miss |
|---|---|
| **Migration** | None. No existing vocabulary is renamed and every new row is optional, so all 84 committed declarations parse unchanged and no branch's commit gate changes behaviour |
| **New environment variable** | None |
| **New dependency** | None |
| **Compatibility break** | None in the tree. One in the **question**: a session on this plugin asks two questions where it asked one, and the answer given most often becomes one click rather than three ticks. Anybody scripting against the old three-box shape is reading a shape that no longer exists |
| **Prompt budget** | Unchanged in count and reduced in size. One batch before the first edit, as today; it moves from the spawning session to the framer, which is the party that already runs an interactive phase, so the two batches that existed become one. The new arm in `chain_check.py` puts no question in front of anybody — it refuses at a pull request, where nobody is sitting |
| **Failure direction** | The new arm **blocks more**. That is the cheaper mistake here: a wrong refusal costs one pull-request run and names the file it wants, where a wrong allow is the reported defect — a work item that declared a framer, drew no frame, and reached the pull request with nothing noticing |
