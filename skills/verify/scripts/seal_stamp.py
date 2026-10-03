#!/usr/bin/env python3
"""seal-stamp — the drawing the broad gate prints when it was earned.

Issue #30 §*What it prints*, redrawn by #717. A letter: what the gate read —
the tree and its branch, the base and its ref, the work item, the suite's
counts, the ledger's, the steps CI also runs, the rounds (`broad_gate.panel`
owns the list) — written on a parchment sheet, with a wax disc pressed over
the sheet's lower right corner and a fleur-de-lis pressed into the wax. The
disc is COMPUTED — `hypot` for its edge — and only the lily is authored, as a
29x32 counted-stitch chart held below as data. Four hand-typed discs came
before #30's and every one was lopsided; a circle that is calculated cannot
be off centre, and resizing it is one number. #717 took off the rope ring and
the outer red band and pressed the lily in one red lit from the upper left,
and the owner chose that drawing, its colours and its scale from renderings.

Two forms, one drawing (`compose`). The block form is half-block characters,
the disc in truecolour and the sheet in 256-colour codes, emitted only where
the colour changes (a code per cell was 282 KB for one seal). The letter twin
is the same footprint as letters — the sheet's edge `|`, its top `.---.` and
its bottom `'---'`, the text as itself, `m` the wax's edge, `.` the field and
`G Y y` the lily's face, highlight and shadow — for a console that cannot
render half-blocks, and for `seal-stamp` on a pipe. The twin is chosen when
stdout is not a UTF-8 terminal, or on `--shape`. An agent's report carries
neither: since #400 the gate draws nothing on a pipe.

**The `Stop` hook's message is held under a budget** (#717): the harness
persists a `systemMessage` longer than `MESSAGE_LIMIT` and shows a preview
instead, so `admitted` carries as many of the oldest stamps as fit with
their disc, each at the highest rung of `SCALE_LADDER` the others leave room
for, and leaves the rest for the next `Stop`. Only one stamp that does not
fit at 0.75 alone is drawn as the sheet with no disc.

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
  seal-stamp --scale 0.75         the chart shrunk; 0.75 is the floor
  seal-stamp --from <file>        a sealed run's values file, drawn once

The gate imports `stamp(rows, scale, shape)`, `not_sealed(tree, base,
failures, branch, ref)`, `sealed_names`, `pick_shape(stream)`,
`is_terminal(stream)` and `write_values`;
the hook imports `pending`, `read_values`, `claim` and `stamp`. The command
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
# at module level — the chart below is parsed by a call.
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


# --- the chart -----------------------------------------------------------
#
# 29 columns by 32 rows. Traced outside the tree by hand against a
# counted-stitch pattern; this is the only copy. Every letter but `.` is the
# lily since #717, which presses it into the wax in one colour; the letters
# were the golds of #30's drawing (`D` the lily, `R` its highlight, `y` and
# `Y` the band) and are kept, because `shrink` takes the majority letter of
# the stitches a cell covers and the owner's rendering came from this chart.
ART = """
..............D..............
.............DDD.............
.............DRD.............
............DDDRD............
...........DDDDRRD...........
...........DDDDRRD...........
..........DDDDDRRDD..........
.........DDDDDDDRRDD.........
.........DDDDDDDRRDD.........
.........DDDDDDDRRDD.........
.........DDDDDDDRRDD.........
..........DDDDDRRDD..........
..DDDDD....DDDDRRD....DDDDD..
.DDDDDDDDD.DDDDRRD.DDDDDRRDD.
DDDDDDDDDDD.DDDRD.DDDDDDDDRRD
DDDDD...DDD.DDRDD.DDD...DDDRD
DDDD.....DDD.DDD.DDD.....DDRD
DDDD......DD.DDD.DD......DRDD
.DDDD..D...D.DDD.D...D..DDDD.
..DDDDD....yyyyYYY....DDDDD..
..........yyyyyyyyy..........
........D.yDyDDDyDy.D........
.......DD..DyDDDyD..DD.......
......DDD.DD.DDD.DD.DDD......
......DDDDDD.DDD.DDDDDD......
.......DDD..DDDDD..DDD.......
...........DDDDRDD...........
...........DDDDRRD...........
...........DDDDRDD...........
............DDRDD............
.............DDD.............
..............D..............
""".strip("\n").splitlines()

# The disc's colours, chosen by the owner from renderings (#717). The rope
# ring and the outer light-red band are gone, so `WAX_M` is the wax's edge;
# the lily is pressed into the field in one colour, lit from the upper left:
# its highlight where the chart cell up-left of a lily cell is field, its
# shadow where the cell down-right is, and its face everywhere else. They are
# truecolour, the one part of the letter drawn that way.
WAX_M = (168, 26, 30)
FIELD = (120, 16, 20)
LILY_LIGHT = (226, 82, 74)
LILY_SHADOW = (96, 10, 14)
LILY_FACE = (186, 34, 38)
DISC_COLOURS = (WAX_M, FIELD, LILY_LIGHT, LILY_SHADOW, LILY_FACE)
# Where the disc ends, as a fraction of its radius, and where its edge begins.
WAX_EDGE, FIELD_EDGE = 0.84, 0.78

# The sheet's colours, as 256-colour codes (#717): the parchment and its
# one-cell edge, the ink, and the red of the `SEALED` title. A code is a
# shorter sequence than a triple, and the sheet is most of the letter's cells.
PARCHMENT = 230  # (255, 255, 215) in the 256-colour cube
SHEET_EDGE = 187  # (215, 215, 175)
INK = 94  # (135, 95, 0)
TITLE = 124  # (175, 0, 0)

# The letter for each disc colour in the twin. `.` is the field, as it was
# before #717; a cell of the sheet is its own character (`compose`).
KEY = {
    WAX_M: "m",
    FIELD: ".",
    LILY_FACE: "G",
    LILY_LIGHT: "Y",
    LILY_SHADOW: "y",
}

# #30 §*Size*: the chart compresses to 75 % with the lily still legible; at
# 60 % the band closes up and the foot becomes a blob, and at 50 % it reads as
# a cross. Above 1.0 nothing enlarges — the chart is one cell per stitch.
SCALE_FLOOR = 0.75
SCALE_CEILING = 1.0
# The scale both commands draw at unless told otherwise (#400 §*The size, and
# why it is 0.90*). Six scales were rendered in colour and looked at by the
# owner before the choice: at 0.90 the disc is 20 lines against the panel's
# 16, the darkest gold that crowds the lily's foot at 0.95 has cleared, the
# rope settles to two rows, and the highlight still runs the centre leaf.
# The trade was the lily's legibility against the two blocks lining up, and
# legibility won. #717 drew the letter at 0.90 again, the owner choosing it
# from renderings at 0.85 and 0.90 with the disc pressed on the sheet; the
# rope this paragraph names is gone.
#
# 0.75 was the other candidate, passed over rather than missed: it is the only
# legal scale where the disc (17 lines) and the panel end within one line of
# each other, and it is the least detail of the band. Disc height moves in
# whole cells, so a scale is not a continuous dial.
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
# write, with each exception's type name cut at its `NAME_CAP` and its text
# at its `MESSAGE_CAP`, is 559 UTF-16 units for one failed gate and 957 for
# two, separator included; a third, at 1,352, would pass the limit beside a
# stamp at the budget (measured 2026-10-03 over `dispatch.describe`, every
# gate in every group it is in, both phases, with a name and a text at their
# caps; `tests/test_a_gate_that_fails_says_so.py#longest_report` is the
# measurement). Before #722 the name had no cap, so a class from outside the
# plugin with a long enough name passed the reserve with two gates. Both caps
# count the same units, so a name or a text outside the BMP keeps these
# figures: cut by code points, a text gave two gates 1,309 in #717's round 3.
MESSAGE_RESERVE = 1000
MESSAGE_BUDGET = MESSAGE_LIMIT - MESSAGE_RESERVE
# The rungs a block steps down, after the file's own scale; past the last, a
# block that does not fit alone is drawn with no disc (`admitted`). Each rung
# is inside `check_scale`'s band, so a step down cannot be refused.
SCALE_LADDER = (0.90, 0.80, 0.75)

SCALE_REFUSED = (
    "seal-stamp: scale {scale} is under the floor of {floor}; below it the "
    "lily is not legible (#30 measured 0.6 closing the band and 0.5 reading as "
    "a cross). Nothing was drawn."
)
# NaN is not under the floor and not above the ceiling; it is not on the line
# at all, and telling a reader it is "under the floor of 0.75" sends them to
# raise a number that will fail the same way.
SCALE_NOT_A_NUMBER = (
    "seal-stamp: scale {scale} is not a number, so it is neither inside the "
    "band {floor}-{ceiling} nor outside it. Nothing was drawn."
)
SCALE_TOO_LARGE = (
    "seal-stamp: scale {scale} is above {ceiling}; the chart is one cell per "
    "stitch and does not enlarge. Nothing was drawn."
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
        if scale < SCALE_FLOOR:
            return SCALE_REFUSED.format(scale=scale, floor=SCALE_FLOOR)
        return SCALE_TOO_LARGE.format(scale=scale, ceiling=SCALE_CEILING)
    return None


def shrink(art, f):
    """The chart at a fraction of its size: each output cell takes the
    majority colour of the stitches it covers, and stays blank only when all
    of them are blank."""
    if f >= 1.0:
        return art
    h, w = len(art), len(art[0])
    nh, nw = max(1, round(h * f)), max(1, round(w * f))
    out = []
    for y in range(nh):
        row = []
        for x in range(nw):
            x0, x1 = int(x * w / nw), max(int(x * w / nw) + 1, int((x + 1) * w / nw))
            y0, y1 = int(y * h / nh), max(int(y * h / nh) + 1, int((y + 1) * h / nh))
            ink = [
                art[b][a]
                for b in range(y0, y1)
                for a in range(x0, x1)
                if b < h and a < w and art[b][a] != "."
            ]
            # `max(set(ink), …)` iterated a set of strings, whose order moves
            # with PYTHONHASHSEED, so a tie between two chart colours drew
            # differently from one process to the next (round 1's 🟡 6). This
            # module's argument is that a circle that is CALCULATED cannot be
            # off centre, and a calculated circle that is not reproducible
            # gives it back at every scale but 1.0. Highest count, then
            # earliest in the chart — both stable.
            row.append(
                max(dict.fromkeys(ink), key=lambda c: (ink.count(c), -ink.index(c)))
                if ink
                else "."
            )
        out.append("".join(row))
    return out


def build(scale=1.0, margin=0.74):
    """`(w, h, px)` — the disc's width and height in cells, and a function
    from a cell to its colour, `None` outside the disc.

    The radius is the chart's reach from its centre over `margin`, so the lily
    fills the field and the wax is drawn around it: nothing past `WAX_EDGE`,
    the wax's edge from `FIELD_EDGE`, the field and the lily inside, the lily
    in the three colours its neighbours decide (#717). The grid keeps the size
    #30's rope gave it, so a scale is the same footprint it was; the cells
    past the wax's edge are outside the disc. `h` is even, because the block
    form prints two cells per line."""
    refusal = check_scale(scale)
    if refusal:
        raise ValueError(refusal)
    art = shrink(ART, scale)
    fh, fw = len(art), len(art[0])
    cx, cy = (fw - 1) / 2, (fh - 1) / 2
    reach = max(
        math.hypot(x - cx, y - cy)
        for y in range(fh)
        for x in range(fw)
        if art[y][x] != "."
    )
    r0 = reach / margin
    w = int(r0 * 2) + 2
    h = w + (w % 2)
    ox, oy = w / 2, h / 2

    def chart(dx, dy):
        # `floor`, not `int`: `int` truncates toward zero, so the cell just
        # outside the chart's top-left would read stitch 0 a second time.
        fx, fy = math.floor(dx + fw / 2), math.floor(dy + fh / 2)
        return art[fy][fx] if 0 <= fy < fh and 0 <= fx < fw else "."

    def px(x, y):
        # Sampled at the cell's centre. Sampled at its corner, the disc sat
        # half a cell right and half a cell down of the grid's centre — the
        # top rope row came out six cells wider than the bottom one — which is
        # the lopsidedness a computed circle is supposed to make impossible.
        dx, dy = x + 0.5 - ox, y + 0.5 - oy
        r = math.hypot(dx, dy) / r0
        if r > WAX_EDGE:
            return None
        if r > FIELD_EDGE:
            return WAX_M
        if chart(dx, dy) == ".":
            return FIELD
        if chart(dx - 1, dy - 1) == ".":
            return LILY_LIGHT
        if chart(dx + 1, dy + 1) == ".":
            return LILY_SHADOW
        return LILY_FACE

    return w, h, px


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
    written there; else the disc's letter for whichever half is the disc's,
    the top first, so a disc cell overrides the sheet's frame as it covers it
    in colour; else the sheet's own character; else a space."""
    out = []
    for top, bottom, text, frame in cells:
        if text:
            out.append(text[0])
        elif top in KEY:
            out.append(KEY[top])
        elif bottom in KEY:
            out.append(KEY[bottom])
        else:
            out.append(frame or " ")
    return "".join(out)


# --- the panel -----------------------------------------------------------

PANEL_WIDTH = 36


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


# --- the letter: the text on a sheet, the disc pressed on its corner -------
#
# #717, the owner's choice from rendered prototypes: the panel's text written
# on parchment, the sheet one blank line taller than the text at its top and
# its bottom, and the disc pressed over the sheet's lower right corner, half
# of it hanging below the last line and, where the disc sets the width, half
# over the right edge.

# The column the text starts in: the edge, then two cells of parchment. Each
# text line keeps one leading space of `letter`'s, so a label stands four in.
TEXT_LEFT = 3
# Clear parchment cells between the last character of a text line and the
# wax on that line. The prototype asked for two and looked for them on the
# disc's equator alone, so its rendering showed wax touching the text on one
# row; two on every line is the prototype's intent (`spec.md` S3).
GAP = 2

Letter = collections.namedtuple("Letter", "cells width height")


def sheet_text(rows):
    """The lines the sheet carries: `letter`'s inner lines without the
    frame, without every blank one — a `None` row an older values file may
    carry draws no line — and with one of their two leading spaces."""
    inner = [line[1:-1].rstrip() for line in letter(rows)[1:-1]]
    return [t[1:] if t.startswith("  ") else t for t in inner if t.strip()]


def compose(rows, scale):
    """The letter of `rows` as cells (see the writers above), with the
    sheet's own width and height: `Letter(cells, width, height)`.

    The disc at `scale` — None leaves it off, which is the last rung
    `fitted` steps down to — stands with its centre line on the sheet's last
    line and as far left as it can without covering a text cell or leaving
    fewer than `GAP` clear cells after any line's last character. The
    sheet's right edge is at the disc's centre column, or two cells past the
    longest line where the text is wider, and its first and last lines are
    blank. Lines end at their last cell something covers."""
    text = sheet_text(rows)
    lines, longest = len(text), max((len(t) for t in text), default=0)
    if scale is None:
        dw = dh = 0
        px = None
    else:
        dw, dh, px = build(scale)
    height = lines + 2
    disc_lines = dh // 2
    disc_top = max(1, height - disc_lines // 2 - 1)

    def disc(left, x, y):
        dx, dy = x - left, y - 2 * disc_top
        return px(dx, dy) if px and 0 <= dx < dw and 0 <= dy < dh else None

    def covered(left):
        for k, said in enumerate(text, 1):
            for x in range(TEXT_LEFT, TEXT_LEFT + len(said) + GAP):
                if disc(left, x, 2 * k) or disc(left, x, 2 * k + 1):
                    return True
        return False

    left = TEXT_LEFT
    while px and covered(left):
        left += 1
    width = max(TEXT_LEFT + longest + 2, left + dw // 2)

    def colour(x, y):
        on_disc = disc(left, x, y)
        if on_disc:
            return on_disc
        if y >= 2 * height or x >= width:
            return None
        return SHEET_EDGE if x in (0, width - 1) else PARCHMENT

    def frame(x, ln):
        if ln >= height or x >= width:
            return None
        side = x in (0, width - 1)
        if ln == 0:
            return "." if side else "-"
        if ln == height - 1:
            return "'" if side else "-"
        return "|" if side else " "

    cells = []
    for ln in range(max(height, disc_top + disc_lines)):
        said = text[ln - 1] if 0 < ln <= lines else ""
        line = []
        for x in range(max(width, left + dw)):
            top, bottom = colour(x, 2 * ln), colour(x, 2 * ln + 1)
            char = None
            if TEXT_LEFT <= x < TEXT_LEFT + len(said) and top == bottom == PARCHMENT:
                # The title is the panel's first row, not a line that reads
                # `SEALED`: keyed on the value, a branch named `SEALED` on a
                # continuation row was inked as a second title (round 1's ⬜ 5).
                ink = TITLE if ln == 1 else INK
                char = (said[x - TEXT_LEFT], ink)
            line.append((top, bottom, char, frame(x, ln)))
        while line and line[-1][0] is None and line[-1][1] is None:
            line.pop()
        cells.append(line)
    # The disc's grid keeps the rows #30's rope needed, and below the wax
    # they are empty; a line that carries nothing is not part of the letter.
    while cells and not cells[-1]:
        cells.pop()
    return Letter(cells, width, height)


# --- what the gate calls -------------------------------------------------


def stamp(rows, scale=1.0, shape=False):
    """The lines of the stamp: the letter of `rows` with the disc at `scale`
    pressed on its corner (#717). `shape` picks the letter twin. Raises
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
    as fit together WITH the disc, each at 0.75 — a scale below it is
    refused before a block reaches here — and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. The blocks past
    those are not drawn here; the hook leaves their files pending, and the
    next `Stop` draws them whole.

    The rung with no disc is for one block alone, the oldest, when it does
    not fit at 0.75 by itself; it is returned whatever its size, because
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
# against `panel`'s now. Since #717 there is no blank row in it, no `chain`,
# no `exit` under the suite and no `drifted` under the ledger, because
# `panel` returns none of them.
SAMPLE_ROWS = [
    ("SEALED", ""),
    ("tree", "c46fd2d"),
    ("", "feat/12-a-branch"),
    ("base", "1e2bed9"),
    ("", "origin/release/next"),
    ("item", "#34 . 1799000000"),
    ("gate", "tree 1.2.3"),
    ("suite", "768 passed, 1 skipped"),
    ("ledger", "187 ok"),
    ("CI also", "4 more steps"),
    ("rounds", "3 . capped"),
    ("", "2 deferred -> #56"),
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
        help=f"the chart's scale; {SCALE_FLOOR} is the floor, {SCALE_CEILING} the "
        f"size, {DEFAULT_SCALE} the default, and a values file's own scale with "
        "--from",
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
