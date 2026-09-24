"""`straight to the PR` owes the sealer's `broad-gate.md`, and every document
that describes the answer says so (#241).

`chain_check.py#direct_seal` has required the sealer's stamp at a ready pull
request since `DIRECT_GATE_FROM`: the one broad run, at a SHA, against the
base. Seven places went on saying the direct answer requires nothing — the
specification's declaration table, the checker's own inventory, the
orchestration skill's four-combinations table and its closing paragraph, the
commit gate's first option, that option's own test, and the routing template's
comment. A session that had written a change and checked it itself read any
of them and concluded the vocabulary had no honest answer for it, and asked
for a third one whose record it would write about itself.

The answer is two answers and not three, and the pins here are the shape
`NO_CHECK_READS` set in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`:
an absence is trivially satisfied by a file that was never opened, so the
sentence that STANDS is what makes the sentence that is GONE evidence. Where
a file never carried the false sentence — it named the two answers and what
neither owes — only the standing half is pinned.

The commit gate's option is pinned through the rendered prompt in
`tests/test_routing_is_recorded.py`, because its text is a Python literal
split across lines, which a whole-file substring cannot read.
"""

import os

import pytest
from conftest import REVIEW_CHAIN_DOCS, review_chain_text

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

STANDS = "the sealer's `broad-gate.md`"

# (the sentence that is gone, or None where the file never carried one; the
# sentence that stands). The standing phrase is one no other sentence of the
# same file uses, so the pin is live for the row it was written for (ledger
# R12: a whole-file substring pin is evidence only where the words occur
# nowhere else).
DIRECT_REQUIRES = {
    ("docs", "commit-review-gate-spec.md"): (
        "nothing required; the declaration is printed",
        STANDS,
    ),
    ("skills", "code-review", "scripts", "chain_check.py"): (
        "nothing required — the declaration is printed",
        STANDS,
    ),
    ("skills", "implement", "orchestration.md"): (
        "| nothing required |",
        STANDS,
    ),
    # The corrected docstring's own words, because that file also carries a
    # case whose docstring names the sealer's record — a pin on the bare
    # phrase would be satisfied by the case and not by the correction.
    ("tests", "test_routing_is_recorded.py"): (
        "requires nothing of it at the pull request",
        "requires " + STANDS + " of it and no reviewer's record",
    ),
    ("templates", "sdd-routing.md"): (None, STANDS),
}

# The closing paragraph of the orchestration skill's routing section said the
# direct answer was checked *by the token in every command* — false since the
# declaration silenced the review arm for either answer.
TOKEN_SENTENCE = "the direct answer by the token in every command"


def flat(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


@pytest.mark.parametrize("parts", sorted(DIRECT_REQUIRES))
def test_each_carrier_says_what_the_direct_answer_requires(parts):
    """A8. A reader opening any of the seven places finds what `straight to
    the PR` requires at a ready pull request and no sentence saying it
    requires nothing. Seen red by restoring one of the old sentences."""
    gone, stands = DIRECT_REQUIRES[parts]
    text = flat(*parts)
    assert stands in text, (
        f"{'/'.join(parts)} does not say the direct answer owes the sealer's "
        "record, so the absence below is a search that found nothing rather "
        "than a file that says nothing"
    )
    if parts in REVIEW_CHAIN_DOCS:
        # The sentence left the spec when the spec was split (#526); it must
        # not come back in either sibling.
        text = review_chain_text(ROOT)
    if gone is not None:
        assert gone not in text, (
            f"{'/'.join(parts)} still tells a reader `straight to the PR` "
            "requires nothing, beside a checker that has required the "
            "sealer's record since `DIRECT_GATE_FROM`"
        )


def test_the_routing_sections_closing_paragraph_names_the_seal_not_the_token():
    """The declaration silences the review arm for either answer, so no token
    checks the direct answer at any commit; what checks it is the sealer's
    record at the pull request, and the paragraph now says so."""
    text = flat("skills", "implement", "orchestration.md")
    assert TOKEN_SENTENCE not in text, (
        "the paragraph still says a token checks the direct answer, which "
        "the declaration made false"
    )
    assert "the direct answer against " + STANDS in text, (
        "the paragraph does not say what checks the direct answer instead"
    )


def test_the_specification_says_why_two_answers_and_not_three():
    """Item 8 of the frame: the sentence a later reader of #241 finds beside
    the declaration table instead of the ticket's proposal — what a
    session's own check leaves that CI can read, and where it lives."""
    text = flat("docs", "commit-review-gate-spec.md")
    assert "Two answers, and not three" in text, (
        "the specification does not say why there is no third `Review` answer"
    )
    assert "a review that certifies itself" in text, (
        "the paragraph does not carry the contract's reason"
    )


def test_the_release_checklist_names_the_waiver_as_the_no_work_item_answer():
    """Item 9: the release-preparation commit declares its class — the
    routing question's `no work item` answer, whose recorded form is the
    token in front of each commit — rather than stepping around a gate."""
    text = flat("docs", "release-checklist.md")
    assert "`no work item` answer" in text, (
        "§4 does not name the waiver as the routing question's `no work item` answer"
    )
