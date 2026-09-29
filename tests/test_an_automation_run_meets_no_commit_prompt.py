"""In a session whose person pressed `automation`, the commit gate puts no
question to anybody: every stop is a `deny` addressed to the model.

Measured in session `ab2760f5`, the milestone-49 run (#662, #665): four
permission prompts reached the person in a run whose preset promised that
nothing would stop to ask. The gate's reading was right each time. What was
wrong was who the stop went to: one deny per session per repository, then an
`ask` for every later stop, and the first deny in the main checkout had been
spent by the orchestrator's own loop, so every agent's stop after it became a
person's prompt (`seal/specs/1790644505-the-commit-gate-stops-asking-about-
commits-that-are-not-there/spec.md` §*Where the four prompts came from*).

What changes is only the choice between `deny` and `ask`, and only where the
harness-written transcript holds the press `hooks/worktree_consent.py`'s
reader accepts. What the gate stops is unchanged, and
`tests/test_no_shape_the_base_stops_reads_silent.py` holds that half.

"Under the press" below means a transcript built by the fixture
`tests/test_the_guard_asks_once_per_session.py` uses, under a projects root
this case owns. No case reads a real transcript.
"""

import io
import json
import os
import shutil
import subprocess
import sys

import pytest
from conftest import load_hook_module
from test_no_shape_the_base_stops_reads_silent import make_repo, q
from test_the_guard_asks_once_per_session import ask_entries, write_transcript

gate = load_hook_module("commit-review-gate.py", "crg_automation")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))
import worktree_consent  # noqa: E402  -- the plain name the gate imports

PRESSED = "pressed"
PLAIN = "plain"
ASK_TOOL = "AskUserQuestion"


@pytest.fixture
def projects(monkeypatch, tmp_path):
    root = tmp_path / "projects"
    root.mkdir()
    monkeypatch.setattr(worktree_consent, "PROJECTS_ROOT", str(root))
    return root


def press(projects, cwd, session=PRESSED, **entries):
    write_transcript(projects, session, ask_entries(cwd, **entries))


def say(monkeypatch, capsys, command, cwd, session=PRESSED, transcript=None):
    """(decision, reason) for one issue of `command`; ("silent", "") for none."""
    payload = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd)}
    if session is not None:
        payload["session_id"] = session
    if transcript is not None:
        payload["transcript_path"] = str(transcript)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    gate.main()
    printed = capsys.readouterr().out.strip()
    if not printed:
        return "silent", ""
    out = json.loads(printed)["hookSpecificOutput"]
    return out["permissionDecision"], out["permissionDecisionReason"]


def spend_the_budget(repo, session=PRESSED):
    """Write the marker the gate writes at a session's first stop."""
    d = repo / ".git" / "specseal-commit-choice"
    d.mkdir(parents=True, exist_ok=True)
    (d / session).write_text("")


def forget_the_budget(repo):
    shutil.rmtree(repo / ".git" / "specseal-commit-choice", ignore_errors=True)


UNREADABLE_BODY = "bash <<'EOF'\ngit commit -m x\nEOF"
# The orchestrator's loop in all three milestone runs on disk, which spent the
# main checkout's deny for the whole run. Its `git` follows a `;`: the base
# reads no commit at all in `do git commit` written on one line, a reading
# this work item does not change (`phases/phase-1.md`).
UNREADABLE_LOOP = (
    'for w in a:1 b:2; do IFS=: read d n <<< "$w"; git -C $d commit -m x; done'
)


# --- S1 and S2: a stop in a repository the gate read -------------------------


def test_a_resolved_stop_after_the_budget_is_spent_is_refused(
    monkeypatch, capsys, projects, tmp_path
):
    """S1. The base answers `ask` here, which is a person's prompt."""
    repo = make_repo(tmp_path / "repo")
    press(projects, repo)
    spend_the_budget(repo)
    decision, reason = say(monkeypatch, capsys, "git commit -m x", repo)
    assert decision == "deny", reason
    assert "pressed `automation`" in reason


def test_a_parity_stop_under_the_press_is_refused_too(
    monkeypatch, capsys, projects, tmp_path
):
    """S1, the other arm. The review arm is waived so the parity arm alone
    stands; a parity prompt in an automation run breaks the same promise."""
    repo = make_repo(tmp_path / "repo")
    (repo / "seal" / "parity.md").write_text("# parity\n")
    press(projects, repo)
    command = ": '[no-review]'; git commit -m x"
    for _ in range(2):
        decision, reason = say(monkeypatch, capsys, command, repo)
        assert decision == "deny", reason
        assert "[no-parity]" in reason, "the waiver offered is not the arm's"
        assert "'[no-review]'" not in reason.split("pressed `automation`")[1]


def test_a_resolved_stop_the_first_time_puts_no_question(
    monkeypatch, capsys, projects, tmp_path
):
    """S2. The base's first stop instructs the model to put the choice up
    with the question tool, which a subagent has none of and which an
    automation run's main session must not use."""
    repo = make_repo(tmp_path / "repo")
    press(projects, repo)
    decision, reason = say(monkeypatch, capsys, "git commit -m x", repo)
    assert decision == "deny"
    assert ASK_TOOL not in reason


def test_the_press_is_read_against_the_sessions_own_repository(
    monkeypatch, capsys, projects, tmp_path
):
    """The press was given in the clone the session sits in, and a commit
    aimed at another repository is still this session's commit. Read against
    the target, it would be found nowhere, and the second stop would be a
    person's prompt again. Seen red by reading it against the target."""
    session = make_repo(tmp_path / "session")
    elsewhere = make_repo(tmp_path / "elsewhere")
    press(projects, session)
    command = f"git -C {q(elsewhere)} commit -m x"
    got = [say(monkeypatch, capsys, command, session)[0] for _ in "12"]
    assert got == ["deny", "deny"]


# --- S3: a stop where the gate could not read the repository -----------------


@pytest.mark.parametrize("command", [UNREADABLE_BODY, UNREADABLE_LOOP])
def test_an_unreadable_stop_is_refused_every_time(
    monkeypatch, capsys, projects, tmp_path, command
):
    """S3. A body a shell runs, and a commit inside a loop over a variable.
    The base denies the first and asks the second."""
    repo = make_repo(tmp_path / "repo")
    press(projects, repo)
    for attempt in (1, 2):
        decision, reason = say(monkeypatch, capsys, command, repo)
        assert decision == "deny", (attempt, reason)
        assert ASK_TOOL not in reason
        assert "pressed `automation`" in reason


# --- S4: the four measured shapes -------------------------------------------


def measured(w):
    return {
        "a heredoc edit, then a commit on the next line": (
            f"cd {q(w)} && python3 - <<'EOF'\nprint(1)\nEOF\n"
            "git add f && git commit -m x"
        ),
        "a ; after the cd, no heredoc": (
            f"cd {q(w)} && true ; git add f && git commit -m x"
        ),
        "a patch whose body loops over a commit string": (
            f"cd {q(w)} && python3 - <<'EOF'\ns = 'don\\'t'\n"
            f"for c in ['cd {w}; git commit -m x']:\n    print(c)\nEOF"
        ),
        "a body line equal to the delimiter ends it early": (
            "cat > note.md <<'EOF'\nquoted:\nEOF\ngit commit -m x\nEOF"
        ),
    }


def test_the_four_measured_shapes_are_refused_under_the_press(
    monkeypatch, capsys, projects, tmp_path
):
    """S4. The session directory is opted in and undeclared, and W is
    declared, as in the measured run. Without the press each is what it was:
    a deny, then an ask. Under it, a deny both times."""
    session = make_repo(tmp_path / "session")
    w = make_repo(tmp_path / "w", declared=True)
    press(projects, session)
    for name, command in measured(w).items():
        plain = [say(monkeypatch, capsys, command, session, PLAIN)[0] for _ in "12"]
        pressed = [say(monkeypatch, capsys, command, session)[0] for _ in "12"]
        assert plain == ["deny", "ask"], (name, plain)
        assert pressed == ["deny", "deny"], (name, pressed)
        forget_the_budget(session)


# --- S5: what the refusal says ----------------------------------------------


def reasons_under_the_press(monkeypatch, capsys, projects, tmp_path):
    repo = make_repo(tmp_path / "repo")
    press(projects, repo)
    return {
        "resolved": say(monkeypatch, capsys, "git commit -m x", repo)[1],
        "unreadable": say(monkeypatch, capsys, UNREADABLE_BODY, repo)[1],
    }


def test_the_refusal_names_the_ways_on_that_need_nobody(
    monkeypatch, capsys, projects, tmp_path
):
    """S5, pinned (contract §14). The ways on are in this order: make the
    repository readable, edit through the tools, the waiver only where no
    work item owns the commit, and hand back otherwise. Seen red by deleting
    each sentence of the text in turn."""
    for where, reason in reasons_under_the_press(
        monkeypatch, capsys, projects, tmp_path
    ).items():
        flat = " ".join(reason.split())
        order = [
            "pressed `automation` on the routing question",
            "so this gate puts no question to them",
            "The ways on, none of which needs a person:",
            "Re-issue the commit so the repository it lands in can be read:",
            "`git -C <absolute path> commit …` in a command of its own",
            "joined to the commit by `&&` alone",
            "because a failed `cd` leaves the shell there",
            "goes through the `Edit` tool, and a new file through the `Write` tool",
            "Neither leaves a command line for this gate to read.",
            "Only for a commit that belongs to no work item",
            ": '[no-review]'; <the same command>",
            "the marker is a pathspec and git rejects the command",
            "hand it back",
            "Re-issuing this command unchanged meets this same refusal.",
        ]
        at = []
        for phrase in order:
            assert phrase in flat, f"{where}: lost {phrase!r}"
            at.append(flat.index(phrase))
        assert at == sorted(at), f"{where}: the ways on are out of order"
        assert ASK_TOOL not in flat, where


def test_the_refusal_still_says_what_was_stopped(
    monkeypatch, capsys, projects, tmp_path
):
    """The state each base prompt opens with stays: which mark is missing in
    which repository, or that the repository could not be read."""
    reasons = reasons_under_the_press(monkeypatch, capsys, projects, tmp_path)
    assert reasons["resolved"].startswith("No review is recorded for this cycle")
    assert reasons["unreadable"].startswith(
        "This command contains something the gate cannot read"
    )


def test_a_later_routing_answer_takes_the_press_back(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 1 of 1790644505, yellow 5. A session that pressed `automation` for
    one work item and then answered `per axis` for another has, on its latest
    answer, a person who may be asked; the automation text would tell the
    model not to. The last answer from this clone stands, so the gate goes
    back to the base's deny-then-ask -- and the guard, whose reader this is,
    asks again as well. A later `automation` press gives it back."""
    repo = make_repo(tmp_path / "repo")
    first = ask_entries(repo, tool_id="toolu_01first")
    later = ask_entries(repo, answer="per axis", tool_id="toolu_01later")
    write_transcript(projects, PRESSED, first + later)
    assert not worktree_consent.automation_answered(str(repo), PRESSED)
    got = [say(monkeypatch, capsys, "git commit -m x", repo)[0] for _ in "12"]
    assert got == ["deny", "ask"]
    again = ask_entries(repo, tool_id="toolu_01again")
    write_transcript(projects, PRESSED, first + later + again)
    assert worktree_consent.automation_answered(str(repo), PRESSED)


def test_an_answer_to_another_question_leaves_the_press_standing(projects, tmp_path):
    """Only an answer to the routing question takes the press back. A later
    question the model put for something else is not a routing answer, and
    reading it as one would put a prompt back in front of a person who said
    nobody would be answering."""
    repo = make_repo(tmp_path / "repo")
    first = ask_entries(repo, tool_id="toolu_01first")
    other = ask_entries(
        repo,
        answer="yes",
        options=("yes", "no"),
        question="Which name?",
        tool_id="toolu_01other",
    )
    write_transcript(projects, PRESSED, first + other)
    assert worktree_consent.automation_answered(str(repo), PRESSED)


# --- S6: without the press, nothing changes ---------------------------------


def sequence(monkeypatch, capsys, repo, session, transcript=None):
    """Two resolved stops and two unreadable ones, from a fresh budget."""
    forget_the_budget(repo)
    out = []
    for command in ("git commit -m x", "git commit -m x"):
        out.append(say(monkeypatch, capsys, command, repo, session, transcript))
    forget_the_budget(repo)
    for command in (UNREADABLE_BODY, UNREADABLE_BODY):
        out.append(say(monkeypatch, capsys, command, repo, session, transcript))
    forget_the_budget(repo)
    return out


def test_without_the_press_the_answer_is_the_bases(
    monkeypatch, capsys, projects, tmp_path
):
    """S6. Every way of not finding the press is byte-identical to the answer
    with no transcript at all, which is the base's answer."""
    repo = make_repo(tmp_path / "repo")
    reference = sequence(monkeypatch, capsys, repo, PLAIN)
    assert [d for d, _ in reference] == ["deny", "ask", "deny", "ask"]

    other = tmp_path / "other"
    subprocess.run(["git", "init", "-q", str(other)], check=True, capture_output=True)

    def sidechain():
        use, result = ask_entries(repo)
        result["isSidechain"] = True
        return [use, result]

    variants = {
        "per axis": ask_entries(repo, answer="per axis"),
        "an Other answer": ask_entries(repo, answer="automation - but ask me first"),
        "a sidechain entry": sidechain(),
        "a press in another clone": ask_entries(other),
        "an unreadable transcript": ["{not json", '{"toolUseResult": {"answers'],
    }
    for name, entries in variants.items():
        write_transcript(projects, PLAIN, entries)
        assert sequence(monkeypatch, capsys, repo, PLAIN) == reference, name

    # A directory where the file would be.
    path = write_transcript(projects, PLAIN, [])
    path.unlink()
    path.mkdir()
    assert sequence(monkeypatch, capsys, repo, PLAIN) == reference, "a directory"


def test_a_reader_that_raises_or_did_not_load_is_no_press(
    monkeypatch, capsys, projects, tmp_path
):
    """S6, contract §13. `hooks/dispatch.py` skips a gate that raises, and a
    skipped gate is silence, so the reader failing must land on the base's
    answer rather than on nothing. Seen red with the guard around the reader
    removed."""
    repo = make_repo(tmp_path / "repo")
    press(projects, repo)
    reference = sequence(monkeypatch, capsys, repo, PLAIN)

    def raises(*_args, **_kwargs):
        raise RuntimeError("a transcript shape nobody measured")

    with monkeypatch.context() as m:
        m.setattr(worktree_consent, "automation_answered", raises)
        assert sequence(monkeypatch, capsys, repo, PRESSED) == reference
    with monkeypatch.context() as m:
        m.setattr(gate, "worktree_consent", None)
        assert sequence(monkeypatch, capsys, repo, PRESSED) == reference


def test_the_press_is_read_only_once_a_stop_is_decided(
    monkeypatch, capsys, projects, tmp_path
):
    """The transcript scan is paid on a stop and never on a command the gate
    lets through. Seen red by reading the press before the declaration."""
    session = make_repo(tmp_path / "session")
    w = make_repo(tmp_path / "w", declared=True)
    press(projects, session)
    calls = []
    real = worktree_consent.automation_answered

    def counted(*args, **kwargs):
        calls.append(args)
        return real(*args, **kwargs)

    monkeypatch.setattr(worktree_consent, "automation_answered", counted)
    for command in ("git status", f"git -C {q(w)} commit -m x", "echo git commit"):
        assert say(monkeypatch, capsys, command, session)[0] == "silent", command
    assert calls == []
    assert say(monkeypatch, capsys, "git commit -m x", session)[0] == "deny"
    assert len(calls) == 1


def test_a_session_with_no_id_still_asks(monkeypatch, capsys, projects, tmp_path):
    """S6. No session id, no transcript to read, and no way to record that a
    question was put, so a deny would repeat forever."""
    repo = make_repo(tmp_path / "repo")
    press(projects, repo)
    for command in ("git commit -m x", UNREADABLE_BODY):
        assert say(monkeypatch, capsys, command, repo, None)[0] == "ask", command


# --- S8: a declared target stays silent -------------------------------------


def test_a_declared_target_stays_silent_under_the_press(
    monkeypatch, capsys, projects, tmp_path
):
    """S8. The press is read only after a stop is decided, so a commit the
    base lets through is let through. Seen red by a mutation that refuses
    under the press before the declaration is read."""
    session = make_repo(tmp_path / "session")
    w = make_repo(tmp_path / "w", declared=True)
    press(projects, session)
    for command in (f"cd {q(w)} && git commit -m x", f"git -C {q(w)} commit -m x"):
        assert say(monkeypatch, capsys, command, session) == ("silent", ""), command
