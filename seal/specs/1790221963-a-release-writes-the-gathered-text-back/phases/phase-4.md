# 1790221963-a-release-writes-the-gathered-text-back — phase 4

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/phases/phase-4.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | a5630f93 |
| Ran by | unknown — the spawn prompt did not hand the value over, and the template forbids the segment naming itself; the orchestrator fills it |

## What this phase was asked

The records. Step A's ledger rows F1 and C2 corrected in place with a dated
`Corrected 2026-09-24` note, since both say the guard keeps gathered text
out and H1/H2 make that false; the drifted rows re-read and `--reverify`d;
this work item's ledger fragment, `changelog.md` and `overview.md`; the
branch's own sweep. One change to the plan, from the spawn prompt: step A's
`plan.md` is not edited, because it is a shipped work item's record of what
it planned, and the gate row #557 gives lives in this work item's `plan.md`
gate table, which already carries one.

## What this phase found

**Q3: the build drifted exactly the rows `spec.md` §*Data & interfaces*
predicted.** `evidence-check --strict` before `--reverify` named four
anchors: `corrected` (rows S3, S1, G5, E1 of `seal/ledger.md` and C2, F1,
R1, U2 of step A's fragment), `newly_released` (F1) and
`a_gathered_fragment` (C2). The docstring heading anchor
`#"## What is excluded, by construction rather than by list"` did not
drift, so rewording and adding a sentence under it changes nothing that
anchor hashes. `--reverify` re-stamped 21 rows: those 10 and the 11 anchors
of this work item's three new rows. Afterwards `evidence-check --strict`
reads 1777 ok, 0 drifted, 0 broken.

**One row the table did not predict: step A's C3.** Its anchors did not
drift, but its note repeated *a release's gathering commit deletes each
fragment*, one of the three sentences phase 1 removed. It is corrected with
a dated note too (`agent-contract` §12). A `git grep` for each removed
sentence across the tree finds the remaining copies only in step A's
`rounds/` records, which record a past state and are not edited, and in the
guard's own comment *a gathered release writes none*, which is true inside
the branch it guards and stays.

**The branch's sweep reports nothing.** Over
`origin/release/v0.15.1...HEAD` at `06277713`, with all eleven
`seal/specs/*/survivors.md` passed as `--exempt`: exit 0, 407 files
examined, against 22 removed sentences, and `no removed wording is still
standing`. So no `survivors.md` row is owed by this work item.

F1's note says where the corrected bound is now, because step A's `plan.md`
gate row is left carrying the old one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The clause *the `lost` guard is what keeps a gathered release's text out of `written`* from step A's rows C2 and F1, and *deletes each fragment* from C3 | The same rows, each with a dated `Corrected 2026-09-24` note quoting what it said; the true bound in F1's claim and in this work item's rows H1–H3 |
