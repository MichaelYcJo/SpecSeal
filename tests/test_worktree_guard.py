"""worktree-guard: command classification, decision matrix, lease detection.

Decision tests stub session detection — CI runners have no claude processes,
which would otherwise push every branch switch into the conservative-deny
path and hide the logic under test.
"""
import json

import pytest

from conftest import load_hook_module

wg = load_hook_module("worktree-guard.py", "wg")

ACTIVE = [(111, "/tree", 1.0, 0.5, "VS Code")]
IDLE = [(222, "/tree", 400.0, 90.0, "Terminal")]


# --- classify: what counts as a branch switch / worktree creation ---------

@pytest.mark.parametrize("cmd,expected", [
    ("git switch feature/x", "switch"),
    ("git switch -c feature/y", "create+switch"),
    ("git switch -", "switch"),                      # previous branch IS a switch
    ("git checkout -b feature/y", "create+switch"),
    ("git checkout -", "switch"),
    ("git worktree add ../wt feature/x", "worktree-add"),
    ("git worktree list", None),
    ("git worktree remove ../wt", None),
    ("echo git switch feature/x", None),             # prose mention, not a command
    ("cat > g.md <<EOF\nrun: git switch feature/x\nEOF", None),
    ("VAR=1 git switch feature/x", "switch"),        # env assignment prefix
    ("command git switch feature/x", "switch"),
    ("git status", None),
])
def test_classify(repo, cmd, expected):
    got = None
    for seg in wg.split_segments(cmd):
        got = wg.classify(seg, str(repo))
        if got:
            break
    assert got == expected


def test_classify_checkout_of_existing_file_is_restore(repo):
    assert wg.classify("git checkout f.txt", str(repo)) is None


def test_classify_checkout_dwim_remote_branch(repo, tmp_path):
    import subprocess
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(repo), str(clone)], check=True)
    # feature/x exists only as origin/feature/x in the clone
    subprocess.run(["git", "-C", str(clone), "branch", "-Dq", "feature/x"],
                   capture_output=True)
    assert wg.classify("git checkout feature/x", str(clone)) == "switch"


# --- decision matrix (session detection stubbed) --------------------------

def decide(monkeypatch, capsys, repo, command, sessions=([], [], True),
           session_id="me"):
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(wg, "load_input", lambda: {
        "tool_name": "Bash", "session_id": session_id,
        "tool_input": {"command": command}, "cwd": str(repo),
    })
    try:
        wg.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out.strip()
    if not out:
        return "silent", ""
    d = json.loads(out)["hookSpecificOutput"]
    return d["permissionDecision"], d["permissionDecisionReason"]


def test_switch_clean_single_allows(monkeypatch, capsys, repo):
    assert decide(monkeypatch, capsys, repo, "git switch feature/x")[0] == "silent"


def test_switch_dirty_single_asks(monkeypatch, capsys, repo):
    (repo / "f.txt").write_text("changed\n")
    assert decide(monkeypatch, capsys, repo, "git switch feature/x")[0] == "ask"


def test_switch_active_session_denies(monkeypatch, capsys, repo):
    decision, reason = decide(monkeypatch, capsys, repo, "git switch feature/x",
                              sessions=(ACTIVE, [], True))
    assert decision == "deny"
    assert "VS Code" in reason  # host app attribution shown


def test_switch_idle_sessions_ask_with_ages(monkeypatch, capsys, repo):
    decision, reason = decide(monkeypatch, capsys, repo, "git switch feature/x",
                              sessions=([], IDLE, True))
    assert decision == "ask"
    assert "터미널 입력/출력" in reason  # disaggregated signals shown


def test_switch_unreliable_detection_denies(monkeypatch, capsys, repo):
    assert decide(monkeypatch, capsys, repo, "git switch feature/x",
                  sessions=([], [], False))[0] == "deny"


def test_worktree_add_single_denies(monkeypatch, capsys, repo):
    assert decide(monkeypatch, capsys, repo,
                  "git worktree add ../wt feature/x")[0] == "deny"


def test_worktree_add_user_tag_downgrades_to_ask(monkeypatch, capsys, repo):
    assert decide(monkeypatch, capsys, repo,
                  "git worktree add ../wt feature/x  # [worktree-ok]")[0] == "ask"


def test_worktree_add_active_session_asks(monkeypatch, capsys, repo):
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt feature/x",
                  sessions=(ACTIVE, [], True))[0] == "ask"


# --- leases: declared work streams ----------------------------------------

def lease_dir(repo):
    import subprocess
    gd = subprocess.run(["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
                        capture_output=True, text=True).stdout.strip()
    d = f"{gd}/claude-preset-leases"
    import os
    os.makedirs(d, exist_ok=True)
    return d


def test_fresh_foreign_lease_is_active(repo):
    (lambda d: open(f"{d}/other-session", "w").write("1"))(lease_dir(repo))
    entries = wg.fresh_leases(str(repo), "me")
    assert len(entries) == 1 and "[lease: other-se" in entries[0][1]


def test_own_lease_is_ignored(repo):
    (lambda d: open(f"{d}/me", "w").write("1"))(lease_dir(repo))
    assert wg.fresh_leases(str(repo), "me") == []


def test_stale_lease_is_ignored(repo):
    import os, time
    d = lease_dir(repo)
    open(f"{d}/old-session", "w").write("1")
    os.utime(f"{d}/old-session", (time.time() - 3600,) * 2)
    assert wg.fresh_leases(str(repo), "me") == []
