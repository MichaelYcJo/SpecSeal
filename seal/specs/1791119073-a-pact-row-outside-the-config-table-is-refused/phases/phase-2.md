# 1791119073-a-pact-row-outside-the-config-table-is-refused — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 7a1f3b13 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The callers, end to end, with no code change expected. S9 and S5's writer
half in `tests/test_a_signatory_records_a_pact_change.py`, S10 in
`tests/test_pact_check.py`, S11 in
`tests/test_a_signatorys_ci_prints_its_pact.py`, each red with phase 1's
commit reverted. Q3: read the refusal sentence through each caller's
lead-in.

## What this phase found

**No caller changed, as the frame said.** The writer's plugin branch already
leaves every row a `notify` of None makes unknown, `pact-check` already
prints each refusal as `REFUSED` and exits 2, and `chain-check` already
prints each as a notice. Phase 1 producing a refusal with `notify` None was
the whole of the change.

**The writer's S6 joined S9 and S5.** `spec.md`'s S6 names a writer case as
well as a reader case: a stray notify row with no `Pact` value anywhere is
re-stamped at exit 0. It passes at the base too, so it is a guard, seen red
by phase 1's M1 break (refuse a stray notify with no pact) through
`mutation-check`.

**Seen red.** With `94d7b2e0`'s `hooks/config.py` in place, S9, S5's writer
half, S10 and S11 all fail: the writer re-stamped at exit 0, `pact-check`
was clean, and `chain-check` printed no notice. The same run is phase 1's
(`phases/phase-1.md`, *Seen red*). At `7a1f3b13` the three modules pass,
154 cases.

**Q3: readable after all three lead-ins.** A probe printed each caller's real
line for a `| Pact notify | always |` under a blank line:

- the writer: ``LEFT <ledger>:1  moved, and `Pact notify` may be `always`,
  and the `Pact` rows will not read: <sentence> — no pact change was
  recorded and nothing was re-stamped; fix the row and run it again``;
- `pact-check`: ``REFUSED <signatory> seal/config.md — <sentence>``,
  followed by ``READ … — `Pact notify`: will not parse``;
- `chain-check`: ``a `Pact` row this CI does not verify: <sentence>. Printed
  rather than refused, …``, beside the pact line's ``(`Pact notify`: a value
  that will not parse)``.

Each starts with the quoted line, and the sentence ends without a period, so
the lead-ins' own ` — `, `.` and `;` close it. The wording stands as phase 1
wrote it, and the three cases pin it whole in each caller's print.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
