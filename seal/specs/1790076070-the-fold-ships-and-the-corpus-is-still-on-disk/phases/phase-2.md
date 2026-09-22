# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 5e56c675 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Every floor repair, before anything is removed: F1–F5 derived from an
independent listing, F3 and F6–F8 re-pointed at fixtures, F9–F10 onto the
fold record. Each repaired module green **before** the fold; each new arm
seen red with the arm removed (agent-contract §15); `uvx ruff check` on the
touched files. **No floor literal is lowered** — `skills/settle/SKILL.md` §3
names that as the answer that turns a check into a comment.

## What this phase found

### The repairs, one line each

| # | Was | Is |
|---|---|---|
| F1, F2 | `assert len(records) > 200` | `_the_walk_found_every_committed_record` — the disk walk covers every record `git ls-tree HEAD` carries and the tree still has |
| F3 | `assert carrying` in the real-corpus sweep | the two-way split moved to `test_a_record_carrying_the_row_is_read_and_one_without_it_prints`, which plants both kinds |
| F4 | `assert len(paths) > 100` | `_the_corpus_covers_every_work_item_that_has_rounds` — every work item whose `rounds/` holds a record contributed one |
| F5 | `assert parsed > 100` | every listed record either parsed or is named, and something parsed |
| F6 | `assert teeth` | **untouched** — declined |
| F7, F8 | two `assert glob(...)` for a live specimen | `test_the_stray_sweep_sees_a_todo_file_one_level_down`, planting both layouts |
| F9, F10 | the cutoff's directory is in the tree | `conftest.cutoff_item_is_traceable` — the directory is there **or** `docs/` records the fold |
| F11–F16 | — | **untouched** — declined |

### Independence is what replaced the literals, and it is measurable

A floor asks *did the sweep read anything* with a number that the fold makes
false. Each replacement asks the same question of the tree through a second
route, so it holds at any corpus size:

- **F1/F2** compare a disk walk against `git ls-tree HEAD`. Neither can go
  quiet without the other noticing. `on_disk` runs first, because a record
  git carries and the tree has deleted is the ordinary state at step 3 of
  `docs/release-checklist.md` and would otherwise read as a record the walk
  missed. The walk is allowed to hold **more** than the listing — an
  uncommitted record mid-round is on disk and not at HEAD — so the assertion
  is coverage rather than equality.
- **F4** derives the expected work items from `os.listdir`, which git never
  sees, and compares against a corpus git produced. Measured both ways: 82
  work items with a record, 82 covered, before; 2 and 2, after.

Both are **stronger** than the floors they replace, not weaker. `> 200` was
green over a listing that lost a whole work item; neither of these is.

### F6 is declined, and the measurement is what decided it

`questions.md` Q3 named a measurement as its instrument and expected the
fixture. Over the 7 surviving records `FINDING_ID_RE` refuses a cell in
**four** of them — `1788395377`'s rounds 1 to 4, carrying `🟢 0b`,
`r1 🔴 1`, `r2 1`, `r3 1b` among others. The floor is right and the
population survives, so the sanctioned answer is **decline** and nothing was
written. Phase 1 recorded the measurement; this phase acted on it by not
acting.

### F3 had no survivor, which decided its repair rather than confirming it

All 34 records carrying `| Fix range |` are in the retire set, because the
row is younger than every kept work item. So the `assert carrying` half could
not be kept over the real corpus by any reading, and the question was only
where it goes. The new case plants a carrier and a grandfathered record in
one scratch repository and asserts the split over both — which is what
`assert carrying` was protecting and never itself pinned.

The item with no row is begun a second **before** the cutoff on purpose. A
record that owes the row and lacks it is *failed*, not printed; the
grandfathered state is the one the split needs.

### The suite has a rule about new listing scopes, and the repairs answer to it

`tests/test_a_shrunken_corpus_declines_to_judge.py#test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard`
classifies every scope in `tests/` that derives a path list from git into one
of six tables, and an unclassified scope turns it red. The repairs add **no
new git-listing scope**: F1/F2 call the module's existing `_real_records`
(already classified `CONTENT_FROM_GIT`) and F4 calls `committed_records`
(already `APPLIES_THE_SHARED_GUARD`). That module is green, run whole.

Worth saying because it is the trap: writing `git ls-tree` into the new
helper would have been the natural shape and would have turned a suite-wide
check red for a reason unrelated to the fold.

### One check is red before the fold and it is not a floor

`test_every_spec_directory_that_reached_the_ladder_has_an_overview` went red
at `5cde6dc5`, when the frame created a directory with a `spec.md` and no
`overview.md`. Phase 1's `overview.md` closes it. Observed both ways: exit 1
with the file moved aside, exit 0 with it restored byte-identical.

## Evidence of the arms

Twelve observations, in a `test_tmp_every_new_arm_is_red.py` probe run once
and deleted (agent-contract §7):

| Arm | Violated by | Seen |
|---|---|---|
| `assert listed` (F1/F2) | `_real_records` returning nothing | "green over an empty corpus" |
| `assert not unwalked` (F1/F2) | one record dropped from the walk | the dropped path named |
| `assert with_rounds` (F4) | — covered by the empty-listing case | |
| `assert not missed` (F4) | one work item's records removed from the corpus | the work item named |
| `assert parsed` (F5) | `id_cells` refusing every record | "parsed as a verdict table" |
| `assert len(carrying) == 1` (F3) | a repository with no carrier planted | the carrier list empty |
| the stray equality (F7/F8) | both files planted at the top level | the deep glob empty |
| the at-level equality (F7/F8) | both files planted one level down | the shallow glob empty |
| `cutoff_item_is_traceable` false | no directory and no marker | "cannot show" |
| its directory arm | a directory and no marker | accepted |
| its marker arm | a marker and no directory | accepted |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `assert len(records) > 200` at two sweeps | `_the_walk_found_every_committed_record`, same module |
| `assert carrying` in the real-corpus fix-range sweep | `test_a_record_carrying_the_row_is_read_and_one_without_it_prints`, same module |
| `assert len(paths) > 100` and `assert parsed > 100` | `_the_corpus_covers_every_work_item_that_has_rounds` and the named-unparsed arm, same module |
| the two live-specimen `assert glob(...)` lines | `test_the_stray_sweep_sees_a_todo_file_one_level_down`, same module |
| the `os.listdir` directory check in both cutoff cases | `conftest.cutoff_item_is_traceable`, which keeps the failing half |
| `tests/test_tmp_every_new_arm_is_red.py` | nowhere — a probe, deleted by §7. What it observed is the table above |
