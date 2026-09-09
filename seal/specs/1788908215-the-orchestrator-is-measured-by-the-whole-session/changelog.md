<!-- specs/1788908215-the-orchestrator-is-measured-by-the-whole-session -->

### Added

- **The orchestrator was the one segment nobody could measure, because the
  only row it had was the whole session.** Every other segment of a chain —
  a smith, a warden, a scribe — is a transcript of its own, so measuring it
  is measuring one file. An orchestrator's segments are spawn cycles inside
  one file, and there was no way to ask for one of them. So three segment
  kinds accumulated bands a later run can be read against and the most
  expensive one accumulated a single cumulative number that answered nothing.

  `session_cost.py --spawns` slices a transcript at its spawn cycles and runs
  the same analysis over each slice, so a cycle carries the numbers a smith
  row carries — span, command time, model time, calls, tools per turn, mean
  turn gap — and the two can sit side by side. A cycle ends when a spawn
  call's result arrives and begins where the row before it ended: the
  **head** is the framing before the first spawn, **cycle N** runs from spawn
  N-1's result to spawn N's, and the **tail** is the closing work after the
  last one. Every paired call in the transcript lands in exactly one of those
  rows, and the printed table says so by putting its own total beside the
  transcript's.

  **The interval the spawn call itself spans leaves the orchestrator's
  numbers**, because whatever ran in it ran in another transcript and is
  already counted there. It is reported beside the row as `delegated`
  instead. The call stays in the count and in the walk that bounds the model
  gaps, because the orchestrator did make it: on a twenty-minute spawn
  between two checks the row reads four seconds of command time, sixteen
  seconds of model time and twenty minutes delegated, where charging the
  interval reads twenty-one minutes of command time and dropping the call
  outright swallows one of the two gaps.

  **How much of an agent's run that interval covers is the harness's answer,
  and the report now says which answer it is looking at.** Measured on this
  one across 67 spawns of three runs: an `Agent` call pairs in 1.5 to 3.7
  seconds, and each subagent's transcript opens at its spawn's result stamp —
  61 of the 67 within a second, the six misses being subagents of subagents,
  which have no call in the main transcript at all. So the result is written
  when the spawn is **accepted**, the agent then runs for a median of about
  1,000 seconds, and that wall clock is in none of the columns of any row: it
  falls between two rows, because a row's span starts at its own first call
  and its model time never counts the gap before it. So the rows partition
  the run's calls and not its wall clock, and the table now prints how much
  time sits between them — 12 to 31 per cent of the three runs measured, of
  which the wait after a spawn's result is 98 per cent. A `delegated` column
  of seconds is the tell, and the report prints the sentence saying so rather
  than leaving a reader to take zeroes for *nothing was delegated*.

  **A row whose span exceeds its own parts by an hour is a different thing,
  and it is not the agent.** That hour is one gap INSIDE the row, above the
  fifteen minutes model time stops counting at — the orchestrator issuing
  nothing between two of its own calls. Every row over 5,000 seconds in the
  three runs measured decomposes that way, with opening gaps of 6 to 580
  seconds beside internal gaps of 1,038 to 6,285. The `delegated` column
  reads 0 to 3 seconds on those same four rows, which is the point: the
  agent's wall clock is the opening gap and never the column named for it.

  **And where a call outlives a spawn's result, the between-the-rows figure
  is refused rather than printed.** Assigning a call by its start is what
  makes the calls partition, and it leaves a long-running one — a background
  command, a suite spanning a cut — in the row it began in while the next row
  has already started, so two rows' spans cover the same seconds and sum past
  the run. The subtraction is then a negative, and a negative printed as *the
  wait* is the one thing this change exists to stop; the report says the
  spans summed past the run instead. No run measured here reaches it.

  **A cycle row is a band and not an attribution**, and the printed report
  says so above the table. Inside one window the orchestrator waits on the
  previous agent, verifies the report it hands over and frames the next
  prompt, and no transcript field marks where any of those ends. Cycle 1 is
  the one row without that window, because the run's own start is a boundary
  a script can take and the framing goes to the head row instead. Splitting
  the acts apart needs a person to label them, which is why it is not what
  this does.

  **Where no spawn is found, the count and the transcript path are printed
  and no table is.** An empty cycle table reads as *this run spawned
  nothing* — and a run that did spawn reads exactly the same way the moment a
  harness stops writing a spawn as an `Agent` block. That is the failure
  shape a wrong family row had for four releases, and it is repaired the same
  way here rather than being discovered the same way twice. (#145)

- `skills/verify/SKILL.md` states the boundary where a session measuring a
  segment reads it, beside the split it already prescribed for a resumed
  agent. That one splits at the user lines the coordinator wrote; an
  orchestrator's boundary is not a user line, and nothing said what it was.
  The paragraph says **spawn cycle** rather than *cycle*, because the review
  chain owns that word for the mark's own unit. (#145)

### Changed

- **Nothing in a reading taken without the new mode moves**, value for value.
  The exclusion of the delegated interval is an argument the plain path does
  not pass, so `--json` and the printed report answer exactly what they
  answered before — the fourth release in a row where a meter change had to
  be weighed against every reading already published. `--json` gains a
  `spawns` key carrying the cycle rows, and a `delegated_s` of 0.0 whose
  meaning is *nothing was removed from the numbers beside it*, never *this
  run delegated nothing*; the `Agent` row of the family table is where that
  second question is answered. (#145)
