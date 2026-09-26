# 1790381329-the-deferred-sentences-and-pins — routing

<!-- seal/specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). Committed,
because the check happens at the pull request and CI sees only what is in the
tree.

This is the first file a work item gets, and below the SDD ladder it may be the
only one — a typo fix writes no `spec.md`, and this is what gives it a place to
exist at all.

The rows are read by machines and their vocabulary is fixed. Anything else in
this file is for people. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/610-the-deferred-sentences-and-pins |

<!-- Review — `through the review chain` or `straight to the PR`. The first
     owes a committed `rounds/round-N.md` at the pull request; the second
     turns off the reviewer alone and owes the sealer's `broad-gate.md` in
     this directory at a ready pull request — the one broad run, at a SHA,
     against the base. Neither is *no enforcement*: a change belonging to no
     work item is the routing question's `no work item` answer, recorded as
     `[no-review]` in front of each commit.
     Destination — `open the pull request` or `stop before the pull request`.
     Planning — `framer` or `the session`. Who draws the frame — `spec.md`,
     `plan.md` and the questions: the `framer` subagent, or this session
     itself. OPTIONAL, on exactly the terms the `Implementation` row below
     has, and for the same reasons — read them there. A second copy of that
     reasoning here is how the two rows drift apart, which is the failure the
     contract records under §11 and §16.
     HOW TO ANSWER IT — nobody is asked. `skills/implement/SKILL.md` §3's
     ladder decides whether a frame is drawn at all, so this row RECORDS which
     way it went rather than putting a fourth box in the routing question
     (#88). Write the answer WITHOUT backticks, the same as below.
     Implementation — `smith` or `the session`. Who writes the code: the
     `smith` subagent, or this session itself. OPTIONAL — a declaration
     without this row is still a declaration, and it reads as "not answered".
     Delete the row rather than inventing a third answer.
     HOW TO ANSWER IT — the criterion, so the row is not answered by habit.
     Ask whether this work is FINDING OUT or WRITING DOWN. Finding out — what
     an unfamiliar codebase does, where a behaviour lives, what an original
     actually did — is a STEP to send to `scribe`: a large input and a small
     output is what a subagent boundary is for. That is a step and not an
     answer to this row, which has two values and no third: the session that
     reads those facts back and writes the code still answers `the session`.
     Writing down stays with the session too, because a delegate re-buys the
     context the session already holds. The one case `smith` answers is a diff
     large enough to threaten what the orchestrator still has to hold.
     So the row is never deleted because the work is discovery — `the session`
     is the answer there, and the sentence above about deleting the row is for
     a work item that genuinely has no answer to give.
     The threshold in that last clause is a number nobody has, and this
     comment does not invent one. What it can say is which axis it is on:
     the case for a delegate there is REPLACEABILITY, not cost — the
     orchestrator is the single participant a release cannot replace mid-run.
     A cheaper delegate is not a reason, and #263 is where answering this row
     by habit was measured against the same class of change done in the
     parent session.
     This one and the `Planning` row above ship as PLACEHOLDERS while
     `Review` and `Destination` ship answered, and the difference is
     deliberate: a wrong answer in those two is caught at the next commit,
     because the gate stops recognising the file and goes back to asking.
     A wrong answer here is never contradicted by
     anything that can stop a commit: a confident `smith` nobody performed
     earns one printed line after a commit, and a confident `the session`
     earns nothing at all. So the commonest mistake — copy the file, never
     revisit the row — must land on "not answered" rather than on a
     confident `smith` that nobody performed. Write the answer WITHOUT backticks; a backticked
     value reads as unanswered here and would have been rejected above.
     Automation — `yes` or `no`. Does this run go from here to its
     destination without stopping to ask. OPTIONAL, on the two rows above's
     terms.
     HOW TO ANSWER IT — it is the one box in the routing question that names
     no party. The other three each switch somebody on or off; this one says
     whether the run may come back with a question at minute thirty. `no` is
     NOT "a person did it by hand" — it is "this run may stop to ask", and
     reading it the first way is how a supervised run gets recorded as a
     manual one.
     UNCHECKED IS A VALUE HERE, not an absence: a question that is asked
     always writes one of the two, so an absent row means nobody was ever
     asked. Writing `no` where the question was never put is the one mistake
     this row cannot survive, because it is then byte-identical to a file
     nobody read (#151).
     WHAT IT DOES NOT BUY — nothing at the pull request can hold a run to it.
     A session that promised not to stop and then stopped leaves no artifact
     to find. What it buys is that the promise is now written down, so a run
     that broke it broke something a reader can point at.
     Answer pressed — `automation` or `per axis`. WHICH answer the person
     pressed, not what it derived to. OPTIONAL, on the same terms.
     HOW TO ANSWER IT — `automation` where they pressed the preset, `per axis`
     where they ticked the boxes themselves. Question 1's third option,
     `no work item`, never reaches this row: it opens no work item, so there
     is no file for it to be written in.
     WHY THE ROW EXISTS — without it a pressed preset and four boxes somebody
     ticked by hand produce the same bytes, so a later reader cannot tell a
     decision from a default. That is #151's shape, and it is why `seal mode`
     writes a row saying a person was asked.
     Branch — one declaration per branch. Two is not an answer, and the gate
     reads it as none. -->

Answered 2026-09-26 by the repository owner, before the first edit.

## Why this way

#610, #611, #612, #613, #615 and #616, what 0.15.4's capped rounds deferred: one sentence, one pin or one exit code each. The owner pressed `automation` once for every work item of `release: 0.15.5` in one question.
