"""worktree-guard activity signals, snippet forensics, and the Agent path."""

import datetime
import json
import os
import subprocess
import sys
import time

import pytest
from conftest import load_hook_module

wg = load_hook_module("worktree-guard.py", "wg2")


def iso(minutes_ago):
    t = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=minutes_ago)
    return t.isoformat().replace("+00:00", "Z")


def write_jsonl(path, events):
    with open(path, "w") as f:
        f.writelines(json.dumps(e) + "\n" for e in events)


# --- transcript activity: passive events must not fake liveness -----------


def test_fresh_passive_events_do_not_count(tmp_path):
    p = tmp_path / "t.jsonl"
    write_jsonl(
        p,
        [
            {"type": "assistant", "timestamp": iso(180)},
            {"type": "attachment", "timestamp": iso(0)},
        ],
    )
    epoch = wg.file_activity_epoch(str(p), time.time() - 300)
    assert epoch is not None and (time.time() - epoch) > 3600  # 3h, not now


def test_fresh_active_event_counts(tmp_path):
    p = tmp_path / "t.jsonl"
    write_jsonl(
        p,
        [
            {"type": "attachment", "timestamp": iso(180)},
            {"type": "assistant", "timestamp": iso(0)},
        ],
    )
    epoch = wg.file_activity_epoch(str(p), time.time() - 300)
    assert epoch is not None and (time.time() - epoch) < 120


def test_stale_mtime_is_trusted_without_parsing(tmp_path):
    p = tmp_path / "t.jsonl"
    write_jsonl(p, [{"type": "assistant", "timestamp": iso(0)}])  # content lies fresh
    os.utime(p, (time.time() - 7200,) * 2)
    epoch = wg.file_activity_epoch(str(p), time.time() - 300)
    assert abs((time.time() - epoch) - 7200) < 90  # mtime wins on the cheap path


def project_dir(monkeypatch, tmp_path, cwd):
    # os.path.expanduser("~") reads HOME on POSIX but USERPROFILE on
    # Windows (ntpath.expanduser never looks at HOME) -- setting only one
    # leaves the other platform resolving "~" to the real home directory.
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    d = tmp_path / ".claude" / "projects" / wg.project_slug(str(cwd))
    d.mkdir(parents=True)
    return d


def test_transcript_scan_reaches_background_agents(monkeypatch, tmp_path):
    cwd = tmp_path / "tree"
    cwd.mkdir()
    proj = project_dir(monkeypatch, tmp_path, cwd)
    sub = proj / "other-session" / "subagents"
    sub.mkdir(parents=True)
    write_jsonl(sub / "agent-x.jsonl", [{"type": "assistant", "timestamp": iso(1)}])
    idle = wg.transcript_idle_minutes(str(cwd), "my-session")
    assert idle is not None and idle < 5


def test_own_session_files_are_excluded(monkeypatch, tmp_path):
    cwd = tmp_path / "tree"
    cwd.mkdir()
    proj = project_dir(monkeypatch, tmp_path, cwd)
    write_jsonl(proj / "mine.jsonl", [{"type": "assistant", "timestamp": iso(0)}])
    assert wg.transcript_idle_minutes(str(cwd), "mine") is None


def test_project_slug_encodes_dots_and_slashes():
    assert wg.project_slug("/Users/x/api.example.com") == "-Users-x-api-example-com"


# --- last-user-message forensics ------------------------------------------


def test_snippet_surfaces_the_conversation(monkeypatch, tmp_path):
    cwd = tmp_path / "tree"
    cwd.mkdir()
    proj = project_dir(monkeypatch, tmp_path, cwd)
    write_jsonl(
        proj / "abcd1234-x.jsonl",
        [
            {
                "type": "user",
                "timestamp": iso(3),
                "message": {"content": "리뷰 이어서 진행해줘"},
            },
            {"type": "assistant", "timestamp": iso(2)},
        ],
    )
    sid, _ts, text = wg.last_user_snippet(str(cwd), "me")
    assert sid == "abcd1234" and "리뷰 이어서" in text


def test_snippet_skips_own_session_and_handles_absence(monkeypatch, tmp_path):
    cwd = tmp_path / "tree"
    cwd.mkdir()
    proj = project_dir(monkeypatch, tmp_path, cwd)
    write_jsonl(
        proj / "mine.jsonl",
        [{"type": "user", "timestamp": iso(1), "message": {"content": "secret"}}],
    )
    assert wg.last_user_snippet(str(cwd), "mine") is None


# --- Agent/Task isolation:"worktree" path ---------------------------------


def agent_decide(monkeypatch, capsys, repo, tool_input, sessions=([], [], True)):
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Agent",
            "session_id": "me",
            "tool_input": tool_input,
            "cwd": str(repo),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out.strip()
    if not out:
        return "silent", ""
    d = json.loads(out)["hookSpecificOutput"]
    return d["permissionDecision"], d["permissionDecisionReason"]


def test_agent_isolation_worktree_single_stream_asks(monkeypatch, capsys, repo):
    """`ask`, not `deny`. The Bash deny has a documented way past it — retry
    with `[worktree-ok]` — and an Agent call has no command line to put one on.
    Reading the token out of the prompt instead was tried and taken back, so
    this path takes the one step the token was worth and asks outright."""
    assert (
        agent_decide(
            monkeypatch, capsys, repo, {"prompt": "x", "isolation": "worktree"}
        )[0]
        == "ask"
    )


def test_agent_isolation_worktree_concurrent_asks(monkeypatch, capsys, repo):
    """Both this and the single-stream row answer `ask` now, so the decision
    alone no longer says which branch ran. The reason does: only the concurrent
    branch lists the other session."""
    decision, reason = agent_decide(
        monkeypatch,
        capsys,
        repo,
        {"prompt": "x", "isolation": "worktree"},
        sessions=([(1, "/t", 0.1, 0.1, None)], [], True),
    )
    assert decision == "ask"
    assert "actively working" in reason
    assert "single-stream" not in reason


def test_agent_without_isolation_is_untouched(monkeypatch, capsys, repo):
    assert agent_decide(monkeypatch, capsys, repo, {"prompt": "x"})[0] == "silent"


# --- decision rows previously uncovered -----------------------------------


def decide(monkeypatch, capsys, repo, command, sessions=([], [], True)):
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": "me",
            "tool_input": {"command": command},
            "cwd": str(repo),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out.strip()
    if not out:
        return "silent", ""
    d = json.loads(out)["hookSpecificOutput"]
    return d["permissionDecision"], d["permissionDecisionReason"]


def test_worktree_add_idle_sessions_offer_both_ways_on(monkeypatch, capsys, repo):
    d, reason = decide(
        monkeypatch,
        capsys,
        repo,
        "git worktree add ../wt feature/x",
        sessions=([], [(2, "/t", 400.0, 90.0, "Terminal")], True),
    )
    assert d == "deny" and "git switch" in reason  # switch may suffice
    assert "AskUserQuestion" in reason and "[shared-tree-ok]" in reason


def test_worktree_add_unreliable_offers_both_ways_on(monkeypatch, capsys, repo):
    assert (
        decide(
            monkeypatch,
            capsys,
            repo,
            "git worktree add ../wt feature/x",
            sessions=([], [], False),
        )[0]
        == "deny"
    )


def test_dirty_ask_lists_the_files(monkeypatch, capsys, repo):
    (repo / "f.txt").write_text("changed\n")
    d, reason = decide(monkeypatch, capsys, repo, "git switch feature/x")
    assert d == "ask" and "f.txt" in reason


def test_lease_entries_flow_into_deny(monkeypatch, capsys, repo):
    lease = [(None, f"{repo}  [lease: abcd1234…]", None, 0.5, None)]
    d, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=(lease, [], True)
    )
    assert d == "deny" and "lease" in reason


def test_tracked_changes_ignore_untracked(repo):
    (repo / "new-untracked.txt").write_text("x")
    assert wg.tracked_changes(str(repo)) == []


def test_bad_idle_override_falls_back_instead_of_crashing(monkeypatch):
    # An unparseable override used to raise at import time; the hook then
    # exited non-zero, which Claude Code reads as "no verdict" — one typo
    # silently disabled the guard.
    from conftest import load_hook_module

    for bad in ("abc", "", "-3", "0"):
        monkeypatch.setenv("WORKTREE_GUARD_IDLE_MIN", bad)
        mod = load_hook_module("worktree-guard.py", f"wg_idle_{bad or 'empty'}")
        assert mod.IDLE_MIN == 5, bad
    monkeypatch.setenv("WORKTREE_GUARD_IDLE_MIN", "12")
    assert load_hook_module("worktree-guard.py", "wg_idle_ok").IDLE_MIN == 12


# --- real OS probes: these helpers are stubbed in every decision test above,
# so without this block they never execute on any platform, CI included ------


def test_proc_cwd_reports_this_process_real_cwd():
    got = wg.proc_cwd(os.getpid())
    if got is None:
        if os.path.isdir("/proc"):
            pytest.fail("/proc exists but proc_cwd returned None")
        pytest.skip("no /proc on this platform and lsof unavailable")
    assert os.path.realpath(got) == os.path.realpath(os.getcwd())


def test_proc_cwd_sees_another_process_without_lsof(monkeypatch, tmp_path):
    # The Linux path must stand on its own: with lsof unavailable, a session
    # working in another tree still has to be visible, or the guard silently
    # decides the tree is single-stream.
    if not os.path.isdir("/proc"):
        pytest.skip("/proc-only behavior")
    monkeypatch.setattr(
        wg.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError("lsof")),
    )
    p = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"], cwd=str(tmp_path)
    )
    try:
        assert os.path.realpath(wg.proc_cwd(p.pid)) == os.path.realpath(str(tmp_path))
    finally:
        p.kill()
        p.wait()


def test_ancestors_includes_self_and_parent():
    a = wg.ancestors(os.getpid())
    assert os.getpid() in a
    if sys.platform == "win32":
        pytest.skip("ancestors() walks `ps`, which Windows doesn't have")
    if os.getppid() > 1:
        assert os.getppid() in a, "parent pid missing — ps parsing is broken"
