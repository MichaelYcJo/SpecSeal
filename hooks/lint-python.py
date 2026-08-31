#!/usr/bin/env python3
"""PostToolUse(Write|Edit): run ruff on Python files in projects that use ruff.

Only there. This hook rewrites the file you just saved, and `ruff check --fix`
changes code rather than layout — it drops unused imports, rewrites
comprehensions, and applies whatever rules are in force. Installed globally,
the old unconditional version did that to every repository on the machine,
including ones that use black, ones with their own ruff settings it would have
ignored, and ones that had chosen no formatter at all.

So the repository decides, by the file it already keeps: `ruff.toml`,
`.ruff.toml`, or a `[tool.ruff]` table in `pyproject.toml`, searched from the
edited file up to the repository root. Configuring ruff is a project saying it
wants ruff; nothing else is. `SPECSEAL_LINT=off` turns the hook off even there.

Failure direction: this stays out. A wrong skip means the formatter runs later
by hand or in CI. A wrong run rewrites someone's source against conventions
they chose, silently — PostToolUse output is not where people look.

Reads the hook JSON on stdin; falls back to argv[1] for manual invocation.
Python (not shell) so the same file runs on Windows, where hook commands
are invoked without a POSIX shell. Formatting is best-effort: no ruff on
the machine, or ruff failing, must never block the edit.

Runner priority: `uv run ruff` (project venv) → `uvx ruff` (ephemeral) →
`ruff` (global fallback).
"""

import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console

CONFIG_FILES = ("ruff.toml", ".ruff.toml")


def uses_ruff(path):
    """True when a project that owns `path` has configured ruff.

    Walks from the file's directory to the filesystem root, stopping at a
    repository boundary so a parent checkout's settings cannot speak for a
    nested one. `pyproject.toml` counts only with a `[tool.ruff]` table —
    the file itself says nothing about formatting.
    """
    d = os.path.dirname(os.path.abspath(path))
    while True:
        for name in CONFIG_FILES:
            if os.path.isfile(os.path.join(d, name)):
                return True
        pyproject = os.path.join(d, "pyproject.toml")
        if os.path.isfile(pyproject):
            try:
                with open(pyproject, encoding="utf-8", errors="replace") as f:
                    if "[tool.ruff" in f.read():
                        return True
            except OSError:
                pass
        if os.path.exists(os.path.join(d, ".git")):
            return False
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def resolve_runner():
    if shutil.which("uv"):
        probe = subprocess.run(
            ["uv", "run", "ruff", "--version"], capture_output=True, timeout=30
        )
        if probe.returncode == 0:
            return ["uv", "run", "ruff"]
    if shutil.which("uvx"):
        return ["uvx", "ruff"]
    if shutil.which("ruff"):
        return ["ruff"]
    return None


def main():
    file = sys.argv[1] if len(sys.argv) > 1 else ""
    if not file and not sys.stdin.isatty():
        try:
            file = (json.load(sys.stdin).get("tool_input") or {}).get("file_path", "")
        except Exception:
            file = ""
    if not file.endswith(".py"):
        return
    if os.environ.get("SPECSEAL_LINT", "").lower() == "off":
        return
    if not uses_ruff(file):
        return

    runner = resolve_runner()
    if not runner:
        return
    for args in (["check", "--fix", "--quiet"], ["format", "--quiet"]):
        try:
            subprocess.run([*runner, *args, file], capture_output=True, timeout=120)
        except Exception:
            pass


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
