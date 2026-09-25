# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 6d66fced |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#598 instance 1. One restoration predicate, asked by the reachability
decision in `main` and by `written_late`. The restored item's printed line
names the commit. Docstrings, the `docs/commit-review-gate-spec.md` row, and
a new `docs/review-chain-spec.md` row in the §*When the record was written*
table. The *what it costs* sentence of the delete and re-add row narrowed to
a restore within the branch. Cases B1 to B4, with B1 and B4 red on the
pre-phase code. Settle `questions.md` Q2 and list the call sites.

## What this phase found

**Q2: a `fork` argument.** `restored_from(root, fork, rel)` is the one
predicate. Two call sites, both in `main`, both passing the `fork` that
`main` already computes from `reader.merge_base`:

- the reachability decision, `restored = restored_from(root, fork, last) if last in touched else None`, which sets `refs` to None and chooses the printed line;
- `written_late(reader, root, args.baseline, record, fork)`, which asks it after `commissioned_fixes` and before `added_on_branch`, so an ordinary record with no fix verdict pays no extra `git log`.

A set computed once in `main` would have saved one `git log` for the last
record, which is asked twice when it names a fix. It would also have split
the definition between `main` and the function that reads it.

**`--full-history` is not in the predicate, and that was measured.** The
frame's command carried it. With the flag removed, every case stayed green.
A probe then built the shape where default simplification hides a side
line from a plain path-limited `git log`: a side line changes the record to
X, changes it back, and merges `--no-ff`. A plain `git log -- <rel>` listed
only the add, but `git log --find-object=<X> -- <rel>` listed both side
commits with or without `--full-history`. `--find-object` already walks
both parents. The flag had nothing behind it, so it came out, and
`test_bytes_the_base_held_only_on_a_merged_side_line_are_found` holds the
property.

**`--topo-order` stays, and needed its own shape to show why.** The commit
the line names is the last one git lists, which is the change the bytes
entered at. On a straight history the walk is already topological, so the
flag's mutation stayed green on B1 even with the add's clock ahead. It goes
red only where the retirement is a side line merged back and the add's
clock ran ahead. In date order the add is then listed first and the line
named the retiring commit, which does not carry the bytes.
`test_the_named_commit_is_where_the_bytes_entered_whatever_the_clock`
builds that shape.

**Seen red (§15), executed:**

| Case | Against | Result |
|---|---|---|
| B1 `test_a_record_restored_from_the_bases_history_makes_no_reachability_claim` | pre-phase code | red, exit 1, `not an ancestor of` |
| B2 `test_a_restored_record_the_pull_request_then_edits_is_its_own_claim` | pre-phase code | green, which is what it pins. Red under M8 below |
| B3 `test_a_restored_record_is_still_read_for_everything_else` | pre-phase code | red: the reachability error it asserts is absent was present |
| B4 `test_a_record_restored_from_the_bases_history_makes_no_claim` | pre-phase code | red, exit 1, `this record was ADDED by <restoring commit>` |

**Mutations, one at a time, restored from a copy kept outside the tree,
`tests/__pycache__` cleared between them (executed):**

| Mutation | Red |
|---|---|
| M1 `restored_from` returns None | B1, B3, B4, the clock case, the side-line case, the `--worktree` case |
| M2 `written_late` does not ask it | B4 |
| M3 `main` does not ask it for `refs` | B1, B3, the clock case, the side-line case, the `--worktree` case |
| M4 `--worktree` reads HEAD's blob | `test_a_restore_not_yet_committed_is_read_from_the_working_tree` |
| M5 the first line named instead of the last | B1, the clock case, the side-line case |
| M7 no `--topo-order` | the clock case |
| M8 `--find-object` dropped, so any commit touching the path counts | B2 |

**Narrow result, executed:** the four modules `plan.md` names, then every
module reading `chain_check.py`, `docs/review-chain-spec.md` or
`docs/commit-review-gate-spec.md` (41): 2285 passed, 8 skipped.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the unqualified *"a record accidentally deleted and restored after the fixes is refused"*, in `added_on_branch`'s docstring, the delete-and-re-add row of `docs/review-chain-spec.md`, and `test_a_record_deleted_and_re_added_after_the_fix_is_judged_on_the_later_add`'s docstring | the same three places, narrowed to a restore *within the branch*; a restore from the base's history is the new row beside it |
