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
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
WRAPPER = os.path.join(ROOT, "bin", "seal-stamp")
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
GATE_WRAPPER = os.path.join(ROOT, "bin", "broad-gate")
GENERATOR = os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py")
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")

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


def test_a_scale_that_is_not_a_number_is_refused_before_anything_runs():
    """A round 1 record correction. `check_scale` compared with `<` and `>`,
    and NaN compares False with both — so `--scale nan` passed the band, every
    check ran, the cell was written, and `stamp` then raised `ValueError:
    cannot convert float NaN to integer`. `broad_gate.main` catches `Refused`
    alone, so that arrived as a traceback after the write."""
    mod = module()
    assert mod.check_scale(float("nan")) is not None, (
        "a scale that is not a number passes the band and fails after the "
        "cell is written"
    )
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
    text = "# Repository config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n"
    if row:
        # The suite runner first, so the base comparison can re-run it on
        # the failing files alone. `-p no:cacheprovider` keeps pytest from
        # writing `.pytest_cache` into a tree the gate later diffs.
        runner = f"{sys.executable} -m pytest -q -p no:cacheprovider tests"
        text += f"| {ROW} | {runner} |\n"
    return text


def env_without_a_pull_request():
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
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


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    return build_repo(tmp_path_factory.mktemp("gate-template") / "repo")


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def run_gate(repo, *extra, keep=None, wrapper=False):
    """`broad_gate.py --base base --root <repo> --shape`, its outputs kept
    under `keep`; returns the completed process."""
    keep = keep or repo.parent / "out"
    command = [GATE_WRAPPER] if wrapper else [sys.executable, GATE]
    return subprocess.run(
        [
            *command,
            "--base",
            "base",
            "--root",
            str(repo),
            "--shape",
            "--keep-output",
            str(keep),
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        env=env_without_a_pull_request(),
    )


def short(repo, ref):
    return git(repo, "rev-parse", "--short", ref).stdout.strip()


def crown_of():
    """The first non-blank line of the letter twin — present in a stamp and
    in nothing else the gate prints."""
    twin = module().stamp(ROWS, shape=True)
    return next(line.strip() for line in twin if line.strip())


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


# --- S1 sealed ---------------------------------------------------------------


def test_a_green_tree_is_sealed_with_every_check_run_in_order(repo, tmp_path):
    """S1. Every check runs, its exit code is read off the process and kept
    with its output, and the stamp prints with the panel: tree, base, the
    suite's counts, the row's exit code, ledger, chain. No `rounds` row
    without `--record`. The `row` label replaced a literal `lint  clean` in
    round 1's 🟡 3 — the gate cannot tell which part of a shell line is a
    linter, so it reports what it measured."""
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "SEALED" in out.stdout and "NOT SEALED" not in out.stdout
    assert crown_of() in out.stdout, "the disc is missing from a sealed run"
    for label, value in (
        ("tree", short(repo, "HEAD")),
        ("base", short(repo, "base")),
        ("suite", "1 passed"),
        ("row", "exit 0"),
        ("ledger", "0 broken"),
        ("chain", "exit 0"),
    ):
        assert re.search(rf"\b{label}\s+[^\n|]*{re.escape(value)}", out.stdout), (
            f"the panel does not carry `{label} {value}`:\n{out.stdout}"
        )
    assert not re.search(r"\brounds\b", out.stdout), "a rounds row without --record"
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


@pytest.mark.skipif(os.name == "nt", reason="the POSIX wrapper needs a POSIX shell")
def test_the_wrapper_runs_the_same_gate(repo):
    """`bin/broad-gate` resolves the script relative to itself and passes
    every argument through; the wrapper pair is pinned by the bin twin
    case."""
    out = run_gate(repo, wrapper=True)
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert "SEALED" in out.stdout


# --- S2 not sealed -----------------------------------------------------------


def test_a_failing_test_is_not_sealed_and_is_new_when_the_base_passes(repo):
    """S2. One planted failure: `NOT SEALED <tree> against <base>`, the
    failing check named with its first lines, the failing file labelled
    `new` because the base does not fail it, no disc, exit 1. The scratch
    worktree the comparison used is gone afterwards."""
    write(repo, "tests/test_two.py", FAILING_TEST)
    commit(repo, "plant a failure")
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    first = out.stdout.strip().splitlines()[0]
    assert first.startswith("NOT SEALED"), first
    assert short(repo, "HEAD") in first and short(repo, "base") in first, first
    assert crown_of() not in out.stdout, "the failure form drew the disc"
    assert not any(c in out.stdout for c in HALF_BLOCKS)
    assert re.search(r"^\s+suite\s", out.stdout, re.M), "the failing check is unnamed"
    gate = gate_module()
    assert re.search(rf"tests/test_two\.py\s+{gate.NEW}\b", out.stdout), (
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
    assert re.search(rf"tests/test_two\.py\s+{gate.ON_BASE}", out.stdout), (
        f"the failing file is not labelled `{gate.ON_BASE}`:\n{out.stdout}"
    )
    assert not re.search(rf"tests/test_two\.py\s+{gate.NEW}\b", out.stdout)
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


def test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict(tmp_path):
    """Round 1's 🟡 4. `compare_at_base` claims its verdicts are measured and
    never inferred, and one absent file turned every one of them into a guess.

    pytest handed a path that does not exist exits 4 with `no tests ran` and
    prints no `FAILED` line at all, so a single run over every failing file
    loses the measurement for ALL of them and each comes back `new`. This
    branch is exactly that shape: it adds a test module the base does not
    carry.

    Here the base already fails `tests/test_two.py`, and the branch adds
    `tests/test_three.py` failing too. The base-carried one has to keep
    `failing on base too`, which is what a reader acts on at
    `agents/smith.md`'s three-returns rule."""
    repo = build_repo(tmp_path / "repo", base_failing=True)
    write(repo, "tests/test_three.py", FAILING_TEST.replace("test_two", "test_three"))
    commit(repo, "a failing file the base does not carry")
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert re.search(rf"tests/test_two\.py\s+{gate.ON_BASE}", out.stdout), (
        "one absent file cost the base-carried file its measured verdict:\n"
        f"{out.stdout}"
    )
    assert re.search(rf"tests/test_three\.py\s+{gate.NEW}\b", out.stdout), out.stdout
    assert len(git(repo, "worktree", "list").stdout.strip().splitlines()) == 1


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


# --- S4 one write: the fixture item --------------------------------------------


def declaration():
    return (
        f"# {os.path.basename(ITEM)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
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


def test_the_refusal_names_the_three_values_the_row_holds(repo):
    """The other side of 🟡 12: what the person who hits it is told.

    The refusal is the one place a reader learns the row's vocabulary, and
    the value that tripped it is by definition outside that vocabulary — so
    naming the three is the difference between a refusal somebody can act on
    and one they work around by guessing.

    **`round-N` is permitted here and cannot be reached on a LAST record**,
    and that is deliberate rather than an oversight nothing catches. A named
    checker must be a round LATER than the record carrying it, and `seal`
    reads the highest-numbered record on disk, so no case can build a last
    record whose cell legitimately names one. Refusing everything but `no
    fixes to check` would be equivalent today and would hard-code a
    conclusion that belongs to `chain_check.checked_by` — which confirms a
    named checker against the repository — into a subcommand that has no
    business deriving it."""
    path = fixed_but_unread_item(repo)
    set_checked_by(path, "pending")
    _code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    for value in ("round-N", "no fixes to check", "nobody"):
        assert value in out, f"the refusal does not name `{value}`:\n{out}"


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


def test_the_gate_with_record_seals_the_item_and_counts_its_rounds(repo, tmp_path):
    """S1 with `--record`: the checks pass, `seal` writes the last record's
    cell with the tree and the base, and the panel carries `rounds 2`."""
    _one, two = settled_item(repo)
    out = run_gate(repo, "--record", str(repo / ITEM), keep=tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert re.search(r"\brounds\s+2\b", out.stdout), out.stdout
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == f"{short(repo, 'HEAD')} against base", cell


def test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter(repo, tmp_path):
    """Round 1's 🟡 3. The panel carried `lint  clean` as a literal, beside
    four rows read from what the checks printed.

    The `Broad gate` row is one shell command line and nothing in it says
    which part is a linter — `templates/config.md` says so itself, which is
    why the base comparison re-runs whatever stands before the first `&&`
    rather than a linter it identified. A repository whose row is only a test
    runner got a seal asserting a check that never ran, on the artifact a
    reader trusts BECAUSE it is drawn on success alone.

    The fixture's row is a bare pytest call, with no linter in it at all."""
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 0, f"{out.stdout}\n{out.stderr}"
    assert re.search(r"\brow\s+exit 0\b", out.stdout), out.stdout
    assert "clean" not in out.stdout, (
        "the seal still asserts a linter over a row that has none in it"
    )


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
    code = mod.gate(
        argparse.Namespace(
            root=str(repo),
            base="base",
            record=str(repo / ITEM),
            shape=True,
            scale=1.0,
            keep_output=str(tmp_path / "out"),
        ),
        False,
    )
    out = capsys.readouterr()
    assert reached, f"the checks failed before `seal` was reached\n{out.out}{out.err}"
    assert code == 2, f"exit {code}\n{out.out}{out.err}"
    assert crown_of() not in out.out, "a stamp printed over a failing chain check"
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
    out = run_gate(repo, "--record", str(repo / ITEM), keep=tmp_path / "out")
    assert out.returncode == 2, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert crown_of() not in out.stdout, "a stamp printed over a refused record"
    assert "`Pass` is unchecked" in out.stdout + out.stderr
    # The other half of round 2's 🟡 11, and the one that makes the
    # discriminator worth having: this is the refusal side, so the gate has
    # to say the opposite. A discriminator that read the bare
    # `round-record:` prefix would tell a reader here that the cell was
    # written, which is the mutation this pair exists to kill.
    assert "no cell was written" in out.stdout + out.stderr, out.stderr
    assert "the cell WAS written" not in out.stdout + out.stderr, out.stderr
    assert read_bytes(path) == before


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


def test_the_sealer_names_its_one_write_as_its_own_exception():
    """§6's last paragraph prescribes the shape: an exception is one agent's,
    and it is named in that agent's definition. A write nobody named is a
    review that certifies itself."""
    text = " ".join(sealer_text().split())
    assert "§6" in text, "the sealer cannot reach the rule its one write excepts"
    assert "round_record.py seal" in text, (
        "the sealer's one write does not name the subcommand that makes it, "
        "so the write is described rather than bounded"
    )
    assert "`Broad gate`" in text, (
        "the exception does not say WHICH cell, and an exception without a "
        "boundary is a general permission"
    )


def test_the_sealer_states_the_contradiction_and_the_ticket_that_settles_it():
    """Q4: the sealer ships under a contract that forbids its one act, for a
    window inside one release branch. A window nobody wrote down is a
    contradiction the next reader resolves by guessing which document wins."""
    text = " ".join(sealer_text().split())
    assert "§2" in text, "the definition does not name the section it stands against"
    assert "#120" in text, (
        "the definition does not name the ticket that rewrites §2, so the "
        "contradiction has no end written into it"
    )
    assert "narrower document" in text, (
        "the definition does not say which of the two wins in the window, "
        "which is the one thing a reader in that window needs"
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
