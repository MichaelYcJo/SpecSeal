# 1788908215-the-orchestrator-is-measured-by-the-whole-session — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 1763b61 |
| Ran by | unknown — the spawn prompt named no model. `templates/sdd-phase.md` makes this row the spawning session's and forbids a segment sourcing it from its own idea of what it is, so it is left for the orchestrator to fill |

## What this phase was asked

`spawn_cycles(calls)` — the pairs, the windows, the head and tail rows, with
every call landing in exactly one row. Verified by a case over two fixtures
(two spawns · no spawn) and the partition case.

The spawn prompt added two things `plan.md`'s row does not carry: that the
partition case is what stops a slice quietly dropping the run's closing work,
and that a run with no `Agent` call must not print an empty cycle table.

## What this phase found

**`spec.md` and `plan.md` disagree about where the head ends, and the
acceptance row is what settled it.** `plan.md` §Technical context says *the
run's head (before report 1)*, which would put the framing AND the first
spawn's whole wait in one row and leave cycle 1 with nothing. `spec.md`
§Scope says *the framing before the first spawn*, and its acceptance row says
*the calls before the first spawn and after the last report are each reported
as their own row*. Built to `spec.md`: the head ends where the first spawn
goes out. The two are still readable as one rule — each row ends at a spawn
result and begins where the last ended — with the head's end being the run's
own first spawn rather than a result.

**Cycle 1 is therefore not the same shape as cycles 2..N**, and that is not a
defect to hide. Cycles 2..N carry the window in which the orchestrator
verified the previous report and framed the next prompt; cycle 1 carries
neither, because the framing went to the head. The rows are printed together
so the two are read together, and both docstring and report say so.

**Spawns are ordered by when their RESULT arrived, not by when they went
out.** A batch's second agent can finish first, and the cycle it names is the
window ending at its own result — its call sits in the first one's cycle,
which is where the orchestrator made it. Nothing else in the module can tell
the two orderings apart, because everywhere else a spawn's result arrives in
send order, so the case for it needed a fixture where one message's two blocks
carry different row stamps.

**The partition is by ONE instant per item — a call's `start`.** Assigning
by overlap would put a call that outlived a result in two rows and make a sum
over the rows exceed the run. The cuts run through a running maximum so they
never go backwards, which only matters for a result stamped before its own
call; that arm survived the first mutation round and now has a case.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
