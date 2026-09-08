"""Every site in `session_cost.py` that converts a number to an int is
discharged — by a guard, or by an operand that cannot be a derived number.

#192. `count` answers whether each value entering from a transcript is
finite. `load` then adds a turn's `input_tokens` to its
`cache_read_input_tokens`, and `token_thirds` sums those and divides. **Two
values that each passed can make one that would not**, and the report ended
with exit 1 and stdout empty on both the report and `--json`. Round 3 of #175
closed that at one site. What is left is the class, and #192's own reading of
why a second site walk is not it: round 3's defect arrived through a call the
existing arithmetic walk had held in its list from the start, so a walk over
operations answers *which operations exist* and never *what two entered
values make*.

**The class is enumerated by construction and every question about it is
decided by execution.** Nothing here is answered by a list of names, because
a list is what this release exists to replace.

  is this site a conversion to an int
      Two probes, and both halves are the owner's own wording — *converting a
      derived number TO an int*. Python reaches an `int` through exactly six
      operand methods (`__int__`, `__index__`, `__trunc__`, `__round__`,
      `__floor__`, `__ceil__`), so `Operand` below answers those six and
      nothing else and the walk hands one to the site's own callable: that
      settles whether the operand is consumed as an integer. Then the same
      callable is asked for its answer to a benign number, and the site is a
      member only when that answer is an exact `int`. `round`, `int`,
      `math.floor`, an aliased import, a `from`-import and a function written
      in this module ten minutes ago all classify the same way, and no name
      appears anywhere in this file.

  what does the conversion raise
      Probed, not assumed: the callable is handed each value `count` admits
      and would not have refused — an infinity, a `NaN`, and an integer with
      no float of its own — and the exception types it raises are collected.
      `round` raises `OverflowError` on an infinity and `ValueError` on a
      `NaN`; `math.floor` raises the same two; a conversion that raises
      nothing needs no guard and says so. This is why there is no hardcoded
      pair of exception classes anywhere below.

  is this member discharged
      Its operand cannot be a derived number — an integer literal, or integer
      arithmetic over integer literals, where *keeps an int* is itself
      decided by evaluating the operator — or the conversion cannot raise at
      all, or a guard dominates it: a finiteness test on the same operand in
      an enclosing conditional, or a `try` whose handlers cover every
      exception the probe above actually saw. *Finiteness test* is decided by
      probing a resolved callable rather than by naming one, and *covers* by
      `issubclass`, so a tupled or aliased exception classifies correctly.

**The failure direction is toward refusing, and one shape is a measured false
refusal rather than an accident.** A guard written as an early return instead
of an enclosing conditional is refused, because dominance here is the
enclosing construct and an early return is not one; it sits in `GUARD_SHAPES`
with the verdict it actually gets. A wrong refusal is a red case with a
coordinate in it and a message saying what to write; a wrong pass is the
report ending with stdout empty, which is what #175 spent four rounds on.

**Three shapes this property does not reach, stated rather than left to be
found.** The first two are `questions.md` rows for the repository owner, and
`token_thirds`' own docstring carries both so a next editor of that file
meets them:

  a subscript bound
      a slice bound and a list index convert through `__index__`, so a
      subscript is a conversion by this same protocol. Whether one is DERIVED
      cannot be decided without provenance: `inputs[third : 2 * third]` is
      safe because `third` is `len(inputs) // 3`, and `by_family[key][0]`
      indexes with a local name this walk cannot see the value of. Excluded,
      with both directions of the mistake measured in `questions.md` Q1.

  a true division on two derived integers
      `sum(part) / len(part)` raises `OverflowError` on two integers that
      each have a float where their sum does not — the second of round 3's
      two routes — and it converts nothing, so it is not a member here. The
      wider predicate that would catch it (*a site that RAISES on a value
      `count` admits*) also flags `share`'s `part / whole * 100`, which is
      unguarded today and whose operands are durations. `questions.md` Q2.

  a callable that converts an operand and answers with something else
      `math.isfinite` is the measured instance, and the walk finds it: it
      consumes its operand through `__index__`, which is why
      `math.isfinite(HUGE_INT)` raises `OverflowError` — round 2 of #175's
      🔴, closed inside `count` by the `try` that is still there. It is not a
      member because it yields a `bool`, and that exclusion is deliberate:
      the alternative refuses the second call, in `token_thirds`, where
      `mean` is a float by construction and the call cannot raise, and paying
      for that with dead defensive code is the trade round 3 already refused
      once. `test_a_predicate_that_converts_but_answers_a_bool_is_not_a_member`
      is what keeps the exclusion visible instead of incidental.

**What the probe costs, because deciding membership by execution means
calling things.** Every callable probed is one this module's own source
calls, and the operand it is handed answers no protocol but the six — no
path, no string value, no arithmetic, no comparison — so a callable that is
not a numeric consumer raises `TypeError` on the spot and nothing reaches a
filesystem. Output is captured and every exception is swallowed, `SystemExit`
included. A future edit could call something whose mere invocation matters;
the bound on that is the operand, which gives such a call nothing to act on.

**And what an unresolved callee can hide, which is less than it looks.** A
method on a runtime receiver (`pattern.search`, `handle.read`) and a call to
a function defined inside another function cannot be resolved to an object,
so they are not probed. They hide a conversion only when the conversion is
written in code this walk does not read: the walk covers every call in the
module's own tree, nested definitions included, so a converter written HERE
is caught at its own `int(...)` whoever calls it.

The scope is one module because that is the module whose operands come out of
a transcript. Widening to the tree makes every `round(` in every script a
member and stops the diff being about #192.
"""

import ast
import builtins
import contextlib
import importlib.util
import io
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE = os.path.join(ROOT, "skills", "verify", "scripts", "session_cost.py")

# A number every numeric consumer accepts, filling the argument slots that
# are not carrying the value under probe.
BENIGN = 3.0

# What `count` admits and would not have refused, so what a sum of admitted
# values can be: a non-finite float, and an integer with no float of its own.
HUGE_INT = int("9" * 401)
DERIVED = (float("inf"), float("-inf"), float("nan"), HUGE_INT)
NON_FINITE = (float("inf"), float("-inf"), float("nan"))

# The whole of Python's route from a number to an `int`. A site consumes its
# operand as an integer when it invokes one of these; nothing else does.
INT_PROTOCOL = (
    "__int__",
    "__index__",
    "__trunc__",
    "__round__",
    "__floor__",
    "__ceil__",
)

# The node kinds the walk classifies. Operators are here so that *no operator
# in this module converts to an int* is derived rather than asserted;
# `Subscript` is deliberately absent and the docstring says why.
SITE_KINDS = (ast.Call, ast.BinOp, ast.UnaryOp, ast.AugAssign, ast.Compare)


class Converted(BaseException):
    """Raised by the recording operand the moment a conversion is asked for.

    It stops the probed callable at the conversion rather than letting it run
    on with a half-converted operand, which is the whole of what it buys.

    **What it does NOT buy, stated because the obvious claim is false.**
    `_recorder` records before it raises, so detection never depends on who
    catches this — a callable that swallows `Exception` around its own `int()`
    still classifies as a converter, which
    `GUARD_SHAPES`' *a converter that already guards itself* is built on.
    Deriving from `BaseException` is therefore a defensive choice no case can
    tell from `Exception`: it survived the mutation battery for #192, and
    that is recorded rather than papered over with a case that would only
    pin the class statement to itself."""


class Operand:
    """An operand that answers the six integer conversions and nothing else.

    Handed to a callable enumerated from the module's source. Anything that
    is not a numeric consumer fails on it immediately — there is no path, no
    string value, no arithmetic and no ordering to act on."""

    def __init__(self):
        self.fired = set()

    def __repr__(self):
        return "<recording operand>"


def _recorder(name):
    def method(self, *_args, **_kwargs):
        self.fired.add(name)
        raise Converted(name)

    method.__name__ = name
    return method


for _name in INT_PROTOCOL:
    setattr(Operand, _name, _recorder(_name))


# --- the module under the walk ----------------------------------------------


def source():
    with open(MODULE, encoding="utf-8") as handle:
        return handle.read()


def namespace_of(path=MODULE):
    """The module's own bindings, so a call resolves to the object it names.

    Resolving the binding rather than matching the written name is what makes
    an alias and a `from`-import classify like the plain call they are."""
    spec = importlib.util.spec_from_file_location("session_cost_under_walk", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return vars(module)


def namespace_of_source(text, directory):
    """The bindings of a constructed module, loaded the way the real one is.

    Written to a file rather than exec'd into a dict because a shape
    classified through a different loader is a shape classified by a
    different code path."""
    path = os.path.join(str(directory), "under_walk.py")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return namespace_of(path)


# --- resolution -------------------------------------------------------------


def resolve(node, namespace):
    """`(object, path)` for what an expression names, or `(None, None)`.

    A bare name comes from the module's own bindings and then from builtins;
    an attribute from its resolved root; a literal is itself, which is what
    makes `" ".join(...)` resolvable. A receiver the module computes at
    runtime resolves to nothing, which is the stated residual."""
    if isinstance(node, ast.Constant):
        return node.value, repr(node.value)
    if isinstance(node, ast.Name):
        if node.id in namespace:
            return namespace[node.id], node.id
        if hasattr(builtins, node.id):
            return getattr(builtins, node.id), node.id
        return None, None
    if isinstance(node, ast.Attribute):
        root, path = resolve(node.value, namespace)
        if root is None:
            return None, None
        try:
            return getattr(root, node.attr), f"{path}.{node.attr}"
        except Exception:
            return None, None
    return None, None


def root_name(node):
    """The bare name an attribute chain hangs off, or None for an expression."""
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def names_bound_inside(tree):
    """Every name this module binds somewhere other than at module level.

    Used to show the resolver's misses are runtime receivers rather than
    lookup failures: an unresolved callee is a name the module binds inside a
    function, never one it never binds at all."""
    bound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            bound.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, ast.alias):
            bound.add((node.asname or node.name).split(".")[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
    return bound


# --- the probes -------------------------------------------------------------


def quiet(call):
    """Run `call` and answer `(value, exception type)`, printing nothing.

    Every exception is swallowed, `SystemExit` included: a probe reports by
    what it recorded, never by propagating."""
    with (
        contextlib.redirect_stdout(io.StringIO()),
        contextlib.redirect_stderr(io.StringIO()),
    ):
        try:
            return call(), None
        except BaseException as raised:
            return None, type(raised)


def slots_of(positional, keywords, value):
    """Each way one probe value can occupy an argument of this call.

    A derived number can arrive in any slot, so every slot is tried."""
    for index in range(positional):
        args = [BENIGN] * positional
        args[index] = value
        yield args, dict.fromkeys(keywords, BENIGN)
    for name in keywords:
        kwargs = dict.fromkeys(keywords, BENIGN)
        kwargs[name] = value
        yield [BENIGN] * positional, kwargs


def consumes_an_integer(fn, positional, keywords):
    """Whether calling `fn` invokes an integer conversion on one of its operands."""
    if not callable(fn):
        return False
    for args, kwargs in slots_of(positional, keywords, None):
        operand = Operand()
        args = [operand if a is None else a for a in args]
        kwargs = {k: (operand if v is None else v) for k, v in kwargs.items()}
        quiet(lambda: fn(*args, **kwargs))  # noqa: B023
        if operand.fired:
            return True
    return False


def yields_an_int(fn, positional, keywords):
    """Whether `fn` answers a benign number with an exact `int`.

    The second half of *converting a number TO an int*. It is what tells a
    conversion from a predicate that converts in order to answer something
    else — `math.isfinite` consumes its operand as an integer and yields a
    `bool`, and the module docstring holds why that exclusion is deliberate."""
    if not callable(fn):
        return False
    value, _raised = quiet(
        lambda: fn(*([BENIGN] * positional), **dict.fromkeys(keywords, BENIGN))
    )
    return type(value) is int


def raised_by(fn, positional, keywords):
    """The exception types this call raises on a value `count` admits.

    Probed rather than assumed, so no pair of exception classes is written
    down anywhere: `round` answers `OverflowError` for an infinity and
    `ValueError` for a `NaN`, and a conversion that answers nothing at all
    needs no guard."""
    kinds = set()
    for value in DERIVED:
        for args, kwargs in slots_of(positional, keywords, value):
            _value, kind = quiet(lambda: fn(*args, **kwargs))  # noqa: B023
            if kind is not None and kind is not TypeError:
                kinds.add(kind)
    return kinds


def operator_forms(node):
    """The source of each way this node's operator can be written out.

    Built by unparsing a synthetic node carrying the operator the module
    actually wrote, so there is no table of symbols to fall behind `ast`."""
    left = ast.Name(id="a", ctx=ast.Load())
    right = ast.Name(id="b", ctx=ast.Load())
    if isinstance(node, ast.BinOp):
        return [ast.unparse(ast.BinOp(left=left, op=node.op, right=right))]
    if isinstance(node, ast.UnaryOp):
        return [ast.unparse(ast.UnaryOp(op=node.op, operand=left))]
    if isinstance(node, ast.AugAssign):
        target = ast.Name(id="a", ctx=ast.Store())
        return [ast.unparse(ast.AugAssign(target=target, op=node.op, value=right))]
    if isinstance(node, ast.Compare):
        return [
            ast.unparse(ast.Compare(left=left, ops=[op], comparators=[right]))
            for op in node.ops
        ]
    return []


def operator_converts(node, benign=BENIGN):
    """Whether this node's operator reaches an int through one of its operands.

    Probed with numeric operands, because numbers are what a transcript
    yields. `benign` is what the other slot holds, and handing it a sequence
    shows the one route the numeric probe cannot see: `"ab" * n` converts `n`
    through `__index__`. Whether an operand is a sequence is provenance this
    walk does not have, so `2 * third` in `token_thirds` must not be read as
    one — which is why the default stays numeric and
    `test_the_operator_half_is_probed_and_says_what_it_cannot_see` holds the
    positive control."""
    for form in operator_forms(node):
        for env in ({"a": Operand(), "b": benign}, {"a": benign, "b": Operand()}):
            quiet(lambda: exec(form, {}, dict(env)))  # noqa: B023
            if any(isinstance(v, Operand) and v.fired for v in env.values()):
                return True
    return False


def operator_raised(node, benign=BENIGN):
    """The exception types this node's operator raises on derived operands."""
    kinds = set()
    for form in operator_forms(node):
        for value in DERIVED:
            for env in ({"a": value, "b": benign}, {"a": benign, "b": value}):
                _value, kind = quiet(lambda: exec(form, {}, dict(env)))  # noqa: B023
                if kind is not None and kind is not TypeError:
                    kinds.add(kind)
    return kinds


def is_finiteness_test(node, namespace):
    """Whether this call answers the finiteness question about its argument.

    Truthy for a benign float and falsy for every non-finite one. Decided by
    asking the resolved object, so a hand-written predicate and an aliased
    `math.isfinite` are the same thing to the walk."""
    if not isinstance(node, ast.Call):
        return False
    fn, _path = resolve(node.func, namespace)
    if not callable(fn):
        return False
    answer, _raised = quiet(lambda: fn(BENIGN))
    if not answer:
        return False
    return all(quiet(lambda: fn(value))[0] is False for value in NON_FINITE)  # noqa: B023


def evaluated(form):
    """What `form` evaluates to over literals, or None when it will not."""
    value, _raised = quiet(lambda: eval(form, {}, {}))
    return value


def keeps_an_int(node):
    """Whether this operator returns an `int` for integer operands.

    Evaluated rather than looked up: `//` keeps one and `/` does not, and
    saying which is which by hand is the list this file exists without."""
    six, three = ast.Constant(value=6), ast.Constant(value=3)
    if isinstance(node, ast.UnaryOp):
        form = ast.unparse(ast.UnaryOp(op=node.op, operand=six))
    else:
        form = ast.unparse(ast.BinOp(left=six, op=node.op, right=three))
    return type(evaluated(form)) is int


def integer_shaped(node):
    """Whether this expression is an integer nothing derived from a transcript.

    An integer literal, or integer arithmetic over integer literals. A name
    is never integer-shaped: what it holds is provenance, which is the
    subscript question in `questions.md` Q1.

    A `bool` counts, and it is the one place this file parts from `count`.
    `count` excludes `bool` because `True + 1` is a wrong number in a token
    column; the question here is only whether a transcript could have derived
    this operand, and a literal `True` no more derives from one than a
    literal `7` does. Excluding it would refuse `round(True)`, which cannot
    raise."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, int)
    if isinstance(node, ast.UnaryOp):
        return integer_shaped(node.operand) and keeps_an_int(node)
    if isinstance(node, ast.BinOp):
        return (
            integer_shaped(node.left)
            and integer_shaped(node.right)
            and keeps_an_int(node)
        )
    return False


# --- the walk ---------------------------------------------------------------


def parents_of(tree):
    return {
        child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)
    }


def unit_of(tree):
    """Which top-level unit each node sits in, for the coordinate in a message."""
    where = {}
    for top in tree.body:
        if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for node in ast.walk(top):
                where[node] = top.name
    return where


def operands_of(node):
    if isinstance(node, ast.Call):
        return list(node.args) + [kw.value for kw in node.keywords]
    if isinstance(node, ast.BinOp):
        return [node.left, node.right]
    if isinstance(node, ast.Compare):
        return [node.left, *node.comparators]
    if isinstance(node, ast.UnaryOp):
        return [node.operand]
    if isinstance(node, ast.AugAssign):
        return [node.target, node.value]
    return []


def catches(handler, exception, namespace):
    if handler.type is None:
        return True
    written = (
        handler.type.elts if isinstance(handler.type, ast.Tuple) else [handler.type]
    )
    for entry in written:
        caught, _path = resolve(entry, namespace)
        if isinstance(caught, type) and issubclass(exception, caught):
            return True
    return False


def try_covers(node, kinds, namespace):
    """Whether this `try` catches every exception the conversion was seen to raise."""
    return all(
        any(catches(handler, exception, namespace) for handler in node.handlers)
        for exception in kinds
    )


def asks_if_finite(test, keys, namespace):
    """Whether `test` asks the finiteness question about one of these operands."""
    for node in ast.walk(test):
        if not is_finiteness_test(node, namespace):
            continue
        if any(ast.dump(arg) in keys for arg in node.args):
            return True
    return False


def negates_finiteness(test, keys, namespace):
    return (
        isinstance(test, ast.UnaryOp)
        and isinstance(test.op, ast.Not)
        and asks_if_finite(test.operand, keys, namespace)
    )


FINITENESS = "a finiteness test on the same operand"


def discharge(site, kinds, parents, namespace):
    """Why this member is safe, or None when nothing makes it safe.

    A dominance question: walking out from the site, the first enclosing
    construct that answers for its operand answers for it. An early return
    is not an enclosing construct, which is the measured false refusal
    `GUARD_SHAPES` carries."""
    operands = operands_of(site)
    if operands and all(integer_shaped(operand) for operand in operands):
        return "the operand cannot be a derived number"
    if not kinds:
        return "the conversion cannot raise on a value the funnel admits"
    keys = {ast.dump(operand) for operand in operands}
    child, node = site, parents.get(site)
    while node is not None:
        if isinstance(node, ast.Try) and child in node.body:
            if try_covers(node, kinds, namespace):
                return "a try that catches what the conversion raises"
        elif isinstance(node, ast.IfExp):
            if child is node.body and asks_if_finite(node.test, keys, namespace):
                return FINITENESS
            if child is node.orelse and negates_finiteness(node.test, keys, namespace):
                return FINITENESS
        elif isinstance(node, ast.If):
            if child in node.body and asks_if_finite(node.test, keys, namespace):
                return FINITENESS
            if child in node.orelse and negates_finiteness(node.test, keys, namespace):
                return FINITENESS
        elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
            before = node.values[: node.values.index(child)]
            if any(asks_if_finite(value, keys, namespace) for value in before):
                return FINITENESS
        child, node = node, parents.get(node)
    return None


def classify(text, namespace):
    """Every site in `text`, as `(members, unresolved, examined)`.

    `members` are the conversions to an int with what discharges each — None
    where nothing does, which is the failure. `unresolved` are the sites
    whose callee is a value the module computes at runtime. `examined` is
    every node the walk looked at, so the enumeration itself can be compared
    with an independent reading."""
    tree = ast.parse(text)
    parents, units = parents_of(tree), unit_of(tree)
    members, unresolved, examined = [], [], []
    for node in ast.walk(tree):
        if not isinstance(node, SITE_KINDS):
            continue
        examined.append(node)
        where = f"{units.get(node, '<module>')}:{getattr(node, 'lineno', 0)}"
        if isinstance(node, ast.Call):
            fn, path = resolve(node.func, namespace)
            if fn is None:
                unresolved.append((where, node))
                continue
            positional = len(node.args)
            keywords = [kw.arg for kw in node.keywords if kw.arg]
            converts = consumes_an_integer(fn, positional, keywords) and yields_an_int(
                fn, positional, keywords
            )
            kinds = raised_by(fn, positional, keywords) if converts else set()
        else:
            path = ast.unparse(node)[:60]
            converts = operator_converts(node)
            kinds = operator_raised(node) if converts else set()
        if converts:
            members.append((where, path, discharge(node, kinds, parents, namespace)))
    return members, unresolved, examined


@pytest.fixture(scope="module")
def namespace():
    return namespace_of()


@pytest.fixture(scope="module")
def module_text():
    return source()


# --- the property, over the shipped module ----------------------------------


def test_every_int_conversion_in_the_module_is_discharged(module_text, namespace):
    """The class, over the module as it stands.

    A member with nothing discharging it is a derived number one non-finite
    sum away from ending the report with stdout empty, which is what #175's
    four rounds were about."""
    members, _unresolved, _examined = classify(module_text, namespace)
    undischarged = [(where, path) for where, path, why in members if why is None]
    assert not undischarged, (
        "a site converts a number to an int and nothing discharges it. Put a "
        "finiteness test on the same operand in the ENCLOSING conditional, or "
        "wrap it in a `try` catching what the conversion raises:\n"
        + "\n".join(f"  session_cost.py#{w}  {p}" for w, p in undischarged)
    )


def test_the_class_holds_the_site_the_defect_came_through(module_text, namespace):
    """A property that found no members would pass on anything.

    The member named here is the one round 3 of #175 fixed, so this case dies
    if the walk stops reaching it — which is how this check would go vacuous
    without anybody noticing."""
    members, _unresolved, _examined = classify(module_text, namespace)
    assert any(where.startswith("token_thirds:") for where, _p, _w in members), (
        f"the walk no longer reaches the conversion in token_thirds: {members}"
    )


def test_the_walk_examines_every_call_and_operator_site(module_text, namespace):
    """The enumeration is by construction, checked against a second reading.

    What `classify` looked at is compared with a set taken independently off
    the module's tree, so a site cannot be dropped on the way through the
    classifier without this case saying so. The claim is set equality; no
    count appears, because a count is what #192 exists to stop standing in
    for a property."""

    def coordinates(nodes):
        return {
            (type(n).__name__, getattr(n, "lineno", 0), getattr(n, "col_offset", 0))
            for n in nodes
        }

    _members, _unresolved, examined = classify(module_text, namespace)
    independent = [
        node
        for node in ast.walk(ast.parse(module_text))
        if isinstance(node, SITE_KINDS)
    ]
    # Two parses give two node objects for one site, so the readings are
    # compared by position and kind rather than by identity.
    assert coordinates(examined) == coordinates(independent)
    assert independent, "the module has no call or operator site; the walk is vacuous"


def test_no_operator_in_this_module_converts_a_number_to_an_int(module_text):
    """The other dimension, closed by construction rather than by assertion.

    `//` and `%` produce integers and neither converts one — `inf // 3` is a
    `nan` and nothing raises — so the operators are enumerated and probed and
    the answer is derived. This case is what turns red if a future operator
    changes it."""
    converting = [
        ast.unparse(node)[:60]
        for node in ast.walk(ast.parse(module_text))
        if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.AugAssign, ast.Compare))
        and operator_converts(node)
    ]
    assert not converting, converting


def test_the_unresolved_callees_are_runtime_receivers(module_text, namespace):
    """The residual, named as a shape a next editor can act on.

    Round 3 of #175 asked for exactly this — a limit written as something
    actionable rather than as an excuse. Every callee this walk cannot
    resolve is a name the module binds inside a function, or an expression
    with no name at all; never a name the module binds nowhere, which would
    be the resolver failing rather than a receiver being a runtime value."""
    _members, unresolved, _examined = classify(module_text, namespace)
    bound = names_bound_inside(ast.parse(module_text))
    stray = [
        (where, ast.unparse(node.func)[:60])
        for where, node in unresolved
        if root_name(node.func) is not None and root_name(node.func) not in bound
    ]
    assert not stray, (
        "a callee resolved to nothing and the module binds its name nowhere, "
        f"so the resolver missed it rather than the receiver being runtime: {stray}"
    )


def test_the_operator_half_is_probed_and_says_what_it_cannot_see():
    """The operator dimension, with a positive control so its `no` is a
    measurement rather than an unreachable branch.

    Over numeric operands no binary operator reaches an int through an
    operand — `//` and `%` build integers out of integers and convert
    nothing — which is what the walk reports for the module. Sequence
    repetition does convert, and it is the route a numeric probe cannot see.

    `//` on a huge integer and a float DOES raise, and it is still not a
    member: what a site raises only matters once it converts, and this is
    the line between #192's class and the wider one in `questions.md` Q2."""
    mult = ast.parse("a * b").body[0].value
    floordiv = ast.parse("a // b").body[0].value
    assert operator_forms(mult) == ["a * b"]
    assert operator_forms(floordiv) == ["a // b"]
    assert not operator_converts(mult)
    assert not operator_converts(floordiv)
    assert operator_converts(mult, benign="ab"), (
        "sequence repetition no longer converts, so the negative answer above "
        "is an unreachable branch rather than a measurement"
    )
    assert operator_raised(mult, benign="ab") == {OverflowError}
    assert operator_raised(floordiv) == {OverflowError}


def test_a_type_error_is_not_a_hazard_the_guard_has_to_cover():
    """A `TypeError` is the probe's own filler talking, not a hazard.

    Measured: `round(3.0, inf)` raises `TypeError` because `ndigits` has to
    be an index, so a derived value in that slot says nothing about the
    conversion — and demanding a guard for it would refuse a site over the
    probe's choice of filler. That filler cuts the other way too and this is
    where the limit is stated: with a benign float in an index slot, every
    call raises `TypeError` first, so a two-argument conversion's hazards
    come from the slot the probe can still reach."""
    assert quiet(lambda: round(3.0, float("inf")))[1] is TypeError
    assert TypeError not in raised_by(round, 2, [])
    assert raised_by(round, 1, []) == {OverflowError, ValueError}


def test_a_call_on_a_literal_receiver_resolves(module_text, namespace):
    """`" ".join(text.split())` in `load` is a method on a literal.

    The resolver answers for it, because a literal is itself. Left
    unresolved it would join the residual, and the residual is the set this
    file promises holds only receivers computed at runtime."""
    _members, unresolved, _examined = classify(module_text, namespace)
    literal_receivers = [
        where
        for where, node in unresolved
        if isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Constant)
    ]
    assert not literal_receivers, literal_receivers
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Constant)
        for node in ast.walk(ast.parse(module_text))
    ), "the module no longer calls a method on a literal, so this case is vacuous"


def test_the_residual_check_names_a_callee_the_module_binds_nowhere(tmp_path):
    """The residual check can fail, which is what makes it a check.

    A call through a name the module binds nowhere is the resolver missing
    something rather than a receiver being a runtime value, and that is the
    one shape `test_the_unresolved_callees_are_runtime_receivers` refuses."""
    text = "def under_test(value):\n    return nowhere.convert(value)\n"
    _members, unresolved, _examined = classify(
        text, namespace_of_source(text, tmp_path)
    )
    bound = names_bound_inside(ast.parse(text))
    stray = [
        where
        for where, node in unresolved
        if root_name(node.func) is not None and root_name(node.func) not in bound
    ]
    assert stray, "a callee the module binds nowhere was not named"


def test_a_callable_that_yields_an_int_without_converting_is_not_a_member(tmp_path):
    """Both probes have to agree, and this is the half the first one answers.

    A function that answers with an integer without ever consuming its
    operand as one cannot raise on a derived value, so requiring a guard of
    it would be a refusal with nothing behind it."""
    text = (
        "def bucket(value):\n"
        "    return 1 if value > 0 else 0\n"
        "\n\n"
        "def under_test(mean):\n"
        "    return [bucket(mean)]\n"
    )
    bindings = namespace_of_source(text, tmp_path)
    assert yields_an_int(bindings["bucket"], 1, [])
    assert not consumes_an_integer(bindings["bucket"], 1, [])
    members, _unresolved, _examined = classify(text, bindings)
    assert not [where for where, _p, _why in members if where.startswith("under_test:")]


def test_a_predicate_that_converts_but_answers_a_bool_is_not_a_member(namespace):
    """The third stated residual, kept visible instead of incidental.

    `math.isfinite` consumes its operand through the integer protocol — which
    is why `math.isfinite` on an integer with no float of its own raises, the
    🔴 of round 2 of #175 — and it answers with a `bool`, so it is not a
    conversion TO an int and not a member here. Both halves are asserted,
    because the exclusion rests on the second one and a later edit that
    dropped `yields_an_int` would otherwise pass silently."""
    isfinite = namespace["math"].isfinite
    assert consumes_an_integer(isfinite, 1, [])
    assert not yields_an_int(isfinite, 1, [])
    assert raised_by(isfinite, 1, []) == {OverflowError}, (
        "the hazard this exclusion accepts is no longer the one it was measured against"
    )


# --- what the classifier accepts, and what it refuses -----------------------

GUARD_SHAPES = (
    (
        "a finiteness test on the same operand, the shape the module uses",
        "    return [round(mean) if math.isfinite(mean) else 0]",
        True,
    ),
    (
        "a statement-level finiteness test",
        "    if math.isfinite(mean):\n        return [round(mean)]\n    return [0]",
        True,
    ),
    (
        "the same test negated, with the conversion in the other arm",
        "    if not math.isfinite(mean):\n        return [0]\n"
        "    else:\n        return [round(mean)]",
        True,
    ),
    (
        "a finiteness test earlier in the same conjunction",
        "    return [math.isfinite(mean) and round(mean)]",
        True,
    ),
    (
        "a try whose handlers cover both exceptions a conversion raises",
        "    try:\n        return [round(mean)]\n"
        "    except (OverflowError, ValueError):\n        return [0]",
        True,
    ),
    (
        "a bare except, which covers whatever the conversion raises",
        "    try:\n        return [round(mean)]\n    except:\n        return [0]",
        True,
    ),
    (
        "an except Exception, which covers both of them",
        "    try:\n        return [round(mean)]\n"
        "    except Exception:\n        return [0]",
        True,
    ),
    (
        "an integer literal operand, which no transcript derived",
        "    return [round(7)]",
        True,
    ),
    (
        "integer arithmetic over literals, still nothing derived",
        "    return [round(7 // 2)]",
        True,
    ),
    (
        "a boolean literal, which no transcript derived either",
        "    return [round(True)]",
        True,
    ),
    (
        "a converter that already guards itself needs no second guard",
        "    return [safe_int(mean)]",
        True,
    ),
    (
        "a conversion nobody could have put on a name list",
        "    return [to_int(mean) if math.isfinite(mean) else 0]",
        True,
    ),
    (
        "an aliased import doing the converting",
        "    return [m.floor(mean) if math.isfinite(mean) else 0]",
        True,
    ),
    (
        "a hand-written finiteness predicate is a guard",
        "    return [round(mean) if sane(mean) else 0]",
        True,
    ),
    # The refusals. The last one is a measured false refusal, kept here with
    # the verdict it actually gets rather than described in prose.
    (
        "no guard at all — the shape this whole file exists to catch",
        "    return [round(mean)]",
        False,
    ),
    (
        "the same conversion by a local function, with the guard taken away",
        "    return [to_int(mean)]",
        False,
    ),
    (
        "the aliased import unguarded",
        "    return [m.floor(mean)]",
        False,
    ),
    (
        "a from-import doing the converting, unguarded",
        "    return [trunc(mean)]",
        False,
    ),
    (
        "a finiteness test on a different operand",
        "    return [round(mean) if math.isfinite(other) else 0]",
        False,
    ),
    (
        "a guard that answers a different question",
        "    return [round(mean) if mean > 0 else 0]",
        False,
    ),
    (
        "a predicate on the same operand that is not a finiteness test",
        "    return [round(mean) if positive(mean) else 0]",
        False,
    ),
    (
        "a predicate that is falsy for a benign number as well",
        "    return [round(mean) if never(mean) else 0]",
        False,
    ),
    (
        "a conversion reached through a keyword argument, guarded",
        "    return [to_int_kw(value=mean) if math.isfinite(mean) else 0]",
        True,
    ),
    (
        "a try covering only the OverflowError, so a NaN still ends the report",
        "    try:\n        return [round(mean)]\n"
        "    except OverflowError:\n        return [0]",
        False,
    ),
    (
        "an early return rather than an enclosing conditional",
        "    if not math.isfinite(mean):\n        return [0]\n    return [round(mean)]",
        False,
    ),
)

PREAMBLE = (
    "import math\n"
    "import math as m\n"
    "from math import trunc\n"
    "\n\n"
    "def to_int(value):\n"
    "    return int(value)\n"
    "\n\n"
    "def sane(value):\n"
    "    return math.isfinite(value)\n"
    "\n\n"
    "def positive(value):\n"
    "    return value > 0\n"
    "\n\n"
    "def never(value):\n"
    "    return False\n"
    "\n\n"
    "def to_int_kw(value=1.0):\n"
    "    return int(value)\n"
    "\n\n"
    "def safe_int(value):\n"
    "    try:\n"
    "        return int(value)\n"
    "    except (OverflowError, ValueError):\n"
    "        return 0\n"
    "\n\n"
)


@pytest.mark.parametrize(
    ("name", "body", "discharged"),
    [pytest.param(*row, id=row[0]) for row in GUARD_SHAPES],
)
def test_the_guard_shapes_are_decided_by_what_they_catch(
    name, body, discharged, tmp_path
):
    """Nineteen constructed shapes, each classified rather than asserted about.

    Three of them are the point of the design: a converter written in the
    module under test, an aliased import and a `from`-import all classify
    like `round`, and a hand-written predicate counts as a guard — none of
    them appears in this file as a name. The refusals are the other half: a
    `try` covering only `OverflowError` leaves a `NaN` ending the report, and
    a test on a different operand answers about a different value."""
    text = f"{PREAMBLE}def under_test(mean, other=1.0):\n{body}\n"
    members, _unresolved, _examined = classify(
        text, namespace_of_source(text, tmp_path)
    )
    inside = [
        (where, why) for where, _p, why in members if where.startswith("under_test:")
    ]
    assert inside, f"{name}: the walk found no conversion in the unit at all"
    assert all(why is not None for _w, why in inside) == discharged, f"{name}: {inside}"


def test_an_unguarded_conversion_added_to_the_module_is_named(module_text, namespace):
    """The mutation, in the suite: the real module with one unguarded site.

    A check that has never failed proves nothing, and this is the shape the
    class exists for — a new conversion added by a later edit, in a unit
    nobody thought to look at."""
    text = module_text.replace(
        "def strip_pipe(command):",
        "def total_seconds(spans):\n    return int(sum(spans))\n\n\n"
        "def strip_pipe(command):",
        1,
    )
    assert "def total_seconds" in text, "the mutation did not land"
    members, _unresolved, _examined = classify(text, namespace)
    undischarged = [where for where, _p, why in members if why is None]
    assert any(where.startswith("total_seconds:") for where in undischarged), (
        f"the added site was not named: {members}"
    )


def test_the_module_states_the_rule_and_the_two_shapes_it_misses(module_text):
    """A rule nobody meets is a rule the next edit breaks.

    `token_thirds` is where the conversion is, so its docstring is where a
    next editor reads what the class is, where the check lives, and the two
    shapes the property does not reach. Pinned here because a stated limit
    that can be deleted silently is not stated."""
    unit = next(
        node
        for node in ast.parse(module_text).body
        if isinstance(node, ast.FunctionDef) and node.name == "token_thirds"
    )
    text = " ".join((ast.get_docstring(unit) or "").split())
    assert "test_a_derived_number_reaching_an_int_carries_a_guard" in text, (
        "the docstring does not name the check that enforces the rule"
    )
    for shape in ("subscript", "division"):
        assert shape in text, f"the docstring does not name the {shape} residual"
    assert "#192" in text, "the docstring does not name the issue the class came from"
