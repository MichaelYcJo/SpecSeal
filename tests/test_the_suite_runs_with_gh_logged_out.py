"""The suite runs with `gh` logged out, on every machine (#510).

A case that fell through its stubs onto a live `gh` passed wherever `gh` was
logged in, which is every developer's machine and the broad gate, and failed
on CI, whose pytest job has no token. `tests/conftest.py` takes `gh`'s login
away at import, so the local answer is CI's answer.

Two cases, because they can fail on different machines. The first reads
what the conftest does to an environment, and it is red on any machine when
the block goes. The second asks `gh` which token it would send, which is the
only thing that can say the block is still enough when a later `gh` finds
its login somewhere new; it can go red only where `gh` is logged in, and it
skips where `gh` is absent.
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

# Pinned verbatim: the conftest's placeholder, which is not a credential.
NOT_A_GH_TOKEN = "specseal-suite-runs-with-gh-logged-out"

# Run the conftest's import-time code in a child whose environment carries
# every token and a config directory of its own, and report what is left.
PROBE = f"""
import json, os, runpy
runpy.run_path({CONFTEST!r})
home = os.environ.get("GH_CONFIG_DIR")
print(json.dumps({{
    "tokens": {{n: os.environ[n] for n in {TOKENS!r} if n in os.environ}},
    "home": home,
    "empty": bool(home) and os.path.isdir(home) and not os.listdir(home),
}}))
"""


def test_the_conftest_takes_every_gh_login_away(tmp_path):
    """A6, structural. With all four token variables set and `GH_CONFIG_DIR`
    naming a directory that holds a login, the conftest's import leaves the
    two variables `gh` reads first holding a placeholder no server accepts,
    removes the other two, and points `GH_CONFIG_DIR` at an empty directory
    of its own. A token variable that is set keeps `gh` from falling back to
    the login it keeps in the OS keyring."""
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
    assert seen["tokens"] == {
        "GH_TOKEN": NOT_A_GH_TOKEN,
        "GH_ENTERPRISE_TOKEN": NOT_A_GH_TOKEN,
    }, f"the suite's token variables: {sorted(seen['tokens'])}"
    assert seen["home"] != str(held), "GH_CONFIG_DIR still names the login's home"
    assert seen["empty"], f"GH_CONFIG_DIR is not an empty directory: {seen['home']}"
    # The directory is the run's own, and it goes when the run does.
    assert not os.path.exists(seen["home"]), f"left behind: {seen['home']}"


def test_the_token_gh_would_send_is_not_a_login():
    """A6, behavioural. `gh auth token` takes the same path as every API
    call -- the variables, then `hosts.yml`, then the keyring's active slot --
    and needs no network. `gh auth status` does not read the keyring without
    a `hosts.yml`, so it reported no login on a machine where `gh api` was
    still logged in. Red on a keyring machine against a block that only
    empties `GH_CONFIG_DIR`. The token is never printed."""
    gh = shutil.which("gh")
    if gh is None:
        pytest.skip("gh is not on PATH, so nothing here can reach one")
    r = subprocess.run(
        [gh, "auth", "token"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env={**os.environ, "GH_PROMPT_DISABLED": "1"},
    )
    token = r.stdout.strip()
    assert r.returncode != 0 or token == NOT_A_GH_TOKEN, (
        "`gh auth token` found a login under the suite's environment "
        f"(exit {r.returncode}, {len(token)} characters, not printed), so a "
        "case that reaches a live `gh` passes here and fails on CI"
    )


def test_contributing_says_the_suite_runs_logged_out():
    """A6, the reader's half (`agent-contract` §14). A contributor whose case
    goes red on a machine where `gh` works everywhere else needs to find why
    in the section that tells them how to run the suite."""
    path = os.path.join(HERE, "..", "CONTRIBUTING.md")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    section = text.split("## Running the checks", 1)[1].split("\n## ", 1)[0]
    prose = " ".join(section.split())
    for needle in (
        "The suite runs with `gh` logged out, on your machine as on CI.",
        "it points `GH_CONFIG_DIR` at an empty directory",
        "sets `GH_TOKEN` and `GH_ENTERPRISE_TOKEN` to a value no server accepts",
        "without a token variable, `gh` reads the login it keeps in your OS keyring",
        *(f"`{name}`" for name in TOKENS),
        "A case that needs `gh` stubs it.",
    ):
        assert needle in prose, f"CONTRIBUTING.md §Running the checks lacks: {needle}"
    assert "removes `GH_TOKEN`" not in prose, (
        "CONTRIBUTING.md still says the suite removes `GH_TOKEN`, which would "
        "leave `gh` reading the login in the OS keyring"
    )
