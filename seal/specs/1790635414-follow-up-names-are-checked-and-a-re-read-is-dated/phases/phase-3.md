# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — phase 3

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | bad06402 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 3, `--reverify --checked`, to the owner's answer
from before the first edit: `--reverify --checked <date>` writes that date on
every row whose hash moved; without the flag the date is left alone and
those rows are named; a row whose hash did not move is never touched. R1–R9:
argument validation, the date-cell finder, splicing by unescaped pipe, the
no-flag naming block, `LEFT` for a moved row with no date cell, and the RIDER
on `reverify` removed. Documents: D1 whole, and D3.

## What this phase found

- **The date-cell finder reads A's `ledger_table_rows`** (Q2), so there is
  still one table walk in the file. `date_column` is the header rule
  (`Checked`, else `Date`, else the fourth cell of a headerless row exactly
  `len(LEDGER_COLUMNS)` wide), and `dated_cell` the splice.
- **`reverify` now collects its hash edits before it writes any.** Under
  `--checked` a row with no date cell is left whole, and that is known only
  once every coordinate on its line has been read, so the splice that used to
  happen as each match was found became a list of edits grouped by row. A
  row is its line: a match's offset is mapped to a line through the
  `gfm_lines` starts, the same line numbers `ledger_table_rows` yields. The
  per-coordinate `old -> new` lines print as the edits are applied, so a
  row left whole prints none of them and is not counted.
- **An anchor outside any table row is a row with no date cell.** M6 found
  none in this repository, but a consumer's ledger can hold one; under the
  flag it is `LEFT` like any other undatable row, and without it the naming
  block says `no date cell`.
- **The naming block cuts a row's first cell to `LABEL_WIDTH`, 72.** A claim
  cell in this repository runs to several hundred characters, and the ledger
  and line already locate the row. The block prints after the count line, so
  `N rows re-verified` stays where every existing reader matches it.
- **The refusal goes to stderr, prefixed `evidence_check:`,** with nothing
  on stdout, the way `rider_check.py` refuses `--only` without `--reverify`.
  `argparse`'s own error could not carry which rule refused, and it prints
  usage the reader did not ask for.
- **Tried against this work item's own fragment, the flag dated 4 rows once
  each and left every cell that already ended in the date alone** (executed,
  the narrowed `--reverify --checked 2026-09-29` that filled phase 3's
  hashes).
- **How each case was seen red.** Against `56e53c90` through the probe
  plugin, 23 of the 26 new cases failed (the flag does not exist there). The
  3 that passed were the R2 untouched direction and two unrelated cases the
  `-k` filter caught; R2 went red with the moved hash mapped to the row below
  its own. Fifteen mutants over the new units. Two stayed green and each got
  a case, both committed at `23645bd4` and both then seen red under the same
  mutant: a headerless row of four cells was dated where only a five-cell
  row may be, and the label was printed whole. One stayed green and is
  recorded instead: `CHECKED_RE`'s `[0-9]` against `\d`, because
  `datetime.date.fromisoformat` refuses fullwidth digits by itself on Python
  3.13. The pattern as a whole is held, by the `20260929` value, which 3.11's
  `fromisoformat` accepts.
- **R9: the RIDER is gone and rider-check reads the tree clean** (executed,
  `.github/scripts/rider_check.py --root .`: `21 ok · 0 drifted · 0 broken`).
  R8's fenced-example case, `tests/test_evidence_check.py`, passes unchanged.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the RIDER on `reverify` ("decide whether it should refuse … or print the ones it left") | answered by the owner before this frame; its measurement now heads the `--checked` section's comment in `evidence_check.py`, and the behaviour is in `reverify` |
| `reverify`'s splice-as-found (`out`, `at` built during the match loop) | the edit list applied per row after the loop |
