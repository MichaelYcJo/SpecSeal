"""A unit that gains a returnable value has changed its contract.

#194. `docs/review-chain-spec.md` §*The fix surface* says `Contract changes`
exists for *a fix that changed a unit's contract while not every place that
contract reaches was revisited*, and names it the largest regression class
#57 measured — four findings of ten. The derivation compared **parameters and
return arities**, so a unit returning the same shape with a meaning it could
not return before changed neither and the row read `none`.

Measured, on work item `1788700685`, round 3: `token_thirds` began returning
**0 for a mean it cannot compute** — a value it could not return before. Round
4 then walked from that new return value to its consumers and found the one
interpreting call site had not been revisited: the context line takes the
charged 0 as a baseline and reports growth on a run whose input collapsed. The
row that exists for exactly that shape had read `none`.

`templates/sdd-round.md` had already promised the wider comparison — its
`Contract changes` field reads *signature, return arity, return type, or set
of returnable values*. This is the fourth of those four arriving.

**The hole this does NOT close is a deliverable, not a gap**, and
`test_the_document_states_the_hole_it_does_not_catch` is what holds the
document to saying so. See the case for the measured instance.

Two cross-checks, because the class here is *units whose returnable literals
changed* and enumerating it by reading is what this repository has eight
measured misses of:

  test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree
      an independent implementation of the literal set, run over every
      top-level def in every tracked `.py` file, compared with the shipped
      one unit by unit

  test_every_constructed_shape_lands_where_the_independent_reading_puts_it
      the same independent reading over 21 before/after pairs, compared with
      what `measure` actually reports as changed

Every case was seen red against the two-element contract, where the literal
set was not compared at all.
"""

import ast
import os
import subprocess

import pytest
from test_the_record_is_generated import ROOT, generator_module, reader_module

# --- an independent reading of the same thing -------------------------------


def literals_of(node):
    """The constant values one def's own `return` statements can produce.

    Written from the rule rather than from the shipped code: every `return`
    that is not inside a nested def, class or lambda, taking the value itself
    when it is a constant and the constant elements when it is a tuple.
    Keyed by type as well as value, because `0` and `False` are one key to a
    plain set and are two different things to return.
    """
    stack, found = list(node.body), set()
    while stack:
        n = stack.pop()
        if isinstance(
            n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        if isinstance(n, ast.Return) and n.value is not None:
            parts = list(n.value.elts) if isinstance(n.value, ast.Tuple) else [n.value]
            for part in parts:
                if isinstance(part, ast.Constant):
                    found.add((type(part.value).__name__, repr(part.value)))
        stack.extend(ast.iter_child_nodes(n))
    return frozenset(found)


def independent(source):
    """{name: literal set} for every top-level def in `source`."""
    return {
        n.name: literals_of(n)
        for n in ast.parse(source).body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


# --- the shipped derivation, over the whole tree ----------------------------


def tracked_python():
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "*.py"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return [p for p in out if os.path.isfile(os.path.join(ROOT, p))]


def test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree():
    """Two readings of the same rule, over every def this repository has.

    Enumerating the class by reading is what eight measured misses in this
    repository came from, so the check is a second implementation rather than
    a list of examples. A disagreement here is one of the two being wrong,
    and the case names the unit.
    """
    generator = generator_module()
    paths = tracked_python()
    assert len(paths) > 50, f"{len(paths)} files; the case is vacuous"
    compared = carrying = 0
    for rel in paths:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            source = f.read()
        try:
            units = generator.top_units(ast.parse(source))
        except SyntaxError:
            continue
        mine = independent(source)
        for name, want in mine.items():
            contract = units[name][0]
            assert contract is not None and len(contract) == 3, (
                f"{rel}#{name}: the contract is {contract!r}, not a triple"
            )
            assert contract[2] == want, f"{rel}#{name}: {contract[2]!r} != {want!r}"
            compared += 1
            carrying += bool(want)
    assert compared > 500, compared
    assert carrying > 50, (
        f"only {carrying} units return a literal at all; a derivation that "
        "always answered the empty set would pass this case"
    )


# --- what the fix range reports ---------------------------------------------

BEFORE_AFTER = [
    # (name, before body, after body, does the literal set change)
    ("a bare sentinel appears", "    return compute(x)", "    return 0", True),
    ("a sentinel disappears", "    return 0", "    return compute(x)", True),
    ("one literal becomes another", "    return 0", "    return 1", True),
    (
        "a literal is added beside one",
        "    return 0",
        "    if x:\n        return 0\n    return 1",
        True,
    ),
    ("a string sentinel appears", "    return x", '    return "gone"', True),
    ("None becomes explicit", "    return x", "    return None", True),
    ("True and 1 are not the same value", "    return 1", "    return True", True),
    ("False and 0 are not the same value", "    return 0", "    return False", True),
    ("0 and 0.0 are not the same value", "    return 0", "    return 0.0", True),
    ("a literal joins a returned tuple", "    return x, y", "    return x, 0", True),
    ("a tuple's literal changes", "    return x, 0", "    return x, 1", True),
    # The blind spots and the unchanged shapes, which must NOT be reported.
    (
        "the same two literals, remapped",
        "    if x:\n        return 0\n    return 1",
        "    if not x:\n        return 0\n    return 1",
        False,
    ),
    ("nothing changes", "    return 0", "    return 0", False),
    (
        "only the order of two returns",
        "    if x:\n        return 0\n    return 1",
        "    if not x:\n        return 1\n    return 0",
        False,
    ),
    (
        "a computed value replaces another",
        "    return compute(x)",
        "    return other(x)",
        False,
    ),
    ("a comment is added", "    return 0", "    # a note\n    return 0", False),
    (
        "a nested def gains a literal",
        "    def inner():\n        return x\n    return compute(x)",
        "    def inner():\n        return 7\n    return compute(x)",
        False,
    ),
    (
        "a lambda gains a literal",
        "    f = lambda: x\n    return compute(x)",
        "    f = lambda: 7\n    return compute(x)",
        False,
    ),
    (
        "a nested class gains a literal",
        "    class C:\n        def m(self):\n            return x\n    return compute(x)",
        "    class C:\n        def m(self):\n            return 7\n    return compute(x)",
        False,
    ),
    (
        "a bare return is arity, not a literal",
        "    return 0",
        "    return 0\n    return",
        False,
    ),
    (
        "a literal in a call argument is not returned",
        "    return compute(x)",
        "    return compute(0)",
        False,
    ),
]


def module_for(bodies):
    return "".join(f"def unit_{i}(x, y=None):\n{b}\n\n\n" for i, b in enumerate(bodies))


def test_every_constructed_shape_lands_where_the_independent_reading_puts_it():
    """21 shapes, and the expectation column is checked against the
    independent reading rather than trusted — a table of hand-written
    booleans is exactly the enumeration-by-reading this cross-check exists to
    replace, so both have to agree before either judges the shipped code."""
    generator = generator_module()
    before = module_for([b for _n, b, _a, _c in BEFORE_AFTER])
    after = module_for([a for _n, _b, a, _c in BEFORE_AFTER])
    mine_before, mine_after = independent(before), independent(after)
    old = generator.top_units(ast.parse(before))
    new = generator.top_units(ast.parse(after))
    for i, (name, _b, _a, changes) in enumerate(BEFORE_AFTER):
        unit = f"unit_{i}"
        independent_says = mine_before[unit] != mine_after[unit]
        assert independent_says == changes, (
            f"{name}: the table disagrees with the reading"
        )
        shipped_says = old[unit][0][2] != new[unit][0][2]
        assert shipped_says == changes, (
            f"{name}: the shipped derivation says {shipped_says}"
        )


def test_the_signature_and_arity_halves_are_untouched():
    """The literal set is a third element, not a replacement. A unit whose
    signature changed and whose literals did not is still a contract change,
    which is every case the row already caught."""
    generator = generator_module()
    old = generator.top_units(ast.parse("def u(a):\n    return compute(a)\n"))
    new = generator.top_units(ast.parse("def u(a, b=None):\n    return compute(a)\n"))
    assert old["u"][0] != new["u"][0]
    assert old["u"][0][2] == new["u"][0][2] == frozenset()


def test_a_class_carries_no_literal_set():
    """A class's contract is its `__init__` parameters. Its methods' returns
    are the methods', and `top_units` reads top-level units only."""
    generator = generator_module()
    units = generator.top_units(
        ast.parse("class C:\n    def __init__(self, a):\n        pass\n")
    )
    assert units["C"][0] == (
        generator.signature(ast.parse("def _(self, a):\n    pass\n").body[0].args),
        None,
        None,
    )


def test_a_constant_still_has_no_contract():
    """A changed value is not a changed contract, and this rule did not move:
    a module-level assignment carries `None` where a def carries a triple."""
    generator = generator_module()
    assert generator.top_units(ast.parse("NAME = 1\n"))["NAME"][0] is None


# --- the hole, which is the other half of the deliverable -------------------


def test_the_document_states_the_hole_it_does_not_catch():
    """The check ships and the paragraph states its limit. Documentation
    alone was refused as an answer; a stated hole is not the same thing as an
    undocumented one, and the paragraph is what keeps the row from reading as
    a guarantee it cannot give.
    """
    with open(f"{ROOT}/docs/review-chain-spec.md", encoding="utf-8") as f:
        text = " ".join(f.read().split())
    # The shape it does not catch, named as a shape rather than as an excuse.
    assert "input" in text, "the paragraph does not name the shape"
    assert "mapping" in text, "the paragraph does not name the shape"
    assert "is_a_record_of_a_moment" in text, "the measured instance is not named"
    # And what stays true of it: everything the derivation compares is unchanged.
    for word in ("signature", "arity", "returnable"):
        assert word in text, word
    assert "the reviewer" in text, "the paragraph does not say whose the residual is"


def test_the_hole_is_a_hole_and_not_a_claim():
    """The measured instance, rebuilt: a unit that changes which inputs reach
    which of the two values it already returned. Signature, arity and the
    returnable set are all unchanged, so the derivation is blind to it by
    construction — which is what the paragraph has to say, and what a later
    session must not quietly 'fix' by widening the check."""
    generator = generator_module()
    before = (
        "def is_a_record_of_a_moment(rel):\n"
        "    for entry in RECORDS:\n"
        "        if rel.startswith(entry):\n"
        "            return True\n"
        "    return False\n"
    )
    after = (
        "def is_a_record_of_a_moment(rel):\n"
        "    for entry in RECORDS:\n"
        "        if rel.startswith(entry) and DATED.match(os.path.basename(rel)):\n"
        "            return True\n"
        "    return False\n"
    )
    old = generator.top_units(ast.parse(before))["is_a_record_of_a_moment"][0]
    new = generator.top_units(ast.parse(after))["is_a_record_of_a_moment"][0]
    assert old == new, "the check caught it, so the documented hole is now false"
    assert old[2] == frozenset({("bool", "True"), ("bool", "False")}), old[2]


# --- end to end, through `close` --------------------------------------------

MOD = "def sentinel(a):\n    return compute(a)\n\n\ndef caller():\n    return sentinel(1)\n"
MOD_SENTINEL = (
    "def sentinel(a):\n"
    "    if a is None:\n"
    "        return 0\n"
    "    return compute(a)\n"
    "\n"
    "\n"
    "def caller():\n"
    "    return sentinel(1)\n"
)
OPEN = "| 🔴 1 | sentinel gains a 0 | `mod.py#sentinel` | open | executed |\n"


@pytest.fixture
def repo(tmp_path):
    from test_the_record_is_generated import commit, git, write

    d = tmp_path / "repo"
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "mod.py", MOD)
    write(d, "README.md", "# a fixture\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")
    return d


def test_the_row_names_the_unit_and_its_reach(repo):
    """The whole point, through the real subcommand: the unit enters the row
    with the call site a reader has to go and check, which is the half the
    diff does not show."""
    from test_the_fixes_close_the_record import close, fix_table
    from test_the_record_is_generated import commit, declared, generate, report, write

    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN))
    assert code == 0, out
    a = commit(repo, "round 1")
    write(repo, "mod.py", MOD_SENTINEL)
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    reader = reader_module()
    row = next(
        reader.visible(reader.split_row(line)[1])
        for line in reader.readable(record)
        for cells in [reader.split_row(line)]
        if cells and reader.visible(cells[0]).strip() == "Contract changes"
    )
    assert row.strip() == "sentinel → caller", (row, out)
