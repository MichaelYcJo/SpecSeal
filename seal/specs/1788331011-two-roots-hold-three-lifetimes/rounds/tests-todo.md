# tests to plant — written by the review orchestrator, acted on by the implementer

| Asserts | Destination |
|---|---|
| an ignored file directly under `.specseal/` does not stop the move (round-1 P1) | `tests/test_the_root_migrates_itself.py` |
| `seal` present as a file stops with a printed line, never an exception (P2) | `tests/test_the_root_migrates_itself.py` |
| a destination that already holds the file is named and not promised a continuation (P3) | `tests/test_the_root_migrates_itself.py` |
| a row citing a foreign `specs/` entry is left where it is (P5) | `tests/test_the_root_migrates_itself.py` |
| `repoint()` failing after the moves stamps nothing and says so | `tests/test_the_root_migrates_itself.py` |
| the README's by-hand sequence yields the hook's tracked set (P6) | `tests/test_the_root_migrates_itself.py` |
