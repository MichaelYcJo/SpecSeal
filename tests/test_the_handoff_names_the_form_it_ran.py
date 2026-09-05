"""A handoff carried a command that has two forms, and named neither.

`docs/review-handoff-protocol.md` lists *the runner incantation* among what an
orchestrator hands an implementer, and said nothing about a command whose flag
changes what it reads. Issue #153 measured what that cost: `evidence-check`
scoped to a work item's own fragment was handed to every segment of one work
item, three review rounds and two fix passes all ran it, all reported a clean
ledger, and the unscoped read at the pull request found fifteen drifted rows
and one broken claim — every one in a file the branch had touched.

Neither instruction was wrong about its own subject. The narrowing is what
keeps `--reverify` off a row whose claim is false and belongs to somebody
else, which is correct for the WRITE; it was carried into the READ, where it
blinds. So the prose has to name both forms, and a reader who only learns the
read's form deletes the narrowing and puts the write back on the false claim.

The sibling execution cases live in
`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`: the tool
announces its own narrowing, because a session that narrows on its own
initiative reads none of this. Every case here was seen red at `23c7ccb`,
before the prose existed.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    return " ".join(read(*parts).split())


def test_the_handoff_says_which_form_of_a_command_it_carries():
    """The requirement itself. Without it the handoff carries whichever form
    somebody last found useful, which is exactly what happened."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "A command with more than one form names the form" in protocol, (
        "the handoff's requirements say nothing about a command whose flag "
        "changes what it reads — which is the whole of #153"
    )
    assert "what the other one is for" in protocol, (
        "naming the form without naming the other form's purpose is how the "
        "narrowing got carried across in the first place"
    )


def test_the_handoff_names_the_measurement_that_bought_the_requirement():
    """Every other requirement in that list carries the failure that bought
    it. One without is a rule a reader can talk themselves out of."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "fifteen drifted rows and one broken claim" in protocol, (
        "the requirement arrives with no measurement, where the three "
        "beside it each name theirs"
    )


def test_the_requirement_count_moved_with_the_requirement():
    """A fourth bullet under a sentence that says three is the list counting
    one thing and the reader counting another — and the sentence is what a
    conformance reader skims."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "Four requirements" in protocol
    assert "Three requirements, each bought" not in protocol


def test_the_review_skill_names_both_forms_and_what_each_is_for():
    """The orchestrator writes the spawn prompt, so the table it copies from
    has to hold both rows. Guidance naming one form is how this happened."""
    skill = flat("skills", "code-review", "SKILL.md")
    assert "The check a round runs reads everything" in skill, (
        "the skill has no section on which form of the ledger check a round is handed"
    )
    assert "only a write is narrowed" in skill, (
        "the section names the read and leaves the write unexplained, which "
        "is the half that made the narrowing right in the first place"
    )
    assert "keeps it off a row whose claim somebody else" in skill, (
        "without the write's reason a reader deletes the narrowing "
        "altogether, and `--reverify` re-stamps a false claim"
    )


def test_the_review_skill_refuses_the_repair_that_looks_obvious():
    """The cheap reading of #153 is *stop narrowing*, and it reintroduces
    the defect the narrowing was adopted to fix. The section has to say so,
    or the next reader makes that trade without knowing it is one."""
    skill = flat("skills", "code-review", "SKILL.md")
    assert "do not answer this by deleting the narrowing" in skill


def test_the_review_skill_carries_the_measurement_too():
    """A rule with the measurement stripped out is one the next orchestrator
    weighs against convenience. This one lost that weighing already."""
    skill = flat("skills", "code-review", "SKILL.md")
    assert "fifteen drifted rows and one broken claim" in skill
