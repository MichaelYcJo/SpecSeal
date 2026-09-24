"""The reviewer-facing report standard is one text in the three places a
reviewer copies from — `agents/warden.md`, `skills/code-review/SKILL.md`
and `docs/review-chain-spec.md` — and in the fourth carrier, the round
template's comment beside the verdict table, which the record itself holds;
each is held to it (#503, #437, the comment-opener rule). The module's name
counts the reviewer's three; `CARRIERS` lists all four (round 1's ⬜ 7).

Three reviewers in one release were refused by `round_record.py new` for the
shape of one cell, and the repair is an example where the reviewer copies
from rather than another rule. An example that drifts in one of its carriers
is the two-file disagreement #437 was filed on, so every carrier is pinned to
the same row, and `agents/warden.md` to the sentences only it carries.

Seen red by deleting the worked row from one file, and by deleting each
sentence from the warden.
"""

import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# The worked carried-closure row, one text. A bare marker in `#`, the verdict
# word `confirmed` and never `fixed`, and no 🔴 anywhere in the row.
CARRIED_CLOSURE = (
    "| 🟢 | round N's blocking finding is closed — <what> | <location> | "
    "confirmed | <grounds> |"
)

CARRIERS = (
    ("agents", "warden.md"),
    ("skills", "code-review", "SKILL.md"),
    ("docs", "review-chain-spec.md"),
    ("templates", "sdd-round.md"),
)

WARDEN = ("agents", "warden.md")

# The three carriers the reviewer copies from, by name: the two files the
# reviewer holds and the specification both cite. The template's comment is
# the record's shape, not the reviewer's rule for writing a `Location`.
REVIEWER_CARRIERS = (
    ("agents", "warden.md"),
    ("skills", "code-review", "SKILL.md"),
    ("docs", "review-chain-spec.md"),
)

# #366's second half, one text. `round_record.py#depth_two` keys on a
# finding's `Location` and refuses every unit that finding's fix commit added
# in that file, so a finding whose coordinates sit at two depths has its
# depth-1 units refused beside the depth-2 one. The convention is the
# reviewer's, and the three carriers say it in the same words.
SPLIT_AT_TWO_DEPTHS = (
    "a finding whose coordinates sit at two depths — one inside a unit an "
    "earlier round's fixes created, another not — is written as two findings, "
    "so each verdict carries one depth and the fix of one does not refuse the "
    "units the other's fix adds"
)

# The five markers the findings format names, in the order it names them.
MARKERS = ("🔴", "🟡", "⬜", "🟢", "❓")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    """The file with every run of whitespace collapsed, so a hand-wrapped
    sentence reads as one line."""
    return " ".join(read(*parts).split())


def test_every_carrier_shows_the_same_carried_closure_row():
    """A16 of #437: the worked row is in the two files the reviewer holds, in
    the specification both cite, and in the template's comment beside the
    verdict table — the same bytes in each, so no carrier can drift into a
    row the generator or the cap refuses."""
    for parts in CARRIERS:
        text = read(*parts)
        assert CARRIED_CLOSURE in text, (
            f"{'/'.join(parts)} does not carry the worked carried-closure row "
            "as the other carriers spell it"
        )


def test_the_row_meets_its_own_three_requirements():
    """The pinned text is checked against the rule it illustrates, so a later
    edit to the constant cannot ship a row the readers refuse."""
    cells = [c.strip() for c in CARRIED_CLOSURE.strip("|").split("|")]
    assert cells[0] == "🟢", "a bare marker in the `#` cell"
    assert cells[3] == "confirmed", "the verdict word is `confirmed`, never `fixed`"
    assert "fixed" not in CARRIED_CLOSURE
    assert "🔴" not in CARRIED_CLOSURE, "the inherited severity is written in words"
    assert "blocking" in cells[1]


def test_every_carrier_tells_the_reviewer_to_split_a_finding_that_sits_at_two_depths():
    """#366's second half. The depth in `New units` is declared per entry and
    `depth_two` refuses per finding, so a finding straddling two depths is
    the one shape the two cannot both be right about. The reviewer splits
    it, and the sentence saying so is one text in the three places the
    reviewer copies from — seen red with it deleted from any one of them."""
    for parts in REVIEWER_CARRIERS:
        assert SPLIT_AT_TWO_DEPTHS in flat(*parts), (
            f"{'/'.join(parts)} does not tell the reviewer to split a finding "
            "whose coordinates sit at two depths, in the words the other "
            "carriers use"
        )


def test_the_warden_names_the_five_markers_and_the_tick_as_not_one():
    """A16's second half. The reviewer is told the marker vocabulary where the
    skeleton is, and that `✅` is not in it — the generator admits a tick as
    a row that commissions nothing (Q7, executed), so nothing refuses it and
    only a sentence keeps a reviewer from writing a sixth vocabulary."""
    text = flat(*WARDEN)
    listed = " · ".join(MARKERS)
    assert listed in text, (
        f"agents/warden.md does not list the five markers as {listed!r}"
    )
    assert "`✅` is not one of them" in text, (
        "agents/warden.md does not say the tick is outside the vocabulary"
    )


def test_the_warden_tells_the_reviewer_to_write_the_opener_escaped():
    """The comment-opener rule, one sentence: `&lt;!--` wherever the four
    characters are meant, a code span included. Code-span-aware parsing was
    declined twice in the tree, so the sentence is the whole of the rule."""
    text = flat(*WARDEN)
    assert "Write `&lt;!--`" in text, (
        "agents/warden.md does not tell the reviewer how to spell a comment opener"
    )
    assert "a code span included" in text, (
        "the sentence has to say the rule reaches backticks, which is the case "
        "a reviewer expects to be exempt"
    )


def test_the_warden_allows_subheadings_under_the_two_fenced_sections():
    """#505's permission, stated where the reviewer reads it: `###` under
    `## Paste-ready fixes` and `## Executed probes`, one per finding."""
    text = flat(*WARDEN)
    assert (
        "Under `## Paste-ready fixes` and under `## Executed probes` you may group "
        "with `###` subheadings" in text
    ), "agents/warden.md does not say a reviewer may group the fenced sections"


def test_the_warden_says_where_the_severity_goes():
    """#503's measured cause: two of three reviewers wrote the severity at the
    head of the summary cell and left `#` empty. The sentence names the cell."""
    text = flat(*WARDEN)
    assert (
        "The severity goes in the `#` cell, and never at the head of the Finding cell"
        in text
    )
    assert "never an empty cell, which is the one shape refused" in text
