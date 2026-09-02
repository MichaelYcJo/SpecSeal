# the ledger fragments fold at release — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show; each part written when it happened. -->

📋 implement applied
· spec:     `docs/one-root-by-lifetime.md` §"What happens at a release" (steps 1 and 3), §"The dependency rule", §"What does not change"; `docs/flow.md`; `docs/branch-and-release.md` (the release-preparation bullet and the "Release preparation runs:" block); `docs/review-handoff-protocol.md` §"evidence-todo.md"; issue #78; `.specseal/follow-up.md` (empty)
· evidence: 8 rows in `.specseal/map/1788326734-the-ledger-fragments-are-never-gathered.md`
· verified: executed — the fold test file (36 cases) and a five-mutation run in which every mutation turned at least one case red; the fold on a copy of this repository's own ledger with `evidence_check.py` before and after; the scope run (nine test files, 117 cases). Read — `hygiene.yml`'s step gated like the changelog step; the design record's "unmerged keeps its fragment" against what a branch cut from the release branch can hold

## Why this work exists

Every work item wrote `.specseal/map/<id>.md` and nothing folded it back, so
the directory grew by one file per work item forever; after this a release
moves those rows into `map.md` and refuses while a reviewer-verified fact is
still waiting outside the ledger.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the folded section lands | the model, `gather_changelog.py`, inserts above every dated section; the fold appends at the end | append | a ledger is read by area and its top holds the notation a reader needs first; `check_ledger` scans the file for anchors and reads no headings, so nothing measures from the position. `questions.md` Q2 |
| What `--check` verifies | the changelog check looks for fragments only; the fold's check also runs the evidence-todo guard | both | a fold done by hand still meets the guard at the release pull request, the last moment anyone is looking. `questions.md` Q3 |
| "any released work item" (design record) vs "any work item" (ticket) | the record says an unmerged item is not part of the release | every `specs/*/evidence-todo.md` in the tree | the step runs on a branch cut from the release branch, which holds merged work only, so the two sets are the same; a work item released earlier whose file was never drained blocks too. `spec.md` §"Which work items", `questions.md` Q1 |
| Checker totals before and after a fold | `spec.md` S6 asks for identical totals | 141 ok → 140 ok on this repository's ledger, no finding changed | `check_ledger` de-duplicates on `(coordinate, hash)` per file, and `skills/code-review/scripts/chain_check.py#main@fd1525ae` is cited by both `map.md` and the `1788272986-…` fragment; two files counted it twice, one file counts it once. Pinned by `test_the_one_thing_a_fold_changes_is_a_duplicate_counted_once` |

## Not verified

| Item | Who must answer |
|---|---|
| The hygiene step on a real pull request into `main` — the step is read against the changelog step's shape and its script is executed, but no release pull request has run it | the repository owner, at the 0.4.0 release pull request |
| The fold as part of an actual release-preparation commit on this repository — executed on a copy of the tree at `72cf296`, not on the release branch | the repository owner, at 0.4.0 release preparation |

## Not done

- The fold was not run on this branch's own fragments. That is the
  release-preparation commit's act; running it here would empty
  `.specseal/map/` before the other 0.4.0 work items are merged.
- `.specseal/map.md`'s `## Coordinates` and area headings were not
  restructured to receive folded rows by area. The fold concatenates, on
  purpose (`spec.md` §"Out").
- `settle` (#83) was not started; the guard here is written so it can be
  reused there.

## Fed back into the spec

- The four-step rule for an open `evidence-todo.md` row, in `spec.md` and in
  `docs/branch-and-release.md` — *inferred during implementation* from the two
  files in the tree and the handoff protocol's one-row-per-fact shape. A
  planner may replace it with a status column; the script reads `drained` and
  ✅ and nothing else.
- Every work item in the tree is "released" at release-preparation time —
  *inferred*, from where the step runs.
