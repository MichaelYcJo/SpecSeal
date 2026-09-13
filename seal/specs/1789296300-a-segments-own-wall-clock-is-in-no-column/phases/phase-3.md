# 1789296300-a-segments-own-wall-clock-is-in-no-column — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `8c01e9a` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and a value a segment sources from its own idea of what it is cannot be checked against anything |

## What this phase was asked

Build `plan.md`'s row 3 and nothing past it: the resume slice. Split a segment
transcript at the coordinator's own message rows and emit one row per slice,
named by inheritance from the file's first slice. Where no marker is found and
an idle gap above `analyse`'s 900-second ceiling is, one row prints and the
report names the gap and what it does to the span.

Verified by a two-slice fixture — each slice's span asserted against the
fixture's stamps, and their sum asserted to be less than the file's own — and
a marker-less fixture for the floor. `questions.md` Q2 is settled by a probe
at the top of this phase, before the shape is fixed.

## What this phase found

**Q2 is answered, and the marker is literal rather than structural.** The
probe read all 350 segment transcripts on this machine. 41 hold an idle gap at
or above the 900-second ceiling, 82 such gaps in all, and 61 of the 82 are
followed by a `type=user` row carrying `isMeta` and a bare-string content. The
sentence those rows begin with is the harness's own and is exactly what
`skills/verify/SKILL.md` describes in prose: `The coordinator sent a message
while you were working:`.

**The row shape alone is the wrong marker, and the probe is what showed it.**
The same `isMeta` bare-string shape also carries two things that are *not* a
resume — a notice that the agent's response was cut off mid-stream (7 of the
sampled post-gap rows) and an automated background-task notification (2).
Splitting at those cuts one stretch of work in half, which is a worse error
than not splitting: it invents a boundary rather than missing one. So the
marker is the sentence.

**What that costs is stated at the constant rather than discovered later.** A
harness rewording the sentence stops every split. That failure is loud: the
file falls to the floor, which prints one row **and** names the idle gap the
span now covers, so a reader sees a segment reported over two hours with a
line saying why. The structural marker fails the other way — a working stretch
cut in two, with nothing on the page. Failing toward a visible sentence is the
same direction `report_spawns` already takes.

**The first slice still opens at the spawn's result, so the join is
untouched.** The probe found exactly 350 `type=user` bare-string rows with no
`isMeta` across 350 files — one per file, the spawn prompt. That is what
`opening_stamp` reads, so slicing changes what a row is without changing what
is joined.

**A per-slice token column was rejected, and the reason is #202.**
`token_totals` keys a streamed message by its id and keeps the largest count
each field reached. Re-deriving that per slice means duplicating the rule, and
a message whose rows straddled a slice boundary would be counted in both —
which is #202's own failure shape rebuilt one reader over. So the figure stays
the file's, rides its first slice, and later slices print a dash rather than a
zero a reader would add up. **What this gives up is a per-slice token column**,
and it is in the docstring rather than left to be found. The alternative —
widening `token_totals` to take a time window — would drift three ledger rows
anchored on it to refine a column this work item is not about.

**Reading a real run's output caught two defects no fixture would have.** The
mode printed `6 segments was resumed` and `2 rows above covers an idle gap` —
subject–verb disagreement on a count, which is the class
`test_the_token_line_says_one_transcript_rather_than_1_transcripts` already
polices one line over. Both sentences now put the count in object position, so
no verb has to agree with it at all, and both are pinned at one and at more
than one. The first attempt at the repair moved a word and left the verbs
standing; the case caught that too.

**Executed against a real resumed run.** 34 segment transcripts, 30 spawns, 4
named by nobody with their paths printed, 6 files sliced — one smith into 4,
one sealer into 4. Two rows carried an unsplittable idle gap and the report
named the widest at 22.6m.

**How each case was seen red — the exception `plan.md` names.** These cases
could not fail on a missing key, because the mode already printed a row for a
resumed file. They failed against **that row**: one row where two are owed, at
a span of `140.1m` covering the idle gap, against the 16s and 21s the two
slices actually worked.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The whole-file reading of a resumed segment — one row whose span covers every idle gap in the file | Replaced by one row per slice in the same mode. Nothing else read it: the mode is four commits old and unreleased, so no published reading carries the old shape |
| none else — no printed line, key or number that predates this work item changed | none |
