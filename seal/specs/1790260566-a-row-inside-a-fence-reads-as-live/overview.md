# 1790260566-a-row-inside-a-fence-reads-as-live — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`; `CONTRIBUTING.md` §*What a change to a gate must carry*; `docs/the-evidence-ledger.md`; `skills/evidence-check/SKILL.md`; `seal/follow-up.md`
· evidence: `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md` P1-1 to P4-2; re-read notes, three corrections and two removals in `seal/releases/`
· verified: executed per `phases/phase-N.md`; the full suite is the sealer's

## Why this work exists

The ledger readers disagreed about where a fenced block starts and ends, so a quoted example row could fail the ledger check or be rewritten, and a quoted `drained` or fold marker could excuse something it only quoted. After this work they share one delimiter rule and one direction rule.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Q2's revert rule | `questions.md` Q2: "A line judged wrong reverts the sub-rule that moved it". The measurement moved 10 `readable` lines in 3 files, each a fenced block indented four to six spaces inside a list item, which the format does fence | the bound kept, nothing reverted | The sub-rule that moved them is the three-space bound, which is #491 itself. Reverting it restores the silent direction, a four-space run hiding every row below it. The new error is loud, because rows are read rather than hidden. No gate that reads through `readable` reads the three files. `phases/phase-1.md` lists the lines |
| The frame's own `spec.md` | Once the ledger fragment existed, the records arm read this work item and refused two example lines of `spec.md` at exit 2: S1's quoted `nosuchfile.py` stamp and S11's `secret_name` | ` · NAME NOT IN TREE` added to those two lines, and nothing else in `spec.md` changed | `skills/evidence-check/SKILL.md`'s remedy table names that marker for a record that means a name the tree does not have. Both lines quote the shapes the cases build |
| The vendored checker | `spec.md` §*Data & interfaces*: "`evidence_check.py` loads `unverified_check.py` the way `chain_check.py` does", and `plan.md` §*Operational impact* names the installed plugin only. `skills/evidence-ci/SKILL.md` has an adopter copy the checker alone into `tools/` | the reader where it is beside the checker, and a vendored pair of the two delimiter functions where it is not, held in step by an agreement case | A hard load would stop every CI run of a vendored copy at import. `hooks/config.py#FENCE` is kept as a copy for the same reason. `questions.md` Q6 holds the choice for a person |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the finished branch | the sealer, once the review rounds settle |
| Behaviour on Linux and Windows. The phases are pure text processing and were run on macOS only | CI's test matrix, whose Linux and Windows legs run at the pull request |

## Not done

The readers `spec.md` leaves out are filed as #584 and are not touched here.

No case pins #220's fence half, a name after a closing run on its own line.
Under the shared delimiter rule that line is fence content rather than a
closer, which `phases/phase-4.md` records. S12 exercises the same closer
rule, and the spec asked for no case of its own.

`questions.md` Q1 and Q6 are open for a person, each with its default built.

## Fed back into the spec

none
