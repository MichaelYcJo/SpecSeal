"""A unit pytest reaches is `pytest only`, not `no call site found`.

#211. `call_sites` greps `name(` across the tracked files, skips the unit's
own `def` line, and sets `tested` only from a call under `tests/`. A pytest
test function is called by collection and never by name, so its only textual
occurrence is the line the walk skips — the reach comes back empty and
`Contract changes` falls to `no call site found`, which reads as *this unit
is dead* about a case that runs on every CI leg. Seen on a live record:
`rounds/round-2.md` of `1788749195-the-record-drops-the-fix-and-a-pipe-
truncates-the-row` carried

    test_the_guard_falls_back_to_the_raw_text_without_the_reader
        → no call site found

**The class is wider than the ticket's instance, and it was enumerated by
running the derivation rather than by reading.** `call_sites` was run over
every top-level def under `tests/` at `ba22b28`:

    test_* function   1892 of 1947 read `no call site found`
    fixture              8 of   42
    other helper         1 of  483
    class                0 of    2

The ticket names the first row and leaves the rest in its *Not verified*
section. A fixture is a member by construction — pytest injects it by
parameter name, so a fixture whose only consumers are tests has no `name(`
anywhere. A `conftest` hook is a member for the same reason, through pytest's
plugin dispatch; this repository holds none today, which is why its case is
built in a repository the test creates rather than found here.

**The one helper is NOT a member, and that is what bounds the rule.**
`tests/test_the_reopening_is_one.py#floor_record` is passed by name as a
value at five call sites and never called, so `no call site found` is a
different cause with a different repair. A rule reading *anything under
tests/* would say *the runner covers this* about a unit nothing covers, so
`test_a_helper_nothing_calls_is_still_unreached` is the case that refuses it.

No new reach value is added: `PYTEST_ONLY` already exists for a unit reached
only from `tests/`, and a pytest test function is the clearest member of that
set. That is why `test_the_fixes_name_their_surface.py`'s derivation of the
reach vocabulary stays green without the spec section growing a sixth word.

Every case was seen red against the unfixed generator, where all four of the
built kinds read `no call site found` alike.
"""

import shutil

import pytest
from test_the_fixes_close_the_record import close, fix_table
from test_the_record_is_generated import (
    ROOT,
    commit,
    declared,
    generate,
    generator_module,
    git,
    reader_module,
    report,
    write,
)

# One open finding, so `close` has a row to answer and the surface is measured.
OPEN = "| 🔴 1 | the four units changed | `mod.py#reached` | open | executed |\n"

# `mod.py` holds one unit with an ordinary in-tree caller, so a record that
# named nothing would be visibly wrong rather than merely empty.
MOD = "def reached(a):\n    return a\n\n\ndef caller():\n    return reached(1)\n"

# The three shapes pytest reaches without a call site, plus one that nothing
# reaches at all. `a_fixture` is requested by PARAMETER NAME in `test_thing`,
# which is the whole point: the text `a_fixture` occurs, `a_fixture(` does not.
CONFTEST = (
    "import pytest\n"
    "\n"
    "\n"
    "def pytest_collection_modifyitems(config, items):\n"
    "    return None\n"
    "\n"
    "\n"
    "@pytest.fixture\n"
    "def a_fixture(a):\n"
    "    return a\n"
)
TEST_MOD = (
    "from mod import reached\n"
    "\n"
    "\n"
    "def test_thing(a_fixture, a_root_fixture):\n"
    "    assert reached(1) == 1\n"
    "\n"
    "\n"
    "def a_dead_helper(x):\n"
    "    return x\n"
    "\n"
    "\n"
    "def pytest_generate_tests(metafunc):\n"
    "    return None\n"
)
# Round 1's finding 1. Collection is TWO rules: `python_files` decides which
# file becomes a test module and `python_functions` decides which def in it is
# a case. `tests/helpers.py` satisfies neither pattern, so a `test_*` def here
# is never imported as a case and nothing else calls it.
HELPERS = "def test_shaped_but_uncollected(x):\n    return x\n"
# Round 1's finding 2. A `conftest.py` at the repository ROOT — the placement
# pytest documents first — holding one fixture and one hook. Both are reached
# without a call site exactly as their `tests/` counterparts are.
ROOT_CONFTEST = (
    "import pytest\n"
    "\n"
    "\n"
    "def pytest_configure(config):\n"
    "    return None\n"
    "\n"
    "\n"
    "@pytest.fixture\n"
    "def a_root_fixture(x):\n"
    "    return x\n"
)
# A `test_*` def that is NOT under `tests/`: the rule is about where pytest
# collects, and a name-shaped def elsewhere is not collected.
ROOT_LEVEL = "def test_looks_like_one(x):\n    return x\n"


# Each def takes one more parameter and nothing else moves: a contract
# change with no unit added and no unit removed, so `Contract changes` names
# all five and `New units` reads `none`. Written out rather than derived — a
# helper that rewrites signatures is one more thing that can silently do
# nothing, which is the failure these cases exist to catch one level up.
WIDENED = {
    "mod.py": (
        "def reached(a, extra=None):\n"
        "    return a\n"
        "\n"
        "\n"
        "def caller():\n"
        "    return reached(1)\n"
    ),
    "tests/conftest.py": (
        "import pytest\n"
        "\n"
        "\n"
        "def pytest_collection_modifyitems(config, items, extra=None):\n"
        "    return None\n"
        "\n"
        "\n"
        "@pytest.fixture\n"
        "def a_fixture(a, extra=None):\n"
        "    return a\n"
    ),
    "tests/test_mod.py": (
        "from mod import reached\n"
        "\n"
        "\n"
        "def test_thing(a_fixture, a_root_fixture, extra=None):\n"
        "    assert reached(1) == 1\n"
        "\n"
        "\n"
        "def a_dead_helper(x, extra=None):\n"
        "    return x\n"
        "\n"
        "\n"
        "def pytest_generate_tests(metafunc, extra=None):\n"
        "    return None\n"
    ),
    "tests/helpers.py": (
        "def test_shaped_but_uncollected(x, extra=None):\n    return x\n"
    ),
    "conftest.py": (
        "import pytest\n"
        "\n"
        "\n"
        "def pytest_configure(config, extra=None):\n"
        "    return None\n"
        "\n"
        "\n"
        "@pytest.fixture\n"
        "def a_root_fixture(x, extra=None):\n"
        "    return x\n"
    ),
    "root_level.py": "def test_looks_like_one(x, extra=None):\n    return x\n",
}
BEFORE = {
    "mod.py": MOD,
    "tests/conftest.py": CONFTEST,
    "tests/test_mod.py": TEST_MOD,
    "tests/helpers.py": HELPERS,
    "conftest.py": ROOT_CONFTEST,
    "root_level.py": ROOT_LEVEL,
}


def test_the_fixture_repository_changes_five_signatures_and_nothing_else():
    """The premise every case below rests on, asserted rather than assumed:
    each `WIDENED` file differs from its `BEFORE` by exactly the one added
    parameter per def, so a case reading `none` would be reading a repository
    that changed nothing rather than a derivation that missed something."""
    import ast

    for rel, after in WIDENED.items():
        old = {
            n.name: len(n.args.args)
            for n in ast.parse(BEFORE[rel]).body
            if isinstance(n, ast.FunctionDef)
        }
        new = {
            n.name: len(n.args.args)
            for n in ast.parse(after).body
            if isinstance(n, ast.FunctionDef)
        }
        assert set(old) == set(new), rel
        widened = [n for n in old if new[n] == old[n] + 1]
        unchanged = [n for n in old if new[n] == old[n]]
        assert sorted(widened + unchanged) == sorted(old), rel
        assert widened, rel
    assert sum(len(ast.parse(t).body) for t in WIDENED.values()) == sum(
        len(ast.parse(t).body) for t in BEFORE.values()
    ), "a unit was added or removed, so `New units` would not be `none`"


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "mod.py", MOD)
    write(d, "tests/conftest.py", CONFTEST)
    write(d, "tests/test_mod.py", TEST_MOD)
    write(d, "tests/helpers.py", HELPERS)
    write(d, "conftest.py", ROOT_CONFTEST)
    write(d, "root_level.py", ROOT_LEVEL)
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("runner-reach-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def contract_row(repo):
    """`Contract changes` after a fix that widens all five signatures."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN))
    assert code == 0, out
    a = commit(repo, "round 1")
    for rel, text in WIDENED.items():
        write(repo, rel, text)
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    reader = reader_module()
    for line in reader.readable(record):
        cells = reader.split_row(line)
        if cells and reader.visible(cells[0]).strip() == "Contract changes":
            return {
                e.split("→")[0].strip(): e.split("→")[1].strip()
                for e in reader.visible(cells[1]).split(";")
                if "→" in e
            }
    raise AssertionError(f"no Contract changes row\n{out}\n{record}")


@pytest.fixture(scope="module")
def reach(tmp_path_factory, _template):
    """The row once, for the cases that each read one entry out of it."""
    d = tmp_path_factory.mktemp("runner-reach-run") / "repo"
    shutil.copytree(_template, d)
    return contract_row(d)


# --- the three kinds pytest reaches -----------------------------------------


def test_a_pytest_test_function_reads_pytest_only(reach):
    """#211's own instance. `test_thing` is called by collection, so the only
    `test_thing(` in the tree is the def line the walk skips."""
    generator = generator_module()
    assert reach["test_thing"] == generator.PYTEST_ONLY, reach


def test_a_fixture_reads_pytest_only(reach):
    """The member the ticket left in its *Not verified* section. `a_fixture`
    is requested as a parameter of `test_thing`, so the name occurs and
    `a_fixture(` never does — 8 of this repository's 42 fixtures read
    `no call site found` before this."""
    generator = generator_module()
    assert reach["a_fixture"] == generator.PYTEST_ONLY, reach


def test_a_conftest_hook_reads_pytest_only(reach):
    """Reached through pytest's plugin dispatch, never by name. No member
    exists in this repository, which is why the case builds one."""
    generator = generator_module()
    assert reach["pytest_collection_modifyitems"] == generator.PYTEST_ONLY, reach


def test_a_conftest_at_the_repository_root_is_still_a_conftest(reach):
    """Round 1's finding 2. `under_tests` used to gate the whole predicate,
    so the fixture and hook arms reached only a `conftest.py` sitting under
    `tests/` — and the repository root is the placement pytest documents
    first, where the fixtures and hooks every module in the tree sees are
    kept. A conftest is a conftest wherever it sits: pytest loads it by name,
    not by directory, so both arms read the basename and the `tests/` gate
    lets a conftest through from anywhere."""
    generator = generator_module()
    assert reach["a_root_fixture"] == generator.PYTEST_ONLY, reach
    assert reach["pytest_configure"] == generator.PYTEST_ONLY, reach


# --- and the boundary that keeps the rule honest ----------------------------


def test_a_helper_nothing_calls_is_still_unreached(reach):
    """`a_dead_helper` sits under `tests/` and pytest reaches it through
    nothing. A rule reading *anything under tests/* would say the runner
    covers a unit nothing covers — which is the false sentence #211 opened
    for, pointing the other way."""
    generator = generator_module()
    assert reach["a_dead_helper"] == generator.NO_SITE, reach


def test_a_hook_outside_a_conftest_is_a_recorded_limit(reach):
    """The hook arm reads `conftest.py` and nothing else, and pytest is
    wider than that: it registers collected test modules as plugins, so a
    `pytest_generate_tests` in a test module really is dispatched and really
    has no call site.

    This case pins the narrower rule rather than the wider behaviour, and the
    trade is which error is cheaper. Reading every `pytest_*` def under
    `tests/` as runner-reached would say *the runner covers this* about any
    helper somebody named `pytest_something` — the false sentence #211 exists
    to remove, pointing the other way. So the limit is written down instead,
    here and in the spec section, and a hook that wants the row moves to a
    `conftest.py` where pytest looks for it first.
    """
    generator = generator_module()
    assert reach["pytest_generate_tests"] == generator.NO_SITE, reach


def test_a_test_shaped_def_in_an_uncollected_module_is_not_the_runners(reach):
    """Round 1's finding 1, and the boundary above pointing the other way.
    `python_files = test_*.py *_test.py` is the half of collection the arm
    was not asking about: `tests/helpers.py` matches neither pattern, so
    pytest never imports it and `test_shaped_but_uncollected` never runs.
    Saying `pytest only` about it is the row claiming the runner covers a
    unit nothing covers — the sentence `plan.md`'s alternatives table
    rejected the wider rule in order to avoid."""
    generator = generator_module()
    assert reach["test_shaped_but_uncollected"] == generator.NO_SITE, reach


def test_a_test_shaped_def_outside_tests_is_not_collected(reach):
    """The rule is about where pytest collects. `root_level.py` is not under
    `tests/`, so a def named `test_*` there is an ordinary unreached unit."""
    generator = generator_module()
    assert reach["test_looks_like_one"] == generator.NO_SITE, reach


def test_a_unit_with_real_callers_still_names_them(reach):
    """The row's ordinary case, unmoved: `reached` is called from `caller`
    in the tree and from a test, so it names the caller and appends
    `pytest`."""
    generator = generator_module()
    assert reach["reached"] == f"caller, {generator.PYTEST}", reach


# --- the vocabulary, and the document that enumerates it --------------------


def test_no_reach_value_was_added():
    """`PYTEST_ONLY` already existed for a unit reached only from `tests/`.
    Adding a sixth word would move `docs/review-chain-spec.md`'s enumeration
    and the test that derives it, for a distinction no reader of the row
    needs."""
    generator = generator_module()
    assert generator.PYTEST_ONLY == "pytest only"
    assert generator.NO_SITE == "no call site found"


def test_the_section_says_when_the_runner_is_the_reach():
    """The five-value paragraph used to define `pytest only` by the callers
    alone. A unit the runner reaches has no callers at all, so a reader
    checking the row against the section found the value undefined for the
    case it is now written in."""
    with open(f"{ROOT}/docs/review-chain-spec.md", encoding="utf-8") as f:
        text = " ".join(f.read().split())
    assert "pytest itself reaches" in text or "the runner reaches" in text, (
        "the section defines `pytest only` by its callers alone"
    )
    for word in ("fixture", "conftest"):
        assert word in text, word
