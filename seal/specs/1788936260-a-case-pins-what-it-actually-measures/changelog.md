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
  removing the branch asks whether one would notice it not being there. On
  `hooks/review-history-guard.py`, against `tests/test_chain_hooks.py`:
  **1 of 32 branches survives inversion and 12 survive removal.** A branch
  counts watched when either is noticed. The report prints both rows and says
  which one #262's table of nine compares with, because every sentence in that
  table is about taking something out — a single merged number invites exactly
  the wrong comparison.

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
