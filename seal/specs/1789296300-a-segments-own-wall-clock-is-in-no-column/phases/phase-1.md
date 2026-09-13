# 1789296300-a-segments-own-wall-clock-is-in-no-column — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `dea1e7c` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and a value a segment sources from its own idea of what it is cannot be checked against anything |

## What this phase was asked

Build `plan.md`'s row 1 and nothing past it: the join. A reader for a
transcript's first stamp, and `segment_rows()` matching each transcript under
`subagents/` to a spawn result within the tolerance — named where it matches,
named by nobody where it does not, one spawn claimed at most once. `--json`
gains a `segments` key beside `spawns`. Verified by cases on a tree built by
`write_run`: a named segment, an unnamed nested one, a segment moved outside
the tolerance, and a run with no `subagents/` directory, each red first.

`questions.md` Q3 — is one second still the right tolerance — is settled by a
probe at the top of this phase.

## What this phase found

**Q3 is answered and the number does not move: 1.0 second.** The probe read
every run with a `subagents/` directory on this machine — 43 of them, 349
segment transcripts, 305 `Agent` calls in the parents — and ran the one-to-one
rule `join_segments` actually uses. 296 of 349 named at 1.0 s, 301 at 2.0 s.
Widening to two seconds buys five segments of 349 and doubles the window in
which a batch of two spawns can match the wrong one. The remainder it does not
buy is structural: 349 transcripts against 305 spawns means 44 have no call in
the parent to be named by at **any** tolerance. The probe was deleted.

**A fact the frame did not have, and it changes what a fixture is realistic
about.** `spec.md` and `plan.md` both describe the unnamable segment as *a
nested transcript under another segment's directory*. On the harness measured
here it is not nested: all 349 transcripts sit **flat** under `subagents/`,
including subagents of subagents, and the probe found zero files at any depth
below one. So what makes a segment unnamable is the absence of an `Agent` call
in the parent, never the directory it sits in. Nothing needs repairing —
`subagent_transcripts` walks rather than lists, so both shapes are already
covered, and the phase-1 case keeps the nested fixture because the walk
supports it and `test_a_segment_of_a_segment_is_still_part_of_the_run` already
uses that shape. What would have been wrong is a join that inferred *unnamed*
from *nested*, and it does not: it infers it from the match failing.

**The row's numbers come from `analyse` with no `delegated`, and that is a
decision rather than an omission.** A segment row has to be the same number a
person gets running this script against that one transcript today, because the
mode replaces the hand method `skills/verify/SKILL.md` prescribes. A row
computed with `delegated=DELEGATING` would be a second meter with its own
rules, and no reading already taken could be compared with it.

**An existing case caught the new key on the commit that added it, which is
what it was built to do.** `test_a_cycle_carries_the_same_numbers_the_whole_run_does`
derives the whole run's `analyse` keys as `set(data) - {"tokens", "spawns"}`,
so `segments` broke it. Its own docstring says adding a top-level key is *a
decision somebody makes here rather than a key that appears in a published
reading* — so the exclusion list gained `segments` and the docstring records
why it is not one of `analyse`'s keys. This is the case working, not a
regression.

**Executed against a real transcript, not only fixtures.** The mode read a
current SpecSeal run: 6 segment transcripts, 6 spawns, 0 unnamed, 0 unclaimed,
with per-agent spans of 5.9m, 8.5m, 8.9m, 7.7m, 7.1m and 6.8m. Those six
numbers are what is in no column of any `--spawns` row.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase is additive; no existing printed line, key or number changed | none |
