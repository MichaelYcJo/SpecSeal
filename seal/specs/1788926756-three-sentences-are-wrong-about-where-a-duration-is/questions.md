# Questions: three sentences are wrong about where a duration is

Routing was not re-asked: the owner said *proceed* to a recommendation naming
this work, and the three axes are the ones answered twice already today. Q5 of
#145 was answered in the same message — **the span goes to `max(end)`** — and
that answer is what makes item 3 part of this work item rather than a
question inside it.

| # | Assumption | Why it does not wait |
|---|---|---|
| 1 | The readings already posted to #51 need no marking line for the span's new definition | **Executed, on every printed surface.** This project's 16 transcripts move nothing: no run span, no row span, no between-the-rows figure. Machine-wide five printed figures do move — 2 row spans and 3 between-the-rows figures — and every one is in another project's transcript. So no reading posted to #51 moves, which is a per-project measurement rather than a property of the rule, and that is what `skills/verify/SKILL.md` now says where a reading is taken |
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
overlap — and overlap above one second in 72 of the 169. **Batching is the
ordinary way in**, not a background command: every tool call in one assistant
message starts at that message's timestamp, so a batch overlaps by
construction, and 100% of the machine's 8,332 seconds of overlap is
intra-turn with none of it crossing a turn. This is the plain path every
published segment reading uses.

**The trigger is the part that needs deciding, not the wording.** A share
above 100% is 1 of the 169. Overlap that moves a printed figure is in 23 of
them, so an answer that fires only above 100% leaves 22 of the 23 inflated
and silent.

| Answer | What it costs | What a reader gets |
|---|---|---|
| Leave it | nothing | a share over 100% of a span, which reads as arithmetic that cannot be right, in the path every reading uses |
| Take `command_s` to the union of the call intervals | the number stops being *command time* and becomes *wall clock with a command running*. **Measured:** 58 of 169 printed `command` minutes change and 23 of 169 printed shares change, the largest 116% → 80% and 315.1m → 219.1m; 111 of 169 are identical either way | a share that cannot pass 100%, and a break in the series for a third of the readings |
| Keep the sum and say so where the share passes 100% | one printed sentence, in `report` beside the share, plus its case | a true reading of the 1 transcript in 169 that passes 100%, and nothing for the other 22 whose share is inflated below it |
| Keep the sum and say so wherever calls overlapped at all | one printed sentence and one union computation, on every reading rather than on one in 169 | *1007s of command time in 1000s of wall clock — calls ran concurrently* wherever it is true, which is where the comparability actually breaks |

The last two are #200's own repair applied one column over: name what the
number is rather than printing a figure that reads as something else. Either
is a printed sentence, so it alters observable behaviour and is a work item
of its own rather than a line added here. What separates them is the trigger
above, and that is the part this question is now asking.

## Q4 — F5 forbids the shipped skill to name this repository's own tracker state, and it names two issue numbers

**For the owner, and it is bigger than this work item.** `seal/ledger.md`'s
F5 holds that `skills/verify/SKILL.md` may name `flow-measurement` and
`flow-baseline` and no tracker state existing in this repository alone. This
work item put `(#300)` into the section F5 anchors on, beside the span's new
definition, and an issue number is exactly that kind of state.

**It was already false before this change, which is what makes it a decision
rather than a fix.** Executed — `(#272)` sits in the shipped skill's `## Scope`
section, outside F5's anchored section but inside the shipped file. And
`test_the_shipped_skill_names_no_repository_specific_tracker_state` stays
green either way, because it asserts three literals — `log: measurement`,
`#51` and a bare backticked `measurement` — and reads for no issue number at
all.

| Answer | What it costs | What it gives up |
|---|---|---|
| Narrow F5's clause to the three literals the case actually reads | one sentence in the row | the clause stops covering the shape it was written about, and the next issue number arrives unremarked |
| Widen the case to the shape — any `#NNN` in the shipped skill | a case change, and every existing issue number in the file has to go or be exempted | two citations a reader may want, and the paragraph that cites `#300` is where a person comparing readings across the change is told which change |
| Leave both, and say in F5 that the clause is literal | nothing | the row keeps a name wider than what anything checks |

Neither the clause nor the case was touched here. The note under F5 now says
the absence is not whole rather than asserting it is.

## Open, and it is small

Whether the disclosure sentence belongs beside the span's definition in
`skills/verify/SKILL.md` or in the report's own output as well. The plan puts
it in the skill, because that is where a session reads what a span is; a
second copy in the output would be the fourteen-place duplication #145's
round 1 spent itself on. If a reader of the report alone should meet it, that
is one line more and the owner's call — it does not block.
