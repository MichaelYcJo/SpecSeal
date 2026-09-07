"""A script run with whatever `python3` is on PATH says what it needs.

Issue #226, reported from another repository on 0.8.3. `round_record.py` uses
`zip(..., strict=True)`, which arrived in python 3.10, and on a machine whose
`python3` is 3.9 it died with `TypeError: zip() takes no keyword arguments` --
after argument parsing, path resolution and the report read had all succeeded.
So the failure read as a bug in the report, and the message named neither the
version needed nor the flag. macOS still ships 3.9 as `/usr/bin/python3`.

What is pinned here is the sentence and the moment it arrives. A person reads
that sentence and acts on it, which is the only reason it exists, and the
whole complaint was that it arrived too late to be about the interpreter.

**Testing a version guard from an interpreter that satisfies it.** Two cases
do it two ways, and neither settles for asserting that a constant exists:

- `test_a_floor_above_this_interpreter_refuses_before_anything_is_read`
  copies the real script into a temporary directory, raises `FLOOR` above
  whatever is running, and runs it. Every line of the guard is the shipped
  line; one constant moved. It never skips, so CI stands on it.
- `test_the_script_refuses_at_entry_on_a_below_floor_interpreter` finds a
  genuinely old interpreter on the machine and runs the real file at its real
  path. It skips where none exists -- which is every CI runner -- and its job
  is to catch the raised-floor copy lying.
"""

import importlib.util
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, "skills", "code-review", "scripts")
SCRIPT = os.path.join(SCRIPTS, "round_record.py")
RUNNER = os.path.join(ROOT, ".github", "scripts", "run_tests.py")
RUFF = os.path.join(ROOT, "ruff.toml")

# Arguments `argparse` accepts in full, naming nothing that exists. Below the
# floor the guard answers before any of them is looked at; above it, the
# script gets as far as complaining about the item -- which is the contrast
# the ticket is about, and one case asserts both halves of it.
JUNK_ITEM = os.path.join("no", "such", "work-item")
ARGS = (
    "new",
    "--item",
    JUNK_ITEM,
    "--round",
    "1",
    "--target",
    "HEAD",
    "--report",
    os.path.join("no", "such", "report.md"),
    "--asked",
    os.path.join("no", "such", "asked.md"),
    "--ran-by",
    "nobody on nothing",
)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generator():
    """`round_record.py`, imported. Importing it loads `chain_check.py` too,
    which is the module-level work the guard is required to precede."""
    return _load("specseal_round_record_floor", SCRIPT)


def runner():
    """`.github/scripts/run_tests.py`, which holds `FLOOR` for the repository
    and which `CONTRIBUTING.md`'s floor sentence names."""
    return _load("specseal_run_tests_floor", RUNNER)


def source():
    with open(SCRIPT, encoding="utf-8") as f:
        return f.read()


def raised_floor(tmp_path, floor="(99, 0)"):
    """The real script, with `FLOOR` raised above any interpreter, in a
    directory holding its sibling checker so `HERE` still resolves.

    The substitution asserts that it matched. A `sed` that misses does
    nothing, says nothing and exits zero, and a test resting on one passes by
    testing an unmodified file -- which is this suite's own rule about edits,
    applied to the edit a test makes."""
    scripts = tmp_path / "scripts"
    shutil.copytree(SCRIPTS, scripts)
    copy = scripts / "round_record.py"
    text = copy.read_text(encoding="utf-8")
    old = "FLOOR = (3, 12)"
    assert old in text, (
        f"round_record.py no longer spells the floor as `{old}`, so this case "
        "has been raising a floor in a file that does not have one"
    )
    copy.write_text(text.replace(old, f"FLOOR = {floor}"), encoding="utf-8")
    return str(copy)


def run(python, script, *extra):
    return subprocess.run(
        [python, script, *ARGS, *extra],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def version_of(python):
    """`(major, minor, micro)` for an interpreter, or None if it will not
    answer. Asked of the interpreter rather than read off its name: a
    `python3.9` on PATH is a filename, not a promise."""
    try:
        out = subprocess.run(
            [python, "-c", "import sys; print('%d %d %d' % sys.version_info[:3])"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    try:
        return tuple(int(part) for part in out.stdout.split())
    except ValueError:
        return None


# Every plausible spelling of an older interpreter, plus the one the ticket is
# actually about: macOS's system python, which is what `python3` resolves to
# for anyone who has not put something else in front of it.
CANDIDATES = (
    "/usr/bin/python3",
    "python3.9",
    "python3.10",
    "python3.11",
    "python3.8",
    "python3",
    "python",
)


def an_interpreter_below(floor):
    """`(path, version_text)` for an interpreter on this machine older than
    `floor`, or None. CI runners have none, which is why the case using this
    skips rather than fails."""
    for name in CANDIDATES:
        path = name if os.path.isabs(name) else shutil.which(name)
        if not path:
            continue
        found = version_of(path)
        if found and found[:2] < tuple(floor):
            return path, ".".join(str(part) for part in found)
    return None


# --- the sentence ---------------------------------------------------------


def test_an_interpreter_below_the_floor_gets_a_sentence():
    """Both numbers, or the sentence cannot be acted on.

    A floor with no found version tells a reader what is wanted and not
    whether they have it -- and the reader whose `python3` is secretly 3.9 is
    exactly the reader who does not know what they are running. The
    interpreter's path is there for the same reason: on macOS the surprise is
    not the version, it is which file `python3` was."""
    module = generator()
    sentence = module.below_floor((3, 9, 6), "/usr/bin/python3")
    assert sentence, "an interpreter below the floor was let through"
    assert module.FLOOR_TEXT in sentence, "the sentence does not name the floor"
    assert "3.9.6" in sentence, (
        "the sentence does not name the version it found, so a reader cannot "
        "tell whether it is talking about their interpreter"
    )
    assert "/usr/bin/python3" in sentence, (
        "the sentence does not name the interpreter it found, which is the "
        "half a reader on macOS is surprised by"
    )
    assert "round-record" in sentence, (
        "the sentence does not name the command, so a reader who ran it "
        "through a wrapper cannot tell what produced it"
    )


def test_the_sentence_says_nothing_was_read_or_written():
    """The ticket's complaint is that the failure read as a bug in the report.

    Saying so is what tells the operator their files are untouched -- the one
    question a mid-run traceback leaves open."""
    sentence = generator().below_floor((3, 9, 6), "/usr/bin/python3")
    assert re.search(r"[Nn]othing was read", sentence), (
        "the sentence does not say nothing was read, so a reader cannot tell "
        "a refusal at entry from a crash partway through"
    )
    assert re.search(r"nothing was written", sentence), (
        "the sentence does not say nothing was written"
    )


def test_the_floor_and_above_are_let_through():
    """The boundary, and one above it. A floor that refuses itself would take
    the whole repository down at the next release."""
    module = generator()
    floor = tuple(module.FLOOR)
    assert module.below_floor((*floor, 0)) is None, (
        "the floor itself is refused, so the supported interpreter cannot run"
    )
    assert module.below_floor((floor[0], floor[1] + 1, 0)) is None
    assert module.below_floor((floor[0] + 1, 0, 0)) is None
    assert module.below_floor((floor[0], floor[1] - 1, 99)) is not None, (
        "one minor below the floor is let through, so the floor is not a floor"
    )


def test_this_interpreter_is_at_or_above_the_floor():
    """The suite runs under `bin/test`, which builds at the floor or refuses.

    If this fails, every other case here is measuring something else."""
    module = generator()
    assert module.below_floor() is None, module.below_floor()


# --- the moment it arrives ------------------------------------------------


def test_a_floor_above_this_interpreter_refuses_before_anything_is_read(tmp_path):
    """The real guard, from any interpreter, by moving the floor instead.

    This is the case that does not skip. What it proves is the whole ticket:
    exit 2, a sentence rather than a traceback, and nothing said about the
    work item -- because the guard answered before `argparse` looked at it."""
    out = run(sys.executable, raised_floor(tmp_path))
    running = ".".join(str(part) for part in sys.version_info[:3])
    assert out.returncode == 2, (
        f"exit {out.returncode}, and 2 is the code for nothing written; "
        f"stderr was {out.stderr!r}"
    )
    assert "99.0" in out.stderr, "the sentence does not name the floor it holds"
    assert running in out.stderr, "the sentence does not name this interpreter"
    assert "Traceback" not in out.stderr, (
        "a traceback is what the ticket is about; the guard is supposed to "
        f"replace it: {out.stderr!r}"
    )
    assert JUNK_ITEM not in out.stderr + out.stdout, (
        "the run got as far as the work item, so the guard is not at entry"
    )
    assert not out.stdout, f"something was printed before the refusal: {out.stdout!r}"


def test_above_the_floor_the_same_arguments_get_past_the_guard(tmp_path):
    """The control, and the half that keeps the case above honest.

    With the floor left where it is, the same junk arguments reach the script
    proper and it complains about the item instead. Without this, a guard that
    refused everything would pass every assertion above."""
    scripts = tmp_path / "scripts"
    shutil.copytree(SCRIPTS, scripts)
    out = run(sys.executable, str(scripts / "round_record.py"))
    assert out.returncode != 0, "junk arguments were accepted"
    assert "99.0" not in out.stderr
    everything = out.stdout + out.stderr
    assert JUNK_ITEM in everything or "item" in everything.lower(), (
        "above the floor the script no longer reaches its own argument "
        f"handling: {everything!r}"
    )


def test_the_script_refuses_at_entry_on_a_below_floor_interpreter():
    """The genuine article, where the machine has one.

    `/usr/bin/python3` is 3.9 on macOS, which is the ticket's own platform.
    CI runners have nothing below the floor, so this skips there -- its job is
    to catch the raised-floor copy above lying about what the real file does
    on a real old interpreter."""
    module = generator()
    found = an_interpreter_below(module.FLOOR)
    if not found:
        pytest.skip("no interpreter below the floor on this machine")
    python, version = found
    out = run(python, SCRIPT)
    assert out.returncode == 2, (
        f"{python} ({version}) exited {out.returncode}; stderr {out.stderr!r}"
    )
    assert module.FLOOR_TEXT in out.stderr
    assert version in out.stderr
    named = re.search(r" at (\S+?)\.?\n", out.stderr)
    assert named, f"the sentence names no interpreter: {out.stderr!r}"
    # Not `assert python in out.stderr`. That passed here for the wrong
    # reason: macOS resolves `/usr/bin/python3` to a shim inside Xcode, whose
    # path ENDS with `/usr/bin/python3`, so the substring held while the
    # message named a different file. What a reader needs is that the path
    # printed is an interpreter, and that it is the one whose version was
    # just reported -- so that is what is asked, of the path itself.
    assert version_of(named.group(1)) == version_of(python), (
        f"the sentence names {named.group(1)}, which is not the interpreter "
        f"that ran ({python})"
    )
    assert "Traceback" not in out.stderr, out.stderr
    assert "zip()" not in out.stderr, (
        "the interpreter's own TypeError still reaches the operator, so the "
        "guard is downstream of the sites that raise it"
    )
    assert JUNK_ITEM not in out.stderr + out.stdout


def test_the_guard_precedes_every_other_module_level_act():
    """Structure, because the two cases above cannot see ordering.

    `chain = load(CHAIN, ...)` reads and executes a second file at import,
    before `main()` is ever called, and on 3.9 that load succeeds -- so a
    guard placed in `main()` would let the operator watch exactly the progress
    the ticket is about. This reads the module's own AST rather than its
    text: a comment mentioning `load(` is not an act."""
    import ast

    def calls(node, name):
        """True for `name(...)` — asked of the tree, so a comment or a string
        mentioning the call is not one."""
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == name
        )

    tree = ast.parse(source())
    asked = refusal = acts = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and "below_floor" in ast.dump(node.value):
            asked = asked or node.lineno
        if isinstance(node, ast.If) and "SystemExit" in ast.dump(node):
            refusal = refusal or node.lineno
        if isinstance(node, ast.Assign) and calls(node.value, "load"):
            acts = acts or node.lineno
    assert asked, "nothing at module level calls `below_floor`"
    assert refusal, "no module-level `if` raises SystemExit"
    assert asked < refusal, "the floor is asked about after the refusal"
    assert acts, "`chain = load(...)` is no longer a module-level assignment"
    assert refusal < acts, (
        f"the guard is at line {refusal} and the sibling checker is loaded at "
        f"{acts}; the guard has to come first or the script does real work "
        "before it says the interpreter is wrong"
    )


def test_the_docstring_says_what_exit_2_now_covers():
    """A code whose meaning is written down and then quietly widened is a code
    nobody can read. The guard exits 2, and 2 already meant one thing."""
    head = source().split('"""')[1]
    assert "Exit codes" in head, "the docstring no longer documents exit codes"
    line = head[head.index("Exit codes") :]
    assert "interpreter" in line.split("\n\n")[0], (
        "exit 2 covers a refused interpreter now, and the docstring still "
        "says it covers unusable input only"
    )


# --- one number ------------------------------------------------------------


def test_the_floor_is_the_number_the_runner_and_the_linter_hold():
    """`CONTRIBUTING.md` §*Running the checks*: the floor is one number, held
    as `FLOOR` in the runner so the sentence and the code agree.

    The guard is a sixth carrier of it -- after `ruff.toml`, both READMEs, the
    CI matrix and that sentence -- and it does not import the constant: a
    fallback-safe read still has to name a floor in its `except` branch, so
    the second spelling survives the import anyway. `spec.md` §*Where the
    floor number lives* carries the argument. This is the pin that makes the
    second spelling not a second number.

    It also ties the repository's two floor authorities together for the first
    time. `test_release_hygiene.py` reads `ruff.toml` and
    `test_the_suite_has_a_command_that_is_cheap_twice.py` reads the runner,
    and nothing read both."""
    module = generator()
    assert tuple(module.FLOOR) == tuple(runner().FLOOR), (
        f"round_record.py holds {module.FLOOR} and "
        f".github/scripts/run_tests.py holds {runner().FLOOR}; "
        "CONTRIBUTING.md says the floor is one number"
    )
    assert module.FLOOR_TEXT == runner().FLOOR_TEXT
    with open(RUFF, encoding="utf-8") as f:
        m = re.search(r'target-version = "py(\d)(\d+)"', f.read())
    assert m, "ruff.toml lost its target-version"
    assert f"{m.group(1)}.{m.group(2)}" == module.FLOOR_TEXT, (
        f"the guard says {module.FLOOR_TEXT} and ruff.toml lints at "
        f"{m.group(1)}.{m.group(2)}"
    )


# --- the class -------------------------------------------------------------

# The two constructs that put a shipped script above the floor today, spelled
# so that neither hides. `zip\([^)]*strict=` was the first spelling and it hid
# round_record.py:935, where an inner `verdict_words(reader, rows)` closes a
# parenthesis before the keyword is reached -- three of four sites answered.
ABOVE_THE_FLOOR = re.compile(r"zip\(.*strict=|datetime\.UTC")

# Every shipped file the pattern finds, and what was decided about it. A row
# here is a classification, not a permission: `spec.md`'s enumeration table
# carries which interpreter each one is invoked with and why it was left.
CLASSIFIED = {
    "skills/code-review/scripts/round_record.py": (
        "guarded -- it refuses at entry with a sentence naming the floor"
    ),
    ".github/scripts/gather_changelog.py": "deferred, seal/follow-up.md (#226)",
    ".github/scripts/fold_ledger.py": "deferred, seal/follow-up.md (#226)",
    "skills/implement/scripts/seal.py": "deferred, seal/follow-up.md (#226)",
    "hooks/root-migrate.py": "deferred, seal/follow-up.md (#226)",
}


def shipped_python():
    """Every tracked `.py` this plugin ships, less the two roots that do not
    run on a user's interpreter: `tests/` runs under `bin/test`'s virtualenv,
    which holds the floor or refuses to build, and `seal/` holds records."""
    out = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return [
        rel
        for rel in out.stdout.split()
        if not rel.startswith(("tests/", "seal/")) and rel
    ]


def test_no_shipped_script_needs_more_than_the_floor_without_saying_so():
    """The class, re-enumerated by the suite instead of by whoever remembers.

    `skills/agent-contract/SKILL.md` §12: the finding named one coordinate and
    what was owed was every instance the same cause produces. Five files
    carried one, and four of them are somebody else's branch or somebody
    else's release. This is what keeps a sixth from arriving as a traceback on
    a stranger's mac."""
    files = shipped_python()
    assert files, "git ls-files found no shipped python at all"
    found = set()
    for rel in files:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            if ABOVE_THE_FLOOR.search(f.read()):
                found.add(rel)
    new = sorted(found - set(CLASSIFIED))
    assert not new, (
        f"{new} use a construct newer than python {generator().FLOOR_TEXT} and "
        "are not classified. A script this plugin ships is run with whatever "
        "`python3` is on PATH, so this is a traceback on somebody's machine. "
        "Guard it the way skills/code-review/scripts/round_record.py is "
        "guarded, or add it to CLASSIFIED with where it was deferred to"
    )
    gone = sorted(set(CLASSIFIED) - found)
    assert not gone, (
        f"{gone} no longer carry the construct they were classified for; "
        "drop the row rather than leaving a classification of nothing"
    )
