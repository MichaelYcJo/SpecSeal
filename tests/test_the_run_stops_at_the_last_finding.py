"""The cap has a floor, and a quiet round is where the run stops.

Three rounds, five while a 🔴 is open. That is a ceiling, and nothing said when
to stop under one, so it was spent like a budget. #81 ran seven rounds: rounds
1 through 4 each found something that loses a record, and rounds 5, 6 and 7
found none of either kind — roughly an hour of agent time on the flat part of
the curve.

The floor is one sentence: **stop when a round finds nothing that leaves the
root and nothing that crashes**, and whatever else it found is deferred with a
named answerer or becomes an issue. Four files carry it, and the four are not
interchangeable:

  docs/review-chain-spec.md   owns the cap's definition, so it owns the floor's
  skills/code-review/SKILL.md the reader who meets the cap is the reader who
                              needs the floor, and this is where the verifying
                              round the floor must leave standing is defined
  agents/warden.md            the reviewer answers it in a line of its own, the
                              way `Needs a fix` is answered. An orchestrator
                              inferring it from a verdict table is reading
                              rather than reporting
  templates/sdd-round.md      the row the answer is copied into

The cases here are prose assertions, and a prose assertion is worth exactly
what its substring is chosen to be. Each one picks a phrase that cannot survive
the drift it guards against, and the ones that could ship beside their own
contradiction carry an absence half as well — a document can gain the corrected
sentence and keep the old one two paragraphs down, which is how two answers
ship at once (`tests/test_one_word_one_meaning.py` is the precedent).

`ROUND_RECORD_FIELDS` in `tests/test_the_pull_request_language_is_the_repositorys.py`
pins the row's presence in the template. What that list cannot see is whether
the label the reviewer writes matches the row it is copied into, which is the
one case here that derives its expectation instead of restating it.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SPEC = ("docs", "review-chain-spec.md")
SKILL = ("skills", "code-review", "SKILL.md")
WARDEN = ("agents", "warden.md")
TEMPLATE = ("templates", "sdd-round.md")

# The four files the floor is stated in, and the two that state the rule
# itself rather than answer it.
STATES_THE_RULE = (SPEC, SKILL)

PROTOCOL = ("docs", "review-handoff-protocol.md")
CHAIN_CHECK = ("skills", "code-review", "scripts", "chain_check.py")

# Every carrier of the floor's COUNT rule -- where the count of records after
# the floor stops. The commit that wrote the rule wrote it in six places, and
# round 7 of work item 1788501054 changed it in three; round 8 found the other
# three still stating the old rule as the whole rule, one of them the protocol
# that says what a conforming tool does. `chain_check.py` is here because it
# carries the sentence twice, in the module docstring and in
# `stopping_floor`'s, and a docstring above a walk is a carrier a reader opens.
COUNT_RULE_CARRIERS = (SPEC, TEMPLATE, SKILL, PROTOCOL, CHAIN_CHECK)

# The second stop, in the spellings the five carriers use. An enumeration,
# and a bounded one: these are this repository's own sentences, pinned here so
# the next correction that reaches some copies and not the rest goes red.
SECOND_STOP = ("closed on a fix", "verdicts say `fixed`", "`fixed` verdict")

FLOOR = "Stop when a round finds nothing that leaves the root and nothing that crashes."
EXIT = "deferred with a named answerer, or becomes an issue"
ROW = "Loses a record or crashes"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


# --- the sentence, in the two documents that state it -----------------------


def test_both_documents_state_the_stopping_condition():
    """#110's condition, verbatim. A paraphrase in one of the two is how the
    skill and the spec come to say different things about the same cap."""
    for parts in STATES_THE_RULE:
        assert FLOOR in flat(*parts), (
            f"{'/'.join(parts)} does not carry the stopping condition, so the "
            "cap is a ceiling with nothing under it again"
        )


def test_the_exit_is_named_where_the_rule_is():
    """A stopping rule that does not say where the stopped round's other
    findings go is a wall. Both homes are named, in the same breath as the
    rule, in both files."""
    for parts in STATES_THE_RULE:
        assert EXIT in flat(*parts), (
            f"{'/'.join(parts)} states the floor without naming where what "
            "the stopped round found goes instead"
        )


def test_every_carrier_of_the_count_rule_states_both_stops():
    """Round 8's 🔴 1 of work item 1788501054, as the class.

    The count of records after the floor stops at a record whose `Needs a fix`
    says the run reopened AND at one whose own verdicts closed on a fix. The
    second stop was added in three of the rule's six carriers and the other
    three kept stating the first as the whole rule -- one of them the
    protocol, which says what a CONFORMING tool does, so a tool built to it
    refused the sequence the change exists to make writable. Nothing pinned
    the protocol or the two docstrings, so nothing went red.

    Each carrier has to name `Needs a fix` and one spelling of the second
    stop. Seen red against the three copies left behind, then green.
    """
    for parts in COUNT_RULE_CARRIERS:
        text = flat(*parts)
        assert "Needs a fix" in text, (
            f"{'/'.join(parts)} no longer states the count rule at all"
        )
        assert any(spelling in text for spelling in SECOND_STOP), (
            f"{'/'.join(parts)} states the count rule's first stop and not its "
            "second -- a `fixed` verdict stops the count whatever `Needs a fix` "
            "says, and a copy that omits it describes a tool that refuses the "
            "run's own honest end"
        )


def test_neither_document_lets_the_floor_read_as_the_caps_arithmetic():
    """The absence half of the distinction, in the shape of a presence.

    Both files already carry *a round that opens nothing needing a fix does
    not consume the cap*, and it is a different rule: that one decides whether
    a round that has already run counts toward three or five, this one decides
    whether the next round is spawned at all. Side by side and undistinguished,
    the second reads as the first said twice, and the reader who takes them
    for one rule keeps the cap the ceiling it was.
    """
    for parts in STATES_THE_RULE:
        text = flat(*parts)
        assert "does not consume the cap" in text, (
            f"{'/'.join(parts)} lost the rule the floor has to be told apart "
            "from, which makes the distinction below unreadable"
        )
        assert "the cap's arithmetic" in text, (
            f"{'/'.join(parts)} states the floor beside the cap's own "
            "arithmetic rule and does not say which is which"
        )


def test_the_floor_leaves_the_verifying_round_standing():
    """The floor stops the finding rounds. A run still ends by reading its own
    last fixes, so the record that meets the floor is followed by exactly the
    one round that reads them — and by no more than that."""
    for parts in (SPEC, SKILL, TEMPLATE):
        assert "is followed by at most one more round record" in flat(*parts), (
            f"{'/'.join(parts)} does not bound what may follow a record that "
            "met the floor, so the floor either forbids the verifying round "
            "or bounds nothing"
        )


def test_the_skill_enumerates_the_floor_where_it_lists_the_records_contents():
    """🟡 4 of round 1. `skills/code-review/SKILL.md`'s `rounds/round-N.md`
    row lists what a record carries — the target, the verdicts, the probes,
    the deferrals, the broad gate, who checked the fixes, the fix surface,
    and `Needs a fix`. It stopped there, so a session reading the list to
    find out what a record owes is not told about the second answer the run
    ends on."""
    row = next(
        line
        for line in read(*SKILL).splitlines()
        if line.startswith("| `rounds/round-N.md` |")
    )
    assert ROW in row, (
        "the skill's enumeration of a record's contents omits the floor row, "
        f"beside a `Needs a fix` it does name: {row}"
    )


# --- the reviewer's line, and the row it is copied into ---------------------


def test_the_reviewer_answers_the_floor_in_a_line_of_its_own():
    """Both values, because a file that shows only `no` leaves the reviewer
    with a round that found something and no spelling for saying so."""
    text = flat(*WARDEN)
    assert f"{ROW}: no" in text, (
        "agents/warden.md does not give the reviewer the line the floor is "
        "answered in, so the answer goes back to living in a transcript"
    )
    assert f"{ROW}: yes" in text, (
        "agents/warden.md shows only the value that ends the run, so a round "
        "that found something has no spelling for saying so"
    )


def test_the_report_format_section_carries_the_line_too():
    """Two places in `agents/warden.md` describe the reviewer's report: the
    passage on the verifying round's job, and `## Report`, which is the format
    a reviewer writes from. A line in the first and not the second is a line
    nobody writes."""
    body = read(*WARDEN)
    report = body[body.index("\n## Report\n") :]
    assert f"{ROW}: no" in " ".join(report.split()), (
        "`## Report` is the section a reviewer builds its report from and it "
        "does not name the floor line, so the passage above asks for an "
        "answer the format has no field for"
    )


def test_the_line_the_reviewer_writes_is_the_row_it_is_copied_into():
    """Derived rather than restated: the label is read out of the template's
    field table and looked for in the reviewer's file.

    `Needs a fix`'s first user copied the whole line into the cell, label and
    all, and the fix was to say the row already names the field. That only
    holds while the two spellings are the same word.
    """
    rows = re.findall(r"^\| ([^|]+?) \| <", read(*TEMPLATE), flags=re.MULTILINE)
    assert ROW in rows, (
        f"{ROW!r} is not a field row of `templates/sdd-round.md` — the rows "
        f"found are {rows}"
    )
    assert f"{ROW}: " in flat(*WARDEN), (
        f"the template's row is {ROW!r} and `agents/warden.md` asks for a "
        "line spelled some other way, so the copy into the row cannot be a copy"
    )


# --- the template row, and what it no longer claims --------------------------


def test_the_template_explains_the_row_below_its_table():
    """Every other field row is explained in the comment block under the
    table. A row that arrives with no explanation is a row a session guesses
    the values of."""
    body = read(*TEMPLATE)
    comment = body[body.index("- [ ] Pass") :].split("-->")[0]
    text = " ".join(comment.split())
    assert f"`{ROW}` is the FLOOR" in text, (
        "the row went into the field table with no explanation under it, "
        "where every other row has one"
    )
    assert "however much of the cap was left" in text, (
        "the explanation does not say the row stops the run below the cap, "
        "which is the whole of what it is for"
    )


# Each file's old claim that `Needs a fix` was the only thing the run ends on,
# beside the sentence that replaced it. The pair is the point: `skills/verify`
# says an absence claim is only as good as the search behind it, and a search
# that read nothing finds nothing — the mutation that made `read()` return an
# empty string left this case green until the present half was added.
ONLY_ENDING = {
    TEMPLATE: (
        "is the answer the run ends on",
        "is one of the two answers the run ends on",
    ),
    SKILL: (
        "that line is the run's terminal condition",
        "that line is one of the two the run ends on",
    ),
    WARDEN: (
        "It is the run's terminal condition, and what",
        "They are the run's terminal conditions",
    ),
}


def test_needs_a_fix_no_longer_claims_to_be_the_only_ending():
    """The run now ends on either of two answers, and a file that still calls
    one of them *the* answer ships both readings two paragraphs apart."""
    for parts, (gone, stands) in ONLY_ENDING.items():
        text = flat(*parts)
        assert stands in text, (
            f"{'/'.join(parts)} does not carry the corrected sentence, so the "
            "absence below is a search that found nothing rather than a file "
            "that says nothing"
        )
        assert gone not in text, (
            f"{'/'.join(parts)} still presents `Needs a fix` as the run's only "
            "terminal condition, beside a second one"
        )
