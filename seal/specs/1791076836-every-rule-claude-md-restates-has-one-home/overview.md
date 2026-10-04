# 1791076836-every-rule-claude-md-restates-has-one-home — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

## Why this work exists

Four rows of `CLAUDE.md` restated rules other files hold, and one copy had
already gone false; each now links its home, and a ratchet stops the next
paste anywhere in the rule documents.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S5's grep | Spec S5: "`git grep -n 'CLAUDE.md. §\*no real identifiers'` returns nothing". Tree: it returns one line, in work item `1790993139`'s `spec.md` Grounding table | the grep outside `seal/`, which is empty, and the module's `LINKED` rows for the four comments | Scope 2 took its four comments from a grep "outside the records". A record cites what was read at its time and is not rewritten (`phases/phase-1.md`) |

## Not verified

none — every scenario this phase reached was executed; phase 2 adds its own rows here if it leaves any.

## Not done

nothing

## Fed back into the spec

none
