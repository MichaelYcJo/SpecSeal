### Fixed

- **A merge of the base inside a fix range no longer fills the round record
  with another work item's units** (#860). `round-record close` compared the
  range's two ends, so everything a merge brought in counted as this round's
  fixes: one record's `New units` named 111 units, and 109 of them were
  another work item's. Now a range `a..b` owns exactly the commits `git log
  --ancestry-path --no-merges a..b` lists, and `Contract changes` and `New
  units` keep a unit only where one of those commits added or changed it.
  A path filter would not have been enough, because one file the item
  touched carried 22 new names at the two ends and 2 of them were the
  item's. `docs/the-record-layout.md` §*A range owns the commits that
  descend from its start* states the rule.

  `Fix of a fix` reads the previous record's range the same way, so a
  finding inside a unit no own commit wrote reads `no`. `close` now refuses
  two shapes before writing anything: a `--range` whose start is not an
  ancestor of its end, and a `fixed` row naming a commit the range does not
  own — a merge, or a commit not made on top of the start. The `Fix range`
  row's count is unchanged and is still git's own count of `a..b`.

- **The changelog-fragment notice reads the range's own commits instead of
  HEAD's first parent** (#805). It followed HEAD's first parent, so on a
  branch rebuilt on its base with the old tip merged in, it named another
  work item's commit on the base and missed the item's own late fix. It now
  reads what the range from round 1's `Target SHA` to HEAD owns, by the same
  rule as `close`. A commit is named when no own commit that changed the
  fragment descends from it. On a straight history that is every commit
  after the fragment's last change, as before. On CI's checkout, the pull
  request merged into its base, the range also holds every base commit with
  round 1's target as an ancestor, so CI can name a commit a local run does
  not. The notice still prints and never refuses.

- **A file whose name git quotes is read as that file** (#860).
  `round-record` read three git listings as plain text. With
  `core.quotePath` on, which is git's default, a non-ASCII file name arrives
  in quotes and matched nothing. The record therefore missed that file's new
  units, named a call inside it by a quoted path, and could not place a
  finding in it. All three listings are now read with `-z`. A `:` inside a
  path no longer splits it, and a binary file that holds the call is left
  out of the search.
