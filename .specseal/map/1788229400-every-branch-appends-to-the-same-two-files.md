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
| A row with no stamp measures from the commit it first appeared in, and a row that wrote one still measures from that | `skills/evidence-check/scripts/evidence_check.py:310-383` | **Executed.** A fragment row with no stamp drifts after the cited file changes and reads OK when it has not. A row naming an earlier commit still drifts against it, so the stamp is not being overridden | 2026-09-01 | The four-argument call is unchanged, so `tests/test_ledger_stamps_resolve.py` goes on asking only what the row wrote |
| First appearance, not the commit that last touched the line | `skills/evidence-check/scripts/evidence_check.py:214-279` | **Executed** on this repository's 36 coordinates: last touch is later than the written stamp on all 36, equal on none, earlier on none. One release commit that rewrote stamps in bulk holds the baseline for 16 of them under last touch and for none under first appearance. Wall clock 455 ms for 36 rows against 17 ms for a single blame | 2026-09-01 | Last touch would have been a strictly narrower drift window than the stamps it replaces, with nothing re-read to earn it. The bulk-rewrite failure is not new — the written stamp has it too — but last touch widens the trigger from an edited stamp to any edit of the line |
| A commit that rewrites rows in bulk does not reset their baselines | `skills/evidence-check/scripts/evidence_check.py:214-279` | **Executed**: a fragment row drifts, its Notes cell is re-worded in a commit that reads nothing, and it still drifts | 2026-09-01 | The cheapest possible version of a bulk rewrite. Under last touch the re-word alone cleared it |
| A squash cannot orphan the baseline | `skills/evidence-check/scripts/evidence_check.py:153-212` | **Executed**, twice. In a fixture: a feature branch writes the row and the code, squashes into `main`, the branch tip stops being an ancestor, and the row still reads OK. On this repository: `git merge-base --is-ancestor 9b5501d origin/main` exits 1, so a fresh clone sees the old stamps as broken | 2026-09-01 | That is the state a repair pull request fixed by hand, which is the step this row removes |
| A row moved out of a ledger that stays loses its history, so a migration carries stamps forward verbatim | `skills/evidence-check/scripts/evidence_check.py:214-279` | **Executed** against git rather than the checker: a ledger keeps one row and gives another to a new file, and in the new file the row's history begins at the move. A whole-file rename is different — git detects and follows that, and the first version of the fixture did it by accident | 2026-09-01 | This is why `.specseal/map.md` is not migrated by this work item, and the rule for whenever it is |
| A SHA a row names in prose is not its baseline, and not the ledger's | `skills/evidence-check/scripts/evidence_check.py:63`, `:81-118`, `:281-308` | **Executed**, found by running the checker against this fragment: it reported drift against a commit reachable in one clone only. A row's baseline now needs a date and a SHA together, and the header scan stops above the first row that cites code | 2026-09-01 | Both halves were live at once — the row read its own prose, and the header scan read into the rows. Q2 in `questions.md` holds what is left: prose in a header is still read as a baseline |
| Blame is read in `--porcelain` because the other forms decorate a boundary commit, and because it maps working-tree lines to commit lines | `skills/evidence-check/scripts/evidence_check.py:153-212` | **Executed** on this tree: `git blame -s HEAD -- .specseal/map.md` answers `^9829412`, porcelain answers the plain SHA with `boundary` on its own metadata line, and `grep -c '^\^'` over the porcelain output returns 0 | 2026-09-01 | The first line of every fragment is a boundary line, so this is the ordinary case. The line mapping is what keeps the history walk correct when the ledger has uncommitted edits above a row |
| A line nobody has committed blames as the all-zero SHA and is dropped | `skills/evidence-check/scripts/evidence_check.py:199-206` | **Executed**: appending an uncommitted row to a fragment and calling `blame_lines` returns no entry for it, and the integration case falls back to the header baseline | 2026-09-01 | Handing that name to `git diff` answers "nothing changed", which is a pass produced by a failure |
| A fragment with no baseline header is checked row by row rather than reported as skipped | `skills/evidence-check/scripts/evidence_check.py:590-600` | **Executed**: a fragment whose cited file changed reads DRIFTED and exits 1, and `drift check skipped` is not printed. The message is kept for a ledger git has never seen | 2026-09-01 | This is what makes the fragment convention possible at all — before it, a headerless ledger passed by measuring from nothing |

## Verdicts the checker reports

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A row reads DRIFTED when its range was touched since the row's own baseline | `skills/evidence-check/scripts/evidence_check.py:604-614` | **Executed**: a fragment row whose cited file changed after its baseline prints DRIFTED and exits 1 | 2026-09-01 | Moved here from `.specseal/map.md`, where it cited `:202` before this work item relocated that code. Re-anchoring it in place left a row whose derived baseline is the repository's FIRST commit — 299 lines of a file the row cites at 604 — so its tripwire was dead. A new line in a new file does not have that problem |
| A row carrying two distinct commits as stamps is measured from the widest of them, not skipped | `skills/evidence-check/scripts/evidence_check.py:574-620` | **Executed**: one stamp gives DRIFTED and exit 1; adding a second stamp in an earlier cell used to give AMBIGUOUS and exit 0, and now gives DRIFTED, exit 1, with both stamps named | 2026-09-01 | Skipping the comparison made a second stamp a way to silence a real finding, and CI runs without `--strict` |
| Two spellings of one commit are one stamp | `skills/evidence-check/scripts/evidence_check.py:86-100`, `:350-386` | **Executed**: `<sha>[:7]` and `<sha>[:11]` in one row read as one stamp and the row's drift still reports | 2026-09-01 | Dedup ran on the matched string. A ledger repaired by hand is where mixed lengths occur |
| A declared baseline is found wherever it sits in the header; an accidental prose SHA only near the top | `skills/evidence-check/scripts/evidence_check.py:173-216` | **Executed**: a `Baseline commit` row at char 2728 is read, and a SHA at char 2734 of a rationale paragraph is not | 2026-09-01 | The header baseline is the fallback for every row the derivation cannot anchor, so an unbounded prose scan turned an honest UNMEASURED into a measurement against whatever a paragraph mentioned |
| A cross-repo row needs the original's baseline declared in the header | `skills/evidence-check/scripts/evidence_check.py:588-601` | **Executed** on a migration-shaped ledger: `1 unmeasured` with `--strict` exit 2 carrying one baseline, `1 ok` and exit 0 carrying both | 2026-09-01 | Committing the ledger line — the remedy the UNMEASURED verdict names — does nothing for such a row, because this repository's commits are not a diff base in the original |

## The changelog fragments

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A fragment counts as gathered when its marker comment is in `CHANGELOG.md`, never by matching its text | `.github/scripts/gather_changelog.py:46-70` | **Executed**: re-wording a released entry leaves `--check` green, and deleting the marker turns it red | 2026-09-01 | Matching the text works exactly once — the first copy-edit to a released entry would reopen its fragment forever |
| Gathering is idempotent and ordered by work item id | `.github/scripts/gather_changelog.py:51-96` | **Executed**: a second run exits 1 with the entry present once, and the earlier id sorts above the later one in the written section | 2026-09-01 | The id is unix seconds, so the order is chronological and, more to the point, does not depend on the filesystem |
| The release pull request fails while a fragment is ungathered, and no other pull request runs the check | `.github/workflows/hygiene.yml:64-67` | Read, not run — the branch condition is the same shape as the version-bump step above it at `:30`. The script's own two directions are executed | 2026-09-01 | On a feature pull request every fragment on the branch is legitimately ungathered, which is why the step skips itself |
