# 1788661274-the-roll-names-the-next-version-by-guessing — phase 1

<!-- seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `deab74c` — the phase is `bcd870c` (the fork settled), `f5e60c0` (the condition and the title), `deab74c` (the case a mutation asked for), on `9b9cc6f` |
| Ran by | |

## What this phase was asked

Settle `plan.md` §Alternatives before the first edit — three rows, a failure
scenario and a verdict each — then build the winner. Then the condition: the
roll fires when the version the open issue names has shipped, not on every
push to `main`, and a run with nothing to roll exits 0, says so, and leaves
both logs alone. Replace the docstring's *a title a human can retitle by hand*
paragraph with what the script now does. Ship both exit lines with the cases
that pin them.

Bounded to `.github/scripts/roll_flow_measurement_issue.py` and its own suite.
The one-open invariant and its single retry were named out of scope, and are
untouched; closed issues are not retitled, so what the old titles mean is
said in the change instead.

## What this phase found

**The three alternatives are not three ways of doing one thing, and settling
the table meant saying so.** Row 1 — parse the version out of the open log's
title — is not a rival to the other two. It answers *where does the condition
read the open log's version*, and there is exactly one answer:
`gh issue list --label flow-measurement --state open --json number,title`
returns a number and a title, and no version exists anywhere else. So every
condition reads the title, whichever title convention wins, and row 1 is
adopted for the condition alone. Rows 2 and 3 are the actual fork.

**What is chosen with row 1 is the direction of the unreadable case, and that
is where the design is.** Reading the title makes a title editable-by-accident,
and the two answers are not symmetric. *Not due* stops the log forever with the
workflow green — the same class as the bug being fixed, one step over, which is
the failure `plan.md` names to design against. *Due* costs at most one roll
that was not owed. So a title this script cannot read as its own is due, and
one rule then covers three things: an old-convention title, a title somebody
tidied, and the migration.

**Row 2 won on the clause `spec.md` already cites.** At the moment the roll
runs, `docs/branch-and-release.md` says whether the next number is a minor or
a patch is known at the end rather than at the cut. So the next version is the
one thing nobody knows and the just-shipped one is the one thing certain, and
row 3 — keep predicting, roll only once confirmed — names the unknown one
anyway. Its failure is the stall: ship a version the prediction did not name
and never ship the predicted one (`0.9.0` predicted, `1.0.0` shipped) and
every release afterwards prints *nothing due* forever. It also fails #155's
third *Done when* head-on, because a prediction that cannot be made has to say
so instead of being made.

**The cheaper shape lost, and it was cheaper.** Row 3 is what the existing
fixtures support: every case in the module expects `chore: flow measurement —
0.8.0` out of a `0.7.0` tree, so row 3 would have added the condition and left
all eighteen green. Row 2 rewrote the expected title, body or recovery version
in five of them and deleted a sixth with the function it covered. That was a
real input to the verdict and it is recorded in the table rather than left to
be discovered. A cheaper set of edits does not make a guess knowable.

**The divergence from `spec.md`, both texts.** `spec.md` §User scenarios, row
1: *"A patch release rolls nothing — Given the open log names a version the
tree has not shipped · when the roll runs · then it exits 0, says nothing was
due, and closes no issue."* What was built: a patch release **does** roll, and
the run that closes nothing is *a push that shipped no new version*. The
scenario is written in row 3's frame, where the title is a prediction and a
patch release is the case that must not fire; under row 2 the log a patch
release closes is named after the version before it and holds exactly the work
that patch shipped, so closing it loses nothing and the 0.8.1 incident does not
recur. The scenario's substance — a run that shipped no new version closes
nothing and says so — is kept and pinned by
`test_a_push_that_shipped_no_new_version_rolls_nothing`. Its literal example is
reachable only through the migration and through a title edited by hand, and in
both of those rolling is the correct act; both are pinned too. `spec.md` is
left as written: rewriting an acceptance row to match what was built is how a
spec stops being worth reading. **The reviewer is the one who settles this**,
and it is the one judgment in this phase that a person may want to overturn.

**`plan.md`'s phase 1 Verified-by cell said *every existing case still green*,
and that was written before the fork was settled.** It is now amended to say
which cases change and why, because the winner renames what the roll writes.
Every one of the eighteen is accounted for: five changed
(`test_one_open_issue_after_the_retry_succeeds`,
`test_one_open_issue_closes_it_and_opens_the_next`,
`test_every_attempt_failing_still_exits_loudly`,
`test_the_body_drops_the_ledger_clause_where_no_durable_log_exists`,
`test_close_succeeds_but_open_fails_names_both_in_the_message`), one deleted
with the function it covered, twelve untouched.

**Every ladder fixture in the module carries an old-convention title, and that
is now load-bearing.** `OPEN_ONE` is `chore: flow measurement — 0.7.0`, which
states no version the roll can read, so it is always due and every existing
case still reaches the roll it is about. The module docstring says so, because
a later session tidying those fixtures into the new convention would silently
turn a dozen cases into no-ops.

**Two mutations survived the first loop, and both were in `rolled_from`.**
Answering the whole title where the marker is absent, and `""` where the marker
is there with nothing after it, left all 24 cases green — its only caller is a
comparison, so a wrong answer that is also unequal to the shipped version still
reads as due. The gap opens at a title that happens to BE a version string,
which the first mutation reads as the log for that version: not due, stalled,
workflow green. `test_rolled_from_reads_only_the_title_the_roll_itself_writes`
pins the pure function directly, and both mutations now kill it by name.

**What phase 2 has to carry.** Neither `skills/verify/SKILL.md` nor
`docs/issues-and-milestones.md` states the title format, so nothing there is
wrong today — but the skill's *"the rolling `flow-measurement` log, which
accumulates for one version and is discarded when that version ships"* now
describes the wrong boundary: the log accumulates between two releases and is
closed by the later one. `docs/issues-and-milestones.md` §*`flow-measurement`
is a label that is not an index* says the script *"closes the current one and
opens the next when a release reaches `main`"*, which needs the condition
added — it is a push to `main`, and only where a new version shipped. That
document is also where *what the old titles mean* belongs for a reader, since
this phase put it only in the script's docstring and in one case. F5 in
`seal/ledger.md` constrains the skill: it may name `flow-measurement` and
`flow-baseline` and no tracker state that exists in this repository alone, so
the title format itself belongs in `docs/issues-and-milestones.md` rather than
in the skill.

**What phase 3 has to carry.** A ledger fragment for the condition, the
direction of the unreadable title, and the writer/reader constant; a changelog
fragment; `overview.md` with the `spec.md` divergence above; `docs/flow.md`'s
#155 box. Nothing in this phase reached the ledger yet.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `next_version(current)` — the guess itself, `X.Y.Z -> X.(Y+1).0`, and the docstring block stating it as a default | Nowhere. The winner has no caller for it: the title names the version in the tree, and the condition compares two version strings for equality rather than computing one. `seal/ledger.md` cites the function in no row |
| `test_next_version_bumps_the_minor_and_resets_the_patch` | Removed with the function it covered. Its third assertion (`1.9.4 -> 1.10.0`, the minor is an integer and not a digit) covered arithmetic that no longer happens anywhere in this module |
| The docstring's *"the cost of a wrong guess is a title a human can retitle by hand, not a broken lookup"* | Replaced in the same docstring by what the script now does. #155's second *Done when* is that this sentence stops being the stated answer, and #155 §*Not this* refuses retitling by hand as the answer |
| The docstring's *"Nothing depends on the title being correct"* | Replaced by the narrower claim that is still true: the lookup is by label and open state and never by the title, and the title is read only once the lookup has already found the issue. An edited title can neither hide the issue nor stop the roll |
