### Fixed

- Three ledger rows each state one reading (#568). Two of them carried a
  second Checked date and Notes cell behind an escaped separator: one merge's
  two sides, kept whole. Their notes are now one union, with every dated
  marker from both sides, under one Checked date. The third row's Notes cell
  was split in three and is joined. One row's claim still described the
  version check without the tagged half #363 added, and is corrected.
- The ledger's cell-count case now counts fragment rows (#501). It named a
  row wider than its table's header, and a fragment has no header by rule,
  so every row a branch wrote was read and none was counted. A row with no
  header above it is now counted against the five columns
  `templates/ledger.md` declares for a ledger row. A branch whose fragment
  row carries a stray `|` is refused on its own pull request rather than at
  the release that folds it.
- The clauses the ledger's edit and conflict rules gained in 0.15.1's review
  are held by a case (#569): a claim an edit made false is corrected first
  with a `Corrected <date>` note, a conflicted row's hash goes to neither side
  where both edited the unit, and the row is re-read against every edit the
  merge carries. Deleting any of them from `CLAUDE.md`, `CONTRIBUTING.md` or
  the ledger policy now fails the build.
