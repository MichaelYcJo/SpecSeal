"""The arm enumeration, and the one property that decides whether it is worth
having: it cannot silently go short.

#262 asked for a checker rather than nine cases, because a written list of
arms rots — its own table says 33 arms where the module now has 31. A checker
that derives the list has the same failure one level up: **its own walk goes
short on an arm shape it does not know, and the number it prints still looks
right.** `test_every_ast_constructor_is_classified` is the case that closes
that, and it is the reason this module exists at all. The rest pin the
counting rule.

The sweep is against the GRAMMAR, not against the module under test. Reading
`ast`'s own class tree is what makes a Python release that adds a node type
turn a case red instead of quietly narrowing the walk — the same move
`tests/test_chain_hooks.py`'s `reader_blanking_passes` makes for the reader's
passes, which is the precedent #262 names.

**That tree is the running interpreter's, and only a run on a Python sees
its grammar.** #684: 3.14 added two node types and removed five, and CI ran
this module at 3.12 alone, so the promise above held only on whichever machine
happened to have 3.14. The two table cases now check the running Python's
slice exactly, as `ONLY_ON_SOME_PYTHONS` declares it, and
`test_every_bound_of_the_range_table_is_a_python_ci_runs_this_module_at` holds
`.github/workflows/test.yml` to running this module at every bound of it and
at the Python just below each.
"""

import ast
import fnmatch
import glob
import hashlib
import importlib.util
import os
import posixpath
import re
import shlex
import subprocess
import sys
import textwrap
import time
import warnings

import pytest
from conftest import code_lines
from test_ci_gives_the_checks_what_they_need import jobs

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "arm_check.py")
GUARD = os.path.join(ROOT, "hooks", "review-history-guard.py")


def module():
    """The checker, loaded from its path.

    Registered in `sys.modules` BEFORE it executes, which is not optional
    here: the module uses `from __future__ import annotations`, so every
    dataclass field's annotation is a string, and `dataclasses` resolves a
    bare one through `sys.modules[cls.__module__]`. Unregistered, that lookup
    returns None and `@dataclass` raises `AttributeError` on the first field
    — a collection error with nothing in the traceback about names.
    """
    spec = importlib.util.spec_from_file_location("specseal_arm_check", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


ARM = module()


# The ASDL sum types. `ast` exposes them as classes and `ast.parse` never
# produces one, so they are the only names the class tree carries that a
# classification of node types has nothing to say about.
ABSTRACT = frozenset(
    {
        "mod",
        "stmt",
        "expr",
        "expr_context",
        "boolop",
        "operator",
        "unaryop",
        "cmpop",
        "excepthandler",
        "pattern",
        "type_ignore",
        "type_param",
        "slice",
    }
)


def grammar():
    """Every AST constructor this interpreter has, from `ast` itself.

    Derived rather than typed, which is the whole of this module. Taken by
    walking `ast.AST`'s subclasses instead of by listing them: a deprecated
    alias like `ast.Num` is a subclass of `Constant`, so a leaves-only walk
    drops `Constant` — the one node type that appears in nearly every parse.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        seen = set()

        def walk(cls):
            for sub in cls.__subclasses__():
                if sub.__name__ not in seen:
                    seen.add(sub.__name__)
                    walk(sub)

        walk(ast.AST)
    return frozenset(n for n in seen if n not in ABSTRACT)


# --- the enumeration cannot go short --------------------------------------


def test_every_ast_constructor_is_classified():
    """The case this module exists for.

    A node type in neither table is one the walk cannot judge, and the
    failure is silent in the worst direction: the arms inside it are not
    counted, the total still reads like a total, and the checker's report is
    as rotten as the hand count it replaced. So `arms()` raises on an
    unclassified type — and this is what keeps the tables total, because a
    refusal only helps if the tables are complete enough that the refusal
    never fires on ordinary code.

    It sees only the running Python's grammar, which is why CI runs this
    module on more than one (#684).

    Red how: deleting `"IfExp"` from `ARM_SHAPES` leaves it in neither table
    and this case names it. Executed. On Python 3.14 at `346b4af7` it named
    `Interpolation` and `TemplateStr`. Executed.
    """
    missing = grammar() - ARM.CLASSIFIED
    assert not missing, (
        f"{sorted(missing)} — AST node types this walk classifies as neither "
        f"an arm shape nor a named non-arm. Every arm inside one of them is "
        f"uncounted while the total still reads like a total, which is #262's "
        f"own defect one level up. Add each to `ARM_SHAPES` with how its arms "
        f"are read, or to `NOT_ARMS` under the reason it carries none. A name "
        f"new in this Python also takes its first version in "
        f"`ONLY_ON_SOME_PYTHONS`, or the case after this one goes red on every "
        f"older Python."
    )


def on_this_python(name, version=None):
    """Whether `ONLY_ON_SOME_PYTHONS` places `name` on `version`, the
    running Python's minor version when none is given. A name the table does
    not hold is on every supported Python."""
    version = version or sys.version_info[:2]
    first, gone = ARM.ONLY_ON_SOME_PYTHONS.get(name, (None, None))
    return (first is None or version >= first) and (gone is None or version < gone)


def test_the_classification_names_nothing_the_grammar_does_not_have():
    """The other direction, and it is not symmetry for its own sake.

    A name in the tables that `ast` no longer has is a classification nobody
    can reach, and it hides the case above: a removed node type leaves the
    count of classified names unchanged while a name the grammar gained goes
    missing. Subtracting in one direction only would pass on a table that has
    drifted in both.

    Exact per Python since #684. The tables serve every Python from the floor
    up, and 3.14 removed five names 3.12 and 3.13 still have, so a name may be
    absent here when `ONLY_ON_SOME_PYTHONS` says this Python lacks it. That
    declaration is checked from both sides: a name it places on this Python
    must be in `ast`, and one it keeps off must not be. A wrong range is then
    red on the Python it misdescribes, and CI runs this module at every bound
    (`test_every_bound_of_the_range_table_is_a_python_ci_runs_this_module_at`).

    Red how: on Python 3.14 at `346b4af7`, naming the five aliases. With
    `TemplateStr`'s range deleted, red on 3.12 (declared present, absent).
    With `Num`'s upper bound at 3.13, red on 3.13 (declared absent, present).
    Executed."""
    here = grammar()
    placed = frozenset(n for n in ARM.CLASSIFIED if on_this_python(n))
    stale = placed - here
    kept_off = (ARM.CLASSIFIED - placed) & here
    assert not stale, (
        f"{sorted(stale)} — classified here and absent from this "
        f"interpreter's `ast`, and `ONLY_ON_SOME_PYTHONS` does not say this "
        f"Python lacks them. A stale name makes the tables look complete "
        f"while a real one is missing. If the name is gone from this Python "
        f"on purpose, give it the first Python without it in "
        f"`ONLY_ON_SOME_PYTHONS`."
    )
    assert not kept_off, (
        f"{sorted(kept_off)} — `ONLY_ON_SOME_PYTHONS` says this Python "
        f"{sys.version_info[0]}.{sys.version_info[1]} lacks them, and its "
        f"`ast` has them. Correct the range, so the check it buys is not "
        f"switched off on a Python that still has the name."
    )


def run_tests_floor():
    """`FLOOR` from `.github/scripts/run_tests.py`, the one place the
    supported floor is held."""
    path = os.path.join(ROOT, ".github", "scripts", "run_tests.py")
    spec = importlib.util.spec_from_file_location("specseal_floor_of_arm_check", path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return tuple(loaded.FLOOR)


def test_the_range_table_holds_classified_names_and_bounds_above_the_floor():
    """S5 of work item 1790690762. A range for a name the tables do not
    classify switches nothing on or off, and reads as if it did. A bound at
    or below the floor describes a Python this repository does not support,
    which no case here runs and no leg of CI will.

    Red how: with a range added for an unclassified name, and with a bound
    of `(3, 12)`. Executed."""
    unclassified = sorted(set(ARM.ONLY_ON_SOME_PYTHONS) - ARM.CLASSIFIED)
    assert not unclassified, (
        f"{unclassified} — ranged in `ONLY_ON_SOME_PYTHONS` and classified "
        f"in neither `ARM_SHAPES` nor `NOT_ARMS`"
    )
    floor = run_tests_floor()
    low = sorted(
        (name, bound)
        for name, bounds in ARM.ONLY_ON_SOME_PYTHONS.items()
        for bound in bounds
        if bound is not None and tuple(bound) <= floor
    )
    assert not low, (
        f"{low} — a bound at or below the supported floor {floor}. Every "
        f"supported Python is above it, so a name missing below the floor "
        f"needs no row, and one missing at the floor is missing everywhere"
    )


WORKFLOW = os.path.join(ROOT, ".github", "workflows", "test.yml")

_PINNED_PYTHON = re.compile(r'\bpython(?:-version)?:\s*"(\d+)\.(\d+)"')
_THIS_MODULE = "tests/test_arm_check.py"
# pytest's options that take a module back out of the paths it was handed.
# These three name what they remove, so each is read for whether it names
# this module.
_REMOVES = ("--ignore", "--ignore-glob", "--deselect")
# These select by an expression or by an earlier run, which no reading of the
# line can resolve, so a job carrying one is not counted as running it.
_UNREADABLE = (
    "-k",
    "-m",
    "--lf",
    "--last-failed",
    "--sw",
    "--stepwise",
    "--co",
    "--collect-only",
)


def _removes_this_module(option, value):
    """Whether `option value` takes `_THIS_MODULE` out of what pytest runs."""
    if option == "--ignore-glob":
        return fnmatch.fnmatch(_THIS_MODULE, value) or fnmatch.fnmatch(
            "tests", value.rstrip("/")
        )
    path = posixpath.normpath(value.split("::", 1)[0])
    return path == _THIS_MODULE or _THIS_MODULE.startswith(path + "/")


def selects_this_module(line):
    """Whether the pytest invocation on `line` runs `tests/test_arm_check.py`:
    it hands pytest the module or `tests/`, and no option takes the module
    back out. The line is split with `shlex`, and only pytest's own
    selection options are read; a line `shlex` cannot split counts as not
    running it."""
    try:
        words = shlex.split(line)
    except ValueError:
        return False
    start = next(
        (i for i, w in enumerate(words) if posixpath.basename(w) == "pytest"), None
    )
    if start is None:
        return False
    args, named, i = words[start + 1 :], False, 0
    while i < len(args):
        word = args[i]
        option, has_value, value = word.partition("=")
        if option in _REMOVES:
            if not has_value and i + 1 < len(args):
                i += 1
                value = args[i]
            if _removes_this_module(option, value):
                return False
        elif option in _UNREADABLE or (word[:2] in ("-k", "-m") and word[:3] != "--"):
            return False
        elif posixpath.normpath(word) in ("tests", _THIS_MODULE):
            named = True
        i += 1
    return named


def pythons_ci_runs_this_module_at(text):
    """Every `(major, minor)` a job in `text` pins while it runs pytest over
    this module, read through `conftest.code_lines` so a commented-out leg
    or step counts for nothing. The jobs are split by
    `tests/test_ci_gives_the_checks_what_they_need.py#jobs`, the suite's one
    reader of a workflow's `jobs:` block."""
    found = set()
    for block in jobs("\n".join(code_lines(text))).values():
        lines = block.splitlines()
        if any(selects_this_module(line) for line in lines):
            for line in lines:
                found.update((int(a), int(b)) for a, b in _PINNED_PYTHON.findall(line))
    return found


def test_every_bound_of_the_range_table_is_a_python_ci_runs_this_module_at():
    """S6 of work item 1790690762. A range is only checked on the Pythons that
    run this module, and the `pytest` job runs it at the floor alone. A bound
    no leg of CI runs is a declaration checked on nobody's interpreter, which
    is how #684 went unseen: 3.14 changed the grammar in both directions, and
    the one run that met it was a contributor's `.venv`.

    Both sides of a bound need a leg. A bound one Python too low is red only
    on the bound itself, and one a Python too high is red only on the Python
    just below it, so a range checked at its bound alone is checked in one
    direction. A job counts only where `selects_this_module` says its pytest
    line runs this module.

    Red how: before `.github/workflows/test.yml` had a job running this module
    at 3.13 and 3.14, naming 3.14; with the 3.13 leg deleted, naming 3.13;
    with the job's `run:` line handing pytest `tests/` and an `--ignore` of
    this module, naming 3.13 and 3.14. Executed."""
    with open(WORKFLOW, encoding="utf-8") as handle:
        ran = pythons_ci_runs_this_module_at(handle.read())
    bounds = {
        tuple(bound)
        for pair in ARM.ONLY_ON_SOME_PYTHONS.values()
        for bound in pair
        if bound is not None
    }
    floor = run_tests_floor()
    below = {
        (major, minor - 1) for major, minor in bounds if (major, minor - 1) >= floor
    }
    unrun = sorted((bounds | below) - ran)
    assert not unrun, (
        f"{['.'.join(map(str, b)) for b in unrun]} — a bound in "
        f"`ONLY_ON_SOME_PYTHONS`, or the Python just below one, that no job "
        f"in test.yml runs `tests/test_arm_check.py` at (it runs it at "
        f"{['.'.join(map(str, v)) for v in sorted(ran)]}). Add the version as "
        f"a leg of the job that runs this module, or that side of the range is "
        f"checked on no interpreter CI has"
    )


@pytest.mark.parametrize(
    "line, runs",
    [
        ("- run: pytest tests/test_arm_check.py -q", True),
        ("- run: pytest tests/ -q -n auto", True),
        ("- run: python -m pytest tests", True),
        ("- run: pytest tests/ --ignore=tests/test_other.py -q", True),
        ("- run: pytest tests/ --ignore=tests/test_arm_check.py -q", False),
        ("- run: pytest tests/ --ignore tests/test_arm_check.py", False),
        ("- run: pytest tests/ --ignore=tests", False),
        ("- run: pytest tests/ --ignore-glob='tests/*arm*'", False),
        ("- run: pytest tests/ --deselect tests/test_arm_check.py::test_x", False),
        ("- run: pytest tests/ -k 'not arm'", False),
        ("- run: pytest tests/ -mslow", False),
        ("- run: pytest tests/test_other.py", False),
        ("- run: pip install pytest", False),
        ('- run: pytest "tests/', False),
    ],
)
def test_a_job_counts_only_where_its_pytest_line_selects_this_module(line, runs):
    """S6's reader, one line at a time. A line that hands pytest `tests/` and
    takes this module back out runs it at no Python, and a filter that only
    pytest can resolve is not counted either.

    Red how: with `_removes_this_module` answering False, and with the
    `_UNREADABLE` branch deleted. Executed."""
    assert selects_this_module(line) is runs


def test_no_node_type_is_both_an_arm_and_a_non_arm():
    """A name in both tables is a classification that answers twice.

    `arms()` dispatches on `ARM_SHAPES` and only consults `NOT_ARMS` for the
    refusal, so a double entry would be silently resolved one way and read as
    excluded by anybody auditing the other table."""
    both = set(ARM.ARM_SHAPES) & ARM.NOT_ARM_NAMES
    assert not both, f"{sorted(both)} — classified as an arm shape AND a non-arm"


def test_an_unclassified_node_type_is_refused_rather_than_skipped():
    """`questions.md` assumption 2, watched.

    A walk that skips what it does not recognise is the failure of the thing
    it replaces. This drives the refusal by classifying a node type OUT of
    both tables at runtime — `Assign` is in every module, so the refusal has
    to fire on the first statement rather than on a shape somebody has to
    construct."""
    without_assign = ARM.CLASSIFIED - {"Assign"}
    original = ARM.CLASSIFIED
    try:
        ARM.CLASSIFIED = without_assign
        with pytest.raises(ARM.UnknownNodeType, match="`Assign` is neither"):
            ARM.arms("x = 1\n", filename="fixture.py")
    finally:
        ARM.CLASSIFIED = original
    # And the refusal is not a permanent state of the walk.
    assert ARM.arms("x = 1\n") == []


# --- the counting rule ----------------------------------------------------


FIXTURE = '''\
"""A module whose arms are known by construction."""


def one_of_each(items, flag):
    try:
        if flag and items:                       # 2 arms
            return [x for x in items if x if x]  # 2 arms
        while flag or not items:                 # 2 arms
            flag = False
        return 1 if flag else 2                  # 1 arm
    except (ValueError, TypeError):              # 2 arms
        return None
    except OSError:                              # 1 arm
        return None


def nested_boolop(a, b, c):
    if a and (b or c):                           # 2 arms, not 4
        return 1
    return 0
'''


def test_the_fixtures_arms_are_counted_by_construction():
    """Every shape #262's rule names, in one fixture, counted by hand in its
    own comments: 10 in `one_of_each` and 2 in `nested_boolop`.

    Red how: dropping the `IfExp` entry from `ARM_SHAPES` takes
    `one_of_each` to 9. Executed."""
    found = ARM.arms(FIXTURE, filename="fixture.py")
    assert ARM.counts(found) == {"one_of_each": 10, "nested_boolop": 2}


def test_a_boolean_test_is_counted_at_its_top_level_and_not_flattened():
    """The rule that keeps this walk comparable to the hand count.

    `a and (b or c)` is TWO arms — the inner `BoolOp` is one member of the
    outer one. Flattening recursively gives three here, and gives
    `gh_segments` seven arms where #262's table and this walk both give five.
    So the property is pinned on the fixture and on the real function, and
    the real one is what says the two rules have not parted."""
    found = ARM.arms(FIXTURE, filename="fixture.py")
    nested = [a for a in found if a.scope == "nested_boolop"]
    # The segments carry no enclosing parens: they are not part of the node.
    # The splice replaces exactly this span, so `not (...)` around the second
    # one lands inside the parens the source already has.
    assert [a.source for a in nested] == ["a", "b or c"], (
        "the inner BoolOp was flattened. `gh_segments` then reads 7 where "
        "#262's hand count and this walk both read 5, and no number the "
        "checker prints can be compared with the ticket's again"
    )


def test_an_arm_added_to_the_fixture_moves_the_count():
    """`spec.md`'s second scenario: the enumeration cannot go short when a
    module gains an arm, and nothing is typed for it to be found.

    This is the property the written list did not have. #210's list of reader
    passes was two literals and a comment asking for a third entry; a third
    pass arrived and the count stayed put."""
    before = sum(ARM.counts(ARM.arms(FIXTURE)).values())
    widened = FIXTURE.replace(
        "def nested_boolop(a, b, c):\n",
        "def nested_boolop(a, b, c):\n    if a is None:\n        return -1\n",
    )
    assert widened != FIXTURE, "the fixture edit did not land"
    assert sum(ARM.counts(ARM.arms(widened)).values()) == before + 1


def test_a_bare_except_is_one_arm_and_an_except_tuple_is_one_per_member():
    """#262's rule for handlers, both halves.

    A tuple counted as one arm is how eight of `main`'s arms went unwatched
    for as long as they did — the count that hid them was taken per handler."""
    found = ARM.arms("try:\n    pass\nexcept (A, B, C):\n    pass\nexcept:\n    pass\n")
    handlers = [a for a in found if a.shape == "ExceptHandler"]
    assert [a.source for a in handlers[:3]] == ["A", "B", "C"]
    assert handlers[3].note == "bare except"
    assert len(handlers) == 4


def test_a_match_case_and_a_comprehension_guard_are_arms():
    """The two shapes #262's rule predates, and the plan's named failure
    scenario: *a new arm shape the walk does not know, a `match` statement, a
    comprehension guard.*

    They change no count on `hooks/review-history-guard.py`, which has
    neither — so the real module's 31 is reproducible under #262's four
    shapes and under these six alike."""
    source = textwrap.dedent(
        """\
        def m(x, items):
            match x:
                case 1 | 2 if x > 0:
                    return "small"
                case _:
                    return "other"
            return [y for y in items if y]
        """
    )
    found = ARM.arms(source)
    shapes = [(a.shape, a.note) for a in found]
    # `1 | 2` is two pattern alternatives, the guard is one arm, `case _` is
    # one pattern, and the comprehension `if` is one.
    assert shapes == [
        ("match_case", "pattern 1/3"),
        ("match_case", "pattern 2/3"),
        ("match_case", "guard 3/3"),
        ("match_case", "pattern"),
        ("comprehension", "guard"),
    ]


def test_a_module_level_arm_is_named_rather_than_dropped():
    """`if __name__ == "__main__":` is an arm and #262's per-function table
    has no row for it.

    That is the enumeration going LONG, which is the safe direction and still
    worth pinning: attributing a module-level arm to the last function it
    followed, or dropping it, are both ways for the total to stop matching
    what the file holds."""
    found = ARM.arms('def f():\n    pass\n\n\nif __name__ == "__main__":\n    f()\n')
    assert ARM.counts(found) == {ARM.MODULE_SCOPE: 1}


# --- a t-string (#684) ----------------------------------------------------
#
# The sources below are string literals, so this module parses on every
# supported Python. Only 3.14 and later parse what is inside them, which is
# why the two cases skip below it and why CI runs this module at 3.14.

NEEDS_T_STRINGS = pytest.mark.skipif(
    sys.version_info < (3, 14), reason="t-strings parse from Python 3.14 on"
)

T_STRING_BRANCH = """\
def render(a, x, b):
    if a:
        return t"{x if a else b}"
    return None
"""

# Every feature an interpolation has, in one module, so the f-string twin is
# one text substitution: an `IfExp` value with a `!r` conversion and a format
# spec whose nested field holds another `IfExp`, a `BoolOp` value, and a
# comprehension with an `if` guard.
T_STRING_FEATURES = """\
def render(a, b, x, w, items):
    return t"{x if a else b!r:>{w if b else 0}} and {a or b}" t"{[i for i in items if i and a]}"
"""


@NEEDS_T_STRINGS
def test_a_module_holding_a_t_string_is_read_rather_than_refused():
    """S1 of work item 1790690762. `TemplateStr` and `Interpolation` were in
    neither table, so on a 3.14 `python3` `arm-check` refused any file with a
    t-string in it. The arms around and inside one are counted now.

    Red how: on Python 3.14 at `346b4af7`, `UnknownNodeType` naming
    `TemplateStr`. Executed."""
    found = ARM.arms(T_STRING_BRANCH, filename="fixture.py")
    assert [(a.shape, a.source) for a in found] == [("If", "a"), ("IfExp", "a")]


@NEEDS_T_STRINGS
def test_an_interpolation_is_counted_exactly_as_an_f_string_field():
    """S2 of work item 1790690762. An interpolation tests nothing, like the
    `FormattedValue` it mirrors, and the walk enters its value and its format
    spec, so an arm inside one is counted where it stands. Held against the
    same text read as f-strings, which the rest of this module already pins.

    Red how: on Python 3.14 at `346b4af7`, refused. With `Interpolation`
    moved into `ARM_SHAPES`, the dispatch in `_node_arms` refuses it.
    Executed."""
    as_f = T_STRING_FEATURES.replace('t"', 'f"')
    assert as_f != T_STRING_FEATURES

    def read(arm):
        return (arm.scope, arm.shape, arm.note, arm.source, arm.lineno)

    as_template = ARM.arms(T_STRING_FEATURES, filename="fixture.py")
    assert [read(a) for a in as_template] == [
        read(a) for a in ARM.arms(as_f, filename="fixture.py")
    ]
    # The `IfExp` in the value, the one in the nested format field, and the
    # comprehension guard's two members. `a or b` is a value, not a branch.
    assert [(a.shape, a.source) for a in as_template] == [
        ("IfExp", "a"),
        ("IfExp", "b"),
        ("comprehension", "i"),
        ("comprehension", "a"),
    ]
    for arm in as_template:
        for operator in ARM.OPERATORS:
            ast.parse(ARM.mutate(T_STRING_FEATURES, arm, operator))


# --- the real module ------------------------------------------------------


def test_the_guards_arms_match_the_count_taken_by_hand():
    """The measured expectation this walk was built against (#262, #210).

    31 arms inside functions, split exactly as the hand count split them —
    and one more at module level, which #262's per-function table had no row
    for. The ticket's own table says 33, differing only in `main` (19); the
    file changed twice after that measurement (`341be0b`, `1dedd1e`) and the
    ticket is left as written, because correcting a shipped measurement
    hides the argument the ticket makes.

    This case is the one that would catch the walk and the rule parting
    company. It is expected to move when the module does — the repair is to
    re-derive the split and change these numbers, never to widen the walk
    until they fit."""
    found = ARM.arms_of_file(GUARD)
    counted = ARM.counts(found)
    assert counted == {
        "reader": 5,
        "is_closed": 4,
        "gh_segments": 5,
        "main": 17,
        ARM.MODULE_SCOPE: 1,
    }
    assert sum(n for s, n in counted.items() if s != ARM.MODULE_SCOPE) == 31


def test_every_arm_of_the_guard_carries_a_source_segment():
    """An arm whose text could not be read is an arm nothing can mutate, and
    `mutate()` refuses it rather than reporting it unwatched. On this module
    that refusal must never fire — if it does, the report's denominator has
    quietly shrunk."""
    for arm in ARM.arms_of_file(GUARD):
        assert arm.source, f"{arm.where}: no source segment"


# --- the mutation and the report ------------------------------------------


# A module with two arms: one a case exercises, one it never reaches. The
# neutral values `spec.md` asks for -- no real host, no real user path.
TWO_ARMS = """\
def classify(host, flag):
    if host == "example.com":
        return "known"
    if flag:
        return "flagged"
    return "other"
"""

# A case that returns at the first arm every time, so the second `if` is
# never reached. Mutating arm one turns it red; mutating arm two changes
# nothing it looks at. That pair IS the verdict the checker reports.
#
# Reaching arm two at all is enough to watch it: an earlier draft called
# `classify("other.example.com", False)` expecting `"other"`, and inverting
# `flag` made that return `"flagged"` — killed, not survived. An unwatched arm
# has to be unreachable by the case, not merely uninteresting to it.
WATCHES_ONE = """\
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

assert m.classify("example.com", False) == "known"
assert m.classify("example.com", True) == "known"
"""


@pytest.fixture
def two_arms(tmp_path):
    """The fixture module and the case that watches one of its two arms."""
    module_path = tmp_path / "under_test.py"
    module_path.write_text(TWO_ARMS, encoding="utf-8")
    case_path = tmp_path / "watches_one.py"
    case_path.write_text(WATCHES_ONE, encoding="utf-8")
    return module_path, [sys.executable, str(case_path), str(module_path)]


def test_a_watched_arm_is_killed_and_an_unwatched_one_survives(two_arms):
    """`plan.md`'s phase 3 verification, and the checker's whole verdict.

    The fixture has two arms and the case reaches one. Inverting the watched
    arm makes the case red — killed. Inverting the unwatched one changes
    nothing the case looks at — survived, which is what gets reported.

    Red how: making `run_arms` read the mutation's exit code as `== 0`
    instead of `!= 0` swaps both verdicts and this case names both. Executed.
    """
    module_path, tests = two_arms
    verdicts, refused = ARM.run_arms(str(module_path), tests)
    assert refused == []
    assert [(v.arm.source, v.killed) for v in verdicts] == [
        ('host == "example.com"', True),
        ("flag", False),
    ]


def test_the_module_is_restored_byte_for_byte_after_the_run(two_arms):
    """The property the plan puts above elegance.

    Not `git checkout`: the working tree of a fix pass carries uncommitted
    work, and a checkout of the wrong path takes it. Held bytes and a hash
    have no such reach."""
    module_path, tests = two_arms
    before = hashlib.sha256(module_path.read_bytes()).hexdigest()
    ARM.run_arms(str(module_path), tests)
    assert hashlib.sha256(module_path.read_bytes()).hexdigest() == before


def test_a_restore_that_did_not_land_stops_the_run(tmp_path):
    """The check that catches a mutation recorded as killed and never applied.

    Four fix passes ran this enumeration by hand in one day and the one that
    skipped the hash compare recorded exactly that — the pattern had missed
    by two spaces of indentation. `restore` is a function of its own so this
    failure is reachable without breaking a real run: handed bytes that are
    not what the file ends up holding, it raises rather than letting the next
    arm be measured against a mutated module."""
    path = tmp_path / "m.py"
    path.write_text("x = 1\n", encoding="utf-8")
    original = b"x = 1\n"
    wrong_sha = hashlib.sha256(b"something else\n").hexdigest()
    with pytest.raises(RuntimeError, match="was not restored"):
        ARM.restore(str(path), original, wrong_sha)
    # The bytes it was given are on disk regardless — it raises about the
    # comparison, it does not leave the file mutated.
    assert path.read_bytes() == original


def test_an_arm_with_no_defined_mutation_is_refused_not_reported_unwatched():
    """`questions.md` assumption 2 again, at the mutation rather than the walk.

    An arm the checker enumerates and cannot mutate must not come back as
    `survived` — that reads as *no case watches this* when the truth is *this
    was never tried*. A match PATTERN is not an expression, so inverting it
    is not available, and a bare `except:` has no type to aim elsewhere."""
    source = textwrap.dedent(
        """\
        def f(x):
            match x:
                case 1:
                    return "one"
            try:
                pass
            except:
                pass
        """
    )
    found = ARM.arms(source)
    pattern = next(a for a in found if a.shape == "match_case")
    bare = next(a for a in found if a.note == "bare except")
    with pytest.raises(ARM.NoMutationDefined, match="no mutation is defined"):
        ARM.mutate(source, pattern)
    with pytest.raises(ARM.NoMutationDefined, match="bare `except:` catches"):
        ARM.mutate(source, bare)


def test_a_refused_arm_is_counted_and_named_in_the_report(tmp_path):
    """A refusal that nothing prints is a skip with extra steps.

    The report has to say how many arms came back with no verdict from any
    operator, and name them — otherwise the denominator quietly shrinks and
    the survivor count still reads like a survivor count.

    **This arm is the one that was never mutated**, and that is now the
    reason's job rather than the header's: `mutate` refuses a bare `except:`
    before anything is written, where a timed-out arm reaches the same list
    with the mutation already applied and restored (round 2's finding 15).
    So the header is asserted without the word *mutated* in it, and the
    reason is asserted to be the never-asked kind."""
    module_path = tmp_path / "m.py"
    module_path.write_text(
        "def f(x):\n    try:\n        return x\n    except:\n        return None\n",
        encoding="utf-8",
    )
    verdicts, refused = ARM.run_arms(str(module_path), [sys.executable, "-c", "pass"])
    assert verdicts == []
    assert len(refused) == 1

    lines = []
    ARM._report(
        str(module_path),
        verdicts,
        refused,
        ARM.counts([a for a, _ in refused]),
        lines.append,
    )
    text = "\n".join(lines)
    assert "1 arms with no verdict from any operator" in text
    assert "not mutated" not in text, (
        "the header cannot claim this arm was not mutated: the same list "
        "holds arms the timeout and OSError paths mutated, ran and restored"
    )
    assert "NoMutationDefined" in text and "bare `except:` catches" in text, (
        "so the reason is what says this one was never asked at all"
    )


def test_a_mutation_inverts_the_arm_and_leaves_the_module_parseable():
    """The mutation's two conditions.

    Its sense has to change, and the result has to still be Python — a
    mutation that does not parse kills every arm, so the run would report a
    perfectly watched module."""
    source = "def f(a, b):\n    if a and b:\n        return 1\n    return 0\n"
    first, second = ARM.arms(source)
    assert "if not (a) and b:" in ARM.mutate(source, first)
    assert "if a and not (b):" in ARM.mutate(source, second)
    for arm in (first, second):
        ast.parse(ARM.mutate(source, arm))


def test_an_except_member_is_aimed_at_an_exception_nothing_raises():
    """Inverting is not available for a handler, so the mutation makes it
    unreachable instead. Spelled as an expression, so it needs no name in
    the module under test — a mutation that requires an import would have to
    edit two places and could not be one splice."""
    source = "def f():\n    try:\n        pass\n    except (OSError, ValueError):\n        pass\n"
    first, second = ARM.arms(source)
    mutated = ARM.mutate(source, first)
    assert "_specseal_never_raised" in mutated
    assert "ValueError" in mutated, "only the mutated member changes"
    ast.parse(mutated)
    assert "OSError" in ARM.mutate(source, second)


def test_the_splice_reads_a_column_offset_as_bytes_not_characters():
    """`col_offset` is a UTF-8 byte offset, and this repository's modules are
    full of non-ASCII prose.

    Sliced as a character index, the head keeps too much and the mutation
    lands in the middle of a token — usually a `SyntaxError`, which `mutate`
    catches and reports as a refused arm, so the arm goes unmeasured and
    nobody is told why."""
    source = 'def f(y, x):\n    if "é" == y or x:\n        return 1\n    return 0\n'
    first, second = ARM.arms(source)
    assert first.source == '"é" == y'
    mutated = ARM.mutate(source, first)
    assert 'if not ("é" == y) or x:' in mutated
    ast.parse(mutated)
    assert 'if "é" == y or not (x):' in ARM.mutate(source, second)


def test_the_report_names_the_scope_the_shape_and_the_line_of_a_survivor():
    """§14 — the report is text a person reads and acts on, so it is pinned.

    A survivor named without its line is a survivor nobody can find, and the
    report also has to say that a survivor is not automatically a defect:
    `reader` has an arm that cannot be constructed and `main` has one whose
    removal preserves behaviour."""
    span = ARM.Span(176, 10, 176, 24)
    arm = ARM.Arm(
        scope="gh_segments",
        shape="While",
        source="i < len(toks)",
        note="1/2",
        span=span,
        group=ARM.Span(176, 10, 177, 60),
        group_without="(os.path.basename(toks[i]) in WRAPPERS)",
    )
    lines = []
    ARM._report(
        "hooks/review-history-guard.py",
        [ARM.Verdict(arm, {"invert": False, "remove": False}, {})],
        [],
        {"gh_segments": 1},
        lines.append,
    )
    text = "\n".join(lines)
    assert "gh_segments:176" in text, "a survivor must carry its scope and line"
    assert "While" in text, "and the shape, so the reader knows what to look at"
    assert "1 watched by no case" in text
    assert "not a list of defects" in text, (
        "the report must say a survivor is not automatically a gap — #262 "
        "already names two arms whose removal preserves behaviour, and a "
        "report read as a defect list turns them into work nobody owes"
    )


# Two scopes, one arm each, so `--only` narrows the run to half the module.
TWO_SCOPES = """\
def one(a):
    if a:
        return 1
    return 0


def two(b):
    if b:
        return 1
    return 0
"""

# A module whose branching lives in the two DECLARED exclusions plus one `if`.
# #262's rule counts the `if` alone, so the total is 1 of three branchings a
# reader would count by eye.
DECLARED = """\
def f(x, items):
    assert x > 0 and x < 10
    for item in items:
        if item:
            return item
    else:
        return None
"""


def test_the_declared_exclusions_are_named_where_the_total_is_printed(tmp_path):
    """Round 1's finding 7. §14 — the report is what a person reads.

    `Assert`, `For` and `AsyncFor` are excluded by DECLARATION rather than
    because they hold no boolean test: an `assert` is a test a mutation could
    flip, and a `for`'s `orelse` is arguably an arm. #262's rule counts
    neither and the hand count this walk is checked against was taken under
    that rule, so the exclusion stands — but on a module whose branching lives
    in them, `1 arms` reads as *this module has one branch* rather than as
    *one under this rule*, and the rule is the part a reader has to be able to
    overturn.

    Named statically rather than counted, which is the smaller fix: a count
    per module would mean a second walk of the tree, and what the reader needs
    is which rule narrowed the total and where its grounds are.

    Red how: deleting the two `echo` lines in `_report` leaves the module's
    `1 arms` with nothing saying what it excludes. Executed."""
    module_path = tmp_path / "declared.py"
    module_path.write_text(DECLARED, encoding="utf-8")
    lines = []
    found = ARM.arms_of_file(str(module_path))
    ARM._report(str(module_path), [], [], ARM.counts(found), lines.append)
    text = "\n".join(lines)
    assert "1 arms" in text, (
        "the fixture's assert pair and for/else are excluded, so the walk "
        "finds only the inner `if` — that is the premise of this case"
    )
    assert "excluded by declaration, not in the total" in text
    for name in ARM.DECLARED_EXCLUSIONS:
        assert name in text, (
            f"{name} is excluded by declaration and the report does not say "
            f"so, so its total reads as the module's branch count"
        )
    assert "NOT_ARMS" in text, "and where the grounds for each exclusion are"


def test_every_declared_exclusion_is_classified_as_a_non_arm():
    """The list the report prints cannot name a shape the walk actually walks.

    A name that drifted into `ARM_SHAPES` would be disclosed as excluded while
    being counted, which is worse than the silence this replaced."""
    for name in ARM.DECLARED_EXCLUSIONS:
        assert name in ARM.NOT_ARM_NAMES, f"{name} is not classified as a non-arm"
        assert name not in ARM.ARM_SHAPES, (
            f"{name} is walked as an arm shape and reported as excluded"
        )


def test_a_filtered_run_does_not_state_its_count_as_the_modules_total(tmp_path, capsys):
    """Round 1's finding 8. §14 again, and the harm is in the paste.

    The header names a file and gives a number, so it reads as the file's
    total. Under `--only` it was the filtered count: `--only reader` printed
    `hooks/review-history-guard.py — 5 arms` for a module holding 32. This
    output goes into records — `phase-4.md` and the ledger fragment both paste
    a run — and the flag that produced it does not travel with the text.

    Both call sites, because `--only` narrows in two places: the listing
    branch filters `arms_of_file` and the mutating branch filters inside
    `run_arms`. The unfiltered total is taken before either.

    Red how: `of_total` dropped from a call site prints `1 arms` for a
    two-arm module. Executed on both."""
    module_path = tmp_path / "two_scopes.py"
    module_path.write_text(TWO_SCOPES, encoding="utf-8")

    # The listing branch.
    ARM.main([str(module_path), "--only", "one"])
    listed = capsys.readouterr().out
    assert "1 of 2 arms (--only)" in listed, (
        f"{listed!r} — a filtered listing must say what it filtered out of, "
        f"or its number is read as the module's"
    )

    # And unfiltered, the same line carries no denominator to misread.
    ARM.main([str(module_path)])
    whole = capsys.readouterr().out
    assert "— 2 arms" in whole and "of 2 arms" not in whole

    # The mutating branch, where the total has to be read before `--only`.
    ARM.main(
        [
            str(module_path),
            "--only",
            "one",
            "--tests",
            shlex.join([sys.executable, "-c", "pass"]),
        ]
    )
    mutated = capsys.readouterr().out
    assert "1 of 2 arms (--only)" in mutated, (
        f"{mutated!r} — the mutating branch filters inside `run_arms`, so it "
        f"needs the total taken before the filter"
    )


def test_the_checker_is_report_only_and_exits_zero_over_the_real_module(two_arms):
    """`questions.md` Q1 is the owner's, and this is the behaviour the code
    has until they answer: report-only.

    Listed here rather than left to be discovered, because the other two
    answers — non-zero on any survivor, non-zero above a recorded baseline —
    both need the first run's number to exist first, and this is the run that
    produces it. Changing the exit rule turns this case red, which is the
    point: it is a decision, not a detail.

    Taken over the MUTATING path with a survivor present, not over the
    listing path. An earlier version of this case called `main([GUARD])` with
    no `--tests`, which returns 0 down a branch that never asks about
    survivors at all — measured: making the mutating branch return the
    survivor count left this case green."""
    module_path, tests = two_arms
    assert ARM.main([str(module_path), "--tests", shlex.join(tests)]) == 0, (
        "the checker is report-only until `questions.md` Q1 is answered"
    )
    # And the run it just did had a survivor to report, so the 0 above is the
    # exit rule rather than an empty report.
    verdicts, _ = ARM.run_arms(str(module_path), tests)
    assert any(not v.killed for v in verdicts)


def test_a_stale_bytecode_cache_cannot_decide_an_arms_verdict(tmp_path):
    """The defect building phase 3 found, and the reason it is invisible.

    CPython validates a `.pyc` against the source's mtime and SIZE. Two
    mutations of the same arm shape are routinely the same length — `not
    (host == "example.com")` and `not (flag)` both add six characters — so
    written inside one mtime tick the second arm loads the first arm's
    bytecode. Measured: the fixture module's unreached second arm came back
    `killed`, with a traceback pointing at an assertion the unmutated module
    satisfies.

    No hash catches it. `restore` compares the bytes on disk and the bytes on
    disk were right; the interpreter never read them. So the cache is cleared
    around every arm and the subprocess is told to write none."""
    module_path = tmp_path / "cached.py"
    module_path.write_text("VALUE = 1\n", encoding="utf-8")

    # A real cache entry, made the way an import makes one.
    spec = importlib.util.spec_from_file_location("specseal_cached_probe", module_path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    cache = tmp_path / "__pycache__"
    assert cache.is_dir() and list(cache.glob("cached.*.pyc")), (
        "this case needs a real .pyc to remove; the interpreter wrote none"
    )

    removed = ARM.clear_bytecode_cache(str(module_path))
    assert removed, "a cached .pyc for the module under test was left in place"
    assert not list(cache.glob("cached.*.pyc"))
    del sys.modules[spec.name]


# A stand-in for the test command that reports what it SAW rather than
# passing or failing: whether cached bytecode for the module under test
# existed, in the directory it is handed, at the moment it ran.
#
# Then it leaves a `.pyc` there, the way a command that builds its own
# environment and ignores `PYTHONDONTWRITEBYTECODE` would. Without that, the
# run against the unmutated module clears the planted cache before any arm
# runs, and the clear before each arm is watched by nothing (#703: measured,
# the cache case stayed green with it deleted). The next run has to see it
# gone, and so does the caller once the run is over.
SEES_CACHE = """\
import glob
import os
import sys

cache, log = sys.argv[1], sys.argv[2]
found = glob.glob(os.path.join(cache, "under_test.*.pyc"))
with open(log, "a", encoding="utf-8") as f:
    f.write("cache\\n" if found else "clean\\n")
os.makedirs(cache, exist_ok=True)
with open(os.path.join(cache, "under_test.specseal-left-behind.pyc"), "wb") as f:
    f.write(b"stale")
"""


def test_no_arm_runs_while_cached_bytecode_for_the_module_exists(two_arms, tmp_path):
    """The call site, watched by what the subprocess can see.

    **Reproducing the defect is timing-dependent, so the mechanism is what
    gets pinned.** CPython validates a `.pyc` on the source's mtime and size:
    two mutations of one arm shape are the same size, so whether arm two
    loads arm one's bytecode depends on the two writes landing in the same
    mtime tick. Measured both ways within this work item — poisoned when the
    writes were adjacent, clean when they were not. A case that reproduces it
    would be a case that fails on a slow machine and passes on a fast one.

    So this asks the only question that has a stable answer: at the moment an
    arm's command runs, is there cached bytecode for the module at all? A
    planted cache and one observation per arm. An earlier version asserted
    the verdicts instead and stayed green with the clear deleted, because the
    plant was invalid for the mutation anyway — `not (...)` adds six bytes,
    so a cache for the ORIGINAL never matches a mutation of it. Only the
    PREVIOUS ARM's cache is the same size as this one's."""
    module_path, _ = two_arms
    log = tmp_path / "seen.txt"
    probe = tmp_path / "sees_cache.py"
    probe.write_text(SEES_CACHE, encoding="utf-8")

    # Plant a cache the way an ordinary import does. `hooks/__pycache__` holds
    # one for `review-history-guard.py` before `arm-check` is ever run,
    # because this repository's own suite imports it.
    spec = importlib.util.spec_from_file_location("specseal_planted", module_path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    del sys.modules[spec.name]
    assert list((module_path.parent / "__pycache__").glob("under_test.*.pyc")), (
        "this case needs a cache to have been planted"
    )

    cache = module_path.parent / "__pycache__"
    verdicts, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, str(probe), str(cache), str(log)],
    )
    assert refused == []
    seen = log.read_text(encoding="utf-8").split()
    # Two arms, and every operator that has a mutation for one of them, plus
    # the one run against the module as it is that comes before them -- which
    # a planted cache would decide just as surely, so it is watched too.
    expected = sum(len(v.by_operator) for v in verdicts) + 1
    assert len(verdicts) == 2
    assert len(seen) == expected == 5, "every run must have been observed"
    assert set(seen) == {"clean"}, (
        f"{seen} — an arm ran with cached bytecode for the module present, so "
        f"its verdict can be decided by another arm's mutation rather than by "
        f"the source on disk"
    )
    assert not list(cache.glob("under_test.*.pyc")), (
        "the last run's cache outlived the run, so the next import of the "
        "module loads the last mutation's bytecode"
    )


@pytest.mark.parametrize("relative", [True, False], ids=["relative", "absolute"])
def test_a_cache_under_a_pycache_prefix_is_cleared_where_the_cases_read_it(
    two_arms, tmp_path, monkeypatch, relative
):
    """#703, S9. Under `PYTHONPYCACHEPREFIX` the cache is a mirror of the
    source tree under the prefix, and CPython joins the prefix as given
    (`importlib._bootstrap_external.cache_from_source`). So a RELATIVE prefix
    is read against the directory of the process that imports: the cases'
    `--cwd`, not `arm-check`'s. Cleared from `arm-check`'s, the stale `.pyc`
    stays exactly where the cases read it — the defect the clear exists for.

    The path the cases read is taken from `cache_from_source` itself, with
    the prefix as a process in `other/` resolves it, so this case asks
    CPython where the file is rather than repeating the clear's own join.
    The absolute parameter pins what the relative one is joined to: there,
    `cwd` changes nothing.

    Red how: against the script at `a340221b` the relative parameter's runs
    see the planted cache, and `clear_bytecode_cache` does not take `cwd`.
    Executed."""
    module_path, _ = two_arms
    other = tmp_path / "other"
    other.mkdir()
    prefix = "specseal-prefix-703" if relative else str(tmp_path / "absolute-prefix")
    monkeypatch.setattr(sys, "pycache_prefix", os.path.join(str(other), prefix))
    planted = importlib.util.cache_from_source(str(module_path))
    # The prefix the clear reads is the environment's, as a session's would be.
    monkeypatch.setattr(sys, "pycache_prefix", None)
    monkeypatch.setenv("PYTHONPYCACHEPREFIX", prefix)

    def plant():
        os.makedirs(os.path.dirname(planted), exist_ok=True)
        with open(planted, "wb") as f:
            f.write(b"stale")

    plant()
    log = tmp_path / "seen.txt"
    probe = tmp_path / "sees_cache.py"
    probe.write_text(SEES_CACHE, encoding="utf-8")
    verdicts, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, str(probe), os.path.dirname(planted), str(log)],
        cwd=str(other),
    )
    assert refused == [] and len(verdicts) == 2
    seen = log.read_text(encoding="utf-8").split()
    assert seen == ["clean"] * 5, (
        f"{seen} — a run read the module's bytecode from the prefix mirror its "
        f"cwd resolves to, so its verdict can be another mutation's"
    )
    left = glob.glob(os.path.join(os.path.dirname(planted), "under_test.*.pyc"))
    assert left == [], f"{left} — the last run's cache outlived the run"

    # And the function on its own, as `mutation_check.py` calls it.
    plant()
    removed = ARM.clear_bytecode_cache(str(module_path), cwd=str(other))
    assert not os.path.exists(planted)
    assert [os.path.normcase(os.path.abspath(p)) for p in removed] == [
        os.path.normcase(os.path.abspath(planted))
    ]
    if not relative:
        # An absolute prefix is read the same from anywhere, so a caller that
        # passes no `cwd` clears it too.
        plant()
        assert ARM.clear_bytecode_cache(str(module_path)) and not os.path.exists(
            planted
        )


def test_no_verdict_is_taken_after_a_restore_that_did_not_land(two_arms):
    """What the PER-ARM restore buys over the one at the end of the run.

    The final restore leaves the tree clean either way. What only the per-arm
    one can do is stop the loop at the arm whose restore failed — every
    verdict after that point is measured against a mutated module, and the
    run would report them as if they meant something. That is the defect four
    fix passes met by hand in a day, and it is why the check is inside the
    loop rather than after it.

    Driven by making `restore` fail at the first arm, and counting how many
    arms got as far as running their command. The first run is the one
    against the module as it is, which writes nothing and restores nothing,
    so the first arm's is the second."""
    module_path, tests = two_arms
    ran = []
    real_run = ARM.subprocess.run

    def counting_run(cmd, **kwargs):
        ran.append(cmd)
        return real_run(cmd, **kwargs)

    def refuses_to_restore(path, original, original_sha):
        raise RuntimeError(f"{path} was not restored: deadbeef != {original_sha}")

    original_restore = ARM.restore
    ARM.subprocess.run = counting_run
    ARM.restore = refuses_to_restore
    try:
        with pytest.raises(RuntimeError, match="was not restored"):
            ARM.run_arms(str(module_path), tests)
    finally:
        ARM.subprocess.run = real_run
        ARM.restore = original_restore
    assert len(ran) == 2, (
        f"{len(ran) - 1} arms ran their command after a restore that did not "
        f"land. Every verdict past the first is measured against a mutated "
        f"module and reported as though it were not"
    )


def test_the_run_leaves_no_bytecode_cache_behind(two_arms):
    """No litter, so a later ordinary import of the module under test does
    not load bytecode the checker's own mutation produced.

    **This property has two mechanisms behind it and either one alone
    satisfies it** — the per-arm `clear_bytecode_cache` and the subprocess's
    `PYTHONDONTWRITEBYTECODE`. So the env var is an arm no case kills. It is
    kept for one narrow path: `run_arms` builds the child's environment from
    `dict(os.environ)`, so the subprocess cannot differ from this process
    through the environment — only a `--tests` command that sets
    `PYTHONPYCACHEPREFIX` itself puts the cache somewhere the clear does not
    look. Named here rather than pinned, because pinning the second mechanism
    separately would pin the implementation and not the claim."""
    module_path, tests = two_arms
    ARM.run_arms(str(module_path), tests)
    stale = list((module_path.parent / "__pycache__").glob("under_test.*.pyc"))
    assert stale == [], (
        f"{stale} — the run left bytecode for the mutated module, so an "
        f"ordinary import afterwards loads a mutation rather than the source"
    )


# A separator `str.splitlines` splits on that the tokenizer does not count,
# above an arm. Written as escapes rather than literally, so this file's own
# source says nothing about what the fixtures hold. Eight of the nine put the
# character inside a string literal, which is where `\u2028` and `\x85`
# realistically occur; the ninth is a form feed on its own line, the
# conventional page break in Python source.
NOT_LINE_ENDS = ("\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")
_TWO_ARM_SOURCE = (
    "{prelude}\n\ndef f(a, b):\n    if a and b:\n        return 1\n    return 0\n"
)
SPLICE_FIXTURES = [
    (
        f"in a string literal: {c!r}",
        _TWO_ARM_SOURCE.format(prelude=f'MESSAGE = "x{c}y"'),
    )
    for c in NOT_LINE_ENDS
]
SPLICE_FIXTURES.append(
    ("a form feed on its own line", _TWO_ARM_SOURCE.format(prelude="\x0c"))
)
# And the two endings `ast` DOES count, because a split that keeps only `\n`
# is the same defect from the other side: a lone `\r` ends a line for the
# tokenizer, and `\r\n` ends exactly one.
_PLAIN = _TWO_ARM_SOURCE.format(prelude='MESSAGE = "x"')
SPLICE_FIXTURES.append(("CRLF endings", _PLAIN.replace("\n", "\r\n")))
SPLICE_FIXTURES.append(("lone CR endings", _PLAIN.replace("\n", "\r")))


@pytest.mark.parametrize(
    "label,source", SPLICE_FIXTURES, ids=[f[0] for f in SPLICE_FIXTURES]
)
def test_a_separator_the_tokenizer_ignores_does_not_move_a_spliced_arm(label, source):
    """Round 1's finding 3, as the class rather than as the coordinate.

    `str.splitlines` splits on eight characters `ast` does not count. Split on
    one, `span.lineno` and the list index part company, and every arm below it
    comes back as an un-asked pair with an `IndentationError` beside it: the
    enumeration going short through a door
    `test_every_ast_constructor_is_classified` cannot see. The bad outcome is
    quieter — a mis-indexed splice that happens to parse is a verdict recorded
    against a mutation nobody asked for, which no hash catches.

    `_splice` is the ONLY place in the checker that turns a `lineno` into a
    list index; every other reader of one displays or sorts it. So the class
    has one site, and this is it.

    Red how, both ways round. `_lines` replaced by
    `source.splitlines(keepends=True)` raises `IndentationError` on all nine
    of the separators, and `_LINE_END` narrowed to `\\n` alone raises it on
    the lone-CR fixture — a split that keeps too few terminators is the same
    defect as one that keeps too many. Executed."""
    first, second = ARM.arms(source)
    assert first.source == "a", f"{label}: the span itself is right either way"
    assert "if not (a) and b:" in ARM.mutate(source, first)
    assert "if a and not (b):" in ARM.mutate(source, second)
    for arm in (first, second):
        ast.parse(ARM.mutate(source, arm))
        ast.parse(ARM.mutate(source, arm, "remove"))


# --- the command that decides the verdict can hang or fail to start -------

# A command that passes against the module as it is and never returns against
# any mutation of it, because the run against the unmutated module has to
# pass before a pair is asked at all (#703). It compares the module's bytes
# with a copy rather than importing it: dropping the unwatched `flag` arm
# leaves `classify("example.com", ...)` unchanged, so a probe that imports
# and sleeps on a changed answer would let that pair return, and these cases
# pin that EVERY pair hangs. `-S` skips `site`, so the passing run starts
# fast enough to finish inside the bound these cases pass.
HANGS_ON_A_MUTATION = """\
import sys
import time

with open(sys.argv[1], "rb") as a, open(sys.argv[2], "rb") as b:
    if a.read() != b.read():
        time.sleep(30)
"""

# Wide enough for the passing run's interpreter to start on a loaded runner;
# every pair waits it out, so it is paid four times per case.
HANG_BOUND = 1.0


def hangs_on_a_mutation(module_path):
    """The command, with the copy and the probe written beside the module."""
    copy = module_path.parent / "as_it_was.py"
    copy.write_bytes(module_path.read_bytes())
    probe = module_path.parent / "hangs_on_a_mutation.py"
    probe.write_text(HANGS_ON_A_MUTATION, encoding="utf-8")
    return [sys.executable, "-S", str(probe), str(module_path), str(copy)]


def test_a_command_that_never_returns_is_recorded_as_unmeasured(two_arms):
    """Round 1's finding 1, the bounded half.

    While an arm's command runs, the module on disk holds the mutation and
    `capture_output=True` means nothing is printed — so an unbounded hang is
    indistinguishable from a slow suite, and the longer the process lives
    mutated the more likely it is ended by something no `finally` sees. The
    bound turns the hang into a NAMED unmeasured pair rather than a wait:
    `killed` would read as *a case noticed* and `survived` as *none did*, and
    neither was measured.

    Red how: `timeout=timeout` removed from the pair's `subprocess.run` call
    hangs this case for 30 seconds per pair instead of failing. Executed —
    and the run is bounded here by the bound the case passes, not by the
    default. The command passes against the unmutated module, so the pairs
    are what time out and not the run before them.
    """
    module_path, _ = two_arms
    verdicts, refused = ARM.run_arms(
        str(module_path), hangs_on_a_mutation(module_path), timeout=HANG_BOUND
    )
    # Every pair timed out, so no arm has a verdict from any operator and
    # both are refused rather than reported as survivors.
    assert verdicts == []
    assert len(refused) == 2
    for _arm, why in refused:
        assert f"did not return within {HANG_BOUND}s" in why, (
            f"{why!r} — a timed-out pair has to say it was not measured and "
            f"what bound it, or the report reads as a verdict"
        )


def test_a_spawn_failure_keeps_the_verdicts_already_measured(two_arms):
    """Round 1's finding 2, and it is the module's own subject arriving from
    the other side.

    `OSError` out of `subprocess.run` used to leave `run_arms` entirely, so
    one failed spawn discarded every verdict measured before it and printed
    no report at all. `bin/test` builds a virtual environment on demand, so a
    mid-run spawn failure is a reachable state rather than a constructed one.

    Driven by making the fourth of the five calls raise — the first is the
    run against the module as it is, arm one is fully measured by the
    fourth, and arm two by nothing.

    Red how: deleting the `except OSError` clause raises `OSError` out of
    `run_arms` here and the first arm's two verdicts are lost. Executed."""
    module_path, tests = two_arms
    real_run = ARM.subprocess.run
    calls = []

    def fails_from_the_fourth_call(cmd, **kwargs):
        calls.append(cmd)
        if len(calls) >= 4:
            raise OSError("Errno 8: Exec format error")
        return real_run(cmd, **kwargs)

    ARM.subprocess.run = fails_from_the_fourth_call
    try:
        verdicts, refused = ARM.run_arms(str(module_path), tests)
    finally:
        ARM.subprocess.run = real_run

    assert len(calls) == 5, "every pair still had its command attempted"
    assert [(v.arm.source, sorted(v.by_operator)) for v in verdicts] == [
        ('host == "example.com"', ["invert", "remove"])
    ], "the verdicts taken before the failure are real and must survive it"
    assert len(refused) == 1
    _arm, why = refused[0]
    assert "OSError" in why and "Exec format error" in why, (
        f"{why!r} — an arm nothing could be spawned for is unmeasured, and "
        f"the reason has to reach the report"
    )


# The two doors to the no-verdict list with a mutation already on disk. Both
# were written, run and restored before the arm got there, which is what
# neither headline line used to say. Each is a command that passes against
# the module as it is, because nothing reaches a pair before that run passes
# (#703): the hang is `hangs_on_a_mutation`, and the spawn failure is a
# `subprocess.run` that spawns a command that does not exist from its second
# call on.
NO_VERDICT_DOORS = ["every pair times out", "the command cannot be spawned"]


@pytest.mark.parametrize("label", NO_VERDICT_DOORS, ids=NO_VERDICT_DOORS)
def test_the_report_does_not_call_a_mutated_arm_unmutated(two_arms, monkeypatch, label):
    """Round 2's finding 15. §14 — the report is what a person reads.

    An arm reached this list only when `mutate` had no mutation for any
    operator, so nothing had been written to disk and *enumerated and not
    mutated* was true. The timeout and `OSError` paths write the mutation, run
    the command, restore, and land in the same list — where the header said
    *enumerated and not mutated* and the summary counted the arm as never
    mutated. Both were false after four mutations, and `0 arms mutated · 0
    killed · 0 watched by no case` reads as a clean sweep at exit 0.

    Both doors are driven, because the cause is one: an arm with no verdict is
    not an arm nothing touched.

    Red how: either label restored prints `not mutated` or `arms mutated`
    here. Executed on both parameters."""
    module_path, tests = two_arms
    if label == "every pair times out":
        tests, timeout = hangs_on_a_mutation(module_path), HANG_BOUND
    else:
        timeout = 900.0
        real_run = ARM.subprocess.run
        calls = []

        def cannot_spawn_after_the_first_call(cmd, **kwargs):
            calls.append(cmd)
            if len(calls) == 1:
                return real_run(cmd, **kwargs)
            return real_run(["specseal-no-such-command-xyz"], **kwargs)

        monkeypatch.setattr(ARM.subprocess, "run", cannot_spawn_after_the_first_call)
    before = hashlib.sha256(module_path.read_bytes()).hexdigest()
    loop = []
    verdicts, refused = ARM.run_arms(
        str(module_path), tests, timeout=timeout, echo=loop.append
    )
    assert verdicts == []
    assert len(refused) == 2
    assert hashlib.sha256(module_path.read_bytes()).hexdigest() == before, (
        "the premise of this case is that the mutation was applied and then "
        "restored, so the module has to be back"
    )

    lines = []
    found = [v.arm for v in verdicts] + [a for a, _ in refused]
    ARM._report(str(module_path), verdicts, refused, ARM.counts(found), lines.append)
    text = "\n".join(lines)
    assert "not mutated" not in text, (
        f"{text!r} — every one of these arms was mutated on disk and then "
        f"restored; what was missing is a verdict, not the mutation"
    )
    assert "arms mutated" not in text, (
        "the summary counts arms that produced a verdict, and an arm that "
        "was mutated without producing one is not among them"
    )
    assert "2 arms with no verdict from any operator" in text
    assert "2 arms measured" not in text and "0 arms measured" in text
    # And the per-arm line the loop prints, for the same reason.
    assert not any("refused" in line for line in loop), (
        f"{loop!r} — `refused` reads as *never tried* for an arm whose "
        f"mutation was written and run"
    )
    assert sum("no verdict" in line for line in loop) == 2


def test_the_help_says_the_bound_reaches_the_command_and_not_its_children(capsys):
    """Round 2's finding 16. §14 — the help text is what a person reads
    before they type the command the skill documents.

    `subprocess.run` sends the kill to the direct child and to nothing below
    it. `bin/test` is `exec python3 .github/scripts/run_tests.py`, and that
    script runs pytest through `subprocess.run`, so the documented
    `--tests "bin/test ..."` form puts the suite one process below the one the
    bound reaches: a timed-out pair leaves a whole suite running, unbounded
    and unreported, competing with every arm after it.

    Two claims, both of which the help got wrong. The bound is per operator
    command, not per arm — an arm asks two, so it can take twice it — and it
    bounds the wait rather than the work.

    Pinned here rather than in the docstring: this text is output, and a
    reader acts on it without opening the source. Whether the bound SHOULD
    reach a process group is #313, not this case.

    Red how: either claim removed from the help. Executed."""
    with pytest.raises(SystemExit):
        ARM.main(["--help"])
    text = " ".join(capsys.readouterr().out.split()).lower()
    assert (
        "only the command's own process is killed, not anything it spawned" in text
    ), (
        "a bound that reads as bounding the command sends a reader to type "
        "the wrapper form the skill documents and leaves a suite behind"
    )
    assert "an arm asks two operators, so it can take twice this" in text, (
        "and the bound is per operator command, measured at 2.0s for one arm "
        "against a 1-second bound"
    )
    # #703: the run against the unmutated module comes first, under the same
    # bound, and a reader typing `--tests` has to know it must pass there.
    assert "the same bound covers the first run against the unmutated module" in text
    assert "runs once against the module as it is first and has to pass" in text, (
        "a `--tests` that does not pass against the module refuses the run, "
        "and the flag's own help is where a person learns that before typing it"
    )


def test_a_negative_bound_is_refused_rather_than_measured(two_arms, capsys):
    """Round 2's finding 17, and it is finding 15's cause through a door no
    label can close.

    `type=float` accepts a negative and `args.timeout or None` passes it
    through, so `subprocess.run` raises `TimeoutExpired` before the command
    starts: every pair of every arm unmeasured, exit 0, and a survivor count
    of zero. `0` is documented as removing the bound and `-1` is how several
    tools spell the same intention, so a person who types it gets the best
    possible result out of a run that measured nothing.

    Honest labels are not enough here — round 2's finding 15 makes the report
    true, and *0 arms measured · 0 watched by no case* is still what a run
    with a typo in it prints. So the value is refused at parse time, which is
    the only place the run can be stopped before it wastes the wall clock.

    A tiny positive bound is NOT refused, and that is deliberate: `0.001` is
    a legitimate thing to type against a fast command, and finding 15's
    labels are what make its output readable.

    Red how: the guard deleted gives exit 0 and `0 arms measured`, measured
    through `main`. Executed."""
    module_path, tests = two_arms
    with pytest.raises(SystemExit) as exit_code:
        ARM.main([str(module_path), "--tests", shlex.join(tests), "--timeout", "-1"])
    assert exit_code.value.code == 2, "argparse's own usage-error exit"
    printed = capsys.readouterr()
    assert "--timeout takes a non-negative number of seconds" in printed.err
    assert "survivor count of zero it never measured" in printed.err, (
        "the refusal has to say what would have happened, or it reads as an "
        "arbitrary validation rule"
    )
    assert "arms measured" not in printed.out, "and nothing was run"


def test_a_pair_whose_command_ran_and_answered_nothing_is_not_called_unasked(two_arms):
    """Finding 15's cause through its third door, which the record does not
    name.

    An arm ANOTHER operator measured is not refused, and its unanswered pair
    is listed on its own. That section said *operator/arm pairs not asked* —
    true while the only way to get there was `mutate` refusing before
    anything ran, and false for a pair whose command was spawned, waited for
    and killed at the bound.

    Driven by timing out the third of the five calls only — the first is the
    run against the module as it is, the third is arm one's `remove` — so one
    arm has a measured operator and an unanswered one.

    Red how: the header restored prints `not asked` here. Executed."""
    module_path, tests = two_arms
    real_run = ARM.subprocess.run
    calls = []

    def times_out_on_the_third_call(cmd, **kwargs):
        calls.append(cmd)
        if len(calls) == 3:
            raise ARM.subprocess.TimeoutExpired(cmd, kwargs.get("timeout") or 0.3)
        return real_run(cmd, **kwargs)

    ARM.subprocess.run = times_out_on_the_third_call
    try:
        verdicts, refused = ARM.run_arms(str(module_path), tests)
    finally:
        ARM.subprocess.run = real_run

    assert refused == []
    first = verdicts[0]
    assert sorted(first.by_operator) == ["invert"]
    assert "TimeoutExpired" in first.not_applicable["remove"]

    lines = []
    ARM._report(
        str(module_path),
        verdicts,
        refused,
        ARM.counts([v.arm for v in verdicts]),
        lines.append,
    )
    text = "\n".join(lines)
    assert "1 operator/arm pairs with no verdict" in text
    assert "not asked" not in text, (
        f"{text!r} — this pair's command was spawned, waited for and killed "
        f"at the bound. Only a pair `mutate` refused was never asked, and the "
        f"reason beside each is what tells the two apart"
    )


# --- the command has to pass against the module as it is first ------------

# What `--tests` exits with against the module whatever the module holds. The
# three shapes of a run that measured nothing and came back as a clean report
# (#703): pytest exits 5 when a `-k` selects no case and 4 on a usage error
# such as a module path that does not exist, and a case already failing exits
# 1. Each used to print `killed` beside every arm at exit 0. The probe prints
# a line first, so a case can see the command's own output reach the reader.
NOT_GREEN = """\
import sys

print({said!r})
sys.exit({code})
"""

# The shape a person meets: a case that imports the module and asserts
# something false of it, mutated or not. The suite was red before anybody
# mutated anything.
ALREADY_FAILING = """\
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

assert m.classify("example.com", False) == "unknown", "this case already fails"
"""

NO_BASELINE_SHAPES = [
    ("a -k that selects no case", 5, "no tests ran"),
    ("a module path that does not exist", 4, "file or directory not found"),
    ("a case that already fails", 1, "1 failed"),
    ("a case that already fails, through an import", None, "this case already fails"),
    # An OOM kill or a SIGKILL is a negative return code, and a check narrowed
    # to `> 0` would read it as a pass (round 1, ⬜ 4). POSIX alone has one.
    pytest.param(
        "a run killed by a signal",
        -9,
        "sending itself SIGKILL",
        marks=pytest.mark.skipif(os.name == "nt", reason="no signals on Windows"),
    ),
]

# The probe for the signal shape: it prints, then sends itself SIGKILL.
KILLS_ITSELF = """\
import os
import sys

print({said!r}, flush=True)
os.kill(os.getpid(), 9)
"""

# A time well in the past, set on the module before a refused run. A write
# moves the mtime even when it writes the bytes that were there, so this is
# what tells "nothing was written" from "written and restored" -- which a
# byte comparison cannot.
LONG_AGO_NS = 10**18


def nothing_was_written(module_path, before):
    """The module holds the bytes it held, was never written, and has no
    cached bytecode beside it."""
    assert module_path.read_bytes() == before
    assert module_path.stat().st_mtime_ns == LONG_AGO_NS, (
        "the module was written: a refused run has to refuse before the first "
        "write, or *Nothing was written* is a sentence about a restore"
    )
    assert not list((module_path.parent / "__pycache__").glob("under_test.*.pyc"))


def refusal_line(out):
    """The verdict line of a refused run, with the three pieces it is pinned
    by checked: the word, the sentence that says why, and the sentence that
    says what holds afterwards (§14)."""
    first = out.splitlines()[0]
    assert first.startswith("no baseline: "), (
        f"{out!r} — a run whose command does not pass against the module as it "
        f"is measured nothing, and its first line has to say so"
    )
    assert "a failure under a mutation says nothing about the mutation" in first
    assert first.endswith("Nothing was written and no arm was measured."), first
    assert "killed" not in out and "SURVIVED" not in out, (
        f"{out!r} — no arm was measured, so no arm can carry a verdict"
    )
    assert "arms measured" not in out
    return first


@pytest.mark.parametrize(
    "label,code,said",
    NO_BASELINE_SHAPES,
    ids=[getattr(s, "values", s)[0] for s in NO_BASELINE_SHAPES],
)
def test_a_command_that_does_not_pass_against_the_module_refuses_the_run(
    two_arms, tmp_path, capsys, label, code, said
):
    """#703, S1 to S3. A `killed` is a measurement only when the same command
    passed against the unmutated module.

    `run_arms` read `returncode != 0` as *a case noticed* and ran nothing to
    compare it with, so a command that cannot pass at all recorded every arm
    killed: `0 watched by no case`, exit 0, the best report there is out of a
    run that measured nothing. Now the command runs once against the module
    as it is, and anything but a pass refuses the run before the first write.

    The command's own output follows the verdict line, because it is the one
    run whose cause a person has to read to act on it — pytest's *no tests
    ran* is what tells a mistyped `-k` from a failing case.

    Red how: against the script at `a340221b` every shape prints `killed`
    beside both arms and exits 0. Executed."""
    module_path, _ = two_arms
    probe = tmp_path / "not_green.py"
    if code is None:
        probe.write_text(ALREADY_FAILING, encoding="utf-8")
        tests = [sys.executable, str(probe), str(module_path)]
        code = 1
    elif code < 0:
        probe.write_text(KILLS_ITSELF.format(said=said), encoding="utf-8")
        tests = [sys.executable, str(probe)]
    else:
        probe.write_text(NOT_GREEN.format(said=said, code=code), encoding="utf-8")
        tests = [sys.executable, str(probe)]
    before = module_path.read_bytes()
    os.utime(module_path, ns=(LONG_AGO_NS, LONG_AGO_NS))

    status = ARM.main([str(module_path), "--tests", shlex.join(tests)])

    out = capsys.readouterr().out
    first = refusal_line(out)
    assert f"no baseline: exit {code}." in first, (
        f"{first!r} — the exit is what tells a `-k` that selected nothing (5) "
        f"from a case that already fails (1)"
    )
    assert said in out, (
        f"{out!r} — the command's own output has to follow the verdict, or "
        f"the cause is one re-run away"
    )
    assert status == 2, "exit 2 is the run refused before measuring"
    nothing_was_written(module_path, before)


def test_the_run_against_the_unmutated_module_is_bounded_by_the_timeout(two_arms):
    """#703, S4. The bound reaches the first run too.

    A command that hangs whatever the module holds now hangs in the run
    against the module as it is, before anything is written. Unbounded there,
    it is the one wait in the whole run that nothing ends — #641's round 2
    found its sibling's baseline bound pinned by no case and survived a
    mutation to `None`.

    Red how: against the script at `a340221b` both arms are filed as no
    verdict after four 0.3s waits and nothing is raised; with the baseline's
    `timeout=timeout` removed this waits the whole 30 seconds and then the
    arms time out one by one. Executed."""
    module_path, _ = two_arms
    before = module_path.read_bytes()
    os.utime(module_path, ns=(LONG_AGO_NS, LONG_AGO_NS))
    started = time.monotonic()
    with pytest.raises(ARM.NoBaseline) as refused:
        ARM.run_arms(
            str(module_path),
            [sys.executable, "-c", "import time; time.sleep(30)"],
            timeout=0.3,
        )
    elapsed = time.monotonic() - started
    assert "did not return within 0.3s" in refused.value.reason, refused.value.reason
    assert elapsed < 15, (
        f"{elapsed:.1f}s — the run against the unmutated module was not "
        f"bounded by the 0.3s the case passed"
    )
    nothing_was_written(module_path, before)


def test_a_first_run_that_timed_out_carries_what_it_printed(
    two_arms, monkeypatch, capsys
):
    """What a hung suite printed before the bound is the nearest thing to
    its cause, so it is carried as the refusal's output.

    It arrives as bytes, and it is decoded with replacement: the output is
    shown, not trusted to be UTF-8, and a suite printing anything else must
    not turn the refusal into a traceback. Driven by a `subprocess.run` that
    raises at once, because a real command's output before a short bound
    depends on how fast its interpreter starts.

    And it reaches the person, not only the exception: `main` prints it after
    the verdict line, on this path as on a non-zero exit (round 1, ⬜ 5).

    Red how: the timeout arm's output dropped, or decoded strictly; and
    `main` printing the output only for an `exit` reason. Executed."""
    module_path, tests = two_arms

    def times_out(cmd, **kwargs):
        raise ARM.subprocess.TimeoutExpired(
            cmd,
            kwargs["timeout"],
            output=b"collected 3 items \xff\n",
            stderr=b"slow\n",
        )

    monkeypatch.setattr(ARM.subprocess, "run", times_out)
    with pytest.raises(ARM.NoBaseline) as refused:
        ARM.run_arms(str(module_path), tests, timeout=0.3)
    assert "collected 3 items \ufffd" in refused.value.output
    assert "slow" in refused.value.output
    assert "b'" not in refused.value.output, "decoded, not the bytes' repr"
    assert ARM.main([str(module_path), "--tests", shlex.join(tests)]) == 2
    assert "collected 3 items" in capsys.readouterr().out.split("\n", 1)[1], (
        "what the hung suite printed has to reach the reader, below the line"
    )


def test_the_first_run_is_taken_where_the_pairs_are(two_arms, tmp_path):
    """The run against the module as it is answers for the pairs only when it
    is the same command in the same place. A command relative to `cwd` that
    passed elsewhere, or failed only because it ran elsewhere, would decide
    the run on the wrong directory.

    Red how: `cwd=cwd` dropped from the first run refuses this run with exit
    2, because the probe exists only under `cwd`. Executed."""
    module_path, _ = two_arms
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "watches_one.py").write_text(WATCHES_ONE, encoding="utf-8")
    verdicts, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, "watches_one.py", str(module_path)],
        cwd=str(elsewhere),
    )
    assert refused == []
    assert [(v.arm.source, v.killed) for v in verdicts] == [
        ('host == "example.com"', True),
        ("flag", False),
    ]


@pytest.mark.parametrize("only", [None, "no_such_scope"], ids=["no arms", "--only"])
def test_the_first_run_is_taken_whatever_the_arms_are(tmp_path, only):
    """Once per `--tests` call, with no exception to state: a module with no
    arms, or an `--only` that selects none of them, still has its command run
    once and refused when it does not pass. A command that cannot pass is the
    thing to learn whichever arms there are.

    Red how: the first run made conditional on there being an arm to mutate
    leaves both parameters returning an empty report. Executed."""
    module_path = tmp_path / "plain.py"
    module_path.write_text(
        "def f(x):\n    if x:\n        return 1\n    return 0\n"
        if only
        else "VALUE = 1\n",
        encoding="utf-8",
    )
    with pytest.raises(ARM.NoBaseline, match="exit 3"):
        ARM.run_arms(
            str(module_path),
            [sys.executable, "-c", "import sys; sys.exit(3)"],
            only=only,
        )


def test_a_command_that_cannot_be_spawned_refuses_the_run(two_arms, capsys):
    """#703, S5. A command that cannot start against the unmutated module
    cannot start against a mutation either, so nothing is measured.

    Red how: against the script at `a340221b` both arms land in the no-verdict
    list at exit 0. Executed."""
    module_path, _ = two_arms
    before = module_path.read_bytes()
    os.utime(module_path, ns=(LONG_AGO_NS, LONG_AGO_NS))

    status = ARM.main([str(module_path), "--tests", "specseal-no-such-command-xyz"])

    first = refusal_line(capsys.readouterr().out)
    assert "FileNotFoundError" in first, (
        f"{first!r} — the error is the cause, and the line has to name it"
    )
    assert status == 2
    nothing_was_written(module_path, before)


def test_a_passing_first_run_changes_no_verdict_and_costs_one_run(
    two_arms, monkeypatch
):
    """#703, S6. One run against the module as it is, before any write, and
    the verdicts it lets through are the ones measured before it existed.

    Watched by what the module held at each call: the first call has to see
    the unmutated bytes and every later one a mutation.

    Red how: against the script at `a340221b` there are four calls and the
    first sees a mutation; with the baseline moved after the first write the
    first call sees a mutation. Executed."""
    module_path, tests = two_arms
    original = module_path.read_bytes()
    real_run = ARM.subprocess.run
    held = []

    def watching_run(cmd, **kwargs):
        held.append(module_path.read_bytes())
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(ARM.subprocess, "run", watching_run)
    verdicts, refused = ARM.run_arms(str(module_path), tests)

    assert refused == []
    assert [(v.arm.source, v.killed) for v in verdicts] == [
        ('host == "example.com"', True),
        ("flag", False),
    ]
    assert len(held) == 5, f"{len(held)} runs — one against the module, four pairs"
    assert held[0] == original, (
        "the first run has to be against the module as it is, before anything "
        "is written"
    )
    assert all(h != original for h in held[1:]), "and every later one a mutation"


# What a first run that does not pass does to the module itself, before it
# exits 1: the ways a suite can leave its own input changed. The last one
# leaves it so that it cannot be put back at all.
CHANGES_THE_MODULE = {
    "rewrites it": "open(sys.argv[1], 'w').write('VALUE = 99\\n')",
    "removes it": "os.remove(sys.argv[1])",
    "locks it": "os.chmod(sys.argv[1], 0)",
}

# POSIX modes, and root reads a mode-000 file anyway.
CANNOT_LOCK = os.name == "nt" or getattr(os, "geteuid", lambda: 1)() == 0


@pytest.mark.parametrize(
    "change",
    [
        "removes it",
        "rewrites it",
        pytest.param(
            "locks it",
            marks=pytest.mark.skipif(
                CANNOT_LOCK, reason="needs a POSIX mode root obeys"
            ),
        ),
    ],
)
def test_a_refused_run_leaves_the_module_as_it_was_before_the_command(
    two_arms, tmp_path, capsys, monkeypatch, change
):
    """Round 1's 🟡 1. The first run sits outside the `try` whose `finally`
    restores, so nothing `arm-check` does there writes the module. The cases
    can, though: a formatter's round-trip test or a generator that rewrites a
    file in place. At `a340221b` every run ended with the module put back
    from the bytes held, and a refusal must not be the one path that keeps
    the cases' version instead, while it says *Nothing was written*.

    Removed is the same fact as rewritten: what is on disk is not what was
    read, and a file that cannot be read differs.

    **Locked is the one shape that cannot be put back** (round 2, 🟡 1).
    The put-back's own `open` fails, and raised out of the `finally` it took
    the refusal's line and the command's output with it, at exit 1, where
    `6bbaa4d1` refused at exit 2. The line names the error instead.

    Red how: at `6bbaa4d1` the module is left as the command changed it, and
    the line says *Nothing was written*; at `dc1b0d14` the locked module is
    a `PermissionError` traceback and no line. Executed on every parameter."""
    module_path, _ = two_arms
    before = module_path.read_bytes()
    probe = tmp_path / "changes_the_module.py"
    probe.write_text(
        "import os\nimport sys\nprint('the cases ran')\n"
        + CHANGES_THE_MODULE[change]
        + "\nsys.exit(1)\n",
        encoding="utf-8",
    )
    tests = [sys.executable, str(probe), str(module_path)]

    try:
        status = ARM.main([str(module_path), "--tests", shlex.join(tests)])
    finally:
        if change == "locks it":
            os.chmod(module_path, 0o644)

    out = capsys.readouterr().out
    first = out.splitlines()[0]
    assert status == 2
    assert first.startswith("no baseline: exit 1."), out
    assert "the cases ran" in out, "the command's own output follows the line"
    if change == "locks it":
        assert "putting it back failed: PermissionError" in first, first
        assert "Nothing was written" not in first and "was put back" not in first
        assert first.endswith("No arm was measured."), first
        assert module_path.read_bytes() == before, "a mode change leaves the bytes"
        # A pass that cannot put the module back propagates, as the loop's own
        # first write would fail on it; that path is not this case's.
        return
    assert "was put back from the bytes read before it" in first, first
    assert "Nothing was written" not in first, (
        f"{first!r} — the command wrote the module, so the sentence that says "
        f"nothing was would be false"
    )
    assert first.endswith("No arm was measured."), first
    assert module_path.read_bytes() == before, (
        f"the module was left as the command {change.split()[0]} it"
    )

    # And when the same command passes, with `--only` selecting no arm: the
    # module still comes back. Two restores cover this path, the first run's
    # and the loop's outer `finally`, so this holds the outcome rather than
    # either one.
    probe.write_text(
        "import os\nimport sys\n" + CHANGES_THE_MODULE[change] + "\nsys.exit(0)\n",
        encoding="utf-8",
    )
    only = ["--only", "no_such_scope"]
    assert ARM.main([str(module_path), "--tests", shlex.join(tests), *only]) == 0
    assert module_path.read_bytes() == before, (
        f"a passing first run {change.split()[0]} the module and it stayed so"
    )

    # And when the first run is interrupted after the command changed the
    # module. The loop's outer `finally` is never entered on this path, so the
    # first run's own put-back is the only restore it has (round 2, ⬜ 2:
    # narrowed to a refusal, the put-back survived every other assertion).
    def interrupted(cmd, **kwargs):
        # The command changes the module the way this parameter's does, in
        # this process, and then the interrupt lands.
        argv = type("sys", (), {"argv": [None, str(module_path)]})
        exec(CHANGES_THE_MODULE[change], {"os": os, "sys": argv})
        raise KeyboardInterrupt

    monkeypatch.setattr(ARM.subprocess, "run", interrupted)
    with pytest.raises(KeyboardInterrupt):
        ARM.run_arms(str(module_path), tests)
    assert module_path.read_bytes() == before, (
        f"an interrupted first run {change.split()[0]} the module and it stayed so"
    )


def test_a_refusal_survives_a_console_that_cannot_encode_its_output(two_arms, tmp_path):
    """Round 1's 🟡 2. `_text` turns a byte that is not UTF-8 into U+FFFD, and
    a console in cp1252 cannot encode that character, so the refusal's own
    output ended in a `UnicodeEncodeError` at exit 1. A Windows pipe is in
    the ANSI code page, which is where an agent's captured run meets it. The
    entry block every other skill script carries is what fixes it, so the
    script is run as a process, the way that block is reached.

    Red how: at `6bbaa4d1` the refusal line is followed by a traceback and
    exit 1. Executed."""
    module_path, _ = two_arms
    probe = tmp_path / "prints_a_byte.py"
    probe.write_text(
        "import sys\nsys.stdout.buffer.write(b'x \\xff y\\n')\nsys.exit(1)\n",
        encoding="utf-8",
    )
    tests = shlex.join([sys.executable, str(probe)])
    run = subprocess.run(
        [sys.executable, SCRIPT, str(module_path), "--tests", tests],
        capture_output=True,
        env=dict(os.environ, PYTHONIOENCODING="cp1252"),
    )
    assert run.returncode == 2, run.stderr.decode("utf-8", "replace")
    assert b"Traceback" not in run.stderr
    assert run.stdout.startswith(b"no baseline: exit 1.")


def test_a_pair_whose_cases_print_a_byte_that_is_not_utf8_keeps_its_verdict(
    two_arms, tmp_path
):
    """Round 1's 🟡 3. A pair's output is never read, and `text=True` decoded
    it strictly anyway, so one mutation whose cases print a byte that is not
    UTF-8 raised `UnicodeDecodeError` out of `run_arms` and every verdict
    measured before it went with it. The same class as the first run's
    decode, in the same function.

    Red how: at `6bbaa4d1` `UnicodeDecodeError` leaves `run_arms`. Executed."""
    module_path, _ = two_arms
    copy = tmp_path / "as_it_was.txt"
    copy.write_bytes(module_path.read_bytes())
    probe = tmp_path / "prints_on_a_mutation.py"
    probe.write_text(
        "import sys\n"
        "if open(sys.argv[1], 'rb').read() != open(sys.argv[2], 'rb').read():\n"
        "    sys.stdout.buffer.write(b'boom \\xff\\n')\n"
        "    sys.exit(1)\n",
        encoding="utf-8",
    )
    verdicts, refused = ARM.run_arms(
        str(module_path), [sys.executable, str(probe), str(module_path), str(copy)]
    )
    assert refused == []
    assert [v.killed for v in verdicts] == [True, True]


# --- the two operators are not interchangeable ----------------------------


def test_removing_an_arm_rewrites_its_whole_decision():
    """`remove` cannot be done inside the arm's own span.

    Dropping a member of `a and b` has to rewrite `a and b`, which is why an
    `Arm` carries a second span and the text its decision reads without it.
    Spliced inside the member instead, `a and b` would become ` and b` and
    every arm of the module would be killed by a `SyntaxError`."""
    source = "def f(a, b, c):\n    if a and b and c:\n        return 1\n    return 0\n"
    first, second, third = ARM.arms(source)
    # Parenthesised: the group span covers whatever brackets the source
    # used, so the remainder has to bring its own back.
    assert first.group_without == "(b and c)"
    assert second.group_without == "(a and c)"
    assert third.group_without == "(a and b)"
    assert "if (b and c):" in ARM.mutate(source, first, "remove")
    assert "if (a and c):" in ARM.mutate(source, second, "remove")
    for arm in (first, second, third):
        ast.parse(ARM.mutate(source, arm, "remove"))


def test_removing_a_sole_arm_makes_its_branch_never_run():
    """A decision with nothing left in it.

    `False` rather than `True`, and the choice is #262's own: *"removing `not
    segs` makes the stray and unreadable notices fire on every Bash call"* —
    the guard clause's body stops happening. The other reading, that the body
    always happens, is the same edit seen from the other side."""
    source = "def f(segs):\n    if not segs:\n        return None\n    return segs\n"
    (arm,) = ARM.arms(source)
    assert ARM.EMPTY_DECISION == "False"
    assert arm.group_without == "(False)"
    assert "if (False):" in ARM.mutate(source, arm, "remove")


def test_removing_an_except_type_leaves_the_handler_catching_the_others():
    """A tuple loses one member; a sole type is aimed at what nothing raises.

    The two spellings are one operator — *this handler no longer catches
    this* — and the second is `NEVER_RAISED` because an `except ():` catching
    nothing is the same thing said less legibly."""
    tuple_source = (
        "def f():\n    try:\n        pass\n    except (OSError, ValueError):\n"
        "        pass\n"
    )
    first, second = ARM.arms(tuple_source)
    assert "except (ValueError):" in ARM.mutate(tuple_source, first, "remove")
    assert "except (OSError):" in ARM.mutate(tuple_source, second, "remove")

    sole_source = (
        "def f():\n    try:\n        pass\n    except OSError:\n        pass\n"
    )
    (only,) = ARM.arms(sole_source)
    assert "_specseal_never_raised" in ARM.mutate(sole_source, only, "remove")


# An arm exactly ONE operator kills, which is the only shape that can tell
# `any` from `all`. The case passes `True, True` and asserts the body runs:
# inverting `a` stops it (killed), while dropping `a` leaves `if b:` and `b`
# is true, so the body still runs (survived).
SPLIT_VERDICT = """\
def both(a, b):
    if a and b:
        return "yes"
    return "no"
"""

WATCHES_BOTH_TRUE = """\
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("under_test", sys.argv[1])
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

assert m.both(True, True) == "yes"
"""


def test_an_arm_is_watched_when_any_operator_is_noticed(tmp_path):
    """The combined verdict, and why it is the one that answers #262.

    The question *is this arm watched* is whether ANY case depends on it, so
    one operator noticing is enough. The per-operator rows stay beside it
    because they answer narrower questions — and #262's table of unwatched
    arms is an answer to `remove` alone.

    **This needs an arm exactly one operator kills, or it cannot tell `any`
    from `all`.** An earlier version used the two-arm fixture, where both
    operators agree on both arms; `any` swapped for `all` left it green.
    `if a and b:` against a case that passes `True, True` is the split: the
    inversion is noticed and the removal is not."""
    module_path = tmp_path / "under_test.py"
    module_path.write_text(SPLIT_VERDICT, encoding="utf-8")
    case_path = tmp_path / "watches_both_true.py"
    case_path.write_text(WATCHES_BOTH_TRUE, encoding="utf-8")
    tests = [sys.executable, str(case_path), str(module_path)]

    verdicts, refused = ARM.run_arms(str(module_path), tests)
    assert refused == []
    first, _second = verdicts
    assert first.by_operator == {"invert": True, "remove": False}, (
        "this case is only meaningful while exactly one operator kills this "
        "arm; both agreeing makes `any` and `all` indistinguishable"
    )
    assert first.killed is True, (
        "an arm one operator notices is watched. Read as `all`, an arm is "
        "reported unwatched while a case demonstrably depends on it"
    )
    assert first.detail == "invert killed · remove survived"


def test_the_report_separates_the_operators_and_names_the_ticket_row(two_arms):
    """§14 — a reader comparing this run with #262 needs the `remove` row, and
    a total that mixed the operators would invite exactly the wrong
    comparison.

    Measured 2026-09-09 on `hooks/review-history-guard.py`: `invert` kills
    every one of the 29 arms it can be asked of and `remove` kills 20 of 32,
    so a single survivor count is not the ticket's nine and must not be read
    as a refutation of it."""
    module_path, tests = two_arms
    verdicts, refused = ARM.run_arms(str(module_path), tests)
    lines = []
    ARM._report(
        str(module_path),
        verdicts,
        refused,
        ARM.counts([v.arm for v in verdicts]),
        lines.append,
    )
    text = "\n".join(lines)
    # The per-operator ROWS, not merely the words. Both operator names also
    # appear in the paragraph explaining the difference, so asserting their
    # presence alone stayed green with the rows merged into one total.
    rows = [
        ln.strip()
        for ln in lines
        if ln.strip().startswith(("invert", "remove")) and "asked" in ln
    ]
    assert len(rows) == 2, f"{lines} — one row per operator, with its own counts"
    for row in rows:
        assert "killed" in row and "survived" in row, (
            f"{row!r} — a row that gives only how many were asked does not "
            f"say how many survived, which is the number being compared"
        )
    assert "#262's own" in text and "`remove` count" in text, (
        "and must say which row the ticket's unwatched-arm table compares "
        "with, or a reader compares it with the total"
    )


def test_the_skill_calls_its_survivor_counts_a_measurement_and_not_a_property():
    """Round 1's finding 5, and it is this work item's own argument turned on
    it.

    #262 exists because a count typed into a document rots: its own table says
    33 arms where the module has 31, because the file changed twice after the
    count was taken. The section that introduces this checker then printed
    `1 of 32` and `12 of 32` in a column headed like a property of the module,
    with no date and nothing reading it.

    What is pinned here is the CLAIM, not the numbers. A case asserting
    `12 of 32` is the rotting list one file further on; a case asserting that
    the column is a measurement is what stops the next edit putting a bare
    number back. Asserted as a whole clause and lowered, for the reasons
    #310's case carries.

    Red how: deleting the sentence, or rewriting it to say the numbers are a
    property of the module. Executed."""
    with open(
        os.path.join(ROOT, "skills", "verify", "SKILL.md"), encoding="utf-8"
    ) as f:
        text = " ".join(f.read().split()).lower()
    assert (
        "that third column is a measurement and not a property of the module" in text
    ), (
        "the section prints two survivor counts, and a reader who takes them "
        "for a property of the module is reading a number that moves when "
        "either the module or its cases change — which is the rot #262 is "
        "about, arriving in the document that introduces the checker"
    )
    assert (
        "re-take it with the command above rather than reading it as current" in text
    ), (
        "and it has to say what to do instead, or the disclosure is a caveat "
        "with no action in it"
    )


def test_a_sole_type_handler_is_measured_by_one_operator_and_not_by_both(tmp_path):
    """Round 1's finding 6, and it is this module's own subject turned on it.

    For a handler with one type left, `remove` splices `NEVER_RAISED` over the
    type and `invert` splices it over the same span: byte-identical before
    this refusal, so ONE measurement was reported as two independent answers
    to the two questions `OPERATORS` says are different. `main:189` in
    `hooks/review-history-guard.py` — the arm the report headlines as watched
    by nothing — is exactly this shape, and it printed `invert survived ·
    remove survived`.

    `remove` is the operator that keeps it, because #262's table is a removal
    count. Nothing is lost by refusing `invert`: the identical text is still
    spliced and still measured, one subprocess run fewer.

    **Both spellings of *one type left*, because the class is not just the
    sole type.** `except (OSError,):` is a one-member tuple whose remainder is
    also `NEVER_RAISED`; the two operators reach different spans there, so the
    texts differ while the edit does not, and it is refused on the same
    grounds.

    Red how: dropping the refusal makes the two mutations compare equal here
    and the report print two rows for one measurement. Executed."""
    sole = "def f():\n    try:\n        pass\n    except OSError:\n        pass\n"
    (only,) = ARM.arms(sole)
    with pytest.raises(ARM.NoMutationDefined, match="one type left"):
        ARM.mutate(sole, only, "invert")
    # And the measurement itself is not lost -- `remove` splices the same text.
    assert "_specseal_never_raised" in ARM.mutate(sole, only, "remove")

    one_member = (
        "def f():\n    try:\n        pass\n    except (OSError,):\n        pass\n"
    )
    (wrapped,) = ARM.arms(one_member)
    assert wrapped.group_without == ARM.NEVER_RAISED, (
        "a one-member tuple's remainder is what nothing raises, which is the "
        "same edit spelled over a different span"
    )
    with pytest.raises(ARM.NoMutationDefined, match="one type left"):
        ARM.mutate(one_member, wrapped, "invert")

    # A handler with more than one type keeps both operators: the refusal is
    # for the arms where the two edits coincide, not for handlers.
    pair = (
        "def f():\n    try:\n        pass\n    except (OSError, ValueError):\n"
        "        pass\n"
    )
    first, _second = ARM.arms(pair)
    assert "_specseal_never_raised" in ARM.mutate(pair, first, "invert")
    assert "except (ValueError):" in ARM.mutate(pair, first, "remove")

    # And the run names the un-asked pair rather than skipping it.
    module_path = tmp_path / "sole.py"
    module_path.write_text(sole, encoding="utf-8")
    verdicts, refused = ARM.run_arms(str(module_path), [sys.executable, "-c", "pass"])
    assert refused == [], "the arm is measured by `remove`, so it is not refused"
    (verdict,) = verdicts
    assert sorted(verdict.by_operator) == ["remove"]
    assert "one type left" in verdict.not_applicable["invert"], (
        "the pair `invert` could not be asked of has to reach the report, or "
        "its denominator shrinks silently -- the skip this module refuses"
    )


def test_an_unknown_operator_is_refused_rather_than_ignored():
    """A silently ignored operator reports every arm as watched by whatever
    ran, with nothing saying an operator was asked for and skipped."""
    source = "def f(a):\n    if a:\n        return 1\n    return 0\n"
    (arm,) = ARM.arms(source)
    with pytest.raises(ARM.NoMutationDefined, match="is not one of"):
        ARM.mutate(source, arm, "delete-the-file")


def test_removing_one_type_from_a_three_member_handler_still_parses():
    """`except OSError, ValueError:` has been a SyntaxError since Python 3.

    An `ast.Tuple` in an except clause spans its own parentheses, so the
    remainder replaces them too and has to bring its own back. Unwrapped,
    `mutate` raises `SyntaxError`, `run_arms` files the arm as REFUSED, and
    all three arms of the handler go unmeasured while the report still shows
    a count.

    `reader` in `hooks/review-history-guard.py` is exactly this shape —
    `except (OSError, ImportError, SyntaxError)` — so this is the real
    module's arms, not a constructed edge."""
    source = (
        "def f():\n    try:\n        pass\n"
        "    except (OSError, ImportError, SyntaxError):\n        pass\n"
    )
    found = ARM.arms(source)
    assert len(found) == 3
    for arm in found:
        mutated = ARM.mutate(source, arm, "remove")
        ast.parse(mutated)
        assert arm.source not in mutated, f"{arm.source} was not removed"
    assert "except (ImportError, SyntaxError):" in ARM.mutate(
        source, found[0], "remove"
    )


def test_an_operator_that_could_not_be_asked_of_an_arm_is_named(tmp_path):
    """The last place a skip could hide, and the real module found it.

    An arm no operator can mutate is `refused` and reported. An arm where
    ONE operator has no mutation is not refused — the other operator
    measured it — so until this was named, the per-operator count simply
    excluded it. The first run over `hooks/review-history-guard.py` printed
    `remove 31 asked` against 32 arms and said nothing about which arm was
    missing or why.

    Driven with an arm `remove` cannot be asked of: a match-case guard next
    to a pattern, where the pattern has no mutation at all. The `remove`
    row's denominator has to be visible, because it is the row #262's table
    is compared with."""
    module_path = tmp_path / "m.py"
    module_path.write_text(
        "def f(x):\n"
        "    match x:\n"
        "        case 1:\n"
        '            return "one"\n'
        '    return "other"\n',
        encoding="utf-8",
    )
    verdicts, refused = ARM.run_arms(str(module_path), [sys.executable, "-c", "pass"])
    # The pattern has no mutation for either operator, so the arm is refused.
    assert verdicts == []
    assert len(refused) == 1
    _arm, why = refused[0]
    assert "invert" in why and "remove" in why, (
        "a refused arm must say which operators had no mutation for it, or "
        "the reason it went unmeasured is lost"
    )
    assert "match PATTERN is not an" in why


def test_a_partly_skipped_operator_is_reported_without_refusing_the_arm():
    """The half above that is not a refusal.

    Constructed rather than found, because the module that found it has been
    fixed: `gh_segments`'s wrapped `while` test was the arm `remove` could
    not be asked of, and the remainder is parenthesised now. The report line
    is what stays."""
    span = ARM.Span(10, 4, 10, 20)
    arm = ARM.Arm(
        scope="f",
        shape="While",
        source="i < len(toks)",
        note="1/2",
        span=span,
        group=ARM.Span(10, 4, 12, 8),
        group_without="(rest)",
    )
    lines = []
    ARM._report(
        "m.py",
        [ARM.Verdict(arm, {"invert": True}, {"remove": "SyntaxError: bad"})],
        [],
        {"f": 1},
        lines.append,
    )
    text = "\n".join(lines)
    assert "operator/arm pairs with no verdict" in text, (
        "an operator with no verdict for an arm must be named; silently "
        "excluding it from that operator's denominator is the skip this "
        "whole module refuses"
    )
    assert "not asked" not in text, (
        "and the section cannot be headed *not asked*: a pair whose command "
        "timed out or could not be spawned was asked and answered nothing, "
        "and it lands in this same list (round 2's finding 15)"
    )
    assert "remove" in text and "f:10" in text and "SyntaxError" in text
