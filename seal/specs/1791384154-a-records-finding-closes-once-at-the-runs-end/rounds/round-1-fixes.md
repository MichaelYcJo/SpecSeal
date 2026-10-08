## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `7706e367` — the rider's three measurements re-run at the base and at the fix (one invocation alone, one with everything above, `_hides_a_commit` True: unchanged by the note paragraph), recorded in the rider, and the stamp re-taken with `rider_check.py --reverify --only agents/smith.md`; `rider_check.py` exit 0 and `tests/test_a_rider_reaches_its_file.py` 49 passed |
| 2 | fixed | `9a37a02d` — `NOTES_FROM = 1791384163`, one past the batch 1791384152–1791384162 whose rounds run under 0.20.0's `close`; the cutoff case moved with it and is red at the old value; the grounds' wording made version-free in `38696bb0` for `tests/test_release_hygiene.py` |
| 3 | fixed | `9a37a02d` — `new` refuses the redesign's first record while the stopped run carries an open ⬜, naming it and `notes`; `test_the_redesign_waits_for_the_stopped_runs_notes`, red with the refusal removed |
| 4 | fixed | `9a37a02d` — `docs/review-chain-spec.md` now says a ⬜ closes at the run's end through `notes` and a 🟡 in its fix table, in place, the document still at 999 lines; the overview's claim that it did not contradict is replaced |
| 5 | fixed | `9a37a02d` — `test_notes_names_each_row_it_cannot_apply_and_writes_nothing` pins the five sentences, each red when changed; the docstring now names the case that asserts the already-closed refusal |
| 6 | answered | corrected at `0966de0e` — the two `Re-read ·` rows are replaced by `Corrected · S10` and `Corrected · S13` in this item's fragment |
| 7 | answered | corrected at `9a37a02d` — `agents/warden.md` excepts a ⬜ the run still carries from the answer every earlier finding needs |
| 8 | answered | corrected at `9a37a02d` — the owner file's rule-1 paragraph and the policy's both read *a ⬜ like any other* where they said *corrected in passing or not at all* |
