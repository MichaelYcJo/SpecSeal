# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c9cd1bde |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The renderer's PNG and its pin. `release_seal.py` with `rgb`, `paint`,
`font` and `png`. `PILLOW = "pillow==12.3.0"` in `run_tests.py#PACKAGES`,
with the adopted-`.venv` top-up. The same string in `test.yml` and
`CONTRIBUTING.md`'s fallback. The holding cases extended. `seal_stamp.py`'s
docstring names the new importer. Cases S6, S7 and S16: the
`paint`-against-`block` case runs without Pillow, the pixel case decodes a
PNG drawn from the fixed rows, and both are seen red by swapping two codes
in `rgb`.

## What this phase found

**The frame holds for this phase, with two corrections.**

- **The frame's ink check could not see a wrong ink.** S6 asks that in
  every text cell the darkest pixel be nearer the ink than the parchment.
  Swapping 95 and 135 in `CUBE_LEVELS` changes exactly one sheet colour,
  `INK` (94), from (135, 95, 0) to (95, 135, 0), and that check stayed green
  (`bin/mutation-check`, SURVIVED). A probe over every glyph cell found that
  each holds at least one pixel of exactly its ink, in Menlo and in Pillow's
  default alike, so the case now asks for that. The same swap then goes red,
  and so does a swap of 215 and 255, which moves the parchment and the edge.
- **A spec claim about the font is now pinned instead of assumed.** S6
  says the pin samples colours away from the glyphs, *so it holds for any
  font*. The pixel case runs twice, once over the face chain (Menlo here)
  and once with `FACES` emptied, so Pillow's default is drawn and held to the
  same samples. Pillow's default is proportional, not monospace, and it
  passes: no glyph reaches a half's outer row at the centre column.

**Settled while building.**

- **Every rectangle starts and ends on a half's edge.** The stdlib case
  refuses any rectangle that does not, and the pixel case samples each
  half's inner row where no glyph is. Before that, an upper half one pixel
  row long survived both cases, because integer division mapped it to the
  same half.
- **Pillow's dist-info is lower case.** Pillow 12.3.0, installed in a
  scratch virtualenv on 2026-10-03, writes `pillow-12.3.0.dist-info`.
  `has_pillow` looks for that name. The mutation to `Pillow-` survives on
  this machine only because APFS is case-insensitive by default.
- **A written space draws nothing.** `compose` writes the whole text run
  of a line, spaces included, as text cells. `paint` lays the parchment
  under them and draws no glyph for a space.
- **The version timer refuses `12.3.0` in `CONTRIBUTING.md`.** It treats a
  version above the running one as a timer, so `tests/test_release_hygiene.py`
  gains a `VERSIONS_OF_ANOTHER_PRODUCT` row for it beside the parser's
  `4.2.0`. Seen red by moving the row's key to `12.3.1`.
- **`__doc__` and source disagree on 3.13.** This was recorded in phase 1.
  It is the reason no case here reads a docstring through `__doc__`.

**Verified.**

- Red first (executed): the four seal cases failed before the module
  existed. The extended pin cases failed before `PILLOW_VERSION` existed.
- Mutations through `bin/mutation-check` (executed). In `release_seal.py`,
  each of these went red: the cube's 95 and 135 swapped, against the stdlib
  case alone and against the pixel case alone; 215 and 255 swapped; the
  middle index `% 5`; the grey step 11; bold on line 0; the upper half one row
  long; the lower half one row long; the text one cell right; the background
  removed; the text anchor `la`; the background opaque; the grey ramp read for
  every code. In `run_tests.py`, each of these went red: `main` skipping
  `add_pillow`; `PILLOW` out of `PACKAGES`; a failed install read as success.
  `Pillow-` for `pillow-` survived, and is equivalent on this machine.
- The 34 modules that read `run_tests.py`, `test.yml`, `CONTRIBUTING.md`,
  `seal_stamp.py` or `release_seal.py` (executed): `bin/test <34> -q` gave
  2140 passed and 1 failed. The failure was
  `test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
  for this work item, which had no `overview.md` yet. It has one from phase 3.
- `uvx ruff check` and `uvx ruff format --check` on the touched files
  (executed): clean.

**Ledger.** R1–R3 are in the fragment. Rows that cite `run_tests.py#PACKAGES`,
`#main`, `CONTRIBUTING.md` §*Running the checks* and three of the extended
cases are re-read and stamped in place: `0.8.2.md` R1, R3 and R4; `0.10.0.md`
S1; `0.15.1.md` P1–P3; `0.15.3.md` A6. `0.16.0.md` P1-1 is corrected in place,
because *the suite's one test-only package* stopped being true.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
