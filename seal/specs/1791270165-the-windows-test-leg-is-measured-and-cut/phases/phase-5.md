# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | open: the budget is a600768e and its records 2794f613; `plan.md`'s Status takes the commit that records the confirming run |
| Ran by | smith on Opus 5.5 (a second smith, on another machine) |

## What this phase was asked

The budget, by `questions.md` Q6's rule (a): the per-case ceiling in
`tests/conftest.py` and the three `timeout-minutes` values, taking as the
base the slower of the runs measured (phase 3 found the runner swinging by
more than the rule's margin), with each constant's comment naming the run
ids it was set from, and saying what macOS's timeout is set from now that it
is the slowest leg. Every new case seen red. Q8's after-figure from the last
run. Then the closing records: `changelog.md`, one ledger row per scenario,
`overview.md` closed.

## What this phase found

### The base each value was set from

Q6 (a): the ceiling is 1.5 times the slowest call on the Windows leg after
phases 3 and 4, rounded up to 30 s; each `timeout-minutes` is 1.5 times the
leg's measured wall time after phases 3 and 4, rounded up to 5 minutes. The
runs after phase 4 are 37457228586 (922ded29), 37458654434 (8a69b393) and
37465328899 (98b817ad, sharded). The slowest of them is the base, because
phase 3 measured the same suite 1.19 times slower from one run to the next
and one shard 1.7 times slower than its siblings inside one run.

| Value | Base | Rule | Set |
|---|---|---|---|
| `CASE_CEILING_S` | 55.13 s, `test_no_shape_the_base_stops_reads_silent`, run 37457228586 (52.49 s in 37458654434, 29.91 s in 37465328899) | 82.7 s, up to 30 | 90 s |
| ubuntu `timeout-minutes` | 7 m 58 s, run 37458654434 (6 m 40 s, 5 m 40 s) | 11.95, up to 5 | 15 |
| macOS `timeout-minutes` | 19 m 52 s, run 37457228586 (16 m 27 s, 17 m 38 s) | 29.8, up to 5 | 30 |
| each Windows shard's `timeout-minutes` | 10 m 03 s, group 3 of run 37465328899, the only sharded run (the other groups 5 m 38 s to 6 m 22 s) | 15.1, up to 5 | 20 |

**macOS's 30 minutes is its own figure, not Windows'.** macOS is now the
longest leg and was never cut: the item's title names Windows, and
`spec.md` Out leaves macOS's time to the budget. Its base is its slowest job
of the three runs, 19 m 52 s, and 1.5 times that lands at 29.8, just under
the rounding. The margin is 1.51 times: a macOS run slower than the slowest
seen by half again fails.

**One value per ceiling, on every platform.** `spec.md` Data & interfaces
introduces no platform factor until a measured case needs one. The case
with the highest call on macOS and ubuntu in the last run is 18.76 s and
13.90 s, so the ceiling binds on Windows first.

**The ceiling also binds `bin/test`.** A case under 90 s on a CI runner can
pass that on a loaded laptop: on the second smith's machine, while other
sessions ran suites, one sealer case took 32.6 s that ran in 12 s on the
Windows leg. No case in the suite is near 90 s locally today, and the
ceiling's comment says what it was set from, so raising it is a visible
decision rather than a quiet one.

### What was built

- `tests/conftest.py`: `CASE_CEILING_S = 90` with its comment; `over_the_ceiling(nodeid, seconds)`, the sentence or None; and a `pytest_runtest_makereport` hook wrapper that turns a PASSING call over the ceiling into a failure whose whole report is that sentence. A call that failed on its own keeps its own report.
- `.github/workflows/test.yml`: a `timeout` on every matrix entry and `timeout-minutes: ${{ matrix.timeout }}` on the job, with the comment above the entries naming each base and run.
- `tests/test_a_slow_case_names_itself.py`, five cases: the sentence, pinned verbatim (§14); nothing at or under the ceiling; the constant; the hook driven through a real inner pytest run that loads this repository's `conftest.py` with the ceiling lowered to 0.3 s (a slow passing case fails with the sentence, a quick one passes, a slow failing one keeps its own failure); every leg has a timeout and the job reads it.
- `CONTRIBUTING.md` §*Running the checks*: what a case over the ceiling asks of a contributor, where the timeouts come from, and how to refresh `.test_durations`.

### Seen red, `executed` 2026-10-06

S7 itself: a `test_tmp_*` probe sleeping 91 s against the real, unpatched
ceiling, beside a quick case, run once and deleted (§7):
`tests/test_tmp_ceiling_probe.py::test_tmp_sleeps_past_the_ceiling ran 91.0 s, over the 90 s ceiling (#841)`,
`1 failed, 1 passed in 91.06s`.

Each through `bin/mutation-check` over the new module:

| Break | Verdict |
|---|---|
| `<=` made `<` in `over_the_ceiling` | `red` |
| the seconds printed with no decimal | `red` |
| the hook sets `passed` where it sets `failed` | `red` |
| the hook also rewrites a call that failed on its own | `red` |
| `CASE_CEILING_S = 120` | `red` |
| the job's `timeout-minutes` line removed | `red` |
| ubuntu's `timeout` removed | `red` |

GitHub failing a job past its `timeout-minutes` is GitHub's, and `read`.

### Q8: the leg after the work

The last run measured is 37465328899 at 98b817ad, before this phase's
budget: the slowest Windows shard took 10 m 03 s, against 37-40 minutes on
0.19.0's pull requests and 36 m 03 s and 33 m 36 s on this branch's two
runs before the shards. The longest leg a pull request waits on is now
macOS, at 17 m 38 s. Windows meets Q1's 12 minutes with two minutes to
spare. The orchestrator's push of this phase is the confirming
run; its figures belong beside these, and a shard over 12 minutes there is
the runner swing above, which the 20-minute timeout absorbs.

### The ledger

One row per scenario, S1, S2 and S4 to S9 (S3 withdrawn), appended to
`seal/ledger/1791270165-…md` with `@00000000` and stamped by `evidence-check
--reverify --ledger <the fragment> --checked 2026-10-06`. `evidence-check
--strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
