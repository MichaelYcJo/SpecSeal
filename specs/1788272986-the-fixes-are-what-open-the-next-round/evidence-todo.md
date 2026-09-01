# verified facts to merge into the work item's ledger fragment

| Claim | Grounds | Label |
|---|---|---|
| an unreadable round record cannot read as "no rows required" — `fix_surface` returns nothing and `checked_by` errors on the same record in the same loop | `skills/code-review/scripts/chain_check.py#fix_surface`, `#main`; probe: garbage record exit 1 | Executed |
| the decode-failure fail-open class cannot reach `chain_check.py` — `git()` pins `encoding="utf-8", errors="replace"`, so `test_gates_do_not_fail_open.py` has nothing to cover here | `skills/code-review/scripts/chain_check.py#git` | Read |
| a separator-only cell passes both fix-surface rows (until 🟡 1's guard lands; re-anchor the row to the refusal after) | `skills/code-review/scripts/chain_check.py#fix_surface`; probe: exit 0 | Executed |
