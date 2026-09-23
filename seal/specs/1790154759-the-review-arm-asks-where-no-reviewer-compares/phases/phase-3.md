# 1790154759-the-review-arm-asks-where-no-reviewer-compares — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 234fdff0 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Write the records: the changelog fragment, the ledger fragment
`seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md`
with the claim that the review arm reads no paths, anchored on
`hooks/commit-review-gate.py#judge`, and `overview.md`. `evidence-check` on
the fragment reports the new row `ok`, and `unverified-check` reads the memo.

## What this phase found

**Phase 2's prose edits drifted four existing `seal/ledger.md` rows, and none
of their claims moved.** `evidence-check --strict` exited 2 before this
phase's writes: the opt-in headings row anchored on §*Review arm*, and two
rows anchored on the orchestration routing section. A `Re-read 2026-09-23`
note on the first of them then drifted a fourth row, the one anchored on the
`1788331011` ledger heading that holds it. Each was re-read against its claim,
given a `Re-read` note naming this work item, and re-stamped by
`evidence-check --reverify`, which changed those four hashes and nothing else.

**S11 did not drift.** It anchors `DOC_ROOTS`, and the comment phase 1 wrote
above the constant is outside the unit, so the row the plan names as the
parity half was left as it is. `judge`'s hash is unchanged too (`6ca45c3c`,
the value `seal/ledger.md`'s Q5 row already holds), because phase 1's comments
sit outside it.

**The fragment's one row cites the behaviour and the prose together.** R1
anchors `judge` and `touches_code` with the three cases, so a change to any
of them re-opens the claim.

**Executed at `234fdff0`:** `evidence-check --strict .` — exit 0,
`1481 ok · 0 drifted · 0 broken`, the fragment `5 ok`.
`unverified-check --baseline origin/release/v0.14.0` on the memo — exit 0,
`1 open · 0 closed · 0 unreadable`, the open row being the sealer's broad
gate. `correction-check --range origin/release/v0.14.0...HEAD` — exit 0, no
merge commit in the range. Twelve modules that read fragments, records or the
ledger, `tests/test_chain_hooks_hardening.py` among them — `468 passed`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
