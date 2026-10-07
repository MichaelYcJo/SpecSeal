"""The release seal is drawn and attached at publish time (#718).

Work item 1790993139. The tag push publishes the note as it always did; a
second job then runs the suite at the tag, draws one seal for the release,
attaches it, and puts it where the note's glance table stood. Any failure
leaves the note as it was.

Since #832 (work item 1791270164) the seal is the owner's own SVG,
`.github/scripts/release-seal.svg`, rasterised by `rsvg-convert` at twice
its display size. It used to be the terminal stamp painted cell for cell,
which is the staircase that ticket opened on.

This module holds `.github/scripts/release_seal.py`: the SVG and its
rasteriser (S6), the rows and their sources (S8-S11), and the publishing path
with every way it can fail (S1-S5, S9, S12). The one case that runs
`rsvg-convert` skips where it is not installed, and reads the PNG with
Pillow, which `bin/test` installs; every other case runs a stand-in for the
binary and imports nothing beyond the standard library.

**The colours here are not read from the SVG through the code under test.**
`LAYERS` and `RED` hold what the owner's file carried, written out, so a case
cannot agree with whatever the tree's copy happens to say.
"""

import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ElementTree

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "release_seal.py")
SVG = os.path.join(ROOT, ".github", "scripts", "release-seal.svg")
NS = "{http://www.w3.org/2000/svg}"

# The owner's three `<text>` layers of the seal's mark, as their file carried
# them: the fill, the opacity (None where the layer had none), and the point
# the glyph was anchored at -- the middle of its advance on `x`, its baseline
# on `y`. The owner drew a §; the tree's copy carries each layer as a `<path>`
# of the seal's placeholder mark, Georgia Bold's S, which #857 replaces.
LAYERS = [
    ("#380709", "0.9", (16.5, 21.5)),
    ("#c42830", None, (16.0, 21.0)),
    ("#e65a61", "0.5", (15.7, 20.7)),
]
# The face of the seal's mark, the layer drawn at full opacity.
RED = (0xC4, 0x28, 0x30)

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


def svg_tree():
    return ElementTree.parse(SVG).getroot()


def points(d):
    """The `(x, y)` pairs of a path's `d`, in order: every command the
    converter writes (`M`, `Q`, `L`, `Z`) takes absolute pairs."""
    numbers = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", d)]
    return list(zip(numbers[::2], numbers[1::2], strict=True))


# --- S6: the PNG is the owner's SVG -----------------------------------------


def test_the_release_seal_svg_is_the_owners_with_its_text_as_paths():
    """S6, the half that needs neither Pillow nor the binary. The tree's SVG
    is the owner's 32 x 32 seal: the radial gradient `sealBg` with its three
    stops, the linear gradient `rimShade`, the wax circle with its rim and
    the pressed groove inside it, and three `<path>` layers of the seal's
    mark in the fills and opacities the owner's three `<text>` layers had.
    The owner's layers drew a §; since the owner's decision of 2026-10-07
    the glyph is the terminal's placeholder mark, Georgia Bold's S, and #857
    replaces it in both. It holds no `<text>`, so the runner looks up no
    font: a fallback serif would draw a different glyph. The three layers
    are one outline, each moved by exactly the offset between the owner's
    anchors, so a layer redrawn from another glyph or put back at another
    point is seen, and the outline stands inside the groove. Seen red before
    the file existed, and by one fill changed."""
    root = svg_tree()
    assert root.tag == f"{NS}svg" and root.get("viewBox") == "0 0 32 32"
    assert not list(root.iter(f"{NS}text")), "the SVG still carries text"
    radial = root.find(f"{NS}defs/{NS}radialGradient[@id='sealBg']")
    assert [(s.get("offset"), s.get("stop-color")) for s in radial] == [
        ("0%", "#931e24"),
        ("70%", "#6e1418"),
        ("100%", "#490b0e"),
    ]
    rim = root.find(f"{NS}defs/{NS}linearGradient[@id='rimShade']")
    assert [s.get("stop-color") for s in rim] == ["#b83238", "#380709"]
    wax, groove = root.findall(f"{NS}circle")
    assert (wax.get("r"), wax.get("fill"), wax.get("stroke")) == (
        "15",
        "url(#sealBg)",
        "url(#rimShade)",
    )
    assert (groove.get("r"), groove.get("stroke"), groove.get("fill")) == (
        "13",
        "#40090c",
        "none",
    )
    layers = root.findall(f"{NS}path")
    assert [(p.get("fill"), p.get("opacity")) for p in layers] == [
        (fill, opacity) for fill, opacity, _ in LAYERS
    ]
    outlines = [points(p.get("d")) for p in layers]
    base, (bx, by) = outlines[1], LAYERS[1][2]
    assert len(base) > 50, "the seal's mark is an outline of curves, not a box"
    for outline, (_, _, (ax, ay)) in zip(outlines, LAYERS, strict=True):
        assert len(outline) == len(base)
        for (x, y), (x0, y0) in zip(outline, base, strict=True):
            assert abs((x - x0) - (ax - bx)) < 0.002, (x, x0)
            assert abs((y - y0) - (ay - by)) < 0.002, (y, y0)
    for x, y in (pair for outline in outlines for pair in outline):
        assert math.hypot(x - 16, y - 16) < 13 - 0.4, (x, y)


def test_the_rasteriser_runs_rsvg_convert_at_two_times_the_display_size(
    monkeypatch, tmp_path
):
    """S6. `rasterise` hands the SVG to `rsvg-convert` at `SEAL_PX` times
    `DENSITY` pixels square, the PNG named after `-o`; the note shows it at
    `SEAL_PX`, so a high-density screen draws it sharp. `SVG` is the file
    beside the script. Seen red before `rasterise` existed, and by the
    density dropped from the size."""
    mod = seal()
    seen = []

    def run(args, **_):
        seen.append(list(args))
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(mod.subprocess, "run", run)
    out = str(tmp_path / "seal.png")
    mod.rasterise(mod.SVG, out)
    assert (mod.SEAL_PX, mod.DENSITY) == (160, 2)
    assert os.path.samefile(mod.SVG, SVG)
    assert seen == [["rsvg-convert", "-w", "320", "-h", "320", mod.SVG, "-o", out]]


@pytest.mark.skipif(
    shutil.which("rsvg-convert") is None,
    reason="rsvg-convert is not installed here; the publishing job installs it",
)
def test_rsvg_convert_draws_the_seal_transparent_round_and_in_its_colours(tmp_path):
    """S6, the pixel half, on the real binary. The PNG `rasterise` writes is
    RGBA and `SEAL_PX * DENSITY` square, clear at its four corners and solid
    at its centre, so it sits on any page background as a disc; somewhere in
    it a pixel is within 8 per channel of the mark's face, `RED`; and the wax
    is lit from the upper left, as the radial gradient centred at 35 % puts
    it, so a point of the field up and left of the mark is lighter than its
    mirror down and right. Seen red by the face's fill changed in the SVG
    (`questions.md` Q11 set the tolerances from this render)."""
    from PIL import Image

    mod = seal()
    out = tmp_path / "seal.png"
    mod.rasterise(mod.SVG, str(out))
    image = Image.open(out)
    side = mod.SEAL_PX * mod.DENSITY
    assert image.mode == "RGBA" and image.size == (side, side)
    pixels = image.load()
    for corner in ((0, 0), (side - 1, 0), (0, side - 1), (side - 1, side - 1)):
        assert pixels[corner][3] == 0, (corner, pixels[corner])
    assert pixels[side // 2, side // 2][3] == 255
    assert any(
        all(abs(have - want) <= 8 for have, want in zip(pixel[:3], RED, strict=True))
        and pixel[3] == 255
        for pixel in (pixels[x, y] for x in range(side) for y in range(side))
    ), "no pixel of the mark's face"

    def at(x, y):
        return sum(pixels[round(x * side / 32), round(y * side / 32)][:3])

    assert at(8, 8) > at(24, 24), (at(8, 8), at(24, 24))


# --- S8: the rows are fixed and fit -----------------------------------------

GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")


def test_the_rows_are_the_fixed_set_in_order_and_fit_the_panel():
    """S8. `release_rows` returns the fixed label set in order, the tag's
    continuation carrying `main`. Every label fits the eight-wide label
    column a dry run prints the rows in -- `deferred` is exactly eight,
    which is the only reason the column looks set by it -- and no value is
    wider than the
    release's own `PANEL_VALUE_WIDTH`, 23. A count of 0 still draws its row.

    The two widths were one number until #832: `broad_gate`'s became 41 for
    the open layout's 80 columns (S5a), and the release's rows are out of
    that work item's scope, so the release keeps 23 and no longer follows
    the gate's."""
    mod = seal()
    rows = mod.release_rows("1.2.3", "aaa11111bbbb", 10, 0, (7003, 66), (10, 27, 6, 13))
    assert rows == [*ROWS[:4], ("issues", "0 closed"), *ROWS[5:]], rows
    assert all(len(label) <= 8 for label in mod.LABELS), mod.LABELS
    assert [label for label, _ in rows if label] == list(mod.LABELS)
    width = load(GATE, "broad_gate_for_the_release_rows").PANEL_VALUE_WIDTH
    assert mod.PANEL_VALUE_WIDTH == 23 < width, (mod.PANEL_VALUE_WIDTH, width)
    assert all(len(value) <= mod.PANEL_VALUE_WIDTH for _, value in rows), rows


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


# --- S9: the suite counts come from the broad gate's record (#869) ----------

SUITE_KEY = "seal-1234567890"


def recorded(tmp_path, *sessions, key=SUITE_KEY, extra=""):
    """A records directory under `tmp_path` holding one file per session,
    each a `session` line carrying `key`, a `test` line per report counted —
    `sessions` are dicts of category to count — and an `end` line with
    nothing stopped. `extra` is written as it is after the last session's
    `test` lines. Returns the directory."""
    directory = tmp_path / "records"
    directory.mkdir(exist_ok=True)
    for n, counts in enumerate(sessions):
        lines = [{"kind": "session", "key": key, "pid": n, "rootdir": str(tmp_path)}]
        for category, count in counts.items():
            outcome = "passed" if category == "passed" else "failed"
            lines += [
                {
                    "kind": "test",
                    "nodeid": f"tests/test_x.py::t{n}_{category}_{i}",
                    "when": "call",
                    "outcome": outcome,
                    "path": str(tmp_path / "tests" / "test_x.py"),
                    "category": category,
                }
                for i in range(count)
            ]
        body = "".join(json.dumps(line) + "\n" for line in lines)
        if n == len(sessions) - 1:
            body += extra
        end = {"kind": "end", "exitstatus": 0, "unplaced": 0, "stopped": []}
        body += json.dumps(end) + "\n"
        (directory / f"{key}-{n}.jsonl").write_text(body, encoding="utf-8")
    return str(directory)


def test_the_suite_counts_are_read_from_the_record_through_the_gates_reader(
    tmp_path,
):
    """S9 and S12 of 1791384158. `(passed, skipped)` are the counts the
    broad gate's own reader and counter give over the sessions carrying the
    key, summed; xfails and xpasses are counted and neither passed nor
    skipped, as on pytest's line."""
    mod = seal()
    directory = recorded(
        tmp_path,
        {"passed": 7000, "skipped": 60, "xfailed": 2},
        {"passed": 69, "skipped": 6, "xpassed": 1},
    )
    assert mod.suite_counts(directory, SUITE_KEY) == (7069, 66)
    assert not hasattr(mod, "ElementTree")


@pytest.mark.parametrize(
    "case",
    [
        "no directory named",
        "no key named",
        "a directory that is not there",
        "no session carries the key",
        "a line that did not parse",
        "a session that stopped part-way",
    ],
)
def test_a_record_that_cannot_vouch_for_the_counts_is_a_failure_never_a_zero(
    tmp_path, case
):
    """S9 and S12. A record nobody can read for the whole suite raises, so
    the seal falls back (S2) rather than drawing a count."""
    directory, key = recorded(tmp_path, {"passed": 10}), SUITE_KEY
    if case == "no directory named":
        directory = ""
    elif case == "no key named":
        key = ""
    elif case == "a directory that is not there":
        directory = str(tmp_path / "absent")
    elif case == "no session carries the key":
        key = "seal-0000000000"
    elif case == "a line that did not parse":
        directory = recorded(tmp_path, {"passed": 10}, extra="{cut off\n")
    elif case == "a session that stopped part-way":
        stopped = tmp_path / "records" / f"{SUITE_KEY}-0.jsonl"
        stopped.write_text(
            stopped.read_text(encoding="utf-8").replace(
                '"stopped": []', '"stopped": [{"by": "failures", "what": "x"}]'
            ),
            encoding="utf-8",
        )
    said = {
        "no directory named": "SUITE_RECORDS names no directory",
        "no key named": "SUITE_KEY names no key",
        "a directory that is not there": "carries the key",
        "no session carries the key": "carries the key",
        "a line that did not parse": "did not parse",
        "a session that stopped part-way": "stopped part-way",
    }[case]
    with pytest.raises(ValueError, match=said):
        seal().suite_counts(directory, key)


@pytest.mark.parametrize("category", ["failed", "error"])
def test_a_suite_that_did_not_pass_is_not_sealed(tmp_path, category):
    """S9. A failure or an error in the record raises: a `SEALED` above a red
    suite would say something false."""
    directory = recorded(tmp_path, {"passed": 10, category: 1})
    with pytest.raises(ValueError, match="did not pass"):
        seal().suite_counts(directory, SUITE_KEY)


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


def rsvg_convert(how="draws"):
    """`subprocess.run` as `rasterise` meets it: `draws` writes a PNG's
    eight-byte signature where `-o` points, `fails` exits 1 with what
    librsvg prints for a file it cannot read, and `missing` raises what
    `subprocess.run` raises for a command that is not on `PATH`.

    Every other command goes to the real `subprocess.run`, because the patch
    reaches the module the whole process shares: the round-record readers
    ask `git rev-parse --git-common-dir` where the `seal/` root is, and a
    stand-in that answered them as `rsvg-convert` failed every draw."""
    real = subprocess.run

    def run(args, **kwargs):
        if args[0] != "rsvg-convert":
            return real(args, **kwargs)
        if how == "missing":
            raise FileNotFoundError(2, "No such file or directory", args[0])
        if how == "fails":
            return subprocess.CompletedProcess(
                args, 1, stdout="", stderr="rsvg-convert: Error reading SVG\n"
            )
        with open(args[args.index("-o") + 1], "wb") as handle:
            handle.write(b"\x89PNG\r\n\x1a\n")
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    return run


def wired(monkeypatch, tmp_path, body=None, fails=(), pulls=PULLS, rsvg="draws", **env):
    """The seal with a fixture suite, a fixture tree, a stand-in for
    `rsvg-convert` and no route to GitHub."""
    mod = seal()
    hub = GitHub(mod, note(pulls) if body is None else body, fails)
    monkeypatch.setattr(mod.subprocess, "run", rsvg_convert(rsvg))
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
    if "SUITE_RECORDS" not in defaults:
        defaults["SUITE_RECORDS"] = recorded(tmp_path, {"passed": 7003, "skipped": 66})
    defaults.setdefault("SUITE_KEY", SUITE_KEY)
    for key in ("DRY_RUN", "SEAL_PNG"):
        monkeypatch.delenv(key, raising=False)
    for key, value in defaults.items():
        monkeypatch.setenv(key, value)
    return mod, hub


def test_the_seal_replaces_the_glance_table_and_is_attached(monkeypatch, tmp_path):
    """S1, S7. The PNG is uploaded as `seal.png`, and the edited note is the
    published one with its glance block replaced by the heading, the image
    at the release-download URL with its alt text and its display width
    `SEAL_PX`, a blank line and one line of the counts -- every other byte
    unchanged. The PNG is `DENSITY` times that width, so the width is what
    keeps it from showing twice its size. Seen red before `main` existed,
    and before the image carried a width."""
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
    sealed = publisher.sealed_glance(
        image, mod.alt_text(rows), mod.SEAL_PX, work, closed, people
    )
    assert body == note().replace(publisher.glance(work, closed, people), sealed)
    assert body.startswith(
        f'### 📊 At a glance\n\n<img src="{image}" alt="The 1.2.3 release seal: '
        "SEALED v1.2.3 at aaa11111 on main, 2 pull requests merged, 2 issues "
        "closed, the suite at 7003 passed and 66 skipped, 1 work item over 1 "
        'review round, 1 of them capped, 1 issue deferred" width="160">\n\n'
        "🔀 Pull requests **2** · ✅ Issues closed **2** · 🙌 Outside contributors **1**"
        "\n\n### ✨ Features"
    ), body[:600]
    assert hub.calls.index(upload) < hub.calls.index(edit)


# What each failure's reason says, so a case that stopped at an EARLIER
# guard than the one it is named for fails rather than passing on the wrong
# reason.
REASONS = {
    "the suite step failed": "ended failure",
    "no record carries the key": "the suite's counts cannot be read: no record under",
    "a line of the record did not parse": "did not parse as the recorder's",
    "a session of the suite stopped part-way": "sessions stopped part-way",
    "the suite counts a failure": "did not pass: 1 failed and 0 errors",
    "the suite counts an error": "did not pass: 0 failed and 1 errors",
    "rsvg-convert is not installed": "rsvg-convert is not installed",
    "rsvg-convert fails": "rsvg-convert failed: rsvg-convert: Error reading SVG",
    "the SVG is not there": "the seal's SVG is not there",
    "gh pr list fails": "gh pr list could not list",
    "gh release view fails": "gh release view failed",
    "gh release upload fails": "gh release upload failed",
    "the glance table is not there": "not in the note exactly once",
    "the glance table is there twice": "not in the note exactly once",
    "gh release edit fails": "gh release edit failed",
    "a module will not load": "ImportError: no publisher",
}


@pytest.mark.parametrize(
    "case",
    [
        "the suite step failed",
        "no record carries the key",
        "a line of the record did not parse",
        "a session of the suite stopped part-way",
        "the suite counts a failure",
        "the suite counts an error",
        "rsvg-convert is not installed",
        "rsvg-convert fails",
        "the SVG is not there",
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
    edit is the call that failed. Seen red by removing the guard each pins;
    the three `rsvg-convert` cases (#832, S9) by `rasterise` letting the
    error through unnamed, and by it not checking the exit code."""
    env, fails, body, pulls, rsvg = {}, (), None, PULLS, "draws"
    if case == "rsvg-convert is not installed":
        rsvg = "missing"
    elif case == "rsvg-convert fails":
        rsvg = "fails"
    elif case == "the suite step failed":
        env["SUITE_OUTCOME"] = "failure"
    elif case == "no record carries the key":
        env["SUITE_KEY"] = "seal-0000000000"
    elif case == "a line of the record did not parse":
        env["SUITE_RECORDS"] = recorded(tmp_path, {"passed": 10}, extra="{cut off\n")
    elif case == "a session of the suite stopped part-way":
        env["SUITE_RECORDS"] = recorded(tmp_path, {"passed": 10}, extra="")
        stopped = tmp_path / "records" / f"{SUITE_KEY}-0.jsonl"
        stopped.write_text(
            stopped.read_text(encoding="utf-8").replace(
                '"exitstatus": 0', '"exitstatus": 2'
            ),
            encoding="utf-8",
        )
    elif case == "the suite counts a failure":
        env["SUITE_RECORDS"] = recorded(tmp_path, {"passed": 10, "failed": 1})
    elif case == "the suite counts an error":
        env["SUITE_RECORDS"] = recorded(tmp_path, {"passed": 10, "error": 1})
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
        rsvg=rsvg,
        **env,
    )
    if case == "the SVG is not there":
        monkeypatch.setattr(mod, "SVG", str(tmp_path / "absent.svg"))
    elif case == "a module will not load":

        def publisher():
            raise ImportError("no publisher")

        monkeypatch.setattr(mod, "publisher", publisher)
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
    assert 'alt="The 1.2.3 release seal: SEALED v1.2.3 at aaa11111' in out, out
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
    # #647: the suite at the tag collects the table walker's case, which
    # imports the pinned renderer.
    assert runner.CMARKGFM in installs[0], installs


def test_a_refused_gh_or_git_call_is_a_reason_naming_the_call(monkeypatch):
    """S2's inputs. `gh` answers a call's stdout and turns a non-zero exit
    into `Refused` naming the call and what it printed; `tagged` does the
    same for the commit a tag names. Both are what the failure cases above
    stand in for."""

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
    names the case that pins the fallback. Since #832 it says the seal is
    the owner's SVG drawn by `rsvg-convert`, and no longer that it is drawn
    from the broad gate's letter; seen red by the old sentence put back."""
    text = flat("docs", "branch-and-release.md")
    bullet = text.split("**The release note publishes itself.**", 1)[1].split(
        "- **", 1
    )[0]
    assert "**Then the release's seal is attached** (#718)" in bullet
    assert (
        "draws the owner's seal from `.github/scripts/release-seal.svg` with "
        "`rsvg-convert`, which the job installs (#832)" in bullet
    )
    assert "letter" not in bullet
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
    # Round 2's ⬜ 12: the reasons match the refusal's three causes.
    assert "published without one" in box
    assert "the pull requests moved between the two lists" in box
    # #832: the seal is drawn by `rsvg-convert`, so the box names the binary
    # among the reasons and the hand-drawn route needs a machine that has it.
    # Seen red against the box as #718 left it.
    assert "`rsvg-convert` was not installed or could not draw the SVG" in box
    assert "from a checkout at the tag on a machine with `rsvg-convert`" in box
