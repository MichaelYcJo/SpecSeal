# 1788425222-release-0-5-0 — routing

<!-- seal/specs/1788425222-release-0-5-0/routing.md — the answer given
before the first edit, in the batch the `implement` skill collects (§1).
Committed, because the check happens at the pull request and CI sees only what
is in the tree. -->

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | release/prepare-v0.5.0 |

Answered 2026-09-03 by the repository owner, before the first edit.

## Why this way

0.5.0's release preparation: gather the changelog fragments, fold the ledger
fragments, move `plugin.json`. Three scripts this repository already owns run
it, and each has a `--check` the hygiene workflow runs on the pull request
into `main`.

There is no new behaviour to review. What review rounds would read is output
the checkers already read, and they read it on every pull request rather than
once. The pull request lands on `release/v0.5.0` and squashes; the merge into
`main` and the `v0.5.0` tag are the repository owner's.
