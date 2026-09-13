# 1789296200-the-record-before-the-fix-sequence-has-no-arm — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | <this commit> |
| Ran by | specseal:smith on claude-opus-5[1m] — the spawn prompt named no model; the segment's own harness line is the source |

## What this phase was asked

The documentation and the pins: `docs/review-chain-spec.md`'s states table,
`skills/code-review/orchestration.md` §*And commit the record before
commissioning the fixes*, `templates/sdd-round.md`, plus this directory's own
`changelog.md` and the ledger fragment. Verified by A8, as cases of the shape
`test_the_spec_carries_the_subsection` already in the module, each seen red by
deleting the sentence it pins. `agent-contract` §14 is satisfied by this phase
riding the same commit as phase 4.

## What this phase found

### What landed where

| File | What it gained |
|---|---|
| `docs/review-chain-spec.md` | a ninth row in the states table, and a subsection — *The fourth exit* — carrying the three repairs it replaces, the four values that buy nothing, why it prints rather than passing in silence, why it owes no `ORDER_FROM`-style cutoff, and phase 1's measurement |
| `skills/code-review/orchestration.md` | the flag with a copyable command, what `new`'s new line means and that it refuses nothing, and the sentence that keeps the flag from becoming the habit |
| `templates/sdd-round.md` | the comment block below the field table. The ROW itself landed in phase 3, and `phases/phase-3.md` says why it had to |
| `seal/specs/…/changelog.md` | three entries — the fourth exit, `new`'s new line, and the row every generated record now carries |
| `seal/ledger/1789296200-….md` | three rows, hashes written by `evidence-check --reverify` at 13 rows re-verified. The file is this work item's fragment, so `seal/ledger.md` is untouched |

### The measurement is written into the spec and not only into this directory

`test_the_spec_carries_the_measurement_the_refusal_rests_on` pins *40 records of
152* in `docs/review-chain-spec.md`. The number is the whole reason `new` prints
rather than refuses, and a work item's directory ends its role when the work
ships while the spec stays. A reader six months on who asks *why does this not
just refuse* has to find the answer without opening a phase record.

### The section that already tells the orchestrator when to commit is where the flag goes

`skills/code-review/orchestration.md` §*And commit the record before
commissioning the fixes* is the section this work item's whole defect lives
under — it is the prose sequence that had no arm. The flag belongs there rather
than in a section of its own, because the reader who needs it is already in
that paragraph, and because the sentence that has to travel with it is *it is an
answer, not a way around the sequence*.

### §15 — what the failure looked like

Four mutations, each deleting the sentence one case pins.
`scratchpad/red_phase45.py`, each substitution asserted (§9), each file restored
from a copy taken before its first mutation.

| Mutation | Result |
|---|---|
| the spec's new states-table row deleted | **1 failed, 49 passed** — `test_the_spec_carries_the_fourth_exit_and_its_states` |
| the spec's `40 records of 152` replaced by `some records` | **1 failed, 49 passed** — `test_the_spec_carries_the_measurement_the_refusal_rests_on` |
| `--written-late` renamed in the orchestration section | **1 failed, 49 passed** — `test_the_orchestration_half_names_the_flag_and_the_shape` |
| the template's `a waiver with no author` replaced by `not ideal` | **1 failed, 49 passed** — `test_the_template_asks_for_the_row_the_generator_writes` |

Each killed exactly one case, which is each case being as narrow as it claims.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
