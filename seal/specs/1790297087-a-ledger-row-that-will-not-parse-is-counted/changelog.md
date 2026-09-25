### Fixed

- **A ledger row whose coordinate does not parse now fails `evidence-check`,
  so a ledger that passed before this update can fail after it (issue #299).**
  A coordinate that matched neither the anchor pattern nor the old
  `path:line` one was counted nowhere. A placeholder or short hash, a missing
  path, a bare `"` inside a quoted locator, or an unquoted minor anchor took
  the claim out of the ledger, and the totals still read clean. The check now
  reads each row's `Code grounds` cell, or the second cell of a row with no
  header, and gives it a new verdict, `MALFORMED`. That covers a coordinate
  neither pattern parses, and a cell that cites nothing while the row claims
  something. The finding names the text as written and says what to write
  instead. It fails the run with or without `--strict`, the way `OLD-FORMAT`
  does. Both totals lines end `· N malformed`, printed at zero too.
  `--reverify` names each such row with a `LEFT` line, writes nothing to it
  and exits 1. The commit advisor prints a `MALFORMED` block. The ledger
  template and the skill now say a `"` inside a quoted anchor is written
  `\"`. This repository's own ledgers held seven such coordinates, five of
  them in a `Code grounds` cell. Each was re-read against its code: six are
  corrected, and one claim that was no longer true is removed. A table whose
  header has no `Code grounds` column is not read, so a ledger that renamed
  the column keeps that table out of the verdict.
- **An invalid escape sequence in a Python string no longer stands anywhere
  in the tree (issue #322).** The docstring the issue cited became a raw
  string in 0.14.0, and every tracked `.py` file compiles under
  `python3 -W error` with no warning. Nothing was changed for it here.
