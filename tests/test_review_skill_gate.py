"""review-skill-gate — the built-in review skill asks before it displaces ours.

Claude Code ships a `code-review` skill of its own. When the model picks it
in a repo that also carries specseal's, the user gets a bug-and-cleanup sweep
where they expected a spec-compliance review — and only finds out after the
review has already run. The gate turns that into one prompt beforehand.
"""

import json
import os
import subprocess

from conftest import decision_of, run_hook


def payload(skill, repo, **extra):
    p = {
        "tool_name": "Skill",
        "session_id": "s1",
        "tool_input": {"skill": skill},
        "cwd": str(repo),
    }
    p.update(extra)
    return p


def opt_in(repo):
    (repo / ".specseal").mkdir(exist_ok=True)


def run(skill, repo, **extra):
    return run_hook("review-skill-gate.py", payload(skill, repo, **extra))


# --- the contended name ----------------------------------------------------


def test_denies_the_builtin_so_the_user_is_offered_a_choice(repo):
    opt_in(repo)
    assert decision_of(run("code-review", repo)) == "deny"


def test_reason_asks_for_a_two_option_question(repo):
    opt_in(repo)
    reason = json.loads(run("code-review", repo))["hookSpecificOutput"][
        "permissionDecisionReason"
    ]
    assert "AskUserQuestion" in reason
    assert "/specseal:code-review" in reason
    assert "/code-review" in reason


def test_second_call_in_the_same_session_goes_through(repo):
    """The user who picks the built-in must not be denied their retry."""
    opt_in(repo)
    assert decision_of(run("code-review", repo)) == "deny"
    assert decision_of(run("code-review", repo)) == "silent"


def test_a_different_session_is_asked_again(repo):
    opt_in(repo)
    assert decision_of(run("code-review", repo)) == "deny"
    assert decision_of(run("code-review", repo, session_id="s2")) == "deny"


def test_without_a_session_id_it_asks_instead_of_denying(repo):
    """No id means no way to record the question, and a deny would repeat.

    `ask` cannot loop: approving is itself the way through."""
    opt_in(repo)
    p = payload("code-review", repo)
    del p["session_id"]
    assert decision_of(run_hook("review-skill-gate.py", p)) == "ask"


# --- a linked worktree is a repository too ---------------------------------


def test_it_fires_in_a_linked_worktree(repo, tmp_path):
    """Splitting review work into a worktree is the flow the README steers
    toward, and the gate went silent on every call made from one.

    `.git` is a FILE there, pointing at `<main>/.git/worktrees/<name>`, so a
    git-dir built as `<root>/.git` is not a directory and the marker write
    raises. An unwritable marker reads as "already asked", so the question
    separating the two review skills disappeared -- silently, every call.
    """
    opt_in(repo)
    # git tracks files, not directories, so the opt-in needs one to ride on --
    # and it has to be committed, or the worktree does not see it at all.
    (repo / ".specseal" / "map.md").write_text("# map\n")
    git = lambda *a: subprocess.run(
        ["git", "-C", str(repo), *a],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    git("add", "-A")
    git("commit", "-qm", "opt in")
    wt = tmp_path / "wt"
    git("worktree", "add", "-q", str(wt), "-b", "wt/x")

    assert decision_of(run("code-review", wt)) == "deny"
    # and the marker landed in the worktree's OWN git dir, so the second call
    # goes through there -- a deny with nowhere to record it would repeat.
    assert decision_of(run("code-review", wt)) == "silent"
    gd = subprocess.run(
        ["git", "-C", str(wt), "rev-parse", "--absolute-git-dir"],
        check=True,  # or `gd` is "" and the join below reads the CWD instead,
        capture_output=True,  # failing as "no such file" and hiding the marker
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    assert os.path.isfile(os.path.join(gd, "specseal-review-choice", "s1"))
    # The isolation runs the other way too: the worktree's marker did not
    # spend the main tree's question, so the same session is still asked
    # there. That is what "once per session per working tree" means, and
    # without this the gate could satisfy the asserts above by recording
    # every tree's question in one shared place.
    assert decision_of(run("code-review", repo)) == "deny"


# --- everything else stays silent ------------------------------------------


def test_silent_without_opt_in(repo):
    assert decision_of(run("code-review", repo)) == "silent"


def test_silent_for_our_own_skill(repo):
    opt_in(repo)
    assert decision_of(run("specseal:code-review", repo)) == "silent"


def test_silent_for_unrelated_skills(repo):
    opt_in(repo)
    for name in ("debug", "specseal:implement", "code-reviewer", "review"):
        assert decision_of(run(name, repo)) == "silent", name


def test_silent_for_a_name_that_merely_contains_it(repo):
    """Substring matching would swallow a third-party skill by accident."""
    opt_in(repo)
    for name in ("acme:code-review", "code-review-strict", "my-code-review"):
        assert decision_of(run(name, repo)) == "silent", name


# --- a gate that crashes must let the work through -------------------------


def test_malformed_payload_stays_silent(repo):
    assert (
        decision_of(run_hook("review-skill-gate.py", {"tool_name": "Skill"}))
        == "silent"
    )


def test_missing_cwd_stays_silent(repo):
    assert (
        decision_of(
            run_hook(
                "review-skill-gate.py",
                {"tool_name": "Skill", "tool_input": {"skill": "code-review"}},
            )
        )
        == "silent"
    )
