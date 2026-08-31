"""deferral-check: does anything other than this session actually run the
check being deferred?

The failure this exists for: a session narrowed its run to one domain and
wrote "the rest is CI's job". The repository had three workflows — reviewer
assignment, deploy on push to the default branch, and a migration-graph check
— and not one of them ran the test suite. The named answerer did not exist,
so the `unverified` row was a loophole wearing condition 4's clothes.
"""

import os
import subprocess
import sys

import pytest

SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "skills", "verify", "scripts", "deferral_check.py"
)


def run(args, cwd=None):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


@pytest.fixture
def repo(tmp_path):
    """A bare project directory; each test writes the CI it wants to assert on."""
    d = tmp_path / "proj"
    (d / ".github" / "workflows").mkdir(parents=True)
    return d


def workflow(repo, name, text):
    (repo / ".github" / "workflows" / name).write_text(text)


# --- the answerer exists -----------------------------------------------------


def test_pytest_on_pull_request_resolves(repo):
    workflow(
        repo,
        "test.yml",
        "name: Test\non: pull_request\njobs:\n"
        "  t:\n    steps:\n      - run: uv run pytest\n",
    )
    r = run(["--kind", "tests", str(repo)])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "test.yml" in r.stdout
    assert "pytest" in r.stdout


def test_inline_event_list_is_read(repo):
    workflow(
        repo,
        "ci.yml",
        "on: [push, pull_request]\njobs:\n  t:\n    steps:\n      - run: make test\n",
    )
    r = run(["--kind", "tests", str(repo)])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "make test" in r.stdout


# --- the answerer is missing -------------------------------------------------


def test_no_ci_at_all_does_not_resolve(tmp_path):
    d = tmp_path / "bare"
    d.mkdir()
    r = run(["--kind", "tests", str(d)])
    assert r.returncode == 1
    assert "nothing" in r.stdout.lower()


def test_workflows_that_run_no_tests_do_not_resolve(repo):
    """The measured shape: three workflows, none of them a test run."""
    workflow(
        repo,
        "assign.yml",
        "on:\n  pull_request:\n    types: [opened]\njobs:\n"
        "  a:\n    steps:\n      - uses: actions/github-script@v7\n",
    )
    workflow(
        repo,
        "deploy.yml",
        "on:\n  push:\n    branches: [main]\njobs:\n"
        "  d:\n    steps:\n      - run: ./deploy.sh\n",
    )
    r = run(["--kind", "tests", str(repo)])
    assert r.returncode == 1
    assert "assign.yml" not in r.stdout or "no runner" in r.stdout.lower()


def test_runner_on_wrong_trigger_is_named_not_counted(repo):
    """A suite that only runs after merge cannot answer a deferral made before it."""
    workflow(
        repo,
        "post.yml",
        "on:\n  push:\n    branches: [main]\njobs:\n"
        "  t:\n    steps:\n      - run: pytest\n",
    )
    r = run(["--kind", "tests", str(repo)])
    assert r.returncode == 1
    assert "post.yml" in r.stdout
    assert "pull_request" in r.stdout


# --- a local hook is not CI --------------------------------------------------


def test_pre_commit_is_reported_but_does_not_resolve(repo):
    (repo / ".pre-commit-config.yaml").write_text(
        "repos:\n  - repo: local\n    hooks:\n      - id: t\n        entry: pytest\n"
    )
    r = run(["--kind", "tests", str(repo)])
    assert r.returncode == 1
    assert "pre-commit" in r.stdout
    assert "local" in r.stdout.lower()


# --- other CI systems --------------------------------------------------------


def test_gitlab_ci_is_read(tmp_path):
    d = tmp_path / "gl"
    d.mkdir()
    (d / ".gitlab-ci.yml").write_text("test:\n  script:\n    - pytest -q\n")
    r = run(["--kind", "tests", str(d)])
    assert r.returncode == 0, r.stdout + r.stderr
    assert ".gitlab-ci.yml" in r.stdout


# --- kinds are independent ---------------------------------------------------


def test_lint_resolves_while_tests_do_not(repo):
    workflow(
        repo,
        "lint.yml",
        "on: pull_request\njobs:\n  l:\n    steps:\n      - run: ruff check .\n",
    )
    assert run(["--kind", "lint", str(repo)]).returncode == 0
    assert run(["--kind", "tests", str(repo)]).returncode == 1


def test_all_kinds_needs_every_kind(repo):
    workflow(
        repo,
        "lint.yml",
        "on: pull_request\njobs:\n  l:\n    steps:\n      - run: ruff check .\n",
    )
    r = run(["--kind", "all", str(repo)])
    assert r.returncode == 1
    assert "tests" in r.stdout


# --- usage -------------------------------------------------------------------


def test_missing_path_exits_two(tmp_path):
    # Asserts on the message too: a missing *script* also exits 2, which would
    # make this the one test in the file that passes before anything is built.
    r = run(["--kind", "tests", str(tmp_path / "nope")])
    assert r.returncode == 2
    assert "no such path" in (r.stdout + r.stderr).lower()


def test_wrapper_is_present_and_executable():
    wrapper = os.path.join(os.path.dirname(__file__), "..", "bin", "deferral-check")
    assert os.path.isfile(wrapper), "bin/deferral-check missing"
    assert os.access(wrapper, os.X_OK), "bin/deferral-check not executable"
