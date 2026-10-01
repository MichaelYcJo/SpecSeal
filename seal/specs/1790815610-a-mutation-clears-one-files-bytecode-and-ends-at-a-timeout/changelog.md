### Added

- **`mutation-check`: one command runs one mutation of one unit.** It refuses
  a replacement that does not occur exactly once, runs the cases against the
  file as it is and stops with `no baseline` if they already fail (so a `-k`
  that selects nothing can never read as caught), writes the break, removes
  only that file's cached bytecode (every interpreter tag, wherever the file
  lives), runs the cases you name under a bound (300 s by default), restores
  the file from the bytes it held and compares the hash, and prints `red`,
  `SURVIVED` or a run that measured nothing, with exit 0, 1 or 2. On POSIX a
  timed-out run's whole process group is ended, so a wrapper's pytest does
  not outlive the verdict, and Ctrl-C ends it the same way before the
  restore. On Windows only the direct child is ended, and the verdict says
  so (#641, #129).

### Changed

- **`agents/smith.md` no longer says to clear `tests/__pycache__` between
  mutations.** That clear removed the test modules' bytecode, which is never
  stale, and missed the cache beside the mutated file, which is the one that
  made a same-length mutation read green. The smith now types
  `mutation-check` once per break, and `skills/verify/SKILL.md` says what
  each verdict means (#641, #129).

### Fixed

- **`arm-check`'s two bytecode cases hold under a mutation loop's own
  environment.** Both planted their cache by importing, and an import writes
  nothing under the `PYTHONDONTWRITEBYTECODE=1` that `arm-check` and
  `mutation-check` give the cases they run, so the two went red on their own
  setup whatever had been mutated (#641).
