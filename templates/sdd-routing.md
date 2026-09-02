# <work-item-id> — routing

<!-- specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
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
| Implementation | <smith, or: the session> |
| Branch | <the branch this work item is being built on> |

<!-- Review — `through the review chain` or `straight to the PR`.
     Destination — `open the pull request` or `stop before the pull request`.
     Implementation — `smith` or `the session`. Who writes the code: the
     `smith` subagent, or this session itself. OPTIONAL — a declaration
     without this row is still a declaration, and it reads as "not answered".
     Delete the row rather than inventing a third answer.
     This one ships as a PLACEHOLDER while the other two ship answered,
     and the difference is deliberate: a wrong answer in the other two is
     caught at the next commit, because the gate stops recognising the file
     and goes back to asking. A wrong answer here is never contradicted by
     anything that can stop a commit: a confident `smith` nobody performed
     earns one printed line after a commit, and a confident `the session`
     earns nothing at all. So the commonest mistake — copy the file, never
     revisit the row — must land on "not answered" rather than on a
     confident `smith` that nobody performed. Write the answer WITHOUT backticks; a backticked
     value reads as unanswered here and would have been rejected above.
     Branch — one declaration per branch. Two is not an answer, and the gate
     reads it as none. -->

Answered <date> by <who>, before the first edit.

## Why this way

<One or two sentences. Nothing reads this; it is what a reviewer and the next
session see instead of guessing from the absence of a token.>
