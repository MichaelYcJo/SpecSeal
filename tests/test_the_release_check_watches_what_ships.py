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
    "seal",
    "evals",
    "assets",
    ".github",
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
    text = read(WORKFLOW)
    assert STEP in text, f"hygiene.yml no longer has a step named {STEP!r}"
    step = text.split(STEP, 1)[1].split("- name:", 1)[0]
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
    trigger the bump. It said five when the pattern said five; both say six —
    the SAME six, so a seventh root written into the paragraph, or one taken
    out of it, reads as a disagreement with the workflow rather than as prose."""
    doc = read(RELEASE_DOC)
    # The paragraph, not the sentence: `.claude-plugin/` carries a full stop.
    paragraph = doc.split("the `hygiene` workflow", 1)[1].split("\n\n", 1)[0]
    named = set(re.findall(r"`([^`]+)/`", paragraph))
    assert named == SHIPS, (
        f"docs/branch-and-release.md's paragraph about the hygiene workflow "
        f"names {sorted(named)} and the pattern's roots are {sorted(SHIPS)} — "
        "the two have to agree, and this file is where the list is decided"
    )


# What a refused author reads (#443).
#
# The step is correct and its condition does not change here. What changed is
# the message: it named `plugin.json` and a version, and the first person it
# ever refused was a contributor whose pull request was aimed at the wrong
# branch. A contributor following that message would edit the one file a
# contribution must not touch.
#
# At the moment it refuses, the two readers are indistinguishable to the step:
# a release that forgot the bump and a contribution filed against `main` both
# arrive here with `base_ref = main`. So the message names both causes and
# asserts neither, release case first — that is the reader for whom the old
# message was already right.


def release_step():
    """The step's body, from its `- name:` to the next one at the same indent."""
    text = read(WORKFLOW)
    start = text.index(f"- name: {STEP}")
    rest = text[start + 1 :]
    end = rest.find("\n      - name:")
    return rest[: end if end != -1 else len(rest)]


def refusal():
    """The one `::error::` line the step emits when the version did not move."""
    found = re.search(r"::error::(.*)", release_step())
    assert found, "the step no longer emits an ::error:: annotation at all"
    return found.group(1)


def test_the_refusal_names_the_wrong_base_as_one_of_the_two_causes():
    """#443. The real cause of the first refusal this step ever issued was the
    base branch, and the message never said the words."""
    text = refusal()
    assert "base" in text, (
        "the refusal never mentions the base branch, so a contributor whose "
        "base is the cause is told only about a file they must not touch:\n"
        f"{text}"
    )
    assert "release/vX.Y.Z" in text, (
        "the refusal does not say where a contribution's base belongs. A "
        "message that diagnoses without naming the fix leaves the reader "
        f"exactly where they were:\n{text}"
    )
    stale = re.findall(r"release/v\d+\.\d+\.\d+", text)
    assert not stale, (
        f"the refusal names {sorted(set(stale))} — a concrete release branch "
        "is deleted after its release, and a CI message is the worst place "
        "for a fact that expires"
    )


def test_the_refusal_still_serves_the_release_and_puts_it_first():
    """A2's readable half. Somebody genuinely cutting a release meets this
    line too, and for them the old message was correct. It stays, and it stays
    first: that is the order of likelihood for whoever is reading."""
    text = refusal()
    assert "plugin.json" in text, (
        "the refusal no longer names the file a release has to move"
    )
    assert text.index("plugin.json") < text.index("base"), (
        "the base-branch case comes before the version case, so a release "
        f"pull request is read a diagnosis aimed at somebody else first:\n{text}"
    )


def test_the_refusal_asserts_neither_case():
    """The step cannot tell the two apart, so the message must not claim to.
    Both halves are conditional or the message is guessing."""
    text = refusal()
    assert text.count("If this is") == 2, (
        "the refusal does not offer both causes as conditions. The step reads "
        "`base_ref = main` and nothing else, so it cannot know which reader "
        f"it has:\n{text}"
    )


def test_the_refusal_says_not_to_move_the_version_to_satisfy_it():
    """The measured harm. A contributor following the old message edits
    `.claude-plugin/plugin.json`, which is the one file their change must
    leave alone — and the edit would not fix the pull request either."""
    text = refusal()
    assert "Change the base rather than plugin.json" in text, (
        "the refusal names two causes without saying which edit is wrong, "
        f"which is the state that produced #443:\n{text}"
    )


def test_the_refusal_names_the_document_that_holds_the_procedure():
    """A CI log is read by somebody already stuck. The message states the
    cause and the fix inline and cites the file after, rather than making a
    second hop the only way to the answer."""
    text = refusal()
    assert "CONTRIBUTING.md" in text, (
        f"the refusal cites no document for the procedure behind it:\n{text}"
    )


def test_the_base_guard_is_a_closed_if_with_the_early_exit_inside_it():
    """A2. The condition, the exit codes and the set of refused pull requests
    are identical before and after the message change — this is what says so.

    The whole guard, in order, not only its condition:
    `tests/test_a_release_cannot_ship_an_untrue_milestone.py` records a
    mutation that deleted the `exit 0` and the `fi` and passed a check that
    asserted the condition alone, leaving a step that runs on every pull
    request and is malformed shell.

    **Closed before the next `if`, and that word is load-bearing.** The first
    form of this case was a regex spanning `then` to `exit 0 … fi` with
    `re.S`, and the same mutation walked straight past it: this step holds a
    second `if … exit 0 … fi` (the `-z "$ships"` early return) for the dotted
    part to reach. Caught by running the mutation rather than by reading.
    """
    lines = release_step().splitlines()
    opens = [
        number
        for number, line in enumerate(lines)
        if 'github.base_ref }}" != "main" ]; then' in line
    ]
    assert opens, (
        "the step no longer opens with the base guard the other release-only "
        f"steps use:\n{release_step()}"
    )
    start = opens[0]
    after = lines[start + 1 :]

    def first(predicate):
        for offset, line in enumerate(after):
            if predicate(line.strip()):
                return offset
        return len(after)

    closes = first(lambda line: line == "fi")
    reopens = first(lambda line: line.startswith("if "))
    assert closes < reopens, (
        "the base guard is not closed before the next `if` — an `if … then` "
        "left open runs its body on every pull request and is malformed "
        f"shell:\n{release_step()}"
    )
    assert any("exit 0" in line for line in after[:closes]), (
        "the base guard is closed but nothing inside it returns early, so "
        "every contribution now reaches the version check and the exemption "
        f"list every contributor reads in CONTRIBUTING.md is false:\n"
        f"{release_step()}"
    )


def test_the_refusal_still_fails_the_run():
    """The message is the only thing that moved. A refusal that stopped
    exiting 1 would ship an unversioned release in silence."""
    step = release_step()
    assert re.search(r"::error::.*\n\s*exit 1\n", step), (
        f"the ::error:: line is no longer followed by `exit 1`:\n{step}"
    )
