# 1789024700-the-framer-moves-and-three-tickets-take-rows — routing

<!-- seal/specs/1789024700-the-framer-moves-and-three-tickets-take-rows/routing.md — the
answer given before the first edit, in the batch the `implement` skill collects
(§1). Committed, because the check happens at the pull request and CI sees only
what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | docs/the-framer-moves-and-three-tickets-take-rows |

Answered 2026-09-10 by the repository owner, before the first edit.

## Why this way

`docs/flow.md` reserves its own branch for housekeeping no branch earned, and
names moving items between releases as one of the two cases. This is that: #84
leaves 0.10.0 for a new 0.11.0 section, and the three tickets 0.10.0's own run
opened — #333, #334 and #335 — take rows in 0.10.1.

It goes straight to the pull request because it changes one document's rows and
no behaviour. Nothing here alters a gate, a hook, a skill or an agent.
