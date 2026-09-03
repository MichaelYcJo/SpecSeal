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
the limit today. These are their current prose maxima, measured the same way:

    agents/scribe.md               160
    agents/smith.md                148
    skills/writing-style/SKILL.md  209
    skills/implement/SKILL.md       99

`skills/commit-pr-convention/SKILL.md` is covered: it was written wrapped, so
it never had a maximum to bring down.

Add a file here once its prose fits, rather than raising LIMIT — the limit is
the thing with value.
"""

import os
import unicodedata

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")

LIMIT = 88

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
    "skills/code-review/SKILL.md",
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
]


def display_width(line):
    """Columns the line occupies: East Asian Wide and Fullwidth count as two."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in line)


def prose_lines(text):
    """Every line that is hand-wrapped prose.

    Skipped: YAML frontmatter, fenced code, table rows, images and block
    quotes (all wrap on their own terms or not at all), and any line carrying
    a URL, which cannot be broken.
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
