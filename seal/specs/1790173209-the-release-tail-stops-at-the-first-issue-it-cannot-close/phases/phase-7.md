# 1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close — phase 7

<!-- seal/specs/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close/phases/phase-7.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 5d8a182e |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#157. `skills/update/SKILL.md` gains a step 2b that reads
`installed_plugins.json`'s `installPath`, compares the installed
`CHANGELOG.md`'s top heading to the version the installer reported, stops
before the summary on a mismatch, and prints the repair with the `.in_use/`
and `installPath` cautions; changelog fragment; `seal/ledger.md`'s row on
the skill's *Procedure* heading re-read and `--reverify`. Verified by S15, a
case pinning the step, seen red at `HEAD`.

## What this phase found

**Step 3 keeps reading the clone.** The ticket's finding is that the clone
was the right file in the wrong place: it is correct, and the installed
copy is what was stale. Step 2b is what makes step 3's summary true of the
copy that will load; moving the summary's source to the installed copy
would summarise a stale copy accurately, which is the wrong repair.

**The case had to pin the word, not the path.** The first spelling asserted
`.in_use` in the step, and a mutation deleting the PID caution while keeping
the repair stayed green, because the repair's `mkdir -p "$p/.in_use"` still
carried the path. The case asserts `PID` now; removing the whole cautions
paragraph turns it red (`1 failed`).

**Red at `0cf5fb5f`, quoted:**

```
E       AssertionError: no step reads the installed copy between 2 and 3
1 failed, 44 deselected in 0.08s
```

Green at `5d8a182e`: `99 passed` over `tests/test_release_hygiene.py
tests/test_first_setup_asks_once.py tests/test_no_real_identifiers.py`, and
`74 passed` after the fragments over the hygiene, identifier and gather
modules.

**Mutations**: the stop turned into a note (red), the repair block dropped
(red), the cautions paragraph dropped (red, once the case was strengthened
as above).

**The shared ledger.** One row — the one on the skill's *Procedure* heading
— drifted; its three-part claim (both moves with their evidence labels, the
run that would settle the open row, that it types neither) is untouched and
the row carries a `Re-read 2026-09-24` note. `evidence-check --strict` exits
0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
