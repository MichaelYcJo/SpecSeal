# verified facts to merge into the work item's ledger fragment

| Claim | Grounds | Label |
|---|---|---|
| S7: with the declaration only under `.git/seal/`, `chain_check.py --baseline main` exits 0 ("examined nothing") and `unverified_check.py --baseline main seal/specs/` exits 2 ("no such path") — reproduced by the reviewer, not taken from phase 3 | `skills/code-review/scripts/chain_check.py#committed_declarations`, `skills/verify/scripts/unverified_check.py#main` | Executed |
| the gate's hint path from a linked worktree (a path with spaces) can be typed as-is and the gate is silent afterwards (P6) | `hooks/commit-review-gate.py#judge` | Executed |
| a stamped local-mode repository that later checks out an old-layout branch moves nothing and stages nothing (P5) | `hooks/root-migrate.py#has_root`, `#main` | Executed |
| in a linked worktree the marks live under `--git-dir` (per worktree) and the root under `--git-common-dir` (P7) | `hooks/commit-review-gate.py#read_mark`, `hooks/optin.py#git_common_dir` | Executed |
