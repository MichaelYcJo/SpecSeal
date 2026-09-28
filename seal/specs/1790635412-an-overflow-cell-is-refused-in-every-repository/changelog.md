### Added

- `evidence-check` names a ledger row with more cells than its table's
  header (#585). An unescaped `|` inside a cell splits the row, and the text
  past the last column is in no column, so no reader sees it, and a marker
  written there is never read. Until now only this repository's own test
  refused such a row; a repository that installs the plugin now gets it from
  the shipped checker, as the new verdict `OVERFLOW`, with the line, both
  cell counts and the remedy (write the pipe as `\|`). A row under no
  header, which is every fragment row, is counted against the five columns of
  a ledger row. It is graded like `MALFORMED`: exit 1 on a lenient run, which
  prints the notice naming it, and exit 2 under `--strict`, which is what
  `broad-gate` and the vendored CI template pass. A row with fewer cells than
  its header is not named, because nothing in it is hidden. Both summary
  lines end with `· N overflow`, printed at zero too, and `--reverify` names
  such a row with a `LEFT` line and exits 1.
