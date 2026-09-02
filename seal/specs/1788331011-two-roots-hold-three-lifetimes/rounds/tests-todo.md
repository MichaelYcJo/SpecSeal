# tests to plant — written by the review orchestrator, acted on by the implementer

| Asserts | Destination |
|---|---|
| ✅ an ignored file directly under `.specseal/` does not stop the move (round-1 P1) — `test_an_ignored_file_directly_under_the_old_root_does_not_stop_the_move`, planted at f2c9570 | `tests/test_the_root_migrates_itself.py` |
| ✅ `seal` present as a file stops with a printed line, never an exception (P2) — `test_a_file_named_seal_stops_with_a_line_not_an_exception`, planted at f2c9570 | `tests/test_the_root_migrates_itself.py` |
| ✅ a destination that already holds the file is named and not promised a continuation (P3) — `test_a_destination_already_holding_the_file_is_named_and_left_to_the_person`, planted at f2c9570 | `tests/test_the_root_migrates_itself.py` |
| ✅ a row citing a foreign `specs/` entry is left where it is (P5) — `test_a_row_citing_a_foreign_specs_entry_is_left_where_it_is`, planted at f2c9570 | `tests/test_the_root_migrates_itself.py` |
| ✅ `repoint()` failing after the moves stamps nothing and says so — `test_a_repoint_that_fails_after_the_moves_says_so_and_stamps_nothing`, planted at f2c9570 | `tests/test_the_root_migrates_itself.py` |
| ✅ the README's by-hand sequence yields the hook's tracked set (P6) — `test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set`, both editions, planted at f2c9570 | `tests/test_the_root_migrates_itself.py` |

round 2 added:

| Asserts | Destination |
|---|---|
| a symlinked `.specseal/` is refused with a line naming the by-hand section, nothing moves, nothing is stamped (round-2 🟡 A) | `tests/test_the_root_migrates_itself.py` |
| when `git ls-files` cannot answer, `dirty()` refuses (round-2 🟢 B) | `tests/test_the_root_migrates_itself.py` |
| an item-shaped tracked file under `specs/` is left where it is (round-2 🟢 C) | `tests/test_the_root_migrates_itself.py` |
| `by_hand_block` fails loudly when the README's block leaves its section (round-2 🟢 E) | `tests/test_the_root_migrates_itself.py` |
