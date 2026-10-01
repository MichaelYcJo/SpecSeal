- **`session-cost --spawns` no longer says no spawn reached a minute under a
  column that prints `1.0m` (issue #701).** The note under the cycle table,
  *`delegated` never reaches a minute here*, was decided on the raw largest
  interval against 60 seconds, while the `delegated` column prints it in
  minutes to one place. A spawn paired in 59.6 s therefore printed `1.0m` in
  the column and *60s at most* in the note beneath it. The note is now decided
  on the minute the column prints, the way #640 fixed the same cause twice for
  the tools-per-turn ratio. Its presence moves only for a largest `delegated`
  interval in (57.0, 60) seconds, so every other reading prints as it did; no
  number on the page moves, the exit code stays 0, and `--json` is unchanged.
  Every other comparison in `session_cost.py` of a value against a threshold
  was checked in the same change: three already compare the figure they print
  (#640), and the rest compare against zero, compare counts, or compare a
  value the page does not print rounded. One has the same shape and was left
  on purpose: the batching line's choice between *one at a time* and *most
  turns send a single call* compares the unrounded ratio with 1.0. At a ratio
  just above 1.0 the page prints `1.00` beside *most turns send a single
  call*, which `1.00` does not contradict and which stays true of a run where
  one turn sent two calls.
