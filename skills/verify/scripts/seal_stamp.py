#!/usr/bin/env python3
"""seal-stamp — the drawing the broad gate prints when it was earned.

Issue #30 §*What it prints*, redrawn by #717 and #832. A letter: what the
gate read — the tree and its branch, the base and its ref, the work item, the
suite's counts, the ledger's, the steps CI also runs, the rounds
(`broad_gate.panel` owns the list) — written on a parchment sheet, with a wax
disc pressed over the sheet's lower right corner and an emblem pressed into
the wax. The disc is COMPUTED — `hypot` for its edge — and only the emblem is
authored, as one vector source held below as data (`EMBLEM_D`, closed paths
in SVG `d` syntax): the disc renders it by area, each cell the mean of a
6 x 6 grid of samples in linear light, and the release PNG fills the same
polygons, so the two forms cannot drift. Four
hand-typed discs came before #30's and every one was lopsided; a circle that
is calculated cannot be off centre, and resizing it is one number. #717 took
off the rope ring and the outer red band and pressed the mark in one red lit
from the upper left, and the owner chose that drawing, its colours and its
scale from renderings. #832 replaced #717's chart of a lily, whose majority
vote mangled it below 1.0, with the vector source, and the owner chose its
mark from renderings: the section sign, §, on a disc 24 cells across.

Two forms, one drawing (`compose`). The block form is half-block characters,
the disc in truecolour and the sheet in 256-colour codes, emitted only where
the colour changes (a code per cell was 282 KB for one seal). The letter twin
is the same footprint as letters — the sheet's edge `|`, its top `.---.` and
its bottom `'---'`, the text as itself, `m` the wax's edge, `M n` the rim's
light and dark ends, `.` the field and `Y y` the emblem and its shadow, a
blended cell taking the letter of the colour nearest it — for a console that
cannot render half-blocks, and for `seal-stamp` on a pipe. The twin is chosen when
stdout is not a UTF-8 terminal, or on `--shape`. An agent's report carries
neither: since #400 the gate draws nothing on a pipe.

**The `Stop` hook's message is held under a budget** (#717): the harness
persists a `systemMessage` longer than `MESSAGE_LIMIT` and shows a preview
instead, so `admitted` carries as many of the oldest stamps as fit with
their disc, each at the highest rung of `SCALE_LADDER` the others leave room
for — one rung since #832, 0.90 — and leaves the rest for the next `Stop`.
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
  seal-stamp --scale 0.75         the disc drawn smaller; 0.75 is the floor
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
import bisect
import collections
import functools
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
# at module level — the emblem below is parsed by a call.
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


# --- the emblem ----------------------------------------------------------
#
# One vector source (#832): closed paths in SVG `d` syntax, absolute `M L C Q
# Z` only, in a 1000 x 1000 viewBox centred on (500, 500) with the field's
# edge at radius 500, filled even-odd. The terminal renders it by area
# (`build`) and the release PNG fills the same flattened polygons with
# Pillow, so the two forms cannot drift. It replaces #717's chart of a
# lily, one cell a mark, whose majority vote mangled the lily below 1.0.
#
# The mark is the section sign, §, chosen by the owner on 2026-10-06 from
# renderings looked at in their own terminal (#832, `spec.md` decision 3 of
# work item 1791270164): Georgia Bold's outline scaled to 820 units, centred
# on (500, 500), two subpaths — the outline and its counter. The string is
# the one handed over, copied character for character; it is data, not a
# drawing anybody re-derives.
EMBLEM_D = (
    "M 721.8 484.0 Q 721.8 535.5 687.5 572.0 Q 653.2 608.5 595.8 627.4 Q "
    "645.4 647.9 670.7 681.9 Q 696.0 715.9 696.0 756.8 Q 696.0 822.5 635.0 "
    "866.2 Q 573.9 910.0 467.9 910.0 Q 417.3 910.0 383.8 900.5 Q 350.2 "
    "891.0 329.8 876.4 Q 309.3 861.9 300.8 844.6 Q 292.3 827.3 292.3 812.2 "
    "Q 292.3 785.5 308.1 768.2 Q 323.9 751.0 354.1 751.0 Q 375.5 751.0 "
    "391.1 762.1 Q 406.6 773.3 417.3 791.3 Q 427.5 808.4 434.6 827.6 Q "
    "441.6 846.8 449.4 868.7 Q 451.9 869.1 456.2 869.6 Q 460.6 870.1 463.0 "
    "870.1 Q 508.8 870.1 538.7 852.6 Q 568.6 835.1 568.6 796.2 Q 568.6 "
    "772.8 558.8 756.8 Q 549.1 740.7 530.2 728.1 Q 511.7 715.0 481.0 702.1 "
    "Q 450.4 689.2 420.2 677.0 Q 346.8 647.4 312.5 609.7 Q 278.2 572.0 "
    "278.2 516.0 Q 278.2 468.4 305.9 433.4 Q 333.7 398.4 404.2 372.6 Q "
    "349.7 350.2 324.9 315.9 Q 300.1 281.6 300.1 238.3 Q 300.1 174.6 363.3 "
    "132.3 Q 426.6 90.0 527.2 90.0 Q 575.4 90.0 609.9 99.2 Q 644.4 108.5 "
    "665.4 123.6 Q 685.3 137.7 694.1 154.9 Q 702.8 172.2 702.8 187.8 Q "
    "702.8 213.5 688.0 231.3 Q 673.1 249.0 641.0 249.0 Q 618.7 249.0 603.8 "
    "237.9 Q 589.0 226.7 577.8 208.7 Q 568.6 194.1 560.1 170.5 Q 551.6 "
    "146.9 545.7 131.3 Q 542.3 130.4 538.4 130.1 Q 534.5 129.9 532.1 129.9 "
    "Q 486.4 129.9 457.0 148.1 Q 427.5 166.4 427.5 203.8 Q 427.5 228.1 "
    "437.5 243.7 Q 447.5 259.3 467.9 272.4 Q 488.3 285.5 518.0 297.7 Q "
    "547.7 309.8 579.8 323.0 Q 652.7 352.1 687.2 389.1 Q 721.8 426.1 721.8 "
    "484.0 Z M 597.8 516.5 Q 597.8 491.2 586.6 473.5 Q 575.4 455.7 554.5 "
    "441.6 Q 535.5 428.5 501.7 413.9 Q 467.9 399.3 443.6 388.6 Q 425.6 "
    "404.2 413.9 431.7 Q 402.2 459.1 402.2 483.5 Q 402.2 509.2 414.4 527.5 "
    "Q 426.6 545.7 447.0 559.3 Q 469.4 573.9 498.3 586.3 Q 527.2 598.7 "
    "556.4 611.4 Q 580.2 590.5 589.0 566.6 Q 597.8 542.8 597.8 516.5 Z"
)

SVG_REFUSED = (
    "seal-stamp: the emblem's path uses `{command}`, and only absolute "
    "M L C Q Z are read; convert it to those before it is written in."
)
SVG_TOKEN = re.compile(r"[A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
SVG_ARITY = {"M": 2, "L": 2, "C": 6, "Q": 4, "Z": 0}


def svg_path(d):
    """The paths an SVG `d` string draws, in the emblem's frame: a tuple of
    paths, each a tuple of segments — `("M", x, y)` first, then `("L", x, y)`
    or `("C", x1, y1, x2, y2, x, y)` from the previous point — closed to its
    first point. The frame's origin is the disc's centre and its unit circle
    the field's edge; `y` grows downward, as cells do. A `Q` is raised to a
    `C`; any command but absolute `M L C Q Z` is refused with its name."""
    tokens = SVG_TOKEN.findall(d)
    stray = re.sub(SVG_TOKEN, " ", d).replace(",", " ").split()
    if stray:
        raise ValueError(SVG_REFUSED.format(command=stray[0]))

    def unit(x, y):
        return ((float(x) - 500) / 500, (float(y) - 500) / 500)

    paths, path, i, here = [], [], 0, (0.0, 0.0)
    while i < len(tokens):
        command = tokens[i]
        if command not in SVG_ARITY:
            raise ValueError(SVG_REFUSED.format(command=command))
        n = SVG_ARITY[command]
        args = tokens[i + 1 : i + 1 + n]
        if len(args) < n or any(a.isalpha() for a in args):
            raise ValueError(SVG_REFUSED.format(command=command + " (arguments)"))
        i += 1 + n
        points = [unit(args[k], args[k + 1]) for k in range(0, n, 2)]
        if command == "M":
            if path:
                paths.append(tuple(path))
            path = [("M", *points[0])]
        elif command == "L":
            path.append(("L", *points[0]))
        elif command == "C":
            path.append(("C", *points[0], *points[1], *points[2]))
        elif command == "Q":
            (qx, qy), (ex, ey) = points
            c1 = (here[0] + 2 / 3 * (qx - here[0]), here[1] + 2 / 3 * (qy - here[1]))
            c2 = (ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey))
            path.append(("C", *c1, *c2, ex, ey))
        else:  # Z
            if path:
                paths.append(tuple(path))
            path = []
            continue
        here = points[-1]
    if path:
        paths.append(tuple(path))
    return tuple(paths)


def flatten(paths, n=16):
    """Each path as a polygon, each cubic as `n` chords."""
    polygons = []
    for path in paths:
        points = [path[0][1:3]]
        for segment in path[1:]:
            if segment[0] == "L":
                points.append(segment[1:3])
                continue
            (x0, y0), (x1, y1, x2, y2, x3, y3) = points[-1], segment[1:]
            for k in range(1, n + 1):
                t = k / n
                a, b, c, e = (
                    (1 - t) ** 3,
                    3 * (1 - t) ** 2 * t,
                    3 * (1 - t) * t * t,
                    t**3,
                )
                points.append(
                    (
                        a * x0 + b * x1 + c * x2 + e * x3,
                        a * y0 + b * y1 + c * y2 + e * y3,
                    )
                )
        polygons.append(points)
    return polygons


def inside(polygons, x, y):
    """Whether `(x, y)` is filled, even-odd: a ray to the right crosses an odd
    number of the polygons' edges."""
    odd = False
    for poly in polygons:
        x0, y0 = poly[-1]
        for x1, y1 in poly:
            if (y1 > y) != (y0 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                odd = not odd
            x0, y0 = x1, y1
    return odd


def shade(filled, x, y, delta):
    """The mark's colour at `(x, y)` in the field, lit from the upper left
    (#832): `LILY_LIGHT` where `filled` says the point is the mark's, the
    shadow `LILY_SHADOW` where it is not and the point `delta` up-left of it
    is — so the shadow falls down-right of the mark — and None, the field,
    everywhere else."""
    if filled(x, y):
        return LILY_LIGHT
    if filled(x - delta, y - delta):
        return LILY_SHADOW
    return None


EMBLEM = svg_path(EMBLEM_D)
EMBLEM_POLYGONS = flatten(EMBLEM)

# The disc's colours. The first four are #717's, chosen by the owner from
# renderings: `WAX_M` the wax's edge, `FIELD` the field, `LILY_LIGHT` the
# mark and `LILY_SHADOW` its shadow (the `LILY_` names are #717's, kept
# because the release script and the cases read them). The rim's two ends
# are the owner's of 2026-10-06 (#832): the field's inner rim is lit by angle
# from `RIM_DARK` at the lower right to `RIM_LIGHT` at the upper left. They
# are truecolour, the one part of the letter drawn that way, and a cell of
# the disc is a blend of them (`build`).
WAX_M = (168, 26, 30)
FIELD = (120, 16, 20)
LILY_LIGHT = (226, 82, 74)
LILY_SHADOW = (96, 10, 14)
RIM_LIGHT = (214, 70, 66)
RIM_DARK = (104, 12, 16)
DISC_COLOURS = (WAX_M, FIELD, LILY_LIGHT, LILY_SHADOW, RIM_LIGHT, RIM_DARK)
# Where the disc ends, as a fraction of its radius, and where its edge begins.
WAX_EDGE, FIELD_EDGE = 0.84, 0.78

# The sheet's colours, as 256-colour codes (#717): the parchment and its
# one-cell edge, the ink, and the red of the `SEALED` title. A code is a
# shorter sequence than a triple, and the sheet is most of the letter's cells.
PARCHMENT = 230  # (255, 255, 215) in the 256-colour cube
SHEET_EDGE = 187  # (215, 215, 175)
INK = 94  # (135, 95, 0)
TITLE = 124  # (175, 0, 0)

# The letter for each disc colour in the twin (#832): `m` the wax's edge and
# `.` the field, as before #717; `Y` the mark and `y` its shadow; `M` and `n`
# the rim's light and dark ends. A blended cell takes the letter of the
# palette colour nearest it (`nearest`), and a cell nearer the parchment than
# any of them is the sheet's own character (`compose`).
KEY = {
    WAX_M: "m",
    FIELD: ".",
    LILY_LIGHT: "Y",
    LILY_SHADOW: "y",
    RIM_LIGHT: "M",
    RIM_DARK: "n",
}

# The six levels of xterm's 6 x 6 x 6 colour cube, which a 256-colour code
# from 16 to 231 indexes.
CUBE_LEVELS = (0, 95, 135, 175, 215, 255)


def cube(code):
    """The triple a 256-colour code in the cube draws (16-231)."""
    k = code - 16
    return (CUBE_LEVELS[k // 36], CUBE_LEVELS[k // 6 % 6], CUBE_LEVELS[k % 6])


# Linear light is (c / 255) ** GAMMA per channel: a mean of colours is taken
# there, because the mean of two sRGB values sits below the mean of their
# intensities and a thin light stroke would read darker than its colour.
GAMMA = 2.2


def linear(colour):
    """`colour`, an sRGB triple, in linear light."""
    return tuple((c / 255) ** GAMMA for c in colour)


def srgb(light):
    """A linear-light triple back in sRGB, each channel rounded."""
    return tuple(round(255 * max(0.0, min(1.0, c)) ** (1 / GAMMA)) for c in light)


@functools.cache
def nearest(colour):
    """The palette colour nearest `colour` in linear light, or None where the
    parchment is nearer than every one of them: the twin's letter for a
    blended cell (`letter_row`)."""
    here = linear(colour)

    def distance(other):
        return sum((a - b) ** 2 for a, b in zip(here, linear(other), strict=True))

    best = min(DISC_COLOURS, key=distance)
    return None if distance(cube(PARCHMENT)) < distance(best) else best


# #30 §*Size* measured the floor on the lily's chart: at 75 % the lily was
# still legible, at 60 % its band closed up and its foot became a blob, and at
# 50 % it read as a cross. #832 renders the § by area and keeps the band's
# floor where #30 put it, for `--scale` by hand: the owner saw the § at 20
# cells, the floor's size, fragment, and accepted nothing below 24, so the
# hook never draws a disc below `DEFAULT_SCALE` (`SCALE_LADDER`). Above 1.0
# nothing is drawn, because the hook's message budget was measured up to 1.0
# (`SCALE_TOO_LARGE`).
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
# rope this paragraph names is gone. Those readings were of the lily, which
# #832 withdrew. #832 kept 0.90 as the scale and made it the one the owner's
# disc is sized at: 24 cells across (`DISC_CELLS`), 13 lines.
#
# 0.75 was the other candidate, passed over rather than missed: under #400's
# disc it was the only legal scale where the disc (then 17 lines) and the
# panel ended within one line of each other, and it was the least detail of
# the band. Disc size moves in whole cells, so a scale is not a continuous
# dial.
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
# since #832: the owner saw the § fragment on a disc smaller than 24 cells, so
# a block that does not fit with its disc at 0.90 is the sheet alone rather
# than a smaller disc. Each rung is inside `check_scale`'s band, so a step
# down cannot be refused.
SCALE_LADDER = (0.90,)

SCALE_REFUSED = (
    "seal-stamp: scale {scale} is under the floor of {floor}; below it the "
    "disc has too few cells for its emblem to be read (#30 measured the floor). "
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
    "seal-stamp: scale {scale} is above {ceiling}; the hook's message budget "
    "was measured up to it, so a larger disc is not drawn. Nothing was drawn."
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


# The disc's numbers (#832), all in cells of the terminal's grid, where a
# cell is one column by one half-row and so square. `DISC_CELLS` is the
# owner's: the disc is 24 cells across at its wax edge at `DEFAULT_SCALE`,
# because they saw 20 fragment the § and accepted nothing smaller. The rim is
# `RIM_WIDTH` cells inside the field's edge; the shadow falls `SHADOW_OFFSET`
# cells down-right of the mark; `FIT_OFFSET` and `FIT_SCALE` place the mark
# on the grid, the fit searched at 24 cells over offsets in eighths of a cell
# and scales 0.96, 1.0 and 1.04 for the most field cells that read clearly
# mark or clearly field. Each cell is the mean of `SAMPLES` x `SAMPLES`
# points, the owner's rendering at 6.
DISC_CELLS = 24
RIM_WIDTH = 1.15
SHADOW_OFFSET = 0.7
FIT_OFFSET = (0.0, 0.375)
FIT_SCALE = 1.04
SAMPLES = 6
# A field cell's mark and shadow shares are tightened past these: a share
# under `TIGHT_LOW` is field and one over `TIGHT_LOW + TIGHT_SPAN` is all
# mark, so a stroke a cell straddles reads as a stroke rather than as a smear.
TIGHT_LOW, TIGHT_SPAN = 0.15, 0.7
# Where the rim is lightest, in radians from the positive x axis with `y`
# down: the upper left.
RIM_LIT_AT = math.radians(225)


def smoothstep(t):
    """`3t² - 2t³` on `t` clamped to [0, 1]."""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def crossings(polygons, y):
    """Where the row at `y` crosses the polygons' edges, sorted — the same
    edges and the same arithmetic `inside` uses, so a point's parity read off
    them is `inside`'s answer."""
    xs = []
    for poly in polygons:
        x0, y0 = poly[-1]
        for x1, y1 in poly:
            if (y1 > y) != (y0 > y):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            x0, y0 = x1, y1
    xs.sort()
    return xs


def build(scale=1.0, disc_cells=DISC_CELLS):
    """`(w, h, px)` — the disc's width and height in cells, and
    `px(x, y, under=None)`, a cell's colour.

    The diameter at the wax edge is `round(disc_cells · scale /
    DEFAULT_SCALE)` cells, 24 at 0.90; `w` is two more and `h` is even,
    because the block form prints two cells per line; the radius is the
    diameter over `2 · WAX_EDGE`. A cell is the mean, in linear light, of
    its `SAMPLES` x `SAMPLES` points at `(x + (i + 0.5) / SAMPLES, y + (j +
    0.5) / SAMPLES)`, each coloured by where it falls (#832): past
    `WAX_EDGE` it is `under`, the colour beneath, or dropped where `under` is
    None; then `WAX_M`; then the rim, `RIM_DARK` mixed toward `RIM_LIGHT` by
    the angle from `RIM_LIT_AT`; then the field, where `shade` decides
    between the mark, its shadow and `FIELD` over `EMBLEM_POLYGONS` placed
    by `FIT_OFFSET` and `FIT_SCALE`. A cell with half or fewer of its points
    on the disc is None where `under` is None. A cell whose every point is
    in the field is tightened: its mark and shadow shares go through
    `smoothstep`, and it is `FIELD` mixed toward the shadow and then toward
    the mark by them.

    Each row of points is read from one sorted list of `crossings` per row,
    which is `inside`'s answer at a fraction of its cost: the hook draws a
    disc for each stamp it prints."""
    refusal = check_scale(scale)
    if refusal:
        raise ValueError(refusal)
    diameter = round(disc_cells * scale / DEFAULT_SCALE)
    w = diameter + 2
    h = w + (w % 2)
    r0 = diameter / 2 / WAX_EDGE
    ox, oy = w / 2, h / 2
    field = FIELD_EDGE * r0
    k = field * FIT_SCALE
    delta = SHADOW_OFFSET / k
    rim = FIELD_EDGE - RIM_WIDTH / r0
    fx, fy = FIT_OFFSET
    n = SAMPLES
    rows = {}

    def filled(u, v):
        xs = rows.get(v)
        if xs is None:
            xs = rows[v] = crossings(EMBLEM_POLYGONS, v)
        return (len(xs) - bisect.bisect_right(xs, u)) % 2 == 1

    def point(dx, dy):
        """A point's colour as an sRGB triple, or None past the wax, and
        whether it is in the field."""
        r = math.hypot(dx, dy) / r0
        if r > WAX_EDGE:
            return None, False
        if r > FIELD_EDGE:
            return WAX_M, False
        if r > rim:
            t = smoothstep((1 + math.cos(math.atan2(dy, dx) - RIM_LIT_AT)) / 2)
            return tuple(
                a + (b - a) * t for a, b in zip(RIM_DARK, RIM_LIGHT, strict=True)
            ), False
        said = shade(filled, (dx - fx) / k, (dy - fy) / k, delta)
        return said or FIELD, True

    cells = []
    for y in range(h):
        line = []
        for x in range(w):
            on, total, every, marks, shadows = 0, [0.0, 0.0, 0.0], True, 0, 0
            for j in range(n):
                dy = y + (j + 0.5) / n - oy
                for i in range(n):
                    colour, in_field = point(x + (i + 0.5) / n - ox, dy)
                    every = every and in_field
                    if colour is None:
                        continue
                    on += 1
                    marks += colour == LILY_LIGHT
                    shadows += colour == LILY_SHADOW
                    for c, part in enumerate(linear(colour)):
                        total[c] += part
            line.append((on, total, every, marks, shadows))
        cells.append(line)
    whole = n * n
    lit, dark, plain = linear(LILY_LIGHT), linear(LILY_SHADOW), linear(FIELD)

    def tighten(share):
        return smoothstep((share - TIGHT_LOW) / TIGHT_SPAN)

    def px(x, y, under=None):
        if not (0 <= x < w and 0 <= y < h):
            return None
        on, total, every, marks, shadows = cells[y][x]
        if every:
            t_mark, t_shadow = tighten(marks / whole), tighten(shadows / whole)
            colour = [
                a + (b - a) * t_shadow * (1 - t_mark)
                for a, b in zip(plain, dark, strict=True)
            ]
            return srgb(a + (b - a) * t_mark for a, b in zip(colour, lit, strict=True))
        if under is None:
            return srgb(c / on for c in total) if 2 * on > whole else None
        if on == 0:
            return under
        beneath = linear(under)
        return srgb(
            (c + (whole - on) * b) / whole for c, b in zip(total, beneath, strict=True)
        )

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
    written there; else the letter of the palette colour nearest whichever
    half is the disc's (`nearest`), the top first, so a disc cell overrides
    the sheet's frame as it covers it in colour; else — a half nearer the
    parchment than the disc, or no disc — the sheet's own character; else a
    space."""
    out = []
    for top, bottom, text, frame in cells:
        if text:
            out.append(text[0])
            continue
        near = None
        for half in (top, bottom):
            if isinstance(half, tuple):
                near = nearest(half)
                if near is not None:
                    break
        out.append(KEY[near] if near is not None else frame or " ")
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

# `disc` is where the disc's grid stands, `(left, top, w, h)`: `left` and
# `w` in cells, `top` and `h` in half-rows from the letter's first line, or
# None with no disc — so the release PNG draws its circle where the terminal
# drew the disc (#832).
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

    The disc at `scale` — None leaves it off, which is the last rung
    `fitted` steps down to — stands with its centre line on the sheet's last
    line and as far left as it can without touching a text cell or leaving
    fewer than `GAP` clear cells after any line's last character; a cell the
    disc touches at all counts, blended or not. The sheet's right edge is at
    the disc's centre column, or two cells past the longest line where the
    text is wider, and its first and last lines are blank. A disc cell over
    the sheet is blended with the sheet's colour beneath it, as a triple
    (`cube`); one off the sheet is the disc's alone (#832). Lines end at
    their last cell something covers."""
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

    def disc(left, x, y, under=None):
        dx, dy = x - left, y - 2 * disc_top
        return px(dx, dy, under) if px and 0 <= dx < dw and 0 <= dy < dh else None

    parchment = cube(PARCHMENT)

    def touched(left, x, y):
        return disc(left, x, y, parchment) not in (None, parchment)

    def covered(left):
        for k, said in enumerate(text, 1):
            for x in range(TEXT_LEFT, TEXT_LEFT + len(said) + GAP):
                if touched(left, x, 2 * k) or touched(left, x, 2 * k + 1):
                    return True
        return False

    left = TEXT_LEFT
    while px and covered(left):
        left += 1
    width = max(TEXT_LEFT + longest + 2, left + dw // 2)

    def colour(x, y):
        sheet = None
        if y < 2 * height and x < width:
            sheet = SHEET_EDGE if x in (0, width - 1) else PARCHMENT
        under = None if sheet is None else cube(sheet)
        on_disc = disc(left, x, y, under)
        return on_disc if on_disc not in (None, under) else sheet

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
    where = (left, 2 * disc_top, dw, dh) if px else None
    return Letter(cells, width, height, where)


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
    as fit together WITH the disc, each at the last rung of `SCALE_LADDER`
    or at its own scale where that is lower, and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. Since #832 the ladder
    is one rung, 0.90: the owner saw the § fragment on a smaller disc, so a
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
        help=f"the disc's scale; {SCALE_FLOOR} is the floor, {SCALE_CEILING} the "
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
