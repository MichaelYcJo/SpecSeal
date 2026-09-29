# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — phase 1

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 3f37cecb |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 1, the oracle, before any reader moves. Q1 was
answered (a) by the owner: `markdown-it-py`, pinned to one version, as a
test-only dependency. `bin/test` and CI install it, an adopted `.venv` gets it
the way `run_tests.py#add_xdist` gives pytest-xdist, and the `CONTRIBUTING.md`
sentence changes. Hooks and shipped scripts stay stdlib-only. A helper in
`tests/` says from the parser's tokens alone which lines a renderer hides, and
the shape table's *Renderer* column is checked against it (Q2). The spawn
added that work item B's three round reports list every shape a previous
attempt got wrong, and each is to be planted as a case.

## What this phase found

- **The frame holds for this phase.** Every coordinate `plan.md` §*Technical
  context* names for it was where it said: `run_tests.py#PACKAGES` was
  `("pytest", "pytest-xdist")`, `#add_xdist` installs by `uv` then `pip`,
  `test.yml` ran `pip install pytest pytest-xdist`, and `CONTRIBUTING.md`
  said "The suite needs only `pytest`". 26 committed `routing.md` files,
  counted with `ls seal/specs/*/routing.md`.
- **The pin is `markdown-it-py==4.2.0`**, the newest release on 2026-09-29,
  which needs Python 3.10 or newer (the floor is 3.12) and pulls in `mdurl`
  0.1.2. The pin is written once, `run_tests.py#MARKDOWN_IT_VERSION`, and CI's
  install line and both fallback commands carry the string `MARKDOWN_IT`
  spells, each held by a case.
- **An adopted `.venv` is checked by the versioned `.dist-info` directory,
  not by the `markdown_it` package.** A package-directory marker, which is
  what `has_xdist` uses, passes a `.venv` holding another version, and the
  pin exists so that cannot happen. A failed install does not make the run
  serial; it is a sentence saying the oracle's cases fail at their import.
- **Q2 is answered (a), by execution.** The oracle gives the frame's
  *Renderer* column, turned into hidden lines, on all 32 shapes in
  `tests/block_shapes.py` (C1 to C14 with C7, C9 and C11 in two texts each,
  R1 to R9 with a second R6, and K1 to K7 without the `.py` K6). The frame's
  reading of CommonMark §4.5, §4.6 and §6.6 held on every row, so no
  *Expected* answer is re-derived and `overview.md` records no divergence.
- **Where an inline comment lies is the parser's answer, not this suite's.**
  markdown-it tokens carry no source offsets, and a code span's content has
  its newlines turned into spaces, so counting newlines through the children
  would misplace a comment after a multi-line code span. The oracle wraps the
  parser's own `html_inline` rule and keeps the offsets that rule read at. It
  decides nothing about what a comment is.
- **GFM tables are on.** A table row is its own inline, so a comment cannot
  run across two rows; with CommonMark's paragraphs alone it could. The files
  the hooks read are rendered as GFM, and the case that shows the difference
  went red with tables off.
- **Seen red.** Each new case, by mutation of the unit it pins, with bytes
  restored from memory and caches cleared between runs:
  `PACKAGES` without the parser (2 red), `add_markdown_it` short-circuited
  (5), the marker accepting any version (2), `main` not calling it (5), CI's
  line unpinned (1) or without the parser (1), the old sentence (1), an
  unpinned fallback (1); in the oracle, the offset wrapper removed (2), HTML
  blocks not counted (20), tables off (1), the opening line counted (2), a
  second import (1).
- **Gate lines, drafted for `CONTRIBUTING.md` §*What a change to a gate must
  carry*.** This phase changes no gate. Its failure direction is the suite's:
  a missing parser fails the oracle's cases loudly at import rather than
  skipping them. It asks no question. Platform: the parser is pure Python and
  CI installs it on all three legs; only macOS ran it here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `CONTRIBUTING.md`'s "The suite needs only `pytest`" | the same paragraph, which now names the parser and `MARKDOWN_IT` |
