# Feature Specification: a run's rounds come mostly from the tool's own fixes and records

<!-- seal/specs/1788597030-…/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | *verification that runs unattended is this project's first goal* — and #161 measured that the last run did run unattended, at fifteen rounds and 22 h 47 min. The cost is rounds and records, not questions, and this work is judged on that cost |
| `docs/review-chain-spec.md` §*The bound has a floor* … §*The last round verifies* | Owns the cap, the floor, and the paragraph *unless that verifying round reopens the run* that every verifying round of the last branch used. The bound this work adds is a subsection there, beside the eight it has |
| `docs/review-handoff-protocol.md` §*round-N.md* | The normative format of the record. Nothing in it says who WRITES the cells; this work says a script does, from two agents' reports |
| `templates/sdd-round.md` | The record's shape, with 180 lines of comment explaining nine parsed fields. A generated record carries the fields and not the comments |
| `skills/code-review/SKILL.md` §*Orchestrator: the run ends with a verifying round* … §*And commit the record before commissioning the fixes* | The reach-backs (`Fixes checked by`, `Contract changes`, `New units`, `Ran by`) — five obligations the orchestrator forgot five times on the last branch. They become the generator's |
| `skills/code-review/SKILL.md` §*Findings format* | `🟡 fix or justify` with no threshold. Half of the last branch's 53 🟡 were true sentences about prose |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget — for the chain_check change |
| issue #161, body and three comments | The measurement this work is built against and the target it is measured by: **build plus two rounds inside three hours for a change under three hundred code lines**, read on 0.8.2's items |

## Scope

**In — the generator.** `skills/code-review/scripts/round_record.py`, two subcommands.

- `new` writes `rounds/round-N.md` from the warden's report and the spawn prompt's round paragraph: every field row derived (Target SHA from git, `Ran by` and `Broad gate` from flags, `PR` from `gh` or `not yet opened`, `Fixes checked by` at its landing value, both surface rows at *not yet written*, `Needs a fix` and `Loses a record or crashes` copied from the report's two lines), the verdict, probe and deferred tables copied from the report, `Inherited coordinates` derived from the earlier records' `Location` cells. It sets the previous record's `Fixes checked by` to `round-N`, ticks `Pass` when no verdict is open, and runs `chain_check --worktree` on the work item before it returns.
- `close` applies the smith's fix table to the verdict cells and derives the fix surface from the fix range: `Contract changes` from an AST comparison of top-level Python units with call sites by search, `New units` with a depth per entry. **A unit at depth 2 is refused at the keyboard** — the finding it answers sits inside a unit an earlier record's `New units` names — with the exit the rule already gives. It runs `chain_check --worktree` before it returns.
- The orchestrator writes one thing by hand: the round paragraph of the spawn prompt, which `new` copies in.

**In — the two report shapes.** The warden's report carries the verdict, probe and deferred tables in the record's own column headers, beneath its findings, and the two terminal lines it already carries. The smith's fix-pass handover carries a fix table, `| # | Verdict | Commit or grounds |`. Both are the agents' own output, so no orchestrator prose sits in a parsed cell.

**In — `chain_check.py`.**

- `--worktree`: read records from the working tree rather than `HEAD`, so a check run before the record commit sees the new cell. Three 🔴 of the last branch reached CI because the check read `HEAD`.
- `deferred <home>` joins `CLOSED_WORDS` and not `FIX_WORDS`: a finding a capped run hands to the tracker closes on the issue it went to. A bare `deferred` stays open, the direction every unreadable verdict takes.
- **The floor's reopening is one.** After a record that met the floor, at most one later record may close on a fix; the second is refused, naming the record, for work items begun on or after `REOPEN_FROM`. Earlier items print.

**In — the rules, each a few sentences in its carriers, one carrier owning each.**

1. A finding whose `Location` is a record (`seal/specs/**`, `seal/ledger/**`, `seal/ledger.md`) is a correction and not a round: what `chain_check` or `evidence_check` refuses is corrected in the closing commit; what they do not read is prose, corrected in passing or not at all. `Needs a fix` does not count it.
2. A fix pass may not add mechanism: a rule, a checker, a template section, a walk. A finding closable only by one is an issue, and the finding is `deferred #N`. The depth rule already refuses the second level; this is the first.
3. 🟡 means *a defect the release would ship* — the tool does something wrong or tells a person something wrong. ⬜ is a sentence that reads badly while the behaviour and the fact stay right, fixed in passing or not at all. `Needs a fix` counts 🔴 and 🟡 only.
4. The floor's reopening exception is bounded to one, and the run ends in `capped`: open findings become issues, verdicts read `deferred #N`, and the pull request says `chain: capped`.
5. A fix pass owes code and a test. It writes no `phase-N.md` and no `plan.md` row; the fix table in its handover is its record, and the generator writes the rest.
6. The draft pull request opens at the end of the build, before round 1, so the platform legs run beside the chain. Three Windows-only defects arrived after round 12 on the last branch.
7. A session that has compacted hands the next round to a fresh one; the generated record is the handoff.
8. **A moratorium for 0.8.x on new parsed fields in `round-N.md` and new rows the ledger must carry.** This work adds a subcommand and a verdict word, and no field.

**Out.**

- The verifying round as a probe re-execution script. It needs a probe list in a runnable shape, which is a new field, which the moratorium refuses. 0.8.2 measures whether the above reaches the target without it.
- Redesigning what a record carries. The generator writes the record as it is; the essay under the table becomes optional and short because nobody is asked to write it.
- Enforcing one round per session. A sentence, measured on 0.8.2.
- #145, #155, #156, #160, #163 — 0.8.2's, and the first readings of this work's target.

## The risk this work item carries, stated before it is discovered

This branch changes the checker, the record's writer, the warden's report, the smith's handover, and five rule carriers at once, and its own review chain runs on all of them — the shape #161 names as term 3, six rounds of fifteen. Two things are decided now rather than discovered: **this branch's records are written by the generator from round 1**, so the generator's first fixture is this branch; and **the rules bind this branch's rounds from round 1**, in the spawn prompt, as the last branch did from round 14.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A record is generated, not written | Given a warden report carrying the three tables and two lines, and the round paragraph · When `round_record.py new` runs · Then `rounds/round-N.md` exists with every field row filled from a source that is not prose, and `chain_check --worktree` accepts it | a case on a fixture repository; the record's field cells equal the derivations |
| The reach-back is the machine's | Given `round-N.md` exists · When `new` runs for round N+1 · Then N's `Fixes checked by` reads `round-N+1` | a case; the cell read back |
| The fix surface is measured | Given a fix range that changes one signature and adds two units · When `close` runs · Then `Contract changes` names the unit and its call sites and `New units` names the two at depth 1 | a case with a real diff, both cells read back |
| Depth 2 is refused at the keyboard | Given a fix that adds a unit answering a finding whose `Location` is inside a unit an earlier record's `New units` names · When `close` runs · Then it exits non-zero naming the unit and the finding, and writes no cell | a case seen red first |
| A malformed cell cannot be written | Given the generator · Then no code path writes prose into `New units`, `Contract changes` or `Fixes checked by` | the writer takes structured values only; a case feeds a comma and sees it refused |
| The working tree is read | Given a record edited on disk and not committed · When `chain_check --worktree` runs · Then it judges the edited cell; without the flag it judges HEAD | a case in both directions |
| The reopening is one | Given a floor record, a verifying record that closed on a fix, and a third record that closed on a fix · When `chain_check` runs · Then it refuses the third, naming it; a two-record run passes; an item begun before the cutoff prints | cases seen red; the well-written two-record run kept green |
| A capped run has a legal end | Given a verifying record whose verdicts read `deferred #N` and whose `Fixes checked by` is `no fixes to check` · When `chain_check` runs on a ready pull request · Then it passes | a case; `deferred` bare stays open, a case |
| The warden's report is the record's input | Given `agents/warden.md` §Report · Then it names the three tables with the record's own column headers, and the generator's parser and the warden's headers are one constant | a pin across both files |
| The smith's handover is the record's input | Given `agents/smith.md` and `implement` §5 · Then a fix pass hands over a fix table and writes no phase record | a pin on each sentence |
| The rules have one carrier each | Given the count rule's eight carriers · Then the spec states the bound and every other carrier links to it in one sentence | the existing carrier pin, re-pointed |
| 🟡 has a threshold | Given `code-review` §Findings format and `warden` §Report · Then 🟡 is defined as a defect the release would ship and ⬜ exists beside it | a pin on the sentence |
| Nobody is asked anything | Given the whole change · Then no step puts a question in front of a person after this batch | prompt budget: zero |

## Data & interfaces

- `round_record.py new --item <dir> --round N --target <sha> --report <file> --asked <file> --ran-by "<agent> on <model>" [--broad-gate "<text>"] [--pr <text>]`
- `round_record.py close --item <dir> --round N --fixes <file> --range <a>..<b> [--broad-gate "<text>"]`
- The warden report's three tables: `| # | Finding | Location | Verdict | Grounds |`, `| What was run | Result |`, `| Finding | Where it went | Who answers it |` under the headings the record uses; the two lines unchanged.
- The smith's fix table: `| # | Verdict | Commit or grounds |`, verdict one of `fixed`, `answered`, `deferred <home>`.
- `chain_check.py --worktree`; `REOPEN_FROM = 1788597030`; `deferred` in `CLOSED_WORDS`.
- The parser reuses `unverified_check.py`'s reader and `chain_check.py`'s constants; it defines none of its own for a string those already hold.

## Open questions → questions.md

Three answered before the first edit, four assumptions stated. None open.
