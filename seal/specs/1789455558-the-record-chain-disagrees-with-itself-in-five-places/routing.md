# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | fix/404-405-406-407-408-414-the-record-chain-disagrees-with-itself-in-five-places |

Answered 2026-09-15 by MichaelYcJo, before the first edit.

## Why this way

Five of the six issues are what round 2 of work item
`1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red` deferred
under its cap, and the sixth arrived the same way from this release's own first
work item. They are one branch because they are one subsystem — the round
record generator, the chain check, and the two case modules that read them —
and splitting them would queue two branches at the same files. Three of the six
change what a checker refuses, which is the ladder's top rung, so the frame is
drawn by a party that does not then build to it.
