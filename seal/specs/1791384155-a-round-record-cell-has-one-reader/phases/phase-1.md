# 1791384155-a-round-record-cell-has-one-reader — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d9c71475 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

J1 of `spec.md`: `broad_gate.py#rounds_rows` reads `Needs a fix` through
`chain.says_reopened`, True drawing ` · capped`, False not capped, None the
count alone. `agents/sealer.md`'s `rounds` sentence by replacement, and the
`Re-read ·` rows the edit owes. Verified by S1's cases red with the
`startswith` reading restored, then green, and the sealer module green.

## What this phase found

- Only one released row needed a citing row: 0.20.0's `Corrected · N9`,
  whose claim said `capped` where the cell begins `yes`. It is false now, so
  this item's fragment carries a `Corrected ·` row in its place rather than a
  `Re-read ·`. The 0.12.x and 0.15.x rows on `agents/sealer.md#"## The
  command"` are already cited by #869's fragment, so `--reverify` re-stamped
  those citing rows in place; none of their claims is about the `rounds`
  sentence.
- The release branch carries 33 drifted rows that no edit of this item
  touches: `agents/warden.md#"## Report"` (8),
  `templates/config.md#"# Repository config"` (14),
  `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` (10)
  and `skills/verify/scripts/payload_meter.py#heading_starts` (1), measured
  on an archive of `origin/release/v0.21.0`. `--reverify` re-stamped three of
  them inside #869's fragment as a side effect; those three were put back by
  hand, because nobody on this branch read their claims. Every later phase
  narrows its `--reverify` with `--ledger` for the same reason.
- The chain check over the tree reads the same as before the phase, at the
  orchestrator's baseline and over every declaration (a baseline at the root
  commit, 13 work items with rounds).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `rounds_rows`' `startswith("yes")` reading of `Needs a fix` | `chain_check.says_reopened`, which the panel now calls |
