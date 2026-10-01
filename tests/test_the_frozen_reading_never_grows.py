"""The frozen reading never grows, and the switch arm keeps it (#692, phase 5:
S10 and S11 under the owner's answer of 2026-10-01).

No git refuses a branch switch before its tree has moved (phase 1's M1, on
2.34.1, 2.39.5, 2.43.0 and 2.50.1), so the owner kept the worktree guard's
switch arm on `hooks/cmdline_base.py` -- `86256492`'s reader -- on every git,
permanently. What keeps that from becoming milestone 49 again is that the file
cannot gain a rule: its bytes below the rider are `86256492:hooks/cmdline.py`,
and a change has to delete a case here first.
"""

import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import load_hook_module

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / "hooks" / "cmdline_base.py"
BASE = "86256492"
START = b'"""Reading a shell command line'

# sha256 of `86256492:hooks/cmdline.py` from its docstring on -- the file less
# its shebang line, which the rider sits under. Computed 2026-10-01 from
# `git show 86256492:hooks/cmdline.py`; the case below also compares against
# git itself wherever the commit is reachable (CI checks out full history).
SHA256 = "ad528c48388d3a5a84f22d073c29e2d90c7575d15a8a50afdc0cda8e4c5bd6e2"


def below_the_rider(data):
    return data[data.index(START) :]


def test_the_bytes_below_the_rider_are_86256492s():
    mine = below_the_rider(FROZEN.read_bytes())
    assert hashlib.sha256(mine).hexdigest() == SHA256, (
        "hooks/cmdline_base.py changed below its rider. It is pinned to "
        f"{BASE}:hooks/cmdline.py: a rule added to the frozen reading is the "
        "stopped class (#692), and this case has to go before it can"
    )
    shown = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{BASE}:hooks/cmdline.py"],
        capture_output=True,
    )
    if shown.returncode != 0:
        pytest.skip(f"{BASE} is not reachable here; the hash above still held")
    assert below_the_rider(shown.stdout) == mine
    assert shown.stdout[: shown.stdout.index(START)] == b"#!/usr/bin/env python3\n"


def test_only_the_two_fallback_arms_read_it():
    """The guard (its switch arm on every git, its creation arm in a foreign
    clone) and the consent writer (in a foreign clone). Nothing else under
    `hooks/` may reach for it."""
    readers = sorted(
        str(p.relative_to(ROOT))
        for p in (ROOT / "hooks").rglob("*.py")
        if p != FROZEN
        and re.search(
            r"^\s*(import cmdline_base|from cmdline_base import)",
            p.read_text(encoding="utf-8"),
            re.M,
        )
    )
    assert readers == ["hooks/worktree-guard.py", "hooks/worktree_consent.py"]


# --- S10: the switch is judged where git decides everything else -------------

guard = load_hook_module("worktree-guard.py", "guard_beside_the_git_hooks")
install_mod = load_hook_module("hook-install.py", "hook_install_beside_the_switch")


def test_s10_a_switch_in_a_git_decided_clone_is_still_judged_by_the_guard(
    tmp_path, monkeypatch, capsys, git_hooks_installed
):
    """The stubs judge commits and creations; a switch has no hook that can
    refuse it before the tree moves, so the guard's reading stands there."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        HOME=str(tmp_path / "home"),
        GIT_CONFIG_NOSYSTEM="1",
        GIT_AUTHOR_NAME="x",
        GIT_AUTHOR_EMAIL="x@example.com",
        GIT_COMMITTER_NAME="x",
        GIT_COMMITTER_EMAIL="x@example.com",
    )
    (tmp_path / "home").mkdir()
    r = tmp_path / "r"
    r.mkdir()

    def g(*args):
        subprocess.run(
            ["git", "-C", str(r), *args], check=True, capture_output=True, env=env
        )

    g("init", "-q")
    g("symbolic-ref", "HEAD", "refs/heads/main")
    (r / "seal").mkdir()
    (r / "seal" / "README.md").write_text("root\n", encoding="utf-8")
    (r / "f.py").write_text("a = 1\n", encoding="utf-8")
    g("add", ".")
    g("commit", "-q", "-m", "init")
    g("branch", "other")
    assert install_mod.install(str(r), "s1")
    sys.path.insert(0, str(ROOT / "hooks"))
    import githooks

    assert githooks.decides(str(r))
    (r / "f.py").write_text("a = 2\n", encoding="utf-8")
    monkeypatch.setattr(guard, "sessions_in_tree", lambda top, own="": ([], [], True))
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "git switch other"},
        "cwd": str(r),
        "session_id": "s1",
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    with pytest.raises(SystemExit):
        guard.main()
    out = json.loads(capsys.readouterr().out)
    assert out["hookSpecificOutput"]["permissionDecision"] == "ask"
    assert (
        "uncommitted tracked changes"
        in out["hookSpecificOutput"]["permissionDecisionReason"]
    )
