"""`mutation-check`: one mutation of one unit, with the loop's housekeeping
derived from the file it mutated.

#641, with #129 as its twin. `agents/smith.md` told the implementer to "clear
`tests/__pycache__` between mutations", which is wrong twice over. It clears
the importers, whose bytecode is valid and unchanged, so every test module is
recompiled on every mutated run. And it misses the one cache that can be
stale -- the one beside the MUTATED file, wherever that file lives
(`.github/scripts/__pycache__` in #129, `skills/verify/scripts/__pycache__`
in #326). Nothing bounded a mutated run either, and one hung for 32 minutes
(#577).

So the command derives the cache from the file, for every interpreter tag;
runs the cases with `PYTHONDONTWRITEBYTECODE=1` under a bound; restores from
bytes it held and compares the hash; and prints one verdict whose exit code
says which of three things happened.

**How the script is loaded here.** By path, with an `importlib` spec,
registered in `sys.modules` before it executes -- the way
`tests/test_arm_check.py` loads `arm_check.py`. The script reaches
`arm_check.py` the same way rather than through `sys.path`, so nothing has to
be put on the path first: a bare `from arm_check import ...` resolves only
when the script is run by its path and `PYTHONSAFEPATH` is unset.

**Every fixture lives under `tmp_path`.** Nothing is planted in the
repository's own `__pycache__` directories, and every process a case starts
is reaped or proven dead before the case returns.
"""

import importlib.util
import os
import shlex
import sys
import textwrap

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "mutation_check.py")
WRAPPER = os.path.join(ROOT, "bin", "mutation-check")


def module():
    """The command, loaded from its path and registered first.

    Missing, this raises -- which is how every case below was seen red before
    the script existed (§15)."""
    spec = importlib.util.spec_from_file_location("specseal_mutation_check", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def run(argv, capsys):
    """`main(argv)` in-process: the exit code and everything it printed."""
    code = module().main([str(a) for a in argv])
    out = capsys.readouterr()
    return code, out.out + out.err


def probe(tmp_path, body, name="probe.py"):
    """A stand-in for the cases: a script that reports what it SAW."""
    path = tmp_path / name
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return path


def cases_command(*argv):
    return shlex.join([sys.executable, *[str(a) for a in argv]])


def snapshot(directory):
    """Every file under `directory`, with its bytes."""
    found = {}
    for here, _dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(here, name)
            with open(path, "rb") as f:
                found[os.path.relpath(path, directory)] = f.read()
    return found


PASSES = "import sys\nsys.exit(0)\n"
FAILS = "import sys\nsys.exit(1)\n"

# Reports the bytes of the file it is handed, so a case can see what the
# cases saw at the moment they ran.
SEES_FILE = """\
import sys
with open(sys.argv[1], encoding="utf-8") as f:
    seen = f.read()
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write(seen)
"""


# --- S3 · a replacement lands exactly once, or nothing is written -----------


@pytest.mark.parametrize(
    ("source", "count"),
    [("VALUE = 1\n", 0), ("OLD = 1\nOLD = 2\n", 2)],
    ids=["absent", "twice"],
)
def test_a_replacement_that_cannot_land_once_is_refused_before_any_write(
    tmp_path, capsys, source, count
):
    """§9: an edit must be able to fail. A pattern that misses writes
    nothing and exits zero when the shell does it, so the loop records a
    verdict for a mutation that never happened -- the two-spaces incident
    `arm_check.run_arms`'s docstring records. One that lands twice breaks two
    units at once, and the verdict cannot say which one a case caught."""
    target = tmp_path / "target.py"
    target.write_text(source, encoding="utf-8")
    log = tmp_path / "ran.txt"
    before = snapshot(tmp_path)

    code, out = run(
        [
            target,
            "--replace",
            "OLD",
            "NEW",
            "--tests",
            cases_command(probe(tmp_path, SEES_FILE), target, log),
        ],
        capsys,
    )
    # The probe was written after the snapshot; take it out before comparing.
    after = snapshot(tmp_path)
    after.pop("probe.py")

    assert code == 2, out
    assert out.startswith("refused"), out
    assert f"{count} times" in out, f"the refusal does not name the count: {out}"
    assert after == before, "a refused replacement wrote something"
    assert not log.exists(), "a refused replacement still ran the cases"


def test_a_replacement_that_lands_once_is_what_the_cases_see(tmp_path, capsys):
    target = tmp_path / "target.py"
    target.write_text("VALUE = 15\n", encoding="utf-8")
    log = tmp_path / "seen.txt"

    run(
        [
            target,
            "--replace",
            "VALUE = 15",
            "VALUE = 25",
            "--tests",
            cases_command(probe(tmp_path, SEES_FILE), target, log),
        ],
        capsys,
    )
    assert log.read_text(encoding="utf-8") == "VALUE = 25\n"
    assert target.read_text(encoding="utf-8") == "VALUE = 15\n"


@pytest.mark.parametrize(
    ("old", "new", "says"),
    [("", "x", "empty"), ("VALUE", "VALUE", "identical")],
    ids=["empty-old", "no-change"],
)
def test_a_replacement_that_mutates_nothing_is_refused(
    tmp_path, capsys, old, new, says
):
    """A mutation that changes no byte would read SURVIVED every time -- a
    verdict about the unmutated file, reported as a verdict about a unit."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    code, out = run(
        [
            target,
            "--replace",
            old,
            new,
            "--tests",
            cases_command(probe(tmp_path, PASSES)),
        ],
        capsys,
    )
    assert code == 2, out
    assert out.startswith("refused") and says in out, out


# --- S4 · restored from held bytes, and the restore is proved ---------------


REWRITES = """\
import sys
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("something the cases wrote\\n")
"""


def test_the_file_is_restored_from_the_bytes_held_before_the_write(tmp_path, capsys):
    """Not from `HEAD`: `git checkout -- <file>` takes every uncommitted fix in
    the file with it, which is the round's work `agents/smith.md`'s
    Boundaries says was wiped once. The cases here rewrite the file, so the
    restore has something to undo besides the mutation."""
    target = tmp_path / "target.py"
    original = b"VALUE = 15\r\n# a CRLF and a byte the codec must keep: \xc3\xa9\n"
    target.write_bytes(original)

    run(
        [
            target,
            "--replace",
            "VALUE = 15",
            "VALUE = 25",
            "--tests",
            cases_command(probe(tmp_path, REWRITES), target),
        ],
        capsys,
    )
    assert target.read_bytes() == original


def test_a_restore_that_did_not_land_stops_the_run_and_says_so(
    tmp_path, capsys, monkeypatch
):
    """Every verdict taken against a file still holding its mutation is a
    verdict about the mutant. The command says so instead of printing one."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 15\n", encoding="utf-8")
    mc = module()

    def refuses(path, original, original_sha):
        raise RuntimeError(f"{path} was not restored: deadbeef != {original_sha}")

    monkeypatch.setattr(mc, "restore", refuses)
    code = mc.main(
        [
            str(target),
            "--replace",
            "VALUE = 15",
            "VALUE = 25",
            "--tests",
            cases_command(probe(tmp_path, FAILS)),
        ]
    )
    out = capsys.readouterr()
    text = out.out + out.err
    assert code == 2, text
    assert "was not restored" in text, text
    assert not text.startswith("red"), (
        f"a verdict was printed over a file that still holds the mutation: {text}"
    )


# --- S7 · the verdict and the exit code say which of three things happened --


def test_cases_that_fail_against_the_mutant_read_red_and_exit_zero(tmp_path, capsys):
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    code, out = run(
        [
            target,
            "--replace",
            "1",
            "2",
            "--tests",
            cases_command(probe(tmp_path, "print('the case output')\n" + FAILS)),
        ],
        capsys,
    )
    assert code == 0, out
    assert out.startswith("red"), out
    assert "the case output" in out, "the command's own output is not shown"


def test_cases_that_pass_against_the_mutant_read_survived_and_exit_one(
    tmp_path, capsys
):
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    code, out = run(
        [
            target,
            "--replace",
            "1",
            "2",
            "--tests",
            cases_command(probe(tmp_path, PASSES)),
        ],
        capsys,
    )
    assert code == 1, out
    assert out.startswith("SURVIVED"), out


def test_a_command_that_cannot_start_measures_nothing_and_exits_two(tmp_path, capsys):
    """Not SURVIVED: nothing ran, so nothing was watched or not watched."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    missing = tmp_path / "no-such-runner"
    code, out = run(
        [target, "--replace", "1", "2", "--tests", shlex.join([str(missing), "-q"])],
        capsys,
    )
    assert code == 2, out
    assert out.startswith("could not start"), out
    assert str(missing) in out, f"the error is not named: {out}"
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"


def test_a_negative_bound_is_refused_rather_than_timing_every_run_out(tmp_path, capsys):
    """`arm-check` refuses it for the same reason: a bound below zero ends
    every run before it starts, and a verdict nobody measured follows."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    with pytest.raises(SystemExit) as raised:
        module().main(
            [
                str(target),
                "--replace",
                "1",
                "2",
                "--tests",
                cases_command(probe(tmp_path, FAILS)),
                "--timeout",
                "-1",
            ]
        )
    assert raised.value.code == 2
    assert "non-negative" in capsys.readouterr().err
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"


# --- S8 · a file that is not Python is mutated the same way -----------------


def test_a_markdown_file_is_mutated_and_restored_the_same_way(tmp_path, capsys):
    """The smith's unit is often a sentence: `agents/*.md` and `skills/*.md`
    are what a session reads and acts on, and §14 pins them by case."""
    target = tmp_path / "notes.md"
    text = "# Notes\n\nThe sentence a case pins. Another one stays.\n"
    target.write_text(text, encoding="utf-8")
    log = tmp_path / "seen.txt"

    code, out = run(
        [
            target,
            "--replace",
            "The sentence a case pins. ",
            "",
            "--tests",
            cases_command(probe(tmp_path, SEES_FILE), target, log),
        ],
        capsys,
    )
    assert log.read_text(encoding="utf-8") == "# Notes\n\nAnother one stays.\n"
    assert target.read_text(encoding="utf-8") == text
    assert code == 1 and out.startswith("SURVIVED"), out
    assert not (tmp_path / "__pycache__").exists()
