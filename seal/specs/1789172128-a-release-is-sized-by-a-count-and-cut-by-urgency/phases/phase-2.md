# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `5b4875f` |
| Ran by | unknown — the spawn prompt named no model, and the template gives this row to the spawning session rather than to the segment. The orchestrating session fills it |

## What this phase was asked

Rewrite the sizing paragraph in place at `docs/issues-and-milestones.md:24-30`,
inside §*A milestone answers* when*, and takes three shapes*. Four things
change in it:

- the criterion replaces the count as what decides a release's size — *what has
  to be in effect before the next work item starts*;
- the count is named a **ceiling**, in `docs/review-chain-spec.md:53`'s
  wording;
- the two releases that demonstrate it are cited in Q1's form — prose, no
  version numbers;
- the paragraph says what does **not** change: the milestone as a pool,
  `backlog:` as the unscheduled pool, and nothing automated reading either for
  scheduling.

`0.8.3` stays as history. The release-hygiene case and the wrap case run on
this phase's own edit, before phase 3 adds to the same file.

## What this phase found

**The `## Done when` row *nothing automated reads either* cannot be written as
it is worded, because §*One thing reads a milestone, and it can stop a release*
says the opposite forty lines down.** #359 made
`.github/scripts/release_completeness_check.py` read the milestone
`release: X.Y.Z` and refuse the release pull request over it, and that section
opens by saying in so many words that *this section said nothing automated
reads a milestone until #359* and that it is not true any more. A paragraph
restating the old claim would have put two answers in one document — the defect
the frame's S6 names for the label section, one section over and unnoticed.

So the clause is written as the narrower thing that is still true: nothing
**schedules** from either, and the one thing that reads a milestone checks a
cut release against its pool and never decides what goes into one. That keeps
the row's substance — a person cannot expect the tracker to size a release for
them — and it does not contradict the document's own later section.
`plan.md` and `spec.md` both carry the row in the wider wording, so this is a
divergence and it is in the closing memo as one.

**`backlog:` is not redefined, because the paragraph under the edit already
defines it.** Line 38 reads *`backlog:` is the unscheduled pool, and an issue
leaves it in one act*, so restating that as a second definition would be a
second carrier of the same sentence. The what-does-not-change clause names
`backlog:` and points down at it instead.

**The two citations are prose and the paragraph says why.** A separate
paragraph states that both releases sit at or above the running version, names
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` as what
refuses them, and points at `CHANGELOG.md` as the one grep that turns either
description back into a number. `plan.md`'s alternatives table asks for exactly
this: without the note, a later author for whom both numbers have become
history would replace the descriptions with numbers and be right to. It also
records that one of the two has already shipped and that #363 is where the
refusal's off-by-one is repaired — phase 1's measurement, written where the
next reader of the paragraph is standing.

**What was executed on this phase's own edit**, exit codes read directly and
not through a pipe:

| Ran | Exit | Reading |
|---|---|---|
| `bin/test -q tests/test_docs_line_wrap.py tests/test_release_hygiene.py` | 0 | 55 passed — S8 and S9 |
| `git grep -n "in effect before the next work item" -- docs skills agents templates tests` | 0 | one line, `docs/issues-and-milestones.md:24` — S1 |
| `git grep -n "ceiling, not a target" -- docs` | 0 | two lines, this file at 32 and `docs/review-chain-spec.md:53` — S2 |
| `git grep -n "is the size" -- <the loaded set>` | 1 | the replaced wording survives nowhere — S3's absence half |
| `bin/test -q` over the eight modules that read this document | 0 | 235 passed |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *A release is sized in work items rather than in ticket numbers, and three or four is the size* — the sentence, from the only place in the loaded tree that stated it | the rewritten paragraph, which keeps the work-items half as the ceiling's unit and drops the target reading. The ledger row that cites the old wording is S3 in `seal/ledger/1789100139-…md`, handled in phase 4 under Q8 |
