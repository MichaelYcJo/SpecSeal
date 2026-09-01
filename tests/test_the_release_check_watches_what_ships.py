"""The hygiene step that asks a release for a version bump watches every root
that ships.

Issue #10. Updates are keyed to the version in `plugin.json`, so a change to
what ships that leaves the version alone reaches nobody — that is the whole
reason the step exists. Its pattern named five roots and `bin/` was not one
of them, although the plugin loader puts `bin/` on the Bash tool's PATH
(Claude Code plugin reference, *File locations*: "Executables added to the
Bash tool's PATH and invokable as bare commands while the plugin is
enabled"). A pull request fixing only a wrapper would have shipped without
moving the version, and nothing would have said so.

Nothing pinned the pattern, which is how a root fell out of it unnoticed.
This file is the pin. It reads the pattern out of the workflow rather than
restating it, classifies every tracked top-level entry of the repository as
shipping or staying home, and fails on an entry nobody has classified — so
the next `commands/` or `output-styles/` is a decision somebody makes in this
file rather than a gap somebody notices while writing a change up.

The pattern is matched with Python's `re`, not by spawning `grep -E`: the
suite runs on windows-latest too, and the pattern uses only anchors,
alternation and one escaped dot, which POSIX ERE and `re` read alike.
"""

import os
import re
import subprocess

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")
RELEASE_DOC = os.path.join(ROOT, "docs", "branch-and-release.md")
STEP = "a change to what ships must move the version"

# What the plugin loader reads or puts in front of a user while the plugin is
# enabled. A root here must be matched by the workflow's pattern.
SHIPS = {
    "skills",  # skills/<name>/SKILL.md
    "agents",  # agents/<name>.md
    "hooks",  # hooks/hooks.json and the scripts it names
    "templates",  # what the implement skill bootstraps a repository from
    ".claude-plugin",  # the manifest; the version itself
    "bin",  # executables the loader puts on the Bash tool's PATH
}

# This repository's own work: read by people on GitHub, by tooling in a clone,
# or by the suite. None of it reaches a user through the plugin, so a change
# confined to it needs no version bump. An entry here must NOT be matched.
STAYS_HOME = {
    "docs",
    "tests",
    "specs",
    "evals",
    "assets",
    ".github",
    ".specseal",
    ".gitattributes",
    ".gitignore",
    "CHANGELOG.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.ko.md",
    "README.md",
    "SECURITY.md",
    "install.sh",  # a person runs it from a clone; the loader never does
    "uninstall.sh",
    "ruff.toml",
}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def ships_pattern():
    """The regex the step filters the diff's file list through, verbatim."""
    step = read(WORKFLOW).split(STEP, 1)[1].split("- name:", 1)[0]
    found = re.search(r"grep -E '(\^\([^']*\)/)'", step)
    assert found, "the step no longer filters the file list with grep -E '^(...)/'"
    return re.compile(found.group(1))


def tracked_top_level_entries():
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return {line.split("/", 1)[0] for line in out.splitlines() if line}


def test_the_two_lists_do_not_overlap():
    assert not SHIPS & STAYS_HOME


@pytest.mark.parametrize("root", sorted(SHIPS))
def test_every_shipping_root_is_watched(root):
    """A change under a root the loader reads has to move the version."""
    pattern = ships_pattern()
    assert pattern.match(f"{root}/anything"), (
        f"`{root}/` ships but the hygiene step's pattern {pattern.pattern!r} "
        f"does not match it — a release fixing only `{root}/` would reach "
        "nobody, because updates are keyed to the version it leaves alone"
    )


@pytest.mark.parametrize("entry", sorted(STAYS_HOME))
def test_nothing_that_stays_home_is_watched(entry):
    """A wrong deny at the release is a stopped release: a change confined to
    this repository's own work must not be asked for a version bump."""
    pattern = ships_pattern()
    assert not pattern.match(f"{entry}/anything"), (
        f"`{entry}` does not reach a user through the plugin, yet the pattern "
        f"{pattern.pattern!r} would demand a version bump for it"
    )


def test_the_pattern_names_nothing_this_file_has_not_classified():
    """The pattern can only name roots this file says ship. A root added to the
    workflow alone is a decision with no record of why."""
    named = set(ships_pattern().pattern[2:-2].replace("\\", "").split("|"))
    assert named == SHIPS, (
        f"the pattern names {sorted(named)} and this file says {sorted(SHIPS)} "
        "ship — classify the difference here, with the reason"
    )


def test_every_top_level_entry_is_classified():
    """A directory nobody has classified is the state `bin/` was in: it ships
    or it does not, and neither answer is safe to leave to whoever notices."""
    unclassified = tracked_top_level_entries() - SHIPS - STAYS_HOME
    assert not unclassified, (
        f"{sorted(unclassified)} is tracked at the top level and classified "
        "neither as shipping nor as staying home. Decide — does the plugin "
        "loader read it, or does a user run it while the plugin is enabled? — "
        f"and add it to SHIPS or STAYS_HOME in {os.path.basename(__file__)}"
    )


def test_the_release_document_names_the_same_roots():
    """`docs/branch-and-release.md` tells the release sequence which roots
    trigger the bump. It said five when the pattern said five; both say six."""
    doc = read(RELEASE_DOC)
    # The paragraph, not the sentence: `.claude-plugin/` carries a full stop.
    paragraph = doc.split("the `hygiene` workflow", 1)[1].split("\n\n", 1)[0]
    missing = [root for root in sorted(SHIPS) if f"`{root}/`" not in paragraph]
    assert not missing, (
        f"docs/branch-and-release.md's paragraph about the hygiene workflow "
        f"does not name {missing} among the roots that need a version bump"
    )
