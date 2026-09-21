# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | the session |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/a-conflict-resolved-by-side-reverts-the-other-sides-corrections |

Answered 2026-09-21 by the repository owner, before the first edit.

## Why this way

The `automation` preset was pressed once, for the whole of the 0.12.2 run,
rather than per work item — the owner asked for the release to be prepared
while they were away, so the question could not be put again without stopping
the thing the answer authorised. This row says so rather than letting a
run-wide answer read as a work-item one: it is the same four values either
way, and what differs is that nobody was asked a second time.

**Planning says `the session` because two `framer` spawns stalled.** Both
died to the harness's 600-second no-progress watchdog — the first on its
opening burst of parallel reads, the second after stage 1, having announced
stage 2. Neither wrote a file. A third identical attempt is what this
repository's 3+ Fix Rule exists to stop, so the frame is drawn here instead.
The separation the framer exists for survives it: what must not happen is the
builder writing the contract it then builds against, and the builder is
`smith`.

The work is #424 — resolving a `seal/ledger.md` conflict by taking one side
silently reverts the other side's corrections, and a reverted row is
byte-identical to a row nobody has touched. That alters what a checker can
see, so the framer draws the frame before anything is built.
