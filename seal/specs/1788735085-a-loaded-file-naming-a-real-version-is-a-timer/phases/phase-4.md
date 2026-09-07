# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `fae986a` — the commit carrying the fragments and these records. It could not carry its own hash, so this cell and `plan.md`'s phase-4 Status were filled in by the stamp commit that follows it |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Write `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, the two
fragments `CLAUDE.md` §*a change writes fragments, never the shared file*
requires in place of an append to the shared files. Verified by the fragments
themselves and `.github/scripts/fold_ledger.py --check`.

## What this phase found

**`fold_ledger.py --check` exits 1 here, and that is the correct answer.**
The plan's Verified-by cell reads as though a green `--check` were the goal.
It is the release gate — it fails while any fragment is still unfolded, and
the hygiene workflow runs it on pull requests into `main` only. This pull
request goes into `release/v0.9.0`, where the fragment is *supposed* to exist.
What the run proves is that the fold sees the fragment and names it, and the
proof it folds cleanly is `--version 0.9.0 --dry-run`, which exits 0 and
prints the section it would write. A later session reading the cell without
this note would take the exit 1 for a defect and go looking for one.

**`seal/ledger/` did not exist on this branch.** Every previous fragment was
folded into `seal/ledger.md` at the 0.8.3 release and git keeps no empty
directory, so this work item recreates it. Nothing had to be arranged for
that; it is recorded because a session expecting the directory to be there
would read its absence as a layout problem.

**A version-shaped or `path:line`-shaped string in a ledger row's PROSE is
read as a coordinate.** The first draft of R1 quoted the check's own failure
line — `docs/issues-and-milestones.md:28 names 0.9.0` — inside its Verified
cell, and `evidence-check` reported it as `OLD-FORMAT … run
evidence-check --migrate`. It is now spelled as "line 28 of
`docs/issues-and-milestones.md`". Worth recording because the row was
describing a coordinate rather than citing one, and nothing in the notation
distinguishes the two.

**The enumeration was re-run over the whole loaded set after four phases**,
which is what a guard that widens owes over its own new surface. Sixty-four
files, and every token in the scanned part is still one of the five: `1.2.3`
(now four occurrences — this branch's edit to
`docs/issues-and-milestones.md` added the fourth), `0.2.0` and `v0.3.0` below
the running version, `2.1.259` under the experiments prefix, `4.4.17`
declared. Everything else the run reports sits in `docs/flow.md` or the two
`docs/one-root-by-lifetime` editions, all three records of a moment. Nothing
this branch wrote is a new offender: the only real versions it added to
loaded prose are in `docs/flow.md`, which is exempt, and everything else it
wrote is under `seal/` or `tests/`, neither of which the check scans.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase only adds the two fragments and the records | none |
