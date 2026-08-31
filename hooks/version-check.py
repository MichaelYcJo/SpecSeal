#!/usr/bin/env python3
"""SessionStart notice: a newer release exists.

Plugin updates are keyed to the version in plugin.json, not to commits, and
nothing checks for them — starting a session does not even refresh the local
marketplace clone (measured). So a release reaches a user only if that user
remembers, unprompted, to run two commands. This hook removes the
remembering; it does not install anything.

Installing is deliberately out of scope: telling someone a release exists and
installing software on their machine are different acts, and only the first is
a notice's job. `/specseal:update` is where the second one lives, because a
user asked for it there.

(The old note here said a self-updating session would run two versions at
once. That is not what happens — the previous version stays in the plugin
cache and `$CLAUDE_PLUGIN_ROOT` keeps resolving to it, so a session simply
keeps what it loaded until a restart.)

This is the plugin's second network touch, after lint-python's `uvx ruff`
fetch, and `CONTRIBUTING.md` names it as an allowed exception. What leaves the
machine is one `git ls-remote --tags` to the plugin's own repository: no
repository contents, no paths, no prompts. Three limits keep it honest:

  - only in repos that opted in with `.specseal/`, like the other gates
  - once a day, tracked in ~/.claude/specseal/version-check — a lookup that
    fails hands the day back and is retried about twenty minutes later
  - silent on every failure — offline, slow, unparseable, anything

The running version comes from $CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json,
which is the version actually loaded. The CLI's installed_plugins.json answers
a different question (what is on disk) and is not read.

Failure direction: this hook stays quiet. A missed notice costs a user one
release of lag, which is where they already are; a wrong notice at every
session start is the kind of noise people disable a plugin over. Tag formats
the parser does not recognise are skipped, so a future rename of the tag
scheme degrades to silence rather than to a wrong warning.
"""

import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import optin

STATE_DIR = os.path.join(os.path.expanduser("~"), ".claude", "specseal")
MARKER = os.path.join(STATE_DIR, "version-check")
INTERVAL = 24 * 60 * 60
RETRY = 20 * 60
TAG = re.compile(r"refs/tags/v(\d+)\.(\d+)\.(\d+)$")


def parse(text):
    """(major, minor, patch) or None. Anything unrecognised is not a version."""
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", (text or "").strip())
    return tuple(int(g) for g in m.groups()) if m else None


def running():
    """The version and repository of the plugin actually loaded, or (None, None)."""
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not root:
        return None, None
    try:
        with open(os.path.join(root, ".claude-plugin", "plugin.json")) as f:
            d = json.load(f)
    except (OSError, ValueError):
        return None, None
    return parse(d.get("version")), d.get("repository")


def due():
    """True if a day has passed; stamps the marker so the next session skips.

    Stamped before the lookup, not after, so a hanging network call cannot
    make every session retry it. A lookup that then fails hands the day back
    through `retry_soon`, so the protection costs minutes rather than a day."""
    try:
        if time.time() - os.path.getmtime(MARKER) < INTERVAL:
            return False
    except OSError:
        pass
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(MARKER, "w") as f:
            f.write(str(int(time.time())))
    except OSError:
        return False
    return True


def retry_soon():
    """Back-date the throttle so a failed lookup costs minutes, not the day.

    Stamping before the lookup stops a hanging call from being retried every
    session, but on its own it also spends the whole day on a laptop that was
    offline for the ten seconds around session start — and the notice this
    hook exists to deliver is the thing that goes missing. Never raises: a
    throttle that cannot be moved is the throttle we already had."""
    try:
        stale = time.time() - INTERVAL + RETRY
        os.utime(MARKER, (stale, stale))
    except OSError:
        pass


def latest(repo):
    """Newest vX.Y.Z tag on the remote, () when it has none, None when the
    lookup itself failed. Never raises.

    The caller needs the last two apart. A remote with no tags is an answer
    and holds the throttle for the day; a lookup that never completed is a
    question that was never asked, and asking again shortly is the point."""
    if not repo:
        return None
    try:
        proc = subprocess.run(
            ["git", "ls-remote", "--tags", repo],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    found = [
        tuple(int(g) for g in m.groups())
        for m in (TAG.search(line) for line in proc.stdout.splitlines())
        if m
    ]
    return max(found) if found else ()


def notice(have, want):
    h, w = ".".join(map(str, have)), ".".join(map(str, want))
    return (
        f"SpecSeal {w} is out; this session is running {h}.\n"
        "Run /specseal:update — it takes the release and tells you what is in "
        "it, which the version number does not.\n"
        "By hand: `claude plugin marketplace update specseal` then "
        "`claude plugin update specseal@specseal`, in that order. The second "
        "alone reports 'already at the latest version' against stale local "
        "data.\nEither way, restart to load it."
    )


def main():
    try:
        event = json.load(sys.stdin) or {}
        cwd = event.get("cwd")
    except (ValueError, AttributeError):
        return
    if not cwd or not os.path.isdir(cwd) or not optin.opted_in(cwd):
        return

    have, repo = running()
    if not have or not due():
        return

    want = latest(repo)
    if want is None:
        retry_soon()
        return
    if want and want > have:
        print(json.dumps({"systemMessage": notice(have, want)}))


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
