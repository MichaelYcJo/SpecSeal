#!/usr/bin/env python3
"""seal-stamp — the drawing the broad gate prints when it was earned.

Issue #30 §*What it prints*. A wax disc with a fleur-de-lis, and a parchment
panel beside it carrying the numbers the gate read: the tree, the base, the
suite's counts, lint, the ledger, the chain, the rounds. The disc is COMPUTED —
`hypot` for the bands, `sin` for the rope's twist — and only the lily is
authored, as a 29x32 counted-stitch chart held below as data. Four hand-typed
discs came before this one and every one was lopsided; a circle that is
calculated cannot be off centre, and resizing it is one number.

Two forms, one drawing. The block form is half-block characters in truecolour,
emitted only where the colour changes (a code per cell was 282 KB for one
seal). The letter twin is the same footprint as letters — `o O` rope, `l m`
wax, `G W y Y` the lily's golds, `.` the field — for a console that cannot
render half-blocks, and for an agent's report, which is a pipe. The twin is
chosen when stdout is not a UTF-8 terminal, or on `--shape`.

The stamp prints on success only. The failure form, `not_sealed`, is the words
`NOT SEALED`, the tree and the base, and the failing checks with their first
lines — no drawing, because a picture that says *sealed* beside a word that
says *not* is read picture first.

Usage:
  seal-stamp                      the stamp over sample rows, for a person
  seal-stamp --shape              the letter twin
  seal-stamp --scale 0.75         the chart shrunk; 0.75 is the floor

The gate imports `stamp(rows, scale, shape)`, `not_sealed(tree, base,
failures)` and `pick_shape(stream)`; the command exists so a person can see
the drawing without running a gate.

Exit codes: 0 printed · 2 refused — a scale under the floor, or an
interpreter under the floor; nothing was written on 2.
"""

import argparse
import math
import re
import sys

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
# 29 columns by 32 rows. `D` the lily's gold, `R` its highlight, `y` the
# band's shadow, `Y` the band's light, `.` the field. Traced outside the tree
# by hand against a counted-stitch pattern; this is the only copy.
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

GOLD = {
    "D": (0xC8, 0x96, 0x1E),
    "R": (0xF7, 0xDC, 0x8A),
    "y": (0x8C, 0x63, 0x12),
    "Y": (0xE8, 0xB7, 0x3C),
}
ROPE_L, ROPE_D = (232, 226, 196), (168, 158, 122)
WAX_L, WAX_M, FIELD = (206, 46, 48), (168, 26, 30), (78, 12, 16)

# The letter for each colour. `None` is outside the disc.
KEY = {
    ROPE_L: "o",
    ROPE_D: "O",
    WAX_L: "l",
    WAX_M: "m",
    FIELD: ".",
    GOLD["D"]: "G",
    GOLD["R"]: "W",
    GOLD["y"]: "y",
    GOLD["Y"]: "Y",
    None: " ",
}

# #30 §*Size*: the chart compresses to 75 % with the lily still legible; at
# 60 % the band closes up and the foot becomes a blob, and at 50 % it reads as
# a cross. Above 1.0 nothing enlarges — the chart is one cell per stitch.
SCALE_FLOOR = 0.75
SCALE_CEILING = 1.0
SCALE_REFUSED = (
    "seal-stamp: scale {scale} is under the floor of {floor}; below it the "
    "lily is not legible (#30 measured 0.6 closing the band and 0.5 reading as "
    "a cross). Nothing was drawn."
)
SCALE_TOO_LARGE = (
    "seal-stamp: scale {scale} is above {ceiling}; the chart is one cell per "
    "stitch and does not enlarge. Nothing was drawn."
)


def check_scale(scale):
    """The refusal for a scale outside the band, or None inside it."""
    if scale < SCALE_FLOOR:
        return SCALE_REFUSED.format(scale=scale, floor=SCALE_FLOOR)
    if scale > SCALE_CEILING:
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
            row.append(max(set(ink), key=ink.count) if ink else ".")
        out.append("".join(row))
    return out


def build(scale=1.0, margin=0.74):
    """`(w, h, px)` — the disc's width and height in cells, and a function
    from a cell to its colour, `None` outside the disc.

    The radius is the chart's reach from its centre over `margin`, so the lily
    fills the field and the bands are drawn around it: rope from 0.90, wax in
    two reds from 0.78, the field and the chart inside. The rope's twist is a
    sine over the angle, so it alternates light and dark around the ring.
    `h` is even, because the block form prints two cells per line."""
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

    def px(x, y):
        # Sampled at the cell's centre. Sampled at its corner, the disc sat
        # half a cell right and half a cell down of the grid's centre — the
        # top rope row came out six cells wider than the bottom one — which is
        # the lopsidedness a computed circle is supposed to make impossible.
        dx, dy = x + 0.5 - ox, y + 0.5 - oy
        r = math.hypot(dx, dy) / r0
        if r > 1.00:
            return None
        if r > 0.90:
            twist = math.sin(math.atan2(dy, dx) * 30 + r * 8)
            return ROPE_L if twist > 0 else ROPE_D
        if r > 0.84:
            return WAX_L
        if r > 0.78:
            return WAX_M
        # `floor`, not `int`: `int` truncates toward zero, so the cell just
        # outside the chart's top-left would read stitch 0 a second time.
        fx, fy = math.floor(dx + fw / 2), math.floor(dy + fh / 2)
        if 0 <= fy < fh and 0 <= fx < fw and art[fy][fx] in GOLD:
            return GOLD[art[fy][fx]]
        return FIELD

    return w, h, px


# --- the two row writers -------------------------------------------------
#
# Both walk the same cells — row `y` on top, `y + 1` below — so the two forms
# have one footprint: a cell is blank in the twin exactly where the block form
# prints a space.


def sgr(ground, rgb):
    """A truecolour sequence: `ground` 38 for the foreground, 48 for the
    background."""
    r, g, b = rgb
    return f"\x1b[{ground};2;{r};{g};{b}m"


def colour_row(px, w, y):
    """One line of the block form, emitting a colour only where it changes.

    A cell whose top half is outside the disc is a lower half-block in the
    bottom colour; one whose bottom half is outside is an upper half-block;
    one inside on both halves is an upper half-block with the bottom colour
    as its background. The line ends with a reset, so nothing bleeds into the
    panel beside it."""
    out, fg, bg = [], None, None
    for x in range(w):
        top, bot = px(x, y), px(x, y + 1)
        if top is None and bot is None:
            if fg or bg:
                out.append("\x1b[0m")
                fg = bg = None
            out.append(" ")
            continue
        if top is None:
            want_fg, want_bg, ch = bot, None, "▄"
        elif bot is None:
            want_fg, want_bg, ch = top, None, "▀"
        else:
            want_fg, want_bg, ch = top, bot, "▀"
        if want_fg != fg:
            out.append(sgr(38, want_fg))
            fg = want_fg
        if want_bg != bg:
            out.append("\x1b[49m" if want_bg is None else sgr(48, want_bg))
            bg = want_bg
        out.append(ch)
    return "".join(out) + "\x1b[0m"


def letter_row(px, w, y):
    """One line of the letter twin over the same two cell rows: the top cell's
    letter, or the bottom cell's where only the bottom is inside the disc."""
    out = []
    for x in range(w):
        top, bot = px(x, y), px(x, y + 1)
        out.append(KEY[top if top is not None else bot])
    return "".join(out)


# --- the panel -----------------------------------------------------------

PANEL_WIDTH = 36


def letter(rows, width=PANEL_WIDTH):
    """A parchment panel carrying the seal's numbers, set beside the disc.

    `rows` is a list of `(label, value)` pairs with `None` for a blank line,
    so what the seal reports is data the gate fills rather than a string it
    formats. A value longer than the panel is cut at the frame."""
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


def beside(left, right, gap=3, pad_left=2):
    """Two blocks side by side, the shorter one centred against the taller.
    Widths are measured with colour codes removed."""
    lw = max(len(strip_ansi(line)) for line in left) if left else 0
    top = max(0, (len(left) - len(right)) // 2)
    rows = max(len(left), len(right) + top)
    out = []
    for i in range(rows):
        line = left[i] if i < len(left) else ""
        pad = lw - len(strip_ansi(line))
        r = right[i - top] if 0 <= i - top < len(right) else ""
        out.append(" " * pad_left + line + " " * (pad + gap) + r)
    return out


# --- what the gate calls -------------------------------------------------


def stamp(rows, scale=1.0, shape=False):
    """The lines of the stamp: the disc at `scale`, the panel of `rows`
    beside it. `shape` picks the letter twin. Raises `ValueError` with the
    refusal sentence for a scale outside the band."""
    w, h, px = build(scale)
    writer = letter_row if shape else colour_row
    disc = [writer(px, w, y) for y in range(0, h, 2)]
    return beside(disc, letter(rows))


def not_sealed(tree, base, failures):
    """The failure form, as lines: `NOT SEALED <tree> against <base>`, then
    each failing check's name with its first lines under it. No drawing.

    `failures` is a list of `(name, lines)` — the check that failed and the
    first lines of what it printed, as the gate kept them."""
    out = [f"NOT SEALED   {tree} against {base}", ""]
    for name, lines in failures:
        lines = list(lines) or ["(no output)"]
        out.append(f"  {name:<8} {lines[0]}")
        out.extend(f"  {'':<8} {line}" for line in lines[1:])
    return out


def pick_shape(stream):
    """True when `stream` gets the letter twin: anything that is not a UTF-8
    terminal. A console on another codepage draws UTF-8 half-blocks as
    mojibake, and a pipe is an agent's report, which carries the twin
    (`spec.md` §Out). Asked BEFORE the stream is reconfigured to UTF-8 — after
    that call every stream answers `utf-8`, and a cp949 console would get the
    blocks it cannot draw."""
    encoding = (getattr(stream, "encoding", None) or "").lower().replace("-", "")
    if encoding != "utf8":
        return True
    isatty = getattr(stream, "isatty", None)
    try:
        return not (isatty and isatty())
    except (ValueError, OSError):
        return True


# --- a person's command --------------------------------------------------

# Neutral values in the panel's shape, so `seal-stamp` shows a person what the
# gate will print without a gate having run.
SAMPLE_ROWS = [
    ("SEALED", ""),
    None,
    ("tree", "c46fd2d"),
    ("base", "1e2bed9"),
    None,
    ("suite", "768 passed, 1 skipped"),
    ("lint", "clean"),
    ("ledger", "187 ok . 0 broken"),
    ("chain", "exit 0"),
    None,
    ("rounds", "4"),
]


def main(argv=None, console_wants_letters=None):
    """`console_wants_letters` is `pick_shape` asked of stdout as the process
    found it. `__main__` asks before it reconfigures the streams, because
    `reconfigure` changes the one object `sys.stdout` and `sys.__stdout__`
    both name; a direct call may leave it to be asked here."""
    parser = argparse.ArgumentParser(
        prog="seal-stamp", description="Print the seal the broad gate stamps."
    )
    parser.add_argument(
        "--shape", action="store_true", help="the letter twin, whatever the console"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help=f"the chart's scale; {SCALE_FLOOR} is the floor, {SCALE_CEILING} the size",
    )
    args = parser.parse_args(argv)
    if console_wants_letters is None:
        console_wants_letters = pick_shape(sys.stdout)
    shape = args.shape or console_wants_letters
    try:
        lines = stamp(SAMPLE_ROWS, scale=args.scale, shape=shape)
    except ValueError as refused:
        sys.stderr.write(str(refused) + "\n")
        return 2
    sys.stdout.write("\n" + "\n".join(lines) + "\n\n")
    return 0


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
