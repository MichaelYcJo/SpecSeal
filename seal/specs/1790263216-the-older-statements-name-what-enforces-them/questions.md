# 1790263216-the-older-statements-name-what-enforces-them — questions for the planner

<!-- seal/specs/1790263216-the-older-statements-name-what-enforces-them/questions.md
     The residue: what reading the tree could not settle. -->

## Answered from the tree, and not to be reopened

The ticket and the spawn left these open. Each was settled by reading or by
one measurement, and `spec.md` carries the grounds.

| Judgment | Answer | Grounds |
|---|---|---|
| How many statements | 115 (106 English decisions, 9 Korean repeats), 26 of them also without a bold opening | executed 2026-09-25: `bin/fold-check --shape-from 0` reads 136, the cutoff binds 21. The ticket's 101 counts a narrower set (`spec.md` §*The measured worklist*) |
| Is the cutoff lowered to `0` | yes, in the last phase | an absent row turns the check off; a kept cutoff leaves the retrofit unheld and makes the prose false (`plan.md` §*Alternatives*) |
| Does the row accept `0` | yes | read: `fold_check.py#declared` takes any whole number, and every test of the cutoff there is `is None`, never a falsy test |
| Are the 26 bold openings in scope | yes | at cutoff `0` they are bound; `fold_check.py#shape_problems` names them |
| Split a long statement | no | `settle` §2 lets a statement run to the next marker or heading; markers are the fold's record |
| Write a case for a rule nothing reads | no; `nothing — no case reads it yet; <what would>` | #565 asks for a decision; the line is the durable record, found by `grep -rn 'Enforced by: nothing' docs/` |
| File an issue for those | no | the line in the document is the record, the way a `# RIDER:` is (`seal/follow-up.md`'s preamble) |
| The Korean edition's line | `Enforced by:` and `nothing` English, targets byte-identical, a `nothing` reason in Korean | `settle` §2's last bullet; `fold_check.py#names_targets` reads `nothing` literally |
| Pair the editions' lines by a check | yes, in phase 6 | `tests/test_both_editions_carry_the_same_folds.py` compares what is language-neutral, and targets are |
| The count's moment in the new prose | a date, not a SHA | the branch squashes (`CLAUDE.md`, the merge table) |
| `templates/config.md`'s example value | stays | an example of the row's shape, pinned to nothing here |

## Open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | When the retrofit reads a statement as **false against the code**, which side moves? The evidence ledger's own prose says review has already found one of these statements false, so the build should expect to meet some. The tree answers one case of this: where a later work item decided the change and the document lagged it, `settle` §2's *the newest work item wins* corrects the document. It does not answer the other case, where the document states a norm and the code breaks it. `implement` §1 ranks policy above code, so the code is wrong — but this is a documents work item and fixing code is outside it, and rewriting the norm to match the code would change a ratified rule without anyone deciding to | a person | (a) **Correct the document to the code**: the ledger stays quiet, but a ratified rule changes and nobody decided that it should. (b) **Keep the document and record the defect**: the line reads `Enforced by: nothing — the code does not hold this as written; <home>`, and the finding is written up for someone who owns code. (c) **Fix the code here**: widens a documents item into gate changes and review rounds it was not framed for | Where the document **lagged** a later work item's decision, apply (a), citing that work item in the phase record with a `Corrected` note. In every other case apply (b): the finding goes into the overview's *Not done*, and one new row is added here for each instance, with the statement and the code coordinate quoted side by side. The build does not stop on this | ⬜ |
| Q2 | How many `nothing` lines, split across the four cases, and which of them are case 4 (*no case reads it yet*)? | the work | Nothing to choose. The count is only known once every statement has been read | Each phase record counts its own. The overview's *Not done* lists the case-4 lines and gives the `grep` that finds them | ✅ answered by the build and round 1's fix pass: 9 lines, 4 of case 1, none of case 2, 2 of case 3 and 3 of case 4; the overview's *Not done* names the three of case 4 |
| Q3 | Which ledger rows do the edits drift, and does any claim become false? | the work | Nothing to choose. `bin/evidence-check .` names them after each phase | Re-read, and re-stamp in the file the row is in with a dated note. Where the edit made the claim false, correct it first with a `Corrected` note (`CLAUDE.md` §*fragments*) | ✅ answered by the build: 29 rows re-read and re-stamped with a dated note (each phase record names them), and one claim made false, the stacked fragment's F6, corrected in place with a `Corrected 2026-09-25` note |
| Q4 | Has a sibling chain (C, D, E or F in `release: 0.15.3`) renamed or removed a function or case that this branch names as a target? | a measurement | Nothing to choose. `bin/fold-check --shape-from 0` over the merged tree answers it | Re-run it after every merge of the release branch. If a target was renamed, read the new unit and repoint the line to it. Never write `nothing` in its place | ⬜ |

**`Who can answer` takes one of three values and nothing else** —
`a person`, `a measurement`, `the work` — as `templates/sdd-questions.md`
defines them. Only Q1 is a person's, and its default lets the build run to
the pull request without asking.
