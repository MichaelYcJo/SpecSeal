# 1788908215-the-orchestrator-is-measured-by-the-whole-session — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 1763b61, corrected at 2dbcdb2 |
| Ran by | `specseal:smith on claude-opus-5` — filled by the spawning session, which is the only participant that knows what it spawned |

## What this phase was asked

The printed report and `--json`: a row per cycle naming its
`subagent_type`, and the refusal-with-count when no spawn was found.
Verified by a case reading the rendered text and one reading the JSON keys.

The spawn prompt named the failure this repays: #200, a family row that read
as *no test run happened*, silently, in every reading this repository
published.

## What this phase found

**`spawns` goes in `--json` unconditionally rather than behind the flag.**
`questions.md` Q1 puts it *beside the existing keys*, and a reading taken
with `--json` and no `--spawns` would otherwise be missing the one thing
this work item exists to produce. `--spawns` selects the printed report
instead.

**A cycle carries no token count and cannot.** `load` gives tokens per
TURN, and the tokens a spawn spent are in the subagent's own transcript — a
per-cycle token column would be summing the wrong file. So `--spawns`
returns before the token walk, which also makes it fast.

**The refusal names the count rather than printing an empty table**, with the
transcript path beside it. Both halves are load-bearing: an empty table reads
as a run that spawned nothing, and a run that DID spawn reads identically the
moment a harness stops writing a spawn as an `Agent` block.

**The partition is printed even when it agrees** — *N calls over the rows
above, of N calls in the transcript*. The rows rest on that property, so the
reader gets to watch it hold rather than taking the file's word for it.

**Then running it over real transcripts made part of this phase's own page
false, and it was corrected at `2dbcdb2`.** The legend said *report N-1
arriving until report N arrives*. Measured over 67 spawns of three runs, an
`Agent` call pairs in 1.5–3.7 seconds and every subagent transcript opens at
its spawn's result stamp, so the result is written when the spawn is ACCEPTED.
The legend now says what the transcript actually holds, the report calls a
cycle row a band over several acts, and it prints a sentence naming which of
the two kinds of harness it is reading whenever `delegated` never reaches a
minute — a column of near-zeroes taken for *nothing was delegated* being
#200's failure shape one column over. That disclosure is the thing this phase
would have shipped wrong.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The legend's claim that a cycle is bounded by a report arriving | The corrected legend and `spawn_cycles`' docstring, both at `2dbcdb2`; the same wording elsewhere in the branch was corrected in the same commit, and the copies left standing in `spec.md`, `plan.md` and `questions.md` are the approved contract and are recorded in `survivors.md` with grounds |
