"""A folded statement names what enforces it — for folds from #520 on.

`skills/settle/SKILL.md` §2 gives a standing statement one shape: a bold rule
sentence, its grounds, and exactly one line `Enforced by: <target>[, …]` or
`Enforced by: nothing — <why>`. The plugin ships no checker for that shape;
this module is this repository's own.

**It binds only markers whose work-item id is at or above `SHAPE_CUTOFF`.**
The 101 statements folded before #520 carry no such line, and retrofitting
them is MichaelYcJo/SpecSeal#526's second item. Work-item ids are
epoch-prefixed, so the cutoff is a comparison and needs no list of
exemptions. `docs/the-evidence-ledger.md` states the value in prose, and
`tests/test_a_document_has_room_for_the_next_fold.py` pins the prose against
this constant.

What the check reads is presence, count and resolution: the bold opening, one
live `Enforced by:` line, and that every target names a file that exists and,
with `::name`, a `def` or `class` in it. It cannot read whether the target
really enforces the rule, or whether the statement is true.

Markers and live lines come from the fold's own reader,
`skills/verify/scripts/unverified_check.py#live_lines` and `#FOLD_MARKER`.
"""

import ast
import importlib.util
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(ROOT, "docs")
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")
SETTLE = os.path.join(ROOT, "skills", "settle", "SKILL.md")

SHAPE_CUTOFF = 1790154761

HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
BOLD_OPENING = re.compile(r"^\*{2,3}[^*\s]")
ENFORCED = "Enforced by: "
NOTHING = "nothing — "


def _reader():
    spec = importlib.util.spec_from_file_location("unverified_check", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uc = _reader()


def statements(text):
    """`[(marker ids, the statement's live lines)]`, in document order.

    Consecutive marker lines are one group. A statement runs from its markers
    to the next marker, the next heading or the end of the file."""
    found = []
    current = None
    previous_was_marker = False
    for line, live in uc.live_lines(text.splitlines()):
        if not live:
            previous_was_marker = False
            continue
        ids = uc.FOLD_MARKER.findall(line)
        if ids:
            if previous_was_marker:
                current[0].extend(ids)
            else:
                current = (list(ids), [])
                found.append(current)
            previous_was_marker = True
            continue
        previous_was_marker = False
        if HEADING.match(line):
            current = None
            continue
        if current is not None:
            current[1].append(line)
    return found


def bound(ids):
    """Whether any id in the group is at or above the cutoff."""
    for work_item in ids:
        prefix = work_item.split("-", 1)[0]
        if prefix.isdigit() and int(prefix) >= SHAPE_CUTOFF:
            return True
    return False


def target_problem(root, target):
    """Why `target` does not resolve under `root`, or None when it does."""
    target = target.strip().strip("`")
    if not target:
        return "an empty target"
    path, _, name = target.partition("::")
    # Both sides through `realpath`, so a symlink inside the root that opens
    # a file outside it is outside, and a root reached through one is itself.
    base = os.path.realpath(root)
    full = os.path.realpath(os.path.join(base, *path.split("/")))
    if os.path.commonpath([full, base]) != base:
        return f"{path} is not a path inside the repository"
    if not os.path.exists(full):
        return f"{path} does not exist"
    if not os.path.isfile(full):
        return f"{path} is not a file in the repository"
    if not name:
        return None
    if not path.endswith(".py"):
        return f"{target}: `::name` needs a Python file"
    with open(full, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    kinds = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    if any(isinstance(n, kinds) and n.name == name for n in ast.walk(tree)):
        return None
    return f"{target}: no def or class named {name} in {path}"


def shape_problems(root, name, text):
    """What is wrong with the shape of each bound statement in `text`."""
    problems = []
    for ids, lines in statements(text):
        if not bound(ids):
            continue
        where = f"{name}: the statement under {ids}"
        body = [line for line in lines if line.strip()]
        if not body or not BOLD_OPENING.match(body[0]):
            problems.append(f"{where} does not open with a bold rule sentence")
        enforced = [line for line in lines if line.startswith(ENFORCED)]
        if len(enforced) != 1:
            problems.append(
                f"{where} carries {len(enforced)} `Enforced by:` lines, not one"
            )
            continue
        value = enforced[0][len(ENFORCED) :].strip()
        if value.startswith(NOTHING.strip()):
            if not value[len(NOTHING.strip()) :].strip():
                problems.append(f"{where} says `nothing` and gives no reason")
            continue
        for target in value.split(","):
            problem = target_problem(root, target)
            if problem:
                problems.append(f"{where}: {problem}")
    return problems


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
