# 1791384162-the-macos-test-leg-runs-in-shards — overview

<!-- Opened in phase 1 at the first divergence; closed in phase 2. -->

## Why this work exists

The macOS leg was the job every run waited on at 15 to 21 minutes. Three
shards took it to 6 m 56 s at the slowest in run 37700567455, and the suite
now reads the matrix in one place.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| When 0.20.0's S4 is corrected | `plan.md` §*The ledger*: "Between phase 1's commit and phase 2's fragment, `evidence-check .` reads DRIFTED on those rows and nothing BROKEN, and the CI `ledger` job warns and does not fail." Executed at ea43bac7: S4's renamed case reads BROKEN, exit 2 | The `Corrected · S4` row is written in phase 1 | `test.yml`'s `ledger` job: `if [ "$code" -ge 2 ]; then exit "$code"; fi`. A rename removes an anchor (`docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: "A released row whose anchor moved is not cleared by a re-read") |
| Which run the collection counts come from | `spec.md` Scope 1: "At 5623d728 (0.20.0 as shipped) macOS ran 12,730 passed and 89 skipped … run 37577753583's job logs". That run's head is 12d576b5 | The workflow comment cites run 37580460950, the one at 5623d728: macOS 12,731 + 88, ubuntu 12,739 + 80, Windows 12,819 across four shards | `gh run view <id> --json headSha` and each job's summary line, executed 2026-10-08. Both runs give 12,819 on every leg, so the argument stands |
| Which sentences name the Windows leg alone | `spec.md` Scope 5 enumerates `test.yml`'s two sentences and timeout comment, `run_tests.py`'s comment and `CONTRIBUTING.md` | Also the pip-line comment in `test.yml` and the `.test_durations` comment in `tests/test_the_release_check_watches_what_ships.py` | Both said only Windows is divided; contract §12 |
| How 0.20.0's S8 is answered | `spec.md` Scope 6 and `plan.md` phase 2: "the `Re-read ·` rows for 0.20.0's S1, S2 and S8 written by `evidence-check --reverify --into`". S8's claim says "macOS 35" | A `Corrected · S8` row, written before the re-read run so the run writes none for S8 | A re-read asserts the cited claim holds, and with three shards at 15 it does not (`docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*) |
| Which released rows are re-read | `plan.md` §*The ledger*: S1, S2 and S8 drift | Five `Re-read ·` rows: 0.8.2 R3, 0.16.0 P1-1, 0.18.0 R3, 0.20.0 S1 and S2 | The floor and pins cases moved onto `matrix_include_entries` and `jobs`, and older rows cite them; each claim read before `--checked` was written |
| The ledger fragment's file name | The spawn prompt: `seal/ledger/1791384162.md`. `spec.md` Scope 6: `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md` | The full work item id | `docs/the-record-layout.md`: `seal/ledger/<work-item-id>.md`, and every earlier fragment carries the slug |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ The three macOS shards' times, counts and sum against ubuntu's (`questions.md` Q1) | run 37700567455 at 3a946dd0, read by phase 2 on 2026-10-08: 5 m 22 s, 6 m 24 s, 6 m 56 s; 12,827 cases, ubuntu's count (`phases/phase-2.md`) |
| That GitHub reads each macOS shard's `timeout` of 15 | the pull request's run at the final SHA |
| The whole suite at the final head | the sealer |

## Not done

- **`.test_durations` is not refreshed.** It is stale: 504 collected cases
  are missing from it, and 727 of its entries name cases that no longer
  exist. The refresh is a dedicated Windows run the owner starts by
  `CONTRIBUTING.md`'s recipe (#874).
- **The heading-unit cut in `evidence-check` is not fixed.** A `#` line
  inside a fence ends a markdown section, so
  `CONTRIBUTING.md#"## Running the checks"` does not cover the lines after
  its fenced `# or:` line (`phases/phase-2.md`). This is the tool's defect,
  outside this work's scope, and it is named for the orchestrator to file.

## Fed back into the spec

none
