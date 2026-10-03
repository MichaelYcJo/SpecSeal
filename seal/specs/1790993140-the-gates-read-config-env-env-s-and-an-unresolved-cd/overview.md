# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     pending — filled when the build closes
· evidence: pending — filled when the build closes
· verified: pending — filled when the build closes

## Why this work exists

Two commits the commit gate's reader did not find (#716) are found, and the
worktree guard's two silences (#686, #678's guard half) are each wired or
named as a limit by a count over the recorded runs.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| M1's class | Spec: "every git global option that takes its value as a separate word". Code: the three git 2.54.0 accepts spaced and the reader lacked (`--config-env`, `--attr-source`, `--shallow-file`); `--super-prefix`, which older gits took spaced, is not added | the installed git's class | `questions.md` M1 names the measurement as running each option on the installed git; 2.54.0 refuses `--super-prefix` with exit 129 (`phases/phase-1.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| Which git global options take a separate value on the gits CI's Linux and Windows legs install (M1 ran on 2.54.0 only) | CI's legs, when the pull request runs |

## Not done

Pending — filled when the build closes.

## Fed back into the spec

none
