# 1788908215-the-orchestrator-is-measured-by-the-whole-session — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 1763b61 |
| Ran by | `specseal:smith on claude-opus-5` — filled by the spawning session, which is the only participant that knows what it spawned |

## What this phase was asked

Per-cycle numbers: `analyse` over each window, with the `Agent` call's own
duration excluded from model time and reported as `delegated_s`. Verified by
the fabricated 20-minute-`Agent` case.

## What this phase found

**The exclusion cannot be done by removing the call from the list.** The
acceptance row asks for *model time unchanged, delegated = 1200s*, and
dropping the spawn out of the calls handed to `analyse` collapses the gap
either side of it into one — the delegated interval then lands in model time,
which is the opposite of what was asked. The call has to stay in the walk that
bounds the gaps and lose only its duration. The case separates all three
implementations: charging the interval reads 1266s of model or 1204s of
command, dropping the call reads 7s of model, and what is right reads 16s.

**The whole-run reading had to stay byte-identical, so the exclusion is a
parameter the plain path does not pass.** Every reading this repository has
published was taken without the mode, and 0.9.4 exists because three meter
numbers moved without anything saying so. `analyse(calls, turns,
delegated=())` keeps the old behaviour exactly; the cycle rows pass
`DELEGATING`.

**That costs one more `--json` key than `questions.md` Q1 named** —
`delegated_s` beside `spawns` — and it buys the acceptance row *the cycle
row's keys equal the whole-run row's keys* being literally assertable. The
divergence is in `overview.md`. `delegated_s` is 0.0 on the whole-run row
and means *nothing was removed from the numbers beside it*, never *this run
delegated nothing*.

**The numbers are nested under `numbers` rather than spread beside the row's
labels, because `analyse` already returns a key called `calls`.** A flat
row would have had to shadow it. Nesting is also what lets a slice with no
calls keep its row with `numbers` at null, which the partition needs.

**A spawn's `command` is the JSON dump of its whole input.** So the family
classifier reads a prompt as a command line: a prompt naming `pytest`
outside a heredoc classifies as a test run, and two prompts differing only
after a `|` — which is what markdown tables make of real spawn prompts —
collapse into one repeat group and read as a check re-run for a result already
in hand. Delegated calls are kept out of the repeat groups and out
`slowest` for that reason. The same defect is in the WHOLE-run reading and
is deliberately left there, because that path passes no `delegated` and must
not move; it is named in the hand-back.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
