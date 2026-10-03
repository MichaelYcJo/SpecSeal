# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     written at the close of the build
· evidence: written at the close of the build
· verified: written at the close of the build

## Why this work exists

A work item that commits in several repositories gets one routing answer in
each, a signatory names the pact it signs, and `pact-check` at the pact's
repository says where the signatories disagree with it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where `normalise_remote` lives | `plan.md` §*Technical context*: "Their parsing and vocabulary live in `hooks/config.py`" and "`skills/implement/scripts/seal.py#normalise_remote` … Import it. Do not copy it." The code moved the function into `hooks/config.py` and left `seal.py` an alias | moved, with the alias | `seal.py` imports `hooks/config.py` by plain name, so the reader importing `seal.py` is a cycle, and `hooks/config.py`'s docstring: "`skills/implement/scripts/seal.py` … is a two-thousand-line command that a `PreToolUse` hook must not import -- so the READER moved here and the writer stayed there, and `seal.py` re-exports these names rather than keeping a second copy." One normaliser stays, which is what the plan's sentence protects |
| How many rows `/specseal:config` shows | `plan.md` phase 1: "`skills/config/SKILL.md`'s row table gains both rows, and every count of that table's rows is corrected (it says *all seven*)". The code added a third row, `Reference specs`, and says ten | ten | `templates/config.md` has shipped `Reference specs` since #688 and the skill's procedure is "Show every row, present or not". Nine would have been a second false count |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at this branch's tip | the sealer, once the review rounds settle |

## Not done

Written at the close of the build.

## Fed back into the spec

Written at the close of the build.
