# 1789621028-nothing-reads-a-record-against-the-tree — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/344-426-427-nothing-reads-a-record-against-the-tree |

Answered 2026-09-17 by MichaelYcJo, before the first edit.

## Why this way

A round record is written once and the tree keeps moving, and nothing reads
one against the other the way `evidence-check` reads the ledger. #344 is the
class — five places where a record says something the tree does not — and
#426 and #427 are two of its instances inside the generator that writes those
records: a guard that compares against a constant and so cannot see a file
that arrived truncated, and a `close` that prefixes grounds instead of
replacing them, so re-closing a corrected record duplicates them invisibly.
What a record asserts is what the next round inherits and what CI reads at the
pull request, so this changes observable behaviour and the frame is drawn by a
party that does not then build to it.

The three travel together because the answer to #344 — an anchor, a checker,
or a rule — decides what #426 and #427 are fixed into. Taking either instance
first fixes it at its own coordinate and the reader that would have caught all
five is never built.
