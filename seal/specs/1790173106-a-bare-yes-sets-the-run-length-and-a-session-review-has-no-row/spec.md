# Feature Specification: a bare `yes` sets the run length, and a session review has no row

<!-- seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/spec.md
Frames MichaelYcJo/SpecSeal#138 and MichaelYcJo/SpecSeal#241, step 0 of the
`release: 0.15.0` milestone. Record language: English (`seal/config.md` has no
`Record language` row). Every claim below is **read** unless it says
otherwise; the framer executed nothing. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask a person has to argue for itself. Both decisions below are taken from the tree, and neither adds a question or a prompt |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | #138 changes what `chain_check.py` refuses, and #241 rewrites one option of the commit gate's prompt. Each phase owes a test seen red, a failure direction, a prompt budget and platform honesty; D&I below states them |
| `docs/review-chain-spec.md` §*The bound has a floor, and a quiet round is where it stops* | The floor's count restarts at the first later record whose `Needs a fix` says the run reopened. That is the sentence a bare `yes` exploits |
| `docs/review-chain-spec.md` §*commit-review-gate* › *Review arm*, the table *The declaration says / At the commit / At the pull request* | Its `straight to the PR` row reads *nothing required; the declaration is printed*. `chain_check.py#direct_seal` has required `seal/specs/<id>/broad-gate.md` at a ready pull request since 0.12.0 (`CHANGELOG.md` §0.12.0, *The broad gate gets a home where no round record exists*; `DIRECT_GATE_FROM = 1789518345`). The row is false, and no `docs/` policy names the file at all |
| `docs/review-chain-spec.md` §*Two records, and what each of them says*, the `Fixes checked by` table, row *anything else, `the session that wrote them` included → fails* | The chain already refuses the author as the checker of its own fixes. A third `Review` answer whose record is written by the author would write the opposite into the same vocabulary |
| `skills/agent-contract/SKILL.md` §6 | *a review that certifies itself is what the commit gate exists to catch* |
| `skills/implement/orchestration.md` §*Orchestrator: how the work is routed*, Question 1 option 3 and the paragraph *What must not happen instead is a standing waiver* | `no work item` is an answer of the routing question, and its recorded form is `[no-review]` in front of every commit. *There is no third value meaning no enforcement anywhere* |
| `seal/specs/1790138190-settle-leaves-twelve-directories-with-no-way-out/spec.md` D1 | *A fold is not a work item.* The release-preparation commit is the same class of change, and #517 settled how that class runs outside the chain |
| `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/spec.md` §Scope | A change confined to `docs/` and `seal/` is judged like any other, and a documentation pass that should reach nobody declares `straight to the PR` before the first edit. This frame builds on that and re-decides none of it |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | A defect belongs to a class; a change to a line a person reads is documented and pinned in the same commit; a new case is seen red first |

## Scope

**In one line: `Needs a fix` is held to the same vocabulary as the floor row
beside it, at the reader and at the writer; and the state the ticket calls a
session review already has its record — the sealer's `broad-gate.md` under
`straight to the PR` — so this work writes that where every document still
says the answer requires nothing, and adds no third answer.**

### #138 — decided: option 1, refuse a bare `yes`, at both ends

**The ticket's asymmetry holds in the tree today.** `chain_check.py#stopping_floor`
refuses `Loses a record or crashes` at `yes` with no reason (*says `yes` and
does not say what*) and passes `Needs a fix` at the same value: its own-row
read computes only `word_needs` (NAME NOT IN TREE: phase 1 replaced the local
with `says_reopened`'s answer) and never the reason. `run_reopened` returns
`True` for a bare `yes`, so the count walk stops there. `round_record.py#terminal_value`
copies either terminal line into the record refusing only a word outside the
vocabulary, so the writer accepts the bare `yes` too. And
`round_record.py#bound_line` reads the same cell a third time, inline
(`chain.yes_or_no(...)[0] == chain.FLOOR_YES`), so a printed bound and the
gate can be made to disagree by one cell (#218's class).

**The ticket's cost still holds after #161.** The reopening walk added by
`REOPEN_FROM` reads `wrote_fixes`, not `Needs a fix`, so it does not fire on
a record that wrote no fixes. Read against the code: `R1 (floor no) → R2
(Needs a fix: yes, no fixes) → R3` passes today, and the same run with `R2:
no` fails at R1 with *the count … reaches 2*. Three characters buy one
uncounted record.

**Why option 1 and not 2 or 3.** `plan.md` §Alternatives carries the table.
The short form: option 2 keeps two rows of one vocabulary disagreeing about
the same three characters, in a checker whose stated design is *one reader
for both* (`yes_or_no`'s docstring); option 3 makes the rule depend on how
many files follow, which no other refusal in this checker does. Option 1 is
one branch the row beside it already has, and the reviewer is already told to
write the reason (`agents/warden.md` §Report: `Needs a fix: yes — <the
findings that do>`).

**What is in:**

1. `chain_check.py`: one reader for the reopening question — a function that
   returns `True` for `yes — <what>`, `False` for `no` (with or without a
   reason), and `None` for a bare `yes`, an empty cell or a word outside the
   vocabulary — used by `stopping_floor`'s own-row read and by `run_reopened`.
   A bare `yes` is refused on the record that carries it, in the floor row's
   words (*says `yes` and does not say what*), under `NEEDS_FROM`'s
   grandfathering: an error for a work item begun at or after it, a notice
   before. In the walk it reads as `None`, which is *not a reopening*, so it
   can no longer stop the count — the direction `run_reopened`'s docstring
   already states: *a row this cannot read must never be the thing that
   quiets a refusal.*
2. `round_record.py#terminal_value`: a bare `yes` in either terminal line
   (`Needs a fix`, `Loses a record or crashes`) is refused at the point of
   writing, in the shape `written_late_cell` already uses (*carries no
   reason*). The class is both lines, not the one the ticket names.
3. `round_record.py#bound_line`: reads the reopening through the reader of
   item 1 rather than its own `== FLOOR_YES`, so the printed bound and the
   gate cannot disagree about this cell.
4. Documents: the `Needs a fix` table in `docs/review-chain-spec.md`
   §*`Needs a fix` — the row the bound above rests on* gains the row *`yes`
   with nothing after it → fails on a work item begun at or after
   `NEEDS_FROM`, prints before it*; `templates/sdd-round.md`'s `Needs a fix`
   comment says the same; `chain_check.py`'s module docstring row for
   `Needs a fix` names the refusal. `agents/warden.md` needs no change — it
   already shows the shape.
5. Tests, each seen red first: in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`,
   a bare `yes` fails after the cutoff and prints before it; a bare `yes` on
   a later record does not stop the count; in the round-record suite, `new`
   refuses a report whose terminal line is a bare `yes`, for both labels; the
   printed bound agrees with the gate on a bare `yes`.
6. The ledger rows anchored on `chain_check.py#stopping_floor` (6),
   `#run_reopened` (1), `#yes_or_no` (1), `round_record.py#bound_line` (2)
   and `#terminal_value` (1) are re-read after the change, and the new claims
   go in this work item's fragment. Row F8 (*the permissiveness is
   deliberate*) is the one whose ground moved: its claim is REMOVED from
   `seal/ledger.md` in this branch and the new claim written into the
   fragment (`CLAUDE.md`, *A row whose anchor a change removes is REMOVED*).

### #241 — decided: no third `Review` answer; write what the second one already requires

**Three of the ticket's coordinates have moved, and the move is most of the
answer.**

| The ticket says | The tree today |
|---|---|
| `straight to the PR` requires nothing at all | `chain_check.py#direct_seal`: a ready pull request for a work item begun at or after `DIRECT_GATE_FROM` must carry `seal/specs/<id>/broad-gate.md`, the sealer's stamp — the SHA the one broad run happened at and the base it was compared against. Since 0.12.0 |
| the only way to produce a record is `round_record.py new`, and `--report <file>` is required | `--report` is optional; the report is read from `rounds/round-N-report.md`, where the reviewer leaves it (#228). A report file is still required; who wrote it is checked by nothing |
| nothing exempts a documentation-only change | decided, not moved: #518 measured it and refused the exemption; a documentation pass declares `straight to the PR` before the first edit |
| the release-preparation commit waives the gate by name every release | still true (`docs/release-checklist.md` §4), and the routing question has since gained the answer it belongs to: Question 1's `no work item`, whose recorded form is `[no-review]` per commit. #517's D1 settled the fold the same way |

**What a session that wrote and checked its own code can record, and why it
is not a round record.** The chain's record is worth something because a
party other than the author wrote it: `Fixes checked by` refuses *the session
that wrote them* in `docs/review-chain-spec.md`, `Ran by` is *the spawning
session's row, never the agent's own* (`chain_check.py#ran_by`), and §6 of
the contract names self-certification as what the gate exists to catch. A
third answer whose record the author writes would put the state those three
refuse into the same vocabulary as the two they guard. What the author's own
check leaves that a checker can read is what it **ran**: the broad gate at a
SHA against a base. That is `broad-gate.md`, and `straight to the PR` already
owes it. The reading half — *here is what I checked* — is prose, and
`agent-contract` §5 says what prose is worth as evidence.

**So the defect is in the documents, not in the vocabulary.** Seven places
say the direct answer requires nothing, and a session reading any of them
concludes it has no honest answer for a change it checked itself:

| Where | Says |
|---|---|
| `docs/review-chain-spec.md` §*Review arm*, the declaration table | `straight to the PR · silent · nothing required; the declaration is printed` |
| `skills/code-review/scripts/chain_check.py` module docstring | `straight to the PR — nothing required — the declaration is printed` |
| `skills/implement/orchestration.md` §*What the answer writes*, the four-combinations table | `direct · open the PR · … · nothing required` |
| `skills/implement/orchestration.md`, the closing paragraph of the routing section | *the direct answer [is checked] by the token in every command* — false since the declaration silenced the arm for either answer |
| `hooks/commit-review-gate.py#judge`, option 1 of the review arm's prompt | *`straight to the PR` is the one CI requires nothing for* |
| `tests/test_routing_is_recorded.py#test_the_first_option_does_not_let_the_model_pick_the_review_answer`, docstring | *`chain_check.py` requires nothing of it at the pull request* |
| `templates/sdd-routing.md`, the `Review` comment | names the two answers and what neither owes |

**What is in:**

7. Each of the seven says what the direct answer requires — the sealer's
   `broad-gate.md` at a ready pull request, for a work item begun at or after
   `DIRECT_GATE_FROM` — and what it turns off, which is the reviewer alone.
   The gate prompt's option 1 keeps every phrase
   `tests/test_routing_is_recorded.py` asserts (`USER'S answer`, both
   spellings).
8. `docs/review-chain-spec.md` gains, beside the declaration table, one short
   paragraph stating why there are two answers and not three: what a
   session's own check leaves that CI can read, and where it lives. This is
   the sentence a later reader of #241 finds instead of the ticket's
   proposal.
9. `docs/release-checklist.md` §4: one sentence naming the waiver as the
   routing question's `no work item` answer (`skills/implement/orchestration.md`
   §Question 1), so the release sequence reads as declaring its class rather
   than stepping around a gate. #517's D1 is the precedent.
10. A pinning test in the shape of `NO_CHECK_READS`
    (`tests/test_the_record_is_held_to_the_floor_and_the_depth.py`): for each
    of the seven files, the sentence that stands (`broad-gate.md`, or the
    file's own wording of the seal) and the sentence that is gone (*nothing
    required* / *requires nothing* of the direct answer). Seen red by
    restoring one of the old sentences.
11. This work item's `changelog.md` and `seal/ledger/<id>.md` fragments.

**Out, one line each:**

- **A third `Review` answer** (`reviewed by the session`), for the grounds
  above and in `plan.md` §Alternatives. If a person overturns this, the
  surfaces are the ones the spawn prompt listed: `hooks/routing.py`
  (`REVIEW_ANSWERS`, strict), the gate prompt, `chain_check.py`'s routing
  branch, the template, the `CLAUDE.md` block, the orchestration table, and
  every test that enumerates the two spellings.
- **Renaming `straight to the PR`.** `routing.py#parse` is strict on
  `Review`; a new spelling makes every committed declaration *not a
  declaration* and reopens the commit gate on each of them.
- **The `CLAUDE.md` routing paragraph and `templates/claude-md-block.md`.**
  Their sentence — *nothing reviews this code before the pull request* — is
  about the reviewer and stays true. Both are pinned against each other by
  `tests/test_waiver_decided_at_start.py`, and moving them for a sentence
  that is not wrong is a cost with no defect behind it.
- **The routing question's box 3 text** (*nothing reviews this code before
  the pull request*), same reason.
- **Making the release-preparation commit a work item** that declares
  `straight to the PR` and takes its seal through `broad-gate --record`.
  #517's D1 decided the fold is not a work item because every fold run as one
  leaves a directory behind; the preparation commit is the same class.
- **The gate denying a commit on a branch whose `routing.md` names another
  branch** (the ticket's measured cost). One declaration per branch is the
  design (`templates/sdd-routing.md`, `Branch`), and the ticket's two cases
  were a temporary branch and a detached HEAD.
- **Whether `Ran by` should accept or refuse `the session on <model>`.** No
  reader depends on it after this decision; it is noted in `questions.md` as
  a measurement nobody is waiting on.
- **`#218`, `#174` and the rest of work item A.** `plan.md` §Alternatives
  says why none is pulled in and what A inherits.
- **The `docs/review-chain-spec.md` split (#526).** Waits for B.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given a work item begun at or after `NEEDS_FROM` whose record reads `\| Needs a fix \| yes \|`, when `chain_check.py` runs at the pull request, then it fails naming the row and *does not say what* | a case in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`, seen red against the current checker |
| A2 | The same record under a work item begun before `NEEDS_FROM`: prints, does not fail | a case beside A1; the grandfathering is `needs_excused`, not a new cutoff — no committed record at or after the cutoff carries a bare `yes` (read: 20 live records, every `yes` carries a reason; no fixture under `tests/` does either) |
| A3 | Given `R1` met the floor and `R2` reads a bare `yes` with no `fixed` verdict and `R3` follows, then the count at `R1` reaches 2 and fails, and `R2` fails on its own row — the bare `yes` no longer stops the count | a case in the same file, seen red: today `R1` passes because `run_reopened` returns `True` |
| A4 | `R2` reading `yes — 🔴 1` still stops the count, and `no — <why>` is still `no` | the existing cases `test_the_verifying_round_may_reopen_the_run_and_its_fixes_get_a_reader` and `test_needs_a_fix_takes_a_reason_after_either_answer` stay green |
| A5 | Given a report whose terminal line is `Needs a fix: yes` or `Loses a record or crashes: yes`, when `round_record.py new` runs, then it refuses naming the label and that the line carries no reason | a case in the round-record suite for each label, seen red against the current `terminal_value` |
| A6 | Given records where `R2`'s cell is a bare `yes`, `round_record.py new`'s printed bound says the same thing the gate does | a case beside the existing `bound_line` cases; the differential #218 ran is the model |
| A7 | A reader opening `docs/review-chain-spec.md` §*`Needs a fix`* finds the bare-`yes` row; opening `templates/sdd-round.md` finds the same sentence; the checker's module docstring names it | a `NO_CHECK_READS`-shaped case, seen red by deleting the row |
| A8 | A reader opening any of the seven places in the #241 table finds what `straight to the PR` requires at a ready pull request and finds no sentence saying it requires nothing | the pinning case of item 10, seen red by restoring one old sentence |
| A9 | `hooks/commit-review-gate.py`'s option 1 still carries `USER'S answer` and both spellings | `tests/test_routing_is_recorded.py`, unchanged and green |
| A10 | Nothing the commit gate decides changes; nothing `chain_check.py` decides for a `through the review chain` record without a bare `yes` changes | the two gate suites and `tests/test_chain_check_at_the_pull_request.py` unchanged and green; `tests/test_every_declaration_in_this_repository_still_parses` green |
| A11 | `evidence-check --strict` passes on the branch with the moved rows re-read | executed by the phase that moves them |

## Data & interfaces

No schema, file format or vocabulary changes. `Needs a fix` keeps its three
readable values (`no`, `no — <why>`, `yes — <what>`); the fourth (`yes` alone)
moves from *accepted and load-bearing* to *refused where the floor row
refuses it*. `Review` keeps two answers. `broad-gate.md` is not touched.

**The four things `CONTRIBUTING.md` asks of a gate change:**

- **A test seen red** — A1, A3, A5, A6, A7, A8, each by the mutation in its
  row.
- **Failure direction** — #138 blocks more: one cell value that passed now
  fails, on records written at or after `NEEDS_FROM`; measured on the tree,
  zero committed records are affected. #241 changes no verdict; it changes a
  prompt's sentence and six documents.
- **Prompt budget** — zero added. #138 fails at the pull request, where
  nobody is sitting; #241's edit to the gate prompt changes its text and not
  when it fires.
- **Platform honesty** — no process inspection, no new shell construct.

**Ledger rows this moves.** `seal/ledger.md` rows anchored on
`chain_check.py#stopping_floor` (6), `#run_reopened` (1), `#yes_or_no` (1),
`round_record.py#bound_line` (2), `#terminal_value` (1) — the module
docstring is not inside `#main`, so the six rows anchored there should not
drift; rows anchored on the `docs/review-chain-spec.md`
headings the #241 paragraph lands under. The phase runs `evidence-check` and
re-reads what drifted; F8 is REMOVED and re-founded in the fragment.

## Open questions → questions.md

Three rows, none a person's. `questions.md` lists the judgments the tickets
left open that this file took, so nobody reopens them.

Framed 2026-09-23 by framer, before the build.
