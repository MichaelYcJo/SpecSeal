"""lint-python: the one hook that rewrites the user's source and can hit the network."""

import json
import os
import subprocess
import sys

from conftest import load_hook_module

lp = load_hook_module("lint-python.py", "lint_py")


def run_hook_stdin(payload, tmp_path):
    script = os.path.join(os.path.dirname(__file__), "..", "hooks", "lint-python.py")
    return subprocess.run(
        [sys.executable, script],
        input=payload,
        cwd=str(tmp_path),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def test_non_python_file_never_reaches_the_formatter(monkeypatch, tmp_path):
    called = []
    monkeypatch.setattr(
        lp, "resolve_runner", lambda: called.append("resolved") or ["ruff"]
    )
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(tmp_path / "notes.md")])
    lp.main()
    assert called == [], "a non-.py path must not even look for a runner"


def test_python_file_runs_check_fix_then_format(monkeypatch, tmp_path):
    (tmp_path / "ruff.toml").write_text("line-length = 88\n")
    f = tmp_path / "m.py"
    f.write_text("x = 1\n")
    invocations = []
    monkeypatch.setattr(lp, "resolve_runner", lambda: ["ruff"])
    monkeypatch.setattr(
        lp.subprocess, "run", lambda cmd, **k: invocations.append(cmd) or None
    )
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(f)])
    lp.main()
    assert [c[1] for c in invocations] == ["check", "format"], invocations
    assert "--fix" in invocations[0] and invocations[0][-1] == str(f)


def test_missing_runner_is_silent(monkeypatch, tmp_path):
    f = tmp_path / "m.py"
    f.write_text("x = 1\n")
    monkeypatch.setattr(lp, "resolve_runner", lambda: None)
    monkeypatch.setattr(
        lp.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("must not run")),
    )
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(f)])
    lp.main()  # no exception == pass


def test_a_failing_formatter_never_blocks_the_edit(monkeypatch, tmp_path):
    f = tmp_path / "m.py"
    f.write_text("x = 1\n")
    monkeypatch.setattr(lp, "resolve_runner", lambda: ["ruff"])
    monkeypatch.setattr(
        lp.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(OSError("boom"))
    )
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(f)])
    lp.main()  # swallowed — a formatter crash must not wedge the session


def test_malformed_payload_exits_zero(tmp_path):
    for payload in ("not json at all", "{}", json.dumps({"tool_input": {}})):
        r = run_hook_stdin(payload, tmp_path)
        assert r.returncode == 0, (payload, r.stderr)


# --- the project decides -----------------------------------------------------
#
# This hook rewrites the file you just saved, and `ruff check --fix` changes
# code, not layout. Installed globally it used to do that everywhere — to repos
# using black, to repos with their own ruff settings it ignored, to repos that
# had chosen no formatter. Configuring ruff is a project saying it wants ruff.


def _py_in(tmp_path, *, config=None, name="m.py"):
    if config:
        for filename, body in config.items():
            (tmp_path / filename).write_text(body)
    f = tmp_path / name
    f.write_text("import os\nx = 1\n")
    return f


def _ran(monkeypatch, tmp_path, path, env=None):
    calls = []
    monkeypatch.setattr(lp, "resolve_runner", lambda: ["ruff"])
    monkeypatch.setattr(
        lp.subprocess,
        "run",
        lambda *a, **k: calls.append(a[0]) or subprocess.CompletedProcess(a, 0),
    )
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(path)])
    for k, v in (env or {}).items():
        monkeypatch.setenv(k, v)
    lp.main()
    return calls


def test_a_project_with_ruff_toml_is_formatted(monkeypatch, tmp_path):
    f = _py_in(tmp_path, config={"ruff.toml": "line-length = 88\n"})
    assert _ran(monkeypatch, tmp_path, f)


def test_a_dotted_ruff_toml_counts_too(monkeypatch, tmp_path):
    f = _py_in(tmp_path, config={".ruff.toml": "line-length = 88\n"})
    assert _ran(monkeypatch, tmp_path, f)


def test_pyproject_with_a_tool_ruff_table_counts(monkeypatch, tmp_path):
    f = _py_in(tmp_path, config={"pyproject.toml": "[tool.ruff]\nline-length = 88\n"})
    assert _ran(monkeypatch, tmp_path, f)


def test_pyproject_alone_does_not(monkeypatch, tmp_path):
    """A pyproject.toml says nothing about formatting."""
    f = _py_in(tmp_path, config={"pyproject.toml": '[project]\nname = "x"\n'})
    assert _ran(monkeypatch, tmp_path, f) == []


def test_a_project_using_black_is_left_alone(monkeypatch, tmp_path):
    f = _py_in(tmp_path, config={"pyproject.toml": "[tool.black]\nline-length = 100\n"})
    assert _ran(monkeypatch, tmp_path, f) == []


def test_a_project_with_no_formatter_is_left_alone(monkeypatch, tmp_path):
    assert _ran(monkeypatch, tmp_path, _py_in(tmp_path)) == []


def test_config_is_found_from_a_subdirectory(monkeypatch, tmp_path):
    (tmp_path / "ruff.toml").write_text("line-length = 88\n")
    sub = tmp_path / "src" / "pkg"
    sub.mkdir(parents=True)
    f = sub / "m.py"
    f.write_text("x = 1\n")
    assert _ran(monkeypatch, tmp_path, f)


def test_the_search_stops_at_a_repository_boundary(monkeypatch, tmp_path):
    """A parent checkout's settings must not speak for a nested one."""
    (tmp_path / "ruff.toml").write_text("line-length = 88\n")
    nested = tmp_path / "vendor" / "other"
    (nested / ".git").mkdir(parents=True)
    f = nested / "m.py"
    f.write_text("x = 1\n")
    assert _ran(monkeypatch, tmp_path, f) == []


def test_the_off_switch_wins_even_where_ruff_is_configured(monkeypatch, tmp_path):
    f = _py_in(tmp_path, config={"ruff.toml": "line-length = 88\n"})
    assert _ran(monkeypatch, tmp_path, f, env={"SPECSEAL_LINT": "off"}) == []
