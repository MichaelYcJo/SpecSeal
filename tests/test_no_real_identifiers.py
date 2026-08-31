"""No real identifiers in the tree — the leak classes that actually bit us.

Both incidents that required a history rewrite entered through the same two
doors: a real domain used as a test fixture, and real machine paths carried
along inside copied config. A written habit decays; a red build does not.

Scope is deliberately class-based (domains, user paths), not a blocklist of
specific names — a blocklist of sensitive words cannot itself live in a
public repo, and (measured) its completeness is exactly what fails.
"""

import os
import re
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")

ALLOWED_DOMAINS = (
    "example.com",  # the designated fixture domain — use this in examples
    "github.com",
    "arxiv.org",
    "claude.com",  # official docs this plugin is built against
)
ALLOWED_USER_PATH = "/Users/x/"  # the designated fixture user

DOMAIN_RE = re.compile(r"\b[a-z0-9][a-z0-9.-]*\.(?:com|io|net|org|ai|dev)\b")
USER_PATH_RE = re.compile(r"/Users/[^\s\"'`)/]+/?")


def tracked_text_files():
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.split()
    for rel in out:
        if rel.endswith((".gif", ".png", ".jpg")):
            continue
        if rel == "tests/test_no_real_identifiers.py":
            continue  # this file defines the patterns and allowlist it hunts
        yield rel


def test_only_neutral_domains():
    violations = []
    for rel in tracked_text_files():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for m in DOMAIN_RE.finditer(line):
                    d = m.group(0)
                    if not any(d == a or d.endswith("." + a) for a in ALLOWED_DOMAINS):
                        violations.append(f"{rel}:{i} {d}")
    assert not violations, (
        "Real-looking domain outside the allowlist — use example.com in "
        "fixtures/examples, or consciously extend ALLOWED_DOMAINS:\n"
        + "\n".join(violations)
    )


def test_only_fixture_user_paths():
    violations = []
    for rel in tracked_text_files():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for m in USER_PATH_RE.finditer(line):
                    if not m.group(0).startswith(ALLOWED_USER_PATH):
                        violations.append(f"{rel}:{i} {m.group(0)}")
    assert not violations, (
        "Real user path in the tree — fixtures use /Users/x/ only:\n"
        + "\n".join(violations)
    )
