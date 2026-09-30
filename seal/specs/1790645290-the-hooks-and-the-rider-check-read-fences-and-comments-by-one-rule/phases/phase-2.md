# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — phase 2

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a10ad490 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 2, the walk, with no reader on it yet: a stdlib-only
module under `hooks/` walking fenced blocks and line-start comment blocks in
one pass, closed only; the uncertainty mask for every context in `spec.md`'s
table; the unclosed-fence opener it saw. The delimiter copy moves there from
`hooks/config.py#FENCE`, or is read from there (Q5), and
`unverified_check.py#fence_opener`'s docstring says where it lives. Property
half 2 on the shapes and a seeded generated corpus, seen red twice (with the
comment-block rule removed, and with a mid-line `<!--` allowed to open a
comment), S3's parity case still green. The spawn made the oracle and the
property the point of the item, to be kept green through every phase.

## What this phase found

- **Q5, decided.** The module is `hooks/blocks.py`, a sibling of `optin.py`.
  Its surface: `FENCE`, `fence_opener`, `fence_closes` (the delimiter rule,
  moved; `hooks/config.py#FENCE` is now `blocks.FENCE`), `fence_only` (the
  fence rule alone, unclosed to the end, which is `hooks/config.py`'s base
  reading), `walk(lines)` returning a `Walk` with `kinds`, `uncertain` and
  `unclosed`, and `Walk.hidden(base)`, which gives the walk's answer where it
  knows and the reader's base answer where it does not. That last method is
  the whole of the acceptance property's half 1, written once, so each reader
  in phases 3 to 5 cannot combine the two readings its own way.
- **The frame's uncertainty minimum was not enough, and the property said
  where.** Four additions, each first seen as a generated document the walk
  claimed and the oracle disagreed with:
  - `- ```` and `>     code`: a construct, or an indented code block, behind
    a list marker or `>`. The frame named only a start indented one to three
    spaces. A fence opened after `- ` hides the item's `  | x |` lines,
    which are indented two and which the minimum called exact. Now a
    construct-looking line behind any container prefix makes the rest of the
    file uncertain, and every line behind a marker is uncertain itself.
  - a blank line between two indented lines, which is inside the code block;
  - a fence whose first closer has a no-break space after its run. The
    shared delimiter rule reads it with `str.strip`, which takes U+00A0, and
    CommonMark counts only spaces and tabs. Rather than a second delimiter
    rule, the walk claims nothing below such an opener; `fence_only` keeps
    the shared rule, and S3 holds.
  - a line holding only a no-break space is paragraph text, not a blank line,
    so a pending mid-line opener is not ended by it: blank is
    `strip(" \t")`.
  Q4 is answered (b), the minimum kept for exactness, widened only in the
  uncertain direction. The overview's first divergence row quotes both
  sides.
- **The oracle had one defect of its own, found the same way.** markdown-it-py
  strips a paragraph's inline source with `str.strip`, which drops a leading
  line holding only a no-break space, so a comment's offset was one line off.
  `commonmark_oracle.py#_comment_lines` counts the dropped lines back. It · NAME NOT IN TREE
  decides nothing about what a comment is.
- **Q7, measured.** One core, this macOS machine: 20,000 documents of up to
  24 lines take about 1.1 s through the oracle and the walk together. The
  suite runs 6,000 of up to 16 lines, seed 667, plus the frame's 32 shapes,
  1790635413's 16 comment shapes and the four found documents, in about a
  third of a second per property case. Wider, outside the suite: 60 seeds of
  20,000 over the committed alphabet plus 33 more lines (no-break spaces,
  `<?php`, `<!DOCTYPE`, `<script>`, `[ref]: <x>`, `10) ````, lines up to 24
  long), 1.2 million documents, no disagreement.
- **`hooks/config.py` imports the walk as a sibling**, the way
  `hooks/routing.py` imports `optin.py`. A copy of it without `blocks.py`
  raises one `ImportError` naming the path and what the file is for; it does
  not exit, because `PreToolUse` hooks import it and `hooks/dispatch.py`
  skips a gate that raises. `seal.py#HOOK_PURPOSES` gained `blocks.py`. This
  is the overview's second divergence row.
- **Seen red, and how.** Each unit mutated alone, bytes restored from memory,
  caches cleared: the comment-block rule removed (2 red), a mid-line `<!--`
  opening a comment block (1), no uncertainty behind a container (1), none
  for another HTML block (1), live lines below an unclosed construct claimed
  (1), no pending paragraph after a mid-line opener (1), pending ended at any
  closer (1), marker lines claimed (1), indented lines claimed (1), a blank
  after an indented line claimed (1), a tab counted as one column (1), the
  no-break-space guard removed (1), blank read by `str.strip` (1),
  `fence_only` never closing (14 in the parity case), the walk closing on
  any fence line (5), the oracle's offset repair removed (1), the import
  sentence removed (1), and `seal.py`'s purpose removed (1). Three were
  green on the first pass (marker lines, the blank after an indented line,
  the tab) because the committed corpus held no such document; the corpus
  gained the lines and `FOUND`, and all three went red.
- **Gate lines, drafted for `CONTRIBUTING.md` §*What a change to a gate must
  carry*.** No gate reads the walk yet, so no verdict moves in this phase.
  The walk's own failure direction is uncertainty: every context it does not
  model hands the line back to the reader's old reading. No question is
  asked. Platform: string processing only; CRLF is in the corpus.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/config.py#FENCE`'s own pattern | `hooks/blocks.py#FENCE`, which `hooks/config.py#FENCE` names |
