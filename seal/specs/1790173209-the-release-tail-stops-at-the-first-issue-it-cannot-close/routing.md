# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/536-the-release-tail-stops-at-the-first-issue-it-cannot-close |

Answered 2026-09-23 by the repository owner, before the first edit.

## Why this way

The owner pressed the `automation` preset once for the whole `release: 0.15.0`
milestone, asked in one batch before its first work item. This item is the
milestone's step C, the release tail: MichaelYcJo/SpecSeal#536 and the seven
tickets beside it, every one paid for by hand at the 0.14.0 release. It runs
in its own worktree because the design item holds the main checkout, and it
is framed first because a change to the release sequence is only ever met at
the next release.
