# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — phase 1

<!-- seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | f06b728f |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md`'s phase 1, #667 round 3's 🟡 2: the oracle asks every inline HTML
token. In `tests/commonmark_oracle.py` the kind `comment` becomes
`inline html`; `_comment_lines` becomes `_inline_html_lines` and keeps every · NAME NOT IN TREE
top-level `html_inline` token; `_starts_in_a_comment` becomes · NAME NOT IN TREE
`_starts_in_inline_html` and finds the sentinel in an `html_inline` token at
any depth; the docstrings say *inline raw HTML* and why lines are read at the
top level and pieces at any depth. `test_the_oracle_names_each_kind_it_hides`
gains one row per construct of `spec.md` S1 and
`test_the_oracle_reads_the_text_not_a_readers_split` gains S2's assertions,
each seen red with the oracle from `3fc0c5bd`. No `FOUND` change. Q5: the
property module green with the base walk. Ledger: P1-2 corrected, its
`_comment_lines` anchor dropped, and a row for the renamed units in this work · NAME NOT IN TREE
item's fragment.

## What this phase found

- **Q5 is green.** With the widened oracle and the walk from `3fc0c5bd`,
  `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -p no:xdist`
  exits 0, 67 passed. No document in the existing corpus puts a line start or
  a piece inside a non-comment construct that runs past a line ending, so
  phase 1 closes alone, as planned.
- **S2 did not hold for the closing tag with one sentinel, so the oracle
  carries two marks.** A piece inside `</span` + break + `>` starts where only
  whitespace may stand, and a run of letters there breaks the tag, so the
  oracle answered "shown" for all eight breaks (executed,
  `<scratchpad>/1790659274/q4.py`). A run of five Unicode spaces
  (U+2002, U+2003 alternating) is tried second. A piece starts just after a
  break the parser reads as whitespace, so the spaces land where one space
  already stands, and every other kind's piece was already found by the
  letters (executed: letters and spaces both found H2 to H6 at all eight
  breaks, spaces alone found H7). The frame's S2 row names H7, so this is
  building to the frame, not past it; `SPACES` is a unit the frame did not
  name.
- **The image description.** The frame said pieces are read "at any depth, an
  image description's children included". An assertion over
  `![x <span title="a` + break + `b">](u)` pins that; the parser renders an
  image's description as `alt` text and drops `html_inline` from it, so the
  piece is hidden. Without it no case covered the recursion, and a
  mutant reading the top level only would have stayed green.
- **R1-1's `_starts_in_a_comment` anchor is dropped here, not in phase 2.** · NAME NOT IN TREE
  The rename lands in this phase, so leaving the anchor for phase 2 would have
  left a BROKEN row across a commit. The row's walk half is still corrected
  in phase 2, where the walk changes.
- **The rename leaves the old names in records, and the records arm refuses
  them.** `bin/evidence-check --ledger <this fragment> .` exits 2 on
  `NOT-IN-TREE` lines: `_comment_lines` and `_starts_in_a_comment` in work · NAME NOT IN TREE
  item 1790645290's `phases/phase-2.md`, `rounds/round-3.md` and
  `rounds/round-3-report.md`, and in this work item's `spec.md` and
  `plan.md`. The frame's §*Data & interfaces* priced the rename in ledger
  anchors and not in record names. The same run also refuses names the tree
  does not have yet (`leaves_html_open`, `TAG_END`, the S3 case) and two it
  will never have, from markdown-it-py's source (`HTML_TAG_RE`, `link_open` · NAME NOT IN TREE
  in `spec.md` and `questions.md`), which were refused at `7b4f105f`
  already. Phase 2 creates the first family and closes with a records pass
  that marks the rest ` · NAME NOT IN TREE`, the remedy the checker names and
  the one earlier work items used in their round records.
- **Mutations, one unit at a time, each red** (`<scratchpad>/1790659274/mutate.py`,
  restored from kept bytes after each run): lines read as comments only;
  pieces read as comments only; the letters mark alone; pieces read at the
  top level only; `_tokens` not recursing. The S1 rows and the S2 assertions
  were also run against the oracle from `3fc0c5bd` with only its kind renamed
  to `inline html`, so the rename could not be what failed them: 14 failed,
  the six new S1 rows and all eight breaks of S2.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tests/commonmark_oracle.py#_comment_lines` and `#_starts_in_a_comment` (renamed) | `_inline_html_lines` and `_starts_in_inline_html`; their claim is P1-1 of `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md`, and the dropped anchors are noted in P1-2 and R1-1 of work item 1790645290's fragment · NAME NOT IN TREE |
| the oracle's kind `comment` | `inline html`, spelled in the two expectations that spelled `comment` |
