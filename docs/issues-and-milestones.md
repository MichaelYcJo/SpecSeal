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
start of a ticket, and the milestone is what answers "what is in 0.9.0"
without opening a file.

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
opens the next when a release reaches `main`, and it fails loudly on zero or
on two rather than guessing which is current.
`skills/verify/SKILL.md` finds the log to post a segment's measurement to by
that key. Reading `--label flow-measurement --state all` finds the rolling
logs and misses `#51`; reading `--label measurement` finds everything and
answers no lookup.

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
