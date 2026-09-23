### Changed

- A `git commit` in an opted-in repository with a large ledger no longer
  waits on the evidence advisor for about fifteen seconds. The checker used
  to parse a Python file once for every ledger row that cited it; it now
  parses each file once per run, keyed on the file's content so an edited
  file is never read from a stale answer. On this repository's ledger the
  advisor went from about 15.3 s to about 1.7 s per commit, and
  `evidence-check --strict .` from about 16.3 s to about 2.0 s. Every
  finding the checker prints is unchanged. The advisor's own description of
  what it costs said "about 114 ms" with no date; it now states the measured
  cost, how it was measured, and when. No ledger row was removed: every
  anchor still resolves, and what the ledger's size cost was the parsing,
  not the rows.
  (`1790154760-the-ledger-grows-and-nothing-takes-a-row-out`, #519)
