# tests to plant — written by the review orchestrator, acted on by the implementer

| Asserts | Destination |
|---|---|
| with `os.path.relpath` monkeypatched to raise `ValueError` in a local fixture, `commit-review-gate.py#main` prints `deny`/`ask` without an exception and the hint path is absolute (round-1 🔴 1) | `tests/test_gates_do_not_fail_open.py` |
| the same monkeypatch: `ledger-migrate.py#main` finishes without an exception and the migration proceeds (🔴 2) | `tests/test_local_mode_resolves_under_the_git_dir.py` |
| the README's switch block run with a subdirectory as cwd still lands the root at `<repo>/seal/` — read the block out of the document the way `test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set` does (🟡 3) | `tests/test_first_setup_asks_once.py` |
| the bootstrap names `CLAUDE_PLUGIN_ROOT` as where the version is read (🟡 4) | `tests/test_first_setup_asks_once.py` |
| a stamped local-mode repository checking out an old branch creates no `<repo>/seal/` and leaves status empty (P5) | `tests/test_the_root_migrates_itself.py` |
