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


def test_the_skill_carries_the_survivors_row_a_fold_branch_owes():
    """The sweep runs on every pull request into a release branch, and a fold
    reports every sentence of every section it deleted. A branch told nothing
    about the range row turns the check off instead."""
    text = flat(skill())
    assert "| Range | Grounds |" in text, "no range-row shape to copy"
    assert "153" in text, "the measured number that makes the row worth having"
    assert "anchored on the range" in text


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


def test_both_editions_took_the_same_decisions():
    """`CONTRIBUTING.md` requires the two editions to move together, and a
    mirror drifts one edit at a time. The rows are prose in two languages, so
    what is compared is that each edition's section has as many rows as the
    other's."""
    en = document("docs", "one-root-by-lifetime.md")
    ko = document("docs", "one-root-by-lifetime.ko.md")
    rows = (
        en.split("## Decided when `settle` was built")[1].count("|---|---|---|"),
        ko.split("## `settle` 을 만들면서 정해진 것")[1].count("|---|---|---|"),
    )
    assert rows == (1, 1), rows
    counted = tuple(
        text.split(marker)[1].count(" | ")
        for text, marker in (
            (en, "## Decided when `settle` was built"),
            (ko, "## `settle` 을 만들면서 정해진 것"),
        )
    )
    assert counted[0] == counted[1], (
        f"the English section holds {counted[0]} cells and the Korean "
        f"{counted[1]} — one edition took a decision the other did not"
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
