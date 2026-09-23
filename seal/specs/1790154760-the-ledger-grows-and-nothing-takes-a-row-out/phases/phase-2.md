# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 9374d402 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Replace the advisor docstring's "about 114 ms" with the measured value, its
method and its date. Write the changelog fragment and the ledger fragment
`seal/ledger/1790154760-the-ledger-grows-and-nothing-takes-a-row-out.md`.
Re-read and `evidence-check --reverify` the shared rows the change drifts
(the `py_spans` row, hash `4045ba55` at framing, at minimum). Write `overview.md`,
carrying Q1's default (close #519).

## What this phase found

**Three shared rows drifted, not one.** `--strict .` after the docstring
edits named `py_spans` and `scan_candidates`, and `--reverify` rewrote three
rows: the `py_spans` row (`seal/ledger.md`, anchors resolve through `ast`)
and two rows citing `scan_candidates` (`--reverify` re-anchors what
reconstruction proves; the scanned-source path keeps its `relpath`). Each
claim was read against the new code and still holds; each carries a
`Re-read 2026-09-23 by work item 1790154760 (#519)` marker in its Notes
cell. The `--reverify` run came before the third row was read, and the read
after it found nothing that needed a different hash: the unit's only change
is its docstring.

**The "114 ms" was one fact in three places.** The advisor's docstring,
`scan_candidates`'s docstring and the docstring of
`test_past_the_file_cap_the_scan_degrades_and_says_so`. The advisor states
the measurement with its instrument. The other two now state the property
without a number, so there is nothing left in them to go stale.

**Writing the ledger fragment made this work item's records readable, and
two things surfaced.** The records arm of `--strict` reads the records of any
work item with a fragment. `spec.md` Scope item 4 carried the `py_spans`
row's framing-time anchor in anchor shape, and it read BROKEN, exit 2. The
sentence now says the same thing in a shape the arm does not read as a stamp,
and so does this record's own copy of it. The names this work's records give
in `tests/test_a_row_points_by_content.py` also made the arm parse that file,
and one docstring there held an escape Python warns about, so every
`--strict` run printed a `SyntaxWarning`. The docstring is now raw, which
keeps its value. `overview.md` records both, with the grounds.

**Verification, executed 2026-09-23 at `9374d402`:**
`evidence_check.py --strict .` exit 0, `total: 1476 ok · 0 drifted · 0 broken`.
The slice `tests/test_a_row_points_by_content.py`, `tests/test_dispatch.py`,
`tests/test_local_mode_resolves_under_the_git_dir.py`,
`tests/test_the_changelog_is_gathered_at_release.py`,
`tests/test_the_ledger_fragments_fold_at_release.py` and
`tests/test_a_merge_cannot_silently_drop_a_correction.py`: `252 passed`,
exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the undated "about 114 ms" in `hooks/evidence-advisor.py`, "~114 ms" in `evidence_check.py#scan_candidates` and "114 ms" in one test docstring | the measured cost now in the advisor's docstring, and ledger row C2 of this work item's fragment |
