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
| 1 | `row_baseline` derives the baseline from the row's own line history when it carries no stamp; a SHA a row names in prose is not a stamp; the header note stops claiming drift was skipped when it was not | `tests/test_a_row_measures_from_its_own_history.py`, plus the two existing evidence-check suites green | `1dc2531`, corrected to first appearance in `9a7ce62` |
| 2 | The fragment convention: `.specseal/map/<work-item-id>.md` with no header, `.specseal/map.md`'s header says what it now is, and every document that stated the old stamp rule is corrected | the same new test file, reading the documents | `22b3690`, re-stated in `9a7ce62` |
| 3 | `.github/scripts/gather_changelog.py` with `--check`, wired into the release pull request; `## Unreleased` retired; the documents that told a change to edit `CHANGELOG.md` corrected | `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_release_hygiene.py` | `9cc7aaf` |
| 4 | Dogfood: this work item's own changelog fragment and ledger fragment, the stale follow-up row removed, the closing memo | `bin/evidence-check .`, the new suites | `9a7ce62`, closed by the commit after it |
| 5 | Review round 1: ten findings — the rejected reading in four documents, the case that missed them, a renamed ledger, a row with no baseline, a manufactured stamp, the dead header cut, the `## Unreleased` carriers, the missing gather instruction, three cases a stub satisfied, and two tidy-ups | `tests/test_a_row_measures_from_its_own_history.py` and `tests/test_the_changelog_is_gathered_at_release.py`, each new case seen red against the pre-fix tree | `b1291b1` · `aacae56` |
| 6 | Review round 2: the re-anchored row moves to the fragment and no stamp is written anywhere; a second stamp stops swallowing a real drift; two spellings of one commit are one stamp; a prose header is bounded again while a declaration is not; the migration two-baseline remedy, the `--help`/workflow verdict lists and the rejected-reading assertion | `tests/test_a_row_measures_from_its_own_history.py`, each new case seen red against the pre-fix tree; the squash simulation for the two 🔴 | `efe1946` · onward |
| 7 | Review round 3: the two-stamp ordering and the abbreviation dedup gain guards that can fail, and the shipped `--strict` sentence stops contradicting the verdict table beneath it | `tests/test_a_row_measures_from_its_own_history.py`, with four mutations run against the four ledger files | `2d56812` |
| 8 | **The rule changed rather than being reconciled.** A coordinate names content — `path#anchor@hash` — instead of a line number, so the baseline, the stamp, the two extra verdicts and the two rules that forbade each other are deleted rather than corrected. `evidence_check.py` drops from 747 lines to 372 and imports no `subprocess` | the 51 real coordinates migrated with a faithfulness report, four proofs, and 13 mutations against `tests/test_a_row_points_by_content.py` | `0ac6997` · `2e2533a` · `76ee764` · `2df35f4` |
| 9 | The anchor gains a second level: a **major** unit that can be BROKEN and an optional **minor** anchor that can only narrow the hash, plus a parser-free unit rule so the design is not Python-only. Markdown sentence anchors become heading paths | 22 mutations over every resolver branch, the widening proof, and a TypeScript fixture for the generic rule | `31b4990` · `33fe38b` |
| 10 | On BROKEN the destination is named when provable — same-file rename, then repo-wide graded by evidence (hash beats name, name alone never fixes) — and `--reverify` re-anchors what reconstruction proves, whole-file renames included. A post-commit advisory arm prints the same lines at the commit that broke them | each grade seen red first; 8 scan mutations and 3 hint/re-anchor mutations, all killed; the advisory confirmed to inherit the hints | `1caf1d5` · `92af060` |
| 11 | A 0.1.0 ledger is loud, never invisible: `OLD-FORMAT` fails the run with or without `--strict`, and `--migrate` ships the same enclosing-unit migration this branch ran on its own 51 coordinates, leaving and naming what it cannot prove | today's silent `0 ok` pinned as the failing expectation first; idempotence and the all-or-nothing row pinned; 6 mutations, all killed | |

## Operational impact

- **The release sequence gains a step.** Release preparation runs
  `python3 .github/scripts/gather_changelog.py --version X.Y.Z` instead of
  renaming `## Unreleased` by hand. `docs/branch-and-release.md` carries it.
- **A release pull request gains a check.** `hygiene.yml` fails a pull request
  into `main` that leaves a changelog fragment ungathered.
- **No migration of existing data.** Rows already stamped keep working; the
  entries already in `CHANGELOG.md` are already released.
