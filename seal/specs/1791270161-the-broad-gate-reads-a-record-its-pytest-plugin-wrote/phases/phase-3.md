# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <the phase-closing commit — the hash `plan.md`'s Status cell for phase 3 carries> |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The ledger and changelog fragments (`spec.md` Scope 11), starting from the
S21 probe's ledger arm, 48 broken and 162 drifted coordinates: each released
row whose unit moved or retired is re-read or corrected in this item's
fragment, through `evidence-check --reverify --into … --checked 2026-10-06`
and hand-written `Corrected ·` rows where the unit is gone, and no released
file changes (`Ledger frozen from`). `bin/evidence-check --strict .` and
`bin/correction-check` exit 0 when the phase closes. `Ran by` is written by
this phase, as the orchestrator asked.

## What this phase found

**What the checker owed, by family root.** `evidence-check --reverify .`
without `--into` named 96 released rows left: 49 roots with a drifted
coordinate, and the broken coordinates of 0.18.1's B2 and 0.18.3's R1, R2,
R3 and the `Corrected ·` rows D1, D2, B3, S5 and B4 there. Each root was
read against this branch's diff before anything was written.

- **Corrected, ten rows and one more in phase 4.** 0.18.1 B2 and 0.18.3 R1,
  R2, R3, R4, D1, D2, B3, S5, B4 each describe the prefix cut, the JUnit
  report, the proof pass, the group or the runs alone, so each is retired
  by a `Corrected ·` row that states what holds now and re-points the claim
  to the units that hold it. R5, the corpus's words, was corrected in phase
  4, once the corpus had words to cite.
- **Re-read, 38 rows.** Every other owed root is a claim about the row's
  refusals, the preflight and its ask, the stamp, the arms and their
  coverage line, the `cmd.exe` rewrite, the config table or the
  `splitlines` list. Each was read against the diff — `args.base` is still
  read once, the preflight still hands the row no environment and writes no
  `records/`, `run` is still the one shell site with `gate` and
  `compare_at_base` its callers — and `--into` wrote one `Re-read ·` row for
  each, citing it.
- **Nine new rows, W1 to W9**, state the work's own claims: the recorder,
  the environment, the reader, the `HEAD` fallback, the one base run, the
  naming, the `PYTHONPATH` limit, rule 3 and the hygiene tables.

**Hashes were written by the tool.** The new and correcting rows were
written with placeholder hashes, and an in-place `--reverify --ledger
<fragment> --checked 2026-10-06` stamped every coordinate and citation of
the fragment; no hash was typed.

**The records sweep read this work item for the first time.** The
fragment's existence marks the item unshipped, so `--strict` began reading
its records and refused 23 backticked names not in the tree: the retired
units and test names the phase records and `overview.md` cite, and the
pytest and xdist internals `spec.md` and `plan.md` read. Each such
line now carries `(NAME NOT IN TREE)`, the marker earlier items wrote,
including seven lines of `spec.md`, three of `plan.md` and one of
`questions.md`. No claim was changed.

**Executed:** `bin/evidence-check --strict .` exit 0 (`6519 ok · 0 drifted
· 0 broken`, the records sweep `0 refused`); `bin/correction-check` over
the branch's range, see `phases/phase-4.md`, which closes after this phase
in the same branch state.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — no released row is removed under the freeze; eleven are retired by `Corrected ·` rows in this item's fragment | none |
