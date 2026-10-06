### Fixed

- **`broad-gate` no longer calls a failing file `new` when a test killed the
  base's own pytest in it (#849).** Without xdist, a test that calls
  `os._exit` or segfaults ends the pytest process itself. Its recorder then
  writes no `end` line, and the base's record held the file's earlier tests
  passing and nothing failing, so the file read `new`: the branch looked to
  have broken a file whose base run had crashed. Now a base session whose
  record has no `end` line is counted as one that stopped part-way, and
  either `new` reads `new?` naming how many such sessions there were. A
  recorder that stopped writing for another reason, such as a disk that
  filled, reads the same way, which is the strict direction. Where a red
  session also left tests out of every list, that count is the one named.
  `failing on base too` is unchanged.
- The recorder remembers each xdist worker's last report by the worker
  itself rather than by `id()` of an object it did not hold, so a worker
  xdist starts in place of a crashed one can no longer take over the
  crashed worker's last report and its file (#849).
