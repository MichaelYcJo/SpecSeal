"""version-check — the one hook that reaches the network, and its three limits.

Plugin updates are keyed to plugin.json's version and nothing checks for them,
so a release reaches a user only if that user remembers to run two commands.
This hook removes the remembering. Every test here is about what it must NOT
do: no network without the opt-in, none more than daily, and no noise when
anything goes wrong.
"""

import json
import os
import subprocess
import time

import pytest
from conftest import load_hook_module, run_hook


@pytest.fixture
def hook(tmp_path, monkeypatch):
    """The module with its throttle marker redirected into the tmp dir."""
    mod = load_hook_module("version-check.py", "version_check")
    mod.STATE_DIR = str(tmp_path / "state")
    mod.MARKER = os.path.join(mod.STATE_DIR, "version-check")
    return mod


def opt_in(repo):
    (repo / ".specseal").mkdir(exist_ok=True)


def drive(hook, repo, running=(0, 7, 1), remote=(0, 8, 0), monkeypatch=None):
    """Run main() with the version lookups stubbed; return what it printed."""
    calls = []
    hook.running = lambda: (running, "https://example.com/x/y")
    hook.latest = lambda repo_url: (calls.append(repo_url), remote)[1]
    import contextlib
    import io
    import sys

    buf = io.StringIO()
    stdin = sys.stdin
    sys.stdin = io.StringIO(json.dumps({"cwd": str(repo)}))
    try:
        with contextlib.redirect_stdout(buf):
            hook.main()
    finally:
        sys.stdin = stdin
    return buf.getvalue(), calls


# --- it speaks only when there is something to say -------------------------


def test_warns_when_a_newer_release_exists(hook, repo):
    opt_in(repo)
    out, _ = drive(hook, repo, running=(0, 7, 1), remote=(0, 8, 0))
    msg = json.loads(out)["systemMessage"]
    assert "0.8.0" in msg and "0.7.1" in msg


def test_the_warning_names_both_commands_in_order(hook, repo):
    opt_in(repo)
    out, _ = drive(hook, repo)
    msg = json.loads(out)["systemMessage"]
    assert msg.index("marketplace update specseal") < msg.index(
        "update specseal@specseal"
    )
    assert "restart" in msg.lower()


def test_silent_when_current(hook, repo):
    opt_in(repo)
    out, _ = drive(hook, repo, running=(0, 8, 0), remote=(0, 8, 0))
    assert out == ""


def test_silent_when_ahead_of_the_newest_tag(hook, repo):
    """A maintainer's working tree is ahead; telling them to downgrade is wrong."""
    opt_in(repo)
    out, _ = drive(hook, repo, running=(0, 9, 0), remote=(0, 8, 0))
    assert out == ""


# --- the three limits ------------------------------------------------------


def test_no_opt_in_means_no_output_and_no_network(hook, repo):
    out, calls = drive(hook, repo)
    assert out == ""
    assert calls == [], "reached the network in a repo that never opted in"


def test_second_run_the_same_day_makes_no_network_call(hook, repo):
    opt_in(repo)
    drive(hook, repo)
    out, calls = drive(hook, repo)
    assert out == ""
    assert calls == [], "checked twice in one day"


def test_a_day_later_it_checks_again(hook, repo):
    opt_in(repo)
    drive(hook, repo)
    os.utime(hook.MARKER, (0, 0))
    out, calls = drive(hook, repo)
    assert calls, "never rechecked after the interval elapsed"
    assert json.loads(out)["systemMessage"]


def test_offline_stays_silent(hook, repo):
    opt_in(repo)
    out, calls = drive(hook, repo, remote=None)
    assert calls, "did not even try the lookup"
    assert out == ""


def test_a_failed_lookup_costs_minutes_not_the_day(hook, repo):
    """Offline at session start must not spend the notice until tomorrow."""
    opt_in(repo)
    drive(hook, repo, remote=None)
    assert os.path.exists(hook.MARKER), "throttle was never stamped"

    # Still held: a failure must not make every session retry a hanging call.
    out, calls = drive(hook, repo, running=(0, 7, 1), remote=(0, 8, 0))
    assert out == "" and not calls, "retried immediately after a failure"

    # RETRY seconds later — not INTERVAL — it asks again and says its piece.
    # Without the handback the marker would still read as stamped just now,
    # and twenty minutes off a day leaves this silent.
    m = os.path.getmtime(hook.MARKER)
    os.utime(hook.MARKER, (m - hook.RETRY, m - hook.RETRY))
    out, _ = drive(hook, repo, running=(0, 7, 1), remote=(0, 8, 0))
    assert "0.8.0" in out


def test_a_remote_with_no_tags_keeps_the_full_day(hook, repo):
    """An answer, not a failure: nothing to retry for."""
    opt_in(repo)
    out, _ = drive(hook, repo, remote=())
    assert out == ""
    age = time.time() - os.path.getmtime(hook.MARKER)
    assert age < hook.RETRY, "backed off as if the lookup had failed"


def test_an_untagged_remote_answers_rather_than_failing(hook, tmp_path):
    """latest() tells "asked, no tags" from "could not ask" — the throttle
    branches on it, so a stub in `drive` could not carry this one."""
    remote = tmp_path / "untagged.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    assert hook.latest(str(remote)) == (), "a reachable remote read as a failure"
    assert hook.latest(str(tmp_path / "does-not-exist.git")) is None


# --- parsing ---------------------------------------------------------------


def test_version_parsing_accepts_the_repo_tag_format(hook):
    assert hook.parse("v0.7.1") == (0, 7, 1)
    assert hook.parse("0.7.1") == (0, 7, 1)


def test_unrecognised_tag_shapes_are_not_versions(hook):
    """A tag scheme this does not know must degrade to silence, not a wrong warn."""
    for bad in ("specseal--v0.7.1", "release-0.7", "v1.2", "", None, "latest"):
        assert hook.parse(bad) is None, bad


# --- a hook that crashes must not wedge the session ------------------------


def test_malformed_stdin_stays_silent():
    assert run_hook("version-check.py", None) == ""


def test_missing_cwd_stays_silent():
    assert run_hook("version-check.py", {}) == ""


def test_a_path_that_is_not_a_repo_stays_silent(tmp_path):
    assert run_hook("version-check.py", {"cwd": str(tmp_path)}) == ""
