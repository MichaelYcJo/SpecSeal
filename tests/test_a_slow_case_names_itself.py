"""A slow case names itself, and a slow leg is stopped (#841).

The Windows leg grew from 7 to 40 minutes in two weeks, and nothing said
which case had grown: a wall-clock total hides the case that pushed it. Two
halves of a budget now say it. `tests/conftest.py` fails a passing call that
runs past `CASE_CEILING_S`, with a sentence naming the case and its seconds,
and every `pytest` leg of `.github/workflows/test.yml` carries a
`timeout-minutes` past which GitHub fails the job.

The sentence is pinned because a person reads it and acts on it. The hook is
driven through a real inner pytest run that loads this repository's
`conftest.py`, with the ceiling lowered so the run takes a second rather than
a minute and a half.
"""

import os
import re
import subprocess
import sys

import conftest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFTEST = os.path.join(ROOT, "tests", "conftest.py")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "test.yml")


def test_a_call_over_the_ceiling_is_named_with_its_seconds():
    assert conftest.over_the_ceiling("tests/test_x.py::test_y", 91.24) == (
        "tests/test_x.py::test_y ran 91.2 s, over the 90 s ceiling (#841)"
    )


def test_a_call_at_or_under_the_ceiling_says_nothing():
    assert conftest.over_the_ceiling("tests/test_x.py::test_y", 90) is None
    assert conftest.over_the_ceiling("tests/test_x.py::test_y", 0.01) is None


def test_the_ceiling_is_the_one_q6_set():
    """`questions.md` Q6 (a): 1.5 times 55.13 s, rounded up to 30 s."""
    assert conftest.CASE_CEILING_S == 90


INNER_CONFTEST = """\
import importlib.util

_spec = importlib.util.spec_from_file_location("repo_conftest", {path!r})
_repo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_repo)
_repo.CASE_CEILING_S = 0.3
pytest_runtest_makereport = _repo.pytest_runtest_makereport
"""

INNER_TESTS = """\
import time


def test_slow():
    time.sleep(0.6)


def test_quick():
    pass


def test_slow_and_failing():
    time.sleep(0.6)
    assert False, "its own failure"
"""


def test_the_hook_fails_a_slow_passing_call_and_nothing_else(tmp_path):
    (tmp_path / "conftest.py").write_text(
        INNER_CONFTEST.format(path=CONFTEST), encoding="utf-8"
    )
    (tmp_path / "test_inner.py").write_text(INNER_TESTS, encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf"],
        cwd=tmp_path,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    out = run.stdout + run.stderr
    assert run.returncode == 1, out
    assert "2 failed, 1 passed" in out, out
    said = re.search(r"test_inner\.py::test_slow ran (\d+\.\d) s, over the 0\.3 s", out)
    assert said, out
    assert "test_slow_and_failing ran" not in out, out
    assert "its own failure" in out, out


def pytest_job():
    with open(WORKFLOW, encoding="utf-8") as handle:
        text = handle.read()
    return text[text.index("  pytest:") : text.index("  ledger:")]


def test_every_pytest_leg_has_a_timeout_and_the_job_reads_it():
    job = pytest_job()
    entries = [
        ln.strip() for ln in job.splitlines() if ln.strip().startswith("- { os:")
    ]
    assert entries
    budgets = [re.search(r"timeout: (\d+) }$", e) for e in entries]
    assert all(budgets), f"a leg with no timeout: {entries}"
    assert all(int(b.group(1)) > 0 for b in budgets), entries
    assert "\n    timeout-minutes: ${{ matrix.timeout }}\n" in job, (
        "the job does not read the matrix's timeout"
    )
