# 1788912166-red-for-following-the-documents-green-for-ignoring-one — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <filled at the phase's commit> |
| Ran by | unknown — the spawn prompt named no runner, and the value is the spawning session's rather than a value this segment decides about itself |

## What this phase was asked

#297 — `survivors.md` takes a whole-range row with grounds, and
`survivor_check` honours it. Verified by cases built from #293's own range
shape: declared passes, undeclared fails.

## What a change to a gate must carry

- **A test seen red.** Eight cases run against the unfixed script: six failed,
  and the two that passed are the ones that had to. `test_an_undeclared_
  deletion_still_fails` is the floor the whole escape sits on — if it ever
  passes, none of the others measure anything — and
  `test_a_range_row_with_no_grounds_is_not_a_declaration` expects exit 2, which
  the old parser produced for the right reason: a two-cell row was not a row,
  so the file held none. The parser-level case failed with
  `ValueError: too many values to unpack`, because `read_exemptions` returned
  one list where it now returns two. Then **six mutations of this script, all
  killed**.
- **A stated failure direction.** The gate **allows more**: a declared range
  keeps its survivors. That direction is chosen because the alternative is not
  a stricter check, it is no check — 153 rows is not an escape anybody takes,
  and the branch turns the step off instead. What bounds the allowance is that
  the declaration is a written sentence in the tree with a reviewer reading it,
  and that the **range is the anchor**: run the check over a different range
  and the row does not hold, so a declaration cannot outlive the deletion it
  was written for.
- **A prompt budget: zero.** No interactive path, no hook, no question. The
  workflow already loops every `seal/specs/*/survivors.md` into `--exempt`, so
  #297 needed no change to `hygiene.yml` at all.
- **Platform honesty.** No process inspection. `git rev-parse` and
  `git merge-base` through the existing `resolves` and `parse_range`, which
  every run already calls for `--range`.

## What this phase found

**The two row shapes can share one file, and the first cell is enough to tell
them apart.** A path cannot match `^[^\s|]+\.\.\.?[^\s|]+$` — the dots need a
non-space word on both sides, so `../notes.md` is a path and `A..B` is a
range. That is why no new file, no new flag and no header convention was
needed: a two-cell range row can sit inside the same
`| Path | Quote | Grounds |` table, which is how it will actually be written.
The old parser skipped two-cell rows in silence, so nothing that used to be
read changes meaning.

**Resolved, not string-matched, and that is not a nicety.** In CI the range is
`origin/<base>...HEAD` and that is the spelling a session copies into the
declaration; a person running it by hand types two oids. Those are the same
range, and comparing the text would refuse one of them.
`test_a_whole_range_row_is_resolved_rather_than_string_matched` declares
`HEAD^..HEAD` and runs with two oids.

**An unresolvable declaration must not be exit 2, and the reason is a
landmine.** A `survivors.md` lives in the tree from the work item's first row
until the release that ships it, and the refs its range names — a release
branch — get deleted. Refusing the run then would turn every later range's
check into exit 2 over a row that has nothing to do with it. So it silences
nothing and prints under `unresolved`, which is the loud direction. This was
not in the plan and it is the one design decision this phase settled on its
own.

**The excused survivors are still printed, all 153 of them.** That looked like
a candidate for summarising and it is not: the existing rule is that a row
which silences something invisibly is a row nobody audits, and what #297
removes is the cost of WRITING 153 rows, never the cost of reading 153 lines.
The mutation that stops printing them turns
`test_a_whole_range_row_excuses_the_survivors_of_that_range` red on its
`notes.md` assertion.

**One message changed and an existing case pinned the old text.** The
emptiness refusal named only `| Path | Quote | Grounds |`; after this phase
that sentence would send somebody to write the shape they had not chosen. It
names both, and `test_an_exemption_file_with_no_rows_is_refused` was updated
to pin the new text in the same commit — §14, and the case is the reason the
next edit cannot quietly take it back.

**A ledger anchor drifts and it is phase 4's to settle.** Row S5 cites
`survivor_check.py#read_exemptions@cd6ee247`, and this phase changed that
function's body and signature. The claim S5 makes — an exemption is anchored
on a contiguous run of the standing text's own words, and neither an empty
quote nor a scattered one silences anything — still holds: this phase adds a
second row shape beside the quote anchor rather than changing it. So it is a
re-read and `evidence-check --reverify`, not a removal.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the emptiness refusal's sentence naming only `\| Path \| Quote \| Grounds \|` | the same sentence, which now names both row shapes; `test_an_exemption_file_with_no_rows_is_refused` pins the new text |
| `read_exemptions`' single-list return | its two-element return, whose only caller is `main`; the new `whole_range` consumes the second element |
