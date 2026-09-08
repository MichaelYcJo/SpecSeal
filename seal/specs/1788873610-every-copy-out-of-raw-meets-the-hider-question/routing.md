# 1788873610-every-copy-out-of-raw-meets-the-hider-question — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/182-every-copy-out-of-raw-meets-the-hider-question |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.3.

## Why this way

Three enumerations on one branch and the first two were each one member short, which is the method this release is named for. The completeness argument names the property — every copy taken out of `raw` — rather than the count, and the property is greppable, which is what makes the argument checkable rather than re-readable.

Straight to the PR because all three of the ticket's `Done when` lines are executable: a hidden section in an inherited row, a comment straddling a copied block, and four documents whose claim a test can read.
