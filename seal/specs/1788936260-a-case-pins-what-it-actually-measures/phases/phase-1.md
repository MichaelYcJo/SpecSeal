# 1788936260-a-case-pins-what-it-actually-measures — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | <pending> |
| Ran by | unknown — the spawn prompt carried no `Ran by` value, and this row is the spawning session's rather than the segment's own; the orchestrator fills it |

## What this phase was asked

Replace the four assertions in
`test_the_section_names_batching_as_the_way_a_share_passes_one_hundred` with
#310's verified whole-clause version. Verified transcription, taken first
because it is the smaller half and independent of the checker.

Two conditions came with it. The paste-ready block in #310 is the source —
this is transcription, not design. And the five mutation arms are re-derived
here rather than taken from the ticket: `skills/verify/SKILL.md` restored
byte-for-byte from held bytes and sha256-compared after each arm, never with
`git checkout`.

## What this phase found

**The three rearrangements are what the substring assertions could not see,
and the probe separated them from the two the old case already caught.** #310
reported five arms all red against the new assertions and did not report which
of them the OLD assertions passed. Running both assertion sets against the
same mutated body, in the same probe, splits the five:

| Arm | Old assertions | New assertions |
|---|---|---|
| 1 causes swapped | **green** | red — clause 2 |
| 2 measurement inverted | **green** | red — clause 3 |
| 3 old phrase sentence-initially | **green** | red — clause 4 |
| 4 old phrase lowercase mid-sentence | red | red — clause 4 |
| 5 concurrency phrase removed | red | red — clause 1 |

The three greens in the first column are the whole of #310. They are
rearrangements of true words, and the two arms the old case caught are both
deletions or additions of a phrase. That is the class stated as a measurement
rather than as an argument: **a substring assertion sees a phrase appearing or
disappearing and cannot see one moving.**

**`section_body()` collapses whitespace, which is what makes a whole-clause
assertion affordable.** The two long clauses span three and four source lines
in `skills/verify/SKILL.md`, so asserting them whole against the raw text
would pin the wrap column. The mutation patterns in the probe carry the file's
own line wrapping for the opposite reason — they are applied to the raw bytes,
where a pattern that misses is a silent no-op, so each is asserted to match
before it is written and the file is asserted to differ after.

**The restore discipline earned itself inside this phase.** The working tree
carried the phase-1 edit to `tests/test_a_segment_feeds_the_flow_log.py` while
the probe was mutating `skills/verify/SKILL.md`. `git checkout --` of a
mistyped path would have taken the phase's own work with it, which is the
defect the plan names from four fix passes today. Held bytes and a hash
compare have no such path: original `fd3a4e7d285d`, restored `fd3a4e7d285d`
after each of the five arms and again at the end.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The substring assertions `"batched into one message"` and `"crossed a turn"` | Absorbed, not dropped — both phrases sit inside the whole clause that replaced them, so the vocabulary they pinned is still pinned and the direction it did not pin now is |
| The case-sensitivity of the negative assertion (`not in body` → `not in body.lower()`) | Nothing needs to own it: it was the arm-3 gap, and lowering it is the fix rather than a loss |
