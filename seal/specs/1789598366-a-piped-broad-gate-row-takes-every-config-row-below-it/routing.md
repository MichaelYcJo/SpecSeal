# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | fix/415-a-piped-broad-gate-row-takes-every-config-row-below-it |

Answered 2026-09-17 by MichaelYcJo, before the first edit.

## Why this way

Configuration disappears without a message: a `Broad gate` row containing a
pipe ends its cell at the first `|`, the reader stops at the line that will
not parse, and every row below it falls back to a default with nothing said
anywhere. That is a reader's behaviour changing for three callers, one of them
a `PreToolUse` hook, so it sits on the ladder's top rung and the frame is drawn
by a party that does not then build to it.

It is its own work item rather than a fifth row of the one before it. The four
already in this release are checks that fail to look; this is a value that
vanishes. One changelog entry covering both would teach a reader they are the
same thing.
