# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | recorded in `plan.md`'s Status cell for phase 6 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The records. Correct G6 and G7 in place, and G1 and A5 as phase 5's record
named them. Write the fragment `seal/ledger/<this item>.md` in one pass.
Write `changelog.md` with one entry per ticket this item closes (#526, #488,
#509, #466, #474, #55, #316, #556, #561, #562), #268 confirmed, #222 credited
to #559 and #331 deferred. Write `overview.md`, and run the branch's sweep
with this item's `survivors.md` if anything stands.

## What this phase found

**The four corrections** (executed). Each carries a `Corrected 2026-09-24`
note naming this work item and its ticket, and `--reverify` stamped the new
anchors.

- **G6** of `1789985781` names its three cases in `Code grounds`: the two
  populations and the joined sentence.
- **G7** names the not-UTF-8 case.
- **G1**'s Notes no longer call #423's finding 4 *half a pin*. They say it was
  a narrow reader naming both directions.
- **A5**'s Clause names the same-run replace.

`correction-check --range origin/release/v0.15.1...HEAD` exit 0 over the one
merge in range.

**The fragment** (executed): 12 rows. S1–S3 are the split, E1–E2 are #488 and
#509, N1–N4 the sentences, P1 is #466, and C1–C2 are #561 and #562. Each is
written with a placeholder hash and stamped by `--reverify` (34 rows, then 0).
`evidence-check --strict .` exit 0. **The records arm refused one stamp at
first**: `spec.md`'s #222 row wrote `round_record.py#depth_two@8c7bfa47`, a
short path. Once the work item had a fragment, the arm read the spec as a
record, found the short path, and found no such file. The sentence names the
unit in words now, the way `1790206437`'s overview records the same finding.

**The changelog** takes an entry per closed ticket, the #268, #222 and #331
lines, and the #556 entry phase 4 wrote.

**The sweep** (executed, `bin/survivor-check --range
origin/release/v0.15.1...HEAD`). At `4b25160c` it was exit 1 on two places:

- `CLAUDE.md:138`, the orchestrator's paste to make.
- `skills/evidence-check/SKILL.md` §*`correction-check`*, a fourth carrier of
  #488's exception the frame did not list. It is corrected to *removes, edits
  or falsifies … keeps that claim true in the file the row is in*.

That correction put `correction_check.py`'s module docstring in the report at
`8a5591b0`. Its sentence narrates #424, where the row stood in the shared
file, and stays true of that incident. With both places exempted in
`survivors.md` with quotes and grounds, the sweep is exit 0: *every survivor
is excused by a row above (2)*.

**What `CLAUDE.md` needs**: phase 3's two replacements, unchanged
(`phases/phase-3.md`). The `CLAUDE.md` row of `survivors.md` stops holding
once they land, which is the intended end of it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| G1's *Half a pin is #423's finding 4* | the same cell, as a narrow reader naming both directions, with a `Corrected` note |
| `spec.md`'s short-path `depth_two` stamp | the same sentence, naming the unit in words |
