# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 865652a9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Run `evidence-check` and read every BROKEN and DRIFTED row it names. Write
the two `Corrected ·` rows by hand in this item's fragment, each carrying
every coordinate its claim still rests on. After reading each drifted row,
run `evidence-check --reverify --into <fragment> --checked <date>`, narrowed
with `--ledger` to what was read, and re-stamp any other work item's fragment
row in place. Add this item's own rows, write `changelog.md`, and run
`survivor-check --range 2b1dcb1f...HEAD`, correcting or exempting each
survivor. Answer M1, M2 and M3. Released ledger files are never edited.

## What this phase found

**Nine rows were drifted before this branch existed.** `evidence-check` over
an archive of 2b1dcb1f names six citations and one `templates/config.md`
coordinate in work item 1790993138's fragment, one `docs/branch-and-release.md`
coordinate in 1790993139's, and `seal/releases/0.5.0.md`'s
`templates/config.md` row. They are the same nine at this branch's tip. The
integration commit bb2f3400 re-stamps them: `evidence-check --strict` over an
archive of it exits 0. They were left, and `--ledger` kept the reverify off
them (`overview.md` §*Not done*).

**What this branch drifted or broke**, each row read against the edit that
moved it:

| Released row | Coordinate | What moved it | Written |
|---|---|---|---|
| 0.17.0 G17 | §*Known limits of the commit gate inside git* | moved, and its first bullet re-pointed | `Corrected ·`, new hash `da878498`, the other four coordinates carried at their released hashes |
| 0.4.0 *two opt-in headings* | §*Review arm*, §*Parity arm* | moved, unchanged | `Corrected ·`, both at the released hashes `3f374912` and `4b9d8901` |
| 0.16.0 E9 | `## commit-review-gate (PreToolUse, Bash)` | the arms left from under it; *the section above* became a citation | `Re-read ·` |
| 0.16.0 E1, E2, E6, E17, E18; 0.17.0 G8 | `hooks/commit-review-gate.py#main` | one comment's citation | `Re-read ·` each |
| 0.14.0 R1 | `#touches_code` and two hardening cases | a docstring citation, a path, a docstring | `Re-read ·` |
| 0.15.1 S3 | `REVIEW_CHAIN_DOCS`, `review_chain_text` | five documents where there were three | `Re-read ·`, noting the five |
| 0.15.4 A2 | `chain_check.py#restored_from` | a docstring citation | `Re-read ·` |
| 0.16.0 E8 | agent contract §17 | its citation of §*The commit gate inside git* | `Re-read ·` |
| 0.12.0 (prose maxima), 0.9.3 (*the eleven modules*) | `tests/test_docs_line_wrap.py#COVERED` | two entries added | `Re-read ·` each |
| work item 1790993137's P11 (a fragment) | `#COVERED` | the same | re-stamped in place by the reverify, with a dated note |

`--reverify --into … --checked 2026-10-03`, narrowed with `--ledger` to the
seven released files and the one fragment read, wrote exactly the 13 rows the
table names and re-stamped the one fragment row. Each `Re-read ·` row's
verification cell was then rewritten from the tool's generic sentence to what
was read.

**M1.** 13 `Re-read ·` rows, against the frame's 2 for the document's own
anchors and an upper bound of about 13 more. One of the frame's two did not
drift: S2's `"Authority for"` minor anchor hashes the line it names, and D4
kept that line. Of the upper bound, `#DOC_ROOTS` in both hooks did not drift
(M2). The rest drifted as read off the anchors: `#main` 6, `#touches_code` 1,
`#restored_from` 1, `tests/conftest.py` 1, `#COVERED` 2 released and 1
fragment row, §17 1. With E9, 13.

**M2.** No. The comments above `DOC_ROOTS` in `hooks/commit-review-gate.py`
and `hooks/gate.py`, and the two above test functions in
`tests/test_the_commit_gate_decides_at_the_commit.py`, sit outside the unit
that follows them: no row anchored on those units drifted. A docstring is
inside its function, which is why `#touches_code` and `#restored_from` did.

**M3.** `survivor-check --range 2b1dcb1f...HEAD` reported one place:
work item 1790815613's `overview.md`, line 49, the memo recording why the
freeze was written. It is a record of that moment, so it is exempted in
`survivors.md` with a quote from its own sentence. The first quote taken from
a later sentence of the same line did not match: the exemption is matched
against the candidate sentence's words, not the line's.

**Verified, executed.**

- `bin/evidence-check --strict .`: this item's fragment 65 ok, 1790993137's
  95 ok, nothing BROKEN; exit 2 on the nine rows drifted at the base, and on
  nothing else.
- `bin/correction-check --range 2b1dcb1f...HEAD`: exit 0, *no released
  ledger file changed*.
- `bin/survivor-check --range 2b1dcb1f...HEAD`: exit 1, one place; with
  `--exempt seal/specs/1791019477-…/survivors.md`: exit 0, *every survivor is
  excused by a row above (1)*.
- A `test_tmp_*` probe that kept both files' bytes and restored them by hash:
  the direct answer's carrier cases passed, went red with a forbidden sentence
  appended to `docs/the-commit-gate-inside-git.md`, and passed with that
  sentence still planted once the inside-git entry was taken out of
  `REVIEW_CHAIN_DOCS`. That is C3's evidence, and §15's red for the tuple
  entry.
- The changelog, ledger-fold, merge-correction and two-branch re-read modules:
  193 passed.
- At 865652a9, once more over the 13 K2 modules, the six other
  `REVIEW_CHAIN_DOCS` consumers and the three hygiene modules
  (`tests/test_no_real_identifiers.py`, `tests/test_release_hygiene.py`,
  `tests/test_a_script_says_which_interpreter_it_needs.py`), one `bin/test`
  command: 1181 passed, 78 skipped. `bin/fold-check --root .`: exit 0.
  `uvx ruff check` and `uvx ruff format --check` over the 15 Python files the
  branch touched: clean.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
