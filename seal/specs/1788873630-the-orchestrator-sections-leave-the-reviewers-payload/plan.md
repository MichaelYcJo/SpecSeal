# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — plan

## The design decision the owner left open: where the five sections go

The owner settled the seam and left the destination to this document. The
constraint is stated in the task: the five sections are still the
orchestrator's procedure and must still be loadable by a session that
orchestrates a review run, **without the orchestrator having to be told a
path**.

Three shapes were considered, and the repository was read before any of them
was invented.

### What this repository already does with material that is not a preload

Measured: `find skills -type f | grep -v 'SKILL.md$'` returns seven files,
all of them under a `scripts/` directory, and **no skill carries non-preload
Markdown at all**. So the two shapes the task named are, in this tree, one
established mechanism and one precedent from a sibling skill:

- **a skill of its own** — `agent-contract` is exactly that: a `SKILL.md`
  carrying `user-invocable: false`, reached through an agent's `skills:`
  list or by being opened.
- **a file under the skill's directory that `SKILL.md` names by path** —
  `skills/code-review/scripts/round_record.py` and `chain_check.py` are
  that. The material's kind differs; the mechanism is identical, and it is
  the mechanism that decides whether an orchestrator can reach it.

### Option 1 — `skills/review-orchestration/SKILL.md`, a skill of its own

**Failure scenario, and it is not hypothetical.** A skill directory is
globbed by four cases in `tests/test_chain_hooks_hardening.py`, and two of
them read a **count**: `test_both_readmes_count_the_skills_that_are_actually_there`
derives the shipped count from `glob("skills/*/SKILL.md")` and demands that
both READMEs spell it, and `test_the_readme_group_counts_are_derived_too`
demands the same of three group counts. So this option moves four pinned
numbers in two languages and adds a spelling to `NUMBER_WORDS`, for prose
nobody is asking to change.

**The worse failure is at runtime.** A new skill is one of two things, and
neither is what this material is. Left model-invocable, it fires on its own
description whenever a session's request looks like review orchestration —
`test_auto_firing_skills_declare_when_not_to_fire` then requires a `NOT for`
boundary, and the boundary does not fix the firing, it only documents it. A
skill that loads itself mid-round is the redundant-context cost this work
item exists to reduce, arriving by a second door. Marked
`disable-model-invocation: true` instead, it becomes a slash command a
person types — and `test_a_skill_nobody_preloads_is_listed…` then requires
both READMEs to show `/specseal:review-orchestration` in the form a person
types, for a procedure no person will ever type.

### Option 2 — leave the sections and add an instruction not to read them

Rejected on the ticket's own grounds. This is #180's class: an instruction
in a check's place. The characters occupy the window whether or not the
agent is told to skip them, so the instruction does not even address the
claim.

### Option 3 — `skills/code-review/orchestration.md`, named by `SKILL.md` — **chosen**

A file beside the `scripts/` the skill already names by path.

| | |
|---|---|
| Reached by | the pointer paragraph in `SKILL.md`, which the orchestrator has loaded by definition — running a review run is what loading `code-review` is for |
| Reached by `warden` | never. It is in no `skills:` list, so nothing preloads it, and the reviewer's half of the skill never names it as something to open |
| Fires on | nothing. It has no frontmatter and no description, so no trigger exists |
| Pinned counts it moves | none. Every glob in the tree is `skills/*/SKILL.md` |

**What it gives up, stated rather than left to be found.** A skill is
guaranteed to arrive; a path has to be opened. An orchestrator that reads
the pointer and does not open the file runs a review run without the rules in
it. That is a real cost and it is the same cost `round_record.py` and
`chain_check.py` already carry — the orchestrator reaches both by a path this
same file names, and the checks those scripts run are what catch the
orchestrator who did not. The rules in the five sections have that property
too: `chain_check.py` refuses a record missing the rows §*And name the fix
surface* describes, and refuses a record committed after the fixes it
commissions. So the enforcement of the moved material does not travel by
preload today either, and moving the prose does not move a guarantee.

**One thing is not given up: the headings.** They keep the `Orchestrator:`
prefix, verbatim. Every live reference names a heading by its text, three
ledger rows anchor on that text, and `test_the_rules_have_one_owner.py`
carries two of them as string constants. Only the **file** in each reference
changes, which is the smallest edit that leaves every reference true.

### The same shape for part 2 — `skills/writing-style/outside-the-review.md`

Symmetric, and for the same reasons. `writing-style` stays in both agents'
`skills:` lists, as the owner required, so the file is what moves and not
the list. The three sections that go are the ones written to somebody outside
the code review — a pull-request reader, another team, the user at the
terminal — and 「리뷰 코멘트에만 해당하는 것」 stays where the reviewer meets
it at startup.

`smith` keeps `writing-style` and reaches the moved three by the pointer when
it writes a pull-request body. That is a downgrade from preload to pointer
for `smith`, and it is the trade the owner took: the alternative is a style
gate, and #180 says an instruction is not one.

## Phases

Each phase is a vertical slice: a move and the references that move with it,
run before the next begins.

| # | Phase | Delivers | Verified by | Status |
|---|---|---|---|---|
| 1 | The five sections move | `skills/code-review/orchestration.md` holds lines 236–653 verbatim; `SKILL.md` holds the pointer | the block is byte-identical to the cut; `git diff` shows no rewritten prose |  |
| 2 | Live references in the documents | `agents/smith.md`, `skills/implement/SKILL.md`, `docs/flow.md`, `docs/review-handoff-protocol.md` name the new file | the construction of spec.md's table re-run: no live reference names a heading in a file that does not hold it |  |
| 3 | The twelve test modules | the eleven that pin the path, plus `test_a_record_precedes_the_fixes_it_commissions.py` | `bin/test` on the twelve, and the two structural cases counted across both halves |  |
| 4 | Part 2 — the three sections move | `skills/writing-style/outside-the-review.md`, the pointer, 「리뷰 코멘트에만」 in place | grep for the four headings across the two files |  |
| 5 | The ledger, and the records | three rows removed in `seal/ledger.md`, the claims re-written in this item's fragment; `docs/flow.md`'s #265 box; `changelog.md`; `overview.md` | `evidence_check.py --strict .` clean, executed |  |

**Phase 1 leaves the suite red on purpose, and phase 3 is what closes it.**
The task asks for the move and the reference fixes in separate commits, and a
move that carries its own reference fixes is one commit nobody can read. The
phase records say so rather than leaving a reader to discover a red commit
and wonder.

## What is not a phase

The `Orchestrator:` prefix stays, `writing-style` stays in both `skills:`
lists, and no gate is built in `round_record.py`. All three are the owner's
answers, recorded in `routing.md`, and none of them is a judgment this plan
re-opens.
