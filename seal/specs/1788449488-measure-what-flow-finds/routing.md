# 1788449488-measure-what-flow-finds — routing

<!-- seal/specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). Committed,
because the check happens at the pull request and CI sees only what is in the
tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/measure-what-flow-finds |

Answered 2026-09-04 by the repository owner, before the first edit.

## Why this way

Issue #109: the segment-measurement instruction moves out of a person's
message and into `skills/verify/SKILL.md`; the destination becomes a
`flow-measurement`-labelled issue instead of a hardcoded number; the release
workflow closes the current one and opens the next. Owner pre-approved
smith · review chain · open the pull request into `release/v0.7.0`, and
squash-merge automatically once CI is green, as part of the same unattended
overnight run that shipped #121+#119.
