# 1790208593-the-fold-writes-each-release-to-its-own-file — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/547-the-fold-writes-each-release-to-its-own-file |

Answered 2026-09-24 by the repository owner, before the first edit.

## Why this way

The owner pressed the `automation` preset once for the whole `release: 0.15.1`
milestone, asked in one batch before its first work item. This item is the
milestone's step D, the ledger's shape: `seal/ledger.md` is one 2,736-line file
every parallel branch re-stamps, and three work items conflicted in seven
hunks in the 0.15.0 run — MichaelYcJo/SpecSeal#547. It edits the same script
as step C's #540 and is built on top of that branch.
