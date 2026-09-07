# 1788826000-a-stamp-names-content-not-a-commit — questions

**No question was put to a person.** Routing arrived answered and committed, and
the ticket assigns both design questions to this work item to *answer and
argue* rather than to ask. What follows is the assumptions that were written
down instead, each with what it would take to overturn it.

## Answered by a document, so not asked

| # | What could have been asked | What answered it |
|---|---|---|
| A1 | Does a drifted rider fail the check or warn? | The ticket's own bound — *whatever replaces the SHA must be checkable the same way, a test seen red*. `evidence_check` exits 1 on drift, so a warning-only rider would be the looser of two rules about one thing |
| A2 | Should `Target SHA` move too? | The ticket asks for it to be answered in this change, not raised. It is answered in `spec.md` §*Question 2*, on measured grounds: `chain_check.py#reachable` already falls back to `refs/pull/<N>/head`, which a squash does not touch |
| A3 | Where does the rider machinery live? | `CLAUDE.md` and `plan.md` — `evidence_check.py` ships to other repositories through `/specseal:evidence-ci`, and riders are this repository's own convention. `.github/scripts/` is where this repository's own tooling already sits |

## Assumptions, written down

| # | Assumed | Overturned by |
|---|---|---|
| B1 | A rider block is the run of comment lines beginning at the `RIDER:` line. An unrelated comment butted against one with no blank line is absorbed into it | Somebody finding a real case where the absorbed lines mattered. The failure is a lost alarm, never a false one, so it is not worth mechanism today |
| B2 | The three riders nothing guarded (`fold_ledger.py`, two under `tests/`) belong under the check rather than outside it | Contract §12 makes the class this change's. If the repository owner wants `tests/` left out, the roots list is one line |
| B3 | `tests/test_the_records_can_be_carried_out_and_in.py:1415`, whose staleness line reads *green at 3f8f846, measured 2026-09-03*, is a rider that was never given a canonical stamp rather than a deliberate exception | Its own text — it is a `# RIDER:` block making a coordinate-tied claim, which is what the convention is. It is given a canonical stamp here |

## Left for a person, and named in the pull request

| # | Question | Who answers it |
|---|---|---|
| C1 | The quoted rider stamp inside `seal/specs/1788184145-…/rounds/round-2.md` still reads `Verified 2026-08-31 at f1cd65d`. It is a record of what a round observed, so by the same argument that exempts `Target SHA` it is left alone — but it is the one place the old string survives, and a future `grep` for the old form will find it | the repository owner |
