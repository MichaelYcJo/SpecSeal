# 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 15fcdcc3 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Show that the readers accept a drop (spec S5 to S7). Build a scratch
repository whose range removes a released item's process record, and show it
passes `chain_check.py`, `survivor_check.py --range` and
`unverified_check.py --baseline`, while the same range removing `routing.md`
as well fails `chain_check`. Pin that the arm's leave-list and
`records_a_past_state` agree on `rounds/`, `phases/` and `survivors.md`. Fix
here any reader that refuses. Answer Q4 by running the real-corpus test
modules after a drop in a scratch copy, and Q5 by comparing the survivor
sweep's exemptions with and without the shipped `survivors.md` files.

## What this phase found

**The frame did not hold in one place, and the place is a reader.** Spec
§*Grounding* says the survivor sweep "already names the class this work
removes … so a range that deletes those files reports nothing from them". That
holds for the three members `records_a_past_state` names. It does not hold for
the rest of D4's leave-list. Executed on a scratch clone of this repository at
`da95e035`: the arm, asked at e141980a, removed 525 files from 54 items, and
`survivor_check --range HEAD~1..HEAD` over that one commit exited 1 with 34
places. All 34 came from three removed files: 10 and 13 from the `handoff.md`
of 1790815613 and 1790913304, and 11 from the `broad-gate.md` of 1791019421.
None was a survivor of anything. `pr.ko.md` reported nothing.

The first real drop is a pull request into a release branch, where
`hygiene.yml` runs the sweep, so it would have gone red. A fold answers this
with no `survivors.md` row because the sweep leaves a retired directory out.
A drop keeps the directory, so it had no such way out.

**The fix, and why it is this shape.** `survivor_check.py` gained
`PULL_REQUEST_FILES` and `written_for_a_pull_request`, and `corrected` drops a
removed sentence whose file is on that list and gone at the range's tip,
after the pairing, beside the retired-directory filter. Two narrower and
wider options were weighed:

- Widening `records_a_past_state` to the whole list would also take a
  standing `handoff.md` out of the pool on every in-flight branch, which is
  a change to what the sweep reports today. The chosen filter leaves the pool
  alone, and a case pins that a standing `handoff.md` is still reported.
- Matching on the deletion alone, without the list, would excuse any file
  removed whole, which is how a real correction by deletion would go silent.

A line corrected inside a standing `handoff.md` is still measured, and a case
pins that too.

**The other two readers held, executed.** On the same scratch clone,
`chain_check --baseline HEAD~1` exited 0 and examined nothing, and
`unverified_check --baseline HEAD~1 seal/specs/` exited 0 with 54 overviews
read. The new module reproduces both in a scratch repository, with the
`routing.md` control red.

**Q4, executed: no test pins a removed file.** The 67 modules under `tests/`
that read `seal/specs` ran on the dropped clone: 4,178 passed, 2 skipped,
1 failed. The failure is
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`, and the
directory it names is this work item, which had no `overview.md` yet. The
closing memo is phase 3's.

**Q5, executed: no.** For each of the 50 non-merge commits in
`v0.15.4..e141980a`, the sweep ran over that commit's range twice: once with
only the `survivors.md` files of the items the commit touched, and once with
every `survivors.md` in its tree. The `exempt` count matched in all 50, so
removing a released `survivors.md` takes no exemption a later range used.

**Seen red, executed through `mutation-check`, all red.** The breaks:

- the new filter switched off: `test_the_drop_leaves_no_survivor`;
- its `not in after` half dropped:
  `test_a_sentence_corrected_inside_a_standing_handoff_is_still_measured`;
- the nested-path guard and the `pr.*.md` match: the agreement case's
  entries;
- `handoff.md` taken off `PULL_REQUEST_FILES`: its agreement entry;
- `overview.md` added to the arm's list:
  `test_the_unverified_record_reads_the_same_after_the_drop` and the
  agreement case;
- `routing.md` added to the arm's list: the fixture refuses, and the
  agreement case fails.

The agreement case covers the whole list, not the three members plan.md
named, because the sweep now holds the rest of it too.

**Every probe is gone.** The scratch clone, the Q5 copies and the probe
scripts were all under the session's scratch directory and were deleted
before the hand-back.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
