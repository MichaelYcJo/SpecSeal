# 1788398967-local-modes-records-never-leave-the-clone — routing

<!-- seal/specs/1788398967-local-modes-records-never-leave-the-clone/routing.md
— the answer given before the first edit, in the batch the `implement` skill
collects (§1). Committed, because the check happens at the pull request and CI
sees only what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/local-modes-records-never-leave-the-clone |

Answered 2026-09-03 by the repository owner, before the first edit.

## Why this way

Issue #81, the last of 0.5.0. Local mode keeps the ledger and the work-item
records under the git directory, so a new machine or a re-clone starts with
nothing and CI's checks cannot run. That is the mode's whole trade-off, and
without a way to carry a copy it reads as *lose it* rather than *take a copy*.

`seal export` zips that root alone, never the session state beside it;
`seal import` never overwrites. Two new commands and a file format, which is
more than a session should build unreviewed, so it goes through the chain and
the pull request lands on `release/v0.5.0`.
