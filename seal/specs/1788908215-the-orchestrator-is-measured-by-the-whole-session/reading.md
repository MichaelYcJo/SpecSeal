<!-- Phase 5's output: the draft comment body, for the orchestrator to post.

Destination: the DURABLE log, because this reading is meant to be compared
against a later version's — `skills/verify/SKILL.md` §*Measure the segment,
and feed the flow log* sends a cross-version reading there and the rolling log
is discarded at the next release. Find it by label rather than by number:

  gh issue list --label flow-baseline --state open
  gh issue comment <n> --body-file seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/reading.md

`questions.md` Q2 records that this issue is #145's own work rather than a
separate act. Everything below the marker line is the comment body. -->

---

## The orchestrator's own segments, measured for the first time

Three segment kinds have had bands since #109. This one had a single
cumulative number, because an orchestrator's segments are spawn cycles inside
one transcript and nothing could ask for one of them. `session_cost.py
--spawns` (0.9.5, #145) can, and this is the first reading it produced.

**It is a band and not a conclusion.** There is nothing to compare it against
yet — that is what it exists to become. No cost target is claimed and none is
implied; #145's own *Not this* refuses both.

### What this covers, and what it does not

| | |
|---|---|
| Runs | 3 orchestrator transcripts — one 2026-09-06, one 2026-09-07, one 2026-09-08 |
| Cycles | 61 spawn cycles, plus 3 head rows and 3 tail rows |
| Calls | 953, every one of them in exactly one row |
| Not covered | This release's own run, which was still open when the reading was taken and therefore has no tail row. Every earlier release line: the mode did not exist, and the transcripts are still on disk if somebody wants them retaken |
| Carried from 0.9.4 | These are the first readings taken after the meter's three defects were fixed (#200, #202, #193). Nothing published before 0.9.4 is comparable with them, and the run-level token rows below are the corrected ones |

### The bands

A row's `span` is wall clock; `command` is tools running; `model` is the gap
between one turn's last result and the next turn's first call. Medians, with
the full range beside the span.

| Row kind | n | span median | span range | command | model | calls | mean gap |
|---|---|---|---|---|---|---|---|
| head — the framing before the first spawn | 3 | 9.4m | 6.9–27.9m | 2.3m | 5.1m | 27 | 12s |
| cycle · `specseal:smith` | 15 | 10.9m | 0.6–116.3m | 1.1m | 5.4m | 13 | 29s |
| cycle · `specseal:warden` | 23 | 12.9m | 0.7–97.0m | 0.7m | 8.5m | 13 | 18s |
| cycle · batched — the window holds only the spawn | 23 | 0.0m | 0.0–0.1m | 0.0m | 0.0m | 1 | 0s |
| tail — the closing work after the last spawn | 3 | 16.7m | 3.9–118.1m | 0.9m | 15.7m | 14 | 34s |

And the three runs whole, for the row a run's report already carries:

| Run | span | command | model | in no column | transcripts | turns | output | cache write | cache read |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-06 | 546m | 47.2m | 263.0m | 236m (43%) | 19 | 1,595 | 863,336 | 7,093,323 | 444,570,708 |
| 2026-09-07 | 448m | 65.0m | 201.3m | 182m (41%) | 33 | 2,926 | 915,658 | 9,148,322 | 699,553,378 |
| 2026-09-08 | 164m | 33.3m | 114.7m | 16m (10%) | 18 | 1,141 | 1,240,861 | 4,063,588 | 195,674,158 |

### Three things the reading found, and the first changes how the rest is read

**1. A `delegated` column of seconds, because a spawn's result is written when
the spawn is accepted.** `plan.md` was built on a spawn's result arriving
being the report. It is not, on this harness. Measured over the 67 spawns of
these three runs: an `Agent` call's own `tool_use` → `tool_result` span is
1.5–3.7 seconds, and each subagent's transcript **opens** at its spawn's
result stamp — 61 of the 67 within one second, the six misses being subagents
of subagents, which have no call in the main transcript at all. The agent then
runs for a median of about 1,000 seconds while the orchestrator issues
nothing.

So the delegated wall clock is **not** in the column named for it. It is in
the next row's `model`, until the wait passes the 900 seconds `analyse` stops
counting a gap at — beyond which it is in **no column**, which is what the *in
no column* figures above are and why one smith cycle reads a 116-minute span
against 11.5 minutes of parts. The exclusion `--spawns` performs is therefore
correct and nearly free here rather than wrong, and it is the whole answer on
a harness that writes the result at completion. What `delegated` should
measure instead has three costed answers in the work item's `questions.md` Q4
and is the owner's call; the join a future answer needs is already exact,
since a subagent transcript's first stamp **is** its spawn's result stamp.

Read the bands with that in mind: a cycle's `model` is mostly the orchestrator
**waiting**, not the orchestrator thinking.

**2. Not one batched call, in 953.** Counted from the raw transcripts rather
than through the meter, because 1.00 tools per turn is exactly the shape of a
meter defect this repository has already had once: every message carrying a
tool_use carries **exactly one**, in all three runs — `{1: 497}`, `{1: 147}`,
`{1: 309}` as the calls-per-message distribution. So every row of every run
reads 1.00, and it is real. Even the consecutive spawns are consecutive
single-call turns, not one message spawning several. At a mean gap of 18–29
seconds a cycle, that is the batching advisory's own case, made by the
orchestrator against itself.

**3. A third of the cycle rows hold nothing but their own spawn.** 23 of 61,
reading 1 call and a span under a tenth of a minute. Those are the second and
later spawns of a group sent back to back: the boundary closes a cycle at each
spawn's result, so a group of four produces three near-empty rows and charges
the whole subsequent window to the fourth. It is not noise to filter — it is
what the boundary does with a group — but a band taken across all 61 cycles
without separating them would halve every median. That is why the table
above separates them, and why a later reading has to separate them the same
way to be comparable.

### What is not claimed

No target, and no comparison. The one thing to check against this is the next
reading of the same kind: whether a cycle's span moves, and whether the *in no
column* share shrinks once it is known what it is made of.
