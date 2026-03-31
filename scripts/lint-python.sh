#!/usr/bin/env bash
# Auto-format Python files after Write/Edit via hook
# Usage: lint-python.sh <filepath>

FILE="$1"

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
