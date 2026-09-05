# 1788501054-a-check-reports-clean-while-something-is-missing — tests to plant

<!-- Regression tests a review round found missing and did not write. One row
each, with the destination file. Planted by a later fix pass or the release
that follows; a row is removed when its case lands. -->

| Case | Destination | Found by | Seen red how |
|---|---|---|---|
| Two dangling symlinks to one missing target are named twice by a narrowed run, never folded into one — `file_identity`'s fallback keys on the path's own absolute spelling, and `realpath` would resolve both to the one missing target and swallow a fragment | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py` | round 15, a mutation battery: the fallback replaced by `os.path.realpath(path)` leaves all 21 cases green | replace the fallback with `realpath` before planting; the case must go red there (§15). Sketch: a clean `seal/ledger.md`, two symlinks under `seal/ledger/` to one file that does not exist, `--ledger seal/ledger.md .` → exit 0 and both link names in the skipped notice |
