# 1790260566-a-row-inside-a-fence-reads-as-live — overview

📋 implement applied
· spec:     see the proof block of the hand-back for each phase
· evidence: `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md`
· verified: see each `phases/phase-N.md`

## Why this work exists

The ledger readers disagreed about where a fenced block starts and ends, so a quoted example row could fail the ledger check or be rewritten, and a quoted `drained` or fold marker could excuse something it only quoted. After this work they share one delimiter rule and one direction rule.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Q2's revert rule | `questions.md` Q2: "A line judged wrong reverts the sub-rule that moved it". The measurement moved 10 `readable` lines in 3 files, each a fenced block indented four to six spaces inside a list item, which the format does fence | the bound kept, nothing reverted | The sub-rule that moved them is the three-space bound, which is #491 itself. Reverting it restores the silent direction, a four-space run hiding every row below it. The new error is loud, because rows are read rather than hidden. No gate that reads through `readable` reads the three files. `phases/phase-1.md` lists the lines |
| The frame's own `spec.md` | Once the ledger fragment existed, the records arm read this work item and refused two example lines of `spec.md` at exit 2: S1's quoted `nosuchfile.py` stamp and S11's `secret_name` | ` · NAME NOT IN TREE` added to those two lines, and nothing else in `spec.md` changed | `skills/evidence-check/SKILL.md`'s remedy table names that marker for a record that means a name the tree does not have. Both lines quote the shapes the cases build |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the finished branch | the sealer, once the review rounds settle |
| Behaviour on Linux and Windows. The phases are pure text processing and were run on macOS only | CI's Linux leg; nobody for Windows |

## Not done

The readers `spec.md` leaves out are filed as #584 and are not touched here.

## Fed back into the spec

none
