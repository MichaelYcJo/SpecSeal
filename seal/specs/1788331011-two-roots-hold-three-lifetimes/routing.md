# 1788331011-two-roots-hold-three-lifetimes — routing

<!-- specs/1788331011-two-roots-hold-three-lifetimes/routing.md — the answer
given before the first edit, in the batch the `implement` skill collects
(§1). Committed, because the check happens at the pull request and CI sees
only what is in the tree.

The rows are read by machines and their vocabulary is fixed. Anything else in
this file is for people. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/two-roots-hold-three-lifetimes |

Answered 2026-09-02 by the repository owner, before the first edit.

## Why this way

Ticket #79, the body of 0.4.0 in `docs/flow.md`: `specs/` and `.specseal/`
become one plugin-owned root laid out by lifetime, opt-in becomes the root's
presence, and the session-start hook moves an existing tree once. It changes
what every gate reads, so it goes through the chain; the pull request lands
on `release/v0.4.0`. The smith is spawned once per phase of `plan.md` rather
than once for the whole item, and the first spawn writes the spec and plan
alone and stops, so the owner reads the frame before anything is built.
