### Fixed

- `broad-gate` no longer gives a failing file `failing on base too`, or `new`,
  because of something a test printed at the base (#789). The comparison at
  the base read its words off the text pytest printed, and that text can hold
  a second pytest run: a test that runs pytest itself and writes the output
  to stdout or stderr under `-s` or `--capture=sys`, or prints it in captured
  output on a run where pytest wrote no `short test summary info` rule of its
  own (`-rN`, or `-rP` with nothing failing), or no summary line at all
  (`-qq`). The inner run's `FAILED` line was then read as the run's own. A
  file the base passes could read `failing on base too`, and one the base
  fails could read `new`.

  Every run at the base now appends `--junitxml=<path>` after the files, and
  the words come from that JUnit report. Only the pytest process the gate
  handed its arguments to writes it, so nothing a test prints reaches it,
  and the reporting flags no longer matter: rows with `-qq` are measured now,
  where they used to read `new?`. Each report is kept as the `.xml` beside the
  run's `suite-at-base-*.txt`.

  A file reads `failing on base too` only where the report places a failing
  or erroring test on that file and no other, by the test's own path. The
  gate appends `-o junit_family=xunit1`, which makes pytest write each
  test's file as a path, and reads that path against the files in the
  base's worktree after the run, tracked, written by the run or ignored, so
  a package, a class or a deeper module named like the file is never taken
  for it, and a test file the row generates is found. Where a same-named
  file the path could also name sits under another rootdir or another
  directory the row could run pytest in, the file reads `new?`. That path is
  where a test's function is defined, so a test a class inherits from
  another module, and every test of a row under `--junit-prefix`, is known
  only by its dotted name. Such a test gives no measured word: a file a
  failing one could be reads `new?`, including a file that fails at the base
  through a test it inherits. A file reads `new` only where the report
  places that file's tests by their path and none failed. Anything else
  reads `new?` with a reason: a failing test that could be this file or
  another one or is known only by its dotted name, a second directory of the
  base that fits the run, or a file the report places no test on
  (`pytest's report at the base does not place a test on this file alone`);
  and a run that is not of one new file alone whose report counts
  no test (`pytest's report at the base counts no test`), which says the
  file is missing or holds no test there, and used to read the `no part of
  the row printed a line…` reason. That reason is reworded to `no part of
  the row wrote the report the gate asked pytest for`.

- A part of the `Broad gate` row that does not pass the gate's arguments on
  to pytest now reads `new?` where it read `new`, where no other part of the
  row runs pytest (#789). That covers a `sh -c '…'`, a `make` target, a
  wrapper that drops its arguments or refuses an option it does not know,
  and a runner given `-p no:junitxml`. Such a part used to print pytest's
  summary over something else, and every file read `new` for a run that
  never ran it. Where another part of the row does run pytest, see the next
  entry. Write such a part so it passes its arguments on, `--junitxml` and
  `-o junit_family=…` included: a wrapper that forwards only the options it
  knows reads `new?`.

- A `Broad gate` row that runs pytest in more than one part, such as
  `pytest -q && cd sub && pytest -q`, now reads `new?` for every failing file
  (#789). Each file used to be asked of the first runner the row reached, in
  the first runner's directory, so a file a later runner named could read
  `new` where the base fails it, or `failing on base too` where the base never
  ran it. To find a second runner, every other prefix of the row runs once
  more at the base with `--collect-only` added to `PYTEST_ADDOPTS`, kept as
  `runners-at-base-<j>.txt`. A prefix before the measured runner gets the
  report's path through `PYTEST_ADDOPTS`, so a runner there that dropped the
  appended arguments is counted too. Only pytest honours `--collect-only`:
  each part of those prefixes that is not pytest runs as written at the
  base, once for each prefix that holds it, including a part after the
  runner that the branch's own run never reached because its suite failed
  first. This happens once per failing gate. A row whose only part runs
  pytest pays nothing; this repository's own row runs its two `uvx ruff`
  prefixes once more. Not counted, and named in `templates/config.md` rule
  3: a runner behind a part that fails at the base under collection alone,
  or behind `||`, a runner given `-p no:junitxml`, a runner whose own
  command line names `--junitxml`, one started without `PYTEST_ADDOPTS`, and
  a later runner inside a part that drops its arguments (#807). In such a
  row, where the base tracks every failing file of a run under both
  runners' directories, each reads `new?`. Where it tracks any one of them
  under the measured runner's directory only, every file of that run is
  measured there, and can read `new` or `failing on base too` from the
  wrong runner.
