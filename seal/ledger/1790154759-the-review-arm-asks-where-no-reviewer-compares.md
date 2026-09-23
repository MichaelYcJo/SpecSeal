<!-- specs/1790154759-the-review-arm-asks-where-no-reviewer-compares -->

<!-- One work item's rows. No header — `fold_ledger.py` writes the `###` at
the release and moves this file into `seal/ledger.md`.

One row: the review arm's half of the line `seal/ledger.md`'s S11 already
claims for the parity arm. S11's anchor on `DOC_ROOTS` did not move — the
comment above the constant is outside the unit — so it was left as it is. -->

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| R1 · the commit gate's review arm reads no paths: in a repository that opted in, a commit confined to `docs/` and `seal/`, with no declaration, no review mark and no waiver, is stopped exactly as a code change is, and in a migration repository the same commit wakes the review arm alone. `DOC_ROOTS` and `touches_code` are the parity arm's, and the decision table and the wake/quiet table say so | `hooks/commit-review-gate.py#judge@6ca45c3c`, `hooks/commit-review-gate.py#touches_code@ebdf77f8`, `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit@97858237`, `tests/test_chain_hooks_hardening.py#test_a_document_only_commit_wakes_one_arm_and_not_two@67066a74`, `tests/test_chain_hooks_hardening.py#test_the_review_arms_missing_path_line_is_written_where_it_is_met@83f20793` | **Executed** 2026-09-23. With `and touches_code(cwd, invocations)` added to the review arm's condition, both behaviour cases fail; with it removed from the parity arm's condition, the migration-repository case fails beside the existing `test_parity_gate_ignores_document_only_commits`. The prose case fails on its own when the `docs/` row, the grounds paragraph, the declaration row or the wake cell's added clause is deleted. Each mutation was restored from a saved copy, and `tests/test_chain_hooks_hardening.py` with `tests/test_gate_judges_the_repo_it_commits_to.py` then passed, 139 cases | 2026-09-23 | **The line is kept off on purpose, and the measurement is the reason** (`spec.md` M1–M4, `docs/review-chain-spec.md` §*Review arm*). A lighter tier for a documentation pass is the `straight to the PR` declaration, chosen before the first edit; it is never inferred from paths |
