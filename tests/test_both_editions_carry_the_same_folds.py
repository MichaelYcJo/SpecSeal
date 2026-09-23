"""Both editions of a document carry the same folds, heading for heading.

`CONTRIBUTING.md` requires every document with a `.ko.md` edition to move
with its English one, and a mirror drifts one edit at a time. It did: the
first fold (#504) wrote a section and ten fold markers into
`docs/one-root-by-lifetime.md` and nothing into its Korean edition, and
nothing noticed, because the only pin compared one section's cell count
(`tests/test_settle_reads_before_it_removes.py#test_both_editions_took_the_same_decisions`).

The two editions are prose in two languages, so nothing here compares
sentences. What is language-neutral is the outline and the markers: the
sequence of heading levels, and the multiset of fold-marker ids under each
heading position. A marker moved to another section in one edition, a
heading added to one edition only, and a fold written into one edition only
each change one of those.

Markers are read with the fold's own reader —
`skills/verify/scripts/unverified_check.py#live_lines` and `#FOLD_MARKER` —
so a marker this counts is exactly one the fold would count
(`docs/the-evidence-ledger.md` §*The fold, and what tells it from a
deletion*: one function decides what live means). A heading is a live line
matching `^#{1,6} `; the space is required, because each edition has a prose
line that begins `#<number>`.
"""

import collections
import importlib.util
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
DOCS = os.path.join(ROOT, "docs")
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")

HEADING = re.compile(r"^(#{1,6}) ")


def _reader():
    spec = importlib.util.spec_from_file_location("unverified_check", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uc = _reader()


def outline(text):
    """`[(level, Counter of marker ids)]`, one entry per heading position.

    Position 0 is everything above the first heading, at level 0, so a marker
    in a preamble has a position too."""
    sections = [(0, collections.Counter())]
    for line, live in uc.live_lines(text.splitlines()):
        if not live:
            continue
        heading = HEADING.match(line)
        if heading:
            sections.append((len(heading.group(1)), collections.Counter()))
            continue
        sections[-1][1].update(uc.FOLD_MARKER.findall(line))
    return sections


def disagreements(name, english, korean):
    """What the two editions of `name` disagree on, as sentences; empty when
    they agree."""
    en, ko = outline(english), outline(korean)
    en_levels = [level for level, _ in en]
    ko_levels = [level for level, _ in ko]
    if en_levels != ko_levels:
        return [
            f"{name}: the heading levels differ — English {en_levels}, "
            f"Korean {ko_levels}; one edition has a heading the other lacks"
        ]
    found = []
    for position, ((_, en_ids), (_, ko_ids)) in enumerate(zip(en, ko, strict=True)):
        if en_ids == ko_ids:
            continue
        missing = sorted((en_ids - ko_ids).elements())
        extra = sorted((ko_ids - en_ids).elements())
        found.append(
            f"{name}: heading position {position} — the Korean edition lacks "
            f"{missing} and carries {extra} the English does not"
        )
    return found


def pairs():
    """Every top-level `docs/X.ko.md` beside a `docs/X.md`, as names."""
    return [
        name[: -len(".ko.md")]
        for name in sorted(os.listdir(DOCS))
        if name.endswith(".ko.md")
        and os.path.isfile(os.path.join(DOCS, name[: -len(".ko.md")] + ".md"))
    ]


def read(name):
    with open(os.path.join(DOCS, name), encoding="utf-8") as f:
        return f.read()


def test_every_paired_document_carries_the_same_folds_under_the_same_headings():
    """A1, A2. The walk reads at least one pair, so a broken listing cannot
    pass on an empty walk."""
    names = pairs()
    assert names, "no docs/X.ko.md beside a docs/X.md was read"
    found = []
    for name in names:
        found += disagreements(name, read(name + ".md"), read(name + ".ko.md"))
    assert not found, "\n".join(found)


def test_the_contribution_guide_owns_the_rule_and_names_this_check():
    """A11. `CONTRIBUTING.md` is the rule's owner, and a rule whose owner does
    not say which check reads it is one a contributor meets only at CI."""
    with open(os.path.join(ROOT, "CONTRIBUTING.md"), encoding="utf-8") as f:
        guide = f.read()
    assert "every document with a `.ko.md`\n  edition" in guide, (
        "CONTRIBUTING.md's pairing rule no longer covers every `.ko.md` edition"
    )
    assert "tests/test_both_editions_carry_the_same_folds.py" in guide, (
        "CONTRIBUTING.md's pairing rule does not name the check that reads it"
    )


def test_a_fold_written_into_one_edition_only_is_named():
    """A1, planted: the English gains a marker, the Korean does not."""
    english = "# T\n\n## A\n\n<!-- specs/1790154762-x -->\nRule.\n"
    korean = "# T\n\n## 가\n\n규칙.\n"
    found = disagreements("d", english, korean)
    assert found == [
        "d: heading position 2 — the Korean edition lacks "
        "['1790154762-x'] and carries [] the English does not"
    ], found


def test_a_marker_under_a_different_heading_is_named():
    """The reason the check pairs per position and not per file: the same
    ids, one of them under another section."""
    english = "# T\n## A\n<!-- specs/1-a -->\n## B\n"
    korean = "# T\n## 가\n## 나\n<!-- specs/1-a -->\n"
    found = disagreements("d", english, korean)
    # Position 0 is the preamble and 1 the title, so `## A` is 2 and `## B` 3.
    assert len(found) == 2, found
    assert "position 2" in found[0] and "position 3" in found[1], found


def test_a_heading_added_to_one_edition_only_is_named():
    """A3, planted."""
    english = "# T\n## A\n## B\n"
    korean = "# T\n## 가\n"
    found = disagreements("d", english, korean)
    assert len(found) == 1 and "heading levels differ" in found[0], found


def test_a_hash_without_a_space_and_a_fenced_marker_are_not_read():
    """`#458 settled` is prose, and a marker inside a fence is a quotation —
    neither is part of the outline the fold would read."""
    english = "# T\n#458 settled it.\n```\n<!-- specs/1-a -->\n## not a heading\n```\n"
    korean = "# T\n"
    assert disagreements("d", english, korean) == []
