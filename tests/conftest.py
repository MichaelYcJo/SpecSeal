import importlib.util
import json
import os
import subprocess
import sys

import pytest

HOOKS = os.path.join(os.path.dirname(__file__), "..", "hooks")

# Default-locale determinism: the suite owns its locale. A plain setdefault
# is not enough — the author's machine exports SPECSEAL_LANG=ko session-wide
# (measured), which would flip every default-language assertion. Tests that
# need Korean monkeypatch the env and fresh-load the module.
os.environ["SPECSEAL_LANG"] = "en"


def load_hook_module(filename, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HOOKS, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_hook(filename, payload, env=None):
    """Feed a hook the stdin JSON the harness would send; return its stdout."""
    r = subprocess.run(
        [sys.executable, os.path.join(HOOKS, filename)],
        input=json.dumps(payload), capture_output=True, text=True, timeout=30,
        env={**os.environ, **(env or {})},
    )
    return r.stdout


def decision_of(stdout):
    """'silent' when a hook allowed by staying quiet, else its decision."""
    if not stdout.strip():
        return "silent"
    return json.loads(stdout)["hookSpecificOutput"]["permissionDecision"]


@pytest.fixture
def repo(tmp_path):
    """A git repo with one committed file and a feature branch to switch to."""
    d = tmp_path / "repo"
    d.mkdir()
    git = lambda *a: subprocess.run(["git", "-C", str(d), *a], check=True,
                                    capture_output=True, text=True)
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (d / "f.txt").write_text("one\ntwo\nthree\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    git("branch", "feature/x")
    return d
