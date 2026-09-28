# 1790635412-an-overflow-cell-is-refused-in-every-repository — phase 3

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | e1ea265f |
| Ran by | unknown — the spawn prompt did not hand this value over, and the template forbids a segment to source it from its own idea of what it is; the orchestrator fills it |

## What this phase was asked

Build `plan.md`'s Phase 3, this repository's case is a caller. In
`tests/test_release_hygiene.py`, the corpus case's walk becomes a helper
taking a root and calling `evidence_check.overflow_rows` over the checker's
own listing; the corpus case calls it on `ROOT`, and a planted-tree case
calls it on a tree with one overflowing fragment row (A12). The old rule's
five units and its two unit cases are deleted. The paragraph in
`docs/the-evidence-ledger.md` says the shipped checker names such a row
`OVERFLOW` in every repository, and its `Enforced by:` line names
`evidence_check.py::overflow_rows` and the corpus case. C2 in
`seal/releases/0.15.1.md` and L1 in `seal/releases/0.15.3.md` are removed.
1790260565's `questions.md` Q1 is ticked.

## What this phase found

- **The helper is `overflowing_rows(root)`**, and it reads
  `resolve_patterns(default_patterns(root))`, the plan's default. The
  planted tree needs nothing more than a `seal/` directory for that listing
  to resolve, so the default held. The planted case plants a split row in
  each of the four places the listing reads, `seal/ledger.md`, a fragment, a
  release file and a `docs/**/_evidence.md`, and asserts all four are named.
- **Seen red, and how.** The planted case, with the helper's call to the
  arm replaced by `[]`: 1 failed. With the listing narrowed to its first
  pattern: 1 failed, so the case also holds that every location is read.
  Both restored from kept bytes. The corpus case is green over this tree.
- **The arm found one row the old case never read.** The fold fixture in
  `tests/test_the_ledger_fragments_fold_at_release.py` wrote a Notes cell
  `a note with a | pipe escaped as \|`, whose first pipe is unescaped, so
  the row had six cells. `test_the_checker_reports_the_same_totals_before_and_after`
  went red with `1 overflow` and exit 1. The row is the defect the arm
  exists to name, not a trade `spec.md` did not state, so the arm is not
  narrowed: the fixture escapes both pipes, which keeps what it was for, an
  escaped pipe surviving the fold byte for byte. This is the one row Q1's
  phase 1 run could not see, because that module was not among Q1's four.
- **The class, enumerated (§12).** Every module under `tests/` that drives
  the checker or the advisor, 28 of them, was run after that fix: 1488
  passed, 7 skipped, 1 failed. The one failure is
  `test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
  which asks this work item for the closing memo phase 4 writes. No other
  fixture holds a split row.
- **The removed rows get a note where they stood**, as S1's removal in
  `0.15.1.md` and S1 and P1's in `0.14.0.md` did: C2's inside the comment
  above its table, and L1's as a comment under its work item's heading in
  `0.15.3.md`, which had no comment to extend.
- **The policy paragraph's last sentence** was "The case reads the shared
  file, every release file and every fragment." It now says the shipped
  checker names such a row `OVERFLOW` in every repository that installs the
  plugin, graded like `MALFORMED`, and that this repository's case holds
  its own ledgers to that reading on every pull request.
- **Narrow runs.** `bin/test tests/test_release_hygiene.py
  tests/test_a_folded_statement_names_what_enforces_it.py
  tests/test_a_document_has_room_for_the_next_fold.py
  tests/test_the_ledger_fragments_fold_at_release.py
  tests/test_docs_line_wrap.py tests/test_a_row_wider_than_its_header_is_named.py`
  green after the fixture fix. `grep` over `tests/` for the five deleted
  names returns nothing (exit 1). `uvx ruff` over the changed test files:
  clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the five units of the old rule in `tests/test_release_hygiene.py`: `overwide_rows`, `cell_count`, `TABLE_RULE`, `ledger_row_width`, `ledger_overwide` · NAME NOT IN TREE | `skills/evidence-check/scripts/evidence_check.py#overflow_rows`, `#ledger_table_rows` and `#LEDGER_COLUMNS`, which the corpus case now calls through `overflowing_rows` |
| its two unit cases, for the #562 split row and the #501 header-less row | `tests/test_a_row_wider_than_its_header_is_named.py`, whose A1 and A2 cases hold both shapes and the header-less row beside a two-column table |
| C2 in `seal/releases/0.15.1.md` | the fragment `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md`, written in phase 4 |
| L1 in `seal/releases/0.15.3.md` | the same fragment |
| the policy paragraph's last sentence, "The case reads the shared file, every release file and every fragment." | the paragraph's new last sentence, naming the shipped checker and this repository's case |
