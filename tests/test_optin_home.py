"""One opt-in signal, read one way: `.specseal/` at the repository root.

It was `_ai/` before 0.10, and `_ai/` stayed readable afterwards so that
nothing would go silent on upgrade. That promise was kept for a population
that turned out to be empty — `_ai/` was the home for two days, and the
repository has no forks and one star. The compatibility read cost two homes to
reason about in every opt-in check, plus a migration notice that could only
fire in a repository nobody had, so it was removed rather than maintained.

The same reasoning removed `docs/parity.md` as a second address for the
migration config. No user-facing document ever named it: the review chain
spec, both READMEs and the skill that writes the file all say
`.specseal/parity.md` and only that.

These cases hold the contract that replaced it — the one address works, and
the old ones are not addresses at all.
"""

import os
import subprocess

import pytest
from conftest import decision_of, fired, load_hook_module, run_hook


@pytest.fixture
def optin():
    return load_hook_module("optin.py", "specseal_optin")


def home(repo):
    (repo / ".specseal").mkdir(exist_ok=True)


def legacy(repo):
    (repo / "_ai").mkdir(exist_ok=True)


# --- the signal itself -----------------------------------------------------


def test_new_home_opts_in(optin, repo):
    home(repo)
    assert optin.opted_in(str(repo))


def test_the_legacy_directory_is_not_an_opt_in(optin, repo):
    """Without this case the constant can come back and everything stays green.

    `_ai/` reads as an ordinary directory now. A repository still holding one
    is a repository that never opted in, which is the same standing as any
    other repository on the machine.
    """
    legacy(repo)
    assert not optin.opted_in(str(repo))
    assert not hasattr(optin, "LEGACY"), "the second address is gone, not renamed"


def test_neither_means_out(optin, repo):
    assert not optin.opted_in(str(repo))


def test_a_path_outside_any_repo_is_out(optin, tmp_path):
    assert not optin.opted_in(str(tmp_path / "nowhere"))


def test_it_answers_the_same_from_a_subdirectory(optin, repo):
    home(repo)
    sub = repo / "a" / "b"
    sub.mkdir(parents=True)
    assert optin.opted_in(str(sub))


# --- the throwaway repository -----------------------------------------------


def scratch(repo):
    (repo / ".specseal" / "scratch").write_text("")


def test_a_scratch_marker_takes_the_opt_in_back(optin, repo):
    """S8. A `.specseal/` directory is the whole opt-in signal, so a git
    repository that exists for thirty seconds as a fixture is indistinguishable
    from a repository under review — and reproducing a gate decision by hand,
    which is what developing these gates consists of, cost a waiver on every
    command (issue #68).

    The marker is written once, by a person, in the repository being thrown
    away. The 17 fixture builders in this suite are untouched: they assert
    that the gates FIRE, and a marker silencing them would invert what they
    test.
    """
    home(repo)
    scratch(repo)
    assert not optin.opted_in(str(repo))


def test_without_the_marker_the_answer_is_the_one_it_always_was(optin, repo):
    """S9. The marker is the whole difference, so removing the condition
    turns the case above red and nothing else moves."""
    home(repo)
    assert optin.opted_in(str(repo))


def test_a_directory_of_that_name_is_not_the_marker(optin, repo):
    """The signal is an empty FILE, and `os.path.exists` did not say so.

    `.specseal/` is committed by design and `.gitignore` does not name
    `scratch`, so a directory created there once turns every gate off in every
    clone of the repository — a kill switch nobody typed. Both the module's
    own docstring and `.specseal/README.md` say "file"; this is the read
    catching up with them.
    """
    home(repo)
    (repo / ".specseal" / "scratch").mkdir()
    assert optin.opted_in(str(repo))


def test_the_scratch_marker_answers_the_same_from_a_subdirectory(optin, repo):
    home(repo)
    scratch(repo)
    sub = repo / "a" / "b"
    sub.mkdir(parents=True)
    assert not optin.opted_in(str(sub))


def test_a_scratch_repository_declares_no_migration_config(optin, repo):
    """The second arm reads the same directory, and a repository that is not
    under review has nothing to compare against an original either."""
    home(repo)
    scratch(repo)
    (repo / ".specseal" / "parity.md").write_text("| Original repo | org/legacy |\n")
    assert optin.parity_config(str(repo)) == ""


# --- the migration config has one address too -------------------------------


def test_the_migration_config_is_found_at_the_one_address(optin, repo):
    home(repo)
    (repo / ".specseal" / "parity.md").write_text("| Original repo | org/legacy |\n")
    # The address, not one platform's spelling of it: `parity_config`
    # builds this with `os.path.join`, and a literal `/` here asserted
    # that the module answers in POSIX on a platform where nothing else
    # does.
    assert optin.parity_config(str(repo)).endswith(
        os.path.join(".specseal", "parity.md")
    )


def test_the_legacy_migration_config_is_not_an_address(optin, repo):
    """`docs/parity.md` was the pre-0.10 location and no document ever said so.

    Leaving the read in meant three documents describing one address while the
    code accepted two, and an audit read that as a documentation gap. Closing
    it by deleting the read makes the documents right, rather than teaching
    three of them about a path nothing has ever written.
    """
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "parity.md").write_text("| Original repo | org/legacy |\n")
    assert optin.parity_config(str(repo)) == ""


def test_the_move_notice_is_gone(optin):
    """Deleted, not muted. A notice with nobody left to warn is a branch that
    runs in no repository and still has to be kept true."""
    for name in ("legacy_only", "MOVE_NOTICE", "notice_due", "NOTICE_DIR"):
        assert not hasattr(optin, name), name


# --- the gates read it -----------------------------------------------------


def payload(cmd, repo):
    return {
        "tool_name": "Bash",
        "session_id": "s1",
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


def test_commit_gate_fires_on_the_new_home(repo):
    home(repo)
    assert fired(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))


def test_commit_gate_stays_silent_on_the_legacy_marker(repo):
    legacy(repo)
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "silent"


def test_review_skill_gate_fires_on_the_new_home(repo):
    home(repo)
    out = run_hook(
        "review-skill-gate.py",
        {
            "tool_name": "Skill",
            "session_id": "s1",
            "tool_input": {"skill": "code-review"},
            "cwd": str(repo),
        },
    )
    assert decision_of(out) == "deny"


def test_the_home_directory_counts_as_documents_not_code(repo):
    """The parity gate compares code against an original; `.specseal/` is neither.

    Asking there would train people to click through the prompt, which costs
    more than the check is worth."""
    gate = load_hook_module("commit-review-gate.py", "commit_review_gate")
    (repo / ".specseal").mkdir()
    (repo / ".specseal" / "map.md").write_text("# map\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    assert not gate.touches_code(
        str(repo), gate.commit_invocations("git commit -m x")[0]
    )


def test_a_code_change_alongside_it_still_counts(repo):
    gate = load_hook_module("commit-review-gate.py", "commit_review_gate")
    (repo / ".specseal").mkdir()
    (repo / ".specseal" / "map.md").write_text("# map\n")
    (repo / "app.py").write_text("x = 1\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True
    )
    assert gate.touches_code(str(repo), gate.commit_invocations("git commit -m x")[0])


def test_the_session_start_hook_says_nothing_in_a_legacy_repo(repo):
    """The repository never opted in, so this hook has no business speaking.

    It used to hear "the home moved" instead — a notice naming four
    destinations, two of which do not exist any more.
    """
    legacy(repo)
    hook = load_hook_module("version-check.py", "vc_move")
    import contextlib
    import io
    import json as _json
    import sys

    sys.stdin = io.StringIO(_json.dumps({"cwd": str(repo), "session_id": "s1"}))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        hook.main()
    assert buf.getvalue() == ""


def test_an_opted_in_repo_at_the_newest_version_hears_nothing(repo):
    home(repo)
    hook = load_hook_module("version-check.py", "vc_moved")
    hook.running = lambda: ((9, 9, 9), "https://example.com/x/y")
    hook.latest = lambda url: (0, 1, 0)
    import contextlib
    import io
    import json as _json
    import sys

    sys.stdin = io.StringIO(_json.dumps({"cwd": str(repo), "session_id": "s1"}))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        hook.main()
    assert buf.getvalue() == ""


def test_the_commit_gate_is_silent_in_a_scratch_repository(repo):
    home(repo)
    scratch(repo)
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "silent"


def test_the_review_skill_gate_is_silent_in_a_scratch_repository(repo):
    home(repo)
    scratch(repo)
    out = run_hook(
        "review-skill-gate.py",
        {
            "tool_name": "Skill",
            "session_id": "s1",
            "tool_input": {"skill": "code-review"},
            "cwd": str(repo),
        },
    )
    assert decision_of(out) == "silent"


def test_the_commit_gate_still_fires_beside_a_scratch_DIRECTORY(repo):
    """The gate-level half of the file-not-directory rule."""
    home(repo)
    (repo / ".specseal" / "scratch").mkdir()
    assert fired(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))


def test_a_scratch_repository_gives_no_standing_over_a_target_it_cannot_read(repo):
    """The stop for an unreadable target is the session's own repository
    speaking, so the marker has to reach that too — otherwise the probe that
    prompted issue #68 keeps prompting, one door along."""
    home(repo)
    scratch(repo)
    out = run_hook("commit-review-gate.py", payload('git -C "$WT" commit -m x', repo))
    assert decision_of(out) == "silent"
