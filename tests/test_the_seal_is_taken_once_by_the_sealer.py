"""The seal is taken once, by the sealer, and this is what it prints.

Issue #30. Part 1 pins the stamp module, `skills/verify/scripts/seal_stamp.py`:
the disc is computed from a chart, so it cannot be off centre; a letter twin
exists for a console that cannot draw half-blocks, and it has the block form's
footprint; colour is emitted at transitions, never per cell; the panel beside
the disc is data; the chart has a floor; and the failure form carries no
drawing at all, because a picture that says *sealed* beside a word that says
*not* is the two-things-disagreeing defect this repository keeps paying for.

Part 2 pins the gate command, `skills/verify/scripts/broad_gate.py`, and the
`seal` subcommand of `round_record.py`, on fixture repositories built and
driven from Python (`agent-contract` §8): the `Broad gate` row is read and
its absence is a refusal with nothing run; every check runs in order and its
exit code is read directly; a failing test is compared against the base in a
scratch worktree, reactively, and reported as `new` or `failing on base
too`; the stamp prints on success only; and the one write sets the last
record's cell and nothing else, refusing while its `Pass` box is unchecked.

Part 3 — the agent and the owner sentences — arrives with the phase that
builds them.
"""

import argparse
import ast
import importlib.util
import io
import json
import ntpath
import os
import re
import shutil
import subprocess
import sys

import pytest
from conftest import posix_row_shell_or_skip

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
WRAPPER = os.path.join(ROOT, "bin", "seal-stamp")
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
GATE_WRAPPER = os.path.join(ROOT, "bin", "broad-gate")
GENERATOR = os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py")
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")

# The shape `broad_gate.panel` returns since #717: a heading row and `(label,
# value)` pairs, `""` labelling a row that continues the one above, and no
# blank row. A file in the older shape, blanks and all, is drawn by the hook's
# cases in `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`.
# Values are neutral.
ROWS = [
    ("SEALED", ""),
    ("tree", "c46fd2d"),
    ("", "feat/12-a-branch"),
    ("base", "1e2bed9"),
    ("", "origin/base"),
    ("suite", "768 passed, 1 skipped"),
    ("ledger", "187 ok"),
    ("rounds", "4"),
]

SGR = re.compile(r"\x1b\[[0-9;]*m")
HALF_BLOCKS = ("▀", "▄")

# Where a sealed run on a pipe leaves its panel for the hook to draw (#400),
# and the variable naming the session it is left for. Spelled here rather
# than read off the modules, and still held to them: the positive cases below
# find their file through `values_files`, so a directory renamed in the
# module and not here turns those red rather than turning the absence
# checks quietly true.
VALUES_DIR = "specseal-stamp"
SESSION_VAR = "CLAUDE_CODE_SESSION_ID"


def module():
    spec = importlib.util.spec_from_file_location("specseal_seal_stamp", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def wrapper_command(wrapper, args, windows=None):
    """The argv that runs one of `bin/`'s wrapper pairs on this platform.

    `windows` is the platform, defaulting to this one, so BOTH branches can
    be driven from a case on either machine — the lesson round 2's 🟡 14
    landed, applied to the thing that failed CI instead of to a unit.

    `bin/seal-stamp` and `bin/broad-gate` open `#!/usr/bin/env sh`, and a
    shebang is a POSIX kernel's convention: `CreateProcess` reads the file as
    an image and answers *[WinError 193] %1 is not a valid Win32
    application*. Both files ship with a `.cmd` twin for exactly this, and
    `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` says why —
    *a new command means both files or it means one platform*. Running the
    twin through `%COMSPEC% /c` is what a person typing the bare name gets,
    so the cases below exercise the file that ships rather than stepping
    around it.
    """
    if windows is None:
        windows = os.name == "nt"
    if not windows:
        return [wrapper, *args]
    return [os.environ.get("COMSPEC", "cmd.exe"), "/c", f"{wrapper}.cmd", *args]


def run_wrapper(*args, env=None):
    return subprocess.run(
        wrapper_command(WRAPPER, args),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=ROOT,
    )


class Stream:
    """Just enough of a text stream for `pick_shape` to ask its two questions."""

    def __init__(self, encoding, tty):
        self.encoding = encoding
        self._tty = tty

    def isatty(self):
        return self._tty


# --- the twin --------------------------------------------------------------


def visible(line):
    """A line's width as a person sees it: colour codes removed and nothing
    else. The sheet's last cell on a row is a painted space, which `ink`'s
    `rstrip` would take off one form and not the other (#717)."""
    return len(SGR.sub("", line))


@pytest.mark.parametrize("scale", [1.0, 0.9, 0.8, 0.75, None])
def test_the_twin_and_the_block_form_have_equal_width_and_height(scale):
    """S5. A twin that is a different size is a different drawing, and the
    reader on a cp949 console would be looking at something nobody measured.
    Compared row by row on visible width, at full scale, at every rung the
    hook can step down to, and with no disc (#717's A10). The twin's first
    line is the sheet's top, `.---.`, where the block form paints the blank
    first line of parchment between its two edge cells."""
    mod = module()
    blocks = mod.stamp(ROWS, scale=scale, shape=False)
    letters = mod.stamp(ROWS, scale=scale, shape=True)
    assert len(blocks) == len(letters), (
        f"{len(blocks)} block rows against {len(letters)} letter rows at {scale}"
    )
    widths = [(visible(b), visible(t)) for b, t in zip(blocks, letters, strict=True)]
    assert all(b == t for b, t in widths), (
        f"the twin's rows differ in width from the block form's: {widths}"
    )
    top = letters[0]
    assert re.fullmatch(r"\.-+\.", top), (
        f"the twin's first line is not the top: {top!r}"
    )
    assert visible(blocks[0]) == len(top) and not SGR.sub("", blocks[0]).strip(), (
        f"the block form's first line is not blank parchment: {blocks[0]!r}"
    )
    assert not any(SGR.search(line) for line in letters), (
        "the letter twin carries colour codes, which is the one thing the "
        "console it exists for cannot show"
    )
    assert not any(c in line for line in letters for c in HALF_BLOCKS), (
        "the letter twin still carries a half-block character"
    )


def test_a_scale_that_is_not_a_number_is_refused_before_anything_runs():
    """A round 1 record correction. `check_scale` compared with `<` and `>`,
    and NaN compares False with both — so `--scale nan` passed the band, every
    check ran, the cell was written, and `stamp` then raised `ValueError:
    cannot convert float NaN to integer`. `broad_gate.main` catches `Refused`
    alone, so that arrived as a traceback after the write."""
    mod = module()
    refusal = mod.check_scale(float("nan"))
    assert refusal is not None, (
        "a scale that is not a number passes the band and fails after the "
        "cell is written"
    )
    # A round 2 correction. The first repair sent NaN down the below-the-floor
    # branch, so the sentence read *scale nan is under the floor of 0.75*.
    # NaN is not under the floor; it is not on the line at all, and a reader
    # told to raise it raises a number that fails the same way.
    assert "is not a number" in refusal, refusal
    assert "under the floor" not in refusal, refusal
    assert mod.check_scale(1.0) is None and mod.check_scale(0.75) is None
    assert mod.check_scale(0.5) is not None and mod.check_scale(1.5) is not None


def test_the_failure_form_lines_up_the_widest_check_name():
    """A round 1 record correction. The name column was padded to a literal
    8 and `survivors` is nine characters, so that one check's first line sat
    a column out from every other check's — on the form a reader scans to
    find which check failed."""
    mod = module()
    out = mod.not_sealed(
        "aaa1111", "bbb2222", [("suite", ["one"]), ("survivors", ["two"])]
    )
    columns = {
        line.index(word) for line, word in zip(out[2:], ("one", "two"), strict=True)
    }
    assert len(columns) == 1, f"the first lines do not share a column:\n{out}"


@pytest.mark.parametrize("scale", [0.75, 0.8, 0.9])
def test_the_disc_draws_the_same_bytes_in_every_process(scale):
    """Round 1's 🟡 6. `shrink` resolved a tie between two chart colours with
    `max(set(ink), key=ink.count)`, and a set of strings iterates in an order
    that moves with PYTHONHASHSEED — so the same scale drew differently from
    one process to the next. Measured over five seeds at 0.75: two distinct
    renderings.

    This module's opening argument is that four hand-typed discs were
    lopsided and a circle that is calculated cannot be off centre. A
    calculated circle that is not reproducible gives that argument back at
    every scale but 1.0, and any case that ever pins bytes below 1.0 flakes.

    Run in child processes, because the seed is fixed before the interpreter
    starts and cannot be changed from inside one."""
    script = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('s', {SCRIPT!r})\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        f"sys.stdout.write(chr(10).join(mod.stamp({ROWS!r}, {scale!r}, True)))\n"
    )
    seen = set()
    for seed in ("0", "1", "2", "12345", "99999"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        r = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=120,
        )
        assert r.returncode == 0, r.stderr
        seen.add(r.stdout)
    assert len(seen) == 1, (
        f"scale {scale} drew {len(seen)} distinct discs across five hash seeds"
    )


def test_the_disc_is_symmetric_because_it_is_computed():
    """#30 §*How it is drawn*: four hand-typed discs were lopsided; a computed
    one cannot be. Every twin row has the same left and right margin."""
    mod = module()
    for scale in (1.0, *mod.SCALE_LADDER):
        w, h, px = mod.build(scale)
        for y in range(0, h, 2):
            line = mod.letter_row(mod.disc_cells(px, w, y))
            left = len(line) - len(line.lstrip())
            right = len(line) - len(line.rstrip())
            assert left == right, (
                f"{scale}, row {y}: {left} blank on the left, {right} on the right"
            )


# --- colour at transitions -------------------------------------------------


def test_a_coloured_row_carries_fewer_colour_sequences_than_cells():
    """#30 §*Output size*: a code per cell was 282 KB for one seal. Emitting at
    transitions is what makes the colour form printable, and every row is
    held to it — the disc's rows, where the lily's edges change colour most,
    and every line of the letter (#717)."""
    mod = module()
    w, h, px = mod.build(1.0)
    for y in range(0, h, 2):
        line = mod.colour_row(mod.disc_cells(px, w, y))
        sequences = len(SGR.findall(line))
        assert sequences < w, f"row {y}: {sequences} colour sequences for {w} cells"
    for line in mod.stamp(ROWS, 0.9, shape=False):
        sequences = len(SGR.findall(line))
        assert sequences < visible(line), f"{sequences} sequences: {line!r}"


# --- the letter: a sheet with the disc pressed on its corner (#717) ----------


def disc_at(cell):
    """True where either half of a cell is the disc's: its colours are
    truecolour triples, and the sheet's are 256-colour codes."""
    return isinstance(cell[0], tuple) or isinstance(cell[1], tuple)


def test_the_text_is_written_on_a_sheet_one_blank_line_inside_it():
    """A9's sheet. The sheet's first and last lines are blank parchment
    between two edge cells — the last one where the disc does not cover it —
    and the text starts on the second line, three cells in from the left
    edge. A cell carrying text is parchment on both halves, so nothing of
    the disc stands on a character."""
    mod = module()
    sheet = mod.compose(mod.SAMPLE_ROWS, 0.9)
    cells, width, height = sheet.cells, sheet.width, sheet.height
    for ln in (0, height - 1):
        for x, cell in enumerate(cells[ln][:width]):
            if disc_at(cell):
                continue
            edge = x in (0, width - 1)
            want = mod.SHEET_EDGE if edge else mod.PARCHMENT
            assert cell[:3] == (want, want, None), (ln, x, cell)
    first = [x for x, cell in enumerate(cells[1]) if cell[2]]
    assert first[0] == mod.TEXT_LEFT == 3, first
    said = "".join(cells[1][x][2][0] for x in first)
    assert said.strip() == "SEALED", said
    texts = 0
    for line in cells:
        for cell in line:
            if cell[2]:
                texts += 1
                assert cell[:2] == (mod.PARCHMENT, mod.PARCHMENT), cell
    assert texts, "no cell carries text"
    # Every row of the panel is on the sheet, one line each, in order.
    rows = [row for row in mod.SAMPLE_ROWS if row]
    assert height == len(rows) + 2, (height, len(rows))
    for k, (label, value) in enumerate(rows, 1):
        line = "".join(cell[2][0] if cell[2] else " " for cell in cells[k])
        assert f"{label:<8} {value}".strip() in line, (k, line)
    # One of `letter`'s two leading spaces is kept, so a label stands four in.
    assert "".join(cells[1][x][2][0] for x in first).startswith(" SEALED"), said
    # Every line of the sheet is the sheet's width where the disc does not
    # carry it further: nothing is padded past the edge, nothing stripped.
    for ln in range(height):
        beyond = [cell for cell in cells[ln][width:] if disc_at(cell)]
        assert len(cells[ln]) == width if not beyond else len(cells[ln]) > width, ln
    # Where the text and not the disc sets the width (no disc at all), the
    # edge stands two cells past the longest line: one of parchment, then it.
    bare = mod.compose(mod.SAMPLE_ROWS, None)
    longest = max(len(t) for t in mod.sheet_text(mod.SAMPLE_ROWS))
    assert bare.width == mod.TEXT_LEFT + longest + 2, (bare.width, longest)


@pytest.mark.parametrize("scale", [0.9, 0.8, 0.75])
def test_the_disc_hangs_over_the_corner_two_clear_cells_from_the_text(scale):
    """A9's disc. It hangs below the sheet's last line and right of its
    edge, and on every text line the two cells after the last character are
    parchment wherever the disc stands further along that line — on every
    line, not only the disc's equator, which is where the prototype's own
    collision test looked (`spec.md` §*What was measured*)."""
    mod = module()
    sheet = mod.compose(mod.SAMPLE_ROWS, scale)
    cells, width, height = sheet.cells, sheet.width, sheet.height
    assert any(disc_at(cell) for line in cells[height:] for cell in line), (
        "the disc does not hang below the sheet"
    )
    assert any(disc_at(cell) for line in cells for cell in line[width:]), (
        "the disc does not hang over the sheet's right edge"
    )
    assert any(disc_at(cell) for line in cells[:height] for cell in line[:width]), (
        "the disc is tucked under the sheet rather than pressed over it"
    )
    for ln in range(1, height - 1):
        line = cells[ln]
        ends = [x for x, cell in enumerate(line) if cell[2] and cell[2][0] != " "]
        wax = [x for x, cell in enumerate(line) if disc_at(cell)]
        if not ends or not wax:
            continue
        end = ends[-1]
        assert wax[0] > end + mod.GAP == end + 2, (scale, ln, end, wax[0])
        for x in range(end + 1, end + 1 + mod.GAP):
            assert line[x][:3] == (mod.PARCHMENT, mod.PARCHMENT, None), (ln, x)
    # The disc's centre line is the sheet's last line and, where it sets the
    # width, its centre column is the sheet's right edge: half below, half
    # over. The letter ends at the disc's lowest line, with no empty line.
    rows_on = [ln for ln, line in enumerate(cells) if any(map(disc_at, line))]
    cols_on = [x for line in cells for x, cell in enumerate(line) if disc_at(cell)]
    assert abs((rows_on[0] + rows_on[-1]) / 2 - (height - 1)) <= 1, (rows_on, height)
    assert abs((min(cols_on) + max(cols_on)) / 2 - (width - 1)) <= 1, (cols_on, width)
    assert rows_on[-1] == len(cells) - 1, "an empty line ends the letter"


def test_the_letter_is_written_in_its_four_codes_and_the_discs_five_colours():
    """A9's colours, read off the encoded lines. The title is 124, the ink
    94, the sheet 230 and its edge 187, as 256-colour codes; every truecolour
    code is one of the disc's five; nothing of the rope, the outer red band
    or the gold is left. A sheet line whose last cell is painted ends with
    that cell and a reset — its trailing spaces are the sheet, not padding."""
    mod = module()
    lines = mod.stamp(mod.SAMPLE_ROWS, 0.9, shape=False)
    text = "\n".join(lines)
    title = text.index("SEALED")
    assert text.rfind("\x1b[38;5;124m", 0, title) > text.rfind(
        "\x1b[38;5;94m", 0, title
    )
    assert "\x1b[38;5;94m" in text and "\x1b[48;5;230m" in text
    assert "\x1b[48;5;187m" in text
    triples = {
        tuple(int(v) for v in m.groups())
        for m in re.finditer(r"\x1b\[[34]8;2;(\d+);(\d+);(\d+)m", text)
    }
    assert triples and triples <= set(mod.DISC_COLOURS), triples
    assert set(mod.DISC_COLOURS) == {
        (168, 26, 30),
        (120, 16, 20),
        (226, 82, 74),
        (96, 10, 14),
        (186, 34, 38),
    }
    for gone in ("ROPE_L", "ROPE_D", "WAX_L", "GOLD"):
        assert not hasattr(mod, gone), gone
    for old in ((232, 226, 196), (168, 158, 122), (206, 46, 48), (200, 150, 30)):
        assert ";".join(map(str, old)) not in text, old
    sheet = mod.compose(mod.SAMPLE_ROWS, 0.9)
    assert visible(lines[0]) == sheet.width, (visible(lines[0]), sheet.width)
    assert lines[0].endswith(" \x1b[0m"), repr(lines[0][-12:])
    # The owner's disc: its edge from 0.78 of the radius and nothing past 0.84.
    assert (mod.FIELD_EDGE, mod.WAX_EDGE) == (0.78, 0.84)


def test_the_title_is_the_sheets_first_line_whatever_a_value_says():
    """Round 1's ⬜ 5. The title's 124 was keyed on a line READING `SEALED`,
    so a continuation row carrying that value — a branch named `SEALED` —
    was inked as a second title. It is keyed on the panel's first row now:
    that line alone is 124, and every other line is ink, whatever it says."""
    mod = module()
    rows = [("SEALED", ""), ("tree", "aaa1111"), ("", "SEALED"), ("rounds", "2")]
    cells = mod.compose(rows, 0.9).cells
    inks = [{c[2][1] for c in line if c[2] and c[2][0] != " "} for line in cells]
    assert inks[1] == {mod.TITLE}, inks[1]
    assert inks[3] == {mod.INK}, "a continuation reading SEALED is inked as the title"
    assert all(ink <= {mod.INK} for k, ink in enumerate(inks) if k != 1), inks


@pytest.mark.parametrize("scale", [0.9, 0.8, 0.75])
def test_the_lily_is_lit_from_the_upper_left(scale):
    """#717's lily, one colour pressed into the wax: a lily cell whose
    up-left neighbour is not lily is its highlight, one whose down-right
    neighbour is not lily is its shadow (where the up-left one is), and
    every other lily cell is its face. Read off `build` cell by cell, at
    every rung, so a light swapped for a shadow or a neighbour taken from
    the wrong side is red."""
    mod = module()
    w, h, px = mod.build(scale)
    lily = {mod.LILY_FACE, mod.LILY_LIGHT, mod.LILY_SHADOW}
    seen = set()
    for y in range(h):
        for x in range(w):
            here = px(x, y)
            if here not in lily:
                continue
            seen.add(here)
            up_left, down_right = px(x - 1, y - 1), px(x + 1, y + 1)
            if here == mod.LILY_LIGHT:
                assert up_left not in lily, (x, y)
            else:
                assert up_left in lily, (x, y, here)
                assert (down_right not in lily) == (here == mod.LILY_SHADOW), (x, y)
    assert seen == lily, seen


def test_the_twin_writes_the_discs_five_letters_over_the_sheets_frame():
    """#717's A10 for the characters. `KEY` gives the disc's five colours
    five letters, the field keeping `.`; a cell whose top half is the disc's
    is that colour's letter whatever the sheet is beneath it, so the disc
    overrides the frame where it covers it; the sheet's last line is its
    bottom, `'---`, and every other line of it is edged with `|`."""
    mod = module()
    assert set(mod.KEY) == set(mod.DISC_COLOURS)
    assert len(set(mod.KEY.values())) == 5 and mod.KEY[mod.FIELD] == ".", mod.KEY
    sheet = mod.compose(mod.SAMPLE_ROWS, 0.9)
    twin = mod.stamp(mod.SAMPLE_ROWS, 0.9, shape=True)
    for line, said in zip(sheet.cells, twin, strict=True):
        for cell, char in zip(line, said, strict=True):
            if isinstance(cell[0], tuple):
                assert char == mod.KEY[cell[0]], (cell, char)
            elif isinstance(cell[1], tuple):
                assert char == mod.KEY[cell[1]], (cell, char)
    bottom = twin[sheet.height - 1]
    assert bottom.startswith("'---"), bottom
    for said in twin[1 : sheet.height - 1]:
        assert said.startswith("|"), said


# --- the panel -------------------------------------------------------------


def test_the_panel_renders_its_rows_and_its_blanks():
    """The panel is data — `(label, value)` rows with `None` for a blank — so
    what the seal reports is a list the gate fills, not a string it formats.
    Every label and value lands on its own line, and every `None` is a line
    carrying nothing but the frame. `panel` returns no `None` since #717,
    and a values file an older gate wrote still carries them, so the blank
    is planted here rather than taken from `ROWS`."""
    mod = module()
    rows = [ROWS[0], None, *ROWS[1:]]
    panel = mod.letter(rows)
    body = panel[2:-2]  # inside the border and its two padding lines
    assert len(body) == len(rows), f"{len(body)} panel lines for {len(rows)} rows"
    for row, line in zip(rows, body, strict=True):
        if row is None:
            assert line.strip("| ") == "", f"a None row rendered as {line!r}"
            continue
        label, value = row
        assert label in line and value in line, f"{row} rendered as {line!r}"
    width = {len(line) for line in panel}
    assert len(width) == 1, f"the panel's lines are not one width: {sorted(width)}"
    # #666: a `""` label continues the row above it — its value starts in the
    # same column as the labelled row's value, and nothing stands before it.
    tree, branch = body[2], body[3]
    assert branch.index("feat/12-a-branch") == tree.index("c46fd2d"), (tree, branch)
    assert branch[1 : branch.index("feat/")].strip() == "", branch


# --- the floor -------------------------------------------------------------


def test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence():
    """#30 §*Size*: 75 % is the floor the issue measured — at 60 % the band
    closes, at 50 % the lily reads as a cross. The floor is let through; a
    scale under it is refused with a sentence naming both numbers, and the
    command exits 2 with nothing drawn, because a seal nobody can read is the
    counterfeit `verify` names."""
    mod = module()
    assert mod.stamp(ROWS, scale=0.75), "the floor itself was refused"
    with pytest.raises(ValueError) as refused:
        mod.stamp(ROWS, scale=0.5)
    sentence = str(refused.value)
    assert "0.75" in sentence and "0.5" in sentence, (
        f"the refusal names neither the floor nor the scale asked for: {sentence!r}"
    )
    with pytest.raises(ValueError, match=r"1\.0") as too_large:
        mod.stamp(ROWS, scale=1.5)
    assert "1.5" in str(too_large.value), (
        "the chart is one cell per stitch and does not enlarge; a scale above "
        "1.0 is refused with a sentence naming the scale asked for"
    )
    out = run_wrapper("--shape", "--scale", "0.5")
    assert out.returncode == 2, f"exit {out.returncode}; stderr {out.stderr!r}"
    assert "0.75" in out.stderr, f"the command's refusal names no floor: {out.stderr!r}"
    assert not out.stdout, f"something was drawn under a refused scale: {out.stdout!r}"


# --- the failure form ------------------------------------------------------


def test_not_sealed_carries_no_disc_and_names_every_failure():
    """#30 §*On failure*: no drawing. What a person needs then is which checks
    broke, and a 22-row picture pushes that off the screen — and a picture
    that says *sealed* beside a word that says *not* is read picture first."""
    mod = module()
    failures = [
        ("suite", ["3 failed, 765 passed", "tests/test_x.py::test_y FAILED"]),
        ("ledger", ["2 broken"]),
    ]
    lines = mod.not_sealed("c46fd2d", "1e2bed9", failures)
    text = "\n".join(lines)
    assert "NOT SEALED" in lines[0], f"the first line is not the verdict: {lines[0]!r}"
    assert "c46fd2d" in lines[0] and "1e2bed9" in lines[0], (
        "the failure form does not name the tree and the base"
    )
    assert not any(c in text for c in HALF_BLOCKS), "the failure form draws the disc"
    assert not SGR.search(text), "the failure form carries colour codes"
    twin = mod.stamp(ROWS, shape=True)
    crown = next(line.strip() for line in twin if line.strip())
    assert crown not in text, "the failure form carries the letter twin"
    for name, first_lines in failures:
        assert name in text, f"failing check {name!r} is not named"
        for line in first_lines:
            assert line in text, f"{name}'s line {line!r} is missing"


# --- which form ------------------------------------------------------------


@pytest.mark.parametrize(
    "stream, why",
    [
        (Stream("cp949", tty=True), "a console that cannot render half-blocks"),
        (Stream("utf-8", tty=False), "a pipe, where `seal-stamp` prints the twin"),
        (io.StringIO(), "a stream with no encoding and no terminal"),
    ],
)
def test_pick_shape_is_letters_off_a_utf8_terminal(stream, why):
    """S5 — the colour form is for a person's terminal. Blocks and colour are
    for a UTF-8 tty and nothing else. (#30's `spec.md` §Out said the sealer's
    returned text carries the twin; since #400 it carries no drawing at all,
    because the gate asks `is_terminal` and draws nothing on a pipe.)"""
    assert module().pick_shape(stream) is True, why


class Raising(Stream):
    def isatty(self):
        raise ValueError("I/O operation on closed file")


@pytest.mark.parametrize(
    "stream, terminal",
    [
        (Stream("cp949", tty=True), True),
        (Stream("utf-8", tty=True), True),
        (Stream("utf-8", tty=False), False),
        (io.StringIO(), False),
        (Raising("utf-8", tty=True), False),
    ],
)
def test_is_terminal_asks_the_tty_and_not_the_encoding(stream, terminal):
    """#400. `pick_shape` folded *not a tty* and *not UTF-8* into one answer,
    and the gate needs them apart: a cp949 terminal has a person in front of
    it and gets letters, a UTF-8 pipe has nobody and gets nothing drawn. A
    stream whose `isatty` raises is a stream nobody is looking at."""
    assert module().is_terminal(stream) is terminal


def test_pick_shape_is_blocks_on_a_utf8_terminal():
    """The control: the one stream that gets the drawing."""
    assert module().pick_shape(Stream("UTF-8", tty=True)) is False


@pytest.mark.parametrize("wrapper", ["seal-stamp", "broad-gate"])
def test_a_wrapper_pair_is_run_through_the_twin_the_platform_can_execute(wrapper):
    """CI's `windows-latest` leg, red on two cases of this module: `OSError:
    [WinError 193] %1 is not a valid Win32 application`.

    Both go through a `bin/` wrapper that opens `#!/usr/bin/env sh`. A
    shebang is a POSIX kernel's convention; `CreateProcess` reads the file as
    an image and refuses it. The repair is not a skip — both files ship with
    a `.cmd` twin for exactly this, and
    `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` states the
    rule: *a new command means both files or it means one platform*.

    Pinned on both branches from either machine, which is the point: a wrong
    wrapper chosen for a platform fails HERE rather than only on the runner.
    That is round 2's 🟡 14 lesson applied to the case rather than the unit —
    the platform is an argument, so the branch the build machine cannot run
    is still one a reviewer can turn red."""
    path = os.path.join(ROOT, "bin", wrapper)
    assert os.path.isfile(path), f"bin/{wrapper} missing"
    assert os.path.isfile(path + ".cmd"), f"bin/{wrapper}.cmd missing"

    assert wrapper_command(path, ["--shape"], windows=False) == [path, "--shape"], (
        "a POSIX machine no longer runs the extensionless file"
    )
    win = wrapper_command(path, ["--shape"], windows=True)
    assert win[0].lower().endswith("cmd.exe"), (
        "Windows runs the wrapper as an image rather than through the command "
        f"interpreter, which is `[WinError 193]` on a `#!` file: {win}"
    )
    assert win[1:] == ["/c", path + ".cmd", "--shape"], (
        "Windows does not reach the `.cmd` twin, which is the file it can "
        f"actually execute: {win}"
    )


def test_the_command_piped_prints_the_twin():
    """The wrapper, run the way an agent runs it — stdout a pipe. Letters, no
    colour, exit 0, and the panel beside the disc."""
    out = run_wrapper()
    assert out.returncode == 0, out.stderr
    assert not SGR.search(out.stdout), "a piped run carries colour codes"
    assert not any(c in out.stdout for c in HALF_BLOCKS), "a piped run drew half-blocks"
    assert "SEALED" in out.stdout and "rounds" in out.stdout, (
        "the panel is missing from the piped drawing"
    )
    assert out.stdout == run_wrapper("--shape").stdout, (
        "a pipe and `--shape` disagree about the twin"
    )


# =============================================================================
# Part 2 — the gate command and the one write
# =============================================================================

# Begun after every cutoff `chain_check.py` carries, so every rule it has
# applies to the records written here.
ITEM = "seal/specs/1799000000-a-sealed-work-item"
ROUNDS = f"{ITEM}/rounds"
ROW = "Broad gate"
# The reviewer's own row. `seal` reads it nowhere: a capped run leaves it
# `yes` over a verdict table with nothing open in it, and the field that
# answers *is a finding still open* is the `Pass` box one row down.
NEEDS = "Needs a fix"
# The row that answers *has this run ended*: `close` leaves it at its
# landing value for the next round to set, and its starting value is the
# state the seal must refuse.
CHECKED_BY = "Fixes checked by"

PASSING_TEST = "def test_one():\n    assert True\n"
FAILING_TEST = "def test_two():\n    assert False, 'planted'\n"
OVERVIEW = "# overview\n\n## Not verified\n\nnone — the fixture verifies nothing\n"

VERDICT_HEADER = (
    "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
)
OPEN_ROW = "| 🔴 1 | the parser drops a row | `f.py:1` | open | executed |\n"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate_module():
    return _load("specseal_broad_gate_for_tests", GATE)


def reader_module():
    return _load("specseal_reader_for_sealed_records", READER)


def check_module():
    return _load("specseal_chain_check_for_sealed_records", CHECK)


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-qm",
        message,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def config(row=True):
    """The fixture's config file. `row` is True for the default runner, a
    string for a row under test, or False for a file with no such row."""
    text = "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n"
    if row:
        # The suite runner alone, so the base comparison's first prefix is
        # the runner and it re-runs only the failing files (#747).
        # `-p no:cacheprovider` keeps pytest from writing `.pytest_cache`
        # into a tree the gate later diffs.
        runner = row if isinstance(row, str) else SUITE_ROW
        text += f"| {ROW} | {runner} |\n"
    return text


SUITE_ROW = f"{sys.executable} -m pytest -q -p no:cacheprovider tests"


def set_row(repo, value):
    """The fixture's `Broad gate` row replaced by VALUE and committed, so the
    gate reads it from a tree with nothing uncommitted in it."""
    write(repo, "seal/config.md", config(value))
    commit(repo, "the row under test")
    return repo


def env_without_a_pull_request():
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    # The suite runs under Claude Code more often than not, and the live
    # session's id would key every fixture's values file to it (1790562543's
    # `questions.md` Q7). A case that wants a session sets one.
    env.pop(SESSION_VAR, None)
    env["GH_PROMPT_DISABLED"] = "1"
    env["GH_NO_UPDATE_NOTIFIER"] = "1"
    return env


def build_repo(d, row=True, base_failing=False):
    """A repository on branch `base` with a one-test suite, the config row
    and an overview, then a `feature` branch one commit ahead."""
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "tests/test_one.py", PASSING_TEST)
    if base_failing:
        write(d, "tests/test_two.py", FAILING_TEST)
    write(d, "seal/config.md", config(row))
    write(d, f"{ITEM}/overview.md", OVERVIEW)
    commit(d, "base")
    git(d, "switch", "-qc", "feature")
    write(d, "README.md", "# a fixture\n")
    commit(d, "feature")
    return d


# --- the runner's environment must not reach a fixture repository ---------
#
# `chain_check` decides draft against ready by reading `GITHUB_EVENT_PATH`,
# and matches a routing declaration against `GITHUB_HEAD_REF`. On a runner
# both are set and both describe the REAL pull request, so a gate run over a
# fixture repository here was judged with #332's own event: the fixture's
# `Broad gate: not yet` failed the arm, the checks failed before `seal` was
# reached, and the case that drives `gate` IN PROCESS went red on all three
# legs while every local run stayed green.
#
# `env_without_a_pull_request` already pops both for the subprocess runs. It
# cannot reach an in-process one, and nothing said which kind a case was.
#
# `phases/phase-2.md` decided the other half of this: *`chain_check` is
# judged as a draft… If `GITHUB_EVENT_PATH` is already set, leave it.* That
# is right for a real run and wrong for a fixture, and this is the fixture's
# side of it.
GITHUB_VARS = ("GITHUB_EVENT_PATH", "GITHUB_HEAD_REF")


def ready_payload(directory):
    """A pull-request event payload that `chain_check` judges READY."""
    path = os.path.join(str(directory), "event.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"pull_request": {"draft": False}}, handle)
    return path


@pytest.fixture(scope="module", autouse=True)
def _a_runner_like_environment(tmp_path_factory):
    """This module runs as though it were on a runner, on every machine.

    Without it, removing the clearing below is red only where the variables
    happen to be set — which is CI, after a pull request has already gone
    red. Setting them here makes the guard's removal red on a laptop, which
    is the whole lesson this branch has now landed twice.

    Module-scoped and restored at teardown, so the simulation is bounded to
    the module that needs it."""
    was = {name: os.environ.get(name) for name in GITHUB_VARS}
    os.environ["GITHUB_EVENT_PATH"] = ready_payload(
        tmp_path_factory.mktemp("runner-event")
    )
    os.environ["GITHUB_HEAD_REF"] = "feat/some-other-pull-request"
    yield
    for name, value in was.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value


@pytest.fixture(autouse=True)
def _no_ambient_pull_request(monkeypatch):
    """The guard. Every case in this module runs with the runner's idea of
    which pull request is open removed, so a fixture repository is judged on
    what the fixture holds. A case that wants one sets it back itself."""
    for name in GITHUB_VARS:
        monkeypatch.delenv(name, raising=False)
    # And the live Claude Code session's id, for the in-process cases, for the
    # reason `env_without_a_pull_request` gives.
    monkeypatch.delenv(SESSION_VAR, raising=False)


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    return build_repo(tmp_path_factory.mktemp("gate-template") / "repo")


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def run_gate(repo, *extra, keep=None, wrapper=False, session=None, cwd=None):
    """`broad_gate.py --base base --root <repo> --shape`, its outputs kept
    under `keep`; returns the completed process. stdout is a pipe, so a
    sealed run signals rather than draws; `session` is the Claude Code
    session the run belongs to, and None runs it with no session at all.
    `cwd` is the directory the gate is started in, which a relative `keep`
    is read from."""
    keep = keep or repo.parent / "out"
    env = env_without_a_pull_request()
    if session is not None:
        env[SESSION_VAR] = session
    tail = [
        "--base",
        "base",
        "--root",
        str(repo),
        "--shape",
        "--keep-output",
        str(keep),
        *extra,
    ]
    command = (
        wrapper_command(GATE_WRAPPER, tail)
        if wrapper
        else [sys.executable, GATE, *tail]
    )
    return subprocess.run(
        command,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        env=env,
        cwd=cwd,
    )


def short(repo, ref):
    return git(repo, "rev-parse", "--short", ref).stdout.strip()


def values_files(repo):
    """Every values file the gate has written for `repo`, drawn or not.

    Read from the git dir rather than from what the gate printed: since #400
    a sealed run on a pipe prints no disc at all, so a disc missing from
    stdout proves nothing about a run that should not have been sealed. A
    file here is what a hook would have drawn."""
    found = []
    for directory, _dirs, names in os.walk(repo / ".git" / VALUES_DIR):
        found += [os.path.join(directory, n) for n in names if n.endswith(".json")]
    return sorted(found)


def signal_lines(text):
    """The lines of `text` that are the gate's `SEALED` signal."""
    return [line for line in text.splitlines() if line.startswith("SEALED")]


def head_of(repo, word="SEALED", branch="feature"):
    """What a `SEALED` or `NOT SEALED` line opens with over the fixture
    (#666): the branch and the tree, then the base's ref and its commit. The
    fixture has no remote, so the ref is `base` as given."""
    named = f"{branch} @ {short(repo, 'HEAD')}" if branch else short(repo, "HEAD")
    return f"{word}   {named} against base @ {short(repo, 'base')}"


def sealed_values(repo, tmp_path, session="s-1"):
    """A settled item sealed through `--record` on a pipe, with `session` set:
    the completed process and the one values file's contents."""
    settled_item(repo)
    out = run_gate(
        repo, "--record", str(repo / ITEM), keep=tmp_path / "out", session=session
    )
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    files = values_files(repo)
    assert len(files) == 1, f"one values file expected, found {files}"
    return out, module().read_values(files[0])


def row_of(values, label):
    """The value the panel carries beside `label`, or None."""
    return next((row[1] for row in values["rows"] if row and row[0] == label), None)


def crown_of():
    """The first non-blank line of the letter twin — present in a stamp and
    in nothing else the gate prints."""
    twin = module().stamp(ROWS, shape=True)
    return next(line.strip() for line in twin if line.strip())


# --- which copy of the gate runs, and the stamp says which (#475) -----------
#
# `bin/broad-gate` on PATH is the installed plugin's, and the script resolves
# every arm relative to itself, so a branch that changes the gate was measured
# by the copy that predates the change and the stamp could not say so. Where
# the gated tree ships `skills/verify/scripts/broad_gate.py` and it is not the
# running file, `main` runs that copy in its place with the same argument
# vector and says so on stderr; every run carries a `gate` row and a line
# naming the running copy's absolute path.

STUB_GATE = "import sys\nprint('STUB GATE RAN', sys.argv[1:])\nsys.exit(3)\n"


def plugin_json_version():
    with open(
        os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as f:
        return json.load(f)["version"]


def test_the_gate_runs_the_copy_the_tree_ships_with_the_same_arguments(repo, tmp_path):
    """A7. The fixture ships a stub at the gate's path that prints a marker
    and its arguments and exits 3. The real gate over that root exits 3,
    prints the marker, hands the stub the argument vector it was given, and
    writes one stderr line naming both absolute paths — the copy it ran and
    the copy it was invoked as. Red at `9f846733`: the installed-style run
    ignored the stub and sealed the fixture (exit 0, no marker)."""
    stub = repo / "skills" / "verify" / "scripts" / "broad_gate.py"
    stub.parent.mkdir(parents=True)
    stub.write_text(STUB_GATE, encoding="utf-8")
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 3, f"{out.stdout}\n{out.stderr}"
    assert out.stdout.count("STUB GATE RAN") == 1, out.stdout
    assert "'--base', 'base'" in out.stdout and repr(str(repo)) in out.stdout, (
        f"the tree's copy was not handed the argument vector as given:\n{out.stdout}"
    )
    assert "SEALED" not in out.stdout, (
        "the invoking copy went on to seal after handing over"
    )
    line = next(
        (line for line in out.stderr.splitlines() if "ships its own gate" in line),
        None,
    )
    assert line, f"no stderr line says the tree's copy ran:\n{out.stderr}"
    assert str(stub) in line and os.path.realpath(GATE) in line, (
        f"the line does not name both copies by absolute path: {line}"
    )


def test_a_flag_only_the_trees_copy_knows_still_reaches_it(repo, tmp_path):
    """A7's other half. A branch whose gate grows an argument is inside
    #475's class — measured by the copy that predates the change — so the
    redirect is decided before this copy's parser can refuse what only the
    tree's copy accepts. Red at 01e5a25f: exit 2, `unrecognized arguments`,
    and the stub never ran."""
    stub = repo / "skills" / "verify" / "scripts" / "broad_gate.py"
    stub.parent.mkdir(parents=True)
    stub.write_text(STUB_GATE, encoding="utf-8")
    out = run_gate(repo, "--new-flag-only-the-tree-knows", keep=tmp_path / "out")
    assert out.returncode == 3, f"{out.stdout}\n{out.stderr}"
    assert "'--new-flag-only-the-tree-knows'" in out.stdout, (
        f"the tree's copy was not handed the flag only it knows:\n{out.stdout}"
    )
    assert "unrecognized arguments" not in out.stderr, out.stderr


def test_the_trees_own_copy_does_not_redirect_to_itself():
    """A8, first half. Over this repository the running script IS the file
    the tree ships, by realpath, so there is nothing to hand over to and no
    loop."""
    assert gate_module().shipped_gate(ROOT) is None


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs a privilege on Windows")
def test_a_shipped_copy_that_is_this_file_by_realpath_is_not_a_redirect(repo):
    """A8, second half. A fixture whose gate path is a symlink to the running
    file: the two paths differ as typed and are one file by realpath, so no
    redirect — which is the check that stops a tree's copy running itself
    forever."""
    link = repo / "skills" / "verify" / "scripts" / "broad_gate.py"
    link.parent.mkdir(parents=True)
    os.symlink(GATE, link)
    assert gate_module().shipped_gate(str(repo)) is None


def test_a_repository_shipping_no_gate_runs_the_invoked_copy(repo, tmp_path):
    """A9 and A10 together, on a sealed run. The fixture ships no gate, so the
    invoked copy runs as before, and stderr carries one line naming the
    running copy's absolute path and `plugin <version>`. Red at `9f846733`:
    no such line.

    Since #666 the panel carries NO `gate` row here (A8): the copy that ran
    is the copy that was invoked, so the row would say nothing, which is the
    owner's complaint about the row on every stamp. The panel is read from
    the run's values file, because a sealed run on a pipe does not draw it."""
    out, values = sealed_values(repo, tmp_path)
    assert row_of(values, "gate") is None, values["rows"]
    assert f"broad-gate: gate {os.path.realpath(GATE)} (plugin " in out.stderr, (
        f"no stderr line names the running copy's path:\n{out.stderr}"
    )
    assert "ships its own gate" not in out.stderr


def test_a_refusal_after_the_root_resolved_still_names_the_running_copy(tmp_path):
    """A10's other outcome. A repository with no `Broad gate` row is refused
    with nothing run, and the line still prints, because which copy refused
    is a fact a reader learns nowhere else."""
    repo = build_repo(tmp_path / "repo", row=False)
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 2, f"{out.stdout}\n{out.stderr}"
    assert f"broad-gate: gate {os.path.realpath(GATE)} (" in out.stderr, out.stderr


def test_the_stderr_line_says_tree_under_the_gated_root_and_plugin_elsewhere(
    tmp_path,
):
    """A10's value, on the stderr line every run prints. `tree <version>`
    where the running copy's realpath lies under the gated root, `plugin
    <version>` otherwise; the version is the running copy's own
    `plugin.json`, and `?` where it cannot be read."""
    gate = gate_module()
    version = plugin_json_version()
    assert gate.copy_origin(ROOT) == f"tree {version}"
    assert gate.copy_origin(str(tmp_path)) == f"plugin {version}"
    assert gate.copy_origin(None) == f"plugin {version}"
    assert gate.copy_origin(str(tmp_path), plugin=str(tmp_path)) == "plugin ?"


def test_the_gate_row_prints_only_where_the_copy_that_ran_is_not_the_one_invoked(
    tmp_path,
):
    """A8, #666's four shapes, at the unit `main` and `gate` feed.

    - a tree whose copy is byte-identical to the copy invoked: no row
    - a tree whose copy differs: `tree <version>`
    - a repository that ships no gate, so the running copy is not under
      its root: no row
    - the tree's copy invoked directly, no installed path handed over:
      the row, the direction that says more when it cannot tell
    """
    gate = gate_module()
    version = plugin_json_version()
    tree = tmp_path / "tree"
    shipped = tree / "skills" / "verify" / "scripts" / "broad_gate.py"
    shipped.parent.mkdir(parents=True)
    shutil.copyfile(GATE, shipped)
    other = tmp_path / "installed.py"
    other.write_text("# a different gate\n", encoding="utf-8")
    running, root = str(shipped), str(tree)
    assert gate.gate_copy(root, running=running, installed=GATE) is None
    assert gate.gate_copy(root, running=running, installed=str(other)) == (
        f"tree {version}"
    )
    assert gate.gate_copy(str(tmp_path / "elsewhere"), running=GATE) is None
    assert gate.gate_copy(root, running=running) == f"tree {version}"
    # An installed copy nobody can read counts as different, so the row says
    # which copy ran.
    missing = str(tmp_path / "gone.py")
    assert gate.gate_copy(root, running=running, installed=missing) == (
        f"tree {version}"
    )


STUB_THAT_SAYS_WHO_INVOKED_IT = (
    "import os, sys\n"
    "print('INVOKED AS', os.environ.get('SPECSEAL_BROAD_GATE_INVOKED_AS'))\n"
    "sys.exit(3)\n"
)


def test_the_redirect_hands_the_child_the_copy_it_was_invoked_as(repo, tmp_path):
    """A8's channel. `main` hands the tree's copy the realpath of the copy the
    caller invoked, in the environment, because the child has no other way to
    know it; and the child takes it OUT of the environment before any check
    inherits it, so a suite loading the gate in process is not answered for a
    redirect it never made."""
    stub = repo / "skills" / "verify" / "scripts" / "broad_gate.py"
    stub.parent.mkdir(parents=True)
    stub.write_text(STUB_THAT_SAYS_WHO_INVOKED_IT, encoding="utf-8")
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 3, f"{out.stdout}\n{out.stderr}"
    assert f"INVOKED AS {os.path.realpath(GATE)}" in out.stdout, out.stdout
    gate = gate_module()
    assert gate.INVOKED_AS_VAR == "SPECSEAL_BROAD_GATE_INVOKED_AS"


def test_the_gate_takes_the_invoked_path_out_of_the_environment(
    repo, tmp_path, monkeypatch
):
    """The other half of the channel, in process: `main` pops the variable,
    so every check it then runs, and the test suite a `Broad gate` row runs,
    sees none."""
    gate = gate_module()
    monkeypatch.setenv(gate.INVOKED_AS_VAR, "/x/elsewhere/broad_gate.py")
    gate.main(
        ["--base", "base", "--root", str(repo), "--keep-output", str(tmp_path / "o")],
        console_wants_letters=True,
        console_is_terminal=False,
    )
    assert gate.INVOKED_AS_VAR not in os.environ


def test_the_gate_row_fits_the_panel_for_a_nine_character_version(tmp_path):
    """A10's width. `plugin ` is seven columns and `PANEL_VALUE_WIDTH` is 23,
    so a nine-character version fits with room; a version that would not is
    elided at the frame (`fit`), never widening the row."""
    gate = gate_module()
    fake = tmp_path / "plugin"
    (fake / ".claude-plugin").mkdir(parents=True)
    for version in ("1.2.3-rc4", "1.2.3-rc4" * 4):
        (fake / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"version": version}), encoding="utf-8"
        )
        value = gate.copy_origin(str(tmp_path), plugin=str(fake))
        assert len(value) <= gate.PANEL_VALUE_WIDTH, value
        assert value.startswith("plugin "), value
    assert gate.copy_origin(str(tmp_path), plugin=str(fake)).endswith(gate.ELISION)
    rows = gate.panel(
        "ccccccc",
        gate.Base("base", "cccccccc", "base", "cccccccc"),
        {
            n: gate.Check(n, 0, "", "")
            for n in (gate.SUITE, gate.LEDGER, gate.CHAIN_NAME)
        },
        None,
        copy="tree 1.2.3-rc4",
    )
    assert ("gate", "tree 1.2.3-rc4") in rows


def test_the_sealer_is_told_the_gate_says_which_copy_ran():
    """A11. The gate line is the same kind of line as the moved-base one: a
    fact about the run a reader learns nowhere else, quoted by the sealer and
    judged by nobody. The definition says the gate prints which copy ran,
    what a `tree` value means, and that the line is quoted in the report."""
    text = " ".join(sealer_text().split())
    assert "which copy of itself ran" in text, (
        "the sealer's definition does not say the gate reports which copy ran"
    )
    assert "measured by the gate it ships" in text, (
        "the definition does not say what a `tree` value on the stamp means"
    )
    assert "Quote the gate line" in text, (
        "the definition does not tell the sealer to quote the gate line the "
        "way it quotes the moved-base line"
    )


# --- S3 no row ---------------------------------------------------------------


def test_without_the_row_the_gate_names_it_and_runs_nothing(tmp_path):
    """S3. A seal taken over a command nobody chose is the counterfeit
    `verify` names, so an absent row is a refusal rather than a default: the
    row is named, exit 2, and no check ran — the output directory holds
    nothing."""
    repo = build_repo(tmp_path / "repo", row=False)
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 2, f"exit {out.returncode}; {out.stdout!r} {out.stderr!r}"
    assert ROW in out.stderr, f"the refusal does not name the row: {out.stderr!r}"
    assert "seal/config.md" in out.stderr.replace(os.sep, "/"), out.stderr
    assert not out.stdout, f"something printed under a refusal: {out.stdout!r}"
    assert not keep.exists() or not os.listdir(keep), (
        f"a check ran under a refusal: {os.listdir(keep)}"
    )


def test_the_absent_row_refusal_sends_the_question_to_a_person(tmp_path):
    """A10 of #401, executed rather than read: the sentence a session actually
    meets. It used to open *Write the repository's own broad command into it*
    and print the row to type — and the only reader standing here is a
    session, which is the one party that may not write it. #401 is that
    session: it ran four candidates, chose one, wrote the row, and told the
    owner afterwards."""
    repo = build_repo(tmp_path / "repo", row=False)
    said = run_gate(repo, keep=tmp_path / "out").stderr
    assert "Write the repository's own broad command" not in said, said
    assert "not this session's to do" in said, said
    assert "a row is a thing a person wrote" in said, said
    assert "/specseal:config" in said, said
    # A5 of #415. This config has no unparseable line at all, so the branch
    # added for one must not have swallowed the message meant for a row that
    # genuinely is not there. Without this the new branch could take every
    # refusal and the case above would still pass on its four sentences.
    assert "does not parse as a row" not in said, said
    assert f"has no `{ROW}` row" in said, said


def test_a_base_that_does_not_resolve_is_refused_with_nothing_run(repo, tmp_path):
    """The other exit-2 the interface names: a base nothing can be compared
    against. Nothing ran."""
    keep = tmp_path / "out"
    out = subprocess.run(
        [
            sys.executable,
            GATE,
            "--base",
            "no-such-ref",
            "--root",
            str(repo),
            "--keep-output",
            str(keep),
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env_without_a_pull_request(),
    )
    assert out.returncode == 2, out.stderr
    assert "no-such-ref" in out.stderr
    assert not keep.exists() or not os.listdir(keep)


# --- A1-A6: a row the gate would not run as the command it reads as ---------
#
# #402, reported from use. `hooks/config.py#config_rows` strips whitespace and
# nothing else, so a value wrapped in backticks -- the way every command in
# every document in this project is written -- reached `/bin/sh` as command
# substitution: the checks ran, their exit status was thrown away, and their
# OUTPUT was executed in their place. The lucky tail of that is exit 127. The
# quiet one is exit 0 over a check that failed, which is the counterfeit
# `skills/verify/SKILL.md` §*The Seal Test* is named after.
#
# Every case below was executed against the gate as it stood at 0e676e6, with
# no refusal in `gate()` at all, and every one failed; the output is in the
# body of the commit that added them. Under that revert the wrapped row of
# `test_the_wrapped_row_...` sealed -- exit 0, SEALED drawn, and `a check
# failed` sitting in the kept output.

# #402's measured pair, as a row: a check that fails and whose output happens
# to be runnable. Bare it exits 1. Wrapped, the shell runs the content,
# discards the 1, and executes the word the content printed -- `true`.
FAILS_BUT_PRINTS_A_COMMAND = 'echo true; echo "a check failed" >&2; false'


def refusal_of(repo, value, keep):
    """The gate run over a fixture whose row is VALUE, asserted to be a
    refusal with nothing run — the shape `test_without_the_row_…` pins for
    the absent row, which is the sibling every refusal here sits beside."""
    out = run_gate(set_row(repo, value), keep=keep)
    assert out.returncode == 2, f"exit {out.returncode}; {out.stdout!r} {out.stderr!r}"
    assert not out.stdout, f"something printed under a refusal: {out.stdout!r}"
    assert ROW in out.stderr, f"the refusal does not name the row: {out.stderr!r}"
    assert "seal/config.md" in out.stderr.replace(os.sep, "/"), out.stderr
    return out.stderr


@pytest.mark.parametrize(
    "row, said",
    [
        # Nothing ran, and the exit is the same 1 a failing test gives.
        ("exit 1", True),
        # A summary was printed, so the form shows the count instead.
        ("echo 1 failed in 0.01s && exit 1", False),
    ],
)
def test_a_failing_row_with_no_summary_says_so_on_the_form(repo, tmp_path, row, said):
    """#448's A5, end to end. Both rows read the same under `/bin/sh` and
    `cmd.exe`, so this runs on every leg. The exit code stays 1 either way;
    what changes is one line on the failure form."""
    out = run_gate(set_row(repo, row), keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert "NOT SEALED" in out.stdout, out.stdout
    line = "no pytest summary in this output, so this exit code is not a count of"
    assert (line in out.stdout) is said, out.stdout
    if not said:
        assert "1 failed" in out.stdout, out.stdout


def test_a_row_wrapped_in_backticks_is_refused_and_shown_rewritten(repo, tmp_path):
    """A1. The reported mistake. The message names the form, quotes the value
    as written, and shows the row as meant — it does not strip anything: a
    value silently repaired leaves the file still wrong and the next person
    still believing backticks were fine (#402 §*Not this*)."""
    said = refusal_of(repo, f"`{SUITE_ROW}`", tmp_path / "out")
    assert "backticks" in said, said
    assert f"as written: | {ROW} | `{SUITE_ROW}` |" in said, said
    assert f"as meant:   | {ROW} | {SUITE_ROW} |" in said, said
    assert "Nothing ran" in said and "nothing was repaired" in said, said
    # The whole message, pinned HERE rather than only in A2 below. This case
    # reads a refusal, so it runs on every platform; A2 needs a POSIX shell
    # to have a subject at all, and `DISCARDED` used to be asserted only
    # there — which left the message's own wording unpinned on Windows.
    assert "DISCARDED" in said, said


def test_the_wrapped_row_that_would_have_seal_a_red_suite_is_refused(repo, tmp_path):
    """A2. The quiet direction, which is the one that matters: the same
    content exits 1 bare and exited 0 wrapped, with the failure still on the
    screen. Bare, the gate is NOT SEALED. Wrapped, it refuses rather than
    sealing — and under the revert this case was written against, it drew the
    stamp.

    **The pair is POSIX command substitution, and `cmd.exe` does not have
    it.** `FAILS_BUT_PRINTS_A_COMMAND` is a `;`-separated line ending in
    `false`; under `cmd.exe` it is one `echo` that succeeds, so the fixture's
    failing check does not fail and there is nothing for the wrapped half to
    be the counterfeit OF. This is not a defect that fails to reproduce there
    — it is a defect that does not exist there. The refusal itself still runs
    on every platform, in the case above.
    """
    posix_row_shell_or_skip()
    keep = tmp_path / "out"
    bare = run_gate(set_row(repo, FAILS_BUT_PRINTS_A_COMMAND), keep=keep)
    assert bare.returncode == 1, f"{bare.stdout}\n{bare.stderr}"
    assert "NOT SEALED" in bare.stdout, bare.stdout

    said = refusal_of(repo, f"`{FAILS_BUT_PRINTS_A_COMMAND}`", tmp_path / "out2")
    assert "DISCARDED" in said, said


def test_the_dollar_spelling_of_the_same_substitution_is_refused(repo, tmp_path):
    """A3. `agent-contract` §12: the fix is owed to every instance the same
    cause produces. Refusing the backtick spelling alone would close the
    instance and leave the cause standing in the spelling somebody who knows
    shell would reach for first."""
    said = refusal_of(repo, f"$({SUITE_ROW})", tmp_path / "out")
    assert "`$(…)`" in said, said
    assert f"as meant:   | {ROW} | {SUITE_ROW} |" in said, said


def test_a_row_ending_in_a_single_ampersand_is_refused(repo, tmp_path):
    """A4. The same green over the same nothing, reached by a different
    keystroke: the shell backgrounds the line and answers 0 before any check
    has finished. Enumerated from the class rather than reported from use."""
    said = refusal_of(repo, f"{SUITE_ROW} &", tmp_path / "out")
    assert "single `&`" in said, said
    assert f"as meant:   | {ROW} | {SUITE_ROW} |" in said, said
    assert "before any check has finished" in said, said
    # Round 1's 🟡 5. The message stated `/bin/sh` semantics as though they
    # were every platform's. Under `cmd.exe` a trailing `&` separates two
    # commands rather than backgrounding — a different wrong answer, refused
    # for the same half of the criterion — and `quote()` one function over
    # already says CI runs `windows-latest`.
    assert "`/bin/sh` backgrounds" in said, said
    assert "`cmd.exe`" in said, (
        "the message names one platform's semantics as though they were all"
    )


@pytest.mark.parametrize(
    "value",
    [
        f"({SUITE_ROW}) & echo second",
        f"{SUITE_ROW} & ruff check .",
        f"{SUITE_ROW} 2>&1",
        'grep "a & b" f && ' + SUITE_ROW,
    ],
)
def test_an_ampersand_that_is_not_last_stays_allowed(value):
    """Round 1's 🟡 1, pinned as the boundary the code actually draws.

    A backgrounding `&` breaks the criterion's second half wherever it
    stands, and only the TRAILING form is refused: `(a failing check) & echo
    second` exits 0 and `not_as_written` returns None. Executed by the round.

    It stays allowed rather than being refused, and the reason is in
    `templates/config.md`'s allowed list beside the form: telling an operator
    `&` from a `2>&1` or a quoted one needs the shell parser `spec.md` §Scope
    refuses, and a false deny would make a legitimate row unwritable. The last
    two values are what such a parser would have to get right.

    What is not defensible is the form being in neither list, which is what
    round 1 found. This case is the tree's half of that answer: the boundary
    is where the document now says it is, and it cannot move in silence.
    """
    module = gate_module()
    assert module.not_as_written("/seal", value) is None, (
        f"{value!r} is refused, and the allowed list says it is legal"
    )


def test_a_refused_row_runs_no_check_and_adds_no_worktree(repo, tmp_path):
    """A6. The refusal is raised before the output directory is made and
    before the first `run`, so nothing was spent — and `compare_at_base`,
    the second place the row reaches a shell, is downstream of that run. The
    scratch worktree it would add is what this asserts the absence of."""
    keep = tmp_path / "out"
    refusal_of(repo, f"`{SUITE_ROW}`", keep)
    assert not keep.exists() or not os.listdir(keep), (
        f"a check ran under a refusal: {os.listdir(keep)}"
    )
    worktrees = git(repo, "worktree", "list").stdout.splitlines()
    assert len(worktrees) == 1, f"a worktree was added under a refusal: {worktrees}"


# --- A5: what stays allowed still runs, and what is refused is a form -------


@pytest.mark.parametrize(
    "value, why, needs_posix",
    [
        (f"echo checking; {SUITE_ROW}", "a `;` needs a shell parser to judge", True),
        (
            f"{sys.executable} -m pytest -q -p no:cacheprovider $(echo tests)",
            "a substitution INSIDE a line still runs as what it reads as",
            True,
        ),
        (
            f"{SUITE_ROW} && echo done",
            "the `&&` chain is the shape every row takes",
            # `&&` is an operator in `cmd.exe` too, so this one is the row
            # every platform can actually compose, and it runs everywhere.
            False,
        ),
    ],
)
def test_the_forms_that_stay_allowed_are_sealed_exactly_as_today(
    repo, tmp_path, value, why, needs_posix
):
    """A5. The row is an arbitrary shell command line by design and that is
    unchanged (#402 §*Not this*). Each of these has a cost and the cost is
    stated in `templates/config.md` rather than paid for by a refusal — a
    piped row exits with the pipe's last status, which is a claim the
    repository made about itself.

    **Sealing is not the whole assertion, and it used to be.** `echo
    checking; …` under `cmd.exe` is one `echo` that succeeds: the gate sealed,
    the case passed, and the suite in the row had not run. Green for a reason
    that has nothing to do with what the case is named for — this release's
    own subject, in this module, on the platform nobody had looked at. CI
    never reported it, because a vacuous pass is a pass. So the suite's own
    output is read too: the row's command has to have run the fixture's one
    test. It used to be read off the panel's `suite` row, which a piped run
    no longer draws (#400); the row is `suite_counts` of this same kept text.
    """
    if needs_posix:
        posix_row_shell_or_skip()
    keep = tmp_path / "out"
    out = run_gate(set_row(repo, value), keep=keep)
    assert out.returncode == 0, f"{why}\n{out.stdout}\n{out.stderr}"
    assert "SEALED" in out.stdout and "NOT SEALED" not in out.stdout
    suite = (keep / "suite.txt").read_text(encoding="utf-8")
    assert gate_module().suite_counts(suite) == "1 passed", (
        f"{why}\nthe gate sealed without the row's suite running:\n{suite}"
    )


def test_an_unescaped_pipe_is_named_as_a_line_that_will_not_parse(repo, tmp_path):
    """A4 of #415, and both halves of `agent-contract` §14 — the new sentence
    is present AND the old one is gone.

    A pipe is allowed by the criterion: `not_as_written` returns None for it
    and nothing here restricts what a broad command may be. Written with
    markdown's escape it now reaches the row. Written BARE it still does not,
    because a bare pipe is where a cell of this table ends — and that is the
    spelling somebody typing *one shell command line* reaches for first.

    What changes for that person is the message, not the outcome. Saying the
    row is ABSENT sent them looking for a row that is sitting in front of
    them; the refusal now quotes the line they wrote and names the escape.

    This case used to pin the opposite — the absent-row message, recorded as
    what the tree did rather than what anybody wanted, *so that the day
    `config_rows` learns to carry a pipe, this case is what says so*. This is
    that day.
    """
    bare = f"{SUITE_ROW} | cat"
    said = refusal_of(repo, bare, tmp_path / "out")
    assert "does not parse as a row" in said, said
    assert bare in said, (
        f"the refusal does not quote the line the person wrote:\n{said}"
    )
    assert "\\|" in said, "the refusal names no way to write the pipe"
    assert "has no `Broad gate` row" not in said, (
        "the absent-row sentence survived beside the new one, which is two "
        "causes offered for one line"
    )
    module = gate_module()
    assert module.not_as_written("/seal", bare) is None, (
        "the pipe was refused by this work's criterion, which allows it"
    )


def refusal_over(tmp_path, name, table):
    """`missing_row` over a config written literally, with no helper between
    the case and the bytes. Every fixture in this region is malformed on
    purpose, so a builder that assembled a well-formed table and checked it
    read back would swallow the subject (`plan.md` §*Every fixture here is
    malformed on purpose*)."""
    home = tmp_path / name / "seal"
    home.mkdir(parents=True)
    (home / "config.md").write_text(table, encoding="utf-8")
    return gate_module().missing_row(str(home))


LOST = "every row written BELOW that line is lost"
KEPT = "the stop rule needs a row before it can stop"
# #430's four sentences, in the two prepositions the arms they live in
# already use: an arm speaking about the line it QUOTES says `below it`, and
# an arm speaking about the line that STOPPED the reader says `under that
# line`. The wording is `spec.md` §*Data & interfaces*'s contract.
#
# **Each says no ROW was written, which is what the value supports.** `below`
# holds what parsed, and a further line the reader will not take as a row is
# written under that line too — so *nothing was written* was false wherever a
# second malformed line stood below the first (round 1's 🟡 3). `MOVES` is
# what those arms say instead of predicting that one edit finishes the file.
ALONE = "no row was written below it"
ALONE_UNDER = "no row was written under that line"
OTHERS = "Every other row under that line is gone the same way"
# Site 4 is the one sentence of the four whose line DOES have a row under it
# — this gate's own, which is why the branch was entered at all — so what it
# can say is that no OTHER row was.
NO_OTHERS = "No other row was written under that line"
MOVES = "moves the stopping place down"
WHOLE = "is the whole of what changes"


def test_what_a_refused_line_cost_is_read_off_the_file_and_not_stated_flat(
    tmp_path,
):
    """Round 1's 🟡 1 of #415. The reader breaks on a line it cannot parse
    only once it has FOUND a row, so the same piped line costs the rows below
    it or costs only itself depending on whether anything parsed above it.
    The branch measured that and wrote it into five records; the sentence a
    person actually reads said the rows were lost either way, and a person
    whose rows arrived was sent to reformat them — this work item's own
    defect, one file over.

    **Both tables are in one case on purpose.** A case that asserted only
    that the conditional sentence exists would pass just as well with the
    chooser wired to the wrong answer, and wiring it to one answer is exactly
    what the old code did. The pair is what makes the CONDITION the subject:
    it is red when the cost is stated flat, and red again when the two
    sentences are swapped.
    """
    below_it = (
        "| Item | Value |\n|---|---|\n"
        "| Record language | English |\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
    )
    first_row = (
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
        "| Record language | English |\n"
    )
    took = refusal_over(tmp_path, "took", below_it)
    kept = refusal_over(tmp_path, "kept", first_row)

    assert "does not parse as a row" in took, took
    assert LOST in took, (
        "a row parsed above the piped line, so the reader stopped there and "
        f"the rows below it did not arrive — the refusal does not say so:\n{took}"
    )
    assert KEPT not in took, took

    assert "does not parse as a row" in kept, kept
    assert LOST not in kept, (
        "the piped line is this table's FIRST row, so nothing had parsed "
        "above it, the reader stepped past it, and `Mode` and `Record "
        f"language` both arrived. The refusal says they were lost:\n{kept}"
    )
    assert KEPT in kept, (
        f"the refusal drops the cost sentence instead of correcting it:\n{kept}"
    )


def test_the_rows_below_a_first_row_refusal_really_do_arrive(tmp_path):
    """The other half of the case above, and the reason it may say what it
    says. The sentence is only true because the reader returns those rows —
    asserted here against `config_rows` itself, so that a change to the stop
    rule turns the claim red rather than leaving a refusal asserting a
    behaviour the reader no longer has."""
    module = gate_module()
    config = module.load(module.CONFIG_READER, "specseal_config_for_this_case")
    rows = config.config_rows(
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
        "| Record language | English |\n"
    )
    assert rows == [("Mode", "shared"), ("Record language", "English")], rows


def test_a_broad_gate_row_below_a_refused_line_is_not_reported_absent(tmp_path):
    """Round 1's 🟡 3 of #415, and the class `agent-contract` §12 asks for:
    a `Broad gate` row the reader could not reach. The build closed the
    member where the refused line IS the `Broad gate` line; this is the
    member one item over, where the person's row is sitting in the file and
    the gate calls it absent — the wrong-cause message this work item exists
    to end.

    **Nobody has to type a pipe to reach it.** The line below is a Windows
    path ending in a separator, which was a row before this branch and is not
    one after it, because a backslash immediately before the closing pipe is
    now markdown's escaped pipe (`spec.md` §*What this repair cannot see*).
    """
    said = refusal_over(
        tmp_path,
        "hidden",
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\docs\\|\n"
        f"| {ROW} | bin/test -q |\n",
    )
    assert f"has no `{ROW}` row" not in said, (
        f"the row is in the file, below a line the reader refused:\n{said}"
    )
    assert "does not parse as a row" in said, said
    assert "see C:\\docs\\" in said, (
        f"the refusal does not show the line that hid the row:\n{said}"
    )
    assert "never reached it" in said, said


def test_a_refused_row_of_some_other_item_is_not_read_as_this_one(tmp_path):
    """The branch is about the `Broad gate` row and reads the refused line's
    first cell to say so. A file whose unparseable line names a different
    item has no `Broad gate` row to quote, and the absent-row refusal is the
    true one there.

    **This is also the guard on the case above.** That one fires on a refused
    line naming another item only when a `Broad gate` row is actually sitting
    below it; a branch that fired on every such line would tell this person
    to go looking for a row their file does not contain, which is the wrong
    cause again with the words rearranged. There is no `Broad gate` row in
    this fixture, so the absent-row refusal is the true one and this case is
    what keeps it (#415 round 1 🟡 3).
    """
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Mode | shared |\n| Record language | a | b |\n",
        encoding="utf-8",
    )
    module = gate_module()
    assert module.refused_broad_row(str(home)) is None, (
        "a refused line naming another item was read as the `Broad gate` row"
    )
    assert f"has no `{ROW}` row" in module.missing_row(str(home))


def test_a_second_refused_line_is_what_decides_what_a_first_one_cost(tmp_path):
    """Round 2's 🟡 1 of #415. The refusal answered about the FIRST line it
    would not take as a row, and both sentences the gate builds are about the
    TABLE — which rows failed to arrive, and whether this gate's row is one of
    them. Those are the same line only while there is one bad line in the file.

    **Both directions are here, because the unit was wrong in both.** With
    some other item refused first, this gate's row sits under the SECOND bad
    line and was reported ABSENT — round 1's 🟡 3 with one more line in the
    file. With the `Broad gate` line itself refused first, a later bad line
    loses rows the refusal then calls read, and nothing sends that person
    back.

    **The one-bad-line file is in the same case, and it is the half a chooser
    keyed on the ROWS still gets wrong.** A `Broad gate` line written last in
    its table loses nothing below it, because there is nothing below it — and
    a chooser reading *no rows were lost* as *the table had not begun* tells a
    person with a `Mode` row above their eyes that nothing parsed above this
    line. What the ARM is read off is the STOPPING line, and this fixture is
    what says so.

    **Its other assertion moved, and the move is the subject of #430.** This
    case used to pin *every row written BELOW that line is lost* for this
    file, recorded as what the tree did while this very docstring said the
    file loses nothing — the defect and its own description sitting one
    paragraph apart. The arm is unchanged and still pinned by `KEPT not in`;
    what the arm SAYS is now read off `below`, and
    `test_a_refused_line_last_in_its_table_took_nothing_and_is_told_so` is
    where both directions of that are pinned.
    """
    hidden = refusal_over(
        tmp_path,
        "hidden_under_the_second",
        "| Item | Value |\n|---|---|\n"
        "| Notes | see C:\\docs\\|\n"
        "| Mode | shared |\n"
        "| Other | see C:\\x\\|\n"
        f"| {ROW} | bin/test -q |\n",
    )
    assert f"has no `{ROW}` row" not in hidden, (
        f"the row is in the file, under the SECOND refused line:\n{hidden}"
    )
    assert "never reached it" in hidden, hidden
    assert "see C:\\x\\" in hidden, (
        "the refusal shows the first refused line rather than the one that "
        f"actually stopped the reader:\n{hidden}"
    )
    assert "see C:\\docs\\" not in hidden, (
        "the line quoted is the first refused one, which the reader stepped "
        f"past and read on from — it took nothing:\n{hidden}"
    )

    lost = refusal_over(
        tmp_path,
        "lost_under_the_second",
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\docs\\|\n"
        "| Record language | Korean |\n",
    )
    assert "The reader stopped LOWER DOWN" in lost, (
        "`Record language` did not arrive, and the refusal tells the person "
        f"every row below this line was read:\n{lost}"
    )
    assert "see C:\\docs\\" in lost, (
        f"the line that lost the rows is not named:\n{lost}"
    )
    assert "so every row under that line is lost" in lost, lost

    last = refusal_over(
        tmp_path,
        "refused_and_last",
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n",
    )
    assert ALONE in last, (
        "a `Mode` row parsed above this line and the line is what stopped "
        f"the reader, so the cost is the rows below it — none, here:\n{last}"
    )
    assert KEPT not in last, (
        "a `Mode` row parsed above this line and the line is what stopped "
        "the reader, so the cost is the rows below it — none, here. The "
        f"refusal says the table had not begun:\n{last}"
    )


def test_the_gate_reads_every_refused_line_and_not_only_the_first(tmp_path):
    """The other half of round 2's 🟡 1, and the one that reaches the message
    this work item exists to end. The gate asked whether the FIRST refused
    line was its own row; a file with two of them can have this row under the
    second, and the answer was *has no `Broad gate` row* about a line sitting
    in front of the person.

    Three shapes, all of them a `Broad gate` line the reader will not take:
    below another refused line, below the line that STOPPED the reader, and
    below a paragraph of prose written above the table's first row — where
    the walk used to give up although `config_rows` steps past prose and
    reads on (round 2's correction). Each was reported absent.
    """
    module = gate_module()
    config = module.load(module.CONFIG_READER, "specseal_config_for_this_case")

    second = refusal_over(
        tmp_path,
        "refused_second",
        "| Item | Value |\n|---|---|\n"
        "| Notes | see C:\\x\\|\n"
        "| Mode | shared |\n"
        f"| {ROW} | bin/test -q | tee out |\n",
    )
    assert f"has no `{ROW}` row" not in second, (
        f"the row is in the file and it is the SECOND refused line:\n{second}"
    )
    assert "bin/test -q | tee out" in second, second
    # This fixture's refused line is the LAST row of its table, so what it
    # cost is itself alone — #430's own instance, pinned here as `LOST`
    # while the shape it describes has no row below it at all. The subject
    # of this case is that the SECOND refused line is the one answered
    # about, which the assertion above is what pins.
    assert ALONE in second, second

    under = refusal_over(
        tmp_path,
        "refused_under_the_stopper",
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\x\\|\n"
        f"| {ROW} | bin/test -q | tee out |\n",
    )
    assert f"has no `{ROW}` row" not in under, (
        f"the row is in the file, below the line that stopped the reader:\n{under}"
    )
    assert "never even reached it" in under, under
    assert "see C:\\x\\" in under, (
        f"the line the reader stopped at is not named:\n{under}"
    )

    prose_table = (
        "| Item | Value |\n|---|---|\n"
        "a paragraph written above the first row, which the reader steps past\n"
        f"| {ROW} | bin/test -q | tee out |\n"
        "| Mode | shared |\n"
    )
    prose = refusal_over(tmp_path, "refused_under_prose", prose_table)
    assert f"has no `{ROW}` row" not in prose, (
        f"the row is in the file, below a line of prose the reader skips:\n{prose}"
    )
    assert KEPT in prose, prose
    assert config.config_rows(prose_table) == [("Mode", "shared")], (
        "the sentence above is only true because the reader steps past both "
        "the prose and the refused line and goes on to read `Mode`"
    )

    home = tmp_path / "refused_under_the_stopper" / "seal"
    assert module.refused_broad_row(str(home)) is not None, (
        "the gate's other caller asks the same question and got None for a "
        "line sitting in the file"
    )


def test_a_refused_line_last_in_its_table_took_nothing_and_is_told_so(tmp_path):
    """A8 and A9 of #430, site 2 — the instance the ticket names.

    The arm that fires when the quoted line is the line that stopped the
    reader ended *every row written BELOW that line is lost with it*, without
    ever asking whether anything was written below it. `seal/config.md` in
    this repository ends with the `Broad gate` row, and so does the table
    `templates/config.md` ships, so the file somebody is likeliest to be
    holding the first time they type a bare pipe is the file that sentence is
    false about.

    **Both directions are in one case, for the reason the case above this one
    states.** A9 is the same file with a row genuinely under the refused
    line, and it is what keeps the repair from being a flat swap: red when
    the new sentence is printed unconditionally, and red again when the two
    are exchanged.
    """
    table = "| Item | Value |\n|---|---|\n| Mode | shared |\n"
    refused_line = f"| {ROW} | bin/test -q | tee out.txt |\n"

    last = refusal_over(tmp_path, "a8_last_row", table + refused_line)
    assert "does not parse as a row" in last, last
    assert ALONE in last, (
        "the refused line is the last row of its table, so nothing was "
        f"written below it and nothing else was lost:\n{last}"
    )
    assert LOST not in last, (
        f"the refusal names rows nobody wrote — #430's own instance:\n{last}"
    )
    assert KEPT not in last, (
        "a `Mode` row parsed above this line and the line is what stopped "
        f"the reader, so the table HAD begun:\n{last}"
    )

    below = refusal_over(
        tmp_path,
        "a9_row_below",
        table + refused_line + "| Record language | Korean |\n",
    )
    assert LOST in below, (
        "`Record language` is written under the stopping line and never "
        f"arrived — the refusal has to say it was lost:\n{below}"
    )
    assert ALONE not in below, (
        "a row IS written below the stopping line, and the refusal says "
        f"nothing was:\n{below}"
    )


def test_a_refusal_above_the_first_row_says_what_actually_arrived(tmp_path):
    """A10 of #430, site 1 — the arm for a line nothing had parsed above.

    The reader steps past a line it cannot parse until it has found a row, so
    a `Broad gate` line written as the table's FIRST row loses only itself.
    The sentence said *The rows below it were read*, which names rows nobody
    wrote where that line is the table's ONLY row.

    **What this arm reads is not `below`.** `hooks/config.py#refusal` fills
    `below` with the rows written under the STOPPING line, and this arm is
    the one where no line stopped the reader at all — so `below` is `[]` in
    both fixtures here and cannot tell them apart. Measured, this session.
    What tells them apart is what the reader actually returned, and in this
    arm every row it returned is below the quoted line: a row parsed ABOVE it
    would have made that line the stopping one, which is site 2's arm.
    """
    only_row = f"| Item | Value |\n|---|---|\n| {ROW} | bin/test -q | tee out.txt |\n"
    alone = refusal_over(tmp_path, "site1_only_row", only_row)
    assert "does not parse as a row" in alone, alone
    assert ALONE in alone, (
        "this line is the whole table — there is nothing below it and no row "
        f"was read:\n{alone}"
    )
    assert "rows below it were read" not in alone, (
        f"the refusal names rows nobody wrote:\n{alone}"
    )
    assert KEPT in alone, (
        "the half that explains WHY the line took nothing is the stop rule, "
        f"and dropping it leaves the person with no cause:\n{alone}"
    )

    with_rows = refusal_over(
        tmp_path, "site1_rows_below", only_row + "| Mode | shared |\n"
    )
    assert "rows below it were read" in with_rows, (
        "`Mode` is written below this line and the reader stepped past the "
        f"line and read it — the refusal has to say so:\n{with_rows}"
    )
    assert ALONE not in with_rows, (
        f"a row IS written below the line, and the refusal says none is:\n{with_rows}"
    )

    module = gate_module()
    config = module.load(module.CONFIG_READER, "specseal_config_for_this_case")
    assert config.config_rows(only_row) == [], (
        "the sentence above is only true because the reader returns no row "
        "for this file"
    )
    assert config.config_rows(only_row + "| Mode | shared |\n") == [
        ("Mode", "shared")
    ], "the other half is only true because `Mode` does arrive"


def test_the_arm_whose_repair_costs_a_row_says_there_is_more_to_write(tmp_path):
    """Round 2's 🟡 4. The arm where the rows below the quoted line WERE read
    is the only one where doing what the refusal asks makes the file worse,
    and it was the one arm with nothing to say about what lies below.

    Nothing has parsed above the quoted line, so the reader steps past both
    malformed lines and the `Mode` row arrives. Escape the pipe as the message
    instructs and the quoted line parses — which is what lets the stop rule
    stop, and it stops at the second malformed line, so the `Mode` row that
    was being read is lost. The person follows the instruction exactly and
    loses a declaration nothing warned them about.

    **The reader is asserted either side of the instructed edit**, because the
    sentence is only worth printing while that is what the edit costs.
    """
    quoted = f"| {ROW} | bin/test -q | tee out.txt |\n"
    with_a_second = (
        "| Item | Value |\n|---|---|\n"
        + quoted
        + "| Record language | a | b |\n| Mode | shared |\n"
    )
    said = refusal_over(tmp_path, "rows_read_and_more_to_write", with_a_second)
    assert "The rows below it were read" in said, said
    assert "There is more than one line to write here" in said, (
        "repairing this line switches the stop rule on and the next line the "
        f"reader will not take is where it stops — the `Mode` row goes:\n{said}"
    )

    alone = refusal_over(
        tmp_path,
        "rows_read_and_nothing_else_to_write",
        "| Item | Value |\n|---|---|\n" + quoted + "| Mode | shared |\n",
    )
    assert "The rows below it were read" in alone, alone
    assert "more than one line to write" not in alone, (
        "this line is the only one the reader will not take, so repairing it "
        f"costs nothing:\n{alone}"
    )

    module = gate_module()
    config = module.load(module.CONFIG_READER, "specseal_config_for_this_case")
    assert config.config_rows(with_a_second) == [("Mode", "shared")], (
        "the sentence is only worth printing because that row arrives today"
    )
    assert config.config_rows(with_a_second.replace("-q | tee", "-q \\| tee")) == [
        (ROW, "bin/test -q | tee out.txt")
    ], "and because the instructed edit is what loses it"


def test_a_stopping_line_lower_down_with_nothing_under_it_names_no_rows(tmp_path):
    """A10 of #430, site 3 — the quoted line was read and something LOWER
    DOWN stopped the reader.

    The sentence ended *so every row under that line is lost*, computed from
    the stopping line's existence rather than from what was written under it.
    Reachable with a refused line above the table's first row, a row, and a
    second refused line written last: the reader stops at the second, and
    there is nothing under it to lose.

    The half that explains the cause — the stop rule, and the quoted stopping
    line — stays in both directions, because that is what the person acts on.
    """
    table = (
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\docs\\|\n"
    )
    nothing_under = refusal_over(tmp_path, "site3_nothing_under", table)
    assert "The reader stopped LOWER DOWN" in nothing_under, nothing_under
    assert "see C:\\docs\\" in nothing_under, (
        f"the line that stopped the reader is not named:\n{nothing_under}"
    )
    assert ALONE_UNDER in nothing_under, (
        "the stopping line is the last line of the table, so nothing was "
        f"written under it and nothing else was lost:\n{nothing_under}"
    )
    assert "so every row under that line is lost" not in nothing_under, (
        f"the refusal names rows nobody wrote:\n{nothing_under}"
    )
    assert KEPT in nothing_under, (
        "the half that says why THIS line cost nothing is the stop rule:\n"
        f"{nothing_under}"
    )

    row_under = refusal_over(
        tmp_path, "site3_row_under", table + "| Record language | Korean |\n"
    )
    assert "so every row under that line is lost" in row_under, (
        "`Record language` is written under the stopping line and never "
        f"arrived:\n{row_under}"
    )
    assert ALONE_UNDER not in row_under, (
        f"a row IS written under the stopping line:\n{row_under}"
    )


def test_a_hidden_row_alone_under_the_stopping_line_has_no_others(tmp_path):
    """A10 of #430, site 4 — the hidden-row refusal, the one sentence of the
    class that is not inside `missing_row`'s arms.

    `hides_this_row` is true only when `below` holds this gate's row, so the
    branch is never entered on an empty `below` — and with that row alone
    under the stopping line, *Every other row under that line is gone the
    same way* names rows nobody wrote. That reachability is `questions.md`
    Q2 for this site, and this case is the instrument: measured this session
    at one row and at two.
    """
    table = (
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\docs\\|\n"
        f"| {ROW} | bin/test -q |\n"
    )
    one = refusal_over(tmp_path, "site4_one_row", table)
    assert "never reached it" in one, one
    assert f"has no `{ROW}` row" not in one, one
    assert OTHERS not in one, f"this gate's row is the only row under that line:\n{one}"
    assert NO_OTHERS in one, (
        "nothing else was written under the stopping line, and the refusal "
        f"has to say that rather than name other rows:\n{one}"
    )

    two = refusal_over(
        tmp_path, "site4_two_rows", table + "| Record language | Korean |\n"
    )
    assert "never reached it" in two, two
    assert OTHERS in two, (
        "`Record language` is written under the stopping line beside this "
        f"gate's row and went the same way:\n{two}"
    )
    assert NO_OTHERS not in two, f"another row IS written under that line:\n{two}"

    module = gate_module()
    config = module.load(module.CONFIG_READER, "specseal_config_for_this_case")
    assert config.refusal(table)[1] == [(ROW, "bin/test -q")], (
        "the sentence above is only true because this gate's row is the one "
        "and only row the stopping line took"
    )


def test_a_second_unparseable_line_below_is_not_called_nothing(tmp_path):
    """Round 1's 🟡 3, at all four sites of #430's class.

    That class is *a sentence about what lies below a line, computed without
    asking what is there*. Asking `below` narrows *what is there* to *what
    parsed as a row*, which closes the shape the tickets named and leaves this
    one: a second malformed line is neither a row nor nothing, and it is what
    the reader stops at next — so *this one line is the whole of what changes*
    is a prediction the file does not keep.

    **All four sites in one case, each with a line below it the reader will
    not take.** Measured before the fix: sites 1, 2 and 3 printed *nothing was
    written*, sites 2 and 3 promised one edit would finish the file, and site
    4 said nothing else was written under a line that has another one under
    it.

    The four sibling cases above are the other direction — the same arms with
    nothing below — so a repair that printed the new sentence flat turns those
    red and this one green.
    """
    head = "| Item | Value |\n|---|---|\n"
    bad = f"| {ROW} | bin/test -q | tee out.txt |\n"
    also_bad = "| Record language | a | b |\n"
    stops = "| Notes | see C:\\docs\\|\n"

    # The removed wording, which is what these fixtures make false. `ALONE`
    # and `ALONE_UNDER` above are the sentences that REPLACED it and are true
    # here, because no ROW was written below the quoted line — a line the
    # reader will not take as a row was.
    was_written = "nothing was written below it"
    was_written_under = "nothing was written under that line"

    site1 = refusal_over(tmp_path, "site1_second_bad_line", head + bad + also_bad)
    assert was_written not in site1, (
        f"a line IS written below it — `refusal` returned it:\n{site1}"
    )
    assert ALONE in site1, site1
    assert MOVES in site1, site1

    site2 = refusal_over(
        tmp_path, "site2_second_bad_line", head + "| Mode | shared |\n" + bad + also_bad
    )
    assert was_written not in site2, site2
    assert ALONE in site2, site2
    assert WHOLE not in site2, (
        "fixing this line moves the stopping place down to the next one the "
        f"reader will not take, so one edit does not finish the file:\n{site2}"
    )
    assert MOVES in site2, site2

    site3 = refusal_over(
        tmp_path,
        "site3_second_bad_line",
        head + bad + "| Mode | shared |\n" + stops + also_bad,
    )
    assert "The reader stopped LOWER DOWN" in site3, site3
    assert was_written_under not in site3, site3
    assert ALONE_UNDER in site3, site3
    assert WHOLE not in site3, site3
    assert MOVES in site3, site3

    site4 = refusal_over(
        tmp_path,
        "site4_second_bad_line",
        head + "| Mode | shared |\n" + stops + f"| {ROW} | bin/test -q |\n" + also_bad,
    )
    assert "never reached it" in site4, site4
    assert "Nothing else was written under that line" not in site4, site4
    assert NO_OTHERS in site4, (
        "this gate's row is still the only ROW under the stopping line, which "
        f"is what the sentence may claim:\n{site4}"
    )
    assert "will not take as rows either" in site4, site4


# --- #429: a `Broad gate` line written where no walk reads it ---------------

FENCED = "written inside a code fence"


def test_a_broad_gate_line_only_inside_a_fence_is_named_and_not_called_absent(
    tmp_path,
):
    """A6. The fence rule makes a fenced `| Broad gate |` line invisible to
    every walk of that table, which is what it is for — and then the
    absent-row refusal below it becomes a true sentence about a cause that is
    not the real one, which is the failure #415 was opened about arriving one
    shape over. The person is sitting in front of the row they are being told
    to write.

    Three things the message owes: the line as they wrote it, why nothing
    read it, and where they answer it.
    """
    said = refusal_over(
        tmp_path,
        "fenced_only",
        "# Repository config\n\n"
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n\n"
        "```markdown\n"
        f"| {ROW} | bin/test -q && uvx ruff check . |\n"
        "```\n",
    )
    assert FENCED in said, said
    assert f"| {ROW} | bin/test -q && uvx ruff check . |" in said, (
        f"the refusal does not quote the line the person wrote:\n{said}"
    )
    assert f"has no `{ROW}` row" not in said, (
        "the row is in the file and the refusal calls it absent — the "
        f"wrong-cause message this work item exists to end:\n{said}"
    )
    assert "does not parse as a row" not in said, (
        f"the line parses perfectly well; what is wrong is where it is:\n{said}"
    )
    assert "/specseal:config" in said, said
    # The other half of round 1's 🟡 2, and what keeps its repair from being a
    # flat swap. This fence IS closed, so the row really is inside an example
    # block and moving it is the act — the sentence for a fence nobody closed
    # would send this person looking for one.
    assert "Move the row into" in said, said
    assert "never closed" not in said, (
        f"every fence in this file is closed, and the refusal says one is not:\n{said}"
    )


def test_a_fence_opened_below_the_row_is_not_the_fence_above_it(tmp_path):
    """Round 2's 🟡 2. The refusal says *a fenced code block ABOVE it is never
    closed*, and the question it asked was whether the FILE has an opener
    nothing closes.

    So a row sitting in an example block that closes correctly, in a file that
    opens a second block lower down, was told to close a fence that has
    nothing to do with it — and the act that person needs, moving the row out
    of the example, was the sentence they did not get. Closing the later fence
    changes nothing about their row.

    **Both directions in one case.** The same file without the trailing block
    is the one the old code answered correctly, so a repair that simply
    stopped saying *Close that fence* leaves this pair green and A5's case
    red.
    """
    example = (
        "# Repository config\n\nAn example of the format:\n\n"
        "```markdown\n| Item | Value |\n|---|---|\n"
        f"| {ROW} | EXAMPLE |\n```\n"
    )
    opened_below = "\nAnd a block somebody opened and never closed:\n\n```markdown\n| Item | Value |\n"

    both = refusal_over(tmp_path, "fence_below", example + opened_below)
    assert FENCED in both, both
    assert "Move the row into" in both, (
        "the row is in a block that closes; moving it out is the act, and the "
        f"unclosed block below it is not its cause:\n{both}"
    )
    assert "never closed" not in both, (
        f"the refusal names a fence that has nothing to do with this row:\n{both}"
    )

    alone = refusal_over(tmp_path, "fence_below_removed", example)
    assert "Move the row into" in alone, alone
    assert "never closed" not in alone, alone


def test_the_absent_row_refusal_still_reaches_a_file_with_no_such_line(tmp_path):
    """The other half of the case above, and what keeps the new branch from
    swallowing every refusal: a file whose table simply has no `Broad gate`
    row anywhere, fenced or not, still gets the absent-row message."""
    said = refusal_over(
        tmp_path,
        "no_row_at_all",
        "| Item | Value |\n|---|---|\n| Mode | shared |\n\n```markdown\n| Mode | local |\n```\n",
    )
    assert f"has no `{ROW}` row" in said, said
    assert FENCED not in said, said


COMMENTED = "written inside an HTML comment"


@pytest.mark.parametrize("name", ["C11a", "C11b"], ids=["in the table", "below it"])
def test_a_broad_gate_line_only_inside_a_comment_is_named_and_not_called_absent(
    tmp_path, name
):
    """S7, C11 (#667). A row inside an HTML comment that closes is shown to
    no walk of the table, which is what the comment half is for -- and then
    the refusal has to say so, or it is the absent-row message about a row
    the person can see, or the fence message about a fence that is not there
    (the #429 wrong-cause shape). The sentence quotes the line, says it is
    commented out rather than absent or fenced, and runs nothing. Red at
    base: the commented row was the row, and a command nobody chose ran."""
    from block_shapes import SHAPES

    said = refusal_over(tmp_path, name, "\n".join(SHAPES[name]) + "\n")
    assert COMMENTED in said, said
    assert f"| {ROW} | bin/test -q |" in said, said
    assert "The row is not absent and it is not in a code fence" in said, said
    assert "take the row out of the comment" in said, said
    assert f"has no `{ROW}` row" not in said, said
    assert FENCED not in said, said
    assert said.endswith("Nothing ran."), said


def test_the_template_documents_the_commented_row_sentence():
    """S7's other half (contract §14): the sentence a person reads is stated
    where `templates/config.md` states the fenced one."""
    root = os.path.join(os.path.dirname(__file__), "..")
    with open(os.path.join(root, "templates", "config.md"), encoding="utf-8") as f:
        text = " ".join(f.read().split())
    assert "A row inside an HTML comment that closes is not a row either" in text
    assert "the refusal quotes that line and says it is commented out" in text


def test_the_template_names_every_inline_html_kind_it_reads_as_before():
    """#673's S10 (contract §14). The sentence tells a person which contexts
    are read as before, and the walk is unsure after any inline raw HTML a
    line leaves open, not after a comment opener alone. Each opener a
    person might write is named, and the old list's narrower phrase is gone."""
    root = os.path.join(os.path.dirname(__file__), "..")
    with open(os.path.join(root, "templates", "config.md"), encoding="utf-8") as f:
        text = " ".join(f.read().split())
    assert "after inline HTML a line leaves open" in text
    for opener in ("<" + "!--", "<![CDATA[", "<?", "<!DOCTYPE"):
        assert f"`{opener}`" in text, opener
    assert "or a tag started in the middle of a line" in text
    assert "after a `<" + "!--` in the middle of a line" not in text


@pytest.mark.parametrize("name", ["LS", "NEL"])
def test_the_gate_names_no_block_a_renderer_does_not_see(tmp_path, name):
    """#667 round 1, 🟡 1, `broad-gate`'s two questions of the reader. A
    `<!--` or a fence run after a character `str.splitlines` breaks at and
    CommonMark does not stands mid-line, so the row under it is in no comment
    and no fence is left open: `commented_row_at` finds nothing and
    `fence_left_open` says no. Both asked the split before."""
    from block_shapes import BREAKS, OPEN

    gate = gate_module()
    commented = tmp_path / "c" / "seal"
    commented.mkdir(parents=True)
    (commented / "config.md").write_text(
        f"A note{BREAKS[name]}{OPEN}\n\n| {ROW} | bin/test -q |\n-->\n",
        encoding="utf-8",
    )
    assert gate.commented_row_at(str(commented)) == (None, None)
    fenced = tmp_path / "f" / "seal"
    fenced.mkdir(parents=True)
    (fenced / "config.md").write_text(
        f"A note{BREAKS[name]}```\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n",
        encoding="utf-8",
    )
    assert gate.fence_left_open(str(fenced)) is False


def test_an_unclosed_fence_hides_the_live_table_and_the_gate_says_which_line(
    tmp_path,
):
    """A5. An unclosed fence runs to the end of the file, so it swallows the
    live table under it — and that lands on *nothing is declared*, which is
    the direction `hooks/config.py` fails in on purpose and the trade
    `plan.md` §*Alternatives considered* accepted for this rule.

    What makes it acceptable is that it is loud where it matters. The exit
    code is read directly off the process and no check ran, and the message
    names the fenced `| Broad gate |` line rather than reporting the row
    absent — so the person is told the one thing that gets them out of it.
    """
    repo = build_repo(tmp_path / "repo", row=False)
    write(
        repo,
        "seal/config.md",
        "# Repository config\n\n"
        "An example of the format:\n\n"
        "```markdown\n"
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        f"| {ROW} | {SUITE_ROW} |\n",
    )
    commit(repo, "a fence nobody closed")
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 2, f"exit {out.returncode}; {out.stdout!r} {out.stderr!r}"
    assert not out.stdout, f"something printed under a refusal: {out.stdout!r}"
    assert not keep.exists() or not os.listdir(keep), (
        f"a check ran under a refusal: {os.listdir(keep)}"
    )
    assert FENCED in out.stderr, out.stderr
    assert f"| {ROW} | {SUITE_ROW} |" in out.stderr, (
        f"the refusal does not quote the line that was swallowed:\n{out.stderr}"
    )
    assert f"has no `{ROW}` row" not in out.stderr, out.stderr
    # Round 1's 🟡 2. The quoted line is the person's LIVE row: it is already
    # in an `| Item | Value |` table and that table is inside no fence anyone
    # wrote — a fence three lines above it was opened and never closed. Told
    # to move the row, they would follow the instruction exactly and change
    # nothing, which is the wrong-cause shape this work item is about.
    assert "never closed" in out.stderr, (
        f"the refusal names no cause the person can act on:\n{out.stderr}"
    )
    assert "Move the row into" not in out.stderr, (
        "the row is already in the live table, and the refusal tells the "
        f"person to move it there:\n{out.stderr}"
    )


def test_both_reads_behind_one_refusal_apply_the_fence_rule(tmp_path):
    """`missing_row` reads the config twice for one refusal — `refusal(home)`
    always, and `rows_read(home)` in the arm where no line stopped the reader
    (#430's site 1). Both go through `hooks/config.py`, so the fence rule
    reaches both by construction; this is that measured rather than assumed.

    The fixture is the one shape where the two could disagree: a fenced
    example BELOW a line with nothing parsed above it. A `rows_read` that did
    not apply the rule would hand back the example's rows, and the refusal
    would tell the person the rows below their line were read — naming rows
    out of a block nobody meant as an answer.
    """
    said = refusal_over(
        tmp_path,
        "two_reads",
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "```markdown\n| Mode | local |\n| Broad gate | EXAMPLE |\n```\n",
    )
    assert "does not parse as a row" in said, said
    assert ALONE in said, (
        "the only rows under this line are inside a code fence, so nothing "
        f"the reader answers with was written below it:\n{said}"
    )
    assert "rows below it were read" not in said, (
        f"the refusal names rows out of an example block:\n{said}"
    )
    assert KEPT in said, (
        f"the half that explains why the line took nothing is gone:\n{said}"
    )


def test_the_documents_state_the_fence_rule_the_refusal_points_at(tmp_path):
    """`agent-contract` §14: a fix that changes what a person sees documents
    it and pins it, in the same commit.

    Two documents and one pointer. `templates/config.md` is the one home of
    what this table's format allows, and the refusal sends the reader to a
    named section of it — so the section has to still be there, and it has to
    say the thing the refusal is about. `skills/config/SKILL.md` step 3 is
    the coordinate that INVITES the shape: it tells a session to copy a block
    carrying a fenced example row and used to name no position for it.
    """
    template = open(
        os.path.join(ROOT, "templates", "config.md"), encoding="utf-8"
    ).read()
    skill = open(
        os.path.join(ROOT, "skills", "config", "SKILL.md"), encoding="utf-8"
    ).read()
    said = refusal_over(
        tmp_path,
        "pointer",
        "| Item | Value |\n|---|---|\n| Mode | shared |\n"
        f"```\n| {ROW} | bin/test -q |\n```\n",
    )

    section = "### What is refused, and what stays allowed"
    assert section in template, (
        f"the refusal points at a section that is not there:\n{said}"
    )
    assert section.lstrip("# ") in said, said
    for claim in (
        "A table inside a code fence is an example of this format",
        "outside every fenced code block",
        "runs to the end of the file",
    ):
        assert claim in template, f"`templates/config.md` does not say: {claim}"
    assert "The copied block lands BELOW the live table" in skill, (
        "the instruction that produces the shape still names no position for "
        "the block it copies"
    )


def test_two_refused_lines_of_one_character_do_not_collide(tmp_path):
    """Round 2's 🟡 3. The tail below the stopping line was found with
    `line is stopper` over a list the loop did not stop walking, so the tail
    came from the LAST line that satisfied it.

    `refused` holds line text, and CPython hands back one shared object for
    every one-character string — so two refused lines that are both `|` are
    one object, the test matched both, and the clause saying more lines stand
    below was dropped although one does. Nothing about the text is wrong:
    the same file with `| x` as its second line printed the clause, which is
    what says the defect is the identity test and not the fixture.

    Both directions here, and the second is what the first is measured
    against.
    """
    two_pipes = (
        "| Item | Value |\n|---|---|\n| Mode | shared |\n|\n|\n"
        f"| {ROW} | bin/test -q |\n"
    )
    collided = refusal_over(tmp_path, "two_bare_pipes", two_pipes)
    assert "never reached it" in collided, collided
    assert "will not take as rows either" in collided, (
        "a second line the reader will not take stands below the stopping "
        f"line, and the refusal says nothing about it:\n{collided}"
    )

    distinct = refusal_over(
        tmp_path, "one_of_them_longer", two_pipes.replace("|\n|\n", "|\n| x\n", 1)
    )
    assert "will not take as rows either" in distinct, distinct

    nothing_after = refusal_over(
        tmp_path,
        "nothing_below_the_stopper",
        f"| Item | Value |\n|---|---|\n| Mode | shared |\n|\n| {ROW} | bin/test -q |\n",
    )
    assert "will not take as rows either" not in nothing_after, (
        "the stopping line is the only line the reader will not take, and the "
        f"refusal names others:\n{nothing_after}"
    )


def test_this_repositorys_own_config_is_answered_exactly_as_before(tmp_path):
    """A11. The file this work item is about is in this repository, and every
    sentence above is a sentence about somebody else's file.

    `seal/config.md` here carries a `Mode` row and a `Broad gate` row and
    nothing the reader will not take, so all three answers are the ones it
    had before this work item: the mode, the command as the row wrote it, and
    no refusal to build at all. Run before and after each phase.
    """
    module = gate_module()
    config = module.load(module.CONFIG_READER, "specseal_config_for_this_case")
    home = os.path.join(ROOT, "seal")
    text = open(os.path.join(home, "config.md"), encoding="utf-8").read()

    assert config.declared_mode(home) == ("mode", "shared"), config.declared_mode(home)
    assert config.refusal(text) == ([], [], None), (
        f"a refusal is built from this repository's own config:\n{config.refusal(text)}"
    )
    command = module.broad_command(home)
    assert command and f"| {ROW} | {command} |" in text, (
        f"the command the gate reads is not the row as written:\n{command}"
    )
    assert module.not_as_written(home, command) is None, command
    # Phase 2's half of the same question. This file carries no backticks at
    # all, so the fence rule removes no line of it and every answer above is
    # the one it had before #429 — asserted rather than assumed, because
    # `fenced_row` is what the new refusal is built from.
    assert module.fenced_row(home) is None, module.fenced_row(home)
    assert "```" not in text and "~~~" not in text, (
        "this repository's own config grew a fence, and the assertions above "
        "stop being about a file that has none. Its header comment does carry "
        "single backticks, which open nothing: a fence is a run of three"
    )


def test_an_escaped_pipe_reaches_the_gate_as_the_command_it_reads_as(tmp_path):
    """A2 of #415. The whole path a value takes before a shell sees it:
    `broad_command` reads the row through `hooks/config.py#config_rows`, and
    `not_as_written` then judges what came back.

    Both units are the ones `gate()` itself calls. The escape is undone in
    the READER, so what arrives here — and what a shell is handed — is a
    plain `|`, on `/bin/sh` and on `cmd.exe` alike; neither meets the
    backslash at all.
    """
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(
        "# Repository config\n\n| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        f"| {ROW} | {SUITE_ROW} \\| tee out.txt |\n"
        "| Record language | English |\n",
        encoding="utf-8",
    )
    module = gate_module()
    command = module.broad_command(str(home))
    assert command == f"{SUITE_ROW} | tee out.txt", (
        f"the gate read {command!r} from a row written with `\\|`"
    )
    assert module.not_as_written(str(home), command) is None, (
        "a pipe satisfies the criterion (`templates/config.md` §*What is "
        "refused, and what stays allowed*) and nothing here restricts it"
    )


@pytest.mark.parametrize(
    "value",
    [
        SUITE_ROW,
        "$(echo a) && $(echo b)",
        "`a` && `b`",
        "pytest -n $(nproc)",
        "bin/test -q | tee out.txt",
        "bin/test -q && ruff check .",
        "sleep 1 && echo done",
        "a && b &&",
    ],
)
def test_a_pair_that_closes_early_wraps_a_part_and_not_the_whole(value):
    """The boundary, read directly off the unit. A substitution the value
    merely CONTAINS is the repository's own composition; only a matched pair
    around the whole value replaces the command with its own output. The last
    row is the `&&` a trailing-`&` check must not read as a lone `&`."""
    module = gate_module()
    assert module.wholly_substituted(value) is None, value
    assert module.not_as_written("/seal", value) is None, value


@pytest.mark.parametrize("pad", ["  `{}`  ", "\t`{}`", "`{}` \n"])
def test_a_padded_value_is_read_as_the_value_it_pads(pad):
    """`not_as_written` strips before it reads, and nothing reaching it
    through the gate can exercise that: `config_rows` strips every cell, and
    `broad_command` turns an all-whitespace value into None. Mutation-tested
    2026-09-15 — removing the `.strip()` left every other case green, which
    is a line claiming a defence it never performs.

    It is kept rather than deleted because the function is module-level and
    its correctness should not depend on which caller reaches it, and this
    case is what makes the keeping honest.
    """
    module = gate_module()
    value = pad.format(SUITE_ROW)
    said = module.not_as_written("/seal", value)
    assert said is not None, f"a padded wrapping went unrefused: {value!r}"
    assert "backticks" in said
    assert f"as meant:   | {ROW} | {SUITE_ROW} |" in said, said


# --- S1 sealed ---------------------------------------------------------------


def test_a_green_tree_is_sealed_with_every_check_run_in_order(repo, tmp_path):
    """S1 of #30, and S9 of 1790562543. Every check runs, its exit code is
    read off the process and kept with its output. Without `--record` a green
    run on a pipe is sealed and draws nothing: one `SEALED` line naming the
    tree and the base and saying nothing was recorded, no disc in either
    form, and no values file for anyone to draw — drawing a stamp takes the
    exit 0 AND the written cell (#400's Done-when). The panel's rows are
    pinned where they are drawn from, in the recorded case below."""
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep, session="s-1")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "NOT SEALED" not in out.stdout
    said = signal_lines(out.stdout)
    assert len(said) == 1, f"one `SEALED` line expected:\n{out.stdout}"
    assert said[0].startswith(head_of(repo)), said
    assert "nothing was recorded" in said[0], said
    # No cell was written, so nothing is uncommitted and the line that says
    # so is absent (#666's S2).
    assert "not committed" not in out.stdout, out.stdout
    assert crown_of() not in out.stdout, "a piped run drew the twin"
    assert not SGR.search(out.stdout), "a piped run carries colour codes"
    assert not any(c in out.stdout for c in HALF_BLOCKS), "a piped run drew blocks"
    assert not re.search(r"\brounds\b", out.stdout), "a rounds row without --record"
    assert not values_files(repo), "a run with no cell written left a stamp to draw"
    gate = gate_module()
    order = [
        gate.SUITE,
        gate.LEDGER,
        gate.UNVERIFIED_NAME,
        gate.CHAIN_NAME,
        gate.SURVIVORS_NAME,
    ]
    kept = sorted(os.listdir(keep))
    for name in order:
        assert f"{name}.txt" in kept, f"{name}'s output was not kept: {kept}"
        text = (keep / f"{name}.txt").read_text(encoding="utf-8")
        assert text.startswith("$ "), f"{name}.txt does not open with its command"
        assert "\nexit 0\n" in text, f"{name}.txt does not carry its exit code"
    times = [os.stat(keep / f"{n}.txt").st_mtime_ns for n in order]
    assert times == sorted(times), f"the checks did not run in order: {times}"


# --- 1790562543: a sealer's run signals, and the panel waits in a file -------


def test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing(repo, tmp_path):
    """S1 of 1790562543 (#400). A sealer's stdout is a pipe into a report
    that arrives folded, so the gate draws nothing there — not the block
    form, not the letter twin, even under the `--shape` `run_gate` passes.
    It writes one values file under the git common dir, keyed by the
    session, and prints one `SEALED` line naming the tree, the base commit
    and that file. The hook draws the file; this line is what the report
    carries.

    Run under a directory whose name holds a space (round 2's ⬜ 3): with no
    space the quoted and unquoted path are the same bytes, so the quoting
    assertion below could not tell a quoted command from a bare one."""
    spaced = tmp_path / "a checkout" / "repo"
    # The parent first, so the move is a rename on every platform. Without
    # it `shutil.move` falls back to a copy and an `rmtree`, which Windows
    # refuses over git's read-only object files.
    spaced.parent.mkdir(parents=True)
    shutil.move(str(repo), str(spaced))
    repo = spaced
    out, _values = sealed_values(repo, tmp_path, session="s-1")
    said = signal_lines(out.stdout)
    assert len(said) == 1, f"one `SEALED` line expected:\n{out.stdout}"
    (path,) = values_files(repo)
    assert said[0].startswith(head_of(repo)), said
    assert path in said[0], f"the line does not name the file {path}: {said}"
    assert "session s-1" in said[0], said
    # Round 1's 🟡 1. The hook draws nothing, and says nothing, where it
    # cannot — a `python3` under the floor, a session outside this clone, a
    # plugin older than the hook — so the common line names the recovery too.
    assert f"`seal-stamp --from {gate_module().quote(path)}`" in said[0], said
    assert " " in path and f"--from {path}`" not in said[0], said
    assert os.path.dirname(path) == str(repo / ".git" / VALUES_DIR / "s-1"), path
    assert not path.endswith(".drawn.json"), "the file was marked drawn by the gate"
    assert crown_of() not in out.stdout, "a piped run drew the twin"
    assert not SGR.search(out.stdout), "a piped run carries colour codes"
    assert not any(c in out.stdout for c in HALF_BLOCKS), "a piped run drew blocks"


def test_the_values_file_holds_this_runs_panel(repo, tmp_path):
    """S2 and S13 of 1790562543. The file holds the rows `panel` returned for
    this run — in `panel`'s order — and the scale the run was given, which
    with no `--scale` is `seal_stamp.DEFAULT_SCALE`. Nothing downstream
    re-derives a row: the drawing is these values.

    #666's A5: the whole sequence, positively, so a row that went missing
    cannot pass by being absent. The branch continues under `tree` and the
    base's ref under `base`; `item` is the work item's id with no pull
    request, because the fixture's record reads `not yet opened`; no `gate`
    row, because the fixture ships no gate; `from` and `row` are gone. No
    `CI also` row: the fixture has no workflow.

    #717's A6: the panel says only what a `SEALED` stamp can say. `chain`,
    the suite's `exit` row and the ledger's `drifted` row are gone, because
    a drawn panel is green by construction and `SEALED` already says each;
    and so is every blank, because the sheet draws none and the values file
    should not claim a row nothing draws."""
    _out, values = sealed_values(repo, tmp_path)
    assert values["rows"] == [
        ("SEALED", ""),
        ("tree", short(repo, "HEAD")),
        ("", "feature"),
        ("base", short(repo, "base")),
        ("", "base"),
        ("item", "1799000000"),
        ("suite", "1 passed"),
        ("ledger", "0 ok"),
        ("rounds", "2"),
    ], values["rows"]
    assert values["scale"] == module().DEFAULT_SCALE == 0.90, values["scale"]
    assert values["session"] == "s-1" and values["item"] == str(repo / ITEM)
    assert (values["tree"], values["base"]) == (
        short(repo, "HEAD"),
        short(repo, "base"),
    )


def test_a_run_with_no_session_says_so_and_names_the_hand_command(repo, tmp_path):
    """S14. With `CLAUDE_CODE_SESSION_ID` unset the run is still sealed and
    its values still written, under `none/`, which no hook reads. The line
    says no session was found and names `seal-stamp --from <path>`, so the
    stamp is not lost and nothing claims it will appear.

    Round 1's ⬜ 5: the path is quoted for the platform's shell, so a
    checkout whose path holds a space prints a command that runs as typed.
    The fixture is moved under such a directory to show it."""
    spaced = tmp_path / "a checkout" / "repo"
    # The parent first, so the move is a rename on every platform. Without
    # it `shutil.move` falls back to a copy and an `rmtree`, which Windows
    # refuses over git's read-only object files.
    spaced.parent.mkdir(parents=True)
    shutil.move(str(repo), str(spaced))
    settled_item(spaced)
    out = run_gate(spaced, "--record", str(spaced / ITEM), keep=tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    (path,) = values_files(spaced)
    assert " " in path, path
    assert os.path.basename(os.path.dirname(path)) == module().NO_SESSION, path
    (said,) = signal_lines(out.stdout)
    assert "no Claude Code session was found" in said, said
    assert f"`seal-stamp --from {gate_module().quote(path)}`" in said, said
    assert f"--from {path}`" not in said, f"the path is unquoted: {said}"


def test_values_that_cannot_be_written_leave_the_seal_standing(repo, tmp_path):
    """S15. The values directory cannot be made — a FILE stands where it
    goes, which refuses on every platform and under every user, where a
    permission bit would not stop root. The checks passed and the cell was
    written, so the run is still sealed, exit 0; stderr says why nothing
    will be drawn and the `SEALED` line says nothing will be."""
    _one, two = settled_item(repo)
    (repo / ".git" / VALUES_DIR).write_text("in the way\n", encoding="utf-8")
    out = run_gate(
        repo, "--record", str(repo / ITEM), keep=tmp_path / "out", session="s-1"
    )
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "the stamp's values could not be written" in out.stderr, out.stderr
    (said,) = signal_lines(out.stdout)
    assert "nothing will be drawn" in said, said
    assert fields(two.read_text(encoding="utf-8"))[ROW] != "not yet", (
        "the cell was not written, so this is not the state S15 is about"
    )


def test_a_person_at_a_terminal_sees_the_stamp_drawn_once(repo, tmp_path):
    """S10. A hand-run on a UTF-8 terminal draws the stamp there, once, in
    the block form, and prints no `SEALED` signal line beside it: the
    drawing IS the signal, and no values file is left for a hook to draw it
    a second time. A tool call has no terminal to reach this path with
    (#400, *The blocking measurement*), so it is a person's alone.

    Driven through a pseudo-terminal, which POSIX has and Windows does not."""
    settled_item(repo)
    code, screen = on_a_terminal(repo, tmp_path, "--record", str(repo / ITEM))
    assert code == 0, screen
    assert screen.count("SEALED") == 1, f"the stamp was not drawn once:\n{screen}"
    assert any(c in screen for c in HALF_BLOCKS), "a UTF-8 terminal got no blocks"
    assert not signal_lines(SGR.sub("", screen).replace("\r", "")), screen
    assert not values_files(repo), "a drawn run left a file for a hook to draw again"
    # #666's S2 on this path too: the cell is in the working tree here as well.
    assert "cell is written to" in screen and "not committed" in screen, screen


def test_a_terminal_run_with_no_record_draws_nothing(repo, tmp_path):
    """#400's Done-when, on a terminal: drawing a stamp takes the exit 0 AND
    the written cell, and no other path draws one. A green hand-run without
    `--record` wrote no cell, so a person's terminal gets the `SEALED` line
    saying nothing was recorded and no disc, the same as a pipe does (S9)."""
    code, screen = on_a_terminal(repo, tmp_path)
    assert code == 0, screen
    assert not any(c in screen for c in HALF_BLOCKS), f"a disc was drawn:\n{screen}"
    said = signal_lines(SGR.sub("", screen).replace("\r", ""))
    assert len(said) == 1 and "nothing was recorded" in said[0], screen
    assert not values_files(repo)


def on_a_terminal(repo, tmp_path, *extra):
    """The gate run with stdout a UTF-8 pseudo-terminal: its exit code and
    everything the terminal received. Skipped where there is no `pty`."""
    pty = pytest.importorskip("pty")
    env = env_without_a_pull_request()
    env[SESSION_VAR] = "s-1"
    env["PYTHONIOENCODING"] = "utf-8"
    main, child = pty.openpty()
    proc = subprocess.Popen(
        [
            sys.executable,
            GATE,
            "--base",
            "base",
            "--root",
            str(repo),
            "--keep-output",
            str(tmp_path / "out"),
            *extra,
        ],
        stdin=subprocess.DEVNULL,
        stdout=child,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    os.close(child)
    chunks = []
    while True:
        try:
            chunk = os.read(main, 65536)
        except OSError:
            break
        if not chunk:
            break
        chunks.append(chunk)
    os.close(main)
    return proc.wait(timeout=300), b"".join(chunks).decode("utf-8", "replace")


def test_the_wrapper_runs_the_same_gate(repo):
    """`bin/broad-gate` resolves the script relative to itself and passes
    every argument through; the wrapper pair is pinned by the bin twin case.

    This carried `skipif(os.name == "nt")` — *the POSIX wrapper needs a POSIX
    shell* — which is true of the POSIX file and was the reason to reach for
    the twin rather than to step around it. `bin/broad-gate.cmd` ships and
    had never been run by anything; `run_gate` picks it on Windows now, and
    this is the first case that exercises it."""
    out = run_gate(repo, wrapper=True)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "SEALED" in out.stdout


# --- #666: the lines name what they sealed, and say to commit the cell -------
#
# 0.16.0's first real stamp named the base and never the branch, so a reader
# matched the line to its work by hash. The head now reads `<branch> @ <tree>
# against <ref> @ <base commit>`, and a recorded seal says on the next line
# that the cell it wrote is not committed, because CI reads HEAD.


def set_field(path, label, value):
    """Rewrite one record's `| label | … |` cell; the record is committed by
    the caller."""
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(
            f"| {label} | {value} |" if line.startswith(f"| {label} |") else line
            for line in text.splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def test_a_recorded_seal_says_the_cell_is_written_and_not_committed(repo, tmp_path):
    """A1 and S2. The line after the `SEALED` line names the file the cell
    went into, says it is not committed, and says CI reads HEAD — on the same
    stream, so the sealer passes both on together. The file IS uncommitted,
    which is what makes the line true: `git status` names it."""
    out, values = sealed_values(repo, tmp_path)
    lines = out.stdout.splitlines()
    (at,) = [i for i, line in enumerate(lines) if line.startswith("SEALED")]
    rel = os.path.join(ITEM, "rounds", "round-2.md").replace("/", os.sep)
    assert lines[at + 1] == gate_module().CELL_UNCOMMITTED.format(path=rel), lines
    assert lines[at + 1] == (
        f"broad-gate: the `Broad gate` cell is written to {rel} and not "
        "committed. CI reads the record at HEAD, so commit it before the pull "
        "request is marked ready"
    )
    assert git(repo, "status", "--porcelain", "--", rel).stdout.strip(), (
        "the line says the cell is uncommitted over a file git calls clean"
    )
    assert values["branch"] == "feature" and values["pr"] is None, values


def test_the_line_is_absent_where_the_cells_file_is_committed(repo):
    """S2's other half, at the unit: `uncommitted_line` asks git rather than
    assuming, so a file that does not differ from HEAD gets no line, and no
    record gets none either."""
    gate = gate_module()
    _one, two = settled_item(repo)
    record = gate.Record(str(two))
    assert gate.uncommitted_line(str(repo), record) is None
    assert gate.uncommitted_line(str(repo), None) is None
    set_field(two, ROW, "abcdef1 against 1234567")
    said = gate.uncommitted_line(str(repo), record)
    assert said and os.path.join("rounds", "round-2.md") in said, said


def test_the_pull_request_the_record_names_reaches_the_values_file(repo, tmp_path):
    """A1, A7's number. `| PR | #12 |` on the record the cell lands on is
    read with `chain_check.PR_RE` and carried as `#12`; `not yet opened`,
    which the fixture's records hold, is None."""
    _one, two = settled_item(repo)
    set_field(two, "PR", "#12")
    commit(repo, "the pull request opened")
    out = run_gate(
        repo, "--record", str(repo / ITEM), keep=tmp_path / "out", session="s-1"
    )
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    (path,) = values_files(repo)
    values = module().read_values(path)
    assert values["pr"] == "#12"
    # A7 on the panel: the pull request leads the `item` row.
    assert row_of(values, "item") == "#12 . 1799000000", values["rows"]


def test_a_detached_head_names_the_tree_alone(repo, tmp_path):
    """A2. A detached HEAD has no branch, so the head reads the tree alone,
    with no stray `@` before it."""
    git(repo, "switch", "-q", "--detach")
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    (said,) = signal_lines(out.stdout)
    assert said.startswith(head_of(repo, branch=None)), said
    assert said.split(" against ", 1)[0] == f"SEALED   {short(repo, 'HEAD')}", said


def test_a_base_given_as_a_commit_is_named_once(repo, tmp_path):
    """A3. `--base <sha>` resolves to itself, so its ref IS the commit, and
    the head names it once: `against <commit>`, never `<commit> @ <commit>`.
    `run_gate`'s own `--base base` comes first, and argparse keeps the last."""
    commit_ = git(repo, "rev-parse", "base").stdout.strip()
    out = run_gate(repo, "--base", commit_, keep=tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    (said,) = signal_lines(out.stdout)
    assert said.startswith(
        f"SEALED   feature @ {short(repo, 'HEAD')} against {short(repo, 'base')} · "
    ), said


@pytest.mark.parametrize(
    "branch, ref, said",
    [
        ("feat/x", "origin/base", "feat/x @ aaa1111 against origin/base @ bbb2222"),
        (None, "origin/base", "aaa1111 against origin/base @ bbb2222"),
        ("feat/x", None, "feat/x @ aaa1111 against bbb2222"),
        ("feat/x", "bbb2222", "feat/x @ aaa1111 against bbb2222"),
        ("feat/x", "bbb2222" + "0" * 33, "feat/x @ aaa1111 against bbb2222"),
        ("feat/x", "bbb2", "feat/x @ aaa1111 against bbb2222"),
        # A branch whose name happens to begin the commit is still a branch:
        # only a ref spelled in hex is read as the commit itself.
        ("feat/x", "b", "feat/x @ aaa1111 against b @ bbb2222"),
        ("feat/x", "bbb-x", "feat/x @ aaa1111 against bbb-x @ bbb2222"),
    ],
)
def test_the_names_collapse_only_where_a_part_would_repeat(branch, ref, said):
    """S1's two collapses, at the composer all three lines share."""
    assert module().sealed_names("aaa1111", "bbb2222", branch, ref) == said


def test_the_failure_form_takes_the_same_names():
    """A4's head, at the unit: `not_sealed` names the branch and the ref the
    way the `SEALED` line does, and a caller naming neither gets the line it
    always got."""
    mod = module()
    failures = [("suite", ["1 failed"])]
    assert mod.not_sealed("aaa1111", "bbb2222", failures, "feat/x", "origin/base")[
        0
    ] == ("NOT SEALED   feat/x @ aaa1111 against origin/base @ bbb2222")
    assert mod.not_sealed("aaa1111", "bbb2222", failures)[0] == (
        "NOT SEALED   aaa1111 against bbb2222"
    )


def test_the_documents_name_the_line_that_says_to_commit_the_cell():
    """S2's documentation (`agent-contract` §14). The sealer is told the line
    exists and is passed on, and the orchestrator is told what to do with
    it — the commit is the orchestrator's act."""
    sealer = " ".join(sealer_text().split())
    assert "one more line says the `Broad gate` cell is written and not committed" in (
        sealer
    )
    assert "naming the branch and the tree, the ref and the base commit" in sealer
    orchestration = " ".join(
        read_document(os.path.join("skills", "code-review", "orchestration.md")).split()
    )
    assert (
        "the line under it says the `Broad gate` cell is written and not "
        "committed: CI reads the record at HEAD, so commit the cell before the "
        "pull request is marked ready"
    ) in orchestration


def read_document(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


# --- #666: the panel names what it sealed, and loses the rows that said
# nothing ---------------------------------------------------------------------


def checks_with(gate, suite="", ledger="", code=0):
    return {
        gate.SUITE: gate.Check(gate.SUITE, code, suite, "suite.txt"),
        gate.LEDGER: gate.Check(gate.LEDGER, code, ledger, "ledger.txt"),
        gate.CHAIN_NAME: gate.Check(gate.CHAIN_NAME, code, "", "chain.txt"),
    }


LONG_BRANCH = (
    "feat/666-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run"
)
# 1.2.3 is illustrative, not a release this repository has (`test_release_hygiene`).
LONG_REF = "refs/remotes/other/release/v1.2.3-hotfix"
LONG_SUITE = "12345 passed, 67890 skipped, 12 xfailed in 1234.56s"
LONG_LEDGER = "total: 12345 ok · 0 drifted · 0 broken · 0 external"


def test_no_value_on_the_panel_is_wider_than_the_frame_gives(tmp_path):
    """A5's width half and A6. Over the longest inputs a real run meets —
    this branch's own 73-character name, a ref under a second remote, five-
    digit counts — every value is at most `PANEL_VALUE_WIDTH`, the branch
    keeps its HEAD and ends in the marker, the ref starts with the marker and
    keeps its TAIL, and the rendered panel carries both. A value the frame
    cut would read as a shorter true statement, which is what the marker
    exists to prevent."""
    gate = gate_module()
    assert len(LONG_BRANCH) == 73, len(LONG_BRANCH)
    item = tmp_path / "1799000000-an-item-with-a-long-name"
    rows = gate.panel(
        "c46fd2db",
        gate.Base("release/v1.2.3-hotfix", "1e2bed90", LONG_REF, "1e2bed90"),
        checks_with(gate, LONG_SUITE + "\n", LONG_LEDGER + "\n"),
        str(item),
        copy=gate.copy_origin(ROOT),
        branch=LONG_BRANCH,
        pr="#12345",
        # Phase 3's longest `rounds` continuation: three homes, one a path.
        record=record_of(
            tmp_path,
            capped_record(
                verdicts=(
                    "| 🟡 1 | a | `f.py:1` | deferred seal/follow-up.md | why |\n"
                    "| 🟡 2 | b | `f.py:2` | deferred #12345 | why |\n"
                    "| 🟡 3 | c | `f.py:3` | deferred #12346 | why |\n"
                )
            ),
        ),
    )
    values = [row[1] for row in rows if row]
    # Round 1's 🟡 1, the owner's Q1 answer: a list continues on the rows
    # beneath its label rather than losing its tail to `...`. Only a branch
    # and a ref, which have no bound, are elided.
    at = next(i for i, row in enumerate(rows) if row and row[0] == "rounds")
    beneath = " ".join(value for _label, value in rows[at + 1 :])
    for home in ("seal/follow-up.md", "#12345", "#12346"):
        assert home in beneath, beneath
    assert all(label == "" for label, _value in rows[at + 1 :]), rows[at:]
    assert "67890 skipped" in " ".join(values), values
    assert "12 xfailed" in " ".join(values), values
    elided = [
        v for v in values if v.endswith(gate.ELISION) or v.startswith(gate.ELISION)
    ]
    assert len(elided) == 2, f"only the branch and the ref are elided: {elided}"
    assert all(len(v) <= gate.PANEL_VALUE_WIDTH for v in values), [
        v for v in values if len(v) > gate.PANEL_VALUE_WIDTH
    ]
    branch = rows[rows.index(("tree", "c46fd2db")) + 1]
    assert branch[0] == "" and branch[1].endswith(gate.ELISION), branch
    assert LONG_BRANCH.startswith(branch[1][: -len(gate.ELISION)]), branch
    ref = rows[rows.index(("base", "1e2bed90")) + 1]
    assert ref[0] == "" and ref[1].startswith(gate.ELISION), ref
    assert LONG_REF.endswith(ref[1][len(gate.ELISION) :]), ref
    assert ("item", "#12345 . 1799000000") in rows, rows
    drawn = "\n".join(module().stamp(rows, shape=True))
    assert branch[1] in drawn and ref[1] in drawn, drawn
    assert "/v1.2.3-hotfix" in drawn, "the ref's tail did not survive the frame"


# Eight distinct homes, the longest list of deferrals `rounds_rows` would
# continue: more than any work item in this tree has deferred to.
EIGHT_HOMES = (
    "seal/follow-up.md",
    "docs/the-broad-gate.md",
    "#12345",
    "#12346",
    "#12347",
    "#12348",
    "skills/verify/SKILL.md",
    "#12349",
)


def test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung(tmp_path):
    """#717's A5. Over the width case's longest inputs — a 73-character
    branch, a ref under a second remote, five-digit counts in three parts —
    plus the `gate` row, this repository's own hygiene workflow and a capped
    record deferring to eight distinct homes, the hook's message for that
    one panel, label and block form at `DEFAULT_SCALE`, is within
    `MESSAGE_BUDGET`, and `fitted` returns the 0.90 drawing itself: the
    ladder is a margin, not something an ordinary seal steps down. The
    drawing before #717 was over 10,000 characters for #666's rows alone."""
    gate, mod = gate_module(), module()
    item = tmp_path / "1799000000-an-item-with-a-long-name"
    verdicts = "".join(
        f"| 🟡 {n} | a | `f.py:{n}` | deferred {home} | why |\n"
        for n, home in enumerate(EIGHT_HOMES, 1)
    )
    with open(
        os.path.join(ROOT, ".github", "workflows", "hygiene.yml"), encoding="utf-8"
    ) as handle:
        workflow = handle.read()
    rows = gate.panel(
        "c46fd2db",
        gate.Base("release/v1.2.3-hotfix", "1e2bed90", LONG_REF, "1e2bed90"),
        checks_with(gate, LONG_SUITE + "\n", LONG_LEDGER + "\n"),
        str(item),
        workflow,
        copy=gate.copy_origin(ROOT),
        branch=LONG_BRANCH,
        pr="#12345",
        record=record_of(tmp_path, capped_record(verdicts=verdicts)),
    )
    beneath = " ".join(value for label, value in rows if label == "")
    for home in EIGHT_HOMES:
        assert home in beneath, (home, rows)
    assert any(label == "CI also" for label, _ in rows), rows
    values = {
        "tree": "c46fd2db",
        "base": "1e2bed90",
        "from": LONG_REF,
        "branch": LONG_BRANCH,
        "pr": "#12345",
        "item": str(item),
    }
    label = mod.label(values)
    at_first = "\n".join([label, *mod.stamp(rows, mod.DEFAULT_SCALE, shape=False)])
    assert len(at_first) <= mod.MESSAGE_BUDGET, len(at_first)
    assert mod.fitted([(label, rows, mod.DEFAULT_SCALE)]) == at_first


def test_a_list_too_long_for_its_row_continues_beneath_it():
    """Round 1's 🟡 1. `wrapped` breaks a list after a separator, keeps the
    separator at the end of the row it leaves, and puts the rest on `""`
    rows; a list that fits stays one row, at the frame's full width; and one
    part wider than the frame is the only thing `fit` elides."""
    gate = gate_module()
    assert gate.wrapped(
        "suite", ["12345 passed", ", 67890 skipped", ", 12 xfailed"]
    ) == [
        ("suite", "12345 passed,"),
        ("", "67890 skipped,"),
        ("", "12 xfailed"),
    ]
    assert gate.wrapped("suite", ["5081 passed", ", 10 skipped"]) == [
        ("suite", "5081 passed, 10 skipped")
    ]
    assert gate.wrapped("", ["3 deferred ->", " seal/follow-up.md", ", #664"]) == [
        ("", "3 deferred ->"),
        ("", "seal/follow-up.md, #664"),
    ]
    # A row that would fill the frame exactly is broken one piece early when
    # more follow, so the comma it ends with is not cut by `fit`.
    assert gate.wrapped("x", ["a" * 20, ", b", ", c"]) == [
        ("x", "a" * 20 + ","),
        ("", "b, c"),
    ]
    assert gate.wrapped("", ["1 deferred ->", " " + "x" * 30]) == [
        ("", "1 deferred ->"),
        ("", gate.fit("x" * 30)),
    ]


@pytest.mark.parametrize(
    "suite, rows",
    [
        (
            "768 passed, 1 skipped in 9.1s\n",
            [("suite", "768 passed, 1 skipped")],
        ),
        (
            "12345 passed, 67890 skipped in 9.1s\n",
            [("suite", "12345 passed,"), ("", "67890 skipped")],
        ),
        ("no summary here\n", [("suite", "exit 0")]),
    ],
)
def test_the_suite_carries_its_counts_and_nothing_under_them(suite, rows):
    """#717's A8, `suite`. The counts where pytest printed them, wrapped as
    #666 wraps them, and the row after the last counts row is the ledger's
    label — not `exit 0`, which a `SEALED` stamp already says. Where there
    are no counts the row reads `exit N`, which is then the only statement
    of what the suite did."""
    gate = gate_module()
    panel = gate.panel(
        "c46fd2db",
        gate.Base("base", "1e2bed90", "base", "1e2bed90"),
        checks_with(gate, suite),
        None,
    )
    at = panel.index(rows[0])
    assert panel[at : at + len(rows)] == rows, panel
    assert panel[at + len(rows)][0] == gate.LEDGER, panel


def test_the_ledger_carries_its_ok_count_and_nothing_beneath():
    """#717's A8, `ledger`, read from one `total:` line: `<N> ok`, and the
    row after it is the next label — `CI also` where a workflow is given —
    rather than `<D> drifted . <B> broken`, which under `--strict` is 0 and
    0 on every drawn panel. A ledger output with no total line reads
    `exit N`, as the suite does."""
    gate = gate_module()
    base = gate.Base("base", "1e2bed90", "base", "1e2bed90")
    workflow = (
        "jobs:\n  release:\n    steps:\n"
        "      - name: a declared review chain has the round record it claimed\n"
    )
    rows = gate.panel(
        "c46fd2db",
        base,
        checks_with(gate, ledger="total: 187 ok · 3 drifted · 4 broken · 0 x\n"),
        None,
        workflow,
    )
    at = rows.index(("ledger", "187 ok"))
    assert rows[at + 1][0] == "CI also", rows
    assert not any("drifted" in row[1] for row in rows), rows
    bare = gate.panel("c46fd2db", base, checks_with(gate), None)
    assert ("ledger", "exit 0") in bare, bare


def test_a_failing_ledger_ends_with_its_total_line(tmp_path):
    """A4's second half. `evidence-check` prints its `total:` line LAST and the
    failure form quotes a check's first eight lines, so a ledger refused for
    one drifted row reached the reader with no counts. The entry ends with
    the total now, once — not a second time where the quoted lines already
    hold it."""
    gate = gate_module()
    long_text = "\n".join(f"  DRIFTED  row {n}" for n in range(12))
    total = "total: 9 ok · 12 drifted · 0 broken · 0 external"
    lines = gate.failure_lines(
        gate.Check(gate.LEDGER, 2, f"{long_text}\n{total}\n", "ledger.txt")
    )
    assert lines[-2:] == [total, "full output: ledger.txt"], lines
    short_text = f"  DRIFTED  row 1\n{total}\n"
    lines = gate.failure_lines(gate.Check(gate.LEDGER, 2, short_text, "ledger.txt"))
    assert lines.count(total) == 1, lines
    suite = gate.failure_lines(gate.Check(gate.SUITE, 1, f"{total}\n", "suite.txt"))
    assert suite.count(total) == 1, (
        "the total was added to a check that is not the ledger"
    )


def test_a_base_that_is_its_own_commit_has_no_ref_row_under_it():
    """A3 on the panel. A bare SHA given as `--base` resolves to itself, so
    the row under `base` would repeat the commit; `ref_is_commit` — the one
    reading the lines use too — leaves it out. A branch-named base keeps
    its row."""
    gate = gate_module()
    sha = "1e2bed90" + "a" * 32
    bare = gate.panel(
        "c46fd2db", gate.Base(sha, "1e2bed90", sha, "1e2bed90"), checks_with(gate), None
    )
    at = bare.index(("base", "1e2bed90"))
    # The next label, and no `""` row: #717 took the blank that used to
    # follow, so the row after `base` is the suite's own.
    assert bare[at + 1] == ("suite", "exit 0"), bare
    named = gate.panel(
        "c46fd2db",
        gate.Base("base", "1e2bed90", "base", "1e2bed90"),
        checks_with(gate),
        None,
    )
    assert named[named.index(("base", "1e2bed90")) + 1] == ("", "base"), named


def test_a_run_with_no_record_has_no_item_and_no_rounds():
    """A7's last shape. Without `--record` there is no work item, so neither
    row prints."""
    gate = gate_module()
    rows = gate.panel(
        "c46fd2db",
        gate.Base("base", "1e2bed90", "base", "1e2bed90"),
        checks_with(gate),
        None,
        branch="feature",
        pr="#12",
    )
    labels = [row[0] for row in rows if row]
    assert "item" not in labels and "rounds" not in labels, labels


def test_the_item_row_is_the_id_alone_without_a_pull_request(tmp_path):
    """A7. `<id>` is the digits before the first `-` of the directory's name,
    and the pull request leads it where the record names one."""
    gate = gate_module()
    item = str(tmp_path / "1790815615-the-seal-names-what-it-sealed")
    assert gate.item_value(item) == "1790815615"
    assert gate.item_value(item, "#666") == "#666 . 1790815615"
    assert gate.item_value(str(tmp_path / "plain")) == "plain"


def test_the_documents_say_where_the_panel_now_carries_each_name():
    """S6 for the panel (`agent-contract` §14). Each sentence that named a
    row the panel lost, or the `gate` row printing on every stamp, says what
    the panel prints now."""
    broad = " ".join(read_document(os.path.join("docs", "the-broad-gate.md")).split())
    assert (
        "the panel's `gate` row reads `tree <version>` wherever the copy that ran "
        "is not byte for byte the copy invoked"
    ) in broad
    assert "panel's `gate` row reads `tree <version>` or `plugin <version>`" not in (
        broad
    )
    verify = " ".join(
        read_document(os.path.join("skills", "verify", "SKILL.md")).split()
    )
    assert "names the ref on the row under the commit" in verify
    sealer = " ".join(sealer_text().split())
    assert "The stamp carries a `gate` row only where the copy that ran is not" in (
        sealer
    )
    assert "a stamp with no `gate` row was measured by the copy you invoked" in sealer
    # Round 1's 🟡 4 and ⬜ 5: the third arm, which fires on every seal an
    # installed copy older than #666 redirects, because it hands over no
    # invoked path to compare against.
    assert "or where nothing told it which copy you invoked" in sealer
    assert (
        "or where the tree's copy ran with no invoked copy named to compare against"
    ) in broad
    item = "1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run"
    changelog = " ".join(
        read_document(os.path.join("seal", "specs", item, "changelog.md")).split()
    )
    assert "or where nothing told it which copy was invoked" in changelog
    source = read_document(os.path.join("skills", "verify", "scripts", "broad_gate.py"))
    above = source.split("GATE_REL = ", 1)[0][-1500:].splitlines()
    comment = " ".join(" ".join(line.lstrip("# ") for line in above).split())
    assert "or where no invoked copy was handed over to compare" in comment
    # Phase 3's row.
    assert (
        "`rounds` row reads `<R> . capped` where the last record's `Needs a fix`"
        in (sealer)
    )
    assert "counts the findings closed `deferred` and names their homes" in sealer


def test_the_sample_carries_every_row_the_panel_can(tmp_path):
    """A16. `seal-stamp` with no arguments shows a person what the gate will
    print, and it read `lint clean` from #400 to #666 because nothing held
    the two lists together. Its labels, in order, are the labels `panel`
    returns for a run with every conditional row present."""
    gate = gate_module()
    workflow = (
        "jobs:\n  release:\n    steps:\n"
        "      - name: a declared review chain has the round record it claimed\n"
    )
    rows = gate.panel(
        "c46fd2db",
        gate.Base("release/x", "1e2bed90", "origin/release/x", "1e2bed90"),
        checks_with(gate, "1 passed in 1s\n", "total: 1 ok · 0 drifted · 0 broken\n"),
        str(tmp_path / "1799000000-an-item"),
        workflow,
        copy="tree 1.2.3",
        branch="feature",
        pr="#12",
        record=record_of(tmp_path, capped_record()),
    )
    labels = [None if row is None else row[0] for row in rows]
    sample = [None if row is None else row[0] for row in module().SAMPLE_ROWS]
    assert sample == labels, (sample, labels)
    # #717's A19, positively: the sequence itself, so the two lists cannot
    # agree by losing the same row.
    assert labels == [
        "SEALED",
        "tree",
        "",
        "base",
        "",
        "item",
        "gate",
        "suite",
        "ledger",
        "CI also",
        "rounds",
        "",
    ], labels


def test_the_docstrings_describe_the_letter_and_the_rows_it_carries():
    """#717, S7 for the code's own prose (`agent-contract` §14). The stamp
    module's docstring describes the letter and the twin's characters rather
    than a rope and golds; the gate's module docstring and `panel`'s row
    diagram list the rows the panel carries now; the comment above
    `SAMPLE_ROWS` says which rows left."""
    stamp = " ".join(
        read_document(
            os.path.join("skills", "verify", "scripts", "seal_stamp.py")
        ).split()
    )
    assert (
        "written on a parchment sheet, with a wax disc pressed over the sheet's "
        "lower right corner"
    ) in stamp
    assert "`m` the wax's edge, `.` the field and `G Y y` the lily's face" in stamp
    assert "`o O` rope" not in stamp and "the lily's golds" not in stamp
    assert "Since #717 there is no blank row in it, no `chain`" in stamp
    gate = " ".join(
        read_document(
            os.path.join("skills", "verify", "scripts", "broad_gate.py")
        ).split()
    )
    assert (
        "the ledger's `ok` count, how many more steps CI runs than this seal answers"
    ) in gate
    assert "the chain's exit, and the round count" not in gate
    assert "CI also <n> more steps absent without a hygiene workflow" in gate
    assert "workflow <n> of <m> not answered" not in gate
    assert "**A drawn panel says only what a `SEALED` stamp can say** (#717)" in gate


def test_the_documents_name_the_ci_also_row():
    """#717, S7 for the rows (`agent-contract` §14). `skills/verify/SKILL.md`
    §*A seal says what it did not answer* and `agents/sealer.md` named the
    `workflow` row and its `<n> of <total> not answered` reading; both name
    the `CI also` row and its `<n> more steps` now, and the denominator is
    said to be on the stderr line."""
    verify = " ".join(
        read_document(os.path.join("skills", "verify", "SKILL.md")).split()
    )
    assert "the panel carries a `CI also` row — *<n> more steps* —" in verify
    assert "A feature seal of SpecSeal itself reads `CI also 4 more steps`" in verify
    assert "the panel carries a `workflow` row" not in verify
    sealer = " ".join(sealer_text().split())
    assert "On any base the `CI also` count leaves out the steps" in sealer
    assert "the `workflow` count" not in sealer


# --- #666: `rounds` says capped and counts the deferred findings -----------


def capped_record(needs="yes — 🟡 1, the wording", verdicts=None, pass_box="x"):
    """A last record in the shape `seal/specs/1790635412-*/rounds/round-3.md`
    has: `Pass` checked, `Fixes checked by | no fixes to check`, `Needs a fix
    | yes — …`, and two findings closed `deferred #664`."""
    if verdicts is None:
        verdicts = (
            "| 🟡 1 | a docstring claim | `f.py:1` | deferred #664 | #664 — why |\n"
            "| ⬜ 2 | its wording | `f.py:2` | **deferred** #664 | #664 — why |\n"
        )
    table = f"## Verdicts\n\n{VERDICT_HEADER}{verdicts}\n" if verdicts else ""
    needs_row = f"| {NEEDS} | {needs} |\n" if needs is not None else ""
    return (
        "# round 3\n\n| Field | Value |\n|---|---|\n| PR | #659 |\n"
        f"| {CHECKED_BY} | no fixes to check |\n{needs_row}\n"
        f"- [{pass_box}] Pass\n\n{table}"
    )


def record_of(tmp_path, text, name="round-3.md"):
    """A `broad_gate.Record` over `text`, read with the plugin's own readers
    the way `sealed_record` reads a record on disk."""
    gate, reader, chain = gate_module(), reader_module(), check_module()
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    lines = reader.readable(text)
    return gate.Record(str(path), chain.table_rows(reader, lines), lines, chain, reader)


def rounds_of(tmp_path, text, rounds=3):
    item = tmp_path / "1799000000-an-item"
    (item / "rounds").mkdir(parents=True, exist_ok=True)
    for n in range(1, rounds + 1):
        (item / "rounds" / f"round-{n}.md").write_text("x\n", encoding="utf-8")
    return gate_module().rounds_rows(str(item), record_of(tmp_path, text))


@pytest.mark.parametrize(
    "text, rows",
    [
        # A10's own shape: capped, two deferrals to one home.
        (capped_record(), [("rounds", "3 . capped"), ("", "2 deferred -> #664")]),
        # Two homes, in table order.
        (
            capped_record(
                verdicts=(
                    "| 🟡 1 | a | `f.py:1` | deferred seal/follow-up.md | why |\n"
                    "| 🟡 2 | b | `f.py:2` | deferred #664 | why |\n"
                    "| 🟡 3 | c | `f.py:3` | deferred #664 | why |\n"
                )
            ),
            # Too long for one row: it continues beneath (round 1's 🟡 1).
            [
                ("rounds", "3 . capped"),
                ("", "3 deferred ->"),
                ("", "seal/follow-up.md, #664"),
            ],
        ),
        # A bare `deferred` is counted and names no home.
        (
            capped_record(
                verdicts=(
                    "| 🟡 1 | a | `f.py:1` | deferred #664 | why |\n"
                    "| 🟡 2 | b | `f.py:2` | deferred | why |\n"
                )
            ),
            [("rounds", "3 . capped"), ("", "2 deferred -> #664")],
        ),
        (
            capped_record(verdicts="| 🟡 1 | a | `f.py:1` | deferred | why |\n"),
            [("rounds", "3 . capped"), ("", "1 deferred")],
        ),
        # A run that ended with nothing needing a fix and nothing deferred.
        (
            capped_record(
                needs="no", verdicts="| 🟢 1 | a | `f.py:1` | answered | why |\n"
            ),
            [("rounds", "3")],
        ),
        # A deferral by choice on a record that needed no fix: counted, not
        # capped (`questions.md` Q2's measurement found ten of these).
        (capped_record(needs="no"), [("rounds", "3"), ("", "2 deferred -> #664")]),
        # Half an answer is no answer: no table, or no `Needs a fix` row.
        (capped_record(verdicts=""), [("rounds", "3")]),
        (capped_record(needs=None), [("rounds", "3")]),
    ],
)
def test_rounds_says_capped_and_counts_what_was_deferred(tmp_path, text, rows):
    """A10. `capped` is read off the last record's `Needs a fix` beginning
    `yes`; the row beneath counts the verdicts `chain_check.verdict_of` calls
    `deferred` and lists their homes, read through `chain_check`'s own
    readers rather than a second parser of a round record."""
    assert rounds_of(tmp_path, text) == rows


def test_a_record_with_no_rows_or_no_record_prints_the_count_alone(tmp_path):
    """A10's last shape: a `broad-gate.md` home has no round record, and a
    record that could not be read gives no rows; both print `<R>` alone."""
    gate = gate_module()
    item = tmp_path / "1799000000-an-item"
    item.mkdir()
    assert gate.rounds_rows(str(item), None) == [("rounds", "0")]
    home = gate.Record(str(item / "broad-gate.md"))
    assert gate.rounds_rows(str(item), home) == [("rounds", "0")]


def test_the_home_is_read_off_the_cell_after_the_word(tmp_path):
    """`verdict_of` hands back the bare word for a homed deferral, so the home
    comes off the cell itself, through the same normalisation: emphasis off,
    the word, then the separators, then the home's first word."""
    gate, chain = gate_module(), check_module()
    for cell, home in (
        ("deferred #664", "#664"),
        ("**deferred** #664", "#664"),
        ("deferred — #664, see the issue", "#664"),
        ("Deferred seal/follow-up.md.", "seal/follow-up.md"),
        ("deferred", None),
        ("fixed abc1234", None),
    ):
        assert gate.deferred_home(chain, cell) == home, cell


@pytest.mark.parametrize(
    "cell, home",
    [
        ("deferred #664", "#664"),
        ("**deferred** #664.", "#664"),
        ("deferred to #664", "#664"),
        ("deferred → #664", "#664"),
        ("deferred (#664)", "#664"),
        ("deferred — issue #97 already holds this axis", "#97"),
        ("deferred `seal/follow-up.md`", "seal/follow-up.md"),
        ("deferred [#664](https://example.com/664)", "#664"),
        ("deferred phase 9 of this branch", "phase 9 of this branch"),
        ("deferred → later", "later"),
        # A path or a `.md` file after other words is still the home.
        ("deferred to seal/follow-up.md", "seal/follow-up.md"),
        ("deferred into the follow-up.md file", "follow-up.md"),
        # Words joined by a slash are words, not a path (round 2's 🟡 1).
        ("deferred — the stdout/stderr split is #700's", "#700"),
        ("deferred to whoever owns CI/CD next", "to whoever owns CI/CD next"),
        ("deferred — read/write order is in seal/follow-up.md", "seal/follow-up.md"),
        ("deferred and/or #701", "#701"),
        # A path written from `./` is still the file, and words in a code
        # span lose the span's marks.
        ("deferred see ./seal/follow-up.md", "seal/follow-up.md"),
        ("deferred `phase 9 of this branch`", "phase 9 of this branch"),
        ("deferred **phase 9 of this branch**", "phase 9 of this branch"),
        # A file name keeps its underscores (round 2's 🟡 2).
        (
            "deferred `tests/test_the_gate_names_every_step_ci_runs.py`",
            "tests/test_the_gate_names_every_step_ci_runs.py",
        ),
        (
            "deferred to `skills/verify/scripts/broad_gate.py`'s owner",
            "skills/verify/scripts/broad_gate.py",
        ),
    ],
)
def test_a_deferrals_home_is_read_whole(cell, home):
    """Round 1's 🟡 2, over the shapes the tree's records and a person
    write: the home is an issue or a path wherever it stands, and the words
    where it is neither, never the first word alone — and what reaches the
    panel is ASCII, because the letter twin is for a console that is not
    UTF-8."""
    gate, chain = gate_module(), check_module()
    assert chain.verdict_of([cell], 0) == chain.DEFERRED, cell
    found = gate.deferred_home(chain, cell)
    assert found == home, (cell, found)
    assert found.isascii(), found


def test_a_capped_run_is_sealed_with_its_deferral_on_the_stamp(repo, tmp_path):
    """A10 end to end, over the fixture `capped_item` builds: round 1 closed
    its one finding `deferred #999` and `Needs a fix` still reads `yes`. The
    gate seals it, and the values file's `rounds` says so."""
    capped_item(repo)
    out = run_gate(
        repo, "--record", str(repo / ITEM), keep=tmp_path / "out", session="s-1"
    )
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    (path,) = values_files(repo)
    rows = module().read_values(path)["rows"]
    assert rows[-2:] == [("rounds", "1 . capped"), ("", "1 deferred -> #999")], rows


# --- S2 not sealed -----------------------------------------------------------


def test_a_failing_test_is_not_sealed_and_is_new_when_the_base_passes(repo):
    """S2. One planted failure: `NOT SEALED <tree> against <base>`, the
    failing check named with its first lines, the failing file labelled
    `new` because the base does not fail it, no disc, exit 1. The scratch
    worktree the comparison used is gone afterwards."""
    write(repo, "tests/test_two.py", FAILING_TEST)
    commit(repo, "plant a failure")
    out = run_gate(repo, session="s-1")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    first = out.stdout.strip().splitlines()[0]
    assert first == head_of(repo, "NOT SEALED"), first
    assert "not committed" not in out.stdout, "a red run said a cell was written"
    assert crown_of() not in out.stdout, "the failure form drew the disc"
    # S7 of 1790562543. A piped run draws no disc even when it seals, so the
    # line above no longer proves the failure form drew nothing; what a hook
    # would draw is a values file, and a red run leaves none.
    assert not values_files(repo), "a red run left a stamp for a hook to draw"
    assert not signal_lines(out.stdout), "a red run printed the `SEALED` signal"
    assert not any(c in out.stdout for c in HALF_BLOCKS)
    assert re.search(r"^\s+suite\s", out.stdout, re.M), "the failing check is unnamed"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.NEW, (
        f"the failing file is not labelled `{gate.NEW}`:\n{out.stdout}"
    )
    assert gate.ON_BASE not in out.stdout
    assert "1 failed, 1 passed" in out.stdout, "the suite's counts are missing"
    worktrees = git(repo, "worktree", "list").stdout.strip().splitlines()
    assert len(worktrees) == 1, f"the scratch worktree was left behind: {worktrees}"


def test_a_failure_the_base_shares_is_labelled_failing_on_base_too(tmp_path):
    """S2, the other word. The base already fails the same file, so the
    comparison — taken reactively, in a scratch worktree at the base — says
    so. The gate decides nothing about it: still `NOT SEALED`, exit 1."""
    repo = build_repo(tmp_path / "repo", base_failing=True)
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, (
        f"the failing file is not labelled `{gate.ON_BASE}`:\n{out.stdout}"
    )
    assert len(git(repo, "worktree", "list").stdout.strip().splitlines()) == 1


def test_the_gate_names_the_row_it_sealed_over(repo, tmp_path):
    """Round 1's 🟡 9. `verify`'s first condition is to name the proving
    command BEFORE running it, and the row is the only part of this run the
    gate did not choose.

    `agents/sealer.md` tells the sealer to quote the row's command and let
    the reader judge it — and the sealer opens no repository file by its own
    rule, so the command has to arrive in the gate's own output. `run` wrote
    it into the kept file and nothing reached the report, which left the one
    thing the Seal Test asks for first as the one thing the sealer could not
    honestly supply."""
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    gate = gate_module()
    printed = out.stdout + out.stderr
    assert f"`{gate.ROW}` says:" in printed, printed
    assert "-m pytest" in printed, (
        "the gate does not name the command it sealed over, so the sealer "
        f"cannot quote it:\n{printed}"
    )


def test_the_suite_row_reads_pytests_counts_and_not_a_linters(tmp_path):
    """Round 1's 🟡 5. `suite_counts` walked the lines backwards and took the
    first `COUNTS_RE` match, and a `Broad gate` row is a test runner joined to
    a linter with `&&` — so the linter's output stands after pytest's summary
    and `2 warnings emitted` matched first.

    The panel's `suite` row is what a reader takes as how many tests ran, so
    a warning count printed there is the seal reporting a number that did not
    come from the run it claims."""
    gate = gate_module()
    assert (
        gate.suite_counts("768 passed, 1 skipped in 30s\nwarning: 2 warnings emitted\n")
        == "768 passed, 1 skipped"
    )
    assert (
        gate.suite_counts("3 failed, 2 passed in 1s\n4 warnings\n")
        == "3 failed, 2 passed"
    )
    assert gate.suite_counts("2 warnings emitted\n") is None, (
        "a run with no pytest summary in it reports a count anyway"
    )
    # Round 2's 🟡 13: the CLASS, not the instance. `warnings` was the word
    # round 1 measured and `errors` is the same defect one linter over —
    # `Found 2 errors.` is what `ruff` and `mypy` print, and a row whose
    # linter runs with `--exit-zero` reaches the panel with it. A
    # skipped-only run is the shape that matched no word at all and came
    # back None, which the panel renders `suite exit 0`: the seal's most
    # trusted row saying nothing about a run in which nothing executed.
    assert gate.suite_counts("1 passed in 1s\nFound 2 errors.\n") == "1 passed"
    assert gate.suite_counts("3 skipped in 0.10s\n") == "3 skipped"
    assert gate.suite_counts("768 passed in 63.21s (0:01:03)\n") == "768 passed"


@pytest.mark.parametrize(
    "path, posix, windows",
    [
        ("tests/test_one.py", "tests/test_one.py", '"tests/test_one.py"'),
        ("tests/a b.py", "'tests/a b.py'", '"tests/a b.py"'),
        ("tests/x&y.py", "'tests/x&y.py'", '"tests/x&y.py"'),
    ],
)
def test_a_path_is_quoted_for_the_shell_of_either_platform(path, posix, windows):
    """Round 2's 🟡 14. The unit read `os.name` inside its body, so the half
    written for Windows could not be driven from the machine the branch was
    written on — and no case asserted the other half either: replacing the
    whole body with `return path` left every case green.

    The disclosure that reached round 2 said the platform was what was
    missing. It was not. CI runs `windows-latest` on every push and
    `compare_at_base` is driven there; what was missing is an assertion, and
    a unit handed the platform can be turned red from either machine.

    `&` is the one that matters. `subprocess.list2cmdline` builds the argv
    quoting `CreateProcess` reads, not `cmd.exe` quoting — it wraps a path
    holding a space and leaves a metacharacter bare — and
    `run(..., shell=True)` on Windows goes through `cmd.exe`, where an
    unquoted `&` ends the command."""
    gate = gate_module()
    assert gate.quote(path, windows=False) == posix
    assert gate.quote(path, windows=True) == windows


def test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict(tmp_path):
    """Round 1's 🟡 4. `compare_at_base` claims its verdicts are measured and
    never inferred, and one absent file turned every one of them into a guess.

    A path that does not exist makes pytest run nothing at all, the files
    beside it included: plain, it prints a not-found reply and exits 4, and
    under xdist it prints only `no tests ran` and exits 5 (#761's
    `phases/phase-1.md`). So one run over every failing file used to lose the
    measurement for ALL of them. This branch is exactly that shape: it adds a
    test module the base does not carry.

    Here the base already fails `tests/test_two.py`, and the branch adds
    `tests/test_three.py` failing too. The base-carried one has to keep
    `failing on base too`, which is what a reader acts on at
    `agents/smith.md`'s three-returns rule. The absent one is not passed with
    it: the base's root tree names it a candidate, and a run of the row at
    the base on it alone collects nothing, which is its `new` (#761)."""
    repo = build_repo(tmp_path / "repo", base_failing=True)
    write(repo, "tests/test_three.py", FAILING_TEST.replace("test_two", "test_three"))
    commit(repo, "a failing file the base does not carry")
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, (
        "one absent file cost the base-carried file its measured verdict:\n"
        f"{out.stdout}"
    )
    assert verdict_of(out.stdout, "tests/test_three.py") == gate.NEW, out.stdout
    assert len(git(repo, "worktree", "list").stdout.strip().splitlines()) == 1


# --- 1791076832: the base re-run finds the part of the row that ran pytest ----
#
# #747. The comparison re-ran the row's first `&&` part, and a lint-first row's
# first part is the linter: no `FAILED` line could appear, and every failing
# file read `new` whatever the base did. The row is now cut where its shell
# cuts it, and each prefix is tried until one prints pytest's summary.


@pytest.mark.parametrize(
    "row, prefixes",
    [
        ("pytest -q", ["pytest -q"]),
        (
            "lint && fmt && pytest -q",
            ["lint", "lint && fmt", "lint && fmt && pytest -q"],
        ),
        ("a || b", ["a", "a || b"]),
        ("a; b", ["a", "a; b"]),
        # A lone `&` backgrounds the part before it, so it ends no prefix
        # (round 1's 🟡 3): a prefix ending there would run that part in the
        # foreground, which the row never does.
        ("a & b", ["a & b"]),
        ("a & b && c", ["a & b", "a & b && c"]),
        ("a |& b", ["a", "a |& b"]),
        ("pytest -q | tee out.txt", ["pytest -q", "pytest -q | tee out.txt"]),
        ("pytest 2>&1 && lint", ["pytest 2>&1", "pytest 2>&1 && lint"]),
        ("pytest >&2 && lint", ["pytest >&2", "pytest >&2 && lint"]),
        ("lint <&0 && pytest", ["lint <&0", "lint <&0 && pytest"]),
        ("echo 'a && b' && pytest", ["echo 'a && b'", "echo 'a && b' && pytest"]),
        ('echo "a; b" && pytest', ['echo "a; b"', 'echo "a; b" && pytest']),
        ("echo a\\&\\&b && pytest", ["echo a\\&\\&b", "echo a\\&\\&b && pytest"]),
        (
            "echo $(true && true) && pytest",
            ["echo $(true && true)", "echo $(true && true) && pytest"],
        ),
        (
            "echo $(echo ')') && pytest",
            ["echo $(echo ')')", "echo $(echo ')') && pytest"],
        ),
        (
            "echo `true && true` && pytest",
            ["echo `true && true`", "echo `true && true` && pytest"],
        ),
        (
            'echo "$(echo "a;b")" && pytest',
            ['echo "$(echo "a;b")"', 'echo "$(echo "a;b")" && pytest'],
        ),
        ('echo "`echo ;`" && pytest', ['echo "`echo ;`"', 'echo "`echo ;`" && pytest']),
        (
            "(cd sub && pytest) && lint",
            ["(cd sub && pytest)", "(cd sub && pytest) && lint"],
        ),
        ("echo 'unclosed && pytest", ["echo 'unclosed && pytest"]),
        # Nothing escapes inside single quotes, and `"` means nothing there.
        ("echo 'a\\' && pytest", ["echo 'a\\'", "echo 'a\\' && pytest"]),
        ("echo '\"' && pytest", ["echo '\"'", "echo '\"' && pytest"]),
        # `'` and `(` mean nothing inside double quotes.
        ('echo "it\'s (" && pytest', ['echo "it\'s ("', 'echo "it\'s (" && pytest']),
        ("; pytest", ["; pytest"]),
        ("lint   &&   pytest  ", ["lint", "lint   &&   pytest"]),
    ],
)
def test_a_row_is_cut_where_sh_cuts_it(row, prefixes):
    """A7, `/bin/sh`. Every top-level operator is a cut, and nothing inside
    a quote, an escape, a `$(…)`, a backtick pair or a group is; an `&`
    straight after `>` or `<` is a redirection. Each prefix is the row's own
    text up to the cut, and the whole row comes last."""
    assert gate_module().row_prefixes(row, cmd_exe=False) == prefixes


@pytest.mark.parametrize(
    "row, prefixes",
    [
        ("bin\\test -q && lint", ["bin\\test -q", "bin\\test -q && lint"]),
        ("lint & pytest", ["lint", "lint & pytest"]),
        ("a || b", ["a", "a || b"]),
        ("pytest | more", ["pytest", "pytest | more"]),
        ("a; b", ["a; b"]),
        ('echo "a && b" && pytest', ['echo "a && b"', 'echo "a && b" && pytest']),
        ("echo a^&^&b && pytest", ["echo a^&^&b", "echo a^&^&b && pytest"]),
        (
            "(cd sub && pytest) && lint",
            ["(cd sub && pytest)", "(cd sub && pytest) && lint"],
        ),
        ("pytest 2>&1 && lint", ["pytest 2>&1", "pytest 2>&1 && lint"]),
        ("echo 'a && b'", ["echo 'a", "echo 'a && b'"]),
        ("echo a\\&& b", ["echo a\\", "echo a\\&& b"]),
        ('echo "unclosed && pytest', ['echo "unclosed && pytest']),
    ],
)
def test_a_row_is_cut_where_cmd_exe_cuts_it(row, prefixes):
    """A7, `cmd.exe`, driven from any machine. `;` separates nothing there,
    `'` and `\\` are ordinary characters, and `^` is the escape."""
    assert gate_module().row_prefixes(row, cmd_exe=True) == prefixes


@pytest.mark.parametrize(
    "windows, comspec, reads",
    [
        (False, r"C:\Windows\System32\cmd.exe", False),
        (True, r"C:\Windows\System32\cmd.exe", True),
        (True, '"C:\\Windows\\System32\\CMD.EXE"', True),
        (True, "", True),
        (True, r"C:\Program Files\Git\bin\bash.exe", False),
    ],
)
def test_the_shell_a_row_is_cut_for_is_the_one_it_is_handed_to(windows, comspec, reads):
    """The grammar `row_prefixes` cuts by and the rewrite `handed_to_shell`
    makes read one answer, `cmd_exe_reads`, driven here from either machine."""
    assert gate_module().cmd_exe_reads(windows=windows, comspec=comspec) is reads


def verdict_of(text, path):
    """The whole word the failure form gives `path` under *compared at the
    base*, or None. Whole, so `new` and `new? …` are told apart: a `new\\b`
    search matches both."""
    found = re.search(rf"^\s+{re.escape(path)}  (.+)$", text, re.M)
    return found and found.group(1).rstrip()


# Two stand-ins that print what a linter and a formatter print and exit 0, so
# a row can be lint-first without a linter installed. `LINT_FAILS_HERE` is a
# file whose presence makes the lint stand-in exit 1.
LINT_FAILS_HERE = "lint.fails"
LINT = f"{sys.executable} -c \"import os, sys; print('All checks passed!'); sys.exit(os.path.exists('{LINT_FAILS_HERE}'))\""
FORMAT = f"{sys.executable} -c \"print('2 files already formatted')\""
LINT_FIRST_ROW = f"{LINT} && {FORMAT} && {SUITE_ROW}"
PASSING_TWO = "def test_two():\n    assert True\n"
# The feature's failing `test_two`, worded apart from the base's so a commit
# replacing one with the other always has something to commit.
FAILING_TWO = FAILING_TEST.replace("planted", "planted on the feature")
UNCOLLECTABLE = "import a_module_nobody_has\n\n\ndef test_three():\n    pass\n"
FAILING_THREE = FAILING_TEST.replace("test_two", "test_three")


def base_then_feature(d, row, at_base, on_feature):
    """A fixture repository under `row` whose `base` branch gains the files
    `at_base`, and whose `feature` branch then takes `on_feature` over them,
    where `None` deletes the file."""
    repo = build_repo(d, row=row)
    git(repo, "switch", "-q", "base")
    for rel, text in at_base.items():
        write(repo, rel, text)
    commit(repo, "the base")
    git(repo, "switch", "-q", "feature")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-edit",
        "base",
    )
    for rel, text in on_feature.items():
        if text is None:
            (repo / rel).unlink()
        else:
            write(repo, rel, text)
    commit(repo, "the feature")
    return repo


def junit(cases, root="testsuites"):
    """A JUnit report in the shape pytest writes for `--junitxml`: a
    `testsuites` root holding one `testsuite`, or a bare `testsuite` where
    `root` says so, with one `testcase` per `(classname, name, outcome)` and
    a `failure` or `error` element where the outcome names one."""
    body = "".join(
        f'<testcase classname="{c}" name="{n}" time="0.001">'
        + (f'<{outcome} message="planted" />' if outcome else "")
        + "</testcase>"
        for c, n, outcome in cases
    )
    suite = (
        f'<testsuite name="pytest" errors="0" failures="0" skipped="0" '
        f'tests="{len(cases)}" time="0.010">{body}</testsuite>'
    )
    if root == "testsuites":
        suite = f'<testsuites name="pytest tests">{suite}</testsuites>'
    return f'<?xml version="1.0" encoding="utf-8"?>{suite}'


# What pytest's report names, and the words it gives (#789). Each is
# `(report, files appended, exit code, stopped, run alone, words)`. The names
# are the ones pytest 9.1.1 wrote in `phases/phase-1.md`'s probe, the same
# under 8.3.5 and 7.4.4: a function, a class's method, a parametrised test
# whose id holds `/`, `.` and `::`, a setup error, a collection error (an empty
# `classname` and the dotted path in `name`), a doctest in a module and in a
# text file, `--import-mode=importlib`, and a rootdir above and below the
# directory pytest runs in. A word in capitals is the module's constant.
REPORTS = [
    pytest.param(
        junit(
            [
                ("tests.test_f", "test_a", "failure"),
                ("tests.test_f", "test_p[a/b]", "failure"),
                ("tests.test_f", "test_p[p::q]", "failure"),
                ("tests.test_s", "test_d", "error"),
                ("tests.test_ok", "test_ok", ""),
            ]
        ),
        ["tests/test_f.py", "tests/test_s.py", "tests/test_ok.py"],
        1,
        False,
        False,
        ["ON_BASE", "ON_BASE", "NEW"],
        id="function-param-setup-error",
    ),
    pytest.param(
        junit(
            [
                ("tests.test_f.TestK", "test_m", "failure"),
                ("tests.test_f", "test_a", ""),
            ]
        ),
        ["tests/test_f.py"],
        1,
        False,
        False,
        ["ON_BASE"],
        id="class-method",
    ),
    pytest.param(
        junit([("", "tests.test_b", "error")]),
        ["tests/test_b.py", "tests/test_f.py"],
        2,
        True,
        False,
        ["ON_BASE", "STOPPED_EARLY"],
        id="collection-error",
    ),
    pytest.param(
        junit([("tests.test_f", "test_a", "failure")]),
        ["tests/test_f.py", "tests/test_ok.py"],
        1,
        True,
        False,
        ["ON_BASE", "STOPPED_EARLY"],
        id="stopped",
    ),
    pytest.param(
        junit([("tests.test_doc", "test_doc.f", "failure")]),
        ["tests/test_doc.py"],
        1,
        False,
        False,
        ["ON_BASE"],
        id="doctest-module",
    ),
    pytest.param(
        junit([("tests.test_doc.txt", "test_doc.txt", "failure")]),
        ["tests/test_doc.txt"],
        1,
        False,
        False,
        ["ON_BASE"],
        id="doctest-text",
    ),
    # Constructed: the text file's name reads as a class `txt` in the module
    # beside it, so its failure could be either file; the module's own
    # failure is placed on the module alone.
    pytest.param(
        junit(
            [
                ("tests.test_doc", "test_doc.f", "failure"),
                ("tests.test_doc.txt", "test_doc.txt", "failure"),
            ]
        ),
        ["tests/test_doc.py", "tests/test_doc.txt"],
        1,
        False,
        False,
        ["ON_BASE", "UNPLACED"],
        id="doctest-text-beside-its-module",
    ),
    # `cd inner` with the ini file one directory up.
    pytest.param(
        junit([("inner.tests.test_two", "test_two", "failure")]),
        ["tests/test_two.py"],
        1,
        False,
        False,
        ["ON_BASE"],
        id="rootdir-above",
    ),
    # From the root, with the ini file in `sub`.
    pytest.param(
        junit([("pkg.tests.test_x", "test_x", "failure")]),
        ["sub/pkg/tests/test_x.py"],
        1,
        False,
        False,
        ["ON_BASE"],
        id="rootdir-below",
    ),
    # No ini file: the rootdir is the arguments' common directory, `tests`,
    # which is this module's own fixture rows.
    pytest.param(
        junit([("test_two", "test_two", "failure"), ("test_one", "test_one", "")]),
        ["tests/test_two.py", "tests/test_one.py"],
        1,
        False,
        False,
        ["ON_BASE", "NEW"],
        id="rootdir-is-tests",
    ),
    # Constructed: a failure two of the appended files could each be.
    pytest.param(
        junit(
            [
                ("sub.tests.test_two", "test_two", "failure"),
                ("tests.test_one", "test_one", ""),
            ]
        ),
        ["tests/test_two.py", "sub/tests/test_two.py", "tests/test_one.py"],
        1,
        False,
        False,
        ["UNPLACED", "UNPLACED", "NEW"],
        id="two-files",
    ),
    # Constructed: one appended file named at two offsets is two files of
    # the run, and the failing one may not be it.
    pytest.param(
        junit(
            [
                ("tests.test_two", "test_two", ""),
                ("other.tests.test_two", "test_two", "failure"),
            ]
        ),
        ["tests/test_two.py"],
        1,
        False,
        False,
        ["UNPLACED"],
        id="two-offsets",
    ),
    # A failure of a file the row collected besides the appended ones.
    pytest.param(
        junit(
            [
                ("tests.test_one", "test_one", "failure"),
                ("tests.test_two", "test_two", ""),
            ]
        ),
        ["tests/test_two.py"],
        1,
        False,
        False,
        ["NEW"],
        id="failure-elsewhere",
    ),
    # Nothing shows the run ran the appended file.
    pytest.param(
        junit([("tests.test_one", "test_one", "")]),
        ["tests/test_two.py"],
        0,
        False,
        False,
        ["UNPLACED"],
        id="not-named",
    ),
    pytest.param(
        junit([]), ["tests/test_two.py"], 4, False, True, ["NEW"], id="alone-4"
    ),
    pytest.param(
        junit([]), ["tests/test_two.py"], 5, False, True, ["NEW"], id="alone-5"
    ),
    pytest.param(
        junit([]),
        ["tests/test_two.py"],
        1,
        False,
        True,
        ["NOTHING_TOGETHER"],
        id="alone-1",
    ),
    pytest.param(
        junit([]),
        ["tests/a.py", "tests/b.py"],
        4,
        False,
        False,
        ["NOTHING_TOGETHER", "NOTHING_TOGETHER"],
        id="several-4",
    ),
    # A run of the others that held one file is not a candidate's run.
    pytest.param(
        junit([]),
        ["tests/a.py"],
        5,
        False,
        False,
        ["NOTHING_TOGETHER"],
        id="others-of-one",
    ),
    pytest.param(
        junit([("tests.test_two", "test_two", "failure")], root="testsuite"),
        ["tests/test_two.py"],
        1,
        False,
        False,
        ["ON_BASE"],
        id="bare-testsuite",
    ),
]


@pytest.mark.parametrize("report, files, code, stopped, alone, words", REPORTS)
def test_the_base_run_is_read_off_pytests_report(
    report, files, code, stopped, alone, words
):
    """S9 (#789). `report_words` places each test pytest's report names on
    the appended files by its dotted name, in either direction between the
    rootdir and the directory pytest runs in; a failing test placed on one
    file alone gives `failing on base too`, anything it cannot place gives
    `new?`, and a report with no test is `new` only for a file run alone
    with exit 4 or 5."""
    gate = gate_module()
    expected = [getattr(gate, w) if w.isupper() else w for w in words]
    got = gate.report_words(report, files, code, stopped, alone=alone)
    assert list(got.values()) == expected


@pytest.mark.parametrize(
    "text",
    [None, "", "no report here", "<html></html>", '<?xml version="1.0"?><testsuites'],
)
def test_what_is_not_a_report_settles_nothing(text):
    """S9 (#789). A prefix settles only where its report was written and
    parses as one; anything else lets the walk go on, and ends in
    `NO_RUNNER` where no prefix wrote one."""
    assert gate_module().report_words(text, ["tests/test_two.py"], 1, False) is None


def test_the_unmeasured_word_says_so_and_every_reader_is_told_it():
    """A9 (#747, contract §14), and S10 (#789). The reasons are text a person
    reads and acts on, so they are pinned whole, and each starts with the
    word that marks it unmeasured. Every document that tells a reader what
    the gate's words mean names `new?` beside the other two, so a sealer
    handing it on and a smith reading it are both told it is not `new`."""
    gate = gate_module()
    assert gate.NO_RUNNER == (
        "new? not measured: no part of the row wrote the report the gate asked "
        "pytest for at the base (each part tried is kept as suite-at-base-<k>.txt, "
        "or as suite-at-base-<k>-<n>.txt for the n-th file run alone, with the "
        "--junitxml path it was handed beside it as .xml)"
    )
    assert gate.STOPPED_EARLY == (
        "new? not measured: the run at the base stopped before every test ran, "
        "and it does not name this file"
    )
    assert gate.UNPLACED == (
        "new? not measured: pytest's report at the base does not place a test on "
        "this file alone (it names none of this file's tests, or a failing test "
        "it names could be this file or another one)"
    )
    assert gate.NOTHING_TOGETHER == (
        "new? not measured: pytest's report at the base counts no test, so a file "
        "the run was handed is missing where the row runs pytest, and a run that "
        "is not of one file alone does not say which"
    )
    assert gate.MULTI_RUNNER == (
        "new? not measured: the row runs pytest in more than one part (part "
        "{first} wrote the report the gate asked for, and part {second} wrote "
        "one under --collect-only, kept as runners-at-base-{second}.txt), so "
        "the gate cannot tell which runner a failing file belongs to"
    )
    readers = {
        ("agents", "sealer.md"): "`new?`",
        ("agents", "smith.md"): "`new?` is neither",
        ("skills", "verify", "SKILL.md"): "**New?**",
        ("README.md",): "new? → not measured at the base",
        ("README.ko.md",): "new? → base 에서 재지 못했다",
        ("templates", "config.md"): "each file reads `new?` with the reason",
    }
    for parts, phrase in readers.items():
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
            assert phrase in handle.read(), f"{'/'.join(parts)} does not name `new?`"
    # #789: the reason a reader acts on names the report the gate asked
    # pytest for, which replaced the summary line it used to read.
    with open(
        os.path.join(ROOT, "skills", "verify", "SKILL.md"), encoding="utf-8"
    ) as handle:
        bullet = handle.read()
    assert "wrote the report the gate asked pytest for" in bullet
    assert "the row runs pytest in more than one part" in bullet
    with open(GATE, encoding="utf-8") as handle:
        docstring = ast.get_docstring(ast.parse(handle.read()))
    assert "`new?` with the reason no run measured it" in docstring


def test_a_part_that_is_not_pytest_is_passed_over_though_it_prints_counts(tmp_path):
    """Round 1's 🟡 1, end to end. The first part prints what `cargo test`
    prints for a filter that matched nothing, a count and a clock that the
    text reader once took for pytest's summary. It writes no report, so the
    comparison goes on to the part that does, and the base's failure is
    found."""
    cargo = (
        "test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; "
        "1 filtered out; finished in 0.00s"
    )
    repo = base_then_feature(
        tmp_path / "repo",
        f"{sys.executable} -c \"print('{cargo}')\" && {SUITE_ROW}",
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE, (
        out.stdout
    )


def test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new(tmp_path):
    """Round 1's 🟡 2. The row runs pytest from `sub`, so the failing file is
    named `tests/test_two.py` and neither tree carries that path at the root.
    It used to read `new` with no run at the base, which fails it. A path the
    base's root does not carry says nothing about the directory pytest runs
    in, so it is run there alone, and that run fails it (#761)."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {SUITE_ROW}",
        {"sub/tests/test_two.py": FAILING_TEST},
        {"sub/tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE, (
        out.stdout
    )


def test_a_runner_first_row_runs_once_at_the_base(tmp_path):
    """A3 (#747). Where the runner is the row's first part, the first prefix
    writes pytest's report and is the only one run with the files: the parts
    after it cost the base comparison one collection run each, which counts
    the row's runners (#789, `runners-at-base-<j>.txt`)."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{SUITE_ROW} && {LINT}",
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE
    kept = sorted(p.name for p in (tmp_path / "out").glob("suite-at-base-*.txt"))
    assert kept == ["suite-at-base-1.txt"], kept
    counted = sorted(p.name for p in (tmp_path / "out").glob("runners-at-base-*"))
    assert counted == ["runners-at-base-2.txt"], counted


def test_a_row_is_cut_at_the_semicolon_its_shell_reads(tmp_path):
    """The comparison cuts by the grammar of the shell it hands the row to:
    under `/bin/sh` a `;` ends a part, so the format stand-in is tried alone
    first and pytest is reached by the second prefix."""
    posix_row_shell_or_skip()
    repo = base_then_feature(
        tmp_path / "repo",
        f"{FORMAT}; {SUITE_ROW}",
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE
    kept = sorted(p.name for p in (tmp_path / "out").glob("suite-at-base-*.txt"))
    assert kept == ["suite-at-base-1.txt", "suite-at-base-2.txt"], kept


def test_a_lint_first_row_finds_a_failure_the_base_shares(tmp_path):
    """A1 (#747). The row runs a linter and a formatter before pytest, and
    the base fails the same file. The comparison used to re-run the first
    `&&` part — the linter — so no `FAILED` line could appear and the file
    read `new`. The prefix that reaches pytest is found by running it."""
    repo = base_then_feature(
        tmp_path / "repo",
        LINT_FIRST_ROW,
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, out.stdout
    # The three prefixes, the last one the run that printed pytest's summary.
    kept = sorted(p.name for p in (tmp_path / "out").glob("suite-at-base-*.txt"))
    assert kept == [f"suite-at-base-{k}.txt" for k in (1, 2, 3)], kept
    assert len(git(repo, "worktree", "list").stdout.strip().splitlines()) == 1


def test_a_lint_first_row_finds_a_failure_the_branch_introduced(tmp_path):
    """A2 (#747). As A1, and the base passes the file: it reads exactly
    `new`, measured, and not `new?`."""
    repo = base_then_feature(
        tmp_path / "repo",
        LINT_FIRST_ROW,
        {"tests/test_two.py": PASSING_TWO},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().NEW, out.stdout


def test_a_row_that_runs_no_pytest_gives_no_measured_word(tmp_path):
    """A4 (#747). The row prints a line in pytest's `FAILED` shape and exits
    1, and prints no summary. No part of it runs pytest, so nothing at the
    base is a measurement: the file reads `new?` with the reason, never
    `new` or `failing on base too`."""
    script = (
        f"{sys.executable} -c \"print('FAILED tests/test_two.py::test_two - x'); "
        'raise SystemExit(1)"'
    )
    repo = base_then_feature(
        tmp_path / "repo",
        script,
        {"tests/test_two.py": PASSING_TWO},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.NO_RUNNER, out.stdout


def test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing(tmp_path):
    """A5 (#747). The lint stand-in fails at the base only, so `&&` stops
    every prefix before pytest runs there, and the file reads `new?`."""
    repo = base_then_feature(
        tmp_path / "repo",
        LINT_FIRST_ROW,
        {"tests/test_two.py": PASSING_TWO, LINT_FAILS_HERE: ""},
        {"tests/test_two.py": FAILING_TWO, LINT_FAILS_HERE: None},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.NO_RUNNER, out.stdout


def test_a_base_run_stopped_by_a_collection_error_names_only_what_it_ran(tmp_path):
    """A6 (#747), with `questions.md` Q1. The base cannot collect
    `test_three`, which pytest reports as an `ERROR` line and an interrupted
    run, so `test_three` reads `failing on base too`. `test_two` fails at the
    base as well, but the interrupted run never reached it: it reads `new?`,
    because a file the run did not name was not shown passing."""
    repo = base_then_feature(
        tmp_path / "repo",
        True,
        {"tests/test_two.py": FAILING_TEST, "tests/test_three.py": UNCOLLECTABLE},
        {"tests/test_two.py": FAILING_TWO, "tests/test_three.py": FAILING_THREE},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_three.py") == gate.ON_BASE, out.stdout
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.STOPPED_EARLY, out.stdout


def test_a_base_run_stopped_at_its_first_failure_names_only_what_it_ran(tmp_path):
    """The maxfail half of A6 (#747). The row stops at the first failure,
    and at the base that is `test_one`, which the branch passes. The base
    run never reached `test_two`, so it reads `new?` and not `new`."""
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW.replace(" tests", " -x tests"),
        {
            "tests/test_one.py": FAILING_TEST.replace("test_two", "test_one"),
            "tests/test_two.py": FAILING_TEST,
        },
        {"tests/test_one.py": PASSING_TEST, "tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.STOPPED_EARLY, out.stdout


# --- 1791119069: a cd row's failing path is measured under its own directory --
#
# #761. The base comparison decided a failing file absent from the root's
# tree, and pytest names a file from the directory it was invoked in. So a
# `cd sub` row's `tests/test_two.py` read `new`, unrun, wherever the branch
# carried a different file at that path under the root. The root's tree now
# only nominates a candidate; a run of the row at the base on that file alone
# decides it. "Under xdist" is the row with `-n 2`, where a missing path
# prints no not-found reply (`phases/phase-1.md`).

XDIST = importlib.util.find_spec("xdist") is not None
NO_XDIST = (
    "the fixture's interpreter carries no pytest-xdist, so a row under `-n 2` "
    "cannot run here"
)
UNDER = [
    pytest.param(False, id="plain"),
    pytest.param(
        True, id="xdist", marks=pytest.mark.skipif(not XDIST, reason=NO_XDIST)
    ),
]


def suite_row(xdist):
    """`SUITE_ROW`, or the same row with `-n 2` before its directory."""
    return SUITE_ROW.removesuffix(" tests") + " -n 2 tests" if xdist else SUITE_ROW


def kept_at_base(keep):
    return sorted(p.name for p in keep.glob("suite-at-base-*.txt"))


@pytest.mark.parametrize("xdist", UNDER)
def test_a_cd_rows_file_the_root_carries_differently_is_run_at_the_base(
    tmp_path, xdist
):
    """S1 and S1x (#761). The base fails `sub/tests/test_two.py`; the branch
    still fails it and adds a different, passing `tests/test_two.py` under the
    root. The row runs pytest from `sub`, so the failing file is named
    `tests/test_two.py`, the branch's root carries that path, and the base's
    root does not. That used to read `new` with no run at the base. It is a
    candidate now, and its run alone at the base, from `sub`, fails it."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {suite_row(xdist)}",
        {"sub/tests/test_two.py": FAILING_TEST},
        {"sub/tests/test_two.py": FAILING_TWO, "tests/test_two.py": PASSING_TWO},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE, (
        out.stdout
    )
    # The candidate's run at each prefix: `cd sub` with the file appended,
    # which settles nothing, then the row, which prints pytest's summary.
    assert kept_at_base(tmp_path / "out") == [
        "suite-at-base-1-1.txt",
        "suite-at-base-2-1.txt",
    ]


@pytest.mark.parametrize("xdist", UNDER)
def test_a_cd_rows_shared_and_new_files_each_get_a_measured_word(tmp_path, xdist):
    """S2 (#761). Under one `cd`, the base fails `sub/tests/test_two.py` and
    the branch adds a failing `sub/tests/test_three.py`. Neither root carries
    either path, so both used to run together at the base, the missing one
    stopped the run, and both read `new?`. Each is now run alone: the shared
    one fails there, and the new one collects nothing there, which is `new`
    measured — plain pytest and xdist alike."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {suite_row(xdist)}",
        {"sub/tests/test_two.py": FAILING_TEST},
        {
            "sub/tests/test_two.py": FAILING_TWO,
            "sub/tests/test_three.py": FAILING_THREE,
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, out.stdout
    assert verdict_of(out.stdout, "tests/test_three.py") == gate.NEW, out.stdout


@pytest.mark.parametrize("xdist", UNDER)
def test_a_root_run_row_measures_the_module_the_branch_added(tmp_path, xdist):
    """S3 (#761), under xdist the shape of this repository's own
    `bin/test -q`. The base fails `tests/test_two.py` and the branch adds a
    failing `tests/test_three.py`. Run together, the missing one would stop
    both (`phases/phase-1.md`). The shared one is run with the others, the new
    one alone, and the new one's `new` now comes from that run.

    The words are listed in the order the branch's `FAILED` lines named the
    files, whichever run measured each. Asserted plain only: under xdist
    the order of those lines is the order the workers finished in."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{suite_row(xdist)} && {LINT}",
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO, "tests/test_three.py": FAILING_THREE},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, out.stdout
    assert verdict_of(out.stdout, "tests/test_three.py") == gate.NEW, out.stdout
    assert kept_at_base(tmp_path / "out") == [
        "suite-at-base-1-1.txt",
        "suite-at-base-1.txt",
    ]
    if not xdist:
        listed = re.findall(r"^\s+(tests/test_\w+\.py)  ", out.stdout, re.M)
        assert listed == ["tests/test_three.py", "tests/test_two.py"], out.stdout


def test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd(
    tmp_path,
):
    """The limit rule 3 names (#761). The row runs pytest from `sub`, the
    base carries `tests/test_two.py` at the root and nothing at
    `sub/tests/test_two.py`, and the branch adds a failing one there. The
    root's tree finds the path, so the file is not run alone; it runs with
    the others, that run collects nothing, and it reads `new?`. A run that
    is not of one candidate alone and collects nothing never gives `new`: it
    does not say which of its files the base lacks. Since #789 its report,
    which counts no test, settles the walk at the runner and the word is
    `NOTHING_TOGETHER`, where the walk used to go on and end in
    `NO_RUNNER`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {SUITE_ROW}",
        {"tests/test_two.py": PASSING_TWO, "sub/tests/test_one.py": PASSING_TEST},
        {"sub/tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.NOTHING_TOGETHER, (
        out.stdout
    )


def test_a_candidate_whose_run_at_the_base_crashes_is_not_measured(tmp_path):
    """S4 (#761). As S1, and the base's `sub/tests/test_two.py` ends the
    process at import. The candidate's run prints neither pytest's summary
    nor its nothing-collected line, so nothing measured it: `new?`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {SUITE_ROW}",
        {"sub/tests/test_two.py": "import os\n\nos._exit(3)\n"},
        {"sub/tests/test_two.py": FAILING_TWO, "tests/test_two.py": PASSING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.NO_RUNNER, out.stdout


@pytest.mark.parametrize("xdist", UNDER)
def test_a_run_of_several_that_counted_only_warnings_is_not_measured(tmp_path, xdist):
    """#761 round 1's 🟡 1. As the limit case, and the base's
    `sub/tests/test_one.py` fails while an ini key pytest does not know gives
    every run a warning. The run of the two files collects nothing, and its
    last line is `1 warning in <t>s` (`3 warnings` under xdist) rather than
    `no tests ran`. That line is not a measurement: `tests/test_one.py`,
    which the base fails, reads `new?`, never `new`. Since #789 the report
    is read instead of the line, and it counts no test whatever the
    warnings, so both read `NOTHING_TOGETHER`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {suite_row(xdist)}",
        {
            "tests/test_two.py": PASSING_TWO,
            "sub/tests/test_one.py": FAILING_TEST.replace("test_two", "test_one"),
            "sub/pytest.ini": "[pytest]\nan_unknown_key = 1\n",
        },
        {
            "sub/tests/test_one.py": FAILING_TWO.replace("test_two", "test_one"),
            "sub/tests/test_two.py": FAILING_TWO,
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    for path in ("tests/test_one.py", "tests/test_two.py"):
        assert verdict_of(out.stdout, path) == gate.NOTHING_TOGETHER, out.stdout


# A base test that fails after printing what an inner pytest run printed: a
# suite that tests a pytest plugin, or runs pytest in a subprocess, does this.
PRINTS_AN_EMPTY_RUN = (
    "import subprocess\nimport sys\n\n\n"
    "def test_two(tmp_path):\n"
    "    inner = subprocess.run(\n"
    "        [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', str(tmp_path)],\n"
    "        capture_output=True, text=True,\n"
    "    )\n"
    "    print(inner.stdout)\n"
    "    assert False, 'planted'\n"
)
PRINTS_A_FAILED_LINE = (
    "def test_one():\n"
    "    print('FAILED tests/test_two.py::test_two - an inner run')\n"
    "    assert False, 'planted'\n"
)
INNER_OUTPUT = [
    # The base fails `tests/test_two.py` after printing an inner run's
    # `no tests ran`: measured, `failing on base too`.
    pytest.param(
        {"tests/test_two.py": PRINTS_AN_EMPTY_RUN},
        {"tests/test_two.py": FAILING_TWO},
        "ON_BASE",
        id="an-inner-empty-run",
    ),
    # The base passes `tests/test_two.py`, and its failing `test_one` prints
    # a `FAILED` line naming it: measured, `new`.
    pytest.param(
        {"tests/test_one.py": PRINTS_A_FAILED_LINE, "tests/test_two.py": PASSING_TWO},
        {"tests/test_one.py": PASSING_TEST, "tests/test_two.py": FAILING_TWO},
        "NEW",
        id="an-inner-failed-line",
    ),
]


@pytest.mark.parametrize("xdist", UNDER)
@pytest.mark.parametrize("at_base, on_feature, word", INNER_OUTPUT)
def test_what_a_test_printed_is_not_read_as_pytests_own_lines(
    tmp_path, at_base, on_feature, word, xdist
):
    """#761 round 2's 🟡 1, and its class. A failing test's captured output
    is printed above pytest's own lines, and a test that ran pytest itself
    carries that run's lines there. Read anywhere, an inner `no tests ran`
    turned a run that measured the file into `new?` with a false reason, and
    an inner `FAILED` line named a file the base passes `failing on base
    too`. Since #789 the words come from the JUnit report the gate asks
    pytest for, which no inner run writes, and both cases keep their word."""
    repo = base_then_feature(tmp_path / "repo", suite_row(xdist), at_base, on_feature)
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    expected = getattr(gate_module(), word)
    assert verdict_of(out.stdout, "tests/test_two.py") == expected, out.stdout


# --- 1791163982: an output holding two pytest runs earns no permissive word ---
#
# #789. The words used to be read off the text pytest printed, and that text
# can hold a second run's lines: an inner run a test writes to a stream pytest
# does not capture (`-s`, `--capture=sys`), or one pytest prints in captured
# output where it writes no rule of its own (`-rN`, `-rP`) or no summary
# (`-qq`). Each run at the base now appends `--junitxml=<path>`, and the words
# come from the report only the run the gate asked about writes.

PASSING_G = "def test_g():\n    assert True\n"
FAILING_G = "def test_g():\n    assert False, 'planted on the feature'\n"
FAILING_ERR = "def test_err():\n    assert False, 'planted on the feature'\n"


def inner_run(fd, fails):
    """A base `tests/test_err.py` whose test runs pytest in a subprocess over
    a scratch `tests/test_g.py` that fails there, and writes that run's
    output straight to file descriptor `fd`, past `sys`-level capture. The
    inner run's `FAILED tests/test_g.py::test_g` line names a path the outer
    run passes. The test fails where `fails` is true."""
    return (
        "import os\nimport subprocess\nimport sys\n\n\n"
        "def test_err(tmp_path):\n"
        "    (tmp_path / 'tests').mkdir()\n"
        "    (tmp_path / 'tests' / 'test_g.py').write_text(\n"
        "        'def test_g():\\n    assert False\\n'\n"
        "    )\n"
        "    inner = subprocess.run(\n"
        "        [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests'],\n"
        "        cwd=tmp_path, capture_output=True, text=True,\n"
        "    )\n"
        f"    os.write({fd}, inner.stdout.encode())\n"
        f"    assert {not fails}, 'planted'\n"
    )


# The base fails `tests/test_err.py`, whose inner run fails `tests/test_g.py`,
# and passes `tests/test_g.py`; the branch fails both.
FAILING_BASE_INNER_ON_STDERR = {
    "tests/test_err.py": inner_run(2, fails=True),
    "tests/test_g.py": PASSING_G,
}
# The base passes everything, and its `tests/test_err.py` writes an inner run
# that fails `tests/test_g.py` to stdout.
PASSING_BASE_INNER_ON_STDOUT = {
    "tests/test_err.py": inner_run(1, fails=False),
    "tests/test_g.py": PASSING_G,
}
BOTH_FAIL = {"tests/test_err.py": FAILING_ERR, "tests/test_g.py": FAILING_G}
# The same, where the branch's own run writes no `FAILED` line (`-rN`, `-rP`):
# its failing test prints the two lines the branch's list of files is read
# from, in its captured output (`spec.md` Axis C).
BOTH_FAIL_NAMED = {
    "tests/test_err.py": (
        "def test_err():\n"
        "    print('FAILED tests/test_err.py::test_err - planted')\n"
        "    print('FAILED tests/test_g.py::test_g - planted')\n"
        "    assert False, 'planted on the feature'\n"
    ),
    "tests/test_g.py": FAILING_G,
}


def words_of(out):
    return {
        f: verdict_of(out.stdout, f) for f in ("tests/test_err.py", "tests/test_g.py")
    }


@pytest.mark.parametrize("xdist", UNDER)
def test_an_inner_run_on_stderr_under_s_is_not_read_as_the_runs_own(tmp_path, xdist):
    """S1 (#789 member 2; #761 round 3's regression test). Under `-s` a test
    writes to the real stderr, and `run` joins stdout and then stderr, so the
    inner run's `short test summary info` rule stood after pytest's own and
    its `FAILED` line was read as the run's: `tests/test_g.py`, which the
    base passes, read `failing on base too`, and `tests/test_err.py`, which
    it fails, read `new`. pytest's report names only the outer run's tests."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{suite_row(xdist)} -s",
        FAILING_BASE_INNER_ON_STDERR,
        BOTH_FAIL,
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert words_of(out) == {
        "tests/test_err.py": gate.ON_BASE,
        "tests/test_g.py": gate.NEW,
    }, out.stdout


@pytest.mark.parametrize("capture", ["-s", "--capture=sys"])
def test_an_inner_run_on_stdout_beside_a_passing_base_gives_no_word(tmp_path, capture):
    """S2 (#789, the shape the issue did not name). The base passes
    everything, so pytest writes no rule of its own, and an inner run a
    passing test writes to stdout carries the only rule in the output: its
    `FAILED` line gave `failing on base too` to a file the base passes.
    Keeping stdout and stderr apart would not have closed it."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{SUITE_ROW} {capture}",
        PASSING_BASE_INNER_ON_STDOUT,
        BOTH_FAIL,
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert words_of(out) == {
        "tests/test_err.py": gate.NEW,
        "tests/test_g.py": gate.NEW,
    }, out.stdout


@pytest.mark.parametrize(
    "flag, at_base, words",
    [
        pytest.param("-rN", FAILING_BASE_INNER_ON_STDERR, ("ON_BASE", "NEW"), id="rN"),
        pytest.param("-rP", FAILING_BASE_INNER_ON_STDERR, ("ON_BASE", "NEW"), id="rP"),
        pytest.param(
            "-rP", PASSING_BASE_INNER_ON_STDOUT, ("NEW", "NEW"), id="rP-passing-base"
        ),
    ],
)
def test_a_run_with_no_rule_of_its_own_is_read_off_its_report(
    tmp_path, flag, at_base, words
):
    """S3 (#789 member 3). Under `-rN`, and under `-rP` with no failure to
    list, pytest writes no `short test summary info` rule, so the last rule in
    the output was the one an inner run printed in a test's captured output,
    and its `FAILED` line was read as the run's own. The branch's run writes
    no `FAILED` line of its own either, so its failing test prints the two
    the list of files is read from."""
    repo = base_then_feature(
        tmp_path / "repo", f"{SUITE_ROW} {flag}", at_base, BOTH_FAIL_NAMED
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    expected = dict(
        zip(
            ("tests/test_err.py", "tests/test_g.py"),
            (getattr(gate, w) for w in words),
            strict=True,
        )
    )
    assert words_of(out) == expected, out.stdout


@pytest.mark.parametrize(
    "at_base, on_feature, expected",
    [
        pytest.param(
            {"tests/test_two.py": PASSING_TWO},
            {"tests/test_two.py": FAILING_TWO},
            {"tests/test_two.py": "NEW"},
            id="no-summary",
        ),
        # The rule here is pytest's own, so a3aa139a read it right too; kept
        # as the guard on the inner summary `-qq` leaves as the last one.
        pytest.param(
            FAILING_BASE_INNER_ON_STDERR,
            BOTH_FAIL,
            {"tests/test_err.py": "ON_BASE", "tests/test_g.py": "NEW"},
            id="inner-summary",
        ),
    ],
)
def test_a_run_with_no_summary_line_is_read_off_its_report(
    tmp_path, at_base, on_feature, expected
):
    """S4 (#789 member 3). Under `-qq` pytest prints no summary line, so no
    prefix printed one and a file the base passes read `new?`; where an inner
    run printed one in captured output, that line was the only summary."""
    repo = base_then_feature(tmp_path / "repo", f"{SUITE_ROW} -q", at_base, on_feature)
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    for path, word in expected.items():
        assert verdict_of(out.stdout, path) == getattr(gate, word), out.stdout


DROPS_ITS_ARGUMENTS = [
    # The shell hands what is appended to `sh -c` as `$0` and `$1`, which the
    # script never reads: it runs its own `tests` and prints a summary.
    pytest.param(
        f"sh -c '{sys.executable} -m pytest -q -p no:cacheprovider tests'",
        True,
        id="sh-c",
    ),
    # pytest without its JUnit writer refuses the option the gate appends.
    pytest.param(f"{SUITE_ROW} -p no:junitxml", False, id="no-junitxml"),
]


@pytest.mark.parametrize("row, posix_only", DROPS_ITS_ARGUMENTS)
def test_a_part_that_drops_the_gates_arguments_gives_no_word(tmp_path, row, posix_only):
    """S6 (#789 Scope 2), replacing the case that named this the one
    counterfeit the gate could not see (round 1's 🟡 5 of #747). A part that
    prints pytest's summary without running the files appended to it used to
    read `new` for a file it never ran. It writes no report where the gate
    asked for one, so the file reads `new?`, whatever the base does."""
    if posix_only:
        posix_row_shell_or_skip()
    repo = base_then_feature(
        tmp_path / "repo",
        row,
        {"tests/test_two.py": PASSING_TWO},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.NO_RUNNER, out.stdout


def test_a_report_an_earlier_run_left_settles_nothing(tmp_path):
    """#789. `--keep-output` can name a directory an earlier gate run wrote
    into, and a report left there at a prefix's path would settle a prefix
    that wrote nothing. Here the earlier report fails `tests/test_two.py` at
    the lint stand-in's prefix; the base passes it, so it reads `new`."""
    repo = base_then_feature(
        tmp_path / "repo",
        LINT_FIRST_ROW,
        {"tests/test_two.py": PASSING_TWO},
        {"tests/test_two.py": FAILING_TWO},
    )
    keep = tmp_path / "out"
    keep.mkdir()
    (keep / "suite-at-base-1.xml").write_text(
        junit([("tests.test_two", "test_two", "failure")]), encoding="utf-8"
    )
    out = run_gate(repo, keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().NEW, out.stdout


def test_a_relative_kept_directory_still_receives_the_report_under_a_cd(tmp_path):
    """#789. The gate hands pytest the report's path, and a `cd` part moves
    the directory pytest resolves a relative path from, so the path is made
    absolute first. Here `--keep-output` is relative and the row runs from
    `sub`, where the base fails the file."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {SUITE_ROW}",
        {"sub/tests/test_two.py": FAILING_TEST},
        {"sub/tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo, keep="out", cwd=tmp_path)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE, (
        out.stdout
    )
    assert (tmp_path / "out" / "suite-at-base-2-1.xml").is_file()


def two_runner_row(xdist):
    return f"{suite_row(xdist)} && cd sub && {suite_row(xdist)}"


# Round 1's p1 and p1b and round 2's p1c of #761, in one repository. The root
# runner passes on the branch, so `&&` reaches the runner in `sub`, which
# names its three failing files `tests/test_x.py`, `tests/test_y.py` and
# `tests/test_z.py`.
TWO_RUNNERS_AT_BASE = {
    # p1: the base fails it in `sub`, and the root has no such file.
    "sub/tests/test_x.py": FAILING_TEST.replace("test_two", "test_x"),
    # p1b: the base fails a root file of the same name, and has none in `sub`.
    "tests/test_y.py": FAILING_TEST.replace("test_two", "test_y"),
    # p1c: the base fails it in `sub`, and passes a root file of the same name.
    "sub/tests/test_z.py": FAILING_TEST.replace("test_two", "test_z"),
    "tests/test_z.py": PASSING_TEST.replace("test_one", "test_z"),
    "sub/tests/test_one.py": PASSING_TEST,
}
TWO_RUNNERS_ON_FEATURE = {
    "sub/tests/test_x.py": FAILING_TWO.replace("test_two", "test_x"),
    "tests/test_y.py": PASSING_TEST.replace("test_one", "test_y"),
    "sub/tests/test_y.py": FAILING_TWO.replace("test_two", "test_y"),
    "sub/tests/test_z.py": FAILING_TWO.replace("test_two", "test_z"),
}


@pytest.mark.parametrize("xdist", UNDER)
def test_a_row_with_two_runners_gives_every_failing_file_no_word(tmp_path, xdist):
    """S7 (#789 member 1, #761 round 1's 🟡 2 and round 2's ⬜ 2). Each file
    was asked of the first runner a prefix reaches, in the root: p1 read
    `new` for a file the base fails in `sub`, p1b `failing on base too` for a
    file the base never ran, and p1c `new` where only the root's same-named
    file passes. The later prefixes are run once under `--collect-only`, the
    third writes its report, and every failing file reads `new?` naming the
    two parts."""
    repo = base_then_feature(
        tmp_path / "repo",
        two_runner_row(xdist),
        TWO_RUNNERS_AT_BASE,
        TWO_RUNNERS_ON_FEATURE,
    )
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    expected = gate.MULTI_RUNNER.format(first=1, second=3)
    for path in ("tests/test_x.py", "tests/test_y.py", "tests/test_z.py"):
        assert verdict_of(out.stdout, path) == expected, out.stdout
    kept = sorted(p.name for p in keep.glob("runners-at-base-*"))
    assert kept == [
        "runners-at-base-2.txt",
        "runners-at-base-3.txt",
        "runners-at-base-3.xml",
    ], kept


def test_a_part_after_the_runner_that_is_not_pytest_keeps_the_words(tmp_path):
    """S8 (#789). The runner comes first and a part that is not pytest
    follows it. The collection pass runs the whole row once under
    `--collect-only`, the last part writes no report, and the words the
    runner measured stand."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{SUITE_ROW} && {sys.executable} -c pass",
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO, "tests/test_three.py": FAILING_THREE},
    )
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, out.stdout
    assert verdict_of(out.stdout, "tests/test_three.py") == gate.NEW, out.stdout
    kept = sorted(p.name for p in keep.glob("runners-at-base-*"))
    assert kept == ["runners-at-base-2.txt"], kept


def test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written():
    """S7 (#761, contract §14). The candidate's run costs a run per such
    file, and it has two limits a row's author can meet. Rule 3 is the one
    home of what the comparison costs a row and which rows it cannot
    measure, so each is pinned there."""
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as handle:
        text = handle.read()
    for sentence in (
        "A failing file the base's tree does not carry at the repository root "
        "is run alone at the base, through the same prefixes, which costs one "
        "more run of each prefix up to and including the runner per such file.",
        "A file that run collects nothing from (a report that counts no test, "
        "with exit 4 or 5) reads `new`, so a base file "
        "with no test in it reads `new` too: the base cannot fail a test it does "
        "not have.",
        "Where a row runs its tests below a directory and the base carries a "
        "same-named file at the root but not below that directory, the file is "
        "not run alone: it runs with the others, that run collects nothing, "
        "and each file in it reads `new?`.",
        # #789: what the gate asks pytest for, and what that closes. These
        # replace #761 round 3's `-s` sentence and round 1's 🟡 5 of #747.
        "and runs each prefix with the files appended, and after them "
        "`--junitxml=<path>`, a path beside the run's kept output, until one "
        "writes that report (#789).",
        "The words are read off pytest's report and never off what was printed, "
        "so nothing a test prints decides them: not an inner pytest run a test "
        "writes to stdout or stderr under `-s`, not one in captured output where "
        "pytest writes no rule of its own (`-rN`, `-rP`), and not one under `-qq`.",
        "A file the report places a failing or erroring test on, and no other "
        "file, reads `failing on base too`, and a file whose tests the report "
        "names with none failing reads `new`.",
        "A part that does not hand the appended arguments on to pytest — a "
        "`sh -c '…'`, a `make` target, a wrapper that drops its arguments or "
        "refuses an option it does not know, a runner given `-p no:junitxml` — "
        "writes no report where the gate asked for one, so each file reads "
        "`new?` where it used to read `new` for a file it never ran. Write such "
        "a part so it passes its arguments on, `--junitxml` included",
        # #789, replacing #761 round 1's 🟡 2 two-runner sentence: the
        # behaviour, its cost, and what collection alone does not reach.
        "A row that runs pytest in more than one part — `pytest -q && cd sub "
        "&& pytest -q` — reads `new?` for every failing file, because the gate "
        "cannot tell which runner a file belongs to",
        "To count the runners, each prefix after the one whose report settled "
        "the walk runs once more at the base with ` --collect-only` added to "
        "`PYTEST_ADDOPTS` and only its own `--junitxml` appended, kept as "
        "`runners-at-base-<j>.txt`: one collection run per prefix after the "
        "runner, once per comparison and only on a failing gate, so a row whose "
        "runner is its last part never pays it.",
        "A runner that does not read `PYTEST_ADDOPTS` runs its tests there "
        "instead of collecting them.",
        "Collection alone does not reach a runner behind a part that exits "
        "non-zero at the base under it — a lint that fails there, an earlier "
        "runner with a collection error or one that collects nothing — nor one "
        "behind `||`; such a row is read as one with a single runner, and a file "
        "a later runner named can read `new` or `failing on base too` from the "
        "first runner's directory.",
        "runner first costs one run at the base and a collection run of each "
        "prefix after it (below)",
        # #761 round 2's ⬜ 3: the clause round 1's survivor-check corrected.
        "each file reads `new?` with the reason, and never `new` unless it "
        "ran alone and that run collected nothing (below).",
    ):
        assert sentence in text, f"rule 3 does not carry: {sentence}"
    # #761 round 1's ⬜ 8: the reader sent to the base by hand is told to open
    # every kept run, the ones a file ran alone in included.
    with open(
        os.path.join(ROOT, "skills", "verify", "SKILL.md"), encoding="utf-8"
    ) as handle:
        assert "open the kept `suite-at-base-*.txt` files" in handle.read()


def test_a_plugin_check_that_fails_is_named_and_the_suite_is_not_compared(repo):
    """The comparison is reactive: it exists for a failing TEST. A failing
    plugin check — here an overview whose `## Not verified` row was deleted,
    which `unverified-check --baseline` refuses — is named with its exit and
    its first lines, and no worktree is added for it."""
    write(repo, f"{ITEM}/overview.md", "# overview\n\n## Not verified\n\n")
    commit(repo, "delete the row")
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert re.search(r"^\s+unverified\s+exit [12]", out.stdout, re.M), out.stdout
    gate = gate_module()
    assert gate.NEW not in out.stdout and gate.ON_BASE not in out.stdout
    assert len(git(repo, "worktree", "list").stdout.strip().splitlines()) == 1


# --- 1790815611: the record arms run before the sealer is spawned (#638) -------
#
# `broad-gate --preflight` is the orchestrator's step before the sealer's
# spawn: the same command, the same resolved base, the same row refusals, and
# then the record arms alone. It runs no row, writes no cell, values file or
# stamp, and prints no line a reader could take for a seal.

PREFLIGHT_PASSED = "PREFLIGHT PASSED   {tree} against {base}"
PREFLIGHT_FAILED = "PREFLIGHT FAILED   {tree} against {base}"
NOT_RUN = "the `Broad gate` row was not run and nothing is sealed"


def record_arms():
    """Every arm `gate()` records except the repository's row, in source
    order — read off the function, never typed here.

    `plan.md`'s failure scenario is an arm landing under the condition that
    skips the row: the partition cases stay green, because the assignment is
    still inside `gate()`, and the preflight runs one arm fewer than the
    sealer. A list typed in this file would agree with the preflight and miss
    it; this one is read from the same source the gate runs, so that arm is a
    kept output file the preflight did not write."""
    gate = gate_module()
    with open(GATE, encoding="utf-8") as handle:
        parsed = ast.parse(handle.read())
    function = next(
        n
        for n in ast.walk(parsed)
        if isinstance(n, ast.FunctionDef) and n.name == "gate"
    )
    found = []
    for node in ast.walk(function):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if ast.unparse(node.value.func) != "run":
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Subscript)
                and ast.unparse(target.value) == "checks"
            ):
                found.append((node.lineno, getattr(gate, ast.unparse(target.slice))))
    return [name for _, name in sorted(found) if name != gate.SUITE]


def no_seal_line(text):
    """True when no line of `text` is one a reader could take for a seal."""
    return not any(
        line.startswith(("SEALED", "NOT SEALED")) for line in text.splitlines()
    )


def test_a_green_tree_preflights_green_and_seals_nothing(repo, tmp_path):
    """S1. Every record arm runs, in the gate's order, with its output kept the
    way the full run keeps it; the row does not run, so there is no
    `suite.txt`. Nothing is sealed: no `SEALED` line, no values file even with
    a session set, no disc in either form and no colour. The one line on
    stdout names the preflight, the tree and the resolved base."""
    keep = tmp_path / "out"
    out = run_gate(repo, "--preflight", keep=keep, session="s-1")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert no_seal_line(out.stdout), out.stdout
    head = PREFLIGHT_PASSED.format(tree=short(repo, "HEAD"), base=short(repo, "base"))
    assert out.stdout.startswith(head), out.stdout
    assert NOT_RUN in out.stdout, out.stdout
    assert "read, and not run: this is a preflight" in out.stderr, out.stderr
    assert not values_files(repo), "a preflight left a stamp to draw"
    assert crown_of() not in out.stdout, "a preflight drew the twin"
    assert not SGR.search(out.stdout), "a preflight carries colour codes"
    assert not any(c in out.stdout for c in HALF_BLOCKS), "a preflight drew blocks"
    arms = record_arms()
    assert len(arms) >= 6, f"the gate's record arms were not read: {arms}"
    # `.txt` alone: the chain arm's draft payload (`draft_env`) is kept here
    # too, and it is an input rather than an arm's output.
    kept = sorted(n for n in os.listdir(keep) if n.endswith(".txt"))
    assert kept == sorted(f"{name}.txt" for name in arms), (
        f"the preflight kept {kept}; the gate's record arms are {arms}"
    )
    for name in arms:
        text = (keep / f"{name}.txt").read_text(encoding="utf-8")
        assert text.startswith("$ "), f"{name}.txt does not open with its command"
        assert "\nexit 0\n" in text, f"{name}.txt does not carry its exit code"
    times = [os.stat(keep / f"{n}.txt").st_mtime_ns for n in arms]
    assert times == sorted(times), f"the arms did not run in the gate's order: {times}"


def test_the_preflight_prints_no_coverage_line(repo, tmp_path):
    """Spec §*Data & interfaces*, step 2. The coverage line says what THIS
    SEAL answers of the workflow's `release` job, and a preflight seals
    nothing, so it prints none — over a fixture carrying this repository's own
    workflow, where the full run over the same tree prints it."""
    workflow = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")
    with open(workflow, encoding="utf-8") as handle:
        write(repo, ".github/workflows/hygiene.yml", handle.read())
    commit(repo, "the workflow")
    said = "this seal answers"
    full = run_gate(repo, keep=tmp_path / "full")
    assert said in full.stderr, f"the full run printed no coverage line:\n{full.stderr}"
    out = run_gate(repo, "--preflight", keep=tmp_path / "pre")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert said not in out.stderr, (
        f"a preflight claimed a seal's coverage:\n{out.stderr}"
    )


def test_the_preflight_does_not_run_the_row(repo, tmp_path):
    """S2, the case that shows the flag does something. The row is `exit 1`,
    so the full gate over this tree is NOT SEALED; the preflight over the same
    tree passes, because it never hands the row to a shell."""
    set_row(repo, "exit 1")
    full = run_gate(repo, keep=tmp_path / "full")
    assert full.returncode == 1, f"{full.stdout}\n{full.stderr}"
    assert "NOT SEALED" in full.stdout, full.stdout
    keep = tmp_path / "pre"
    out = run_gate(repo, "--preflight", keep=keep)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert not (keep / "suite.txt").exists(), "the preflight ran the row"


def test_a_failing_record_arm_is_named_and_the_row_is_still_not_run(repo, tmp_path):
    """S3. The overview's `## Not verified` row deleted, which
    `unverified-check --baseline` refuses, and the row `exit 1`. The preflight
    exits 1 and names `unverified` in the failure form's own words — the exit,
    the first lines, the file holding the rest — under a first line naming the
    preflight rather than a seal. The row did not run and no worktree was
    added for a comparison that exists only for a failing test."""
    write(repo, f"{ITEM}/overview.md", "# overview\n\n## Not verified\n\n")
    commit(repo, "delete the row")
    set_row(repo, "exit 1")
    keep = tmp_path / "out"
    out = run_gate(repo, "--preflight", keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    head = PREFLIGHT_FAILED.format(tree=short(repo, "HEAD"), base=short(repo, "base"))
    assert out.stdout.startswith(head), out.stdout
    assert NOT_RUN in out.stdout.splitlines()[0], out.stdout
    assert no_seal_line(out.stdout), out.stdout
    assert re.search(r"^\s+unverified\s+exit [12]", out.stdout, re.M), out.stdout
    assert "full output:" in out.stdout and "unverified.txt" in out.stdout, out.stdout
    assert not (keep / "suite.txt").exists(), "the preflight ran the row"
    assert len(git(repo, "worktree", "list").stdout.strip().splitlines()) == 1


def test_a_preflight_with_record_is_refused_and_writes_no_cell(repo, tmp_path):
    """S4. A preflight that took `--record` would write the cell, which it
    exists not to do, or ignore the flag, which is a flag that does nothing.
    So the pair is a refusal: exit 2, nothing run, the record byte-identical,
    and a sentence naming both flags and saying the preflight writes no
    cell."""
    _one, two = settled_item(repo)
    before = read_bytes(two)
    keep = tmp_path / "out"
    out = run_gate(repo, "--preflight", "--record", str(repo / ITEM), keep=keep)
    assert out.returncode == 2, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert not out.stdout, f"something printed under a refusal: {out.stdout!r}"
    assert "--preflight" in out.stderr and "--record" in out.stderr, out.stderr
    assert "a preflight writes no cell" in out.stderr, out.stderr
    assert not keep.exists() or not os.listdir(keep), (
        f"a check ran under a refusal: {os.listdir(keep)}"
    )
    assert read_bytes(two) == before, "the record changed under a refusal"


def a_verifying_round_that_says_fixed_at(repo):
    """#535's item C, as a fixture. Round 1 opened a finding and its fix
    landed; round 2 is the verifying round, and its reviewer wrote the verdict
    `fixed at <sha>` — what round 1's fix did, which `chain_check` reads as
    this round closing on a fix of its own — beside `Fixes checked by: no
    fixes to check`, the cell #535's record carried.

    `chain_check.py#closed_with_a_fix` refuses that pair, and the refusal is
    not excused on a draft (`questions.md` Q1). The cell is written by hand
    because today's generator no longer writes it beside a fix word — `new`
    lands `nobody — the fixes are not yet written` and `close` corrects that
    to `nobody — the fixes are written…` (`phases/phase-2.md` of 1790815611
    measured both) — and a hand-repaired cell is the way that pair still
    reaches a tree. Returns round 2's record."""
    declared(repo)
    generate(repo, 1, OPEN_ROW, "yes — 🔴 1")
    a = git(repo, "rev-parse", "HEAD").stdout.strip()
    write(repo, "f.py", "x = 2\n")
    b = commit(repo, "fix")
    close_round(repo, 1, f"| 1 | fixed | {b[:7]} |\n", f"{a}..{b}")
    two = generate(
        repo,
        2,
        f"| 🟢 1 | round 1's fix holds | `f.py:1` | fixed at {b[:7]} | read |\n",
        "no",
    )
    lines = two.read_text(encoding="utf-8").splitlines(keepends=True)
    at = [i for i, line in enumerate(lines) if line.startswith(f"| {CHECKED_BY} |")]
    assert len(at) == 1, f"round 2 carries {len(at)} `{CHECKED_BY}` rows"
    lines[at[0]] = f"| {CHECKED_BY} | no fixes to check |\n"
    two.write_text("".join(lines), encoding="utf-8")
    commit(repo, "the cell #535's record carried")
    return two


# A file the row writes into the repository root where it runs, so a row
# that ran leaves evidence the gate did not write.
ROW_RAN = "row-ran"


def test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight(repo, tmp_path):
    """S7, the ticket's verification (#638 §*How to verify*). A verifying
    round's table carries `fixed at` beside `Fixes checked by: no fixes to
    check`. The preflight exits 1 with `chain` named in the failure form, and
    the row — a command that would leave a file behind and fail — was never
    invoked. Seen red first: without the flag argparse refuses the command,
    and with the flag ignored the row runs."""
    two = a_verifying_round_that_says_fixed_at(repo)
    record = two.read_text(encoding="utf-8")
    assert "fixed at" in record, record
    assert re.search(rf"\| {CHECKED_BY} \| no fixes to check \|", record), record
    set_row(repo, f"{sys.executable} -c \"open('{ROW_RAN}', 'w')\" && exit 1")
    keep = tmp_path / "out"
    out = run_gate(repo, "--preflight", keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert out.stdout.startswith("PREFLIGHT FAILED"), out.stdout
    assert re.search(r"^\s+chain\s+exit 1", out.stdout, re.M), out.stdout
    assert no_seal_line(out.stdout), out.stdout
    assert not (repo / ROW_RAN).exists(), "the preflight invoked the row"
    assert not (keep / "suite.txt").exists(), "the preflight ran the row"
    chain = (keep / "chain.txt").read_text(encoding="utf-8")
    assert "no fixes to check" in chain and "closed on a fix" in chain, chain


def test_without_the_row_the_preflight_names_it_and_runs_nothing(tmp_path):
    """S6. The preflight asks the row's questions before anything runs, the
    same as the full run, because a refusal about the row is the cheapest one
    the sealer gives and it costs a spawn when it arrives there."""
    repo = build_repo(tmp_path / "repo", row=False)
    keep = tmp_path / "out"
    out = run_gate(repo, "--preflight", keep=keep)
    assert out.returncode == 2, f"exit {out.returncode}; {out.stdout!r} {out.stderr!r}"
    assert f"has no `{ROW}` row" in out.stderr, out.stderr
    assert not out.stdout, f"something printed under a refusal: {out.stdout!r}"
    assert not keep.exists() or not os.listdir(keep), (
        f"a check ran under a refusal: {os.listdir(keep)}"
    )


def test_a_preflight_over_a_wrapped_row_is_refused_and_runs_nothing(repo, tmp_path):
    """S6's second half: a row the gate would not run as the command it reads
    as is refused by the preflight too, though the preflight would not have
    run it either. The refusal is about what the sealer will meet."""
    keep = tmp_path / "out"
    out = run_gate(set_row(repo, f"`{SUITE_ROW}`"), "--preflight", keep=keep)
    assert out.returncode == 2, f"exit {out.returncode}; {out.stdout!r} {out.stderr!r}"
    assert "backticks" in out.stderr, out.stderr
    assert not out.stdout, f"something printed under a refusal: {out.stdout!r}"
    assert not keep.exists() or not os.listdir(keep), (
        f"a check ran under a refusal: {os.listdir(keep)}"
    )


# --- S4 one write: the fixture item --------------------------------------------


def declaration(review="through the review chain"):
    return (
        f"# {os.path.basename(ITEM)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {review} |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def report(verdicts, needs):
    return (
        "# what the round found\n\nProse.\n\n"
        f"## Verdicts\n\n{VERDICT_HEADER}{verdicts}\n"
        "## Executed probes\n\n| What was run | Result |\n|---|---|\n"
        "| `pytest tests/test_one.py -q` | 1 passed |\n\n"
        "## Deferred\n\n| Finding | Where it went | Who answers it |\n|---|---|---|\n\n"
        f"Needs a fix: {needs}\nLoses a record or crashes: no\n"
    )


def generate(repo, n, verdicts, needs, target=None):
    """`round_record.py new` for round `n`, then the record committed."""
    scratch = repo.parent
    (scratch / f"report-{n}.md").write_text(report(verdicts, needs), encoding="utf-8")
    (scratch / f"asked-{n}.md").write_text("Attack the gate.\n", encoding="utf-8")
    target = target or git(repo, "rev-parse", "HEAD").stdout.strip()
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "new",
            "--item",
            str(repo / ITEM),
            "--round",
            str(n),
            "--target",
            target,
            "--report",
            str(scratch / f"report-{n}.md"),
            "--asked",
            str(scratch / f"asked-{n}.md"),
            "--ran-by",
            "specseal:warden on a model",
            "--baseline",
            "base",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    path = repo / ROUNDS / f"round-{n}.md"
    assert path.exists(), r.stdout + r.stderr
    commit(repo, f"round {n}")
    return path


def declared(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    return commit(repo, "declare")


def close_round(repo, n, rows, rng):
    """`round_record.py close` with a fix table of `rows`, then committed."""
    generator = _load("specseal_round_record_for_sealed_records", GENERATOR)
    table = (
        f"{generator.FIXES}\n\n{generator.row(generator.FIXES_HEADER)}\n"
        f"{generator.separator(len(generator.FIXES_HEADER))}\n{rows}"
    )
    path = repo.parent / f"fixes-{n}.md"
    path.write_text(table, encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "close",
            "--item",
            str(repo / ITEM),
            "--round",
            str(n),
            "--fixes",
            str(path),
            "--range",
            rng,
            "--baseline",
            "base",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    commit(repo, f"close round {n}")


def settled_item(repo):
    """The state the broad gate runs in: round 1 opened a finding, a fix
    landed and `close` applied its table, round 2 verified the fix and
    closed everything with `Needs a fix: no`. Every verdict in both records
    is closed, so `close` would refuse a fix table for either — which is the
    state the `seal` subcommand exists for. Returns (round-1, round-2)."""
    declared(repo)
    one = generate(repo, 1, OPEN_ROW, "yes — 🔴 1")
    a = git(repo, "rev-parse", "HEAD").stdout.strip()
    write(repo, "f.py", "x = 2\n")
    b = commit(repo, "fix")
    close_round(repo, 1, f"| 1 | fixed | {b[:7]} |\n", f"{a}..{b}")
    two = generate(
        repo,
        2,
        "| 🟢 1 | round 1's fix holds | `f.py:1` | answered | read |\n",
        "no",
    )
    return one, two


def fixed_but_unread_item(repo):
    """Round 1 closed on a FIX and no round 2 has run — the window between a
    fix pass and the verifying round that reads it.

    `close` ticks `Pass` from the verdict table alone, so the box is checked;
    it writes `Fixes checked by` only when the answer is `no fixes to check`,
    so a record whose findings closed on fixes keeps the landing value
    `nobody — the fixes are not yet written` for the NEXT round's `new` to
    set. Returns the record."""
    declared(repo)
    one = generate(repo, 1, OPEN_ROW, "yes — 🔴 1")
    a = git(repo, "rev-parse", "HEAD").stdout.strip()
    write(repo, "f.py", "x = 2\n")
    b = commit(repo, "fix")
    close_round(repo, 1, f"| 1 | fixed | {b[:7]} |\n", f"{a}..{b}")
    return one


def capped_item(repo):
    """The state a CAPPED run ends in, and the one the seal could not reach.

    `docs/review-chain-spec.md` bounds a run at three rounds. A run that
    reaches the cap with a finding still live closes it `deferred <home>`
    rather than fixed — which is a closing word, so `Pass` comes out checked
    — while `Needs a fix` keeps the `yes` the reviewer wrote while the round
    was running, because nothing rewrites the reviewer's own row. Returns
    the record."""
    declared(repo)
    one = generate(repo, 1, OPEN_ROW, "yes — 🔴 1")
    a = git(repo, "rev-parse", "HEAD").stdout.strip()
    write(repo, "f.py", "x = 2\n")
    b = commit(repo, "carry the finding to an issue")
    close_round(repo, 1, "| 1 | deferred #999 | #999 |\n", f"{a}..{b}")
    return one


def run_seal(repo, value, extra=()):
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "seal",
            "--item",
            str(repo / ITEM),
            "--broad-gate",
            value,
            "--baseline",
            "base",
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    return r.returncode, r.stdout + r.stderr


def fields(text):
    reader, chain = reader_module(), check_module()
    rows = chain.table_rows(reader, reader.readable(text))
    return {cells[0].strip(): cells[1].strip() for cells in rows if len(cells) == 2}


def read_bytes(path):
    return path.read_bytes()


# --- S4 the one write ----------------------------------------------------------


def test_seal_writes_the_last_records_cell_and_nothing_else(repo):
    """S4. Two records; `seal` changes the last one's `Broad gate` cell and
    touches no other line of it — byte for byte — and the earlier record not
    at all. Every verdict of the last record is already closed, which is the
    state `close` refuses a fix table for: the write `close` cannot make is
    the one this subcommand exists for."""
    one, two = settled_item(repo)
    before_one, before_two = read_bytes(one), read_bytes(two)
    assert fields(two.read_text(encoding="utf-8"))[ROW] == "not yet"
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    assert "sealed" in out and "round-2.md" in out, out
    assert read_bytes(one) == before_one, "the earlier record was touched"
    after = read_bytes(two)
    assert after != before_two, "the last record did not change"
    old, new = (
        before_two.decode("utf-8").splitlines(),
        after.decode("utf-8").splitlines(),
    )
    assert len(old) == len(new), "a line was added or removed"
    changed = [(a, b) for a, b in zip(old, new, strict=True) if a != b]
    assert len(changed) == 1, f"{len(changed)} lines changed: {changed}"
    assert changed[0][0].startswith(f"| {ROW} |"), changed
    assert fields(after.decode("utf-8"))[ROW] == f"{head} against base"
    assert "- [x] Pass" in after.decode("utf-8")


GATE_FILE = "broad-gate.md"


def test_seal_writes_a_file_where_no_round_record_exists(repo):
    """S18. A work item declaring `straight to the PR` runs no rounds, so the
    cell has no record to live on — and `seal` used to REFUSE outright.

    That refusal is one half of a seal with no home. `last_record` raised
    rather than returning, and `chain_check`'s direct arm returned before it
    looked; neither repairs the other, which is why both are phase 5's. The
    `straight to the PR` answer turns off the REVIEWER and nothing else, so
    the broad run is owed here exactly as it is on the chain path.
    """
    write(repo, f"{ITEM}/routing.md", declaration(review="straight to the PR"))
    commit(repo, "declare direct")
    assert not (repo / ROUNDS).exists(), "the fixture is not the no-rounds state"
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    path = repo / ITEM / GATE_FILE
    assert path.exists(), f"`seal` wrote no {GATE_FILE}: {out}"
    assert GATE_FILE in out, "the line printed does not name the home it chose"
    text = path.read_text(encoding="utf-8")
    assert fields(text)[ROW] == f"{head} against base", text
    # The cell and nothing else. A file that grows a second row is a file the
    # one reader has to start choosing between rows in.
    table = [ln for ln in text.splitlines() if ln.startswith("|")]
    assert len(table) == 3, (
        f"{GATE_FILE} holds {len(table)} table lines, not a header, a "
        f"separator and the cell:\n{text}"
    )


def test_seal_refuses_a_chain_declaration_with_no_round_record(repo):
    """The home is the DECLARATION's, not whatever is on disk.

    `rounds/` empty is two different states. One is a work item that runs no
    rounds, and its cell belongs in `broad-gate.md`. The other is a work item
    whose rounds are running and whose first record is not written yet, and
    its cell belongs on that record — filed in the other home it is a seal the
    chain arm never opens, over which `seal` printed `sealed`.

    Round 1 executed exactly this in a throwaway clone and got exit 0 with the
    cell written to the unread home. It fails closed — `chain_check` still
    refuses the pull request on the record's `not yet` — so what was lost is
    the sealer's answer rather than the enforcement.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare the chain, rounds not written yet")
    assert not (repo / ROUNDS).exists(), "the fixture is not the no-rounds state"
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert GATE_FILE in out and "round-N.md" in out, (
        "the refusal names neither the home it declined nor the record it wants"
    )
    assert not (repo / ITEM / GATE_FILE).exists(), (
        "the cell went into the home the chain arm never reads"
    )


def test_a_direct_declaration_seals_into_its_own_home_even_with_rounds(repo):
    """The SAME defect running the other way, which the same fix closes.

    A `straight to the PR` work item that does have round records was sealed
    onto the last one — and `chain_check`'s direct arm reads `broad-gate.md`
    and nothing else, so that cell is unread too. Round 1 named this direction
    without a case; a fix aimed only at the direction that was reproduced
    would have left half the class standing, which is §12.
    """
    _one, two = settled_item(repo)
    write(repo, f"{ITEM}/routing.md", declaration(review="straight to the PR"))
    commit(repo, "the declaration says direct after all")
    before = read_bytes(two)
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    path = repo / ITEM / GATE_FILE
    assert path.exists(), f"the direct home was not written: {out}"
    assert fields(path.read_text(encoding="utf-8"))[ROW] == f"{head} against base"
    assert read_bytes(two) == before, (
        "the cell went onto the last round record, which the direct arm "
        "never reads — the same misfiling, in the other direction"
    )


def test_a_work_item_with_rounds_still_seals_onto_its_last_record(repo):
    """The other direction, and the one a new home quietly breaks.

    Adding a second home is a change to where the writer LOOKS, and a writer
    that starts preferring the new home seals every work item into a file no
    chain-path reader opens — silently, because both writes succeed. So the
    property is asserted from both ends: the record's cell is filled, and no
    `broad-gate.md` exists at all.
    """
    _one, two = settled_item(repo)
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    assert fields(two.read_text(encoding="utf-8"))[ROW] == f"{head} against base"
    assert not (repo / ITEM / GATE_FILE).exists(), (
        "a work item that ran rounds got the no-rounds home as well, so the "
        "cell now exists in two places and the readers disagree"
    )


def test_a_re_seal_keeps_the_earlier_run_and_the_reader_takes_the_newest(repo):
    """A12 of #174. A run that meets a pre-existing failure, or whose last
    fixes land after the gate, takes the broad run again — and the cell held
    one entry that `seal` REPLACED, so the second run erased the record of
    the first and the run-level table was filled from memory. The cell now
    holds one entry per run, newest first: `seal` writes the new entry in
    front and keeps what was there. `chain_check.broad_gate` reads the first
    SHA-shaped word as the run, so newest-first is what keeps its reading
    unchanged, and that half is asserted through the reader itself."""
    _one, two = settled_item(repo)
    first = short(repo, "HEAD")
    code, out = run_seal(repo, f"{first} against base")
    assert code == 0, out
    write(repo, "f.py", "x = 3\n")
    commit(repo, "a fix after the gate, which spends it")
    second = short(repo, "HEAD")
    code, out = run_seal(repo, f"{second} against base")
    assert code == 0, out
    after = two.read_text(encoding="utf-8")
    generator = _load("specseal_round_record_for_a_re_seal", GENERATOR)
    assert fields(after)[ROW] == (
        f"{second} against base{generator.EARLIER_RUN}{first} against base"
    ), after
    # The reader: at a ready pull request, the newest entry is the run, and
    # the cell has nothing to be refused for.
    check, reader = check_module(), reader_module()
    check.WORKTREE = True
    errors, notices = check.broad_gate(reader, str(repo), f"{ROUNDS}/round-2.md", True)
    assert errors == [] and notices == [], (errors, notices)


def test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry(repo):
    """Round 1's ⬜ 8, decided: a run taken again at the commit the newest
    entry already names is the same claim about the same tree, so the new
    entry replaces that one rather than standing beside it — the cell holds
    one entry per run at a distinct commit, and a sealer re-run over an
    unchanged tree does not grow it. An earlier run at a different commit
    stays behind the newest as before."""
    _one, two = settled_item(repo)
    first = short(repo, "HEAD")
    assert run_seal(repo, f"{first} against base")[0] == 0
    write(repo, "f.py", "x = 3\n")
    commit(repo, "a fix after the gate")
    second = short(repo, "HEAD")
    assert run_seal(repo, f"{second} against base")[0] == 0
    code, out = run_seal(repo, f"{second} against base")
    assert code == 0, out
    generator = _load("specseal_round_record_for_a_same_commit_re_seal", GENERATOR)
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == (
        f"{second} against base{generator.EARLIER_RUN}{first} against base"
    ), cell
    assert cell.count(second) == 1, "the same commit was entered twice"


def test_a_re_seal_at_the_same_commit_against_another_base_keeps_both(repo):
    """Round 2's 🟡 1. The seal is the commit AND the base (`agents/sealer.md`
    §Bind the result to a tree state), so a run at one commit against a
    moved base is a second comparison and stays beside the first rather
    than replacing it — the erasure #174 was filed on, one field narrower.
    Keyed on the SHA alone, the replace erased the first base, which the
    four sentences promising *a second run never erases the first* forbid."""
    _one, two = settled_item(repo)
    sha = short(repo, "HEAD")
    assert run_seal(repo, f"{sha} against base")[0] == 0
    code, out = run_seal(repo, f"{sha} against origin/base")
    assert code == 0, out
    generator = _load("specseal_round_record_for_another_base", GENERATOR)
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == (
        f"{sha} against origin/base{generator.EARLIER_RUN}{sha} against base"
    ), cell


def test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list(repo):
    """A13 of #174: with nothing to keep there is no separator, so every
    committed record and every fixture in the tree is already the shape."""
    _one, two = settled_item(repo)
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == f"{head} against base", cell
    generator = _load("specseal_round_record_for_a_first_seal", GENERATOR)
    assert generator.EARLIER_RUN.strip(" ;:") not in cell, cell


def test_the_written_broad_gate_file_says_a_same_run_re_seal_replaces_its_entry(
    repo,
):
    """#542. The comment `seal` writes into every `broad-gate.md` described
    the cell's rule as it stood before `same_run`: *a run taken again is
    written in front, and the earlier one stays behind it*. No test read the
    written file for that sentence, so a third rewording of the rule would
    reach every `broad-gate.md` unpinned. The file a person opens says what
    the writer does: a run the newest entry already records — the same
    commit against the same base — replaces it."""
    write(repo, f"{ITEM}/routing.md", declaration(review="straight to the PR"))
    commit(repo, "declare direct")
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    text = " ".join((repo / ITEM / GATE_FILE).read_text(encoding="utf-8").split())
    assert (
        "a run the newest entry already records — the same commit against the "
        "same base — replaces it"
    ) in text, f"the written comment does not state the same-run replace:\n{text}"
    assert "a run taken again is written in front" not in text, (
        f"the written comment still states the rule `same_run` replaced:\n{text}"
    )


def test_the_direct_home_takes_the_same_shape_on_a_re_seal(repo):
    """A14 of #174. `broad-gate.md` is the whole record of a `straight to the
    PR` work item and `direct_seal` reads it through `broad_gate`, so one
    writer gives both homes one shape: the re-sealed file holds both entries
    and the direct arm passes on the newest."""
    write(repo, f"{ITEM}/routing.md", declaration(review="straight to the PR"))
    commit(repo, "declare direct")
    first = short(repo, "HEAD")
    code, out = run_seal(repo, f"{first} against base")
    assert code == 0, out
    write(repo, "f.py", "x = 3\n")
    commit(repo, "a fix after the gate")
    second = short(repo, "HEAD")
    code, out = run_seal(repo, f"{second} against base")
    assert code == 0, out
    path = repo / ITEM / GATE_FILE
    text = path.read_text(encoding="utf-8")
    generator = _load("specseal_round_record_for_a_direct_re_seal", GENERATOR)
    assert fields(text)[ROW] == (
        f"{second} against base{generator.EARLIER_RUN}{first} against base"
    ), text
    table = [ln for ln in text.splitlines() if ln.startswith("|")]
    assert len(table) == 3, "the cell is still one row, and the file still one cell"
    check, reader = check_module(), reader_module()
    check.WORKTREE = True
    routing = generator.load(check.ROUTING, "specseal_routing_for_a_re_seal")
    errors, notices = check.direct_seal(
        reader, routing, str(repo), str(repo / ITEM), f"{ITEM}/{GATE_FILE}", True
    )
    assert errors == [] and notices == [], (errors, notices)


def test_seal_writes_over_a_capped_runs_needs_a_fix(repo):
    """S5. A capped run seals, and until phase 5 it could not.

    `Needs a fix: yes` used to refuse before anything else was read. Phase 4
    of #30 measured what that cost on a fixture built exactly like this one:
    `close` applied a fix table closing the finding `deferred #999`, `Pass`
    came out checked because `deferred <home>` is a closing word, `Needs a
    fix` stayed `yes` because it is the reviewer's row and nothing rewrites
    it, `seal` refused — and `chain_check` then failed the ready pull
    request on a `Broad gate` cell nothing could write. Two rules of this
    repository contradicted each other over the case the cap exists for.

    So the cell is written, `Needs a fix` is left exactly as the reviewer
    wrote it, and the run of `chain_check` that `seal` ends with passes —
    which is the whole chain the measurement found broken, end to end. The
    other two refusals are untouched and are asserted below.
    """
    path = capped_item(repo)
    text = path.read_text(encoding="utf-8")
    assert "- [x] Pass" in text, "the fixture is not the capped state"
    assert fields(text)[NEEDS].startswith("yes"), text
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    after = path.read_text(encoding="utf-8")
    assert fields(after)[ROW] == f"{head} against base", after
    assert fields(after)[NEEDS].startswith("yes"), (
        "the reviewer's own row was rewritten to make the seal reachable"
    )


def test_seal_refuses_while_pass_is_unchecked(repo):
    """S4. An open finding leaves `Pass` unchecked even where the reviewer
    wrote `no`; the seal is refused naming the box, and no byte is written.

    Since phase 5 this is the ONLY refusal that answers *has the run
    ended*, so the message says what it does not read: a reader who has
    just watched a `Needs a fix: yes` seal needs the two rows told apart at
    the one moment the difference bites."""
    declared(repo)
    path = generate(repo, 1, OPEN_ROW, "no")
    assert "- [ ] Pass" in path.read_text(encoding="utf-8")
    before = read_bytes(path)
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert "`Pass` is unchecked" in out and "no cell was written" in out, out
    assert f"`{NEEDS}` is not read here" in out, out
    assert read_bytes(path) == before


def test_seal_refuses_while_the_fixes_have_been_read_by_nobody(repo):
    """Round 1's 🔴 2. The third refusal, and the third answer to one question.

    `Pass` says the verdict TABLE is closed. It does not say the run ended:
    `close` ticks the box the moment a fix table applies, and the verifying
    round that reads those fixes has not run yet. Sealing there spends the run
    in the window `skills/code-review/orchestration.md` calls red — the
    verifying round's record becomes the last one, its own cell reads `not
    yet`, and the whole broad run is taken again.

    The row that answers *has this run ended* is `Fixes checked by`, and its
    starting value is exactly the state that must refuse. `Needs a fix` was
    the first answer and refused a capped run; `Pass` was the second and lets
    this through; this is the third and it is not a replacement for the
    second — the case below asserts both refusals still exist by asserting
    that a capped record, whose cell reads `no fixes to check`, still seals.
    """
    path = fixed_but_unread_item(repo)
    text = path.read_text(encoding="utf-8")
    assert "- [x] Pass" in text, "the fixture is not the window this is about"
    assert fields(text)[CHECKED_BY].startswith("nobody"), text
    before = read_bytes(path)
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert CHECKED_BY in out and "no cell was written" in out, out
    assert "read by no LATER round" in out, out
    assert "Spawn the verifying round first" in out, out
    assert "fails a ready pull request" in out, out
    assert read_bytes(path) == before, "the record was written under a refusal"


def set_checked_by(path, value):
    """Rewrite one record's `Fixes checked by` cell and return its bytes."""
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(
            f"| {CHECKED_BY} | {value} |"
            if line.startswith(f"| {CHECKED_BY} |")
            else line
            for line in text.splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    return path.read_bytes()


@pytest.mark.parametrize("value", ["the smith", "pending", ""])
def test_seal_refuses_a_fixes_checked_by_that_is_outside_the_vocabulary(repo, value):
    """Round 2's 🟡 12. The refusal added for round 1's 🔴 2 asked
    `nobody_reason(...) is not None`, which is true for `nobody` and false for
    everything else — including everything else the row must not hold.

    So the other two thirds of what the cell can carry reached the write: the
    cell was written, `round-record: sealed …` printed, and the chain check
    this subcommand runs AFTER the write then refused on that very row. The
    subcommand wrote onto a record its own check will not accept, which is the
    state 🔴 2 exists to prevent, reached through the value it did not read.

    `reach_back` in this file already refuses an unreadable cell rather than
    acting on it, and says why. This is the same cell one subcommand over."""
    path = fixed_but_unread_item(repo)
    before = set_checked_by(path, value)
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert "no cell was written" in out, out
    assert read_bytes(path) == before, "the record was written under a refusal"


@pytest.mark.parametrize("value", ["round-1", "round-9", "round-2.md", "ROUND-1"])
def test_seal_refuses_a_round_n_on_the_last_record(repo, value):
    """#335. `CHECKER_RE` tests the SHAPE of `Fixes checked by` and cannot
    test its POSITION, so every `round-N` spelling passed the refusal, the
    cell was written, and the chain check `seal` runs after the write refused
    that same row.

    The position is what decides it. A named checker has to be a round LATER
    than the record carrying it, and `last_record` chose this file by being
    the highest-numbered one on disk — so the value is unreachable on the
    record the subcommand is holding. The rule is stated about the last
    record in `docs/review-handoff-protocol.md` §*The `Fixes checked by`
    field*, twice more in `docs/review-chain-spec.md` §*What the record
    carries*, and a third time in `skills/code-review/orchestration.md`'s
    three-value table; enforcing it where the value is WRITTEN is not a new
    inference.

    Red against the tree before this: all four pass the refusal, the cell is
    written, `round-record: sealed …` prints, and the run comes back non-zero
    from the check afterwards.
    """
    path = fixed_but_unread_item(repo)
    before = set_checked_by(path, value)
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert "no cell was written" in out, out
    assert "round-record: sealed" not in out, "the cell was written"
    assert read_bytes(path) == before, "the record was written under a refusal"


def test_the_refusal_says_which_value_the_last_record_may_hold(repo):
    """§14, and the sentence #335 stops being true.

    The refusal used to read *The row holds one of three values: `round-N`,
    `no fixes to check`, or `nobody — <why>`* — true of the ROW and false at
    the place it is printed, which is a last record where two of the three
    are refused. A refusal is read by whoever is stopped by it, so the half
    that says what to do is the half that has to survive the change.

    So: the one value `seal` accepts, both refused values named with the
    reason each is refused, and the exit — spawn the verifying round.

    **The literal names the subcommand rather than reading `the seal`**, and
    it moved here in the commit that moved the message. Two sentences of this
    refusal left the instance anonymous, which is the rule
    `skills/verify/SKILL.md` owns and `tests/test_one_word_one_meaning.py`
    sweeps for.

    **A third assertion stood here and it refused the one spelling the rule
    allows** (#406). `assert "the seal" not in out` had no next-character
    guard, so it turned red on `the sealer` — the correct way to name the
    agent, and what the exit sentence now says. The sweep that owns the rule
    skips a hit whose next character is a letter, and its `SEAL_SWEPT` lists
    `skills/code-review/scripts/round_record.py`, the module this refusal
    lives in. What went is a second, stricter reading of one rule, held by the
    check that is not the rule's owner.

    **The deletion did lose one shape, and round 1's 🟡 2 measured it.** The
    sweep reads that module's flattened SOURCE while this assertion read the
    run's OUTPUT, and Python joins adjacent string literals where a flattened
    read does not — so an anonymous instance split across two literals was
    invisible to the sweep and plain in the refusal. `flat` folds that seam
    now, which restores the coverage inside the one check rather than by
    bringing this assertion back. The two positive pins above stay, which is what keeps §14's
    requirement on this refusal's text met inside the module a reader of it
    opens.
    """
    path = fixed_but_unread_item(repo)
    set_checked_by(path, "pending")
    _code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert "the only value `seal` accepts" in out, out
    # The second sentence the sweep caught, pinned beside the first so the
    # pair cannot drift apart: both name `seal` and neither reads `the seal`.
    assert "`seal` runs with `Pass` ticked" in out, out
    assert "no fixes to check" in out, out
    assert "nobody" in out, out
    assert "Spawn the verifying round first" in out, out
    assert "fails a ready pull request" in out, out
    # §14 for the reworded exit, and the opposite direction of #406: this
    # spelling names whose seal it is, and it is the spelling the deleted
    # assertion turned red.
    assert "before the sealer runs" in out, out
    assert "The row holds one of three values" not in out, (
        "the refusal still names three values on a record that accepts one"
    )


def test_the_capped_run_still_seals_beside_the_third_refusal(repo):
    """The other half of 🔴 2, and what keeps it from undoing phase 5.

    A capped run closes every finding `deferred <home>`, so `close`
    re-derives `Fixes checked by` to `no fixes to check` — nothing here
    commissioned a fix, so nobody owes it a reading. `nobody_reason` returns
    None for that value and the new refusal does not fire. Asserted rather
    than argued, because the two rows look alike and a reader who conflates
    them takes the capped run's seal away again."""
    path = capped_item(repo)
    assert fields(path.read_text(encoding="utf-8"))[CHECKED_BY] == "no fixes to check"
    head = short(repo, "HEAD")
    code, out = run_seal(repo, f"{head} against base")
    assert code == 0, out
    assert fields(path.read_text(encoding="utf-8"))[ROW] == f"{head} against base"


def test_seal_refuses_a_sha_the_target_descends_from(repo):
    """S4. The gate ran at the base and the round reviewed a commit after
    it: the run was spent before the round it seals — the test
    `chain_check.broad_gate` applies at the pull request, asked before the
    cell is written. Refused, naming both commits, and no byte written."""
    _one, two = settled_item(repo)
    before = read_bytes(two)
    premature = short(repo, "base")
    code, out = run_seal(repo, f"{premature} against base")
    assert code == 2, out
    assert "descends from" in out and premature in out and "no cell was written" in out
    assert read_bytes(two) == before


def test_seal_refuses_a_cell_with_no_sha_in_it(repo):
    """The cell records a commit; a value the pull-request check could not
    read as one is refused here rather than failed there."""
    _one, two = settled_item(repo)
    before = read_bytes(two)
    code, out = run_seal(repo, "passed, trust me")
    assert code == 2, out
    assert "SHA-shaped" in out and read_bytes(two) == before


# --- 1790835051: `seal --check` asks every refusal and writes nothing (#702) --
#
# The preflight asks the sealer's own subcommand rather than restating its
# predicates, so the flag has two halves to hold: everything `seal` refuses,
# `--check` refuses with the same sentence, and nothing `--check` passes is
# written — no cell, no `broad-gate.md`, no chain check after.

CHECK_FLAG = ("--check",)


def generator_module():
    return _load("specseal_round_record_for_seal_check", GENERATOR)


def unchecked_pass(repo):
    """An open finding, so the last record's `Pass` is unchecked."""
    declared(repo)
    return generate(repo, 1, OPEN_ROW, "no"), None


def unread_fixes(repo):
    """#535's shape as `new` and `close` write it: `Pass` ticked beside
    `nobody — the fixes are not yet written` on the last record."""
    return fixed_but_unread_item(repo), None


def spent_sha(repo):
    """A settled item, asked with the base's commit: round 2's `Target SHA`
    descends from it."""
    _one, two = settled_item(repo)
    return two, short(repo, "base")


def no_round_record(repo):
    """A chain declaration whose `rounds/` holds nothing yet."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare the chain, rounds not written yet")
    return repo / ITEM / GATE_FILE, None


@pytest.mark.parametrize(
    "shape, said",
    [
        (unchecked_pass, "`Pass` is unchecked"),
        (unread_fixes, "read by no LATER round"),
        (spent_sha, "descends from"),
        (no_round_record, "holds no `round-N.md`"),
    ],
    ids=["pass-unchecked", "nobody-on-the-last-record", "spent-sha", "no-record"],
)
def test_seal_check_refuses_what_seal_refuses_and_writes_nothing(repo, shape, said):
    """S1. Each refusal `seal` raises before the write, asked under `--check`:
    exit 2 with `seal`'s own sentence, the record (or the absent
    `broad-gate.md`) unchanged, and no chain check run. Seen red first with
    the flag absent, where argparse refuses the command before any of them is
    asked."""
    path, at = shape(repo)
    before = read_bytes(path) if path.exists() else None
    code, out = run_seal(repo, f"{at or short(repo, 'HEAD')} against base", CHECK_FLAG)
    assert code == 2, out
    assert said in out and "no cell was written" in out, out
    assert "chain-check:" not in out, f"`--check` ran the chain check:\n{out}"
    after = read_bytes(path) if path.exists() else None
    assert after == before, f"`--check` wrote {path.name} under a refusal"


def hand_edited_last(edit):
    """A settled item whose last record `edit` rewrites and commits."""

    def shape(repo):
        _one, two = settled_item(repo)
        two.write_text(edit(two.read_text(encoding="utf-8")), encoding="utf-8")
        commit(repo, "the last record edited by hand")
        return two

    return shape


def without_the_row(text):
    return "".join(
        line for line in text.splitlines(True) if not line.startswith("| Broad gate |")
    )


def with_the_row_twice(text):
    return "".join(
        line * (2 if line.startswith("| Broad gate |") else 1)
        for line in text.splitlines(True)
    )


def with_an_open_comment(text):
    # Spelled in two parts so no record generated from a report quoting this
    # case carries a literal comment opener.
    return text + "\n<" + "!-- left open by hand\n"


@pytest.mark.parametrize(
    "edit, said",
    [
        (without_the_row, "has 0 `| Broad gate | … |` rows"),
        (with_the_row_twice, "has 2 `| Broad gate | … |` rows"),
        (with_an_open_comment, "never closed"),
    ],
    ids=["no-row", "two-rows", "open-comment"],
)
def test_seal_check_refuses_what_the_write_path_refuses(repo, edit, said):
    """S1's class, past the six `raise` sites (round 1's 🟡 1): `field_index`,
    `cell` and `hiders_close` refuse on the write path, inside callees.
    `--check` exited 0 on each while `seal` refused it after the sealer's
    suite. Seen red at `090cb32f`, where the `--check` return stood above
    all three."""
    path = hand_edited_last(edit)(repo)
    before = read_bytes(path)
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base", CHECK_FLAG)
    assert code == 2, out
    assert said in out, out
    assert "chain-check:" not in out, out
    assert read_bytes(path) == before


def settled_last(repo):
    return settled_item(repo)[1]


def direct_home(repo):
    """`straight to the PR`, no rounds: the cell's home is `broad-gate.md`."""
    write(repo, f"{ITEM}/routing.md", declaration(review="straight to the PR"))
    commit(repo, "declare direct")
    return repo / ITEM / GATE_FILE


@pytest.mark.parametrize(
    "shape, line",
    [
        (settled_last, "CHECKED"),
        (capped_item, "CHECKED"),
        (direct_home, "CHECKED_NO_ROUND"),
    ],
    ids=["settled", "capped", "straight-to-the-pr"],
)
def test_seal_check_passes_what_seal_would_seal_and_writes_nothing(repo, shape, line):
    """S2. A record `seal` would write, asked under `--check`: exit 0, the
    record (or the absent `broad-gate.md`) byte-identical, no chain check,
    and the one line naming the home asked and saying nothing was written.
    The line never begins `round-record: sealed`, which `broad_gate.py#gate`
    reads as the cell having been written. Seen red with `--check` ignored:
    the cell is written and the byte comparison fails."""
    path = shape(repo)
    before = read_bytes(path) if path.exists() else None
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base", CHECK_FLAG)
    assert code == 0, out
    after = read_bytes(path) if path.exists() else None
    assert after == before, f"`--check` wrote {path.name}"
    assert "chain-check:" not in out, f"`--check` ran the chain check:\n{out}"
    generator = generator_module()
    said = getattr(generator, line).format(
        path=path.relative_to(repo).as_posix(), dash=generator.DASH
    )
    assert out.splitlines() == [said], out
    assert not out.startswith("round-record: sealed"), out


# A repository-relative path a line prints is written with `/` on every
# platform. `ntpath` drives the Windows separators from a POSIX machine, so the
# Windows leg of CI is not the only witness (`agent-contract` §13): every
# integration case above runs on macOS, where `os.sep` is already `/`.
WINDOWS_ROOT = r"C:\x\repo"


def windows_path(home):
    """`home`, a `/`-joined repository-relative path, under `WINDOWS_ROOT`
    as `ntpath` spells it."""
    return ntpath.join(WINDOWS_ROOT, *home.split("/"))


@pytest.mark.parametrize(
    "n, line, home",
    [
        (2, "CHECKED", f"{ROUNDS}/round-2.md"),
        (None, "CHECKED_NO_ROUND", f"{ITEM}/{GATE_FILE}"),
    ],
    ids=["a-round-record", "straight-to-the-pr"],
)
def test_the_checked_line_names_its_home_with_slashes_on_windows(n, line, home):
    """The `seal --check` line formatted with Windows separators names the
    home it asked with `/`. Seen red with `checked_line` formatting
    `flavour.relpath` unreplaced, as `seal` did at `04d8bfd7`: the line named
    `seal\\specs\\…`, which is what the Windows leg failed on."""
    generator = generator_module()
    said = generator.checked_line(n, windows_path(home), WINDOWS_ROOT, ntpath)
    assert said == getattr(generator, line).format(path=home, dash=generator.DASH)


def test_the_check_returns_after_the_last_refusal_and_before_the_write():
    """`plan.md`'s failure scenario. A refusal added to `seal` below the
    `--check` return is refused by the sealer after a suite and passed by the
    preflight — the gap this work closes, reopened one refusal at a time. So
    the statement immediately before `write_record` in `seal`'s body is the
    `--check` guard ending in a `return`, nothing after it raises, and the
    callees that refuse on the write path are each called above it (round
    1's 🟡 1: a `raise` walk alone passed over all three)."""
    with open(GENERATOR, encoding="utf-8") as handle:
        parsed = ast.parse(handle.read())
    seal = next(
        n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == "seal"
    )
    keep = [
        i
        for i, statement in enumerate(seal.body)
        if isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Call)
        and ast.unparse(statement.value.func) == "write_record"
    ]
    assert len(keep) == 1, f"`seal` calls `write_record` {len(keep)} times"
    guard = seal.body[keep[0] - 1]
    assert isinstance(guard, ast.If) and ast.unparse(guard.test) == "args.check", (
        "the statement before `write_record` is not the `--check` guard"
    )
    # The callees that refuse on the write path are asked above the guard.
    above = {
        ast.unparse(node.func)
        for statement in seal.body[: keep[0] - 1]
        for node in ast.walk(statement)
        if isinstance(node, ast.Call)
    }
    for callee in ("kept_broad_gate", "field_index", "cell", "hiders_close"):
        assert callee in above, f"`{callee}` is not asked above the `--check` return"
    assert isinstance(guard.body[-1], ast.Return), "the guard does not return"
    later = [
        node
        for statement in seal.body[keep[0] - 1 :]
        for node in ast.walk(statement)
        if isinstance(node, ast.Raise)
    ]
    assert not later, "a refusal stands below the `--check` return"
    earlier = [
        node
        for statement in seal.body[: keep[0] - 1]
        for node in ast.walk(statement)
        if isinstance(node, ast.Raise)
    ]
    assert earlier, "no refusal stands above the `--check` return"


# --- 1790835051: the preflight asks `seal`'s refusals (#702) -----------------
#
# Under `--preflight`, after the record arms, the gate runs `seal --check` for
# the work item declared for the checked-out branch, keeps its output as
# `seal.txt`, and names `seal` under `PREFLIGHT FAILED` where it refused. A
# skipped ask is a missing `seal.txt` and one stderr line, never a pass.

RECORD_FILE = f"{ITEM}/rounds/round-{{n}}.md"


def preflight(repo, tmp_path, row=None):
    """The preflight over `repo`, with a session set so a values file would
    land where `values_files` looks. `row`, where given, is committed as the
    `Broad gate` row first."""
    if row is not None:
        set_row(repo, row)
    keep = tmp_path / "out"
    return run_gate(repo, "--preflight", keep=keep, session="s-1"), keep


def marker_row():
    """A row that leaves a file behind and fails, so a row that ran is
    evidence the gate did not write."""
    return f"{sys.executable} -c \"open('{ROW_RAN}', 'w')\" && exit 1"


def asked_line(home, outcome):
    """The ask's stderr line, naming `home` — the record `seal --check` read
    where it passed and that file is on disk, the work item otherwise."""
    gate = gate_module()
    return gate.PREFLIGHT_ASKED.format(home=home, branch="`feature`", outcome=outcome)


def assert_refused_at_seal(out, keep, said):
    """The preflight's verdict where `seal --check` refused: exit 1, the
    preflight's own head, `seal` among the failing checks in the failure
    form's words, and `seal`'s sentence in the kept file."""
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert out.stdout.startswith("PREFLIGHT FAILED"), out.stdout
    assert re.search(r"^\s+seal\s+exit 2", out.stdout, re.M), out.stdout
    assert "seal.txt" in out.stdout, "the failure form names no file for `seal`"
    assert no_seal_line(out.stdout), out.stdout
    text = (keep / "seal.txt").read_text(encoding="utf-8")
    assert text.startswith("$ ") and "--check" in text.splitlines()[0], text
    assert "\nexit 2\n" in text, text
    assert said in text, text
    assert not (keep / "suite.txt").exists(), "the preflight ran the row"


def test_the_generated_unread_fixes_fail_the_preflight_at_seal(repo, tmp_path):
    """S3, #702's own case. #535's shape exactly as `new` and `close` write it
    — round 1 closed on a fix, no round 2, so `Pass` is ticked beside
    `nobody — the fixes are not yet written` — passed the preflight with exit
    0, and the sealer's run refused it at `seal` after the suite. Now the
    preflight refuses it, names `seal`, and the row, which would leave a file
    and fail, was never invoked. Nothing is written: the record is
    byte-identical and no values file exists. Seen red against phase 1's
    gate, which exits 0 here."""
    path = fixed_but_unread_item(repo)
    text = path.read_text(encoding="utf-8")
    assert "- [x] Pass" in text, "the fixture is not #535's shape"
    assert fields(text)[CHECKED_BY].startswith("nobody"), text
    before = read_bytes(path)
    out, keep = preflight(repo, tmp_path, marker_row())
    assert_refused_at_seal(out, keep, "read by no LATER round")
    assert CHECKED_BY in (keep / "seal.txt").read_text(encoding="utf-8")
    assert not (repo / ROW_RAN).exists(), "the preflight invoked the row"
    assert read_bytes(path) == before, "the preflight wrote the record"
    assert not values_files(repo), "a preflight left a stamp to draw"
    gate = gate_module()
    assert asked_line(ITEM, gate.ASKED_REFUSED) in out.stderr.splitlines(), out.stderr


def test_an_unchecked_pass_fails_the_preflight_at_seal(repo, tmp_path):
    """S4, #456's first instance: an open finding leaves `Pass` unchecked,
    and `seal` refuses it. The preflight now says so before the suite."""
    declared(repo)
    path = generate(repo, 1, OPEN_ROW, "no")
    before = read_bytes(path)
    out, keep = preflight(repo, tmp_path)
    assert_refused_at_seal(out, keep, "`Pass` is unchecked")
    assert read_bytes(path) == before, "the preflight wrote the record"


def test_a_target_that_descends_from_the_tree_fails_the_preflight_at_seal(
    repo, tmp_path
):
    """S5. The gate hands `seal --check` the tree it stands on, so a record
    whose `Target SHA` descends from that tree is a run spent before the round
    it would seal. The target is a commit on a side branch cut from HEAD; the
    record naming it is written by `new` and left uncommitted, so HEAD stays
    the commit the target descends from (`questions.md` Q2)."""
    declared(repo)
    git(repo, "switch", "-qc", "side")
    write(repo, "g.py", "y = 1\n")
    later = commit(repo, "a commit after the tree the gate stands on")
    git(repo, "switch", "-q", "feature")
    generate(
        repo,
        1,
        "| 🟢 1 | the reviewed commit holds | `g.py:1` | answered | read |\n",
        "no",
        target=later,
    )
    git(repo, "reset", "-q", "--soft", "HEAD~1")
    out, keep = preflight(repo, tmp_path)
    assert_refused_at_seal(out, keep, "descends from")


def test_a_settled_item_preflights_green_and_names_the_record_it_asked(repo, tmp_path):
    """S6. The state the sealer runs in: round 2 reads `no fixes to check`
    with `Pass` ticked. Every arm green and `seal --check` exits 0, so the
    preflight passes; `seal.txt` is kept with its exit, the record is
    byte-identical, and one stderr line names `round-2.md` as the record
    asked. Seen red with the ask dropped (no `seal.txt`) and with `--check`
    dropped from the argv (the cell written)."""
    _one, two = settled_item(repo)
    before = read_bytes(two)
    out, keep = preflight(repo, tmp_path)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    head = PREFLIGHT_PASSED.format(tree=short(repo, "HEAD"), base=short(repo, "base"))
    gate = gate_module()
    assert out.stdout.splitlines()[0] == head + gate.PREFLIGHT_TAIL, out.stdout
    assert "`seal`'s refusals" in gate.PREFLIGHT_TAIL, gate.PREFLIGHT_TAIL
    assert NOT_RUN in gate.PREFLIGHT_TAIL, gate.PREFLIGHT_TAIL
    assert no_seal_line(out.stdout), out.stdout
    text = (keep / "seal.txt").read_text(encoding="utf-8")
    assert text.startswith("$ ") and "--check" in text.splitlines()[0], text
    assert "\nexit 0\n" in text, text
    assert read_bytes(two) == before, "the preflight wrote the record"
    assert not values_files(repo), "a preflight left a stamp to draw"
    gate = gate_module()
    said = asked_line(RECORD_FILE.format(n=2), gate.ASKED_PASSED)
    assert said in out.stderr.splitlines(), out.stderr
    # Round 1's ⬜ 4: the record is named as a record, not as the work item.
    assert "found through the one declaration naming `feature`" in said, said


def test_a_direct_item_preflights_green_and_names_the_work_item_it_asked(
    repo, tmp_path
):
    """Round 1's ⬜ 4. A `straight to the PR` item with no rounds is asked and
    passes, and the cell's home is a `broad-gate.md` the sealer has not
    written yet, so the stderr line names the work item rather than a file
    nobody can open. Seen red at `090cb32f`, where the line named the absent
    `broad-gate.md`."""
    path = direct_home(repo)
    assert not path.exists(), "the fixture wrote `broad-gate.md`"
    out, keep = preflight(repo, tmp_path)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "\nexit 0\n" in (keep / "seal.txt").read_text(encoding="utf-8")
    assert not path.exists(), "the preflight wrote `broad-gate.md`"
    gate = gate_module()
    assert asked_line(ITEM, gate.ASKED_PASSED) in out.stderr.splitlines(), out.stderr
    assert GATE_FILE not in out.stderr, out.stderr


@pytest.mark.parametrize(
    "home, outcome",
    [
        (RECORD_FILE.format(n=2), "ASKED_PASSED"),
        (ITEM, "ASKED_REFUSED"),
    ],
    ids=["a-record", "the-work-item"],
)
def test_the_asked_line_names_its_home_with_slashes_on_windows(home, outcome):
    """The ask's stderr line formatted with Windows separators names its home
    with `/`, as `asked_line` spells it for the integration cases above. Seen
    red with `preflight_asked_line` formatting `flavour.relpath` unreplaced,
    as `gate` did at `04d8bfd7`: the line named `seal\\specs\\…`, and S3, S6
    and round 1's ⬜ 4 failed on the Windows leg for it."""
    gate = gate_module()
    said = gate.preflight_asked_line(
        windows_path(home), WINDOWS_ROOT, "feature", getattr(gate, outcome), ntpath
    )
    assert said == asked_line(home, getattr(gate, outcome))


@pytest.mark.parametrize(
    "script, formatter, names, caller",
    [
        (GATE, "preflight_asked_line", ("PREFLIGHT_ASKED",), "gate"),
        (GENERATOR, "checked_line", ("CHECKED", "CHECKED_NO_ROUND"), "seal"),
    ],
    ids=["the-ask", "seal-check"],
)
def test_each_line_naming_a_home_is_formatted_only_by_its_line_function(
    script, formatter, names, caller
):
    """The two cases above drive the line functions with `ntpath`, and every
    integration case runs where `os.sep` is `/` already, so a caller that
    formats the constant itself again prints `\\` on Windows and nothing on
    macOS goes red. So each constant is read inside its line function and
    nowhere else, and the caller calls that function once. Seen red with
    `gate` formatting `PREFLIGHT_ASKED` from `os.path.relpath` again, as it
    did at `04d8bfd7`, which the two cases above passed."""
    with open(script, encoding="utf-8") as handle:
        parsed = ast.parse(handle.read())
    functions = {n.name: n for n in parsed.body if isinstance(n, ast.FunctionDef)}
    inside = {id(node) for node in ast.walk(functions[formatter])}
    outside = [
        f"`{node.id}` at line {node.lineno}"
        for node in ast.walk(parsed)
        if isinstance(node, ast.Name)
        and node.id in names
        and isinstance(node.ctx, ast.Load)
        and id(node) not in inside
    ]
    assert not outside, f"read outside `{formatter}`: {outside}"
    calls = [
        node
        for node in ast.walk(functions[caller])
        if isinstance(node, ast.Call) and ast.unparse(node.func) == formatter
    ]
    assert len(calls) == 1, f"`{caller}` calls `{formatter}` {len(calls)} times"


def test_an_undeclared_branch_is_not_asked_and_the_preflight_says_so(repo, tmp_path):
    """S8. No declaration names `feature`, so there is no work item for a
    sealer to seal and nothing to ask: exit 0, no `seal.txt`, and one stderr
    line naming the branch and saying `seal`'s refusals were not asked."""
    out, keep = preflight(repo, tmp_path)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert not (keep / "seal.txt").exists(), "the preflight asked an undeclared item"
    gate = gate_module()
    said = gate.PREFLIGHT_NOT_ASKED.format(branch="`feature`")
    assert said in out.stderr.splitlines(), out.stderr


def test_two_declarations_for_one_branch_are_not_asked(repo, tmp_path):
    """S8's second half. Two declarations naming `feature` are not an answer
    (`hooks/routing.py#item_dir`), so the ask is skipped with the same line;
    the chain arm's own refusal of the pair is what fails the run, and `seal`
    is not among the failures."""
    write(repo, f"{ITEM}/routing.md", declaration())
    write(repo, "seal/specs/1799000001-a-second-item/routing.md", declaration())
    commit(repo, "two declarations name one branch")
    out, keep = preflight(repo, tmp_path)
    assert not (keep / "seal.txt").exists(), "the preflight asked one of two"
    assert not re.search(r"^\s+seal\s+exit", out.stdout, re.M), out.stdout
    gate = gate_module()
    said = gate.PREFLIGHT_NOT_ASKED.format(branch="`feature`")
    assert said in out.stderr.splitlines(), out.stderr
    # Round 1's ⬜ 4: two declarations are not "no record"; the line says so.
    assert "more than one does" in said, said


def test_a_detached_head_is_not_asked_and_the_preflight_says_why(repo, tmp_path):
    """S8 on a detached HEAD: no branch is checked out, so no declaration can
    name this checkout. The item is declared for `feature` and would refuse
    — an unchecked `Pass` — so an ask that ran anyway is a `seal.txt` and a
    failing run."""
    declared(repo)
    generate(repo, 1, OPEN_ROW, "no")
    git(repo, "switch", "-q", "--detach")
    out, keep = preflight(repo, tmp_path)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert not (keep / "seal.txt").exists(), "the preflight asked on a detached HEAD"
    assert gate_module().PREFLIGHT_DETACHED in out.stderr.splitlines(), out.stderr


def test_the_gate_with_record_seals_the_item_and_counts_its_rounds(repo, tmp_path):
    """S1 with `--record`: the checks pass, `seal` writes the last record's
    cell with the tree and the base, and the panel carries `rounds 2` — read
    from the values file since #400, which is where a piped run's panel is."""
    _out, values = sealed_values(repo, tmp_path)
    two = repo / ROUNDS / "round-2.md"
    assert row_of(values, "rounds") == "2", values["rows"]
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    # The base half used to be the ref as the caller typed it -- `against
    # base`. #423 is that a ref re-resolves and a commit does not, so the
    # cell now names the commit the gate actually compared against. This
    # fixture has no remote, so the resolution lands on the ref as given and
    # the COMMIT is the only thing that moved. Both parsers of this cell read
    # the FIRST SHA-shaped word, which is the tree, so neither sees a
    # difference (`chain_check.broad_gate`, `round_record.py seal`).
    assert cell == f"{short(repo, 'HEAD')} against {short(repo, 'base')}", cell


def test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter(repo, tmp_path):
    """Round 1's 🟡 3. The panel carried `lint  clean` as a literal, beside
    four rows read from what the checks printed.

    The `Broad gate` row is one shell command line and nothing in it says
    which part is a linter — `templates/config.md` says so itself, which is
    why the base comparison re-runs whatever stands before the first `&&`
    rather than a linter it identified. A repository whose row is only a test
    runner got a seal asserting a check that never ran, on the artifact a
    reader trusts BECAUSE it is drawn on success alone.

    The fixture's row is a bare pytest call, with no linter in it at all.
    Read from the values file since #400, which is where a piped run's panel
    is. Since #666 the exit code continued under `suite` rather than on a
    `row` of its own, and since #717 it is not on the panel at all: a drawn
    panel's row came back 0 by construction, which `SEALED` says, so the row
    after the counts is the ledger's."""
    _out, values = sealed_values(repo, tmp_path)
    rows = values["rows"]
    at = rows.index(("suite", "1 passed"))
    assert rows[at + 1] == ("ledger", "0 ok"), rows
    assert not any("clean" in cell for row in values["rows"] if row for cell in row), (
        "the seal still asserts a linter over a row that has none in it"
    )


def test_a_runners_event_payload_judges_the_fixture_and_fails_its_gate(
    repo, tmp_path, monkeypatch, capsys
):
    """What the leak did, reproduced deliberately so it is not only CI's to
    find. `1 failed, 3168 passed` on ubuntu, macOS and windows alike, and
    green on every laptop.

    With `GITHUB_EVENT_PATH` pointing at a REAL pull request's payload, the
    gate's own chain check judges this fixture repository a ready pull
    request and fails it on the fixture record's `Broad gate: not yet` —
    which is #332's state, read into a repository that has nothing to do with
    it. The gate then never reaches `seal` at all.

    This is the case that gives the clearing fixture above its teeth on a
    machine that sets nothing: it puts the variable back on purpose and
    asserts the consequence, so a reader who removes the guard can see what
    the guard was for without waiting for a pull request to go red."""
    settled_item(repo)
    monkeypatch.setenv("GITHUB_EVENT_PATH", ready_payload(tmp_path))
    mod = gate_module()
    code = mod.gate(
        argparse.Namespace(
            root=str(repo),
            base="base",
            record=str(repo / ITEM),
            shape=True,
            scale=1.0,
            keep_output=str(tmp_path / "out"),
            preflight=False,
        ),
        False,
    )
    out = capsys.readouterr()
    assert code == 1, f"exit {code}\n{out.out}{out.err}"
    assert "NOT SEALED" in out.out, out.out
    assert re.search(r"^\s+chain\s+exit 1", out.out, re.M), (
        f"the chain check is not what failed:\n{out.out}"
    )
    assert "ready pull request" in out.out, out.out


def test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed(
    repo, tmp_path, monkeypatch, capsys
):
    """Round 1's 🔴 1. `seal` has two ways to end non-zero and the gate read
    one of them.

    A refusal raised BEFORE the write exits 2. What `seal` returns AFTER the
    write is `run_check`, which is `chain_check.main`'s `1 if errors else 0`
    — so a chain check that fails once the cell is on disk comes back as 1,
    fell past a branch reading `== 2`, and the gate printed the disc and
    returned 0. A seal over a tree its own chain check refuses is the
    counterfeit `verify` names.

    Driven in process with `seal_record` stubbed, because the exit code is
    the whole subject: a fixture that makes the real chain check fail after
    the write would be testing which state trips `chain_check`, not which
    codes the gate reads."""
    settled_item(repo)
    mod = gate_module()
    reached = []

    def sealed_then_the_chain_failed(item, tree, root, base, keep):
        reached.append(item)
        return (
            1,
            "round-record: sealed round-2.md — `Broad gate` | abc123 against base\n",
        )

    monkeypatch.setattr(mod, "seal_record", sealed_then_the_chain_failed)
    monkeypatch.setenv(SESSION_VAR, "s-1")
    code = mod.gate(
        argparse.Namespace(
            root=str(repo),
            base="base",
            record=str(repo / ITEM),
            shape=True,
            scale=1.0,
            keep_output=str(tmp_path / "out"),
            preflight=False,
        ),
        False,
    )
    out = capsys.readouterr()
    assert reached, f"the checks failed before `seal` was reached\n{out.out}{out.err}"
    assert code == 2, f"exit {code}\n{out.out}{out.err}"
    assert crown_of() not in out.out, "a stamp printed over a failing chain check"
    # S8 of 1790562543: the line above is vacuous on a pipe since #400.
    assert not values_files(repo), "a stamp was left to draw over a failing chain"
    # Round 2's 🟡 11. The stub's text is a `round-record: sealed …` line,
    # which is what the real subcommand prints when the cell WAS written.
    # The message has to read it that way round, or the reader is told the
    # record is untouched while the cell stands on it — and the pointer it
    # shipped with, *a `round-record:` line above*, is printed by both
    # endings of `seal`.
    assert "exited 1" in out.err, out.err
    assert "the cell WAS written" in out.err, out.err
    assert "no cell was written" not in out.err, out.err


def test_the_gate_with_record_prints_no_stamp_when_the_record_refuses(repo, tmp_path):
    """With `--record`, success is the checks green AND the cell written. A
    record that refuses — a finding still open in its verdict table — leaves
    the tree unsealed: the refusal, exit 2, no disc."""
    declared(repo)
    path = generate(repo, 1, OPEN_ROW, "yes — 🔴 1")
    before = read_bytes(path)
    out = run_gate(
        repo, "--record", str(repo / ITEM), keep=tmp_path / "out", session="s-1"
    )
    assert out.returncode == 2, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert crown_of() not in out.stdout, "a stamp printed over a refused record"
    # S8 of 1790562543: the line above is vacuous on a pipe since #400.
    assert not values_files(repo), "a stamp was left to draw over a refused record"
    assert "`Pass` is unchecked" in out.stdout + out.stderr
    # The other half of round 2's 🟡 11, and the one that makes the
    # discriminator worth having: this is the refusal side, so the gate has
    # to say the opposite. A discriminator that read the bare
    # `round-record:` prefix would tell a reader here that the cell was
    # written, which is the mutation this pair exists to kill.
    assert "no cell was written" in out.stdout + out.stderr, out.stderr
    assert "the cell WAS written" not in out.stdout + out.stderr, out.stderr
    assert read_bytes(path) == before


def a_record_the_chain_check_refuses_after_the_write(repo):
    """The route to *the cell was written, and then the check refused*.

    **This is Q3's answer and it is asserted as the route.** The cheapest way
    to that state used to be #335's own defect — `round-1` in a last record's
    `Fixes checked by`, which passed the shape test, wrote the cell, and was
    then refused by the chain check on the same row. The refusal above closes
    it, so the case below needs a route that does not depend on anything this
    work item changes.

    Four candidates were run against the real `seal` on 2026-09-15. Three
    reached the state and one did not:

      an earlier record's `New units` emptied      reached — CHOSEN
      the last record's `Target SHA` unresolvable  reached
      an earlier record's floor row emptied        reached
      a stray `round-draft.md` under `rounds/`     NOT reached, exit 0

    The first is chosen because it is the one furthest from anything `seal`
    reads: `seal` opens the LAST record only, and `chain_check.fix_surface`
    opens every record of the item. A present-and-empty row is refused on any
    record and is not grandfathered, so the route does not age out with a
    cutoff either.

    **And it is left UNCOMMITTED, which is the half a case going through the
    gate has to get right.** `broad_gate` runs `chain_check` itself, at HEAD,
    before it ever calls `seal`; `seal` runs `chain_check --worktree` after
    the write. So a committed refusal never reaches `seal` at all — the
    gate's own chain check fails first and the run stops there, which is a
    third ending and not one of the two this pair is about. A refusal that
    exists in the working tree and not at HEAD passes the gate's check and
    fails `seal`'s, which is exactly the window `--worktree` exists for.

    Returns the last record, whose cell `seal` will write.
    """
    _one, two = settled_item(repo)
    text = _one.read_text(encoding="utf-8")
    assert "| New units |" in text, "the fixture record has no `New units` row"
    _one.write_text(
        "\n".join(
            "| New units |  |" if line.startswith("| New units |") else line
            for line in text.splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    return two


def test_the_gate_reads_the_real_seals_two_endings_apart(repo, tmp_path):
    """#334. The gate discriminates two endings of `seal` on the literal
    `round-record: sealed`, which the other package PRINTS — and nothing bound
    them. The case for the written-then-refused ending drove a stub whose text
    the case itself wrote, so changing the real print left 130 cases green.

    This is the same pair, both endings, through the REAL `seal`:

      `Pass` unchecked            a refusal raised BEFORE the write, so no
                                  `round-record: sealed` line and no cell
      an earlier record refused    the cell IS written, `round-record: sealed`
        by the chain check         prints, and what follows is the chain check
                                   `seal` runs after the write

    The exit code cannot tell them apart — both come back 2 from the gate —
    and neither can the presence of a `round-record:` line, which both endings
    print. The word is the discriminator, and this case is what says so about
    the word the generator actually prints rather than one a fixture wrote.
    """
    two = a_record_the_chain_check_refuses_after_the_write(repo)
    before = read_bytes(two)
    out = run_gate(
        repo, "--record", str(repo / ITEM), keep=tmp_path / "out", session="s-1"
    )
    printed = out.stdout + out.stderr

    assert out.returncode == 2, f"exit {out.returncode}\n{printed}"
    assert crown_of() not in out.stdout, "a stamp printed over a failing chain check"
    # S8 of 1790562543: the line above is vacuous on a pipe since #400.
    assert not values_files(repo), "a stamp was left to draw over a failing chain"
    # The route reached the state it was written for, asserted rather than
    # assumed, so it cannot quietly stop reaching it.
    assert "round-record: sealed" in printed, (
        "the route no longer reaches the written-then-refused state; the case "
        "below would then be asserting the refusal side twice"
    )
    assert "`New units` is empty" in printed, printed
    assert "the cell WAS written" in printed, printed
    assert "no cell was written" not in printed, printed
    assert read_bytes(two) != before, "the cell was not written"


def test_the_sealers_definition_names_the_narrowed_row(repo):
    """§14 for the person who meets the refusal. #335 narrows what `seal`
    accepts in `Fixes checked by`, and the sealer is the only agent that runs
    it — so its own definition has to say so, or the one party who is stopped
    by the refusal learns the rule from the refusal alone.

    The definition listed two refusals where the subcommand has had three
    since round 1 of #30 added the `Fixes checked by` one; this is that gap
    closed in the same commit that changes what the row accepts.
    """
    text = sealer_text()
    assert "reading anything but `no fixes to check`" in text, text
    assert "refuses outright on three things" in text, (
        "the definition still counts two refusals where `seal` raises on three"
    )


# =============================================================================
# Part 3 — the owner, and the fourth definition
# =============================================================================

# `agents/smith.md` and `agents/warden.md` each carried the rule with no owner
# in it: *the full suite is the orchestrator's*. #30's opening argument is that
# a rule forbidding two agents an act and assigning it to nobody is assigned to
# whoever remembers. The sentence names the sealer in both, and the definitions
# are where it has to be named — a document a session loads on demand reaches
# the session that already knew.
SEALER = os.path.join(ROOT, "agents", "sealer.md")
OWNED = "the full suite is the sealer's, once, after the rounds settle"
UNOWNED = "the full suite is the orchestrator's"
PROBE = (
    "a coverage probe — nothing in the suite catches this — is a different "
    "act: run it, and report it as a probe, never as a seal"
)
DEFINITIONS = ("smith.md", "warden.md")

# The contract's own §2 and §6, read from the contract rather than typed, so a
# section that is rewritten (#120) is compared as it then stands.
CONTRACT = os.path.join(ROOT, "skills", "agent-contract", "SKILL.md")

# `tests/test_a_moved_rule_leaves_its_definition.py` measured this: 15 words is
# longer than any phrase a kept application shares with a section, and shorter
# than the smallest real paste. Imported as a number rather than a rule — the
# case below applies it to ONE definition, the one that talks about §2 by name
# and is therefore the one at risk of quoting it.
WINDOW = 15


def agent(name):
    with open(os.path.join(ROOT, "agents", name), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


def sealer_text():
    with open(SEALER, encoding="utf-8") as handle:
        return handle.read()


def section(number):
    """The body of `## §N` in the contract, heading excluded."""
    with open(CONTRACT, encoding="utf-8") as handle:
        text = handle.read()
    heads = list(re.finditer(r"^## §(\d+) (.+)$", text, re.M))
    for index, match in enumerate(heads):
        if int(match.group(1)) != number:
            continue
        end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
        return " ".join(text[match.end() : end].split())
    raise AssertionError(f"the contract has no §{number}")


# --- S6 the owner ------------------------------------------------------------


@pytest.mark.parametrize("definition", DEFINITIONS)
def test_the_definition_names_the_sealer_as_the_suites_owner(definition):
    """The rule reached both definitions with no owner in it. Naming the
    sealer in the skill alone would leave both agents reading a sentence that
    forbids without assigning, which is the state #30 opens with."""
    text = agent(definition)
    assert OWNED in text, (
        f"agents/{definition} no longer says whose the full suite is, so the "
        "rule forbids it to this agent and assigns it to nobody"
    )
    assert UNOWNED not in text, (
        f"agents/{definition} still names the orchestrator as the suite's "
        "owner beside the sealer, which is two owners for one act"
    )


@pytest.mark.parametrize("definition", DEFINITIONS)
def test_the_owner_is_named_once_in_each_definition(definition):
    """Twice is how the two copies drift apart — which is the failure the
    contract exists to end, one file down."""
    assert agent(definition).count(OWNED) == 1, (
        f"agents/{definition} states the owner sentence "
        f"{agent(definition).count(OWNED)} times"
    )


@pytest.mark.parametrize("definition", DEFINITIONS)
def test_the_definition_separates_a_coverage_probe_from_a_seal(definition):
    """The near miss the owner sentence creates. *Does anything in the suite
    catch this* is answered by running the suite, and an agent that reads only
    *the full suite is the sealer's* either does not ask it or reports the
    answer as a seal. It is a probe: run it, and label it one."""
    assert PROBE in agent(definition), (
        f"agents/{definition} does not separate a coverage probe from a seal, "
        "so the one run that is not a seal has no name"
    )


def test_the_warden_says_what_comes_due():
    """The warden's report is what ends the rounds, so it is the one segment
    positioned to say the gate is next. Saying so without naming what is
    spawned leaves the orchestrator to remember the sealer exists."""
    warden = agent("warden.md")
    assert "what comes due is the sealer's spawn" in warden, (
        "the warden says the broad run is next and does not say who takes it"
    )


def test_the_smith_says_who_takes_the_gate_it_hands_to():
    """`Then the broad gate runs once` named no runner, in the file the
    implementer reads at the end of every chain."""
    smith = agent("smith.md")
    assert "Then the sealer takes the broad gate once" in smith, (
        "the smith's closing paragraph still leaves the broad run unassigned"
    )


# --- S7 the fourth definition ------------------------------------------------
#
# The contract paragraph this file opens with is held to byte identity by
# `tests/test_every_agent_reads_the_contract.py`, over a glob this file joins
# on the day it lands. Re-pinning it here would be the duplication that module
# and `tests/test_a_moved_rule_leaves_its_definition.py` exist to refuse, so
# what part 3 pins is what no existing module reads.


def test_the_fourth_definition_exists():
    assert os.path.exists(SEALER), "agents/sealer.md is not in the tree"


def test_the_sealer_preloads_the_contract_and_nothing_else():
    """Q5: its whole procedure is one command, and #292 measured every
    preloaded body as a cost paid again on every spawn. `verify` is 35 KB for
    four conditions the definition states in four lines."""
    head = sealer_text().split("\n---\n", 1)[0]
    assert re.findall(r"^  - (\S+)", head, re.M) == ["agent-contract"], (
        "the sealer's `skills:` list is not `agent-contract` alone, so a body "
        "rides every spawn for a procedure that is one command"
    )


def test_the_sealer_names_the_command_it_runs():
    """The procedure is the command; a definition that describes the checks
    instead is a second source that drifts from `broad_gate.py`."""
    text = " ".join(sealer_text().split())
    assert "broad-gate --base <base> --record <item>" in text, (
        "the sealer's definition does not name the command that is its whole procedure"
    )


def test_the_sealer_names_the_one_write_its_definition_is_allowed():
    """§6 says what an agent writes is named in its own definition and nothing
    else, so this file is the whole of the sealer's permission. A write nobody
    named is a review that certifies itself.

    Before #120 the same case read `as its own exception`, because §6 carved
    exceptions and pointed at the definition holding each one. The mechanism
    did not move -- it stopped being the exception and became the rule -- so
    every assertion below is unchanged and only the name and the grounds are."""
    text = " ".join(sealer_text().split())
    assert "§6" in text, "the sealer cannot reach the rule that names its one write"
    assert "round_record.py seal" in text, (
        "the sealer's one write does not name the subcommand that makes it, "
        "so the write is described rather than bounded"
    )
    assert "`Broad gate`" in text, (
        "the exception does not say WHICH cell, and an exception without a "
        "boundary is a general permission"
    )


def test_the_sealer_recites_the_four_acts_s6_actually_withholds():
    """Round 1, finding 10 of #120. The definition recited §6's withheld acts
    as *no pull request, no push, no commit, no agent spawned* -- it dropped
    `post` and added `commit`, which §6 withholds from nobody.

    Nothing shipped broken, and that is why it is a correction rather than a
    fix: §6 now binds its four `whatever its file says`, so the sealer could
    not have granted itself posting either way. What the branch changed is
    that §6's list became explicit and countable, and a loose recitation
    beside a countable list is a second source that disagrees with the first.

    The four words are checked against §6's own sentence before they are
    checked against the definition, so the two cannot drift apart silently:
    change §6's list and this case names the word that left."""
    withheld = next(part for part in section(6).split(". ") if "post nothing" in part)
    recital = next(
        part
        for part in " ".join(sealer_text().split()).split(". ")
        if "§6 withholds stays withheld" in part
    )
    for act in ("post", "push", "pull request", "spawn"):
        assert act in withheld, (
            f"§6's own list no longer withholds `{act}`, so this case is "
            "measuring the definition against a sentence that moved"
        )
        assert act in recital, (
            f"the sealer's recitation of §6 drops `{act}`. The list is "
            "countable now, and a recitation one short reads as permission"
        )
    assert "commit" not in recital, (
        "the recitation adds an act §6 withholds from nobody. A definition "
        "that over-recites teaches the next reader a rule the contract does "
        "not have, which is the same defect as under-reciting"
    )


def test_the_window_the_sealer_shipped_under_is_closed():
    """#120 closed it, and this case is the one that says so.

    The sealer shipped under a §2 that forbade its one act, for a window
    inside one release branch, and its definition wrote the contradiction down
    rather than leaving the next reader to guess which document wins. That
    paragraph carried its own expiry -- *when #120 lands, this section is the
    paragraph it deletes* -- and #120 deleted it.

    Rewritten rather than deleted, and that is the point of it. A case removed
    with the paragraph it pinned leaves nothing to notice the paragraph coming
    back, and this one came with a ticket number in it, which is exactly the
    prose a later session restores while tidying. So the assertions invert:
    the window's own words are absent, and what the section was standing
    against is now a positive assignment.

    The two facts `spec.md` requires the definition to keep -- §6 and the one
    cell -- are asserted by
    `test_the_sealer_names_the_one_write_its_definition_is_allowed` above, which
    is where they belong; repeating them here would make two cases fail for one
    edit and neither of them say which."""
    text = " ".join(sealer_text().split())
    assert "narrower document" not in text, (
        "the window paragraph is back. It says the definition wins over the "
        "contract, which was true only while §2 forbade the sealer's one act"
    )
    assert "#120" not in text, (
        "the definition still names the ticket that was to settle §2. #120 "
        "has landed, so a reader following it finds a closed issue and no "
        "contradiction to match it against"
    )
    assert "§2 as it stands" not in text, "the section heading survived"
    assert "§2" in text, (
        "the definition stopped citing §2 altogether. §2 now says the "
        "assignment lives in the definition rather than in the contract, so a "
        "silent definition makes that pointer name a file that does not answer"
    )
    assert "spawned for exactly that" in text, (
        "the positive assignment went with the apology. Deleting the window "
        "without it leaves the one act nobody's again, which is #30's opening"
    )


def test_the_sealer_carries_the_four_conditions_in_its_own_words():
    """Q5 again, from the other side: dropping `verify` from the spawn is only
    correct if the conditions arrive some other way."""
    text = " ".join(sealer_text().split())
    for condition in (
        "Name the command before you run it",
        "show the check can fail",
        "Bind the result to a tree state",
        "`executed`",
        "`unverified`",
    ):
        assert condition in text, (
            f"the sealer's definition does not carry `{condition}`, and "
            "`verify` is not in its `skills:` list to carry it instead"
        )


@pytest.mark.parametrize("number", (2, 6))
def test_the_sealer_cites_the_section_without_carrying_it(number):
    """The sealer is the one definition that talks about §2 and §6 by name, so
    it is the one at risk of quoting them. Citing a number and saying what it
    means for this role is the application form; a run of the section's own
    words is the paste `tests/test_a_moved_rule_leaves_its_definition.py`
    measured, and that module holds the whole glob to it."""
    body = section(number).split()
    text = " ".join(sealer_text().split())
    copied = [
        " ".join(body[i : i + WINDOW])
        for i in range(len(body) - WINDOW + 1)
        if " ".join(body[i : i + WINDOW]) in text
    ]
    assert not copied, f"agents/sealer.md carries §{number}'s own words: {copied}"
