### Fixed

- `broad-gate` no longer calls a failing test `new` without running it at the
  base when the `Broad gate` row runs its tests from a subdirectory (#761).
  pytest names a failing file from the directory it runs in, and the gate
  looked for that path under the repository root. So with a row like
  `cd sub && pytest`, a test the base fails at `sub/tests/test_two.py` read
  `new` whenever the branch also had a different `tests/test_two.py` at the
  root. The same held for `make -C`, `env -C` and any runner script that
  changes directory.

  The root is now only where the gate looks for candidates. A failing file
  the base does not have at the root is run on its own at the base, through
  the row, from the directory the row runs in. If that run prints pytest's
  summary, the file gets the word the run measured. If it prints pytest's
  `no tests ran` line, or a count of warnings alone, with exit code 4 or 5,
  the base has no test in that file, and the file reads `new`. A run that
  collected nothing is never read as a summary, so a warning at the base no
  longer turns a file the base fails into `new`. This holds under `pytest-xdist` too, which
  prints no "file not found" message for a missing path. Any other output
  gives `new?`. Every other failing file is compared as before. Each run of a
  file on its own is kept as `suite-at-base-<k>-<n>.txt`.

  `templates/config.md` rule 3 states what this costs: one more run of the
  row's parts up to the runner for each such file, only when the broad gate
  fails. It also states three limits. A base file with no test in it reads
  `new`. A row whose subdirectory lacks a file that the base has under the
  same name at the root reads `new?`. And a row that runs pytest in two
  directories is asked about every file in the first runner's directory, so
  its words are the row's claim rather than a measurement.
