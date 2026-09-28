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

import json
import os
import shutil
import subprocess
import sys

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


def dispatch(hooks, group, body):
    r = subprocess.run(
        [sys.executable, str(hooks / "dispatch.py"), group],
        input=json.dumps(body),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
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
