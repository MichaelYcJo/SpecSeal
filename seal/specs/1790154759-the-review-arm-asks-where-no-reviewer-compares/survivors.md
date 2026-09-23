# Survivors — the review arm asks where no reviewer compares

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_chain_hooks_hardening.py` | parity_repo(repo) (repo / "docs" / "policies").mkdir(parents=True, exist_ok=True) stage(repo, "docs/policies/note.md", "text\n") cmd = parity_only( | Fixture code in `test_parity_gate_ignores_document_only_commits`, not a sentence. Round 1's fix pass replaced the same three lines in the review arm's cases with one path per root, because those cases guard a line that can leak by halves. This case guards the parity arm's silence on `docs/`, which is the row it was written for, and `seal/` for the parity arm is covered by the parametrised migration-repository case beside it |
| `tests/test_a_row_points_by_content.py` | d = repo / "docs" / "policies" | Unrelated fixture: it builds the pre-0.2 `docs/**/_evidence.md` address for the evidence checker. It shares a path, not a claim, with the lines the range replaced |
| `tests/test_local_mode_resolves_under_the_git_dir.py` | `docs/**/_evidence.md` stays under the repository root | Unrelated fixture about the evidence advisor's old address. It shares the words `repo docs policies` with the replaced lines and makes no claim about either gate arm |
| `tests/test_local_mode_resolves_under_the_git_dir.py` | The old address under the tree keeps its boundary | Unrelated fixture about a dirty ledger under the tree in local mode. It shares the words `repo docs policies` with the replaced lines and makes no claim about either gate arm |
