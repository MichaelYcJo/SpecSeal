# 1790297086-the-broad-gate-says-what-ci-says — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <the phase's closing commit, as `plan.md`'s Status cell for phase 3 names it> |
| Ran by | unknown — the spawn prompt did not name the agent and model, and this segment does not source that value from its own idea of itself |

## What this phase was asked

#473. Phase 3 had these parts:

- A constant beside `PARTITION`.
- The guard in `gate`, with both conditions: the base names `main`, and the
  gated repository's `release` job carries the arm's step.
- The stderr line, its text pinned.
- `skills/verify/SKILL.md` §*What the count does not say* rewritten so it no
  longer calls the instance live.
- Cases C1 with its non-`main` red twin, C2, and C3 through phase 2's
  `workflow_step`.
- The ledger rows on `#gate` and `#PARTITION` re-read, and the new claim in
  the fragment. The changelog fragment extended.

C1 is shown red at the frame commit, and C3 red with one arm removed from the
constant.

## What this phase found

- **`PARTITION` itself did not move, and `gate` drifted in four release
  files.** The rows on `#gate` in `0.10.0.md` (S7, S12), `0.12.0.md` and
  `0.12.2.md` (R2, G3) were re-read against the guard, and all still hold.
  R2's claim that `args.base` is read once still holds, because the guard
  reads `base.given` and not `args.base`.
- **A note in `0.12.2.md` G4 turned false without its anchor moving.** Its
  note named #473 as the home of "the gate skips neither when the base is
  `main`". The case it anchors on did not change, so `evidence-check`
  reported nothing. `git grep '#473'` found it, and it was corrected in place
  with a dated note.
- **Where the line prints.** It prints after the coverage line and before
  the first check. Both arms are skipped by not building their `checks`
  entry, so `failures` and `panel` needed no change: neither ever read
  those two keys. A3's AST reader still finds both `checks[...] = run(...)`
  assignments inside their `if` blocks, and it is green.
- **C2's end-to-end red needed its own mutation.** Taking out only the
  "carries the step" half turns the unit table red but not C2: with no
  workflow the early return already gives no arms. Skipping at `main`
  whatever the workflow says is the mutation that turns C2 itself red.
- **The frame's gate, run on C1's fixture against `main`,** said NOT SEALED
  with exit 1. That is the red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence in `skills/verify/SKILL.md` calling #473's instance live | the same section, rewritten to say it is closed and how, with the class kept named |
