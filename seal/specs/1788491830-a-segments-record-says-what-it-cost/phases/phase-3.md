# 1788491830-a-segments-record-says-what-it-cost — phase 3

<!-- seal/specs/1788491830-a-segments-record-says-what-it-cost/phases/phase-3.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | bf2eddc |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 3 only: `skills/verify/SKILL.md` says the spawning session fills
the row, because it is the one that knows. Verified by a case pinning the
sentence.

## What this phase found

**The plan named one skill and two needed it, and the second one is the
urgent half.** `skills/code-review/SKILL.md:167` enumerates every mandatory
row of `round-N.md` in a single cell — target SHA, verdict table, probes,
inherited coordinates, deferrals, broad gate, who checked the fixes, the fix
surface, `Needs a fix`, the floor. An orchestrator writing a round record
reads that list and nothing else, so leaving `Ran by` out of it shipped a
skill whose own output phase 2's checker refuses. That is this repository's
three-times-learned failure arriving from the opposite direction: not a check
landing before the instruction, but an instruction that never grew the row the
check now reads.

So the row went into both, and the two are read by different sessions at
different moments — `code-review` by the orchestrator writing the round
record, `verify` by whoever watches a segment end and posts its numbers. The
case that pins them is parametrised over both for exactly that reason.

**Two sentences carry what the row cannot say for itself**, and both are
pinned rather than left to a reader's inference:

- whose row it is. Shown without it, the row reads as something the segment
  reports about itself, and the subject is the one filler whose answer nothing
  can check against anything.
- that `unknown` needs its reason. A skill teaching only the confident answer
  gets the confident answer written, true or not.

**A sweep that checks a name is not a sweep that checks a row.** The
`INSTRUCTORS` case first asserted `"Ran by" in read(...)` for all five files,
and the mutation renaming the protocol's `| Ran by |` row to `| Run by |`
survived it — the protocol also says `Ran by` in the prose section and the
drafts log around the table, so the name was still there while the row was
gone. The needle now differs by kind: the three files carrying it AS A ROW are
pinned on the row, and the two skills, which carry no table, on the name.

That is the same shape as phase 2's survivor and worth naming as one class: a
case whose needle is satisfied by something other than the thing it means to
pin is green against its own mutation. Both survivors this work item produced
were of it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
