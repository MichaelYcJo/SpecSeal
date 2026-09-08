# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | smith |
| Branch | perf/265-the-orchestrator-sections-leave-the-reviewers-payload |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.3.

## Why this way

The seam is the one the author already drew in the headings: the five sections the file prefixes `Orchestrator:` are 24,553 characters a reviewer never acts on, and no reference crosses it. The owner also took the narrower half of part 2 — the per-document sections of `writing-style` that are not a reviewer's leave the reviewer's payload — because that half needs no mechanical style check and gives up no guarantee.

Straight to the PR because the eleven modules that pin the path are the test that a split kept its claims, and two of them say what a path swap alone would break.

`writing-style` stays in the preload. Moving it out is the half whose open question is whether a style rule can be checked mechanically, and #180's conclusion is that an instruction in its place is the next instance.
