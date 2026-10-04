### Fixed

- `broad-gate` compares a failing test with the base using the part of the
  `Broad gate` row that runs pytest, wherever that part stands (#747). It
  used to re-run the row's first `&&` part. In a row that lints first, that
  part is the linter, so no failure could show at the base and every failing
  file read `new`, whatever the base did. Now the gate cuts the row where its
  shell does, at `&&`, `||`, `;`, `|` and `&` outside quotes and groups, with
  no `;` under `cmd.exe`. It runs each prefix at the base with the failing
  files added, and reads the first one that prints pytest's summary.

  A file that run names in a `FAILED` or `ERROR` line reads
  `failing on base too`, and one it does not name reads `new`. Where no part
  of the row prints a summary, or the run at the base stopped before every
  test ran, the file reads `new?` with the reason, never `new`. Each run is
  kept as `suite-at-base-<k>.txt`.

  `templates/config.md` rule 3 no longer asks for the runner first. It
  describes both orders: runner first costs one run at the base, and lint
  first re-runs the earlier parts once for each prefix tried. A runner inside
  a `( … )` group, or one whose output goes to a file, reads `new?`.

- The test that checks a row which does not end leaves nothing behind no
  longer fails on a loaded machine (#748). It waited a fixed half second
  after the bound and then looked for the loop's marker. Now it checks in
  one-second windows for up to five seconds, and it still fails when the
  group kill is missing.
