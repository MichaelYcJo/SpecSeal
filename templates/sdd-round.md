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
| Fixes checked by | <`round-<N>`, a LATER round · `no fixes to check` · `nobody — <why>`> |
| Needs a fix | <`yes — <what>` · `no`. The reviewer's own answer — what stands after the colon in its `Needs a fix:` line, never the whole line> |

- [ ] Pass

<!-- `Fixes checked by` is the companion to the box below, and they answer
different questions. `Pass` says no finding in this round's table is still
open. This says who opened the work that closed them, and it takes three
values and nothing else:

  `round-<N>`          a LATER round read these fixes and reported on them. It
                       has to exist and its number has to be above this one —
                       a round cannot check itself, and one that ran before
                       the fixes existed cannot have read them
  `no fixes to check`  nothing here closed with a fix. Refused beside a
                       verdict cell reading `fixed`, which is the same
                       contradiction-inside-one-file the `Pass` rule refuses
  `nobody — <why>`     the gap, written down. The reason is required

Only a later round may be named, so the LAST record of a finished run reads
`no fixes to check` or `nobody — <why>`. That is the rule's shape, not a
limit on it: a run ends at a round that wrote no code nobody read, or it ends
with the gap where a reader meets it.

`nobody` prints on every run. On the run's LAST record it also FAILS the pull
request when `Pass` is checked beside it, because that pair is the review
claiming to have passed while its own fixes went unread. Work items begun
before the rule landed are excused and only print. The way out costs no round:
one verifying round at the diff of those fixes, and a round that opens nothing
needing a fix does not consume the cap.

`Needs a fix` is the answer the run ends on, and it is the reviewer's rather
than the orchestrator's. A round that opened nothing needing a fix ends the
run and does not consume the cap; `no` is what says so. A 🟡 the smith answers
with grounds is still `no` — the condition is *this round wrote no code nobody
read*, not *this round found nothing*.

It is copied from the reviewer's report and not inferred from the verdict
table. A verdict table says what was found and this says what the finder
concluded about it, and the two come apart at exactly the case above.

No check reads this row. It is here because the reviewer is told to answer the
question and had nowhere to write the answer, which is how a decision ends up
living in a transcript.

Check `Pass` only when no finding in the verdict table below is still
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
