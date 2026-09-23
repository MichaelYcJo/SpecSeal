# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 8472cd45 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Not a phase of the frame. The spawn prompt added #366 from work item B's
frame: the release-sizing sweep's reach is unpinned, its three widenings
revert with the module green, and two test-only cases pinning `STATES_A_SIZE`
and `SCANNED` were drafted and refused at depth 2 in the work item that found
the gap. Decide from the tree whether it fits as a small sixth phase here or
is deferred with grounds, without widening it into mechanism beyond the
ticket.

## What this phase found

**It fits, as cases and nothing else.** The three widenings — the noun-form
alternatives of `STATES_A_SIZE`, `hits()`'s joined-line branch, `CLAUDE.md`
in `SCANNED` — are shipped code here, not units a fix pass of this run
added, so a case pinning any of them is depth 1 in this work item; the depth
rule that refused them in `1789172128-…` was about that work item's own fix
pass, and the ticket's own analysis says so. The two drafted cases were
recovered from the retired work item's round 2 report at `9816d3de` (the
directory itself was settled away in #504), and the third — the one the
ticket calls correctly never written there — was in the same report, so all
three are planted: `test_the_pattern_catches_the_noun_forms_and_not_only_the_verb`,
`test_the_sweep_reads_a_statement_whose_wrap_falls_inside_it`,
`test_the_scanned_set_reaches_the_file_a_rule_gets_restated_in`. The one
edit beyond the drafts: `tracked()` returns `(files, missing)` now, so the
scanned-set case reads the first half.

**Seen red by reverting each widening, one at a time** (executed, from kept
bytes; the cases are green at HEAD by construction, because what they pin
already stands): the three noun alternatives dropped — the noun-forms case
red alone; `hits()` reverted to a plain line scan — the wrap case red alone;
`CLAUDE.md` dropped from `SCANNED` — the scanned-set case red alone. 11
passed with all three in place.

**The open question is deferred, with grounds.** #366's second half asks
what `round_record.py#depth_two` should do when one finding's `Location`
spans units of two depths. That is a change to a gate — a case seen red for
a two-depth Location, a failure direction, a prompt budget — and the ticket
itself says the cheaper answer may be a reviewing convention: a reviewer
splits a finding whose coordinates sit at two depths, so each verdict
carries one depth. Neither is this work item's: the standard phase 5 writes
is about the shape `new` accepts, and adding a splitting rule there would
widen it into a rule the ticket has not decided. `overview.md` §Not done
carries it, and the hand-back names #366 as still open on that half.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the comment in `tests/test_a_release_is_sized_by_a_criterion.py` saying the sweep's reach is not pinned and #366 holds the drafted cases | the same place, rewritten to say the three cases below pin it and why they could land here |
