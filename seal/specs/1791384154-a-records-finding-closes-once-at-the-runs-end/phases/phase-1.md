# 1791384154-a-records-finding-closes-once-at-the-runs-end — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 61721ab6 |
| Ran by | unknown — the spawn prompt named the work item and the routing but not the agent and model running it; the orchestrator fills it |

## What this phase was asked

Build every phase of `plan.md` end to end without stopping (`routing.md`,
`automation`), with Q1 answered (a), unbounded. Phase 1 is the reader and
the gate: `NOTE`, `NOTES_FROM = 1791384154` and `note_rows` in
`chain_check.py`; arm A (a ⬜ closed on a fix word, an error from the cutoff
and a notice before it) and arm B (an open ⬜ on a record of the current run,
an error at a ready pull request and a notice on a draft), wired once per
work item after the per-record walk; `round_record.py`'s
`COMMISSIONS_NOTHING` built from `chain.NOTE`; the owner's `###` in
`skills/code-review/orchestration.md` and its row in the acts table. Verified
by the new module, each case red first, and the acts test.

## What this phase found

**The frame holds in the part phase 1 builds, and two parts of it do not
hold for phases 2 and 3.** Both were found by reading the tree before the
first edit, and both are built to rather than sent back.

1. **A finding's id restarts at every round, so a notes table keyed by the
   bare id cannot say which record a row closes.** `spec.md` Scope 5 has
   `notes` take *one `## Fixes` table in the shape `close` takes*, keyed by
   `#`. Measured over the seven work items carrying `rounds/` at 5623d728:
   every record numbers from 1 (for one, `1791270161`, round 1 holds ⬜ 4 and
   ⬜ 5, round 2 holds ⬜ 2–4 and round 3 holds ⬜ 4 and ⬜ 5). Two open
   notes of one run sharing an id is the ordinary case. The notes table takes
   a `Round` column in front: `| Round | # | Verdict | Commit or grounds |`.
   `overview.md` records the divergence.
2. **An open ⬜ makes a record's landing pending, so a run carrying a note
   could never end.** `round_record.py#landing_values` returns
   `nobody — the fixes are not yet written` for any open verdict, a ⬜
   included, and both `new` and `close` write that value. A verifying round
   that opened only a note would never read `no fixes to check`, which is the
   run's end `notes` keys on, so `notes` would refuse forever. Phase 2 lets
   an open note out of the landing (a note commissions nothing, so it
   commissions no reader) and leaves `Pass` derived as before. `overview.md`
   records the divergence.

**The run `notes` closes is the run the LAST record belongs to**, which is
not `round_record.py#current_run`'s answer: `current_run` returns the run the
NEXT record would belong to, which is empty when the last record is a
`second`. Phase 2 reads the run as `current_run(records[:-1]) + [last]`.

**Measured over the tree's seven work items carrying `rounds/`**, executed
2026-10-08 through `carried_notes` on each item's records: 24 notices for ⬜
rows closed `fixed` (every item before the cutoff), 0 errors, ready and draft
alike, and no open ⬜ anywhere. `chain-check` judges only the declarations a
branch touches, so the plan's *exit 0 under `chain-check`* for those items
was measured on the arm directly rather than through `main`.

**The released ledger rows phase 1 drifted are re-read once, in phase 4.**
`evidence-check .` after phase 1 names 51 drifted rows: `chain_check.py#main`
(23), the acts section of `skills/implement/orchestration.md` (18), the
code-review orchestration file's top and verifying-round sections (7), a
`chain_check.py` comment anchor (2) and `round_record.py#COMMISSIONS_NOTHING`
(1). Phases 2 and 3 move several of the same units again, so a re-read now
would be spent; `plan.md` phase 4 writes them with `--reverify --into`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
