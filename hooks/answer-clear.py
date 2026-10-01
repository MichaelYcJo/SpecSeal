#!/usr/bin/env python3
"""PostToolUse(Bash): the call that carried a consent token is over, so the
token is too (#692, P3, W6). `hooks/answers.py` holds the reasoning."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answers
import console


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        return
    answers.clear(payload.get("session_id") or "")


if __name__ == "__main__":
    console.to_utf8()
    main()
