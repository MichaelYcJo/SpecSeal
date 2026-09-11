# the writer of the contract is not its executor — overview

<!-- Opened in phase 1 rather than at the end, on two grounds. The implement
skill §4 says the memo opens at the first divergence and phase 1 had one; and
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` went red
on this branch the moment `spec.md` and `plan.md` were committed, which the
sealer would report as `new`. Closed when the implementation ends. -->

📋 implement applied
· spec:     `seal/specs/1789081272-…/spec.md` S1–S14 · `plan.md` Phases rows 1–6 · `questions.md` Q1–Q4 · `skills/agent-contract/SKILL.md` §2, §5, §6, §12, §15 · `skills/implement/SKILL.md` §1, §3, §4 · `CLAUDE.md` *a change writes fragments* · `CONTRIBUTING.md` *House rules*
· evidence: three rows in `seal/ledger/1789081272-the-writer-of-the-contract-is-not-its-executor.md` — the `Planning` mark, its notice, and how the fourth axis is parsed. 21 coordinates, all resolving
· verified: each phase executed its own narrow slice; phase 6 re-ran the modules that read `docs/flow.md`, the two READMEs and the fourth axis. The broad gate is unrun and labelled below

## Why this work exists

When one agent writes a work item's `spec.md` and then builds against it, the
document stops being a contract and becomes an account of what got built —
which leaves `warden`'s *spec compliance first* comparing the work against
its own description of itself. The framer is the party that writes it instead.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `agents/framer.md`'s `skills:` list | spec silent; `plan.md` row 1 silent. The phase-1 spawn prompt gave five entries, `feature-planner` and `confidence-check` among them | the three `agents/smith.md` carries — `agent-contract`, `implement`, `writing-style` — with the two utility skills named as callable in prose | Measured: the five-entry list moves both utility skills into the preloaded group and turns `test_every_shipped_skill_is_named_in_both_readmes` and `test_the_readme_group_counts_are_derived_too` red. The repair is two README editions plus a `9:` entry in the second case's `spellings` table, and it appears in no phase row and in no `spec.md` scope item. S4 asks only that the two be *named as callable* in one `agents/*.md`, which is how `agents/smith.md` names them today — in prose. Phase 1's record holds the full reading |
| where the `docs/flow.md` step 2 edit belongs | `plan.md` row 6 lists *step 2 loses `once #84 exists`* beside 0.11.0's checkbox; phase 2's prompt assigns the clause to phase 2 | phase 2 edits step 2; phase 6 keeps the checkbox and the section | S11's scenario names the flow sentence and the sealer's count together, and row 2's Verified-by cell makes the S11 case phase 2's. The case is red until step 2 is edited, so the plan as written cannot be followed. `plan.md` row 6's Delivers text is left alone — that column is the framer's writing and only Status is the builder's |
| where *say whether the frame holds* lands in `agents/smith.md` | `plan.md` §Technical context says phase 3, **Implement**; the phase-2 prompt hands the judgment to the phase | the head of phase 1, **Requirements** | The check runs on the chain that was just read, and below it sits the design gate — the one interruption of the run. A frame judged after that gate is judged after its questions have already been put to a person. It is also the same act §5 asks for one level down, *open the coordinates before you build on them*, so the case pins the home as well as the sentence |
| what `plan.md` row 6's Verified-by can actually verify | row 6 names `fold_ledger.py --check` as one of three checks this phase passes | it is run, and its exit 1 is read as the correct answer rather than as a failure | Measured in phase 6: both gatherers read exit 0 before the fragments existed and exit 1 after, each naming exactly this work item's file. That is what they are for — `--check` asks *has every fragment reached the shared file*, and a feature branch is supposed to leave one that has not. The hygiene workflow runs it only on a pull request into `main`, where the answer has to be yes. What proves a fragment instead is `--version 0.11.0 --dry-run`, which built the released section and the folded ledger section from both fragments and wrote nothing, exit 0 each. The row is not wrong about the command, it is wrong about the direction of a pass |
| what phase 6 does, against what row 6 says it does | row 6 delivers `docs/flow.md`, the two fragments and the closing memo | four more acts, none of them in the row | Every one of them postdates the drawing. Row 5 was deferred to #350 by the repository owner on 2026-09-11, so row 5's Status and `spec.md` §Scope item 7 both have to say so, and `docs/flow.md`'s own rule — *a row for any ticket that work opened* — earns #350 a row under 0.11.1. The fourth is the README row phase 1 left in `## Not done`, which this phase settles below. A frame written before a deferral cannot name the deferral's consequences, and the plan's Delivers column is the framer's writing, so the row is left as it stands |
| how many constants `hooks/routing.py` gains for the fourth axis | `spec.md` §Data & interfaces names four and lists `BY_SESSION_PLANNING = BY_SESSION  # the same string, one vocabulary`; `plan.md` row 4 names three — `PLANNING`, `BY_FRAMER`, `PLANNING_ANSWERS` | three, and `plan.md` wins | The fourth constant exists to say that the planning axis's session answer is not a different string, and `PLANNING_ANSWERS = (BY_FRAMER, BY_SESSION)` says it by USING that string rather than by naming it a second time. An alias is the shape `hooks/implementer.py`'s docstring refuses one storey down — two spellings of one thing — and it is what a later edit turns into `BY_SESSION_PLANNING = "the session"` with nothing going red. The sentence the constant carried is a comment beside `BY_FRAMER` |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — §2 makes the broad gate the sealer's one run, after the rounds settle |
| whether the third axis's own template pin should be widened the way phase 4 widened the fourth's — `test_the_template_PARSES_into_the_three_answers_it_ships` substitutes its own constants into the template's row, which is self-consistent by construction and cannot see the two files drift | the repository owner, through the row phase 4 opened in `seal/follow-up.md`. The answerer used to read *a later work item*, which is a condition wearing a person's clothes and is what that file's own opening refuses |
| whether both README editions join `spec.md` §Scope item 8, which enumerates the documents describing the agent set as four and names neither | the repository owner — `questions.md` Q4 |
| ✅ `test_every_spec_directory_that_reached_the_ladder_has_an_overview`, red on this branch since `d146944` | **Executed** 2026-09-11 in phase 6, green — opening this file was the answer and phase 6 closed it |
| `bin/evidence-check .`'s records arm reports `phases/phase-1.md:131` DRIFTED, and there is no correct edit. That line quotes the coordinate `COVERED` held BEFORE phase 1 changed it and names the new hash in the next sentence, which is the record doing its job; the arm reads any `path#anchor@hash` in a record as a live citation. Re-stamping it would make the sentence say the old and new hashes are the same, and breaking the form would make the coordinate unopenable. Advisory only — CI runs the checker without `--strict`, so drift is a warning and the ledger itself reads 1121 ok · 0 drifted · 0 broken | the repository owner — whether the records arm should tolerate a superseded coordinate quoted beside its successor is a decision about the checker, not about this record |

## Not done

~~The READMEs have no `framer` row in their *What ships* table.~~ **Written in
phase 6, in both editions.** Phase 1's grounds for leaving it conflated two
things that come apart: whether the table gains a `framer` row at all, and
what its middle cell says. Only the second depends on `questions.md` Q4. The
row is owed either way, because a release whose headline is a fifth agent
cannot ship a *What ships* table naming four — which is `spec.md` §Scope item
8's own class, one file further out than the four documents it enumerates. The
cell says what ships today, `agent-contract · implement · writing-style`, and
a Q4 answered *preload* edits that one cell alongside the two skills rows and
the test constant Q4 already prices. Nothing went red: the derived cases read
the agents table for which definition preloads a skill, and the fifth row
preloads nothing the first four did not.

**#350 — the per-agent wall clock.** `spec.md` §Scope item 7 and `plan.md`
row 5, deferred by the repository owner on 2026-09-11 to milestone 0.11.1. It
is the one clause of #84's reasoning that was measurable, and without it the
release ships the separation argument with no number behind the cost
argument. S10 is the scenario nothing in this work item now answers.

**`questions.md` Q3 and Q4 are both still open.** Q3 — where a *no* goes when
the smith reads the frame and it does not hold — is answered by **the work**,
and phase 2 built its default: the phase record's `## What this phase found`,
plus the hand-back. It stays open because the row's own answerer column says
the work answers it and the work is not finished being done. Q4 —
whether `agents/framer.md` preloads the two utility skills or names them
callable in prose — is **the repository owner's**, and prose is what shipped.

**The `seal/follow-up.md` row phase 4 opened.** The THIRD routing axis's
template pin substitutes its own constants into the template's row, so it is
self-consistent by construction and cannot see the two files drift. The
fourth axis's was built differently and the same four lines carry over; the
third was left, because phase 4 has no row for it and widening it is a sweep.
Answerer: the repository owner.

**A ledger anchor was re-pointed where `CLAUDE.md` says a row is REMOVED, and
it was deliberate.** Phase 4b moved `seal/ledger.md`'s row from
`hooks/implementer.py#is_smith` to `#mark_for` rather than marking it REMOVED
and rewriting the claim in this work item's fragment. Its grounds are in the
row itself and in `phases/phase-4.md`: the rule's stated rationale is *its
claim went with the code*, and this claim did not — the qualifier is still
dropped with `rsplit(":", 1)` and never a substring test, in the same module,
with four of the row's five anchors never moving. **This is a deviation from a
stated rule and the orchestrator hands it to round 1 as a named item.** It is
recorded here rather than re-argued, and the row is left as phase 4b wrote it.

~~`agents/smith.md` is untouched, per phase 1's bound.~~ Closed in phase 2:
the paragraph is out of the design gate, each skill is named in one
definition, and both stand-down clauses name the framer. The clauses are read
out of the glob now rather than typed, so the next move takes them with it.

## Fed back into the spec

`spec.md` §Scope item 7 is struck through with the deferral to #350 beside it,
in the shape §Scope/Out already uses for Q1's reversal — the sentence is kept
so a reader meets the promise and its answer in one place, rather than finding
a scope item that silently stopped existing. Nothing was inferred during
implementation that the frame did not already carry, so no clause is added for
a planner to overturn.
