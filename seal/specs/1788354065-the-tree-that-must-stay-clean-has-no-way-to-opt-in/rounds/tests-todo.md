# tests to plant — written by the review orchestrator, acted on by the implementer

| Asserts | Destination |
|---|---|
| ✅ with `os.path.relpath` monkeypatched to raise `ValueError` in a local fixture, `commit-review-gate.py#main` prints `deny`/`ask` without an exception and the hint path is absolute (round-1 🔴 1) — `test_the_commit_gates_hint_survives_a_root_with_no_relative_spelling`, planted at 1f27eac | `tests/test_gates_do_not_fail_open.py` |
| ✅ the same monkeypatch: `ledger-migrate.py#main` finishes without an exception and the migration proceeds (🔴 2) — `test_the_ledger_migration_hook_survives_a_ledger_with_no_relative_spelling`, planted at 2078984 (with `test_in_local_mode_the_migration_notice_does_not_promise_a_diff` and `test_in_shared_mode_the_migration_notice_still_ends_with_the_diff` for 🟡 5) | `tests/test_local_mode_resolves_under_the_git_dir.py` |
| ✅ the README's switch block run with a subdirectory as cwd still lands the root at `<repo>/seal/` — read the block out of the document the way `test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set` does (🟡 3) — `switch_block` and `test_the_switch_block_lands_the_root_at_the_tree_root_from_a_subdirectory`, both editions, planted at f53d615 | `tests/test_first_setup_asks_once.py` |
| ✅ the bootstrap names `CLAUDE_PLUGIN_ROOT` as where the version is read (🟡 4) — `test_the_version_is_read_from_the_plugin_root_and_not_from_the_tree`, planted at f53d615 | `tests/test_first_setup_asks_once.py` |
| ✅ a stamped local-mode repository checking out an old branch creates no `<repo>/seal/` and leaves status empty (P5) — `test_a_stamped_local_mode_repository_leaves_an_old_layout_branch_alone`, planted at 2388341 | `tests/test_the_root_migrates_itself.py` |
