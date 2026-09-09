<!-- specs/1788936260-a-case-pins-what-it-actually-measures -->

### Added

- **`arm-check` asks *would any case notice if this were wrong* of a whole
  module, one branch at a time.** A module's branches were counted by hand
  once, and #262's own table says 33 where
  `hooks/review-history-guard.py` now has 31 — the file changed twice after
  the count was taken. The new checker derives the list from the module's own
  syntax tree instead, makes each branch wrong, runs a command you name, and
  reports the branches nothing notices.

  **There are two ways to be wrong and the answers differ by a lot.**
  Inverting a test asks whether a case would notice it running backwards;
  removing the branch asks whether one would notice it not being there.
  Measured 2026-09-09 on `hooks/review-history-guard.py`, against
  `tests/test_chain_hooks.py`: **12 of 32 branches survive removal, and none
  of the 29 that inversion can be asked of survives it.** A branch counts
  watched when either is noticed. The report prints both rows, says which one
  #262's table of nine compares with — every sentence in that table is about
  taking something out, so a single merged number invites exactly the wrong
  comparison — and names every branch it asked one operator and not the
  other, which is why the two denominators differ: for a handler with one
  type left, inverting it and removing it are the same edit, so it is asked
  once.

  **The walk refuses a syntax it does not recognise instead of skipping it.**
  A checker whose own enumeration goes short prints a shorter count that still
  reads like a total, which is the defect it replaces one level up. So every
  one of this interpreter's 122 syntax-tree constructors is classified — a
  branch-carrying shape, or a non-branch with the grounds written beside it —
  and a Python release that adds one turns a test red rather than quietly
  narrowing the walk.

  **A branch nothing notices is not automatically a defect**, and the report
  says so where it prints them: a branch that cannot be reached, or one whose
  removal changes no behaviour, belongs in that list. It is report-only —
  exit 0 either way.

  **The wait for one command is bounded and the run survives a failed one.**
  `--timeout` defaults to 900 seconds and 0 removes the bound; a negative is
  refused. A command that does not return in time, and one that cannot be
  started at all, is recorded as a branch nothing measured rather than as a
  verdict — so a virtual environment that stops being buildable partway
  through costs one branch instead of the whole run. **It bounds the wait and
  not the work**: only the command's own process is killed, so a command that
  spawns something — a wrapper script running the suite one process down —
  leaves that running. Each branch asks two questions, so a branch can take
  twice the bound.

  **The total says which rule narrowed it.** `assert` and `for`/`else` are not
  counted, by #262's rule rather than because they hold no test, and the
  report names them where it prints the total. A run narrowed with `--only`
  says what it was narrowed out of, so a number pasted into a record does not
  read as the module's.

  Run it as `arm-check <module>` to list the branches, or with
  `--tests "<command>"` to get the verdict. `skills/verify/SKILL.md` §2
  carries the details.

### Fixed

- **A test that pinned a paragraph's wording let three rearrangements of its
  claim through.** `skills/verify/SKILL.md` explains why a command-time share
  can read above 100% — concurrent calls, ordinarily from batching rather than
  from a background command — and the test guarding that paragraph asserted
  four short phrases. Measured one edit at a time: swapping the two causes,
  inverting the measured direction, and putting the old wording back at the
  start of a sentence all **passed**. Each of the three is exactly the
  regression the test was written to stop.

  Every regression it was written against is a *rearrangement of true words*,
  and no substring assertion sees a rearrangement. The two load-bearing
  clauses are now asserted whole and the negative assertion is
  case-insensitive. Verified over five edits, one at a time, with the file
  restored and hash-compared after each: all five now fail, and the three
  above used to pass.

  **Where a paragraph carries a ranking (*this is the ordinary cause, that the
  rarer one*) or a direction (*it came from A and not from B*), the assertion
  has to carry the ranking or the direction.**
