# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — phase 1

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `ae0d276` |
| Ran by | specseal:smith on Opus 5 — the model the orchestrator chose at the spawn, filled in by the orchestrating session as the template requires |

## What this phase was asked

Build the signal: `.github/scripts/label_merged_on_release_branch.py` and its
workflow on push to `release/*`, importing the readers from
`close_issues_on_release` rather than writing a second copy. Create the label
if it is absent, add it, write nothing else. Verified by S1, S2 and S3 as
cases monkeypatching the module's own `run`, following
`tests/test_a_release_rolls_the_flow_measurement_issue.py`. Answer Q3 and Q6
here, before the script is trusted.

## What this phase found

**The frame holds, with one correction to `plan.md` §Technical context.** It
says `hygiene.yml` *already holds four release-only steps, each opening with
the same `if [ "${{ github.base_ref }}" != "main" ]` guard*. Three of them do
— the version bump, the changelog gather and the ledger fold. The fourth,
*wording this branch removed is not still standing elsewhere*, opens with the
**inverted** guard (`= "main"` → skip), because it runs on a pull request into
a release branch and not on one into `main`. So the shape phase 3's new step
copies is the three, and a reader who took the sentence at its word would
write a step that runs in exactly the wrong direction.

**Q6 stopped being load-bearing rather than being answered.** Whether adding
a label an issue already carries errors or is a no-op cannot be measured
without a write to the tracker, which this segment is not permitted to make,
and GitHub's REST documentation for *Add labels to an issue* does not say
(fetched 2026-09-11; it states only that the endpoint "adds labels to an
issue's existing labels", and lists no response for the duplicate case). So
the script reads first and adds only what is missing. The re-run guarantee S3
asks for then holds **by construction** instead of resting on an assumption
nobody has run, and
`test_an_issue_that_already_carries_the_label_is_left_alone` goes red the
moment the read is dropped — measured, not assumed.

**The same shape answers the label's own creation, and it is the difference
between green and red on every release after the first.** `gh label create`
on a name that already exists is an error rather than a no-op, so a script
that created unconditionally would fail every push after the first squash of
a release. The read is `gh label list --json name` over the whole set rather
than `GET /labels/{name}`: the name carries a space and a colon, and a
one-label read would turn on how those are encoded in a path.

**Q3 is not answerable from this segment, and the answer it needs is one
permission line.** Whether a job holding `permissions: issues: write` can
create a label with the default `github.token` needs either a real workflow
run or a label create, and both are writes. GitHub's documentation for the
Actions `issues` scope says only that it "permits an action to add a comment
to an issue" and does not enumerate labels (fetched 2026-09-11). What is
decided rather than assumed: the workflow declares
`contents: read` + `issues: write`, the smallest set that can reach the
Issues API at all, and the create path is reached at most once per release.
If the token turns out not to cover it, the failure is loud, at the create,
with the label name in the message — never a silent half-run. **This is the
first thing to watch on this branch's own squash**, which is the one real run
the plan asks for.

**Q7 is confirmed: import `close_issues_on_release` directly.** What the
signal needs from it is `MERGED_PR`, `keywords_in`, `pull_request_body`,
`arrived` and the 404-tolerant `_issue_api` — five of its readers, which is
most of the module. Extracting them would move `FENCE`'s `# RIDER:` anchor
and force a re-stamp on a comment whose subject is #266's open decision, for
no gain. Reaching for `_issue_api` by its private name is deliberate and is
commented where it happens: the two public wrappers beside it return a state
and a body, and the signal needs the label list out of the same 404-tolerant
read.

**The name mapping lives here, in the signal, and phase 2's gate imports
it.** `version_of`, `milestone_title`, `label_name` and `label_description`
are four spellings of one fact — branch `release/vX.Y.Z` → version `X.Y.Z` →
milestone `release: X.Y.Z` → label `merged: X.Y.Z` — and nothing checked the
chain before. It goes in the first of the two scripts to exist because both
scripts already take their readers from one source and a second mapping is
the same drift one layer over. The trade, stated because it runs the wrong
way: the gate is a reader and it will import a module that can write. What
keeps that safe is that the signal does nothing at module level but define
constants and functions, which is the property `round_record.py`'s guard case
already pins for itself.

**`release/*` is wider than `release/vX.Y.Z`.** The workflow's trigger cannot
be narrowed to the version shape — a glob matches path segments, not a
pattern — so `release/next` reaches the script. It names no version, and the
script says so and exits 0 rather than inventing one. Six branch shapes are
pinned as cases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
