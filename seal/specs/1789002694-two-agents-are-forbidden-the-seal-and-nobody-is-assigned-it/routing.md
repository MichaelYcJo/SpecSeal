# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — routing

<!-- seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/routing.md
— the answer given before the first edit, in the batch the `implement` skill
collects (§1). Committed, because the check happens at the pull request and CI
sees only what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/30-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it |

Answered 2026-09-10 by the repository owner, before the first edit, in the one
batch of three checkboxes that covered all four work items of this release.

## Why this way

Issue #30, the second work item of 0.10.0: the fourth agent, `sealer`, and
the rule that the one broad run is taken by it, once, after the rounds
settle. It adds an agent definition, changes two others and the documents
that say who runs the suite — everything a session reads and acts on — which
is what buys the chain rather than a straight pull request.

The pull request lands on `release/v0.10.0`.
