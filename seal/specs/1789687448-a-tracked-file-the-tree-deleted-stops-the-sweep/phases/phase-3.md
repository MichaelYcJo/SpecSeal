# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | bb5a6c36 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The inverse direction. `test_every_keep_entry_is_still_in_use` and the `gone`
assertion stop reading a skipped file as a deleted entry, decline to judge,
and name the missing paths. Q3 is answered here: every case in the five
modules is read for a verdict that depends on the corpus being whole. Each
skip reason is pinned by a case in the same commit (§14), and the two cases
are seen red with phase 1's bare skip and no liveness guard before they are
seen green.

## What this phase found

**Q3's answer is three, not two.** Reading the twenty-eight `test_` functions
across the five modules, a third case takes its verdict from the corpus being
whole: `test_no_document_names_the_old_roots.py#test_the_scan_covers_something`.
It asserts that two named paths are in the corpus, and
`skills/implement/SKILL.md` leaving through a `git mv` that has not been
staged is exactly the state this work is about — the case then reports the
scan as no longer covering a file that is merely somewhere else. It is
repaired here rather than carried back to `questions.md`, which is what that
row asked for.

Nothing else in the five modules qualifies. Only one function in
`tests/test_release_hygiene.py` consumes the corpus at all — `timer_offenders`,
a positive sweep — and its exemption cases (`RECORDS_OF_A_MOMENT`,
`ILLUSTRATIVE_VERSION`, `VERSIONS_OF_ANOTHER_PRODUCT`) read named files
directly rather than the listing, so a skip cannot reach them.
`test_a_release_is_sized_by_a_criterion.py`'s other cases read `OWNER` and
`CEILING_MODEL` by name for the same reason.

**The decline is conditional on there being a finding, and that is the
decision this phase settled.** A skip can only ever make an allowlist entry
LOOK unused, never used, so a run that finds every entry still in place has
reached the right verdict whatever it skipped. Declining unconditionally
would turn both checks off on any mid-edit tree, which trades a false alarm
for a check that stops running — the direction `seal/follow-up.md`'s first
row forbids. So the shape at all three call sites is *compute the finding;
if there is one, decline over the missing paths; otherwise judge*.

**The vacuity floor is the one half that does not decline.** In
`test_the_scan_covers_something`, `len(files) > 30` is what stops the sweep
passing on an empty read, so turning it off on a shrunken corpus would remove
the guard at the moment the corpus is actually short. The floor stays; only
the two named paths decline, and only when one of them is among the missing.

**Q2, measured rather than carried.** Two commands and one probe:

| Reading | Command | Result |
|---|---|---|
| What a fold removes | `python3 .github/scripts/fold_ledger.py --dry-run --version 0.12.1` | one file, `seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md`. `gather_changelog.py` removes nothing — it has no `os.remove`, and 79 changelog fragments stand |
| What the suite prints on that tree | the fragment removed from disk, removal unstaged, six modules run | **84 passed, 0 skipped**, exit 0 |
| The same tree before the guard | the fragment removed and `on_disk`'s classifying line reverted | `test_only_neutral_domains` and `test_only_fixture_user_paths` both `FileNotFoundError`, exit 1 — #432 reproduced at its own coordinate |

**So the skip count at a fold is zero, and `plan.md` says otherwise.** The
fold's missing path is under `seal/ledger/`, and only
`tracked_text_files` has a corpus reaching it — the other four exclude `seal/`
by their own prefix lists. Both of that helper's callers are positive sweeps,
which judge what remains and do not decline. A skipped case appears on a
different tree: a deletion under `docs/`, `skills/`, `.github/workflows/`,
`templates/` or a shipped `.py`, where one of the three declining cases reads
the corpus. `plan.md`'s Operational impact says a reader after a fold sees
`… passed, N skipped`; that is false for the fold and true for the other
deletions, and phase 5's checklist sentence is written to the measurement
rather than to the plan. The divergence is in `overview.md`.

**§15, how each case was shown red.** Four mutations, each applied alone to
`tests/conftest.py` and restored from bytes the probe kept:

| Mutation | What went red |
|---|---|
| `pytest.skip(...)` → `pass` — the bare skip with no liveness guard, which is phase 1's state | all three declining cases, plus `test_declining_raises_the_skip_carrying_that_reason`. Exit 1, 4 failed 34 passed |
| the reason's `", ".join(sorted(missing))` dropped | the three declining cases and both reason-shape cases. Exit 1, 5 failed 33 passed |
| the reason's `{what}` replaced by a fixed phrase | the three declining cases and `test_the_reason_names_every_path_and_what_declined`. Exit 1, 4 failed 34 passed |
| `os.path.isfile` → `os.path.exists` | `test_a_directory_on_the_list_is_not_a_file_that_is_there`. Exit 1, 1 failed 7 passed |

The six modules together are **84 passed** at exit 0 with everything in
place, read from `$?`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_the_scan_covers_something`'s two `assert <path> in files` lines | `COVERED` and `uncovered()` in the same module, which name the same two paths and decline over them |
| The corpus walk inside `test_every_keep_entry_is_still_in_use` | `keep_entries_not_in_use()`, in the same module. The refusal text stayed in the `test_` function |
| The `gone` computation inside `test_no_shipped_script_needs_more_than_the_floor_without_saying_so` | `classifications_of_nothing()`, in the same module, for the same reason |
