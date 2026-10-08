#!/usr/bin/env python3
"""seal-stamp — the drawing the broad gate prints when it was earned.

Issue #30 §*What it prints*, redrawn by #717 and #832. Two things side by
side on the terminal's own background, and nothing else: at the left a wax
disc with the disc's mark pressed into it, and three columns right of it
the panel's text — a bold red `SEALED` and a dim rule, then what the gate
read: the tree and its branch, the base and its ref, the work item, the
suite's counts, the ledger's, the chain's exit, the steps CI also runs, the
rounds (`broad_gate.panel` owns the list). The disc is COMPUTED — `hypot`
for its edge, its rim and its groove — and only the disc's mark is
authored: a 28 x 28 chart in `seal-mark.txt` beside this file, read as data
(`read_chart`). Four hand-typed discs came before #30's and every one was
lopsided; a circle that is calculated cannot be off centre. #832's owner
settled the frame on 2026-10-07 — 28 cells across and 14 lines, a wax edge,
a rim lit from the upper left in three steps and a groove lit the other way,
every cell exactly one of nine colours — and left the disc's mark a
placeholder S until #857 chooses one: changing it is changing that file
alone. The same day the owner retired the parchment sheet #717 wrote the
text on, so nothing outside the disc is painted and the stamp reads in the
terminal's own theme.

Two forms, one drawing (`compose`). The block form is half-block characters,
the disc in truecolour and the text in the terminal's own colours and
styles, and it writes a code only where the colour or the style changes:
one SGR per change and no reset inside a line (a code per cell was 282 KB
for one seal). The letter twin is the same footprint as letters — `KEY`
for the disc, `m` its wax edge, `M n N` its rim lit, mid and dark, `.` its
field, `X Y x` the disc's mark's face, highlight and inner shadow and `y`
its drop shadow; the text as itself, with the owner's `·`, `✓`, `─` and
`→` written `.`, `+`, `-` and `>` — for a console that cannot render
half-blocks, and for `seal-stamp` on a pipe. The twin is chosen when
stdout is not a UTF-8 terminal, or on `--shape`. An agent's report carries
neither: since #400 the gate draws nothing on a pipe.

**The `Stop` hook's message is held under a budget** (#717): the harness
persists a `systemMessage` longer than `MESSAGE_LIMIT` and shows a preview
instead, so `admitted` carries as many of the oldest stamps as fit with
their disc and leaves the rest for the next `Stop`. Only one stamp that does
not fit with its disc alone is drawn as the text block with no disc.

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
  seal-stamp --from <file>        a sealed run's values file, drawn once

The gate imports `stamp(rows, shape)`, `not_sealed(tree, base,
failures, branch, ref)`, `sealed_names`, `pick_shape(stream)`,
`is_terminal(stream)` and `write_values`;
the hook imports `pending`, `read_values`, `claim` and `stamp`.
`.github/scripts/release_seal.py`, which the tag push runs, drew a
release's seal from this module's cells as a PNG, one cell to one rectangle
(#718), until #832 drew it from the owner's SVG instead. That script is the
repository's own and the plugin ships nothing that runs it. The command
exists so a person can see the drawing without running a gate, and so a
values file no hook drew can still be drawn by hand.

Exit codes: 0 printed · 2 refused — an interpreter under the floor, or a
values file that is unreadable or drawn already; nothing was written on 2.
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
# The owner's frame of 2026-10-07 (#832, `spec.md` decision 5 of work item
# 1791270164), named as the owner's `seal28.py` names them: `WAX_EDGE`; the
# rim, lit from the upper left in three steps, `RIM_LIT`, `RIM_MID` and
# `RIM_DARK`, whose lit and dark the groove inside it takes the other way
# round; `FIELD`; and the disc's mark in the red lily's three tones — `FACE`,
# `LIGHT` where the cell up-left of the disc's mark is the field, `INNER`
# where the cell down-right is — with `DROP`, the shadow the disc's mark
# casts on the field down-right of it. No mid tones and no blend: every
# cell of the disc is exactly one of these nine (`build`), and with
# `TITLE_RED` they are the only colours the stamp sets.
WAX_EDGE = (150, 24, 28)
RIM_LIT = (208, 68, 64)
RIM_MID = (160, 30, 34)
RIM_DARK = (96, 10, 14)
FIELD = (112, 16, 20)
FACE = (186, 38, 42)
LIGHT = (222, 86, 78)
INNER = (90, 8, 12)
DROP = (84, 8, 12)
DISC_COLOURS = (WAX_EDGE, RIM_LIT, RIM_MID, RIM_DARK, FIELD, FACE, LIGHT, INNER, DROP)

# `SEALED` is bold and in this red, the owner's `frames.py`'s `RED`. The rest
# of the text is in the terminal's own colours (`STYLE_CODES`), since #832
# retired the parchment sheet and its four 256-colour codes.
TITLE_RED = (196, 40, 44)

# The letter for each disc colour in the twin (#832): capitals lit and lower
# case shadow — `m` the wax edge and `.` the field, as #30 had them; `M n N`
# the rim lit, mid and dark; `X` the disc's mark's face, and `Y` and `y` its
# highlight and its drop shadow, as #717 had them; `x` its inner shadow. The
# framer chose them (`spec.md` §*Data & interfaces*): the twin is for a
# console that cannot draw half-blocks, and no decision of the owner's names
# its letters. Every disc cell is exactly one of these colours, so a cell's
# letter is a lookup (`letter_row`).
KEY = {
    WAX_EDGE: "m",
    RIM_LIT: "M",
    RIM_MID: "n",
    RIM_DARK: "N",
    FIELD: ".",
    FACE: "X",
    LIGHT: "Y",
    INNER: "x",
    DROP: "y",
}


# There is no scale (#853). #30 measured a band of them, 0.75 to 1.0, on the
# lily's chart, #400 chose 0.90 and #717 drew the letter at it; since #832's
# disc of 2026-10-07 the disc is `DISC_CELLS` across whatever a scale said,
# because the disc's mark is a chart and a chart has one size. The band, its
# refusals, `--scale` on both commands and the values file's `scale` field
# were a dial that turned nothing, and they went together.

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


# The disc's numbers (#832), in cells of the terminal's grid, where a cell is
# one column by one half-row and so square. The owner's frame of 2026-10-07:
# the disc is 28 cells across and so `DISC_LINES` lines tall, because the
# disc's mark is a chart drawn for that grid and a chart has one size. Measured inward from the radius, a cell more than `EDGE_INSET` inside
# it is on the disc; one no more than `WAX_INSET` inside it is the wax edge,
# no more than `RIM_INSET` the rim, no more than `GROOVE_INSET` the groove,
# and the rest the field. `LIT_AT` is where the rim turns from mid to lit on
# one side and to dark on the other.
DISC_CELLS = 28
DISC_LINES = DISC_CELLS // 2
EDGE_INSET = 0.2
WAX_INSET = 1.2
RIM_INSET = 3.2
GROOVE_INSET = 4.2
LIT_AT = 0.35

# The disc's mark (#832): one chart in a file beside this one, `DISC_CELLS`
# lines of `DISC_CELLS` characters over `.M`, `M` a cell of the disc's mark.
# It is the owner's placeholder S, Georgia Bold fitted to the grid, until
# #857 chooses the stamp's mark for good — and changing the disc's mark is
# replacing that file and nothing else, which is why it is data read here
# rather than a tuple typed into this module. A candidate in
# `assets/seals/candidates/` is the same `.M` text.
CHART_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seal-mark.txt")
CHART_MALFORMED = (
    "seal-stamp: the disc's mark chart {path} is not {n} lines of {n} "
    "characters over `.M` with every `M` inside the disc's field ({fault}). "
    "Nothing was drawn."
)


def read_chart(path):
    """The chart at `path` as a tuple of its lines, or `ValueError` with
    `CHART_MALFORMED` naming the path and the first fault: a count of lines
    that is not `DISC_CELLS`, a line of another length, a character outside
    `.M`, or an `M` outside the field — more than `GROOVE_INSET` short of
    the radius, where `build` would draw the rim over it and the disc's mark
    would lose a cell nobody sees go. `utf-8-sig` reads a chart an editor
    saved with a byte-order mark as the same chart, rather than refusing its
    first line as one character too long."""
    with open(path, encoding="utf-8-sig") as handle:
        lines = handle.read().splitlines()
    n = DISC_CELLS
    c, field = (n - 1) / 2, n / 2 - GROOVE_INSET
    fault = None if len(lines) == n else f"{len(lines)} lines"
    for y, line in enumerate(lines):
        if fault:
            break
        stray = sorted(set(line) - set(".M"))
        outside = [
            x
            for x, char in enumerate(line)
            if char == "M" and math.hypot(x - c, y - c) > field
        ]
        if len(line) != n:
            fault = f"line {y + 1} is {len(line)} characters"
        elif stray:
            fault = f"line {y + 1} carries {stray[0]!r}"
        elif outside:
            fault = f"line {y + 1} marks column {outside[0] + 1}, outside the field"
    if fault:
        raise ValueError(CHART_MALFORMED.format(path=path, n=n, fault=fault))
    return tuple(lines)


CHART = read_chart(CHART_PATH)


def build():
    """`(w, h, px)` — the disc's width and height in cells, `DISC_CELLS`
    each, and `px(x, y)`, a cell's colour or None.

    The centre is `c = (DISC_CELLS - 1) / 2` on both axes and the radius
    `r = DISC_CELLS / 2`. A cell `dx, dy` from the centre at distance `d` is,
    from the outside in: None past `r - EDGE_INSET`; `WAX_EDGE` past
    `r - WAX_INSET`; the rim past `r - RIM_INSET` — `RIM_LIT` where `lit =
    (dx + dy) / (|dx| + |dy|)` is under `-LIT_AT`, `RIM_DARK` where it is
    over `LIT_AT`, `RIM_MID` between, `lit` being -1 at the upper left and
    +1 at the lower right; the groove past `r - GROOVE_INSET`, lit the
    other way — `RIM_DARK` where `lit` is under 0, else `RIM_LIT`; then the
    field. In the field a cell under an `M` of `CHART` is `LIGHT` where the
    cell up-left is not under one, else `INNER` where the cell down-right is
    not, else `FACE`; a cell not under one whose up-left is, is `DROP`; the
    rest are `FIELD`. Every cell is exactly one of the nine colours (#832,
    the owner's frame of 2026-10-07). `lit` is read only past the groove's
    inner edge, where `d` is never 0, so it needs no guard."""
    n = DISC_CELLS
    c, r = (n - 1) / 2, n / 2

    def on(x, y):
        return 0 <= x < n and 0 <= y < n and CHART[y][x] == "M"

    def px(x, y):
        if not (0 <= x < n and 0 <= y < n):
            return None
        dx, dy = x - c, y - c
        d = math.hypot(dx, dy)
        if d > r - EDGE_INSET:
            return None
        if d > r - WAX_INSET:
            return WAX_EDGE
        if d > r - GROOVE_INSET:
            lit = (dx + dy) / (abs(dx) + abs(dy))
            if d <= r - RIM_INSET:
                return RIM_DARK if lit < 0 else RIM_LIT
            if lit < -LIT_AT:
                return RIM_LIT
            return RIM_DARK if lit > LIT_AT else RIM_MID
        if on(x, y):
            if not on(x - 1, y - 1):
                return LIGHT
            return INNER if not on(x + 1, y + 1) else FACE
        return DROP if on(x - 1, y - 1) else FIELD

    return n, n, px


# --- the two row writers -------------------------------------------------
#
# Both walk the same cells, so the two forms have one footprint: one
# character per cell. A cell is `(char, fg, bg, style)` (#832): the
# character, or None for an empty cell; `fg` and `bg` a triple — one of the
# disc's colours or `TITLE_RED` — or None for the terminal's own; `style`
# None, `"dim"`, `"bold"` or `"green"`. A disc cell is `▀` with its top
# half's colour as the foreground and its bottom half's as the background,
# or `▄` in its bottom half's colour where the top half is off the disc.
# Nothing but a disc cell has a background.

RESET = "\x1b[0m"
EMPTY = (None, None, None, None)
HALF_BLOCKS = ("▀", "▄")
# The code each text style is written as: the terminal's own dim, bold and
# green. `22;39` ends any of them — 22 the intensity, 39 the foreground,
# which the green set.
STYLE_CODES = {"dim": "2", "bold": "1", "green": "32"}
# The owner's characters the letter twin writes in ASCII, one for one, so a
# console that is not UTF-8 is handed a printable line as wide as the block
# form's (#832).
TWIN_ASCII = {"·": ".", "✓": "+", "─": "-", "→": ">"}


def disc_cell(top, bottom):
    """The cell over two half-rows of the disc, `top` and `bottom` each a
    colour or None."""
    if top and bottom:
        return ("▀", top, bottom, None)
    if top:
        return ("▀", top, None, None)
    if bottom:
        return ("▄", bottom, None, None)
    return EMPTY


def disc_cells(px, w, y):
    """One line of cells over the disc alone: row `y` on top, `y + 1`
    below."""
    return [disc_cell(px(x, y), px(x, y + 1)) for x in range(w)]


def colour_code(ground, colour):
    """One colour's part of an SGR: `ground` 38 for the foreground, 48 for
    the background; a triple is truecolour, None the terminal's own."""
    if colour is None:
        return "39" if ground == 38 else "49"
    r, g, b = colour
    return f"{ground};2;{r};{g};{b}"


def colour_row(cells):
    """One line of the block form, lean (#832, `spec.md` S11, after the
    owner's `frames.py#encode`). A code only where the next visible cell's
    foreground, background or style differs from what is set; every part of
    that change in one SGR; no reset inside the line, and `RESET` at its end
    where it wrote a code. An empty cell or a space — no space carries a
    background, because only a disc cell has one — is written as a space
    that keeps the foreground and the style as they are set, since a space
    shows neither; but a background would paint it, so one still set from
    the disc ends there with `49`. A style that ends is written `22;39`
    first, which takes the foreground back to the terminal's own as well, so
    `39` is not written a second time in the same SGR. A green cell writes no
    foreground part: `32` is its colour, and a `39` after it in the same SGR
    would take the green back off — which a tick leading a `""` row beside
    the disc met, the disc's colour being still set across the label's
    spaces."""
    out, state, wrote = [], (None, None, None), False
    for char, fg, bg, style in cells:
        if char in (None, " "):
            char, fg, style = " ", state[0], state[2]
        if (fg, bg, style) != state:
            parts, shown = [], state[0]
            if style != state[2]:
                if state[2]:
                    parts.append("22;39")
                    shown = None
                if style:
                    parts.append(STYLE_CODES[style])
            if fg != shown and style != "green":
                parts.append(colour_code(38, fg))
            if bg != state[1]:
                parts.append(colour_code(48, bg))
            out.append(f"\x1b[{';'.join(parts)}m")
            wrote = True
            state = (fg, bg, style)
        out.append(char)
    return "".join(out) + (RESET if wrote else "")


def letter_row(cells):
    """One line of the letter twin over the same cells (#832, `spec.md`
    S4): a half-block's `KEY` letter — its foreground's, which is the top
    half's colour on `▀` and the bottom half's on `▄` — the text's own
    character with `TWIN_ASCII` applied, and a space for an empty cell.
    Every disc cell is exactly one palette colour, so the letter is a
    lookup. A cell is the disc's by its colour, never by its character: a
    value may carry `▀` or `▄` — a branch name can — and that is text,
    written as itself."""
    out = []
    for char, fg, _bg, _style in cells:
        if char in HALF_BLOCKS and fg in KEY:
            out.append(KEY[fg])
        else:
            out.append(TWIN_ASCII.get(char, char or " "))
    return "".join(out)


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


# --- the stamp: the disc at the left, the text block at the right ---------
#
# #832, the owner's layout of 2026-10-07 (`spec.md` decision 6 of work item
# 1791270164, the owner's `frames.py#design_open`): no parchment, no edge, no
# frame and no background outside the disc, the text in the terminal's own
# colours. #717's sheet, which the text was written on, is retired.

# The columns a label is padded to before the one space ahead of its value:
# the owner's seven, which `CI also` fills.
LABEL_WIDTH = 7
# The dim `─` rule after the title: the owner's reference's thirty.
RULE_WIDTH = 30
# The panel's first row, which is drawn as the title rather than as a row.
TITLE_ROW = ("SEALED", "")
# The mark that leads a value and the style it is drawn in: a result row
# that passed, green, and a row that is not a pass, dim (#832).
VALUE_MARKS = {"✓": "green", "·": "dim"}
# The clear columns between the disc's last column and the text block's
# first (#832, the owner's three).
GAP = 3

# `disc` is where the disc's grid stands, `(left, top, w, h)`: `left` and
# `w` in cells, `top` and `h` in half-rows from the stamp's first line, or
# None with no disc — what a case reads to find the disc without
# re-deriving the layout (#832).
Letter = collections.namedtuple("Letter", "cells width height disc")


def text_cells(text, style=None, fg=None):
    """`text` as cells in one style and foreground, with no background."""
    return [(char, fg, None, style) for char in text]


def text_lines(rows):
    """The text block of `rows`, as lines of cells (#832, `spec.md` S3a).

    Where the first row is the panel's title row, `("SEALED", "")`, the
    first line is `SEALED ` bold in `TITLE_RED` and a dim rule of
    `RULE_WIDTH` `─`, and the second is blank; rows without it draw no
    title. Then one line per row: the label padded to `LABEL_WIDTH` and a
    space, dim, and the value in the terminal's own foreground — a leading
    `✓ ` with the `✓` green, a leading `· ` with the `·` dim. A `None` row
    is a blank line; a `""` label is seven spaces and one, so its value
    stands under the value above it. The rows are drawn as given:
    `broad_gate.panel` owns their shape, and a values file an older gate
    wrote draws its older rows in this layout."""
    rows, lines = list(rows), []
    if rows and rows[0] is not None and tuple(rows[0]) == TITLE_ROW:
        title = text_cells("SEALED ", "bold", TITLE_RED)
        lines += [title + text_cells("─" * RULE_WIDTH, "dim"), []]
        rows = rows[1:]
    for row in rows:
        if row is None:
            lines.append([])
            continue
        label, value = row
        mark = VALUE_MARKS.get(value[:1]) if value[1:2] == " " else None
        lines.append(
            text_cells(f"{label:<{LABEL_WIDTH}} ", "dim")
            + text_cells(value[:1], mark)
            + text_cells(value[1:])
        )
    return lines


def compose(rows, disc=True):
    """The stamp of `rows` as lines of cells (see the writers above), with
    its width and height and where the disc stands: `Letter(cells, width,
    height, disc)` (#832, `spec.md` S3, the owner's layout of 2026-10-07).

    The disc — `disc` False leaves it off, which is the rung `fitted` steps
    down to — stands at column 0, `DISC_CELLS` wide and
    `DISC_LINES` tall, and the text block (`text_lines`) begins `GAP`
    columns right of it, or at column 0 with no disc. The height is the
    taller one's, and each is centred on it. A cell inside the circle is its
    colour on both halves; every other cell of the disc's columns is empty,
    and nothing outside the disc has a background. No line runs past its
    own last visible cell, so the width is the longest line's."""
    text = text_lines(rows)
    if disc:
        n, _, px = build()
        tall = DISC_LINES
    else:
        n, tall, px = 0, 0, None
    height = max(len(text), tall)
    top_disc, top_text = (height - tall) // 2, (height - len(text)) // 2
    cells = []
    for ln in range(height):
        k, t = ln - top_disc, ln - top_text
        line = disc_cells(px, n, 2 * k) if 0 <= k < tall else [EMPTY] * n
        said = text[t] if 0 <= t < len(text) else []
        line += [EMPTY] * (GAP if px else 0) + said
        # No space carries a background, so a blank at the end is padding.
        while line and line[-1][0] in (None, " "):
            line.pop()
        cells.append(line)
    width = max((len(line) for line in cells), default=0)
    where = (0, 2 * top_disc, n, n) if px else None
    return Letter(cells, width, height, where)


# --- what the gate calls -------------------------------------------------


def stamp(rows, shape=False, disc=True):
    """The lines of the stamp: the disc beside the text block of `rows`
    (#717, #832). `shape` picks the letter twin. `disc` False is the text
    block with no disc, the rung `fitted` steps down to."""
    writer = letter_row if shape else colour_row
    return [writer(line) for line in compose(rows, disc).cells]


def admitted(blocks, budget=MESSAGE_BUDGET):
    """The drawn blocks one `Stop` message carries under `budget`, oldest
    first (#717). `blocks` is `(label, rows)` per values file, oldest first;
    a drawn block is its label and then its block form.

    The owner's rule of 2026-10-02 (`questions.md` Q6), which replaced one
    rung for the whole message: a seal keeps its disc rather than share a
    message without it. So the message carries as many of the oldest blocks
    as fit together WITH the disc. A block has two rungs since #853: with its
    disc, and the text block alone, because the disc has one size. The
    blocks past those are not drawn here; the hook leaves their files
    pending, and the next `Stop` draws them whole.

    The rung with no disc is for one block alone, the oldest, when it does
    not fit with its disc by itself; it is returned whatever its size, because
    nothing comes after it. So the first block is always drawn and the queue
    cannot stall. A text block with no disc is about 50 characters a row with
    its codes (925 with its label for the widest panel this tree can
    produce, measured 2026-10-07), its width bounded by
    `broad_gate.PANEL_VALUE_WIDTH`.

    A size is counted in UTF-16 units, which is what the harness counts
    (`MESSAGE_LIMIT`): a character outside the BMP is two. `budget` is a
    parameter so a case can drive both rungs."""

    def drawn(block, disc):
        label, rows = block
        text = "\n".join([label, *stamp(rows, disc=disc)])
        # `surrogatepass`: a values file is JSON, which can carry a lone
        # surrogate, and a size that raised would leave every file pending.
        return text, len(text.encode("utf-16-le", "surrogatepass")) // 2

    out, used = [], -2
    for block in blocks:
        text, size = drawn(block, True)
        if used + 2 + size > budget:
            break
        out.append(text)
        used += 2 + size
    if not out and blocks:
        return [drawn(blocks[0], False)[0]]
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
    that cannot be read or is not in that shape. A `scale` key, which every
    gate through 0.21's cycle writes (`broad_gate.SCALE_FOR_OLDER_HOOKS`), is
    read as nothing: such a file draws as one written without it."""
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
            lines = stamp(SAMPLE_ROWS, shape=shape)
        else:
            lines = drawn_from(args.values, shape)
    except ValueError as refused:
        sys.stderr.write(str(refused) + "\n")
        return 2
    sys.stdout.write("\n" + "\n".join(lines) + "\n\n")
    return 0


def drawn_from(path, shape):
    """The lines for the values file at `path`, which is claimed before they
    are returned. Raises `ValueError`
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
    lines = stamp(values["rows"], shape)
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
