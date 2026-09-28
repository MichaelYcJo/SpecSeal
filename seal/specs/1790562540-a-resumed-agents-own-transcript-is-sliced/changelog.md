- **`session-cost --segments` given a resumed agent's own transcript prints
  one row per stretch of work (issue #637).** It printed `0 segments found`,
  because it only ever looked for transcripts beside the file it was given,
  and an agent's own file never has any. That file is the path a harness's
  task output hands the orchestrator, so the mode that exists to split a
  resumed agent was the one reading a fix pass could not get. A file with no
  transcripts beside it and at least one coordinator message is now cut at
  those messages, with the same numbers the mode prints for that agent when
  it walks the run's transcript. Its rows are named by the file, because the
  spawn that would name them is in the run's transcript. The page says so in
  a header naming the file, its coordinator messages and its slices, in
  place of the join counts. The §6 list still names a spawn made inside a
  slice, and the line reconciling it against unnamed transcripts is left
  out, because no parent was in view to reconcile against. `--json` carries
  the same rows and one added key, `own_file`, present only in this case.
  The trigger is the coordinator's message and not the directory, so a file
  the coordinator never restarted keeps the empty branch byte for byte,
  wherever it sits.
- **The plain reading of such a file says it holds a restarted agent.**
  `session-cost <transcript>` on a file with coordinator messages and
  nothing beside it prints one added line before the span, counting the
  messages and saying the span covers every stretch of work and the waits
  between them, and that `--segments` prints one row per stretch. Every
  number and every other line it prints is unchanged.
- **Readings this bears on, none of which becomes wrong.** Fix-pass
  readings posted as the whole resumed transcript, build and fix together,
  because `--segments` could not split it: four in #577, four in #535 and
  six in #601. Fix-pass readings taken from the harness's own completion
  figures for the same reason: four in #496 and three in #619. Counted
  2026-09-28 by the phrase each comment uses for its source. Each is a true
  reading of what it names. What this change makes possible is re-deriving
  the fix pass alone from the same file, which is its own work.
