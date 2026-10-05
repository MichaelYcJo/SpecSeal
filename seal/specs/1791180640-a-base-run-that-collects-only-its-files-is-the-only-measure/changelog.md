### Fixed

- `broad-gate` no longer says `failing on base too` about a failing test the
  base passes (#789, #812, #807). That word is the one that lets a red suite
  through as somebody else's failure, and the gate gave it in three ways.
  It read the words off what pytest printed, so a test that runs pytest
  itself, as a suite that tests a pytest plugin does, could make the gate
  read an inner run's `FAILED` line as the real one, under `-s`, `-rN`,
  `-rP` or `-qq`. It asked every failing file of a row that runs pytest twice
  of whichever runner it reached first, often in the wrong directory. And a
  redesign that read pytest's JUnit report placed each failing test on a
  file by its names, and three fixes to that placement each left a layout
  where the word came back.

  Now `failing on base too` is given only where a run of the row at the base
  collected nothing but that one file, and only to a file that is the one
  failing file of its run. Such a file runs at the base on its own, with `--junitxml=<path>` appended, and the report is read for two
  counts only: its tests, and the ones that failed or errored. Where the
  base fails the file, the gate runs the whole row once more at the base with
  the file inserted after the part that measured it and
  `--collect-only -o verbosity_test_cases=-2 -vv` added to `PYTEST_ADDOPTS`.
  No test runs under collection alone, so nothing a test prints can get in
  the way, and a second runner the row starts later reads the same variable.
  The runner that measured is handed `-o verbosity_test_cases=-1` after the
  file, so it lists node ids no other runner prints. The word needs that run
  to show one pytest session, that runner's own, listing the file and
  nothing else, and no runner that ran tests anyway, which is what a runner
  started without the gate's environment does. Several failing files the
  base has at the repository root still run together first, but that run
  can only say `new`, where every test it collected passed. Otherwise every
  one of them reads `new?`, and none is measured on its own: a file's run
  alone is not the row's run, and the run of them together does not say
  which failed in it.

### Changed

- **More failing files read `new?` at the base, and that is on purpose.**
  `new?` sends a person to run the file at the base by hand; it never lets a
  red suite through. These rows now read `new?` for every file the base
  fails, where 0.18.2 often gave the right `failing on base too`:

  - a row whose runner also names a directory that collects more than the
    file, like `pytest -q tests/unit` with a failing file outside
    `tests/unit`, or `pytest -q tests` under pytest 9 (pytest 8.1 to 8.3
    collect only the handed file there, so that row earns the word);
  - a row whose pytest rootdir is not the directory it runs pytest in, like
    `cd sub && pytest` with the ini file at the repository root;
  - pytest older than 8.1, which does not know `verbosity_test_cases`;
  - a row that sets `PYTEST_ADDOPTS` itself, or runs at `-qqqq`;
  - a row that runs pytest more than once, a runner started without the
    gate's environment (`tox`, `env -i`, a container) included, wherever it
    stands in the row;
  - every failing file of a run of several that fails at the base, a
    pre-existing one included. A file's run alone is not the row's run: a
    sibling puts a module on `sys.path` or sets state at import, a session
    fixture's error lands on each session's last test, a flaky test fails in
    one run and not the other;
  - a row whose measuring runner sends its output to a file, so the only
    session the extra run shows is another runner's.

  A row earns the measured word back by letting the files the gate appends
  be pytest's only paths, for example `pytest -q` with `testpaths` in the
  ini file rather than `pytest -q tests`, and by running pytest once. This
  repository's own row, `bin/test -q` after the two `ruff` checks, already
  does.

- A part of the row that drops the gate's arguments, such as `sh -c '…'`, a
  `make` target or a runner given `-p no:junitxml`, now reads `new?` with the
  reason. It used to read `new` from a summary of tests it never ran.

- The `new?` reasons say what happened and name the file kept for it. A
  file that the base fails but that ran beside other files, or under a row
  that ran pytest twice, names its `collected-at-base-<n>.txt`, and a run
  that ended with an exit pytest does not give for passing tests names its
  exit and its `suite-at-base-<k>-<n>.txt`. A file of a run of several that
  failed names that run. `templates/config.md` rule 3 and
  `skills/verify/SKILL.md` say how each is read and what the extra runs
  cost.

- When the base fails a file, every part of the row after the part that
  measured it runs once more at the base under collection alone, including
  parts the branch's own run never reached. Their writes inside the scratch
  worktree go when it is removed; writes outside it stay.

Two limits are unchanged and named in rule 3. A second runner the extra run
cannot reach, or that prints nothing it can read (behind `||`, behind a part
that fails under collection alone, at `-qqqq`, or started without the gate's
environment at `-qq` or quieter), leaves the row read as having one runner.
And in a row that runs pytest twice, a file the base passes under the first
runner reads `new` from that runner. Two routes never meet a group, as
before: a file that runs alone from the start (the one failing file the
root carries, or every failing file of a `cd sub` row) is compared with no
sibling, and a sibling the branch passes is never run at the base.
