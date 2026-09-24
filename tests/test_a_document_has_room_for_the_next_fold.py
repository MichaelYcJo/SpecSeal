"""A document has room for the next fold, or it takes no new statement.

`skills/settle/SKILL.md` §2 places a folded rule in the document that owns its
subject, and says a document over the repository's ceiling takes no new
standing statement. The reader ships, as `skills/settle/scripts/fold_check.py`
(`fold-check`); this module is this repository's ceiling and its pin over it.

Two fold runs put 29 folded statements into
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

The three values are rows of `seal/config.md` — `Fold shape from`,
`Document line ceiling`, `Over the ceiling` — which is where the shipped
command reads them. `docs/the-evidence-ledger.md` §*The fold, and what tells
it from a deletion* states them in prose, and the prose pin below reads the
rows through the command's own reader and holds the two equal, so the prose,
the config and the check are one set of numbers.
"""

import importlib.util
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "settle", "scripts", "fold_check.py")


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


def declared():
    """`(cutoff, ceiling, over, digests)` as this repository's
    `seal/config.md` states them, read by the shipped command's own reader.

    `over` holds WHICH markers each listed document holds through its digest,
    not only how many: a fold that adds a statement there and removes another
    keeps the count and changes the digest (round 1, finding 1)."""
    return fold_check.declared(fold_check.seal_home(ROOT))


def test_every_document_in_docs_is_under_the_ceiling_or_frozen():
    _, ceiling, over, digests = declared()
    assert ceiling, "this repository's seal/config.md declares no ceiling"
    assert documents(ROOT), "no document under docs/ was read"
    problems = ceiling_problems(ROOT, ceiling, over, digests)
    assert not problems, "\n".join(problems)


def test_the_listed_document_still_holds_markers():
    """A frozen count of zero would freeze nothing; the reader has to have
    read the markers it freezes."""
    for rel, (frozen, _) in declared()[2].items():
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


def ledger_prose():
    with open(
        os.path.join(ROOT, "docs", "the-evidence-ledger.md"), encoding="utf-8"
    ) as f:
        return f.read()


def prose_disagreements(text, values):
    """How the evidence-ledger prose and the declared values differ, or []."""
    cutoff, ceiling, over, _ = values
    section = text.split("## The fold, and what tells it from a deletion")[1]
    stated_cutoff = re.search(r"from work item `(\d+)` on", section)
    stated_ceiling = re.search(r"at or under ([\d,]+) lines", section)
    listed = re.findall(
        r"`(docs/[^`]+)`,\s+frozen at (\d+) fold markers until (\S+#\d+)", section
    )
    found = []
    if not stated_cutoff or int(stated_cutoff.group(1)) != cutoff:
        found.append(f"the prose states the cutoff {stated_cutoff}, the row {cutoff}")
    if not stated_ceiling or int(stated_ceiling.group(1).replace(",", "")) != ceiling:
        found.append(
            f"the prose states the ceiling {stated_ceiling}, the row {ceiling}"
        )
    if {rel: (int(n), home) for rel, n, home in listed} != over:
        found.append(f"the prose lists {listed}, the row {over}")
    return found


def test_the_evidence_ledger_states_the_values_the_config_rows_hold():
    """A11 and S10. The values are stated once in prose, for a reader, and
    once as `seal/config.md` rows, for the command; this case is what keeps
    the two the same numbers. The rows are read by the command's own reader,
    so a row it would not read fails here too."""
    text = ledger_prose()
    section = text.split("## The fold, and what tells it from a deletion")[1]
    assert (
        "`skills/settle/SKILL.md` §*2. Write one standing statement per\nsegment*"
        in section
    ), "the evidence ledger no longer links to settle §2, the rules' owner"
    assert not prose_disagreements(text, declared()), prose_disagreements(
        text, declared()
    )


def test_the_prose_pin_fails_when_either_side_moves_alone():
    """S10, from both sides: the rows edited with the prose left alone, and
    the prose edited with the rows left alone."""
    text, values = ledger_prose(), declared()
    cutoff, ceiling, over, digests = values
    assert prose_disagreements(text, (cutoff + 1, ceiling, over, digests))
    assert prose_disagreements(text, (cutoff, ceiling + 1, over, digests))
    listed = {"docs/big.md": (29, "owner/repo#1")}
    assert prose_disagreements(text, (cutoff, ceiling, listed, digests))
    edited = text.replace(f"from work item `{cutoff}` on", "from work item `1` on")
    assert edited != text, "the prose no longer states the cutoff this way"
    assert prose_disagreements(edited, values)
    edited = text.replace(f"at or under {ceiling:,} lines", "at or under 1 lines")
    edited = edited.replace(f"at or under {ceiling} lines", "at or under 1 lines")
    assert edited != text, "the prose no longer states the ceiling this way"
    assert prose_disagreements(edited, values)


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
    _, _, over, digests = declared()
    assert set(digests) == set(over)
    for rel, digest in digests.items():
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
    assert (
        f"set the entry's digest to {marker_digest(body(12, 1))}, the file's "
        "marker_digest() now, in the commit that lowered the count"
    ) in found[0], found
    assert "keeps the count" not in found[0], found


def test_a_count_that_moved_is_told_to_recompute_the_digest_too(tmp_path):
    """The count message is the one a removal meets first."""
    root = tree(tmp_path, {"big.md": body(12, 1)})
    found = ceiling_problems(
        root, 10, OVER, {"docs/big.md": marker_digest(body(12, 2))}
    )
    assert len(found) == 1, found
    assert (
        "sets the entry's digest in the `Over the ceiling` row to "
        f"{marker_digest(body(12, 1))}, the file's marker_digest() now"
    ) in found[0], found


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


def test_this_repository_passes_the_command_with_no_flags():
    """S1: the values come from `seal/config.md`, and both checks run."""
    code, out, err = command("--root", ROOT)
    assert code == 0, (out, err)
    cutoff, ceiling, _, _ = declared()
    assert f"; the cutoff {cutoff} binds " in out, out
    assert f" to {ceiling} lines, 0 listed over it\n" in out, out


def config_root(tmp_path, rows):
    """A planted repository whose `seal/config.md` carries `rows` under the
    table header, with one short document under `docs/`."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "seal").mkdir()
    table = "".join(f"| {item} | {value} |\n" for item, value in rows)
    (tmp_path / "seal" / "config.md").write_text(
        f"# Repository config\n\n| Item | Value |\n|---|---|\n{table}",
        encoding="utf-8",
    )
    return str(tmp_path)


def test_a_root_that_declares_neither_value_checks_nothing_and_says_so(tmp_path):
    """S4. Absent means not declared, as every optional row does; the line
    names both rows and the file they were looked for in (§14)."""
    root = config_root(tmp_path, [("Mode", "shared")])
    code, out, err = command("--root", root)
    config = os.path.join(root, "seal", "config.md")
    assert code == 0, (out, err)
    assert out == (
        "fold-check: neither `Fold shape from` nor `Document line ceiling` is "
        f"declared in {config}, so nothing was checked\n"
    ), out


def test_a_row_with_an_empty_value_is_not_declared(tmp_path):
    """The template writes a row it leaves open with an empty cell, as it does
    `Mode` and `Broad gate`; an empty cell is no value, not a bad one."""
    root = config_root(tmp_path, [("Fold shape from", ""), ("Over the ceiling", "")])
    code, out, err = command("--root", root)
    assert code == 0, (out, err)
    assert "neither `Fold shape from` nor `Document line ceiling` is declared" in out


def test_one_absent_row_skips_its_check_and_says_which(tmp_path):
    root = config_root(tmp_path, [("Document line ceiling", "10")])
    code, out, _ = command("--root", root)
    config = os.path.join(root, "seal", "config.md")
    assert code == 0, out
    assert (
        f"fold-check: `Fold shape from` is not declared in {config}, so the "
        "shape was not checked\n"
    ) in out, out
    assert "held 1 document under docs/ to 10 lines, 0 listed over it\n" in out


@pytest.mark.parametrize(
    "row, value, says",
    [
        (
            "Fold shape from",
            "17x",
            "the `Fold shape from` row holds `17x`, which is not a work-item "
            "id's epoch prefix (a whole number; `0` binds every statement)",
        ),
        (
            "Document line ceiling",
            "ten",
            "the `Document line ceiling` row holds `ten`, which is not a "
            "positive whole number of lines",
        ),
        (
            "Over the ceiling",
            "docs/a.md frozen at some markers",
            "the `Over the ceiling` row holds `docs/a.md frozen at some markers`, "
            "which is not `none` and not an entry `<path> frozen at <n> markers "
            "<12-hex digest> until <home>`",
        ),
    ],
)
def test_a_row_that_will_not_parse_is_named_and_nothing_is_checked(
    tmp_path, row, value, says
):
    """S5, one case per row, each message pinned (§14)."""
    root = config_root(tmp_path, [(row, value)])
    code, out, err = command("--root", root)
    config = os.path.join(root, "seal", "config.md")
    assert code == 2 and not out, (out, err)
    assert err == f"fold-check: in {config}, {says} — nothing was checked\n", err


def test_an_over_the_ceiling_entry_is_read_with_its_digest(tmp_path):
    """The entry shape `spec.md` fixes, read into the listing the check uses."""
    over, digests = fold_check.parse_over(
        "docs/big.md frozen at 29 markers 0123456789ab until owner/repo#1; "
        "docs/b.md frozen at 2 markers aaaaaaaaaaaa until #7"
    )
    assert over == {"docs/big.md": (29, "owner/repo#1"), "docs/b.md": (2, "#7")}
    assert digests == {"docs/big.md": "0123456789ab", "docs/b.md": "aaaaaaaaaaaa"}
    assert fold_check.parse_over("none") == ({}, {})
    assert fold_check.parse_over(None) == ({}, {})


def test_a_flag_overrides_its_row_for_one_run(tmp_path):
    root = config_root(tmp_path, [("Document line ceiling", "10")])
    (tmp_path / "docs" / "long.md").write_text("x\n" * 11, encoding="utf-8")
    code, out, _ = command("--root", root)
    assert code == 1 and "docs/long.md is 11 lines" in out, out
    code, out, _ = command("--root", root, "--ceiling", "11")
    assert code == 0, out
    assert (tmp_path / "seal" / "config.md").read_text(encoding="utf-8").count(
        "| Document line ceiling | 10 |"
    ) == 1
