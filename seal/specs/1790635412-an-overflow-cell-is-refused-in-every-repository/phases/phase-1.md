# 1790635412-an-overflow-cell-is-refused-in-every-repository — phase 1

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | dd9f89e6 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s Phase 1, the arm and the pages that state it. In
`evidence_check.py`: `LEDGER_COLUMNS`, `ledger_table_rows`, `grounds_cells`
reading through it, `overflow_rows`, the `check_ledger` call, the totals key
and both summary lines, `exit_code`'s branch, `LENIENT_NOTICE` naming
`OVERFLOW`, and `reverify`'s `LEFT` line with exit 1. The pages: the
`--strict` flag row, the reader table except the advisor's cell, a verdict
row and two *Known limits* bullets in `skills/evidence-check/SKILL.md`;
`skills/evidence-ci/SKILL.md`'s "1 is not only drift" paragraph;
`templates/evidence-check.yml`'s comment; `.github/workflows/test.yml`'s
comment and warning; and the command-table row of both READMEs. A new
module for A1–A6, A8, A9 and A13, the lenient-notice module extended for
A11, and the changelog fragment's entry. The spawn prompt added that work
item C (#508, #387) builds on `LEDGER_COLUMNS` and `ledger_table_rows` after
this squashes, so both keep the names and the shape `spec.md` states.

## What this phase found

- **The frame holds.** Every coordinate `plan.md` §*Technical context* names
  was where it said: `check_ledger`'s two `extend` calls, `grounds_cells`'
  header rule, `exit_code`'s `MALFORMED` branch below `BROKEN`, the four pins
  on the notice, and `broad_gate.py#LEDGER_RE` reading only up to `broken`.
  The checker at the branch's base is byte-identical to `11e3104c`'s
  (`git diff --stat 11e3104c HEAD` over `skills hooks tests` printed
  nothing), so "seen red at `11e3104c`" was run against the unedited file in
  place rather than a saved copy.
- **No walk was added, so `unverified_check.py#fence_opener`'s docstring is
  not edited.** `ledger_table_rows` is `grounds_cells`' walk moved out, and
  `overflow_rows` reads through it; the count of ledger walks that read
  through `quoted_lines` is what it was. B (#584) is free to edit that
  docstring.
- **`grounds_cells` takes a header-less row's column from `LEDGER_COLUMNS`**,
  `LEDGER_COLUMNS.index(CODE_GROUNDS)`, which is `1`, the literal it replaced.
- **The `LEFT` line's coordinate is the ledger's display name and the line**,
  `seal/ledger/f.md line 5`, through `display_name`, so
  `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` stays
  green without a new carrier.
- **Q1, measured.** The boundary run of the four modules
  (`test_a_row_points_by_content.py`, `test_evidence_check.py`,
  `test_the_lenient_run_says_what_the_broad_gate_will_say.py`,
  `test_dispatch.py`) after the arm and before any case was edited: 7
  failed, 255 passed, and all seven in the lenient-notice module. Each pins
  a sentence or a key this work changes, and each took the new text:
  - the `NOTICE` literal (three cases matched it);
  - the two key tuples, in `test_the_grading_is_one_function_and_the_line_reads_its_answer`
    and `grading`, which raised `KeyError: 'OVERFLOW'` in two cases;
  - the module docstring's `1 drift or malformed only`, now
    `1 drift, malformed or overflow only`.
  No case in the other three modules moved: the totals are matched as
  substrings, and the new field is last. No verdict or exit code moved for a
  row this work did not mean to touch.
- **A11's shape: a column of its own.** The reader table gained an
  `OVERFLOW is` column rather than widening `MALFORMED is`, and
  `test_the_skill_states_the_grading_exit_code_returns_for_malformed` now
  walks both columns against `exit_code`. One shared column would have made
  the advisor's cell false between phase 1 and phase 2; this phase's advisor
  cell says, truly, that the advisor's filter drops `OVERFLOW`, and phase 2
  fills it. The page assertions were seen red before the pages were edited:
  the header was `['Reader', 'Drift is', 'MALFORMED is']`, the flag row did
  not name an overflowing row, and the CI warning did not say `overflow`.
- **The `reverify` rider went DRIFTED**, because the `LEFT` line is inside
  the function it sits in. It was read: it says `reverify` rewrites the hash
  and never the `Checked` column, which this edit leaves true, and the
  decision it asks for is work item C's (#387), sequenced after this squash.
  It is re-stamped with `.github/scripts/rider_check.py --reverify --only
  skills/evidence-check/scripts/evidence_check.py`, the one rider in that file
  that had drifted.
- **Q2, measured.** `bin/evidence-check .` after this phase read 36 ledger
  files; every per-ledger line and `total: 2605 ok · 29 drifted · 0 broken ·
  0 external · 0 old-format · 0 malformed · 0 overflow` end at zero overflow.
  The 29 drifted rows are this branch's, and phase 4 re-reads them.
- **Seen red, and how.** The new module ran against the unedited checker
  before the arm existed: 23 failed. A1, the header-less run case and A5
  exited 0 with no finding; A9 printed `0 rows re-verified` and exited 0;
  the function-level cases had no `overflow_rows`, `ledger_table_rows` or
  `LEDGER_COLUMNS` to call. A6 was seen red by the mutation below.
- **Mutation, one unit at a time,** restored from kept bytes with
  `tests/__pycache__` cleared between runs, over the new module, the
  lenient-notice module and `test_a_row_points_by_content.py`. Each turned a
  case red: `overflow_rows` returning `[]` (14 red), `<=` changed to `<` so a
  full row counts (11), a header-less row skipped (12), `check_ledger`
  dropping the arm (3), `exit_code` dropping `OVERFLOW` (7), `reverify`
  dropping the `LEFT` exit (1), a column renamed in `LEDGER_COLUMNS` (1, A6),
  and the walk not resetting its header on a non-row line (3, two of them
  existing `MALFORMED` cases).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
