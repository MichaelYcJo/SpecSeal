# 1788993115-a-payload-is-written-again-on-every-spawn — routing

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/routing.md
— the answer given before the first edit, in the batch the `implement` skill
collects (§1). Committed, because the check happens at the pull request and CI
sees only what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | perf/292-a-payload-is-written-again-on-every-spawn |

Answered 2026-09-10 by the repository owner, before the first edit, as one
batch of three checkboxes for all four work items of this release rather than
four batches.

## Why this way

Issue #292, the first work item of 0.10.0. It builds the meter that every
later item of this release is measured with — #120 removes sections from a
payload and this is what says whether that worked — and it moves the
orchestrator's half of `implement` out of the largest payload the plugin
injects. Both change what a session reads and acts on, which is what buys the
chain rather than a straight pull request.

The pull request lands on `release/v0.10.0`.
