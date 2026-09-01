# 1788229400-every-branch-appends-to-the-same-two-files

Rows for the work item that closed #46 and #52. **No baseline header, and no
SHA in a Checked cell** — both are what this work item removed. Every row below
measures from the commit `git blame` names for its own line, and the Checked
column carries the date somebody read the code.

## A ledger row's baseline

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A row with no SHA measures from the commit blame names for its line, and a row that wrote one still measures from that | `skills/evidence-check/scripts/evidence_check.py:120-176` | **Executed.** A fragment row with no SHA drifts after the cited file changes, and reads OK when it has not. A row naming an earlier commit still drifts against it, so the stamp is not being overridden | 2026-09-01 | The four-argument call is unchanged, so `tests/test_ledger_stamps_resolve.py` goes on asking only what the row wrote |
| A squash cannot orphan the baseline | `skills/evidence-check/scripts/evidence_check.py:83-118` | **Executed**, twice. In a fixture: a feature branch writes the row and the code, squashes into `main`, the branch tip stops being an ancestor, and the row still reads OK. On this repository: `git merge-base --is-ancestor 9b5501d origin/main` exits 1, while blame of `.specseal/map.md` attributes 20 lines to `e7ff924`, #48's squash commit | 2026-09-01 | `e7ff924` is the value #49 wrote into seven cells by hand. That repair is the thing this row makes unnecessary |
| Blame is read in `--porcelain` because the other forms decorate a boundary commit | `skills/evidence-check/scripts/evidence_check.py:107-115` | **Executed** on this tree: `git blame -s HEAD -- .specseal/map.md` answers `^9829412`, and porcelain answers the plain SHA with `boundary` on a metadata line of its own. `grep -c '^\^'` over the porcelain output returns 0 | 2026-09-01 | The first line of every fragment is a boundary line, so this is the ordinary case. `git cat-file` is asked before the answer is used either way |
| A line nobody has committed blames as the all-zero SHA and is dropped | `skills/evidence-check/scripts/evidence_check.py:114` | **Executed**: appending an uncommitted row to a fragment and calling `blame_lines` returns no entry for it, and the integration case falls back to the header baseline | 2026-09-01 | Handing that name to `git diff` answers "nothing changed", which is a pass produced by a failure |
| A fragment with no baseline header is checked row by row rather than reported as skipped | `skills/evidence-check/scripts/evidence_check.py:349-356` | **Executed**: a fragment whose cited file changed reads DRIFTED and exits 1, and `drift check skipped` is not printed. The message is kept for a ledger git has never seen | 2026-09-01 | This is what makes the fragment convention possible at all — before it, a headerless ledger passed by measuring from nothing |

## The changelog fragments

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A fragment counts as gathered when its marker comment is in `CHANGELOG.md`, never by matching its text | `.github/scripts/gather_changelog.py:46-70` | **Executed**: re-wording a released entry leaves `--check` green, and deleting the marker turns it red | 2026-09-01 | Matching the text works exactly once — the first copy-edit to a released entry would reopen its fragment forever |
| Gathering is idempotent and ordered by work item id | `.github/scripts/gather_changelog.py:51-96` | **Executed**: a second run exits 1 with the entry present once, and the earlier id sorts above the later one in the written section | 2026-09-01 | The id is unix seconds, so the order is chronological and, more to the point, does not depend on the filesystem |
| The release pull request fails while a fragment is ungathered, and no other pull request runs the check | `.github/workflows/hygiene.yml:64-67` | Read, not run — the branch condition is the same shape as the version-bump step above it at `:30`. The script's own two directions are executed | 2026-09-01 | On a feature pull request every fragment on the branch is legitimately ungathered, which is why the step skips itself |
