"""commit-review-gate, review-history-guard, session-lease — via real stdin."""

import json
import os
import subprocess

from conftest import (
    decision_of,
    declare_routing,
    fired,
    load_hook_module,
    rounds_dir,
    run_hook,
)

# The gate's own name for the directory it records the question in. Read
# from the module rather than written again, so a rename moves both.
CHOICE_DIR = load_hook_module("commit-review-gate.py", "gate_choice_dir").CHOICE_DIR


def payload(cmd, repo, session="s1", tool="Bash", **extra):
    p = {
        "tool_name": tool,
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }
    p.update(extra)
    return p


def opt_in(repo):
    (repo / "seal").mkdir(exist_ok=True)


def git_dir(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


# --- commit-review-gate ----------------------------------------------------


def test_gate_silent_without_opt_in(repo):
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "silent"
    )


def test_gate_denies_so_the_user_is_offered_both_ways_on(repo):
    """Declining an `ask` is a bare "No": the user who wanted the other way on
    has to retype the command. A deny gives the model the turn back."""
    opt_in(repo)
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "deny"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "AskUserQuestion" in reason
    assert "[no-review]" in reason and "review chain" in reason.lower()


def test_the_next_attempt_gets_the_plain_prompt(repo):
    """Denying every time would trap a session whose answer the gate cannot
    read off the command. The fallback is the prompt this gate always had."""
    opt_in(repo)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "deny"
    )
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "ask"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "Approving is the waiver" in reason


def test_a_different_session_is_asked_the_question_too(repo):
    opt_in(repo)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "deny"
    )
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload("git commit -m x", repo, session="s2")
            )
        )
        == "deny"
    )


def test_an_unwritable_marker_counts_as_already_asked(repo):
    """The rule the chain spec states: a marker that cannot be recorded means
    the question is treated as asked. Inverted, the deny repeats forever in
    exactly the environments that cannot write, and the commit never lands."""
    opt_in(repo)
    # Unwritable on BOTH platforms. `os.chmod(gd, 0o500)` is a no-op for a
    # directory on Windows -- the mode bits are accepted and the write still
    # succeeds -- so the gate recorded the question, answered `silent`, and
    # the rule this case states went unheld on the one platform where an
    # unwritable git-dir is most likely.
    #
    # Occupying the marker directory's own name with a file raises `OSError`
    # everywhere: `makedirs(..., exist_ok=True)` re-raises when the name it
    # finds is not a directory.
    gd = git_dir(repo)
    with open(os.path.join(gd, CHOICE_DIR), "w", encoding="utf-8") as f:
        f.write("not a directory")
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "ask"
    )


def test_a_session_id_with_separators_stays_inside_the_git_dir(repo):
    """The id names a file. Measured on the sibling guard: `../../escaped`
    put an empty file at the repository root."""
    opt_in(repo)
    run_hook(
        "commit-review-gate.py",
        payload("git commit -m x", repo, session="../../escaped"),
    )
    assert not (repo / "escaped").exists()
    assert os.path.isfile(
        os.path.join(git_dir(repo), "specseal-commit-choice", "escaped")
    )


def test_without_a_session_id_it_asks_instead_of_denying(repo):
    """No id means nowhere to record that the question was asked, and a deny
    would then repeat forever. `ask` cannot loop: approving is the way out."""
    opt_in(repo)
    p = payload("git commit -m x", repo)
    del p["session_id"]
    assert decision_of(run_hook("commit-review-gate.py", p)) == "ask"


def test_gate_allows_when_cycle_reviewed(repo):
    opt_in(repo)
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    with open(os.path.join(git_dir(repo), "specseal-reviewed"), "w") as f:
        f.write(head)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "silent"
    )


def test_gate_ignores_non_commit_and_bypass_tag(repo):
    opt_in(repo)
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git log", repo)))
        == "silent"
    )
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload("git commit -m x [no-review]", repo)
            )
        )
        == "silent"
    )


def test_the_marker_inside_a_message_is_prose_not_a_waiver(repo):
    """`-m "drop [no-review] from the docs"` describes work; it does not waive.

    A substring test cannot tell a waiver from a sentence about one, and the
    message body is where people write sentences."""
    opt_in(repo)
    assert fired(
        run_hook(
            "commit-review-gate.py", payload('git commit -m "x [no-review]"', repo)
        )
    )


# --- review-history-guard --------------------------------------------------


def test_history_guard_reminds_posting_without_record(repo):
    opt_in(repo)
    item = declare_routing(repo)
    out = run_hook(
        "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
    )
    assert item.name in out, out


def test_history_guard_silent_when_record_exists_on_post(repo):
    opt_in(repo)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Target SHA | abc |\n")
    assert (
        run_hook(
            "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
        ).strip()
        == ""
    )


def test_history_guard_says_nothing_where_no_work_item_is_declared(repo):
    """The work item is the key now. Without a declaration there is no
    directory to name, and a reminder that names nothing is noise."""
    opt_in(repo)
    assert (
        run_hook(
            "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
        ).strip()
        == ""
    )


def test_history_guard_reminds_reading_with_record(repo):
    opt_in(repo)
    item = declare_routing(repo)
    (rounds_dir(item) / "round-1.md").write_text("| Target SHA | abc |\n")
    out = run_hook(
        "review-history-guard.py", payload("gh pr view 42 --json comments", repo)
    )
    assert "tests-todo" in out


def test_history_guard_silent_without_opt_in(repo):
    assert (
        run_hook(
            "review-history-guard.py", payload("gh pr comment 42 --body hi", repo)
        ).strip()
        == ""
    )


# --- session-lease ---------------------------------------------------------


def leases_of(repo):
    d = os.path.join(git_dir(repo), "specseal-leases")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def test_bash_leases_cwd_repo(repo):
    run_hook("session-lease.py", payload("ls", repo, session="sess-a"))
    assert leases_of(repo) == ["sess-a"]


def test_write_leases_edited_files_repo_not_cwd(repo, tmp_path):
    p = {
        "tool_name": "Write",
        "session_id": "sess-b",
        "tool_input": {"file_path": str(repo / "f.txt")},
        "cwd": str(tmp_path),
    }
    run_hook("session-lease.py", p)
    assert "sess-b" in leases_of(repo)


def test_lease_outside_any_repo_is_silent(tmp_path):
    p = {
        "tool_name": "Bash",
        "session_id": "sess-c",
        "tool_input": {"command": "ls"},
        "cwd": str(tmp_path),
    }
    assert run_hook("session-lease.py", p).strip() == ""


def test_stale_leases_are_pruned(repo):
    import time

    run_hook("session-lease.py", payload("ls", repo, session="sess-old"))
    stale = os.path.join(git_dir(repo), "specseal-leases", "sess-old")
    os.utime(stale, (time.time() - 100000,) * 2)
    run_hook("session-lease.py", payload("ls", repo, session="sess-new"))
    assert leases_of(repo) == ["sess-new"]
