# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — phase 5

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-5.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 943651b8 |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

#551, filed by the orchestrating session from phase 3's Q5 finding and
added to this work item by the owner, in front of round 1's fix pass:
`--no-renames` on both `git diff --name-only` calls (`corrected`,
`whole_range`), so a renamed file is read as a deletion plus an addition and
the old path's sentences enter `wanted`; a case in probe 3's shape — a
forty-paragraph file moved with one sentence reworded, git reporting
`R09x`, its copy standing in another file — seen red first against the tree
as it stood, plus a case that a pure move stays silent; the docstring
paragraph saying why the silence comes from `wanted` now; the gate-table row
in `plan.md`; the four real-range cases re-run and any moved count pinned;
`spec.md` §Scope widened; a fragment row; a `changelog.md` entry; ledger row
U2's note updated; `overview.md` corrected; `--reverify` over what drifts.
Not to be touched: `rounds/`, and any commit at or below `6a424d81`.

## What this phase found

**Both cases were red for the same reason, `against 0 sentence(s)`.**
Executed 2026-09-24 against the script at `6a424d81`: the reworded rename at
exit 0 where 1 is owed, and the verbatim move silent with the removed count
at zero — which is the second case's own point. Each case asserts
`git diff --name-status` reports `R…` for its commit, so the fixture cannot
quietly fall under git's similarity threshold and become the delete-plus-add
shape the sweep already handled. Green after `--no-renames`; the module is
93 cases.

**No number moved on the four real ranges.** Re-run at `943651b8`: the same
coordinates as after phase 2 (4, 0, 8, 1 places) and the same
removed-sentence counts (60, 61, 35, 156), so none of the four squash
commits carried a rename that `--no-renames` now reads differently. The
branch's own sweep is unchanged too (exit 0, zero places, zero `unresolved`).

**`whole_range`'s arm has no case.** The same flag goes on its `changed`
list, so a file moved out of a work item's directory counts as touching it;
the mutation that removes the flag there stays green over the ownership
cases, because none of them moves a file. The arm is named here and in
ledger row R1 rather than pinned — a fixture that renames a file out of a
work item directory while declaring a range is a case the next reader can
add, and the failure direction of leaving it is a declaration refused as
`not yours` on a range that did touch its work item by a move, which prints
rather than silences.

**Mutations, executed at `943651b8` from Python, file restored
byte-identical:**

| Mutation | Cases run | Result |
|---|---|---|
| `corrected` without `--no-renames` | the two #551 cases | red (2 of 2) |
| `whole_range` without `--no-renames` | the ownership cases | green — no case moves a file, as above |

**Records.** Ledger row U2 keeps its claim as the measurement that found
the gap, with a note that R1 is the repair; eight `seal/ledger.md` rows on
`corrected` and `whole_range` take a phase 5 `Re-read` note and are
re-stamped; `overview.md`'s `Not verified` row for the issue is closed with
a mark, its `Not done` bullet is struck rather than deleted, and the
*inferred* clause under `Fed back` says the rename is read now.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sweep's silence on a file moved and reworded in one commit | nowhere — it was the defect; `spec.md` §Scope's `#551` row states the reading that replaces it |
