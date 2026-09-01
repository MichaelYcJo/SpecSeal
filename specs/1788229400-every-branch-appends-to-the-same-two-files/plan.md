# Implementation Plan: every branch appends to the same two files

## Summary

Three things, in dependency order. The blame baseline (A) is what makes a
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
  **uncommitted**, so blame cannot answer for it and it goes on exercising the
  header fallback without an edit.

**What breaks in six months.** Blame answers for the row's LINE, so an edit
that only re-words a Notes cell moves the baseline forward without anybody
re-reading the code. The `Checked` date is what makes that visible: a row read
in August and re-worded in September still says August, and a reader comparing
the date against `git log` sees the gap. This is written into the ledger
header and the skill so it is a known limit rather than a discovery.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A row's baseline comes from `git blame`** | An unrelated edit to the row moves the baseline forward silently; the `Checked` date is the only thing that shows it | **chosen** — the only option where no rewrite can orphan the baseline, because nothing is written down to be orphaned |
| Re-stamp after the squash, by machine | A workflow writing to the release branch, which takes changes only through pull requests — so it needs a ruleset exception or an auto-PR. Both are new machinery that can fail silently | rejected: it repairs the damage rather than removing the cause, and the repair is what #49 already did by hand |
| Stamp `refs/pull/<N>/head` | The ref does not exist until the pull request opens, and stamps are written during the work. A late re-stamp pass is needed anyway, at which point the row above did the job | rejected |
| Keep the manual re-stamp, name it in the merge sequence | A step nobody owns, discovered each time by a red test | rejected — it is issue #52's own "accept it" row |
| **A changelog fragment marked in the released file by an HTML comment** | The marker is invisible to a reader and can be deleted by hand, which makes the fragment look ungathered and fails a release pull request loudly | **chosen** — the failure direction is a red build on a release, not a silent double-entry |
| Match a fragment's text verbatim against `CHANGELOG.md` | Any later copy-edit to a released entry makes its fragment read as ungathered, forever | rejected |
| Delete a fragment once gathered | `specs/` is the permanent record of a work item; deleting the entry loses the link between an entry and the work that produced it | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `row_baseline` resolves from `git blame` when the row carries no SHA; the header note stops claiming drift was skipped when it was not | `tests/test_a_row_measures_from_its_own_history.py`, plus the two existing evidence-check suites green | |
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
