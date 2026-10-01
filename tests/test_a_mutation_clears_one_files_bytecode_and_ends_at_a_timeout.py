"""`mutation-check`: one mutation of one unit, with the loop's housekeeping
derived from the file it mutated.

#641, with #129 as its twin. `agents/smith.md` told the implementer to "clear
`tests/__pycache__` between mutations", which aims at the wrong cache. It
clears the importers, whose bytecode is valid and unchanged, and it misses
the one cache that can be stale -- the one beside the MUTATED file, wherever
that file lives
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
import py_compile
import re
import shlex
import subprocess
import sys
import textwrap
import time

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

# Fails only while the file it is handed carries the text it is handed, so
# the run against the file as it is passes and the run against the mutant is
# red -- the one shape a red means anything in (round 1, 🔴 1).
FAILS_ON_THE_MUTANT = """\
import sys
with open(sys.argv[1], encoding="utf-8") as f:
    sys.exit(1 if sys.argv[2] in f.read() else 0)
"""


def red_on(tmp_path, target, marker, name="red_on.py"):
    """The cases command that is red only against the mutant holding `marker`."""
    return cases_command(probe(tmp_path, FAILS_ON_THE_MUTANT, name), target, marker)


# Reports the bytes of the file it is handed, so a case can see what the
# cases saw at the moment they ran.
SEES_FILE = """\
import sys
with open(sys.argv[1], encoding="utf-8") as f:
    seen = f.read()
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write(seen)
"""


# --- S1 · the mutated file's bytecode is gone for every tag -----------------


def plant_import_cache(path):
    """A cache entry for `path`, the timestamp-checked kind an import writes.

    Written by `py_compile` rather than by importing, because an import
    honours `PYTHONDONTWRITEBYTECODE` -- and this module is itself run under
    `mutation-check`, which sets it, whenever a unit of the command is
    mutated. Planted by import, the cache is never written there and the case
    goes red on its own precondition whatever the mutation was: measured
    while mutating this module's script, 2026-10-01."""
    py_compile.compile(
        str(path), cfile=importlib.util.cache_from_source(str(path)), doraise=True
    )
    cached = list((path.parent / "__pycache__").glob(f"{path.stem}.*.pyc"))
    assert cached, "this case needs a real .pyc to remove; the interpreter wrote none"
    return cached


# Reports what it SAW rather than passing or failing: whether any cached
# bytecode for the module existed at the moment the cases ran, and whether the
# run was told to write none.
SEES_CACHE = """\
import glob, os, sys
module, log = sys.argv[1], sys.argv[2]
stem = os.path.splitext(os.path.basename(module))[0]
cache = os.path.join(os.path.dirname(module), "__pycache__")
found = sorted(os.path.basename(p) for p in glob.glob(os.path.join(cache, stem + ".*.pyc")))
with open(log, "a", encoding="utf-8") as f:
    f.write(repr((found, os.environ.get("PYTHONDONTWRITEBYTECODE"))) + "\\n")
"""


def seen_runs(log):
    """One `(caches found, the variable)` per run the command made."""
    return [eval(line) for line in log.read_text(encoding="utf-8").splitlines()]


def test_no_bytecode_for_the_mutated_file_exists_while_the_cases_run(
    tmp_path, capsys, monkeypatch
):
    """The mechanism, watched by what the subprocess can see.

    Two tags are planted, because two coexist beside one source on the
    machine this was built on: `python3` is 3.14 and `bin/test`'s virtualenv
    is 3.13. `importlib.util.cache_from_source` names the CALLING
    interpreter's file only, so a removal spelled that way leaves the other
    tag for the cases' interpreter to read. The foreign tag here is written by
    hand, since no second interpreter is guaranteed on a CI runner.

    Reproducing a stale read by timing is not attempted -- whether two writes
    land in one mtime second is the machine's, not the case's, which is what
    `tests/test_arm_check.py` measured and says. S2 below makes the stale
    read deterministic instead.

    The variable is taken out of this process's environment first, so the
    flag the cases report is the one the command set and not one inherited
    from whatever ran this suite."""
    monkeypatch.delenv("PYTHONDONTWRITEBYTECODE", raising=False)
    target = tmp_path / "under_test.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    plant_import_cache(target)
    foreign = tmp_path / "__pycache__" / "under_test.cpython-399.pyc"
    foreign.write_bytes(b"not bytecode any interpreter here reads")
    log = tmp_path / "seen.txt"

    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, SEES_CACHE), target, log),
        ],
        capsys,
    )
    # Every run the command made: the baseline against the file as it is, and
    # the run against the mutant.
    for found, flag in seen_runs(log):
        assert found == [], (
            f"{found} -- cached bytecode for the mutated file existed while the "
            f"cases ran, so the interpreter can run a previous mutation instead of "
            f"this one. A tag left behind is the one `cache_from_source` does not name"
        )
        assert flag == "1", "the cases were not told to write no bytecode"
    assert not list((tmp_path / "__pycache__").glob("under_test.*.pyc"))
    assert code == 1, out


# Imports the mutated module with bytecode writing switched back ON, the way
# a `--tests` command that builds its own environment would.
WRITES_CACHE = """\
import importlib.util, sys
sys.dont_write_bytecode = False
spec = importlib.util.spec_from_file_location("mutant", sys.argv[1])
spec.loader.exec_module(importlib.util.module_from_spec(spec))
"""


def test_bytecode_the_baseline_wrote_is_gone_before_the_mutated_run(tmp_path, capsys):
    """The baseline runs the cases against the original, and a command that
    builds its own environment writes the original's `.pyc` while it does. A
    same-length break written inside the same second matches that cache, so
    the mutated run would read the original. So the removal happens again
    between the write and the mutated run, and the mutated run sees none."""
    target = tmp_path / "under_test.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    log = tmp_path / "seen.txt"
    run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            # Look first, then write: so each line says what the run before
            # this one left behind.
            cases_command(probe(tmp_path, SEES_CACHE + WRITES_CACHE), target, log),
        ],
        capsys,
    )
    runs = seen_runs(log)
    assert len(runs) == 2, f"the command ran the cases {len(runs)} times, not twice"
    assert runs[1][0] == [], (
        f"{runs[1][0]} -- the baseline's bytecode for the original was still "
        f"there when the mutated run started"
    )


def test_bytecode_the_cases_wrote_for_the_mutant_is_not_left_behind(tmp_path, capsys):
    """The second removal, after the restore. The environment variable stops
    a run that honours it; a command that builds its own environment does
    not, and the mutant's `.pyc` it leaves is the same size as the next
    same-length mutation's source."""
    target = tmp_path / "under_test.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")

    run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, WRITES_CACHE), target),
        ],
        capsys,
    )
    left = list((tmp_path / "__pycache__").glob("under_test.*.pyc"))
    assert left == [], f"{left} -- the run left the mutant's bytecode behind"


# --- S2 · the same-length mutation reads red --------------------------------


# Passes while the module it loads still says 15.
ASSERTS_FIFTEEN = """\
import importlib.util, sys
spec = importlib.util.spec_from_file_location("under_test", sys.argv[1])
loaded = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loaded)
sys.exit(0 if loaded.VALUE == 15 else 1)
"""


def test_a_same_length_mutation_reads_red_over_a_trusted_cache(tmp_path, capsys):
    """#641's *what must not break*, and the smith's loop in miniature:
    `WINDOW = 15` to `25` read green once, because the interpreter ran the
    cached original.

    The cache planted here is an unchecked-hash `.pyc`, which CPython trusts
    without consulting the source at all. That makes the stale read the
    timestamp cache produces only inside one mtime second happen on every
    run, so this case is red whenever the removal is missing rather than
    whenever the machine is fast."""
    target = tmp_path / "under_test.py"
    target.write_text("VALUE = 15\n", encoding="utf-8")
    py_compile.compile(
        str(target),
        cfile=importlib.util.cache_from_source(str(target)),
        invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH,
        doraise=True,
    )

    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 15",
            "VALUE = 25",
            "--tests",
            cases_command(probe(tmp_path, ASSERTS_FIFTEEN), target),
        ],
        capsys,
    )
    assert code == 0 and out.startswith("red"), (
        f"the cases ran the cached original rather than the mutation: {out}"
    )


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


def test_a_file_that_is_not_utf8_text_is_refused_untouched(tmp_path, capsys):
    """The replacement is literal text, so a file that does not decode has no
    text to find it in. Re-encoded leniently it would come back different
    from the bytes it was read as, and the restore would be the mutation."""
    target = tmp_path / "blob.bin"
    original = b"OLD \xff\xfe not text\n"
    target.write_bytes(original)
    code, out = run(
        [
            target,
            "--replace",
            "OLD",
            "NEW",
            "--tests",
            cases_command(probe(tmp_path, FAILS)),
        ],
        capsys,
    )
    assert code == 2, out
    assert out.startswith("refused") and "UTF-8" in out, out
    assert target.read_bytes() == original


def test_a_tests_command_that_names_nothing_is_refused(tmp_path, capsys):
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    with pytest.raises(SystemExit) as raised:
        module().main([str(target), "--replace", "1", "2", "--tests", "  "])
    assert raised.value.code == 2
    assert "names no command" in capsys.readouterr().err
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"


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
            red_on(tmp_path, target, "VALUE = 25"),
        ]
    )
    out = capsys.readouterr()
    text = out.out + out.err
    assert code == 2, text
    assert "was not restored" in text, text
    # The verdict word itself, not only the phrase the fake's message carries:
    # this is the line that tells a person the file holds a mutant (round 1,
    # 🟡 5).
    assert text.startswith("not restored:"), (
        f"the line that says the file still holds a mutation lost its verdict word: {text}"
    )


# Makes the file it is handed read-only once it holds the mutant, so the
# restore's own write raises rather than its hash differing.
LOCKS_THE_MUTANT = """\
import os, stat, sys
with open(sys.argv[1], encoding="utf-8") as f:
    mutant = sys.argv[2] in f.read()
if mutant:
    os.chmod(sys.argv[1], stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
sys.exit(1 if mutant else 0)
"""


@pytest.mark.skipif(
    os.name != "nt" and os.geteuid() == 0, reason="root writes a read-only file"
)
def test_a_restore_whose_write_raises_is_not_restored_and_exits_two(tmp_path, capsys):
    """Round 1, 🟡 2. A restore can fail by raising as well as by landing the
    wrong bytes: the cases made the file read-only, or removed its directory,
    or a second Ctrl-C arrived inside the write. Each leaves the mutant on
    disk, which is the one outcome `not restored` exists to say."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    try:
        code, out = run(
            [
                target,
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                cases_command(probe(tmp_path, LOCKS_THE_MUTANT), target, "VALUE = 2"),
            ],
            capsys,
        )
    finally:
        os.chmod(target, 0o644)
    assert code == 2, out
    assert out.startswith("not restored:"), out
    assert "PermissionError" in out, f"the cause is not named: {out}"


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
            cases_command(
                probe(tmp_path, "print('the case output')\n" + FAILS_ON_THE_MUTANT),
                target,
                "VALUE = 2",
            ),
        ],
        capsys,
    )
    assert code == 0, out
    assert out.startswith("red"), out
    assert "the case output" in out, "the command's own output is not shown"
    first = out.splitlines()[0]
    assert re.search(r"\(\d+\.\ds\)$", first), (
        f"the verdict line no longer says how long the run took: {first}"
    )


@pytest.mark.parametrize(
    ("exit_code", "why"),
    [
        (1, "a case already failing"),
        (5, "a -k that selects nothing"),
        (4, "a mistyped module"),
    ],
    ids=["failing", "nothing-selected", "usage-error"],
)
def test_cases_that_fail_without_the_mutation_measure_nothing(
    tmp_path, capsys, exit_code, why
):
    """Round 1, 🔴 1: a non-zero exit is red only when the cases passed
    against the file as it was. Otherwise a mistyped `-k` -- pytest's exit 5
    -- reads *a case watches this unit* for a file no case ran against, and
    the smith hands over on it. So the cases run once against the file as it
    is, and a failure there is `no baseline`, exit 2, with nothing written."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    log = tmp_path / "seen.txt"
    body = (
        SEES_FILE.replace('"w", encoding', '"a", encoding') + f"sys.exit({exit_code})\n"
    )
    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, body), target, log),
        ],
        capsys,
    )
    assert code == 2, f"{why}: {out}"
    assert out.startswith("no baseline"), f"{why}: {out}"
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
    assert log.read_text(encoding="utf-8") == "VALUE = 1\n", (
        f"{why}: the cases saw a mutant after failing without one"
    )


@pytest.mark.parametrize("kind", ["missing", "directory"])
def test_a_path_that_cannot_be_read_measures_nothing_and_exits_two(
    tmp_path, capsys, kind
):
    """Round 1, 🟡 3. Left to Python an uncaught exception exits 1, which is
    SURVIVED's code, so a mistyped path read as *nothing watches this unit*."""
    target = tmp_path / ("no-such-file.py" if kind == "missing" else "a-directory")
    if kind == "directory":
        target.mkdir()
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
    assert code == 2, out
    assert out.startswith("could not run:"), out


# Starts a child that keeps the cases' output open, then exits at once:
# red against the mutant, green against the file as it is.
LEAVES_A_CHILD_ON_THE_OUTPUT = """\
import subprocess, sys
with open(sys.argv[1], encoding="utf-8") as f:
    mutant = sys.argv[2] in f.read()
if mutant:
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write(str(child.pid))
sys.exit(1 if mutant else 0)
"""


@pytest.mark.skipif(os.name == "nt", reason="the process-group bound is POSIX's")
def test_cases_that_exit_but_leave_a_child_on_the_output_read_red_at_once(
    tmp_path, capsys
):
    """Round 1, 🟡 4. A wait on the output pipe returns only when every
    holder has closed it, so a run that exited red at once read `timed out`
    after the whole bound -- 300 s per mutation at the default. The wait is on
    the process; and what the cases left behind is ended with them."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    pid_file = tmp_path / "child.pid"
    started = time.monotonic()
    try:
        code, out = run(
            [
                target,
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                cases_command(
                    probe(tmp_path, LEAVES_A_CHILD_ON_THE_OUTPUT),
                    target,
                    "VALUE = 2",
                    pid_file,
                ),
                "--timeout",
                "20",
            ],
            capsys,
        )
        elapsed = time.monotonic() - started
        pid = read_pid(pid_file)
        assert pid is not None, "the cases never started their child"
        assert gone_within(pid, 5), "the run left the child the cases started"
    finally:
        end_if_alive(read_pid(pid_file))
    assert code == 0 and out.startswith("red"), out
    assert elapsed < 10, f"a run that exited at once took {elapsed:.1f}s to read"


# Prints bytes that are not UTF-8, then fails only on the mutant.
PRINTS_NOT_UTF8 = """\
import sys
sys.stdout.buffer.write(b"\\xff\\xfe\\n")
sys.stdout.flush()
with open(sys.argv[1], encoding="utf-8") as f:
    sys.exit(1 if sys.argv[2] in f.read() else 0)
"""


def test_output_that_is_not_utf8_does_not_cost_the_verdict(tmp_path, capsys):
    """Round 1, 🟡 5: the cases' output is shown, not trusted to decode."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, PRINTS_NOT_UTF8), target, "VALUE = 2"),
        ],
        capsys,
    )
    assert code == 0 and out.startswith("red"), out


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
    # It failed in the baseline, so the break was never written, and the
    # verdict says which run it was.
    assert "before the mutation was written" in out, out
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


@pytest.mark.skipif(
    os.name == "nt", reason="the POSIX wrapper; its .cmd twin is read, not run"
)
def test_the_command_a_session_types_reaches_the_script(tmp_path):
    """`bin/mutation-check`, run the way the Bash tool runs it, through the
    shell: the verdict and the exit code arrive unchanged."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    done = subprocess.run(
        [
            WRAPPER,
            str(target),
            "--replace",
            "1",
            "2",
            "--tests",
            red_on(tmp_path, target, "VALUE = 2"),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.startswith("red"), done.stdout + done.stderr
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


# --- S9 · the definition names the command and no directory to clear -------


def flat(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return " ".join(f.read().split())


def test_the_smiths_definition_names_the_command_and_no_directory_to_clear():
    """§14: the sentence the smith acts on changed, so the new text is pinned
    and so is the absence of the old one. *Clear `tests/__pycache__`* cleared
    the importers, whose bytecode is never stale, and missed the mutated
    file's, which is; any second directory named in its place would miss the
    third the same way (#129).

    The two sentences `tests/test_the_handoff_before_round_one.py` pins are
    asserted here too, because the rewording happens around them and that
    case is the one that would notice their loss -- this one says the loss
    did not come from this edit."""
    smith = flat("agents", "smith.md")
    # Any runner: the definition ships to repositories with no `bin/test`,
    # and `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` holds it
    # to naming none.
    assert re.search(r"mutation-check \S+ --replace .+? --tests \"", smith), (
        "`agents/smith.md` does not show the mutation loop as one command, "
        "with its replacement and the cases it runs"
    )
    assert "-p no:xdist" in smith, (
        "the example dropped `-p no:xdist`, which `questions.md` Q1's "
        "measurement put there for a handful of cases"
    )
    assert "tests/__pycache__" not in smith, (
        "`agents/smith.md` still names a directory to clear between mutations"
    )
    assert (
        "Mutation-test every unit you added, one at a time, before you hand over."
        in smith
    )
    assert "watch one go red" in smith


def test_the_boundaries_bullet_says_the_command_holds_the_copy():
    smith = flat("agents", "smith.md")
    bullet = smith[smith.index("**Commit before you mutate") :]
    bullet = bullet[: bullet.index("## Report")]
    assert "`mutation-check` holds that copy" in bullet, bullet


def test_the_verify_skill_says_what_each_verdict_means_and_what_the_bound_ends():
    """The section a reader opens to learn the command: its verdicts with
    their exit codes, its bound, and what that bound ends on each platform."""
    skill = flat("skills", "verify", "SKILL.md")
    start = skill.index("#### `mutation-check`")
    section = skill[start : skill.index("### 3. Bound to the tree")]
    for said in (
        "mutation-check <file> --replace",
        "`red`, exit 0",
        "`SURVIVED`, exit 1",
        "exit 2",
        "300 seconds",
        "process group",
        "Windows",
        "PYTHONDONTWRITEBYTECODE",
        "arm-check",
        # Round 1, 🔴 1: the baseline, and the verdict it gives.
        "first runs `--tests` against the file as it is",
        "`no baseline`",
    ):
        assert said in section, f"the section does not say {said!r}"


def test_the_default_bound_is_the_one_both_documents_state(tmp_path, monkeypatch):
    """`questions.md` Q4: a value somebody waits on. The constant, the bound a
    call with no `--timeout` actually gets, and the figure the smith and the
    skill are told are one number, so moving one is seen in all three."""
    mc = module()
    seen = {}

    def records(path, old, new, command, *, cwd, timeout):
        seen["timeout"] = timeout
        return mc.RED, "recorded", ""

    monkeypatch.setattr(mc, "mutation_run", records)
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    assert mc.main([str(target), "--replace", "1", "2", "--tests", "x"]) == 0
    assert seen["timeout"] == mc.DEFAULT_TIMEOUT == 300.0
    bound = f"{mc.DEFAULT_TIMEOUT:g}"
    assert f"bound ({bound} s unless `--timeout`" in flat("agents", "smith.md")
    assert f"{bound} seconds by default" in flat("skills", "verify", "SKILL.md")


# --- S5 · a run that never returns ends at the bound, and so does its child -


# A wrapper in `bin/test`'s position: against the mutant it starts the process
# that does the work as a child of its own and waits for it, and against the
# file as it is it passes at once, so the run the bound ends is the mutated
# one. The child's pid is written down first, so a case can ask afterwards
# whether it is still alive. Arguments: the file, the mutant's text, the pid
# file.
STARTS_A_CHILD = """\
import subprocess, sys
with open(sys.argv[1], encoding="utf-8") as f:
    if sys.argv[2] not in f.read():
        sys.exit(0)
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
with open(sys.argv[3], "w", encoding="utf-8") as f:
    f.write(str(child.pid))
child.wait()
"""


def starts_a_child(tmp_path, target, pid_file, body=STARTS_A_CHILD):
    return cases_command(probe(tmp_path, body), target, "VALUE = 2", pid_file)


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def gone_within(pid, seconds):
    """Polled, because the orphan is reaped by the system, not by us."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not alive(pid):
            return True
        time.sleep(0.05)
    return not alive(pid)


def end_if_alive(pid):
    """So a red case leaves nothing running either (C5)."""
    if pid is not None and alive(pid):
        try:
            os.kill(pid, 9)
        except ProcessLookupError:
            pass


def read_pid(path):
    try:
        return int(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


@pytest.mark.skipif(os.name == "nt", reason="the process-group bound is POSIX's")
def test_a_run_past_the_bound_is_timed_out_and_leaves_nothing_it_started(
    tmp_path, capsys
):
    """#577: a mutated run hung for 32 minutes. #313 measured why a bound in
    the loop is not enough by itself: `subprocess.run`'s timeout ends the
    direct child, and `bin/test` puts pytest one process further down, so the
    suite outlives the verdict and runs on, unbounded and unreported.

    Not red, not SURVIVED: neither was measured."""
    target = tmp_path / "under_test.py"
    original = b"VALUE = 1\n"
    target.write_bytes(original)
    pid_file = tmp_path / "child.pid"
    started = time.monotonic()
    try:
        code, out = run(
            [
                target,
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                starts_a_child(tmp_path, target, pid_file),
                "--timeout",
                "1",
            ],
            capsys,
        )
        elapsed = time.monotonic() - started
        pid = read_pid(pid_file)
        assert pid is not None, "the wrapper never started its child"
        assert gone_within(pid, 5), (
            "the bound ended the wrapper and left the process it started "
            "running -- a wrapper's pytest outliving the verdict, #313"
        )
    finally:
        end_if_alive(read_pid(pid_file))
    assert code == 2, out
    assert out.startswith("timed out after 1s"), out
    assert elapsed < 15, f"the bound of 1s took {elapsed:.1f}s to end the run"
    assert target.read_bytes() == original
    assert not list(tmp_path.glob("__pycache__/under_test.*.pyc"))


# A child that leaves the wrapper's process group and keeps the cases'
# output open, so no group kill reaches it.
STARTS_AN_ESCAPED_CHILD = STARTS_A_CHILD.replace(
    '"import time; time.sleep(30)"])',
    '"import time; time.sleep(30)"], start_new_session=True)',
)


@pytest.mark.skipif(os.name == "nt", reason="the process-group bound is POSIX's")
def test_a_process_outside_the_group_does_not_hold_the_verdict_back(tmp_path, capsys):
    """A process that started a session of its own is outside the group, so
    the kill does not reach it, and it holds the cases' output for as long as
    it runs. Nothing after the kill may wait on that output, or the hang is
    back one step later; the verdict names the escape as the bound's limit."""
    assert STARTS_AN_ESCAPED_CHILD != STARTS_A_CHILD, "the fixture did not change"
    mc = module()
    target = tmp_path / "under_test.py"
    target.write_bytes(b"VALUE = 1\n")
    pid_file = tmp_path / "child.pid"
    started = time.monotonic()
    try:
        code = mc.main(
            [
                str(target),
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                starts_a_child(tmp_path, target, pid_file, STARTS_AN_ESCAPED_CHILD),
                "--timeout",
                "1",
            ]
        )
        elapsed = time.monotonic() - started
    finally:
        end_if_alive(read_pid(pid_file))
    out = capsys.readouterr().out
    assert elapsed < 15, (
        f"collecting the output waited {elapsed:.1f}s on the escaped child"
    )
    assert code == 2 and out.startswith("timed out after 1s"), out
    assert "session of its own" in out, out
    assert target.read_bytes() == b"VALUE = 1\n"


@pytest.mark.skipif(os.name == "nt", reason="the process-group bound is POSIX's")
def test_a_group_that_ended_on_its_own_at_the_bound_is_not_an_error():
    """The command can finish between the bound expiring and the kill. The
    group is gone by then, and the run is still a `timed out` rather than a
    traceback that skips the verdict."""
    mc = module()
    proc = subprocess.Popen(
        [sys.executable, "-c", "pass"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    proc.communicate(timeout=30)
    mc._end(proc, mc.GROUP)
    assert proc.returncode == 0


# --- S6 · the Windows half ends the direct child and says what it did not ---


def test_the_bound_is_chosen_by_the_platform_and_windows_says_what_it_left():
    """§13: a defence resting on a platform's guarantee is asked without it.
    The chooser takes the platform as an argument, so the Windows half is
    pinned from a machine that is not Windows."""
    mc = module()
    assert mc.strategy("posix") == mc.GROUP
    assert mc.strategy("nt") == mc.CHILD
    windows = mc.timed_out_detail(5.0, mc.CHILD)
    assert "after 5s" in windows
    assert "not ended" in windows, (
        f"the Windows verdict does not say that what the command started may "
        f"still be running: {windows}"
    )
    posix = mc.timed_out_detail(5.0, mc.GROUP)
    assert "not ended" not in posix and "process group" in posix, posix


# --- Ctrl-C ends what the run started, then restores ------------------------


@pytest.mark.skipif(os.name == "nt", reason="the process-group bound is POSIX's")
def test_an_interrupt_ends_the_run_it_started_and_restores_the_file(
    tmp_path, capsys, monkeypatch
):
    """The run is in a session of its own, so the terminal's Ctrl-C reaches
    this process and not the cases (#313 names that consequence). So the
    interrupt has to end the group here, or the suite runs on after the
    command has gone. Delivered as the `KeyboardInterrupt` Python raises for
    it, once the child is known to be running."""
    target = tmp_path / "under_test.py"
    original = b"VALUE = 1\n"
    target.write_bytes(original)
    pid_file = tmp_path / "child.pid"
    mc = module()
    real_wait = mc._wait

    def interrupted(proc, timeout):
        # Against the file as it is the cases pass at once; the interrupt
        # lands in the mutated run, while the mutant is on disk.
        if "VALUE = 2" not in target.read_text(encoding="utf-8"):
            return real_wait(proc, timeout)
        deadline = time.monotonic() + 10
        while read_pid(pid_file) is None and time.monotonic() < deadline:
            time.sleep(0.05)
        raise KeyboardInterrupt

    monkeypatch.setattr(mc, "_wait", interrupted)
    try:
        code = mc.main(
            [
                str(target),
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                starts_a_child(tmp_path, target, pid_file),
            ]
        )
        out = capsys.readouterr().out
        pid = read_pid(pid_file)
        assert pid is not None, "the wrapper never started its child"
        assert gone_within(pid, 5), "the interrupt left the process the run started"
    finally:
        end_if_alive(read_pid(pid_file))
        monkeypatch.setattr(mc, "_wait", real_wait)
    assert code == 2, out
    assert out.startswith("interrupted"), out
    assert target.read_bytes() == original
