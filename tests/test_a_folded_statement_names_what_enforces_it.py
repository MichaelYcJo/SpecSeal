"""A folded statement names what enforces it — for folds from #520 on.

`skills/settle/SKILL.md` §2 gives a standing statement one shape: a bold rule
sentence, its grounds, and exactly one line `Enforced by: <target>[, …]` or
`Enforced by: nothing — <why>`. The reader ships, as
`skills/settle/scripts/fold_check.py` (`fold-check`); this module is this
repository's pin over it — the planted statements below call the shipped
functions, and the real-tree case runs them over this repository's `docs/`.

**It binds only markers whose work-item id is at or above `SHAPE_CUTOFF`.**
The statements folded before #520 carry no such line, and retrofitting them
is MichaelYcJo/SpecSeal#565. Work-item ids are epoch-prefixed, so the cutoff
is a comparison and needs no list of exemptions.
`docs/the-evidence-ledger.md` states the value in prose, and
`tests/test_a_document_has_room_for_the_next_fold.py` pins the prose against
this constant.

What the check reads is presence, count and resolution: the bold opening, one
live `Enforced by:` line, and that every target names a file that exists and,
with `::name`, a `def` or `class` in it. It cannot read whether the target
really enforces the rule, or whether the statement is true.
"""

import importlib.util
import os
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(ROOT, "docs")
SCRIPT = os.path.join(ROOT, "skills", "settle", "scripts", "fold_check.py")
SETTLE = os.path.join(ROOT, "skills", "settle", "SKILL.md")

SHAPE_CUTOFF = 1790154761


def _load():
    spec = importlib.util.spec_from_file_location("specseal_fold_check", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fold_check = _load()
statements = fold_check.statements
target_problem = fold_check.target_problem


def shape_problems(root, name, text, cutoff=SHAPE_CUTOFF):
    """The shipped check, at this repository's cutoff unless a case names one."""
    return fold_check.shape_problems(root, name, text, cutoff)


def docs_documents():
    return [
        name
        for name in sorted(os.listdir(DOCS))
        if name.endswith(".md") and os.path.isfile(os.path.join(DOCS, name))
    ]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# --- the real tree -----------------------------------------------------------


def test_every_bound_statement_in_docs_has_the_shape():
    """A7. The walk has to have read markers, so a broken reader cannot pass
    on an empty walk; the ones folded before the cutoff are read and skipped."""
    problems = []
    groups = 0
    for name in docs_documents():
        text = read(os.path.join(DOCS, name))
        groups += len(statements(text))
        problems += shape_problems(ROOT, "docs/" + name, text)
    assert groups, "no fold marker was read under docs/"
    assert not problems, "\n".join(problems)


def test_settle_owns_the_shape_rule():
    """A11. The rule is stated in the fold's procedure, the document the
    folder reads, and this module is only its reader here."""
    text = read(SETTLE)
    section = text.split("### 2. Write one standing statement per segment")[1]
    section = section.split("### 3.")[0]
    for phrase in (
        "**A standing statement has one shape: the rule, its grounds, and what "
        "enforces\nit.**",
        "Enforced by: nothing — <why>",
        "**Stacked markers share one statement.**",
        "It ships no checker for the shape",
        "it is review's to find",
    ):
        assert phrase in section, f"settle §2 no longer says: {phrase!r}"


# --- planted statements ------------------------------------------------------

BOUND = "<!-- specs/1790154762-a-later-fold -->"
OLD = "<!-- specs/1790154760-an-earlier-fold -->"


def planted(tmp_path, body, marker=BOUND):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_x.py").write_text(
        "def test_here():\n    pass\n\n\nclass Holder:\n    pass\n"
    )
    text = f"# D\n\n## S\n\n{marker}\n{body}"
    return shape_problems(str(tmp_path), "d.md", text)


def test_a_statement_with_the_shape_passes(tmp_path):
    body = "**Rule.** Grounds.\nEnforced by: tests/test_x.py::test_here\n"
    assert planted(tmp_path, body) == []


def test_several_targets_in_backticks_and_a_class_resolve(tmp_path):
    body = "**Rule.**\nEnforced by: `tests/test_x.py::Holder`, `tests/test_x.py`\n"
    assert planted(tmp_path, body) == []


def test_no_enforced_by_line_is_named(tmp_path):
    """A4."""
    found = planted(tmp_path, "**Rule.** Grounds.\n")
    assert found == [
        "d.md: the statement under ['1790154762-a-later-fold'] carries 0 "
        "`Enforced by:` lines, not one"
    ], found


def test_two_enforced_by_lines_are_named(tmp_path):
    """A4."""
    body = "**Rule.**\nEnforced by: tests/test_x.py\nEnforced by: tests/test_x.py\n"
    found = planted(tmp_path, body)
    assert len(found) == 1 and "carries 2" in found[0], found


def test_a_statement_that_does_not_open_bold_is_named(tmp_path):
    found = planted(tmp_path, "Rule.\nEnforced by: tests/test_x.py\n")
    assert len(found) == 1 and "bold rule sentence" in found[0], found


def test_a_missing_file_is_named(tmp_path):
    """A5."""
    found = planted(tmp_path, "**Rule.**\nEnforced by: tests/test_gone.py\n")
    assert len(found) == 1 and "tests/test_gone.py does not exist" in found[0]


def test_a_missing_name_is_named(tmp_path):
    """A5."""
    found = planted(tmp_path, "**Rule.**\nEnforced by: tests/test_x.py::test_gone\n")
    assert len(found) == 1 and "no def or class named test_gone" in found[0]


def test_nothing_with_a_reason_passes_and_without_one_fails(tmp_path):
    """A6."""
    body = "**Rule.**\nEnforced by: nothing — only a reader can tell\n"
    assert planted(tmp_path, body) == []
    found = shape_problems(
        str(tmp_path), "d.md", f"{BOUND}\n**Rule.**\nEnforced by: nothing — \n"
    )
    assert len(found) == 1 and "gives no reason" in found[0], found


def test_a_statement_folded_before_the_cutoff_is_not_bound(tmp_path):
    assert planted(tmp_path, "Rule, with no line.\n", marker=OLD) == []


def test_stacked_markers_share_one_statement_and_one_bound_id_binds_it(tmp_path):
    """The bound marker is on top, so read as a group of its own it would have
    no statement at all, and the case would name it."""
    body = "**Rule.**\nEnforced by: tests/test_x.py\n"
    assert planted(tmp_path, body, marker=f"{BOUND}\n{OLD}") == []
    (tmp_path / "x").mkdir()
    found = planted(tmp_path / "x", "Rule.\n", marker=f"{OLD}\n{BOUND}")
    assert len(found) == 2, found


def test_a_statement_ends_at_the_next_heading(tmp_path):
    """The line after a heading belongs to no statement, so a later section's
    `Enforced by:` does not satisfy an earlier one."""
    body = "**Rule.**\n\n## Next\n\nEnforced by: tests/test_x.py\n"
    found = planted(tmp_path, body)
    assert len(found) == 1 and "carries 0" in found[0], found


def test_a_quoted_example_in_a_fence_is_not_a_statement(tmp_path):
    body = "```\n" + BOUND + "\nRule.\n```\n"
    text = f"# D\n\n{body}"
    assert shape_problems(str(tmp_path), "d.md", text) == []


def test_a_target_that_is_not_a_file_in_the_repository_is_named(tmp_path):
    """Round 1, finding 2: the root, a directory and a path outside the root
    all exist, and none of them is a file the repository holds."""
    (tmp_path / "outside.txt").write_text("x")
    for i, target in enumerate((".", "tests", "../outside.txt", "tests/../..")):
        sub = tmp_path / f"t{i}"
        sub.mkdir()
        found = planted(sub, f"**Rule.**\nEnforced by: {target}\n")
        assert len(found) == 1 and "repository" in found[0], (target, found)


def test_a_bare_bold_delimiter_is_not_a_rule_sentence(tmp_path):
    """Round 1, correction: a first line of `**` alone opens nothing."""
    found = planted(tmp_path, "**\nEnforced by: nothing — r\n")
    assert len(found) == 1 and "bold rule sentence" in found[0], found


def test_a_rule_sentence_in_bold_italics_opens_bold(tmp_path):
    """Round 2, correction: `***Rule.***` is bold, and `***` alone is not."""
    body = "***Rule.***\nEnforced by: nothing — r\n"
    assert planted(tmp_path, body) == []
    (tmp_path / "x").mkdir()
    assert len(planted(tmp_path / "x", "***\nEnforced by: nothing — r\n")) == 1


def test_a_heading_with_a_tab_or_no_text_ends_a_statement(tmp_path):
    """Round 2, correction: `##<tab>Next` and a bare `##` are headings."""
    for i, heading in enumerate(("##\tNext", "##")):
        sub = tmp_path / f"h{i}"
        sub.mkdir()
        found = planted(sub, f"**Rule.**\n{heading}\nEnforced by: tests/test_x.py\n")
        assert len(found) == 1 and "carries 0" in found[0], (heading, found)


def test_a_symlink_inside_the_root_that_leaves_it_is_named(tmp_path):
    """Round 2, correction: the path is inside, and the file it opens is not."""
    from conftest import symlink_or_skip

    (tmp_path / "outside.txt").write_text("x")
    sub = tmp_path / "repo"
    sub.mkdir()
    (sub / "docs").mkdir()
    symlink_or_skip(str(tmp_path / "outside.txt"), str(sub / "docs" / "link.txt"))
    found = planted(sub, "**Rule.**\nEnforced by: docs/link.txt\n")
    assert len(found) == 1 and "inside the repository" in found[0], found


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


def planted_docs(tmp_path, body, marker=BOUND):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "d.md").write_text(
        f"# D\n\n## S\n\n{marker}\n{body}", encoding="utf-8"
    )
    return str(tmp_path)


def test_the_command_names_a_bound_statement_with_no_line_and_exits_1(tmp_path):
    """S2: the problem the module pins, printed by the command, at exit 1."""
    root = planted_docs(tmp_path, "**Rule.** Grounds.\n")
    code, out, err = command("--root", root, "--shape-from", str(SHAPE_CUTOFF))
    assert code == 1, (code, out, err)
    assert (
        "docs/d.md: the statement under ['1790154762-a-later-fold'] carries 0 "
        "`Enforced by:` lines, not one\n"
    ) in out, out
    assert (
        f"read 1 statement in 1 document under docs/; the cutoff {SHAPE_CUTOFF} "
        "binds 1\n"
    ) in out, out


def test_the_command_exits_0_over_a_statement_with_the_shape(tmp_path):
    root = planted_docs(tmp_path, "**Rule.**\nEnforced by: nothing — a reader\n")
    code, out, err = command("--root", root, "--shape-from", str(SHAPE_CUTOFF))
    assert code == 0, (code, out, err)
    assert "no ceiling is declared, so no document's length was checked" in out


def test_shape_from_0_binds_a_statement_folded_before_any_cutoff(tmp_path):
    """S6: the worklist #565 runs — every statement is bound, the old one too."""
    root = planted_docs(tmp_path, "Rule, with no line.\n", marker=OLD)
    code, out, _ = command("--root", root, "--shape-from", str(SHAPE_CUTOFF))
    assert code == 0, out
    code, out, _ = command("--root", root, "--shape-from", "0")
    assert code == 1, out
    assert "['1790154760-an-earlier-fold'] carries 0 `Enforced by:` lines" in out


def test_the_command_exits_2_with_nothing_checked_on_an_unusable_root(tmp_path):
    code, _, err = command("--root", str(tmp_path / "gone"), "--shape-from", "0")
    assert code == 2 and "is not a directory — nothing was checked" in err, err
    code, _, err = command("--root", str(tmp_path), "--shape-from", "0")
    assert code == 2 and "has no docs/ directory — nothing was checked" in err, err


def test_this_repository_has_the_shape_through_the_command():
    """S1 at this phase: the flags this repository's values would give."""
    code, out, err = command("--root", ROOT, "--shape-from", str(SHAPE_CUTOFF))
    assert code == 0, (out, err)
