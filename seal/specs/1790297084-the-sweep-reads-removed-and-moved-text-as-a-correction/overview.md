# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's spec.md, plan.md and questions.md
· evidence: seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md
· verified: each phase's record under phases/ says what was executed

## Why this work exists

The survivor sweep named the wrong file as a correction, hid a correction
behind text a fold carried verbatim, and reported a removed ledger row's
claim as a correction. After this work it names the correction, holds the
fold's text, and leaves the removed row out.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A fourth #592 case | `spec.md` names S1–S3 for #592. S1's moved file is gone at the tip, so a gone-at-`b`-only rule passes it | A split case where both files remain, added beside S1 | `plan.md` §*Alternatives considered*: gone-at-`b` as the primary rule "falls back to path order: #592 again" on a split. Only a split case can go red for it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |
| Windows and Linux: only macOS was run | the three-OS matrix in `test.yml` at the pull request |

## Not done

nothing

## Fed back into the spec

none
