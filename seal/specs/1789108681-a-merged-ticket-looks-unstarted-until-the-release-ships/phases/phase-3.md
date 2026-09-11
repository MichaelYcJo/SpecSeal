# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — phase 3

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `a20c02c` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

The step in `hygiene.yml`, release-only and head-shape guarded, with the
comment block the file's other steps carry. Verified by S7 against each
non-release head shape, and by
`tests/test_ci_gives_the_checks_what_they_need.py` still being green.

## What this phase found

**It closed in the same commit as phase 2, and that is the honest record
rather than a shortcut.** A gate that is not wired into CI is not runnable,
which is what `plan.md` asks a phase to end with; splitting them would have
put a script in the tree that nothing calls and three cases that had to be
written and then rewritten. Both Status cells carry `a20c02c` and both records
say so.

**The frame's description of the step's shape is wrong in a way that would
have produced a step running in exactly the wrong direction.** `plan.md`
§Technical context says `hygiene.yml` *already holds four release-only steps,
each opening with the same `if [ "${{ github.base_ref }}" != "main" ]`
guard*. Measured: three do — the version bump, the changelog gather and the
ledger fold. The fourth, *wording this branch removed is not still standing
elsewhere*, opens with `if [ "${{ github.base_ref }}" = "main" ]` and skips,
because a release pull request's range is the union of every work item the
release carries and that is not a range any fix pass wrote. So the shape this
step copies is the three, and a reader taking the sentence at its word would
have written the inverted guard. This is the same finding phase 1 recorded;
it is repeated here because this is the phase that acted on it.

**The head-shape half of the guard is the script's rather than the step's,
and that is a decision rather than a convenience.** A shell condition on
`github.head_ref` would be untestable — nothing in this suite can run a
workflow step — while a skip inside the script is S7, six branch shapes as
parametrised cases. So the step guards only on the base and hands the head
over in `HEAD_BRANCH`.

**The step's own guard needed a stronger case than the one first written.**
Mutation-testing found it: deleting the guard's `exit 0` and its `fi`, leaving
`if …; then` with the run below it, left `test_the_gate_runs_only_for_a_
release_pull_request` green — and that mutation both runs the check on every
pull request and leaves malformed shell in the file. The case now matches the
whole guard in order: the condition, a body that exits, the `fi`, and the
script after it. That repair is `f137a21`, and it is what §15 buys that a
passing suite does not.

**`tests/test_ci_gives_the_checks_what_they_need.py` reads every workflow in
the directory, so phase 1's new file is inside it too.** Its
`test_a_pull_request_workflow_reruns_when_a_draft_becomes_ready` applies only
to workflows carrying `on: pull_request:`, and the signal's trigger is a push,
so it is exempt by construction rather than by an entry in a list. Executed:
green with both new files present.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hygiene.yml`'s absent `permissions:` block — the job used to inherit whatever an enterprise, organisation or repository default was | The block now stated at the top of the file, `contents: read` + `issues: read`, pinned by `test_the_job_asks_for_a_token_that_can_read_issues`. Nothing is lost: every step in the job reads, so the stated block is narrower than any default it replaced |
