"""Every act addressed to the orchestrator names what delivers it.

Issue #330. A rule that reaches an agent is delivered by mechanism -- the
`skills:` frontmatter, injected at startup with nothing typed and no path to
resolve. A rule that reaches the orchestrator is a sentence it has to
remember, because the orchestrator has no spawn for a preload to attach to.
The ticket asked, among other things, whether the orchestrator's acts should
be enumerated anywhere at all, and set its own condition: *unless something
reads it*. This module is what reads it.

The table lives in `skills/implement/orchestration.md` under
`## Orchestrator: which of these acts runs itself`, and this holds it against
both orchestration files **from both sides**: an act with no row fails, and a
row naming an act no file carries fails. One-sided is the state
`broad_gate.PARTITION` was written to end one subject over -- that list went
three releases at five entries while the workflow it mirrored went to
thirteen steps, and no case went red for it.

**The row set is mechanical**: every `##` heading whose text begins
`Orchestrator:` in either file, plus every `###` heading directly beneath
one. The section holding the table is itself such a heading, so it has a row
of its own, which is the shape the frame anticipated.

**The headings are read through the parser that already reads them.**
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#headings`
tracks fences and both levels, and its docstring records that a `##`-only
reader came out short. Importing it rather than writing a second reader is
the whole reason that function was widened: two parsers of one marker is how
half of them keep the old answer.

What this does not catch, stated rather than left to be found: an act written
for the orchestrator under a heading carrying no `Orchestrator:` prefix has
no row here and nothing notices. The check reads the marker, not the meaning
-- the same limit its neighbour states for itself. The mitigation is that the
marker is already load-bearing for a different reason, so a heading without
it costs something immediately and visibly.

Red-first, per the contract's §15. Each case below builds a temp root with
one defect in it and asserts the finding names that defect.

**Eight planted trees carry a defect, and all eight are listed.** A list
short of the tree is the defect this module exists to catch one file over,
so it says what it is a list OF: the first five are `plan.md`'s four red
directions plus the one round 1's finding 3 added, and the last three are
cases beyond what the frame asked for. Every name is written whole on its
own line, because the name this block used to carry was split across a line
break and a single-line search could not find it — which is how it went two
rounds naming a case that is in no file.

  `test_an_act_with_no_row_is_named`
      a marked heading the table does not carry
  `test_a_row_naming_no_heading_is_named`
      a row naming a heading no file carries
  `test_a_named_command_must_exist`
      a row naming a command that is in neither tree
  `test_a_named_path_is_resolved_against_the_tree_under_check`
      a row naming a path the tree under check lacks and the repository has
  `test_a_sentence_row_carries_grounds`
      `still a sentence` with an empty `Grounds` cell
  `test_a_value_outside_the_four_is_named`
      a `Delivered by` spelling that is none of the four values
  `test_a_top_level_act_cannot_be_part_of_a_parent`
      `part of its parent's act` on a `##`, which has no parent
  `test_a_missing_table_is_named_rather_than_read_as_empty`
      no table at all, which would otherwise report zero rows

**Two more planted trees carry no defect and are the floor beneath those
eight** — `test_a_clean_planted_tree_is_clean`, the same tree without the
defect, and
`test_a_third_level_heading_under_an_unmarked_section_is_not_an_act`. A
direction proves nothing while the floor under it is green for the wrong
reason, which is what round 1's finding 3 measured: `_delivery` resolved a
named path against this repository instead of against the tree it was given,
so the floor was clean because the check never asked the planted tree
anything.

The case that asserts the check can fail against the REAL tree is
`test_every_orchestrator_act_names_its_delivery` itself.
"""

import importlib.util
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NEIGHBOUR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "test_a_section_marked_for_one_role_reaches_only_that_role.py",
)

FILES = (
    "skills/implement/orchestration.md",
    "skills/code-review/orchestration.md",
)
# Where the table is. It is one of the two files above, which is what makes
# its own section a row.
TABLE_FILE = "skills/implement/orchestration.md"
HEADER = "| Act | File | Delivered by | Grounds |"

MARKER = "Orchestrator:"
PART = "part of its parent's act"
SENTENCE = "still a sentence"
NAMED = ("command", "check")


def _reader():
    """The neighbour's heading parser, loaded by path.

    Imported rather than copied: `headings` is the one reading of the
    `Orchestrator:` marker this repository has, and the neighbour's docstring
    holds the fence reasoning behind it.
    """
    spec = importlib.util.spec_from_file_location("marker_reader_for_acts", NEIGHBOUR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def _bare(cell):
    """A table cell with its backticks taken off."""
    return cell.strip().strip("`").strip()


def acts(root):
    """`(file, heading text, level)` for every act addressed to the
    orchestrator, in document order, over both orchestration files.

    A `##` whose text begins with the marker is an act. A `###` is an act
    when the `##` above it was one -- *directly beneath* means the nearest
    `##` and not the nearest marked one, so a `###` under an unmarked
    section is not swept in by a marked section further up the file.
    """
    reader = _reader()
    found = []
    for rel in FILES:
        path = os.path.join(root, *rel.split("/"))
        if not os.path.isfile(path):
            continue
        under_marked = False
        for level, title, _line in reader.headings(_read(path)):
            if level == 2:
                under_marked = title.startswith(MARKER)
                if under_marked:
                    found.append((rel, title, level))
            elif level == 3 and under_marked:
                found.append((rel, title, level))
    return found


def rows(root):
    """`(act, file, delivered by, grounds)` for every row of the table, plus
    the rows the header line could not be found for.

    Returns `(parsed, error)`: `error` is a sentence when the table itself is
    missing or malformed, and `None` otherwise.
    """
    path = os.path.join(root, *TABLE_FILE.split("/"))
    if not os.path.isfile(path):
        return [], f"{TABLE_FILE} does not exist, so the table cannot be read"
    lines = _read(path).splitlines()
    start = None
    for number, line in enumerate(lines):
        if line.strip() == HEADER:
            start = number
            break
    if start is None:
        return [], (
            f"{TABLE_FILE} carries no `{HEADER}` header line, so the "
            f"orchestrator's acts are enumerated nowhere"
        )
    parsed = []
    # `start + 1` is the `|---|` separator; the rows follow it and end at the
    # first line that is not a table row.
    for line in lines[start + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        parsed.append(cells)
    return parsed, None


def findings(root):
    """One line per defect, each naming the row or the act. Empty on a clean
    tree."""
    out = []
    parsed, error = rows(root)
    if error:
        return [error]
    known = {(rel, title): level for rel, title, level in acts(root)}
    seen = {}
    for cells in parsed:
        if len(cells) != 4:
            out.append(
                f"a row has {len(cells)} cells and the table has four "
                f"columns: {' | '.join(cells)}"
            )
            continue
        act, rel, delivered, grounds = cells
        rel = _bare(rel)
        key = (rel, act)
        if key in seen:
            out.append(
                f"`{act}` in `{rel}` has more than one row, and an act "
                f"answers with one delivery"
            )
        seen[key] = delivered
        if key not in known:
            out.append(
                f"a row names `{act}` in `{rel}`, and no heading of that "
                f"text is marked for the orchestrator there -- a rename "
                f"left the row behind"
            )
            continue
        out += _delivery(root, act, rel, known[key], delivered, grounds)
    for rel, title, _level in acts(root):
        if (rel, title) not in seen:
            out.append(
                f"`{title}` in `{rel}` is an act addressed to the "
                f"orchestrator and the table has no row for it"
            )
    return out


def _delivery(root, act, rel, level, delivered, grounds):
    """The `Delivered by` cell's own defects, as lines.

    **Paths resolve against `root` — the tree `findings` was given — and never
    against this module's own repository.** Round 1's finding: resolving
    against `ROOT` makes a planted tree green for files it does not carry, so
    the floor case under all four red directions held by leak rather than by
    being clean, and `test_a_named_command_must_exist` demonstrated *a path
    absent from the repository is named* where `findings(root)`'s own contract
    says *absent from the tree under check*. The real-tree case was unaffected,
    because there the two are one directory — which is exactly why nothing
    shipped was wrong and nothing went red.
    """
    if delivered == PART:
        if level == 2:
            return [
                f"`{act}` in `{rel}` reads `{PART}` and is a `##` heading, "
                f"which has no parent act to be part of"
            ]
        return []
    if delivered == SENTENCE:
        if not grounds:
            return [
                f"`{act}` in `{rel}` reads `{SENTENCE}` with an empty "
                f"`Grounds` cell -- the grounds are what say the tree was "
                f"looked at and came back empty"
            ]
        return []
    kind, _, named = delivered.partition(":")
    if kind not in NAMED or not _:
        return [
            f"`{act}` in `{rel}` reads `{delivered}`, which is none of the "
            f"four values: `command: <path>`, `check: <path>`, `{PART}`, "
            f"`{SENTENCE}`"
        ]
    path = _bare(named)
    if not path:
        return [f"`{act}` in `{rel}` reads `{kind}:` and names nothing"]
    if not os.path.exists(os.path.join(root, *path.split("/"))):
        return [
            f"`{act}` in `{rel}` names the {kind} `{path}`, and the tree has "
            f"no such file -- a row naming a {kind} that does not exist "
            f"reads as delivered"
        ]
    return []


# --- planted trees ------------------------------------------------------------

ACT = "Orchestrator: an act"
PLANTED = [
    (ACT, "skills/implement/orchestration.md", "still a sentence", "Nothing reads it."),
]


def _tree(base, extra_acts=(), table=None):
    """A root with both orchestration files and the table in the first.

    `extra_acts` are marked `##` headings added to the code-review file;
    `table` replaces `PLANTED` as the row set.
    """
    rows_text = "\n".join(
        f"| {a} | `{f}` | {d} | {g} |"
        for a, f, d, g in (PLANTED if table is None else table)
    )
    body = (
        f"# implement\n\n## {ACT}\n\nProse.\n\n"
        f"## Orchestrator: which of these acts runs itself\n\n"
        f"{HEADER}\n|---|---|---|---|\n{rows_text}\n\nProse after.\n"
    )
    other = "# code-review\n\n" + "".join(f"## {a}\n\nProse.\n\n" for a in extra_acts)
    # The check `SELF`'s row names, so the planted tree CARRIES what its own
    # table claims. Without it the floor case was green because `_delivery`
    # resolved against the repository, and every direction below was red over
    # a tree that was itself dirty in a way nothing said (round 1, finding 3).
    files = {
        "skills/implement/orchestration.md": body,
        "skills/code-review/orchestration.md": other,
        "tests/test_every_orchestrator_act_names_its_delivery.py": (
            "# the check `SELF`'s row names, so the tree carries it\n"
        ),
    }
    for rel, text in files.items():
        path = os.path.join(base, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    return str(base)


SELF = (
    "Orchestrator: which of these acts runs itself",
    "skills/implement/orchestration.md",
    "check: `tests/test_every_orchestrator_act_names_its_delivery.py`",
    "This module.",
)


def test_a_clean_planted_tree_is_clean(tmp_path):
    """The floor under the four directions below: each of them plants one
    defect into THIS tree, so a tree that is already dirty would prove
    nothing about the defect."""
    root = _tree(tmp_path, table=[PLANTED[0], SELF])
    assert findings(root) == []


def test_an_act_with_no_row_is_named(tmp_path):
    """A1, red-first: a marked heading the table does not carry."""
    root = _tree(
        tmp_path, extra_acts=("Orchestrator: a second act",), table=[PLANTED[0], SELF]
    )
    found = findings(root)
    assert len(found) == 1, found
    assert "Orchestrator: a second act" in found[0]
    assert "no row for it" in found[0]


def test_a_row_naming_no_heading_is_named(tmp_path):
    """A2, red-first: the table outliving a rename."""
    stale = (
        "Orchestrator: a heading nobody carries",
        "skills/implement/orchestration.md",
        "still a sentence",
        "Nothing reads it.",
    )
    root = _tree(tmp_path, table=[PLANTED[0], SELF, stale])
    found = findings(root)
    assert len(found) == 1, found
    assert "Orchestrator: a heading nobody carries" in found[0]
    assert "left the row behind" in found[0]


def test_a_named_path_is_resolved_against_the_tree_under_check(tmp_path):
    """Round 1's finding 3, as the case that keeps the leak from returning.

    `bin/round-record` exists in this repository and not in a planted tree,
    so resolving against `ROOT` reports nothing here and resolving against
    the given root names it. A path absent from BOTH trees — which is what
    `test_a_named_command_must_exist` uses — cannot tell the two apart, which
    is why that direction was red for the wrong reason.
    """
    assert os.path.exists(os.path.join(ROOT, "bin", "round-record")), (
        "this case needs a path the repository carries; `bin/round-record` "
        "was it, and the tree no longer has it"
    )
    root = _tree(
        tmp_path,
        table=[
            (
                ACT,
                "skills/implement/orchestration.md",
                "command: `bin/round-record`",
                "",
            ),
            SELF,
        ],
    )
    assert not os.path.exists(os.path.join(root, "bin", "round-record"))
    found = findings(root)
    assert len(found) == 1, found
    assert "bin/round-record" in found[0]
    assert "reads as delivered" in found[0]


def test_a_named_command_must_exist(tmp_path):
    """A3, red-first: a row naming a command with no file behind it."""
    root = _tree(
        tmp_path,
        table=[
            (
                ACT,
                "skills/implement/orchestration.md",
                "command: `bin/does-not-exist`",
                "",
            ),
            SELF,
        ],
    )
    found = findings(root)
    assert len(found) == 1, found
    assert "bin/does-not-exist" in found[0]
    assert "reads as delivered" in found[0]


def test_a_sentence_row_carries_grounds(tmp_path):
    """A4, red-first: `still a sentence` with an empty `Grounds` cell."""
    root = _tree(
        tmp_path,
        table=[
            (ACT, "skills/implement/orchestration.md", "still a sentence", ""),
            SELF,
        ],
    )
    found = findings(root)
    assert len(found) == 1, found
    assert "empty" in found[0] and "Grounds" in found[0]


def test_a_value_outside_the_four_is_named(tmp_path):
    """The `Delivered by` cell holds one of four values and nothing else, so
    a fifth spelling is a defect rather than a row with extra prose in it."""
    root = _tree(
        tmp_path,
        table=[
            (ACT, "skills/implement/orchestration.md", "a command, roughly", "x"),
            SELF,
        ],
    )
    found = findings(root)
    assert len(found) == 1, found
    assert "none of the four values" in found[0]


def test_a_top_level_act_cannot_be_part_of_a_parent(tmp_path):
    """`part of its parent's act` is a `###` answer. A `##` has no parent,
    so the value there is a row that says nothing."""
    root = _tree(
        tmp_path,
        table=[(ACT, "skills/implement/orchestration.md", PART, ""), SELF],
    )
    found = findings(root)
    assert len(found) == 1, found
    assert "no parent act" in found[0]


def test_a_missing_table_is_named_rather_than_read_as_empty(tmp_path):
    """A table nobody can find reports zero rows, and zero rows against zero
    acts is green over nothing -- the shape the neighbour's real-tree case
    guards against."""
    path = os.path.join(_tree(tmp_path, table=[SELF]), "skills", "implement")
    with open(os.path.join(path, "orchestration.md"), "w", encoding="utf-8") as handle:
        handle.write(f"# implement\n\n## {ACT}\n\nProse.\n")
    found = findings(str(tmp_path))
    assert len(found) == 1, found
    assert "enumerated nowhere" in found[0]


def test_a_third_level_heading_under_an_unmarked_section_is_not_an_act(tmp_path):
    """*Directly beneath* is the nearest `##`, not the nearest marked one.
    Reading it the other way sweeps in every `###` after the last marked
    section, which in `code-review`'s file is most of the document."""
    path = os.path.join(
        _tree(tmp_path, table=[PLANTED[0], SELF]), "skills", "code-review"
    )
    with open(os.path.join(path, "orchestration.md"), "w", encoding="utf-8") as handle:
        handle.write("# code-review\n\n## Not an act\n\n### Nor this\n\nProse.\n")
    assert findings(str(tmp_path)) == []


# --- the real tree ------------------------------------------------------------


def test_every_orchestrator_act_names_its_delivery():
    """Both sides against the tree as it stands.

    The acts are asserted first, for the reason the neighbour's real-tree
    case records: `acts` derives them from two files, so a tree without them
    has nothing to check and a check over nothing is green over nothing.
    """
    found_acts = acts(ROOT)
    assert found_acts, (
        "no orchestrator act was read -- the check would pass over nothing"
    )
    parsed, error = rows(ROOT)
    assert error is None, error
    assert parsed, "the table has no rows"
    found = findings(ROOT)
    assert found == [], "\n".join(found)


def test_the_table_reads_the_section_that_holds_it():
    """The table's own section is a marked `##` in one of the two files, so
    the rule that builds the row set reaches it. A table exempting the
    section that holds it would be the one act in the class nothing counts.
    """
    titles = {title for _rel, title, _level in acts(ROOT)}
    assert "Orchestrator: which of these acts runs itself" in titles


@pytest.mark.parametrize("rel", FILES)
def test_both_orchestration_files_are_read(rel):
    """A path that stops resolving makes `acts` quietly skip a file, and the
    rows for it would then all read as rows naming no heading. This fails on
    the path instead."""
    assert os.path.isfile(os.path.join(ROOT, *rel.split("/")))
