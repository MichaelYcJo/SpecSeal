# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — phase 3

<!-- seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8591f1f9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md`'s phase 3, #667 round 3's ⬜ 4: `test_a_break_commonmark_does_not_honour_quotes_no_rider`
gets back its old region half over `text` (`region_lines` keeps no `RIDER:`
line), directly after the `riders_in` assertion and before `region = (`, and
its docstring says the case asks the hasher twice. Seen red under a
`region_lines` mutant that walks the reader's split, all eight breaks, and
green at HEAD. Ledger: R1-1's anchor on this case re-read. This phase touches
only the rider case, because work item G (#664, PR #675) is under review in
the same module's neighbourhood; whichever lands second resolves hunk by hunk.

## What this phase found

- **The restored half is the old one, byte for byte.** Read from
  `8b1492aa^` (`git show`): `region_lines(CHECKER, "doc.md", '"# doc"', text)`
  and `not any("RIDER:" in line for line in kept)`, with the
  `kept is not None` guard. It sits where the plan put it.
- **Each half catches a hasher the other passes.** Executed with two
  mutants of `.github/scripts/rider_check.py#region_lines`, one at a time,
  restored from kept bytes (`<scratchpad>/1790659274/m_rider.py`):
  `lines = text.splitlines()` fails the restored half (the assertion on
  `RIDER:`) for all eight breaks; handing `comment_blocks` the text, the
  merge's own defect, fails the merge's half (the assertion on `real`) for
  all eight while the restored half passes. At HEAD the case passes and the
  rider module exits 0. Whether the merge's half also passes under the first
  mutant was not re-run here, because the restored half stops the case first;
  the round 3 reviewer executed it and it did.
- **No overlap with #664 in this file.** The edit is inside one case's
  docstring and body; `riders_in`, `inferred_anchor` and the reader's
  mid-line marker (round 3's 🟡 3) are untouched, so G's changes to
  `rider_check.py` and this case do not meet in a hunk.
- `python3 .github/scripts/rider_check.py --root .` over this tree: exit 0,
  19 ok, 0 drifted, 0 broken (a probe, not a seal).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
