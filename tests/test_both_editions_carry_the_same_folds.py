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

A folded statement's `Enforced by:` line is language-neutral too, in the
part a checker reads: the field, its targets, and the word `nothing`
(`skills/settle/SKILL.md` §2). So each statement is paired with the one under
the same markers at the same heading position of the other edition, and the
two lines must name the same targets, or `nothing` in both. The reason after
`nothing — ` is prose, written in each edition's language, and is not
compared (#565).

Markers are read with the fold's own reader —
`skills/verify/scripts/unverified_check.py#live_lines` and `#FOLD_MARKER` —
so a marker this counts is exactly one the fold would count
(`docs/the-evidence-ledger.md` §*The fold, and what tells it from a
deletion*: one function decides what live means). A heading is a live line
matching `^ {0,3}#{1,6}` followed by a space, a tab or the end of the line
(CommonMark allows up to three spaces of indentation). A digit straight
after the hashes is prose, and each edition has a line that begins
`#<number>`.
"""

import collections
import importlib.util
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
DOCS = os.path.join(ROOT, "docs")
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")
# The shape's own reader, for where a statement's span ends and which
# `Enforced by:` value is read as targets rather than as `nothing — <why>`.
FOLD_CHECK = os.path.join(ROOT, "skills", "settle", "scripts", "fold_check.py")

HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]|$)")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uc = _load(READER, "unverified_check")
fc = _load(FOLD_CHECK, "fold_check_for_the_editions")


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


def enforcement(text):
    """`{(heading position, marker ids): [each statement's enforcement]}`.

    A statement's enforcement is what its `Enforced by:` lines name, in the
    part a checker reads literally: the targets, split on the comma and
    stripped of code-span backticks, or the word `nothing` alone. The reason
    after `nothing — ` is prose in each edition's own language
    (`skills/settle/SKILL.md` §2), so it is not compared. A statement with no
    line has an empty enforcement. The position is the one `outline` gives,
    so a statement is paired with the statement under the same markers at the
    same heading position of the other edition."""
    lines = text.splitlines()
    position_at, position = [], 0
    for line, live in uc.live_lines(lines):
        if live and HEADING.match(line):
            position += 1
        position_at.append(position)
    found = collections.defaultdict(list)
    for ids, body in fc.numbered_statements(text):
        if not body:
            continue
        named = []
        for _number, line in body:
            if not line.startswith(fc.ENFORCED):
                continue
            value = line[len(fc.ENFORCED) :].strip()
            if fc.names_targets(value):
                named.append(tuple(t.strip().strip("`") for t in value.split(",")))
            else:
                named.append(("nothing",))
        found[(position_at[body[0][0] - 1], tuple(ids))].append(tuple(named))
    return found


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
    # Only statements both editions hold under the same markers are paired:
    # a marker one edition lacks is already named above.
    en_named, ko_named = enforcement(english), enforcement(korean)
    for key in sorted(set(en_named) & set(ko_named)):
        if en_named[key] == ko_named[key]:
            continue
        position, ids = key
        found.append(
            f"{name}: heading position {position}, the statement under "
            f"{list(ids)} — the English edition's `Enforced by:` names "
            f"{en_named[key]} and the Korean edition's names {ko_named[key]}"
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


def test_an_enforced_by_line_naming_other_targets_is_named():
    """S7, planted: the same statement under the same marker, and the Korean
    edition's line names another target."""
    english = "# T\n## A\n<!-- specs/1-a -->\n**Rule.**\nEnforced by: tests/a.py::x\n"
    korean = "# T\n## 가\n<!-- specs/1-a -->\n**규칙.**\nEnforced by: tests/b.py::x\n"
    found = disagreements("d", english, korean)
    assert len(found) == 1, found
    assert "heading position 2" in found[0] and "1-a" in found[0], found
    assert "tests/a.py::x" in found[0] and "tests/b.py::x" in found[0], found


def test_an_enforced_by_line_one_edition_lacks_is_named():
    """S7, planted: a line written into the English edition only."""
    english = "# T\n## A\n<!-- specs/1-a -->\n**Rule.**\nEnforced by: tests/a.py\n"
    korean = "# T\n## 가\n<!-- specs/1-a -->\n**규칙.**\n"
    found = disagreements("d", english, korean)
    assert len(found) == 1 and "tests/a.py" in found[0], found


def test_the_reason_after_nothing_is_each_editions_own_prose():
    """The field and the word `nothing` are read literally in both editions;
    the reason after them is written in the edition's language, so two
    reasons in two languages are one enforcement. `nothing` in one edition
    against targets in the other is not."""
    english = (
        "# T\n## A\n<!-- specs/1-a -->\n**Rule.**\n"
        "Enforced by: nothing — no case reads it yet\n"
    )
    korean = (
        "# T\n## 가\n<!-- specs/1-a -->\n**규칙.**\n"
        "Enforced by: nothing — 아직 읽는 케이스가 없습니다\n"
    )
    assert disagreements("d", english, korean) == []
    targets = korean.replace("nothing — 아직 읽는 케이스가 없습니다", "tests/a.py")
    found = disagreements("d", english, targets)
    assert len(found) == 1 and "nothing" in found[0], found


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


def test_a_heading_indented_up_to_three_spaces_is_read():
    """Round 1, correction: CommonMark reads `   ## A` as a heading, and four
    spaces as an indented code block."""
    assert "heading levels differ" in disagreements("d", "# T\n   ## A\n", "# T\n")[0]
    assert disagreements("d", "# T\n    ## code\n", "# T\n") == []


def test_a_heading_with_a_tab_or_no_text_is_read():
    """Round 2, correction: CommonMark ends the hashes at a space, a tab or
    the end of the line."""
    for heading in ("##\tA", "##"):
        found = disagreements("d", f"# T\n{heading}\n", "# T\n")
        assert found and "heading levels differ" in found[0], heading
