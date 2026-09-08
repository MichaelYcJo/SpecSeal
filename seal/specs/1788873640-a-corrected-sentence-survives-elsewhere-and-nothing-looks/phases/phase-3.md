# 1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 28b90da · 198d580 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The verification the task requires, in its own words: *mutation-test every unit
you add, one at a time — break it, run the cases covering it, watch one go red,
restore from bytes you kept, clear `tests/__pycache__` between mutations.
Commit before you mutate and never restore from HEAD.* And contract §15: a new
case is not planted until it has been seen red.

This phase is not in `plan.md`'s original table. It is what the verification
turned up, and the plan could not have named it — see `overview.md`'s
divergence row.

## What this phase found

**A probe repository of two files found two defects the two real cases could
not.**

*The threshold measured this repository, not the defect.* The score was raw
`log2(F / df)` bits with a floor of 15, calibrated against a corpus of 633
files. In a two-file corpus the most any phrase can be worth is `log2(2)`, so a
survivor plainly sitting there scored 2 — and **every smaller repository
running the plugin would have been silently exempt from a check reporting
clean.** Dividing by `log2(F)` makes the unit *one phrase that occurs nowhere
else*, so the number means the same thing in a twenty-file tree and a
thousand-file one.

*The self-match guard compared a line number across two revisions.* It skipped
a candidate sharing the source's path and line — but the source is read at `a`
and the candidate at `b`, so equal line numbers are two revisions of one file
rather than one sentence. Where a claim was corrected in the first of two
copies inside one file, both landed at line 5 and the guard discarded the
survivor it exists to find. No guard is needed: `corrected` counts, so a
sentence is a source only where the file holds it fewer times after.

**Then twenty-four mutations, and seven survived the first sweep.**

| Survivor | What it was |
|---|---|
| `SHARED_FLOOR = 2` → `1` | **the constant could not change any answer.** One run is worth at most 1.0, so a floor of 1.6 already refuses every one-run candidate. Removed rather than pinned |
| the corpus scale dropped | unobservable *while* `SHARED_FLOOR` existed. Removing the redundant constant made the unit load-bearing, and the pin case now catches it |
| `records_a_past_round` → `False` | **the case was measuring the threshold.** Those two records score 1.51 against a floor of 1.6, so it passed with the exclusion switched off. It runs at 1.4 now |
| an exemption row with no quote | a zero-length run is contained in every text, so the row **exempted its whole file** — the *check nothing* value this design says it does not have. Refused, with a case |
| the quote matched on any word | a bag of words rather than a phrase. Cased, with the contiguous half beside it so the case cannot pass vacuously |
| `parse_range` ignoring the merge base | pinned at the unit. Three end-to-end fixtures were built and each was absorbed by a different part of the design — the case records all three |
| a candidate scored against its weakest source | **left unwatched and disclosed.** See below |

**The one that stays unpinned, and why.** Reporting a candidate against its
weakest source instead of its best changes nothing observable, because the
floor is applied per source-candidate pair *before* the tie-break. A candidate
reaches the tie-break twice only when two sources each clear the floor alone:
on `ad6f81a`, row R3 is reached by two sources scoring 1.79 and 0.46, and the
second never enters. What the mutation would change is which true source the
report names, not whether a survivor is reported. Building a fixture with two
independently-clearing sources for a presentation tie-break was not worth the
unit it would add.

**The second sweep, after the six repairs: every mutation caught.** The list,
the verdicts and the restore-from-kept-bytes protocol are in this phase's
commits.

**What the 3+ Fix Rule stopped.** The merge-base fixture was attempted three
times — a base whose additions read as removals but survive nowhere at `b`; a
sentence both sides wrote, which `wanted` subtracts as wording the range also
added; an identical copy, which shares one contiguous run and the floor
refuses. Three absorptions by three different parts of the design is the
architecture saying the difference is real in the input and not visible in the
output on a small probe. The case moved to the unit and says so.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `SHARED_FLOOR`, the constant requiring two shared runs | nowhere — the requirement is not lost, it moved into the unit. One run is worth at most 1.0, so `FLOOR > 1.0` enforces it, and `test_one_independent_run_can_never_clear_the_floor` is what holds the relationship |
| the self-match guard in `score` | nowhere — `corrected`'s counting already does what the guard was reaching for, and the comment in its place says so |
