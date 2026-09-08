# Implementation Plan: the orchestrator segment is measured by the whole session

## Summary

Slice an orchestrator's transcript at its spawn cycles and run the existing
analysis over each slice, so the most expensive segment in a chain produces a
row the other three kinds' rows can be read beside. Then write the boundary
into `skills/verify/SKILL.md` and post one reading.

## Technical context

`session_cost.py` already separates the two things a slice needs. `load`
(`skills/verify/scripts/session_cost.py#load`) returns calls carrying
`start`, `end`, `tool`, `command` and a `turn` key, and `analyse`
(`#analyse`) is a pure function of `(calls, turns)`. So a cycle is a filter
over the call list and a second `analyse` call — not a second meter.

**The boundary, stated exactly, because this is the decision the ticket is
about.** A spawn is an `Agent` `tool_use` block; its result arrival is the
report. Cycle *N* runs **from the arrival of report *N-1* to the arrival of
report *N*** — the orchestrator becomes free, writes the next prompt, waits,
and takes the next report. The run's head (before report 1) and tail (after
the last report) are their own rows.

**What that boundary cannot separate, said here rather than found later.**
Between report *N-1* and spawn *N* the orchestrator does two different acts —
verifying the report it just took, and framing the next prompt — and no
transcript field marks where one ends. The whole window is charged to cycle
*N*, so verifying report *N-1* is counted in the cycle after it. This is the
one thing the per-act split (#145's second candidate, out of scope) would
answer, and it is why the cycle row is a band rather than an attribution.

**Failure scenario, in six months.** A harness renames the spawn tool, or
spawns arrive through a path that writes no `tool_use` block, and the mode
reports zero cycles on a run that had six. That reads as *this run spawned
nothing*, which is #200's failure shape exactly. So the mode names the
count it found and refuses to print a cycle table when it found none, with
the transcript path beside it — the same repair #200 took.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Spawn cycle, bounded by consecutive `Agent` results | Cannot separate verifying a report from framing the next prompt (above) | **Chosen.** It is the only boundary in the ticket's three that a script can take unattended, and it makes the row comparable to a `smith` row, which is what #51's observation 1 is missing |
| Per act — framing · prompt · verify · record · issue | Needs a person to label each act, so no reading is ever produced without one. Refused by `CLAUDE.md`'s first goal, and the labels would be invented before a cycle-level reading exists to argue against | Out of scope, and the finer split this one's residual points at |
| Split at user lines, as the resumed-agent rule does | An orchestrator's user lines are the human's messages, which bound nothing about orchestration. A run with one user message yields one slice — today's cumulative number, renamed | Rejected |
| Fixed wall-clock windows | Comparable to nothing. A ten-minute window holds part of a spawn on one run and three on another | Rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `spawn_cycles(calls)` — the pairs, the windows, the head and tail rows; every call lands in exactly one row | a case over two fixtures (two spawns · no spawn) and the partition case | |
| 2 | Per-cycle numbers: `analyse` over each window, with the `Agent` call's own duration excluded from model time and reported as `delegated_s` | the fabricated 20-minute-`Agent` case | |
| 3 | The printed report and `--json`: a row per cycle naming its `subagent_type`, and the refusal-with-count when no spawn was found | a case reading the rendered text, and one reading the JSON keys | |
| 4 | `skills/verify/SKILL.md`'s instruction beside the resumed-agent one; the changelog and ledger fragments | the suite, and `evidence-check` on the fragment | |
| 5 | The first reading: the mode over this release line's own orchestrator transcripts, posted to #51 with what it covers stated beside the number | the posted comment | |

## Operational impact

None to deploy. One new CLI mode, additive; no existing output changes
shape, which is what keeps every reading already published comparable to
what this prints.
