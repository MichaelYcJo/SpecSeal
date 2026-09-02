# verified facts to merge into the work item's ledger fragment

Merge each into `.specseal/map/1788326734-the-ledger-fragments-are-never-gathered.md`, then write `drained` above this table or mark each row ✅. The fold this work item adds refuses to run while a row here is open, so this file is the first the guard will ever read.

| Claim | Grounds | Label |
|---|---|---|
| `check_ledger`'s dedup is per file: `seen` is a local of one call, keyed `(coordinate, hash)`, so a fold moves the checker's total by exactly the rows two files cited identically | `skills/evidence-check/scripts/evidence_check.py#check_ledger`; executed on a copy at e4b74fc: 155 ok → 154 ok, 0 drifted, 0 broken | Executed |
| The hygiene step exits 0 with a message on a pull request whose base is not `main`, and runs `fold_ledger.py --check` only when it is | `.github/workflows/hygiene.yml` step "every ledger fragment folded into the gathered ledger" | Read |
| Fragment row 11's "six fragments, 55 table rows" describes the tree before this work item's own fragment existed; at e4b74fc the tree holds seven, and `--check` after a fold prints `7 work items marked` | `.github/scripts/fold_ledger.py#main`; executed on the copy | Executed |
