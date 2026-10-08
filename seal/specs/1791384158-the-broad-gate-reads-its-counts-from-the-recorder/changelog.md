### Fixed

- **The broad gate's suite counts come from what its own pytest recorded,
  never from what the row printed (#869).** The seal's `suite` row and the
  failure form's counts were read off pytest's printed summary line, so a
  test that printed a summary of its own could put its number on the seal.
  The gate's pytest recorder now writes, for every test report, the category
  pytest's own summary counts it under, and a line for a module that skipped
  itself beside one that failed to import. The panel and the failure form
  count those lines, in pytest's order and wording, and add up every pytest
  session the row ran. Where no pytest the row ran left a record, the form
  says so and names the three causes, instead of saying no summary was
  printed. Where a record holds a line that is not the recorder's, the form
  says how many lines were passed over and prints no count, and a file that
  would read `new` from such a base reads `new?` instead.
- **The release seal reads the same record through the gate's own reader
  (#869).** The `seal` job runs the suite at the tag with the recorder
  loaded and no JUnit file, and `release_seal.py` takes its passed and
  skipped counts from that record. A record with no session for the run's
  key, a line that is not the recorder's, a session that stopped part-way,
  or a failure or an error in it gives no seal, with the reason on a
  `::warning::` line, as an unreadable JUnit file did. Drawing a seal by
  hand now names `SUITE_RECORDS` and `SUITE_KEY` instead of `SUITE_XML`
  (`docs/release-checklist.md`).
- **A malformed `seal-mark.txt` stops the gate with its own sentence
  (#869).** `broad-gate` and `broad-gate --preflight` ended in a Python
  traceback where the disc's mark chart was not in shape. They now exit 2
  before anything runs, saying which file would not load and why.
- **A base that `pytest.exit()`, `-x` or `--maxfail` stopped part-way is no
  longer read as finished (#852).** These stops can end a session with exit
  0, 1 or 5, the same exits a session gives when it ran every test, so a
  file the base never finished read `new`. The recorder now writes on the
  session's last line what stopped it, read from pytest's own hooks and
  flags: an interrupt, `pytest.exit()` with whatever code it chose, `-x` or
  `--maxfail`, or a plugin's stop such as `--stepwise`. The gate reads such
  a session as stopped part-way, so the file reads `new?` naming it, and
  the two stops `templates/config.md` rule 3 left open are closed. Measured
  on pytest 6.1, 7.0 and 9.1, and on 9.1 with pytest-xdist 3.8.

### Removed

- **The stamp's scale (#853).** Since the disc became one size in 0.20.0,
  the scale changed nothing the stamp drew. `--scale` is gone from
  `seal-stamp` and `broad-gate`, the gate writes no `scale` into the values
  file, and a values file that still carries one draws as before. The
  drawing is byte for byte the same. In this repository, a seal sealed by
  the tree's gate before the plugin is updated stays pending under the
  installed 0.20.0 hook, which refuses a file with no `scale`;
  `seal-stamp --from <path>`, which the `SEALED` line names, draws it, and
  so does the next turn after the update.
