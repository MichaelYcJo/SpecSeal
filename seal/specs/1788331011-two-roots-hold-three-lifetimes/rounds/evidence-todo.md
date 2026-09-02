# verified facts to merge into the work item's ledger fragment

drained — all four rows merged into `seal/ledger/1788331011-two-roots-hold-three-lifetimes.md` ("What round 1 settled") at 2ba5301; rows 1, 2 and 4 re-run in the fix pass rather than copied, row 3 pinned by the planted by-hand test.

| Claim | Grounds | Label |
|---|---|---|
| `chain_check.py --baseline origin/release/v0.4.0` at 4516166 judges one declaration (this item) and excludes fourteen `R100` renames | `skills/code-review/scripts/chain_check.py#changed`, `#changed_routing` | Executed |
| `hooks/dispatch.py session-start` delivers `root-migrate.py`'s `systemMessage` and writes the marker (round-1 P7) — closes overview §Not verified's dispatch row for the dispatch path, not for a real repository | `hooks/dispatch.py#GROUPS`, `hooks/root-migrate.py#main` | Executed |
| the hook and the README's by-hand sequence produce the same `git ls-files` set on an old-layout fixture (P6); the hand sequence needs `--reverify` to close the rows | `hooks/root-migrate.py#moves`, `README.md` §"Coming up from 0.3.x" | Executed |
| `evidence_check.py --strict .` at 4516166: 208 ok · 0 drifted · 0 broken; `unverified_check.py`: 13 · 29 · 12 · 0 | `skills/evidence-check/scripts/evidence_check.py`, `skills/verify/scripts/unverified_check.py` | Executed |
