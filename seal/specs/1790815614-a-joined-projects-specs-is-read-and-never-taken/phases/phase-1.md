# 1790815614-a-joined-projects-specs-is-read-and-never-taken — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 97590015 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

Build every phase of `plan.md` to the frame and say first whether the frame
holds. This phase: `hooks/root-migrate.py` moves a `specs/<id>/` only when it
carries `routing.md` or `rounds/` directly under it, the re-point follows what
moved, the symbolic-link refusal reads the same marks, the printed line names
an unmarked id-shaped directory with its reason, and the docstring says so.
Re-read and re-stamp the drifted `hooks/root-migrate.py#…` rows; open the
changelog and ledger fragments. B1, B2 seen red against the old hook; B3 a pin
shown red with `rounds` out of `MARKS`.

## What this phase found

**The frame holds.** Every coordinate `plan.md` §*Technical context* names
for phases 1–4 was opened before the first edit and stands where it says
(`root-migrate.py#old_items`, `#moves`, `#repoint_path`, `#main`;
`orchestration.md`'s *First, look for the 0.3.x layout* paragraph and the
case pinning it; `survivor_check.py#tracked`, `#records_a_past_state`,
`#WORK_ITEM_DIR`, `#corpus`, `#corrected`, `#hook`, `#OPTIN`;
`unverified_check.py#SKIP_DIRS`, `#overviews`, `#main`; `hooks/config.py#config_rows`).
Line numbers drifted by a few in places; no unit is missing or renamed.

One part of the frame does not hold as drawn, and the build went around it:

- **`repoint` cannot take the moved set as an argument.**
  `test_a_repoint_that_fails_after_the_moves_says_so_and_stamps_nothing`
  replaces `repoint` with a one-argument stand-in, so `repoint(root)` keeps its
  shape and computes the set itself (`moved_items`).
- **The moved set is read from `seal/specs/`, not from this run's `moves`.**
  A stopped run leaves some work items already under `seal/specs/` and their
  rows still citing `specs/`; the resume lists only what remains, so a set
  taken from this run's units would leave the first half's rows behind. What
  is under `seal/specs/` after the moves is both halves. `overview.md` records
  this as the one divergence of the phase.

Two units of the first draft had nothing that could break them, found while
writing the mutations rather than by a reviewer: `marked`'s `isdir` on the
directory (implied by either mark's own test) and `moved_items`' shape filter
(nothing outside the hook writes `seal/specs/` names it would refuse). Both
were removed before the mutation run, so every unit the phase adds has a case
that goes red without it — twelve mutations, twelve red, the list in the
ledger fragment's rows.

The joined project itself — a `specs/` holding only unmarked id-shaped
directories and no `.specseal/` — now has nothing old, so it falls into the
hook's existing *nothing to do* branch: silent, and stamped only where
`seal/` already exists. That is `questions.md`'s decided row about naming
what was left, and it needed no new branch.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The name test (`ITEM_RE` alone) as the proof that a `specs/<x>/` is a work item, in `old_items`, `repoint_path` and `main`'s link refusal | `hooks/root-migrate.py#marked` and `#moved_items`; the claim is row B1–B4 of `seal/ledger/1790815614-….md` |
