# 1791384154-a-records-finding-closes-once-at-the-runs-end — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     this item's `spec.md`, `plan.md` (Approved 2026-10-08), `questions.md` (Q1 answered (a)), `handoff.md`, `routing.md`; `skills/code-review/orchestration.md` §*Orchestrator: the run ends with a verifying round* and §*A fix of a fix twice sends the work item back to its framer*; `skills/code-review/SKILL.md` §*Findings format*; `skills/implement/SKILL.md` §3–§5; `docs/the-evidence-ledger.md` via `evidence-check --help`; `CONTRIBUTING.md` §*House rules*
· evidence: `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md` N1–N13, `Corrected · S6` (0.10.0), and 73 `Re-read ·` rows for the released rows the build drifted
· verified: executed — every new case seen red first (`bin/mutation-check`, 30 breaks, all red; one more first named a `-k` that matched no case and was re-run with one that did), the touched test modules and the text-hygiene modules narrow, `ruff check` and `ruff format --check` on every touched Python file, `survivor-check` over the branch, `evidence-check --strict .` exit 0, Q2's corpus count; read — the 152 released rows' claims, `chain-check`'s other arms' interaction with notes; unverified — the full suite, lint and typecheck (the sealer's)

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
| `notes`, `close`'s carried note and the two `chain-check` arms on a real run, through a warden's report rather than a fixture: this item's own review rounds are the first run under the rule | the orchestrator, over this item's review rounds |
| The merge with #860 and #866, which edit `close` and `chain_check.py` beside this item's lines | the orchestrator, when it integrates the siblings |

## Not done

Phase 2 left a stopped run's notes unread once the redesign's first record exists. Round 1's 🟡 3 found it a defect rather than a leaving, and the fix pass closed it: `new` refuses the redesign's first record while the stopped run carries an open note, naming it and `notes`.

Phase 4 left `docs/review-chain-spec.md` §*The last round verifies* saying a record-located correction closes in the fix table and is "corrected in passing or not at all". Round 1's 🟡 4 found that it does contradict the rule, since `close` refuses a ⬜ row. The fix pass reworded both sentences in place, adding no line to the document at 999 of 1,000: a ⬜ closes at the run's end through `notes`, a 🟡 in its fix table.

`NOTES_FROM` is `1791384163`, one past 0.21.0's batch, not this item's own id as the other cutoffs are: every sibling of the batch runs its rounds under the installed 0.20.0 `close`, which demands a row for a ⬜ and admits `fixed` (round 1's 🟡 2).

`CAPPED_EXIT` and `REFRAME_EXIT` still say every finding still open closes `deferred`; with notes carried, a ⬜ closes through `notes` at that same moment. Rewording the pair is the repository owner's decision (`spec.md` Out), so they stand, and the owner file's reframe table says what happens to a ⬜ there.

## Fed back into the spec

Inferred during implementation, each one a planner may overturn:

- The notes table carries a `Round` column, `| Round | # | Verdict | Commit or grounds |`, keyed by round and id (`spec.md` Scope 5 said the fix table's shape).
- An open note is left out of a record's landing, so a record whose other rows closed without a fix word reads `no fixes to check`; `Pass` is unchanged (`spec.md` Scope 4 was silent on the landing).
- The run `notes`, `seal` and `close`'s count read is the run the LAST record on disk belongs to — `current_run` of the records before it, plus that record — so a `second` closes its own stopped run.
- `seal`'s note refusal fires only where the last record reads `no fixes to check`, and comes before the `Pass` refusal; before the run's end the existing refusals are the true ones.
- The corrected grounds name `--at` resolved, in eight hex characters, so `--at HEAD` is a legal spelling.
