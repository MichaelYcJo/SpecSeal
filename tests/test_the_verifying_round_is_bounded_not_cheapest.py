"""The verifying round is bounded by its diff, and no document calls it the
cheapest round of the run (#639).

Three documents said it was, and a fourth said its surface was the whole
reason it was affordable; one paragraph above that, the fourth also said a
re-check round widened to the whole diff pays the price of a first round.
The measurements did not hold that: #456 measured nine rounds over three
work items at 13.8-17.8 minutes whatever their target, and over
0.14.0-0.15.5 twenty-nine verifying rounds ran at a median of 0.83 x the
span of their own round 1, five of them at or above it. What a round
spends is the frame, the earlier records and the probes, and none of those
shrink with the diff. The diff target bounds the round; it does not make it
cheap.

Each carrier is held to a phrase only the corrected wording uses, and to the
absence of the sentence it used to carry: the gone/stands pair of
`test_the_broad_gate_cell_keeps_every_run.py`. The tree-wide case turns
#639's acceptance grep into a pin, so a new carrier that repeats the exact
phrase is red here. A new carrier that says the same thing in other words
("the least expensive round") is not: the meaning is guarded by the five
pairs, and a new wording of it is a reviewer's catch, as round 1's 🟡 2 was.

Seen red by restoring each old sentence and by deleting each new phrase.
"""

import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# (carrier, the phrase only the corrected wording uses, the sentences it used
# to carry). A gone phrase is the carrier's own old wording at `1fa25931`,
# the base #639 was cut from.
CARRIERS = (
    (
        ("skills", "code-review", "orchestration.md"),
        "so it runs close to a finding round",
        ("That is what keeps it bounded: it is the cheapest round of the run",),
    ),
    (
        ("docs", "review-handoff-protocol.md"),
        "which is the ground #51 observation 1 recorded for the exemption",
        (
            "is the cheapest round of the run by design",
            "a segment that small is the nuance below in its every case",
        ),
    ),
    (
        ("docs", "review-chain-spec.md"),
        # The multiplication sign is named because ruff's RUF001 refuses it.
        "29 verifying rounds ran at a median of 0.83 \N{MULTIPLICATION SIGN} "
        "the span of their own",
        ("on a surface that is a diff rather than a branch — the cheapest round",),
    ),
    (
        ("agents", "warden.md"),
        "The reason is the round's job, not its price",
        (
            "That surface is the whole reason the round is affordable",
            "the shape of round this one exists to be cheaper than",
        ),
    ),
    # The paragraph above the verifying-round bullet, which scoped a re-check
    # round on price too (round 1's 🟡 2). Its gone half is the wording at
    # `5a66666d`, which is also the wording at `1fa25931`.
    (
        ("agents", "warden.md"),
        "instead of answering the finding that came back",
        (
            "turns every returned finding into the price of a first round",
            "which is how a review loop costs more than the work it reviews",
        ),
    ),
)

# Where a session reads what the verifying round is. `tests/` is left out
# because it holds the gone halves above, verbatim.
READ_BY_SESSIONS = ("agents", "skills", "docs", "templates")
READ_BY_PEOPLE = ("README.md", "README.ko.md")
PHRASE = "cheapest round of the run"


def flat(*parts):
    """The file with every run of whitespace collapsed, so a hand-wrapped
    sentence reads as one line."""
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return " ".join(f.read().split())


def test_every_carrier_says_the_round_is_bounded_and_not_cheap():
    for parts, phrase, _gone in CARRIERS:
        assert phrase in flat(*parts), (
            f"{'/'.join(parts)} no longer carries the corrected wording "
            f"({phrase!r} missing)"
        )


def test_no_carrier_calls_the_verifying_round_cheap_again():
    """The absent half, which is evidence only beside the present half
    above: an absence is trivially satisfied by a file that was never
    opened."""
    for parts, _phrase, gone in CARRIERS:
        text = flat(*parts)
        for sentence in gone:
            assert sentence not in text, (
                f"{'/'.join(parts)} carries the retracted cost claim again: "
                f"{sentence!r}"
            )


def test_the_verifying_bar_is_grounded_on_neither_cost_nor_size():
    """`exempt` stays, and the Grounds cell beside it says what the round is.
    #456 measured verifying rounds at 46-58 calls, twice the nuance's
    23-call round, so a size ground is false in the other direction."""
    row = "| verifying | exempt |"
    with open(
        os.path.join(ROOT, "docs", "review-handoff-protocol.md"), encoding="utf-8"
    ) as f:
        rows = [line for line in f if line.startswith(row)]
    assert len(rows) == 1, (
        f"docs/review-handoff-protocol.md has {len(rows)} `{row}` rows"
    )
    grounds = rows[0][len(row) :]
    for word in ("cheap", "small", "by design", "afford"):
        assert word not in grounds, (
            f"the verifying row's Grounds cell makes a cost or size claim "
            f"again: {word!r} in {grounds!r}"
        )


def test_the_phrase_appears_nowhere_a_session_or_a_person_reads():
    found = []
    for top in READ_BY_SESSIONS:
        for dirpath, _dirnames, filenames in os.walk(os.path.join(ROOT, top)):
            for name in filenames:
                path = os.path.join(dirpath, name)
                try:
                    with open(path, encoding="utf-8") as f:
                        text = " ".join(f.read().split())
                except (UnicodeDecodeError, OSError):
                    continue
                if PHRASE in text:
                    found.append(os.path.relpath(path, ROOT))
    for name in READ_BY_PEOPLE:
        if PHRASE in flat(name):
            found.append(name)
    assert not found, f"{PHRASE!r} stands again in: {', '.join(sorted(found))}"
