# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | cba1b536 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The marker reader: verb-and-date matching over ledger text, and the
row-survival test. A7 and the row-survival half, each red against the
reader's absence. Plus M1's measurement over this repository's own merge
history — how many merges of the ledger exist in reachable history and how
many dropped a marker — recorded in `overview.md` whatever it says,
including zero.

## What this phase found

**M1 is not zero, and what it found is not a defect — it is the rule in
`spec.md` §Scope 1 reporting correct work.** Measured over 37 merge commits
reachable from every ref, 24 of which had a parent carrying a ledger with
markers. The rule as the spec states it — *a marker present in either
parent's ledger text and absent from the merge result, while the row carrying
it survives* — reports **one** merge, `87eced1` (the v0.9.3 release merge),
and **five** markers, all on one row. Opening it: `release/v0.9.3`
deliberately re-anchored that row when its section moved file, rewrote the
Notes cell to say *Re-anchored, not re-verified*, and dropped four historical
`Re-read` sentences with the prose it replaced. The merge took that rewrite.
The merge decided nothing; one parent had already decided it.

**So the spec's rule needs a third input, and the third input is the merge
base.** A merge is correct to drop a marker when a PARENT deleted it relative
to the base, and wrong to drop one that no parent asked to lose. The two
cases are structurally identical without the base and separate cleanly with
it:

| | base | the parent that has it | the other parent | result | verdict |
|---|---|---|---|---|---|
| #424's incident | absent | present — it added the correction | absent, unchanged | absent | the merge discarded an addition — **report** |
| `87eced1` | present | present, unchanged | absent — it deleted the marker | absent | a parent deleted it and the merge honoured that — **silent** |

Re-measured with the base test: **0 merges, 0 markers.** The refinement
strictly narrows what the check reports, which is the direction A3 argues
for, and it leaves A1, A2, A3 and A6 untouched because in each of their
fixtures the base carries no marker at all. It is a divergence from
`spec.md` §Scope 1 as written and `overview.md` carries the row.

**The incident's own merge is not in reachable history, and that is the
squash `spec.md` predicted.** No `refs/pull/*` namespace is fetched in this
clone, and the feature branch that carried the #424 resolution squashed into
its release branch. So M1's measurement is over what a clone can reach, and
the one thing it cannot reach is the instance the ticket is about — which is
the whole of why M2 is a measurement and not an assumption.

**Two units were green while broken, and both were repaired here rather than
noted.** The mutation sweep ran eight mutations over the six units this phase
adds. `standing` returning any row of the result — the permissive direction,
which is the one A3 exists to refuse — left A3's case green, because the
first mutation attempted returned the PARENT's row and the marker counts then
cancelled. `_index`'s ambiguity guard turned nothing red at all: the parent's
own ambiguity is computed in `losses` and shadowed it, so the guard's real
subject is the RESULT's side — a merge that split one row into two citing one
unit — and that had no case. Both cases are now in the module.

**A row's identity is two things and the second is not a nicety.** All three
of the incident's corrections landed in a cell after the first, so the first
cell alone would have carried them. A correction to the claim cell itself is
the case the anchors answer, and the anchors are available for exactly the
reason the ledger has the rule it has: a row is never re-pointed, it is
removed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds one script and one test module and takes nothing out of the tree | none |
