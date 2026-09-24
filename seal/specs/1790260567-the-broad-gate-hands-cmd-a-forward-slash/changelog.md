- **The broad gate hands `cmd.exe` a command name it can run (issue #448).**
  On Windows the gate's shell is `cmd.exe`, which reads a `/` inside a
  command name as the start of a switch. The row `bin/test -q` therefore ran
  a command called `bin`, and a suite that never started was reported as a
  suite that failed. Where the shell is `cmd.exe`, the gate now writes `/`
  as `\` inside each command name and nowhere else, so `bin/test` runs as
  `bin\test` and reaches `bin/test.cmd`. Arguments, quoted paths, `%VAR%`,
  operators and escaped characters reach the shell as written, and every
  other shell gets the row unchanged. When the two differ, the gate prints
  one line saying what `cmd.exe` was handed, and the check's kept output
  carries it under the row as written. `templates/config.md` §*Broad gate*
  names the positions that are rewritten and the two that are not.
- **A failing suite whose output holds no pytest summary says so (issue
  #448).** The failure form now adds one line where the `suite` check failed
  without printing a summary: its exit code is not a count of failing tests,
  and the row may have stopped before any test ran. `cmd.exe` exits 1 for a
  command it cannot find, which is pytest's own 1, so the line reads the
  missing summary rather than the exit code. The exit code is unchanged.
- **This repository's suite runs with `gh` logged out, on every machine
  (issue #510).** A case that fell through its stubs onto a live `gh` passed
  wherever `gh` was logged in, which included the broad gate, and failed only
  on CI, whose pytest job has no token. `tests/conftest.py` now points
  `GH_CONFIG_DIR` at an empty directory and removes the four token variables
  when it is imported, so a local run gives CI's answer.
  `CONTRIBUTING.md` §*Running the checks* says so.
