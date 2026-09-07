# 1788761915-a-record-states-what-nothing-reads — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `b821e7c` |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

`seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`. Verified by the
fragments and `fold_ledger.py --check`.

## What this phase found

**Writing the ledger fragment is what found the arm's last defect, and it
found it by making the arm wrong about this very work item.** A fragment is
the work item writing about itself — same branch, same author, same lifetime
as the records beside it — and the name corpus was reading it. Naming
`header_of`, `row_baseline`, `_correction_traces` and <!-- NAME NOT IN TREE -->
`test_ledger_stamps_resolve` in R1's notes put all four into the corpus and <!-- NAME NOT IN TREE -->
silenced four refusals in this work item's own `phase-2.md`. A work item could
clear the check on its records by naming the unit in its own ledger file.
`seal/ledger/` is excluded now. `seal/ledger.md` is not, and the line between
them is lifetime — the same line the boundary is drawn on, and the fold moves
a fragment across it at the release, which is the same moment the work item
stops being live.

**The marker example in the skill was doing the same thing one file over.**
Phase 3 wrote *`chain_module` deleted and its one call site moved* into <!-- NAME NOT IN TREE -->
`skills/code-review/SKILL.md` as the worked example, which put `chain_module` <!-- NAME NOT IN TREE -->
back into the tree the check compares against — so the four occurrences phase
2 had gone red on would have passed with their markers reverted, and phase 3's
correction stopped being load-bearing. The example uses an invented name now
and says why.

**A name in any other file is a name the tree has, and that is the claim
rather than a hole in it.** The check says nothing outside the records carries
the name, and a document naming it is a place a reader can find it. The two
cases above are what that costs, and both are closed by not writing a real
gone name into a document.

**Five `seal/ledger.md` rows are re-pointed rather than removed.** Phase 4
moved the anchor loop out of `check_ledger` into `check_text`, and five rows
whose claim is about that loop cited the old unit — an edit falsifying a row
by moving the content out from under it, which is `CLAUDE.md`'s one exception
to the fragment rule. Nothing was removed and no claim changed. The two rows
whose claim is about `check_ledger` itself — a ledger nobody can read is
reported, and every ledger path a person reads goes through `display_name` —
were left where they are.

**Eight `seal/ledger.md` rows were re-read before the re-verify, not
re-stamped blind.** Their claims are unchanged: the axes table's OS-boundary
sentence and the 🟡/⬜ threshold in `## Findings format`, the two opt-in
headings in `docs/review-chain-spec.md`, `new` deriving every field row, the
reopening subsection, the header case, and the fix pass's own past
measurement anchored on `main`.

**This work item's own records carry the marker, in an HTML comment.**
Its own `spec.md`, `plan.md` and phase records name `some_helper`, <!-- NAME NOT IN TREE -->
`chain_module` and the four spot-checked units on purpose, and its `plan.md` <!-- NAME NOT IN TREE -->
carries the fixture stamp `mod.py#helper@deadbeef`. An HTML comment keeps the <!-- NAME NOT IN TREE -->
marker out of the rendered prose and the reader still meets it in the diff;
the checker reads raw lines, so it works.

**`fold_ledger.py --check` and `gather_changelog.py --check` both exit 1, and
that is the correct state.** Three fragments are unfolded — this work item's
and the two earlier ones on this release branch — and both checks run only for
a pull request into `main`. On a feature pull request every fragment on the
branch is legitimately ungathered.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `chain_module` as the marker's worked example in `skills/code-review/SKILL.md` | an invented name, with the reason beside it — and this record, which is where the reason a real name may not be used there is written down | <!-- NAME NOT IN TREE -->
