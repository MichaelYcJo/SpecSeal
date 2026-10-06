"""The broad gate's recorder writes down what its own pytest process ran (#825).

`skills/verify/scripts/pytest_record/specseal_pytest_record.py` is loaded into
every run the broad gate measures, through `PYTHONPATH` and a `-p` in
`PYTEST_ADDOPTS`, and keyed by `SPECSEAL_RECORD_KEY`. The gate's permissive
word rests on one property: a line in a keyed record was written by the pytest
process that collected the test it names, and by no other. These cases drive
pytest as a subprocess over a scratch project, the way the gate does, and
hold that property from both sides -- the claiming process records (S1, S4),
and a pytest it starts in turn, in a child process or in its own, records
nothing (S2, S3); with no key or no directory nothing is written (S5).

Since the reframe after round 3 a line's path is the node's own, read where
pytest holds the node and carried on the report to the process that writes,
never a path made from a node id and a rootdir (S23). So every layout rounds
1-3 refused is recorded under its own path (S24), the recorder runs none of
the row's code (S25), and what it cannot place it leaves out and counts on
the `end` line (S27).
"""

import importlib.util
import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDER_DIR = os.path.join(ROOT, "skills", "verify", "scripts", "pytest_record")
KEY = "head-0123456789abcdef"

PASSING_AND_FAILING = "def test_ok():\n    pass\n\n\ndef test_bad():\n    assert 0\n"

# A file pytest is handed by name, so its name need not match `test_*.py`
# and the outer run never collects it.
INNER_TARGET = "def test_inner():\n    print('INNER-RAN-ITS-TEST')\n"

SPAWNS_A_CHILD = """\
import os
import subprocess
import sys


def test_spawns_a_child():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "inner_target.py")
    subprocess.run([sys.executable, "-m", "pytest", "-s", "-p", "no:cacheprovider", target])
    assert 0
"""

CALLS_PYTEST_MAIN = """\
import os

import pytest


def test_calls_pytest_main():
    here = os.path.dirname(os.path.abspath(__file__))
    pytest.main(["-s", "-p", "no:cacheprovider", os.path.join(here, "inner_target.py")])
    assert 0
"""


def project(tmp_path, files):
    """A scratch project: `tests/<name>` for each entry, and an empty
    `records/` beside it. Returns (project root, records directory)."""
    root = tmp_path / "project"
    (root / "tests").mkdir(parents=True)
    for name, body in files.items():
        (root / "tests" / name).write_text(body, encoding="utf-8")
    records = tmp_path / "records"
    records.mkdir()
    return root, records


def recording_env(records, key=KEY, directory=True):
    """The environment the gate hands a run it measures (`spec.md` Scope 2),
    built on this process's own with the recorder's variables cleared first,
    so an outer gate's run of this suite does not leak into the case."""
    env = dict(os.environ)
    for name in ("SPECSEAL_RECORD_KEY", "SPECSEAL_RECORD_DIR", "PYTEST_ADDOPTS"):
        env.pop(name, None)
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (RECORDER_DIR, env.get("PYTHONPATH")) if p
    )
    env["PYTEST_ADDOPTS"] = "-p specseal_pytest_record"
    if key is not None:
        env["SPECSEAL_RECORD_KEY"] = key
    if directory:
        env["SPECSEAL_RECORD_DIR"] = str(records)
    return env


def run_pytest(root, env, *args):
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", *args, "tests"],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=240,
    )


def records_of(records):
    """`{file name: [parsed lines]}` for every file in `records`."""
    out = {}
    for name in sorted(os.listdir(str(records))):
        with open(os.path.join(str(records), name), encoding="utf-8") as f:
            out[name] = [json.loads(line) for line in f if line.strip()]
    return out


def the_one_record(records):
    found = records_of(records)
    assert len(found) == 1, f"expected exactly one record file, found {sorted(found)}"
    ((name, lines),) = found.items()
    return name, lines


def test_the_recorder_records_its_own_process(tmp_path):
    """S1. One `<key>-<pid>.jsonl`: a session line, a test line per phase
    per test whose path is the test file, and an end line with pytest's
    exit."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    result = run_pytest(root, recording_env(records), "-q")
    assert result.returncode == 1, result.stdout + result.stderr

    name, lines = the_one_record(records)
    assert name.startswith(KEY + "-") and name.endswith(".jsonl")
    assert [line["kind"] for line in lines[:1]] == ["session"]
    session = lines[0]
    assert session["key"] == KEY
    assert os.path.realpath(session["rootdir"]) == os.path.realpath(str(root))
    assert os.path.realpath(session["invocation_dir"]) == os.path.realpath(str(root))
    assert lines[-1] == {"kind": "end", "exitstatus": 1, "unplaced": 0}

    tests = [line for line in lines if line["kind"] == "test"]
    assert sorted((t["nodeid"], t["when"]) for t in tests) == sorted(
        (f"tests/test_mixed.py::{name}", when)
        for name in ("test_ok", "test_bad")
        for when in ("setup", "call", "teardown")
    )
    target = os.path.realpath(str(root / "tests" / "test_mixed.py"))
    assert {os.path.realpath(t["path"]) for t in tests} == {target}
    assert all(os.path.isabs(t["path"]) for t in tests)
    failed = [(t["nodeid"], t["when"]) for t in tests if t["outcome"] == "failed"]
    assert failed == [("tests/test_mixed.py::test_bad", "call")]


# A base class whose test is defined in one module and collected, by
# inheritance, in another; and a test function one module imports from the
# other. pytest's `report.location` names the module that DEFINES the test.
DEFINES_THE_TEST = (
    "class Base:\n    v = 1\n\n    def test_shared(self):\n        assert self.v == 1\n\n\n"
    "def test_imported():\n    assert False\n"
)
COLLECTS_IT = (
    "import os\nimport sys\n\n"
    "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
    "from test_defines import Base, test_imported  # noqa: E402,F401\n\n\n"
    "class TestCollected(Base):\n    v = 2\n"
)


@pytest.mark.parametrize("flags", [(), ("-n", "2")], ids=["plain", "xdist"])
def test_a_test_is_recorded_under_the_module_that_collected_it(tmp_path, flags):
    """#825 phase 4, found by the regression corpus (N1, N1b, Q4). A test a
    module inherits or imports from another fails there, and the record
    names the COLLECTING module: the word at the base is about the file the
    gate compares, and `report.location[0]` names the defining one, which
    gave a file the base passes `failing on base too`. The defining module's
    own collected tests stay under it."""
    if flags and importlib.util.find_spec("xdist") is None:
        pytest.skip("pytest-xdist is not installed here")
    root, records = project(
        tmp_path,
        {"test_defines.py": DEFINES_THE_TEST, "test_collects.py": COLLECTS_IT},
    )
    result = run_pytest(root, recording_env(records), "-q", *flags)
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    failed = {
        (line["nodeid"], os.path.basename(line["path"]))
        for line in lines
        if line["kind"] == "test" and line["outcome"] == "failed"
    }
    assert failed == {
        ("tests/test_collects.py::TestCollected::test_shared", "test_collects.py"),
        ("tests/test_collects.py::test_imported", "test_collects.py"),
        ("tests/test_defines.py::test_imported", "test_defines.py"),
    }, failed


@pytest.mark.parametrize(
    "flags", [("-s",), ("-q",), ("-n", "2")], ids=["s", "q", "xdist"]
)
def test_a_pytest_the_measured_process_spawns_records_nothing(tmp_path, flags):
    """S2. A test spawns pytest on a second file in a child process. The
    child inherits an environment the recorder took the key out of, so
    exactly one record carries the key and it names the outer file only --
    while the child's own output still reaches the run's text."""
    root, records = project(
        tmp_path, {"test_spawns.py": SPAWNS_A_CHILD, "inner_target.py": INNER_TARGET}
    )
    result = run_pytest(root, recording_env(records), *flags)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "INNER-RAN-ITS-TEST" in result.stdout + result.stderr

    _, lines = the_one_record(records)
    paths = {os.path.realpath(line["path"]) for line in lines if "path" in line}
    assert paths == {os.path.realpath(str(root / "tests" / "test_spawns.py"))}


def test_a_second_session_in_the_measured_process_records_nothing(tmp_path):
    """S3. A test calls `pytest.main` in the measured process. The first
    session configured claimed the key, so the second finds none: one
    record, naming the outer file only."""
    root, records = project(
        tmp_path,
        {"test_calls_main.py": CALLS_PYTEST_MAIN, "inner_target.py": INNER_TARGET},
    )
    result = run_pytest(root, recording_env(records), "-s")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "INNER-RAN-ITS-TEST" in result.stdout

    _, lines = the_one_record(records)
    paths = {os.path.realpath(line["path"]) for line in lines if "path" in line}
    assert paths == {os.path.realpath(str(root / "tests" / "test_calls_main.py"))}
    assert [line["kind"] for line in lines].count("session") == 1


def test_the_xdist_controller_records_the_whole_run(tmp_path):
    """S4. Under `-n 2`, one file failing and one that fails to collect: one
    record file, written by the controller, holding the failing test's lines
    and the collection error as a `collect` line (Q-M2, measured in phase 1:
    the controller receives one failed collect report per worker, so the
    line may repeat)."""
    root, records = project(
        tmp_path,
        {
            "test_mixed.py": PASSING_AND_FAILING,
            "test_broken.py": "raise RuntimeError('fails at import')\n",
        },
    )
    result = run_pytest(
        root, recording_env(records), "-n", "2", "--continue-on-collection-errors"
    )
    assert result.returncode == 1, result.stdout + result.stderr

    _, lines = the_one_record(records)
    broken = os.path.realpath(str(root / "tests" / "test_broken.py"))
    mixed = os.path.realpath(str(root / "tests" / "test_mixed.py"))
    collects = [line for line in lines if line["kind"] == "collect"]
    assert collects, lines
    assert {os.path.realpath(c["path"]) for c in collects} == {broken}
    assert {c["outcome"] for c in collects} == {"failed"}
    failing = {
        os.path.realpath(line["path"])
        for line in lines
        if line["kind"] == "test" and line["outcome"] == "failed"
    }
    assert failing == {mixed}


@pytest.mark.parametrize("missing", ["key", "directory"])
def test_without_a_key_or_a_directory_nothing_is_written(tmp_path, missing):
    """S5. With no `SPECSEAL_RECORD_KEY`, or no `SPECSEAL_RECORD_DIR`, the
    recorder registers nothing: no file anywhere under the scratch tree, and
    the run's exit is pytest's own."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    env = (
        recording_env(records, key=None)
        if missing == "key"
        else recording_env(records, directory=False)
    )
    result = run_pytest(root, env, "-q")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "1 failed, 1 passed" in result.stdout
    assert records_of(records) == {}
    written = [
        os.path.join(d, f)
        for d, _, fs in os.walk(str(tmp_path))
        for f in fs
        if f.endswith(".jsonl")
    ]
    assert written == []


def test_a_record_it_cannot_write_leaves_pytest_its_own_exit_under_w_error(tmp_path):
    """#825 round 1, 🟡 3. The records directory is not there, so the
    recorder warns once and writes nothing. Under `python -W error` that
    warning used to be raised out of `pytest_sessionstart`, and pytest ended
    in INTERNALERROR, exit 3, its own result lost. It is shown under the
    recorder's own filter now, so the exit is the suite's own, 1."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    env = recording_env(records)
    env["SPECSEAL_RECORD_DIR"] = str(tmp_path / "absent")
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "error",
            "-m",
            "pytest",
            "-p",
            "no:cacheprovider",
            "-q",
            "tests",
        ],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=240,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 1, output
    assert "INTERNALERROR" not in output, output
    assert "no record written" in output, output


def pytest_in(root, env, *args):
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", *args],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=240,
    )


def failing_paths(lines):
    """The `realpath` of every file a `test` line records failing or a
    `collect` line records."""
    return {
        os.path.realpath(line["path"])
        for line in lines
        if (line["kind"] == "test" and line["outcome"] == "failed")
        or line["kind"] == "collect"
    }


def real(path):
    return os.path.realpath(str(path))


@pytest.mark.parametrize("flags", [(), ("-n", "2")], ids=["plain", "xdist"])
def test_the_path_each_line_carries_is_the_nodes_own(tmp_path, flags):
    """S23 (#825's reframe after round 3). A hookwrapper on the hook that
    makes each report sets the node's own path on it, in the process that
    holds the node -- an xdist worker under `-n 2` -- and the controller's
    recorder writes that path. Every `test` and `collect` line names its
    file exactly, one record holds the whole run, and nothing is unplaced
    (`questions.md` Q-M3, measured in phase 5)."""
    if flags and importlib.util.find_spec("xdist") is None:
        pytest.skip("pytest-xdist is not installed here")
    root, records = project(
        tmp_path,
        {
            "test_mixed.py": PASSING_AND_FAILING,
            "test_broken.py": "import no_such_module_here\n",
        },
    )
    result = run_pytest(
        root, recording_env(records), "-q", "--continue-on-collection-errors", *flags
    )
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    mixed = real(root / "tests" / "test_mixed.py")
    broken = real(root / "tests" / "test_broken.py")
    by_kind = {}
    for line in lines:
        if "path" in line:
            by_kind.setdefault(line["kind"], set()).add(real(line["path"]))
    assert by_kind == {"test": {mixed}, "collect": {broken}}, lines
    assert failing_paths(lines) == {mixed, broken}, lines
    assert lines[-1] == {"kind": "end", "exitstatus": 1, "unplaced": 0}, lines


def test_a_pyargs_module_inside_the_rootdir_is_recorded_under_its_own_path(
    tmp_path,
):
    """#825 rounds 1 and 2, read again after the reframe. A `--pyargs`
    module name is no path, and the module pytest imports for it is
    `tests/test_mixed.py` under the rootdir: its tests are written under
    that file."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(root / "tests")])
    result = pytest_in(root, env, "--pyargs", "test_mixed")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(root / "tests" / "test_mixed.py")}, lines


def test_a_pyargs_package_outside_the_rootdir_is_recorded_where_it_lives(tmp_path):
    """#825 round 2, flipped by the reframe (S24). pytest finds a `--pyargs`
    package where Python imports it from, outside the rootdir here, and
    names its `test_mixed.py` against the package: `test_mixed.py`, the name
    a file at the rootdir has. Joined to the rootdir that named the other
    file, so round 2 refused the session. The node's own path is the
    package's file, and the record says so; the file at the rootdir it
    shares a name with is in no line."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    package = tmp_path / "site" / "extpkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(tmp_path / "site")])
    result = pytest_in(root, env, "--pyargs", "extpkg")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(package / "test_mixed.py")}, lines


def test_a_namespace_package_outside_the_rootdir_is_recorded_where_it_lives(
    tmp_path,
):
    """#825 round 2, flipped by the reframe (S24). Under
    `consider_namespace_packages` pytest locates a `--pyargs` namespace
    package at its first search location, outside the rootdir, and names
    its modules against it. The record names the module's own file."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text(
        "[pytest]\nconsider_namespace_packages = true\n", encoding="utf-8"
    )
    (root / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    package = tmp_path / "site" / "nspkg"
    package.mkdir(parents=True)
    (package / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(tmp_path / "site")])
    result = pytest_in(root, env, "--pyargs", "nspkg")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(package / "test_mixed.py")}, lines


def test_a_pyargs_module_outside_that_cannot_be_collected_is_recorded_by_its_file(
    tmp_path,
):
    """#825 round 2, flipped by the reframe (S24). A plain `--pyargs` module
    outside the rootdir is its own initial path, so pytest gives it an empty
    node id, which joined to the rootdir named the rootdir itself. Its
    collector's own path is the module's file, and the failed collection's
    line names it."""
    root, records = project(tmp_path, {})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    site = tmp_path / "site"
    site.mkdir()
    (site / "extbroken.py").write_text("import no_such_module\n", encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(site)])
    result = pytest_in(root, env, "--pyargs", "extbroken")
    assert result.returncode == 2, result.stdout + result.stderr
    _, lines = the_one_record(records)
    collects = [line for line in lines if line["kind"] == "collect"]
    assert {real(line["path"]) for line in collects} == {real(site / "extbroken.py")}
    assert failing_paths(lines) == {real(site / "extbroken.py")}, lines


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_a_rootdir_named_through_a_symlink_records_the_file_pytest_ran(tmp_path):
    """#825 round 2, flipped by the reframe (S24). pytest compares a path
    with its rootdir lexically, so a `--rootdir` spelled through a symlink
    puts `tests/` outside it and pytest names `tests/test_mixed.py`
    `test_mixed.py`, the name `test_mixed.py` at the root has. The node's
    path is the one pytest ran, `tests/test_mixed.py`, and the record names
    it and never the file at the root."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    link = tmp_path / "link"
    link.symlink_to(root, target_is_directory=True)
    result = pytest_in(root, recording_env(records), "--rootdir", str(link), "tests")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(root / "tests" / "test_mixed.py")}, lines


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_an_argument_named_through_a_symlink_records_the_file_pytest_ran(tmp_path):
    """#825 round 2, the same branch from the other side, flipped by the
    reframe (S24). The rootdir is the project, named by `-c` as it is, and
    the argument reaches `tests/` through a symlink, so pytest names
    `tests/test_mixed.py` `test_mixed.py`. The node's path is the lexical one
    pytest holds, under the link, and it resolves to `tests/test_mixed.py`,
    never to the file at the root."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    link = tmp_path / "link"
    link.symlink_to(root, target_is_directory=True)
    result = pytest_in(
        root,
        recording_env(records),
        "-c",
        str(root / "pytest.ini"),
        str(link / "tests"),
    )
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(root / "tests" / "test_mixed.py")}, lines


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_a_symlinked_directory_under_the_rootdir_is_recorded_by_its_own_name(
    tmp_path,
):
    """#825 round 2. A directory under the rootdir that is a symlink to a
    place outside it is named by pytest under the rootdir, and the record
    names its file under the link."""
    root, records = project(tmp_path, {})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    shared = tmp_path / "shared"
    shared.mkdir()
    (shared / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    (root / "shared_tests").symlink_to(shared, target_is_directory=True)
    result = pytest_in(root, recording_env(records), "shared_tests")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    failed = {
        os.path.relpath(line["path"], str(root))
        for line in lines
        if line["kind"] == "test" and line["outcome"] == "failed"
    }
    assert failed == {os.path.join("shared_tests", "test_mixed.py")}, lines


BUILDS_A_COLLECTOR_ELSEWHERE = """\
from pathlib import Path

import pytest

OUTSIDE = Path(__file__).resolve().parent.parent / "outside"


def pytest_collect_directory(path, parent):
    if path.name == "tests":
        return pytest.Dir.from_parent(parent, path=OUTSIDE)
"""


def test_a_collector_built_for_a_path_no_argument_holds_is_recorded_by_its_files(
    tmp_path,
):
    """#825 round 2, flipped by the reframe (S24). A conftest builds a
    collector for a directory outside the rootdir and outside every
    argument, so pytest gives its tests the parent's node id and a `::`
    name, `.::outside::test_far.py::test_out`, whose path is no file. The
    node's own path is `outside/test_far.py`, and the record names it."""
    root, records = project(tmp_path, {"test_near.py": "def test_in():\n    pass\n"})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "conftest.py").write_text(BUILDS_A_COLLECTOR_ELSEWHERE, encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "test_far.py").write_text(
        "def test_out():\n    assert False\n", encoding="utf-8"
    )
    result = pytest_in(root, recording_env(records))
    assert result.returncode == 1, result.stdout + result.stderr
    assert ".::outside::test_far.py::test_out" in result.stdout, result.stdout
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(outside / "test_far.py")}, lines
    assert lines[-1]["unplaced"] == 0, lines


SETS_AT_SESSIONSTART = """\
import os


def pytest_sessionstart(session):
    os.environ["RECORDER_PROBE_READY"] = "1"
"""


def test_the_recorder_runs_none_of_the_rows_code(tmp_path):
    """S25, round 3's 🔴 1. A conftest sets at `pytest_sessionstart` what
    `pkg/__init__.py` reads at import, and the row runs `--pyargs
    pkg.test_ready`. Round 2's refusal located the name with `find_spec`,
    which imported `pkg` before the conftest's hook ran, and a test that
    passes without the recorder failed with it. The recorder looks nothing
    up now, so the run exits 0 as it does without it (`spec.md` Scope 1:
    it never changes an outcome)."""
    root, records = project(tmp_path, {})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "conftest.py").write_text(SETS_AT_SESSIONSTART, encoding="utf-8")
    package = root / "pkg"
    package.mkdir()
    (package / "__init__.py").write_text(
        "import os\nREADY = os.environ.get('RECORDER_PROBE_READY')\n",
        encoding="utf-8",
    )
    (package / "test_ready.py").write_text(
        "import pkg\n\n\ndef test_ready():\n    assert pkg.READY == '1'\n",
        encoding="utf-8",
    )
    env = recording_env(records)
    env.pop("RECORDER_PROBE_READY", None)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(root)])
    result = pytest_in(root, env, "--pyargs", "pkg.test_ready")
    assert result.returncode == 0, result.stdout + result.stderr
    _, lines = the_one_record(records)
    tests = [line for line in lines if line["kind"] == "test"]
    assert {line["outcome"] for line in tests} == {"passed"}, lines
    assert {real(line["path"]) for line in tests} == {real(package / "test_ready.py")}


ADDS_AN_ITEM_TO_THE_SESSION = """\
import pytest


class Status(pytest.Item):
    def runtest(self):
        raise AssertionError("the status item fails")

    def reportinfo(self):
        return self.path, None, "status"


def pytest_collection_modifyitems(session, config, items):
    items.append(Status.from_parent(session, name="status"))
"""


def test_a_test_with_no_file_of_its_own_is_left_out_and_counted(tmp_path):
    """S27, round 3's ⬜ 4. A conftest parents an item to the session, so
    the node's path is the rootdir, a directory and no file of its own: its
    lines are written nowhere and the `end` line counts it once, while the
    failing `tests/test_a.py` beside it is recorded as before. Round 2's
    guard abandoned the whole record here, silently."""
    root, records = project(
        tmp_path, {"test_a.py": "def test_a():\n    assert False\n"}
    )
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "conftest.py").write_text(ADDS_AN_ITEM_TO_THE_SESSION, encoding="utf-8")
    result = pytest_in(root, recording_env(records), "tests")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "::status" in result.stdout, result.stdout
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(root / "tests" / "test_a.py")}, lines
    assert all(line.get("nodeid") != "::status" for line in lines), lines
    assert lines[-1] == {"kind": "end", "exitstatus": 1, "unplaced": 1}, lines


REMOVES_ITS_OWN_FILE = """\
import os


def test_gone():
    os.remove(__file__)
    assert False
"""


def test_a_module_that_removes_its_own_file_is_still_recorded_under_it(tmp_path):
    """S27's second layout, `plan.md` Alternative U. A test removes its own
    module while it runs, so its `call` report names a file that is no
    longer there. A path that is no FILE is not dropped: only a directory
    is, so the failing line is written under the module and the base's
    word can be a failure."""
    root, records = project(tmp_path, {"test_gone.py": REMOVES_ITS_OWN_FILE})
    result = pytest_in(root, recording_env(records), "tests")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert failing_paths(lines) == {real(root / "tests" / "test_gone.py")}, lines
    assert lines[-1]["unplaced"] == 0, lines


RAISES_IN_MAKEREPORT = """\
import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == "call":
        raise RuntimeError("PLANTED-IN-MAKEREPORT")
"""


def test_a_report_hook_that_raises_is_not_laid_at_the_recorders_door(tmp_path):
    """#825's reframe. The recorder's hookwrapper reads the report another
    hook made; where that hook raised there is no report, and the wrapper
    lets pytest's own error stand rather than raise it a second time from
    its own frame, which pluggy reports as the recorder's teardown failing."""
    root, records = project(tmp_path, {"test_ok.py": "def test_ok():\n    pass\n"})
    (root / "tests" / "conftest.py").write_text(RAISES_IN_MAKEREPORT, encoding="utf-8")
    result = pytest_in(root, recording_env(records), "tests")
    output = result.stdout + result.stderr
    assert "PLANTED-IN-MAKEREPORT" in output, output
    assert "specseal_pytest_record" not in output, output
