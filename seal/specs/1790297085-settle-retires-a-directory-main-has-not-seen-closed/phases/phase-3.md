# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 127dbe64 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#586, decided by the owner as option (a): the gatherer refuses.
`gather_changelog.py --version`, and so `--dry-run`, refuses an ungathered
fragment carrying a line that starts `## `, naming the path, the line number,
the line and the remedy, at exit 1 with nothing written. The docstring's exit
list, `docs/branch-and-release.md` and `CONTRIBUTING.md` say so. Spec S9 and
S10 as cases, S9 seen red first; the module and
`tests/test_a_release_publishes_its_note.py` green;
`gather_changelog.py --dry-run --version 0.15.4` on this repository read.
`questions.md` Q3 is not built.

## What this phase found

- **The frame holds.** The refusal sits in `main` after the
  *nothing to gather* arm and before the section is built, so neither the
  write nor the dry run prints a section when it fires.
- **The line numbers are read from the file again.** `fragments` strips each
  body, so a fragment that opens with a blank line would count from its first
  line with text on it. `section_lines` re-reads the fragment and numbers the
  file's own lines; the predicate is a module constant, `SECTION_LINE`, beside
  the comment naming its two readers.
- **The predicate is exactly the readers' and nothing wider.** `###`, a bare
  `##`, an indented `## ` and `##` with no space are gathered; a `## ` inside
  a fence is refused, since neither reader knows a fence. Each is a case.
- **The frame's measurement still holds:** no fragment in this tree carries
  such a line. The dry run on this repository printed the 0.15.4 section with
  this work item's fragment and exited 0.
- **Seen red (§15).** Against the code at `8f6648d0`, with only the cases
  added: 4 failed — S9 in both arms, the fenced line, and the documents — and
  6 passed, the five S10 lines and the already-gathered case, which are
  counter-cases. After the change, the module with
  `tests/test_a_release_publishes_its_note.py`: 56 passed. Mutations at
  `127dbe64`, each restored from the bytes read before it and each red: the
  predicate widened to `##` (4), the predicate reading stripped lines (1),
  line numbers from 0 (3), the refusal off (3), every fragment on disk read
  instead of the ungathered (1), and one deletion each of the docstring's
  clause, the `docs/branch-and-release.md` sentence and the `CONTRIBUTING.md`
  sentence (1 each).
- **Verified by (executed, 2026-09-25):** 45 test modules in one `bin/test`
  call — every one naming `gather_changelog`, `branch-and-release` or
  `CONTRIBUTING`, every one that globs `docs/` or lists the tree, and the
  release-note module. 2308 passed, 1 skipped, 2 failed: the S9 case asserted
  a lower-case `demote` against a sentence that opens `Demote`. The assertion
  now pins the sentence as printed, and the two modules re-ran at 56 passed.
  `ruff check` and `ruff format --check` clean on both changed Python files.
- **Ledger.** Seven rows anchor a unit this phase edited, and each was
  re-read against the edit and re-stamped in its own file, with a
  `Re-read 2026-09-25` note: `gather_changelog.py#main` in
  `seal/releases/0.13.0.md` S2 and `seal/releases/0.15.0.md` P3 and P3b;
  `docs/branch-and-release.md`'s release-branch section in
  `seal/releases/0.15.0.md` P1c; and `CONTRIBUTING.md`'s house rules in
  `seal/releases/0.12.2.md` C8 and `seal/releases/0.15.1.md` D1 and E1.
  None of the claims was made false. The frame's list named S2 and P3; P3b,
  P1c, C8, D1 and E1 were found by `evidence-check`. `#fragments` was not
  edited, so the 0.4.0 and 0.5.0 rows citing it did not move. The new claim
  is M4 in the fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
