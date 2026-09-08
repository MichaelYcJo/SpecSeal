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

`backlog:` is the unscheduled pool. An issue leaves it when it is scheduled,
and scheduling is two acts rather than one: the milestone changes, and the
issue gains a line in `docs/flow.md` under the release that will carry it.
Neither act alone is a schedule — `flow.md` is what a person reads at the
start of a ticket, and the milestone is what answers "what is in 1.2.3"
without opening a file. The number is illustrative, for the reason
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
whether it has shipped or is still ahead — and this paragraph would go red
at its own next release.
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

## Nothing automated reads a milestone

Worth stating because it is the opposite of what the fields suggest. No hook,
script or workflow in this repository reads a milestone; the only writer is a
person. What closes an issue is the pull request body:
`.github/scripts/close_issues_on_release.py` reads `Closes #N` from the pull
requests a release carries, and closes what they name when the release
reaches `main`. `docs/flow.md` says the same thing from the ticket's side.

So a milestone that is wrong costs a person a wrong answer to "what is in
this version" and costs no automation anything. A missing `Closes #N` costs
an issue that stays open forever.

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
past-tense narrative keyword is still a keyword, so the paragraph above says a
release *acted on* one number rather than using the verb this section is
about, and a sentence that used it with a second number beside it would earn
the warning like any body.

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
