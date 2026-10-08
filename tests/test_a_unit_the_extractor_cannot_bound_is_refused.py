"""A unit the extractor cannot bound is refused, never hashed over a span
that leaves its body out (#870, #848).

Every file that was not `.py` or `.md` went through one rule — a declaration
line, then every line until the next line at the same or lower indentation.
In a brace language the indentation is formatting, so the rule ended a
Prettier-formatted multi-line TypeScript signature at its `): number {` line,
and the body sat outside the hash: a rewrite of it read `ok`. A `.py` the
running interpreter could not parse fell through to the same rule.

What replaced it is one table of rules, `bounding_rule`, each refusing what
it does not recognise, and one reading, `resolve_unit`'s `Resolution`, that
carries the refusal to every caller.

  the table      one suffix test, read by the four units that used to test
                 the suffix on their own
  the refusals   a `.py` that will not parse, a suffix no rule names, a bare
                 symbol in markdown: BROKEN, the reason and the remedy on it
  one reading    `judge`, `read_citation`, the rider check and the survivor
                 sweep read the refusal from `resolve_unit`, none re-derives it
"""

import ast
import importlib.util
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")
RIDER = os.path.join(ROOT, ".github", "scripts", "rider_check.py")
SURVIVOR = os.path.join(ROOT, "skills", "code-review", "scripts", "survivor_check.py")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ec = _load("specseal_evidence_check_870", SCRIPT)


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "seal" / "ledger").mkdir(parents=True)
    return d


def cite(repo, coordinate):
    """One ledger row citing COORDINATE, as a fragment."""
    (repo / "seal" / "ledger" / "f.md").write_text(
        "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
        "|---|---|---|---|---|\n"
        f"| C1 | `{coordinate}` | read | 2026-10-08 | n |\n",
        encoding="utf-8",
    )
    return (repo / "seal" / "ledger" / "f.md").read_text(encoding="utf-8")


# --- S5: a suffix no rule names --------------------------------------------

RUBY = "def render\n  1\nend\n"
NO_RULE = "no bounding rule for `.rb`; anchor a quoted line instead"


def test_a_bare_symbol_in_a_suffix_no_rule_names_is_refused_with_the_remedy(repo):
    """S5. Ruby's `end` closes a block no bracket marks, and the indentation
    rule read it only because it happened to sit at the declaration's
    indent. The refusal is the line a person reads, so it is pinned whole;
    the quoted-line anchor it names still resolves as it always did."""
    unit = ec.resolve_unit("svc.rb", "render", RUBY)
    assert unit.places == [] and unit.refused == NO_RULE, unit.refused
    assert ec.resolve_unit("svc.rb", '"def render"', RUBY) == ([(1, 3)], False)
    assert ec.resolve_unit("svc.rb", '"def render"', RUBY).refused is None
    bare = ec.resolve_unit("bin/tool", "main", "main() {\n  x\n}\n").refused
    assert bare == "no bounding rule for a file with no suffix; " + (
        "anchor a quoted line instead"
    )

    (repo / "src" / "svc.rb").write_text(RUBY, encoding="utf-8")
    ledger = cite(repo, "src/svc.rb#render@00000000")
    r = run(["."], str(repo))
    assert r.returncode == 2, r.stdout
    assert "BROKEN" in r.stdout and NO_RULE in r.stdout, r.stdout
    rr = run(["--reverify", "--checked", "2026-10-08", "."], str(repo))
    assert NO_RULE in rr.stdout + rr.stderr, rr.stdout + rr.stderr
    assert (repo / "seal" / "ledger" / "f.md").read_text(encoding="utf-8") == ledger


def test_a_bare_symbol_in_markdown_is_refused_and_names_the_heading_path():
    """The heading rule bounds a quoted heading path; a bare symbol in a
    `.md` was read by the brace rule before, which no markdown file is."""
    text = "## A\n\nrender: x\n  y\n"
    unit = ec.resolve_unit("d.md", "render", text)
    assert unit.places == [], unit
    assert unit.refused == (
        "a markdown unit is a heading, and a bare symbol names none — "
        'anchor its heading path instead, `"## <heading>"`'
    )
    assert ec.resolve_unit("d.md", '"## A"', text) == ([(1, 4)], False)


def test_markdown_and_mdx_are_no_heading_files():
    """They were never on the heading rule (a quoted heading there resolves
    as a paragraph), so refusing their bare symbols changes no right
    reading."""
    for name in ("d.markdown", "d.mdx", "d.rb", "d.sh", "d.toml", "d.json"):
        assert ec.bounding_rule(name) is None, name
    assert ec.bounding_rule("a.py") == ec.bounding_rule("a.pyi") == "ast"
    assert ec.bounding_rule("a.md") == "heading"
    assert ec.bounding_rule("w.yml") == ec.bounding_rule("w.yaml") == "block"
    assert ec.bounding_rule("svc.ts") == ec.bounding_rule("lib.rs") == "brace"


# --- S6: Python refuses, never guesses -------------------------------------

# A multi-line `def` the running interpreter cannot read, because of one
# deliberate SyntaxError line below it. The indentation rule bounded `f` at
# lines 1-2: `):` sits at the declaration's own indent.
UNPARSEABLE = "def f(\n    a,\n):\n    return a\n\nx = (:\n"


def test_a_python_file_that_will_not_parse_is_refused_naming_the_interpreter(repo):
    """S6. The fall-through to the text rule hashed lines 1-2 of the five
    and left the body out, silently. The refusal names the interpreter so a
    reader can tell a grammar mismatch from a missing file, and the line of
    the error so they can find it."""
    assert ec.py_spans(UNPARSEABLE) is None
    unit = ec.resolve_unit("bad.py", "f", UNPARSEABLE)
    version = ".".join(str(n) for n in sys.version_info[:3])
    assert unit.places == [], unit
    assert unit.refused.startswith(f"Python {version} cannot parse this file ("), (
        unit.refused
    )
    assert "at line 6)" in unit.refused, unit.refused
    assert unit.refused.endswith(
        "so no unit in it is bounded and none is guessed at — run the checker "
        "on the Python the file is written for, or anchor a quoted line instead"
    ), unit.refused

    lines = ec.gfm_lines(UNPARSEABLE)
    old = ec.content_hash(lines[0:2])
    (repo / "src" / "bad.py").write_text(UNPARSEABLE, encoding="utf-8")
    cite(repo, f"src/bad.py#f@{old}")
    r = run(["."], str(repo))
    assert r.returncode == 2 and "BROKEN" in r.stdout, r.stdout
    assert f"Python {version} cannot parse" in r.stdout, r.stdout
    assert old not in r.stdout.replace(f"#f@{old}", ""), r.stdout


def test_a_python_file_that_parses_is_read_as_it_was():
    parsing = UNPARSEABLE.replace("x = (:\n", "x = 1\n")
    assert ec.resolve_unit("ok.py", "f", parsing) == ([(1, 4)], False)
    assert ec.resolve_unit("ok.py", "f", parsing).refused is None
    assert ec.resolve_unit("ok.py", "missing", parsing).refused is None


# --- S8: one reading reaches every caller ----------------------------------


def callers(path, name):
    """{function: source of its body} for every function in PATH whose body
    calls NAME, by name or as an attribute."""
    tree = ast.parse(open(path, encoding="utf-8").read())
    out = {}

    def walk(node, owner):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                walk(child, child)
                continue
            if isinstance(child, ast.Call) and owner is not None:
                f = child.func
                called = f.id if isinstance(f, ast.Name) else getattr(f, "attr", None)
                if called == name:
                    out[owner.name] = ast.unparse(owner)
            walk(child, owner)

    walk(tree, None)
    return out


def test_every_caller_reads_the_refusal_from_resolve_unit_and_derives_none():
    """S8. Two readings of one coordinate describe one row two ways (#809).
    So the refusal travels in `resolve_unit`'s answer, and the callers that
    print a verdict ask that answer for it; none of the five asks the suffix
    table or the parser for itself."""
    found = {
        "evidence_check": callers(SCRIPT, "resolve_unit"),
        "rider_check": callers(RIDER, "resolve_unit"),
        "survivor_check": callers(SURVIVOR, "resolve_unit"),
    }
    assert {k: sorted(v) for k, v in found.items()} == {
        "evidence_check": ["judge", "read_citation", "resolve"],
        "rider_check": ["region_lines"],
        "survivor_check": ["resolves"],
    }, found
    for module, funcs in found.items():
        for name, source in funcs.items():
            for derived in ("bounding_rule(", "py_spans(", "unbounded("):
                assert derived not in source, f"{module}.{name} calls {derived}"
    for name, source in [
        ("judge", found["evidence_check"]["judge"]),
        ("read_citation", found["evidence_check"]["read_citation"]),
        ("region_lines", found["rider_check"]["region_lines"]),
    ]:
        assert ".refused" in source, f"{name} drops the refusal"


def test_the_rider_check_prints_the_checkers_refusal():
    riders = _load("rider_check_870", RIDER)
    kept, why = riders.region_lines(ec, "svc.rb", "render", RUBY)
    assert kept is None and why == NO_RULE, why


def test_the_survivor_sweep_reads_a_refused_anchor_as_not_resolving():
    """A refused anchor resolves at neither end of a range, so it never
    counts as one the range removed. The sweep reads `resolve_unit`'s places,
    which a refusal leaves empty — where the fall-through gave a `.py` that
    will not parse a two-line span to resolve to."""
    assert not ec.resolve_unit("bad.py", "f", UNPARSEABLE)[0]
    assert not ec.resolve_unit("svc.rb", "render", RUBY)[0]


# --- S10: one suffix table --------------------------------------------------


def test_the_four_dispatches_read_one_table():
    """S10. Four units tested the suffix on their own (inventory E16), so a
    language added in one was missing in three."""
    source = open(SCRIPT, encoding="utf-8").read()
    tree = ast.parse(source)
    bodies = {
        n.name: ast.unparse(n)
        for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef)
        and n.name in ("resolve_unit", "minor_region", "file_units", "content_matches")
    }
    assert len(bodies) == 4, sorted(bodies)
    for name, body in bodies.items():
        assert "bounding_rule(" in body, f"{name} does not read the table"
        for spelled in ('endswith(".py")', "endswith('.py')", ".md')", '.md")'):
            assert spelled not in body, f"{name} tests the suffix itself: {spelled}"
