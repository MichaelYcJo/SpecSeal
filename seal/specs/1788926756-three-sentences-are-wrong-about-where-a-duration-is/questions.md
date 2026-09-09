# Questions: three sentences are wrong about where a duration is

Routing was not re-asked: the owner said *proceed* to a recommendation naming
this work, and the three axes are the ones answered twice already today. Q5 of
#145 was answered in the same message — **the span goes to `max(end)`** — and
that answer is what makes item 3 part of this work item rather than a
question inside it.

| # | Assumption | Why it does not wait |
|---|---|---|
| 1 | The readings already posted to #51 need no marking line for the span's new definition | **Executed twice.** The handoff computed both rules over this project's directory — 16 transcripts, 0 spans move. Phase 1 widened it to every project on the machine: 169 transcripts, **one span moves, by 0.006s**, and its printed span is 10.3m either way with a `command` share of 0% either way. No PRINTED figure moves, so a marking line would say something false. The literal claim *no span moves* is what needed the correction, not the assumption |
| 2 | Phase 2 takes the report's paste-ready text where it still holds after phase 1 and says where it does not, rather than pasting it unchanged | The text was written against today's span rule. Pasting it unchanged is what the two prior runs' fix passes correctly refused to do twice |

## Q3 — `command` still prints over 100% of the span, and no span rule closes it

**For the owner. It did not block phase 1 and it does not block this work
item**, because item 3 is right on its own terms either way: a window must
not be shorter than a call inside it. What it does change is what item 3 can
be *said* to close, which is why the spec's own row was corrected rather than
built to.

#145's round 3 finding 5 diagnosed the plain report's `command 16.8m 101%`
as the span reading the end of the last call **to begin**. Phase 1 measured
the fix and the share did not move:

| | span_s | command_s | printed |
|---|---|---|---|
| before | 995 | 1007 | `command 16.8m 101%` |
| after | 1000 | 1007 | `command 16.8m 101%` |

There are two causes and the span was the smaller one. `command_s` sums call
durations, and on that shape the calls **overlap**: [0,1000] ∪ [10,12] ∪
[990,995] is 1000 seconds of wall clock holding 1007 seconds of command time,
because the two short calls ran *while* the background command ran and each
is counted in full.

**It is not synthetic.** Sweeping every transcript under
`~/.claude/projects/*/*.jsonl` with the new rule: 169 with calls, **one
printing `command` at 115.7%** — 99 calls carrying 5,761.8 seconds of real
overlap — and overlap above one second in 72 of the 169. A background command
is the ordinary way in, and this is the plain path every published segment
reading uses.

Three answers, and the third is the cheapest thing that is also true:

| Answer | What it costs | What a reader gets |
|---|---|---|
| Leave it | nothing | a share over 100% of a span, which reads as arithmetic that cannot be right, in the path every reading uses |
| Take `command_s` to the union of the call intervals | the number stops being *command time* and becomes *wall clock with a command running*, and every published `command` figure changes meaning — the incomparability `analyse`'s own docstring exists to prevent | a share that cannot pass 100%, and a break in the series |
| Keep the sum and say so where the share passes 100% | one printed sentence, in `report` beside the share, plus its case | *1007s of command time in 1000s of wall clock — calls ran concurrently*, which is a true reading of a number that is already true |

The third is #200's own repair applied one column over: name what the number
is rather than printing a figure that reads as something else. It is a
printed sentence, so it alters observable behaviour and is a work item of its
own rather than a line added here.

## Open, and it is small

Whether the disclosure sentence belongs beside the span's definition in
`skills/verify/SKILL.md` or in the report's own output as well. The plan puts
it in the skill, because that is where a session reads what a span is; a
second copy in the output would be the fourteen-place duplication #145's
round 1 spent itself on. If a reader of the report alone should meet it, that
is one line more and the owner's call — it does not block.
