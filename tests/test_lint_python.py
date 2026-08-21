"""lint-python: the one hook that rewrites the user's source and can hit the network."""
import json
import subprocess

from conftest import load_hook_module

lp = load_hook_module("lint-python.py", "lint_py")


def run_hook_stdin(payload, tmp_path):
    import os
    script = os.path.join(os.path.dirname(__file__), "..", "hooks", "lint-python.py")
    return subprocess.run(["python3", script], input=payload, cwd=str(tmp_path),
                          capture_output=True, text=True)


def test_non_python_file_never_reaches_the_formatter(monkeypatch, tmp_path):
    called = []
    monkeypatch.setattr(lp, "resolve_runner", lambda: called.append("resolved") or ["ruff"])
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(tmp_path / "notes.md")])
    lp.main()
    assert called == [], "a non-.py path must not even look for a runner"


def test_python_file_runs_check_fix_then_format(monkeypatch, tmp_path):
    f = tmp_path / "m.py"
    f.write_text("x = 1\n")
    invocations = []
    monkeypatch.setattr(lp, "resolve_runner", lambda: ["ruff"])
    monkeypatch.setattr(lp.subprocess, "run",
                        lambda cmd, **k: invocations.append(cmd) or None)
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(f)])
    lp.main()
    assert [c[1] for c in invocations] == ["check", "format"], invocations
    assert "--fix" in invocations[0] and invocations[0][-1] == str(f)


def test_missing_runner_is_silent(monkeypatch, tmp_path):
    f = tmp_path / "m.py"
    f.write_text("x = 1\n")
    monkeypatch.setattr(lp, "resolve_runner", lambda: None)
    monkeypatch.setattr(lp.subprocess, "run",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("must not run")))
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(f)])
    lp.main()  # no exception == pass


def test_a_failing_formatter_never_blocks_the_edit(monkeypatch, tmp_path):
    f = tmp_path / "m.py"
    f.write_text("x = 1\n")
    monkeypatch.setattr(lp, "resolve_runner", lambda: ["ruff"])
    monkeypatch.setattr(lp.subprocess, "run",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("boom")))
    monkeypatch.setattr(lp.sys, "argv", ["lint-python.py", str(f)])
    lp.main()  # swallowed — a formatter crash must not wedge the session


def test_malformed_payload_exits_zero(tmp_path):
    for payload in ("not json at all", "{}", json.dumps({"tool_input": {}})):
        r = run_hook_stdin(payload, tmp_path)
        assert r.returncode == 0, (payload, r.stderr)
