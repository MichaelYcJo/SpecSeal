# tests to plant — written by the review orchestrator, acted on by the implementer

| Asserts | Destination |
|---|---|
| ✅ a cell of only separators (`;`, `—`) in either fix-surface row is refused | planted as `test_a_cell_of_only_separators_is_not_an_answer` in `tests/test_the_fixes_name_their_surface.py`, red-first, dc2a752 |
| ✅ the recorded limit of 🟡 3 is pinned wherever its sentence lands | planted as `test_the_arrow_limit_is_recorded_where_the_rule_lives` (+ the executed-behavior case) in `tests/test_the_fixes_name_their_surface.py`, dc2a752 |

drained — both rows planted by the round-1 fix pass; round 2 read them as its finding surface.
