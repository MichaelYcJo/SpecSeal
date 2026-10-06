# Implementation Plan: a base session that died part-way is not read as finished (#849)

<!-- seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-07 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

Apply round 6's paste-ready fixes for 🟡 1 and ⬜ 2, plant the cases that show each one red first, and correct work item 1791270161's overview for ⬜ 3. One phase.

## Technical context

- `skills/verify/scripts/broad_gate.py#read_record` and `#base_word` hold the demotion. The `unplaced_red` check from #825's round 5 comes first and stays first.
- `skills/verify/scripts/pytest_record/specseal_pytest_record.py#Recorder` holds `last_sent`.
- The round-6 report's *Executed probes* section names the fixtures `CRASHES_ITS_WORKER` and `CRASHES_ITS_WORKER_IN_SETUP` and the layout (`FILES_ROW tests`) that read `new` at the base.
- Failure scenario of the chosen approach: a recorder that stops writing for another reason, such as a full disk, also reads as unended and turns `new` into `new?`. That is the strict direction, and rule 3 says so.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Count sessions with no `end` line as unended (round 6's fix) | a recorder that stopped writing for another reason also demotes: strict, and named | chosen |
| Treat a missing `end` line as the run's exit code alone | plain pytest that died has no exit code the gate can tie to one session among several | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | 🟡 1 and ⬜ 2 fixed, rule 3's sentence and its pin, S1–S6 cases, the 1791270161 overview row, the changelog fragment and ledger rows | each new case red at 6de64c19 and green after; `bin/mutation-check` red on each new unit; the gate and recorder modules; `bin/evidence-check --strict .`; `survivor-check --range origin/release/v0.20.0...HEAD` | 57eb5307 |

## Operational impact

A failing suite whose base run had a session die part-way now reads `new?` instead of `new` for the files that would have read `new`. No other word changes.
