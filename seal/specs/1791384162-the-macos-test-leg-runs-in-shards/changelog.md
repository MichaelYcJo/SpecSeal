### Changed

- **The macOS test leg runs in three shards, and a pull request no longer
  waits on it (#864).** macOS was the leg every run waited on: one job of
  15 m 25 s to 20 m 52 s on the runs of 2026-10-06 and 2026-10-07 (the
  slowest, run 37469595104). On the first sharded run, 37700567455 of
  2026-10-08, its three shards took 5 m 22 s, 6 m 24 s and 6 m 56 s, and
  between them ran 12,827 cases, ubuntu's count at the same commit. The
  Windows shards are now the longest jobs of a run. Each macOS shard's
  timeout is 15 minutes, 1.5 times the slowest shard rounded up to 5, where
  the single job had 35. A run starts three macOS jobs where it started one.
  ubuntu stays one job.

  The shards are divided by the same `.test_durations` as the Windows
  shards, because every leg collects the same cases; only each case's time
  differs by system, and that is read off each leg's own jobs.

- **What changes for a contributor.** Refreshing `.test_durations` still
  means one dispatched run with the Windows leg as a single job; the three
  macOS shard entries stay as they are on that branch (`CONTRIBUTING.md`
  §*Running the checks*). A matrix entry in `test.yml` written other than as
  a one-line `- { … }` mapping now fails the suite with its line, because
  the suite reads the matrix in one place and refuses a shape it does not
  read rather than skipping it.
