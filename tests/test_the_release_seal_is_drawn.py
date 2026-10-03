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
    over the halves it covers, in order, the way a raster would take it.
    A rectangle that does not start and end on a half's edge is refused,
    because a half that bleeds a pixel row into its neighbour is a colour
    this map would not see."""
    cw, ch = mod.CELL_W, mod.CELL_H
    halves, text = {}, {}
    for op in ops:
        if op[0] == "rect":
            _, x0, y0, x1, y1, rgb = op
            assert x0 % cw == 0 and (x1 + 1) % cw == 0, op
            assert y0 % (ch // 2) == 0 and (y1 + 1) % (ch // 2) == 0, op
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
    that carries a character other than a space, some pixel is the cell's
    ink exactly, which is stronger than the frame's *the darkest pixel is
    nearer the ink than the parchment*: that one passed with the ink's red
    and green swapped, measured with `bin/mutation-check` over `rgb`'s cube
    levels, because every stroke at this size covers whole pixels in both
    fonts measured, Menlo and Pillow's default. The font the run used is one `font`
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
    for y, line in enumerate(letter.cells):
        for x, cell in enumerate(line):
            top, bottom, said = expected(stamp, cell)
            # A half's outer row always, and its inner row where no glyph
            # can reach it, so a half one pixel row short or long is seen.
            rows = [(top, y * ch), (bottom, y * ch + ch - 1)]
            if not said:
                rows += [(top, y * ch + ch // 2 - 1), (bottom, y * ch + ch // 2)]
            for want, row in rows:
                got = pixels[x * cw + cw // 2, row]
                if want is None:
                    assert got[3] == 0, (x, y, got)
                else:
                    assert got == (*want, 255), (x, y, got, want)
            if said and said[0] != " ":
                inked = {
                    pixels[a, b]
                    for a in range(x * cw, x * cw + cw)
                    for b in range(y * ch, y * ch + ch)
                }
                assert (*said[1], 255) in inked, (x, y, said)


def test_the_seal_module_imports_without_pillow(monkeypatch):
    """Pillow is imported inside `png` alone, so the rows, the alt text and
    `paint` load on an interpreter without it, and so does the module the
    publishing step imports before it knows whether a draw is possible."""
    monkeypatch.setitem(sys.modules, "PIL", None)
    mod = seal()
    assert callable(mod.paint) and callable(mod.png)


# --- S8: the rows are fixed and fit -----------------------------------------

GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")


def test_the_rows_are_the_fixed_set_in_order_and_fit_the_panel():
    """S8. `release_rows` returns the fixed label set in order, the tag's
    continuation carrying `main`. Every label fits `seal_stamp.letter`'s
    eight-wide label column -- `deferred` is exactly eight, which is the only
    reason the column looks set by it -- and no value is wider than
    `broad_gate.PANEL_VALUE_WIDTH`. A count of 0 still draws its row."""
    mod = seal()
    rows = mod.release_rows("1.2.3", "aaa11111bbbb", 10, 0, (7003, 66), (10, 27, 6, 13))
    assert rows == [*ROWS[:4], ("issues", "0 closed"), *ROWS[5:]], rows
    assert all(len(label) <= 8 for label in mod.LABELS), mod.LABELS
    assert [label for label, _ in rows if label] == list(mod.LABELS)
    width = load(GATE, "broad_gate_for_the_release_rows").PANEL_VALUE_WIDTH
    assert mod.PANEL_VALUE_WIDTH == width == 23
    assert all(len(value) <= width for _, value in rows), rows


def test_a_suite_wider_than_the_value_column_moves_skipped_to_its_own_row():
    """S8, `questions.md` Q6. `7003 passed, 66 skipped` is exactly 23; a
    five-digit suite is 25, so `S skipped` moves under `P passed` on a
    continuation row rather than being cut at the frame. Seen red against
    the rows that wrote the value whole."""
    mod = seal()
    rows = mod.release_rows("1.2.3", "aaa11111", 1, 1, (10003, 166), (1, 1, 0, 0))
    at = [label for label, _ in rows].index("suite")
    assert rows[at : at + 2] == [("suite", "10003 passed"), ("", "166 skipped")]
    assert ("suite", "7003 passed, 66 skipped") in mod.release_rows(
        "1.2.3", "aaa11111", 1, 1, (7003, 66), (1, 1, 0, 0)
    )


def test_a_chain_count_nobody_could_read_says_so_and_keeps_its_row():
    """S8, S10, `questions.md` Q8. A chain count that is None was not read:
    its row stays and says `not read`, never dropped and never 0. One issue
    and one round are singular."""
    mod = seal()
    rows = dict(
        (label, value)
        for label, value in mod.release_rows(
            "1.2.3", "aaa11111", 1, 1, (5, 0), (None, None, None, None)
        )
        if label
    )
    assert rows["items"] == rows["capped"] == rows["deferred"] == "not read"
    # Each row that needs two counts says `not read` when either is missing.
    half = dict(mod.release_rows("1.2.3", "aaa11111", 1, 1, (5, 0), (1, None, 0, 0)))
    assert half["items"] == "not read", half
    labels = dict(
        mod.release_rows("1.2.3", "aaa11111", 1, 1, (5, 0), (None, None, 2, None))
    )
    assert labels["capped"] == "not read", labels
    one = dict(mod.release_rows("1.2.3", "aaa11111", 1, 1, (5, 0), (1, 1, 0, 1)))
    assert one["items"] == "1 . 1 round" and one["deferred"] == "1 issue", one
    assert one["capped"] == "0 of 1", one


# --- S9: the suite counts come from JUnit -----------------------------------

JUNIT = """<?xml version="1.0" encoding="utf-8"?>
<testsuites name="pytest tests">{suites}</testsuites>
"""
SUITE = (
    '<testsuite name="pytest" errors="{errors}" failures="{failures}" '
    'skipped="{skipped}" tests="{tests}" time="1.0" '
    'timestamp="2026-01-02T00:00:00" hostname="example">'
    '<testcase classname="tests.test_x" name="test_y" time="0.1" />'
    "</testsuite>"
)


def junit(tmp_path, *suites):
    path = tmp_path / "suite.xml"
    path.write_text(
        JUNIT.format(
            suites="".join(
                SUITE.format(tests=t, failures=f, errors=e, skipped=s)
                for t, f, e, s in suites
            )
        ),
        encoding="utf-8",
    )
    return str(path)


def test_the_suite_counts_are_read_from_pytests_junit_file(tmp_path):
    """S9. Passed is `tests - failures - errors - skipped`, in the shape
    pytest writes, and more than one `testsuite` is summed."""
    mod = seal()
    assert mod.suite_counts(junit(tmp_path, (7069, 0, 0, 66))) == (7003, 66)
    assert mod.suite_counts(junit(tmp_path, (10, 0, 0, 2), (5, 0, 0, 1))) == (12, 3)


@pytest.mark.parametrize(
    "text",
    [
        "not xml at all",
        "<testsuites></testsuites>",
        '<testsuites><testsuite tests="x" failures="0" errors="0" skipped="0"/>'
        "</testsuites>",
    ],
    ids=["unparsable", "no suite", "not a number"],
)
def test_a_junit_file_that_cannot_be_read_is_a_failure_never_a_zero(tmp_path, text):
    """S9. A file that does not parse, holds no suite or a count that is not
    a number raises, so the seal falls back (S2) rather than drawing 0."""
    path = tmp_path / "suite.xml"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        seal().suite_counts(str(path))
    with pytest.raises(OSError):
        seal().suite_counts(str(tmp_path / "absent.xml"))


@pytest.mark.parametrize(
    "failed", [(10, 1, 0, 0), (10, 0, 1, 0)], ids=["failure", "error"]
)
def test_a_suite_that_did_not_pass_is_not_sealed(tmp_path, failed):
    """S9. A failure or an error in the file raises: a `SEALED` above a red
    suite would say something false."""
    with pytest.raises(ValueError):
        seal().suite_counts(junit(tmp_path, failed))


# --- S10: the chain rows read the tree at the tag ---------------------------

ROUTING = """| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Branch | {branch} |
"""
ROUND = """# round {n}

## Verdicts

| # | Verdict | Grounds |
|---|---|---|
{rows}
"""


def tree(tmp_path, branch="feat/12-an-item", verdicts=()):
    """A repository root holding one work item that declares `branch`, with
    one round record per entry of `verdicts`, each a list of verdict cells."""
    item = tmp_path / "seal" / "specs" / "1700000000-an-item"
    (item / "rounds").mkdir(parents=True)
    (item / "routing.md").write_text(ROUTING.format(branch=branch), encoding="utf-8")
    for n, cells in enumerate(verdicts, 1):
        rows = "\n".join(f"| {i} | {cell} | why |" for i, cell in enumerate(cells, 1))
        (item / "rounds" / f"round-{n}.md").write_text(
            ROUND.format(n=n, rows=rows), encoding="utf-8"
        )
    return str(tmp_path)


def pr(number, branch, *labels):
    return {
        "number": number,
        "headRefName": branch,
        "labels": [{"name": name} for name in labels],
    }


def test_the_chain_rows_count_items_rounds_capped_and_deferred(tmp_path):
    """S10. One work item declaring the pull request's branch, three rounds
    whose verdicts defer #12, then #13 and #14, then a file: one item, three
    rounds, one capped, three distinct issues. A pull request no declaration
    names is not an item, and its label still counts."""
    root = tree(
        tmp_path,
        verdicts=[
            ["fixed", "deferred #12"],
            [
                "**deferred** #13, #14",
                "answered, and #99 was deferred by another round",
            ],
            ["deferred seal/follow-up.md", "deferred #12"],
        ],
    )
    pulls = [
        pr(20, "feat/12-an-item", "chain: capped"),
        pr(21, "fix/nobody-declared-this"),
    ]
    assert seal().chain_counts(root, pulls) == (1, 3, 1, 3)


def test_a_deferred_count_nobody_could_read_is_none_and_the_log_says_why(
    tmp_path, capsys
):
    """S10, `questions.md` Q8. A round record whose verdict table cannot be
    read leaves the deferred count None, which the row shows as `not read`,
    and the log names the file; the items and rounds it could count stand."""
    root = tree(tmp_path, verdicts=[["deferred #12"]])
    record = tmp_path / "seal" / "specs" / "1700000000-an-item" / "rounds"
    (record / "round-2.md").write_text("# round 2\n\nno verdicts\n", encoding="utf-8")
    counts = seal().chain_counts(root, [pr(20, "feat/12-an-item")])
    assert counts == (1, 2, 0, None), counts
    out = capsys.readouterr().out
    assert "round-2.md" in out and "deferred" in out, out


def test_readers_that_will_not_load_leave_every_tree_row_unread(
    tmp_path, monkeypatch, capsys
):
    """S10. Where the shared readers cannot be loaded, the three tree rows are
    None and the log says why; capped is read from the labels alone."""
    mod = seal()

    def broken(*_):
        raise ImportError("no reader")

    monkeypatch.setattr(mod, "readers", broken)
    counts = mod.chain_counts(
        tree(tmp_path), [pr(20, "feat/12-an-item", "chain: capped")]
    )
    assert counts == (None, None, 1, None), counts
    assert "no reader" in capsys.readouterr().out


# --- S11: the alt text says what the image says -----------------------------


def test_the_alt_text_is_one_sentence_carrying_every_value():
    """S11. One sentence in the shape of 0.17.0's hand-written alt text,
    carrying every value of the rows, with no `]` and no line break, so the
    Markdown image it sits in cannot end early."""
    text = seal().alt_text(ROWS)
    assert text == (
        "The 1.2.3 release seal: SEALED v1.2.3 at aaa11111 on main, 10 pull "
        "requests merged, 11 issues closed, the suite at 7003 passed and 66 "
        "skipped, 10 work items over 27 review rounds, 6 of them capped, 13 "
        "issues deferred"
    ), text
    unread = seal().release_rows("1.2.3", "aaa11111", 1, 1, (5, 0), (None,) * 4)
    text = seal().alt_text(unread)
    assert "work items not read" in text and "deferred not read" in text, text
    assert "]" not in text and "\n" not in text
    # A value carrying either cannot end the image early.
    odd = [(label, f"{value}]\n[") for label, value in ROWS]
    assert not set("[]\n") & set(seal().alt_text(odd))
