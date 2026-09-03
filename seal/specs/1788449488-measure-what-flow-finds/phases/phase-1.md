# 1788449488-measure-what-flow-finds — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 80f26ce |

## What this phase was asked

Build phase 1 only, of the 3-phase table in `plan.md`: give
`skills/verify/SKILL.md` a new section between `## Seal block` and
`## Counterfeits (stop on sight)` — after every smith or warden segment,
measure its transcript with `skills/verify/scripts/session_cost.py`; find
the destination with `gh issue list --label flow-measurement --state open`
(exactly one expected — the mechanism's invariant); post with `gh issue
comment <n> --body-file`; do it as part of the segment, before the next one
spawns or at the latest with the round/phase record; never ask. State
explicitly that where no such issue is open, this is a no-op, not a
failure. Carry over the subagent-transcript-path shape and the "split a
resumed segment at the coordinator's message" rule from
`~/.claude/projects/-Users-yc-Documents-GitHub-SpecSeal/memory/measure-every-segment-to-89.md`.

In THIS repository specifically (a one-time bootstrap): create the
`flow-measurement` label and apply it to #89, verified by re-running
`gh issue list --label flow-measurement --state open --json number,title`
and confirming it returns exactly #89.

Write a new test module (name chosen by this phase, following
`tests/test_a_phase_hands_the_next_one_a_record.py`'s pin-test shape but
closer to `tests/test_review_axes.py`'s plain-substring style since the
source is skill prose, not a template) asserting: the section exists, it
names both commands, and it states the no-op case explicitly. Every new
case shown red first.

Phase 2 (the release-time rollover script) and phase 3 (`docs/flow.md`
cleanup and closing SDD artifacts) were explicitly out of scope — stop once
phase 1's own scope is committed and its narrow verification is green.

One extra step beyond the plan's own Phase 1 row, matching how
`1788445862-a-phase-hands-the-next-one-a-record`'s own phase 1 used the
mechanism on itself: write this file with `templates/sdd-phase.md`, and fill
`plan.md`'s Phase 1 Status cell with the commit that closed this phase.

## What this phase found

**The label lookup's own eventual-consistency gap.** Right after `gh label
create` and `gh issue edit 89 --add-label flow-measurement`, the very next
`gh issue list --label flow-measurement --state open` returned `[]` — empty
— even though `gh issue view 89 --json labels,state` in the same breath
showed the label applied and the issue open. A second `gh issue list` call,
seconds later, returned `#89` correctly. This is GitHub's search index
lagging the label write, not a bug in either command. `spec.md`'s acceptance
table already treats "exactly one open" as the mechanism's invariant to
enforce, not as a check that must be instantaneous after a label write — so
this needed no design change, only a retry before trusting the first empty
result as ground truth. Worth a phase 2 note: the rollover script's own
"count is not exactly 1 → fail loudly" path should not fire on a
just-written label in the same breath as a release; in practice the script
runs against an issue opened by the *previous* release, not one just
labelled, so this gap is unlikely to reach it — flagged here rather than
acted on, since phase 2 is out of this phase's scope.

**Line-wrap sensitivity in the pin test.** The first draft of the new test
module asserted exact substrings against the raw (unwrapped) markdown text,
and two assertions failed against the actual section even though the
section said exactly what was required — because the prose's own 80-column
hard-wrap happened to split `gh issue list --label flow-measurement --state
open` and `nothing fails` across a line break. Fixed two ways: rewording the
skill section so the `gh issue list …` command sits on one line (a command
meant to be copied should not wrap anyway), and changing the test's
`section_body()` helper to collapse whitespace (`" ".join(text.split())`)
before matching, so future re-wrapping of the prose does not re-break a pin
that is really about the wording, not the column it happens to land on.

**Mutation testing found no gaps.** Each of the 6 substantive assertions was
mutated out of the section text individually (the exact phrase it checks
for), and each corresponding test went red on that specific mutation, then
was restored from the original string held in memory (not from `git
checkout`, which would have discarded the working-tree state at the time) —
byte-identical restore confirmed by comparing the file's content before and
after the run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
