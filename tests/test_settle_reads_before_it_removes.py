"""`settle` names what a policy document has yet to absorb, and removes only
what one already has.

`seal/README.md` has said a work item's directory waits for a later `settle`
since the root existed, and nothing was ever built: 98 work items and 15M on
the tree this shipped from. #458, closing #83.

The split this file holds to is the one `docs/one-root-by-lifetime.md`
§*What keeps `settle` light* fixes — the step "moves and does not verify". So
every case below asks what the command READ, and the two that touch the tree
ask what it removed and what it refused to remove. Nothing here asserts that
prose was written, because the command writes none.
"""

import glob
import importlib.util
import io
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "settle", "scripts", "settle.py")


def load():
    spec = importlib.util.spec_from_file_location("settle", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


settle = load()

LEDGER = """# spec-to-code map

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| a row from before the fragments existed | `hooks/old.py#thing@11111111` | read | 2026-01-01 | |

## 0.1.0 — 2026-01-01

<!-- specs/1700000001-alpha -->
### 1700000001-alpha

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| one | `hooks/a.py#one@aaaaaaaa` | read | 2026-01-01 | |
| two | `hooks/a.py#two@bbbbbbbb` | read | 2026-01-01 | |
| three | `tests/test_a.py#"a line"@cccccccc` | read | 2026-01-01 | |

<!-- specs/1700000002-beta -->
### 1700000002-beta

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| only a case | `tests/test_b.py#test_b@dddddddd` | read | 2026-01-01 | |

<!-- specs/1700000003-gamma -->
### 1700000003-gamma

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| one | `hooks/a.py#one@eeeeeeee` | read | 2026-01-01 | |
"""

CLEAN_TODO = """# evidence-todo

| Fact | Where it goes |
|---|---|
| ✅ something a reviewer verified | merged into the fragment |
"""

OPEN_TODO = """# evidence-todo

| Fact | Where it goes |
|---|---|
| a fact that never reached the ledger | the work item's fragment |
"""


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def tree(tmp_path):
    """Four work items: three released, one that arrives after the commit.

    `gamma` is the guard's, `beta` is anchored only under `tests/`, and
    `delta` is this branch's own unreleased work.
    """
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "one-root.md").write_text("# a policy\n\nA rule.\n", "utf-8")
    (repo / "seal").mkdir()
    (repo / "seal" / "ledger.md").write_text(LEDGER, encoding="utf-8")
    for name, todo in (
        ("1700000001-alpha", CLEAN_TODO),
        ("1700000002-beta", CLEAN_TODO),
        ("1700000003-gamma", OPEN_TODO),
    ):
        item = repo / "seal" / "specs" / name
        item.mkdir(parents=True)
        (item / "spec.md").write_text(f"# {name}\n\nWhat it decided.\n", "utf-8")
        (item / "evidence-todo.md").write_text(todo, encoding="utf-8")
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "x@example.com")
    git(repo, "config", "user.name", "x")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "released")
    later = repo / "seal" / "specs" / "1700000004-delta"
    later.mkdir()
    (later / "spec.md").write_text("# delta\n\nIn flight.\n", encoding="utf-8")
    return repo


def fold(repo, work_item_id, document="one-root.md"):
    """Record a fold the way the skill's procedure does: the folded sentence
    carries the work item's provenance comment in the `docs/` document it
    landed in, and there is no second file."""
    path = repo / "docs" / document
    path.write_text(
        path.read_text(encoding="utf-8")
        + f"\n<!-- specs/{work_item_id} -->\nThe standing statement.\n",
        encoding="utf-8",
    )


def run(repo, *args):
    """`(exit code, what a person reads)`."""
    out = io.StringIO()
    found = settle.survey(str(repo), "HEAD")
    assert found is not None, "the fixture's HEAD does not resolve"
    if "--retire" in args:
        code = settle.retire(found, str(repo), out=out)
    else:
        code = settle.report(found, "HEAD", out=out)
    return code, out.getvalue()


# --- A3: it names what it would fold, and folds nothing ---------------------


def test_the_report_groups_released_work_items_by_segment(tree):
    code, text = run(tree)
    assert code == 0, text
    assert "hooks/a.py" in text, text
    assert "1700000001-alpha" in text, text
    # The segment is the file the item's code anchors name, by majority. Two
    # of alpha's three rows are `hooks/a.py` and the third is a case that
    # pins it, which is Q2's rule: a test anchor rolls up to the code it
    # pins, and never to a segment called `tests`.
    assert "tests/test_a.py" not in text, text


def test_an_item_anchored_only_under_tests_is_named_not_guessed(tree):
    """Q2's other half. The link from a case to the code it pins is nowhere a
    machine reads, so an item with no code anchor is named rather than filed
    under a guess."""
    _, text = run(tree)
    assert "1700000002-beta  (tests only)" in text, text


def test_the_report_writes_nothing_and_removes_nothing(tree):
    before = sorted(str(p.relative_to(tree)) for p in tree.rglob("*") if p.is_file())
    run(tree)
    after = sorted(str(p.relative_to(tree)) for p in tree.rglob("*") if p.is_file())
    assert before == after, "the report touched the tree"
    assert "Nothing was written and nothing was removed" in run(tree)[1]


def test_an_unreleased_work_item_is_not_a_candidate(tree):
    """Released means present on the branch the release merges to, so this
    branch's own work item is outside the corpus entirely."""
    _, text = run(tree)
    assert "1700000004-delta" not in text, text
    assert "1 unreleased and untouched" in text, text


def test_a_ref_that_does_not_resolve_is_refused_rather_than_empty(tree):
    """The quiet zero this is written against: a ref nothing can read makes
    every work item look unreleased, and the report would then say there is
    nothing to fold."""
    assert settle.survey(str(tree), "no/such/ref") is None


# --- A5: the guard stops one item and not the run --------------------------


def test_an_open_evidence_todo_row_skips_that_item_and_names_it(tree):
    _, text = run(tree)
    assert "1700000003-gamma" in text, text
    assert "skipped" in text and "evidence-todo.md" in text, text


def test_the_guard_does_not_reach_the_other_items(tree):
    _, text = run(tree)
    assert "1700000001-alpha" in text.split("\nskipped —")[0], text


def test_a_drained_line_closes_the_file(tree):
    """The rule a person can apply by hand, and the one shape that closes a
    file without marking every row."""
    assert settle.open_rows(OPEN_TODO)
    assert not settle.open_rows(OPEN_TODO + "\ndrained — every row is in the ledger\n")


# --- A4: a second run folds nothing twice ----------------------------------


def test_a_recorded_fold_leaves_the_foldable_list(tree):
    fold(tree, "1700000001-alpha")
    _, text = run(tree)
    listed = text.split("folded already")[0]
    assert "1700000001-alpha" not in listed, text
    assert "1700000001-alpha" in text.split("folded already")[1], text


def test_retire_removes_only_what_docs_records(tree):
    fold(tree, "1700000001-alpha")
    code, text = run(tree, "--retire")
    assert code == 0, text
    assert not (tree / "seal" / "specs" / "1700000001-alpha").exists()
    assert (tree / "seal" / "specs" / "1700000002-beta").exists(), (
        "a work item with no fold record was removed"
    )


def test_retire_refuses_an_item_the_guard_is_holding(tree):
    """A fold recorded while a fact the reviewer verified is still waiting for
    the ledger. The record says the prose landed; the row says something else
    has not, and the directory is what holds it."""
    fold(tree, "1700000003-gamma")
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000003-gamma").exists()
    assert "kept" in text and "1700000003-gamma" in text, text


def test_an_interrupted_run_resumes(tree):
    """Two items folded, one retired by hand, and the command picks up the
    other: the record is derived from the destination, so it says which half
    of the work is done without a file of its own to keep in step.

    Round 1, finding 5 corrected what the run says once both halves are done:
    the markers are still in `docs/` and the fold DID happen, so *nothing has
    been folded yet* was the one reading the tree contradicts."""
    fold(tree, "1700000001-alpha")
    fold(tree, "1700000002-beta")
    run(tree, "--retire")
    assert not (tree / "seal" / "specs" / "1700000001-alpha").exists()
    assert not (tree / "seal" / "specs" / "1700000002-beta").exists()
    code, text = run(tree, "--retire")
    assert code == 0, text
    assert "The fold is complete." in text, text


# --- #511: a ledger row anchored inside a directory keeps it ---------------

INSIDE = (
    '`seal/specs/1700000001-alpha/rounds/round-1.md#"# alpha — review round 1"'
    "@abcdef12`"
)
INSIDE_ROW = f"| a claim read in a round record | {INSIDE} | read | 2026-01-01 | |"


def anchor(repo, row, after):
    """Put `row` into the fixture ledger on the line after `after`."""
    ledger = repo / "seal" / "ledger.md"
    text = ledger.read_text(encoding="utf-8")
    assert after in text, f"the fixture has no line {after!r}"
    ledger.write_text(text.replace(after, f"{after}\n{row}", 1), encoding="utf-8")
    return text.split("\n").index(after) + 2


def test_a_row_anchored_inside_a_candidate_keeps_that_directory(tree):
    """#511's red direction. The fold's own retirement broke five permanent
    rows, each anchored at a retired work item's `spec.md`, and the branch
    found them only when `evidence_check .` went red after the removal. The
    guard keeps per directory — the evidence-todo guard's shape — so the other
    candidate still goes."""
    fold(tree, "1700000001-alpha")
    fold(tree, "1700000002-beta")
    line = anchor(
        tree, INSIDE_ROW, "| one | `hooks/a.py#one@aaaaaaaa` | read | 2026-01-01 | |"
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), (
        "a directory a ledger row anchors into was removed"
    )
    assert not (tree / "seal" / "specs" / "1700000002-beta").exists(), (
        "the guard held a directory no row anchors into"
    )
    assert f"seal/ledger.md:{line}" in text, text
    assert "a claim read in a round record" in text, text
    assert "REMOVED" in text, text


def test_a_row_above_the_first_marker_is_read_by_the_guard(tree):
    """`coordinates` skips every row above the first `<!-- specs/ -->` marker,
    and the one row that anchors under `seal/specs/` in this repository's own
    ledger sits exactly there. A guard built on that reader would never see
    it."""
    fold(tree, "1700000001-alpha")
    line = anchor(
        tree,
        INSIDE_ROW,
        "| a row from before the fragments existed | `hooks/old.py#thing@11111111`"
        " | read | 2026-01-01 | |",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert f"seal/ledger.md:{line}" in text, text


def test_a_row_in_a_fragment_is_read_by_the_guard(tree):
    """The second address the checker reads. A fragment row anchored at a
    work item's own `survivors.md` is the other instance #511 measured."""
    fold(tree, "1700000001-alpha")
    fragments = tree / "seal" / "ledger"
    fragments.mkdir()
    (fragments / "1700000009-later.md").write_text(INSIDE_ROW + "\n", encoding="utf-8")
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert "seal/ledger/1700000009-later.md:1" in text, text


def test_a_row_with_a_live_anchor_beside_the_dead_one_is_narrowed(tree):
    """A row that keeps a live anchor is not REMOVED by `CLAUDE.md`'s rule,
    and whether it should be is the repository owner's question — so the line
    says to drop the dead anchor and names who answers the rest."""
    fold(tree, "1700000001-alpha")
    anchor(
        tree,
        f"| two anchors | {INSIDE}, `hooks/a.py#one@aaaaaaaa` | read | 2026-01-01 | |",
        "| one | `hooks/a.py#one@aaaaaaaa` | read | 2026-01-01 | |",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert "narrow" in text, text
    assert "REMOVED" not in text, text
    assert "repository owner" in text, (
        "the multi-anchor answer is the owner's and the line does not say so"
    )


def test_the_report_names_an_anchored_row_before_anything_is_removed(tree):
    """The session sees the row while it writes the prose, not after. The
    report reads every released directory, folded or not."""
    anchor(
        tree, INSIDE_ROW, "| one | `hooks/a.py#one@aaaaaaaa` | read | 2026-01-01 | |"
    )
    code, text = run(tree)
    assert code == 0, text
    assert "anchored" in text and "a claim read in a round record" in text, text
    assert "1700000001-alpha" in text.split("anchored")[1], text


def test_a_fenced_anchor_still_keeps_the_directory(tree):
    """evidence-check reads an anchor inside a fence as a coordinate like any
    other, so the guard has to as well: a fenced row's directory removed is a
    BROKEN row found after the fact, which is #511 (round 1's finding 1)."""
    fold(tree, "1700000001-alpha")
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + f"\n```markdown\n{INSIDE_ROW}\n```\n",
        encoding="utf-8",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text


def test_a_commented_out_row_is_named_by_its_claim(tree):
    """Round 2's finding 7: a row inside an HTML comment keeps its directory,
    and the report names it by its first cell, not by the comment opener."""
    fold(tree, "1700000001-alpha")
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + f"\n<!-- {INSIDE_ROW} -->\n",
        encoding="utf-8",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert "a claim read in a round record" in text, text
    assert "  <!--\n" not in text, text


@pytest.mark.parametrize(
    "line",
    [
        "> | claim | `a.py#b@11111111` |",
        "- | claim | `a.py#b@11111111` |",
        "> - | claim | `a.py#b@11111111` |",
        "> > | claim | `a.py#b@11111111` |",
        "1. | claim | `a.py#b@11111111` |",
        ">| claim | `a.py#b@11111111` |",
        "* + 2) | claim | `a.py#b@11111111` |",
        "<!-- > | claim | `a.py#b@11111111` |",
    ],
)
def test_a_row_inside_container_syntax_is_named_by_its_claim(line):
    """#530. Whatever stands before a row's first pipe as blockquote, list or
    comment syntax is the container, not the claim — the class, in any
    combination and spaced or not, rather than the five single tokens round
    3's paste-ready fix named (`agent-contract` §12)."""
    assert settle.first_cell(line) == "claim", line


def test_a_quoted_list_row_is_named_by_its_claim_in_the_report(tree):
    """#530, through the command: the line a person reads names the claim, and
    not the `> -` the row happens to stand behind."""
    fold(tree, "1700000001-alpha")
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + f"\n> - {INSIDE_ROW}\n",
        encoding="utf-8",
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert "a claim read in a round record" in text, text
    assert "  > -\n" not in text and "  >\n" not in text, text


@pytest.mark.parametrize(
    "line, label",
    [
        # Green before and after: today's comment-opener arm, and a prefix
        # that holds prose, which is left exactly as it was.
        ("<!-- | claim | `a.py#b@11111111` |", "claim"),
        ("see this row | claim | `a.py#b@11111111` |", "see this row"),
        ("> note - | claim | `a.py#b@11111111` |", "> note -"),
        ("1.5 | claim | `a.py#b@11111111` |", "1.5"),
    ],
)
def test_a_prefix_that_is_not_container_syntax_keeps_todays_label(line, label):
    assert settle.first_cell(line) == label, line


def test_a_row_at_the_old_evidence_address_keeps_the_directory(tree):
    """The checker's third address, `docs/**/_evidence.md`, is still read, so
    a row there anchored inside a retiring directory is BROKEN after the
    removal all the same."""
    fold(tree, "1700000001-alpha")
    old = tree / "docs" / "area" / "_evidence.md"
    old.parent.mkdir(parents=True)
    old.write_text(INSIDE_ROW + "\n", encoding="utf-8")
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert "docs/area/_evidence.md:1" in text, text


def test_a_row_in_a_release_file_is_read_by_the_guard(tree):
    """#547, S4's second half. The fold writes each release's rows to
    `seal/releases/<X.Y.Z>.md`; the guard follows the checker's list, so a
    row there anchored inside a retiring directory keeps it. Asserted once,
    here, because `anchored_rows` reads `default_patterns` and does not
    spell the list itself."""
    fold(tree, "1700000001-alpha")
    release = tree / "seal" / "releases" / "0.4.0.md"
    release.parent.mkdir()
    release.write_text(
        "## 0.4.0 — 2026-01-02\n\n" + INSIDE_ROW + "\n", encoding="utf-8"
    )
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists(), text
    assert "seal/releases/0.4.0.md:3" in text, text


def test_the_documents_say_the_retirement_keeps_an_anchored_directory():
    """§14's half of #511: the skill a fold session reads and the policy it
    folds under both say the guard exists, and neither still says nothing
    refuses the removal."""
    text = flat(skill())
    assert "A directory a ledger row anchors into is kept too" in text
    assert (
        "the ones above the first section marker and the ones inside a fence "
        "included" in text
    )
    assert "`docs/**/_evidence.md`" in text, (
        "the skill does not name the checker's third ledger address"
    )
    policy = document("docs", "the-evidence-ledger.md")
    assert "the rows inside a fence included, because the checker" in flat(policy), (
        "the policy still says the guard reads only live rows"
    )
    assert "nothing refuses the removal first" not in policy, (
        "the policy still says nothing refuses the removal"
    )
    assert "so the retirement refuses that directory first" in policy
    assert "The command names the rows and edits none of them" in policy


def test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item():
    """#517's repair step 2, and the rule it leaves behind. The one row the
    guard found when it shipped — anchored at `1788184145`'s round 3 — was
    REMOVED and its claim re-founded on the prose that states it, and no row
    a later work item writes may anchor under `seal/specs/`, its own directory
    included, or the next fold keeps that directory.

    Every work item, released or not, and no floor: at zero directories the
    list is empty and the property still holds."""
    rows = settle.anchored_rows(ROOT, settle.work_items(ROOT))
    assert not rows, [f"{r.file}:{r.line}  {r.clause[:60]}" for r in rows]


def test_the_policy_says_the_held_row_was_answered():
    policy = document("docs", "the-evidence-ledger.md")
    assert "is carried by #517's design comment" not in policy, (
        "the policy still says the question for 1788184145 is open"
    )
    assert "that trade was taken" in policy


# --- D3: a released work item with no spec.md is retired by a rule ---------

OVERVIEW_OPEN = """# x — overview

## Not verified

| Item | Who must answer |
|---|---|
| a claim nobody ran | the repository owner |
"""

OVERVIEW_CLOSED = """# x — overview

## Not verified

| Item | Who must answer |
|---|---|
| ✅ a claim | run on 2026-01-01 |
"""

MOMENT = "1700000006-release-0-1-0"


def moment(repo, name=MOMENT, overview=None, todo=None):
    """A released work item below the SDD ladder: a routing declaration and
    perhaps a memo, and no `spec.md`. Committed on its own path, so the
    unreleased `delta` the fixture leaves on disk stays unreleased."""
    item = repo / "seal" / "specs" / name
    item.mkdir(parents=True)
    (item / "routing.md").write_text(f"# {name} — routing\n", encoding="utf-8")
    if overview is not None:
        (item / "overview.md").write_text(overview, encoding="utf-8")
    if todo is not None:
        (item / "evidence-todo.md").write_text(todo, encoding="utf-8")
    git(repo, "add", "--", f"seal/specs/{name}")
    git(repo, "commit", "-qm", f"released {name}")
    return item


def docs_text(repo):
    return {p.name: p.read_text(encoding="utf-8") for p in (repo / "docs").glob("*")}


def test_a_spec_less_directory_is_listed_under_its_own_heading(tree):
    """D3: `settle` prints these under their own heading rather than as
    *ungrouped — yours to place*, because there is nothing to place."""
    moment(tree, overview=OVERVIEW_CLOSED)
    code, text = run(tree)
    assert code == 0, text
    assert "retired by the rule" in text, text
    assert MOMENT in text.split("retired by the rule")[1], text
    ungrouped = (
        text.split("ungrouped —")[1].split("\n\n")[0] if "ungrouped —" in text else ""
    )
    assert MOMENT not in ungrouped, text


def test_the_rule_arm_removes_it_with_no_marker(tree):
    moment(tree, overview=OVERVIEW_CLOSED)
    before = docs_text(tree)
    code, text = run(tree, "--retire")
    assert not (tree / "seal" / "specs" / MOMENT).exists(), text
    assert docs_text(tree) == before, "the rule arm wrote a marker into docs/"
    assert f"removed seal/specs/{MOMENT}/" in text, text
    assert "no `spec.md`" in text, text
    # The fixture's other released items carry a spec and no marker, so they
    # stay; nothing refused, so the run is clean.
    assert code == 0, text
    assert (tree / "seal" / "specs" / "1700000001-alpha").exists()


def test_an_open_memo_row_keeps_a_spec_less_directory(tree):
    """G2: D3 is true of the spec and false of the memo. An open
    `## Not verified` row is a claim with an answerer, and it leaves by being
    closed or re-homed — never with the directory."""
    moment(tree, overview=OVERVIEW_OPEN)
    _, text = run(tree)
    assert "kept by the rule" in text, text
    assert "a claim nobody ran" in text.split("kept by the rule")[1], text
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / MOMENT).exists(), text
    assert "a claim nobody ran" in text, text


def test_a_closed_row_is_told_to_merge_before_its_directory_goes(tree):
    """Round 1's finding 2. The CI readers ask the rule of the merge base, so
    a row closed and its directory retired in one pull request is refused
    there after `settle --retire` said the removal was fine. The report, the
    skill and the policy all say the closure merges first."""
    moment(tree, overview=OVERVIEW_OPEN)
    _, text = run(tree)
    assert "in a pull request merged before the one that retires the directory" in (
        flat(text)
    ), text
    assert "merge first" in flat(skill()), (
        "the skill lets a fold close a row and retire its directory in one "
        "pull request, which the CI readers refuse at the merge base"
    )
    assert "in a pull request merged before the one that retires" in document(
        "docs", "the-evidence-ledger.md"
    )


def test_an_open_evidence_todo_row_keeps_a_spec_less_directory(tree):
    moment(tree, todo=OPEN_TODO)
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / MOMENT).exists(), text


def test_an_unreadable_memo_keeps_a_spec_less_directory(tree):
    """A section this cannot read is a count it does not know, never zero."""
    moment(tree, overview="# x — overview\n\n## Not checked\n")
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / MOMENT).exists(), text
    assert "cannot be read" in text, text


def test_a_row_anchored_inside_a_rule_arm_directory_keeps_it(tree):
    """Phase 1's guard over the widened set: the rule arm may not reopen
    #511 the moment it ships."""
    moment(tree)
    anchor(
        tree,
        f'| a moment\'s claim | `seal/specs/{MOMENT}/routing.md#"# {MOMENT} — routing"@abcdef12` | read | 2026-01-01 | |',
        "| one | `hooks/a.py#one@aaaaaaaa` | read | 2026-01-01 | |",
    )
    # Round 1's finding 5: the report does not list it under the heading
    # that says `settle --retire` removes what it lists.
    _, report = run(tree)
    assert "retired by the rule" not in report, report
    assert "0 to retire by the rule" in report, report
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert (tree / "seal" / "specs" / MOMENT).exists(), text
    assert "a moment's claim" in text, text


def test_an_unreleased_spec_less_directory_is_not_a_candidate(tree):
    item = tree / "seal" / "specs" / MOMENT
    item.mkdir()
    (item / "routing.md").write_text("# routing\n", encoding="utf-8")
    _, text = run(tree, "--retire")
    assert item.exists(), text


def test_the_report_lists_what_a_retirement_would_take(tree):
    """D1's table: the command reports by itself the open memo rows in what
    it would retire, the paths outside `seal/specs/` that cite into it, and the
    `tests/` files that read `seal/specs` — the three things #514's frame
    found by hand."""
    fold(tree, "1700000001-alpha")
    (tree / "seal" / "specs" / "1700000001-alpha" / "overview.md").write_text(
        OVERVIEW_OPEN, encoding="utf-8"
    )
    moment(tree)
    (tree / "docs" / "cites.md").write_text(
        "See `seal/specs/1700000001-alpha/spec.md` for the decision.\n"
        f"And `seal/specs/{MOMENT[:11]}…/routing.md` for the moment.\n"
        "A marker <!-- specs/1700000002-beta --> and a bare 1700000002-beta.\n",
        encoding="utf-8",
    )
    (tree / "tests").mkdir()
    (tree / "tests" / "test_reads.py").write_text(
        'SPECS = "seal/specs"\n', encoding="utf-8"
    )
    git(tree, "add", "--", "docs", "tests")
    git(tree, "commit", "-qm", "citations")
    _, text = run(tree)
    takes = text.split("what a retirement here would take with it")[1]
    assert "a claim nobody ran" in takes, text
    assert "docs/cites.md:1" in takes, text
    assert "docs/cites.md:2" in takes, "an abbreviated path is a citation too"
    assert "1700000002-beta" not in takes, "a marker or a bare id is not a path"
    assert "tests/test_reads.py" in text.split("checks that read")[1], text


@pytest.mark.parametrize("ref", [None, "HEAD"])
def test_the_predicate_asks_every_condition_itself(tree, ref):
    """`settle` checks `spec.md` and the evidence-todo guard before the
    predicate can decide, so through `settle` alone the predicate's own
    conditions are never seen. The CI readers ask it of a merge-base where
    neither check has run, so each condition is asked here directly, of the
    working tree and of a ref."""
    reader = settle.load(settle.READER, "specseal_unverified_reader_rule")
    moment(tree, overview=OVERVIEW_CLOSED)
    moment(tree, name="1700000007-with-todo", todo=OPEN_TODO)
    moment(tree, name="1700000008-with-memo", overview=OVERVIEW_OPEN)
    root = str(tree)
    assert reader.retired_by_rule(root, ref, f"seal/specs/{MOMENT}")
    assert not reader.retired_by_rule(root, ref, "seal/specs/1700000001-alpha"), (
        "a directory holding a spec.md read as a rule retirement"
    )
    assert not reader.retired_by_rule(root, ref, "seal/specs/1700000007-with-todo")
    assert not reader.retired_by_rule(root, ref, "seal/specs/1700000008-with-memo")
    assert not reader.retired_by_rule(root, ref, "seal/specs/1700009999-nowhere"), (
        "a directory that never existed read as retired by the rule"
    )
    # Round 1's finding 3: a spec an earlier commit deleted was still written.
    dropped = moment(tree, name="1700000009-spec-dropped")
    (dropped / "spec.md").write_text("# a spec\n\nA rule.\n", encoding="utf-8")
    git(tree, "add", "--", "seal/specs/1700000009-spec-dropped")
    git(tree, "commit", "-qm", "a spec")
    git(tree, "rm", "-q", "seal/specs/1700000009-spec-dropped/spec.md")
    git(tree, "commit", "-qm", "the spec, dropped")
    assert not reader.retired_by_rule(
        root, ref, "seal/specs/1700000009-spec-dropped"
    ), "a directory whose spec.md an earlier commit deleted read as one that wrote none"


def test_the_predicate_is_what_settle_asks(tree, monkeypatch):
    """`plan.md` §*What breaks in six months*: one predicate, asked by every
    reader. With it answering False, the rule arm lists nothing."""
    moment(tree)
    reader = settle.load(settle.READER, "specseal_unverified_reader")
    real_load = settle.load
    monkeypatch.setattr(reader, "retired_by_rule", lambda root, ref, d: False)
    monkeypatch.setattr(
        settle,
        "load",
        lambda path, name: reader if path == settle.READER else real_load(path, name),
    )
    _, text = run(tree, "--retire")
    assert (tree / "seal" / "specs" / MOMENT).exists(), text


def test_the_documents_say_a_spec_less_directory_is_retired_by_the_rule():
    """§14's half of D3. The policy said such an item *is kept by name*, and
    the skill offered it as *yours to place*; both are overturned, and the one
    condition the frame added is stated where the owner can overturn it."""
    policy = document("docs", "the-evidence-ledger.md")
    assert "and it is kept by name" not in policy, (
        "the policy still keeps a spec-less directory by name"
    )
    assert "it is retired by that rule, with no marker" in policy
    assert "nothing in the record may still be open" in policy
    assert "a judgment the repository owner may overturn" in policy
    text = flat(skill())
    assert "A released work item with no `spec.md` is not yours to place." in text
    assert "*retired by the rule*" in text and "*kept by the rule*" in text
    assert "The rule arm is not an exception" in text
    for edition in ("README.md", "README.ko.md"):
        assert "`spec.md`" in document(edition).split("`settle [--retire]`")[1][:900], (
            f"{edition}'s cheat-sheet row does not name the rule arm"
        )


def test_a_marker_quoted_in_prose_is_not_a_fold_record(tree):
    """The line anchor `fold_ledger.py#is_marked` already pays for. Every
    document describing the convention quotes the marker's shape inline."""
    (tree / "docs" / "how.md").write_text(
        "Each sentence carries `<!-- specs/1700000001-alpha -->` above it.\n",
        encoding="utf-8",
    )
    _, text = run(tree)
    assert "folded already" not in text, text
    code, _ = run(tree, "--retire")
    assert code == 1


# --- the reader's own rules ------------------------------------------------


@pytest.mark.parametrize(
    "paths, expected",
    [
        ([], (None, "no ledger row")),
        (["tests/test_a.py"], (None, "tests only")),
        (["hooks/a.py", "tests/test_a.py"], ("hooks/a.py", None)),
        (["hooks/b.py", "hooks/a.py", "hooks/a.py"], ("hooks/a.py", None)),
        # A tie is broken by path order, so the same input always gives the
        # same segment — a grouping that depends on dict order cannot be
        # compared with the run before it.
        (["hooks/b.py", "hooks/a.py"], ("hooks/a.py", None)),
    ],
)
def test_the_segment_rule(paths, expected):
    assert settle.segment_of(paths) == expected


def test_a_coordinate_is_read_out_of_a_row(tree):
    rows = settle.coordinates(str(tree))
    assert rows["1700000001-alpha"] == ["hooks/a.py", "hooks/a.py", "tests/test_a.py"]
    assert rows["1700000002-beta"] == ["tests/test_b.py"]


def test_rows_above_the_first_marker_belong_to_no_work_item(tree):
    """The ledger's own header says the areas above the folded sections are
    the rows from before the fragments existed. Attributing them to whichever
    work item happens to be marked first would give that item a segment it
    never wrote a row about."""
    rows = settle.coordinates(str(tree))
    assert "hooks/old.py" not in [p for paths in rows.values() for p in paths]


RELEASE_SECTION = """## 0.2.0 — 2026-01-02

<!-- specs/1700000002-beta -->
### 1700000002-beta

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| c | `hooks/b.py#thing@ffffffff` | read | 2026-01-01 | |
"""


def test_a_release_file_is_read_as_well_as_the_gathered_ledger(tree):
    """#547, S4. A release file is the section byte for byte — one `## `
    line, then the markers — so the loop that attributes `seal/ledger.md`'s
    rows attributes a release file's rows the same way. Red before
    `coordinates` opened `seal/releases/*.md`: beta stayed tests-only."""
    release = tree / "seal" / "releases" / "0.2.0.md"
    release.parent.mkdir()
    release.write_text(RELEASE_SECTION, encoding="utf-8")
    rows = settle.coordinates(str(tree))
    assert rows["1700000002-beta"] == ["tests/test_b.py", "hooks/b.py"], rows
    _, text = run(tree)
    assert "hooks/b.py" in text, text
    assert "1700000002-beta  (tests only)" not in text, text


def test_a_fragment_is_read_as_well_as_the_gathered_ledger(tree):
    fragment = tree / "seal" / "ledger"
    fragment.mkdir()
    (fragment / "1700000002-beta.md").write_text(
        "| c | `hooks/b.py#thing@ffffffff` | read | 2026-01-01 | |\n", encoding="utf-8"
    )
    _, text = run(tree)
    assert "hooks/b.py" in text, text
    assert "1700000002-beta  (tests only)" not in text, text


def test_the_checks_can_fail():
    """A grouping that answered for everything would make every case above
    vacuous, and so would a guard that found no row open."""
    assert settle.segment_of([])[0] is None
    assert settle.open_rows(CLEAN_TODO) == []
    assert len(settle.open_rows(OPEN_TODO)) == 1


# --- what ships ------------------------------------------------------------


def test_the_command_is_reachable_by_the_name_a_document_gives_it():
    """A6. The pair rule is `tests/test_a_document_that_names_a_script_says_
    how_to_reach_it.py`'s; this is the instance, asked here so a missing twin
    names this work item rather than a parametrisation."""
    for name in ("settle", "settle.cmd"):
        assert os.path.isfile(os.path.join(ROOT, "bin", name)), name
    assert os.access(os.path.join(ROOT, "bin", "settle"), os.X_OK), (
        "`bin/settle` ships without its executable bit, so the command "
        "resolves on PATH and then refuses"
    )


def test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback(tmp_path):
    """`spec_from_file_location` hands back a spec for any path ending in
    `.py`, present or not, so a missing sibling reaches `exec_module` and dies
    with `FileNotFoundError` — which is what the rider on
    `skills/code-review/scripts/round_record.py#load` is still waiting for
    somebody to fix. This copy arrives repaired, and this is the case that
    keeps it repaired."""
    with pytest.raises(SystemExit) as raised:
        settle.load(str(tmp_path / "not-here.py"), "absent")
    assert "not-here.py" in str(raised.value), raised.value
    assert "fold record" in str(raised.value), (
        "the refusal does not say what the missing file was for"
    )


# --- what the skill has to say ---------------------------------------------

SKILL = os.path.join(ROOT, "skills", "settle", "SKILL.md")


def skill():
    with open(SKILL, encoding="utf-8") as f:
        return f.read()


def flat(text):
    return " ".join(text.split())


def test_the_skill_names_the_floors_a_fold_has_to_answer():
    """A11. `docs/one-root-by-lifetime.md` §*The dependency rule* names two
    readers and the real list is longer — fourteen test modules read this
    repository's own corpus and at least six carry a population floor. A
    session that folds without answering them removes the population its own
    suite was asserting over, and the commit under review is what broke it.

    The three answers are named because the fourth — lowering the floor until
    the run passes — is the one that turns a check into a comment."""
    text = flat(skill())
    assert "population floor" in text, (
        "the skill never tells a session that its own checks read the corpus"
    )
    assert "is not the whole list" in text, (
        "the skill lets `docs/one-root-by-lifetime.md`'s two readers stand as "
        "the whole list, which is what makes a fold turn a suite red"
    )
    for answer in ("retire the case", "re-point it at a fixture corpus", "decline"):
        assert answer in text, f"the skill does not offer `{answer}`"


def test_the_skill_says_who_judges_and_who_reads():
    """G1. A session that reads this and then lets the command decide which
    sentence is still true has read the one thing it may not do."""
    text = flat(skill())
    assert "moves and does not verify" in text, text[:200]
    assert "The command reads and groups; you judge and write." in text


def test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row():
    """#517's D1, and the sentence it retired. The skill used to hand a fold
    branch a `survivors.md` range-row to copy, anchored on the range and on
    the work item whose directory held it — and a fold with no work item has
    no directory to hold one. The sweep leaves a retired directory out of its
    range instead, so the row shape is gone and the rule that replaced it is
    what a fold session reads."""
    text = flat(skill())
    assert "| Range | Grounds |" not in text, "the skill still hands a fold a range row"
    assert "No `survivors.md` row." in text
    assert "## A fold is not a work item" in skill()
    assert "A fold opens no directory under `seal/specs/`" in text
    assert "`: '[no-review]';`" in text, "the skill does not say how a fold commits"
    assert "reviewed at its pull request" in text
    assert "keep a log of folds" in text


def test_the_skill_says_what_a_fold_does_to_the_ledger():
    """Q3's default. *Nothing in `seal/ledger.md` moves* was false of both
    folds — one removed rows, the other re-verified four — and it disagreed
    with the policy the fold works under."""
    text = flat(skill())
    assert "Nothing in `seal/ledger.md` moves" not in text
    assert "`seal/ledger.md` changes only by removal and re-verification." in text
    assert "A fold appends nothing" in text
    policy = document("docs", "the-evidence-ledger.md")
    assert "A fold is not a work item, and it adds nothing to the ledger." in policy


def test_the_skill_says_the_retirement_is_the_second_half_of_the_fold():
    text = flat(skill())
    assert "second half of the fold and never its own act" in text


def test_the_skill_states_the_destination_rule():
    """G2: merge into a document that exists, create one only for a new area,
    newest wins, and every folded sentence carries its work item's comment."""
    text = flat(skill())
    assert "Merge into a document that already exists" in text
    assert "newest work item wins" in text
    assert "<!-- specs/" in text
    assert "no `docs/policy/` directory" in text


def test_the_skill_says_it_fails_no_build():
    """G5. `settle` is invoked, never triggered — the ticket's own *Not this*."""
    text = flat(skill())
    assert "It is invoked, never triggered" in text
    assert "It does not fail a build." in text


# --- A9: no document still describes a `settle` that does not exist --------


def document(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return flat(f.read())


@pytest.mark.parametrize(
    "parts", [("seal", "README.md"), ("templates", "seal-README.md")]
)
def test_the_seal_readme_says_the_step_exists(parts):
    """Both editions of the same file, which
    `tests/test_first_setup_asks_once.py` holds byte for byte. It has said a
    work item "waits until a later `settle` folds it" since the root existed,
    and a reader who went looking for the step found nothing."""
    text = document(*parts)
    assert "That step exists now" in text, (
        f"{'/'.join(parts)} still describes a `settle` that has not been built"
    )
    assert "skills/settle/SKILL.md" in text and "settle --retire" in text
    assert "A fold is not a work item and opens no directory here." in text, (
        f"{'/'.join(parts)} does not say a fold opens no work item (#517)"
    )
    assert "wrote no `spec.md` and holds nothing open" in text


def test_the_implement_skill_names_the_one_writer_of_docs():
    """G6. The layout table said `docs/` is *never created here*, and that
    sentence stopped being true the moment `settle` wrote there —
    `docs/one-root-by-lifetime.md` §*Decided after the thread* listed it as a
    sentence to correct before the step existed to correct it."""
    text = document("skills", "implement", "SKILL.md")
    assert "never created here" not in text, (
        "the layout table still says `docs/` is never created here"
    )
    assert "The one writer that does is `settle`" in text


def test_the_handoff_protocol_separates_the_two_deadlines():
    """Closing before the merge is the implementer's and is the protocol's;
    retiring after the release is `settle`'s and is the implementation's. The
    document said the directory outlives the merge and is not deleted, with
    nothing distinguishing the deadline draft 0.1 got wrong from the one that
    comes years later."""
    text = document("docs", "review-handoff-protocol.md")
    assert "Outliving the merge is not outliving the release" in text
    assert "It is deleted eventually, and that is a different deadline." in text


@pytest.mark.parametrize(
    "parts, heading",
    [
        (("docs", "one-root-by-lifetime.md"), "## Decided when `settle` was built"),
        (("docs", "one-root-by-lifetime.ko.md"), "## `settle` 을 만들면서 정해진 것"),
    ],
)
def test_the_design_record_takes_the_later_decision_as_a_dated_section(parts, heading):
    """`tests/test_no_document_names_the_old_roots.py#DESIGN_RECORD`
    classifies this document as a record of a moment, and a record of a moment
    is not rewritten. The shape it already uses for a later decision is a
    dated section, and both editions take one."""
    text = document(*parts)
    assert heading in text, f"{'/'.join(parts)} carries no dated section for #458"
    assert "2026-09-22" in text
    assert "2026-09-02" in text, (
        "the dated section no longer says which text it is leaving alone"
    )


@pytest.mark.parametrize(
    "parts, heading",
    [
        (
            ("docs", "one-root-by-lifetime.md"),
            "## Decided when the fold stopped being a work item (2026-09-23)",
        ),
        (
            ("docs", "one-root-by-lifetime.ko.md"),
            "## fold 가 작업 항목이 아니게 되면서 정해진 것 (2026-09-23)",
        ),
    ],
)
def test_the_design_record_takes_d1_as_a_dated_section(parts, heading):
    """#517's D1 overturns the 2026-09-22 row that made the fold its own work
    item, and a record of a moment takes the overturning as a new dated
    section rather than an edit to the row."""
    text = document(*parts)
    assert heading in text, f"{'/'.join(parts)} carries no dated section for #517"
    later = text.split(heading, 1)[1]
    assert "2026-09-02" in later and "2026-09-22" in later, (
        "the new section does not say which two records it leaves alone"
    )
    assert "[no-review]" in later


DATED_SECTIONS = (
    ("## Decided when `settle` was built", "## `settle` 을 만들면서 정해진 것"),
    (
        "## Decided when the fold stopped being a work item",
        "## fold 가 작업 항목이 아니게 되면서 정해진 것",
    ),
)


def section(flat_text, heading):
    """A dated section of a flattened document, from its heading to the next."""
    rest = flat_text.split(heading, 1)[1]
    return rest.split(" ## ", 1)[0]


def test_both_editions_took_the_same_decisions():
    """`CONTRIBUTING.md` requires the two editions to move together, and a
    mirror drifts one edit at a time. The rows are prose in two languages, so
    what is compared is that each edition's section has as many rows as the
    other's."""
    en = document("docs", "one-root-by-lifetime.md")
    ko = document("docs", "one-root-by-lifetime.ko.md")
    # Each section is read up to the next `## ` heading, so a later dated
    # section is compared with its own twin rather than counted into this
    # one's (#517 added the second).
    for en_heading, ko_heading in DATED_SECTIONS:
        sections = (section(en, en_heading), section(ko, ko_heading))
        rows = tuple(s.count("|---|---|---|") for s in sections)
        assert rows == (1, 1), (en_heading, rows)
        counted = tuple(s.count(" | ") for s in sections)
        assert counted[0] == counted[1], (
            f"{en_heading}: the English section holds {counted[0]} cells and "
            f"the Korean {counted[1]} — one edition took a decision the other "
            "did not"
        )


# --- what the plugin says it ships -----------------------------------------


def test_the_release_checklist_carries_the_by_hand_step():
    """G5. `settle` is invoked and never triggered, so the only thing that
    makes it happen is a line in the list somebody works down on the day.

    It is also the only place that says the step is a branch of its own: step
    2 is two dry runs a person reads and one mechanical commit, and folding
    writes policy prose."""
    text = document("docs", "release-checklist.md")
    assert "settle --retire" in text, "the checklist never names the step"
    assert "separate branch and a separate pull request" in text, (
        "the checklist does not say the fold is its own branch, which is what "
        "keeps a judgment act out of the release-preparation commit"
    )
    assert "A fold is not a work item" in text, (
        "the checklist does not say the fold opens no work item"
    )
    assert "range-row" not in text, "the checklist still owes a fold a range row"
    assert "skills/settle/SKILL.md" in text


@pytest.mark.parametrize("edition", ["README.md", "README.ko.md"])
def test_both_cheat_sheets_carry_the_command(edition):
    """The count and the name are derived by
    `tests/test_chain_hooks_hardening.py`; what nothing derives is the row a
    reader actually types from. `CONTRIBUTING.md` requires the two editions to
    move together and the hygiene workflow only warns about it."""
    text = document(edition)
    assert "`settle [--retire]`" in text, (
        f"{edition}'s cheat sheet has no row for the command"
    )


# --- round 1's fixes -------------------------------------------------------


def test_local_mode_is_refused_rather_than_read_as_an_empty_repository(tmp_path):
    """Round 1, finding 3. `settle` looked only at `<root>/seal/specs`, so a
    local-mode repository holding work items was told it had none — and the
    sentence written for local mode, behind the `--released-at` refusal, could
    never be printed because this check fired first and always.

    Resolving the root is half of it. With the root found, the run would go on
    to ask git which work items are released, git would answer with none — an
    uncommitted root has no path in any tree — and the report would say there
    is nothing to fold. That is the quiet zero by another door, so the state
    is named instead."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    git(repo, "init", "-q")
    item = repo / ".git" / "seal" / "specs" / "1700000001-alpha"
    item.mkdir(parents=True)
    (item / "spec.md").write_text("# a\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "HEAD"],
        capture_output=True,
        encoding="utf-8",
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "which is local mode" in r.stderr, r.stderr
    assert "seal mode shared" in r.stderr, (
        "the refusal does not say how to get out of it"
    )
    assert "has nothing to settle" not in r.stderr, (
        "a repository holding a work item is still being told it has none"
    )


def test_a_repository_with_no_root_at_either_place_says_so(tmp_path):
    """The other arm of the same resolution, kept apart from local mode
    because the two are different states and used to share one sentence."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    r = subprocess.run(
        [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "HEAD"],
        capture_output=True,
        encoding="utf-8",
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "at either place" in r.stderr, r.stderr


def test_a_held_item_is_skipped_and_named_even_when_its_fold_is_recorded(tree):
    """Round 1, finding 4. `spec.md` G3 says an item with an open
    `evidence-todo.md` row is skipped AND NAMED, never folded. An item that
    was both folded and held was named under *waiting to be retired* — which
    tells the reader to run the command that will refuse it — while the
    summary counted it `0 skipped`."""
    fold(tree, "1700000003-gamma")
    code, text = run(tree)
    assert code == 0, text
    assert "1 skipped" in text, text
    listed = text.split("\nskipped —")
    assert len(listed) == 2, f"the held item is in no skipped list: {text}"
    assert "1700000003-gamma" in listed[1], text
    assert "folded already" not in text, (
        "the held item is still offered to `--retire`, which will refuse it"
    )


def test_a_complete_retirement_is_not_reported_as_nothing_ever_folded(tree):
    """Round 1, finding 5. A marker in `docs/` whose directory is already gone
    leaves the survey nothing to list, so the next run said nothing had ever
    been folded — the one thing the tree plainly contradicts, and the state
    every run of `docs/release-checklist.md` step 2b ends in. The exit code
    carried the same conflation: the docstring says exit 1 is a refusal, and
    nothing refused this one."""
    fold(tree, "1700000001-alpha")
    first, _ = run(tree, "--retire")
    assert first == 0
    code, text = run(tree, "--retire")
    assert code == 0, text
    assert "The fold is complete." in text, text
    assert "none of them has been folded yet" not in text, text


def test_an_untouched_tree_still_says_nothing_has_been_folded(tree):
    """The other state, kept apart from the one above. A repository where
    nobody has folded anything is a refusal, because `--retire` was asked for
    and there was nothing it could do."""
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert "none of them has been folded yet" in text, text


# --- round 2's fixes -------------------------------------------------------


def test_a_marked_item_still_on_disk_is_not_the_fold_being_complete(tree):
    """Round 2, finding 2. The arm fired on `if marked:`, which asks only
    whether `docs/` records any fold at all, while the sentence it prints
    asserts something narrower — that none of the marked items still has a
    directory. A reader who acts on *the fold is complete* stops looking, and
    the directory the marker named stays in the tree.

    The state is reachable whenever a marker is written for a work item that
    is not present at `--released-at`: a policy absorbing work that has not
    merged yet, or a run pointed at an older ref."""
    fold(tree, "1700000004-delta")  # present on disk, never committed
    code, text = run(tree, "--retire")
    assert code == 1, text
    assert "The fold is complete." not in text, text
    assert "1700000004-delta" in text, text
    assert "still under seal/specs/" in text, text
    assert (tree / "seal" / "specs" / "1700000004-delta").exists()


def test_the_fold_is_complete_still_prints_when_it_is(tree):
    """The arm the one above narrowed, kept honest: with every marked item's
    directory actually gone, the sentence is true and the exit code is 0."""
    fold(tree, "1700000001-alpha")
    assert run(tree, "--retire")[0] == 0
    code, text = run(tree, "--retire")
    assert code == 0, text
    assert "The fold is complete." in text, text


def test_a_fenced_marker_in_the_ledger_opens_no_section(tree):
    """Round 2, finding 5 — round 1's finding 1 one function over, and the
    same cause: a line anchor is not a test that the line is live.

    Closed by the reader this module already loads rather than by a third copy
    of the rule. `.github/scripts/fold_ledger.py` carries the second copy and
    #487 is the ticket for that pair; writing a third here would be the same
    ticket again."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\nAn example of the convention:\n\n```markdown\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n"
        + "```\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/quoted.py" not in rows["1700000002-beta"], rows["1700000002-beta"]
    assert rows["1700000001-alpha"] == ["hooks/a.py", "hooks/a.py", "tests/test_a.py"]
    # The fenced block sits after gamma's section, so a reader without fence
    # tracking would have attributed the quoted coordinate to whichever id the
    # quotation names — which is the defect, not merely a miscount.
    _, text = run(tree)
    assert "hooks/quoted.py" not in text, text


def test_a_parked_marker_in_the_ledger_opens_no_section(tree):
    """Round 3, finding 2 — the other way a line stops being live, which
    `folded_items` had and `coordinates` did not. A marker inside a
    commented-out draft opened a section and took the draft's coordinate with
    it, so `segment_of` grouped that work item by a coordinate nobody wrote
    for it. Closed by reading through the one `live_lines` the reader owns,
    never by asking the comment state of the raw text — the case after this
    one is why."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"
        + "| q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| r | `hooks/reopened.py#thing@66666666` | read | 2026-01-01 | |\n"
        + "-->\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert all("hooks/quoted.py" not in paths for paths in rows.values()), dict(rows)
    # The parked marker opened no section; the real one after the draft did.
    assert rows["1700000002-beta"] == ["tests/test_b.py", "hooks/after.py"], rows
    # HTML comments do not nest, so the parked marker's own `-->` closed the
    # draft: the row after it is live again and falls to the section that was
    # open. That is `comment_scan`'s rule, which `seal/ledger.md` pins for
    # every record reader, and not a rule of this module.
    assert rows["1700000003-gamma"] == ["hooks/a.py", "hooks/reopened.py"], rows


def test_a_closer_quoted_in_prose_still_closes_a_parked_draft(tree):
    """The span pass blanks a whole span, delimiters and all, so a draft's
    closing delimiter quoted in a row or a sentence disappeared before the
    comment state was asked and the draft never closed. The next real section
    marker then began inside the draft and opened nothing — and because a
    marker carries a closer of its own, the row below it came back live and
    went to whichever section was open. Round 3's finding 2 again, arriving
    through the fix for it. Inside a comment nothing is markdown, so the
    quotation is not one and the pass must leave it alone."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the quoted closer below is what ends it
        + "the draft ends with `-->` said in prose\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" in rows["1700000002-beta"], dict(rows)
    assert "hooks/after.py" not in rows["1700000003-gamma"], dict(rows)


def test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in(tree):
    """The other half of the shape above. A span quoting a COMPLETE comment
    holds the opener, so a pass that blanks the span blanked it whole and the
    quoted closing delimiter went with it — the draft stayed open, the next
    real section marker began inside it and opened nothing, and the row below
    went to whichever section was open. Inside a comment nothing is markdown,
    so what the pass owes the comment scan is the opener blanked and the
    closer left where it stands: the DELIMITER, not the span around it."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the whole comment quoted below ends it
        + "the draft ends with `<!-- a note -->` quoted whole\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" in rows["1700000002-beta"], dict(rows)
    assert "hooks/after.py" not in rows["1700000003-gamma"], dict(rows)


def test_an_opener_after_a_quoted_closer_still_parks_the_marker_below(tree):
    """The residue of the shape above, in the expensive direction. A pass
    that blanked code spans before the comment state was read could not know
    that inside a parked draft the backticks are not a span at all: the first
    closing delimiter ends the draft and the opener after it re-opens one.
    Blanking that opener read a parked marker as a fold record, and
    `settle --retire` removed the directory at exit 0 with nothing having
    absorbed it. The scan carries the comment state as it goes, so inside a
    draft it reads no spans at all and the question does not arise."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the span below ends it and re-opens it
        + "prose that quotes `--> and then <!--` on one line\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n"
        + "-->\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" not in rows.get("1700000002-beta", []), dict(rows)


def test_an_indented_example_row_is_counted_and_the_reader_says_so(tree):
    """The third quotation, pinned as read rather than as fixed. `blank_fences`
    knows the two fenced forms and markdown's indented code block is neither,
    so a fragment showing its example row indented has that example counted as
    its own coordinate. Widening the fence reader would move `readable`,
    `check_text`, `round_record.py` and the review-history guard at once —
    measured, it reddens a record reader's continuation case with no stake in
    this rule. `tests/test_chain_hooks.py#reader_blanking_passes` is not that
    refusal: it reads the calls `readable` makes by name and a widened
    `blank_fences` leaves them unchanged.
    The case exists so a session that widens it one day is told what
    this one decided, and why it decided it in the docstring instead of in the
    code."""
    fragments = tree / "seal" / "ledger"
    fragments.mkdir()
    (fragments / "1700000001-alpha.md").write_text(
        "| r | `hooks/frag.py#real@12345678` | read | 2026-01-01 | |\n"
        "\nAn example, indented rather than fenced:\n\n"
        "    | q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))["1700000001-alpha"]
    assert "hooks/frag.py" in rows, rows
    assert "hooks/quoted.py" in rows, (
        "an indented example is read as the fragment's own coordinate; the "
        "docstring says so on purpose, so change both or neither"
    )


def test_an_opener_quoted_inside_a_code_span_parks_nothing(tree):
    """Why the obvious closure is wrong. A ledger row's anchor quotes the text
    it is anchored to, and that text is often a comment: `seal/ledger.md`
    carries four anchors holding `<!--` with no closer on the line, and asking
    the comment state of the file as it stands parks every section below the
    first of them — three real markers lost, round 3's measurement and the
    framer's at `3cdfd8ad`. So `live_lines` carries the code-span state as it
    scans and an opener inside a span opens nothing, while the line comes back
    unchanged — the coordinate lives inside backticks too."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + '| four | `docs/x.md#"<!-- a quoted opener"@ffffffff` | read | 2026-01-01 | |\n'
        + "\n<!-- specs/1700000005-epsilon -->\n"
        + "### 1700000005-epsilon\n"
        + "| one | `hooks/e.py#one@12121212` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert rows["1700000005-epsilon"] == ["hooks/e.py"], dict(rows)
    assert "docs/x.md" in rows["1700000003-gamma"], rows["1700000003-gamma"]


def real_ledgers():
    """`seal/ledger.md` and every `seal/releases/*.md` — where a folded
    section stands, before the one-time split and after it (#547)."""
    return [
        os.path.join(ROOT, "seal", "ledger.md"),
        *sorted(glob.glob(os.path.join(ROOT, "seal", "releases", "*.md"))),
    ]


def test_the_rule_over_this_repositorys_ledger_loses_no_section():
    """The same fact over the real corpus: the ids `coordinates` sections are
    the ids `blank_fences` alone would section, and there are some. Set
    equality rather than a number — the number grows at every release fold,
    and a floor over the repository's own records is the shape
    `skills/settle/SKILL.md` §3 names as the expensive one. With the span pass
    removed this reports three ids missing."""
    reader = settle.load(settle.READER, "specseal_unverified_reader_a4")
    sectioned = set()
    for path in real_ledgers():
        with open(path, encoding="utf-8") as f:
            fenced = reader.blank_fences(f.read().split("\n"))
        sectioned |= {m.group(1) for m in map(settle.MARKER_LINE_RE.match, fenced) if m}
    fragments = {
        os.path.basename(path)[: -len(".md")]
        for path in glob.glob(os.path.join(ROOT, "seal", "ledger", "*.md"))
    }
    assert sectioned, "the ledger carries no section marker"
    assert set(settle.coordinates(ROOT)) == sectioned | fragments


def test_no_section_of_this_repositorys_ledger_loses_a_coordinate():
    """The invariant every formulation of the liveness rule has had to keep,
    and the one a case did not reach until round 5's fix pass.

    Sectioning by the fence-only reading is what `seal/ledger.md` meant
    before any comment or code-span rule existed, and the file carries no
    fence, so that reading is the ground truth for it. A rule that parks a
    row inside a section does not lose the section — the id set is unchanged
    and `test_the_rule_over_this_repositorys_ledger_loses_no_section` stays
    green — it loses the row, and `segment_of` then groups that work item by
    what is left. Measured while building this: bounding the crossing
    reading by a blank line alone keeps all 94 markers and all 83 ids and
    still takes three work items from 12, 57 and 29 coordinates to 5, 40 and
    19."""
    reader = settle.load(settle.READER, "specseal_unverified_reader_coords")

    def sectioned(pairs):
        out, current = {}, None
        for line, live in pairs:
            if not live:
                continue
            marker = settle.MARKER_LINE_RE.match(line)
            if marker:
                current = marker.group(1)
                continue
            if line.startswith("## "):
                current = None
            if current:
                out.setdefault(current, []).extend(
                    m.group("path") for m in settle.COORDINATE_RE.finditer(line)
                )
        return out

    fence_only, live = {}, {}
    for path in real_ledgers():
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")
        pairs = [(line, True) for line in reader.blank_fences(lines)]
        for key, paths in sectioned(pairs).items():
            fence_only.setdefault(key, []).extend(paths)
        for key, paths in sectioned(reader.live_lines(lines)).items():
            live.setdefault(key, []).extend(paths)
    assert live == fence_only
    assert sum(len(v) for v in fence_only.values()) > 1000, "the ledger went empty"


def test_a_fragments_quoted_coordinates_are_not_the_fragments_own(tree):
    """Round 3, finding 3 — the other half of round 2's finding 5.
    `coordinates` reads two places and the fix changed both; only the ledger
    half had a case, so reverting the fragment loop to a whole-file `finditer`
    turned nothing red. A fragment is where a work item explains its own rows,
    so a fenced example row or a parked draft of one is more plausible there
    than in the shared file, not less."""
    fragments = tree / "seal" / "ledger"
    fragments.mkdir()
    (fragments / "1700000001-alpha.md").write_text(
        "| r | `hooks/frag.py#real@12345678` | read | 2026-01-01 | |\n"
        "\nAn example of the convention:\n\n```markdown\n"
        "| q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n"
        "```\n"
        "<!-- a draft, parked\n"
        "| p | `hooks/parked.py#thing@77777777` | read | 2026-01-01 | |\n"
        "-->\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))["1700000001-alpha"]
    assert "hooks/frag.py" in rows, rows
    assert "hooks/quoted.py" not in rows, rows
    assert "hooks/parked.py" not in rows, rows


def test_an_opted_out_repository_is_told_which_state_it_is_in(tmp_path):
    """Round 2, finding 7. `home_at` answers `""` for two states — no root at
    either place, and a repository that opted out with the scratch marker —
    and they were given one sentence, so a tree holding work items was told it
    had none. That is finding 3's defect through another door."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    git(repo, "init", "-q")
    item = repo / "seal" / "specs" / "1700000001-alpha"
    item.mkdir(parents=True)
    (item / "spec.md").write_text("# a\n", encoding="utf-8")
    (repo / ".git" / "specseal-scratch").write_text("", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "HEAD"],
        capture_output=True,
        encoding="utf-8",
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "has opted out" in r.stderr, r.stderr
    assert "specseal-scratch" in r.stderr, r.stderr
    assert "has nothing to settle" not in r.stderr, (
        "a repository holding a work item is still being told it has none"
    )


def test_a_directory_of_the_markers_name_is_not_an_opt_out(tmp_path):
    """Round 3, finding 1. `hooks/optin.py#home_at` reads the scratch marker
    with `os.path.isfile` and says why: `os.path.exists` also accepted a
    DIRECTORY of that name, and one created once turned every gate off in
    every clone. The refusal here asked `exists`, so a repository holding a
    directory of that name and no root was told it had opted out and to delete
    "that file" — and no gate reads a directory as the opt-out, so every clause
    of that sentence was false. The three readers of one marker answer alike."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / ".git" / "specseal-scratch").mkdir()
    r = subprocess.run(
        [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "HEAD"],
        capture_output=True,
        encoding="utf-8",
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "has no seal/specs/ at either place" in r.stderr, r.stderr
    assert "has opted out" not in r.stderr, (
        "a directory of the marker's name is read as the opt-out, which is the "
        "reading `hooks/optin.py` rejected by name"
    )


def test_the_refusal_path_asks_for_the_common_directory_once(tmp_path, monkeypatch):
    """Round 3, finding 5. `home_at(root)` resolves the common git directory
    for itself, and the opt-out arm then resolved it a second time, although
    `home_at(root, common)` exists for a caller that needs the value too and
    `hooks/optin.py` documents the parameter with the measurement that created
    it. Counted through the module `settle.load` hands `main`, and counted as
    calls rather than processes: on a main worktree the resolver's fast path
    costs no process, so a process count would have said nothing."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    optin = settle.load(settle.OPTIN, "specseal_optin_counted")
    calls, received = [], []
    common_dir, home_at = optin.git_common_dir, optin.home_at

    def counted(root):
        calls.append(root)
        return common_dir(root)

    def recorded(root, common=None):
        received.append(common)
        return home_at(root, common)

    # `home_at` reaches `git_common_dir` through the module global, so the
    # counter sees the resolver's own call as well as `main`'s.
    optin.git_common_dir, optin.home_at = counted, recorded
    real_load = settle.load
    monkeypatch.setattr(
        settle,
        "load",
        lambda path, name: optin if path == settle.OPTIN else real_load(path, name),
    )
    assert settle.main(["--root", str(repo), "--released-at", "HEAD"]) == 2
    assert len(calls) == 1, calls
    assert received == [common_dir(os.path.abspath(str(repo)))], received


def test_the_released_at_refusal_is_about_the_ref_and_nothing_else(tmp_path):
    """Round 2, finding 4. The clause about local mode sat inside a message
    for a different failure and could not fire in the case it described:
    local mode returns before `survey` is ever called."""
    repo = tmp_path / "repo"
    (repo / "seal" / "specs" / "1700000001-alpha").mkdir(parents=True)
    (repo / "seal" / "specs" / "1700000001-alpha" / "spec.md").write_text(
        "# a\n", encoding="utf-8"
    )
    git(repo, "init", "-q")
    r = subprocess.run(
        [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "no/such/ref"],
        capture_output=True,
        encoding="utf-8",
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "does not resolve" in r.stderr, r.stderr
    assert "local mode" not in r.stderr, (
        "the ref refusal still talks about a state it cannot be in"
    )


def test_the_module_and_the_skill_both_say_local_mode_is_refused():
    """Round 2, finding 3 — §14's other half. The exit-code list named three
    causes of exit 2 and there were four, and the one document a session reads
    before it folds said nothing about the refusal at all. A person whose root
    sits under the git directory meets a stop no document predicted."""
    with open(SCRIPT, encoding="utf-8") as f:
        head = f.read().split('"""')[1]
    assert "Exit codes" in head, "the docstring no longer documents exit codes"
    assert "local mode" in head, "exit 2 covers a local-mode root and the list does not"
    assert "opted out" in head, "exit 2 covers the opt-out and the list does not"
    text = flat(skill())
    assert "refuses to run in local mode" in text, (
        "the skill never tells a session that this command stops in local mode"
    )
    assert "seal mode shared" in text, "the skill does not give the way out"


def test_surveys_docstring_does_not_invite_the_mutation_that_reopens_finding_4():
    """Round 2, finding 6. `retire` performs the second traversal `survey`'s
    docstring warned against, and the two contradicted each other — the stale
    half being the one a reader meets first. A pin catches the edit; a
    docstring is what a reader consults before making it."""
    import ast

    with open(SCRIPT, encoding="utf-8") as f:
        tree_ = ast.parse(f.read())
    doc = {
        node.name: ast.get_docstring(node) or ""
        for node in tree_.body
        if isinstance(node, ast.FunctionDef)
    }
    assert "the retirement are both derived from" not in doc["survey"], doc["survey"]
    assert "does not take its candidates from here" in doc["survey"], doc["survey"]
    assert "not taken from `survey`" in doc["retire"], doc["retire"]


# --- G7: an empty seal/specs/ is not one state but two, and both are green --


def settled_repo(tmp_path, keep_empty_dir):
    """A repository whose fold is complete: a `seal/` root with its ledger,
    and `seal/specs/` either empty on disk — the tree `--retire` leaves — or
    absent, which is what a fresh checkout of that commit has."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "one-root.md").write_text("# a policy\n", encoding="utf-8")
    (repo / "seal").mkdir()
    (repo / "seal" / "ledger.md").write_text("# spec-to-code map\n", encoding="utf-8")
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "x@example.com")
    git(repo, "config", "user.name", "x")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "settled")
    if keep_empty_dir:
        (repo / "seal" / "specs").mkdir()
    return repo


@pytest.mark.parametrize("keep_empty_dir", [True, False], ids=["empty", "absent"])
@pytest.mark.parametrize("retire", [False, True], ids=["report", "retire"])
def test_a_settled_root_is_green_and_says_so(tmp_path, keep_empty_dir, retire):
    """G7. After the last retirement a fresh checkout has no `seal/specs/`
    at all and the tree that ran `--retire` has an empty one. Both are the
    state a complete fold reaches, and `settle` used to refuse the first at
    exit 2 — so the command could not run on its own finished work."""
    repo = settled_repo(tmp_path, keep_empty_dir)
    argv = [sys.executable, SCRIPT, "--root", str(repo), "--released-at", "HEAD"]
    r = subprocess.run(
        argv + (["--retire"] if retire else []), capture_output=True, encoding="utf-8"
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "holds no work item" in r.stdout, r.stdout + r.stderr
    assert "A complete fold ends here" in r.stdout, r.stdout
