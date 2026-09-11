# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — phase 2

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `a20c02c` |
| Ran by | unknown — the spawn prompt named no model for this segment; the orchestrator fills this row |

## What this phase was asked

Build the gate: `.github/scripts/release_completeness_check.py`, refusing on
`M \ D`, reporting `L ≠ D` by direction and `D \ M` without failing, with the
range taken from `git merge-base`. Verified by S4 **seen red first** against a
milestone claiming an item the branch does not carry, then S5, S6, S7 and S8.
Answer Q4 and Q5 here.

## What this phase found

**S4 was seen red against the live tracker, not against a fixture.** Run from
this branch with `HEAD_BRANCH=release/v0.11.1 BASE=origin/main`, the gate
exits **1** and prints:

```
::error::M \ D — the milestone 'release: 0.11.1' claims 1 open issue(s) this
release branch does not carry: #359. …
M (open in 'release: 0.11.1'): #351, #359
D (carried by this release branch): #351
L (carrying 'merged: 0.11.1'): #351
```

That is the correct answer and the reddest possible one: #359 is this work
item, the release branch does not carry it yet, and the release must not ship
until it does. The three passing paths were run the same way — a shipped
milestone (`release/v0.9.5`) exits 0 and reports `D \ L` and `D \ M`, a
hotfix head exits 0 with its reason, a milestone that does not exist exits 0
with its warning.

**A milestone that does not exist is a hole the frame did not name, and it is
the one direction a checker of claims must not fail in.** Executed:
`gh issue list --milestone "release: 9.9.9" --state open --json number`
returns `[]` and **exits 0**. So a mistyped or absent milestone would make the
whole gate pass by measuring an empty set — a check that cannot fail. The gate
now reads `repos/{repo}/milestones?state=all` first and, when the title is
absent, prints `this run verified NOTHING` and passes. Passing rather than
failing, for the reason `D \ M` was rejected on: a release nobody scheduled is
a person's call, not this gate's. What it must not be is silent, and a case
pins the sentence.

**Q4 is answered by removing the question rather than by measuring the
default.** What token `hygiene.yml` gets with no `permissions:` block comes
from an enterprise, organisation or repository setting nobody here has read,
and GitHub's own documentation says only that "the permissions for the
`GITHUB_TOKEN` are initially set to the default setting for the enterprise, <!-- NAME NOT IN TREE: GitHub's own name for the token a workflow run is given, quoted verbatim from their reference. Nothing in this tree spells it — the workflows here pass `${{ github.token }}` into `GH_TOKEN`, which is what `gh` reads. Paraphrasing the quote to remove the name would make it a claim about GitHub's documentation rather than a reading of it. -->
organization, or repository" (read, fetched 2026-09-11). So the block is
stated: `contents: read` and `issues: read`. Every step in that job reads and
none writes, so the block is **narrower** than any default it could have been
inheriting — the change cannot make an existing step fail for want of a scope,
which is what made it safe to take in this work item rather than in one of its
own. `GH_TOKEN: ${{ github.token }}` goes on the step rather than being left
to whatever the runner has.

**Q5 is answered and it decided which command reads M.** `gh issue list`
excludes pull requests and the REST `/issues` endpoint does not — executed, on
this repository: `gh api "repos/<repo>/issues?state=all&per_page=6"` returns
#359, **#358**, #357, **#356**, **#355**, #354 with the three bold ones
carrying a `pull_request` key, while `gh issue list --state all --limit 6`
returns #359, #357, #354, #353, #351, #350 and `gh pr list --state all
--limit 3` returns exactly the three that went missing. It matters because a
pull request carrying the milestone could never carry `merged: X.Y.Z`, so it
would sit in `M \ D` and block the release with nothing anybody could do about
it. No pull request in this repository carries a milestone today, which is why
the question was measured on the general property rather than on an instance.

**Q8 is confirmed: the range is the fork point.** `origin/main..HEAD` and
`$(git merge-base origin/main HEAD)..HEAD` give the same set today and come
apart the moment a hotfix that was also merged into the release branch moves
`main` during a release's life. The merge-base form is what "what this release
accumulated since it was cut" means, and a case pins the exact two commands
rather than the resulting set, because the resulting set is equal under every
history this repository currently has.

**`L` is read in every state, and reading only the open ones would blame the
signal for a person's edit.** An issue somebody closed by hand mid-release
still carries the label the signal put on it; dropping it from `L` puts it in
`D \ L`, which reads as *the signal missed one*. Its own case, and the
mutation that flips `--state all` to `--state open` turns that case red.

**`judge()` is pure, so all four directions are cases rather than runs.** The
only thing that needs the fake tracker is the wiring above it — which command
each set is read with, and the range `D` is read over.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
