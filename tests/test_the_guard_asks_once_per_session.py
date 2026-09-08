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
import sys

from conftest import load_hook_module, run_hook

wg = load_hook_module("worktree-guard.py", "wg_consent")
wc = load_hook_module("worktree_consent.py", "wc_consent")
HOOKS = os.path.join(os.path.dirname(__file__), "..", "hooks")

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
    monkeypatch,
    capsys,
    repo,
    command,
    sessions=([], [], True),
    session_id="me",
    cwd=None,
):
    """`cwd` is where the SHELL is, which is not always `repo`: a `git -C
    <repo> worktree add` issued from outside any repository is the one shape
    that reaches the guard's second silent exit."""
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": session_id,
            "tool_input": {"command": command},
            "cwd": str(cwd or repo),
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
    creation and nothing else; anything more it does not speak for at all.

    `silent`, not `ask`, since #257. The record has already answered the
    worktree question, and the rest of the command line is the harness's to
    judge -- not this guard's to ask about a second time. What this case pins
    is unchanged and is the only thing that matters here: none of these earns
    an `allow`, which would speak for the whole tool call."""
    grant(repo)
    for command in (
        "git worktree add ../wt f && echo done",
        "cd /tmp && git worktree add ../wt f",
        "git status; git worktree add ../wt f",
    ):
        decision, reason = decide(monkeypatch, capsys, repo, command)
        assert decision == "silent", (command, decision)
        assert "git switch" not in reason, command
    # ...and a command the lexer gave up on is not vouched for either: what it
    # could not read is what the allow would be covering.
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt f  # don't")[0]
        == "silent"
    )


def test_a_command_with_no_creation_in_it_is_vouched_for_by_nothing(repo):
    """The predicate on its own. `main` only reaches it after a creation
    verdict, so nothing else can put a creation-free command in front of it —
    and a predicate whose false case is unreachable is a predicate no case can
    pin."""
    for command in ("", "echo hi", "git status", "git worktree list"):
        assert not wg.only_creates_a_worktree(command, str(repo)), command
    assert wg.only_creates_a_worktree("git worktree add ../wt f", str(repo))


def test_the_allow_refuses_a_segment_that_does_anything_else(monkeypatch, capsys, repo):
    """The test above asks about a COMPOUND, and every shape here is one
    segment. `permissionDecision: "allow"` bypasses the user's own permission
    settings for the whole tool call, and all ten of these answered `allow`
    before this case existed -- two of them were run in a real shell and did
    what a shell does: `$(touch <marker>)` created the marker, and `> <file>`
    left a file that held `important` holding `''`."""
    grant(repo)
    for command in (
        "git worktree add ../wt f $(touch /tmp/marker)",
        "git worktree add ../wt f `touch /tmp/marker`",
        "git worktree add ../wt f > /tmp/clobber",
        "git worktree add ../wt f >> /tmp/clobber",
        "git worktree add ../wt f < /tmp/clobber",
        "git worktree add ../wt f 2>/tmp/clobber",
        "git worktree add ../wt f <(touch /tmp/marker)",
        "(git worktree add ../wt f)",
        "git worktree add ../wt f <<EOF\nbody\nEOF",
        'git worktree add "$HOME/wt" f',
    ):
        decision, reason = decide(monkeypatch, capsys, repo, command)
        assert decision == "silent", (command, decision)
        assert "git switch" not in reason, command


def test_a_wrapper_in_front_of_the_creation_carries_no_allow(monkeypatch, capsys, repo):
    """`cmdline.parse_git` reads past `WRAPPERS` and leading `VAR=val`, which
    is right for "is this a git invocation" and wrong for "is this nothing but
    a creation". A user's own `permissions.deny` on `Bash(sudo:*)` must not be
    spoken over by a hook that was reasoning about worktrees."""
    grant(repo)
    for command in (
        "sudo git worktree add ../wt f",
        "env LD_PRELOAD=/tmp/e.so git worktree add ../wt f",
        "LD_PRELOAD=/tmp/e.so git worktree add ../wt f",
        "command git worktree add ../wt f",
    ):
        assert decide(monkeypatch, capsys, repo, command)[0] == "silent", command
    # ...and the two forms that are ordinary git are untouched. `-C` names
    # another clone, whose consent is its own, so the predicate is asked
    # directly rather than through a verdict about this one.
    assert wg.only_creates_a_worktree(
        "git -C /elsewhere worktree add ../wt f", str(repo)
    )
    assert (
        decide(
            monkeypatch, capsys, repo, "git worktree add ../a -b feature/x origin/main"
        )[0]
        == "allow"
    )


def test_a_path_qualified_git_carries_no_allow(monkeypatch, capsys, repo):
    """A basename is not an identity, and `allow` covers the whole tool call.

    The wrapper case above stops at `sudo`; this is the same class one step
    further in. `os.path.basename(tokens[0]) != "git"` vouches for a FILENAME,
    so a session that had one creation approved could then run any executable
    on the machine by giving it a last component of `git`. Seen red first: with
    a record present, every command below answered `allow`, `~/git` and `*/git`
    included -- the second of which the docstring already claimed was refused
    "one line below, where `git` has to be the word itself".

    What the exact-equality test costs is a prompt on `/usr/bin/git worktree
    add …`, and that is the trade the `$`/`>` refusals already make: a wrong
    deny spends one prompt, a wrong allow signs for a binary nobody
    identified."""
    grant(repo)
    for command in (
        "./git worktree add ../wt f",
        "../git worktree add ../wt f",
        "bin/git worktree add ../wt f",
        "/tmp/evil/git worktree add ../wt f",
        "/usr/bin/git worktree add ../wt f",
        "~/git worktree add ../wt f",
        "*/git worktree add ../wt f",
    ):
        assert decide(monkeypatch, capsys, repo, command)[0] == "silent", command
    # ...and the spellings the LEXER hands back as the word `git` are the
    # command `git`, so they stay allowed. Refusing them would spend a prompt
    # on nothing.
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f")[0] == "allow"
    # `\git` is TWO different commands and the boundary is right about both.
    # On POSIX the backslash escapes the `g` and the lexer hands back the word
    # `git`, so it is the command `git` and stays allowed. On Windows `\` is
    # the path separator, so `\git` names a file at the drive root -- exactly
    # what this case refuses above, and `silent` is the correct answer there.
    # Asserting one of the two on both platforms is what CI's Windows leg
    # caught: the guard was right and this case was not.
    want = "silent" if os.name == "nt" else "allow"
    assert decide(monkeypatch, capsys, repo, r"\git worktree add ../wt f")[0] == want
    assert wg.only_creates_a_worktree(
        "git -C /elsewhere worktree add ../wt f", str(repo)
    )


def test_a_backgrounded_creation_is_still_only_a_creation(monkeypatch, capsys, repo):
    """The one shape from that enumeration left allowed, pinned as a decision
    rather than left looking like an oversight. A trailing `&` backgrounds the
    creation and runs nothing else, so it is inside the bound the docstring
    claims -- and `… & rm -rf <path>` is two segments, where the second one
    fails the first test in `only_creates_a_worktree`."""
    grant(repo)
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f &")[0] == "allow"
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt f & rm -rf /tmp/x")[0]
        == "silent"
    )


def test_a_second_creation_never_denies(monkeypatch, capsys, repo):
    """The consented answer is a floor, not a fallthrough. Landing back on the
    ladder would put the single-stream deny in front of a session that has
    already been told yes.

    `silent` since #257, and the case still distinguishes the record arm from
    a fallthrough for every tuple below: without the record arm these reach
    the ladder and answer `deny` (no sessions, reliable), `ask` (an idle
    session) and `ask` (detection unusable). None of the three is silence, so
    a regression that dropped the arm is still caught here."""
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
            == "silent"
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


# --- the walk: a creation behind another verdict ---------------------------
#
# `main` classifies the FIRST segment it can read, while the writer below
# records for a creation ANYWHERE in a command that ran. Those two readings
# disagreed, and the gap was writable by whoever composed the command: a
# `git switch` in front of a creation took the verdict, the creation ladder
# never ran, and `PostToolUse` then minted session-wide consent for a question
# nobody was asked. The premise the whole design rests on -- a creation runs
# only if the deny did not fire and the ask was answered yes -- was false for
# exactly that shape.


def test_a_creation_behind_another_verdict_is_still_judged(monkeypatch, capsys, repo):
    """The class is any first segment whose OWN verdict is not None. `git
    status` classifies to nothing, so the walk moved on and the creation ladder
    did run -- that is the safe half, and the only half the build tried."""
    assert not consent_dir(repo).exists()
    for command in (
        "git switch feature/x && git worktree add ../wt f",
        "git switch feature/x; git worktree add ../wt f",
        "git switch feature/x || git worktree add ../wt f",
        "git checkout feature/x && git worktree add ../wt f",
        "git switch -c newbranch && git worktree add ../wt f",
        "git switch feature/x\ngit worktree add ../wt f",
    ):
        decision, reason = decide(monkeypatch, capsys, repo, command)
        assert decision == "deny", (command, decision)
        assert "git switch" in reason, command


def test_the_switch_ladder_keeps_every_verdict_it_had(monkeypatch, capsys, repo):
    """The alternative -- making a creation OUTRANK the earlier verdict --
    closes the same hole and costs this. A switch in a tree another session is
    working in denies, and under that alternative it becomes an `ask` about the
    creation: the branch is still taken out from under the other session, one
    approval later. So the switch ladder is left intact and only its one silent
    exit falls through."""
    # A session id per row. Two of these rows are `choose` sites, whose deny is
    # spent once per session per direction, so three rows sharing one id would
    # measure that budget rather than the verdict.
    for n, sessions in enumerate(
        ((ACTIVE, [], True), ([], IDLE, True), ([], [], False))
    ):
        assert (
            decide(
                monkeypatch,
                capsys,
                repo,
                "git switch feature/x && git worktree add ../wt f",
                sessions=sessions,
                session_id=f"s{n}",
            )[0]
            == "deny"
        ), sessions


def test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned(
    monkeypatch, capsys, repo
):
    """ "The three rows above the creation all deny" was true of two of them.

    Rows 1-b and 2 are `choose` sites, and `choose` denies ONCE per session per
    direction and asks on every attempt after. Seen red first, in both the
    idle and the detection-unusable states: the same command answered `deny`
    then `ask`, the `ask` read *Approve — switch branches in this shared tree*,
    and approving it created the worktree and minted session-wide consent with
    the creation question never put.

    What is pinned is the property rather than one verdict per attempt: at no
    attempt can this command proceed without the creation question having been
    put. Attempt 1 stops it with the switch's own two options, and every
    attempt after names the creation."""
    for name, sessions in (("idle", ([], IDLE, True)), ("blind", ([], [], False))):
        for attempt in (1, 2, 3):
            decision, reason = decide(
                monkeypatch,
                capsys,
                repo,
                "git switch feature/x && git worktree add ../wt f",
                sessions=sessions,
                session_id=name,
            )
            if attempt == 1:
                # The deny stops the whole command line, creation included.
                assert decision == "deny", (name, attempt, decision)
            else:
                assert "Attempting to create a worktree" in reason, (name, attempt)


def test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned(
    monkeypatch, capsys, repo
):
    """Silence is not the only way the creation question went unasked. Row 3 of
    the switch ladder asks about uncommitted changes riding along, and its own
    text says *the switch is allowed* -- it protects nothing about concurrency.
    Approving it created the worktree and recorded session-wide consent, so
    whether the creation was questioned at all came down to whether the tree
    happened to be dirty. Executed before this case: the clean tree denied and
    the dirty one asked about the changes, for the same command.

    The three rows above it keep their precedence, because those ARE the
    concurrency protections -- `test_the_switch_ladder_keeps_every_verdict_it_had`
    is the other half of this."""
    (repo / "f.txt").write_text("changed on purpose\n")
    decision, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x && git worktree add ../wt f"
    )
    assert decision == "deny", (decision, reason)
    assert "git switch" in reason, reason


def test_the_guard_is_never_silent_where_the_writer_records(
    monkeypatch, capsys, repo, tmp_path
):
    """The property, rather than the six shapes above. Whatever the writer
    would record for, the guard has already said something about -- a `deny`
    that stops the creation with the rest of the command, or an `ask` that puts
    the whole command line to a person, which is the standing a creation that
    runs is claimed to have.

    The `outside` half is the guard's SECOND silent exit: `judgeable` falls
    back to the session's own directory, so `top` is empty only when the SHELL
    is outside any repository -- and a `git -C <repo> worktree add` in the same
    command is not. Executed before this case: silent here, record written.

    **Silence was the first half of the property and not the whole of it.**
    An `ask` lets the command run too -- approving one runs every segment of
    the line -- so a row that asks about something else leaves the creation
    just as unjudged as a row that says nothing. Round 2 found the guard doing
    exactly that: two of the switch ladder's three concurrency rows are choice
    sites, which deny once per session per direction and `ask` after, and the
    second attempt at `git switch feature/x && git worktree add ../wt f`
    answered *Approve — switch branches in this shared tree*. So the test is
    now `deny`, or an `ask` whose text names the creation, and the attempt and
    tree-state axes are here because the old shape could not have seen it."""
    outside = tmp_path / "outside"
    outside.mkdir()
    holes = []
    for state, sessions in (
        ("single", ([], [], True)),
        ("active", (ACTIVE, [], True)),
        ("idle", ([], IDLE, True)),
        ("unusable", ([], [], False)),
    ):
        for cwd in (repo, outside):
            for n, command in enumerate(
                (
                    "git worktree add ../wt f",
                    "git status && git worktree add ../wt f",
                    "git switch feature/x && git worktree add ../wt f",
                    "git switch feature/x; git worktree add ../wt f",
                    "git checkout feature/x && git worktree add ../wt f",
                    "git switch feature/x && echo mid && git worktree add ../wt f",
                    "git switch feature/x && git worktree add ../wt f && git switch main",
                    "git switch feature/x && git worktree add ../wt f  # [worktree-ok]",
                    "git worktree list && git switch feature/x && git worktree add ../wt f",
                    "git switch feature/x && git worktree add ../wt f &",
                    f"git switch feature/x && git -C {repo} worktree add ../wt f",
                    f"cd {repo} && git switch feature/x && git worktree add ../wt f",
                )
            ):
                acted = wc.creation_directory(command, str(cwd))
                if not acted or not wc.optin.repo_root(acted):
                    continue
                # One session id per cell, then three attempts through it, so
                # both `choose` budgets are spent inside the cell rather than
                # measured across it.
                sid = f"{state}-{cwd is repo}-{n}"
                for _attempt in range(3):
                    verdict, reason = decide(
                        monkeypatch,
                        capsys,
                        repo,
                        command,
                        sessions=sessions,
                        session_id=sid,
                        cwd=cwd,
                    )
                    if verdict != "deny" and "Attempting to create a worktree" not in (
                        reason
                    ):
                        holes.append((state, str(cwd), verdict, command))
    assert not holes, holes


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
    and the next creation meets the question it always did.

    stdout being empty is not the claim: a traceback goes to STDERR and leaves
    stdout empty too, which is how a crashing hook and a quiet one look alike.
    The exit status and stderr are what tell them apart, so both are read."""
    blocked = consent_dir(repo)
    blocked.parent.mkdir(parents=True, exist_ok=True)
    blocked.write_text("not a directory")
    assert wc.record(str(repo), "me") is False
    r = subprocess.run(
        [sys.executable, os.path.join(HOOKS, "worktree_consent.py")],
        input=json.dumps(post(repo)),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == ""
    assert r.stderr.strip() == "", r.stderr
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f")[0] == "deny"


def test_a_directory_at_the_record_path_is_not_a_record(monkeypatch, capsys, repo):
    """The record is a FILE, and its existence is the fact. A directory of that
    name is not one — the same distinction `optin.py` draws for
    `specseal-scratch`, where a directory of the marker's name silenced every
    gate in the tree."""
    (consent_dir(repo) / "me").mkdir(parents=True)
    assert not wc.granted(str(repo), "me")
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f")[0] == "deny"


def test_a_session_id_that_is_only_separators_has_no_record_path(repo):
    """The id names a file, so an id that reduces to nothing must resolve to no
    path at all rather than to the directory above it. Left to the filesystem,
    `..` would be refused by `open` raising on a directory — a defence resting
    on a platform guarantee, which `agent-contract` §13 refuses."""
    for bad in ("", ".", "..", "/", "../..", os.sep):
        assert wc.consent_path(str(repo), bad) == "", bad
    assert wc.consent_path(str(repo), "me").endswith(os.path.join("me"))


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


def test_a_consent_record_buys_silence_for_a_compound_not_a_second_prompt(
    monkeypatch, capsys, repo
):
    """#257's headline table, as the three rows a person sees.

    A `silent` verdict here means the guard emitted NOTHING -- `decide`
    reports it only for empty stdout -- so it granted nothing and denied
    nothing, and the harness's own permission flow judges the call. That is
    the probe the ticket asked for, and it is what separates `silent` from
    `allow`: an `allow` speaks for the whole tool call, and none of these
    earns one.

    Measured on this repository's 0.9.2 release run: five worktrees created,
    two confirmations paid on exactly the middle row, both because the command
    carried a pipe or a `cd` -- the shape CLAUDE.md asks sessions to write
    when it tells them to batch independent runs into one call.
    """
    grant(repo)
    # bare creation -> the guard speaks for it, because it is all there is
    assert decide(monkeypatch, capsys, repo, "git worktree add ../wt f")[0] == "allow"
    # creation plus anything -> the guard withdraws and says nothing
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt f | tail -2")[0]
        == "silent"
    )
    # ...including the row that has to be argued for: `sudo` is left to the
    # user's own permissions.deny, which is where Bash(sudo:*) already lives.
    # A guard prompt on top of that was one stop buying nothing.
    assert (
        decide(monkeypatch, capsys, repo, "sudo git worktree add ../wt f")[0]
        == "silent"
    )


def test_the_first_creation_of_a_session_is_still_a_question(monkeypatch, capsys, repo):
    """#237's invariant, which #257 must not move. Without a record there is
    nothing to be silent about, and every shape above still meets the ladder."""
    for command in (
        "git worktree add ../wt f",
        "git worktree add ../wt f | tail -2",
        "sudo git worktree add ../wt f",
    ):
        assert decide(monkeypatch, capsys, repo, command)[0] != "silent", command


def test_the_silent_arm_emits_nothing_at_all(monkeypatch, capsys, repo):
    """`silent` is the ABSENCE of a decision, not a decision named "silent".

    Seen red by deleting the early return in `guard_worktree_creation`'s
    `granted` block. `respond` then prints `permissionDecision: "silent"` --
    not one of the three values the harness defines -- and every other case in
    this file still passed, because `decide` reports the same word for an
    empty stream as for that JSON. So the whole suite could not tell a guard
    that withdrew from a guard that answered with a word nobody implements.

    What the harness does with an undefined decision is not this repository's
    to assume, and #257 rests on the opposite: that a call the hook declines
    to decide falls to the harness's normal permission flow. That only holds
    if the hook truly says nothing, which is asserted here on the raw stream.
    """
    grant(repo)
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": ([], [], True))
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": "me",
            "tool_input": {"command": "git worktree add ../wt f | tail -2"},
            "cwd": str(repo),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    assert capsys.readouterr().out == "", "the silent arm printed a decision"
