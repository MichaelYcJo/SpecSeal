# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — phase 4

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | eabeb69e |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 4, the routing reader on the walk: `table_rows` skips
the lines the walk hides and reads every other line as today. Its docstring and
`parse`'s state the reading, and that R2 and R9 read as no declaration. R1 to
R9, each marked red failing against `3911a8cf`'s `hooks/routing.py`; the
property case for this reader; R10's measurement over the committed files and
the template.

## What this phase found

- **`hooks/routing.py#shown` is the one new unit**, `table_rows` walks it,
  and it is `blocks.walk(lines).hidden()` with an empty base, because this
  reader's base reading hid nothing. Every other line is read exactly as it
  was: the strip, the two-cell rule and `parse`'s last-row-wins are untouched.
  `hooks/routing.py` imports the walk inside the same `ImportError` sentence
  `hooks/config.py` has, and the copied-alone case gained it with `optin.py`
  beside it.
- **Seen red against `3911a8cf`** with that commit's `hooks/routing.py` in
  place: R1, R2, R5, R6, R6b, R7, R8 and R9 failed, which is every row the
  frame marks red plus the second R6 text this build added (no blank line
  between the note and the fence, where the fence line interrupts the note's
  paragraph); R3 and R4, which the frame marks *pins*, passed, and so did the
  template case.
- **R3 reverses `1790635413`'s pinned `routing.parse("```\n" +
  two_axis_text()) is None`**, as the frame decided (D4): a fence nobody
  closed is not a block, and the declaration under it reads. The mutation that
  hides uncertain lines with the fence-only reading turned R3 and the
  property's half 1 red, which is that decision seen from the other side.
- **Mutation:** `shown` hiding nothing (9 red), hiding uncertain lines too
  (2), `table_rows` not reading `shown` (8), the import sentence removed (1).
- **R10, measured (Q3's routing third, answered (a)).** Every committed
  `routing.md`, 27 of them since #660's merge added one, and
  `templates/sdd-routing.md`: 28 files, 28 parse at `3911a8cf`, and `parse`
  and `table_rows` give the same value for every one at HEAD.
- **A phase 1 defect surfaced here.** Running the modules that name
  `routing` included `tests/test_release_hygiene.py`, which refuses a loaded
  file naming a version above the running one: `CONTRIBUTING.md`'s fallback
  names `4.2.0`. It is markdown-it-py's, so it went into
  `VERSIONS_OF_ANOTHER_PRODUCT` with that argument, the shape the git and
  bash builds already have there.
- **Gate lines, drafted for `CONTRIBUTING.md` §*What a change to a gate must
  carry*.** Seen red: above. Failure direction: the commit gate asks where the
  only table was fenced or commented out (R2, R9), and is silent everywhere it
  was silent; a row it stops reading could only have overridden the live
  table, which is the silent direction #658 was opened about. CI's
  `chain_check.py` reads the same function, so the pull request agrees with
  the commit. Prompt budget: the one ask is the one every undeclared commit
  already gets, and no committed declaration reaches it. Platform: string
  processing only; macOS only here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
