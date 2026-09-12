# Issues and milestones

What the issue tracker's fields mean here, and which of them anything reads.

Every other mechanism in this repository has a document that owns it —
`branch-and-release.md` owns the merge rules, `review-chain-spec.md` owns the
cap, `worktree-guard-spec.md` owns the guard. The tracker had none, and its
conventions lived in the shape of the data plus one sentence inside a design
record. This is that document.

## A milestone answers *when*, and takes three shapes

| Prefix | Holds | Ends |
|---|---|---|
| `release:` | the work going out in that version | closed when the version ships |
| `backlog:` | work with no release yet, bucketed by area | closed when the area is empty |
| `log:` | **not work** — a record that is kept rather than finished | never closed |

`release:` milestones carry the version's release date as their due date, and
are closed when the release reaches `main`. An open milestone with a past due
date reads as overdue, which is the tracker's way of saying a release shipped
and nobody closed its milestone.

**A release is sized by what has to be in effect before the next work item
starts, and not by a count.** One change that decides how the next ticket runs
is a release on its own. The release that shipped the framer carried a single
work item, because the agent that writes a frame had to exist before anything
was framed; the release that replaced the deleted checklist with a gate carried
two, because the next work item had to start with the replacement already in
effect. Neither of them was cut short of a target.

**Three or four is a ceiling, not a target.** It is as much as one section can
describe while a reader still comes away knowing what the release is about, and
it says nothing about when to stop under it. The count is in work items rather
than in ticket numbers because a run that reaches the reopening bound turns
every finding still open into an issue, which is right — and it means one
branch's leftovers arrive as four ticket numbers, which a reader counts as four
releases' worth of work. Size a ticket set that will be one branch as one
item. 0.8.3 shipped three of eight, and carrying five forward was the call
rather than the failure.

**The two releases above are named rather than numbered on purpose.** Both sit
at or above the running version, and
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` refuses a
loaded file that names one — the same rule that keeps the number illustrative
in **A rolling log is titled after the version it rolled from** below.
`CHANGELOG.md` turns either description back into a number in one grep. One of
the two has already shipped, so for one release's length the refusal outlives
its own reason; #363 is where that is repaired, and not here.

**What the criterion does not change.** It decides a release's size and nothing
else. A `release:` milestone is still the pool a release is cut from rather than
the release itself, `backlog:` below is still the unscheduled pool, and nothing
schedules from either — the one thing that reads a milestone checks a cut
release against its pool and never decides what goes into one.

`backlog:` is the unscheduled pool, and an issue leaves it in one act: the
milestone changes. It used to be two, the second being a line in a checklist
every branch appended to; that file is gone and what it carried is here and
on the tracker (#351). **A scheduled release milestone's description states
the release's purpose and the grounds for the order its issues sit in**, and
grounds belonging to one ticket sit on that ticket. So "what is in 1.2.3, and
why in that order" is answered without opening a file. The number is
illustrative, for the reason
**A rolling log is titled after the version it rolled from** gives below.
It named a real unshipped release here for three of them (#179).

`log:` is the shape that surprises people, and there is one of it:
`log: measurement`. What it holds are not tasks. `#51` is the durable
performance ledger whose body is the current state, and the open
`flow-measurement` issue is this version's rolling log. Neither has a done
condition, so neither closes, so the milestone does not either.

## A label answers *what it is about*, and survives the move

GitHub gives an issue one milestone. That field is spent on *when*, so a
concern that outlives a schedule needs a label instead: `measurement` is
carried by `#51`, by the rolling log, and by the scheduled work that came out
of them, whichever milestone each one sits in. Query the concern by label and
the release by milestone; neither substitutes for the other.

**`flow-measurement` is a label that is not an index.** It is a lookup key,
and it carries an invariant: *exactly one open at a time*.
`.github/scripts/roll_flow_measurement_issue.py` closes the current one and
opens the next on a push to `main`, and **only where a new version has
shipped** since the open log opened; it fails loudly on zero or on two
rather than guessing which is current. The workflow fires on every push to
the default branch, so a push that moved no version — a re-run of the job,
or a merge that shipped nothing — rolls nothing and says so in the job log.
`skills/verify/SKILL.md` finds the log to post a segment's measurement to by
that key. Reading `--label flow-measurement --state all` finds the rolling
logs and misses `#51`; reading `--label measurement` finds everything and
answers no lookup.

**A rolling log is titled after the version it rolled from**, in the form
`chore: flow measurement — after 1.2.3`. That log opened at the 1.2.3
release, holds the measurements taken since, and is closed by whatever ships
next. The number here is illustrative on purpose: a real version written
into a loaded file is what
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` refuses —
at or above the running one, whether that is the version being cut or one
still ahead of it — and this paragraph would go red at its own next release.
**A version below the running one is history and is kept.** That half is not
a detail: it is what lets this document say further down which release an
issue shipped in, and a rule that refused every version this repository has
ever shipped would have refused that sentence too.
The version in it is a fact rather than a prediction:
`docs/branch-and-release.md` says whether the next number is a minor or a
patch is known at the end and not at the cut, so at the moment the roll runs
the next version is the one thing nobody can name.

**A title that does not begin with `chore: flow measurement — after ` was
written before that convention, or by hand, and the roll reads it as due.**
The whole of that prefix is what the roll writes, and the whole of it is what
the roll requires, from the first character of the title. A title carrying
those words somewhere inside it — `docs: explain flow measurement — after
1.2.3` — is not one of these logs, and reading a version out of it would
leave that log never due. Titles written before this convention were named
for the version they were predicted to be *for*, which is how a patch
release came to close a log titled for a minor that had not shipped — #155
carries the measurement, and no real version is named here for the reason
above. They are **not rewritten**: a retitle would falsify every comment
that cites them. A title the roll
cannot read as its own is due rather than silent, so the first release after
each one rolls it and the older convention retires itself.

## Closing one of these by hand breaks the next release

The invariant above is what makes `log: measurement` dangerous to tidy. A
milestone holding two issues that never close looks exactly like a milestone
somebody abandoned. **Closing the open `flow-measurement` issue leaves zero
open, and the next release fails on it** — which is the loud failure working
as designed, at the worst possible moment.

If a `log:` issue has been closed, reopen it rather than opening a new one:
two open ones fail the same check from the other side.

## One thing reads a milestone, and it can stop a release

This section said *nothing automated reads a milestone* until #359, and for
as long as that was true a wrong milestone cost a person a wrong answer to
"what is in this version" and cost no automation anything. It is not true any
more, and the cost moved.

`.github/scripts/release_completeness_check.py` runs on a pull request from
`release/vX.Y.Z` into `main` and reads the milestone `release: X.Y.Z`. It
**refuses the release** while that milestone holds an open issue the release
branch does not carry, and names each one. So a milestone left holding next
quarter's work does not produce a wrong answer any more, it produces a red
release pull request — at the moment the release is being cut, which is the
worst moment to do the scheduling it is asking for.
`docs/release-checklist.md` step 0 is where that act belongs — the box asking
whether the milestone holds what the release is carrying, which is inside
step 0 and so is ticked before any of the release's cost is paid.

What the gate compares the milestone against is still the pull request body.
It reads the release branch's own commit subjects, takes the `(#N)` a squash
writes, fetches those bodies, and collects what their closing keywords name —
the same readers `.github/scripts/close_issues_on_release.py` uses to close
them when the release reaches `main`, imported rather than copied.
`skills/implement/orchestration.md` §*Orchestrator: the order inside a
ticket* says the same thing from the ticket's side.

**A missing `Closes #N` still costs an issue that stays open forever, and now
something reports it.** An issue nobody claimed is in the milestone and never
enters what the release carries, so it is indistinguishable from work that
was never built — and the release is refused until somebody either writes the
keyword, or moves the issue, or builds it. That is a louder failure than the
silence it replaces, and it lands on the release rather than on the work item
that caused it.

## A label says a ticket is already in, before the release ships

An issue's state does not move until `main` moves, and `main` moves once per
release. So for the length of a release a finished work item and one nobody
has started look identical on the tracker, and for a while the only thing
that told them apart was a bullet in a checklist that has since been deleted
(#351).

`.github/scripts/label_merged_on_release_branch.py` runs on a push to
`release/*` and puts `merged: X.Y.Z` on every issue the arriving pull
requests claimed, creating the label the first time. One query answers *what
is already in* — `gh issue list --milestone "release: X.Y.Z"`, and the merged
ones carry the label.

Three things about it are worth knowing before anyone tidies it.

- **It never closes anything.** An issue closed at the release-branch merge
  is closed for something nobody has received; the close stays on `main`.
- **The labels accumulate and are never removed**, one per release. Deleting
  one deletes it from every issue that ever carried it, which falsifies the
  record it was created to leave.
- **A label is a cache and the commits are the truth.** The gate above
  recomputes what the release carries from the branch itself and never asks
  the labels, so a label write that failed cannot block a release. It does
  compare the two and says which way they disagree: a label naming a release
  the issue is not in **fails**, because that is always a hand-edit or a
  squash subject that lost its `(#N)` and one command repairs it, while a
  missing label only **reports**, because a release must not be held for a
  failure of the signal rather than of its contents.

## A keyword claims the one number after it

`Closes #153 and #150` claims #153. The second number carries no keyword of
its own, so nothing reads it as a claim — not GitHub, and not the script
above, whose own comment says `Closes #1, #2` is not read as two either. PR
#162 wrote that sentence; the 0.8.0 release acted on #153 alone, and #150
stayed open until somebody dealt with it by hand.

**Write the keyword in front of every number**: `closes #153 and closes #150`.

The hygiene workflow reports the split on every pull request —
`.github/scripts/issue_claims_check.py` prints every issue the body claims,
every one it merely mentions, and a warning for any sentence that claims one
number and names another beside it. It reports and never fails, so the
correction is the author's to make while the pull request is open. A body
quoting the failing shape inside a fence or a code span, the way this section
does, is not an instance of it.

The prose around those spans keeps its keywords out for the same reason. A
past-tense narrative keyword is still a keyword, so the opening paragraph of
this section says a release *acted on* one number rather than using the verb
this section is about, and a sentence that used it with a second number beside
it would earn the warning like any body.

## An issue is its body and its comments together

Corrections, measurements and improvements land as comments, and the question
a reader is answering — *what does this ticket now ask for* — is answered by
reading all of them and then judging. That is how the tickets here have
actually been used, and a rule that told people to read the body alone would
be describing a different repository.

What the body owes in return is that nobody has to **reconcile** it. A body
that contradicts a comment leaves the reader to work out which is current,
which is the cost this section exists to keep down. Two ways to pay it, and
which one fits depends on whether the original text is worth keeping:

- **Consolidate the body**, once the design is settled. The comments stay and
  are still part of the issue; what goes away is the need to cross-check four
  places to learn what the ticket asks for. #136 is the worked example.
- **Leave the body and open it with `> **Update <date>.**`**, naming what has
  moved since it was written. #30 is the worked example: the original design
  is preserved and the block says which two things below it have changed.

The exception is an issue that is a **ledger rather than a ticket** — `#51`
and the rolling `flow-measurement` log. There the body IS the current state
and is maintained: a better baseline replaces the table, an observation that
gets an answer is rewritten where it stands, and the comments are the evidence
a change was made on rather than the answer. `#51`'s own body says so at the
top, because the distinction is not guessable from the outside.

## An issue is titled like a commit

Same prefix vocabulary as commits and pull requests — `feat:`, `fix:`,
`docs:`, `chore:`, `test:`, `refactor:`, `perf:` — and the subject is the
**symptom**, not the classification.
`skills/commit-pr-convention/SKILL.md` is the authority for the vocabulary;
this is only the note that issues use it too.

```
good   chore: the round cap is a ceiling and has been spent like a budget
bad    Round cap improvements
```

## Reconstructing a missing milestone

The signal is the tag, not the branch. For a closed issue with no milestone,
find the pull request whose body names it with `Closes #N`, take that pull
request's merge commit, and read the **first tag that contains it** — that is
the release it shipped in.

A branch name is not that signal and has been wrong here: the branch
`release/v0.3.0` shipped as 0.2.0, and its own release pull request says so
in its title. Where no pull request names the issue at all, the close date
against `CHANGELOG.md`'s release dates is what is left, and it is a guess
rather than a reading.
