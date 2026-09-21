# 1789996775-the-gate-states-what-its-own-fixes-disproved — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/the-gate-states-what-its-own-fixes-disproved |

Answered 2026-09-21 by the repository owner, before the first edit.

## Why this way

The `automation` preset was pressed once, for the whole of the 0.12.3 run,
and in the same call the owner chose how the milestone's six issues are cut
into work items — two of them, by the file each set of statements sits in.
This row says the answer was run-wide rather than work-item-wide: the four
values are the same either way, and what differs is that nobody is asked a
second time.

The work is #461, #464 and #465 — three sets of statements the gate's own
fixes disproved, left open because #423 capped before they could be spent as
reopenings. None of them changes what the gate does; every one of them makes
a reader believe something the same work item measured to be false.

**`Planning` says `framer`, and the row was added in this commit rather than
the one before it.** The previous run's two `framer` spawns both died to the
harness's 600-second no-progress watchdog, so at the routing commit it was
not yet known whether one would draw this frame — and an absent row reads as
*not answered*, which was the true state. This spawn was told not to open
with a parallel read burst and to write a skeleton `spec.md` inside its first
few calls; it finished in ten minutes and wrote all three files.
