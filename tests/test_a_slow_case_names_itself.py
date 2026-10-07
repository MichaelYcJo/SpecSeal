"""A slow case names itself, and a slow leg is stopped (#841).

The Windows leg grew from 7 to 40 minutes in two weeks, and nothing said
which case had grown: a wall-clock total hides the case that pushed it. Two
halves of a budget now say it. `tests/conftest.py` fails a passing call that
runs past `CASE_CEILING_S`, with a sentence naming the case and its seconds,
and every `pytest` leg of `.github/workflows/test.yml` carries a
`timeout-minutes` past which GitHub fails the job. `SPECSEAL_CASE_CEILING_S`
raises the ceiling for one run on a busy machine; CI never sets it.

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
import pytest
from test_ci_gives_the_checks_what_they_need import jobs, pytest_matrix, read

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFTEST = os.path.join(ROOT, "tests", "conftest.py")


def test_a_call_over_the_ceiling_is_named_with_its_seconds(monkeypatch):
    monkeypatch.setattr(conftest, "CASE_CEILING_S", 90)
    assert conftest.over_the_ceiling("tests/test_x.py::test_y", 91.24) == (
        "tests/test_x.py::test_y ran 91.2 s, over the 90 s ceiling (#841). On a "
        "machine running other suites, SPECSEAL_CASE_CEILING_S=<seconds> raises "
        "it for one run; CI never sets it"
    )


def test_a_call_at_or_under_the_ceiling_says_nothing(monkeypatch):
    monkeypatch.setattr(conftest, "CASE_CEILING_S", 90)
    assert conftest.over_the_ceiling("tests/test_x.py::test_y", 90) is None
    assert conftest.over_the_ceiling("tests/test_x.py::test_y", 0.01) is None


def test_the_ceiling_is_the_one_q6_set():
    """`questions.md` Q6 (a): 1.5 times 55.77 s, rounded up to 30 s."""
    assert conftest.CASE_CEILING_DEFAULT_S == 90


def ceiling_read_by_a_fresh_import(**variables):
    """`CASE_CEILING_S` as a new interpreter importing `conftest.py` reads
    it, with `variables` set and the ceiling's variable otherwise unset."""
    env = {k: v for k, v in os.environ.items() if k != conftest.CEILING_VARIABLE}
    env.update(variables)
    program = (
        "import importlib.util\n"
        f"spec = importlib.util.spec_from_file_location('c', {CONFTEST!r})\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        "print(mod.CASE_CEILING_S)\n"
    )
    run = subprocess.run(
        [sys.executable, "-c", program],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=60,
    )
    assert run.returncode == 0, run.stderr
    return run.stdout.strip()


def test_the_variable_raises_the_ceiling_for_one_run_and_unset_is_ninety():
    """Round 1's 🟡 2. A busy machine may raise the ceiling on purpose; a run
    that sets nothing, which is every CI run, reads Q6's 90."""
    assert conftest.CEILING_VARIABLE == "SPECSEAL_CASE_CEILING_S"
    assert ceiling_read_by_a_fresh_import() == "90"
    assert ceiling_read_by_a_fresh_import(SPECSEAL_CASE_CEILING_S="240") == "240"


def test_an_empty_variable_is_unset_and_a_decimal_is_seconds():
    """Round 2's 🟡 2. An empty value used to stop conftest's import, and a
    decimal one with it."""
    assert ceiling_read_by_a_fresh_import(SPECSEAL_CASE_CEILING_S="") == "90"
    assert ceiling_read_by_a_fresh_import(SPECSEAL_CASE_CEILING_S="120.5") == "120.5"


def test_a_ceiling_of_zero_or_less_is_refused_naming_the_variable():
    """Round 2's 🟡 2. Zero or a negative value used to fail every case,
    and a word stopped the import with `int()`'s traceback."""
    for bad in ("0", "-5", "abc"):
        with pytest.raises(ValueError, match="SPECSEAL_CASE_CEILING_S="):
            conftest.ceiling_from({"SPECSEAL_CASE_CEILING_S": bad})


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


def test_every_pytest_leg_has_a_timeout_and_the_job_reads_it():
    text = read("test.yml")
    entries = pytest_matrix(text)
    assert entries
    budgets = [e.get("timeout", "") for e in entries]
    assert all(b.isdigit() for b in budgets), f"a leg with no timeout: {entries}"
    assert all(int(b) > 0 for b in budgets), entries
    job = jobs(text)["pytest"]
    assert "\n    timeout-minutes: ${{ matrix.timeout }}\n" in job, (
        "the job does not read the matrix's timeout"
    )
