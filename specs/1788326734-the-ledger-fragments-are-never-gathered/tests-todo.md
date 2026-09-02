# regression tests to plant — prescribed by round 1, planted by the implementer

All in `tests/test_the_ledger_fragments_fold_at_release.py` unless a row says otherwise.

| # | What it asserts | Destination | Grounds | Status |
|---|---|---|---|---|
| 1 | `--check` output and the already-folded refusal contain no `\` on any platform — the paths in messages are `/`-joined | `tests/test_the_ledger_fragments_fold_at_release.py` | round 1 🔴 1: three assertions fail on `windows-latest` today; a test that asserts no backslash catches the regression on all three legs, not only Windows | ⬜ |
| 2 | `test_this_work_item_wrote_its_own_fragment` passes on a copy of `ROOT` after the fold has run there — the proof moves from the fragment file to its marker in `map.md` | same file, the "this repository" block | round 1 🔴 2: the release-preparation commit removes the file the test reads | ⬜ |
| 3 | a marker for a real work item id quoted in `map.md` prose neither folds nor refuses: the fold runs and exits 0 | same file | round 1 🟡 3 | ⬜ |
| 4 | a row holding U+2028 in a cell arrives in `map.md` as one row, and the same row in `evidence-todo.md` with `drained` after the separator still reads as one open row | same file | round 1 🟡 4 and 🟡 5 | ⬜ |
| 5 | the last row of a fragment keeps its trailing whitespace; a `#` line inside a code fence is not demoted | same file | round 1 🟡 5 | ⬜ |
