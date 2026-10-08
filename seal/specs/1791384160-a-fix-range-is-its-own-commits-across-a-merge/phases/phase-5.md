# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | e43c3c27 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 5, the first phase of the redesign after round 3. Build the
shapes as cases: one new test module (its name the work's, Q7), with one case
per shape A, A2, B, B2, B3, C, D-branch and D-CI. Each case builds the history
the round reports' probes built, and asserts `own_commits`' list, plus
`touched`'s where the probe read it. Add shape D as a case of
`tests/test_a_fragment_left_behind_is_named.py`, on the branch and on
`ci_merge_ref`, with `judged`'s exit pin. See each case red under a mutation
of `own_commits` (`--ancestry-path` dropped, `--first-parent` added), and say
which mutation turned which case (S15, S17).

## What this phase found

**Every case matches its probe.** Each module case builds its history in a
repository it makes itself, and each returned what the round reports
recorded: A `{f1, S, f2}`; A2 `{f2}`; B `{f}`; B2 `{topic-fix}`; B3 nothing;
C `{f2}`; D `{f2}` on the branch and `{S, f2}` on CI's merge ref. `touched`
matched too. The cases compare sets of subjects, because commits made in one
second have no order git promises.

**Which mutation turns which case** (`bin/mutation-check` over
`own_commits`, executed):

| Case | `--ancestry-path` dropped | `--first-parent` added |
|---|---|---|
| A, a back-merge then a commit on the base | green | red |
| A2, the base merges a commit older than the start | red | green |
| B, a topic cut before the start, merged after | red | green |
| B2, a topic that merges the start and then commits | green | red |
| B3, a topic that commits and then merges the start | red | green |
| C, a branch cut from the base before it merged the start | red | green |
| D, from the branch and from CI's merge ref | green | red |
| S17, the notice on both checkouts | green | red |

Each case is red under one of the two, and each mutation turns at least one
case red. The fragment module's existing merge cases go red under one or both
as well.

**D is one case, not two.** On the branch, D's half is a straight line from
the start, and every reading of a range agrees on a straight line. Run on its
own, neither mutation turned it red. The branch and the merge ref are
therefore read in one case, which `--first-parent` turns red. S17 does the
same in the fragment module. This is a decision against the plan's eight-row
list, recorded in `overview.md`.

**S17 names the branch in `GITHUB_HEAD_REF` for the merge ref's run.** The
base has merged the branch, so it already holds the item's `routing.md`. The
diff against the base therefore adds no declaration, and on a detached HEAD
`chain_check` found none and never reached the arm. A workflow sets
`GITHUB_HEAD_REF`, so `check` and `judged` gained a `head_ref` argument, and
only that case passes one.

**Q7 is answered (a):** the shapes live in a module of their own,
`tests/test_a_range_owns_what_git_lists_for_it.py`. The close module's
fixture runs the generator, and these cases call `own_commits` and `touched`
directly.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
