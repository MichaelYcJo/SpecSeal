# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 66d39e30 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#529. `added_on_branch` passes `--full-history --topo-order`. Its docstring
gives the two reasons (simplification, S1; date order, S7) and the measured
answer that a merge is never an `A`. The `docs/review-chain-spec.md` delete
and re-add row says the reading holds across a merge and a skewed clock.
Cases A1 and A2, plus A3 if no existing case builds a merge. A1 red against
the current line and A2 red with `--full-history` alone, both shown here.

## What this phase found

**The test's own clock is a date tie, and a tie is A2's failure.** Built as
`spec.md` A1 describes it, with no dates, A1 stayed red under
`--full-history` alone. A probe printed why: every commit in the fixture
carries the same committer second (`1790298174`), so the date order has
nothing to separate the two adds and listed the early one first.

| Flags | `git log --diff-filter=A` over the undated A1 fixture |
|---|---|
| none | early add only |
| `--full-history` | early add, late add |
| `--full-history --topo-order` | late add, early add |

So A1 now dates the side branch ahead of the early add (`LATER`, 2099),
which is what a real side branch's clock does, and A2 dates it behind
(`EARLIER`, 2001). That separates the two members of the class: A1 is the
simplification alone and A2 is the order alone. Recorded in `overview.md`
as a divergence from `spec.md` A1's wording.

**Seen red (§15), executed:**

| Case | Against | Result |
|---|---|---|
| A1 `test_a_re_add_merged_back_from_a_side_branch_is_the_latest_add` | the pre-phase line (no history flag) | red, exit 0 where 1 was expected, neither add named |
| A2 `test_a_re_add_on_a_side_branch_with_an_older_clock_is_the_latest_add` | the pre-phase line | red, exit 0 |
| A2 | `--full-history` without `--topo-order` | red, exit 0 (A1 green there) |
| A3 `test_a_record_added_on_a_merged_side_branch_is_read_at_its_own_add` | the pre-phase line | green, which is what it pins |
| A3 | the phase's flags plus `--first-parent` | red: the merge commit was named as the add |

**Questions Q3:** no existing case builds a merge for `added_on_branch`. The
five merges in `tests/test_chain_check_at_the_pull_request.py` are
retirement fixtures (`git merge -q base` before removing a directory), and
none of them reaches `written_late`. So A3 is the new S3 case.

**Narrow result, executed:** `bin/test tests/test_a_record_precedes_the_fixes_it_commissions.py -q`
55 passed. Every module that reads a file this phase edits (38, found by
path and by basename, plus the review-chain-text readers,
`test_docs_line_wrap.py` and `test_a_folded_statement_names_what_enforces_it.py`):
2034 passed, 8 skipped, 1 failed. The failure was
`test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
because this work item had no `overview.md` yet. It is written in this
phase's commit, and the case passes.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `added_on_branch`'s docstring sentence *"`git log` prints newest first, so the FIRST line is the LATEST add"* | the same docstring, which now names the two flags that make it true |
