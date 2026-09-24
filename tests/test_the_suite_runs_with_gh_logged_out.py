"""The suite runs with `gh` logged out, on every machine (#510).

A case that fell through its stubs onto a live `gh` passed wherever `gh` was
logged in, which is every developer's machine and the broad gate, and failed
on CI, whose pytest job has no token. `tests/conftest.py` takes `gh`'s login
away at import, so the local answer is CI's answer.

Two cases, because they can fail on different machines. The first reads
what the conftest does to an environment, and it is red on any machine when
the block goes. The second asks `gh` itself, which is the only thing that
can say the block is still enough when a later `gh` finds its login
somewhere new; it can go red only where `gh` is logged in, and it skips
where `gh` is absent.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
CONFTEST = os.path.join(HERE, "conftest.py")
TOKENS = ("GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN", "GITHUB_ENTERPRISE_TOKEN")

# Run the conftest's import-time code in a child whose environment carries
# every token and a config directory of its own, and report what is left.
PROBE = f"""
import json, os, runpy
runpy.run_path({CONFTEST!r})
home = os.environ.get("GH_CONFIG_DIR")
print(json.dumps({{
    "tokens": [n for n in {TOKENS!r} if n in os.environ],
    "home": home,
    "empty": bool(home) and os.path.isdir(home) and not os.listdir(home),
}}))
"""


def test_the_conftest_takes_every_gh_login_away(tmp_path):
    """A6, structural. With all four token variables set and `GH_CONFIG_DIR`
    naming a directory that holds a login, the conftest's import leaves no
    token and points `GH_CONFIG_DIR` at an empty directory of its own."""
    held = tmp_path / "gh-home"
    held.mkdir()
    (held / "hosts.yml").write_text("example.com:\n    oauth_token: x\n", "utf-8")
    env = {**os.environ, "GH_CONFIG_DIR": str(held)}
    env.update({name: "x" for name in TOKENS})
    r = subprocess.run(
        [sys.executable, "-c", PROBE],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
        cwd=HERE,
    )
    assert r.returncode == 0, r.stderr
    seen = json.loads(r.stdout.strip().splitlines()[-1])
    assert seen["tokens"] == [], f"left in the suite's environment: {seen['tokens']}"
    assert seen["home"] != str(held), "GH_CONFIG_DIR still names the login's home"
    assert seen["empty"], f"GH_CONFIG_DIR is not an empty directory: {seen['home']}"


def test_gh_reports_no_login_under_the_suites_environment():
    """A6, behavioural. `gh auth status` under exactly the environment every
    case and child inherits. On a machine where `gh` is logged in, this is
    the case that goes red if the conftest block goes or stops being enough;
    on CI it is green either way, which is the point of the block."""
    gh = shutil.which("gh")
    if gh is None:
        pytest.skip("gh is not on PATH, so nothing here can reach one")
    r = subprocess.run(
        [gh, "auth", "status"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env={**os.environ, "GH_PROMPT_DISABLED": "1"},
    )
    assert r.returncode != 0, (
        "`gh auth status` found a login under the suite's environment, so a "
        "case that reaches a live `gh` passes here and fails on CI:\n"
        f"{r.stdout}{r.stderr}"
    )
