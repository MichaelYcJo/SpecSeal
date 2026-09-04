# 1788491830-a-segments-record-says-what-it-cost — phase 4

<!-- seal/specs/1788491830-a-segments-record-says-what-it-cost/phases/phase-4.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | b353704 |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 4 only: the changelog and ledger fragments, and `docs/flow.md` —
this ticket's box, and a row for the outcome-column ticket this work opens.
Verified by `evidence-check --ledger`, `fold_ledger --dry-run` and
`unverified-check`.

The `docs/flow.md` rule arrived in `1ee83ad`, the commit this branch sits on:
a branch writes that file for the rows its own work created or closed, in the
pull request that earns them. Nothing else in that file is this branch's.

## What this phase found

**The ticket was not opened, and that is a rule rather than an omission.**
`skills/agent-contract/SKILL.md` §6 — an implementing agent writes no durable
record, posts nothing, and opens no pull request. A GitHub issue is a durable
record outside the repository, so the row in `docs/flow.md` is written and its
number is not. The row says so in its own text rather than carrying a
placeholder that reads like a reference, and the drafted body went into the
handback for whoever opens it. `overview.md`'s *Not verified* carries it with
the orchestrator named, which is what keeps it from being a deferral to
nobody.

**The ledger rows came out of the mutation loop, not out of reading the
diff.** Two of the three — R2 and R3 — are the loop's two survivors, and each
is the same shape: a case that existed, named the thing it meant to pin, and
stayed green against the mutation of that thing. R2's `carbon` tripped an
earlier clause than the one it named; R3's bare-name needle was satisfied by
prose around the row it named. Reading the diff would have produced neither,
because both cases read as correct.

That is worth stating as a class rather than as two instances: **a case whose
input or needle is satisfied by something other than the thing it means to pin
is green against its own mutation.** It is what the loop is for, and this work
item produced two in twenty mutations.

**`fold_ledger.py --check` reports the three unfolded fragments and exits 0.**
That is the informational half of the command, not a refusal — it refuses only
while an `evidence-todo.md` in the tree has an open row, and this work item
has none.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/flow.md`'s open box for #137 | the box is ticked in place, and the half this work item did not build is a new row in the same file's 0.9.0 section — the removal and its destination are one edit |
