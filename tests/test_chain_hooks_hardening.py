"""Hardening cases: prose-mention false positives, cycle edges, lease isolation."""

import json
import os
import subprocess

from conftest import decision_of, run_hook


def payload(cmd, repo, session="s1"):
    return {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


def opt_in(repo):
    (repo / "_ai").mkdir(exist_ok=True)


def git(repo, *a):
    return subprocess.run(
        ["git", "-C", str(repo), *a], capture_output=True, text=True, check=False
    )


# --- gate: prose mentions must not gate (regression for the fixed FP) -----


def test_gate_ignores_echoed_git_commit(repo):
    opt_in(repo)
    assert (
        decision_of(
            run_hook("commit-review-gate.py", payload("echo git commit -m x", repo))
        )
        == "silent"
    )


def test_gate_ignores_heredoc_mentions(repo):
    opt_in(repo)
    cmd = "cat > doc.md <<EOF\nrun: git commit -m x\nEOF"
    assert (
        decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "silent"
    )


def test_gate_catches_heredoc_message_commit(repo):
    # The commit form Claude Code itself is instructed to use: the message
    # arrives via $(cat <<'EOF' ...) inside double quotes. A quote-blind
    # splitter shredded this and the gate stayed silent.
    opt_in(repo)
    cmd = "git commit -m \"$(cat <<'EOF'\nfix: thing\n\nbody\nEOF\n)\""
    assert decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "ask"


def test_gate_catches_separators_inside_message(repo):
    opt_in(repo)
    for cmd in (
        'git commit -m "fix && update deps"',
        'git commit -m "a; b"',
        'git commit -m "line1\nline2"',
    ):
        assert (
            decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "ask"
        ), cmd


def test_gate_fails_closed_on_unparseable_commit(repo):
    # Unbalanced quotes defeat tokenization; if git+commit appear anyway,
    # asking beats exempting exactly the commands too gnarly to parse.
    opt_in(repo)
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload('git commit -m "unbalanced', repo)
            )
        )
        == "ask"
    )
    assert (
        decision_of(
            run_hook("commit-review-gate.py", payload('echo "unbalanced git', repo))
        )
        == "silent"
    )


def test_gate_catches_commit_after_cd_chain(repo):
    opt_in(repo)
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload("cd sub && git commit -m x", repo)
            )
        )
        == "ask"
    )


def test_gate_catches_env_prefixed_commit(repo):
    opt_in(repo)
    cmd = "GIT_AUTHOR_DATE=2026-01-01T00:00:00 git commit -m x"
    assert decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "ask"


def test_gate_rearms_after_commit_moves_head(repo):
    opt_in(repo)
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    with open(os.path.join(gd, "specseal-reviewed"), "w") as f:
        f.write(head)
    (repo / "f.txt").write_text("more\n")
    git(repo, "commit", "-qam", "next")  # cycle closes, mark goes stale
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "ask"
    )


def test_gate_ignores_non_bash_tools(repo):
    opt_in(repo)
    p = {
        "tool_name": "Write",
        "session_id": "s",
        "tool_input": {"file_path": str(repo / "x")},
        "cwd": str(repo),
    }
    assert decision_of(run_hook("commit-review-gate.py", p)) == "silent"


# --- history guard: prose mentions must not remind ------------------------


def test_history_guard_ignores_echoed_gh(repo):
    opt_in(repo)
    assert (
        run_hook(
            "review-history-guard.py", payload("echo gh pr comment 42", repo)
        ).strip()
        == ""
    )


def test_history_guard_catches_gh_after_chain(repo):
    opt_in(repo)
    out = run_hook(
        "review-history-guard.py", payload("cd x && gh pr comment 7 --body hi", repo)
    )
    assert "PR-7" in out


# --- session-lease: repo resolution and isolation -------------------------


def leases_of(repo):
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    d = os.path.join(gd, "specseal-leases")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def test_edit_tool_leases_like_write(repo, tmp_path):
    p = {
        "tool_name": "Edit",
        "session_id": "sess-e",
        "tool_input": {"file_path": str(repo / "f.txt")},
        "cwd": str(tmp_path),
    }
    run_hook("session-lease.py", p)
    assert "sess-e" in leases_of(repo)


def test_bash_in_subdir_leases_repo_root(repo):
    (repo / "sub").mkdir()
    p = {
        "tool_name": "Bash",
        "session_id": "sess-sub",
        "tool_input": {"command": "ls"},
        "cwd": str(repo / "sub"),
    }
    run_hook("session-lease.py", p)
    assert "sess-sub" in leases_of(repo)


def test_linked_worktree_lease_stays_isolated(repo, tmp_path):
    wt = tmp_path / "wt"
    git(repo, "worktree", "add", "-q", str(wt), "feature/x")
    p = {
        "tool_name": "Bash",
        "session_id": "sess-wt",
        "tool_input": {"command": "ls"},
        "cwd": str(wt),
    }
    run_hook("session-lease.py", p)
    # the worktree session's lease lands in the worktree's own git-dir,
    # so it does NOT count against the main tree (already-isolated rule)
    assert "sess-wt" not in leases_of(repo)


def test_missing_session_id_falls_back_to_pid(repo):
    p = {"tool_name": "Bash", "tool_input": {"command": "ls"}, "cwd": str(repo)}
    run_hook("session-lease.py", p)
    assert any(name.startswith("pid-") for name in leases_of(repo))


# --- packaging sanity ------------------------------------------------------

ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_hooks_json_points_at_existing_executables():
    with open(os.path.join(ROOT, "hooks", "hooks.json")) as f:
        cfg = json.load(f)
    for groups in cfg["hooks"].values():
        for group in groups:
            for h in group["hooks"]:
                rel = h["command"].replace("${CLAUDE_PLUGIN_ROOT}/", "")
                path = os.path.join(ROOT, rel)
                assert os.path.isfile(path), rel
                assert os.access(path, os.X_OK), f"{rel} not executable"


def test_plugin_version_is_in_changelog():
    with open(os.path.join(ROOT, ".claude-plugin", "plugin.json")) as f:
        version = json.load(f)["version"]
    with open(os.path.join(ROOT, "CHANGELOG.md")) as f:
        assert version in f.read(), f"CHANGELOG missing {version}"
