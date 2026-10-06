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
    assert lines[-1] == {"kind": "end", "exitstatus": 1}

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


def test_a_pyargs_module_name_is_not_read_as_a_path_outside_the_rootdir(tmp_path):
    """#825 round 1. The recorder refuses a session handed a path outside its
    rootdir, and an argument that is no path here -- a `--pyargs` module
    name -- is passed over rather than read as one, so such a run still
    records its tests under the module that collected them."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(root / "tests")])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "no:cacheprovider",
            "-q",
            "--pyargs",
            "test_mixed",
        ],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=240,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    failed = [
        os.path.basename(line["path"])
        for line in lines
        if line["kind"] == "test" and line["outcome"] == "failed"
    ]
    assert failed == ["test_mixed.py"], lines


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


def records_written(records):
    return [f for f in os.listdir(str(records)) if f.endswith(".jsonl")]


def test_a_pyargs_module_outside_the_rootdir_writes_no_record(tmp_path):
    """#825 round 2. pytest finds a `--pyargs` package where Python imports
    it from, outside the rootdir here, and names its `test_mixed.py` against
    the package: `test_mixed.py`, the name a file at the rootdir has. The
    argument is no path, so the refusal used to pass it over and the record
    named another file."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    package = tmp_path / "site" / "extpkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(tmp_path / "site")])
    result = pytest_in(root, env, "--pyargs", "extpkg")
    assert result.returncode == 1, result.stdout + result.stderr
    assert records_written(records) == [], records_of(records)


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_a_rootdir_named_through_a_symlink_writes_no_record(tmp_path):
    """#825 round 2. pytest compares a path with its rootdir lexically, so a
    `--rootdir` spelled through a symlink puts `tests/` outside it, and
    `tests/test_mixed.py` is named `test_mixed.py`. A `realpath` comparison
    called it inside."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    link = tmp_path / "link"
    link.symlink_to(root, target_is_directory=True)
    result = pytest_in(root, recording_env(records), "--rootdir", str(link), "tests")
    assert result.returncode == 1, result.stdout + result.stderr
    assert records_written(records) == [], records_of(records)


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_an_argument_named_through_a_symlink_writes_no_record(tmp_path):
    """#825 round 2, the same branch from the other side. The rootdir is the
    project, named by `-c` as it is, and the argument reaches `tests/`
    through a symlink, so pytest finds it outside the rootdir and names
    `tests/test_mixed.py` `test_mixed.py`."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
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
    assert records_written(records) == [], records_of(records)


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_a_symlinked_directory_under_the_rootdir_is_recorded_by_its_own_name(
    tmp_path,
):
    """#825 round 2. A directory under the rootdir that is a symlink to a
    place outside it is named by pytest under the rootdir, and it was
    refused only when it was spelled as an argument."""
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


def test_a_collector_built_for_a_path_no_argument_holds_writes_no_record(tmp_path):
    """#825 round 2, the branch the arguments cannot show. A conftest builds
    a collector for a directory outside the rootdir and outside every
    argument, so pytest gives its tests the parent's node id and a `::`
    name, `.::outside::test_far.py::test_out`, whose path is the rootdir
    itself. A test line whose path is no file is not the test's module, so
    the session's record is abandoned: the strict side."""
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
    assert records_written(records) == [], records_of(records)
