# 1788217118-a-gate-change-is-not-judged-on-prompt-cost — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | docs/a-gate-change-is-not-judged-on-prompt-cost |

Answered 2026-09-01 by the repository owner, before the first edit.

## Why this way

The change is prose in two documents that `install.sh` does not distribute —
`CONTRIBUTING.md` and the repo-local half of `CLAUDE.md`. Nothing a spawned
session reads as its contract changes, and no gate's verdict moves, so the
review chain would cost more than the risk it covers.

It runs in a worktree rather than the shared tree because
`1788212517-the-last-rounds-fixes-are-reviewed-by-nobody` is mid-review there.
The two touch no file in common.

The pull request lands on `release/v0.0.2`, cut for this release.
