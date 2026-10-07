# 1791384162-the-macos-test-leg-runs-in-shards — overview

<!-- Opened in phase 1 at the first divergence; closed in phase 2. -->

## Why this work exists

The macOS leg was the job every run waited on at 15 to 21 minutes; three
shards bring it near the Windows shards, and the suite reads the matrix once.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| When 0.20.0's S4 is corrected | `plan.md` §*The ledger*: "Between phase 1's commit and phase 2's fragment, `evidence-check .` reads DRIFTED on those rows and nothing BROKEN, and the CI `ledger` job warns and does not fail." Executed at ea43bac7: S4's renamed case reads BROKEN, exit 2 | The `Corrected · S4` row is written in phase 1 | `test.yml`'s `ledger` job: `if [ "$code" -ge 2 ]; then exit "$code"; fi`. A rename removes an anchor (`docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: "A released row whose anchor moved is not cleared by a re-read") |
| Which run the collection counts come from | `spec.md` Scope 1: "At 5623d728 (0.20.0 as shipped) macOS ran 12,730 passed and 89 skipped … run 37577753583's job logs". That run's head is 12d576b5 | The workflow comment cites run 37580460950, the one at 5623d728: macOS 12,731 + 88, ubuntu 12,739 + 80, Windows 12,819 across four shards | `gh run view <id> --json headSha` and each job's summary line, executed 2026-10-08. Both runs give 12,819 on every leg, so the argument stands |
| Which sentences name the Windows leg alone | `spec.md` Scope 5 enumerates `test.yml`'s two sentences and timeout comment, `run_tests.py`'s comment and `CONTRIBUTING.md` | Also the pip-line comment in `test.yml` and the `.test_durations` comment in `tests/test_the_release_check_watches_what_ships.py` | Both said only Windows is divided; contract §12 |
| The ledger fragment's file name | The spawn prompt: `seal/ledger/1791384162.md`. `spec.md` Scope 6: `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` | The full work item id | `docs/the-record-layout.md`: `seal/ledger/<work-item-id>.md`, and every earlier fragment carries the slug |

## Not verified

| Item | Who must answer |
|---|---|
| The three macOS shards' times, counts and sum against ubuntu's (`questions.md` Q1) | the CI run the orchestrator dispatches after phase 1; phase 2 reads it |
| The whole suite at the final head | the sealer |

## Not done

Phase 2's work: the measured budget, the scenario rows, the `Re-read ·` rows
and the changelog fragment.

## Fed back into the spec

none
