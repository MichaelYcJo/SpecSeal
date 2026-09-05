#!/usr/bin/env python3
"""One interpreter per hook event instead of one per gate.

Every gate here decides in well under a millisecond of its own work; the cost
is the Python that has to start before it can decide. Measured on the author's
machine, a bare interpreter is ~92ms and each gate ~110-180ms — so four gates
firing on one Bash call spent most of half a second starting up to conclude
that three of them had nothing to do.

This runs a group of gates in ONE process, feeding each the same payload and
merging what they print. The gate modules are imported and their `main()`
called, unchanged — they stay runnable on their own (that is how the tests
drive them, and how anyone debugging one reaches it).

Usage: dispatch.py <group>, payload on stdin.

Merging: a PreToolUse group can produce more than one decision, and the
strictest wins — deny over ask over silence — with every reason kept, because
a gate that was overruled still has something the user needs to read.

Failure is isolated and open: a gate that raises is skipped, and the others
still decide. A crashing gate must not block a tool call, and must not take
its neighbours down with it.
"""

import importlib.util
import io
import json
import os
import sys
from contextlib import redirect_stderr, redirect_stdout

HOOKS = os.path.dirname(os.path.abspath(__file__))

GROUPS = {
    "pre-bash": ("commit-review-gate.py", "worktree-guard.py"),
    "pre-agent": ("worktree-guard.py", "implementer-mark.py"),
    "pre-skill": ("review-skill-gate.py",),
    "post-bash": (
        "review-history-guard.py",
        "implementer-notice.py",
        "session-lease.py",
        "evidence-advisor.py",
    ),
    "post-edit": ("lint-python.py", "session-lease.py"),
    # The root move precedes the ledger-format migration, because the second
    # reads the ledgers at the addresses the first creates.
    "session-start": ("version-check.py", "root-migrate.py", "ledger-migrate.py"),
}

RANK = {"deny": 3, "ask": 2, "allow": 1}


def run_gate(filename, payload):
    """A gate's stdout, or "" when it printed nothing or failed.

    stdin, stdout and argv are swapped for the call: the gates read the
    payload from stdin, and lint-python reads a path from argv[1] — left
    alone it would read the group name as a filename.
    """
    path = os.path.join(HOOKS, filename)
    out = io.StringIO()
    argv, stdin = sys.argv, sys.stdin
    try:
        spec = importlib.util.spec_from_file_location(
            f"specseal_gate_{filename.replace('-', '_')[:-3]}", path
        )
        module = importlib.util.module_from_spec(spec)
        sys.argv = [path]
        sys.stdin = io.StringIO(payload)
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            spec.loader.exec_module(module)
            # Import must not consume stdin; main() gets its own copy.
            sys.stdin = io.StringIO(payload)
            try:
                module.main()
            except SystemExit:
                pass
    except Exception:
        # RIDER: this catch is deliberate -- a crashing gate must not block a
        # tool call or take its neighbours down. What it costs is that an
        # IMPORT failure reads exactly like an allow. Measured with
        # `hooks/cmdline.py` deliberately broken: `pre-bash` and `pre-agent`
        # both exit 0 with no output, and the worktree guard is the only gate
        # in `pre-agent` that decides anything, so the Agent `isolation:
        # "worktree"` path goes undefended with nobody told. The mark gate
        # beside it does not import `cmdline.py` and prints nothing either
        # way, so it neither widens nor narrows that silence (measured: with
        # `cmdline.py` broken the group prints nothing and the mark is still
        # written). Moving the shared reading into `cmdline.py` removed the
        # likeliest trigger, not the silence. Whatever replaces this has to
        # keep the isolation property `tests/test_dispatch.py` and
        # `tests/test_the_implementer_is_recorded.py` assert.
        # Verified 2026-09-02 at 5a831e8.
        return ""
    finally:
        sys.argv, sys.stdin = argv, stdin
    return out.getvalue()


def classify(text):
    """('decision'|'json'|'text', value) for one gate's output."""
    stripped = text.strip()
    if not stripped:
        return None, None
    try:
        parsed = json.loads(stripped)
    except ValueError:
        return "text", text.rstrip("\n")
    hook_out = (parsed or {}).get("hookSpecificOutput") or {}
    if isinstance(parsed, dict) and hook_out.get("permissionDecision"):
        return "decision", parsed
    return "json", parsed


def merge(outputs, event_name):
    """One stdout for the whole group."""
    decisions, jsons, texts = [], [], []
    for text in outputs:
        kind, value = classify(text)
        if kind == "decision":
            decisions.append(value)
        elif kind == "json":
            jsons.append(value)
        elif kind == "text":
            texts.append(value)

    if decisions:
        winner = max(
            decisions,
            key=lambda d: RANK.get(
                d["hookSpecificOutput"]["permissionDecision"].lower(), 0
            ),
        )
        reasons = [
            d["hookSpecificOutput"].get("permissionDecisionReason", "")
            for d in decisions
        ]
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": event_name,
                    "permissionDecision": winner["hookSpecificOutput"][
                        "permissionDecision"
                    ],
                    "permissionDecisionReason": "\n\n".join(
                        r for r in reasons + texts if r
                    ),
                }
            }
        )
    if jsons:
        merged = dict(jsons[0])
        extra = [j.get("systemMessage") for j in jsons[1:] if j.get("systemMessage")]
        if extra and merged.get("systemMessage"):
            merged["systemMessage"] = "\n\n".join([merged["systemMessage"], *extra])
        return json.dumps(merged)
    return "\n".join(texts)


def main():
    group = sys.argv[1] if len(sys.argv) > 1 else ""
    gates = GROUPS.get(group)
    if not gates:
        return
    payload = sys.stdin.read()
    event_name = "PreToolUse" if group.startswith("pre-") else "PostToolUse"
    merged = merge([run_gate(g, payload) for g in gates], event_name)
    if merged.strip():
        print(merged)


if __name__ == "__main__":
    # THE entry point, and the only one that matters in production: `hooks.json`
    # spawns this file and nothing else, and it loads each gate with
    # `exec_module` and calls `main()` in-process. Seven of the eleven
    # `__main__` blocks in this tree are therefore unreachable when Claude Code
    # runs them -- so this block is where the streams get fixed, not each
    # gate's.
    #
    # A console whose encoding is not UTF-8 cannot encode the em dash, arrow
    # and middle dot these gates print, and the UnicodeEncodeError leaves
    # stdout EMPTY -- which is exactly how a hook says "nothing to see here".
    # The command the gate existed to stop goes through, and nothing reports
    # that a gate crashed. Korean, Japanese and Chinese Windows default to
    # cp949/cp932/cp936 and hit this.
    #
    # `stdin` is in the loop because the payload is where the non-ASCII
    # actually is: it carries the user's own command text, and one Korean path
    # or an em dash in a commit subject is enough. This file reads it, so a
    # raise there takes every gate in the group down at once -- and `hooks.json`
    # runs `python3 … || py -3 …`, so the retry meets an already-consumed stdin
    # and passes silently a second time.
    #
    # Unconditional, because branching on `os.name` would leave the Windows
    # path proven by nothing while Linux CI runs the other one; where a stream
    # is already UTF-8 this is a no-op. `errors` is named because `reconfigure`
    # resets it to `strict` whenever `encoding` is given without it, and stderr
    # ships as `backslashreplace` -- a path holding a lone surrogate must
    # degrade, not take the gate down on its way to reporting something. The
    # `hasattr` guard covers a stream that is None, which is what a hook
    # invoked with a closed stdin would hand us.
    #
    # The names are held rather than the streams, because `hooks/console.py`
    # -- the module this loop duplicates -- says a stream can be ABSENT and
    # reaches for it with `getattr(sys, name, None)`. Building the tuple from
    # `sys.stdin` directly raises `AttributeError` in that state, at module
    # level, before `main()`, with stdout empty. That is the silent allow this
    # block exists to close, arriving through the block itself.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    main()
