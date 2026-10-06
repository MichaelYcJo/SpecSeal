# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | open: the shards are 340dc6fa and 65c8ed98; the phase closes when the first sharded run's counts are read (S4) |
| Ran by | smith on Opus 5.5 (a second smith, on another machine) |

## What this phase was asked

Two halves, each a spawn of its own. The first: make the Windows leg write
`.test_durations` with `pytest-split`'s `--store-durations` and upload it as
an artifact, with `pytest-split` on the pip line and the pins of Q9 kept
green, and shard nothing. The second, once that push's run finished: download
the artifact from run 37458654434, read the Windows tables and counts of that
run and of run 37457228586 (the last run before the shards, S4), compute `K`
against Q1's default (the slowest shard at or under 12 minutes), and commit
the durations file and the Windows shard matrix, with every new or changed
case seen red. The sharded run on the pull request is the confirming
measurement, and the orchestrator starts it.

## What this phase found

### The two runs, `executed` 2026-10-06

Both are pull request #845's runs, both green on every job. Read with
`gh run view <id> --json jobs` and `gh run view --job <id> --log`.

| Run | SHA | What it is | Windows job | Windows pytest summary | ubuntu job | macOS job |
|---|---|---|---|---|---|---|
| 37457228586 | 922ded29 | the leg after 4b, the last run before the shards (S4) | 36 m 03 s | `12836 passed, 206 skipped in 2132.60s` | 6 m 40 s, `12961 passed, 81 skipped in 385.25s` | 19 m 52 s, `12954 passed, 88 skipped in 1166.87s` |
| 37458654434 | 8a69b393 | the same suite with `--store-durations` on Windows | 33 m 36 s | `12836 passed, 206 skipped in 1973.63s` | 7 m 58 s, `12963 passed, 79 skipped in 463.38s` | 16 m 27 s, `12955 passed, 87 skipped in 964.15s` |

**S4's baseline is 12,836 passed and 206 skipped**, 13,042 cases, on both
runs. The four shards' counts have to sum to that, less whatever a case
added since then (this phase adds three: the new module below).

**The Windows table, top lines of each run.** The same cases lead both, in
nearly the same order:

| Case | 37457228586 | 37458654434 | run 37429940700 (phase 1) |
|---|---|---|---|
| `test_no_shape_the_base_stops_reads_silent` | 55.13 s | 52.49 s | 36.44 s |
| `test_nothing_the_base_read_as_a_switch_goes_quiet` | 37.19 s | 36.24 s | 25.12 s |
| `test_the_guard_is_never_silent_where_the_writer_records` | 34.62 s | 31.73 s | 23.27 s |
| `test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item` | 29.86 s | 29.12 s | 17.14 s |
| `test_a_reason_the_checker_does_not_recognise_passes` | 28.18 s | 25.91 s | 20.36 s |
| the top 50, summed | 828.9 s | 758.5 s | 652.4 s |

### The runner varies more than 4b moved anything

The case at the top of the table did not change between be8a4115 and
922ded29, and it ran 36.4 s in phase 1's run and 55.1 s and 52.5 s in these
two. The leading cases are 1.4 to 1.7 times phase 1's figures across the
board, and the whole Windows leg took 1,791 s of pytest time then against
2,133 s and 1,974 s now. The ubuntu and macOS legs moved the same way (352 s
then, 385 s and 463 s now; 793 s then, 1,167 s and 964 s now). A slowdown
that uniform, on cases nobody edited, is the runner and not the suite.

**What this means for 4b.** Its effect on the Windows leg cannot be read
off these runs: whatever it saved is smaller than the swing between two runs
of the same day. `phases/phase-4.md` stated its bound from phase 1's table
(at most 2.7 minutes), and that stands as the only figure.

**Whether the two runs' overlap coloured them.** They overlapped from 11:46
to 12:09 UTC. Each GitHub-hosted job runs on a fresh virtual machine of its
own (`read`, from GitHub's documentation of hosted runners), so our two runs
did not share a machine. That they agree with each other within 8% and both
sit well above phase 1's run points the same way: the variation is between
runner hosts or times, and the overlap is not its cause. Nothing here can
rule out a slower host pool at that hour.

**What it means for phase 5.** Q6's rule sets the budget at 1.5 times the
measured figure. The same code just measured 1.19 times slower from one run
to the next on Windows (2,133 s against 1,791 s), and per case up to 1.7
times. A budget at 1.5 times one run's figure would sit at the edge of that
swing; phase 5 should take the slower of several runs as its base, and this
phase's two runs are two of them.

### `K`, from the durations file

The artifact `test-durations-windows-latest` of run 37458654434 holds
13,042 cases summing to 7,530 s of setup, call and teardown. The leg ran
that in 1,973.63 s of pytest time, 1.05 times 7,530 / 4: four xdist workers
(`read`: GitHub gives a hosted `windows-latest` four cores, and the log names
`[gw2]`) kept almost fully busy. Around pytest, the job spent 37 s on
checkout, Python and the pip install, and about 25 s more from the step's
start to the first case.

`pytest-split`'s default algorithm, `duration_based_chunks`, divides the · NAME NOT IN TREE
cases in collection order, so a module stays in one shard and its session
fixtures, 4b's templates among them, are built once there. Run offline over
this file (`executed`, the algorithm imported from the 0.11.0 wheel), it
gives groups within 0.2% of each other:

| `K` | worker-seconds per group | a shard's job, on run 37458654434's pace | on run 37457228586's pace (1.08 times slower) |
|---|---|---|---|
| 3 | 2,508 to 2,513 | 37 + 25 + 1,949 / 3 = 712 s, 11.9 min | 765 s, 12.8 min |
| 4 | 1,881 to 1,884 | 37 + 25 + 1,949 / 4 = 549 s, 9.2 min | 589 s, 9.8 min |
| 5 | 1,498 to 1,510 | 452 s, 7.5 min | 484 s, 8.1 min |

**`K` is 4.** Three meets Q1's 12 minutes on the faster run only, and by
seconds; four meets it on both with two minutes to spare, which is the
smallest count that does. Five buys another 1.7 minutes for one more
runner's 62 s of fixed cost. The slowest single case, 52.5 s, is far under
any shard.

### What was built

- `.github/workflows/test.yml`: four Windows entries carrying
  `split: "--splits 4 --group <g>"`, the pytest line ending in
  `${{ matrix.split }}`, empty on ubuntu and macOS, which stay one job
  each. The first half's `store` entry and its upload step are gone: the
  file they produced is committed, and storing it again is a one-run change
  of the same two lines (below).
- `.test_durations` at the repository root, the artifact as downloaded, with
  its CRLF line ends made LF (`.gitattributes` says `eol=lf`) and nothing
  else changed: 13,042 entries, ASCII, no user path but `/Users/x/`.
- `CONTRIBUTING.md` §*Running the checks*: the CI sentence counts the shards.
- `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`, three
  cases: every Windows entry is a shard of one count `K`, its groups are 1 to
  `K` exactly once, no other leg carries a split; the pytest line ends in the
  split; the durations file parses and names `tests/…::…` cases with
  non-negative seconds.
- `tests/test_the_release_check_watches_what_ships.py`: `.test_durations`
  classified as staying home. The case went red on the new top-level entry in
  the narrow run before this line was added, which is its red.

**Refreshing the file.** It goes stale as cases are added. A stale file
unbalances the shards and drops nothing: a case it does not name is given
the average and runs in one shard. To refresh, one run of the Windows leg
unsharded with `--store-durations` and the upload step of 43326715, then the
file is downloaded and committed. Phase 5's per-case ceiling and the shards'
own `--durations` tables say when it is due.

### Seen red, `executed` 2026-10-06

Each through `bin/mutation-check` over the new module:

| Break | Verdict |
|---|---|
| group 4 named as group 3 | `red`: the groups case |
| one entry saying `--splits 5` | `red`: the groups case |
| ubuntu given a split | `red`: the groups case |
| `${{ matrix.split }}` dropped from the pytest line | `red`: the line case |
| a node id in the file without `tests/` and `::` | `red`: the file case |
| the file's opening `{` made `[` | `red`: the file case |

The first half's extension of `test_ci_installs_the_parser_the_runner_pins`
was seen red the same way, three times: the pip line's version changed to
0.10.0, `pytest-split` dropped from the line, and `PYTEST_SPLIT` put into
`PACKAGES`.

**Narrow runs.** Every module that reads `.github/workflows/`,
`run_tests.py`, `CONTRIBUTING.md` or the tracked tree (60 modules):
`1 failed, 4117 passed, 8 skipped`, the one being the classification above;
after it, that module and the new one: `40 passed`. Exit codes read
directly. `ruff check` and `ruff format --check` exit 0 on every Python file
touched.

### What the confirming run must show (S4)

The sharded run's four Windows jobs: each one's `passed` and `skipped`,
summing to 12,836 and 206 plus the three new cases; each job's wall time,
the slowest at or under 12 minutes; and each shard's `--durations=50`
table, which phase 5 reads for its ceiling. If a shard collects a different
suite from the others, xdist and `pytest-split` will say so at collection.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The one unsharded Windows job | the four shard entries of the same matrix |
| The first half's `store` entry and its upload step (43326715) | `.test_durations`, committed; the refresh above names the two lines to put back for one run |
