# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 869ac116 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 3: `--reverify` records pact changes in both paths — the
trigger (`spec.md` item 4), the work item from `--into` or the branch's
declaration, the notify filter, `BROKEN`, no duplicate rows; the pact-changes
reader on the walker; the docs and skill text for the writer. Verified by
S7–S11 each red with the writer's call removed, `bin/mutation-check` over the
notify branches and the id resolution, and the evidence-check modules naming
`evidence_check.py` green. The spawn added: answer Q15 here.

## What this phase found

**The frame holds.** The writer is `evidence_check.py#record_pact_changes`,
fed by a `moves` list `reverify` and `reverify_into` append to at the moment
they know a coordinate's recorded hash and its new one, or that no one place
holds it. Collecting there rather than re-classifying the ledger beforehand
means the record follows what the re-read actually did: a row `--checked`
leaves whole (no date cell) moved nothing and records nothing, a file moved
whole re-points without moving a hash and records nothing, and a released
row is recorded only where `reverify_into` writes its `Re-read ·` row.
`released_drift`'s BROKEN tuples gained the row key and the recorded hash so
a released BROKEN coordinate can be recorded against its row.

**Q15: a vendored copy names each row citing a pact on a `LEFT` line,
records nothing, and exits 1.** It cannot read the `Pact` row with the
plugin's reader, so it cannot tell a declared pact from another; the ledger is
re-stamped as before, and the exit moves because every other `LEFT` line of
`--reverify` moves it. The sentence is pinned in
`test_a_vendored_copy_says_it_recorded_nothing`.

**Decisions inside the frame's room**: a ledger row citing two clauses of the
pact records one row with both anchors in its `Clause` cell, joined by `, `,
because the spec says one row per ledger row. The duplicate test compares
`Clause`, `Row` and `Code` and not `Checked`, so a BROKEN coordinate still
standing on the next day's run is not recorded again. An unparseable `Pact
notify` is read as the default, `when the pact is touched`, the direction that
records more. The `Checked` cell is `--checked`'s date, else today's.

**Mutation: 15 breaks, each red** — each writer call, `never` and `always`,
an undeclared pact counted, the duplicate test, each id source, both BROKEN
collection points in `reverify`, the released re-read and released BROKEN in
`reverify_into`, a left-whole row, the vendored refusal and a record that will
not parse. Three survived the first pass (the left-whole row, an ambiguous
coordinate, a released BROKEN) and each got the case it named.

**Seen red against `2b1dcb1f`**: 12 of the 16 cases. The four green there are
the negative cases (`never`, an undeclared pact, a left-whole row) and the
ledger-bytes invariant, and the first three are each red under the mutation
of the arm they watch.

**What the next phase needs**: the record's rows come back from
`hooks/config.py#pact_changes` as `(line, clause, row, code, checked)`; a
`—` clause is `config.NO_CLAUSE`; the record file's content hash is
`content_hash(gfm_lines(text))` over the whole file.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/the-pact.md`'s sentence that nothing acts on `Pact notify` | §*How a signatory names the pact* now says what the value decides, and §*A signatory records a pact change* states it |
