#!/usr/bin/env bash
# PostToolUse(Write|Edit): auto-format Python files with ruff.
# Reads the hook JSON on stdin; falls back to $1 for manual invocation.

FILE="${1:-}"
if [ -z "$FILE" ] && [ ! -t 0 ]; then
    FILE=$(python3 -c 'import json,sys
try:
    print((json.load(sys.stdin).get("tool_input") or {}).get("file_path", ""))
except Exception:
    pass' 2>/dev/null)
fi

# Only run on Python files
[[ "$FILE" != *.py ]] && exit 0

# Priority: uv run (project venv) → uvx (temp) → ruff (global fallback)
run_ruff() {
    if command -v uv &> /dev/null && uv run ruff --version &> /dev/null; then
        uv run ruff "$@"
    elif command -v uvx &> /dev/null; then
        uvx ruff "$@"
    elif command -v ruff &> /dev/null; then
        ruff "$@"
    else
        return 1
    fi
}

run_ruff check --fix --quiet "$FILE" 2>/dev/null
run_ruff format --quiet "$FILE" 2>/dev/null
exit 0
