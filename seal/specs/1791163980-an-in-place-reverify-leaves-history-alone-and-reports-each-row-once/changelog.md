### Fixed

- An in-place `evidence-check --reverify` no longer re-stamps and re-dates a
  reading nobody re-read (#785). A family counts only its newest readings,
  so an older `Re-read ·` row a newer one outranks is history, and so is
  every row of a family a `Corrected ·` row supersedes. The run re-stamped
  such a row to the current hash and added the `--checked` date to it, which
  claimed a reading that never happened and could make the old row the
  newest one. The run now judges each code coordinate once, before its first
  walk, the way `--strict` does: a coordinate its family already holds, or
  that a superseded family carries, keeps its hash and its date, is named on
  no line, and records no pact change. On a row the run dates for another
  coordinate, a held coordinate takes the new hash too, because the date
  makes that row its newest reading; where no one place holds it, it is named
  `left` and recorded BROKEN, as any such coordinate is. A coordinate naming a
  line of a ledger the run rewrites is never treated as held, because the run
  can move that line. Without the freeze, a run narrowed to a released file
  whose family a fragment already holds now exits 0, where it re-stamped the
  released row and then named the fragment's citation of it.

- An in-place `--reverify` prints each coordinate's `left` line once, after
  its walks (#792). A file the run walks more than once printed its `left`
  lines on the first walk only, so a coordinate a later walk cleared was
  still reported as left, and one a later walk left was never reported. The
  lines now come from the same fold as the pact-change record, and print
  where the last walk left the coordinate.

- The `LEFT … still DRIFTED` line no longer tells you to run without
  `--ledger` when that cannot help (#792). The line used to end with that
  remedy whatever the cause, including on a run that had no `--ledger`. It
  now names a remedy per coordinate: `--ledger` only where a newest reading
  of it sits in a file the run did not write; that the run left it, pointing
  at the line above that says why, where the run left it itself; and no
  remedy where neither is found, as for a ledger the run cannot read. The
  exit code is unchanged.

- `--reverify` names a claim whose minor content two places hold (#808).
  The check calls such a row BROKEN, because two units sharing one line is
  a tie the recorded hash cannot break, and `--reverify` read it as
  unchanged and said nothing. It now prints the check's reason on a `left`
  line and records the BROKEN in a signatory's pact changes.

- `docs/the-evidence-ledger.md` says what an in-place re-read writes without
  the freeze (#781): the date of the reading, added to the row's `Checked`
  cell. It used to promise a dated note, which the writer never wrote.
