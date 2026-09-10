# the writer of the contract is not its executor — overview

<!-- Opened in phase 1 rather than at the end, on two grounds. The implement
skill §4 says the memo opens at the first divergence and phase 1 had one; and
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` went red
on this branch the moment `spec.md` and `plan.md` were committed, which the
sealer would report as `new`. Closed when the implementation ends. -->

📋 implement applied
· spec:     `seal/specs/1789081272-…/spec.md` S1–S3 · `plan.md` Phases row 1 · `questions.md` Q1–Q3 · `skills/agent-contract/SKILL.md` §2, §5, §6, §12, §15 · `skills/implement/SKILL.md` §1, §3, §4
· evidence: none yet — `seal/ledger/1789081272-….md` is phase 6's
· verified: phase 1 executed the ten-module slice below; the broad gate is unrun and labelled

## Why this work exists

When one agent writes a work item's `spec.md` and then builds against it, the
document stops being a contract and becomes an account of what got built —
which leaves `warden`'s *spec compliance first* comparing the work against
its own description of itself. The framer is the party that writes it instead.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `agents/framer.md`'s `skills:` list | spec silent; `plan.md` row 1 silent. The phase-1 spawn prompt gave five entries, `feature-planner` and `confidence-check` among them | the three `agents/smith.md` carries — `agent-contract`, `implement`, `writing-style` — with the two utility skills named as callable in prose | Measured: the five-entry list moves both utility skills into the preloaded group and turns `test_every_shipped_skill_is_named_in_both_readmes` and `test_the_readme_group_counts_are_derived_too` red. The repair is two README editions plus a `9:` entry in the second case's `spellings` table, and it appears in no phase row and in no `spec.md` scope item. S4 asks only that the two be *named as callable* in one `agents/*.md`, which is how `agents/smith.md` names them today — in prose. Phase 1's record holds the full reading |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — §2 makes the broad gate the sealer's one run, after the rounds settle |
| whether both README editions join `spec.md` §Scope item 8, which enumerates the documents describing the agent set as four and names neither | the repository owner — `questions.md` Q4 |
| `test_every_spec_directory_that_reached_the_ladder_has_an_overview`, red on this branch since `d146944` | this file — opening it is the answer, and phase 6 closes it |

## Not done

The READMEs have no `framer` row in their *What ships* table, and no phase
row asks for one. A fifth shipped agent absent from the table a reader opens
first is a gap, but nothing is red about it today: that table is not derived
from the `agents/*.md` glob, only the skills column's membership is. Left
deliberately, because the row's content depends on the frontmatter decision
`questions.md` Q4 puts to the owner — the skills column is what the derived
case reads, and writing the row before the answer means writing it twice.

`agents/smith.md` is untouched, per phase 1's bound. The two utility skills
are therefore named in two definitions until phase 2 removes the smith's
paragraph, and both skills' `smith is driving` stand-down clause still names
the smith.

## Fed back into the spec

none yet.
