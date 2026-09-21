# 1789956662-the-gate-and-ci-ask-about-different-ranges — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/the-gate-and-ci-ask-about-different-ranges |

Answered 2026-09-21 by the repository owner, before the first edit.

## Why this way

The preset was pressed, so every party runs and the run does not come back
with a question. The work is #423 — the broad gate resolves `--base` to a
local ref where CI resolves it to the remote-tracking one, so a stale base
seals a branch green that CI then refuses. That alters a gate's verdict and
what its stamp claims, which is the ladder's top rung, so the framer draws
the frame before anything is built.
