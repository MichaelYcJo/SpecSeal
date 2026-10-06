### Changed

- **The Windows test leg runs in four shards, and a pull request no longer
  waits half an hour on it (#841).** The leg had grown from 7 minutes to
  37-40 minutes in two weeks. It ran 36 m 03 s and 33 m 36 s on the two runs
  of 2026-10-06 before the shards (runs 37457228586 and 37458654434), and
  its slowest shard took 10 m 03 s and 10 m 34 s on the two sharded runs
  (37465328899 and 37469595104).
  `pytest-split` divides the suite by each case's duration on Windows,
  stored in `.test_durations` at the repository root, and the four shards
  run the whole suite between them. macOS is now the longest leg, at 17 to
  21 minutes. ubuntu and macOS stay one job each.

- **A case whose call runs longer than 90 seconds now fails, under
  `bin/test` as in CI.** The report is one line,
  `<case> ran <seconds> s, over the 90 s ceiling (#841)`, followed by how
  to raise it on a busy machine, so a case that grows names itself instead
  of hiding in a leg's total. The ceiling is `CASE_CEILING_S` in
  `tests/conftest.py`, 1.5 times the slowest case measured on Windows. A
  case that meets it is made cheaper, split, or sampled. On a machine
  running other suites at the same time, `SPECSEAL_CASE_CEILING_S=<seconds>`
  raises it for one run; CI never sets it. Changing the 90 is a decision for
  the repository owner, and its comment says what it was set from.

  The ceiling reads a case's call only. Time a fixture spends in setup,
  where this change moved three shared builds, is not held to it; the
  `--durations` table and the leg's timeout are what see a fixture that
  grows.

- **Each `pytest` leg has a timeout**: 15 minutes on ubuntu, 35 on macOS and
  20 for each Windows shard, each 1.5 times the slowest run of that leg
  measured on 2026-10-06, rounded up to 5 minutes. GitHub fails a leg that
  runs past it.

- **Two things change for a contributor.** `pytest-split` 0.11.0 joins CI's
  install line (pinned as `PYTEST_SPLIT` in `.github/scripts/run_tests.py`);
  `bin/test` installs nothing new. `.test_durations` goes stale as cases are
  added, which unbalances the shards and drops no case: a case the file does
  not name still runs in exactly one shard. `CONTRIBUTING.md` §*Running the
  checks* says how to refresh it, and what to do with a case over the
  ceiling.
