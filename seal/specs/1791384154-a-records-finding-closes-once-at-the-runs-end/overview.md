# 1791384154-a-records-finding-closes-once-at-the-runs-end — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     pending — filled when the build closes
· evidence: pending — filled when the build closes
· verified: pending — filled when the build closes

## Why this work exists

A ⬜ note stops costing a fix pass, a reader and sometimes the run's one reopening each round: it is carried open and closed once at the run's end by `round-record notes`, and `seal` and `chain-check` refuse a run whose notes are still open.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How the notes table names a note | `spec.md` Scope 5: `notes` "takes one `## Fixes` table in the shape `close` takes", keyed by `#` / the table carries a `Round` column in front, `\| Round \| # \| Verdict \| Commit or grounds \|` | the `Round` column | A finding's id restarts at every round. Measured over the seven work items carrying `rounds/` at 5623d728: every record numbers from 1, and in `1791270161` round 1 holds ⬜ 4 and ⬜ 5, round 2 ⬜ 2–4 and round 3 ⬜ 4 and ⬜ 5. A table keyed by the bare id cannot say which of two open notes a row closes (phase 1) |
| Whether an open note makes a record's landing pending | `spec.md` Scope 4: "`Pass` is derived as today", and the landing is not named / an open ⬜ no longer makes `Fixes checked by` read `nobody — the fixes are not yet written`; `Pass` is derived as before | the landing leaves open notes out | `round_record.py#landing_values` returned the pending value for any open verdict, so a verifying round that opened only a note never read `no fixes to check` — the run's end `notes` keys on (Scope 5), which then refused forever. A note commissions nothing, so it commissions no reader (phase 1, built in phase 2) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds settle |

## Not done

Pending — filled when the build closes.

## Fed back into the spec

Pending — filled when the build closes.
