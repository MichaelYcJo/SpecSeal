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
    (repo / "seal").mkdir(exist_ok=True)


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


def test_the_warning_names_the_cheap_move_before_the_expensive_one(hook, repo):
    """`/reload-plugins` costs no session and a restart costs the one you are
    in, so the cheaper move is named first.

    What the notice may not do is oversell it. The experiment behind this
    (`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md`,
    run 6) measured one thing: a preloaded skill body handed to a SPAWNED
    AGENT is re-read at a reload. It measured nothing about hooks and nothing
    about agent definitions, and its sentinel sat in the running version's own
    directory, so it says nothing about picking up a newly installed one
    either. A reader infers from silence that the reload covers everything, so
    the gap is stated rather than left.
    """
    opt_in(repo)
    out, _ = drive(hook, repo)
    msg = json.loads(out)["systemMessage"]

    assert "/reload-plugins" in msg, "the notice names only the expensive move"
    assert msg.index("/reload-plugins") < msg.lower().index("restart")

    # Per SENTENCE, not over the whole message: a bare `"measured" in msg` is
    # satisfied by the gap sentence alone, so the reload's claim could drop its
    # source label and stay green. And per CLAIM, not per word — round 1 killed
    # the sentence-split version too, with `a reload was measured to install
    # the new version into this session`, which carries every word this case
    # used to look for. Lowered, so a capitalised `Hooks` cannot make the gap
    # lookup raise instead of assert.
    sentences = [s.strip().lower() for s in msg.replace("\n", " ").split(". ")]

    reload_claim = next((s for s in sentences if "/reload-plugins" in s), "")
    assert reload_claim, "no sentence carries the reload's own claim"
    assert "measured" in reload_claim, "the reload's reach is asserted, not sourced"
    assert "skill bodies" in reload_claim, (
        "the reload's claim names no subject, so it pins a word and not a fact"
    )
    assert any(
        scope in reload_claim for scope in ("already on", "in force", "already running")
    ), (
        "run 6's sentinel sat in the RUNNING version's directory, so what it "
        "measured is a re-read of the copy in force. Without that qualifier the "
        "notice sells the reload as the cheap way to load the new install, "
        "which nothing measured — and the module docstring says the opposite "
        "130 lines up"
    )

    # All THREE unmeasured axes. The third — picking up a newly installed
    # version — is the one run 6's own sentinel placement rules out, and it is
    # the axis the ticket assumed, so it is the one most likely to be dropped.
    gap = next(
        (s for s in sentences if "hooks" in s and "/reload-plugins" not in s), ""
    )
    assert gap, "no sentence states the gap apart from the reload's own claim"
    for axis in ("agent definitions", "installed"):
        assert axis in gap, f"the gap leaves {axis} to silence"
    assert any(
        negation in gap
        for negation in ("nobody", "not measured", "unmeasured", "no one")
    ), "the gap is stated as a fact rather than as an absence of measurement"

    # A required phrase cannot see an ADDED clause. That is the class round 1
    # named, and the assertions above only moved it down one level: each axis
    # is pinned by its own word appearing SOMEWHERE in the sentence, and one
    # negation anywhere in that sentence stands for all three. Round 2 ran the
    # body above verbatim against two mutations that carry every word it looks
    # for and still tell a user the reload picks up the new install:
    #   M6 — the gap keeps its negation for two axes and hands the third back:
    #        `hooks or agent definitions is unmeasured, BUT the version you
    #        just installed is picked up`.
    #   M7 — the reload's own claim keeps its subject and its scope and gains
    #        `and out of the one you just installed`.
    # Both were green. So pin the negative by POSITION rather than by presence.
    # Wherever a sentence names the newly installed version, the clause
    # carrying that mention has to be the clause that calls the pairing
    # unmeasured, and no adversative may follow to hand it back. The weaker
    # sentence-wide check above is implied by this one and is kept for its own
    # failure message.
    for where, sentence in (("the reload's claim", reload_claim), ("the gap", gap)):
        if "install" not in sentence:
            continue
        clause = sentence[sentence.index("install") :]
        for boundary in (",", ";", "."):
            clause = clause.split(boundary)[0]
        assert any(
            negation in clause
            for negation in ("nobody", "not measured", "unmeasured", "no one")
        ), (
            f"{where} names the newly installed version in a clause that does "
            "not call that pairing unmeasured, so the sentence asserts what "
            "run 6's own sentinel placement rules out"
        )
        assert not any(
            adversative in sentence
            for adversative in (" but ", " however", " though ", " except ")
        ), (
            f"{where} carries an adversative, so a negation that reads as "
            "covering the whole sentence governs only the clause before it, "
            "and what follows hands an axis back as a positive claim"
        )


def test_the_notice_agrees_with_the_docstring_about_what_a_reload_re_reads(hook):
    """The module docstring scopes a reload to the copy already in force. A
    notice that sells the reload as the way to load the NEW version contradicts
    the file it lives in, and the contradiction is silent — the docstring is
    130 lines above the string a user actually reads.

    What this case checks is the PRESENCE half of that agreement: the notice
    carries the scope qualifier the docstring states. The absence half — that
    no sentence claims the reload picks up the newly installed version — is
    pinned in the case above, because a mutation that appends `and out of the
    one you just installed` to the reload's claim leaves every phrase this
    case looks for standing.

    The docstring is read whitespace-normalised: it is hand-wrapped prose, so
    `out of that same copy` straddles a line break and a raw `in` is False
    against the very text it is checking.
    """
    doc = " ".join((hook.__doc__ or "").split())
    assert "out of that same copy" in doc, (
        "the docstring no longer scopes the reload to the copy in force, so "
        "this case is comparing the notice against nothing"
    )

    msg = hook.notice((0, 7, 1), (0, 8, 0))
    claim = next((s for s in msg.replace("\n", " ").split(". ") if "/reload" in s), "")
    assert claim, "the notice names no reload for the docstring to disagree with"
    assert any(
        q in claim.lower() for q in ("already on", "in force", "already running")
    ), (
        "the docstring scopes the reload and the notice does not; a user reads the notice"
    )


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
