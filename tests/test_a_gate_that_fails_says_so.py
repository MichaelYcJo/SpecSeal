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

import pytest
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
    at = body.pop("at")
    assert body == {
        "group": "g",
        "phase": "load",
        "error": "SystemExit",
        "message": "0",
    }
    # When and in what order this call's failures happened: the writer's
    # clock in nanoseconds, and this gate's place among them.
    assert type(at[0]) is int and at[0] > 0 and at[1] == 0, at


# --- S6, S6b: a shared module breaks several gates -------------------------


def gates_said(lines):
    """The gate each line of a report names, in the order said."""
    return [line.split(" ", 1)[0] for line in lines[1:-1]]


@pytest.mark.parametrize(
    "broken, named",
    [
        ({"cmdline.py": BROKEN}, ["commit-review-gate.py", "implementer-notice.py"]),
        ({"cmdline_base.py": BROKEN}, ["worktree-guard.py", "worktree_consent.py"]),
        (
            {"cmdline.py": BROKEN, "cmdline_base.py": BROKEN},
            [
                "commit-review-gate.py",
                "worktree-guard.py",
                "implementer-notice.py",
                "worktree_consent.py",
            ],
        ),
    ],
    ids=["cmdline", "cmdline_base", "both"],
)
def test_a_broken_shared_module_names_every_gate_that_imports_it(
    repo, tmp_path, broken, named
):
    """S6. A broken shared reader names every gate that imports it, once, and
    no gate that does not. `cmdline.py` is imported by the commit gate and
    `implementer-notice.py`; since #689 `cmdline_base.py`, the reader frozen at
    `86256492`, is imported by the worktree guard and `worktree_consent.py`. The
    commit gate's own import of `worktree_consent` is guarded, so a broken
    `cmdline_base.py` does not name it. The `post-bash` call is not a commit: a
    copy of `hooks/` has no `skills/` beside it, so `evidence-advisor.py` would
    fail at run on a commit for want of its checker, which is the fixture and
    not the reader.

    Changed by #689 twice. Round 1's fix pass broke both readers at once to
    keep four gates named, which lost the per-module "no gate that does not"
    (round 2 of 1790745049, white 4); each reader is now broken alone as well."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, broken)
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    dispatch(
        hooks,
        "post-bash",
        bash(repo, "s-x", command="ls", hook_event_name="PostToolUse"),
    )
    # Every record gets one file time, as a file system with coarse times
    # gives records written in one call (Windows CI did): the order said is
    # the order the gates failed, which each record carries itself.
    for path in (repo / ".git" / RECORDS / "s-x").iterdir():
        os.utime(path, ns=(10**18, 10**18))
    lines = said(stop(hooks, repo, "s-x"))
    assert lines[0] == f"SpecSeal: {len(named)} gates failed and were skipped", lines
    assert gates_said(lines) == named, lines
    assert lines[-1] == CLOSING


def test_a_gate_that_fails_to_load_names_every_group_that_loads_it(repo, tmp_path):
    """Round 1's 🟡 1. A load failure belongs to the file, so it fails in
    every group that loads it, and the record is written once, by the first.
    `worktree-guard.py` sits in `pre-bash` and `pre-agent`, and the
    `pre-agent` half is the `isolation: "worktree"` spawn going unguarded:
    one `pre-bash` failure must not read as a Bash-only gap. A group where
    the gate stands alone, `post-agent` for `worktree_consent.py`, is named
    among the failures and not among the groups whose other gates decided.

    Changed by #689: the guard and the consent writer load `cmdline_base.py`,
    so that module is broken beside `cmdline.py`, which the commit gate
    loads."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"cmdline.py": BROKEN, "cmdline_base.py": BROKEN})
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

    # A failure while running depends on the payload, so the same two-group
    # gate failing in `main()` names only the group it was seen in.
    directory = repo / ".git" / RECORDS / "s-y"
    directory.mkdir(parents=True)
    (directory / "worktree-guard.py.pending").write_text(
        json.dumps({"group": "pre-agent", "phase": "run", "error": "E"}),
        encoding="utf-8",
    )
    assert said(stop(hooks, repo, "s-y"))[1] == (
        "worktree-guard.py failed while running in pre-agent (E); calls went "
        "ahead without it, and the other gates in pre-agent still decided."
    )


def test_a_broken_opt_in_module_is_said_rather_than_read_as_not_opted_in(
    repo, tmp_path
):
    """S6b. `optin.py` is what the report asks whether to speak, and it is
    the broken module: "cannot tell" writes the record. `sealer-stamp.py`
    fails in the `stop` group itself and is said in the same invocation."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, {"optin.py": BROKEN})
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    # One file time for all of them, as a coarse file system gives: the order
    # said is `pre-bash`'s own order, which is not name order here. The git
    # hook installer imports `optin.py` too, and it runs first (#692).
    for path in (repo / ".git" / RECORDS / "s-x").iterdir():
        os.utime(path, ns=(10**18, 10**18))
    lines = said(stop(hooks, repo, "s-x"))
    assert gates_said(lines) == [
        "hook-install.py",
        "commit-review-gate.py",
        "worktree-guard.py",
        "mode-gate.py",
        "sealer-stamp.py",
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
    """One line per record, in the order the gates failed, so a name that
    sorts first is not said first. The order is the `at` pair each record
    carries — the writer's clock and its place in that call's failures — and
    not the file's time, which Windows CI gave two records alike (NTFS keeps
    100 ns, and a file time can be set at a coarser tick). A record with no
    `at`, from another plugin version, falls back to its file time, set here
    whole seconds apart so every file system keeps them distinct."""
    opted_in(repo)
    directory = repo / ".git" / RECORDS / "s-x"
    directory.mkdir(parents=True)
    carried = (
        ("worktree-guard.py", [10**18, 0]),
        ("commit-review-gate.py", [10**18, 1]),
        ("mode-gate.py", [10**18 + 5, 0]),
    )
    for gate, at in carried:
        path = directory / (gate + ".pending")
        path.write_text(json.dumps({"group": "pre-bash", "at": at}), encoding="utf-8")
        os.utime(path, ns=(10**18, 10**18))
    # An `at` that is not two integers is read as absent, not compared.
    for gate, body, seconds in (
        ("version-check.py", {"group": "session-start", "at": ["late", 1]}, 1),
        ("session-lease.py", {"group": "post-bash"}, 2),
    ):
        old = directory / (gate + ".pending")
        old.write_text(json.dumps(body), encoding="utf-8")
        os.utime(old, ns=(10**18 + seconds * 10**9, 10**18 + seconds * 10**9))
    lines = said(stop(hooks_copy(tmp_path, {}), repo, "s-x"))
    assert gates_said(lines) == [
        "worktree-guard.py",
        "commit-review-gate.py",
        "mode-gate.py",
        "version-check.py",
        "session-lease.py",
    ], lines


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
    # None of these carries an `at`, so their file times order them: whole
    # seconds apart, which every file system keeps distinct. 1 ns apart was
    # below NTFS's 100 ns, and Windows CI said them in name order.
    for n, (gate, body) in enumerate(planted.items()):
        path = directory / (gate + ".pending")
        path.write_text(body, encoding="utf-8")
        os.utime(path, ns=(10**18 + n * 10**9, 10**18 + n * 10**9))
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
    # The cap is in UTF-16 units, the unit the harness counts the `Stop`
    # message in (`seal_stamp.MESSAGE_RESERVE`): a character outside the BMP
    # is two, and one that would pass the cap is left out whole.
    astral = "\U0001d54f"
    assert d.first_line(RuntimeError(astral * 500)) == astral * 100
    assert d.first_line(RuntimeError("y" + astral * 500)) == "y" + astral * 99
    # The last character inside the BMP is one unit.
    last = chr(0xFFFF)
    assert d.first_line(RuntimeError(last * 500)) == last * d.MESSAGE_CAP


# --- #722: a class name from outside the plugin is capped too -----------------

ASTRAL = "\U0001d54f"


def units(text):
    """`text`'s length in UTF-16 units, the length the harness counts."""
    return len(text.encode("utf-16-le", "surrogatepass")) // 2


def test_a_foreign_class_name_is_capped_where_it_is_written(repo):
    """S14 (#722). `record` wrote `type(exc).__name__` whole, and a class
    from outside the plugin names itself whatever it likes. A 120-character
    name and a name of 60 characters outside the BMP (120 units) are each
    written at `NAME_CAP` units, and an astral character that would cross
    the cap is left out whole rather than split into half a pair. Seen red
    against the `record` that wrote the name uncapped."""
    opted_in(repo)
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_the_name_cap")
    assert d.NAME_CAP == 40
    wide = type("N" * 120, (Exception,), {})
    astral = type("y" + ASTRAL * 60, (Exception,), {})
    d.record(
        "pre-bash",
        [
            ("mode-gate.py", "run", wide("x")),
            ("worktree-guard.py", "load", astral("z")),
        ],
        bash(repo, "s-x"),
    )
    directory = repo / ".git" / RECORDS / "s-x"
    written = {
        name: json.loads((directory / name).read_text(encoding="utf-8"))["error"]
        for name in ("mode-gate.py.pending", "worktree-guard.py.pending")
    }
    assert written == {
        "mode-gate.py.pending": "N" * 40,
        "worktree-guard.py.pending": "y" + ASTRAL * 19,
    }, written
    assert all(units(name) <= d.NAME_CAP for name in written.values())
    body = json.loads((directory / "mode-gate.py.pending").read_text(encoding="utf-8"))
    line = d.describe("mode-gate.py", body)
    assert f"({'N' * 40}: x)" in line, line


def test_a_record_an_older_plugin_wrote_is_capped_when_it_is_read():
    """S15 (#722). `read_record` says an older or newer plugin may have
    written the record, so `describe` cannot trust the writer's caps: a
    300-unit `error`, a 400-unit `message` and a 300-unit `group` are each
    cut to their cap as the line is built. Seen red against the `describe`
    that interpolated the fields whole."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_the_read_cap")
    line = d.describe(
        "mode-gate.py",
        {"group": "g" * 300, "phase": "run", "error": "E" * 300, "message": "m" * 400},
    )
    assert f" in {'g' * d.NAME_CAP} (" in line, line
    assert f"({'E' * d.NAME_CAP}: {'m' * d.MESSAGE_CAP})" in line, line
    astral = d.describe(
        "mode-gate.py",
        {"phase": "run", "error": "y" + ASTRAL * 300, "message": ASTRAL * 400},
    )
    assert f"(y{ASTRAL * 19}: {ASTRAL * 100})" in astral, astral


def longest_report(d, count):
    """The longest report `count` failed gates can put before a stamp, in
    UTF-16 units, the blank line `report` adds included: every gate in every
    group it is in, both phases, with the name and the message at their caps.
    Each gate is said once per session, so `count` distinct gates."""
    fields = {"error": "E" * d.NAME_CAP, "message": "m" * d.MESSAGE_CAP}
    longest = {}
    for group, gates in d.GROUPS.items():
        for gate in gates:
            for phase in ("load", "run"):
                line = d.describe(gate, {"group": group, "phase": phase, **fields})
                longest[gate] = max(longest.get(gate, ""), line, key=units)
    chosen = sorted(longest.values(), key=units, reverse=True)[:count]
    one = count == 1
    label = d.LABEL.format(
        count=f"{count} gate{'' if one else 's'}", verb="was" if one else "were"
    )
    return units("\n".join([label, *chosen, d.CLOSING])) + 2


def test_two_failed_gates_fit_the_reserve_with_every_field_at_its_cap():
    """S14 (#722). With the name capped as well as the message, the longest
    two-gate report fits `seal_stamp.MESSAGE_RESERVE` and a third would not.
    The reserve's comment states the figures this measures, so a cap that
    moves has to move the comment with it."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_the_reserve")
    stamp = load(STAMP, "seal_stamp_for_the_reserve")
    one, two, three = (longest_report(d, n) for n in (1, 2, 3))
    assert two <= stamp.MESSAGE_RESERVE < three, (one, two, three)
    with open(STAMP, encoding="utf-8") as handle:
        source = handle.read()
    comment = source.split("\nMESSAGE_RESERVE = ", 1)[0].rsplit("\n\n", 1)[1]
    for figure in (one, two, three):
        assert f"{figure:,}" in comment, (figure, comment)


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


# --- #661: a gate's JSON the dispatcher cannot read ends nothing --------------

# Every shape found to raise in `classify` or `merge` at `551c7967`, after the
# gates had run and outside `run_gate`'s isolation, so the group exited 1.
UNREADABLE = (
    "null",
    "0",
    "3",
    "[1]",
    "[]",
    '"words"',
    "true",
    '{"hookSpecificOutput": 3}',
    '{"hookSpecificOutput": {"permissionDecision": 5}}',
    '{"hookSpecificOutput": {"permissionDecision": "ask", '
    '"permissionDecisionReason": 7}}',
    '{"systemMessage": 3}',
)


def printing(text):
    """A gate whose `main()` prints `text` and nothing else."""
    return f"def main():\n    print({text!r})\n"


def test_json_a_gate_prints_that_is_not_a_hooks_output_ends_nothing(repo, tmp_path):
    """#661. A gate printing JSON the merge cannot read — not an object, or
    an object whose decision or reason is not text, or with no decision a
    message that is not text — used to end its whole group with exit 1,
    taking a neighbour's `deny` or `systemMessage` with it. `null` and `0` survive beside a deny and end a group beside a
    message, so each shape is planted beside both. The output is dropped, the
    group decides as it would without it, and the gate is said at turn end."""
    opted_in(repo)
    for n, shape in enumerate(UNREADABLE):
        hooks = hooks_copy(
            tmp_path / f"h{n}",
            {
                "mode-gate.py": printing(shape),
                "version-check.py": printing('{"systemMessage": "m"}'),
                "root-migrate.py": printing(shape),
                "ledger-migrate.py": printing(""),
            },
        )
        session = f"s-{n}"
        out = dispatch(hooks, "pre-bash", bash(repo, session))
        assert decision_of(out) == "deny", (shape, out)
        start = {"hook_event_name": "SessionStart", "session_id": session}
        start["cwd"] = str(repo)
        assert json.loads(dispatch(hooks, "session-start", start)) == {
            "systemMessage": "m"
        }, shape
        lines = said(stop(hooks, repo, session))
        assert lines[1].startswith(
            "mode-gate.py failed while running in pre-bash (ValueError: printed "
            "JSON the dispatcher cannot read: "
        ), (shape, lines)
        assert gates_said(lines) == ["mode-gate.py", "root-migrate.py"], lines


def test_json_the_merge_can_read_is_merged_as_before():
    """The shapes that were read before still are: an object with no
    decision, one whose optional fields are null, and a decision."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_readable")
    assert d.classify('{"a": 1}') == ("json", {"a": 1})
    nulls = {"hookSpecificOutput": None, "systemMessage": None}
    assert d.classify(json.dumps(nulls)) == ("json", nulls)
    ask = {"hookSpecificOutput": {"permissionDecision": "ask"}}
    assert d.classify(json.dumps(ask)) == ("decision", ask)
    assert d.classify("plain\n") == ("text", "plain")


def test_a_deny_beside_a_message_that_is_not_text_still_denies():
    """Round 2's 🟡 3. #661 must not drop output the merge read before. Its
    decision path reads the decision and its reason and never the
    `systemMessage`, and a falsy `hookSpecificOutput` was read as absent.
    Seen red at `02e47435`, where the merge printed nothing for either."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_a_deny")
    deny = {"hookSpecificOutput": {"permissionDecision": "deny"}, "systemMessage": 3}
    assert d.classify(json.dumps(deny)) == ("decision", deny)
    assert decision_of(d.merge([json.dumps(deny)], "PreToolUse")) == "deny"
    for falsy in (False, 0, "", []):
        body = {"hookSpecificOutput": falsy, "systemMessage": "m"}
        assert d.classify(json.dumps(body)) == ("json", body), falsy
        assert json.loads(d.merge([json.dumps(body)], "Stop")) == body, falsy
    reason = {
        "hookSpecificOutput": {
            "permissionDecision": "ask",
            "permissionDecisionReason": 7,
        }
    }
    assert d.classify(json.dumps(reason))[0] == "unreadable"
