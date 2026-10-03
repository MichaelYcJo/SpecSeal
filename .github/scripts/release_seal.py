#!/usr/bin/env python3
"""Draw the release's seal as a PNG, attach it, and put it in the note (#718).

The 0.17.0 seal was drawn by hand: a script outside the tree read the cells
`seal_stamp.compose` builds, painted each the way `seal_stamp.block` describes
it, and the PNG was uploaded and edited into the note. This is that script,
in the tree and run by the tag push.

**One cell, one rectangle.** A cell of the letter is two halves and maybe a
character. `paint` turns each into rectangles and text in a `CELL_W` x
`CELL_H` pixel cell, each half `CELL_H // 2` tall, and `png` rasterises them.
So the PNG is the terminal form at a fixed pixel size: the same cells, the
same colours through xterm's 256-colour table (`rgb`), and transparent where
the terminal form paints nothing. `paint` is kept free of Pillow, so the case
that pins it against `block` runs on any interpreter, and Pillow is imported
inside `png` alone.

**Pillow is a test-and-release dependency, never a plugin one.** The gates
are stdlib-only (`CONTRIBUTING.md` §*Running the checks*), and nothing under
`hooks/` or `skills/` imports this file or Pillow. The version is pinned once,
in `.github/scripts/run_tests.py#PILLOW`.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "skills", "verify", "scripts"))
import seal_stamp  # noqa: E402

# One cell of the letter in pixels, and the size its characters are drawn
# at: the hand-drawn 0.17.0 seal's, which the owner saw on the release page.
CELL_W, CELL_H = 14, 28
FONT_SIZE = 22

# xterm's 256-colour table past the sixteen system colours: a 6x6x6 cube on
# these levels, then a ramp of 24 greys. The system colours are a terminal's
# own choice, and the sheet uses none of them.
CUBE_LEVELS = (0, 95, 135, 175, 215, 255)


def rgb(colour):
    """`colour` as an `(r, g, b)` triple: a triple as it is, and a
    256-colour code through xterm's cube and grey ramp. Raises `ValueError`
    for 0-15, whose values a terminal chooses."""
    if isinstance(colour, tuple):
        return colour
    if 16 <= colour <= 231:
        n = colour - 16
        return (CUBE_LEVELS[n // 36], CUBE_LEVELS[n // 6 % 6], CUBE_LEVELS[n % 6])
    if 232 <= colour <= 255:
        grey = 8 + 10 * (colour - 232)
        return (grey, grey, grey)
    raise ValueError(f"no fixed colour for 256-colour code {colour}")


def size(letter):
    """The PNG's `(width, height)` in pixels for `letter`'s cells."""
    width = max((len(line) for line in letter.cells), default=0)
    return width * CELL_W, len(letter.cells) * CELL_H


def paint(letter):
    """`letter`'s cells as drawing operations, in the order they are laid.

    Each is `("rect", x0, y0, x1, y1, rgb)` with the corners inclusive, or
    `("text", cx, cy, character, rgb, bold)` centred on the cell. A cell
    takes its background over the whole cell, then the half its half-block
    colours, or its character; a cell `block` paints nothing gets nothing,
    which is what leaves it transparent. The title line, the letter's
    second, is bold, the way `compose` inks it in `TITLE`."""
    ops, half = [], CELL_H // 2
    for y, line in enumerate(letter.cells):
        for x, cell in enumerate(line):
            char, fg, bg = seal_stamp.block(cell)
            x0, y0 = x * CELL_W, y * CELL_H
            x1, y1 = x0 + CELL_W - 1, y0 + CELL_H - 1
            if bg is not None:
                ops.append(("rect", x0, y0, x1, y1, rgb(bg)))
            if char == "▀":
                ops.append(("rect", x0, y0, x1, y0 + half - 1, rgb(fg)))
            elif char == "▄":
                ops.append(("rect", x0, y0 + half, x1, y1, rgb(fg)))
            elif char != " ":
                ops.append(("text", x0 + CELL_W // 2, y0 + half, char, rgb(fg), y == 1))
    return ops


# The faces `font` tries, in order, as `(name, regular, bold, regular index,
# bold index)`: DejaVu Sans Mono where a Linux runner has it, Menlo on macOS,
# Consolas on Windows. The hand-drawn seal used Menlo, which is macOS-only,
# which is why this is a chain rather than a path.
FACES = (
    (
        "DejaVu Sans Mono",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        0,
        0,
    ),
    (
        "Menlo",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Menlo.ttc",
        0,
        1,
    ),
    (
        "Consolas",
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\consolab.ttf",
        0,
        0,
    ),
)


def font(image_font):
    """`(regular, bold, name)`: the first face in `FACES` that loads at
    `FONT_SIZE`, its bold where one loads and its regular where not, else
    Pillow's own default at that size. `image_font` is `PIL.ImageFont`,
    handed in so this module imports Pillow in `png` alone. `name` is what
    the log prints, because a runner's font is a fact nobody wrote down
    (`questions.md` Q11)."""
    for name, regular, bold, at, bold_at in FACES:
        try:
            face = image_font.truetype(regular, FONT_SIZE, index=at)
        except OSError:
            continue
        try:
            heavy = image_font.truetype(bold, FONT_SIZE, index=bold_at)
        except OSError:
            heavy = face
        return face, heavy, name
    face = image_font.load_default(size=FONT_SIZE)
    return face, face, "Pillow's default"


def png(ops, dimensions, path):
    """Write `ops` as an RGBA PNG of `dimensions` at `path`, transparent
    where nothing is laid, and answer the name of the font it drew with."""
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    pen = ImageDraw.Draw(image)
    regular, bold, name = font(ImageFont)
    for op in ops:
        if op[0] == "rect":
            _, x0, y0, x1, y1, colour = op
            pen.rectangle([x0, y0, x1, y1], fill=colour)
        else:
            _, cx, cy, char, colour, heavy = op
            face = bold if heavy else regular
            pen.text((cx, cy), char, fill=colour, font=face, anchor="mm")
    image.save(path, format="PNG")
    return name
