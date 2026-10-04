# 1791076833-the-reverify-writer-records-before-it-restamps — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 2cfb60f3 |
| Ran by | unknown — the spawn prompt handed over no value, and a segment does not source this row from itself |

## What this phase was asked

The ledger and the closing records. `bin/evidence-check` names the released
rows this item drifts; each is read, then re-read into this item's fragment
with `--reverify --into seal/ledger/1791076833-….md --checked <date>`, and a
released claim the change made false takes a `Corrected ·` row instead. New
claim rows for W8–W10. `survivors.md` for the branch's range, and
`overview.md`. Verified by `bin/evidence-check --strict .` exit 0,
`correction-check`, `survivor-check`, `unverified-check` and `chain-check
--worktree --baseline origin/release/v0.18.1`. Q5 closes here, and Q7 as far
as #741 allows.

## What this phase found

**Q5, measured.** `bin/evidence-check .` at `25473301` named 57 released rows:
56 DRIFTED and 0.18.0's P8, whose `hooks/config.py#TABLE_BREAK` is BROKEN · NAME NOT IN TREE
because the one table walker replaced the walk it served. Every claim was read
against the tree; the carry's additions (a `cmarkgfm` pin, the pact-review act,
`pact-changes/` in the drawings, the walker) and phase 2's (the strict read,
the held lines) leave each one true. P8's claim holds through the walker, so
its `Corrected ·` row carries the other nine coordinates and puts
`hooks/config.py#gfm_table` where `TABLE_BREAK` stood.
`--reverify --into … --checked 2026-10-04` then wrote 50 `Re-read ·` rows,
the 0.18.0 members of a family being answered through its root, and
re-stamped this item's own rows in place. Two re-reads carry a note: P1-1,
because `cmarkgfm` is a second test-only package beside the parser its claim
names, and L1 of 0.15.1, because it drifted on the base already: #752 changed
its case at `f19e2762` and this branch does not touch that file.

**A re-read found a defect in phase 2.** 0.8.3's row says every place a
ledger path becomes a name a person reads calls `display_name`. Phase 2's
W10 `LEFT` line used `built_name`, which is for a coordinate the run builds.
`2e5c6c35` switches it; the cases pin the POSIX spelling, which both
functions print the same, so no case changed.

**C1's claim was out of date in a fragment row, so it was edited in place.**
It said "a row identical in `Clause`, `Row` and `Code` is not appended",
which PR #749's round 2 replaced with the record's last word per coordinate.
A fragment row is not frozen, so the claim now says what the code does, and
its coordinates gain the three cases phase 2 added for it.

**Q7, half.** `origin/release/v0.18.1` did not move during the build, so #741's
check has not run over the carry. An AST scan of the calls on every line this
branch adds found no `open`, `fdopen`, `read_text` or `write_text` without an
encoding; the whole-file scan found some in test modules the carry rewrote,
on lines the base already had, and none in a product file.

**Verified, executed:** `bin/evidence-check --strict .` at `b67c2bbb`: 4352
OK, 0 drifted, 0 broken, exit 0. `bin/correction-check --range
e141980a..HEAD`: no merge commit in the range, no released ledger file
changed, exit 0. `bin/survivor-check --range e141980a..HEAD --exempt
…/survivors.md`: three places in `tests/test_a_signatory_declares_its_pact.py`,
each judged in `survivors.md`, exit 0. `bin/unverified-check --baseline
origin/release/v0.18.1 <this directory>`: 3 open, 0 unreadable, exit 0.
`chain_check.py --worktree --baseline origin/release/v0.18.1`, judged as a
ready pull request: exit 1, because `rounds/` holds no `round-N.md` yet. That
is the review chain's to write, and round 1 has not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| C1's sentence "a row identical in `Clause`, `Row` and `Code` is not appended" | C1's claim in this item's fragment, reworded to the record's last word per coordinate |
