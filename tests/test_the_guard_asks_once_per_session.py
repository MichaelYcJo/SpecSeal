"""The worktree guard asked once per worktree, so an unattended run stopped
at the first `git worktree add` and again at every one after it.

Measured on the 0.9.1 release run (#237): six work items on six branches needed
six creations, and the guard held the run at all six. There was no path through
it that cost zero prompts — the `[worktree-ok]` site says so in writing, and it
is right about the token: the token is written into the command by whoever
issues it, so the model can write it on the first attempt, and reading it as
consent would turn the guard off with nobody asked.

What separates the first creation from the sixth is available without trusting
the token. **The harness only runs a `git worktree add` that was approved**, so
a `PostToolUse` observation of one that actually ran is written after the
answer rather than before the question, which is the one thing a command text
cannot forge.

Two halves, and they are separable on purpose:

  the writer   `hooks/worktree_consent.py` — the `PostToolUse` arm. Its own
               file rather than a branch inside the guard, because
               `hooks/dispatch.py` hands every gate the same payload with no
               event name, so one file wired to both events would have to tell
               them apart by sniffing a harness field. A gate wired only to
               `PostToolUse` needs no such guarantee (`agent-contract` §13).
  the reader   `guard_worktree_creation`'s new first row. The tests here grant
               consent by writing the record BY HAND, so the reader is pinned
               without the writer under it.

What must not change is pinned here too: a session with no record still asks,
the single-stream site still denies, and nothing in the switch direction moves.
"""

import json
import os
import pathlib
import subprocess

from conftest import load_hook_module, run_hook

wg = load_hook_module("worktree-guard.py", "wg_consent")

ACTIVE = [(111, "/tree", 1.0, 0.5, "VS Code")]
IDLE = [(222, "/tree", 400.0, 90.0, "Terminal")]


def common_dir(repo):
    """The clone's git directory — where the record lives.

    `--git-common-dir` rather than `--absolute-git-dir`: the record stands for
    "this session may split this clone into worktrees", and a linked worktree
    is the same clone. git answers relatively from a main worktree, so the
    join is not optional.
    """
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-common-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    return pathlib.Path(os.path.normpath(os.path.join(str(repo), out)))


def consent_dir(repo):
    return common_dir(repo) / "specseal-worktree-consent"


def grant(repo, session="me"):
    """Write the record by hand — the reader's tests do not need the writer."""
    d = consent_dir(repo)
    d.mkdir(parents=True, exist_ok=True)
    (d / session).write_text("")
    return d / session


def decide(
    monkeypatch, capsys, repo, command, sessions=([], [], True), session_id="me"
):
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": session_id,
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


def agent_decide(
    monkeypatch, capsys, repo, tool_input, sessions=([], [], True), session_id="me"
):
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Agent",
            "session_id": session_id,
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


def post(repo, tool="Bash", command="git worktree add ../wt feature/x", **extra):
    """The payload the harness sends AFTER a tool call has run."""
    payload = {
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "session_id": "me",
        "cwd": str(repo),
        "tool_input": {"command": command} if tool == "Bash" else command,
        "tool_response": {"stdout": "", "stderr": "", "interrupted": False},
    }
    payload.update(extra)
    return payload


# --- the reader: what a recorded consent changes ---------------------------


def test_the_first_creation_is_still_a_question(monkeypatch, capsys, repo):
    """The row this work must NOT move. A session with no record meets the
    single-stream deny, which is the whole reason the guard exists."""
    assert not consent_dir(repo).exists()
    decision, reason = decide(monkeypatch, capsys, repo, "git worktree add ../wt f")
    assert decision == "deny"
    assert "git switch" in reason


def test_a_second_creation_in_the_same_session_is_allowed(monkeypatch, capsys, repo):
    """The measured failure, one line. Six creations cost six stops; after
    this, the first costs one and the rest cost none."""
    grant(repo)
    decision, reason = decide(monkeypatch, capsys, repo, "git worktree add ../wt f")
    assert decision == "allow", reason


def test_consent_outranks_every_row_below_it(monkeypatch, capsys, repo):
    """Each row of §B asks something the record has already answered — the
    ACTIVE row asks for a confirmation, the two choice rows ask which way to
    go, and the `[worktree-ok]` row asks whether the token was meant. So the
    read goes above all of them rather than beside one."""
    grant(repo)
    for sessions in ((ACTIVE, [], True), ([], IDLE, True), ([], [], False)):
        assert (
            decide(
                monkeypatch, capsys, repo, "git worktree add ../wt f", sessions=sessions
            )[0]
            == "allow"
        ), sessions
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt f  # [worktree-ok]")[
            0
        ]
        == "allow"
    )


def test_consent_belongs_to_the_session_that_earned_it(monkeypatch, capsys, repo):
    """Per session, not per repository. A second conversation in the same
    clone has answered nothing."""
    grant(repo, "session-a")
    assert (
        decide(
            monkeypatch,
            capsys,
            repo,
            "git worktree add ../wt f",
            session_id="session-b",
        )[0]
        == "deny"
    )


def test_a_session_with_no_id_is_never_consented(monkeypatch, capsys, repo):
    """No id, no record to key — and in particular the empty id must not
    resolve to the consent DIRECTORY, which exists here. The guard's other
    budget reads a missing id the same way: the site's old decision stands
    from the start."""
    grant(repo, "me")
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt f", session_id="")[0]
        == "deny"
    )


def test_the_allow_covers_only_a_command_that_is_nothing_else(
    monkeypatch, capsys, repo
):
    """`permissionDecision: "allow"` covers the WHOLE tool call, and a
    creation is routinely one segment of a compound. The record is about
    worktree creation, so the guard speaks for a command that is worktree
    creation and nothing else; anything more is an `ask` about the rest of the
    command line, never a deny about the worktree."""
    grant(repo)
    for command in (
        "git worktree add ../wt f && echo done",
        "cd /tmp && git worktree add ../wt f",
        "git status; git worktree add ../wt f",
    ):
        decision, reason = decide(monkeypatch, capsys, repo, command)
        assert decision == "ask", (command, decision)
        assert "git switch" not in reason, command
    # ...and a command the lexer gave up on is not vouched for either: what it
    # could not read is what the allow would be covering.
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt f  # don't")[0]
        == "ask"
    )


def test_a_second_creation_never_denies(monkeypatch, capsys, repo):
    """The consented `ask` is a floor, not a fallthrough. Landing back on the
    ladder would put the single-stream deny in front of a session that has
    already been told yes."""
    grant(repo)
    for sessions in (([], [], True), ([], IDLE, True), ([], [], False)):
        assert (
            decide(
                monkeypatch,
                capsys,
                repo,
                "git worktree add ../wt f && echo done",
                sessions=sessions,
            )[0]
            == "ask"
        ), sessions


def test_creation_consent_does_not_reach_the_switch_direction(
    monkeypatch, capsys, repo
):
    """One direction, one record. A creation the user agreed to says nothing
    about taking another session's branch out from under it."""
    grant(repo)
    assert (
        decide(
            monkeypatch,
            capsys,
            repo,
            "git switch feature/x",
            sessions=(ACTIVE, [], True),
        )[0]
        == "deny"
    )
    assert (
        decide(
            monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
        )[0]
        == "deny"
    )


def test_the_pre_tool_use_arm_records_nothing(monkeypatch, capsys, repo):
    """The integrity property, stated as a test rather than left to the file
    layout: nothing on the asking side may write the record it later reads."""
    decide(monkeypatch, capsys, repo, "git worktree add ../wt f")
    decide(monkeypatch, capsys, repo, "git worktree add ../wt f  # [worktree-ok]")
    decide(
        monkeypatch,
        capsys,
        repo,
        "git worktree add ../wt f",
        sessions=(ACTIVE, [], True),
    )
    assert not consent_dir(repo).exists()


# --- the writer: a creation that actually ran ------------------------------


def test_a_creation_that_ran_leaves_a_record(repo):
    run_hook("worktree_consent.py", post(repo))
    assert (consent_dir(repo) / "me").is_file()


def test_a_command_that_creates_nothing_leaves_no_record(repo):
    for command in ("git status", "git switch feature/x", "git worktree list"):
        run_hook("worktree_consent.py", post(repo, command=command))
    assert not consent_dir(repo).exists()


def test_a_creation_anywhere_in_the_command_records(repo):
    """The guard's PreToolUse walk stops at the first verdict because that is
    the one it must decide. A creation ANYWHERE in a command that ran is a
    creation that was approved, so the writer reads every segment."""
    run_hook(
        "worktree_consent.py",
        post(repo, command="git status && git worktree add ../wt feature/x"),
    )
    assert (consent_dir(repo) / "me").is_file()


def test_a_failed_creation_still_records_the_approval(repo):
    """Q2. The record is about the approval, which happened. The retry after a
    failure — a path that already exists, a branch already checked out — is the
    worst moment to put the question again."""
    run_hook(
        "worktree_consent.py",
        post(
            repo,
            tool_response={
                "stdout": "",
                "stderr": "fatal: '../wt' already exists",
                "interrupted": False,
                "is_error": True,
            },
        ),
    )
    assert (consent_dir(repo) / "me").is_file()


def test_a_malformed_session_id_cannot_escape_the_directory(repo):
    """The id names a file. `../../escaped` put an empty file at a repository
    root once already, through the other marker."""
    run_hook("worktree_consent.py", post(repo, session_id="../../escaped"))
    assert (consent_dir(repo) / "escaped").is_file()
    assert not (repo / "escaped").exists()


def test_a_pre_tool_use_payload_is_not_a_creation_that_ran(repo):
    """The writer is wired to one event, and it also refuses a payload that
    names the other. Nothing sends it one; a group misconfigured by hand
    would."""
    payload = post(repo)
    payload["hook_event_name"] = "PreToolUse"
    payload.pop("tool_response")
    run_hook("worktree_consent.py", payload)
    assert not consent_dir(repo).exists()


def test_an_unrecordable_consent_asks_rather_than_crashing(
    monkeypatch, capsys, repo, tmp_path
):
    """Q3. A guard that crashes reads as a silent allow — the module says so
    about `_idle_minutes`. The write fails silently instead, no record exists,
    and the next creation meets the question it always did."""
    blocked = consent_dir(repo)
    blocked.parent.mkdir(parents=True, exist_ok=True)
    blocked.write_text("not a directory")
    out = run_hook("worktree_consent.py", post(repo))
    assert out.strip() == ""
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f")[0] == "deny"


def test_the_record_follows_the_clone_not_the_worktree(repo, tmp_path):
    """Q4's neighbour: the SCOPE. A session that creates its first worktree
    from the main tree and its second from inside a linked one has made one
    decision, so it pays for one."""
    linked = tmp_path / "linked"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", str(linked), "feature/x"],
        check=True,
        capture_output=True,
    )
    run_hook("worktree_consent.py", post(linked))
    assert (consent_dir(repo) / "me").is_file()
    assert consent_dir(linked) == consent_dir(repo)


# --- the Agent/Task path shares the record ---------------------------------


def test_the_agent_path_reads_the_record_a_bash_creation_wrote(
    monkeypatch, capsys, repo
):
    """It is the same decision arriving through a different tool. Silent
    rather than `allow`: that call is a worktree creation PLUS an agent with a
    prompt, and the record is about the first half only."""
    grant(repo)
    assert (
        agent_decide(
            monkeypatch, capsys, repo, {"prompt": "x", "isolation": "worktree"}
        )[0]
        == "silent"
    )


def test_the_agent_path_without_consent_still_asks(monkeypatch, capsys, repo):
    assert (
        agent_decide(
            monkeypatch, capsys, repo, {"prompt": "x", "isolation": "worktree"}
        )[0]
        == "ask"
    )


def test_the_agent_path_writes_the_record_bash_reads(monkeypatch, capsys, repo):
    run_hook(
        "worktree_consent.py",
        post(repo, tool="Agent", command={"prompt": "x", "isolation": "worktree"}),
    )
    assert (consent_dir(repo) / "me").is_file()
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f")[0] == "allow"


def test_an_agent_without_isolation_records_nothing(repo):
    run_hook("worktree_consent.py", post(repo, tool="Agent", command={"prompt": "x"}))
    assert not consent_dir(repo).exists()


# --- wiring ----------------------------------------------------------------


def test_the_writer_is_in_both_post_groups():
    d = load_hook_module("dispatch.py", "dispatch_consent")
    assert "worktree_consent.py" in d.GROUPS["post-bash"]
    assert "worktree_consent.py" in d.GROUPS["post-agent"]


def test_hooks_json_sends_the_agent_after_event_to_the_group():
    root = os.path.join(os.path.dirname(__file__), "..")
    with open(os.path.join(root, "hooks", "hooks.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    matchers = {
        group["matcher"]: group["hooks"][0]["command"]
        for group in cfg["hooks"]["PostToolUse"]
    }
    assert "Agent|Task" in matchers, matchers
    assert "post-agent" in matchers["Agent|Task"]
