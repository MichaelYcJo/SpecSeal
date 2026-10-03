"""The release seal is drawn and attached at publish time (#718).

Work item 1790993139. The tag push publishes the note as it always did; a
second job then runs the suite at the tag, draws one seal for the release from
`seal_stamp.compose`'s letter, attaches it, and puts it where the note's glance
table stood. Any failure leaves the note as it was.

This module holds `.github/scripts/release_seal.py`: the drawing and its pin
against the terminal form (S6, S7), the rows and their sources (S8-S11), and
the publishing path with every way it can fail (S1-S5, S12). The pixel case
needs Pillow, which `bin/test` installs; the case that pins `paint` against
`block` imports nothing beyond the standard library.

**The colours here are not read from `release_seal.rgb`.** A case that asked
the code for the expected colour would agree with whatever the code says, so
`XTERM` below holds the four codes the sheet uses as xterm defines them, the
values `seal_stamp.py`'s own comments give.
"""

import importlib.util
import os
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "release_seal.py")
STAMP = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")

# The four 256-colour codes the sheet uses, as xterm's table gives them, and
# as `seal_stamp.py` states them beside `PARCHMENT`, `SHEET_EDGE`, `INK` and
# `TITLE`.
XTERM = {
    230: (255, 255, 215),
    187: (215, 215, 175),
    94: (135, 95, 0),
    124: (175, 0, 0),
}

# A release's rows in the shape `release_rows` returns. The version is the
# illustrative one `tests/test_release_hygiene.py` exempts; the rest are
# neutral numbers in the widths a real release has.
ROWS = [
    ("SEALED", "v1.2.3"),
    ("tag", "aaa11111"),
    ("", "main"),
    ("PRs", "10 merged"),
    ("issues", "11 closed"),
    ("suite", "7003 passed, 66 skipped"),
    ("items", "10 . 27 rounds"),
    ("capped", "6 of 10"),
    ("deferred", "13 issues"),
]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def seal():
    return load(SCRIPT, "specseal_release_seal_for_tests")


def expected(stamp, cell):
    """`(top, bottom, text)` for one cell as `block` describes it, through
    `XTERM` rather than the code under test: each half's colour or None, and
    `(character, ink)` where something is written."""

    def colour(c):
        return None if c is None else XTERM[c] if isinstance(c, int) else c

    ch, fg, bg = stamp.block(cell)
    if cell[2]:
        return colour(bg), colour(bg), (ch, colour(fg))
    if ch == "▀":
        return colour(fg), colour(bg), None
    if ch == "▄":
        return colour(bg), colour(fg), None
    return colour(bg), colour(bg), None


def painted(mod, ops):
    """`{(x, y): [top, bottom]}` over the cells the ops cover, and
    `{(x, y): (character, colour, bold)}` for the text: each rectangle laid
    over the halves it covers, in order, the way a raster would take it."""
    cw, ch = mod.CELL_W, mod.CELL_H
    halves, text = {}, {}
    for op in ops:
        if op[0] == "rect":
            _, x0, y0, x1, y1, rgb = op
            for y in range(y0 // (ch // 2), (y1 + 1) // (ch // 2)):
                for x in range(x0 // cw, (x1 + 1) // cw):
                    halves.setdefault((x, y // 2), [None, None])[y % 2] = rgb
        else:
            _, cx, cy, char, rgb, bold = op
            text[(cx // cw, cy // ch)] = (char, rgb, bold)
    return halves, text


# --- S7: `rgb` is xterm's table ---------------------------------------------


def test_rgb_is_xterms_table_and_a_triple_passes_through():
    """S7. The four codes the sheet uses map to xterm's values; a triple is
    returned as it is; a code from the sixteen system colours, which the
    sheet never uses and whose values a terminal chooses, is refused."""
    mod = seal()
    assert {code: mod.rgb(code) for code in XTERM} == XTERM
    assert mod.rgb((168, 26, 30)) == (168, 26, 30)
    assert mod.rgb(16) == (0, 0, 0) and mod.rgb(231) == (255, 255, 255)
    assert mod.rgb(232) == (8, 8, 8) and mod.rgb(255) == (238, 238, 238)
    for code in (0, 15):
        with pytest.raises(ValueError):
            mod.rgb(code)


# --- S6: the PNG carries the terminal form's colours ------------------------


def test_paint_lays_every_cell_in_the_colours_block_gives_it():
    """S6, the half that needs no third-party module. For every cell of
    `compose(ROWS, DEFAULT_SCALE)`, the rectangles `paint` lays over its two
    halves are the colours `block` gives them, a half `block` leaves empty is
    covered by nothing, and every written character but a space is drawn
    once, in its ink, bold on the title line alone. Seen red by swapping two
    codes in `rgb`'s table."""
    mod = seal()
    stamp = load(STAMP, "seal_stamp_for_the_release_seal")
    letter = stamp.compose(ROWS, stamp.DEFAULT_SCALE)
    halves, text = painted(mod, mod.paint(letter))
    seen = 0
    for y, line in enumerate(letter.cells):
        for x, cell in enumerate(line):
            top, bottom, said = expected(stamp, cell)
            assert halves.get((x, y), [None, None]) == [top, bottom], (x, y, cell)
            if said and said[0] != " ":
                assert text.get((x, y)) == (*said, y == 1), (x, y, cell)
                seen += 1
            else:
                assert (x, y) not in text, (x, y, cell)
    assert seen == len(text) and seen > 0
    assert mod.size(letter) == (
        max(len(line) for line in letter.cells) * mod.CELL_W,
        len(letter.cells) * mod.CELL_H,
    )


@pytest.mark.parametrize("faces", ["the chain", "none"])
def test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted(
    tmp_path, monkeypatch, faces
):
    """S6, the pixel half. The PNG `png` writes from the fixed rows is
    decoded, and each half of each cell is sampled on its outer row at the
    cell's centre column, away from where a glyph is drawn: the colour
    `block` gives that half, or alpha 0 where it gives none. In every cell
    that carries a character other than a space, the darkest pixel is nearer
    the cell's ink than the parchment. The font the run used is one `font`
    names, and it is printed for a run under `-s` (`questions.md` Q11; the
    publishing step logs it at the tag). Seen red by swapping two codes in
    `rgb`'s table. Run twice: with the face chain as it is, and with no face
    loading, so Pillow's own default -- the font a runner with none of the
    three draws with -- is held to the same pin."""
    from PIL import Image

    mod = seal()
    if faces == "none":
        monkeypatch.setattr(mod, "FACES", ())
    stamp = load(STAMP, "seal_stamp_for_the_pixels")
    letter = stamp.compose(ROWS, stamp.DEFAULT_SCALE)
    path = tmp_path / "seal.png"
    used = mod.png(mod.paint(letter), mod.size(letter), str(path))
    print(f"font: {used}")
    assert used in {face[0] for face in mod.FACES} | {"Pillow's default"}, used
    image = Image.open(path)
    assert image.mode == "RGBA" and image.size == mod.size(letter)
    pixels = image.load()
    cw, ch = mod.CELL_W, mod.CELL_H
    parchment = XTERM[stamp.PARCHMENT]

    def far(a, b):
        return sum((p - q) ** 2 for p, q in zip(a, b, strict=True))

    for y, line in enumerate(letter.cells):
        for x, cell in enumerate(line):
            top, bottom, said = expected(stamp, cell)
            for want, row in ((top, y * ch), (bottom, y * ch + ch - 1)):
                got = pixels[x * cw + cw // 2, row]
                if want is None:
                    assert got[3] == 0, (x, y, got)
                else:
                    assert got == (*want, 255), (x, y, got, want)
            if said and said[0] != " ":
                darkest = min(
                    (
                        pixels[a, b][:3]
                        for a in range(x * cw, x * cw + cw)
                        for b in range(y * ch, y * ch + ch)
                    ),
                    key=sum,
                )
                assert far(darkest, said[1]) < far(darkest, parchment), (
                    x,
                    y,
                    said,
                    darkest,
                )


def test_the_seal_module_imports_without_pillow(monkeypatch):
    """Pillow is imported inside `png` alone, so the rows, the alt text and
    `paint` load on an interpreter without it, and so does the module the
    publishing step imports before it knows whether a draw is possible."""
    monkeypatch.setitem(sys.modules, "PIL", None)
    mod = seal()
    assert callable(mod.paint) and callable(mod.png)
