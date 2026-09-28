"""A gate that fails to load says so (#28).

Work item 1790635415. `hooks/dispatch.py` skips a gate that raises, so the
rest of its group still decides and no tool call is blocked. That stays. What
changes is that the skip leaves a record under the git common dir, keyed by
session and gate, and the `stop` group says every pending record once, at the
end of the main session's turn, as a `systemMessage`.

Every case drives `dispatch.py` from a COPY of `hooks/` as a subprocess, which
is what production spawns. A broken gate is one whose file is replaced by
`def broken(:\\n`, the shape
`tests/test_the_implementer_is_recorded.py#test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone`
already uses. The live `hooks/` is never touched.
"""

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys

from conftest import decision_of, load_hook_module

HOOKS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hooks"))
BROKEN = "def broken(:\n"
RECORDS = "specseal-gate-failure"

# The words a person reads (contract §14). Pinned whole, so an edit that
# changes what the line says has to change this too.
LABEL_ONE = "SpecSeal: 1 gate failed and was skipped"
CLOSING = (
    "Nothing was blocked, and each gate is said once per session. "
    "Updating or reinstalling the plugin usually repairs it."
)


def hooks_copy(tmp_path, files):
    """A copy of `hooks/` with each `files` entry written over the file of
    that name; a value of None removes it."""
    hooks = tmp_path / "hooks"
    shutil.copytree(HOOKS, hooks, ignore=shutil.ignore_patterns("__pycache__"))
    for name, body in files.items():
        path = hooks / name
        if body is None:
            path.unlink()
        else:
            path.write_text(body, encoding="utf-8")
    return hooks


def dispatch(hooks, group, body, cwd=None):
    """`dispatch.py <group>` from `hooks`, as the harness spawns it. `body`
    is sent as JSON, or as it is where it is already a string."""
    r = subprocess.run(
        [sys.executable, str(hooks / "dispatch.py"), group],
        input=body if isinstance(body, str) else json.dumps(body),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        cwd=cwd,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


def bash(repo, session, command="git commit -m x", **extra):
    body = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": command},
        "cwd": str(repo),
    }
    body.update(extra)
    return body


def stop(hooks, repo, session, **extra):
    body = {"hook_event_name": "Stop", "session_id": session, "cwd": str(repo)}
    body.update(extra)
    return dispatch(hooks, "stop", body)


def said(stdout):
    """The `systemMessage` lines of one JSON object, which carries no
    decision (S12)."""
    out = json.loads(stdout)
    assert "hookSpecificOutput" not in out and "decision" not in out, out
    return out["systemMessage"].split("\n")


def records(repo, session):
    directory = repo / ".git" / RECORDS / session
    return sorted(os.listdir(directory)) if directory.is_dir() else []


def opted_in(repo):
    (repo / "seal").mkdir()
    return repo


# --- S1, S2, S3, S4: said once per session, and the group decides as before --


def test_a_broken_gate_is_said_at_the_end_of_the_turn_and_only_once(repo, tmp_path):
    """S1, S3, S4, S12, S14. Seen red against the `dispatch.py` that only
    swallowed, where `stop` printed nothing at all."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"commit-review-gate.py": BROKEN})

    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    assert records(repo, "s-x") == ["commit-review-gate.py.pending"]
    lines = said(stop(hooks, repo, "s-x"))
    assert lines[0] == LABEL_ONE, lines
    assert lines[1].startswith(
        "commit-review-gate.py failed to load in pre-bash (SyntaxError: "
    ), lines
    assert lines[1].endswith(
        "); calls went ahead without it, and the other gates in pre-bash still decided."
    ), lines
    assert lines[2:] == [CLOSING], lines
    assert records(repo, "s-x") == ["commit-review-gate.py.reported"]

    # S3: the same session, the same broken gate: nothing new, nothing said.
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    assert records(repo, "s-x") == ["commit-review-gate.py.reported"]
    assert stop(hooks, repo, "s-x") == ""

    # S4: another session is told for itself.
    dispatch(hooks, "pre-bash", bash(repo, "s-y"))
    assert said(stop(hooks, repo, "s-y"))[0] == LABEL_ONE


def test_the_group_decides_exactly_as_it_did_without_the_gate(repo, tmp_path):
    """S2. The report leaves the failing call's own stdout alone: a broken
    commit gate and an absent one give the same bytes."""
    opted_in(repo)
    broken = hooks_copy(tmp_path / "a", {"commit-review-gate.py": BROKEN})
    absent = hooks_copy(tmp_path / "b", {"commit-review-gate.py": None})
    assert dispatch(broken, "pre-bash", bash(repo, "s-a")) == dispatch(
        absent, "pre-bash", bash(repo, "s-b")
    )


def test_a_gate_that_raises_in_main_is_said_as_a_run_failure(repo, tmp_path):
    """S5. The import succeeded and `main()` raised: the line says `while
    running`, and names the class and the message's first line."""
    opted_in(repo)
    hooks = hooks_copy(
        tmp_path,
        {"mode-gate.py": "def main():\n    raise RuntimeError('boom\\nsecond line')\n"},
    )
    dispatch(hooks, "pre-bash", bash(repo, "s-x", command="ls"))
    lines = said(stop(hooks, repo, "s-x"))
    assert lines[1] == (
        "mode-gate.py failed while running in pre-bash (RuntimeError: boom); "
        "calls went ahead without it, and the other gates in pre-bash still "
        "decided."
    ), lines


def test_a_system_exit_from_main_is_not_a_failure(repo, tmp_path):
    """`worktree-guard.py` ends with `sys.exit(0)` from `main()` at nine
    sites, so a `SystemExit` there is a gate finishing, not failing."""
    opted_in(repo)
    hooks = hooks_copy(
        tmp_path, {"mode-gate.py": "import sys\ndef main():\n    sys.exit(0)\n"}
    )
    dispatch(hooks, "pre-bash", bash(repo, "s-x", command="ls"))
    assert records(repo, "s-x") == []


# --- S8, S13: where nothing is written -----------------------------------------


def test_a_repository_that_never_opted_in_records_nothing(repo, tmp_path):
    """S8. A globally installed plugin does not write into, or speak about,
    a repository that does not run the workflow."""
    hooks = hooks_copy(tmp_path, {"commit-review-gate.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    assert not (repo / ".git" / RECORDS).exists()
    assert stop(hooks, repo, "s-x") == ""


def test_nowhere_to_write_is_todays_silence_and_nothing_raises(repo, tmp_path):
    """S13. No session id, or a records directory that cannot be made — a
    FILE of that name, because the CI job runs as root and `chmod` stops
    nothing there (`tests/test_gates_do_not_fail_open.py` records why). Each
    leaves the group's stdout what it is with the gate absent, and exits 0.

    Each side of a comparison gets a session of its own: `mode-gate.py`
    denies the first call of a session and not the next, so two calls under
    one id differ on that gate's state and say nothing about this one."""
    opted_in(repo)
    broken = hooks_copy(tmp_path / "a", {"commit-review-gate.py": BROKEN})
    absent = hooks_copy(tmp_path / "b", {"commit-review-gate.py": None})

    nameless = bash(repo, "")
    del nameless["session_id"]
    assert dispatch(broken, "pre-bash", nameless) == dispatch(
        absent, "pre-bash", nameless
    )
    assert not (repo / ".git" / RECORDS).exists(), "recorded with no session"

    (repo / ".git" / RECORDS).write_text("", encoding="utf-8")
    assert dispatch(broken, "pre-bash", bash(repo, "s-f1")) == dispatch(
        absent, "pre-bash", bash(repo, "s-f2")
    )
    assert stop(broken, repo, "s-f1") == ""


def test_a_session_id_cannot_name_a_directory_outside_the_records(repo, tmp_path):
    """The id becomes a path part, so a separator in a malformed one must not
    escape — `hooks/worktree-guard.py#already_asked` measured `../../escaped`
    putting a file at the repository root."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"commit-review-gate.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "../../escaped"))
    assert not (repo / "escaped").exists()
    assert not (repo / ".git" / "escaped").exists()
    assert records(repo, "escaped") == ["commit-review-gate.py.pending"]
    # `..` has no separator to strip, and would name the records directory's
    # parent: the common dir itself.
    dispatch(hooks, "pre-bash", bash(repo, ".."))
    assert not (repo / ".git" / "commit-review-gate.py.pending").exists()


def test_a_payload_the_report_cannot_read_records_nothing(repo, tmp_path):
    """Not JSON, not an object, or an empty `cwd`: nothing is recorded,
    nothing raises, and dispatch exits 0 with the group's own stdout. An
    empty `cwd` must not fall back to the directory the process happens to
    stand in, which is a repository here."""
    opted_in(repo)
    broken = hooks_copy(tmp_path / "a", {"commit-review-gate.py": BROKEN})
    absent = hooks_copy(tmp_path / "b", {"commit-review-gate.py": None})
    for payload in ("not json", "[1, 2]"):
        assert dispatch(broken, "pre-bash", payload) == dispatch(
            absent, "pre-bash", payload
        )
    dispatch(broken, "pre-bash", bash(repo, "s-x", cwd=""), cwd=str(repo))
    assert not (repo / ".git" / RECORDS).exists()


# --- S7: a `SystemExit` at load is isolated --------------------------------


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_system_exit_at_load_does_not_take_the_group_down(
    repo, tmp_path, monkeypatch
):
    """S7. A module body calling `sys.exit(0)` used to escape `run_gate`,
    whose catch was `Exception` alone, and end the whole group: the commit
    gate after it never decided. Seen red against the phase-1 tree, where
    `main()` raised `SystemExit` and printed nothing. The shape of
    `tests/test_dispatch.py#test_a_crashing_gate_does_not_take_the_group_down`,
    run against a copy so the planted gate never enters the live `hooks/`."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"exits-at-load.py": "import sys\nsys.exit(0)\n"})
    d = load(hooks / "dispatch.py", "dispatch_for_s7")
    monkeypatch.setattr(
        d, "GROUPS", {"g": ("exits-at-load.py", "commit-review-gate.py")}
    )
    out = io.StringIO()
    monkeypatch.setattr(sys, "argv", ["dispatch.py", "g"])
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(bash(repo, "s-x"))))
    with contextlib.redirect_stdout(out):
        d.main()
    assert decision_of(out.getvalue()) == "deny", out.getvalue()
    record = repo / ".git" / RECORDS / "s-x" / "exits-at-load.py.pending"
    body = json.loads(record.read_text(encoding="utf-8"))
    assert body == {
        "group": "g",
        "phase": "load",
        "error": "SystemExit",
        "message": "0",
    }


# --- S6, S6b: a shared module breaks several gates -------------------------


def gates_said(lines):
    """The gate each line of a report names, in the order said."""
    return [line.split(" ", 1)[0] for line in lines[1:-1]]


def test_a_broken_shared_module_names_every_gate_that_imports_it(repo, tmp_path):
    """S6. `cmdline.py` is imported by two `pre-bash` gates and two
    `post-bash` gates, and every one of them is said, once, with no gate
    that does not import it. The `post-bash` call is not a commit: a copy of
    `hooks/` has no `skills/` beside it, so `evidence-advisor.py` would fail
    at run on a commit for want of its checker, which is the fixture and not
    `cmdline.py`."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"cmdline.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    dispatch(
        hooks,
        "post-bash",
        bash(repo, "s-x", command="ls", hook_event_name="PostToolUse"),
    )
    lines = said(stop(hooks, repo, "s-x"))
    assert lines[0] == "SpecSeal: 4 gates failed and were skipped", lines
    assert sorted(gates_said(lines)) == [
        "commit-review-gate.py",
        "implementer-notice.py",
        "worktree-guard.py",
        "worktree_consent.py",
    ], lines
    assert lines[-1] == CLOSING


def test_a_gate_that_fails_to_load_names_every_group_that_loads_it(repo, tmp_path):
    """Round 1's 🟡 1. A load failure belongs to the file, so it fails in
    every group that loads it, and the record is written once, by the first.
    `worktree-guard.py` sits in `pre-bash` and `pre-agent`, and the
    `pre-agent` half is the `isolation: "worktree"` spawn going unguarded:
    one `pre-bash` failure must not read as a Bash-only gap. A group where
    the gate stands alone, `post-agent` for `worktree_consent.py`, is named
    among the failures and not among the groups whose other gates decided."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"cmdline.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    dispatch(
        hooks,
        "post-bash",
        bash(repo, "s-x", command="ls", hook_event_name="PostToolUse"),
    )
    lines = said(stop(hooks, repo, "s-x"))
    by_gate = {line.split(" ", 1)[0]: line for line in lines[1:-1]}
    guard, consent = by_gate["worktree-guard.py"], by_gate["worktree_consent.py"]
    assert guard.startswith(
        "worktree-guard.py failed to load in pre-bash and pre-agent ("
    ), guard
    assert guard.endswith(
        "; calls went ahead without it, and the other gates in pre-bash and "
        "pre-agent still decided."
    ), guard
    assert consent.startswith(
        "worktree_consent.py failed to load in post-bash and post-agent ("
    ), consent
    assert consent.endswith(
        "; calls went ahead without it, and the other gates in post-bash still decided."
    ), consent
    assert by_gate["commit-review-gate.py"].startswith(
        "commit-review-gate.py failed to load in pre-bash ("
    ), by_gate


def test_a_broken_opt_in_module_is_said_rather_than_read_as_not_opted_in(
    repo, tmp_path
):
    """S6b. `optin.py` is what the report asks whether to speak, and it is
    the broken module: "cannot tell" writes the record. `sealer-stamp.py`
    fails in the `stop` group itself and is said in the same invocation."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"optin.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    lines = said(stop(hooks, repo, "s-x"))
    assert sorted(gates_said(lines)) == [
        "commit-review-gate.py",
        "mode-gate.py",
        "sealer-stamp.py",
        "worktree-guard.py",
    ], lines
    assert "sealer-stamp.py failed to load in stop (SyntaxError: " in "\n".join(
        lines
    ), lines
    assert any(
        line.startswith("sealer-stamp.py ")
        and line.endswith("); calls went ahead without it.")
        for line in lines
    ), lines


def test_records_are_said_oldest_first(repo, tmp_path):
    """One line per record, in the order the gates failed — read from each
    record's time, so a name that sorts first is not said first."""
    opted_in(repo)
    directory = repo / ".git" / RECORDS / "s-x"
    directory.mkdir(parents=True)
    for n, gate in enumerate(("worktree-guard.py", "commit-review-gate.py")):
        path = directory / (gate + ".pending")
        path.write_text(json.dumps({"group": "pre-bash"}), encoding="utf-8")
        os.utime(path, ns=(10**18 + n, 10**18 + n))
    lines = said(stop(hooks_copy(tmp_path, {}), repo, "s-x"))
    assert gates_said(lines) == ["worktree-guard.py", "commit-review-gate.py"]


def test_a_record_that_cannot_be_read_still_names_its_gate(repo, tmp_path):
    """A record another plugin version wrote, or a half-written one: the
    gate's name is the file's name, and that is the report's whole value."""
    opted_in(repo)
    directory = repo / ".git" / RECORDS / "s-x"
    directory.mkdir(parents=True)
    planted = {
        "lint-python.py": "not json",
        "mode-gate.py": "[1]",
        "version-check.py": json.dumps({"group": 5, "phase": "load"}),
        "session-lease.py": json.dumps({"error": "OSError"}),
        "worktree-guard.py": json.dumps(
            {"group": "pre-bash\nstop", "error": "E", "message": "a\n  b"}
        ),
    }
    for n, (gate, body) in enumerate(planted.items()):
        path = directory / (gate + ".pending")
        path.write_text(body, encoding="utf-8")
        os.utime(path, ns=(10**18 + n, 10**18 + n))
    lines = said(stop(hooks_copy(tmp_path, {}), repo, "s-x"))
    assert lines[1:-1] == [
        "lint-python.py failed; calls went ahead without it.",
        "mode-gate.py failed; calls went ahead without it.",
        "version-check.py failed to load; calls went ahead without it.",
        "session-lease.py failed (OSError); calls went ahead without it.",
        "worktree-guard.py failed in pre-bash stop (E: a b); calls went ahead "
        "without it.",
    ], lines


def test_a_record_that_cannot_be_claimed_is_not_said(repo, tmp_path):
    """The rename to `.reported` comes before the line, so a record another
    drawer took first — here, one whose `.reported` name is a directory the
    rename cannot replace — is not said by this one."""
    opted_in(repo)
    directory = repo / ".git" / RECORDS / "s-x"
    (directory / "mode-gate.py.reported").mkdir(parents=True)
    (directory / "mode-gate.py.pending").write_text("{}", encoding="utf-8")
    assert stop(hooks_copy(tmp_path, {}), repo, "s-x") == ""


def test_records_in_a_repository_not_opted_in_are_not_said(repo, tmp_path):
    """A record that is there in a repository that does not run the workflow
    — left from before it opted out — is neither said nor taken."""
    directory = repo / ".git" / RECORDS / "s-x"
    directory.mkdir(parents=True)
    (directory / "mode-gate.py.pending").write_text("{}", encoding="utf-8")
    assert stop(hooks_copy(tmp_path, {}), repo, "s-x") == ""
    assert records(repo, "s-x") == ["mode-gate.py.pending"]


def test_a_record_is_created_once_and_asked_about_once(repo, monkeypatch):
    """The opt-in is asked only for a gate not yet written down, so a gate
    that stays broken costs no `optin.py` load after its first record. And
    the file is created exclusively: a record that appears between the check
    and the write — the race, forced here by blinding the check — is not
    overwritten."""
    opted_in(repo)
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_the_record")
    asked = []
    real = d.opted_in
    monkeypatch.setattr(d, "opted_in", lambda *a: asked.append(a) or real(*a))
    body = bash(repo, "s-x")
    failure = [("mode-gate.py", "run", RuntimeError("first"))]
    d.record("pre-bash", failure, body)
    d.record("pre-bash", [("mode-gate.py", "run", RuntimeError("second"))], body)
    assert len(asked) == 1, asked
    # Blind only the records directory: `toplevel` asks `exists` too, and
    # blinding that would stop the call before it reached the write.
    real_exists = os.path.exists
    monkeypatch.setattr(
        d.os.path, "exists", lambda p: False if RECORDS in str(p) else real_exists(p)
    )
    d.record("pre-bash", [("mode-gate.py", "run", RuntimeError("third"))], body)
    path = repo / ".git" / RECORDS / "s-x" / "mode-gate.py.pending"
    assert json.loads(path.read_text(encoding="utf-8"))["message"] == "first"


def test_a_message_is_its_first_line_and_capped():
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_the_cap")
    assert d.first_line(RuntimeError("\n  one  \ntwo")) == "one"
    assert d.first_line(RuntimeError("y" * 500)) == "y" * d.MESSAGE_CAP
    assert d.MESSAGE_CAP == 200


# --- S10: a subagent's failure reaches the main session ----------------------


def test_a_subagents_failure_is_said_at_the_main_sessions_stop(repo, tmp_path):
    """S10. A subagent's tool payload carries the parent's `session_id`, so
    its failure is recorded under the main session. A `Stop`-shaped payload
    naming an agent is a subagent's end, and draws nothing."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"session-lease.py": BROKEN})
    dispatch(
        hooks,
        "post-bash",
        bash(repo, "s-x", command="ls", hook_event_name="PostToolUse", agent_id="a-1"),
    )
    assert records(repo, "s-x") == ["session-lease.py.pending"]
    assert stop(hooks, repo, "s-x", agent_id="a-1") == ""
    assert stop(hooks, repo, "s-x", hook_event_name="SubagentStop") == ""
    assert records(repo, "s-x") == ["session-lease.py.pending"]
    assert said(stop(hooks, repo, "s-x"))[0] == LABEL_ONE


# --- S9: beside the stamp ------------------------------------------------------

STAMP = os.path.join(
    os.path.dirname(HOOKS), "skills", "verify", "scripts", "seal_stamp.py"
)
STAMP_VALUES = {
    "tree": "aaa1111",
    "base": "bbb2222",
    "from": "origin/base",
    "item": "/x/seal/specs/1799000000-an-item",
    "session": "s-1",
    "scale": 0.9,
    "rows": [("SEALED", ""), None, ("tree", "aaa1111"), ("suite", "3 passed")],
}


def test_the_report_goes_before_the_stamp_and_the_stamp_is_unchanged(repo, tmp_path):
    """S9. One `systemMessage`: the report first, then a blank line, then
    the stamp exactly as it is drawn with nothing pending — so the drawing
    stays the last thing on the screen (#400). The live `hooks/` is run, not
    a copy, because `sealer-stamp.py` reaches `seal_stamp.py` beside it; the
    record is planted, which is also a record written by another process."""
    opted_in(repo)
    stamp = load(STAMP, "seal_stamp_for_s9")
    for session in ("s-alone", "s-both"):
        stamp.write_values(str(repo / ".git"), session, STAMP_VALUES)
    directory = repo / ".git" / RECORDS / "s-both"
    directory.mkdir(parents=True)
    (directory / "mode-gate.py.pending").write_text(
        json.dumps(
            {"group": "pre-bash", "phase": "run", "error": "KeyError", "message": "'x'"}
        ),
        encoding="utf-8",
    )
    alone = said(stop_live(repo, "s-alone"))
    both = said(stop_live(repo, "s-both"))
    assert alone[0].startswith("SEALED aaa1111"), alone
    assert both[: len(both) - len(alone) - 1] == [
        LABEL_ONE,
        "mode-gate.py failed while running in pre-bash (KeyError: 'x'); calls "
        "went ahead without it, and the other gates in pre-bash still decided.",
        CLOSING,
    ], both
    assert both[len(both) - len(alone) - 1] == "", both
    assert both[len(both) - len(alone) :] == alone, "the stamp moved"


def stop_live(repo, session):
    r = subprocess.run(
        [sys.executable, os.path.join(HOOKS, "dispatch.py"), "stop"],
        input=json.dumps(
            {"hook_event_name": "Stop", "session_id": session, "cwd": str(repo)}
        ),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


# --- Q2: the walk is duplicated, and the twins agree -------------------------


def git(repo, *args):
    """git driven from Python, so no Bash line carries a commit (§8)."""
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def test_the_walk_agrees_with_its_twin_in_sealer_stamp(repo, tmp_path):
    """`questions.md` Q2, answered duplicated: `dispatch.py` cannot import
    `sealer-stamp.py` without importing `console` and `optin` with it. So the
    two walks are held to one answer — in a subdirectory of the main
    checkout, and in a linked worktree, where `.git` is a file and git is
    asked. A failure recorded from the worktree is said from the checkout."""
    d = load_hook_module("dispatch.py", "dispatch_for_the_twin")
    sealer = load_hook_module("sealer-stamp.py", "sealer_stamp_for_the_twin")
    optin = load_hook_module("optin.py", "optin_for_the_twin")
    tree = tmp_path / "tree"
    git(repo, "worktree", "add", "-q", str(tree), "feature/x")
    (repo / "docs" / "deep").mkdir(parents=True)
    for cwd in (repo / "docs" / "deep", tree):
        top = d.toplevel(str(cwd))
        assert top == sealer.toplevel(str(cwd)), cwd
        assert d.common_dir(top) == optin.git_common_dir(top), cwd
    assert os.path.samefile(d.common_dir(d.toplevel(str(tree))), repo / ".git")

    def no_process(*_a, **_k):
        raise AssertionError("a main checkout started a process")

    real_run = d.subprocess.run
    d.subprocess.run = no_process
    try:
        assert d.common_dir(str(repo)) == str(repo / ".git")
    finally:
        d.subprocess.run = real_run

    # Local mode, so the worktree's branch, which has no `seal/`, is opted
    # in from both trees.
    (repo / ".git" / "seal").mkdir()
    hooks = hooks_copy(tmp_path, {"commit-review-gate.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(tree, "s-x"))
    assert records(repo, "s-x") == ["commit-review-gate.py.pending"]
    assert said(stop(hooks, repo, "s-x"))[0] == LABEL_ONE


def stop_in_process(repo, monkeypatch, capsys, printed):
    """`dispatch.main()` for `stop`, with the group's own output replaced by
    `printed`; what it printed."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_the_join")
    monkeypatch.setattr(d, "run_gate", lambda _gate, _payload: printed)
    monkeypatch.setattr(sys, "argv", ["dispatch.py", "stop"])
    body = {"hook_event_name": "Stop", "session_id": "s-x", "cwd": str(repo)}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(body)))
    d.main()
    return capsys.readouterr().out


def pending_record(repo):
    directory = repo / ".git" / RECORDS / "s-x"
    directory.mkdir(parents=True)
    (directory / "mode-gate.py.pending").write_text("{}", encoding="utf-8")


def test_plain_text_at_stop_is_left_alone_and_the_records_wait(
    repo, monkeypatch, capsys
):
    """No gate in `stop` prints plain text, and plain `Stop` stdout reaches a
    different reader than a `systemMessage`. So such a turn end is printed
    as it was, and the records wait for one that can carry them."""
    opted_in(repo)
    pending_record(repo)
    assert stop_in_process(repo, monkeypatch, capsys, "plain words\n") == (
        "plain words\n"
    )
    assert records(repo, "s-x") == ["mode-gate.py.pending"]


def test_only_nothing_or_an_object_can_carry_the_report():
    """JSON that is not an object has nowhere to put a message either. It
    cannot reach `beside` through `main()` today — `merge()`'s own reader
    raises on it first — so it is asked of `beside` directly."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_beside")
    assert d.beside("  \n") == {}
    assert d.beside('{"a": 1}') == {"a": 1}
    assert d.beside("[1]") is None
    assert d.beside("plain") is None


def test_an_object_without_a_message_takes_the_report_as_its_message(
    repo, monkeypatch, capsys
):
    """The group's own keys are kept, and the report is the whole message
    where the group had none."""
    opted_in(repo)
    pending_record(repo)
    out = json.loads(stop_in_process(repo, monkeypatch, capsys, '{"continue": true}'))
    assert out["continue"] is True
    assert out["systemMessage"].split("\n")[0] == LABEL_ONE
    assert out["systemMessage"].endswith(CLOSING), out


# --- S14: the policy says it, and names what enforces it -----------------------


def test_the_registration_section_says_a_failure_is_said_and_names_its_case():
    """S14. The ratified rule in `docs/commit-review-gate-spec.md`
    §*Registration* was that a raising gate is skipped. It now also says the
    skip is said, and its `Enforced by:` line names the case above that pins
    the words a person reads."""
    path = os.path.join(os.path.dirname(HOOKS), "docs", "commit-review-gate-spec.md")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    start = text.index("## Registration — gates run in groups, not one process each")
    section = text[start : text.index("\n## ", start + 1)]
    flat_text = " ".join(section.split())
    assert (
        "**A gate that fails is said once per session, at the end of the main "
        "session's turn, and the call it failed on still goes ahead.**"
    ) in flat_text, section
    assert "<!-- specs/1790635415-a-gate-that-fails-to-load-says-so -->" in section
    enforced = [ln for ln in section.splitlines() if ln.startswith("Enforced by: ")]
    assert len(enforced) == 1, enforced
    assert (
        "tests/test_a_gate_that_fails_says_so.py::"
        "test_a_broken_gate_is_said_at_the_end_of_the_turn_and_only_once"
    ) in enforced[0], enforced
