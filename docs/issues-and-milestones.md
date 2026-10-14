# Issues and milestones

What the issue tracker's fields mean here, and which of them anything reads.

## A milestone answers *when*, and takes three shapes

<!-- specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency -->
**A milestone answers *when* and never a release's size, which is decided by what
has to be in effect before the next work item starts.**

| Prefix | Holds | Ends |
|---|---|---|
| `release:` | the work going out in that version | closed when the version ships |
| `backlog:` | work with no release yet, bucketed by area | closed when the area is empty |
| `log:` | **not work** — a record that is kept rather than finished | never closed |

A `release:` milestone carries the release date as its due date and closes when the
release reaches `main`, so one open past its due date is a shipped release nobody
closed.

**A release is sized by what has to be in effect before the next work item
starts, and not by a count.** One change that decides how the next ticket runs is
a release on its own.

**Three or four is a ceiling, not a target.** It is as much as one section can
describe, and it says nothing about when to stop under it. It counts work items,
not tickets, because one branch's leftovers arrive as several tickets.

**What the criterion does not change.** It decides a release's size and nothing
else: a `release:` milestone is still the pool a release is cut from, `backlog:`
is still the unscheduled pool, and nothing schedules from either.

**An issue leaves `backlog:` in one act: its milestone changes.** A scheduled
release milestone's description states its purpose and the grounds for its order,
so "what is in 1.2.3, and why" needs no file; the number is illustrative, for the
reason **A rolling log is titled after the version it rolled from** gives below.

**`log:` holds what is not work: `log: measurement`.** `#51` is the durable
performance ledger and the open `flow-measurement` issue this version's rolling
log; neither has a done condition, so neither they nor the milestone close.
Enforced by: tests/test_a_release_is_sized_by_a_criterion.py::test_the_rule_states_the_criterion_and_not_the_count, tests/test_a_release_is_sized_by_a_criterion.py::test_one_document_states_a_releases_size

## A label answers *what it is about*, and survives the move

**A concern that outlives a schedule is a label**, because an issue's one
milestone is spent on *when*: `measurement` is carried by `#51`, the rolling log
and their work, whatever their milestones.

**`from-review` marks an issue a review round filed**, for one query:
`--label from-review --state all` beside `--state closed` is the share of filed
findings acted on. **Quote the date with the number**; the label set moves.
`docs/review-chain-spec.md` §*Where a leftover goes — the ladder, and why a new
issue is not the default* owns where a filed finding goes.

<!-- specs/1788661274-the-roll-names-the-next-version-by-guessing -->
<!-- specs/1788486395-the-roll-opens-the-next-log-with-no-body -->
**`flow-measurement` is a label that is not an index.** It is a lookup key with an
invariant: *exactly one open at a time*.
`.github/scripts/roll_flow_measurement_issue.py` closes the current one and opens
the next on a push to `main`, **only where a new version has shipped** since the
open log opened, and fails loudly on zero or two.
A push that moved no version rolls nothing and says so. **A log rolled with no
comment on it is said so** in the close comment, the new body and the job output,
and the release ships anyway. `skills/verify/SKILL.md` finds the log by that key;
`--label measurement` would also find `#51`.
Enforced by: tests/test_a_release_rolls_the_flow_measurement_issue.py::test_two_open_issues_fails_loudly_without_retrying, tests/test_a_release_rolls_the_flow_measurement_issue.py::test_a_push_that_shipped_no_new_version_rolls_nothing

<!-- specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible -->
**A rolling log is titled after the version it rolled from**:
`chore: flow measurement — after 1.2.3` opened at the 1.2.3 release and closes when
the next one ships. The number is illustrative because
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` refuses a real
version at or above the running one, not yet tagged. **A version below the running
one, or one this repository has tagged, is history and is kept**: after the
preparation commit's bump the running version has shipped, and a tag says so.
The title names a fact, because the next number is known only at the end
(`docs/branch-and-release.md`).

**A title that does not begin with `chore: flow measurement — after ` was written
before that convention, or by hand, and the roll reads it as due.** The roll
requires the whole prefix from the first character, so
`docs: explain flow measurement — after 1.2.3` is not a log. An older title names
the version it was predicted to be *for* and is **not rewritten**, since a retitle
falsifies every comment citing it.

**`size: now` says this ticket has to be in effect before the next work item
starts.** It records the sizing judgment so the next cut re-reads no issue. Two
states: without it, a ticket rides the next release that happens to carry it.

**The subject sits in the prefix and the verdict in the value**, as in
`chain: capped`, so a spent label is removed whole; `flow-measurement` stays the
one label that is not a topic. `chain: reframed` marks a run whose fix passes went
back to the framer, and nothing reads it (`skills/code-review/orchestration.md`
§*A fix of a fix twice sends the work item back to its framer*).

**Nothing schedules from this label**, so a stale one costs a reader a wrong
answer and no automation anything.

**One thing reads it, and only to spend it.**
`.github/workflows/close-issues-on-release.yml` removes `size: now` from each issue
it closes when the release reaches `main`, after the close, so a failed label
write cannot cost an issue its close.

**The judgment is made at filing, and again when an issue moves milestone.**
Somebody is reading the body then. A ticket filed without it is unjudged, which
reads the same as *not now*.

**No sweep of the standing backlog is owed, and none should be done.** The
judgment is cheap at filing; a sweep is the batch, performed once, by the very
party the label exists to spare. An old ticket gets it when somebody next opens it.

**`merged: X.Y.Z` goes on earlier**, at the squash onto the release branch
(§*A label says a ticket is already in, before the release ships*), and answers
*is this in yet*. Neither label decides which release a ticket lands in.
Enforced by: tests/test_a_release_rolls_the_flow_measurement_issue.py::test_the_title_the_roll_writes_is_the_title_the_next_roll_reads, tests/test_a_release_rolls_the_flow_measurement_issue.py::test_rolled_from_reads_only_the_title_the_roll_itself_writes

## Closing one of these by hand breaks the next release

**Closing the open `flow-measurement` issue leaves zero open, and the next release
fails on it.** Reopen a closed `log:` issue rather than opening a new one: two
open ones fail the same check.

## One thing reads a milestone, and it can stop a release

**`.github/scripts/release_completeness_check.py` refuses the release while its
milestone holds an open issue the release branch does not carry**, naming each,
on the pull request from `release/vX.Y.Z` into `main`;
`docs/release-checklist.md` step 0 is where that is fixed. It reads what the
release carries from the closing keywords of the bodies its squash subjects'
`(#N)` name, with `.github/scripts/close_issues_on_release.py`'s readers,
imported. `skills/implement/orchestration.md` §*Orchestrator: the order inside a
ticket* says the same from the ticket's side.

**A missing `Closes #N` leaves an issue in the milestone that never enters what
the release carries**, and the release is refused until somebody writes the
keyword, moves the issue, or builds it.

## A label says a ticket is already in, before the release ships

<!-- specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships -->
**An issue a pull request into a release branch claimed carries `merged: X.Y.Z`
before the release ships**, because an issue's state moves only when `main` does.
`.github/scripts/label_merged_on_release_branch.py` runs on a push to `release/*`
and labels every issue the arriving pull requests claimed, creating the label the
first time.

- **It never closes anything.** The close stays on `main`.
- **The labels accumulate and are never removed.** Deleting one deletes it from
  every issue that ever carried it, which falsifies the record it was created to
  leave.
- **A label is a cache and the commits are the truth.** The gate above never asks
  the labels, so a failed write cannot block a release. A label naming a release
  the issue is not in **fails**, being a hand-edit or a lost `(#N)`; a missing
  label only **reports**.

Enforced by: tests/test_a_merged_ticket_says_so_on_the_tracker.py::test_it_labels_the_issue_the_keyword_named_and_nothing_else, tests/test_a_merged_ticket_says_so_on_the_tracker.py::test_the_trigger_is_a_push_to_a_release_branch_and_nothing_else

## A keyword claims the one number after it

<!-- specs/1788844400-a-body-naming-two-issues-claims-one -->
**A closing keyword claims the one number after it.** `Closes #1 and #2` claims
the first issue, and neither GitHub nor the closer reads `Closes #1, #2` as two.
**Write the keyword in front of every number**: `closes #1 and closes #2`.
`.github/scripts/issue_claims_check.py` reports the split on every pull request
and never fails. A body quoting the failing shape in a fence or a code span, as
this section does, is not an instance of it; the prose around them keeps its
keywords out, past tense included.
Enforced by: tests/test_a_body_naming_two_issues_claims_one.py::test_the_sentence_that_lost_an_issue, tests/test_a_body_naming_two_issues_claims_one.py::test_the_two_lists_say_what_closes_and_what_does_not

<!-- specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close -->
**A keyword inside a fence or a code span claims nothing, whatever the fence or
the span is made of.** A fence opens with backticks or tildes at any indent; a
span is one backtick or two. Masking more closes fewer, the safe direction. Two
shapes are still read as claims, each pinned by a case: a four-space indented
block, which pull request bodies here use for a bullet's continuation, and an HTML
comment, whose reading by GitHub is unmeasured. `issue_claims_check.py` imports
the closer's two patterns.
Enforced by: tests/test_release_hygiene.py

## An issue is its body and its comments together

**An issue is read whole, and its body owes the reader no reconciling.** A body
that contradicts a comment is fixed by consolidating it once the design settles,
or by opening it with `> **Update <date>.**` naming what has moved, when the
original is worth keeping.

**An issue that is a ledger rather than a ticket keeps its body as the current
state** — `#51` and the rolling `flow-measurement` log: a better baseline replaces
the table, an answered observation is rewritten in place, and `#51`'s body says
so at the top.

## An issue is titled like a commit

**An issue takes the commit prefix vocabulary, and its subject is the symptom, not
the classification** (`skills/commit-pr-convention/SKILL.md`).

```
good   chore: the round cap is a ceiling and has been spent like a budget
bad    Round cap improvements
```

## Reconstructing a missing milestone

**The signal is the tag, not the branch.** For a closed issue with no milestone,
read the **first tag that contains** the merge commit of the pull request whose
body names it with `Closes #N`; a release branch can ship under another number.
Where no pull request names it, its close date is a guess, not a reading.
