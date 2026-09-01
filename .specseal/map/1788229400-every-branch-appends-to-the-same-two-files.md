# 1788229400-every-branch-appends-to-the-same-two-files

Rows for the work item that closed #46 and #52. **No baseline header**, which
is what a fragment does without: every row in it measures from the commit it
first appeared in.

The rows citing `evidence_check.py` carry a stamp all the same, and they are
what showed why one is still needed. They were written when the fragment was
created and rewritten when the design changed to first appearance — so their
lines first appear at the earlier commit, while the code they cite moved at the
later one, and all four read DRIFTED. Re-reading them changes nothing on its
own, because the derivation walks past an edit to the row. The stamp in each
Checked cell is the assertion that the row was re-read at that commit, and it
wins over the derivation.

**A fragment's prose names no commit.** A commit named in a header is read as
the file's baseline — which is how this file twice reported drift against a
commit only one clone can resolve, the second time in the paragraph explaining
the first. Two things now hold it: the run prints where a baseline came from,
and an accidental prose SHA is only read near the top of a header while a
declared one is read wherever it sits.

**No row here carries a stamp, and that is the rule rather than an omission.**
A stamp naming a commit this branch made stops resolving at the squash, and
the paragraph that once licensed it was wrong about the code: an EDITED row
walks back to its original commit, not to the squash. So a row whose
coordinate a branch invalidates is removed from `.specseal/map.md` and written
afresh here, where it is a new line whose first appearance is the squash
commit itself.

Rows may name commits in prose freely. A row's baseline has to be a date and a
SHA together, so a bare hex word in a row is inert, and a row carrying two
distinct commits as stamps is still measured — from the widest of them — with
the disagreement reported beside the verdict.

## A ledger row's baseline

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The baseline is the commit a row first appeared in; a stamp it wrote still wins | `skills/evidence-check/scripts/evidence_check.py:388-461` | **Executed.** A fragment row with no stamp drifts once the cited file changes and reads OK when it has not; a row naming an earlier commit still drifts against that commit | 2026-09-01 | The four-argument call is untouched, so `tests/test_ledger_stamps_resolve.py` still asks only what the row wrote |
| First appearance, not the commit that last touched the line | `skills/evidence-check/scripts/evidence_check.py:283-348` | **Executed** across this repository's 36 coordinates: last touch is later than the written stamp on all 36 and one release commit holds 16 of them, against none by first appearance | 2026-09-01 | Last touch would be a strictly narrower window than the stamps it replaced, with nothing re-read to earn it |
| A commit that rewrites rows in bulk does not reset their baselines | `skills/evidence-check/scripts/evidence_check.py:283-348` | **Executed**: a fragment row drifts, its Notes cell is re-worded in a commit that reads nothing, and it still drifts | 2026-09-01 | The cheapest possible bulk rewrite. Under last touch the re-word alone cleared it |
| A squash cannot orphan the baseline | `skills/evidence-check/scripts/evidence_check.py:218-281` | **Executed** in a fixture: a branch writes the row and the code, squashes into `main`, its tip stops being an ancestor, and the row still reads OK | 2026-09-01 | The state a repair pull request once fixed by hand, which is the step this removes |
| A row moved out of a ledger that stays loses its history, so a migration carries stamps forward verbatim | `skills/evidence-check/scripts/evidence_check.py:283-348` | **Executed** against git rather than the checker: a ledger keeps one row and gives another to a new file, and in the new file the row's history begins at the move. A whole-file rename is different, and git follows that | 2026-09-01 | Why `.specseal/map.md` is not migrated wholesale, and the rule for whenever it is |
| A SHA a row names in prose is not its baseline, and not the ledger's | `skills/evidence-check/scripts/evidence_check.py:72`, `:129-171`, `:350-386` | **Executed**, found by running the checker against this fragment: it reported drift against a commit reachable in one clone only. A row's baseline needs a date and a SHA together, and the header ends above the first row that cites code | 2026-09-01 | Both halves were live at once — the row read its own prose, and the header scan read into the rows |
| Blame is read in `--porcelain` for the boundary spelling, the line mapping and the path | `skills/evidence-check/scripts/evidence_check.py:218-281` | **Executed**: `git blame -s` answers `^9829412` where porcelain answers the plain SHA with `boundary` on its own line, and `grep -c '^\^'` over porcelain output returns 0 | 2026-09-01 | The first line of every fragment is a boundary line. The line mapping keeps the history walk correct under uncommitted edits, and the path keeps it correct after a rename |
| A line nobody has committed blames as the all-zero SHA and is dropped | `skills/evidence-check/scripts/evidence_check.py:262-272` | **Executed**: appending an uncommitted row to a fragment and calling `blame_lines` returns no entry for it, and the row falls back to the header | 2026-09-01 | Handing that name to `git diff` answers "nothing changed", a pass produced by a failure |
| A fragment with no baseline header is checked row by row rather than reported as skipped | `skills/evidence-check/scripts/evidence_check.py:657-667` | **Executed**: a fragment whose cited file changed reads DRIFTED and exits 1, and `drift check skipped` is not printed | 2026-09-01 | What makes the fragment convention possible at all — before it, a headerless ledger passed by measuring from nothing |

## Verdicts the checker reports

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A row reads DRIFTED when its range was touched since the row's own baseline | `skills/evidence-check/scripts/evidence_check.py:604-614` | **Executed**: a fragment row whose cited file changed after its baseline prints DRIFTED and exits 1 | 2026-09-01 | Moved here from `.specseal/map.md`, where it cited `:202` before this work item relocated that code. Re-anchoring it in place left a row whose derived baseline is the repository's FIRST commit — 299 lines of a file the row cites at 604 — so its tripwire was dead. A new line in a new file does not have that problem |
| A row carrying two distinct commits as stamps is measured from the widest of them, not skipped | `skills/evidence-check/scripts/evidence_check.py:574-620` | **Executed**: one stamp gives DRIFTED and exit 1; adding a second stamp in an earlier cell used to give AMBIGUOUS and exit 0, and now gives DRIFTED, exit 1, with both stamps named | 2026-09-01 | Skipping the comparison made a second stamp a way to silence a real finding, and CI runs without `--strict` |
| Two spellings of one commit are one stamp | `skills/evidence-check/scripts/evidence_check.py:86-100`, `:350-386` | **Executed**: `<sha>[:7]` and `<sha>[:11]` in one row read as one stamp and the row's drift still reports | 2026-09-01 | Dedup ran on the matched string. A ledger repaired by hand is where mixed lengths occur |
| A declared baseline is found wherever it sits in the header; an accidental prose SHA only near the top | `skills/evidence-check/scripts/evidence_check.py:173-216` | **Executed**: a `Baseline commit` row at char 2728 is read, and a SHA at char 2734 of a rationale paragraph is not | 2026-09-01 | The header baseline is the fallback for every row the derivation cannot anchor, so an unbounded prose scan turned an honest UNMEASURED into a measurement against whatever a paragraph mentioned |
| Both branches of the two-stamp ordering are guarded, and each independently | `tests/test_a_row_measures_from_its_own_history.py:508-538`, `:540-587` | **Executed**, four mutations. `return shas[0]` turns both cases red; deleting the date fallback alone turns exactly the second red; disabling the ancestry branch alone turns exactly the first red; as shipped, 64 pass | 2026-09-01 | The finding was that the ordering had no guard at all — `return shas[0]` left all 62 cases green, and that is the choice round 2's 🔴 4 exists not to trust |
| Two spellings of one commit are told apart on an UNTOUCHED row, not a drifted one | `tests/test_a_row_measures_from_its_own_history.py:476-506` | **Executed**: reverting the dedup to the matched string leaves a drifted row reading DRIFTED either way, so the old case could not fail; on an untouched row the readings differ, `1 ok` against `AMBIGUOUS` | 2026-09-01 | Since a drifted ambiguous row reports DRIFTED, the `AMBIGUOUS` string never appeared for the old assertion to catch. Both fixtures exit 0, so the verdict is asserted rather than the exit code |
| A cross-repo row needs the original's baseline declared in the header | `skills/evidence-check/scripts/evidence_check.py:588-601` | **Executed** on a migration-shaped ledger: `1 unmeasured` with `--strict` exit 2 carrying one baseline, `1 ok` and exit 0 carrying both | 2026-09-01 | Committing the ledger line — the remedy the UNMEASURED verdict names — does nothing for such a row, because this repository's commits are not a diff base in the original |

## The changelog fragments

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A fragment counts as gathered when its marker comment is in `CHANGELOG.md`, never by matching its text | `.github/scripts/gather_changelog.py:46-70` | **Executed**: re-wording a released entry leaves `--check` green, and deleting the marker turns it red | 2026-09-01 | Matching the text works exactly once — the first copy-edit to a released entry would reopen its fragment forever |
| Gathering is idempotent and ordered by work item id | `.github/scripts/gather_changelog.py:51-96` | **Executed**: a second run exits 1 with the entry present once, and the earlier id sorts above the later one in the written section | 2026-09-01 | The id is unix seconds, so the order is chronological and, more to the point, does not depend on the filesystem |
| The release pull request fails while a fragment is ungathered, and no other pull request runs the check | `.github/workflows/hygiene.yml:64-67` | Read, not run — the branch condition is the same shape as the version-bump step above it at `:30`. The script's own two directions are executed | 2026-09-01 | On a feature pull request every fragment on the branch is legitimately ungathered, which is why the step skips itself |
