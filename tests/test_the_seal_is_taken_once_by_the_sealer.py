"""The seal is taken once, by the sealer, and this is what it prints.

Issue #30. Part 1 pins the stamp module, `skills/verify/scripts/seal_stamp.py`:
the disc is computed from a chart, so it cannot be off centre; a letter twin
exists for a console that cannot draw half-blocks, and it has the block form's
footprint; colour is emitted at transitions, never per cell; the panel beside
the disc is data; the chart has a floor; and the failure form carries no
drawing at all, because a picture that says *sealed* beside a word that says
*not* is the two-things-disagreeing defect this repository keeps paying for.

Parts 2 and 3 — the gate command, the `seal` subcommand, the agent and the
owner sentences — arrive with the phases that build them.
"""

import importlib.util
import io
import os
import re
import subprocess

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
WRAPPER = os.path.join(ROOT, "bin", "seal-stamp")

# The shape `spec.md` §*Data & interfaces* draws: a heading row, blanks between
# groups, and `(label, value)` pairs. Values are neutral.
ROWS = [
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

SGR = re.compile(r"\x1b\[[0-9;]*m")
HALF_BLOCKS = ("▀", "▄")


def module():
    spec = importlib.util.spec_from_file_location("specseal_seal_stamp", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ink(line):
    """The visible width of a line: colour codes removed, trailing blanks
    dropped. Two forms of the same disc agree on this and on nothing finer,
    because one of them carries escape sequences and the other does not."""
    return len(SGR.sub("", line).rstrip())


def run_wrapper(*args, env=None):
    return subprocess.run(
        [WRAPPER, *args],
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


@pytest.mark.parametrize("scale", [1.0, 0.75])
def test_the_twin_and_the_block_form_have_equal_width_and_height(scale):
    """S5. A twin that is a different size is a different drawing, and the
    reader on a cp949 console would be looking at something nobody measured.
    Compared row by row on visible width, at full scale and at the floor."""
    mod = module()
    blocks = mod.stamp(ROWS, scale=scale, shape=False)
    letters = mod.stamp(ROWS, scale=scale, shape=True)
    assert len(blocks) == len(letters), (
        f"{len(blocks)} block rows against {len(letters)} letter rows at {scale}"
    )
    widths = [(ink(b), ink(t)) for b, t in zip(blocks, letters, strict=True)]
    assert all(b == t for b, t in widths), (
        f"the twin's rows differ in width from the block form's: {widths}"
    )
    assert not any(SGR.search(line) for line in letters), (
        "the letter twin carries colour codes, which is the one thing the "
        "console it exists for cannot show"
    )
    assert not any(c in line for line in letters for c in HALF_BLOCKS), (
        "the letter twin still carries a half-block character"
    )


def test_the_disc_is_symmetric_because_it_is_computed():
    """#30 §*How it is drawn*: four hand-typed discs were lopsided; a computed
    one cannot be. Every twin row has the same left and right margin."""
    mod = module()
    w, h, px = mod.build(1.0)
    for y in range(0, h, 2):
        line = mod.letter_row(px, w, y)
        left = len(line) - len(line.lstrip())
        right = len(line) - len(line.rstrip())
        assert left == right, f"row {y}: {left} blank on the left, {right} on the right"


# --- colour at transitions -------------------------------------------------


def test_a_coloured_row_carries_fewer_colour_sequences_than_cells():
    """#30 §*Output size*: a code per cell was 282 KB for one seal. Emitting at
    transitions is what makes the colour form printable, and every row is
    held to it — the rope rows, where colour alternates most, included."""
    mod = module()
    w, h, px = mod.build(1.0)
    for y in range(0, h, 2):
        line = mod.colour_row(px, w, y)
        sequences = len(SGR.findall(line))
        assert sequences < w, f"row {y}: {sequences} colour sequences for {w} cells"


# --- the panel -------------------------------------------------------------


def test_the_panel_renders_its_rows_and_its_blanks():
    """The panel is data — `(label, value)` rows with `None` for a blank — so
    what the seal reports is a list the gate fills, not a string it formats.
    Every label and value lands on its own line, and every `None` is a line
    carrying nothing but the frame."""
    mod = module()
    panel = mod.letter(ROWS)
    body = panel[2:-2]  # inside the border and its two padding lines
    assert len(body) == len(ROWS), f"{len(body)} panel lines for {len(ROWS)} rows"
    for row, line in zip(ROWS, body, strict=True):
        if row is None:
            assert line.strip("| ") == "", f"a None row rendered as {line!r}"
            continue
        label, value = row
        assert label in line and value in line, f"{row} rendered as {line!r}"
    width = {len(line) for line in panel}
    assert len(width) == 1, f"the panel's lines are not one width: {sorted(width)}"


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
        (Stream("utf-8", tty=False), "a pipe — an agent's report carries the twin"),
        (io.StringIO(), "a stream with no encoding and no terminal"),
    ],
)
def test_pick_shape_is_letters_off_a_utf8_terminal(stream, why):
    """S5 and `spec.md` §Out — *the sealer's returned text carries the ASCII
    twin; the colour form is for a person's terminal*. Blocks and colour are
    for a UTF-8 tty and nothing else."""
    assert module().pick_shape(stream) is True, why


def test_pick_shape_is_blocks_on_a_utf8_terminal():
    """The control: the one stream that gets the drawing."""
    assert module().pick_shape(Stream("UTF-8", tty=True)) is False


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
