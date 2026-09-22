# Measuring a run — what a segment cost, and what the number means

A run is a sequence of segments, each one an agent spawned for a piece of
work. This document is the standing account of what gets measured, what the
measurement is read against, and where a reading goes so somebody can use it.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

`docs/review-handoff-protocol.md` §*After the run — the per-segment bars*
holds the bar each kind of segment is judged against, and it stays there
because it is part of what a handoff carries. This document is about the
measurement itself.

## The unit is a segment, and a segment has its own transcript

<!-- specs/1789296300-a-segments-own-wall-clock-is-in-no-column -->
**A spawned segment is measured from its own transcript, not from the
parent's columns.** The parent sees a spawn go out and a result come back;
what happened in between is a session of its own, with its own turns, its own
gaps and its own wall clock. A segment named by matching its transcript's
opening stamp against a spawn's result stamp is a **join**, and a join is
asserted rather than assumed — a match within a tolerance is a claim about
which transcript belongs to which spawn, and an unasserted one silently
attributes one agent's cost to another.

<!-- specs/1788908215-the-orchestrator-is-measured-by-the-whole-session -->
**An orchestrator measured by its whole session is measured by its
children.** A session that spawns agents contains their durations, so the
orchestrator's own row reads as the sum of everything it delegated. The
transcript is sliced into spawn cycles and each reported as its own segment,
carrying the same numbers a spawned row carries, so an orchestrator row can
sit beside them — and **the delegated interval is excluded from the
orchestrator's model time and reported as its own number**, because time
spent waiting for another agent is not time spent thinking.

<!-- specs/1788613827-a-runs-report-carries-one-comparison-table -->
**A run's report is one comparison table.** Tokens are summed over the
transcript given **and** every subagent transcript beneath it, so the total
is the run's rather than the parent's. One table, one shape, for every run —
a report whose shape changes between runs cannot be compared with the run
before it, which is the only thing a cost number is for.

## What a measurement must survive, and what it must not invent

<!-- specs/1788700685-two-value-shaped-odd-rows-end-the-report -->
**A degenerate reading is reported, never divided by.** A paired call whose
request and result share a timestamp has a span of zero, and four divisions
downstream of it end the report with the span line printed and the token
block lost. A transcript mixing a zone-aware stamp with a naive one ends it
with nothing printed at all. What the meter owes is a report that survives
both; what it must not do is invent a percentage for a span of zero.

<!-- specs/1788873620-two-in-range-values-make-one-that-is-not -->
**Two in-range values can make one that is not.** Every site converting a
number for display is enumerated from the module's own source, with
membership decided by running the code rather than by a list of names, and
each one is discharged — by a guard, or by an operand that cannot be a
derived number. A list of names goes stale the moment somebody adds a site;
an enumeration from the source cannot.

<!-- specs/1788904490-every-published-reading-carries-three-wrong-rows -->
**A reading that was published is still wrong after it is published.** Three
defects in one meter put a wrong row into every reading it had ever produced
— a family classification, a per-message deduplication, and an input filter.
Correcting the code does not correct the readings, and re-deriving them is
its own work: what the correcting work item owes is to say which published
numbers are affected, so nobody reasons from them in the meantime.

<!-- specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is -->
**A refusal names the cut its row ends at, not the event it went looking
for.** A head row's cut is the first spawn's *start*, so a head call can
outlive its own row's cut and end before any spawn's result — and a refusal
naming the result as the cause pointed at a call the transcript does not
contain. A refusal that prints two sums rather than their difference leaves
the reader able to see which of the two is wrong.

## Where a reading goes

<!-- specs/1788449488-measure-what-flow-finds -->
**A measurement nobody posted is a measurement nobody has.** Whichever
session watched a segment finish is the only party still holding its
transcript, so that session measures the segment and posts what it found to
the repository's rolling measurement log — by label rather than by number, so
the destination survives the log being rolled. A repository with no such log
gets nothing and is told so; the instruction is unconditional prose and the
posting is conditional on a place to post to.

Two readings are kept apart because they answer different questions: the
rolling log holds what this version's runs cost, and the durable log holds
findings that outlive a version. A repository declares its durable one with a
second label, since the instruction ships to repositories that have no such
issue at all — and **a repository that never measured and one that stopped
are told apart**, because both used to be the same silence.
