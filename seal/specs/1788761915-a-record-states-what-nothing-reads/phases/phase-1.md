# 1788761915-a-record-states-what-nothing-reads — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `10871e3` |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Build the boundary the identifier and stamp arms are drawn against: a reader
answering *has this work item shipped* from the presence of
`seal/ledger/<id>.md`, with the fold as its stated grounds. Cases for both
arms, and the tree's own two unreleased work items as the live example.

## What this phase found

**The arm's home was not settled by `plan.md`, and it is
`skills/evidence-check/scripts/evidence_check.py`.** `spec.md` says *no new
file and no new CLI* and then leaves *a new command or an arm of one that
exists* to the plan, which names neither. Three homes were weighed against
what each already holds. `chain_check.py` needs a `--baseline` and a pull
request's state, and this check is neither diff-scoped nor branch-scoped.
`seal.py` has the subcommand shape and none of the resolution machinery.
`evidence_check.py` is the checker whose one job is already *does a written
claim about the tree still hold*, and the stamp arm of phase 4 is spelled in
`plan.md` as *resolved the way a ledger anchor is* — which is
`resolve_unit`, `content_hash` and `place`, all of them here. It also
resolves the `seal/` root itself (`seal_home`), which the boundary needs, and
it ships with `bin/evidence-check` already on PATH, so no new CLI appears.

**The corpus the identifier arm compares against is everything outside
`seal/specs/`, and widening it to everything outside `seal/` is wrong.**
Measured on this tree: the wider exclusion refuses five occurrences of
`test_no_loaded_file_hardcodes_the_running_version` in work item
`1788735085`'s records, and all five are that work item narrating its own
rename. `seal/ledger.md`'s S15 note deliberately keeps the old name beside
the new one *so a reader coming from an older record can follow it*, and the
narrower corpus reads that note. The gathered ledger is a permanent, curated
document; `seal/specs/` is the per-work-item set nothing reads, which is the
whole subject of #190.

**A `__pycache__` under a record directory is not a record, and a
`__pycache__` anywhere is not the tree.** A compiled module carries its own
identifiers in its constants pool, so a name walk that reads one answers *the
tree still has this* for a name the tree lost at the last commit. `SKIP_DIRS`
is shared by both walks for that reason.

**One mutation of `unshipped` is equivalent rather than uncaught.** Sourcing
the names from `specs/` instead of `ledger/` leaves all nine cases green,
because the `isfile` guard against the fragment directory still decides. The
mutation that actually removes the boundary — that guard dropped as well —
turns three cases red, which is the one the arm rests on.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
