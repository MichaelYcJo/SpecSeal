# 1790263216-the-older-statements-name-what-enforces-them — overview

📋 implement applied
· spec:     this work item's spec.md (Grounding, Scope, What a decision is, S1–S11, Data & interfaces), plan.md (phases 1–7, Technical context, Alternatives), questions.md Q1–Q4; skills/settle/scripts/fold_check.py; docs/the-evidence-ledger.md; CLAUDE.md §fragments, §commit early
· evidence: filled in when the work item closes
· verified: filled in when the work item closes

## Why this work exists

115 folded statements were written before the fold's shape existed and named
nothing that reads them; each now carries one `Enforced by:` line, and the
shape check binds every statement from then on.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| none yet | | | |

## Not verified

none — every decision is labelled `mutated` or `read` in the phase record that makes it, and the full suite, lint and format are the sealer's broad gate, recorded in the last round record's `Broad gate` cell.

## Not done

Filled in as the phases close. The `nothing` lines of case 4 (*no case reads
it yet*) are listed here, and `grep -rn 'Enforced by: nothing' docs/` finds
every `nothing` line in the document a reader already has open.

## Fed back into the spec

none
