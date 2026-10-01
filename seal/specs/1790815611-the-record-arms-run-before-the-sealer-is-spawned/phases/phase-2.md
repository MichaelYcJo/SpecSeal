# 1790815611-the-record-arms-run-before-the-sealer-is-spawned — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 4b061820 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

S7, the ticket's verification: a fixture item whose verifying round's record
carries `fixed at` in the shape `chain_check` refuses on a draft (Q1).
`broad-gate --preflight` exits 1 with `chain` named, and the row is not run.
The wall clock is measured once, on the fixture and on this repository, and
written here (Q2).

## What this phase found

**Q1 holds as (a), and the cell has to be written by hand.** Measured with a
probe over the fixture, all three shapes under the draft payload the gate
passes:

| Round 2's `Fixes checked by` beside a `fixed at <sha>` verdict | How it got there | chain arm |
|---|---|---|
| `nobody — the fixes are not yet written` | `round_record.py new` | exit 0, a notice |
| `nobody — the fixes are written and no round has opened them` | `close` with an empty fix table | exit 0, a notice |
| `no fixes to check` | written by hand, the cell #535's record carried | exit 1, `closed_with_a_fix` |

So today's generator never writes #535's pair. `new` lands `nobody`, `close`
corrects it to the written form, and both print on a draft rather than fail.
The S7 fixture writes the cell by hand. The docstring of
`a_verifying_round_that_says_fixed_at` says why, so a reader does not take it
for a generator shape.

**What the table means for the ticket's instance, and it is not this
branch's to change.** A verifying round's `fixed at` verdict now surfaces as
`Pass` beside `nobody` on the last record. On a draft, which is what the gate
and the preflight both judge, that pair prints and exits 0 (executed, the
table above). `chain_check` fails it at a READY pull request (read, not
run: `chain_check.py#checked_by`, the `strict` branch after `if not
strict:`). So a generated record with #535's verdict no longer reaches the
gate as a refusal: it passes the preflight and the sealer, and it fails
after the pull request is marked ready. The preflight cannot
catch it while it judges a draft, which the spec requires ("the same names,
arguments and environment `gate()` gives them"). This is written into
`overview.md` §*Not verified* with the owner named.

**Red first, executed:**

- R1, the flag absent: the `--preflight` argument renamed to a name it is
  not a prefix of. argparse refuses the command, exit 2.
- R2, the flag ignored: `if not args.preflight:` read as `if True:`. The row
  ran and wrote its marker file.
- T3, the fixture cell left as `nobody — …`: the case's own precondition
  fails.

A first R1, which renamed the flag to `--preflight-gone`, was red for the
wrong reason. argparse accepts `--preflight` as an abbreviation of it, and the
gate then failed on the missing attribute. It is reported here so nobody
takes it for R1.

**The wall clock, measured once (Q2).** Apple M3 Pro (arm64), macOS, on
2026-10-01 around 10:35 KST.

| Tree | Wall clock | Exit |
|---|---|---|
| the S7 fixture, `--preflight` | 1.57 s | 1, `chain` |
| the same tree, the full gate (row: a marker write, then `exit 1`) | 1.83 s | 1 |
| this repository at `4b061820`, `bin/broad-gate --preflight --base release/v0.17.0` | 30.86 s | 1, `ledger` |

The fixture is under the ticket's 10 s bound. This repository is not. Split
by the kept files' modification times: `ledger` (`evidence-check --strict`)
about 18.8 s including startup, `survivors` 8.46 s, `chain` 1.77 s,
`unverified` 1.51 s, `mode` 0.16 s, `corrections` 0.14 s. The ledger arm is
the cost, and why it is the cost was not measured (`overview.md`).

**The run on this repository was itself the preflight doing its job.** Its
`ledger` arm exited 2 on two DRIFTED rows in `seal/releases/0.10.0.md`: the
rows citing `broad_gate.py#gate` and
`tests/test_the_seal_is_taken_once_by_the_sealer.py#test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed`.
Both are anchors this branch edited, and phase 4 re-reads them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
