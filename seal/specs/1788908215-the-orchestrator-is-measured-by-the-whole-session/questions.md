# Questions: the orchestrator segment is measured by the whole session

The routing batch was answered before the first edit: `smith` implements, the
review chain reviews, the pull request opens, and the boundary is the spawn
cycle. What follows are the assumptions taken under that answer. **None of
them changes what is built**, which is why each is an assumption here rather
than a question that stopped the work.

| # | Assumption | Why it does not wait |
|---|---|---|
| 1 | The mode is spelled `--spawns`, and `--json` gains a `spawns` key beside the existing ones | A flag name is not a decision about behaviour. Renaming it costs one line and no reading |
| 2 | Posting the first reading to #51 is part of this work rather than a separate act | `skills/verify/SKILL.md` §*Where a log is open* already prescribes posting a segment's numbers as part of the segment, and #145's *Done when* names the band #51 is missing |
| 3 | The interpreter-floor guard on `session_cost.py` stays out, with `seal/follow-up.md`'s row untouched | That row's open question is where the five-script class belongs, not how to fix it. Answering it inside this work item would settle a tracker question by editing one of its members |

## Q4 — what `delegated_s` should measure, now that the premise under it is measured false

**This one is a question and not an assumption, and it is the owner's.** It
did not stop the build: what `plan.md` specifies was built, it is correct as
specified, and the reading it produces is publishable with the sentence the
report now prints. But the number `spec.md` wanted is not the number the
column holds, and only a person decides whether that changes.

`plan.md` §Technical context says a spawn is an `Agent` `tool_use` block and
**its result arrival is the report**. Measured over three orchestrator
transcripts of the 0.9.x line, that is false on this harness:

| What was measured | Result |
|---|---|
| An `Agent` call's own `tool_use` → `tool_result` span, 67 spawns | 1.5–3.7 seconds |
| Subagent transcripts whose FIRST stamp equals a spawn's result stamp within 1s | 61 of 67 — the six misses are subagents of subagents, which have no call in the main transcript |
| Subagent span, median | about 1,000 seconds |
| The three largest opening gaps of one 18-gap run — cycle 10, cycle 14, the tail — none of them in any column | 351s · 768s · 962s |
| That run's 17 gaps under the 900s ceiling, in `model_s` for none of them | 1,507s of 2,469s |

So the result is written when the spawn is **accepted**. `spec.md`'s reason
for `delegated_s` — *"A subagent's thinking is already counted in that
subagent's row; charging it to the orchestrator too is the double count that
makes a cumulative reading look like a slow orchestrator"* — is a real double
count, and it is in **no column of any row** rather than in the interval
`delegated_s` excludes. `analyse` starts a window's `span_s` at that window's
own first call and its model walk never counts the gap before that call, so
the wait after a spawn's result is outside every column of the row that
follows it — under the 900-second ceiling as much as above it. Over the three
runs it is 12 to 31 per cent of each run's wall clock.

A cycle whose span exceeds its own parts is a **different** finding: the row
reading a 116-minute span against 11.5 minutes of columns owes 104.8 of those
minutes to one gap *inside* the cycle, above the ceiling, with a delegated
wait of 580 seconds. Round 1 found the two conflated on four pages.

Three answers, and the third is the cheap one:

| Answer | What it costs | What it gives up |
|---|---|---|
| Leave it. `delegated_s` is the call's own interval, the report says which of the two kinds of harness it is reading, and the agent's wall clock is quoted from the agent's own transcript | nothing — it is what is built | the wait is in no column at all, so the rows' spans do not add up to the run and every reader has to be told the total is short by 12 to 31 per cent. The printed report now tells them |
| Charge the wait: the gap from a spawn's result to the orchestrator's next call becomes `delegated_s`. It comes out of no other column, because no column holds it today — it is added to the row, and the row's `span_s` has to start at the cut for the columns to sum | one arm in `analyse` and a second in `spawn_cycles`, since the window's own start becomes load-bearing; every published cycle span moves | it is a guess where the agent really finished — the orchestrator's next call may come minutes after the report landed, and the gap includes that |
| Join the subagent transcript: `subagent_transcripts` already walks them, and a transcript's first stamp IS its spawn's result stamp, so the join key is exact and measured. `delegated_s` becomes the agent's own span | a walk per cycle, and a row that reads nothing where the transcripts were pruned | nothing about the numbers already published, since it is additive |

Whichever it is, it is a change to what a number means and it belongs to a
work item of its own — #149 is the next row of this release and this is the
same kind of question about the same rows.

## Undecidable from a transcript, and therefore not asked

Between taking report *N-1* and spawning *N*, the orchestrator verifies one
report and frames the next prompt. Nothing in the transcript marks the
boundary between those two acts, so a person could not answer it either
without labelling acts by hand — which is what the per-act split would be.
The whole window is charged to the cycle that follows it, `plan.md` says so,
and the row is read as a band rather than as an attribution.
