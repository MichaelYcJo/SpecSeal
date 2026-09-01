# 1788212517-the-last-rounds-fixes-are-reviewed-by-nobody — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/the-last-rounds-fixes-are-reviewed-by-nobody |

Answered 2026-09-01 by the repository owner, before the first edit.

## Why this way

Issue #33 changes the review chain itself — the round record's schema, what
`chain_check` refuses, and when the last reviewer is spawned. A change to the
chain that ships without going through the chain would be the defect wearing
its own fix, so it goes through the review chain rather than straight to the
pull request. The pull request lands on `release/v0.0.2`, cut for this
release, alongside #34.

The scope was answered in the same breath: **option B and option A of the
issue, together.** B makes the state checkable in git, A is the one that would
actually have caught round 2's seven.
