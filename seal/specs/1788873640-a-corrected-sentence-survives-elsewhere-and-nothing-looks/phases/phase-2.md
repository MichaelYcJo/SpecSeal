# 1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 23066d4 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Put the check where the act happens, and give it the escape `plan.md`
designed. From the task: it runs unattended, so it belongs where CI or `bin/`
reaches it; and the escape for a false positive must be named and must not be
*turn it off*, because a shared sentence two documents are supposed to carry is
the common case in this tree.

## What this phase found

**Where it runs is the ticket, not a detail of it.** #269's second clause is
that the walk which would have caught the defect ran in a reviewer's clone and
left with it. So a check nothing in the tree invokes is that walk again, and
three carriers name it now — the fix-pass procedure, the smith's own verify
step, and the pull request.

**The fix pass needs no new argument.** `round_record.py close --range <a>..<b>`
already takes the fix range, so the step costs one command and no derivation.
That is worth saying in the prose, because a second range somebody has to work
out is a step that gets skipped.

**No review round can be the home.** Contract §2 reserves the broad gate for
the orchestrator, which is exactly why #269's pin sat red from the commit that
reworded the sentence through two rounds and two gates. The one party that
could run it is the one that wrote the fixes.

**The CI step fails where the two steps beside it only print, and the
difference was measured rather than argued.** `issue_claims_check.py` and the
README-pair step deliberately never fail, on the grounds that a red build for a
false positive stops a release. So this step owed a measurement. Run at the
range each pull request actually had — `origin/release/v0.9.2...<branch>`, not
a base the branch had already merged past:

| Branch | Reports |
|---|---|
| `chore/228-…` | 0 |
| `fix/203-204-205-206-…` | **1** |
| `feat/167-…` | 0 |
| `test/209-210-…` | 0 |

One report over four real merged pull requests, and it is `seal/ledger.md` row
R3 carrying a claim a docstring had corrected — a defect that shipped and
became #267. A step whose one report over four pull requests is true can
afford to fail.

**The measurement also produced a fact worth handing on**: that row is still
standing in the tree today. It is not this work item's to fix — #267's own
second open item is that `CONTRIBUTING.md` §House rules does not name the case
of correcting a false note in a `seal/ledger.md` row that has not drifted, and
two branches have already had to decide it without a written rule. It is named
in `overview.md` and in the pull request body instead.

**Two defects in the escape were found by running it rather than reading it.**
The emptiness refusal counted the rows collected *so far*, so a second
`--exempt` naming an empty file passed on the strength of the first one's rows.
And a run where every survivor was excused printed *no removed wording is still
standing* — false, and it makes the exemption rows above it read as something
other than what silenced the run.

**One shell detail, because `set -e` is not worth recalling to read a
workflow.** The exemption glob matches nothing on most branches, so the loop
runs once with the pattern itself as its value; whether `set -e` forgives a
failing test at the tail of an `&&` list is a rule the step should not depend
on a reader knowing. It is an `if`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — wrappers, prose and a workflow step are all additions | none |
