# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/237-the-guard-asks-once-per-worktree-not-once-per-session |

Answered 2026-09-08 by the repository owner, before the first edit.

## Why this way

This item was added to the 0.9.1 run by the owner mid-run, after the guard
held the run at each of five `git worktree add` calls. It inherits the run's
routing answer unchanged — `smith` builds, the review chain runs, the pull
request opens — and it inherits the run's stop condition too: if it is not
finished when the rest of 0.9.1 is, it moves to 0.9.2 rather than holding the
release. It changes a gate, so `CONTRIBUTING.md` *What a change to a gate must
carry* governs the pull request body, and the prompt budget is the claim.
