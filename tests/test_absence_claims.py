"""An absence claim ships nothing anyone can open.

"No caller exists", "the original has no such branch" — an existence claim
comes with a coordinate and an absence claim comes with a search that did not
find one, so the cost of checking the two is asymmetric and the absence tends
to pass unread. It reaches a policy document as a fact and stays there.

The rule lives in two places: the skill that labels claims, and the agent that
produces them.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def test_the_skill_applies_the_able_to_fail_condition_to_the_search():
    verify = read("skills", "verify", "SKILL.md")
    assert "An absence claim is only as good as the search behind it" in verify
    assert "run it against a case you know is\npresent" in verify, (
        "condition 2 applied to the search is the operative part"
    )
    assert '"not there"' in verify, (
        "the skill lost the distinction between not found and not there"
    )


def test_the_scribe_does_not_file_an_unrepeatable_absence_as_a_fact():
    """The agent that produces these is where the rule has to hold."""
    scribe = read("agents", "scribe.md")
    assert "An absence carries its search" in scribe
    assert "not under facts" in scribe
