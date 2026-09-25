# 1790297087-a-ledger-row-that-will-not-parse-is-counted — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b94697c3 |
| Ran by | unknown — the spawn prompt did not name the agent and model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 3: the commit advisor names `MALFORMED` rows.
`hooks/evidence-advisor.py#failing_rows` takes the verdict into its filter,
its docstring says so, and `main` prints a block with the remedy. Then the
work item closes, with `changelog.md` and `overview.md`. The spawn adds that
#322 is already fixed at `97e29b7a`, so nothing is built for it, and this
record and the overview say so for the pull request to claim. Verified by
S11 in `tests/test_dispatch.py` beside
`test_a_commit_with_a_pre_anchor_ledger_is_pointed_at_the_migrator`, and by
the docstring pin in `tests/test_a_row_points_by_content.py` extended to
`MALFORMED`, both seen red first. `tests/test_dispatch.py` runs whole at the
boundary, with every module that reads a document this phase edits.

## What this phase found

- **Both cases were red first**, executed against the phase-2 advisor
  (`80e2f3af`). S11's commit printed nothing at all, an empty stdout: the checker named
  the row, and `failing_rows` dropped it. The docstring pin failed with
  *the docstring does not name the MALFORMED block*. Both are green after.
- **Mutation**, executed one at a time over `tests/test_dispatch.py` and
  restored from saved bytes. Taking `MALFORMED` out of the filter, turning off
  the block, and dropping the block's row lines each turn S11 red.
- **#322 needs no code, and none was written.** Executed 2026-09-25, not
  taken from the frame: `97e29b7a` (#531) is the commit that made the
  docstring `r"""`, and `git tag --contains` puts it first in `v0.14.0`. The
  docstring is now at `tests/test_a_row_points_by_content.py#test_an_old_format_ledger_is_loud_never_invisible`,
  still raw. Every `git ls-files '*.py'` file (176, this branch's new code
  included) compiles with warnings as errors under Python 3.12.11, with
  0 errors. `questions.md` Q2's default (a) adds no guard, so the pull
  request can say `Closes #322` on these grounds.
- **Five release-file rows cite the advisor's two units** and drifted. They
  are 0.4.0's advisory row, 0.5.0's S6 and S12, and 0.15.1's R2. Each was
  re-read against the edit, holds, and carries a dated note and the
  re-stamped hash. **The drift report named four of them, and `--reverify`
  re-stamped five.** 0.5.0.md holds two rows citing `failing_rows` at one
  hash, and the report names a coordinate once per file. That is the hazard
  `seal/follow-up.md`'s drift-report row describes. S12 was found by counting
  rows per anchor after the re-stamp, and it was read and noted before the
  commit. Phase 2's re-stamps were enumerated from the rows rather than the
  report, and the same count finds no other file with two rows at one
  re-stamped anchor.
- **The advisor's per-commit cost moves a little.** `malformed_rows` over
  this repository's 33 ledger files takes about 55 ms in process, against
  318 ms for `old_format_rows` on the same files, executed 2026-09-25. The
  docstring's 1.7 s figure is dated 2026-09-23 and is left as that dated
  measurement.
- **Boundary run**, executed at `b94697c3`'s tree before its commit: 38
  modules, 2031 passed, exit 0. They are `tests/test_dispatch.py`,
  `tests/test_a_row_points_by_content.py`, and every `tests/` file naming
  `evidence-advisor`, `releases/0.5.0.md`, `releases/0.15.1.md`,
  `releases/0.4.0.md`, `changelog.md`, `seal/ledger/`, `overview.md` or
  `"releases"`. Ruff check and format are clean on the three changed Python
  files.
- **The survivor sweep over the whole build**, `survivor-check --range
  0abfb371..HEAD` at `b94697c3`, reported four places, none a claim the
  range corrected. Each is in `survivors.md` with a quote and grounds, and
  the sweep with `--exempt` reads *every survivor is excused*.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
