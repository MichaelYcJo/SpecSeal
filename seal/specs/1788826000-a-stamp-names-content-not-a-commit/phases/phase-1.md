# 1788826000-a-stamp-names-content-not-a-commit — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `c2c7864` |
| Ran by | `smith on unknown — the spawn prompt named the agent and not the model, and this record does not source that value from the segment's own idea of what it is` |

## What this phase was asked

Write the SDD ladder for a migration whose direction was already settled, and
answer two questions in `spec.md` rather than raising them: what a rider stamp
names instead of a commit, and whether a round record's `Target SHA` moves with
it. Re-derive the corpus rather than trusting the handoff's count.

## What this phase found

**The handoff's count was false in both numbers, and its own file list
contradicted it.** It said 13 stamps across 10 files; the list it gave sums to
15, and a walk of the tree finds **19 real riders across 14 files** plus one
quoted inside a round record. Contract §5 is why this was measured before
anything was built on it.

**Two further instances of the same class turned up in the counting**, and §12
makes them this work item's rather than a later one's:

- `RIDER_ROOTS` scanned four roots and the tree has riders in six, so
  `.github/scripts/fold_ledger.py` and two riders under `tests/` were held by
  nothing at all;
- one of those two had never carried a stamp in any form — its staleness line
  read *"green at 3f8f846, measured 2026-09-03"*, matching no pattern — so it
  was invisible even to the case that refuses an unstamped rider.

**The residual was measured before it was designed against.** Twelve of the
nineteen riders sit inside the AST span of the unit they are about, so a rider
hashing its own enclosing unit is the dominant case rather than a corner, and
"exclude rider blocks from the region" had to be the rule rather than a
special case.

**Question 2 was settled by opening `chain_check.py`, not by analogy.**
`reachable()` falls back to `carried_by_a_pull_head`, which scans
`refs/remotes/pull/<N>/head` — the mirror CI fetches of a namespace a squash
does not touch. The phase wrote the remote spelling, `refs/pull/<N>/head`, and
round 1 found it in six places; it is corrected here. So a round
record's SHA already survives the merge rule that orphans a rider's, and the
two mechanisms were never the same mechanism with a different corpus. That is
the whole grounds for leaving `Target SHA` alone, and it would not have been
available from reasoning about what the two rows look like.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
