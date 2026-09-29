### Changed

- **A repository's build can go red at this upgrade** (#508). `evidence-check`
  now reads `seal/follow-up.md` on every run, and a name written as
  `path#name` in a live work item's records or in that file. A stale
  backticked name there, or a `path#name` whose file does not carry the name,
  is `NOT-IN-TREE`: exit 2 in every reader, the lenient `ledger` CI job and
  `--strict` in `broad-gate` alike. The repair is to correct the line, or to
  write `NAME NOT IN TREE` on it where the name is meant to be absent.

### Added

- `evidence-check` reads `seal/follow-up.md` (#508). Its rows name units for
  a person to act on months later, and nothing read them: a row once named a
  case in no file and was found by grepping. The file is read whether or not
  a work item is live, by the same rules a record is read by, and it is left
  out of the name corpus, so the row naming a name is not that name's
  evidence. A refusal names every place the corpus leaves out, and the
  records summary line ends by saying whether the file was read, absent, or
  unreadable.
- `evidence-check` checks a name written as `path#name`, `path#name()` or
  `path#Class.method` (#508). Where the path resolves to a file, every part
  of the name has to appear in that file, one word or not, so a case named
  under the wrong test file is refused even though another file has it.
  Where the path does not resolve, a bare file name for instance, the name is
  read the way the same name written bare would be.
- `evidence-check --reverify --checked YYYY-MM-DD` writes the date of the
  reading into every row whose hash it moves (#387): after the dates the cell
  holds, once per row. The date cell is the `Checked` column, else the `Date`
  column, else the fourth cell of a headerless ledger row; a moved row with
  none is left whole and named, and the run exits 1. A value that is not a
  calendar date in that form, a date after today, and the flag without
  `--reverify` or beside `--migrate` exit 2 before anything is read. The flag
  says every such row was re-read, so the documents now say to read each row
  citing a drifted coordinate first, or to narrow the write with `--ledger`.
- Without `--checked`, `--reverify` still leaves every date alone, and now
  names each row whose hash it moved, with its ledger and line, its first
  cell and its date as it stands (#387). The exit code is unchanged.

### Fixed

- `evidence-check` hashes the region an anchor names even below a form feed,
  U+2028 or one of the six other characters Python's `splitlines` ends a line
  at and GFM does not (#664). Where one stood in the middle of a line, a
  Python function below it was hashed one line off, a markdown section could
  end at a line that only looked like a heading, and a block in another
  language could end early, and an edit to the unit then passed as unchanged.
  A row whose region holds such a character mid-line, or a Python unit below
  one, reads `DRIFTED` once after the upgrade: re-read it and re-stamp it. A
  character at the end of a line or on a blank line moves no hash.
- `fold-check` counts a document's lines where GFM ends them, so such a
  character no longer puts a document at the ceiling over it (#664).
