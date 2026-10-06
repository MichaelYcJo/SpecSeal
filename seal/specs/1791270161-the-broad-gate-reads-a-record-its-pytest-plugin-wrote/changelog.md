### Changed

- **`broad-gate` compares a failing test with the base from a record its
  own pytest wrote, not from what pytest printed** (#825). Four designs in a
  row guessed which pytest run, in which directory, printed each failing
  line, and every fix moved the guess one level up. Now the gate loads a
  small pytest plugin of its own, the recorder, into every run it measures:
  it puts the recorder's directory first on `PYTHONPATH`, adds
  `-p specseal_pytest_record` to `PYTEST_ADDOPTS`, and hands the run a key
  made fresh for it. The pytest process that collects a test writes that
  test's outcome down, under the module that collected it. A pytest a test
  starts, and an xdist worker, inherit no key and write nothing, so nothing
  a test prints or runs can change a word.

  On a failing suite the failing files come from that record. Then the row
  runs once more, unchanged, at the base: nothing is appended to it and no
  part of it is cut. Each failing file reads:

  - `failing on base too` where the base's run fails a test of that file, or
    cannot collect it;
  - `new` where the base's run collects the file and passes it, or runs to
    exit 0 without collecting it;
  - `new?` where no pytest at the base left a record, because the row
    ended there before it started one, none loaded the recorder, or the one
    that did could not write its record; or where the base's row exited
    non-zero before any of its pytest sessions collected the file. The last
    is also how a file the branch added reads on a base whose row already
    fails.

  Where no pytest of the row left a record at all, the `FAILED` lines name
  the files, each reads `new?`, and the base is not run. The reason printed
  beside each such file names every cause the gate cannot tell apart: the
  row started no pytest, none it started loaded the recorder, or the one
  that did could not write its record. The kept output holds
  `suite-at-base.txt` and the records under `records/`.

- **Rows 0.18.3 refused to measure now get a measured word.** A row that runs
  pytest twice, a runner inside `sh -c '…'`, a runner given
  `-p no:junitxml`, a runner whose output goes to a file, and several
  failing files at once each read `failing on base too` or `new` from the
  base's own run, where 0.18.3 gave `new?` (#807). A file the base fails
  only when it runs alone reads the outcome the row itself gives it. No
  proof run exists any more, so a later runner that sets
  `-o verbosity_test_cases=-1` itself can no longer lend a file a word the
  base did not give it (#816).

- **A cost moved.** A failing suite costs one more run of the whole row at
  the base, whatever the number of failing files, in place of a run per
  prefix and per file. For this repository's own suite each run's record is
  about 14 MB under the kept output.

- **A row that keeps `PYTEST_ADDOPTS` and loses `PYTHONPATH` now fails at
  the gate.** Such a row keeps the gate's `-p` but drops the directory it
  names, and pytest exits 1 on the import before any test runs. That is a
  row that replaces the variable (`PYTHONPATH=src pytest`), an interpreter
  run with `-I` or `-E`, or a wrapper that passes `PYTEST_ADDOPTS` or
  `PYTEST_*` on and not `PYTHONPATH`. Add to the variable instead,
  `PYTHONPATH=src:$PYTHONPATH`, and pass it on wherever `PYTEST_ADDOPTS`
  goes. A row that replaces `PYTEST_ADDOPTS`, or starts pytest through
  `tox`, `nox`, `env -i`, a container or a wrapper that rebuilds the
  environment without either variable, loses only the recorder, and its
  files read `new?`.

- **Each failing file is named by the path pytest holds for it.** The
  recorder reads a test's own path where pytest holds the test, in an xdist
  worker too, and carries it on the report to the process that writes the
  record. A file outside the rootdir, a `--pyargs` module installed outside
  the repository, and a collector a conftest builds for files elsewhere are
  each named by their own path and get a measured word, where a name pytest
  made from the path could give two files one name. A test with no file of
  its own, which a conftest or a plugin attaches to the session or to a
  directory, a failed collection of the whole session, which is where
  pytest 7 reports a conftest's import error, and a report a plugin rebuilt
  without the path are left out of every list and counted on the record's
  `end` line, and the gate says how many under the failing files. A test
  whose xdist worker crashed keeps the path its earlier reports carried, so
  its failure counts. The path travels as a report attribute, so a row that
  writes `--report-log` finds it in that log while the gate measures it.

### Fixed

- A failing file of a `cd sub` row is named from the repository root,
  `sub/tests/test_x.py`, so a root file of the same name never shares its
  word.
- A failing file whose path holds a space is named and compared (#813).
- The listed path is spelled with `/` on Windows too (#818).

`templates/config.md` rule 3 is rewritten whole and now gives a row's author
the five cases, the cost, how a row earns the measured word, and the one
limit named rather than closed: a test written against the gate's own key or
record file.
