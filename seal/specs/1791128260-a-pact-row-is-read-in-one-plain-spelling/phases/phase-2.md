# 1791128260-a-pact-row-is-read-in-one-plain-spelling — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e2f81bdb |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The callers, end to end, with no caller code changed. S6: the writer,
`evidence-check --reverify --into`, under `CONFIG` and a stray
`| Pact notify | always |` below a blank line, leaves the moved row citing no
clause on a `LEFT` line naming the refusal, exits 1, keeps the ledger
byte-identical and writes no `seal/pact-changes/`. S7: `pact-check` at the
pact's repository prints a `REFUSED` line carrying the sentence and exits 2.
S8: `chain-check` prints a notice carrying the sentence and its exit does not
move. Each seen red at the base. #784's caller cases are the source.

## What this phase found

**No caller code changes, as the frame said.** The writer's plugin branch
already leaves every moved row a refusal makes unknown: `blind` holds where
`notify` is None, and `refused and unknown` prints `LEFT` with `refused[0]`
and returns 1. The reader puts the line refusals after the doubled-`Pact`
refusal and before the entry refusals, so where one stands it is the first
refusal, and the `LEFT` line names it.

**S6 is two rows.** The notify line below a `Pact` row, which is the spec's
S6, and a `Pact` line below a table that holds none, citing the pact's clause.
The second is #784's S5 writer half, kept because it is where "refusing is not
split by item" reaches the writer: with no plain `Pact` row, `pacts` is `[]`
and `notify` None, and the row citing the clause is left as
"cites a pact clause".

**The sentence reads after all three prefixes** (Q4). The cases pin it whole,
including `chain-check`'s appended ". Printed rather than refused" and
`pact-check`'s ` — ` after `seal/config.md`. The writer's `LEFT` line is
compared with its whitespace collapsed, as #784's was, because the line puts
two spaces after `LEFT`.

**Seen red (§15).** With `94d7b2e0`'s `hooks/config.py` in place and the
phase 3 edits set aside, all four cases failed: both writer rows on
`assert 0 == 1`, re-stamping `src/orders.py#serialize 57f678c6 -> 7069baf7`;
`pact-check` on `assert 0 == 2`; `chain-check` with no notice. At
`e2f81bdb` they pass, and so do the three modules whole, 153 cases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
