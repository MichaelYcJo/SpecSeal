#!/usr/bin/env python3
"""seal-stamp — the drawing the broad gate prints when it was earned.

Issue #30 §*What it prints*, redrawn by #717 and #832. A letter: what the
gate read — the tree and its branch, the base and its ref, the work item, the
suite's counts, the ledger's, the steps CI also runs, the rounds
(`broad_gate.panel` owns the list) — written on a parchment sheet, with a wax
disc pressed into the sheet against its right edge and the disc's mark
pressed into the wax. The disc is COMPUTED — `hypot` for its edge — and only
the disc's mark is authored: the owner's chart of the section sign, §, held
below as data (`CHART`, ten rows of seven cells), placed on the disc by two
computed offsets. Four hand-typed discs came before #30's and every one was
lopsided; a circle that is calculated cannot be off centre. #717 took off
the rope ring and the outer red band and pressed the disc's mark in one red
lit from the upper left, and the owner chose that drawing, its colours and
its scale from renderings. #832 replaced #717's chart of a lily, and the
owner chose the § from renderings looked at in their own terminal: a disc
14 cells across and 7 lines, every cell exactly one of four colours — the
ring, the field, the disc's mark and its one-cell shadow — with no blend.

Two forms, one drawing (`compose`). The block form is half-block characters,
the disc in truecolour and the sheet in 256-colour codes, emitted only where
the colour changes (a code per cell was 282 KB for one seal). The letter twin
is the same footprint as letters — the sheet's edge `|`, its top `.---.` and
its bottom `'---'`, the text as itself, `m` the disc's ring, `.` its field
and `Y y` the disc's mark and its shadow — for a console that cannot render
half-blocks, and for `seal-stamp` on a pipe. The twin is chosen when
stdout is not a UTF-8 terminal, or on `--shape`. An agent's report carries
neither: since #400 the gate draws nothing on a pipe.

**The `Stop` hook's message is held under a budget** (#717): the harness
persists a `systemMessage` longer than `MESSAGE_LIMIT` and shows a preview
instead, so `admitted` carries as many of the oldest stamps as fit with
their disc, each at the highest rung of `SCALE_LADDER` the others leave room
for — one rung since #832, 0.90, because the disc has one size — and leaves
the rest for the next `Stop`.
Only one stamp that does not fit with its disc alone is drawn as the sheet
with no disc.

The stamp prints on success only. The failure form, `not_sealed`, is the words
`NOT SEALED`, the branch and the tree, the base's ref and its commit
(`sealed_names`), and the failing checks with their first lines — no drawing,
because a picture that says *sealed* beside a word that says *not* is read
picture first.

**A sealed run is drawn where a person sees it, and that is rarely where it
ran** (#400). The gate draws only on a terminal, and only over a written
cell. A recorded seal on a pipe — which is every sealer's run — writes the
panel's rows to a values file under the git common dir instead, keyed by the
Claude Code session, and
`hooks/sealer-stamp.py` draws each undrawn file once, at the end of that
session's turn. This module owns the file: `write_values`, `read_values`,
`pending` and `claim`. Drawing claims the file first, by renaming it to
`.drawn.json`, so a file is drawn once whoever draws it.

Usage:
  seal-stamp                      the stamp over sample rows, for a person
  seal-stamp --shape              the letter twin
  seal-stamp --scale 0.75         a scale in the band, 0.75 its floor; the
                                  disc is one size at every scale
  seal-stamp --from <file>        a sealed run's values file, drawn once

The gate imports `stamp(rows, scale, shape)`, `not_sealed(tree, base,
failures, branch, ref)`, `sealed_names`, `pick_shape(stream)`,
`is_terminal(stream)` and `write_values`;
the hook imports `pending`, `read_values`, `claim` and `stamp`; and
`.github/scripts/release_seal.py`, which the tag push runs, imports
`compose`, `block` and `DEFAULT_SCALE` to draw a release's seal as a PNG,
one cell to one rectangle (#718). That script is the repository's own and
the plugin ships nothing that runs it. The command
exists so a person can see the drawing without running a gate, and so a
values file no hook drew can still be drawn by hand.

Exit codes: 0 printed · 2 refused — a scale under the floor, an interpreter
under the floor, or a values file that is unreadable or drawn already;
nothing was written on 2.
"""

import argparse
import collections
import json
import math
import os
import re
import sys
import time

# --- the interpreter floor -----------------------------------------------
#
# Copied from `skills/code-review/scripts/round_record.py`, whose comment says
# this block is the spelling to copy. It sits after the imports, uses no syntax
# newer than the interpreter it means to catch, and precedes every other act
# at module level.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "seal-stamp: needs python {floor} or newer, and this is python {found} "
    "at {executable}.\n"
    "Nothing was read and nothing was written.\n"
    "`python3` is not always the newest interpreter installed -- macOS ships "
    "python 3.9 under that name -- so name one explicitly, `python{floor} "
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
)


def below_floor(version=None, executable=None):
    """The sentence for an interpreter under the floor, or None above it."""
    version = tuple(sys.version_info[:3]) if version is None else tuple(version)
    if version[:2] >= FLOOR:
        return None
    return BELOW_FLOOR.format(
        floor=FLOOR_TEXT,
        found=".".join(str(part) for part in version),
        executable=sys.executable if executable is None else executable,
    )


_refusal = below_floor()
if _refusal:
    sys.stderr.write(_refusal + "\n")
    raise SystemExit(2)


# --- the disc's colours --------------------------------------------------
#
# The owner's of 2026-10-07 (#832, `spec.md` decision 4 of work item
# 1791270164), chosen from renderings looked at in their own terminal: `WAX_M`
# the ring, `FIELD` the field — both #717's — `MARK` the disc's mark and
# `MARK_SHADOW` the disc's mark's shadow, one cell down-right of it. Every cell
# of the disc is exactly one of them (`build`); the owner saw a highlight and
# mid tones and refused both. They are truecolour, the one part of the letter
# drawn that way.
WAX_M = (168, 26, 30)
FIELD = (120, 16, 20)
MARK = (240, 130, 118)
MARK_SHADOW = (96, 10, 14)
DISC_COLOURS = (WAX_M, FIELD, MARK, MARK_SHADOW)

# The sheet's colours, as 256-colour codes (#717): the parchment and its
# one-cell edge, the ink, and the red of the `SEALED` title. A code is a
# shorter sequence than a triple, and the sheet is most of the letter's cells.
PARCHMENT = 230  # (255, 255, 215) in the 256-colour cube
SHEET_EDGE = 187  # (215, 215, 175)
INK = 94  # (135, 95, 0)
TITLE = 124  # (175, 0, 0)

# The letter for each disc colour in the twin (#832): `m` the ring and `.`
# the field, as before #717; `Y` the disc's mark and `y` its shadow. Every
# disc cell is exactly one of these colours, so a cell's letter is a lookup
# (`letter_row`).
KEY = {
    WAX_M: "m",
    FIELD: ".",
    MARK: "Y",
    MARK_SHADOW: "y",
}


# #30 §*Size* measured the floor on the lily's chart: at 75 % the lily was
# still legible, at 60 % its band closed up and its foot became a blob, and at
# 50 % it read as a cross. The band stays where #30 put it, 0.75 to 1.0, as
# what a values file and `--scale` may carry: since #832's hand-drawn disc
# the scale no longer sizes the disc, and a scale outside the band is refused
# (`check_scale`) because no gate writes one, not because of what it would
# draw.
SCALE_FLOOR = 0.75
SCALE_CEILING = 1.0
# The scale both commands draw at unless told otherwise (#400 §*The size, and
# why it is 0.90*). Six scales were rendered in colour and looked at by the
# owner before the choice: at 0.90 the disc was then 20 lines against the
# panel's 16, the darkest gold that crowded the lily's foot at 0.95 had
# cleared, the rope settled to two rows, and the highlight still ran the
# centre leaf.
# The trade was the lily's legibility against the two blocks lining up, and
# legibility won. #717 drew the letter at 0.90 again, the owner choosing it
# from renderings at 0.85 and 0.90 with the disc pressed on the sheet; the
# rope this paragraph names is gone. Those readings were of the lily, which
# #832 withdrew. #832 kept 0.90 as the scale a values file carries, and since
# the owner's hand-drawn disc of 2026-10-07 the disc is `DISC_CELLS` across
# at every scale in the band, so the scale sizes nothing: a chart drawn by
# hand has one size.
#
# 0.75 was the other candidate, passed over rather than missed: under #400's
# disc it was the only legal scale where the disc (then 17 lines) and the
# panel ended within one line of each other, and it was the least detail of
# the band.
DEFAULT_SCALE = 0.90

# --- what one hook message may hold (#717) ---------------------------------
#
# The harness writes a `Stop` hook's `systemMessage` longer than this many
# characters to a file and shows the person a 2 KB preview of it, so a stamp
# past it is not seen. Counted in UTF-16 units, the length JavaScript gives a
# string, not as bytes: a character outside the BMP is two, and Python's `str`
# length counts it as one (`admitted` counts it as two). Measured 2026-10-02
# on Claude Code 2.1.287, with a `Stop` hook in a scratch project and one
# headless `claude -p` turn per size: 9,990 and 10,000 characters, and 9,990
# `▀` (29,942 bytes), were shown with nothing written to the session's
# `tool-results/`; 10,001, 10,010 and 12,000 each left a
# `hook-<uuid>-<n>-systemMessage.txt` there. Then, in round 1's fix pass,
# 4,999 U+1D54F (9,998 units) were shown and 5,001 (10,002 units),
# 9,990 and 10,001 were persisted. This project's own sessions had
# bracketed it before the probe: 9,919 shown, 10,090 persisted. The harness
# can move it, and the only sign is a preview on the owner's screen; the same
# hook at two sizes either side of this number is the whole probe again.
MESSAGE_LIMIT = 10000
# What the hook holds its WHOLE message under — every block, every label and
# the blank line between two blocks. The reserve is for what the hook cannot
# see: `hooks/dispatch.py#report` prepends the session's gate-failure report
# to this same message after the hook has printed. The longest report it can
# write, with each exception's type name and each gate's name cut at
# `NAME_CAP` and its text at `MESSAGE_CAP`, is 564 UTF-16 units for one failed
# gate and 972 for two, separator included; a third, at 1,378, would pass the
# limit beside a stamp at the budget (measured 2026-10-03 over
# `dispatch.describe`, every gate this plugin names and three foreign ones,
# in every group it names and a foreign one, at every phase, with every field
# past its cap -- a record an older or newer plugin wrote;
# `tests/test_a_gate_that_fails_says_so.py#longest_report` is the
# measurement). Before #722 the name had no cap, so a class from outside the
# plugin with a long enough name passed the reserve with two gates. The caps
# count the same units, so a name or a text outside the BMP keeps these
# figures: cut by code points, a text gave two gates 1,309 in #717's round 3.
MESSAGE_RESERVE = 1000
MESSAGE_BUDGET = MESSAGE_LIMIT - MESSAGE_RESERVE
# The rungs a block steps down, after the file's own scale; past the last, a
# block that does not fit alone is drawn with no disc (`admitted`). One rung
# since #832: the owner's disc is drawn `DISC_CELLS` across at every scale,
# so there is no smaller disc to step to, and a block that does not fit with
# its disc at 0.90 is the sheet alone. Each rung is inside `check_scale`'s
# band, so a step down cannot be refused.
SCALE_LADDER = (0.90,)

SCALE_REFUSED = (
    "seal-stamp: scale {scale} is under the floor of {floor}. The disc is "
    "drawn at one size whatever the scale, and the band {floor}-{ceiling} is "
    "what a values file and `--scale` may carry (#30 measured the floor). "
    "Nothing was drawn."
)
# NaN is not under the floor and not above the ceiling; it is not on the line
# at all, and telling a reader it is "under the floor of 0.75" sends them to
# raise a number that will fail the same way.
SCALE_NOT_A_NUMBER = (
    "seal-stamp: scale {scale} is not a number, so it is neither inside the "
    "band {floor}-{ceiling} nor outside it. Nothing was drawn."
)
SCALE_TOO_LARGE = (
    "seal-stamp: scale {scale} is above {ceiling}. The disc is drawn at one "
    "size whatever the scale, and the band {floor}-{ceiling} is what a values "
    "file and `--scale` may carry. Nothing was drawn."
)


def check_scale(scale):
    """The refusal for a scale outside the band, or None inside it."""
    # `not (floor <= scale <= ceiling)` rather than two `<`/`>` tests: NaN
    # compares False with everything, so the pair let it through and it
    # failed later inside `stamp` with `cannot convert float NaN to integer`
    # — after every check had run and the cell had been written, and
    # `broad_gate.main` catches `Refused` alone.
    if not (SCALE_FLOOR <= scale <= SCALE_CEILING):
        if scale != scale:  # NaN, and no comparison against it is true
            return SCALE_NOT_A_NUMBER.format(
                scale=scale, floor=SCALE_FLOOR, ceiling=SCALE_CEILING
            )
        band = {"scale": scale, "floor": SCALE_FLOOR, "ceiling": SCALE_CEILING}
        return (SCALE_REFUSED if scale < SCALE_FLOOR else SCALE_TOO_LARGE).format(
            **band
        )
    return None


# The disc's numbers (#832), in cells of the terminal's grid, where a cell is
# one column by one half-row and so square. `DISC_CELLS` is the owner's of
# 2026-10-07: the disc is 14 cells across and so `DISC_LINES` lines tall, at
# every scale, because the disc's mark is a chart drawn by hand for that size
# and a hand-drawn chart has one size. A cell more than `EDGE_INSET` inside
# the radius is on the disc, and one no more than `RING_INSET` inside it is
# the ring.
DISC_CELLS = 14
DISC_LINES = DISC_CELLS // 2
EDGE_INSET = 0.2
RING_INSET = 1.2

# The disc's mark: the owner's chart of the section sign for a disc of
# `DISC_CELLS`, ten rows of seven, `M` a cell of the disc's mark (#832,
# `spec.md` §*Data & interfaces* of work item 1791270164). It is copied
# character for character from the chart the owner chose; it is data, not a
# drawing anybody re-derives, and `build` places it by two computed offsets.
CHART = (
    ".MMMMM.",
    "MM...MM",
    "MM.....",
    ".MMMMM.",
    "MM...MM",
    "MM...MM",
    ".MMMMM.",
    ".....MM",
    "MM...MM",
    ".MMMMM.",
)


def build(scale=1.0):
    """`(w, h, px)` — the disc's width and height in cells, `DISC_CELLS` at
    every scale in the band, and `px(x, y)`, a cell's colour or None.

    The centre is `c = (DISC_CELLS - 1) / 2` on both axes and the radius
    `r = DISC_CELLS / 2`. A cell at distance `d` from the centre is None past
    `r - EDGE_INSET`, the ring `WAX_M` past `r - RING_INSET`, and otherwise
    in the field: `MARK` under an `M` of `CHART` — placed
    `(DISC_CELLS - rows) // 2` rows down and `(DISC_CELLS - columns + 1) //
    2` columns in — then `MARK_SHADOW` where the cell one up-left is under
    an `M`, so the disc is lit from the upper left, then `FIELD`. Every cell
    is exactly one of the four colours (#832, the owner's of 2026-10-07).
    `scale` is checked against the band and sizes nothing."""
    refusal = check_scale(scale)
    if refusal:
        raise ValueError(refusal)
    n = DISC_CELLS
    c, r = (n - 1) / 2, n / 2
    rows, columns = len(CHART), len(CHART[0])
    top, left = (n - rows) // 2, (n - columns + 1) // 2

    def on(x, y):
        gx, gy = x - left, y - top
        return 0 <= gy < rows and 0 <= gx < columns and CHART[gy][gx] == "M"

    def px(x, y):
        if not (0 <= x < n and 0 <= y < n):
            return None
        d = math.hypot(x - c, y - c)
        if d > r - EDGE_INSET:
            return None
        if d > r - RING_INSET:
            return WAX_M
        if on(x, y):
            return MARK
        if on(x - 1, y - 1):
            return MARK_SHADOW
        return FIELD

    return n, n, px


# --- the two row writers -------------------------------------------------
#
# Both walk the same cells, so the two forms have one footprint: one
# character per cell, the block form's a half-block or a space and the twin's
# a letter. A cell is `(top, bottom, text, frame)`: the colours of its two
# halves — a disc colour as a triple, a sheet colour as a 256-colour code, or
# None for nothing — the `(character, colour)` written on it or None, and the
# twin's character for the sheet there or None off it (`compose`).

RESET = "\x1b[0m"


def sgr(ground, colour):
    """A colour sequence: `ground` 38 for the foreground, 48 for the
    background. A triple is truecolour; an int is a 256-colour code (#717)."""
    if isinstance(colour, int):
        return f"\x1b[{ground};5;{colour}m"
    r, g, b = colour
    return f"\x1b[{ground};2;{r};{g};{b}m"


def disc_cells(px, w, y):
    """One line of cells over the disc alone: row `y` on top, `y + 1`
    below, nothing written and no sheet."""
    return [(px(x, y), px(x, y + 1), None, None) for x in range(w)]


def block(cell):
    """`(character, foreground, background)` for one cell of the block form.

    Text is its character in its colour on parchment. A cell nothing covers
    is a bare space. One half outside everything is a half-block in the
    other half's colour with no background; two halves of one colour are a
    space painted that colour; two colours are an upper half-block with the
    bottom one as its background."""
    top, bottom, text, _frame = cell
    if text:
        return text[0], text[1], PARCHMENT
    if top is None and bottom is None:
        return " ", None, None
    if top is None:
        return "▄", bottom, None
    if bottom is None:
        return "▀", top, None
    if top == bottom:
        return " ", None, top
    return "▀", top, bottom


def colour_row(cells):
    """One line of the block form, emitting a colour only where it changes.

    A painted space keeps the foreground it was handed, because it draws
    none. A cell nothing covers resets both, so no colour bleeds past the
    letter, and so does the line's end. Trailing cells nothing covers are
    `compose`'s to leave off; a painted one at the end is the sheet, and it
    is kept with its colour rather than stripped as padding."""
    out, fg, bg = [], None, None
    for cell in cells:
        ch, want_fg, want_bg = block(cell)
        if want_fg is None and want_bg is None:
            if fg is not None or bg is not None:
                out.append(RESET)
                fg = bg = None
            out.append(ch)
            continue
        if want_fg is not None and want_fg != fg:
            out.append(sgr(38, want_fg))
            fg = want_fg
        if want_bg != bg:
            out.append("\x1b[49m" if want_bg is None else sgr(48, want_bg))
            bg = want_bg
        out.append(ch)
    return "".join(out) + (RESET if fg is not None or bg is not None else "")


def letter_row(cells):
    """One line of the letter twin over the same cells: the character
    written there; else the `KEY` letter of the top half's colour, else of
    the bottom half's, so a disc cell overrides the sheet's frame as it
    covers it in colour; else the sheet's own character; else a space. Every
    disc cell is exactly one palette colour (#832), so the letter is a
    lookup."""
    out = []
    for top, bottom, text, frame in cells:
        if text:
            out.append(text[0])
            continue
        out.append(KEY.get(top) or KEY.get(bottom) or frame or " ")
    return "".join(out)


# --- the panel -----------------------------------------------------------

# Wide enough that a value gets `broad_gate.PANEL_VALUE_WIDTH` columns: the
# frame's two edges and the `"  {label:<8} "` prefix's eleven, then 41 (#832,
# phase 5 of work item 1791270164; 36 and 23 before it).
PANEL_WIDTH = 54


def letter(rows, width=PANEL_WIDTH):
    """The panel carrying the stamp's numbers, framed in letters. Nothing
    draws the frame since #717: `compose` takes the inner lines, without the
    frame and without the blank ones, and writes them on the sheet. This is
    still the one place a value's width is decided, which
    `broad_gate.PANEL_VALUE_WIDTH` is measured against.

    `rows` is a list of `(label, value)` pairs with `None` for a blank line,
    so what the stamp reports is data the gate fills rather than a string it
    formats. A pair whose label is `""` is a continuation: its value lands in
    the value column under the row above it. A value longer than the panel is
    cut at the frame, which is why `broad_gate.fit` elides before it does."""
    inner = width - 2
    out = ["." + "-" * inner + ".", "|" + " " * inner + "|"]
    for row in rows:
        if row is None:
            out.append("|" + " " * inner + "|")
            continue
        label, value = row
        out.append("|" + f"  {label:<8} {value}".ljust(inner)[:inner] + "|")
    out.append("|" + " " * inner + "|")
    out.append("'" + "-" * inner + "'")
    return out


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


# --- the letter: the text on a sheet, the disc pressed into it -------------
#
# #717, the owner's choice from rendered prototypes: the panel's text written
# on parchment, the sheet one blank line taller than the text at its top and
# its bottom. #832, the owner's layout of 2026-10-07: the disc stands inside
# the sheet against its right edge, its last line the sheet's second-to-last,
# and the sheet keeps its height and widens to the right to hold it.

# The column the text starts in: the edge, then two cells of parchment. Each
# text line keeps one leading space of `letter`'s, so a label stands four in.
TEXT_LEFT = 3
# Columns the sheet is widened past the first width at which no character
# stands under the disc's square; the disc moves with the right edge, so on
# the line whose text reaches furthest under it this is the number of clear
# cells between the text and the square (#832, the owner's variant 2).
GAP = 3

# `disc` is where the disc's grid stands, `(left, top, w, h)`: `left` and
# `w` in cells, `top` and `h` in half-rows from the letter's first line, or
# None with no disc — what a case reads to find the disc without
# re-deriving the layout (#832).
Letter = collections.namedtuple("Letter", "cells width height disc")


def sheet_text(rows):
    """The lines the sheet carries: `letter`'s inner lines without the
    frame, without every blank one — a `None` row an older values file may
    carry draws no line — and with one of their two leading spaces."""
    inner = [line[1:-1].rstrip() for line in letter(rows)[1:-1]]
    return [t[1:] if t.startswith("  ") else t for t in inner if t.strip()]


def compose(rows, scale):
    """The letter of `rows` as cells (see the writers above), with the
    sheet's own width and height and where the disc stands: `Letter(cells,
    width, height, disc)`.

    The sheet is the text with a blank line above and below it, and its
    right edge two cells past the longest line. The disc at `scale` — None
    leaves it off, which is the last rung `fitted` steps down to — stands
    inside the sheet (#832, the owner's layout of 2026-10-07): its last line
    is the sheet's second-to-last and its last column the one before the
    right edge. The sheet keeps its height, or takes `DISC_LINES + 2` where
    the text is shorter than that, which no gate writes; it widens one
    column at a time until no character stands under the disc's square — its
    `DISC_CELLS` columns on its `DISC_LINES` lines — and then `GAP` columns
    more, the disc moving with the edge. A cell inside the circle is the
    disc's colour; a cell of the square outside it, and every other cell, is
    the sheet's. Nothing stands below or right of the sheet."""
    text = sheet_text(rows)
    lines, longest = len(text), max((len(t) for t in text), default=0)
    width = TEXT_LEFT + longest + 2
    if scale is None:
        n, px = 0, None
        height = lines + 2
    else:
        n, _, px = build(scale)
        height = max(lines + 2, DISC_LINES + 2)
    top = height - 1 - DISC_LINES

    def clear(width):
        """No character under the disc's square, and the square inside the
        sheet's edge. The square runs to the column before the edge, and no
        line reaches past it, so a character at or right of its first column
        is under it."""
        left = width - 1 - n
        if left < 1:
            return False
        for ln in range(top, top + DISC_LINES):
            said = text[ln - 1] if 0 < ln <= lines else ""
            for k, char in enumerate(said):
                if char != " " and TEXT_LEFT + k >= left:
                    return False
        return True

    if px:
        while not clear(width):
            width += 1
        width += GAP
    left = width - 1 - n

    def colour(x, y):
        dx, dy = x - left, y - 2 * top
        on_disc = px(dx, dy) if px and 0 <= dx < n and 0 <= dy < n else None
        if on_disc is not None:
            return on_disc
        return SHEET_EDGE if x in (0, width - 1) else PARCHMENT

    def frame(x, ln):
        side = x in (0, width - 1)
        if ln == 0:
            return "." if side else "-"
        if ln == height - 1:
            return "'" if side else "-"
        return "|" if side else " "

    cells = []
    for ln in range(height):
        said = text[ln - 1] if 0 < ln <= lines else ""
        line = []
        for x in range(width):
            top_half, bottom_half = colour(x, 2 * ln), colour(x, 2 * ln + 1)
            char = None
            if (
                TEXT_LEFT <= x < TEXT_LEFT + len(said)
                and top_half == bottom_half == PARCHMENT
            ):
                # The title is the panel's first row, not a line that reads
                # `SEALED`: keyed on the value, a branch named `SEALED` on a
                # continuation row was inked as a second title (round 1's ⬜ 5).
                ink = TITLE if ln == 1 else INK
                char = (said[x - TEXT_LEFT], ink)
            line.append((top_half, bottom_half, char, frame(x, ln)))
        cells.append(line)
    where = (left, 2 * top, n, n) if px else None
    return Letter(cells, width, height, where)


# --- what the gate calls -------------------------------------------------


def stamp(rows, scale=1.0, shape=False):
    """The lines of the stamp: the letter of `rows` with the disc pressed
    into it (#717, #832). `shape` picks the letter twin. Raises
    `ValueError` with the refusal sentence for a scale outside the band.
    `scale` None is the sheet with no disc, the last rung `fitted` steps
    down to."""
    writer = letter_row if shape else colour_row
    return [writer(line) for line in compose(rows, scale).cells]


def admitted(blocks, budget=MESSAGE_BUDGET):
    """The drawn blocks one `Stop` message carries under `budget`, oldest
    first (#717). `blocks` is `(label, rows, scale)` per values file, oldest
    first; a drawn block is its label and then its block form.

    The owner's rule of 2026-10-02 (`questions.md` Q6), which replaced one
    rung for the whole message: a seal keeps its disc rather than share a
    message without it. So the message carries as many of the oldest blocks
    as fit together WITH the disc, each at the last rung of `SCALE_LADDER`
    or at its own scale where that is lower, and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. Since #832 the ladder
    is one rung, 0.90: the owner's disc is one size at every scale, so a
    block steps from its disc straight to the sheet alone. The blocks past
    those are not drawn here; the hook leaves their files pending, and the
    next `Stop` draws them whole.

    The rung with no disc is for one block alone, the oldest, when it does
    not fit with its disc by itself; it is returned whatever its size, because
    nothing comes after it. So the first block is always drawn and the queue
    cannot stall. A sheet with no disc is about 70 characters a row with its
    colour codes (2,071 for the widest panel this tree can produce, measured
    2026-10-02), its width bounded by `broad_gate.PANEL_VALUE_WIDTH`.

    A size is counted in UTF-16 units, which is what the harness counts
    (`MESSAGE_LIMIT`): a character outside the BMP is two. `budget` is a
    parameter so a case can drive every rung."""

    def drawn(block, rung):
        label, rows, scale = block
        text = "\n".join(
            [label, *stamp(rows, None if rung is None else min(scale, rung))]
        )
        # `surrogatepass`: a values file is JSON, which can carry a lone
        # surrogate, and a size that raised would leave every file pending.
        return text, len(text.encode("utf-16-le", "surrogatepass")) // 2

    def rungs(scale):
        return list(
            dict.fromkeys(min(scale, rung) for rung in (SCALE_CEILING, *SCALE_LADDER))
        )

    floor, used = [], -2
    for block in blocks:
        text, size = drawn(block, SCALE_LADDER[-1])
        if used + 2 + size > budget:
            break
        floor.append((text, size))
        used += 2 + size
    if not floor:
        return [drawn(blocks[0], None)[0]] if blocks else []
    out = []
    for block, (text, size) in zip(blocks[: len(floor)], floor, strict=True):
        rest = used - size
        for rung in rungs(block[2])[:-1]:
            higher, more = drawn(block, rung)
            if rest + more <= budget:
                text, size = higher, more
                break
        out.append(text)
        used = rest + size
    return out


def fitted(blocks, budget=MESSAGE_BUDGET):
    """The message the `Stop` hook prints for `blocks`: `admitted`'s drawn
    blocks joined by a blank line, held under `budget` (#717). The blocks
    past what `admitted` carries are not in it; the hook claims only the
    files whose blocks it holds."""
    return "\n\n".join(admitted(blocks, budget))


# A ref spelled as a commit: what `--base <sha>` resolves to (`sealed_names`).
HEX_REF = re.compile(r"[0-9a-fA-F]{4,40}")


def sealed_names(tree, base, branch=None, ref=None):
    """`<branch> @ <tree> against <ref> @ <base>` — what a `SEALED` line, a
    `NOT SEALED` line and a drawn stamp's label say was sealed (#666).

    A head naming two commits named neither the branch nor the base's ref,
    so a reader matched a stamp to its work by hash alone. One composer for
    the three lines, because two spellings of one sentence drift.

    Two collapses, and each leaves a part out rather than printing it twice:

      - `branch` None — a detached HEAD has no branch, so the tree prints
        alone, with no stray `@`
      - `ref` None, or a ref that is the commit itself — a bare SHA given as
        `--base` resolves to itself, and `1e2bed9 @ 1e2bed9` says one thing
        twice. Read as a ref spelled in hex with either hash a prefix of the
        other, because the caller may have typed forty characters where the
        gate prints eight, and a branch named `b` is not the commit `b1e2…`

    `ref` is the RESOLVED ref (`broad_gate.Base.ref`), the one CI reads, not
    the spelling the caller typed: #423's repair was that a reader can tell
    `origin/<base>` from a local ref a week behind it."""
    named = f"{branch} @ {tree}" if branch else f"{tree}"
    against = f"{base}" if ref_is_commit(ref, base) else f"{ref} @ {base}"
    return f"{named} against {against}"


def ref_is_commit(ref, base):
    """True where `ref` names nothing the commit `base` does not: no ref at
    all, or a ref spelled in hex that `base` begins, or that begins with
    `base`. The one reading of *the ref is the commit*, asked by
    `sealed_names` for the lines and by `broad_gate.panel` for the row under
    `base`, so the two cannot disagree about when a ref is worth printing."""
    base, ref = str(base), ("" if ref is None else str(ref))
    if not ref:
        return True
    return bool(HEX_REF.fullmatch(ref)) and (
        base.startswith(ref) or ref.startswith(base)
    )


def not_sealed(tree, base, failures, branch=None, ref=None):
    """The failure form, as lines: `NOT SEALED <branch> @ <tree> against
    <ref> @ <base>` (`sealed_names`), then each failing check's name with its
    first lines under it. No drawing.

    `failures` is a list of `(name, lines)` — the check that failed and the
    first lines of what it printed, as the gate kept them. `branch` and `ref`
    None leave their half out, which is the line a caller that names neither
    has always got."""
    out = [f"NOT SEALED   {sealed_names(tree, base, branch, ref)}", ""]
    # The widest name present, not a literal 8: `survivors` is nine
    # characters, so that one check's first line sat a column out from every
    # other check's.
    pad = max([len(name) for name, _ in failures] + [8])
    for name, lines in failures:
        lines = list(lines) or ["(no output)"]
        out.append(f"  {name:<{pad}} {lines[0]}")
        out.extend(f"  {'':<{pad}} {line}" for line in lines[1:])
    return out


def pick_shape(stream):
    """True when `stream` gets the letter twin: anything that is not a UTF-8
    terminal. A console on another codepage draws UTF-8 half-blocks as
    mojibake, and a pipe has no terminal to draw colour on, so `seal-stamp`
    on one prints the twin; the gate asks `is_terminal` first and draws
    nothing on a pipe at all (#400). Asked BEFORE the stream is reconfigured to UTF-8 — after
    that call every stream answers `utf-8`, and a cp949 console would get the
    blocks it cannot draw."""
    encoding = (getattr(stream, "encoding", None) or "").lower().replace("-", "")
    if encoding != "utf8":
        return True
    return not is_terminal(stream)


def is_terminal(stream):
    """True when `stream` is a terminal, whatever its encoding.

    The other half of what `pick_shape` used to fold into one answer, split
    out because the gate asks two different questions (#400): whether to
    draw at all — only a terminal has a person in front of it — and, where
    it draws, which form. A cp949 terminal is a terminal that gets letters,
    and a UTF-8 pipe is not a terminal. Asked with `pick_shape`, before the
    streams are reconfigured, so both answers describe the stream as the
    process found it."""
    isatty = getattr(stream, "isatty", None)
    try:
        return bool(isatty and isatty())
    except (ValueError, OSError):
        return False


# --- a sealed run's values, drawn by somebody else -----------------------
#
# The gate's stdout on a sealer's run is a pipe into a report nobody sees
# unfolded (#400), so it writes the run's panel here and a `Stop` hook in the
# session that spawned the sealer draws it. The directory is under the git
# COMMON dir because the sealer's root and that session's cwd are different
# worktrees of one clone, and the common dir is the one place both resolve
# alike. It is keyed by session so that a concurrent session of the same
# clone does not draw, and take, a stamp that is not its own.

VALUES_DIR = "specseal-stamp"
# The key of a run no Claude Code session was found for. No hook reads it;
# `seal-stamp --from` is how such a file is drawn.
NO_SESSION = "none"
PENDING = ".json"
DRAWN = ".drawn.json"

VALUES_UNREADABLE = "seal-stamp: {path} cannot be read ({why}). Nothing was drawn."
VALUES_MALFORMED = (
    "seal-stamp: {path} is not a values file the broad gate wrote: {why}. "
    "Nothing was drawn."
)
VALUES_DRAWN = (
    "seal-stamp: {path} was drawn already, and a sealed run's values are drawn "
    "once. Nothing was drawn; the values stay in {drawn}."
)


def session_key(session):
    """The directory name for `session`: the id's last path part, or
    `NO_SESSION` where there is none. The id names a directory, so a
    separator in a malformed one must not become a path escape."""
    name = os.path.basename(str(session or "").strip())
    return name if name and name not in (".", "..") else NO_SESSION


def values_dir(common, session):
    """Where the runs of `session` wait to be drawn."""
    return os.path.join(common, VALUES_DIR, session_key(session))


def drawn_path(path):
    """The name `path` takes once it has been claimed."""
    stem = path[: -len(PENDING)] if path.endswith(PENDING) else path
    return stem + DRAWN


def write_values(common, session, values, now=None):
    """Write one run's `values` for `session`; returns the file's path.

    Written to a hidden temporary name and renamed into place, so a hook
    listing the directory never reads half a file. The name leads with the
    time in nanoseconds, so a name sort is oldest first. Raises `OSError`
    where the directory cannot be made or the file cannot be written."""
    directory = values_dir(common, session)
    os.makedirs(directory, exist_ok=True)
    moment = time.time_ns() if now is None else now
    name = f"{moment}-{os.path.basename(str(values.get('tree') or 'tree'))}"
    path = os.path.join(directory, name + PENDING)
    temporary = os.path.join(directory, f".{name}.tmp")
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(values, handle)
    os.replace(temporary, path)
    return path


def read_values(path):
    """A values file as the gate wrote it, with each row a `(label, value)`
    pair or None. Raises `ValueError` with the refusal sentence for a file
    that cannot be read or is not in that shape — which covers a scale the
    band refuses too, because `stamp` checks it again when it draws."""
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except OSError as exc:
        raise ValueError(
            VALUES_UNREADABLE.format(path=path, why=exc.strerror or exc)
        ) from exc
    except ValueError as exc:
        raise ValueError(
            VALUES_MALFORMED.format(path=path, why="it is not JSON")
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(VALUES_MALFORMED.format(path=path, why="it is not an object"))
    rows = data.get("rows")
    shaped = isinstance(rows, list) and all(
        row is None
        or (
            isinstance(row, list)
            and len(row) == 2
            and all(isinstance(cell, str) for cell in row)
        )
        for row in rows
    )
    if not shaped:
        raise ValueError(
            VALUES_MALFORMED.format(
                path=path, why="`rows` is not a list of label and value pairs"
            )
        )
    scale = data.get("scale")
    if isinstance(scale, bool) or not isinstance(scale, (int, float)):
        raise ValueError(
            VALUES_MALFORMED.format(path=path, why="`scale` is not a number")
        )
    return {**data, "rows": [None if row is None else tuple(row) for row in rows]}


def pending(directory):
    """The undrawn values files in `directory`, oldest first; empty where
    the directory does not exist."""
    try:
        names = os.listdir(directory)
    except OSError:
        return []
    return sorted(
        os.path.join(directory, name)
        for name in names
        if name.endswith(PENDING)
        and not name.endswith(DRAWN)
        and not name.startswith(".")
    )


def claim(path):
    """Mark `path` drawn by renaming it; the new path, or None where it was
    not there to rename — somebody else claimed it first.

    Called BEFORE anything is printed. Two drawers racing for one file both
    reach `os.replace` and only one finds it, so the file is drawn at most
    once; a crash between the rename and the print loses that one drawing
    rather than repeating it."""
    target = drawn_path(path)
    try:
        os.replace(path, target)
    except OSError:
        return None
    return target


def label(values):
    """The line said above a drawn stamp: what was sealed, and for which
    work item. The harness shows a hook message's first line as a dim label,
    so this is the line that must not be blank.

    A file carrying `branch` — written by a gate that has #666, `null` on a
    detached HEAD — gets the `SEALED` line's own names (`sealed_names`) and
    then ` · #<pr>` where the record named a pull request (#666). **A file
    without the key draws the label it always drew**, `SEALED <tree> against
    <base> · <item>`: the file is written by the gate the TREE ships and read
    by the hook the INSTALLED plugin ships, so a file from an older gate may
    still be pending when a newer hook draws it."""
    item = values.get("item")
    where = f" · {os.path.basename(os.path.normpath(item))}" if item else ""
    if "branch" not in values:
        return f"SEALED {values.get('tree')} against {values.get('base')}{where}"
    pr = values.get("pr")
    names = sealed_names(
        values.get("tree"), values.get("base"), values.get("branch"), values.get("from")
    )
    return f"SEALED {names}{f' · {pr}' if pr else ''}{where}"


# --- a person's command --------------------------------------------------

# Neutral values in the panel's shape, so `seal-stamp` shows a person what the
# gate will print without a gate having run — every row `broad_gate.panel`
# can return, the conditional ones included, in its order. It read `lint
# clean` from #400 to #666, which the real panel's own comment refuses as a
# counterfeit, because nothing held the two lists together; a case in
# `tests/test_the_seal_is_taken_once_by_the_sealer.py` holds the labels
# against `panel`'s now. #717 took the blank row, `chain`, the suite's `exit`
# and the ledger's `drifted` out of it, because `panel` returned none of them.
# Since #832 it carries the blank row, `chain` and the ledger's three counts
# again, in the owner's shapes of 2026-10-07: the ref beside its commit, a
# `✓` on a result row, ` · ` and `→` between parts, a dim `·` before a row
# that is not a pass.
SAMPLE_ROWS = [
    ("SEALED", ""),
    ("tree", "c46fd2d"),
    ("", "feat/12-a-branch"),
    ("base", "1e2bed9  origin/release/next"),
    ("item", "#34 · 1799000000"),
    ("gate", "tree 1.2.3"),
    None,
    ("suite", "✓ 768 passed · 1 skipped"),
    ("ledger", "✓ 187 ok · 0 drifted · 0 broken"),
    ("chain", "✓ exit 0"),
    ("CI also", "· 4 more steps"),
    ("rounds", "3 · capped"),
    ("", "2 deferred → #56"),
]


def main(argv=None, console_wants_letters=None):
    """`console_wants_letters` is `pick_shape` asked of stdout as the process
    found it. `__main__` asks before it reconfigures the streams, because
    `reconfigure` changes the one object `sys.stdout` and `sys.__stdout__`
    both name; a direct call may leave it to be asked here."""
    parser = argparse.ArgumentParser(
        prog="seal-stamp",
        description="Print the sealer's seal — the letter the broad gate stamps.",
    )
    parser.add_argument(
        "--shape", action="store_true", help="the letter twin, whatever the console"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=None,
        help=f"a scale in the band {SCALE_FLOOR}-{SCALE_CEILING}, {DEFAULT_SCALE} "
        "the default, and a values file's own scale with --from; the disc is "
        "one size at every scale",
    )
    parser.add_argument(
        "--from",
        dest="values",
        default=None,
        metavar="FILE",
        help="draw a sealed run's values file, once, instead of the sample",
    )
    args = parser.parse_args(argv)
    if console_wants_letters is None:
        console_wants_letters = pick_shape(sys.stdout)
    shape = args.shape or console_wants_letters
    try:
        if args.values is None:
            scale = DEFAULT_SCALE if args.scale is None else args.scale
            lines = stamp(SAMPLE_ROWS, scale=scale, shape=shape)
        else:
            lines = drawn_from(args.values, args.scale, shape)
    except ValueError as refused:
        sys.stderr.write(str(refused) + "\n")
        return 2
    sys.stdout.write("\n" + "\n".join(lines) + "\n\n")
    return 0


def drawn_from(path, scale, shape):
    """The lines for the values file at `path`, which is claimed before they
    are returned. `scale` None takes the file's own. Raises `ValueError`
    with a refusal for a file drawn already, unreadable, or out of shape —
    and every refusal comes before the claim, so a file refused for its
    content is still there to be drawn once it is repaired."""
    if path.endswith(DRAWN) or (
        not os.path.exists(path) and os.path.exists(drawn_path(path))
    ):
        # The drawn file's own name, where that is what was given:
        # `drawn_path` of it is `X.drawn.drawn.json`, which does not exist,
        # and this is the sentence a person recovers the values from (round
        # 1's 🟡 3).
        drawn = path if path.endswith(DRAWN) else drawn_path(path)
        raise ValueError(VALUES_DRAWN.format(path=path, drawn=drawn))
    values = read_values(path)
    lines = stamp(values["rows"], values["scale"] if scale is None else scale, shape)
    if claim(path) is None:
        raise ValueError(VALUES_DRAWN.format(path=path, drawn=drawn_path(path)))
    return lines


if __name__ == "__main__":
    # Which form, asked of stdout as the process found it. It has to come
    # before the loop below: `reconfigure` puts the stream into UTF-8, and a
    # cp949 console asked afterwards would be handed the blocks it cannot draw.
    _letters = pick_shape(sys.stdout)
    # A console that cannot encode what this prints kills it with stdout
    # empty. `hooks/console.py` owns the reasoning and the three decisions
    # behind these lines.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main(console_wants_letters=_letters))
