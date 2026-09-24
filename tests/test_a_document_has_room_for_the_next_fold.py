"""A document has room for the next fold, or it takes no new statement.

`skills/settle/SKILL.md` §2 places a folded rule in the document that owns its
subject, and says a document over the repository's ceiling takes no new
standing statement. The reader ships, as `skills/settle/scripts/fold_check.py`
(`fold-check`); this module is this repository's ceiling and its pin over it.

Two fold runs put 29 of the 101 folded statements into
`docs/review-chain-spec.md`, which reached 2,246 lines while the next largest
document was 839. Its fold-marker count was frozen until
MichaelYcJo/SpecSeal#526 split it along its own headings into three
documents, each under the ceiling, and the entry could not outlive the split:
once the file was back under the ceiling, the listing itself failed, which is
how the entry below came to be removed. The listing stays, empty, for the
next document a fold takes past the ceiling before it can be split.

The marker count is frozen, not the line count, because a marker is the one
thing only a fold adds. A sibling that edits a listed document's prose moves
its line count and folds nothing.

`docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*
states the three values in prose. The last case here pins that prose against
the constants below, `SHAPE_CUTOFF` included, which lives in
`tests/test_a_folded_statement_names_what_enforces_it.py`.
"""

import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "settle", "scripts", "fold_check.py")
SHAPE = os.path.join(
    os.path.dirname(__file__), "test_a_folded_statement_names_what_enforces_it.py"
)

LINE_CEILING = 1000
OVER_CEILING = {}
# WHICH markers each listed document holds, not only how many: a fold that
# adds a statement there and removes another keeps the count and changes this
# (round 1, finding 1). A marker removed on purpose recomputes it with
# `marker_digest` in the same commit that lowers the count.
FROZEN_IDS_DIGEST = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fold_check = _load("specseal_fold_check", SCRIPT)
markers = fold_check.markers
marker_digest = fold_check.marker_digest
documents = fold_check.documents
ceiling_problems = fold_check.ceiling_problems


def test_every_document_in_docs_is_under_the_ceiling_or_frozen():
    assert documents(ROOT), "no document under docs/ was read"
    problems = ceiling_problems(ROOT, LINE_CEILING, OVER_CEILING, FROZEN_IDS_DIGEST)
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


def test_a_marker_swapped_into_the_listed_document_is_named(tmp_path):
    """Round 1, finding 1: a fold that adds a statement to the listed document
    and removes another keeps the count and changes which markers it holds."""
    frozen = body(12, 2)
    swapped = "<!-- specs/1790154762-new -->\n" + body(11, 1)
    root = tree(tmp_path, {"big.md": swapped})
    found = ceiling_problems(root, 10, OVER, {"docs/big.md": marker_digest(frozen)})
    assert len(found) == 1 and "but not the ones frozen" in found[0], found


def test_the_frozen_digest_is_the_listed_document_s_markers():
    """Every listed document has a digest, and it is the one on disk."""
    assert set(FROZEN_IDS_DIGEST) == set(OVER_CEILING)
    for rel, digest in FROZEN_IDS_DIGEST.items():
        with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8") as f:
            assert marker_digest(f.read()) == digest, rel


def test_a_marker_removed_on_purpose_is_told_to_recompute_the_digest(tmp_path):
    """Round 2, finding 3: the count was lowered and the digest was not. The
    message may not report a swap as fact, and it names the recomputation."""
    frozen = body(12, 2)
    root = tree(tmp_path, {"big.md": body(12, 1)})
    found = ceiling_problems(
        root, 10, {"docs/big.md": (1, "#1")}, {"docs/big.md": marker_digest(frozen)}
    )
    assert len(found) == 1, found
    assert "set the digest to marker_digest() of the file" in found[0], found
    assert "keeps the count" not in found[0], found


def test_a_count_that_moved_is_told_to_recompute_the_digest_too(tmp_path):
    """The count message is the one a removal meets first."""
    root = tree(tmp_path, {"big.md": body(12, 1)})
    found = ceiling_problems(
        root, 10, OVER, {"docs/big.md": marker_digest(body(12, 2))}
    )
    assert len(found) == 1, found
    assert "recomputes FROZEN_IDS_DIGEST with marker_digest()" in found[0], found


# --- the command -------------------------------------------------------------


def command(*args):
    """`fold-check` as a person types it, run on this interpreter."""
    done = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return done.returncode, done.stdout, done.stderr


def test_the_command_names_a_document_over_the_ceiling_and_exits_1(tmp_path):
    """S3: the message the module pins, printed by the command, at exit 1."""
    root = tree(tmp_path, {"other.md": body(11), "small.md": body(10)})
    code, out, err = command("--root", root, "--ceiling", "10")
    assert code == 1, (code, out, err)
    assert (
        "docs/other.md is 11 lines, over the ceiling of 10. Split it along its "
        "own headings, or place the rule in the document for its own "
        "sub-subject\n"
    ) in out, out
    assert "held 2 documents under docs/ to 10 lines, 0 listed over it\n" in out


def test_the_command_refuses_a_ceiling_that_is_not_a_positive_integer(tmp_path):
    root = tree(tmp_path, {"small.md": body(3)})
    for value in ("0", "ten"):
        code, out, err = command("--root", root, "--ceiling", value)
        assert code == 2 and not out, (value, out, err)


def test_this_repository_is_under_the_ceiling_through_the_command():
    code, out, err = command("--root", ROOT, "--ceiling", str(LINE_CEILING))
    assert code == 0, (out, err)
