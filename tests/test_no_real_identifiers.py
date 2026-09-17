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

from conftest import build_tracked_tree, on_disk

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


def tracked_text_files(root=ROOT):
    """`(the text files on disk, the tracked paths that are not)` under `root`.

    `root` is an argument so a case can build a repository with a
    tracked-and-deleted file and watch the guard work. `on_disk` carries why
    the second half is returned instead of dropped.
    """
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.split()
    listed = [
        rel
        for rel in out
        if not rel.endswith((".gif", ".png", ".jpg"))
        # this file defines the patterns and allowlist it hunts
        and rel != "tests/test_no_real_identifiers.py"
    ]
    return on_disk(root, listed)


def domains_in(root=ROOT):
    """`rel:line domain` for every domain outside the allowlist under `root`."""
    violations = []
    files, _ = tracked_text_files(root)
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for m in DOMAIN_RE.finditer(line):
                    d = m.group(0)
                    if not any(d == a or d.endswith("." + a) for a in ALLOWED_DOMAINS):
                        violations.append(f"{rel}:{i} {d}")
    return violations


def user_paths_in(root=ROOT):
    """`rel:line path` for every user path outside the fixture one."""
    violations = []
    files, _ = tracked_text_files(root)
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for m in USER_PATH_RE.finditer(line):
                    if not m.group(0).startswith(ALLOWED_USER_PATH):
                        violations.append(f"{rel}:{i} {m.group(0)}")
    return violations


def test_only_neutral_domains():
    violations = domains_in()
    assert not violations, (
        "Real-looking domain outside the allowlist — use example.com in "
        "fixtures/examples, or consciously extend ALLOWED_DOMAINS:\n"
        + "\n".join(violations)
    )


def test_only_fixture_user_paths():
    violations = user_paths_in()
    assert not violations, (
        "Real user path in the tree — fixtures use /Users/x/ only:\n"
        + "\n".join(violations)
    )


# --- the sweep on a tree the fold has emptied -------------------------------
#
# What a can-fail case has to plant is a token this sweep REFUSES, and the
# two designated fixture values are exactly the ones it allows. So:
#
#   - RFC 2606 reserves `example.net` in the same breath as `example.com`, so
#     it is a domain nobody can ever register and it is not in
#     ALLOWED_DOMAINS. That is the whole of what the case needs.
#   - `/Users/x/` is the allowed user path, so the refused one is spelled with
#     another placeholder name that belongs to nobody.
#
# Both literals sit in this file, which the sweep leaves out of its own corpus
# three functions up, and neither is a real identifier by construction.
REFUSED_DOMAIN = "fixture.example.net"
REFUSED_USER_PATH = "/Users/someone/"


def test_the_domain_sweep_survives_a_tracked_file_the_tree_deleted(tmp_path):
    """#432 at its own coordinate.

    Step 2 of `docs/release-checklist.md` folds every `seal/ledger/` fragment
    away and step 3 runs the whole gate before anything is staged, so the
    index lists paths the disk does not have. This sweep used to end at the
    first of them and report nothing about any file.
    """
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "kept.md": f"a domain the sweep must refuse: {REFUSED_DOMAIN}\n",
            "seal/ledger/folded.md": "the fragment the fold removes\n",
        },
        deleted=["seal/ledger/folded.md"],
    )
    files, missing = tracked_text_files(root)
    assert missing == ["seal/ledger/folded.md"], missing
    assert "kept.md" in files, files
    assert domains_in(root) == [f"kept.md:1 {REFUSED_DOMAIN}"]


def test_the_user_path_sweep_survives_the_same_tree(tmp_path):
    """Both call sites, not one. The defect had already reproduced twice
    inside this module, which is why the guard went into the helper."""
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "kept.md": f"a path the sweep must refuse: {REFUSED_USER_PATH}\n",
            "seal/ledger/folded.md": "the fragment the fold removes\n",
        },
        deleted=["seal/ledger/folded.md"],
    )
    assert user_paths_in(root) == [f"kept.md:1 {REFUSED_USER_PATH}"]


def test_the_sweeps_still_report_nothing_on_a_clean_fixture(tmp_path):
    """The guard does not buy its survival by reporting less: a tree with
    nothing missing and nothing to find is silent from both sweeps."""
    root = build_tracked_tree(
        tmp_path / "r", {"kept.md": "example.com and /Users/x/\n"}
    )
    files, missing = tracked_text_files(root)
    assert missing == [] and files == ["kept.md"]
    assert domains_in(root) == []
    assert user_paths_in(root) == []
