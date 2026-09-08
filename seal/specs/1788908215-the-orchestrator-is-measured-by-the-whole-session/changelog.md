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
  turn gap — and the two can sit side by side. A cycle ends when a subagent's
  report arrives and begins where the row before it ended: the **head** is
  the framing before the first spawn, **cycle N** is report N-1 arriving until
  report N arrives, and the **tail** is the closing work after the last
  report. Every paired call in the transcript lands in exactly one of those
  rows, and the printed table says so by putting its own total beside the
  transcript's.

  **The subagent's wait leaves the orchestrator's numbers.** An `Agent` call
  spans an interval that is a subagent thinking, already counted in full in
  that subagent's own row — charged here too, it is the double count that
  makes a cumulative reading look like a slow orchestrator. It is reported
  beside the row as `delegated` instead. The call itself stays in the count
  and in the walk that bounds the model gaps, because the orchestrator did
  make it: on a twenty-minute spawn between two checks, the row reads four
  seconds of command time, sixteen seconds of model time, and twenty minutes
  delegated, where charging the interval reads twenty-one minutes of command
  time and dropping the call outright swallows one of the two gaps.

  **A cycle row is a band and not an attribution**, and the printed report
  says so above the table. Between a report arriving and the next spawn going
  out the orchestrator verifies one report and frames the next prompt, and no
  transcript field marks where the first act ends — so the whole window is
  charged to the cycle after it. Cycle 1 is the one row without that window,
  because the run's own start is a boundary a script can take and the framing
  goes to the head row instead. Splitting those two acts needs a person to
  label them, which is why it is not what this does.

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
