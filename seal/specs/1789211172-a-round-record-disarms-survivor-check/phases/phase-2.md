# 1789211172-a-round-record-disarms-survivor-check — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `ac8e33a` |
| Ran by | `specseal:smith` on `claude-opus-5` — filled by the orchestrating session, which chose the spawn-time argument, from the segment's own transcript |

## What this phase was asked

`records_a_past_round` applied to `corrected`'s `paths`; the module docstring
section at `:63-79` rewritten to name the pool **and** the range; a case
pinning that sentence. Phase 1's two cases green, and
`test_a_record_of_a_past_round_is_not_a_survivor` still green — the pool side
must not move.

## What this phase found

**The fix is the list comprehension the plan named, and the argument for it
had to be written twice, at two altitudes.** The module docstring says which
sides the exclusion holds on, because that is the sentence a reader checks the
design against. `corrected`'s own docstring says why the range refuses a
record and why the filter sits on `paths` rather than on the added side,
because that is what the next author editing this function meets. Neither
paragraph is the other's summary: the first one was already there, stated the
intent, and named no function — which is precisely how the defect survived
five releases without the module's own account of itself being wrong.

**The docstring case pins the sentence by what it must SAY, not by its text.**
It reads the section up to the next heading, isolates the paragraph the
exclusion opens with, and asserts `pool`, `range` and `both sides` are all in
it. A rewrite that keeps the claim passes; a rewrite that drops a side does
not. The last assertion is the only literal one, and it is negative: the
pre-#365 sentence `Everything under a work item's `rounds/` is out.` may not
come back.

**Seen red two ways, each restored from bytes kept in the mutating script
rather than from `HEAD`** — the phase's own edits were uncommitted, so a
`git checkout --` restore would have taken them with it:

| Mutation | Exit | What it said |
|---|---|---|
| the paragraph deleted | 1 | `**A record of a past round.** is no longer the first exclusion stated` |
| the pre-#365 one-sided sentence back | 1 | `the paragraph does not say the exclusion applies to the pool` |

The module compared byte-identical to the original after both.

### The real-range measurement

`bin/survivor-check --range 7e17f5e..941dab5`, run before and after the edit
while those refs resolve. Both numbers the plan said must not move did not
move, and the survivor came back at the score round 2 of #361 recorded.

| | Files examined | Sentences the range removed | Exit | Reported |
|---|---|---|---|---|
| before | 894 | 16 | 0 | `no removed wording is still standing` |
| after | 894 | 16 | **1** | `seal/specs/1789100139-…/changelog.md:22` at **2.00** |

The two counts are the load-bearing half. `corrected` returns the removed
sentences from the same list the filter now narrows, so a filter that reached
too far would show up here as a smaller number — and a round record that the
range only ADDS removes nothing, so 16 is the number that proves the filter
took nothing it was not meant to. The survivor and its score match
`seal/specs/1789172128-…/rounds/round-2-report.md:160-163` exactly, which is
the reviewer's independent measurement of the same range.

This is an **executed** measurement on refs that live only while the local
branch `docs/361-a-release-is-sized-by-a-count-and-cut-by-urgency` does.
Nothing in the tree depends on it; it is recorded here and in `overview.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The docstring sentence *Everything under a work item's `rounds/` is out.* — it stated the exclusion without naming either function it had to hold in | Replaced in place by a sentence naming the pool and the range, and pinned by `test_the_docstring_names_both_sides_of_the_round_record_exclusion`. The account of why it was wrong is the new paragraph beside it and this record |
