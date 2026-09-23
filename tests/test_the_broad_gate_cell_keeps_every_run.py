"""Every document that describes the `Broad gate` cell says it holds one
entry per run, newest first — and no document still describes it as one run.

#174 made the cell a list and rewrote eight carriers; round 1 of the work
item that built it found a ninth in `agents/warden.md` by grep, and no test
over any of the nine, so `plan.md`'s "a red test rather than a stale
sentence" did not exist. Each carrier is held to a phrase that only the
list shape uses, and to the absence of the sentence it used to carry — the
gone/stands pair, so that a carrier drifting back to one run is red here
rather than an eighth stale sentence.

Seen red by restoring one old sentence.
"""

import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# (carrier, the phrase only the list shape uses, the sentence it used to
# carry). A gone phrase is the carrier's own old wording at `0b8dc4b2`, the
# commit before #174 landed; `None` where the carrier gained a sentence and
# lost none.
GATE_CARRIERS = (
    (
        ("agents", "sealer.md"),
        "earlier run",
        "which is precisely what the cell records. A tree",
    ),
    (
        ("agents", "warden.md"),
        "earlier run",
        "or the SHA it ran at and the base it was compared against — is",
    ),
    (
        ("docs", "review-chain-spec.md"),
        "earlier run",
        "`not yet` or naming a SHA that precedes",
    ),
    (
        ("docs", "review-handoff-protocol.md"),
        "earlier run",
        "`not yet`, or the SHA it ran at and the base it was compared against. A session",
    ),
    (
        ("skills", "code-review", "SKILL.md"),
        "one entry per full-suite run",
        "or the SHA the one full-suite run happened at, **who",
    ),
    (
        ("skills", "code-review", "orchestration.md"),
        "earlier run",
        "into that cell through `round_record.py seal`. You read",
    ),
    (
        ("skills", "verify", "SKILL.md"),
        "earlier run",
        "one SHA with the base it was compared against",
    ),
    (
        ("templates", "sdd-round.md"),
        "earlier run",
        "or the SHA the one full-suite run happened at and the base it was compared against. WRITTEN",
    ),
)


def flat(*parts):
    """The file with every run of whitespace collapsed, so a hand-wrapped
    sentence reads as one line."""
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return " ".join(f.read().split())


def test_every_carrier_says_the_cell_holds_one_entry_per_run():
    for parts, phrase, _gone in GATE_CARRIERS:
        assert phrase in flat(*parts), (
            f"{'/'.join(parts)} no longer says the Broad gate cell holds one "
            f"entry per run ({phrase!r} missing)"
        )


def test_no_carrier_still_describes_the_cell_as_one_run():
    """The absent half, which is evidence only beside the present half
    above: an absence is trivially satisfied by a file that was never
    opened."""
    for parts, _phrase, gone in GATE_CARRIERS:
        assert gone not in flat(*parts), (
            f"{'/'.join(parts)} describes the cell as one run again: {gone!r}"
        )


def test_the_writers_are_named_as_one_path():
    """The template and the orchestration skill name `close --broad-gate` as
    writing the same cell; since round 1's 🟡 1 they say it writes through
    the same path, so a reader is not told one writer keeps a held run and
    left to guess about the other."""
    assert "through the same path" in flat("templates", "sdd-round.md")
    assert "through the same newest-first path" in flat(
        "skills", "code-review", "orchestration.md"
    )
