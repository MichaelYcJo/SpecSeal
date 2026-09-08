# 1788873620-two-in-range-values-make-one-that-is-not — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | ae0c238 |
| Ran by | smith on `claude-opus-5[1m]` — the spawn prompt named no model. The segment's own harness line is the source; the transcript's `message.model` rows carry the bare id `claude-opus-5`, the same model without the context-window marker |

## What this phase was asked

Write the records this work item owes: the ledger rows in the work item's own
fragment, the changelog fragment, the phase records, the closing memo, and
**only** the `#192` box in `docs/flow.md`'s 0.9.3 section — not the section's
prose and not another item's row, because the `#272` branch owns that prose
tonight.

## What this phase found

**The one place a fragment could not do the work.** `--reverify` reported
`skills/verify/scripts/session_cost.py#token_thirds` drifting from `4666a9fd`
to `46763d25`, because phase 1 added the rule to that unit's docstring. The
drifting row is R3 of work item `1788700685` in the shared `seal/ledger.md`,
and its clause reads *the class is not closed and is not closable by a guard
… handed over as issue #192* — which this branch makes half false. The two
halves come apart: not closable by a **guard** stays true, and the class is
closable by a **checker**. Rewriting only the hash would have left the
sentence standing.

So one row of the shared file is touched, and it is a re-read rather than an
append: the hash, the `Checked` cell, and a Notes paragraph saying where the
class went, what moved, and that the wrong-number direction the clause's last
sentence names is still open. `CLAUDE.md` §*a change writes fragments* forbids
appending to that file and permits touching it to leave the ledger true, which
is the same reason its removal exception exists.

**The records check earned its keep.** `evidence_check.py` refused three case
names in `spec.md`'s acceptance table — names that changed between the plan and
the code, in a file nothing else reads. All three were corrected and the table
now names the cases that shipped, which is the difference between a spec that
can be checked against the tree and one that reads as though it were.

**`fold_ledger.py --check` exits 1 on this branch and that is the correct
state.** The fragment is unfolded because the release that ships it has not
happened; CI runs that check only for a pull request whose base is `main`,
verified in `.github/workflows/hygiene.yml`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the claim in `seal/ledger.md` R3 that the class is not closed | the work item's own ledger fragment, which carries the closed claim, and that row's Notes cell, which points at it |
| three case names `spec.md` claimed the tree carries | nowhere — they never existed; the table now names the cases that do |
