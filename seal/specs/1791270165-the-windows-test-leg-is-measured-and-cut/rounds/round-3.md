# 1791270165-the-windows-test-leg-is-measured-and-cut — review round 3

| Field | Value |
|---|---|
| Target SHA | 3468d368eebfd6d50bb59492d8cee745128e115c |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #845 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `8fa8b07051e8c45c0b82191dad31a5262106cdb9..8fa8b07051e8c45c0b82191dad31a5262106cdb9`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1 (the refresh recipe's upload step needs `if: always() && matrix.store != ''`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the verifying round for round 2's fixes at `458ae587..ae88b626`, which had recorded the run's first fix of a fix, and the last round of the run. The reviewer was asked to open both 🟡 fixes and judge whether each closes its class, inheriting rounds 1 and 2, then the rest of `a9d7b0e5..3468d368`, reading every workflow's checks for the pushed HEAD, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the three changed test files, `bin/survivor-check --range a9d7b0e5...HEAD --exempt <item>/survivors.md` (exit 0) and four modules (125 passed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The refresh recipe's upload step carries no `if: always() && matrix.store != ''`: the shard cases fail on the refresh branch by construction, so the step is skipped and no file is uploaded, and with `always()` alone ubuntu uploads the stale committed file first | `CONTRIBUTING.md:194` | deferred #847 | #847 — the run is capped; fixed on this branch after the rounds, before the seal; executed: the recipe applied in a clone, two shard cases red; a probe showed `pytest-split` writes the file on a red session; the name conflict is read from the action's documented behaviour |
| 🟢 | round 2's finding 1 is closed at both instances — no commit named, and the unsharded entry's timeout of 55 | `CONTRIBUTING.md:191` | confirmed | read; 1.5 times 33 m 36 s is 50.4, rounded up to 55; the class is open as 🟡 1 |
| 🟢 | round 2's finding 2 is closed with its class — the variable's empty, decimal, zero, negative, word and nan values | `tests/conftest.py#ceiling_from` | confirmed | executed: fresh imports with eight values beside the cases' own, a pytest run under `abc`, and the empty-value case red with the old line put back |
| 🟢 | round 2's ⬜ 3 is closed — the three templates say per worker | `tests/test_a_fix_of_a_fix_is_counted.py#_stopped_untouched` | confirmed | read; every session or module fixture the branch adds was checked |
| 🟢 | round 2's ⬜ 4 is closed — the ledger's S7 claim is split and anchored | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md:19` | confirmed | executed: `bin/evidence-check --strict .` exit 0 |
| carried | round 1's verdicts and round 2's carried confirmations | `tests/conftest.py`, `.github/workflows/test.yml`, `tests/test_a_fix_of_a_fix_is_counted.py` | confirmed | carried from round 2; the fix range touched none of their code but what this table answers above |

## Paste-ready fixes

```markdown
`.test_durations` goes stale as cases are added, which unbalances the
Windows shards and drops no case. To refresh it, push a branch on which
`test.yml` runs the Windows leg as one job again for a single run: one
Windows entry with `store: "--store-durations"` in place of the four shard
entries, with a `timeout` for the whole leg rather than a shard's 20 (it
ran 34 minutes unsharded when the file was first made, so 55 by the rule
beside the values); `${{ matrix.store }}` on the pytest line; and an
`actions/upload-artifact@v4` step with `if: always() && matrix.store != ''`,
`path: .test_durations` and `include-hidden-files: true` (the name starts
with a dot, which the action skips by default). Both halves of the
condition are needed. On that branch the shard cases in
`tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py` fail,
because the matrix has no shards, so without `always()` the upload is
skipped although the file was written. Without `matrix.store != ''`,
ubuntu and macOS upload the committed file under the same name first.
Download the artifact with `gh run download <run> -n <artifact>`, make its
line ends LF, commit it, and restore the shards.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_slow_case_names_itself.py tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py -q` in a `--no-local` clone at `3468d368` | `11 passed`, exit 0 |
| `bin/evidence-check --strict .` in the clone | exit 0 |
| `bin/survivor-check --range 458ae587..HEAD` in the clone | exit 0, no removed wording standing |
| a fresh import of `tests/conftest.py` under `SPECSEAL_CASE_CEILING_S` set to `inf`, `nan`, `1e3`, `" 120 "`, a thousand written with an underscore, three Arabic-Indic digits, `0.0001`, `abc` | `inf`; ValueError; `1000`; `120`; `1000`; `300`; `0.0001`; ValueError, each naming the variable |
| `pytest tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py` with the variable set to `abc` | exit 4, ImportError while loading conftest, the `E` line is the sentence naming the variable |
| the clone's `test.yml` edited as the recipe words it, and the conftest line put back to `int()`; the shard module, the timeout case and the two new variable cases run; both files restored | 3 failed, 3 passed: the two shard cases and the empty-value case red; the timeout case and the zero-or-less case green |
| `pytest-split` 0.11.0 under `-n 2` with `--store-durations` over one passing and one failing case, in a scratch directory, deleted | exit 1, and the durations file held both cases |
| `gh run view 37458654434` and its artifacts | every job `success`; artifact `test-durations-windows-latest`, which the shard module did not yet exist to fail |
| `gh pr checks 845` and `gh run view` on runs 37482442997 and 37482443016 at `3468d368` | every check `pass`; the Windows shards total 12,848 passed and 206 skipped, 13,054 as on ubuntu and macOS; slowest shard 10 m 27 s |
| the full suite (the broad gate) | not yet run, by anyone; it is the sealer's, once, after the rounds |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2797` | round 1's 🔴 1 — fixed |
| round-1 | `tests/conftest.py:842` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_a_fix_of_a_fix_is_counted.py:511` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_a_slow_case_names_itself.py:40` | round 1's ⬜ 4 — fixed |
| round-1 | `.github/workflows/test.yml:105` | round 1's ⬜ 5 — fixed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:970` | round 1's ⬜ 6 — fixed |
| round-1 | `CONTRIBUTING.md:184` | round 1's ⬜ 7 — fixed |
| round-1 | `tests/conftest.py:860` | round 1's ⬜ 8 — answered |
| round-1 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/phases/phase-5.md:51` | round 1's ⬜ 9 — fixed |
| round-1 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/overview.md:24` | round 1's ⬜ 10 — fixed |
| round-1 | `tests/conftest.py:842`, `.github/workflows/test.yml:61` | round 1's 🟢 — confirmed |
| round-1 | `.github/workflows/test.yml:75` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py#_sample`, `tests/test_the_seal_is_taken_once_by_the_sealer.py#a_sealed_run` | round 1's 🟢 — confirmed |
| round-1 | `tests/conftest.py:854` | round 1's 🟢 — confirmed |
| round-2 | `CONTRIBUTING.md:194` | round 2's 🟡 1 — fixed |
| round-2 | `tests/conftest.py:851` | round 2's 🟡 2 — fixed |
| round-2 | `tests/test_a_fix_of_a_fix_is_counted.py:500` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md:19` | round 2's ⬜ 4 — fixed |
| round-2 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_fix_of_a_fix_is_counted.py#a_stopped_run` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_slow_case_names_itself.py:45`, `.github/workflows/test.yml:105`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:970`, `phases/phase-5.md:52`, `overview.md:24` | round 2's 🟢 — confirmed |
| round-2 | `CONTRIBUTING.md:193` | round 2's 🟢 — confirmed |
| round-2 | `CONTRIBUTING.md:182` | round 2's 🟢 — confirmed |
| round-2 | `tests/conftest.py`, `.github/workflows/test.yml` | round 2's carried — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The 4b cuts' yield, with the two figures round 2 recorded | `overview.md` Not verified; already deferred in round 1 and carried by round 2 | the repository owner, if the figure is wanted |
