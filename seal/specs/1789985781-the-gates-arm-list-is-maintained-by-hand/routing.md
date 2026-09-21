# 1789985781-the-gates-arm-list-is-maintained-by-hand — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | the session |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/the-gates-arm-list-is-maintained-by-hand |

Answered 2026-09-21 by the repository owner, before the first edit.

## Why this way

The `automation` preset was pressed once for the whole of the 0.12.2 run
rather than per work item — the owner asked for the release to be prepared
while they were away, so the question could not be put again without stopping
the thing the answer authorised. This row says so rather than letting a
run-wide answer read as a work-item one.

`Planning` says `the session` for the same reason it did on the work item
before this: two `framer` spawns died to the harness's 600-second no-progress
watchdog on that item, 17.6 minutes and 1.2M tokens for no file, and a third
attempt of the same shape is what the 3+ Fix Rule exists to stop. The
separation the framer is for survives it — what must not happen is the builder
writing the contract it then builds against, and the builder is `smith`.

The work is #468, and it is in this release rather than the backlog because
**0.12.2 is the release that opened the gap.** #424 added a sixth hygiene arm
and `broad_gate.py` mirrors five, so from this release onward a sealer's run
answers a shorter list than the merge is judged by. `docs/issues-and-
milestones.md` sizes a release by what has to be in effect before the next
work item starts; a seal that under-answers is exactly that.
