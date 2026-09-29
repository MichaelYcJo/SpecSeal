# 1790666894-the-oracle-counts-dropped-lines-from-the-parser — phase 1

<!-- seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | cbfe84f8 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model; the orchestrator fills this row |

## What this phase was asked

`plan.md`'s phase 1 row: the oracle takes the dropped-line count from
markdown-it-py's own `paragraph` and `lheading` rules through a wrapper,
`_recording_lines`; the hand-written marker helper is deleted;
`_inline_html_lines` loses its `lines` parameter and starts at `map[0]` plus
`meta["dropped"]`; the module docstring gains its sentence. A new case holds
S1 and S2, and S5 goes into `FOUND`. In the same commit: H's R1-1 REMOVED,
H's P1-1 corrected and re-stamped, F's P1-2 re-read and re-stamped, a new
row in this work item's fragment, and ` · NAME NOT IN TREE` on exactly the
lines of H's records the records arm names. Each new row seen red: S1 and S5
against the oracle from `cd56113c`, S2 with `lheading` unwrapped, the whole
case with the count forced to 0. The round 3 report's numbers were the
reviewer's until re-run.

## What this phase found

**The runs, all executed in this worktree** (`bin/test` on the property
module, `-p no:xdist` for the red runs, `tests/__pycache__` cleared between
mutations, each mutation restored from bytes kept in the scratchpad and
checked with `cmp`):

| Oracle | Result |
|---|---|
| At base, before any edit | exit 0, 87 passed |
| The oracle at `cd56113c` (byte-identical to the base) with the new rows | exit 1, 6 failed: the five S1 rows and `test_where_the_walk_claims_to_be_exact_it_is` on S5, as `[(4, 'live', True)]`; the three S2 rows green |
| The fix | exit 0, 95 passed |
| The fix, `lheading` unwrapped | exit 1, 3 failed: the three S2 rows alone |
| The fix, `paragraph` unwrapped | exit 1, 17 failed: the five S1 rows, 11 of the 13 existing marker rows, half 2 |
| The fix, the count forced to 0 on the read side | exit 1, 20 failed: all eight new rows, the same 11 marker rows, half 2 |

The report's numbers re-run in their shape. Its 16 red with the count forced
to 0 were the 11 existing marker rows, its three `>` rows, its setext row and
half 2; with the five S1 rows and three S2 rows planted here the same run
gives 20. Its "1 red with `lheading` unwrapped" is three here because S2 has
three rows. Its 18/18 probe was not re-run as a probe; the eight rows are the
shapes it covered that were wrong or unpinned. The two existing marker rows
that stay green under every mutation are `a dash that is no marker` and
`ten digits are no marker`: their first line is text, so nothing is dropped.

**Q1, S1 and S2: markdown-it-py gives CommonMark's answer on all eight**, as
the spec wrote them; no row pins a departure.

**Q3: the floor holds**, so S5 stays in `FOUND`. The records arm named 26
refusals on 24 lines in five files — `round-1.md` (1), `round-2-report.md`
(7), `round-2.md` (4), `round-3-report.md` (9), `round-3.md` (3). Grep had
found 38 lines in six files; `round-1-report.md` names the helper only where
the arm does not read. On a table row the marker goes inside the last cell,
before the closing ` |`, as H did for F, so the row keeps its cell count for
the readers of `rounds/round-N.md`.

**The checker named two drifted rows the frame's grep did not**: H's P2-1 and
F's P2-1, both through `FOUND`. Each took a `Re-read` note: the walk is
untouched and the new document agrees. H's P1-1 re-stamped only
`_inline_html_lines`; `test_the_oracle_names_each_kind_it_hides` did not
change, so its hash did not move.

**A constraint found by trying.** The PostToolUse formatter removes an import
the moment an edit adds it, if nothing uses it yet. The first edit added the
two `rules_block` imports before the wrapper that uses them, and the next run
failed on `NameError: name 'paragraph'`. Adding the import after its first
use keeps it.

**For phase 2.** S3 and S4 rows go in
`test_the_oracle_counts_the_lines_the_parsers_strip_dropped` (S3) and a case
of their own (S4). The count-forced-to-0 mutation is
`.get("dropped", 0) * 0` in `_inline_html_lines`. The virtualenv `bin/test`
built runs Python 3.13.9, not the 3.14 the spec's S4 names; S4 computes its
set, so the case is the same code either way, and the set phase 2 measures is
3.13's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tests/commonmark_oracle.py`'s hand-written marker helper and its docstring's reading of CommonMark 5.1 and 5.2 | `tests/commonmark_oracle.py#_recording_lines` and `#_inline_html_lines`' docstring; the reason it went is `seal/ledger/1790666894-the-oracle-counts-dropped-lines-from-the-parser.md` P1-1's tidy-up note |
| H's ledger row R1-1 | its claim went with the helper; the new claim is P1-1 of this work item's fragment, and H's P1-1 carries a `Corrected` note naming it |
| `_inline_html_lines`' `lines` parameter | nowhere: nothing read it after the count moved to the parser |
