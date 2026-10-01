#!/usr/bin/env python3
"""PreToolUse(Bash): hand the old consent tokens a command carries to the git
hooks that will judge it (#692, P3). `hooks/answers.py` holds the reasoning.

It decides nothing and prints nothing: a token is read here and weighed in the
hook, beside the git-native spelling the refusals advise first.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answers
import console
import tokens


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        return
    session = payload.get("session_id") or ""
    command = (payload.get("tool_input") or {}).get("command", "") or ""
    answers.write(session, tokens.given(command))


if __name__ == "__main__":
    console.to_utf8()
    main()
