"""`CONTRIBUTING.md` tells an outside contributor where a pull request goes,
and what this repository's own workflow does not ask of them.

A first-time contributor opened #443 against `main`, because nothing this
repository shows a contributor said where a pull request goes. The hygiene
step that caught it then named `plugin.json` — the one file a contribution
must not touch — instead of the base branch. The message is repaired in
`tests/test_the_release_check_watches_what_ships.py`; this file pins the
other half, the procedure itself.

**The pin is deliberately minimal.** A case per sentence goes red for a
reword, which teaches people to write less prose, and prose is what this
section is. What is pinned is that the section exists, that it is the first
thing in the file, that it names the branch by convention rather than by
version number, and that the exemption list still names each thing a
contributor does not write. Anything finer is a reader's job.

**`test_no_contributor_facing_surface_names_a_concrete_release_branch`
reaches past `CONTRIBUTING.md`.** Round 1's 🟡 5
found the branch-by-convention rule pinned on one surface and written on four,
so that one case reads `README.md`, `README.ko.md` and the pull request
template as well. It stays here rather than in a module of its own because it
is the same rule this file already pins, one surface wider.

Modelled on `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`'s
`running_the_checks()`, which reads one `CONTRIBUTING.md` section to the next
heading and asserts what that section names. (`plan.md` and `questions.md` Q6
name that helper `contributing_section`; no helper of that name exists, and
the correction is recorded in `phases/phase-1.md`.)
"""

import os
import re

import pytest
from conftest import build_tracked_tree
from test_release_hygiene import LOADED, tracked

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUIDE = os.path.join(ROOT, "CONTRIBUTING.md")
HEADING = "## Opening a pull request"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def section(text, heading=HEADING):
    """The named section of `CONTRIBUTING.md`, to the next `## ` heading."""
    start = text.index(heading)
    return text[start : text.index("\n## ", start + 1)]


def guide_section():
    return section(read(GUIDE))


def test_the_procedure_is_the_first_section_of_the_guide():
    """A4. The file used to open on how to run the suite, which is the fourth
    thing a newcomer needs and the first thing they met."""
    headings = re.findall(r"^## .+$", read(GUIDE), re.MULTILINE)
    assert headings, "CONTRIBUTING.md has no `## ` headings at all"
    assert headings[0] == HEADING, (
        f"the first section of CONTRIBUTING.md is {headings[0]!r}; a "
        f"contributor meets it before {HEADING!r}, which is the one written "
        "for them"
    )


def test_the_section_names_the_branch_by_convention_not_by_number():
    """Q1. A version number in a contribution guide is a fact that goes stale
    on a schedule, in the one document a newcomer trusts."""
    body = guide_section()
    assert "release/vX.Y.Z" in body, (
        "the section does not name the release-branch convention, so a "
        "contributor has no rule to apply after the next release"
    )
    stale = re.findall(r"release/v\d+\.\d+\.\d+", body)
    assert not stale, (
        f"the section names {sorted(set(stale))} — a concrete release branch "
        "is deleted after its release, so this sentence becomes false on a "
        "schedule. Name the convention instead"
    )


def test_the_section_says_the_base_branch_is_what_the_refusal_is_about():
    """A1's other half. The contributor who arrives here arrives from a CI
    message about `plugin.json`, and has to come away knowing the base is the
    cause. Both terms have to be in the section a reader searches."""
    body = guide_section()
    assert "`main`" in body, "the section never names the branch to avoid"
    assert "plugin.json" in body, (
        "the section never names the file the refusal names, so a contributor "
        "reading that refusal cannot tell this section is about them"
    )


@pytest.mark.parametrize(
    "thing",
    [
        "routing.md",
        "spec.md",
        "plan.md",
        "review round record",
        "seal/ledger/",
        "changelog.md",
        "overview.md",
        ".claude-plugin/plugin.json",
    ],
)
def test_the_exemption_list_names_what_a_contribution_does_not_write(thing):
    """A5. An outsider looking at this repository's work items, review rounds
    and ledger has every reason to assume all of it applies to them. The list
    is the half of the section that cannot be inferred."""
    body = guide_section()
    assert thing in body, (
        f"the section does not say a contribution writes no {thing!r} — an "
        "exemption that is not stated reads as a requirement nobody explained"
    )


def test_the_exemption_list_says_which_guard_makes_it_true():
    """A10. The list is true because the release-only steps exit early on any
    base but `main`. Stated as a bare promise it is a sentence a new
    always-on CI step silently falsifies; stated with the guard, a reader
    adding a step can see which sentence it lands in."""
    body = guide_section()
    assert "exits 0 unless the base is `main`" in body, (
        "the exemption list does not name the guard that makes it true, so it "
        "reads as a promise rather than as a consequence of the workflow"
    )


def test_the_section_warns_about_the_check_that_can_still_refuse():
    """Q4. `survivor_check.py`'s refusal tells the author to record the
    exemption in a `survivors.md` under `seal/specs/` — a convention a
    contribution has none of. The message is out of scope; the trap is closed
    with a sentence instead.

    Round 1's 🟡 4 found a second check of the same shape — a BROKEN ledger
    anchor is exit 2, not a warning — so the section names two. This case
    still pins only `survivor_check.py`'s, which is the one whose own refusal
    names the file to create.
    """
    body = guide_section()
    assert "survivors.md" in body, (
        "the section does not mention the check whose refusal sends a "
        "contributor into a convention they do not have"
    )
    assert "Do not create one" in body, (
        "the section names `survivors.md` without telling a contributor not "
        "to create one, which is the instruction the refusal itself gives"
    )


def test_the_check_can_fail():
    """A guard that cannot fail is a counterfeit. A guide without the section
    raises rather than passing vacuously."""
    with pytest.raises(ValueError):
        section("# Contributing\n\n## Running the checks\n\ntext\n")


# --- Q1 as a class, not as the coordinate it was found on (round 1, 🟡 5) ---

CONVENTION_SURFACES = [
    "README.md",
    "README.ko.md",
    os.path.join(".github", "PULL_REQUEST_TEMPLATE.md"),
]


@pytest.mark.parametrize("surface", CONVENTION_SURFACES)
def test_no_contributor_facing_surface_names_a_concrete_release_branch(surface):
    """Q1 holds wherever the convention is written, not only where it was
    first written.

    Four surfaces carry the release-branch convention after this work item and
    two of them were pinned — `CONTRIBUTING.md` above, and the refusal text in
    `tests/test_the_release_check_watches_what_ships.py`. This branch put the
    same sentence on three more and guarded none, which is the defect being
    the coordinate rather than the class.

    The template is the most exposed of the three: it is pre-filled into every
    pull request, a maintainer reads it weekly, and "helpfully" replacing
    `release/vX.Y.Z` with today's branch is the single edit Q1 exists to stop.
    A concrete branch is deleted after its release, so the sentence becomes
    false on a schedule wherever it stands.
    """
    text = read(os.path.join(ROOT, surface))
    assert "release/vX.Y.Z" in text, (
        f"{surface} no longer names the release-branch convention at all, so "
        "a contributor reading it has no rule to apply after the next release"
    )
    stale = re.findall(r"release/v\d+\.\d+\.\d+", text)
    assert not stale, (
        f"{surface} names {sorted(set(stale))} — a concrete release branch is "
        "deleted after its release. Name the convention instead"
    )


# --- the same rule, one population wider (#466) -----------------------------

# The four surfaces above were the population the convention was WRITTEN on.
# A concrete branch name goes stale wherever a reader meets it, so the rule
# reaches every file the hygiene timer rule already reads — the tuple
# `tests/test_release_hygiene.py#LOADED` names, through that module's own
# `tracked` — and not a list of its own that would rot the way the four did.
RELEASE_BRANCH = re.compile(r"release/v\d+\.\d+\.\d+")

# A concrete name that is history rather than a timer: a dated measurement, a
# branch that shipped under another version, and a merge the correction
# checker's own history walk found. Each is the sentence that carries the
# name, whitespace-collapsed, so the name is allowed where that sentence
# stands and nowhere else in the file — the shape `test_release_hygiene.py`
# gives *the branch `release/v0.3.0` shipped as 0.2.0*.
RELEASE_BRANCH_HISTORY = {
    "agents/smith.md": "measurement was taken at `release/v0.9.3`",
    "docs/issues-and-milestones.md": "the branch `release/v0.3.0` shipped as 0.2.0",
    "skills/evidence-check/scripts/correction_check.py": (
        "opening it showed correct work: `release/v0.9.3` re-anchored a row"
    ),
}


def concrete_release_branches(root, history=RELEASE_BRANCH_HISTORY):
    """{file: the concrete release branches it names outside its history}."""
    files, _missing = tracked(*LOADED, root=root)
    found = {}
    for rel in files:
        try:
            text = " ".join(read(os.path.join(root, rel)).split())
        except UnicodeDecodeError:
            continue
        phrase = history.get(rel)
        if phrase is not None:
            text = text.replace(phrase, "")
        names = RELEASE_BRANCH.findall(text)
        if names:
            found[rel] = sorted(set(names))
    return found


def test_no_loaded_file_names_a_concrete_release_branch():
    found = concrete_release_branches(ROOT)
    assert not found, (
        "a concrete release branch is deleted after its release, so a file "
        "that ships naming one is false on a schedule. Name the convention "
        "(`release/vX.Y.Z`) instead, or, where the name is history, add the "
        "sentence that carries it to RELEASE_BRANCH_HISTORY: "
        + "; ".join(f"{rel}: {', '.join(n)}" for rel, n in sorted(found.items()))
    )


def test_the_widened_pin_reads_a_file_the_four_surfaces_never_held(tmp_path):
    """S16. A shipped skill outside the original four surfaces, naming a
    concrete branch in a usage line, is refused; the history sentence beside
    it in the same tree is not."""
    root = build_tracked_tree(
        tmp_path / "tree",
        {
            "skills/x/SKILL.md": "Run `x --range origin/release/v1.2.3...HEAD`.\n",
            "docs/issues-and-milestones.md": (
                "Here the branch `release/v0.3.0` shipped as 0.2.0, once.\n"
            ),
        },
    )
    assert concrete_release_branches(str(root)) == {
        "skills/x/SKILL.md": ["release/v1.2.3"]
    }


@pytest.mark.parametrize("rel", sorted(RELEASE_BRANCH_HISTORY))
def test_each_history_sentence_still_stands(rel):
    """An allowance whose sentence is gone allows nothing and reads as if it
    did. It is removed with its sentence, so the list stays the set of names
    that are history in the tree as it stands."""
    text = " ".join(read(os.path.join(ROOT, rel)).split())
    assert RELEASE_BRANCH_HISTORY[rel] in text, (
        f"{rel} no longer carries the history sentence the allowance names; "
        "remove the entry"
    )
