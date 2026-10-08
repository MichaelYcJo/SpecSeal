### Added

- **A ledger row may name the test that holds its claim, and such a row never
  drifts (#836).** A row's Code grounds cell can name tests as pytest spells
  them — `tests/test_x.py::test_y`, or `tests/test_x.py::TestA::test_b` for a
  method — in place of `path#anchor@hash`. A hashed row records what the code
  held when somebody read it, so every edit to that code owed a re-read; most
  rows written since 0.18.0 were those re-reads. A test row has no hash:
  `evidence-check` reads that each test is there, and the suite reads that it
  passes. It is `OK` for what reads as a test without running pytest — a
  `test…` function or `Test…` class in a `test_*.py` or `*_test.py` file, no
  `__init__` on its class — under no unconditional `skip` or `xfail` mark;
  whether pytest collects it under your configuration, and whether it
  passes, stay the suite's answers. It is `BROKEN` for a test or file that is
  gone (a method written bare is told its spelling), and `MALFORMED` for a
  unit that is not a test, a test that cannot fail, or a row that mixes a
  test with a code coordinate; a coordinate whose quoted locator holds `::`
  stays a coordinate. `--reverify` writes nothing on it. A released row
  moves onto its test by one `Corrected ·` row naming the test, written by
  the branch whose edit drifted it, and a released test row whose test was
  renamed is re-pointed the same way; `--into` names that option once when it
  writes a `Re-read ·` row, and so does the commit advisor's repair line
  under a frozen ledger. A repository that vendors the checker through
  `evidence-ci` updates its copy before writing a test row: an older copy
  reads one as `MALFORMED`.

### Changed

- **`fold-check` reads an `Enforced by:` target with the ledger's resolver
  (#836).** A method is now written `path::Class::method`, as pytest and a
  test row spell it, and a name is found where it is defined rather than
  anywhere in the file. Every target in this repository's `docs/` resolves as
  before.
