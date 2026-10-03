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


def test_a_tree_whose_records_are_not_there_is_not_read_never_zero(tmp_path, capsys):
    """S10, `questions.md` Q1 (round 1's 🔴 1). A root with no declaration --
    the records moved by #715, or retired before the tag -- leaves the three
    tree rows None, and the log says why; capped is read from the labels
    alone. Seen red at `e01e1b12`, which drew `(0, 0, 1, 0)` and said nothing."""
    counts = seal().chain_counts(
        str(tmp_path), [pr(20, "feat/12-an-item", "chain: capped")]
    )
    assert counts == (None, None, 1, None), counts
    assert "not read" in capsys.readouterr().out
    # With no capped pull request to miss, the empty tree alone is the reason.
    counts = seal().chain_counts(str(tmp_path), [pr(20, "feat/12-an-item")])
    assert counts == (None, None, 0, None), counts
    assert "no routing.md" in capsys.readouterr().out


def test_a_capped_pull_request_with_no_work_item_leaves_the_tree_rows_unread(
    tmp_path, capsys
):
    """S10 (round 1's 🔴 1). A pull request labelled `chain: capped` was
    reviewed, so one that resolves to no declaration makes the item count
    incomplete, and the log names it."""
    root = tree(tmp_path, verdicts=[["deferred #12"]])
    pulls = [pr(20, "feat/12-an-item"), pr(21, "feat/99-retired", "chain: capped")]
    assert seal().chain_counts(root, pulls) == (None, None, 1, None)
    assert "#21" in capsys.readouterr().out


def test_an_unlistable_rounds_leaves_rounds_unread_not_zero(tmp_path, capsys):
    """S10 (round 1's 🟡 2). A `rounds` that is a file holds records nobody
    can count: the rounds row is not read, and the log names it. Seen red at
    `7966a9f9`, which drew `(1, 0, 0, None)`."""
    root = tree(tmp_path)
    item = tmp_path / "seal" / "specs" / "1700000000-an-item"
    (item / "rounds").rmdir()
    (item / "rounds").write_text("# round 1\n", encoding="utf-8")
    assert seal().chain_counts(root, [pr(20, "feat/12-an-item")]) == (1, None, 0, None)
    out = capsys.readouterr().out
    assert "rounds" in out and "not read" in out, out


def test_a_verdict_row_the_table_skipped_leaves_deferred_unread(tmp_path, capsys):
    """S10 (round 1's 🟡 2). `verdict_table` skips a row too short for the
    Verdict column; a deferral in it is a count nobody made, so deferred is
    not read and the log names the record. Seen red at `7966a9f9`, which
    counted 1."""
    root = tree(tmp_path, verdicts=[["deferred #12"]])
    record = (
        tmp_path / "seal" / "specs" / "1700000000-an-item" / "rounds" / "round-1.md"
    )
    record.write_text(record.read_text(encoding="utf-8") + "| 2 |\n", encoding="utf-8")
    assert seal().chain_counts(root, [pr(20, "feat/12-an-item")]) == (1, 1, 0, None)
    assert "round-1.md" in capsys.readouterr().out


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


# --- S1, S2, S3, S12: publishing --------------------------------------------

REPO = "example/repo"
TAG = "v1.2.3"
SHA = "aaa11111bbbbccccddddeeeeffff000011112222"
PUBLISHER = os.path.join(ROOT, ".github", "scripts", "publish_release_note.py")
OWNER = REPO.split("/")[0]
SECTION = "- **A thing that changed.** And what it changes for a reader."


def pull(number, branch, title, body="", *labels, login=OWNER):
    return {
        "number": number,
        "title": title,
        "body": body,
        "author": {"login": login, "is_bot": False},
        "headRefName": branch,
        "labels": [{"name": name} for name in labels],
    }


PULLS = [
    pull(9, "chore/the-fragments", "chore: release 1.2.3 — the gathering"),
    pull(10, "feat/12-an-item", "feat: a thing", "Closes #12", "chain: capped"),
    pull(11, "fix/13-another", "fix: another thing", "Closes #13", login="someone"),
]


class GitHub:
    """`gh` and `git` as the seal calls them: every call recorded in order,
    the note served from `body`, and any verb in `fails` answered with the
    refusal `main` turns into today's note."""

    def __init__(self, mod, body, fails=()):
        self.mod, self.body, self.fails, self.calls = mod, body, set(fails), []

    def gh(self, *args):
        self.calls.append(args)
        verb = args[1] if args[0] == "release" else args[0]
        if verb in self.fails:
            raise self.mod.Refused(f"gh {' '.join(args[:2])} failed: HTTP 502")
        if args[:2] == ("release", "view"):
            import json

            return json.dumps({"body": self.body})
        return ""

    def writes(self, verb):
        return [a for a in self.calls if a[:2] == ("release", verb)]


def note(pulls=PULLS):
    """The note `publish_release_note.release_body` publishes for `pulls`."""
    publisher = load(PUBLISHER, "publish_release_note_for_the_seal")
    return publisher.release_body(SECTION, pulls, OWNER, REPO, TAG)


def wired(monkeypatch, tmp_path, body=None, fails=(), pulls=PULLS, **env):
    """The seal with a fixture suite, a fixture tree and no route to GitHub."""
    mod = seal()
    hub = GitHub(mod, note(pulls) if body is None else body, fails)
    monkeypatch.setattr(mod, "gh", hub.gh)
    monkeypatch.setattr(mod, "tagged", lambda tag: SHA)
    monkeypatch.setattr(mod, "ROOT", tree(tmp_path, verdicts=[["deferred #12"]]))
    publisher = mod.publisher()
    monkeypatch.setattr(
        publisher,
        "merged_pulls",
        lambda repo, version: None if pulls is None else pulls,
    )
    defaults = {"TAG": TAG, "REPO": REPO, "SUITE_OUTCOME": "success"}
    defaults.update(env)
    if "SUITE_XML" not in defaults:
        defaults["SUITE_XML"] = junit(tmp_path, (7069, 0, 0, 66))
    for key in ("DRY_RUN", "SEAL_PNG"):
        monkeypatch.delenv(key, raising=False)
    for key, value in defaults.items():
        monkeypatch.setenv(key, value)
    return mod, hub


def test_the_seal_replaces_the_glance_table_and_is_attached(monkeypatch, tmp_path):
    """S1. The PNG is uploaded as `seal.png`, and the edited note is the
    published one with its glance block replaced by the heading, the image
    at the release-download URL with its alt text, a blank line and one line
    of the counts -- every other byte unchanged. Seen red before `main`
    existed."""
    mod, hub = wired(monkeypatch, tmp_path)
    assert mod.main() == 0
    (upload,) = hub.writes("upload")
    assert upload[:3] == ("release", "upload", TAG)
    assert os.path.basename(upload[3]) == "seal.png" and os.path.isfile(upload[3])
    assert upload[4:] == ("--repo", REPO)
    (edit,) = hub.writes("edit")
    assert edit[:5] == ("release", "edit", TAG, "--repo", REPO)
    body = edit[edit.index("--notes") + 1]
    publisher = load(PUBLISHER, "publish_release_note_for_s1")
    work, closed, people = publisher.tally(PULLS, OWNER)
    rows = mod.release_rows("1.2.3", SHA, 2, 2, (7003, 66), (1, 1, 1, 1))
    image = f"https://github.com/{REPO}/releases/download/{TAG}/seal.png"
    sealed = publisher.sealed_glance(image, mod.alt_text(rows), work, closed, people)
    assert body == note().replace(publisher.glance(work, closed, people), sealed)
    assert body.startswith(
        "### 📊 At a glance\n\n![The 1.2.3 release seal: SEALED v1.2.3 at aaa11111 on "
        "main, 2 pull requests merged, 2 issues closed, the suite at 7003 passed and "
        "66 skipped, 1 work item over 1 review round, 1 of them capped, 1 issue "
        f"deferred]({image})\n\n"
        "🔀 Pull requests **2** · ✅ Issues closed **2** · 🙌 Outside contributors **1**"
        "\n\n### ✨ Features"
    ), body[:600]
    assert hub.calls.index(upload) < hub.calls.index(edit)


# What each failure's reason says, so a case that stopped at an EARLIER
# guard than the one it is named for fails rather than passing on the wrong
# reason.
REASONS = {
    "the suite step failed": "ended failure",
    "the JUnit file is missing": "the suite's counts cannot be read",
    "the JUnit file does not parse": "is not JUnit XML",
    "the suite counts a failure": "did not pass: 1 failed and 0 errors",
    "the suite counts an error": "did not pass: 0 failed and 1 errors",
    "Pillow does not import": "could not be drawn: ModuleNotFoundError",
    "compose raises": "could not be drawn: ValueError",
    "compose exits": "could not be drawn: SystemExit",
    "the PNG writer exits": "could not be drawn: SystemExit",
    "gh pr list fails": "gh pr list could not list",
    "gh release view fails": "gh release view failed",
    "gh release upload fails": "gh release upload failed",
    "the glance table is not there": "not in the note exactly once",
    "the glance table is there twice": "not in the note exactly once",
    "gh release edit fails": "gh release edit failed",
    "a module will not load": "ImportError: no publisher",
}


def broken_compose(mod, exc):
    def compose(*_):
        raise exc

    return compose


@pytest.mark.parametrize(
    "case",
    [
        "the suite step failed",
        "the JUnit file is missing",
        "the JUnit file does not parse",
        "the suite counts a failure",
        "the suite counts an error",
        "Pillow does not import",
        "compose raises",
        "compose exits",
        "the PNG writer exits",
        "gh pr list fails",
        "gh release view fails",
        "gh release upload fails",
        "the glance table is not there",
        "the glance table is there twice",
        "gh release edit fails",
        "a module will not load",
    ],
)
def test_any_failure_leaves_the_note_as_it_was_published(
    monkeypatch, tmp_path, capsys, case
):
    """S2, the case #718's box 2 asks for. Each failure, one at a time: the
    process exits 0, prints a line naming the failure and a `::warning::`
    with the same reason, and calls no `gh release edit` -- except where the
    edit is the call that failed. Seen red by removing the guard each pins."""
    env, fails, body, pulls = {}, (), None, PULLS
    if case == "the suite step failed":
        env["SUITE_OUTCOME"] = "failure"
    elif case == "the JUnit file is missing":
        env["SUITE_XML"] = str(tmp_path / "absent.xml")
    elif case == "the JUnit file does not parse":
        (tmp_path / "bad.xml").write_text("not xml", encoding="utf-8")
        env["SUITE_XML"] = str(tmp_path / "bad.xml")
    elif case == "the suite counts a failure":
        env["SUITE_XML"] = junit(tmp_path, (10, 1, 0, 0))
    elif case == "the suite counts an error":
        env["SUITE_XML"] = junit(tmp_path, (10, 0, 1, 0))
    elif case == "gh pr list fails":
        pulls = None
    elif case == "gh release view fails":
        fails = ("view",)
    elif case == "gh release upload fails":
        fails = ("upload",)
    elif case == "gh release edit fails":
        fails = ("edit",)
    elif case == "the glance table is not there":
        body = note().replace(
            "| ✅ Issues closed | **2** |", "| ✅ Issues closed | **3** |"
        )
    elif case == "the glance table is there twice":
        body = note() + "\n\n" + note().split("\n\n### ✨")[0]
    mod, hub = wired(
        monkeypatch,
        tmp_path,
        body=body if body is not None else (note() if pulls is not None else ""),
        fails=fails,
        pulls=pulls,
        **env,
    )
    if case == "Pillow does not import":
        monkeypatch.setitem(sys.modules, "PIL", None)
    elif case == "compose raises":
        monkeypatch.setattr(
            mod.stamp(), "compose", broken_compose(mod, ValueError("x"))
        )
    elif case == "compose exits":
        monkeypatch.setattr(mod.stamp(), "compose", broken_compose(mod, SystemExit(2)))
    elif case == "a module will not load":

        def publisher():
            raise ImportError("no publisher")

        monkeypatch.setattr(mod, "publisher", publisher)
    elif case == "the PNG writer exits":

        def png(*_):
            raise SystemExit(1)

        monkeypatch.setattr(mod, "png", png)
    assert mod.main() == 0
    out = capsys.readouterr().out.splitlines()
    warnings = [line for line in out if line.startswith("::warning::")]
    assert len(warnings) == 1, out
    reason = warnings[0].removeprefix("::warning::release seal skipped: ")
    assert reason and [line for line in out if line.startswith("no seal: ")] == [
        f"no seal: {reason} -- the note stays as it was published"
    ], out
    assert REASONS[case] in reason, (case, reason)
    edits = hub.writes("edit")
    if case == "gh release edit fails":
        assert len(edits) == 1 and "uploaded" in reason, (edits, reason)
    else:
        assert edits == [], (case, hub.calls)


def test_a_hand_edited_note_is_left_alone_and_nothing_is_uploaded(
    monkeypatch, tmp_path, capsys
):
    """S3. A glance table changed by one character after publication is not
    the generated shape: the note is not edited, the asset is not uploaded,
    and the log says the table was not found."""
    edited = note().replace(
        "| 🔀 Pull requests | **2** |", "| 🔀 Pull requests | **2**  |"
    )
    mod, hub = wired(monkeypatch, tmp_path, body=edited)
    assert mod.main() == 0
    assert hub.writes("upload") == [] and hub.writes("edit") == []
    out = capsys.readouterr().out
    # Round 1's ⬜ 7: the refusal names every way the table can be missing,
    # not a hand edit alone.
    assert (
        "the glance table is not in the note exactly once as `glance` writes it "
        "for this release -- the note was edited after publication, went out "
        "without one, or the pull requests moved between the two lists; nothing "
        "was uploaded"
    ) in out, out


def test_a_dry_run_draws_and_prints_and_writes_nothing(monkeypatch, tmp_path, capsys):
    """S12. `DRY_RUN=1` writes the PNG where `SEAL_PNG` says, prints the rows
    and the edited note, and calls neither `gh release upload` nor
    `gh release edit`."""
    target = tmp_path / "out" / "seal.png"
    target.parent.mkdir()
    mod, hub = wired(
        monkeypatch,
        tmp_path,
        fails=("upload", "edit"),
        DRY_RUN="1",
        SEAL_PNG=str(target),
    )
    assert mod.main() == 0
    assert target.is_file()
    assert hub.writes("upload") == [] and hub.writes("edit") == []
    out = capsys.readouterr().out
    assert "deferred 1 issue" in out and "suite    7003 passed, 66 skipped" in out, out
    assert "![The 1.2.3 release seal: SEALED v1.2.3 at aaa11111" in out, out
    assert "::warning::" not in out, out


def test_the_publishing_workflow_installs_the_pins_the_runner_holds():
    """S16 (#718). The `seal` job's install line carries the parser and
    Pillow exactly as `run_tests.py` pins them, so the suite at the tag and
    the drawing run on the versions every other run of the suite uses."""
    runner = load(
        os.path.join(ROOT, ".github", "scripts", "run_tests.py"), "rt_for_seal"
    )
    with open(
        os.path.join(ROOT, ".github", "workflows", "publish-release.yml"),
        encoding="utf-8",
    ) as handle:
        installs = [
            line.split("run:", 1)[1].split()
            for line in handle
            if "run: pip install" in line
        ]
    assert len(installs) == 1, installs
    assert runner.MARKDOWN_IT in installs[0] and runner.PILLOW in installs[0], installs


def test_a_refused_gh_or_git_call_is_a_reason_naming_the_call(monkeypatch):
    """S2's inputs. `gh` answers a call's stdout and turns a non-zero exit
    into `Refused` naming the call and what it printed; `tagged` does the
    same for the commit a tag names. Both are what the failure cases above
    stand in for."""
    import subprocess

    mod = seal()
    seen = []

    def run(args, **_):
        seen.append(args)
        code = 1 if "edit" in args or "nope" in args[-1] else 0
        return subprocess.CompletedProcess(
            args, code, stdout=f"{SHA}\n", stderr="HTTP 502\n"
        )

    monkeypatch.setattr(mod.subprocess, "run", run)
    assert mod.gh("release", "view", TAG) == f"{SHA}\n"
    with pytest.raises(mod.Refused, match=r"^gh release edit failed: HTTP 502$"):
        mod.gh("release", "edit", TAG, "--notes", "x")
    assert mod.tagged(TAG) == SHA
    assert seen[-1] == ["git", "rev-parse", f"{TAG}^{{commit}}"]
    with pytest.raises(mod.Refused, match=r"^git rev-parse nope failed: HTTP 502$"):
        mod.tagged("nope")


# --- the documents a person reads (contract §14) ----------------------------


def flat(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


def test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it():
    """`docs/branch-and-release.md` §*Every act the release performs once it
    reaches `main`*: the bullet on the note says the seal job runs only on a
    release this run created, edits only a glance table still as generated,
    and cannot turn the release red, and the section's `Enforced by:` line
    names the case that pins the fallback."""
    text = flat("docs", "branch-and-release.md")
    bullet = text.split("**The release note publishes itself.**", 1)[1].split(
        "- **", 1
    )[0]
    assert "**Then the release's seal is attached** (#718)" in bullet
    assert "runs only when this run created the release" in bullet
    assert (
        "only to one whose glance table is still exactly as it was generated" in bullet
    )
    assert "so the seal can never turn the release red" in bullet
    section = text.split("**Every act the release performs once it reaches `main`", 1)[
        1
    ]
    enforced = section.split("Enforced by:", 1)[1].split("###", 1)[0]
    assert (
        "tests/test_the_release_seal_is_drawn.py::"
        "test_any_failure_leaves_the_note_as_it_was_published" in enforced
    )


def test_the_checklist_box_says_where_a_missing_seal_is_explained():
    """`docs/release-checklist.md` §6, the release-note box: it names the
    `seal` job, says its log carries the reason on a `::warning::` line and
    that it never fails the release, and gives the hand-drawn route."""
    text = flat("docs", "release-checklist.md")
    box = text.split("**A GitHub Release exists at `vX.Y.Z`**", 1)[1].split("- [ ]", 1)[
        0
    ]
    assert "the same workflow's `seal` job attaches `seal.png`" in box
    assert "says why on a `::warning::` line" in box
    assert "That job never fails the release." in box
    assert "`DRY_RUN=1 python3 .github/scripts/release_seal.py`" in box
    assert "`gh release upload`" in box
    # Round 1's ⬜ 8: the route draws from the tag's tree and ends at the edit.
    assert "from a checkout at the tag" in box
    assert "then apply the note it prints with `gh release edit --notes-file`" in box
