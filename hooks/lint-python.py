#!/usr/bin/env python3
"""PostToolUse(Write|Edit): auto-format Python files with ruff.

Reads the hook JSON on stdin; falls back to argv[1] for manual invocation.
Python (not shell) so the same file runs on Windows, where hook commands
are invoked without a POSIX shell. Formatting is best-effort: no ruff on
the machine, or ruff failing, must never block the edit.

Runner priority: `uv run ruff` (project venv) → `uvx ruff` (ephemeral) →
`ruff` (global fallback).
"""

import json
import shutil
import subprocess
import sys


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

    runner = resolve_runner()
    if not runner:
        return
    for args in (["check", "--fix", "--quiet"], ["format", "--quiet"]):
        try:
            subprocess.run([*runner, *args, file], capture_output=True, timeout=120)
        except Exception:
            pass


if __name__ == "__main__":
    main()
