### Fixed

- **A merge of the base inside a fix range no longer fills the round record
  with a sibling's units** (#860). `round-record close` compared the range's
  two ends, so everything a merge brought in counted as this round's fixes:
  one record's `New units` named 111 units, and 109 of them were a sibling's.
  Now a range owns only its non-merge commits that descend from its start.
  `Contract changes` and `New units` keep a unit only where one of those
  commits added or changed it. A path filter would not have been enough,
  because one file the item touched carried 22 new names at the two ends and
  2 of them were the item's.

  `Fix of a fix` reads the previous record's range the same way, so a
  finding inside a unit a merge brought in reads `no`. `close` now refuses
  two shapes before writing anything: a `--range` whose start is not an
  ancestor of its end, and a `fixed` row naming a merge or a commit a merge
  brought in. The `Fix range` row's count is unchanged and is still git's
  own count of `a..b`.

- **The changelog-fragment notice names the item's own commits whichever way
  a merge was made** (#805). It followed HEAD's first parent, so on a branch
  rebuilt on its base with the old tip merged in, it named a sibling's squash
  as the item's and missed the item's own late fix. It now reads the commits
  that descend from round 1's `Target SHA`. A commit is named when no own
  commit that changed the fragment descends from it. On a straight history
  that is every commit after the fragment's last change, as before, and a
  topic branch merged in after the build is now read too. The notice still
  prints and never refuses.

- **A file whose name git quotes is read as that file** (#860).
  `round-record` read three git listings as plain text. With
  `core.quotePath` on, which is git's default, a non-ASCII file name arrives
  in quotes and matched nothing. The record therefore missed that file's new
  units, named a call inside it by a quoted path, and could not place a
  finding in it. All three listings are now read with `-z`. A `:` inside a
  path no longer splits it, and a binary file that holds the call is left
  out of the search.
