"""A document has room for the next fold, or it takes no new statement.

`skills/settle/SKILL.md` §2 places a folded rule in the document that owns its
subject, and says a document over the repository's ceiling takes no new
standing statement. This module is this repository's ceiling and its reader.

Two fold runs put 29 of the 101 folded statements into
`docs/review-chain-spec.md`, which is 2,159 lines, while the next largest
document is 839. Splitting it is MichaelYcJo/SpecSeal#526. Until then its
fold-marker count is frozen, and the entry cannot outlive the split: once the
file is back under the ceiling, the listing itself fails.

The marker count is frozen, not the line count, because a marker is the one
thing only a fold adds. A sibling that edits the chain spec's prose moves its
line count and folds nothing.

`docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*
states the three values in prose. The last case here pins that prose against
the constants below, `SHAPE_CUTOFF` included, which lives in
`tests/test_a_folded_statement_names_what_enforces_it.py`.
"""

import importlib.util
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")
SHAPE = os.path.join(
    os.path.dirname(__file__), "test_a_folded_statement_names_what_enforces_it.py"
)

LINE_CEILING = 1000
OVER_CEILING = {
    "docs/review-chain-spec.md": (29, "MichaelYcJo/SpecSeal#526"),
}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uc = _load("unverified_check", READER)


def markers(text):
    """How many fold markers the fold itself would read in `text`."""
    return sum(
        len(uc.FOLD_MARKER.findall(line))
        for line, live in uc.live_lines(text.splitlines())
        if live
    )


def documents(root):
    top = os.path.join(root, "docs")
    return [
        "docs/" + name
        for name in sorted(os.listdir(top))
        if name.endswith(".md") and os.path.isfile(os.path.join(top, name))
    ]


def ceiling_problems(root, ceiling, over):
    """Every way the tree at `root` breaks the ceiling or its listing."""
    problems = []
    names = documents(root)
    for rel in sorted(set(over) - set(names)):
        problems.append(f"{rel} is listed over the ceiling and does not exist")
    for rel in names:
        with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
            text = f.read()
        lines = len(text.splitlines())
        if rel not in over:
            if lines > ceiling:
                problems.append(
                    f"{rel} is {lines} lines, over the ceiling of {ceiling}. "
                    "Split it along its own headings, or place the rule in the "
                    "document for its own sub-subject"
                )
            continue
        frozen, home = over[rel]
        if lines <= ceiling:
            problems.append(
                f"{rel} is {lines} lines, no longer over the ceiling of "
                f"{ceiling}. Remove its entry; {home} was its home"
            )
        found = markers(text)
        if found != frozen:
            problems.append(
                f"{rel} carries {found} fold markers and is frozen at {frozen} "
                f"until {home} splits it. A new fold goes to the document for "
                "the rule's own sub-subject; a removed marker lowers the frozen "
                "count, so the room it made is not refilled"
            )
    return problems


def test_every_document_in_docs_is_under_the_ceiling_or_frozen():
    assert documents(ROOT), "no document under docs/ was read"
    problems = ceiling_problems(ROOT, LINE_CEILING, OVER_CEILING)
    assert not problems, "\n".join(problems)


def test_the_listed_document_still_holds_markers():
    """A frozen count of zero would freeze nothing; the reader has to have
    read the markers it freezes."""
    for rel, (frozen, _) in OVER_CEILING.items():
        with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8") as f:
            assert markers(f.read()) == frozen > 0, rel


# --- planted trees -----------------------------------------------------------


def tree(tmp_path, files):
    (tmp_path / "docs").mkdir()
    for name, text in files.items():
        (tmp_path / "docs" / name).write_text(text, encoding="utf-8")
    return str(tmp_path)


def body(lines, marker_count=0):
    text = [f"<!-- specs/1-m{i} -->" for i in range(marker_count)]
    text += ["prose"] * (lines - len(text))
    return "\n".join(text) + "\n"


OVER = {"docs/big.md": (2, "#1")}


def test_a_listed_document_at_its_frozen_count_passes(tmp_path):
    root = tree(tmp_path, {"big.md": body(12, 2), "small.md": body(10)})
    assert ceiling_problems(root, 10, OVER) == []


def test_a_fold_into_the_listed_document_is_named(tmp_path):
    """A8."""
    root = tree(tmp_path, {"big.md": body(12, 3)})
    found = ceiling_problems(root, 10, OVER)
    assert len(found) == 1, found
    assert "carries 3 fold markers and is frozen at 2 until #1" in found[0]


def test_a_marker_removed_from_the_listed_document_is_named(tmp_path):
    root = tree(tmp_path, {"big.md": body(12, 1)})
    found = ceiling_problems(root, 10, OVER)
    assert len(found) == 1 and "carries 1 fold markers" in found[0], found


def test_a_document_past_the_ceiling_outside_the_list_is_named(tmp_path):
    """A9."""
    root = tree(tmp_path, {"big.md": body(12, 2), "other.md": body(11)})
    found = ceiling_problems(root, 10, OVER)
    assert found == [
        "docs/other.md is 11 lines, over the ceiling of 10. Split it along its "
        "own headings, or place the rule in the document for its own "
        "sub-subject"
    ], found


def test_a_document_at_the_ceiling_is_not_over_it(tmp_path):
    root = tree(tmp_path, {"big.md": body(12, 2), "other.md": body(10)})
    assert ceiling_problems(root, 10, OVER) == []


def test_a_listed_document_back_under_the_ceiling_is_named(tmp_path):
    """A10: the entry cannot outlive the split."""
    root = tree(tmp_path, {"big.md": body(10, 2)})
    found = ceiling_problems(root, 10, OVER)
    assert len(found) == 1 and "no longer over the ceiling" in found[0], found


def test_a_listed_document_that_is_gone_is_named(tmp_path):
    root = tree(tmp_path, {"other.md": body(3)})
    found = ceiling_problems(root, 10, OVER)
    assert found == ["docs/big.md is listed over the ceiling and does not exist"]


def test_a_quoted_marker_is_not_counted(tmp_path):
    fenced = "```\n<!-- specs/1-q -->\n```\n"
    root = tree(tmp_path, {"big.md": body(12, 2) + fenced})
    assert ceiling_problems(root, 20, {"docs/big.md": (2, "#1")})[0].startswith(
        "docs/big.md is 15 lines, no longer over"
    )
    assert markers(fenced) == 0


# --- the prose that states the rule and the values ---------------------------


def test_settle_owns_the_placement_rule():
    """A11. The rule is settle's, in general form, and it sets no value."""
    with open(
        os.path.join(ROOT, "skills", "settle", "SKILL.md"), encoding="utf-8"
    ) as f:
        text = f.read()
    section = text.split("### 2. Write one standing statement per segment")[1]
    section = section.split("### 3.")[0]
    for phrase in (
        "**One subject, one document, and a document over its ceiling takes no new\n"
        "statement.**",
        "along the headings it already has",
        "The plugin sets\nno ceiling",
    ):
        assert phrase in section, f"settle §2 no longer says: {phrase!r}"


def test_the_evidence_ledger_states_the_values_these_constants_hold():
    """A11. The values are stated once in prose, for a reader, and held here,
    for the check; this case is what keeps the two the same numbers."""
    with open(
        os.path.join(ROOT, "docs", "the-evidence-ledger.md"), encoding="utf-8"
    ) as f:
        text = f.read()
    section = text.split("## The fold, and what tells it from a deletion")[1]
    assert (
        "`skills/settle/SKILL.md` §*2. Write one standing statement per\nsegment*"
        in section
    ), "the evidence ledger no longer links to settle §2, the rules' owner"
    cutoff = re.search(r"from work item `(\d+)` on", section)
    ceiling = re.search(r"at or under ([\d,]+) lines", section)
    listed = re.findall(
        r"`(docs/[^`]+)`,\s+frozen at (\d+) fold markers until (\S+#\d+)", section
    )
    shape = _load("shape_check", SHAPE)
    assert cutoff and int(cutoff.group(1)) == shape.SHAPE_CUTOFF, cutoff
    assert ceiling and int(ceiling.group(1).replace(",", "")) == LINE_CEILING, ceiling
    assert {rel: (int(n), home) for rel, n, home in listed} == OVER_CEILING, listed
