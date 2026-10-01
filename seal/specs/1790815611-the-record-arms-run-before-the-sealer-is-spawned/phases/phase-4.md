# 1790815611-the-record-arms-run-before-the-sealer-is-spawned — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | the commit that adds this file; `plan.md`'s Status cell for phase 4 names it |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

The records. `seal/specs/<id>/changelog.md` under `### Added`;
`seal/ledger/<id>.md` with one row per scenario the build verified;
`overview.md` with the `agents/sealer.md` diff recorded empty; a
`phases/phase-N.md` for each closed phase. Every row in `seal/ledger.md` or
`seal/releases/*.md` whose anchor the branch edited is re-read and re-stamped
there with a dated note, or removed if its anchor went.

## What this phase found

**The branch drifted 27 rows in 12 release ledgers, and one claim had become
false.** `evidence-check --strict` reports one line per anchor and hash in
each file, 23 in all, and several rows share an anchor. So every row citing
a drifted anchor was found by its anchor rather than by the report's count,
read against the branch's edit, given a dated `Re-read` note, and re-stamped
with `--reverify --checked 2026-10-01 --ledger <file>`, one file at a time.
`seal/releases/0.15.7.md` N2 said every green run without `--record` prints a
`SEALED` line, and a green `--preflight` run prints `PREFLIGHT PASSED`. It is
corrected in place with a `Corrected` note, and the preflight's own claim is
P1 of this work item's fragment. Afterwards the whole ledger reads 3,152 ok
and 0 drifted, exit 0. No anchor was removed, so no row was.

**The changelog takes `### Changed` beside `### Added`**, because the
template's example row is a change to something that shipped rather than an
addition.

`git diff --quiet cd24f516 -- agents/sealer.md` exits 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
