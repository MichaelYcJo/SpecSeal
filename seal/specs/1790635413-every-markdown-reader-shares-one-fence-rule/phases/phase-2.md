# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a031f605 |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the segment does not source that value from itself |

## What this phase was asked

`plan.md` phase 2: `gather_changelog.py#ungathered` and the `--check` count
read markers through `live_lines`, loaded as `fold_ledger.py` loads it, and
the module docstring says a marker counts only on a live line. Verified by
S6 and S7 in `tests/test_the_changelog_is_gathered_at_release.py`.

## What this phase found

- **The substring test was the wider hole.** `ungathered` read the inline
  shape too, which the count's line anchor already excluded. S6 is
  parametrized over three shapes (fenced, inline, commented), and all three
  were red against the substring test.
- **S6 as written left the count unpinned.** Every S6 shape fails at
  `ungathered` first, so a count mutation survived it. A fourth case,
  `test_a_quoted_marker_is_not_counted`, gathers for real and then quotes a
  marker in a fence and a comment; it was red against the old count
  (`4 work items marked` for 2) and is what kills the count mutation.
- **Lines are split with `splitlines()` here and `split("\n")` in
  `fold_ledger.py`.** Each matches the other reader of its own file:
  `survivor_check.py#gathered_fragments` splits `CHANGELOG.md` with
  `splitlines()`, and `fold_ledger.py`'s release files are split on `\n`
  alone for byte-for-byte reasons its docstring gives. S7 compares the gather
  with the survivor check by patching `read_blobs` to hand it the file, so
  the case needs no git repository.
- **Nothing in this tree changes answer.** `--check` reads 23 fragments and
  140 markers before and after, exit 0. `spec.md`'s five extra substring
  hits name no work item, as it assumed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
