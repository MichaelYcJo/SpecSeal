# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     in progress
· evidence: in progress
· verified: in progress

## Why this work exists

The commit gate's policy was one 1,047-line document frozen over the ceiling;
cut along its headings into three, each answers one question and each takes
the next fold again.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The parent's base line count | Spec §*Data & interfaces*: "parent (1–40, 278–759, 995–1047) \| 576". The move script counted 575 base lines (40 + 482 + 53); with the rewritten preamble the parent is 586 | the measured count | the script's own `len()` over the three ranges, which asserts each boundary heading before it copies (`phases/phase-1.md`) |
| K6's crossing lines | Spec K6: "Line 91 …, 199 and 273–274 …, and 283–284" cross the cut. Line 152, *the PreToolUse reading in the next section stands aside*, crosses too: in its new file there is no next section | line 152 cited by file and section as well | K6's command was `awk` for `above`/`below`, which `next section` does not match. W1 is the row that asks for exactly this re-read (`phases/phase-1.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

nothing

## Fed back into the spec

none
