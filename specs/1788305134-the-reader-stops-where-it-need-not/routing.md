# 1788305134-the-reader-stops-where-it-need-not — routing

<!-- specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). Committed,
because the check happens at the pull request and CI sees only what is in the
tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/the-reader-stops-where-it-need-not |

Answered 2026-09-02 by the repository owner, before the first edit.

## Why this way

The command reader's two needless stops — a `VAR=value` the command itself
wrote out, and a `((` inside `${…}` read as arithmetic — were built and
reviewed through two rounds on a branch that predates this repository's
history rewrite (`fix/stops-the-reader-need-not-make`, local only, no common
ancestor with `release/v0.3.0`). That branch cannot be pulled; its change is
re-applied here onto the current reader, and round 2's four open 🟡 close in
the same work item. All three axes were answered in one question, together
with the sibling item that re-applies the implementer mark.
