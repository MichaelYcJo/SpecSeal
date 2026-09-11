# Feature Specification: the writer of the contract is not its executor

Closes #84. The fifth agent, `framer`, and the four things that have to move
with it so it arrives against documents that permit what it does.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §6 — *what you write is named in your own definition* | The framer writes three durable records. Under the §6 this repository shipped in 0.10.0 that needs no exception: naming them in `agents/framer.md` is the whole grant. This is the sentence #120 was ordered before this ticket to obtain |
| `skills/agent-contract/SKILL.md` §2 — *One definition in this plugin does hand them over* | `agents/framer.md` must not assign the broad gate. §2's count stays `One`, and `tests/test_broad_gate_rule.py#test_only_one_definition_assigns_the_broad_gate` is the case that reads it — its own docstring names this release's arrival as the thing it was written for |
| `skills/implement/SKILL.md` §3 — the SDD ladder | The ladder already decides when a `spec.md` is written, so it decides when the framer runs. Nothing new has to choose, and no box has to be added to the routing question (#88) |
| `skills/implement/SKILL.md` §1 — one batch before the first edit | The framer phase is the interactive one and the batch is its output. Spawning `smith` is the approval, so the approval is not a second interruption |
| `docs/flow.md` *Order inside a ticket* step 2 | Reads `spec · plan (framer, once #84 exists; the session until then)`. This work item is what removes the second clause |
| `CLAUDE.md` *a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, never `CHANGELOG.md`'s `## Unreleased` or `seal/ledger.md` |

## Scope

**In.**

1. `agents/framer.md` — a new definition: the contract opening verbatim, the
   three writes named under §6, what it reads, and what it is not.
2. The two utility skills move out of `smith`'s design gate onto the framer —
   `feature-planner` and `confidence-check`.
3. `smith`'s first act on a drawing becomes *say whether it holds*. Written
   down for the first time: it happened twice unprompted in #107's run and
   lives in no document.
4. `templates/sdd-plan.md` gains `Approved <date> by <who>`, written when
   `smith` is spawned.
5. `templates/sdd-questions.md` gains a column for **who can answer this row**
   — a person · a measurement · the work — and the framer opens rows without
   owning their answers.
6. `templates/sdd-routing.md` gains a `Planning` row, `framer` · `the session`,
   on the terms the `Implementation` row already has, and `hooks/routing.py`
   reads it on those terms.
7. ~~`skills/verify/scripts/session_cost.py` reports **time per agent from the
   subagent transcripts**, so the framer's cost is a number rather than the
   34-second orchestrator turns nobody can see.~~ — **deferred to #350**,
   milestone 0.11.1, by the repository owner on 2026-09-11. It is the one
   scope item that is not the framer itself, and the framer ships without it.
   What the deferral costs is written down rather than left to be found: S10
   is the scenario nothing in this work item now answers, and the falsifiable
   test #84's own last comment states — *if the frame is complete, `smith`
   reads it instead of the repository and its token count drops* — has no
   command behind it for another release. 0.11.0's own four segments were
   measured by opening each transcript by hand, one `session-cost` call per
   file, and #350 carries those readings. `plan.md` row 5's Status is
   `deferred #350`.
8. The documents that describe the agent set as four: `agents/sealer.md`'s
   *the three definitions that stay silent*, `skills/implement/SKILL.md` §3's
   file table, `skills/implement/orchestration.md`, `docs/flow.md`.

**Out, and each with its reason.**

- **A fourth checkbox in the routing question.** #88 settles it: the framer
  runs where the ladder calls for a `spec.md`, so the ladder decides and not a
  person. The `Planning` row is a record. #88 stays unscheduled and this work
  item does not answer its *all three* half.
- ~~**A `framer` mark under the git dir**~~ — **in scope after all.**
  `questions.md` Q1 was put to the owner as this file's *out*, with *no mark*
  as the default, and was answered **a mark** on 2026-09-11 against that
  default: a session can declare `framer` and frame the work itself exactly
  as it can declare `smith` and build it, so the gap is the same gap and it
  closes the same way. The mark is a **second constant inside
  `hooks/implementer.py`**, not a second module — that file is named for the
  axis rather than for the agent, and its docstring's own reason for being a
  module is that two spellings of one path is a mark written and never found.
  `plan.md` phase 4b carries it.
- **Retiring `feature-planner`'s task decomposition into `plan.md`'s Phases
  table.** §3 already states what that gives up and why; moving the skill is
  not re-opening it.
- **`CHANGELOG.md` and `seal/ledger.md`.** Fragments only.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the fifth definition inherits the contract without anyone deciding to give it one | Given `agents/framer.md` lands · When the suite runs · Then every case parametrised on `agents/*.md` covers it, and the opening paragraph's four pins are present verbatim | `tests/test_every_agent_reads_the_contract.py` over the glob, at five files |
| S2 §2's count stays true | Given five definitions · When `test_only_one_definition_assigns_the_broad_gate` runs · Then `assigning == ["sealer.md"]` still, and §2 still carries `One definition in this plugin does hand them over` | `tests/test_broad_gate_rule.py`, executed |
| S3 the framer carries no universal rule | Given `agents/framer.md` · When the moved-rule check runs · Then no 15-word run of any contract section body appears in it | `tests/test_a_moved_rule_leaves_its_definition.py` over the glob |
| S4 the two skills have one home and it is the framer | Given the design gate paragraph moves · When the tree is swept · Then `feature-planner` and `confidence-check` are named as callable in `agents/framer.md` and in no other `agents/*.md` | a new case, red against `agents/smith.md` as it stands today |
| S5 the smith checks the drawing before building to it | Given a phase begins · When `agents/smith.md` is read · Then its first act on a frame is to say whether the frame holds, and the sentence names where a *no* goes | a new case pinning the sentence, and its home |
| S6 `plan.md` records who approved it and when | Given the template · When a work item copies it · Then an `Approved <date> by <who>` line is there to fill, in the shape `routing.md`'s `Answered` line has | a new case comparing the two spellings |
| S7 a question's row says who can answer it | Given `templates/sdd-questions.md` · When a framer opens a row · Then the row carries one of *a person* · *a measurement* · *the work*, and the file says the framer opens rows rather than answering them | a new case pinning the three values and the sentence |
| S8 the fourth axis reads as unanswered when absent | Given every declaration already committed in this repository, none of which has a `Planning` row · When `hooks/routing.py` parses them · Then each is still a declaration and `planning` is `None` | `tests/test_routing_is_recorded.py#test_every_declaration_in_this_repository_still_parses`, plus a new case per answer |
| S9 a wrong answer in the fourth axis decides no commit | Given a declaration whose `Planning` cell is backticked, capitalised or absent · When the commit gate runs · Then it decides exactly what it decides without the row | a new case in the shape `test_the_commit_gate_decides_the_same_with_the_row_and_without_it` already has |
| ~~S10 an agent's own wall clock is a number~~ — **deferred to #350**, milestone 0.11.1, on 2026-09-11 | ~~Given a transcript with subagent transcripts beside it · When `session-cost` runs in the new mode · Then one row per segment, named by the spawn's `subagent_type`, with its own span, calls and tokens — and the count of segments it could not name is printed rather than hidden~~ | ~~a new case over a built transcript tree, executed~~ — nothing in this work item answers it |
| S11 the documents stop saying four | Given the agent set is five · When the tree is swept for the count | `agents/sealer.md`'s *three definitions that stay silent* reads four, and `docs/flow.md` step 2 no longer says *once #84 exists* | a case counting from the glob, never from a list |
| S13 a declared framer that never ran earns one line | Given a declaration answering `Planning` with `framer` · When a commit lands on that branch and no framer mark stands for it · Then one line says so, once per repository per session, and nothing is blocked. Given the mark stands · Then nothing is said at all | new cases beside the `Implementation` ones, plus a case that a mark for one axis does not answer for the other |
| S14 one notice, not two | Given a declaration whose `Planning` and `Implementation` are both unfulfilled · When a commit lands · Then the session is told once, naming both axes, not once per axis | a new case; the once-per-session grain is `hooks/implementer-notice.py`'s existing marker and does not change |
| S12 the flow's order survives the edit | Given `docs/flow.md` step 2 is rewritten · When the rules-have-one-owner case runs · Then `) → warden rounds → sealer → the pull request is marked ready.` is still in it and the draft PR still precedes the rounds | `tests/test_the_rules_have_one_owner.py#test_the_flow_opens_the_draft_between_the_build_and_the_rounds`, executed |

## Data & interfaces

**`hooks/routing.py`** gains four module constants and one dict key, on the
terms the third axis already has:

```
PLANNING = "Planning"
BY_FRAMER = "framer"
BY_SESSION_PLANNING = BY_SESSION      # the same string, one vocabulary
PLANNING_ANSWERS = (BY_FRAMER, BY_SESSION)
```

`parse()` returns `"planning"` beside `"implementation"` — optional, and an
answer outside the vocabulary reads as unanswered rather than as *this file is
not a declaration*. The reason is the one that module's own docstring gives
for the third axis: nothing decides a commit on it, so taking the whole
declaration down for a typo there would ask the review question again on
branches whose answer is committed.

`table_rows()` needs no change. Its docstring already says unknown labels are
left in rather than filtered, *so a reader that does not recognise a label
cannot gain a third axis later* — and this is the fourth arriving on that
promise.

**`session_cost.py`** gains one report mode. It joins each subagent transcript
to a spawn by the stamp the block comment above `DELEGATING` already measured:
a segment's transcript opens at its spawn's result, 61 of 67 within one
second. The six misses are subagents of subagents, which have no call in the
main transcript at all — they are reported as named-by-nobody rather than
dropped, the direction `tool_name` and `count` already take.

No schema, no endpoint, no migration.

## Open questions → questions.md

Three, and only one of them is a person's. `questions.md` carries which is
which, in the column this work item adds.
