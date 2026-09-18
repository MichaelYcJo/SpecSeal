"""The three helpers five modules now share, and the sentence a person reads.

`git ls-files` lists the index, so a tracked file the working tree has deleted
is on the list and not on disk. Five helpers in this suite used to open every
listed path, and the walk ended at the first of them: no file after it was
read and the rule the walk holds reported nothing (#432, #282).

The repair is `conftest.on_disk`, and the half that needed deciding is what a
case does with the paths it skipped. A sweep that judges what it finds is
strictly better off — on that tree it used to report nothing about any file.
A case that reads the corpus to prove an entry is still ALIVE is not: to it a
skipped file and a deleted entry are the same evidence, so a silent skip buys
it a false alarm. Those decline, through `decline_if_shrunken`.

**The reason string is why this module exists.** It is text a person reads at
a release and acts on, which `skills/agent-contract/SKILL.md` §14 says has to
be pinned in the commit that writes it — and `seal/follow-up.md`'s seventh
row is that omission in an earlier release, a refusal whose second half
nothing held. The three call sites pin their own `what`; the shape is pinned
here, once, because one function produces all three sentences.
"""

import ast
import os
import subprocess
import warnings

import pytest
from conftest import (
    build_tracked_tree,
    decline_if_shrunken,
    git_listing,
    on_disk,
    shrunken_corpus,
)

ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_on_disk_splits_a_listing_by_what_the_tree_actually_has(tmp_path):
    root = build_tracked_tree(
        tmp_path / "r",
        {"a.md": "one\n", "b/c.md": "two\n", "d.md": "three\n"},
        deleted=["b/c.md"],
    )
    present, missing = on_disk(root, ["a.md", "b/c.md", "d.md"])
    assert present == ["a.md", "d.md"]
    assert missing == ["b/c.md"]


def test_on_disk_keeps_the_order_it_was_given(tmp_path):
    """A corpus is walked in the order git listed it, and a refusal naming
    `rel:line` is read against that order."""
    root = build_tracked_tree(tmp_path / "r", {"a.md": "", "b.md": "", "c.md": ""})
    present, missing = on_disk(root, ["c.md", "a.md", "b.md"])
    assert present == ["c.md", "a.md", "b.md"]
    assert missing == []


def test_a_directory_on_the_list_is_not_a_file_that_is_there(tmp_path):
    """`os.path.isfile` rather than `os.path.exists`: a path git named that
    is now a directory has no content to read, and `open` would raise on it
    exactly the way a missing file does."""
    root = build_tracked_tree(tmp_path / "r", {"a.md": "one\n"})
    os.mkdir(os.path.join(root, "b"))
    present, missing = on_disk(root, ["a.md", "b"])
    assert present == ["a.md"] and missing == ["b"]


def test_the_reason_names_every_path_and_what_declined():
    """A count alone is a claim removed from the corpus without a word, which
    `seal/follow-up.md`'s first row calls the one direction a checker of
    claims must not fail in. The reader needs the paths in order to judge
    them by hand."""
    reason = shrunken_corpus(
        ["seal/ledger/two.md", "docs/one.md"], "the KEEP allowlist's liveness check"
    )
    assert "docs/one.md" in reason
    assert "seal/ledger/two.md" in reason
    assert "2 tracked path(s)" in reason
    assert "the KEEP allowlist's liveness check" in reason
    assert "not judging" in reason


def test_the_reason_sorts_the_paths_it_names():
    """The set a caller hands over comes from a walk, so an unsorted reason
    would read differently run to run for the same tree."""
    reason = shrunken_corpus(["b.md", "a.md"], "x")
    assert reason.index("a.md") < reason.index("b.md")


def test_declining_is_silent_when_nothing_is_missing():
    """The guard must not turn a check off on a whole tree, which is the one
    way this repair could report less than the crash it replaces."""
    assert decline_if_shrunken([], "x") is None


def test_declining_raises_the_skip_carrying_that_reason():
    with pytest.raises(pytest.skip.Exception) as declined:
        decline_if_shrunken(["docs/one.md"], "the KEEP allowlist's liveness check")
    assert str(declined.value) == shrunken_corpus(
        ["docs/one.md"], "the KEEP allowlist's liveness check"
    )


def test_the_builder_leaves_a_deleted_file_tracked(tmp_path):
    """The fixture shape itself, because a fixture that staged the removal
    would build the tree this defect is NOT about."""
    root = build_tracked_tree(
        tmp_path / "r", {"a.md": "one\n", "b.md": "two\n"}, deleted=["b.md"]
    )
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    assert listed == ["a.md", "b.md"], listed
    assert not os.path.exists(os.path.join(root, "b.md"))


# --- the class, re-enumerated over tests/ -----------------------------------
#
# The guard is per helper, so a sixth helper written without one is the defect
# again. This is what stops that, and it is modelled on
# `tests/test_a_corrected_sentence_survives_elsewhere.py#_derives_a_path_list`
# — the machinery this repository already wrote for finding path-listing git
# calls by scope. Two of its decisions are copied with it, and both were
# bought by that module's own round 1:
#
#   - **the unit is the CALL SITE, not the function name.** A second
#     unfiltered list inside a function that already filters one is this
#     defect one LINE over, and a set of names cannot see it. A list built at
#     import time is in no function at all, so module scope is a scope and is
#     spelled.
#   - **the words are kept wider than the two forms in use**, so a call
#     written as a direct `subprocess.run(["git", …, "--name-only", …])` is
#     found too.
#
# What it cannot see is stated rather than left to be found: a listing word
# built from a variable, and a scope that hands its list to a helper in
# ANOTHER module which then opens it. The vacuity assertion below is what
# keeps it from passing on a read that found nothing.
LISTS_PATHS = {"--name-only", "ls-files", "ls-tree"}
MODULE_SCOPE = "<module>"
SHARED_GUARD = "on_disk"

# Every scope in `tests/*.py` that derives a path list from git, and how many
# such calls it makes. A scope missing from all six tables below turns the
# case red until somebody classifies it.
#
# 1. It applies the shared predicate. The reader checks the code rather than
#    the row: the name has to be mentioned in the scope.
APPLIES_THE_SHARED_GUARD = {
    "tests/test_no_real_identifiers.py#tracked_text_files": 1,
    "tests/test_no_document_names_the_old_roots.py#tracked": 1,
    "tests/test_release_hygiene.py#tracked": 1,
    "tests/test_a_release_is_sized_by_a_criterion.py#tracked": 1,
    "tests/test_a_script_says_which_interpreter_it_needs.py#shipped_python": 1,
    "tests/test_a_finding_id_is_a_bare_integer.py#committed_records": 1,
    # The reader itself. It lists the modules it is about to parse, and a
    # module listed and not on disk would end the enumeration at it --
    # this case reporting no offender because it read almost nothing.
    "tests/test_a_shrunken_corpus_declines_to_judge.py#suite_modules": 1,
}

# 2. It guards its own list by another predicate, which predates this work.
#    Checked the same way — the predicate has to be in the scope.
GUARDS_ITS_OWN_LIST = {
    "tests/test_a_new_returnable_value_is_a_contract_change.py#tracked_python": "isfile",
}

# 3. Its list is only ever OPENED behind a scope that catches the error. The
#    reader checks that the named scope still carries the handler. This is not
#    an endorsement: that silence dropped a document from the corpus and
#    produced a false report at its own round 5, and `spec.md` §*Out, and why*
#    leaves repairing it to a different work item.
OPENED_ONLY_BEHIND = {
    "tests/test_the_pull_request_language_is_the_repositorys.py#shipped_templates": "unreachable_templates",
    "tests/test_the_pull_request_language_is_the_repositorys.py#test_every_template_is_named_by_a_document_that_ships": "unreachable_templates",
}

# 4. Immune by construction: the name comes from git and so does the content,
#    so there is no tree state in which one exists without the other.
CONTENT_FROM_GIT = {
    "tests/test_the_reopening_is_one.py#_real_records": (
        "the listing is `ls-tree HEAD` and `stopping_floor` takes its content "
        "from HEAD, which is the repair #142 made across all three readers"
    ),
    "tests/test_chain_check_at_the_pull_request.py#_real_records": (
        "the twin of the row above, same repair, same commit"
    ),
    "tests/test_gate_judges_the_repo_it_commits_to.py#released_hooks": (
        "reads the last release's hooks out of a tag, file by file, through "
        "git — the working tree is never consulted"
    ),
}

# 5. It opens nothing it listed.
OPENS_NOTHING = {
    "tests/test_the_release_check_watches_what_ships.py#tracked_top_level_entries": (
        "takes the first path segment of each line and returns a set of "
        "top-level names; no path in it is ever opened"
    ),
    "tests/test_a_shrunken_corpus_declines_to_judge.py#test_the_builder_leaves_a_deleted_file_tracked": (
        "asserts what the listing says about a fixture repository, which is "
        "the fixture shape itself rather than a corpus"
    ),
}

# 6. It lists a repository the case built, so what is on disk there is what
#    the case put there. A guard would be asserting the fixture against
#    itself.
LISTS_A_FIXTURE = {
    "tests/test_optin_home.py#test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore": 1,
    "tests/test_routing_is_recorded.py#test_an_uncommitted_declaration_silences_the_commit_that_adds_it": 1,
    "tests/test_the_mode_is_a_row_and_a_command.py#test_the_recovery_commands_work_where_they_are_printed": 1,
    "tests/test_the_mode_is_a_row_and_a_command.py#test_an_ignored_workflow_path_is_not_reported_as_staged": 1,
    "tests/test_the_root_migrates_itself.py#test_every_move_is_staged_and_history_follows_the_file": 1,
    "tests/test_the_root_migrates_itself.py#test_the_readme_is_rewritten_from_the_new_template": 1,
    "tests/test_the_root_migrates_itself.py#test_the_re_pointed_ledgers_are_staged_with_the_move": 1,
    "tests/test_the_root_migrates_itself.py#test_an_ignored_file_directly_under_the_old_root_does_not_stop_the_move": 1,
    "tests/test_the_root_migrates_itself.py#test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set": 1,
    "tests/test_chain_check_at_the_pull_request.py#test_a_symbolic_link_cannot_stand_in_for_the_last_round": 1,
    "tests/test_chain_check_at_the_pull_request.py#test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure": 1,
}

# One call per scope everywhere today. Spelled as a map rather than as "one
# each" so a SECOND call inside a classified scope goes red — the call-site
# unit, which is the decision copied from the model.
PATH_LIST_CALLS = {
    **APPLIES_THE_SHARED_GUARD,
    **dict.fromkeys(GUARDS_ITS_OWN_LIST, 1),
    **dict.fromkeys(OPENED_ONLY_BEHIND, 1),
    **dict.fromkeys(CONTENT_FROM_GIT, 1),
    **dict.fromkeys(OPENS_NOTHING, 1),
    **LISTS_A_FIXTURE,
}


def _path_list_words(call):
    """The path-listing words `call` names ITSELF, nested calls excluded.

    Excluded because a nested call is its own site; reading the constants of
    the whole subtree would see the outer call once and collapse two lists
    into one.
    """
    words, stack = set(), list(ast.iter_child_nodes(call))
    while stack:
        node = stack.pop()
        if isinstance(node, ast.Call):
            continue
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                words.add(node.value)
            continue
        stack.extend(ast.iter_child_nodes(node))
    return words & LISTS_PATHS


def _derives_a_path_list(tree):
    """`{scope: how many path-listing calls it makes}` for one module."""
    found = {}

    def visit(node, scope):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(child, child.name)
                continue
            if isinstance(child, ast.Call) and _path_list_words(child):
                found[scope] = found.get(scope, 0) + 1
            visit(child, scope)

    visit(tree, MODULE_SCOPE)
    return found


def derivers(paths, root=ROOT):
    """`{"<rel>#<scope>": calls}` over the modules at `paths`.

    `ast.parse` raises a `SyntaxWarning` for a string literal carrying an
    escape python does not know, and `tests/test_a_row_points_by_content.py`
    has one at line 763. It predates this case --
    `test_a_new_returnable_value_is_a_contract_change.py` already emits it by
    parsing the same file -- and it is a fact about a docstring rather than
    about the class, so this reader does not become a second source of it.
    Caught at the one call that provokes it rather than filtered globally,
    which would hide the next one.
    """
    found = {}
    for rel in paths:
        with open(os.path.join(root, rel), encoding="utf-8") as f:
            source = f.read()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(source)
        for scope, calls in _derives_a_path_list(tree).items():
            found[f"{rel}#{scope}"] = calls
    return found


DECLINES_CLASS = "the suite-wide enumeration of scopes that list paths from git"


def suite_modules():
    """`(every `tests/*.py` on disk, the tracked ones that are not)`."""
    out = git_listing(ROOT, "ls-files", "tests/*.py", check=True)
    return on_disk(ROOT, out)


def vanished_scopes(found, missing):
    """The classified scopes the reader no longer finds, or `pytest.skip` when
    every one of them is in a module the working tree deleted.

    **Only this half declines, and the split is round 2's finding.** The case
    below asks three questions of one reading, and they are not the same kind
    of question. A scope the reader FOUND that no table accounts for, and a
    scope whose call count moved, are both evidence about a module that is on
    disk: they need no whole corpus and they judge what remains, which is what
    `spec.md` §*Is a skip a weakening* asks of a positive sweep. Only the
    scopes that VANISHED are the half a skipped module can explain.

    The first shape of this helper declined in front of all three, and round 2
    measured what that cost: with one test module off disk and the removal
    unstaged, a planted unguarded scope went unnamed and the case exited 0 --
    the gate going quiet on exactly the seventh helper it exists to catch.
    Round 1's finding was this case failing where it should decline; that one
    was it declining where it should judge.

    Conditional on EVERY vanished scope being explained, so a genuine removal
    is still reported beside a skipped one.

    `found` and `missing` are parameters rather than fetched here, so a case
    can hand over a tree it chose without deleting a file the suite is
    running from.
    """
    vanished = sorted(set(PATH_LIST_CALLS) - set(found))
    if vanished:
        gone = {key.split("#", 1)[0] for key in vanished}
        if gone <= set(missing):
            decline_if_shrunken(sorted(gone), DECLINES_CLASS)
    return vanished


def miscounted_scopes(found):
    """`{scope: (calls now, calls accounted)}` for scopes on both sides.

    The CALL SITE half, kept out of the decline for the same reason the
    offender half is: a scope whose count moved is in a module the reader
    just read, so the working tree explains nothing about it.
    """
    return {
        key: (calls, PATH_LIST_CALLS[key])
        for key, calls in found.items()
        if key in PATH_LIST_CALLS and PATH_LIST_CALLS[key] != calls
    }


def _function(tree, name):
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == name
        ):
            return node
    return None


def _mentions(tree, scope, name):
    """True when `scope` names `name` anywhere in its body."""
    node = tree if scope == MODULE_SCOPE else _function(tree, scope)
    assert node is not None, f"{scope} is no longer a scope in this module"
    return any(
        (isinstance(inner, ast.Name) and inner.id == name)
        or (isinstance(inner, ast.Attribute) and inner.attr == name)
        for inner in ast.walk(node)
    )


def _catches_oserror(tree, scope):
    node = _function(tree, scope)
    assert node is not None, f"{scope} is no longer a function in this module"
    for inner in ast.walk(node):
        if isinstance(inner, ast.ExceptHandler) and inner.type is not None:
            if "OSError" in ast.dump(inner.type):
                return True
    return False


def _tree_of(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return ast.parse(f.read())


def test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard():
    """The class, re-enumerated by the suite rather than by whoever remembers.

    `skills/agent-contract/SKILL.md` §12: the finding named one coordinate and
    what was owed was every instance the same cause produces. Five helpers
    carried it, a sixth was found by this case while it was being written, and
    a seventh is what this exists to stop.
    """
    present, missing = suite_modules()
    found = derivers(present)

    # The two positive halves first, and never behind the decline. Each is
    # evidence about a module the reader has just read, so neither needs the
    # corpus to be whole (round 2 🟡 1).
    unaccounted = sorted(set(found) - set(PATH_LIST_CALLS))
    assert not unaccounted, (
        f"the suite derives a path list from git in {unaccounted} that this "
        "case does not account for. Classify it: it either applies "
        f"`{SHARED_GUARD}`, or it belongs in one of the five tables above "
        "with the grounds a reader can weigh"
    )

    miscounted = miscounted_scopes(found)
    assert not miscounted, (
        f"the suite derives path lists at {miscounted}, read as "
        "`{scope: (now, accounted)}`. The unit is the CALL SITE: a second "
        "list inside a scope that already holds one is classified nowhere, "
        "and the grounds recorded above are about the call this case counted"
    )

    vanished = vanished_scopes(found, missing)
    assert not vanished, (
        f"this case accounts for {vanished}, which no longer derives a path "
        "list although its module is on disk. Classify the difference: it "
        f"either applies `{SHARED_GUARD}`, or it belongs in one of the five "
        "tables above with the grounds a reader can weigh"
    )
    for key in APPLIES_THE_SHARED_GUARD:
        rel, scope = key.split("#", 1)
        assert _mentions(_tree_of(rel), scope, SHARED_GUARD), (
            f"{key} derives a path list and no longer applies `{SHARED_GUARD}`, "
            "so a tracked file the working tree deleted ends its walk again "
            "and every path after it goes unread"
        )
    for key, predicate in GUARDS_ITS_OWN_LIST.items():
        rel, scope = key.split("#", 1)
        assert _mentions(_tree_of(rel), scope, predicate), (
            f"{key} is declared as guarding its own list with `{predicate}` "
            f"and no longer names it. Either bring it to `{SHARED_GUARD}` or "
            "move it into a table whose grounds are true of it"
        )
    for key, consumer in OPENED_ONLY_BEHIND.items():
        rel, _scope = key.split("#", 1)
        assert _catches_oserror(_tree_of(rel), consumer), (
            f"{key}'s list is declared safe because `{consumer}` catches the "
            "error when it opens one. That handler is gone, so the list is "
            "opened unguarded now"
        )


def test_the_reader_finds_the_helpers_this_work_guarded():
    """The vacuity assertion. A reader that has stopped matching answers *no
    offender* and nobody hears — which is the failure mode this whole case is
    written against, so it is the one that has to be pinned separately."""
    present, missing = suite_modules()
    found = derivers(present)
    # Declines when the working tree explains the gap; judges otherwise.
    vanished_scopes(found, missing)
    for key in APPLIES_THE_SHARED_GUARD:
        assert key in found, (
            f"{key} is no longer read as deriving a path list from git, so "
            "this case is measuring something other than the class"
        )
    assert derivers([]) == {}, "the reader answers the same on an empty corpus"


def test_a_planted_unguarded_scope_is_named(tmp_path):
    """The reader run against the sixth helper nobody has written yet."""
    module = tmp_path / "test_tmp_planted.py"
    module.write_text(
        "import subprocess\n"
        "def sweep():\n"
        "    out = subprocess.run(['git', 'ls-files'], capture_output=True)\n"
        "    return out.stdout.split()\n",
        encoding="utf-8",
    )
    found = derivers(["test_tmp_planted.py"], root=tmp_path)
    assert found == {"test_tmp_planted.py#sweep": 1}, found
    assert set(found) - set(PATH_LIST_CALLS), "a planted scope was not new"


def test_a_second_list_in_one_scope_is_counted_twice(tmp_path):
    """The call-site unit. A scope that already filters one list and then
    builds a second is this defect one LINE over, and a set of scope names
    cannot see it."""
    module = tmp_path / "test_tmp_two.py"
    module.write_text(
        "import subprocess\n"
        "def sweep():\n"
        "    a = subprocess.run(['git', 'ls-files'])\n"
        "    b = subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'HEAD'])\n"
        "    return a, b\n",
        encoding="utf-8",
    )
    assert derivers(["test_tmp_two.py"], root=tmp_path) == {"test_tmp_two.py#sweep": 2}


def test_a_list_built_at_import_time_is_a_scope(tmp_path):
    """Module scope is a scope. A corpus built at import is in no function at
    all, and a reader keyed on functions never sees it."""
    module = tmp_path / "test_tmp_module.py"
    module.write_text(
        "import subprocess\n"
        "FILES = subprocess.run(['git', 'ls-files']).stdout.split()\n",
        encoding="utf-8",
    )
    assert derivers(["test_tmp_module.py"], root=tmp_path) == {
        f"test_tmp_module.py#{MODULE_SCOPE}": 1
    }


def test_only_an_os_error_handler_reads_as_the_declared_guard():
    """`_catches_oserror` is the whole of what stands behind
    `OPENED_ONLY_BEHIND`, so a handler catching something else must not read
    as one. Measured: with the type check dropped, every case in this module
    still passed, which is a declaration verified by nothing.

    A BARE `except:` reads as not guarded although it would catch the error.
    That is the direction this reader fails in on purpose — it names a scope
    it cannot classify rather than going quiet — and the scope then gets a
    row with grounds somebody wrote.
    """
    tree = ast.parse(
        "def guarded():\n    try:\n        open('x')\n    except OSError:\n        pass\n"
        "def other():\n    try:\n        open('x')\n    except ValueError:\n        pass\n"
        "def bare():\n    try:\n        open('x')\n    except:\n        pass\n"
    )
    assert _catches_oserror(tree, "guarded")
    assert not _catches_oserror(tree, "other")
    assert not _catches_oserror(tree, "bare")


def test_a_test_module_the_tree_deleted_is_not_a_scope_somebody_removed():
    """The inverse direction in the module that enumerates the class.

    An unstaged `git mv` of a test module would otherwise report its scope as
    no longer deriving a path list, and the instruction that comes with that
    report is to classify the difference -- a live row edited out of a table
    on evidence about a working tree.
    """
    key = sorted(APPLIES_THE_SHARED_GUARD)[0]
    rel = key.split("#", 1)[0]
    # Whatever the tree is ALREADY missing rides along in both calls. A case
    # that assumed a whole tree would itself be red on the mid-edit tree this
    # module is about, which is the class one level up from the finding.
    present, missing = suite_modules()
    thinned = derivers([p for p in present if p != rel])
    with pytest.raises(pytest.skip.Exception) as declined:
        vanished_scopes(thinned, [rel, *missing])
    reason = str(declined.value)
    assert rel in reason, reason
    assert DECLINES_CLASS in reason, reason
    assert "not judging" in reason, reason

    # A scope that vanished for any other reason is still a finding. The same
    # shrunken corpus with NOTHING explained by the working tree must reach
    # the refusal rather than the skip — a decline that fires on a vanished
    # scope regardless would carry a real removal away with it.
    try:
        partial = vanished_scopes(thinned, [])
    except pytest.skip.Exception as declined:
        raise AssertionError(
            "a scope that vanished with its module still on disk was declined "
            f"rather than reported: {declined}"
        ) from None
    assert key in partial, partial


def test_an_unguarded_scope_is_named_although_a_module_is_mid_edit():
    """The two positive halves do not decline, which is round 2 🟡 1.

    Measured against the shape this replaces: with the decline in front of
    all three halves, a planted unguarded scope went unnamed on a tree with
    one test module deleted from disk, and the case exited 0 — a gate going
    quiet on the seventh helper it exists to catch. `spec.md` §*Is a skip a
    weakening* is the rule this module was breaking on itself: the positive
    sweeps do not skip themselves.
    """
    key = sorted(APPLIES_THE_SHARED_GUARD)[0]
    rel = key.split("#", 1)[0]
    present, missing = suite_modules()
    thinned = dict(derivers([p for p in present if p != rel]))

    planted = "tests/test_tmp_seventh.py#sweep"
    found = {**thinned, planted: 1}
    assert sorted(set(found) - set(PATH_LIST_CALLS)) == [planted], found
    assert miscounted_scopes(found) == {}

    # A second call inside a scope that already holds one, on a module that
    # is on disk: the count half is evidence about what the reader just read.
    kept = next(k for k in thinned if k != key)
    doubled = {**thinned, kept: thinned[kept] + 1}
    assert miscounted_scopes(doubled) == {
        kept: (thinned[kept] + 1, PATH_LIST_CALLS[kept])
    }

    # Both were judged on inputs that make the liveness half decline, which is
    # the whole of the split.
    with pytest.raises(pytest.skip.Exception):
        vanished_scopes(found, [rel, *missing])


SELF = "tests/test_a_shrunken_corpus_declines_to_judge.py"
GUARDED_CASE = "test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard"


def test_the_positive_halves_are_asked_before_the_decline():
    """The ORDER is the fix, and no unit-level case can see it.

    `vanished_scopes` skips the rest of the function when it declines, so what
    keeps the two positive halves judging is that they sit in front of it.
    Round 2 🟡 1 was that ordering the other way round: a planted unguarded
    scope went unnamed on a tree with one test module mid-edit, and the case
    exited 0. Every helper here was correct at the time; the defect lived in
    the sequence, which is a property of one function's body and of nothing
    this module could otherwise assert.

    Read from the source rather than from behaviour, because reproducing it
    needs a module deleted from the running suite's own tree.
    """
    body = _function(_tree_of(SELF), GUARDED_CASE).body
    dumped = [ast.dump(node) for node in body]
    decline = next(i for i, d in enumerate(dumped) if "vanished_scopes" in d)
    for name in ("unaccounted", "miscounted_scopes"):
        at = next((i for i, d in enumerate(dumped) if name in d), None)
        assert at is not None, f"{GUARDED_CASE} no longer asks for `{name}`"
        assert at < decline, (
            f"`{name}` is evaluated after `vanished_scopes`, so a tree that is "
            "merely mid-edit turns that half of this case off. It is evidence "
            "about a module the reader has just read, and a skip explains "
            "nothing about it — round 2 🟡 1"
        )
