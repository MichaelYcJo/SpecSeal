# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 88d5fe61 |
| Ran by | unknown — the spawn prompt named no agent and model for this row; the orchestrator fills it |

## What this phase was asked

`plan.md` phase 4, the records: `changelog.md`; the ledger fragment with the
new claims; the `Corrected ·` rows for 0.18.3's two anchoring rows and the
re-read of 0.19.0's `A1`; `overview.md`'s divergences and *Not verified*;
and the five text-hygiene modules the brief names. Verified by
`bin/evidence-check` green on the branch (S13) and by the hygiene modules.

## What this phase found

**Most of the ledger work moved into the phases it belongs to.** Each phase
broke released coordinates as it went: phase 1 removed `walk_tip`, phase 2
changed `close`, and phase 3 changed `call_sites`. `bin/evidence-check`
would have stayed red across three commits if the corrections had waited for
this phase. So each phase closed with its own rows. Five `Corrected ·` rows
stand in the fragment: 0.18.3's two, 0.19.0's `A1` (a correction rather than
a re-read, `overview.md`), and 0.16.0's `G9`, which phase 3 found. The
`Re-read ·` rows were written by `evidence-check --reverify --into`, after
each cited row was read against what this branch changed.
`bin/evidence-check --strict` exits 0 at 88d5fe61.

**"The five text-hygiene modules the brief names" named nothing this branch
can open.** The brief is not in this tree, and it is not on
`chore/834-every-reader-and-record-is-inventoried` either. This phase ran the
seven modules that hold document text to its rules over the files this item
changed. All seven passed (`overview.md`).

**#860's own range, measured after the build.** `99bcad40..092004bb`
resolves in this clone, so the new surface was read over it by a probe that
wrote no record and was deleted. It found 5 own commits, 9 paths, 13 units
added between the ends in those paths, and 2 kept. The old reading found 113
added units over the two ends' `.py` paths. `overview.md` holds the figures.

**`survivor-check` over `4e849e50..88d5fe61` named 7 places.** Each was read.
None is live text stating the retired walk, and each is excused in
`survivors.md` with a quote and the grounds.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
