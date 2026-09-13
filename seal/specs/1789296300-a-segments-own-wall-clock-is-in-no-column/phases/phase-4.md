# 1789296300-a-segments-own-wall-clock-is-in-no-column — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `fce9ba0` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and a value a segment sources from its own idea of what it is cannot be checked against anything |

## What this phase was asked

Build `plan.md`'s row 4 and nothing past it: #343. Each segment row carries
its own spawn count, taken from that segment's own `Agent` calls; a non-zero
count prints a line naming the agent, the count and §6. The count of nested
transcripts is reconciled against it, and a disagreement is printed rather
than resolved.

Verified by a fixture where a named segment's transcript holds an `Agent` call
and a nested transcript sits under it: the line names the agent and the count.
**The negative case — segments with no `Agent` call print no line — is what
keeps this from being a check that cannot fail, and it is planted in the same
commit.**

## What this phase found

**The instrument found the breach on real data, thirteen times.** Run across
all 43 runs with a `subagents/` directory on this machine: exit 0 on every
one, and **13 of the 43 carry a §6 finding**. One of them is a
`specseal:warden`, which is precisely the act #343 was written about — an
agent that spawned another agent with the rule already in its payload. This is
the answer to the question #343 could not settle from inside a transcript:
the act is not rare and it is not hypothetical.

**The count is per slice, not per file, and phase 3 is why.** A resumed agent
is several rows, and a breach attributed to the file would name an agent
without saying which of its stretches did it. Putting the count on the slice
costs one line and makes the report's own label — `specseal:smith 2/4` —
the thing that identifies the breach.

**The reconciliation earns its place on the disagreeing case, not the
agreeing one.** A spawn inside a segment arrives twice, as a call in the
spawning segment's file and as a transcript the parent cannot name. The
fixture where they agree is easy; what settles the design is the fixture where
they do not — an agent that spawned and whose child's transcript is absent.
Nothing in the file can tell that from a segment unnamed for the other reason,
its opening outside the tolerance. Both numbers print and the page says
whether they agree, which is `report_spawns`' partition tally one mode over.

**One case here can never be seen red, and it is named rather than counted as
evidence.** `test_the_mode_still_exits_zero_when_it_finds_a_breach` passes
against the code as it stood, because exit 0 was already true. It is a guard
against a later change turning the report into a gate, not a case that
demonstrates this phase's behaviour. Every other case in this phase was red
first: the row-shape ones on `KeyError: 'spawns'`, the printed ones on the
absence of `§6` from a report quoted back by the assertion.

**The negative half cannot be seen red on its own either, and that is the
nature of a negative case.** What makes it worth having is that its positive
twin was red and went green in the same commit: the same code path that
prints `§6` for a segment that spawned is asserted silent for two segments
that did not.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds a key to a row and two blocks to a report that is four commits old and unreleased | none |
