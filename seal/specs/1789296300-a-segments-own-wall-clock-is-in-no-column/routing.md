# 1789296300-a-segments-own-wall-clock-is-in-no-column — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | feat/350-a-segments-own-wall-clock-is-in-no-column |

Answered 2026-09-13 by the owner, before the first edit.

## Why this way

This work item carries **#350 and #343 together**, because both land on the
same unbuilt thing: a reader that opens a spawned segment's own transcript.
#350 wants its span, calls and gaps in a column; #343 wants an agent's own
`Agent` call noticed there. Split across two branches the reader is written
once and reviewed twice.

Review was the one genuinely open axis here — a report mode is not a gate — and
the owner checked it: #343's shape is undecided in its own issue, which is
exactly what a round is for. The framer draws the frame and answers that shape.
The owner answered all three axes in one batch with the other two work items of
0.11.3.
