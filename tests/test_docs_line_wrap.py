"""Prose in the hand-wrapped documents stays inside 88 display columns.

Nothing else guards this: ruff never opens a markdown file, so a session that
splices a sentence into a paragraph and does not re-wrap leaves a 145-column
line that no check complains about. It happened, which is why this exists.

Width is measured in DISPLAY columns, not characters — a Hangul or CJK
codepoint occupies two. Counting characters would let a Korean line run to
twice the visual width of an English one.

YAML frontmatter is excluded because `description:` is a field tools read, not
prose a reader wraps. That exclusion is load-bearing rather than incidental:
`skills/code-review/SKILL.md:6` is 92 columns, so covering that file at all
depends on it.

Scope is narrower than `agents/*.md` + `skills/*/SKILL.md`, which do not hold
the limit today. These are their current prose maxima, re-derived 2026-09-16
with `prose_lines` and `display_width` below — a number written by hand goes
stale silently, and two of these four had (#422 reported one of them):

    agents/scribe.md               160
    agents/smith.md                109
    skills/writing-style/SKILL.md  209
    skills/implement/SKILL.md       90

`skills/commit-pr-convention/SKILL.md` is covered: it was written wrapped, so
it never had a maximum to bring down.

Add a file here once its prose fits, rather than raising LIMIT — the limit is
the thing with value.
"""

import os
import re
import unicodedata

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")

LIMIT = 88

# Spelled the way `skills/verify/scripts/unverified_check.py#FOLD_MARKER`
# spells it, because what this skips has to be exactly what that reads: a
# line this skipped and the reader did not would be an unwrapped line nobody
# checks, and a line the reader accepted and this did not is the wrap limit
# refusing a fold record.
FOLD_MARKER = re.compile(r"<!-- specs/\S+ -->")

# Both editions or neither. `CONTRIBUTING.md` requires the two READMEs to move
# together, so every documentation change touches the Korean one — and it was
# the furthest outside the limit, which made it the first file a
# "cover what already fits" rule dropped. That is exactly backwards: the file
# edits reach most often would have been the one nothing guarded.
README_PAIR = ["README.md", "README.ko.md"]

COVERED = [
    *README_PAIR,
    "CONTRIBUTING.md",
    # Wrapped from its first line, so it goes in at birth rather than waiting
    # for the sweep that would otherwise be needed to bring it under.
    "SECURITY.md",
    "agents/warden.md",
    # Wrapped from its first line, so it goes in at birth rather than waiting
    # for the sweep that would otherwise be needed to bring it under. It was
    # the first `agents/*.md` file to arrive that way; `framer.md` below is
    # the second, and `smith.md` and `scribe.md` sit at 109 and 160, which is
    # why the docstring lists those two instead of this list holding them.
    # Whether those two join this list is an open row in `seal/follow-up.md`
    # for the repository owner; a corrected number is not that argument.
    "agents/sealer.md",
    # The fifth definition (#84), on the sealer's terms exactly: a file
    # written wrapped has no sweep to owe, so it goes in at birth.
    "agents/framer.md",
    "skills/code-review/SKILL.md",
    # The orchestrator's half of the same file (#265). It arrives
    # already wrapped, because it was wrapped as part of the file it
    # was cut from — dropping it here would lose coverage 418 lines
    # of prose already had.
    "skills/code-review/orchestration.md",
    # The orchestrator's half of `implement` (#292), the same way: its prose
    # fits at birth (83 columns, measured when it was cut), where the file it
    # was cut from does not, so covering it here loses nothing and keeps it.
    "skills/implement/orchestration.md",
    # Wrapped from its first line, so it goes in at birth rather than waiting
    # for the sweep that would otherwise be needed to bring it under.
    "skills/commit-pr-convention/SKILL.md",
    # Wrapped from its first line, so it goes in at birth rather than waiting
    # for the sweep that would otherwise be needed to bring it under.
    "docs/release-checklist.md",
    # The same, and the first `templates/` entry. Its siblings are not here
    # because they hold tree drawings and placeholder rows wider than the
    # limit, and bringing those under is a sweep, not this work item.
    "templates/config.md",
    # Wrapped from their first line, so they go in at birth rather than
    # waiting for a sweep; the directory holds measured platform facts.
    "docs/experiments/README.md",
    "docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md",
    "docs/experiments/README.ko.md",
    "docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.ko.md",
    # Wrapped from its first line, so it goes in at birth rather than waiting
    # for the sweep that would otherwise be needed to bring it under.
    "skills/agent-contract/SKILL.md",
    # The twenty-fourth skill (#458), on the same terms: written wrapped, so
    # it has no sweep to owe and goes in with its first commit.
    "skills/settle/SKILL.md",
    # The same, and the tracker's own authority: it was written wrapped, so it
    # never had a maximum to bring down.
    "docs/issues-and-milestones.md",
    # Wrapped from its first line, so it goes in at birth. Nearly all of it is
    # HTML comments, which GitHub does not render and this file does not skip
    # — and the edit box a contributor reads them in wraps nothing for them,
    # so the limit is doing visible work here rather than tidying a source.
    ".github/PULL_REQUEST_TEMPLATE.md",
    # The policy documents the first fold wrote. Each was written wrapped,
    # so each goes in at birth with no sweep to owe — and each is a document
    # a work item's spec was folded INTO, which is what puts the fold marker
    # above in the way of the limit.
    "docs/the-evidence-ledger.md",
    "docs/the-broad-gate.md",
    "docs/measuring-a-run.md",
    "docs/the-agent-set.md",
    # Two of the three documents #526 split `docs/review-chain-spec.md` into.
    # The file they were cut from never joined this list; the two new ones
    # arrive measured under the limit, so they go in at birth with no sweep
    # to owe.
    "docs/commit-review-gate-spec.md",
    "docs/round-record-spec.md",
]


def display_width(line):
    """Columns the line occupies: East Asian Wide and Fullwidth count as two."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in line)


def prose_lines(text):
    """Every line that is hand-wrapped prose.

    Skipped: YAML frontmatter, fenced code, table rows, images and block
    quotes (all wrap on their own terms or not at all), any line carrying a
    URL, which cannot be broken, and a fold marker, which cannot be broken
    either.

    **A fold marker is not prose.** `<!-- specs/<work-item-id> -->` is the
    record `settle` reads to know a work item's spec was absorbed by a policy
    document, and the reader matches it whole:
    `^<!-- specs/(\\S+) -->$`. Wrapping it makes it stop being a fold record,
    so the retirement refuses the directory it covers — the line is fixed at
    the length of the id it names, and the id is
    `<unix-epoch-seconds>-<slug>` with nothing bounding the slug.

    Measured when the first fold landed: of 88 markers, one reached 89
    columns and the rest fit. So this is not a limit somebody can stay under
    by choosing shorter words in the document — it is decided by a directory
    name chosen months earlier, in another work item, by whoever opened it.
    """
    lines = text.splitlines()
    in_fence = False
    in_frontmatter = lines[:1] == ["---"]
    for number, line in enumerate(lines, 1):
        if in_frontmatter:
            if number > 1 and line.strip() == "---":
                in_frontmatter = False
            continue
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith(("|", "![", ">")):
            continue
        if "http://" in line or "https://" in line:
            continue
        # The raw line, not `stripped`: the reader anchors the marker at
        # column 0 with nothing after it, so an indented one is no fold record.
        if FOLD_MARKER.fullmatch(line):
            continue
        yield number, line


@pytest.mark.parametrize("relative", COVERED)
def test_prose_stays_within_the_wrap_limit(relative):
    with open(os.path.join(ROOT, relative), encoding="utf-8") as handle:
        text = handle.read()
    over = [
        (number, display_width(line))
        for number, line in prose_lines(text)
        if display_width(line) > LIMIT
    ]
    assert not over, "\n".join(
        f"{relative}:{number} is {width} columns (limit {LIMIT})"
        for number, width in over
    )


def test_a_fold_marker_is_skipped_and_the_line_beside_it_is_not():
    """The skip is exactly one line wide.

    A marker cannot be wrapped without ceasing to be a fold record, so it is
    skipped; everything else in the file is still prose. The pair matters
    because a skip written one line too wide would take the folded sentence
    with it, and a folded sentence is the prose this limit exists for.
    """
    marker = "<!-- specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections -->"
    assert display_width(marker) > LIMIT, (
        "the marker this case is about now fits, so it proves nothing — pick "
        "a longer work item id"
    )
    over_long_prose = "word " * 30
    numbers = [n for n, _line in prose_lines(f"{marker}\n{over_long_prose}\n")]
    assert numbers == [2], (
        f"the marker is line 1 and the prose is line 2; prose_lines yielded {numbers}"
    )


def test_a_marker_that_is_not_on_a_line_of_its_own_is_still_prose():
    """A marker quoted inside a sentence is a description, not a fold record
    — the same rule `unverified_check.folded_items` reads it by — so the
    sentence carrying it wraps like any other."""
    line = "The comment " + "<!-- specs/x -->" + " is what records a fold, " * 4
    assert display_width(line) > LIMIT
    assert [n for n, _ in prose_lines(line + "\n")] == [1]
    # Nor is an indented one: the reader matches the raw line from column 0,
    # so a skip that stripped first would pass a line nobody reads as a fold.
    indented = "  <!-- specs/" + "an-indented-marker-" * 5 + " -->"
    assert display_width(indented) > LIMIT
    assert [n for n, _ in prose_lines(indented + "\n")] == [1]


def test_the_check_can_fail():
    """A limit nothing can trip is not a limit."""
    long_line = "word " * 30
    assert display_width(long_line) > LIMIT
    assert list(prose_lines(long_line)) == [(1, long_line)]


def test_both_readmes_are_covered_together():
    """Neither README may be dropped from COVERED without the other."""
    covered = [f for f in README_PAIR if f in COVERED]
    assert covered == README_PAIR, (
        "README.md and README.ko.md are covered together or not at all — "
        f"COVERED holds {covered}"
    )


def test_wide_characters_count_double():
    assert display_width("가나다") == 6
    assert display_width("abc") == 3


def test_tables_and_fences_are_not_prose():
    text = "| a | b |\n```\nlong fenced line\n```\nplain\n"
    assert [line for _, line in prose_lines(text)] == ["plain"]
