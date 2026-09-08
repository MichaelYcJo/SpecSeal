# 1788873600-the-baseline-is-the-moving-pull-request-base — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/272-the-baseline-is-the-moving-pull-request-base |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.3.

## Why this way

The baseline arm is right about what it measured and wrong about what happened, and the cost is roughly quadratic in the number of work items a release carries. This release carries five, so the item is built first and squashed first: every sibling then merges a release branch that already holds the repair.

Straight to the PR because the arm's own case is executable — a squashed sibling's overview.md present at the base and absent on the branch — so what a round would judge, a case pins.
