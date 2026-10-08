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
    # A refused suffix yields no units, so the rename scan and `--migrate`
    # name nothing there: `render(` here would match the brace rule's opener.
    assert ec.file_units("svc.rb", "def render(x)\n  1\nend\n") == []
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


def test_a_citation_of_a_released_row_by_a_bare_symbol_is_refused(tmp_path):
    """`read_citation` is the fourth caller, and the one the frame did not
    list: a citing row's first coordinate names a section of a released
    ledger file. A bare symbol there names no heading, and the line says so
    rather than calling the section gone."""
    body = "# 0.3.0\n\n## Rows\n\n| R1 · claim | `a.py#f@00000000` |\n"
    released = tmp_path / "seal" / "releases"
    released.mkdir(parents=True)
    (released / "0.3.0.md").write_text(body, encoding="utf-8")
    cite = ec.ANCHOR_RE.search('`seal/releases/0.3.0.md#Rows>"| R1 · claim"@0000abcd`')

    def load(path):
        return "id", (path, body, ec.gfm_lines(body), {5: None})

    verdict, at = ec.read_citation(cite, "Re-read", str(tmp_path), {}, None, load)
    assert verdict.status == "BROKEN" and at is None, verdict
    assert verdict.detail == ec.resolve_unit("x.md", "Rows", body).refused, verdict


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


# --- S1, S3: the bracket walk bounds what the indentation rule cut ----------

MULTI_LINE = (
    "export function multiLine(\n"
    "  opts: { a: number },\n"
    "): number {\n"
    "  return opts.a + 1\n"
    "}\n"
)


def test_a_prettier_signature_keeps_its_body_in_the_span():
    """S1, #848's shape. The `(` stays open over the parameter lines, the
    `{` opens the body, and the unit ends where both have closed. The
    indentation rule ended it at `): number {`, lines 1-2."""
    assert ec.resolve_unit("f.ts", "multiLine", MULTI_LINE) == ([(1, 4)], False)


def test_848s_reproduction_reads_a_body_edit_as_drifted(repo):
    """#848's own script, as a case: stamp the row with `--reverify`, change
    the body only, and `--strict` must say DRIFTED where it said `1 ok`."""
    (repo / "f.ts").write_text(MULTI_LINE, encoding="utf-8")
    cite(repo, "f.ts#multiLine@00000000")
    ledger = "seal/ledger/f.md"
    rr = run(
        ["--reverify", "--checked", "2026-10-07", "--ledger", ledger, "."], str(repo)
    )
    assert rr.returncode == 0, rr.stdout + rr.stderr
    assert run(["--strict", "--ledger", ledger, "."], str(repo)).returncode == 0
    body = MULTI_LINE.replace("return opts.a + 1", "return opts.a * 100")
    (repo / "f.ts").write_text(body, encoding="utf-8")
    r = run(["--strict", "--ledger", ledger, "."], str(repo))
    assert r.returncode != 0 and "DRIFTED" in r.stdout, r.stdout
    assert "content changed at 1-4" in r.stdout, r.stdout


@pytest.mark.parametrize(
    "rel, text, name, span",
    [
        # S3: Allman. The parentheses close on the signature line and the
        # next line opens with `{`; the indentation rule bounded line 1 alone.
        ("f.c", "int add(int x)\n{\n  return x + 1;\n}\n", "add", (1, 3)),
        # GNU: the `{` is deeper than the signature, which the walk also reads.
        ("f.c", "int add(int x)\n  {\n    return x;\n  }\n", "add", (1, 3)),
        # A constant whose value continues on deeper lines.
        ("f.ts", "export const L =\n  [1, 2];\nexport const B = 2;\n", "L", (1, 2)),
        # A one-line signature, exactly as the indentation rule had it.
        ("f.go", "func f(x int) int {\n\treturn x\n}\n", "f", (1, 2)),
    ],
)
def test_the_walk_bounds_the_shapes_a_formatter_writes(rel, text, name, span):
    assert ec.resolve_unit(rel, name, text) == ([span], False)


# --- Q1: each family's forms are blanked, a case per form ------------------

# Every fixture holds an OPENING bracket inside each string, char and comment
# form of its language, so a form read as code leaves a bracket open and the
# unit is refused. A stray closer would not show it: the body's deeper lines
# carry the walk past an early close, and the closer-only last line is left
# out either way (measured by mutating each form, #870). Holes hold a nested
# string with a bracket in it, so a hole read as content ends its string
# early. Each unit ends at its last line, so its span is (1, last - 1).
FORMS = {
    "js": (
        "f.ts",
        "function f(a) {\n"
        '  const s = "{";\n'
        "  const t = '(';\n"
        "  const u = `[ ${ {k: 1}.k }`;\n"
        "  const v = `{\n"
        "  `;\n"
        "  // {\n"
        "  /* ( */\n"
        "  return a;\n"
        "}\n",
    ),
    "c": (
        "f.c",
        "int f(int a) {\n"
        "  char c = '{';\n"
        '  const char *s = "(\\"";\n'
        "  int n = 1'000;\n"
        "  /* { */\n"
        "  // (\n"
        "  return a;\n"
        "}\n",
    ),
    "cpp": (
        "f.cpp",
        "int f(int a) {\n"
        '  auto r = R"x({)x";\n'
        '  auto p = u8R"(")";\n'
        "  char c = '{';\n"
        "  return a;\n"
        "}\n",
    ),
    "java": (
        "F.java",
        "String f(int a) {\n"
        '  String b = """\n'
        "      {\n"
        '      """;\n'
        "  char c = '(';\n"
        '  return "[";\n'
        "}\n",
    ),
    "cs": (
        "F.cs",
        "string F(int a) {\n"
        '  var v = @"C:\\" + a + "(";\n'
        '  var i = $"{a} }}{{ {d["{"]}";\n'
        '  var r = """\n'
        "    {\n"
        '    """;\n'
        "  char c = '(';\n"
        '  return $@"{d["{"]}\\";\n'
        "}\n",
    ),
    "kotlin": (
        "f.kt",
        "fun f(a: Int): String {\n"
        '  val s = "${ mapOf(1 to "{").size } ("\n'
        '  val r = """\n'
        "    { ${a}\n"
        '  """\n'
        "  val c = '['\n"
        "  /* outer /* inner ( */ still comment { */\n"
        "  return s\n"
        "}\n",
    ),
    "swift": (
        "f.swift",
        "func f(a: Int) -> String {\n"
        '  let s = "\\( d["{"] ) ("\n'
        '  let r = #"raw "{" here"#\n'
        '  let m = """\n'
        "    {\n"
        '    """\n'
        "  /* a /* nested { */ ( */\n"
        "  return s\n"
        "}\n",
    ),
    "go": (
        "f.go",
        "func f(a int) string {\n"
        "\tr := '{'\n"
        "\ts := `(\n"
        "\t`\n"
        '\tt := "["\n'
        "\treturn s\n"
        "}\n",
    ),
    "rust": (
        "f.rs",
        "fn f(a: &'static str) -> &'static str {\n"
        "    let c = '{';\n"
        '    let r = r#"("{"#;\n'
        '    let s = "multi\n'
        '    [ line";\n'
        "    /* outer /* inner { */ ( */\n"
        "    a\n"
        "}\n",
    ),
}


@pytest.mark.parametrize("family", sorted(FORMS))
def test_each_familys_string_and_comment_forms_are_blanked(family):
    rel, text = FORMS[family]
    name = "F" if rel.endswith(".cs") else "f"
    assert ec.brace_family(rel) == family
    last = len(text.splitlines())
    unit = ec.resolve_unit(rel, name, text)
    assert unit == ([(1, last - 1)], False), (family, unit, unit.refused)


def test_every_suffix_on_the_list_names_a_family_with_a_case():
    """A language joins the list only with its forms written down and a case
    for each (Q1)."""
    assert set(ec.BRACE_FAMILY.values()) == set(FORMS)
    assert frozenset(ec.BRACE_FAMILY) == ec.BRACE_SUFFIXES


# --- S4: what the walk cannot bound is refused -----------------------------

REMEDY = "; anchor a quoted line instead"


@pytest.mark.parametrize(
    "rel, text, why",
    [
        (
            "f.ts",
            "export function f() {\n  if (x) {\n    return 1;\n}\n",
            "declared on line 1: the `{` of line 1 is never closed",
        ),
        (
            "f.ts",
            "function f() {\n  return 1;\n}}\n",
            "declared on line 1: line 3 closes a `}` nobody opened",
        ),
        (
            "f.ts",
            "function f() {\n  return (1];\n}\n",
            "declared on line 1: line 2 closes the `(` of line 2 with `]`",
        ),
        (
            "f.ts",
            "function f() {\n  /* never\n  return 1;\n}\n",
            "declared on line 1: a string or comment opened at line 2 never ends",
        ),
        (
            "f.ts",
            'function f() {\n  const s = "abc;\n  return 1;\n}\n',
            "declared on line 1: line 2 opens a string or char literal it never closes",
        ),
        (
            "f.cpp",
            'int f() {\n  auto r = R"a b(x)a b";\n  return 1;\n}\n',
            "declared on line 1: line 2 holds a raw string the walk cannot read",
        ),
    ],
)
def test_a_unit_the_walk_cannot_bound_is_refused_with_why(rel, text, why):
    """S4, and the unterminated forms. Each line a person reads is pinned
    whole: the unit, the reason, the remedy."""
    unit = ec.resolve_unit(rel, "f", text)
    assert unit.places == [], unit
    assert unit.refused == f"the bracket walk cannot bound `f` ({why}){REMEDY}"


def test_an_unbalanced_unit_reads_broken_and_reverify_writes_nothing(repo):
    """S4, both readings: the check prints the refusal and exits 2, and
    `--reverify` prints it too and leaves the row as it was."""
    text = "export function f() {\n  if (x) {\n    return 1;\n}\n"
    (repo / "src" / "f.ts").write_text(text, encoding="utf-8")
    ledger = cite(repo, "src/f.ts#f@00000000")
    line = "the bracket walk cannot bound `f` (declared on line 1: the `{` of "
    r = run(["."], str(repo))
    assert r.returncode == 2 and "BROKEN" in r.stdout and line in r.stdout, r.stdout
    rr = run(["--reverify", "--checked", "2026-10-08", "."], str(repo))
    assert line in rr.stdout + rr.stderr, rr.stdout + rr.stderr
    assert (repo / "seal" / "ledger" / "f.md").read_text(encoding="utf-8") == ledger


def test_a_walk_refusal_reaches_past_a_unit_it_does_not_cross():
    """An unterminated string refuses the unit that crosses it, and only
    that unit: the line after it is lexed as code again."""
    text = 'function g() {\n  return 1;\n}\n\nconst s = "open;\n'
    assert ec.resolve_unit("f.js", "g", text) == ([(1, 2)], False)


def test_nothing_below_a_raw_string_the_walk_cannot_read_is_bounded():
    """Where an unreadable form ends is exactly what is unknown, so every
    line below it is refused too, and a unit above it is not."""
    text = 'int g() {\n  return 0;\n}\n\nauto r = R"a b(x)a b";\n\nint f() {\n  return 1;\n}\n'
    assert ec.resolve_unit("f.cpp", "g", text) == ([(1, 2)], False)
    assert "line 5 holds a raw string" in ec.resolve_unit("f.cpp", "f", text).refused


def test_the_lexed_stream_is_computed_once_per_text():
    """A file many rows cite is lexed once, as `parsed_spans` parses once."""
    text = MULTI_LINE + "\nexport const OTHER = 1;\n"
    ec.brace_lexed.cache_clear()
    ec.resolve_unit("f.ts", "multiLine", text)
    ec.resolve_unit("f.ts", "OTHER", text)
    info = ec.brace_lexed.cache_info()
    assert info.misses == 1 and info.hits >= 1, info


# --- S9: one opener ----------------------------------------------------------


def test_the_declaration_opener_is_spelled_once():
    """S9. `file_units` listed names with its own copy of the opener
    (inventory E18), so a change to one could list a name the other could
    then not find."""
    source = open(SCRIPT, encoding="utf-8").read()
    assert source.count(r"[\w\s*&]*?") == 1, "the opener is spelled twice"
    tree = ast.parse(source)
    for fn in ("generic_units", "file_units"):
        (node,) = [
            n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == fn
        ]
        assert "declaration_opener(" in ast.unparse(node), fn
    units = {n: p for n, p, _u in ec.file_units("f.ts", MULTI_LINE)}
    assert units["multiLine"] == (1, 4), units
    # The colon judgment travels with the opener: `x in NAME:` is a use.
    use = "LIMIT: 1\nwhen v in OTHER:\n"
    assert ec.resolve_unit("w.yml", "OTHER", use) == ([], False)
    assert {n for n, _p, _u in ec.file_units("w.yml", use)} == {"LIMIT"}
