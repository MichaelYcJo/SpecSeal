# verified facts to merge into the work item's ledger fragment

drained — all four rows merged into `seal/ledger/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in.md` ("What round 1 settled") by the round-1 fix pass; rows 1, 2 and 4 carried as the reviewer executed them, with the units they cite re-run through their test files where the fix pass touched them (`committed_declarations`, `judge`); row 3 pinned by the planted P5 test (`test_a_stamped_local_mode_repository_leaves_an_old_layout_branch_alone`, 2388341).

| Claim | Grounds | Label |
|---|---|---|
| S7: with the declaration only under `.git/seal/`, `chain_check.py --baseline main` exits 0 ("examined nothing") and `unverified_check.py --baseline main seal/specs/` exits 2 ("no such path") — reproduced by the reviewer, not taken from phase 3 | `skills/code-review/scripts/chain_check.py#declared_for_this_branch`, `skills/verify/scripts/unverified_check.py#main` | Executed |
| the gate's hint path from a linked worktree (a path with spaces) can be typed as-is and the gate is silent afterwards (P6) | `hooks/commit-review-gate.py#judge` | Executed |
| a stamped local-mode repository that later checks out an old-layout branch moves nothing and stages nothing (P5) | `hooks/root-migrate.py#has_root`, `#main` | Executed |
| in a linked worktree the marks live under `--git-dir` (per worktree) and the root under `--git-common-dir` (P7) | `hooks/commit-review-gate.py#read_mark`, `hooks/optin.py#git_common_dir` | Executed |
