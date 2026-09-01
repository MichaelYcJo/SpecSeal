# Implementation Plan: every branch appends to the same two files

## Summary

Three things, in dependency order. The derived baseline (A) is what makes a
ledger fragment possible (B), because a fragment with no header has no
baseline of its own. The changelog half (C) shares the fragment shape and
nothing else.

## Technical context

- `skills/evidence-check/scripts/evidence_check.py:77-96` — `row_baseline()`
  scans the row's line for a SHA that resolves and returns `None` otherwise.
  `check_ledger` then falls back to `find_baseline()`, the ledger header's.
- `:99-115` — the baseline is used for exactly one thing:
  `git diff --unified=0 <baseline>..HEAD -- <path>`, judged on the diff's OLD
  side. It is a diff base, never an identity, which is why a commit that
  merely CONTAINS the row's line is a correct answer.
- `:238-242` — the default globs already include `.specseal/map/*.md`, so the
  checker reads fragments today. Confirmed by running it against a throwaway
  fragment before any of this was written.
- `tests/test_ledger_stamps_resolve.py` reads `.specseal/map.md` for stamps
  and asserts each resolves and is an ancestor of HEAD. Rows written under the
  old rule keep theirs, so it keeps having something to read.
- `tests/test_evidence_check_hardening.py:104` writes its ledger fixture
  **uncommitted**, so the derivation cannot answer for it and it goes on
  exercising the header fallback without an edit.
- The file is read from the WORKING TREE and `git log -L` counts lines in a
  commit, so one `git blame --porcelain` maps working-tree line to
  (commit, line-in-that-commit) and the walk starts there. Without that
  anchor an uncommitted insertion above a row shifts every number below it.

**What breaks in six months.** A row can be stale the moment it lands — two
branches, one citing lines the other changed, the other merging first — and no
derived baseline sees it, because the row's first appearance already contains
the other change. The written stamp caught that noisily and by accident rather
than by design. Recorded as Q1 in `questions.md` with issue #31 named, because
closing it means checking the coordinate against the code it cites rather than
against a diff window.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A row's baseline is the commit it FIRST APPEARED in** (`git log -L`, oldest entry) | A row written on one branch citing lines another branch changed, where the second merges first, reads clean while its coordinate was stale on arrival — Q1 in `questions.md` | **chosen** — no rewrite can orphan it, because nothing is written down to be orphaned, and a bulk rewrite does not reset it |
| A row's baseline is the commit that LAST TOUCHED its line (one `git blame`) | Any commit rewriting rows en masse pulls every one forward to itself. Measured: later than the written stamp on all 36 rows, never equal, never earlier, and one release commit holding 16 of the 36 | rejected on the numbers — a strictly narrower window than the stamps it replaces, with nothing re-read to earn it. It is 26× cheaper (17 ms against 455 ms for 36 rows) and the cost falls only on rows with no stamp |
| Re-stamp after the squash, by machine | A workflow writing to the release branch, which takes changes only through pull requests — so it needs a ruleset exception or an auto-PR. Both are new machinery that can fail silently | rejected: it repairs the damage rather than removing the cause, and the repair is what #49 already did by hand |
| Stamp `refs/pull/<N>/head` | The ref does not exist until the pull request opens, and stamps are written during the work. A late re-stamp pass is needed anyway, at which point the row above did the job | rejected |
| Keep the manual re-stamp, name it in the merge sequence | A step nobody owns, discovered each time by a red test | rejected — it is issue #52's own "accept it" row |
| **A changelog fragment marked in the released file by an HTML comment** | The marker is invisible to a reader and can be deleted by hand, which makes the fragment look ungathered and fails a release pull request loudly | **chosen** — the failure direction is a red build on a release, not a silent double-entry |
| Match a fragment's text verbatim against `CHANGELOG.md` | Any later copy-edit to a released entry makes its fragment read as ungathered, forever | rejected |
| Delete a fragment once gathered | `specs/` is the permanent record of a work item; deleting the entry loses the link between an entry and the work that produced it | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `row_baseline` derives the baseline from the row's own line history when it carries no stamp; a SHA a row names in prose is not a stamp; the header note stops claiming drift was skipped when it was not | `tests/test_a_row_measures_from_its_own_history.py`, plus the two existing evidence-check suites green | |
| 2 | The fragment convention: `.specseal/map/<work-item-id>.md` with no header, `.specseal/map.md`'s header says what it now is, and every document that stated the old stamp rule is corrected | the same new test file, reading the documents | |
| 3 | `.github/scripts/gather_changelog.py` with `--check`, wired into the release pull request; `## Unreleased` retired; the documents that told a change to edit `CHANGELOG.md` corrected | `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_release_hygiene.py` | |
| 4 | Dogfood: this work item's own changelog fragment and ledger fragment, the stale follow-up row removed, the closing memo | `bin/evidence-check .`, the new suites | |

## Operational impact

- **The release sequence gains a step.** Release preparation runs
  `python3 .github/scripts/gather_changelog.py --version X.Y.Z` instead of
  renaming `## Unreleased` by hand. `docs/branch-and-release.md` carries it.
- **A release pull request gains a check.** `hygiene.yml` fails a pull request
  into `main` that leaves a changelog fragment ungathered.
- **No migration of existing data.** Rows already stamped keep working; the
  entries already in `CHANGELOG.md` are already released.
