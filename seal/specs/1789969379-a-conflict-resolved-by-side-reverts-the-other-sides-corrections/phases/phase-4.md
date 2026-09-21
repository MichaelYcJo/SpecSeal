# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | e5776914 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The wrapper in `bin/` and the CI leg, plus M2's measurement that the merges
are reachable where the leg runs. A9, and M2 recorded — with a negative
answer moving the leg rather than dropping it, and a divergence row in
`overview.md`.

## What this phase found

**M2 is yes, in both directions, and the measurement is two cases rather
than a sentence.** The shape that matters is #424's own: a feature branch
merging its release branch in and resolving by taking a side. Built as a
fixture, that merge is reachable from the commit a `pull_request` job
actually sits on — which is the MERGE ref, the head already merged into the
base, not the head commit — and the check reports the dropped correction
there. Squash the branch into its release branch and the same range holds no
merge at all; the check says so and exits 0. Nothing moved, and the leg's
placement now rests on a run.

**The merge ref is the part that could have made the answer no, and reading
it wrong would have been invisible.** `git merge-base origin/main HEAD` from
a `pull_request` checkout answers the base tip rather than the fork point,
which `.github/workflows/hygiene.yml` already carries a comment about two
steps further down (#359, round 1). The fixture builds the merge ref rather
than checking out the head, so the measurement is about the commit the leg
will really be standing on.

**The leg skips a pull request into `main`, and the reason is not the
survivor step's.** That one skips because a release range is the union of
every work item it carries, which is a range no fix pass ever writes. This
one skips because a release branch carries **squashed** commits rather than
its work items' merges — so the range there holds merges of `main` back into
the release branch, a different question, and every work item was already
read at its own pull request. Same skip, different argument; the comment in
the workflow says which.

**It blocks, which is Q2's default and needed no answer to proceed.** Every
other arm of the hygiene workflow blocks, a lost correction is silent by
construction, and A3 is what keeps it off correct work. Q2 stays open for the
owner to overturn; nothing waits on it.

**`templates/hygiene.yml` does not gain the leg**, and that is a decision
rather than an omission. That template carries five steps, not fourteen — it
has no survivor step either — so it ships the subset a new repository needs
rather than a mirror of this one's workflow. `overview.md` §*Not done* has
the row.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
