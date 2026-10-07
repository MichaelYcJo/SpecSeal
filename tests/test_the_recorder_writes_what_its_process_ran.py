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
never a path made from a node id and a rootdir (S23); a report xdist builds
for a crashed worker takes the path of that worker's last report of the same
node, never a node id's (round 5). So every layout rounds
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
    assert lines[-1] == {"kind": "end", "exitstatus": 1, "unplaced": 0, "stopped": []}

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
    """The `realpath` of every file a `test` line or a `collect` line records
    failing."""
    return {
        os.path.realpath(line["path"])
        for line in lines
        if line["kind"] in ("test", "collect") and line["outcome"] == "failed"
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
    assert lines[-1] == {
        "kind": "end",
        "exitstatus": 1,
        "unplaced": 0,
        "stopped": [],
    }, lines


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
    assert lines[-1] == {
        "kind": "end",
        "exitstatus": 1,
        "unplaced": 1,
        "stopped": [],
    }, lines


LOGS_REPORTS_OF_ITS_OWN = """\
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    yield
    built = pytest.TestReport(
        item.nodeid + "::built", item.location, {}, "failed", "built", "call"
    )
    item.ihook.pytest_runtest_logreport(report=built)
    collected = pytest.CollectReport("built::collector", "failed", "built", None)
    item.ihook.pytest_collectreport(report=collected)
"""


def test_a_report_a_plugin_built_without_the_path_is_left_out_and_counted(
    tmp_path,
):
    """S27's other half, `plan.md` Alternative S. A conftest logs a failed
    test report and a failed collect report it built itself, so neither
    passed through the hooks that set the node's path. Each is written as no
    line -- no path is guessed for it -- and each node is counted once on the
    `end` line, while the passing test beside them is recorded."""
    root, records = project(tmp_path, {"test_ok.py": "def test_ok():\n    pass\n"})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "conftest.py").write_text(LOGS_REPORTS_OF_ITS_OWN, encoding="utf-8")
    pytest_in(root, recording_env(records), "tests")
    _, lines = the_one_record(records)
    named = [line for line in lines if "path" in line]
    assert {real(line["path"]) for line in named} == {
        real(root / "tests" / "test_ok.py")
    }, lines
    assert {line["outcome"] for line in named} == {"passed"}, lines
    assert lines[-1]["unplaced"] == 2, lines


def test_a_directory_that_cannot_be_collected_is_recorded_by_its_own_path(
    tmp_path,
):
    """A failed collection's path is the collector's own, and a directory's
    is the directory: the thing that failed. Here its `conftest.py` fails at
    import, and pytest fails `tests/sub`'s collection. Only a TEST whose path
    is a directory is left out; a failed collection of one is written."""
    root, records = project(tmp_path, {})
    sub = root / "tests" / "sub"
    sub.mkdir()
    (sub / "conftest.py").write_text(
        "raise RuntimeError('the conftest fails at import')\n", encoding="utf-8"
    )
    (sub / "test_in.py").write_text("def test_in():\n    pass\n", encoding="utf-8")
    result = pytest_in(root, recording_env(records), "tests")
    assert result.returncode == 2, result.stdout + result.stderr
    _, lines = the_one_record(records)
    collects = [line for line in lines if line["kind"] == "collect"]
    assert {real(line["path"]) for line in collects} == {real(sub)}, lines
    assert lines[-1]["unplaced"] == 0, lines


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


SESSION_WALK_FAILS = """\
def pytest_collect_directory(path, parent):
    if parent is parent.session:
        raise RuntimeError("the session's own walk fails")
"""


def test_a_failed_collection_of_the_session_itself_is_left_out_and_counted(
    tmp_path,
):
    """#825 round 4's 🔴 1. pytest lays a failure it meets while the session
    walks its arguments on the session itself, whose path is the rootdir:
    pytest 7 does so for a conftest's import error anywhere below the root,
    and a plugin's hook can on every build, as here. Written, two different
    breakages shared the rootdir's word and the branch's own read `failing on
    base too`. The session is no file of the tree's, so its failed collection
    is written as no line and counted."""
    root, records = project(tmp_path, {"test_ok.py": "def test_ok():\n    pass\n"})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "session_walk.py").write_text(SESSION_WALK_FAILS, encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(root)])
    result = pytest_in(root, env, "-p", "session_walk", "tests")
    assert result.returncode == 2, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert [line for line in lines if line["kind"] == "collect"] == [], lines
    assert lines[-1]["unplaced"] == 1, lines


CRASHES_ITS_WORKER = """\
import os


def test_ok():
    pass


def test_crash():
    os._exit(1)
"""


def test_a_test_whose_worker_crashed_is_recorded_failing_under_its_file(tmp_path):
    """#825 round 4's 🟡 2. xdist builds the report for a test whose worker
    crashed on the controller itself (`DSession.handle_crashitem`), outside
    the hook that carries the node's path, so the recorder wrote it as no
    line and the file read collected and passing. The crashed test's `setup`
    report carried the node's path, and the crash report of the same node in
    the same session takes it."""
    if importlib.util.find_spec("xdist") is None:
        pytest.skip("pytest-xdist is not installed here")
    root, records = project(tmp_path, {"test_two.py": CRASHES_ITS_WORKER})
    result = run_pytest(root, recording_env(records), "-q", "-n", "2")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    crashed = [
        line
        for line in lines
        if line.get("nodeid") == "tests/test_two.py::test_crash"
        and line["outcome"] == "failed"
    ]
    assert crashed, lines
    assert {real(line["path"]) for line in crashed} == {
        real(root / "tests" / "test_two.py")
    }, lines
    assert lines[-1]["unplaced"] == 0, lines


# Two files outside every default pattern that a conftest collects under ONE
# node id, `check_m.py`, the way pytest 7 names two files outside the rootdir
# from the arguments they came from (`../a/test_m.py`, `../b/test_m.py`).
COLLECTS_TWO_FILES_UNDER_ONE_ID = """\
import pytest


def pytest_collect_file(file_path, parent):
    if file_path.name == "check_m.py":
        return pytest.Module.from_parent(parent, path=file_path, nodeid="check_m.py")
"""

PASSES_ITS_TEST = "def test_crash():\n    pass\n"
CRASHES_IN_ITS_BODY = "import os\n\n\ndef test_crash():\n    os._exit(1)\n"
CRASHES_IN_ITS_FIXTURE = (
    "import os\n\nimport pytest\n\n\n@pytest.fixture\ndef dies():\n"
    "    os._exit(1)\n\n\ndef test_crash(dies):\n    pass\n"
)


@pytest.mark.parametrize(
    "crash", [CRASHES_IN_ITS_BODY, CRASHES_IN_ITS_FIXTURE], ids=["body", "fixture"]
)
def test_a_crash_is_never_placed_by_a_node_id_another_file_shares(tmp_path, crash):
    """#825 round 5's 🔴 1. `a`'s test passes and then `b`'s test, which
    shares its node id, crashes its xdist worker. Round 4 placed the crash
    report by node id, so it took `a`'s path and `a` was written failing:
    at the base, `failing on base too` for the branch's own breakage. The
    crash is placed only by the same worker's last report, where that report
    was of the same node and not its teardown: a crash in the body takes
    `b`'s path from its `setup` report, and a crash in a fixture, before any
    report of `b`, is written as no line and counted. The two directories
    are the arguments; handed as files on pytest 9 the two modules keep ids
    of their own, so pytest 7's file-argument shape is an executed probe
    recorded in the ledger's W1 rather than a case here."""
    if importlib.util.find_spec("xdist") is None:
        pytest.skip("pytest-xdist is not installed here")
    root, records = project(tmp_path, {})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "conftest.py").write_text(COLLECTS_TWO_FILES_UNDER_ONE_ID, encoding="utf-8")
    for name, body in (("a", PASSES_ITS_TEST), ("b", crash)):
        (root / name).mkdir()
        # A package each, so the two modules import under two names.
        (root / name / "__init__.py").write_text("", encoding="utf-8")
        (root / name / "check_m.py").write_text(body, encoding="utf-8")
    result = pytest_in(root, recording_env(records), "-n", "1", "a", "b")
    assert "check_m.py::test_crash" in result.stdout + result.stderr, result.stdout
    _, lines = the_one_record(records)
    a, b = real(root / "a" / "check_m.py"), real(root / "b" / "check_m.py")
    assert failing_paths(lines) == ({b} if crash is CRASHES_IN_ITS_BODY else set()), (
        lines
    )
    assert real(lines[1]["path"]) == a, lines
    if crash is CRASHES_IN_ITS_FIXTURE:
        assert lines[-1]["unplaced"] == 1, lines


def test_a_crash_report_takes_a_path_only_from_its_own_workers_report_of_it():
    """#825 round 5's 🔴 1, at `Recorder.path_of`, for the orders a pytest
    run does not produce on demand. A report with no path takes the path of
    the last report the SAME worker sent, and only where that report was of
    the same node and not its teardown: another worker's report of the same
    node, the same worker's report of another node, and the node's own
    teardown each leave it unplaced."""
    spec = importlib.util.spec_from_file_location(
        "specseal_pytest_record_under_test",
        os.path.join(RECORDER_DIR, "specseal_pytest_record.py"),
    )
    recorder_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder_module)

    class Config:
        rootpath = "/r"

    class Report:
        def __init__(self, nodeid, when, node, path=None):
            self.nodeid, self.when, self.node = nodeid, when, node
            if path is not None:
                setattr(self, recorder_module.PATH_ATTRIBUTE, path)

    one, two = object(), object()
    recorder = recorder_module.Recorder("k", "/d", Config())
    sent = Report("t::x", "call", one, "/r/a.py")
    assert recorder.path_of(sent, "test") == "/r/a.py"
    assert recorder.path_of(Report("t::x", "???", one), "test") == "/r/a.py"
    assert recorder.path_of(Report("t::x", "???", two), "test") is None
    assert recorder.path_of(Report("t::y", "???", one), "test") is None
    recorder.path_of(Report("t::x", "teardown", one, "/r/a.py"), "test")
    assert recorder.path_of(Report("t::x", "???", one), "test") is None
    assert recorder.unplaced == {("test", "t::x"), ("test", "t::y")}


def test_a_worker_made_after_another_is_freed_inherits_none_of_its_reports():
    """#849 (#825 round 6's ⬜ 2, S5), at `Recorder.path_of`. xdist replaces
    a crashed worker with a new controller object, and CPython hands a new
    object the address of one it freed. Keyed on `id()` of a worker it did
    not hold, the map gave a replacement the freed worker's last report, so
    a crash on the new worker took the old node's path. Keyed on `id()` with
    the worker held in the value, the old one is never freed, so no later
    object can take its address (#849 round 1's 🟡 3: keyed on the worker
    itself, a `node` whose hash raised escaped the hook, and two that compared
    equal shared one entry).

    A replacement inside a live xdist run cannot be provoked on demand --
    the terminal reporter keeps the crash report, which holds the old worker
    -- so the case frees the worker itself and makes objects until one takes
    its address, or a thousand have been made. A plain `object()` stands in
    for the worker, as above: CPython 3.13 hands a freed one's address to the
    very next, where an instance of a class of the case's own was measured
    not to reuse it within a thousand."""
    spec = importlib.util.spec_from_file_location(
        "specseal_pytest_record_under_test",
        os.path.join(RECORDER_DIR, "specseal_pytest_record.py"),
    )
    recorder_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder_module)

    class Config:
        rootpath = "/r"

    class Report:
        def __init__(self, nodeid, when, node, path=None):
            self.nodeid, self.when, self.node = nodeid, when, node
            if path is not None:
                setattr(self, recorder_module.PATH_ATTRIBUTE, path)

    recorder = recorder_module.Recorder("k", "/d", Config())
    made = [None] * 1000
    old = object()
    freed = id(old)
    recorder.path_of(Report("t::x", "setup", old, "/r/a.py"), "test")
    del old
    for index in range(len(made)):
        made[index] = object()
        if id(made[index]) == freed:
            break
    for worker in made[: index + 1]:
        assert recorder.path_of(Report("t::x", "???", worker), "test") is None
    assert recorder.unplaced == {("test", "t::x")}

    # Keyed on identity, a `node` no dict could key, or one whose `__hash__`
    # raises, is a sender like any other, and nothing raises.
    class Unhashable:
        def __hash__(self):
            raise ValueError("no hash")

    for unkeyable in ([], Unhashable()):
        assert recorder.path_of(
            Report("t::z", "call", unkeyable, "/r/z.py"), "test"
        ) == ("/r/z.py")
        assert recorder.path_of(Report("t::z", "???", unkeyable), "test") == "/r/z.py"

    # Two distinct workers that compare equal are two senders: the second
    # inherits nothing the first sent.
    class Equal:
        def __eq__(self, other):
            return isinstance(other, Equal)

        def __hash__(self):
            return 0

    first, second = Equal(), Equal()
    recorder.path_of(Report("t::e", "setup", first, "/r/e.py"), "test")
    assert recorder.path_of(Report("t::e", "???", second), "test") is None
    assert recorder.path_of(Report("t::e", "???", first), "test") == "/r/e.py"
    assert recorder.unplaced == {("test", "t::x"), ("test", "t::e")}


# --- what pytest counts, and what stopped the session (#869, #852) ----------

GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")

SETUP_FAILS = "import pytest\n\n\n@pytest.fixture\ndef broken():\n    raise RuntimeError('setup')\n"
EVERY_CATEGORY = """\
import pytest


def test_pass():
    pass


def test_fail():
    assert False


def test_setup_error(broken):
    pass


@pytest.mark.xfail
def test_xfail():
    assert False


@pytest.mark.xfail
def test_xpass():
    pass


@pytest.mark.xfail(strict=True)
def test_xpass_strict():
    pass


def test_skip():
    pytest.skip("no")
"""
SKIPS_ITS_MODULE = "import pytest\n\npytest.skip('whole', allow_module_level=True)\n"
CANNOT_IMPORT = "import a_module_nobody_has\n"


def the_gate():
    spec = importlib.util.spec_from_file_location("broad_gate_for_recorder", GATE)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    return gate


def printed_counts(stdout):
    """pytest's own summary line, the counts alone: its clock and its
    warnings, which no report carries, left off."""
    for line in reversed(stdout.splitlines()):
        line = line.strip("= ")
        if " in " in line and line[:1].isdigit():
            said = line.rsplit(" in ", 1)[0]
            return ", ".join(
                part
                for part in said.split(", ")
                if not part.split(" ")[1].startswith("warning")
            )
    return None


@pytest.mark.parametrize("flags", [(), ("-n", "2")], ids=["plain", "xdist"])
def test_each_test_line_carries_the_category_pytests_own_line_counts(tmp_path, flags):
    """S5 (#869). Each `test` line carries the word pytest's teststatus hook
    gives its report, asked the way the terminal reporter asks it: `error`
    for a failed setup, `xfailed`, `xpassed`, `skipped`, `passed`, `failed`
    for a strict xfail that passed, `""` for a report pytest counts nowhere.
    A module that skips itself is a `collect` line with outcome `skipped`, a
    module that cannot import one with `failed`. Counted the gate's way, the
    record gives exactly the counts pytest's own summary line printed, plain
    and under xdist's controller."""
    root, records = project(
        tmp_path,
        {
            "conftest.py": SETUP_FAILS,
            "test_cats.py": EVERY_CATEGORY,
            "test_modskip.py": SKIPS_ITS_MODULE,
            "test_zbroken.py": CANNOT_IMPORT,
        },
    )
    result = run_pytest(
        root, recording_env(records), "--continue-on-collection-errors", *flags
    )
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    calls = {
        line["nodeid"].rsplit("::", 1)[1]: line["category"]
        for line in lines
        if line["kind"] == "test" and line["when"] == "call"
    }
    assert calls == {
        "test_pass": "passed",
        "test_fail": "failed",
        "test_xfail": "xfailed",
        "test_xpass": "xpassed",
        "test_xpass_strict": "failed",
        "test_skip": "skipped",
    }, lines
    setups = {
        line["nodeid"].rsplit("::", 1)[1]: line["category"]
        for line in lines
        if line["kind"] == "test" and line["when"] == "setup"
    }
    assert setups["test_setup_error"] == "error", lines
    assert setups["test_skip"] == "", lines
    assert {
        (real(line["path"]), line["outcome"])
        for line in lines
        if line["kind"] == "collect"
    } == {
        (real(root / "tests" / "test_modskip.py"), "skipped"),
        (real(root / "tests" / "test_zbroken.py"), "failed"),
    }, lines
    gate = the_gate()
    record = gate.read_record(str(records), KEY, str(root))
    assert record.counts["skipped"] == 2, record.counts
    assert gate.suite_counts(record) == printed_counts(result.stdout), result.stdout


def end_line(records):
    _, lines = the_one_record(records)
    assert lines[-1]["kind"] == "end", lines
    return lines[-1]


EXITS_FROM_ITS_TEST = """\
import pytest


def test_one():
    pass


def test_two():
    pytest.exit("stop here"{code})
"""


@pytest.mark.parametrize("code", [0, 1, 5, None], ids=["0", "1", "5", "none"])
def test_a_pytest_exit_in_a_test_is_written_as_a_stop_whatever_code_it_chose(
    tmp_path, code
):
    """S7 (#852's first limit). `pytest.exit()` in a test, with a return code
    of 0, 1 or 5 -- each an exit a session that ran to its end gives too --
    or none, is written on the `end` line as an `exit` stop carrying pytest's
    message and the code: pytest hands it to `pytest_keyboard_interrupt`
    before the `end` line is written."""
    chosen = "" if code is None else f", returncode={code}"
    root, records = project(
        tmp_path,
        {
            "test_a.py": EXITS_FROM_ITS_TEST.format(code=chosen),
            "test_b.py": "def test_ok():\n    pass\n",
        },
    )
    result = run_pytest(root, recording_env(records))
    expected_exit = 2 if code is None else code
    assert result.returncode == expected_exit, result.stdout + result.stderr
    end = end_line(records)
    assert end["exitstatus"] == expected_exit
    assert end["stopped"] == [
        {"by": "exit", "what": f"Exit: stop here (returncode {code})"}
    ], end


def test_a_keyboard_interrupt_in_a_test_is_written_as_a_stop(tmp_path):
    """S7's neighbour (#852). A `KeyboardInterrupt` in a test is an
    `interrupt` stop on the `end` line, named by its type."""
    root, records = project(
        tmp_path, {"test_a.py": "def test_one():\n    raise KeyboardInterrupt\n"}
    )
    result = run_pytest(root, recording_env(records))
    assert result.returncode == 2, result.stdout + result.stderr
    assert end_line(records)["stopped"] == [
        {"by": "interrupt", "what": "KeyboardInterrupt"}
    ]


FAILS_TWICE = "def test_bad():\n    assert 0\n\n\ndef test_bad_again():\n    assert 0\n"


@pytest.mark.parametrize(
    "flag, count", [("-x", 1), ("--maxfail=2", 2)], ids=["x", "maxfail-2"]
)
def test_a_stop_after_failures_is_written_as_a_stop(tmp_path, flag, count):
    """S8 (#852's second limit). A run without xdist that `-x` or
    `--maxfail` stopped exits 1, as one that ran every test and failed some
    does; pytest leaves `session.shouldfail` set, and the `end` line carries
    it as a `failures` stop. The file after the stop has no line."""
    root, records = project(
        tmp_path,
        {"test_one.py": FAILS_TWICE, "test_two.py": "def test_ok():\n    pass\n"},
    )
    result = run_pytest(root, recording_env(records), flag)
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert lines[-1]["stopped"] == [
        {"by": "failures", "what": f"stopping after {count} failures"}
    ], lines
    assert not any("test_two" in line.get("nodeid", "") for line in lines), lines


@pytest.mark.parametrize(
    "broken, other, exit_code",
    [
        ("test_a_broken.py", "test_b.py", 1),
        ("test_z_broken.py", "test_a.py", 2),
    ],
    ids=["collected-first-exits-1", "collected-last-exits-2"],
)
def test_a_failed_collection_under_x_is_written_as_a_stop_in_either_order(
    tmp_path, broken, other, exit_code
):
    """S8, #852's comment. A failed collection under `-x` exits 1 where
    another collector starts after it and 2 where it was the last; either
    way pytest leaves `session.shouldfail` set, and the `end` line carries a
    `failures` stop."""
    root, records = project(
        tmp_path, {broken: CANNOT_IMPORT, other: "def test_ok():\n    pass\n"}
    )
    result = run_pytest(root, recording_env(records), "-x")
    assert result.returncode == exit_code, result.stdout + result.stderr
    stopped = end_line(records)["stopped"]
    assert {"by": "failures", "what": "stopping after 1 failures"} in stopped, stopped
    # Where it was the last, the run loop raised pytest's `Interrupted`,
    # which reaches the keyboard-interrupt hook with pytest's own sentence.
    interrupted = {"by": "interrupt", "what": "Interrupted: 1 error during collection"}
    assert (interrupted in stopped) is (exit_code == 2), stopped


def test_a_plugins_stop_is_written_as_a_stop(tmp_path):
    """S9 (#852). `--stepwise` stops a run by setting `session.shouldstop`,
    as any plugin can; the `end` line carries it as a `stop`, whatever the
    exit."""
    root, records = project(
        tmp_path,
        {"test_one.py": FAILS_TWICE, "test_two.py": "def test_ok():\n    pass\n"},
    )
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--stepwise", "tests"],
        cwd=str(root),
        env=recording_env(records),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=240,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    stopped = end_line(records)["stopped"]
    assert [entry["by"] for entry in stopped if entry["by"] == "stop"] == ["stop"], (
        stopped
    )


def test_a_teststatus_answer_that_holds_no_word_writes_no_category():
    """#869, at `Recorder.category_of`, for answers no pytest build gives on
    demand. The hook is asked with the report and the config; a word is its
    answer's first element. An answer with no first element, a first element
    that is not a word, and a hook that raises each write `None`, which the
    gate counts under no category -- and nothing is raised out of the
    hook."""
    spec = importlib.util.spec_from_file_location(
        "specseal_pytest_record_for_categories",
        os.path.join(RECORDER_DIR, "specseal_pytest_record.py"),
    )
    recorder_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder_module)
    asked = []

    class Hook:
        answer = ("passed", ".", "PASSED")

        def pytest_report_teststatus(self, report, config):
            asked.append((report, config))
            if isinstance(self.answer, Exception):
                raise self.answer
            return self.answer

    class Config:
        rootpath = "/r"
        hook = Hook()

    config = Config()
    recorder = recorder_module.Recorder("k", "/d", config)
    report = object()
    assert recorder.category_of(report) == "passed"
    assert asked == [(report, config)]
    for answer in (None, (), [], (7, "x", "y"), RuntimeError("a plugin's hook")):
        Config.hook.answer = answer
        assert recorder.category_of(report) is None, answer
    Config.hook.answer = ["", "", ""]
    assert recorder.category_of(report) == ""
