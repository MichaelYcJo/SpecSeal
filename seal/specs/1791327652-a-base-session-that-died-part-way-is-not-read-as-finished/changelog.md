### Fixed

- **`broad-gate` no longer calls a failing file `new` when the base's own
  pytest stopped part-way in it (#849).** Without xdist, a test that calls
  `os._exit` or segfaults ends the pytest process itself. Its recorder then
  writes no `end` line, and the base's record held the file's earlier tests
  passing and nothing failing, so the file read `new`: the branch looked to
  have broken a file whose base run had crashed. pytest can also stop a
  session itself and still write the `end` line: a `KeyboardInterrupt` or
  `pytest.exit()` in a test, a failed collection, and xdist under `-x` all
  end it with exit 2. Now a base session is counted as one that stopped
  part-way where its record has no `end` line, or where that line shows an
  exit other than 0, 1 and 5, the three of a session that ran to its end.
  Either `new` then reads `new?` naming how many such sessions there were. A
  recorder that stopped writing for another reason, such as a disk that
  filled, reads the same way, which is the strict direction. Where a red
  session also left tests out of every list, that count is the one named.
  `failing on base too` is unchanged. Two stops are named rather than
  closed: a test that calls `pytest.exit` with a return code of 0, 1 or 5,
  and a run without xdist that `-x` stops while its order mixes files.
- **The failure form says when a session at `HEAD` stopped part-way.** A
  test that kills pytest on the branch writes no failing line, so its file
  was in no list and nothing said a session had stopped. The form now
  counts those sessions under the failing files, and its line for a run
  with no pytest summary names a pytest that died part-way beside one that
  never started (#849).
- The recorder remembers each xdist worker's last report by the worker's
  `id()` while holding the worker itself, so a worker xdist starts in place
  of a crashed one can no longer take over the crashed worker's last report
  and its file. Nothing else is asked of the worker, so no `node` a plugin
  sets can raise out of the recorder's hooks (#849).
