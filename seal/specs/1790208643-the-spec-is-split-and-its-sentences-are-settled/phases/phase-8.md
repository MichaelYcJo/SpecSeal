# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 8

| Field | Value |
|---|---|
| Phase | 8 |
| Commit | 28439296 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

#562, added at the resumption. Escape every unescaped `|` inside a ledger
cell as `\|`, with the text otherwise byte-identical: rows R5 and P2 that
#547's notes split, and the twenty older rows the issue names. A row's cell
count must equal its table header's. If a check for the class is cheap (a
case in an existing ledger module), add it red-first; otherwise say why not.

## What this phase found

**22 rows, as the issue counted** (executed: a scratch scanner that splits on
unescaped `|`, skips fenced blocks, and compares each table row with the
header above it, over `seal/ledger.md` and every fragment). 21 rows are in
`seal/ledger.md` and P2 is in D's fragment; R5 is `seal/ledger.md:2315`.

**19 were a pipe inside a code span**, a quoted shell pipe or `grep -c '^|'`.
Escaping exactly the in-span pipes brought each row to its header's five
cells, and the script asserts both, the count and the byte-identity.

**Three were not a pipe in a code span.** Each Notes cell carried a second
`… | <date> | <notes>` pair that an earlier re-read wrote in, rather than
editing the cell: G5 (`1789…`, #386's), S4 beside it, and *The eleven
modules that pin the path*, which also has no trailing pipe. The two extra
separators in each are escaped too. Which pair is the row's true
`Checked`/`Notes` was not the escape's to decide, so the first date stays the
`Checked` column and the rest reads as Notes. A reader may want those three
rows rewritten as one note each, and that is a judgment about a claim,
outside #562.

**The text is otherwise unchanged** (executed): both files equal their
`HEAD` versions once `\|` is read as `|`. `evidence-check --strict .` exit 0
with the same `1831 ok`, because no anchor cell and no anchored section
moved.

**The check is cheap, so it was added** in `tests/test_release_hygiene.py`,
the module that already reads this repository's own ledger files
(`ledger_files`). It adds `overwide_rows(text)`, a fixture case (an
unescaped pipe in a code span is named, the escaped twin is not), and
`test_no_ledger_row_splits_into_more_cells_than_its_header`. The last one
reads `ledger_files()` (the shared file and every release file) and every
fragment.

- Red first: the ledger and D's fragment were put back to `HEAD`'s bytes,
  with copies kept. The real-tree case was exit 1 and named 22 rows, the
  fixture case passed, and both files were restored and compared (`cmp`).
- Green after: the hygiene module gave `50 passed`.
- `uvx ruff check` and `uvx ruff format --check` exit 0.

**What `CLAUDE.md` needs: nothing from this phase.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — escapes only | none |
