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

import datetime
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


# --- a lease also retires the TRANSCRIPT its session left behind --------------
#
# The rule this module opens with — a lease whose owning process is gone is not
# a work stream — was enforced in one place and ignored in another.
#
# `sessions_in_tree`'s last arm reads "no process, but a fresh transcript in
# this project" as an unattached live session. Those are also, exactly, the
# inputs of a session that exited inside the idle window. Measured in this
# repository on 2026-09-08: `fresh_leases` retired session fdbb7b51's lease on
# positive evidence its pid was gone, and the arm then read that same session's
# two-minute-old transcript and put it straight back into `active` — which on
# the switch path is a hard deny. The tree read as concurrent for five minutes
# after every session in the project ended.
#
# Two probes the ticket proposed were measured and BOTH are false, which is why
# the repair is here and not in a new syscall:
#
#   - "a live session holds its transcript open" — it does not. No live
#     `claude` process holds any transcript fd, including one writing its own
#     file seconds earlier. That discriminator would answer "not held" for
#     every session and collapse the arm to always-idle.
#   - "an exited session leaves a terminal marker" — none exists. Across 188
#     transcripts no last-record type separates the populations.
#
# The lease already carries the answer, and the direction is safe by
# construction: a session lands in the dead set only on positive evidence its
# owner is gone, so every unreadable answer leaves the transcript counted
# exactly as before.


def iso(minutes_ago):
    t = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=minutes_ago)
    return t.isoformat().replace("+00:00", "Z")


def transcripts_for(monkeypatch, tmp_path, cwd):
    """The ~/.claude/projects directory the guard will scan for `cwd`.

    HOME and USERPROFILE both: expanduser reads HOME on POSIX and USERPROFILE
    on Windows, so setting one leaves the other platform pointed at the real
    home directory.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    d = tmp_path / ".claude" / "projects" / wg.project_slug(str(cwd))
    d.mkdir(parents=True)
    return d


def fresh_transcript(path):
    """A transcript whose tail is ACTIVE events — an exited session's tail
    looks exactly like this, which is the whole difficulty."""
    with open(path, "w") as f:
        f.write(json.dumps({"type": "assistant", "timestamp": iso(1)}) + "\n")


def exited_session(repo, tmp_path, monkeypatch, sid="ended-session"):
    """The incident: a fresh transcript whose owner the lease proves is gone."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / f"{sid}.jsonl")
    write_lease(
        repo,
        sid,
        json.dumps(
            {"ts": int(time.time()), "pid": dead_pid(), "host": socket.gethostname()}
        ),
    )
    return proj


def idle_minutes(repo, own="my-session"):
    return wg.transcript_idle_minutes(
        str(repo), own, dead_ids=wg.dead_session_ids(str(repo))
    )


def test_an_exited_sessions_transcript_is_not_a_work_stream(
    repo, tmp_path, monkeypatch
):
    """THE INCIDENT. Fresh transcript, active tail, owner provably gone."""
    exited_session(repo, tmp_path, monkeypatch)
    assert idle_minutes(repo) is None


def test_a_transcript_with_no_lease_still_counts(repo, tmp_path, monkeypatch):
    """THE CASE THAT MUST NOT BREAK — an extension-panel session that has
    written transcripts but not yet touched the repo, so it has no lease.
    Nothing proves it dead, so it stays a live work stream."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / "panel-session.jsonl")
    idle = idle_minutes(repo)
    assert idle is not None and idle < wg.IDLE_MIN


def test_a_live_lease_owner_keeps_its_transcript(repo, tmp_path, monkeypatch):
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / "running-session.jsonl")
    write_lease(
        repo,
        "running-session",
        json.dumps(
            {"ts": int(time.time()), "pid": os.getpid(), "host": socket.gethostname()}
        ),
    )
    idle = idle_minutes(repo)
    assert idle is not None and idle < wg.IDLE_MIN


def test_a_lease_from_another_host_does_not_retire_a_transcript(
    repo, tmp_path, monkeypatch
):
    """Another machine's pid is not ours to probe, so it is not evidence.

    The pid here is one that has certainly exited ON THIS host, which is the
    whole point: only the host check keeps it out of the dead set. An earlier
    draft used pid 1, which is alive everywhere, so the case passed with the
    host check deleted — it was pinning nothing."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / "elsewhere.jsonl")
    write_lease(
        repo,
        "elsewhere",
        json.dumps(
            {"ts": int(time.time()), "pid": dead_pid(), "host": "some-other-host"}
        ),
    )
    idle = idle_minutes(repo)
    assert idle is not None and idle < wg.IDLE_MIN


def test_a_lease_without_a_pid_does_not_retire_a_transcript(
    repo, tmp_path, monkeypatch
):
    """The pre-upgrade bare-timestamp format: no owner to ask about."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / "legacy-session.jsonl")
    write_lease(repo, "legacy-session", "1")
    idle = idle_minutes(repo)
    assert idle is not None and idle < wg.IDLE_MIN


def test_a_dead_sessions_subagent_transcripts_are_skipped(repo, tmp_path, monkeypatch):
    """Background agents run inside their session's process; when the lease
    proves that process gone, its subagents went with it."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    sub = proj / "ended-session" / "subagents"
    sub.mkdir(parents=True)
    fresh_transcript(sub / "agent-x.jsonl")
    write_lease(
        repo,
        "ended-session",
        json.dumps(
            {"ts": int(time.time()), "pid": dead_pid(), "host": socket.gethostname()}
        ),
    )
    assert idle_minutes(repo) is None


def test_dead_session_ids_names_only_provably_dead_owners(repo, tmp_path, monkeypatch):
    """Every shape that is not positive evidence of death stays out."""
    write_lease(
        repo,
        "gone",
        json.dumps(
            {"ts": int(time.time()), "pid": dead_pid(), "host": socket.gethostname()}
        ),
    )
    write_lease(
        repo,
        "running",
        json.dumps(
            {"ts": int(time.time()), "pid": os.getpid(), "host": socket.gethostname()}
        ),
    )
    write_lease(
        repo,
        "far-away",
        json.dumps({"ts": int(time.time()), "pid": 1, "host": "some-other-host"}),
    )
    write_lease(repo, "no-pid", "1")
    assert wg.dead_session_ids(str(repo)) == frozenset({"gone"})


def test_dead_session_ids_is_empty_without_a_lease_directory(tmp_path):
    """No repo, no leases, no exclusions — and no exception."""
    d = tmp_path / "not-a-repo"
    d.mkdir()
    assert wg.dead_session_ids(str(d)) == frozenset()


def only_our_own_claude(monkeypatch, fake_pid=424242, *others):
    """Make the process scan work and find no OTHER session — the incident.

    `sessions_in_tree` returns unreliable unless it can spot its own process,
    and the test runner is not named `claude`. Feeding the scan one pid and
    putting that pid in the ancestor set reproduces the state at the denial:
    a scan that worked, correctly finding nobody else.
    """
    real = wg.subprocess.run
    listing = "".join(f"{p} claude\n" for p in (fake_pid, *others))

    def fake(cmd, *a, **k):
        if list(cmd[:2]) == ["ps", "-axo"]:
            return subprocess.CompletedProcess(cmd, 0, listing, "")
        return real(cmd, *a, **k)

    monkeypatch.setattr(wg.subprocess, "run", fake)
    monkeypatch.setattr(wg, "ancestors", lambda pid: {fake_pid})


def test_sessions_in_tree_does_not_resurrect_an_exited_session(
    repo, tmp_path, monkeypatch
):
    """End to end: the arm must not put back what fresh_leases just buried."""
    exited_session(repo, tmp_path, monkeypatch)
    only_our_own_claude(monkeypatch)
    active, _idle, reliable = wg.sessions_in_tree(str(repo), "my-session")
    assert reliable is True
    assert active == [], f"an exited session came back as active: {active}"


def test_sessions_in_tree_still_sees_an_unattached_live_session(
    repo, tmp_path, monkeypatch
):
    """The arm still fires for the case it exists for: a fresh transcript with
    no process AND nothing proving its session dead."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / "panel-session.jsonl")
    only_our_own_claude(monkeypatch)
    active, _idle, reliable = wg.sessions_in_tree(str(repo), "my-session")
    assert reliable is True
    assert len(active) == 1 and active[0][0] is None


def test_an_unprobeable_owner_does_not_retire_a_transcript(repo, tmp_path, monkeypatch):
    """Where this fix's fail direction lives. `None` from lease_owner_alive is
    "could not ask", never "is gone" — so the transcript stays counted, and an
    unreadable answer reproduces today's behaviour rather than opening the
    fail-open direction where the guard allows a switch that takes someone
    else's branch."""
    proj = transcripts_for(monkeypatch, tmp_path, repo)
    fresh_transcript(proj / "unprobeable.jsonl")
    write_lease(
        repo,
        "unprobeable",
        json.dumps(
            {"ts": int(time.time()), "pid": 424242, "host": socket.gethostname()}
        ),
    )
    monkeypatch.setattr(wg, "lease_owner_alive", lambda pid: None)
    idle = idle_minutes(repo)
    assert idle is not None and idle < wg.IDLE_MIN


def test_a_non_integer_pid_is_never_asked_about(repo, monkeypatch):
    """The guard clause, pinned where POSIX cannot show it on its own.

    `os.kill` rejects a string pid with TypeError, so on this platform a bad
    pid falls out anyway and the check looks redundant. It is not: Windows
    probes with `tasklist /FI "PID eq {pid}"`, where a string interpolates
    happily and can match a real process. Forcing lease_owner_alive to answer
    "gone" for anything is what makes the clause the only thing standing
    between a malformed lease and a retired transcript.
    """
    write_lease(
        repo,
        "bad-pid",
        json.dumps(
            {"ts": int(time.time()), "pid": "424242", "host": socket.gethostname()}
        ),
    )
    monkeypatch.setattr(wg, "lease_owner_alive", lambda pid: False)
    assert wg.dead_session_ids(str(repo)) == frozenset()


def test_a_live_session_is_not_kept_active_by_a_dead_neighbours_transcript(
    repo, tmp_path, monkeypatch
):
    """The same defect on the OTHER call site, which the arm's fix does not
    reach on its own.

    A live `claude` process sits in the tree with no terminal input for an
    hour. Its only remaining evidence of work is the project transcript — and
    that transcript belongs to a neighbour that has exited. Counting it holds
    the session in `active`, which on the switch path is a hard deny; with the
    dead session excluded it falls to `idle`, which is a question the user can
    answer. Never a silent allow either way: the pid is real, so the session
    stays in one of the two lists.
    """
    exited_session(repo, tmp_path, monkeypatch)
    other = 525252
    only_our_own_claude(monkeypatch, 424242, other)
    monkeypatch.setattr(wg, "proc_cwd", lambda pid: str(repo))
    monkeypatch.setattr(wg, "tty_idle_minutes", lambda pid: 60.0)

    active, idle, reliable = wg.sessions_in_tree(str(repo), "my-session")
    assert reliable is True
    assert active == [], f"a dead neighbour's transcript held it active: {active}"
    assert len(idle) == 1 and idle[0][0] == other
