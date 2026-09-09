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
"""

import ast
import hashlib
import importlib.util
import os
import shlex
import sys
import textwrap
import warnings

import pytest

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

    Red how: deleting `"IfExp"` from `ARM_SHAPES` leaves it in neither table
    and this case names it. Executed.
    """
    missing = grammar() - ARM.CLASSIFIED
    assert not missing, (
        f"{sorted(missing)} — AST node types this walk classifies as neither "
        f"an arm shape nor a named non-arm. Every arm inside one of them is "
        f"uncounted while the total still reads like a total, which is #262's "
        f"own defect one level up. Add each to `ARM_SHAPES` with how its arms "
        f"are read, or to `NOT_ARMS` under the reason it carries none."
    )


def test_the_classification_names_nothing_the_grammar_does_not_have():
    """The other direction, and it is not symmetry for its own sake.

    A name in the tables that `ast` no longer has is a classification nobody
    can reach, and it hides the case above: a removed node type leaves the
    count of classified names unchanged while a name the grammar gained goes
    missing. Subtracting in one direction only would pass on a table that has
    drifted in both."""
    extra = ARM.CLASSIFIED - grammar()
    assert not extra, (
        f"{sorted(extra)} — classified here and absent from this "
        f"interpreter's `ast`. A stale name makes the tables look complete "
        f"while a real one is missing."
    )


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

    The report has to say how many arms it enumerated and did not mutate, and
    name them — otherwise the denominator quietly shrinks and the survivor
    count still reads like a survivor count."""
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
    assert "1 arms refused" in text
    assert "enumerated and not mutated" in text


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
# existed at the moment it ran.
SEES_CACHE = """\
import glob
import os
import sys

module, log = sys.argv[1], sys.argv[2]
cache = os.path.join(os.path.dirname(module), "__pycache__")
found = glob.glob(os.path.join(cache, "under_test.*.pyc"))
with open(log, "a", encoding="utf-8") as f:
    f.write("cache\\n" if found else "clean\\n")
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

    verdicts, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, str(probe), str(module_path), str(log)],
    )
    assert refused == []
    seen = log.read_text(encoding="utf-8").split()
    # Two arms, and every operator that has a mutation for one of them.
    expected = sum(len(v.by_operator) for v in verdicts)
    assert len(verdicts) == 2
    assert len(seen) == expected == 4, "every mutation must have been observed"
    assert set(seen) == {"clean"}, (
        f"{seen} — an arm ran with cached bytecode for the module present, so "
        f"its verdict can be decided by another arm's mutation rather than by "
        f"the source on disk"
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
    arms got as far as running their command."""
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
    assert len(ran) == 1, (
        f"{len(ran)} arms ran their command after a restore that did not "
        f"land. Every verdict past the first is measured against a mutated "
        f"module and reported as though it were not"
    )


def test_the_run_leaves_no_bytecode_cache_behind(two_arms):
    """No litter, so a later ordinary import of the module under test does
    not load bytecode the checker's own mutation produced.

    **This property has two mechanisms behind it and either one alone
    satisfies it** — the per-arm `clear_bytecode_cache` and the subprocess's
    `PYTHONDONTWRITEBYTECODE`. So the env var is an arm no case kills: it is
    redundant insurance for a subprocess whose `PYTHONPYCACHEPREFIX` differs
    from this process's, where the clear would look in the wrong directory.
    Named here rather than pinned, because pinning the second mechanism
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
PRELUDES = [
    (f"in a string literal: {c!r}", f'MESSAGE = "x{c}y"\n') for c in NOT_LINE_ENDS
]
PRELUDES.append(("a form feed on its own line", "\x0c\n"))


@pytest.mark.parametrize("label,prelude", PRELUDES, ids=[p[0] for p in PRELUDES])
def test_a_separator_the_tokenizer_ignores_does_not_move_a_spliced_arm(label, prelude):
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

    Red how: `_lines` replaced by `source.splitlines(keepends=True)` raises
    `IndentationError` on every one of these nine. Executed."""
    source = (
        prelude + "\n\ndef f(a, b):\n    if a and b:\n        return 1\n    return 0\n"
    )
    first, second = ARM.arms(source)
    assert first.source == "a", f"{label}: the span itself is right either way"
    assert "if not (a) and b:" in ARM.mutate(source, first)
    assert "if a and not (b):" in ARM.mutate(source, second)
    for arm in (first, second):
        ast.parse(ARM.mutate(source, arm))
        ast.parse(ARM.mutate(source, arm, "remove"))


# --- the command that decides the verdict can hang or fail to start -------


def test_a_command_that_never_returns_is_recorded_as_unmeasured(two_arms):
    """Round 1's finding 1, the bounded half.

    While an arm's command runs, the module on disk holds the mutation and
    `capture_output=True` means nothing is printed — so an unbounded hang is
    indistinguishable from a slow suite, and the longer the process lives
    mutated the more likely it is ended by something no `finally` sees. The
    bound turns the hang into a NAMED unmeasured pair rather than a wait:
    `killed` would read as *a case noticed* and `survived` as *none did*, and
    neither was measured.

    Red how: `timeout=timeout` removed from the `subprocess.run` call hangs
    this case for 30 seconds per pair instead of failing. Executed — and the
    run is bounded here by the 0.3s the case passes, not by the default.
    """
    module_path, _ = two_arms
    verdicts, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, "-c", "import time; time.sleep(30)"],
        timeout=0.3,
    )
    # Every pair timed out, so no arm has a verdict from any operator and
    # both are refused rather than reported as survivors.
    assert verdicts == []
    assert len(refused) == 2
    for _arm, why in refused:
        assert "did not return within 0.3s" in why, (
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

    Driven by making the third of the four calls raise — arm one is fully
    measured by then, arm two by nothing.

    Red how: deleting the `except OSError` clause raises `OSError` out of
    `run_arms` here and the first arm's two verdicts are lost. Executed."""
    module_path, tests = two_arms
    real_run = ARM.subprocess.run
    calls = []

    def fails_from_the_third_call(cmd, **kwargs):
        calls.append(cmd)
        if len(calls) >= 3:
            raise OSError("Errno 8: Exec format error")
        return real_run(cmd, **kwargs)

    ARM.subprocess.run = fails_from_the_third_call
    try:
        verdicts, refused = ARM.run_arms(str(module_path), tests)
    finally:
        ARM.subprocess.run = real_run

    assert len(calls) == 4, "every pair still had its command attempted"
    assert [(v.arm.source, sorted(v.by_operator)) for v in verdicts] == [
        ('host == "example.com"', ["invert", "remove"])
    ], "the verdicts taken before the failure are real and must survive it"
    assert len(refused) == 1
    _arm, why = refused[0]
    assert "OSError" in why and "Exec format error" in why, (
        f"{why!r} — an arm nothing could be spawned for is unmeasured, and "
        f"the reason has to reach the report"
    )


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
    first, second = verdicts
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

    Measured on `hooks/review-history-guard.py`: `invert` kills 31 of 32 arms
    and `remove` far fewer, so a single survivor count is not the ticket's
    nine and must not be read as a refutation of it."""
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
    arm, why = refused[0]
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
    assert "not asked" in text, (
        "an operator with no mutation for an arm must be named; silently "
        "excluding it from that operator's denominator is the skip this "
        "whole module refuses"
    )
    assert "remove" in text and "f:10" in text and "SyntaxError" in text
