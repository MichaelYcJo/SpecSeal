"""A work item writes a ledger fragment; the release folds them.

Issue #78. Every work item writes its evidence rows to
`.specseal/map/<id>.md` and nothing ever folded them into `.specseal/map.md`,
so the directory gained one file per work item forever and almost every pull
request touched it. The fragment layout exists to stop two branches queueing
at one file, and after the merge there is no branch left to queue
(`docs/one-root-by-lifetime.md`, "What happens at a release", step 1).

Step 3 of the same section is the guard: a fact that must outlive the release
has to have reached the ledger, and `specs/<id>/evidence-todo.md` is where a
reviewer lists the ones still waiting. The fold refuses while any such file
has an open row.

This file holds both halves — that the fold happens, that it is a move and
not a deletion, that it refuses in the right places, and that a release pull
request cannot go out with a fragment or an open row left behind. It is the
shape of `test_the_changelog_is_gathered_at_release.py`, because the script is
the shape of `gather_changelog.py`.
"""

import importlib.util
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "fold_ledger.py")
CHECKER = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def _load_checker():
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = _load_checker()


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


def run(*args, root=None):
    return subprocess.run(
        [sys.executable, SCRIPT, *args, "--root", str(root)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def check(root):
    """`evidence_check.py` on the fixture — the totals line and the exit."""
    r = subprocess.run(
        [sys.executable, CHECKER, "."],
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    totals = [line for line in r.stdout.splitlines() if line.startswith("total:")]
    assert totals, r.stdout
    return totals[0], r.returncode


SERVICE = (
    "import os\n\n\ndef handler(x):\n    y = x + 1\n    return y\n\n\n"
    "def parse(s):\n    return s.split()\n\n\n"
    "class Box:\n    def open(self):\n        return self\n"
)


def unit_hash(anchor):
    """The hash a row citing `src/service.py#<anchor>` carries in the fixture."""
    a, b = ec.resolve("src/service.py", anchor, SERVICE)[0]
    return ec.content_hash(SERVICE.splitlines()[a - 1 : b])


def handler_hash():
    return unit_hash("handler")


LEDGER_HEAD = (
    "# spec-to-code map\n\n> The gathered ledger.\n\n## Coordinates\n\n"
    "| Item | Value |\n|---|---|\n| Coordinate notation | `path#anchor@hash` |\n\n"
    "## An area from before the fragments\n\n"
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
    "| the old claim | `src/service.py#handler@{h}` | read | 2026-09-01 | |\n"
)


def row(claim, h, note="", anchor="handler"):
    return (
        f"| {claim} | `src/service.py#{anchor}@{h}` | executed | 2026-09-02 | {note} |"
    )


def fragment(work_item_id, preamble, rows):
    return (
        f"# {work_item_id}\n\n{preamble}\n\n## The area this work item wrote\n\n"
        "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
    )


@pytest.fixture
def tree(tmp_path):
    """A repository shape: a gathered ledger, two fragments whose rows resolve,
    a cited file, and a work item whose evidence-todo file is drained."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    h = handler_hash()
    (tmp_path / ".specseal" / "map").mkdir(parents=True)
    (tmp_path / ".specseal" / "map.md").write_text(
        LEDGER_HEAD.format(h=h), encoding="utf-8"
    )
    later = fragment(
        "1788229400-later",
        "Rows for the later work item.",
        [
            row(
                "the later claim",
                unit_hash("parse"),
                "a note with a | pipe escaped as \\|",
                anchor="parse",
            )
        ],
    )
    earlier = fragment(
        "1700000000-earlier",
        "Rows for the earlier work item.",
        [
            row("the earlier claim", unit_hash("Box"), anchor="Box"),
            row("the earlier second claim", unit_hash("Box.open"), anchor="Box.open"),
        ],
    )
    (tmp_path / ".specseal" / "map" / "1788229400-later.md").write_text(
        later, encoding="utf-8"
    )
    (tmp_path / ".specseal" / "map" / "1700000000-earlier.md").write_text(
        earlier, encoding="utf-8"
    )
    d = tmp_path / "specs" / "1788229400-later"
    d.mkdir(parents=True)
    (d / "evidence-todo.md").write_text(
        "# verified facts to merge\n\ndrained — both rows merged at abc1234.\n\n"
        "| Claim | Grounds | Label |\n|---|---|---|\n"
        "| the later claim | `src/service.py#handler` | Executed |\n",
        encoding="utf-8",
    )
    return tmp_path


def ledger(tree):
    return (tree / ".specseal" / "map.md").read_text(encoding="utf-8")


def fragments_left(tree):
    d = tree / ".specseal" / "map"
    return sorted(p.name for p in d.iterdir()) if d.exists() else []


def fold(tree, version="0.4.0", date="2026-09-15"):
    """Run the fold and prove it actually folded.

    A return code is not an effect — the marker landing in the file and the
    fragment leaving the directory are — so every case that depends on a fold
    having happened goes through this.
    """
    r = run("--version", version, "--date", date, root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    text = ledger(tree)
    assert f"## {version} — {date}" in text, f"exited 0 and wrote no section:\n{text}"
    assert "<!-- specs/" in text, f"exited 0 and wrote no marker:\n{text}"
    return r


def evidence_todo(tree, work_item_id, text):
    d = tree / "specs" / work_item_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "evidence-todo.md").write_text(text, encoding="utf-8")


OPEN_FILE = (
    "# verified facts to merge\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
    "| a fact nobody merged | `src/service.py#handler` | Executed |\n"
)


# --- the fold is a move -----------------------------------------------------


def test_every_row_reaches_the_ledger_byte_for_byte_and_the_fragment_is_gone(tree):
    """A move, not a deletion: the ticket's first "done when"."""
    before = {
        name: (tree / ".specseal" / "map" / name).read_text(encoding="utf-8")
        for name in fragments_left(tree)
    }
    fold(tree)
    text = ledger(tree)
    for name, frag in before.items():
        rows = [line for line in frag.splitlines() if line.startswith("| ")]
        assert rows, f"the fixture fragment {name} has no rows to move"
        for line in rows:
            assert line in text.splitlines(), f"row moved changed or lost:\n{line}"
    assert fragments_left(tree) == [], fragments_left(tree)


def test_the_directory_is_removed_when_it_is_empty(tree):
    fold(tree)
    assert not (tree / ".specseal" / "map").exists()


def test_the_rows_that_were_already_in_the_ledger_stay(tree):
    fold(tree)
    assert "| the old claim |" in ledger(tree)


def test_each_work_item_is_marked_and_headed(tree):
    fold(tree)
    text = ledger(tree)
    assert "<!-- specs/1788229400-later -->\n### 1788229400-later" in text, text
    assert "<!-- specs/1700000000-earlier -->\n### 1700000000-earlier" in text, text


def test_the_fragment_headings_sit_under_the_work_item(tree):
    """The fragment's `## area` becomes `####`, its `# <id>` title is the
    `###` heading above, and the preamble survives between them."""
    fold(tree)
    text = ledger(tree)
    assert "#### The area this work item wrote" in text, text
    assert "\n# 1788229400-later\n" not in text, text
    assert "Rows for the later work item." in text, text


def test_the_section_is_appended_below_the_existing_areas(tree):
    """Q2: a ledger is read by area and its top holds the notation a reader
    needs first, so the release section goes at the end — where the changelog
    gather puts its section at the top."""
    fold(tree)
    headings = re.findall(r"^## (.+)$", ledger(tree), re.M)
    assert headings[-1].startswith("0.4.0"), headings
    assert headings[0] == "Coordinates", headings


def test_the_work_items_are_in_id_order(tree):
    fold(tree)
    text = ledger(tree)
    assert text.index("1700000000-earlier") < text.index("1788229400-later"), text


def test_folding_twice_finds_nothing_and_writes_nothing(tree):
    fold(tree)
    once = ledger(tree)
    second = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert second.returncode == 1, second.stdout
    assert "nothing to fold" in second.stdout, second.stdout
    assert ledger(tree) == once


def test_a_fragment_whose_marker_is_already_in_the_ledger_is_refused(tree):
    """Folding it again would put the same rows in the file twice with no way
    to tell which is current. A stop naming the file is cheaper."""
    fold(tree)
    once = ledger(tree)
    (tree / ".specseal" / "map").mkdir()
    (tree / ".specseal" / "map" / "1788229400-later.md").write_text(
        fragment(
            "1788229400-later", "Re-created.", [row("late claim", handler_hash())]
        ),
        encoding="utf-8",
    )
    r = run("--version", "0.4.1", "--date", "2026-09-16", root=tree)
    assert r.returncode == 1, r.stdout
    assert ".specseal/map/1788229400-later.md" in r.stdout, r.stdout
    assert "already" in r.stdout, r.stdout
    assert ledger(tree) == once, "the refusal wrote to the ledger"
    assert fragments_left(tree) == ["1788229400-later.md"], "the refusal removed it"


def test_a_marker_quoted_in_the_ledgers_prose_is_not_a_folded_work_item(tree):
    """Round 1, 🟡 3. A substring test read the marker's shape in prose as a
    fold that had happened, and refused with advice to remove the fragment —
    the only copy of the rows. The mark is a line of its own."""
    text = ledger(tree).replace(
        "> The gathered ledger.",
        "> The gathered ledger. A folded item is marked like "
        "`<!-- specs/1788229400-later -->`.",
    )
    assert "<!-- specs/1788229400-later -->" in text
    (tree / ".specseal" / "map.md").write_text(text, encoding="utf-8")
    fold(tree)
    assert "| the later claim |" in ledger(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    assert "2 work items marked" in r.stdout, r.stdout


def test_the_messages_print_slash_joined_paths_on_every_platform(tree):
    """Round 1, 🔴 1. `os.path.join` printed `.specseal\\map` on Windows and
    three assertions expected `/`. A backslash in either message is the
    regression, on every leg and not only the Windows one."""
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "\\" not in r.stdout, r.stdout
    fold(tree)
    (tree / ".specseal" / "map").mkdir()
    (tree / ".specseal" / "map" / "1788229400-later.md").write_text(
        fragment("1788229400-later", "Again.", [row("late", handler_hash())]),
        encoding="utf-8",
    )
    for args in (("--version", "0.4.1"), ("--check",)):
        r = run(*args, root=tree)
        assert r.returncode == 1, r.stdout
        assert ".specseal/map/1788229400-later.md" in r.stdout, r.stdout
        assert "\\" not in r.stdout, r.stdout


U2028_ROW = "| a claim\u2028with a line separator | `src/service.py#handler` | c |"


def test_a_row_holding_a_line_separator_arrives_as_one_row(tree):
    """Round 1, 🟡 5 (probe B). `splitlines()` breaks on U+2028, which is
    not a newline to the file, so one row became two lines."""
    (tree / ".specseal" / "map" / "1788229400-later.md").write_text(
        fragment("1788229400-later", "Odd bytes.", [U2028_ROW]), encoding="utf-8"
    )
    fold(tree)
    assert U2028_ROW in ledger(tree).split("\n"), ledger(tree)


def test_the_last_row_keeps_its_trailing_whitespace_and_a_fenced_hash_is_text(tree):
    """Round 1, 🟡 5 (probes A and C). `strip()` took the last row's trailing
    tab, and a `#` line inside a code fence was demoted as a heading."""
    last = row("the last claim", unit_hash("parse"), anchor="parse") + " \t"
    body = (
        "# 1788229400-later\n\nA note:\n\n```\n# not a heading\n```\n\n"
        "## The area\n\n| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n" + last + "\n"
    )
    (tree / ".specseal" / "map" / "1788229400-later.md").write_text(
        body, encoding="utf-8"
    )
    fold(tree)
    lines = ledger(tree).split("\n")
    assert last in lines, "the trailing whitespace was stripped"
    assert "# not a heading" in lines, "the fenced line was demoted"
    assert "#### The area" in lines


def test_dry_run_writes_and_removes_nothing(tree):
    before = ledger(tree)
    left = fragments_left(tree)
    r = run("--version", "0.4.0", "--date", "2026-09-15", "--dry-run", root=tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "## 0.4.0 — 2026-09-15" in r.stdout, r.stdout
    assert "<!-- specs/1700000000-earlier -->" in r.stdout, r.stdout
    assert ledger(tree) == before, "--dry-run wrote to the ledger"
    assert fragments_left(tree) == left, "--dry-run removed a fragment"


def test_an_empty_fragment_is_removed_and_named_and_gets_no_marker(tree):
    """A marker with nothing under it would make `--check` say the rows
    arrived when there were none."""
    (tree / ".specseal" / "map" / "1788300000-empty.md").write_text(
        "# 1788300000-empty\n\n", encoding="utf-8"
    )
    r = fold(tree)
    assert "1788300000-empty.md  (empty, removed)" in r.stdout, r.stdout
    assert "1788300000-empty" not in ledger(tree)
    assert fragments_left(tree) == []


def test_a_missing_ledger_is_a_failure_not_a_fresh_start(tree):
    """Nothing to fold INTO is a broken tree; creating one would hide it."""
    (tree / ".specseal" / "map.md").unlink()
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, r.stdout
    assert fragments_left(tree) == ["1700000000-earlier.md", "1788229400-later.md"]


# --- the checker cannot tell ------------------------------------------------


def test_the_checker_reports_the_same_totals_before_and_after(tree):
    """A row is a content anchor, so moving it between files changes nothing
    the checker measures. Both runs are executed here, not inferred."""
    before, before_rc = check(tree)
    assert before_rc == 0 and "0 broken" in before and "0 drifted" in before, before
    assert "4 ok" in before, before  # one old row, three fragment rows
    fold(tree)
    after, after_rc = check(tree)
    assert (after, after_rc) == (before, before_rc), (before, after)


def test_the_one_thing_a_fold_changes_is_a_duplicate_counted_once(tree):
    """`check_ledger` de-duplicates on (coordinate, hash) within one file, so
    a row a fragment repeats from `map.md` counts twice before the fold and
    once after. No finding changes; the spec's S6 names this so a release
    reading a smaller total does not go looking for a lost row."""
    (tree / ".specseal" / "map" / "1788229400-later.md").write_text(
        fragment(
            "1788229400-later",
            "A repeat.",
            [row("the old claim again", handler_hash())],
        ),
        encoding="utf-8",
    )
    before, _ = check(tree)
    assert "4 ok" in before, before
    fold(tree)
    after, rc = check(tree)
    assert "3 ok" in after and rc == 0, after


# --- the guard --------------------------------------------------------------


def test_an_open_evidence_todo_row_refuses_the_fold_and_touches_nothing(tree):
    evidence_todo(tree, "1700000000-earlier", OPEN_FILE)
    before = ledger(tree)
    left = fragments_left(tree)
    r = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 1, r.stdout
    assert "specs/1700000000-earlier/evidence-todo.md" in r.stdout, r.stdout
    assert "1 open row" in r.stdout, r.stdout
    assert ledger(tree) == before, "the refusal wrote to the ledger"
    assert fragments_left(tree) == left, "the refusal removed a fragment"


def test_the_guard_reads_every_work_item_in_the_tree_not_only_folded_ones(tree):
    """Q1: a work item released earlier whose file was never drained blocks
    this release too. It has no fragment left, and it still stops the fold."""
    evidence_todo(tree, "1600000000-released-long-ago", OPEN_FILE)
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1600000000-released-long-ago" in r.stdout, r.stdout


@pytest.mark.parametrize(
    "shape, text",
    [
        (
            "drained above the table",
            "# facts\n\ndrained — all rows merged at abc1234.\n\n"
            "| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n",
        ),
        (
            "drained below the table",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n\n"
            "drained — applied by the round-1 fix pass.\n",
        ),
        (
            "drained in bold",
            "# facts\n\n**Drained.**\n\n"
            "| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n",
        ),
        (
            "every row marked",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
            "| ✅ a | merged at abc1234 | c |\n| ✅ b | merged at abc1234 | c |\n",
        ),
        (
            "header and no body row",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n",
        ),
        ("no table at all", "# facts\n\nnothing was prescribed.\n"),
    ],
)
def test_a_closed_evidence_todo_file_does_not_refuse(tree, shape, text):
    evidence_todo(tree, "1700000000-earlier", text)
    r = run("--version", "0.4.0", "--date", "2026-09-15", root=tree)
    assert r.returncode == 0, f"{shape}:\n{r.stdout}{r.stderr}"


@pytest.mark.parametrize(
    "shape, text",
    [
        (
            "not drained is not drained",
            "# facts\n\nnot drained yet.\n\n"
            "| Claim | Grounds | Label |\n|---|---|---|\n| a | b | c |\n",
        ),
        (
            "one row marked, one not",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
            "| ✅ a | merged | c |\n| b | still waiting | c |\n",
        ),
        (
            "drained inside a table cell does not close the file",
            "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
            "| drained | b | c |\n",
        ),
    ],
)
def test_an_open_shape_refuses(tree, shape, text):
    evidence_todo(tree, "1700000000-earlier", text)
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, f"{shape}:\n{r.stdout}"
    assert "1700000000-earlier/evidence-todo.md" in r.stdout, r.stdout


def test_a_line_separator_in_a_cell_does_not_close_the_file(tree):
    """Round 1, 🟡 4 (probe E). `splitlines()` read the cell's tail after
    U+2028 as a line of its own, and `drained` there closed the file: zero
    open rows where one was — the silent direction for a guard."""
    evidence_todo(
        tree,
        "1700000000-earlier",
        "# facts\n\n| Claim | Grounds | Label |\n|---|---|---|\n"
        "| a claim\u2028drained | b | c |\n",
    )
    r = run("--version", "0.4.0", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1700000000-earlier/evidence-todo.md  (1 open row)" in r.stdout, r.stdout


def test_a_work_item_without_the_file_has_no_open_row(tree):
    """The fixture's second work item has no `specs/` directory at all."""
    assert not (tree / "specs" / "1700000000-earlier").exists()
    fold(tree)


# --- --check ----------------------------------------------------------------


def test_check_fails_while_a_fragment_is_left(tree):
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert ".specseal/map/1788229400-later.md" in r.stdout, r.stdout
    assert ".specseal/map/1700000000-earlier.md" in r.stdout, r.stdout


def test_check_fails_on_an_open_evidence_todo_row_even_with_nothing_to_fold(tree):
    """Q3: a fold done by hand still meets the guard at the release pull
    request, the last moment anyone is looking."""
    fold(tree)
    evidence_todo(tree, "1600000000-released-long-ago", OPEN_FILE)
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "1600000000-released-long-ago/evidence-todo.md" in r.stdout, r.stdout


def test_check_passes_once_folded_and_says_what_it_counted(tree):
    fold(tree)
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout
    # A `--check` that exits 0 because it found nothing at all would satisfy
    # the line above. It has to say it saw both work items in the ledger.
    assert "2 work items marked in .specseal/map.md" in r.stdout, r.stdout


def test_a_copy_edit_to_a_folded_section_does_not_reopen_it(tree):
    """Marked, not matched: re-wording a folded note leaves `--check` green."""
    fold(tree)
    text = ledger(tree).replace("the later claim", "the later claim, reworded")
    (tree / ".specseal" / "map.md").write_text(text, encoding="utf-8")
    r = run("--check", root=tree)
    assert r.returncode == 0, r.stdout


def test_check_names_a_left_fragment_whose_marker_is_already_there(tree):
    fold(tree)
    (tree / ".specseal" / "map").mkdir()
    (tree / ".specseal" / "map" / "1788229400-later.md").write_text(
        fragment("1788229400-later", "Re-created.", [row("late", handler_hash())]),
        encoding="utf-8",
    )
    r = run("--check", root=tree)
    assert r.returncode == 1, r.stdout
    assert "compare by hand" in r.stdout, r.stdout


# --- this repository --------------------------------------------------------


def test_the_release_pull_request_runs_the_check():
    """A convention nothing enforces is a convention somebody forgets at the
    release, which is the last moment anyone is looking."""
    workflow = read(".github", "workflows", "hygiene.yml")
    assert "fold_ledger.py --check" in workflow, (
        "the release workflow does not check the ledger fragments"
    )
    assert os.path.isfile(SCRIPT), "the workflow calls a script that is not there"


def test_the_check_only_runs_for_a_release():
    """On a feature pull request every fragment on the branch is legitimately
    unfolded — running it there would fail every branch that writes one."""
    workflow = read(".github", "workflows", "hygiene.yml")
    step = workflow.split("every ledger fragment folded into the gathered ledger")[1]
    step = step.split("- name:")[0]
    assert 'github.base_ref }}" != "main"' in step, (
        "the step no longer skips itself outside a release pull request"
    )


def test_no_document_says_the_fragments_are_never_gathered():
    """Every place that said so now says what is true: rows go in the
    fragment during development and the release folds them into `map.md`."""
    for parts in (
        ("CLAUDE.md",),
        ("CONTRIBUTING.md",),
        ("README.md",),
        ("README.ko.md",),
        (".specseal", "README.md"),
        (".specseal", "map.md"),
        ("templates", "map.md"),
        ("templates", "specseal-README.md"),
        ("skills", "implement", "SKILL.md"),
        ("skills", "evidence-check", "SKILL.md"),
        ("docs", "branch-and-release.md"),
    ):
        text = flat(*parts)
        for old in (
            "never gathered",
            "never are",
            "Fragments are never gathered back",
            "stays where it is forever",
            "다시 합치지 않는다",
        ):
            assert old not in text, "/".join(parts) + f" still says: {old}"


def test_the_release_sequence_names_the_fold_beside_the_gather():
    """The sequence in `docs/branch-and-release.md` is walked by whoever cuts
    a release, and `CONTRIBUTING.md` holds the commands. A step that is only
    in a workflow comment is a step that gets discovered by a red build."""
    for parts in (("docs", "branch-and-release.md"), ("CONTRIBUTING.md",)):
        text = flat(*parts)
        assert "fold_ledger.py" in text, (
            "/".join(parts) + " does not name the script that folds the ledger"
        )
        assert text.index("gather_changelog.py") < text.index("fold_ledger.py"), (
            "/".join(parts) + " names the fold before the gather it belongs beside"
        )


THIS_WORK_ITEM = "1788326734-the-ledger-fragments-are-never-gathered"


def this_work_items_rows_are_in_the_ledger(root):
    """The fragment while it exists, its folded section in `map.md` after.

    Round 1, 🔴 2: reading the fragment alone is a permanent test of a file
    that lives between releases, which is the shape the dependency rule names
    "would break on removal" — the release-preparation commit would have
    turned the tests red on its own pull request.
    """
    frag = os.path.join(root, ".specseal", "map", f"{THIS_WORK_ITEM}.md")
    if os.path.isfile(frag):
        with open(frag, encoding="utf-8") as f:
            text = f.read()
        where = "the fragment"
    else:
        with open(os.path.join(root, ".specseal", "map.md"), encoding="utf-8") as f:
            text = f.read()
        lines = text.split("\n")
        assert f"<!-- specs/{THIS_WORK_ITEM} -->" in lines, (
            "this work item wrote no ledger fragment, and no fold marked it"
        )
        text = text.split(f"<!-- specs/{THIS_WORK_ITEM} -->", 1)[1]
        where = "the folded section"
    assert "fold_ledger.py#" in text, f"{where} cites nothing in the script"


def test_this_work_item_wrote_its_own_fragment():
    """Dogfood. A convention the branch introducing it did not follow is one
    nobody has tried."""
    this_work_items_rows_are_in_the_ledger(ROOT)


def test_this_work_items_rows_are_still_found_after_the_release_folds_them(tmp_path):
    """The same body, on a copy of this repository after the fold has run
    there. `specs/` rides along because the guard reads every evidence-todo
    file in the tree, this work item's included."""
    for d in (".specseal", "specs"):
        shutil.copytree(os.path.join(ROOT, d), tmp_path / d)
    r = run("--version", "9.9.9", "--date", "2026-12-31", root=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert not (tmp_path / ".specseal" / "map").exists(), "the fold removed nothing"
    this_work_items_rows_are_in_the_ledger(str(tmp_path))
