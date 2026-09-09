# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `82c1dbb` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Item 3, and it goes first: a window's `span_s` is taken to `max(end)` over
its calls rather than to the end of the last call **to begin**. It is Q5 of
#145, answered by the owner on 2026-09-09. Verified by a case on calls
0–1000s · 10–12s · 990–995s asserting the span and no share over 100%, the
partition case still green, and the 15-transcript sweep re-run and still
reading 0 deltas.

The order is a constraint rather than a preference: taking the span to
`max(end)` makes the between-the-rows refusal fire strictly less often, so
phase 2's sentences had to be re-read against the new rule rather than pasted
from a report written against the old one.

## What this phase found

**The acceptance criterion's second half is false, and measuring it is what
showed that.** `spec.md`'s scenario row reads *then `span_s` is 1000 and
`command` is at or under 100%*. The first half holds; the second does not, on
that exact shape:

| | span_s | command_s | printed |
|---|---|---|---|
| before | 995 | 1007 | `command 16.8m 101%` |
| after | 1000 | 1007 | `command 16.8m 101%` |

`command_s` sums call durations, and those three calls **overlap**: the union
of [0,1000], [10,12] and [990,995] is 1000s while their durations sum to
1007s. The seven-second excess is the two inner calls running *while* the
background command ran, each counted in full. So the share passes 100%
because command time is not wall-clock time, and no span rule can close it —
the old rule's five-second understatement was the smaller of the two causes,
and #145's round 3 finding 5 named only that one.

**It is reachable outside a fixture, and it is already on this machine.**
Sweeping every transcript under `~/.claude/projects/*/*.jsonl` with the new
span rule: 169 transcripts with calls, of which **one prints `command` at
115.7%** — 99 calls with 5,761.8s of genuine overlap. Concurrency of more
than a second is present in 72 of the 169. Handed to the owner in
`questions.md` Q3, with the measurement, because deciding what the report
should say about a share over 100% is a choice about printed output.

**The published readings are safe, and one figure in the handoff was
slightly off.** The prompt handed over *no transcript on this machine has a
span that moves*. Over this project's own directory that is exactly right —
16 transcripts, 12 to 836 calls, 0 spans move. Over every project on the
machine one span moves, by **0.006s**: printed span 10.3m → 10.3m, `command`
share 0% → 0%. So nothing printed moves and no marking line is owed, but the
literal claim needs the word *printed* in it.

**A negative span means something narrower now, and one existing case
flipped.** `span_s < 0` used to mean the last call *to begin* ended before
the first call began; it now means **no call** ended after the first call
began. A transcript holding one call that ran 10:00–12:00 beside a result
written before its own call read minus sixty minutes for a run that plainly
lasted two hours, and now reads 120.0m. The third arm of
`test_a_negative_span_says_what_it_actually_saw` pinned the old reading and
now pins the new one. That is a second real defect item 3 closes and nothing
had named it.

**Two numbers phase 2 inherits.** The pinned shape's run span moves 995 → 1000,
so the refusal prints `the run's own 16.7m` where the report's paste-ready
text says `16.6m`, and the magnitude is 16.4m rather than 16.5m. Any figure
copied from that report has to be recomputed.

**And the reason the refusal must not name the shortfall an overlap has
changed, though the conclusion has not.** The old grounds were that an
outliving call shortens the run's span too, so the difference carried both
errors. That is gone — the run's span is now correct. The new grounds:
`outside` is the between-row gaps *minus* the rows' overlap, so a negative
value is the overlap net of the gaps and not the overlap itself. On the
pinned shape the head row covers the whole run, so there are no gaps and the
987s does happen to equal the overlap — which is precisely why naming it the
overlap would be a claim that holds on the fixture and fails in general.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The printed sentence *the last call to begin ended before the first call began* | Replaced in place by *no call ended after the first call began*, at `session_cost.py#report`. Its three assertions moved with it |
| The claim that a negative span is *exactly the proposition* the old sentence stated — #145's sibling work item settled it that way at `1788700685-…/rounds/round-3.md:56` | Nothing needs to own it: that round record describes the tree at its own Target SHA and stays true of it. The live sentence is the one that moved |
| `analyse`'s docstring promise that every number it returns is what it was before `--spawns` existed | The same docstring, which now names `span_s` as the one measured exception and points at the comment carrying the sweep |
