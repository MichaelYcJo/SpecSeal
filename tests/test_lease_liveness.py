"""A lease outlives the session that wrote it.

The lease file is stamped on every tool call and never removed at session end,
so for IDLE_MIN minutes after a session closes its lease still reads as work in
progress. Measured: two conversations ended at 11:28 and 11:32 and their
leases denied a branch switch in a third — with no way to say so, because every
lease went straight into `active`, and `active` is a hard deny.

Two things are asserted here. A lease whose owning process is gone is not a
work stream. A lease that cannot be attributed is a question for the user, not
a refusal.
"""

import json
import os
import socket
import subprocess
import sys
import time

from conftest import load_hook_module

wg = load_hook_module("worktree-guard.py", "wg_lease")

HOOKS = os.path.join(os.path.dirname(__file__), "..", "hooks")


def lease_dir(repo):
    d = os.path.join(str(repo), ".git", "specseal-leases")
    os.makedirs(d, exist_ok=True)
    return d


def write_lease(repo, name, body):
    p = os.path.join(lease_dir(repo), name)
    with open(p, "w") as f:
        f.write(body)
    return p


def dead_pid():
    """A pid that has certainly exited — spawned and reaped here."""
    p = subprocess.Popen([sys.executable, "-c", "pass"])
    p.wait()
    return p.pid


# --- fresh_leases: liveness decides ------------------------------------------


def test_lease_of_a_dead_process_is_dropped(repo):
    write_lease(
        repo,
        "ended-session",
        json.dumps(
            {"ts": int(time.time()), "pid": dead_pid(), "host": socket.gethostname()}
        ),
    )
    live, unattributable = wg.fresh_leases(str(repo), "me")
    assert live == [] and unattributable == []


def test_lease_of_a_live_process_stays_active(repo):
    write_lease(
        repo,
        "running-session",
        json.dumps(
            {"ts": int(time.time()), "pid": os.getpid(), "host": socket.gethostname()}
        ),
    )
    live, unattributable = wg.fresh_leases(str(repo), "me")
    assert len(live) == 1 and "running-" in live[0][1]
    assert unattributable == []


def test_lease_without_a_pid_is_unattributable_not_active(repo):
    """The pre-upgrade format: a bare timestamp. Ask, do not deny."""
    write_lease(repo, "legacy-session", "1")
    live, unattributable = wg.fresh_leases(str(repo), "me")
    assert live == []
    assert len(unattributable) == 1 and "legacy-s" in unattributable[0][1]


def test_lease_from_another_host_stays_active(repo):
    """No pid to check here, and a fresh stamp still means someone is working."""
    write_lease(
        repo,
        "elsewhere",
        json.dumps({"ts": int(time.time()), "pid": 1, "host": "some-other-host"}),
    )
    live, unattributable = wg.fresh_leases(str(repo), "me")
    assert len(live) == 1 and unattributable == []


def test_own_lease_is_ignored_in_both_lists(repo):
    write_lease(
        repo,
        "me",
        json.dumps(
            {"ts": int(time.time()), "pid": os.getpid(), "host": socket.gethostname()}
        ),
    )
    assert wg.fresh_leases(str(repo), "me") == ([], [])


def stale_lease(repo, name, pid):
    p = write_lease(
        repo, name, json.dumps({"ts": 1, "pid": pid, "host": socket.gethostname()})
    )
    os.utime(p, (time.time() - 3600,) * 2)
    return p


# --- quiet is not the same question as gone ----------------------------------
#
# Alive answers "does the session exist"; the idle window answers "is it
# working". Neither substitutes for the other, and a lease had only the second.
# A session quiet for an hour but still running is a forgotten tab — which the
# process scan already treats as a question, not a pass. A lease was dropping
# it outright, so the same state got two different answers depending on which
# signal happened to see it.
#
# The escalation is confined to what the scan CANNOT see. A lease naming a pid
# the scan already reports adds nothing: that session is classified once, on
# its own signals, and counting it twice only multiplies prompts.


def test_stale_lease_with_a_live_owner_the_scan_misses_asks(repo):
    stale_lease(repo, "other-cwd-session", os.getpid())
    live, unattributable = wg.fresh_leases(str(repo), "me", scanned_pids=frozenset())
    assert live == []
    assert len(unattributable) == 1 and "other-cw" in unattributable[0][1]


def test_stale_lease_the_scan_already_reports_is_not_counted_twice(repo):
    """The narrowing. The scan saw this pid and classified it; the lease steps
    aside rather than raising a second prompt for one session."""
    stale_lease(repo, "seen-session", os.getpid())
    assert wg.fresh_leases(str(repo), "me", scanned_pids=frozenset({os.getpid()})) == (
        [],
        [],
    )


def test_stale_lease_with_a_dead_owner_stays_dropped(repo):
    stale_lease(repo, "ended-session", dead_pid())
    assert wg.fresh_leases(str(repo), "me", scanned_pids=frozenset()) == ([], [])


def test_stale_lease_without_a_pid_stays_dropped(repo):
    """No owner to ask about, so age remains the only filter it has."""
    p = write_lease(repo, "legacy-old", "1")
    os.utime(p, (time.time() - 3600,) * 2)
    assert wg.fresh_leases(str(repo), "me", scanned_pids=frozenset()) == ([], [])


def test_stale_lease_with_an_unprobeable_owner_is_not_escalated(repo, monkeypatch):
    """`None` is "could not ask", not "is running". Escalating it would turn
    every unanswerable probe into a prompt, which is the absence of evidence
    being read as evidence."""
    stale_lease(repo, "unprobeable", 424242)
    monkeypatch.setattr(wg, "lease_owner_alive", lambda pid: None)
    assert wg.fresh_leases(str(repo), "me", scanned_pids=frozenset()) == ([], [])


def test_fresh_lease_with_an_unprobeable_owner_still_denies(repo, monkeypatch):
    """The fresh path keeps treating an unanswerable probe as active work —
    conservative there, because the stamp itself says someone just worked."""
    write_lease(
        repo,
        "unprobeable-now",
        json.dumps(
            {"ts": int(time.time()), "pid": 424242, "host": socket.gethostname()}
        ),
    )
    monkeypatch.setattr(wg, "lease_owner_alive", lambda pid: None)
    live, _ = wg.fresh_leases(str(repo), "me", scanned_pids=frozenset())
    assert len(live) == 1 and "unprobeable" in live[0][1]


def test_the_fresh_path_is_unchanged_by_the_scan(repo):
    """A lease stamped moments ago is active work whether or not the scan
    also found it; this narrowing must not touch the deny path."""
    write_lease(
        repo,
        "busy-session",
        json.dumps(
            {"ts": int(time.time()), "pid": os.getpid(), "host": socket.gethostname()}
        ),
    )
    live, _ = wg.fresh_leases(str(repo), "me", scanned_pids=frozenset({os.getpid()}))
    assert len(live) == 1


# --- the decision the user sees ----------------------------------------------


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


def test_unattributable_lease_offers_a_choice_instead_of_blocking(
    monkeypatch, capsys, repo
):
    """Both this and the ACTIVE-session block return `deny` now, so the reason
    is what tells them apart: this one hands the decision back to the user."""
    lease = [(None, f"{repo}  [lease: legacy-s… owner unknown]", None, 0.5, None)]
    d, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=([], lease, True)
    )
    assert d == "deny"
    assert "AskUserQuestion" in reason


def test_the_question_names_both_choices(monkeypatch, capsys, repo):
    """The point of denying here is that BOTH ways on get named — the shared
    tree with its retry token, and the worktree."""
    lease = [(None, f"{repo}  [lease: legacy-s… owner unknown]", None, 0.5, None)]
    _, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=([], lease, True)
    )
    assert "[shared-tree-ok]" in reason
    assert "worktree" in reason.lower()


def test_live_lease_still_denies(monkeypatch, capsys, repo):
    lease = [(None, f"{repo}  [lease: running-… pid 42 alive]", None, 0.5, None)]
    d, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=(lease, [], True)
    )
    assert d == "deny" and "lease" in reason


# --- what session-lease writes -----------------------------------------------


def run_lease_hook(repo, session):
    payload = {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": "ls"},
        "cwd": str(repo),
    }
    subprocess.run(
        [sys.executable, os.path.join(HOOKS, "session-lease.py")],
        input=json.dumps(payload),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def test_lease_records_a_parseable_record(repo):
    """Through a real subprocess, so only what holds in every environment is
    asserted. Whether a pid lands depends on the ancestry the hook happens to
    have — present under a Claude Code session, absent on a CI runner, and both
    are correct. The pid logic is pinned by the stubbed-tree cases below, which
    do not depend on where the suite runs.

    The first version of this asserted a pid unconditionally. It passed locally
    for the wrong reason: pytest was launched from inside a session, so `claude`
    really was an ancestor. CI is what said so.
    """
    run_lease_hook(repo, "sess-x")
    with open(os.path.join(lease_dir(repo), "sess-x")) as f:
        rec = json.load(f)
    assert rec["host"] == socket.gethostname()
    assert abs(rec["ts"] - time.time()) < 60
    if "pid" in rec:
        assert isinstance(rec["pid"], int) and rec["pid"] > 0


# --- who the lease says owns it ----------------------------------------------

sl = load_hook_module("session-lease.py", "sl_owner")


def stub_process_tree(monkeypatch, start, tree):
    """`ps -o ppid=,comm= -p <pid>` against a fixture tree of {pid: (ppid, comm)}.

    Only `ps` is faked; everything else (git, notably) reaches the real
    subprocess, so main() can still resolve the repo.
    """
    import types

    real_run = sl.subprocess.run
    monkeypatch.setattr(sl.os, "getppid", lambda: start)

    def fake_run(cmd, **kwargs):
        if not (isinstance(cmd, (list, tuple)) and cmd and cmd[0] == "ps"):
            return real_run(cmd, **kwargs)
        pid = int(cmd[-1])
        if pid not in tree:
            return types.SimpleNamespace(stdout="")
        ppid, comm = tree[pid]
        return types.SimpleNamespace(stdout=f"{ppid} {comm}\n")

    monkeypatch.setattr(sl.subprocess, "run", fake_run)


def test_owner_pid_walks_past_the_shell(monkeypatch):
    """The immediate parent is the shell that spawned the hook — measured here,
    /bin/zsh, with claude two levels up. Recording getppid() would name a
    process that dies constantly, and every dead shell would retire a live
    session's lease."""
    stub_process_tree(monkeypatch, 100, {100: (50, "/bin/zsh"), 50: (1, "claude")})
    assert sl.owner_pid() == 50


def test_owner_pid_is_none_without_a_claude_ancestor(monkeypatch):
    """An extension host is not named `claude`. No pid is recorded, so the
    guard reads the lease as unattributable rather than as an exited session."""
    stub_process_tree(monkeypatch, 100, {100: (50, "/bin/zsh"), 50: (1, "code")})
    assert sl.owner_pid() is None


def run_main_in_process(repo, monkeypatch, session):
    """main() with stdin stubbed, so the wiring — not just owner_pid() — is
    under test. A version that recorded getppid() passes every test that only
    calls owner_pid() directly."""
    import io

    monkeypatch.setattr(
        sl.sys,
        "stdin",
        io.StringIO(
            json.dumps(
                {
                    "tool_name": "Bash",
                    "session_id": session,
                    "tool_input": {"command": "ls"},
                    "cwd": str(repo),
                }
            )
        ),
    )
    sl.main()
    with open(os.path.join(lease_dir(repo), session)) as f:
        return json.load(f)


def test_main_records_the_claude_ancestor_not_the_shell(repo, monkeypatch):
    stub_process_tree(monkeypatch, 100, {100: (50, "/bin/zsh"), 50: (1, "claude")})
    rec = run_main_in_process(repo, monkeypatch, "sess-owner")
    assert rec["pid"] == 50, "recorded the shell (getppid) instead of the session"


def test_main_omits_pid_when_the_owner_is_unknown(repo, monkeypatch):
    stub_process_tree(monkeypatch, 100, {100: (1, "code")})
    rec = run_main_in_process(repo, monkeypatch, "sess-ext")
    assert "pid" not in rec
    assert rec["host"] == socket.gethostname()


def test_lease_write_survives_an_unwritable_dir(repo):
    """Failure is silent by contract; the hook must not become a blocker."""
    d = lease_dir(repo)
    os.chmod(d, 0o500)
    try:
        run_lease_hook(repo, "sess-y")
    finally:
        os.chmod(d, 0o700)
