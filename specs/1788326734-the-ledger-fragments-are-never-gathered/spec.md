# Feature Specification: the ledger fragments fold at release

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/spec.md — WHAT
this work delivers and how we'll know. `docs/one-root-by-lifetime.md` outranks
this file; it is cited, not restated. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §"What happens at a release", step 1 | the fragment `.specseal/map/<id>.md` folds into `.specseal/map.md` at the release-preparation step and is removed; a move, never a deletion; an unmerged work item keeps its fragment |
| the same section, step 3 | the release step refuses while any released work item has an open `evidence-todo.md` row, naming the item |
| the same document, "Why the rows fold rather than stay" | the fragment layout exists to stop two branches queueing at one file, and after the merge there is no branch left to queue |
| the same document, §"The dependency rule", "Kept on purpose" | the evidence-todo guard is a sanctioned reader of `specs/<id>/` after the merge — it is the proof that nothing permanent lives only in the work item |
| `docs/branch-and-release.md`, "The release branch merges into `main` as a merge commit, carrying one commit of its own" | the fold belongs in that same release-preparation commit, and the "Release preparation runs:" block is where the command is documented |
| `docs/review-handoff-protocol.md` §"evidence-todo.md" | one row per fact; the reviewer writes the file and the implementer merges each fact into the fragment |
| issue #78 "Done when" | both halves work on today's paths, so this lands before the root merge (#79) and the root merge only re-points them |

## Scope

**In.**

- A release-preparation script, `.github/scripts/fold_ledger.py`, beside
  `gather_changelog.py` and shaped like it: `--version X.Y.Z` writes,
  `--dry-run` prints, `--check` verifies, `--root` for tests, exit 0 done and
  exit 1 for anything a release pull request should stop on.
- The evidence-todo guard inside that script, and the rule that says what an
  open row is (below), written so a person can apply it by hand.
- A `--check` step in `.github/workflows/hygiene.yml`, on pull requests into
  `main` only, the way the changelog check runs.
- Every document that says the ledger fragments are never gathered, or that
  says where a work item's rows go, corrected to what is now true: rows go in
  the fragment during development and the release folds them into `map.md`.
- Tests for the script, in the shape of
  `tests/test_the_changelog_is_gathered_at_release.py`.

**Out.**

- The root merge (#79). Paths in this work are today's: `.specseal/map.md`,
  `.specseal/map/<id>.md`, `specs/<id>/evidence-todo.md`.
- `settle` (#83), which folds a work item's SDD set into `docs/`. The guard
  written here is the one `settle` will reuse, and nothing else of it.
- Merging folded rows into `map.md`'s existing areas by topic. The fold is a
  concatenation, the way the changelog gather is; where a row belongs by area
  is a judgment, and a release step that makes judgments is one nobody trusts
  to run unattended.
- Running the fold on this repository's own fragments. That is the 0.4.0
  release-preparation commit's act, not this branch's.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 every row survives the fold | Given `.specseal/map.md` and two fragments under `.specseal/map/`, when `fold_ledger.py --version 0.4.0` runs, then every table row of every fragment is in `map.md` byte-identical, and every fragment file is gone | test: rows compared as strings; `os.path.exists` on each fragment |
| S2 a fold is marked, not matched | Given a fold has run, then `map.md` carries `<!-- specs/<id> -->` above each work item's rows, and a fragment that is present while its marker is already in `map.md` refuses the fold naming it, nothing written | test |
| S3 the fold is ordered and idempotent | Given fragments with ids in either filesystem order, then the folded sections are in id order; a second run with nothing left exits 1 and says so | test |
| S4 an open evidence-todo row refuses the whole fold | Given a work item whose `evidence-todo.md` has an open row (rule below), when the fold runs, then it exits 1 naming `specs/<id>/evidence-todo.md`, `map.md` is byte-identical and every fragment is still there | test |
| S5 a drained file is not open | Given an `evidence-todo.md` with rows and a `drained` line, or with every row marked ✅, or with a header and no body row, or no file at all, then the fold runs | test, one case per shape |
| S6 the checker's result is unchanged by a fold | Given a tree whose rows all resolve, then `evidence_check.py` reports the same ok · drifted · broken totals before and after the fold | test on a fixture; executed by hand on a copy of this repository's own ledger and recorded in the fragment |
| S7 `--dry-run` writes nothing | Given fragments to fold, when `--dry-run` runs, then the section is printed, `map.md` is unchanged and every fragment is still there | test |
| S8 `--check` is what the release pull request runs | Given a fragment left under `.specseal/map/`, or an open evidence-todo row, then `--check` exits 1 naming it; given neither, it exits 0 and says how many work items are marked in `map.md`, so a run that looked at nothing cannot pass | test; `hygiene.yml` carries the step gated on `base_ref == main` |
| S9 the documents say the new rule | Given the documents that used to say *never gathered*, then none of them says it, and the release sequence in `docs/branch-and-release.md` names the fold beside the gather | test over the document list |
| S10 an empty fragment is removed and named | Given a fragment with no content under its title, then the fold removes it, prints that it was empty, and writes no section for it | test |

## The rule for an open evidence-todo row

Applied to every `specs/*/evidence-todo.md` in the tree. A person can run it
by eye; the script runs the same steps.

1. **A file that does not exist has no open row.** A work item that never had
   facts to merge never wrote one.
2. **A line outside a table whose first word is `drained` closes the whole
   file**, wherever it stands — above the table, as
   `specs/1788272986-…/evidence-todo.md` writes it, or below, as
   `specs/1788277657-…/evidence-todo.md` does. The word is matched
   case-insensitively at the start of the line, after any leading `*`, `_`
   or whitespace, so `**drained**` counts and `not drained` does not.
3. **Otherwise every table body row is open unless its first cell begins
   with ✅.** A table is a run of consecutive lines starting with `|`; the
   first line is the header when the second is a separator (`|---|---|`),
   and neither of those two is a body row. The ✅ form mirrors
   `overview.md`'s Not verified table, where a row is closed by marking it
   and never by deleting it.
4. **A file with a header and no body row is not open.** Nothing was ever
   prescribed.

So a file with rows and no `drained` line is open, which is the case the
design record's guard exists for, and both files in the tree today are
closed by rule 2.

**Which work items.** Every one whose directory is in the tree when the
release-preparation step runs. That step runs on a branch cut from the
release branch, and a branch holds only merged work; an unmerged work item
is on its own branch and is not in this tree at all. So "every released work
item" and "every work item present" name the same set, and the script reads
the tree. A work item released in an earlier version whose file was never
drained blocks this release too, by design: the guard is about what the tree
holds, and the remedy is to drain the file, which is one commit on the
release branch.

## Data & interfaces

**`fold_ledger.py`**

| Flag | Does |
|---|---|
| `--version X.Y.Z` | fold: append `## X.Y.Z — <date>` to `.specseal/map.md` with one section per fragment, remove the fragments, remove `.specseal/map/` if it is empty afterwards |
| `--date YYYY-MM-DD` | the date in the heading (default today, UTC) |
| `--dry-run` | print the section, write and remove nothing |
| `--check` | exit 1 naming every fragment still under `.specseal/map/` and every open evidence-todo file; exit 0 with the count of work items marked in `map.md` |
| `--root PATH` | the repository root (default: this one) |

Neither `--version` nor `--check` is an error, the way `gather_changelog.py`
refuses it.

**What a folded section looks like.** Under one release heading, each
fragment becomes its marker, a `###` heading carrying the work item id (the
fragment's own `#` title, demoted), then the fragment's text with every
heading demoted by two levels so the fragment's `## area` sections sit as
`####` under the work item. Table rows are copied byte for byte; nothing
inside a table is touched.

```
## 0.4.0 — 2026-09-15

<!-- specs/1788229400-every-branch-appends-to-the-same-two-files -->
### 1788229400-every-branch-appends-to-the-same-two-files

Rows for the work item that closed #46 and #52.

#### A coordinate names content, not a position

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| … | … | … | … | … |
```

The section is **appended** at the end of `map.md`, where the changelog
gather inserts at the top. A changelog is read newest-first and a section
that lands low reads as older than what shipped; a ledger is read by area
and by coordinate, and its top holds the notation rules a reader needs
before any row. Nothing measures from the position of a row — the checker
scans the file for anchors and reads no headings — so the order is for
people, and people read the rules first.

**Exit codes.** 0 done · 1 for each of: nothing to fold, an open
evidence-todo row, a fragment whose marker is already in `map.md`, a
fragment left at `--check`, `.specseal/map.md` missing. All are failures a
release pull request should stop on.

**What the checker sees.** `evidence_check.py` reads `.specseal/map.md` and
`.specseal/map/*.md` and scans each for `path#unit@hash` anchors without
reading tables or headings (`check_ledger`). A row moved between the two
files is the same anchor in a different file. One thing can change the
totals: the checker de-duplicates on `(coordinate, hash)` within one file,
so two rows citing one unit at the same hash in a fragment and in `map.md`
count twice before the fold and once after. That is one row counted twice
becoming one row counted once, and no finding changes; S6 records whether
this repository's ledger has such a pair.

## Open questions → questions.md

Anything a planner must answer lives in `questions.md`, not inline.
