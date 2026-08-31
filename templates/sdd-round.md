# <work-item-id> — review round <N>

<!-- specs/<unix-epoch-seconds>-<slug>/rounds/round-<N>.md — what this round of the
review chain did, written by the review orchestrator right after it posts.

It lives here rather than under a pull request number because the number does
not exist while the rounds that fill this file are running. `docs/review-handoff-protocol.md`
carries the format; this is the shape it takes in this repository. -->

| Field | Value |
|---|---|
| Target SHA | <the commit this round actually reviewed — both, if HEAD moved mid-review> |
| PR | <the pull request, once one exists. A field, not the key> |
| Broad gate | <`not yet`, or the SHA the one full-suite run happened at and the base it was compared against> |

- [ ] Pass

<!-- Check `Pass` only when no finding in the verdict table below is still
open. It is the last round's checkbox that speaks for the whole review: every
earlier verdict needs an answer in the round that follows, so nothing can be
open here and absent from the next file.

**By the time a ready pull request opens, this has to be checked.** The chain
runs before the pull request, so an unchecked box there means the review was
skipped or has not finished, and CI fails the pull request for it. A review
still running opens its pull request as a DRAFT, which is excused this and
nothing else.

A checked `Pass` beside an unanswered 🔴 is a contradiction inside one file,
and CI fails the pull request for that too. It fails the same way for a
verdict table it cannot read — a tolerant reader finds no open findings there,
and no open findings reads exactly like all of them closed. -->

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | <what is wrong> | `file.py:120` | <fixed · answered · open> | <the policy clause, the original's behavior, or the constraint — not "it probably meant that"> |

<!-- Severities name what they require, not a rank:
     🔴 blocks merge · 🟡 needs grounds · 🟢 matches · ❓ could not be judged.
     Earlier rounds' verdicts set this round's agenda. Every one needs an
     answer here, on this round's grounds — a verdict on current code carries
     nothing, because no check would tell you it went stale. -->

## Executed probes

| What was run | Result |
|---|---|
| <the command> | <what came back — this column is for what RAN, never for what was read> |

## Inherited coordinates

<!-- For N>1: where earlier rounds looked, so this round opens those places
instead of searching again. Coordinates carry; conclusions do not. -->

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

<!-- Findings this round neither fixed nor answered, each with the durable home
it went to. `nothing to drain` is a valid answer and has to be written.

The row stays here as well as in its new home. A deferral that leaves this
file leaves the inheritance range, and the next round raises it again. -->

| Finding | Where it went | Who answers it |
|---|---|---|
