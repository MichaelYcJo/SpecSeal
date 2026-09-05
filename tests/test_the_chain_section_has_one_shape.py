"""A chain-routed pull request body carries one chain section, in one shape:
the comparison table first, then what the rounds found.

Two bodies of the same chain came out unreadable side by side. PR #162 wrote
that section as prose and PR #168 as a table, so the numbers a reader wants to
hold against each other sat in two different shapes -- which is the whole of
what a fixed set of rows buys. `skills/commit-pr-convention/SKILL.md`
§*Pull request bodies* is where a session writing a body actually reads, so
that is where the shape is stated.

Why this is its own file rather than a case in an existing module. The two
modules that already read this skill are about something else:
`tests/test_the_pull_request_language_is_the_repositorys.py` pins the language
row and nothing but it, and `tests/test_a_segment_feeds_the_flow_log.py` pins
`skills/verify/SKILL.md`'s measurement section, which owns the table rather
than carrying it. A reader asking why the chain section has this shape would
open neither.

The absence half is the load-bearing one. The table's rows are defined in
`skills/verify/SKILL.md`, and a second copy of them in this skill is a second
thing to keep in step -- the copy that drifts is the one nobody owns. So the
pointer is asserted and the rows are refused, in the same case.

Each case here was seen red before the prose it pins landed (§15).
"""

import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")

SKILL = ("skills", "commit-pr-convention", "SKILL.md")

# Verbatim from the table in `skills/verify/SKILL.md` §*Measure the segment,
# and feed the flow log*. A paste-back of the rows into the skill under test
# is red rather than invisible.
ROWS = [
    "Findings by severity",
    "Records' share of the diff",
    "Broad gate: how many times",
]


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def body_section():
    """The body of `## Pull request bodies`, heading to the next `## `, as one
    line so a pinned phrase survives re-wrapping.

    Scoped rather than whole-file: this skill names the review chain in other
    sections, so a document-wide search would stay green with the section
    itself saying nothing about the shape."""
    match = re.search(
        r"^## Pull request bodies$(.*?)(?=^## )",
        read(*SKILL),
        re.M | re.S,
    )
    assert match, (
        "the pull request bodies section is gone or renamed. It is the "
        "section a session opens while writing a body, and a rename has to "
        "bring this case with it"
    )
    return " ".join(match.group(1).split())


def test_the_section_states_the_chain_sections_shape():
    """Both halves of the shape, and the condition it holds under.

    The order is the claim: a reader who stops at the first paragraph has
    the numbers, and one who reads on learns what they mean. A body that
    puts the prose first makes the table something to scroll for."""
    section = body_section()
    assert "through the review chain" in section, (
        "the section states a shape without saying which work items it "
        "holds for. This skill ships to repositories that never run this "
        "chain, and a rule with no condition on it reads as a rule for them "
        "too"
    )
    assert "the comparison table first, then what the rounds found" in section, (
        "the chain section has no stated shape, so two runs of the same "
        "chain come out in two shapes -- PR #162 in prose, PR #168 as a "
        "table, neither readable beside the other"
    )


def test_the_section_points_at_the_tables_definition_rather_than_copying_it():
    """The rows have one owner, and this skill is a carrier.

    A carrier that restates the rows is a second place for them to drift,
    and the drift is invisible: both copies read as authoritative, and the
    reader has no way to tell which one the last edit reached."""
    section = body_section()
    assert "skills/verify/SKILL.md" in section, (
        "the section names no owner for the table, so a session writing a "
        "body has a shape to follow and no rows to fill it with"
    )
    assert "Measure the segment, and feed the flow log" in section, (
        "the pointer names the file and not the section, which is a whole "
        "skill to search for one table"
    )
    for row in ROWS:
        assert row not in section, (
            f"the section copies the table's rows ({row!r}). They are "
            "defined in `skills/verify/SKILL.md`; two copies of nine rows "
            "are two things to keep in step"
        )


def test_the_pinned_rows_are_the_owners_own():
    """The absence half above is only worth having while the strings it
    refuses are the strings the owner actually uses. A row reworded in
    `skills/verify/SKILL.md` and not here leaves the refusal guarding
    nothing, silently."""
    owner = read("skills", "verify", "SKILL.md")
    for row in ROWS:
        assert row in owner, (
            f"{row!r} is no longer a row of the table in "
            "`skills/verify/SKILL.md`, so the case above refuses a string "
            "nobody would paste. Re-take these from the owner's table"
        )
