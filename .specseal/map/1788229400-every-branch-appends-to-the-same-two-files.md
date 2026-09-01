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

## Verdicts the checker reports

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|

## The changelog fragments

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A fragment counts as gathered when its marker comment is in `CHANGELOG.md`, never by matching its text | `.github/scripts/gather_changelog.py:46-70` | **Executed**: re-wording a released entry leaves `--check` green, and deleting the marker turns it red | 2026-09-01 | Matching the text works exactly once — the first copy-edit to a released entry would reopen its fragment forever |
| Gathering is idempotent and ordered by work item id | `.github/scripts/gather_changelog.py:51-96` | **Executed**: a second run exits 1 with the entry present once, and the earlier id sorts above the later one in the written section | 2026-09-01 | The id is unix seconds, so the order is chronological and, more to the point, does not depend on the filesystem |
| The release pull request fails while a fragment is ungathered, and no other pull request runs the check | `.github/workflows/hygiene.yml:64-67` | Read, not run — the branch condition is the same shape as the version-bump step above it at `:30`. The script's own two directions are executed | 2026-09-01 | On a feature pull request every fragment on the branch is legitimately ungathered, which is why the step skips itself |
