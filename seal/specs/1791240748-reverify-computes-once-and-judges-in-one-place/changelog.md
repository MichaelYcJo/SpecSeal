### Fixed

- One `evidence-check --reverify` run now settles every ledger line it
  rewrites (#806, #824). A coordinate naming a line of a ledger the run
  writes, whether a citing row's citation or any other coordinate quoting a
  released row, is judged against the text the run will write there, and the
  run recomputes what it plans until nothing it would write changes, then
  writes once. A fragment naming a line of a release file that the same run
  re-stamped no longer needs a second run before `--strict` reads it clean,
  and what the run writes no longer depends on the order the ledgers are
  listed in. A row whose coordinate names text that every re-stamp of it
  moves again, its own line or a row naming it back, is left at the hash it
  recorded and named on a `LEFT` line saying it does not settle, and the run
  exits 1; it used to be re-stamped once, to a hash that drifted at once.

- `--reverify` reads a coordinate the way `--strict` does (#809, #824). A
  claim on a place the declaration rule is unsure of, which the check calls
  DRIFTED, is now re-stamped at the hash of the statement it quotes, in place
  and under `--into`, and a pact change records that move. It used to be
  left, or named *no one place to hash*, and recorded BROKEN. Every `left`
  line now carries the check's own sentence for that coordinate followed by
  ` — left`, so a tie among places the rule is unsure of reads `locator is
  ambiguous — 3 places: …` from both commands.

- A pact change recorded by an in-place re-stamp is the hash before the run
  and the hash after it (#824). A coordinate the run leaves is recorded
  BROKEN at its row's own hash, never after a hash on the way that no file
  ended up holding.

- A run narrowed with `--ledger` names a row in a file it left out whenever
  it re-stamps a ledger line that any coordinate of the row names, not only
  the row's citation, and exits 1 (#824).
