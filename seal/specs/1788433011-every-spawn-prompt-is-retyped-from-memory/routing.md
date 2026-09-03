# 1788433011-every-spawn-prompt-is-retyped-from-memory — routing

<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/routing.md
— the answer given before the first edit, in the batch the `implement` skill
collects (§1). Committed, because the check happens at the pull request and CI
sees only what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | chore/every-spawn-prompt-is-retyped-from-memory |

Answered 2026-09-03 by the repository owner, before the first edit, as one
batch of three checkboxes rather than three waits.

## Why this way

Issue #107, and the first work item of 0.6.0. It rewrites `agents/smith.md`
and `agents/warden.md` — the files every later round in this release and the
next one runs on — so a rule that goes missing here goes missing everywhere
after it. That is what buys the chain rather than a straight pull request.

There is a second reason to run the full chain on this one in particular:
its own review is the **last chain this repository runs under hand-typed
spawn prompts**. #109 lands next and makes the measurement automatic, so
these segments are 0.6.0's before-figure, and a chain cut short here leaves
the comparison with nothing on one side.

The pull request lands on `release/v0.6.0`.
