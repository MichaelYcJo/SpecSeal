"""commit-review-gate, review-history-guard, session-lease — via real stdin."""
import os
import subprocess

from conftest import decision_of, run_hook


def payload(cmd, repo, session="s1", tool="Bash", **extra):
    p = {"tool_name": tool, "session_id": session,
         "tool_input": {"command": cmd}, "cwd": str(repo)}
    p.update(extra)
    return p


def opt_in(repo):
    (repo / "_ai").mkdir(exist_ok=True)


def git_dir(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
                          capture_output=True, text=True).stdout.strip()


# --- commit-review-gate ----------------------------------------------------

def test_gate_silent_without_opt_in(repo):
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x", repo))) == "silent"


def test_gate_asks_on_unreviewed_cycle(repo):
    opt_in(repo)
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x", repo))) == "ask"


def test_gate_allows_when_cycle_reviewed(repo):
    opt_in(repo)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    with open(os.path.join(git_dir(repo), "claude-preset-reviewed"), "w") as f:
        f.write(head)
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x", repo))) == "silent"


def test_gate_ignores_non_commit_and_bypass_tag(repo):
    opt_in(repo)
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git log", repo))) == "silent"
    assert decision_of(run_hook("commit-review-gate.py",
                                payload('git commit -m "x [no-review]"', repo))) == "silent"


# --- review-history-guard --------------------------------------------------

def test_history_guard_reminds_posting_without_record(repo):
    opt_in(repo)
    out = run_hook("review-history-guard.py",
                   payload("gh pr comment 42 --body hi", repo))
    assert "PR-42" in out


def test_history_guard_silent_when_record_exists_on_post(repo):
    opt_in(repo)
    (repo / "_ai" / "review-history" / "PR-42").mkdir(parents=True)
    assert run_hook("review-history-guard.py",
                    payload("gh pr comment 42 --body hi", repo)).strip() == ""


def test_history_guard_reminds_reading_with_record(repo):
    opt_in(repo)
    (repo / "_ai" / "review-history" / "PR-42").mkdir(parents=True)
    out = run_hook("review-history-guard.py",
                   payload("gh pr view 42 --json comments", repo))
    assert "tests-todo" in out


def test_history_guard_silent_without_opt_in(repo):
    assert run_hook("review-history-guard.py",
                    payload("gh pr comment 42 --body hi", repo)).strip() == ""


# --- session-lease ---------------------------------------------------------

def leases_of(repo):
    d = os.path.join(git_dir(repo), "claude-preset-leases")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def test_bash_leases_cwd_repo(repo):
    run_hook("session-lease.py", payload("ls", repo, session="sess-a"))
    assert leases_of(repo) == ["sess-a"]


def test_write_leases_edited_files_repo_not_cwd(repo, tmp_path):
    p = {"tool_name": "Write", "session_id": "sess-b",
         "tool_input": {"file_path": str(repo / "f.txt")}, "cwd": str(tmp_path)}
    run_hook("session-lease.py", p)
    assert "sess-b" in leases_of(repo)


def test_lease_outside_any_repo_is_silent(tmp_path):
    p = {"tool_name": "Bash", "session_id": "sess-c",
         "tool_input": {"command": "ls"}, "cwd": str(tmp_path)}
    assert run_hook("session-lease.py", p).strip() == ""


def test_stale_leases_are_pruned(repo):
    import time
    run_hook("session-lease.py", payload("ls", repo, session="sess-old"))
    stale = os.path.join(git_dir(repo), "claude-preset-leases", "sess-old")
    os.utime(stale, (time.time() - 100000,) * 2)
    run_hook("session-lease.py", payload("ls", repo, session="sess-new"))
    assert leases_of(repo) == ["sess-new"]
