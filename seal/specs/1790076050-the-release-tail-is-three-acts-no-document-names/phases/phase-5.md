# 1790076050-the-release-tail-is-three-acts-no-document-names — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `c5c35693` |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The fragments. `seal/specs/<work-item-id>/changelog.md`, and a
`seal/ledger/<work-item-id>.md` row for each fact this work settled by opening
code. Verified by `gather_changelog.py --check` and `evidence_check.py
--strict .` at the broad gate, which is the sealer's single run.

## What this phase found

### The ledger fragment was written in phase 4, not here

`plan.md` puts both fragments in phase 5. The ledger rows could not wait: phase
4 removed `seal/ledger.md`'s R2, and a removed row whose claim has nowhere to
go is a claim that left the repository. So
`seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`
was written and stamped inside phase 4's commit, in the same commit as the
removal. What this phase carries is the changelog fragment and the closing
memo.

That follows the skill's own cadence rather than departing from it — *write
the rows you have been keeping, and let that write ride the commit that closes
the phase*. The rows were kept across phases 1 to 4 and written once. Phase 5
existing as a separate row in `plan.md` is what made it look like a later act.

### The fragment directory did not exist

`seal/ledger/` was absent from the worktree before this work item — the 0.13.0
release folded the last fragment away and git keeps no empty directory. The
first fragment recreates it, which is the state
`docs/release-checklist.md` §3's table already records having caught once, from
the other direction.

### `gather_changelog.py --check` reports the fragment as ungathered

Which is correct and is the state a feature branch is supposed to be in: the
fragment exists and `CHANGELOG.md` carries no marker for it, because gathering
happens at the release. The check names the file and prints the command that
gathers it. The hygiene workflow runs the same check on every pull request into
`main`, where that state would be a failure; into a release branch it is not.

### What deliberately earned no ledger row

The release-note workflow and the directory command are pinned case for case
by their own modules, so a row per arm would be an inventory of the diff. The
three rows that exist are judgments a later tidy-up would undo in good faith: a
delegation that looks like indirection (T3), an invariant that looks like it
was simply relaxed (T1), and a claim about a document that a reader cannot
check without the tracker in front of them (T2). The fragment's header comment
says this, so the absence is a decision rather than a gap.

### Verification run here

- `evidence_check.py .` unscoped — **1452 ok · 0 drifted · 0 broken · 0
  external · 0 old-format**, up from 1440 at the branch point (R2's two
  anchors out, the fragment's fourteen in).
- `unverified_check.py --baseline origin/release/v0.13.1 seal/specs/` — exit
  0, this work item's `overview.md` read as **5 open · 0 closed**.
- `gather_changelog.py --check` — names this fragment, as above.
- `tests/test_the_set_a_work_item_always_has.py`,
  `test_unverified_rows_close.py`,
  `test_the_changelog_is_gathered_at_release.py`,
  `test_the_ledger_fragments_fold_at_release.py` — 209 passed.

The broad gate is not run here and is not this segment's (`agent-contract`
§2); `overview.md` carries it labelled `unverified` with the sealer named.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
