"""The sealer's stamp reaches the person it is drawn for (#400).

Work item 1790562543. A sealer's stdout is a pipe into a report that arrives
folded behind `ctrl+o`, so a stamp drawn there was never seen. The gate now
draws only on a terminal; a recorded seal on a pipe writes its panel to a
values file under the git common dir, and a `Stop` hook in the session that
spawned the sealer draws each undrawn file once, after that turn's text.

This module holds the stamp's half — the values file, `seal-stamp --from`,
the default scale. The gate's half is in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside the fixtures
that drive a real gate over a settled work item.
"""

import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAMP = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")

# A panel in the shape `broad_gate.panel` returns. Neutral values.
ROWS = [
    ("SEALED", ""),
    None,
    ("tree", "aaa1111"),
    ("base", "bbb2222"),
    ("from", "origin/base"),
    ("gate", "plugin 0.0.0"),
    None,
    ("suite", "3 passed"),
    ("row", "exit 0"),
    ("ledger", "4 ok . 0 broken"),
    ("chain", "exit 0"),
    None,
    ("rounds", "2"),
]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def stamp_module():
    return _load("specseal_seal_stamp_for_its_values", STAMP)


def values(scale=0.9, item="/x/seal/specs/1799000000-an-item", rows=ROWS):
    return {
        "tree": "aaa1111",
        "base": "bbb2222",
        "from": "origin/base",
        "item": item,
        "session": "s-1",
        "scale": scale,
        "rows": rows,
    }


def seal_stamp(*args):
    """`seal_stamp.py` as a person types it, stdout a pipe."""
    return subprocess.run(
        [sys.executable, STAMP, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )


# --- S11: a values file drawn by hand, once --------------------------------


def test_a_values_file_is_drawn_by_hand_once_and_then_refused(tmp_path):
    """S11. `seal-stamp --from <file>` draws that run's rows — not the
    sample — at the file's own scale, and marks the file drawn. The same
    command again refuses with one sentence and exit 2, because a sealed
    run's values are drawn once whoever draws them."""
    mod = stamp_module()
    path = mod.write_values(str(tmp_path), "s-1", values())
    out = seal_stamp("--from", path)
    assert out.returncode == 0, out.stderr
    assert out.stdout == "\n" + "\n".join(mod.stamp(ROWS, 0.9, shape=True)) + "\n\n"
    assert "aaa1111" in out.stdout and "c46fd2d" not in out.stdout, (
        "the drawing is the sample's, not the run's"
    )
    assert not os.path.exists(path), "the file was drawn and not marked drawn"
    assert os.path.exists(mod.drawn_path(path)), "the drawn file's values are gone"

    again = seal_stamp("--from", path)
    assert again.returncode == 2, again.stdout + again.stderr
    assert again.stdout == "", f"something was drawn a second time:\n{again.stdout}"
    refusal = again.stderr.strip()
    assert "was drawn already" in refusal and "\n" not in refusal, refusal
    assert seal_stamp("--from", mod.drawn_path(path)).returncode == 2, (
        "the drawn file itself can be drawn again by naming it"
    )


def test_a_file_that_is_not_a_run_is_refused_and_left_for_a_repair(tmp_path):
    """A values file that is not in the gate's shape is refused before it is
    claimed, so it is still there to be drawn once somebody repairs it — and
    one refused for a scale under the floor is refused by the function that
    draws, which checks the band itself."""
    for broken, said in (
        ("not json", "it is not JSON"),
        (json.dumps({**values(), "rows": "SEALED"}), "`rows` is not a list"),
        (json.dumps(values(scale=0.5)), "under the floor"),
    ):
        path = tmp_path / "1-aaa1111.json"
        path.write_text(broken, encoding="utf-8")
        out = seal_stamp("--from", str(path))
        assert out.returncode == 2, (broken, out.stdout, out.stderr)
        assert said in out.stderr, out.stderr
        assert out.stdout == "", out.stdout
        assert path.exists(), f"a refused file was claimed: {broken!r}"


def test_pending_lists_the_undrawn_oldest_first_and_claim_takes_one_once(tmp_path):
    """The reader the hook uses. `pending` lists undrawn files oldest first
    and skips drawn ones and the writer's hidden temporary; `claim` renames a
    file to its drawn name and answers None to the second caller, which is
    what keeps two drawers racing for one file to one drawing."""
    mod = stamp_module()
    older = mod.write_values(str(tmp_path), "s-1", values(), now=1)
    newer = mod.write_values(str(tmp_path), "s-1", values(), now=2)
    directory = mod.values_dir(str(tmp_path), "s-1")
    open(os.path.join(directory, ".3-aaa1111.tmp"), "w").close()
    assert mod.pending(directory) == [older, newer]
    assert mod.claim(older) == mod.drawn_path(older)
    assert mod.claim(older) is None, "a claimed file was claimed a second time"
    assert mod.pending(directory) == [newer]
    assert mod.pending(str(tmp_path / "nowhere")) == []


def test_a_session_id_cannot_name_a_directory_outside_the_values_dir(tmp_path):
    """The session id names a directory, so a separator in a malformed one
    must not become a path escape, and an absent one lands under `none/`."""
    mod = stamp_module()
    assert mod.session_key("../../elsewhere") == "elsewhere"
    for absent in (None, "", "  ", ".", ".."):
        assert mod.session_key(absent) == mod.NO_SESSION, absent
    path = mod.write_values(str(tmp_path), "../../elsewhere", values())
    assert os.path.dirname(path) == os.path.join(
        str(tmp_path), mod.VALUES_DIR, "elsewhere"
    ), path


# --- S16: the sealer is told it draws nothing --------------------------------


def flat(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


def test_the_sealer_is_told_the_gate_draws_nothing_and_neither_does_it():
    """S16, the sealer's half (contract §14). `agents/sealer.md` said the
    drawing arrives as letters and to pass it through, which the 0.15.6 run
    did — every seal behind `ctrl+o`. It now says the gate draws nothing in a
    sealer, that the session which spawned it has the stamp drawn, that the
    sealer draws none by either route, and that the exit-0 outcome is the
    `SEALED` line; and the old instruction is gone."""
    text = flat("agents", "sealer.md")
    for said in (
        "**The gate draws nothing in a sealer, and neither do you**",
        "A hook in the session that spawned you draws that file once",
        "Do not draw it yourself, neither with `seal-stamp` nor from the file",
        "The gate printed one line beginning `SEALED`",
    ):
        assert said in text, said
    assert "the drawing arrives as letters" not in text
    assert "pass it through as it came" not in text


# --- S13: the scale --------------------------------------------------------


def test_the_default_scale_is_ninety_percent_with_its_reason_beside_it():
    """S13. `DEFAULT_SCALE` is 0.90, and the comment above it says why and
    names 0.75 as the candidate passed over, so the next reader does not
    re-run #400's six-scale comparison to find out."""
    mod = stamp_module()
    assert mod.DEFAULT_SCALE == 0.90
    with open(STAMP, encoding="utf-8") as handle:
        source = handle.read()
    above = source.split("DEFAULT_SCALE = 0.90", 1)[0].rsplit("\n\n", 1)[-1]
    assert "0.75 was the other candidate" in above, above
    assert "passed over" in above, above


def test_both_commands_draw_at_the_default_scale_when_given_none():
    """S13's other half: `seal-stamp` with no `--scale` draws the sample at
    `DEFAULT_SCALE`, and `broad-gate`'s own default is the same constant —
    the gate's values file carries it, which the gate module's cases read."""
    mod = stamp_module()
    out = seal_stamp("--shape")
    assert out.returncode == 0, out.stderr
    assert out.stdout == (
        "\n" + "\n".join(mod.stamp(mod.SAMPLE_ROWS, mod.DEFAULT_SCALE, True)) + "\n\n"
    )
    help_text = subprocess.run(
        [sys.executable, GATE, "--help"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    ).stdout
    assert f"default {mod.DEFAULT_SCALE}" in help_text, help_text
