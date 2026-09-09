# 1788908215-the-orchestrator-is-measured-by-the-whole-session — overview

The orchestrator is the most expensive segment in a chain and was the only one
with no band, because its segments are spawn cycles inside one transcript and
nothing could ask for one of them; `session_cost.py --spawns` can, and the
first reading it produced is drafted for the durable log.

## Where spec and implementation diverged

**1. Where the head ends.** Both sides are in the contract and they disagree.

> `plan.md` §Technical context — "The run's head (before report 1) and tail
> (after the last report) are their own rows."

> `spec.md` §Scope — "the framing before the first spawn, and the closing work
> after the last report." And its acceptance row: "the calls **before the
> first spawn** and after the last report are each reported as their own row."

`spec.md` won. Bounding the head by the first result would put the framing and
the first spawn's whole wait in one row and leave cycle 1 empty, and the
acceptance row is the more specific of the two and is what a case can assert.
Consequence, stated on the page rather than left to be found: cycle 1 is the
one cycle without a verify-and-frame window, because that window went to the
head.

**2. What a spawn's result means — and this one was measured false, not
chosen.**

> `plan.md` §Technical context — "A spawn is an `Agent` `tool_use` block; **its
> result arrival is the report.**"

Measured over the 67 spawns of three orchestrator runs: an `Agent` call's own
`tool_use` → `tool_result` span is 1.5–3.7 seconds, and each subagent's
transcript **opens** at its spawn's result stamp — 61 of the 67 within one
second, the six misses being subagents of subagents, which have no call in the
main transcript at all. The result is written when the spawn is **accepted**.
The agent then runs for a median of about 1,000 seconds.

So `spec.md`'s reason for `delegated_s` is right about the double count and
wrong about where it is:

> `spec.md` §Scope — "A subagent's thinking is already counted in that
> subagent's row; charging it to the orchestrator too is the double count that
> makes a cumulative reading look like a slow orchestrator."

The double count is real and it is in **no column of any row**. It falls
between two rows: `analyse` starts a window's `span_s` at that window's own
first call and its model walk never counts the gap before that call, so the
wait after a spawn's result is outside every column of the row that follows
it — under the 900-second ceiling as much as above it. Measured over the three
runs, that interval is 12 to 31 per cent of each run's wall clock.

A row whose span exceeds its own parts is a **separate** thing, and round 1
found four pages conflating the two. The cycle that reads 116 minutes against
11.5 minutes of parts owes the difference to one gap of 104.8 minutes *inside*
the cycle, above the ceiling — the orchestrator issuing nothing between two of
its own calls. That row's opening gap is 580 seconds, against a `delegated`
column reading 2 seconds — the two quantities the pages had conflated.

**What was NOT done about it, deliberately.** The code was built to `plan.md`
and left that way: the exclusion is right and nearly free on this harness, and
it is the whole answer on a harness that writes the result at completion. What
changed is that nothing on the page says something false — the report names
what `delegated` measures, calls a cycle row a band, and prints a sentence
naming which kind of harness it is reading when `delegated` never reaches a
minute. Changing what `delegated_s` MEASURES moves a published number, so it
is `questions.md` Q4 with three costed answers, and the owner's.

The premise stays in `spec.md` and `plan.md` as written. Editing it out would
delete the evidence that the Design Gate approved it, and `survivors.md`
records each surviving copy with grounds.

**3. Two `--json` keys where `questions.md` Q1 named one.** Q1 said "`--json`
gains a `spawns` key beside the existing ones"; `delegated_s` is there too,
because `analyse` returns it and the acceptance row asks that "the cycle row's
keys equal the whole-run row's keys" — which is literally assertable only if
the whole run carries it as well. On the whole-run row it is 0.0 and means
*nothing was removed from the numbers beside it*, never *this run delegated
nothing*.

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator — `skills/agent-contract/SKILL.md` §2 makes the broad gate theirs, run once after the rounds settle |
| Whether the reading actually reaches the durable log | the orchestrator — phase 5's posting is theirs, and `gh issue comment` was not run |
| ✅ `Ran by` on all five phase records | filled at `e389fc1`, a commit that touches those five rows and nothing else — the reach-back `templates/sdd-phase.md` names beside the spawn-prompt route. All five read `specseal:smith on claude-opus-5`. Read at the coordinates in round 1's fix pass; what the template forbids is a segment sourcing the value from its own idea of what it is, and a standalone later commit is the other route it permits |
| The whole-run reading charges a spawn's prompt to a command family, so a prompt naming `pytest` outside a heredoc classifies as a test run and two prompts differing only after a `\|` read as a check re-run | the owner — it is fixed inside cycle rows and deliberately left in the whole-run path, which must not move; it wants a work item of its own |
| Windows | nobody has run this on it — #103's standing gap, not this branch's |

## What was fed back into the spec

Two clauses, both *inferred during implementation* and both overturnable:

- **A cycle is bounded by a spawn call's RESULT arriving**, which is a
  transcript fact, where *the report arriving* is an interpretation of it that
  depends on the harness. The distinction is now in `skills/verify/SKILL.md`,
  in the script's docstrings, and in both fragments.
- **A group of spawns sent back to back produces near-empty cycle rows** — 23
  of the 61 cycles measured — and a band that does not separate them from
  cycles holding work halves every median. Any later reading has to separate
  them the same way to be comparable. This is in `reading.md` and is the one
  thing a comparison against this reading can get wrong for free.
