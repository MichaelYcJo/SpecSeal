"""A ledger coordinate names a place by content, and reports change by content.

The whole of the mechanism this replaces was compensation for one fact: a
coordinate made of a line number rots on contact. A line moves for edits that
have nothing to do with the claim, so the coordinate is re-anchored, so the
row's derived baseline resets, so a stamp is needed to clear it, so a squash
orphans the stamp. Three review rounds were spent on that chain, and half of
the branch's commits touched `.specseal/` rather than the code it describes.

An anchor plus a content hash removes the cause. There is no baseline, no
stamp, no commit SHA, and the CHECK path reaches for git nowhere — the one
exception is `--migrate`, a one-shot writer that may consult the old stamp's
commit before trusting a line number (round 4, 🟡 10), and
`test_the_checker_asks_git_for_nothing` pins the boundary between the two.

Four things this file holds, in the order they can go wrong:

  the anchor resolves   a symbol via `ast`, a quoted line otherwise, and an
                        ambiguous anchor is BROKEN rather than a guess
  the hash notices      a change inside the region drifts; a change that only
                        moves the region does not
  the region is right   a markdown heading owns its section, a comment does
                        not own the file, indentation is content
  the verdicts hold     and each is reachable, so none of them is decoration
"""

import importlib.util
import os
import re
import stat
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def load():
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load()


def run(args, cwd):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


SERVICE = (
    "import os\n"
    "\n"
    "\n"
    "def handler(x):\n"
    "    y = x + 1\n"
    "    return y\n"
    "\n"
    "\n"
    "class Box:\n"
    "    def open(self):\n"
    "        return 1\n"
)


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / ".specseal" / "map").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE)
    return d


def write_row(repo, path, anchor):
    """A ledger row citing `path#anchor` at the content it holds right now."""
    body = (repo / path).read_text()
    places = ec.resolve(path, anchor, body)
    assert len(places) == 1, f"fixture anchor is not unique: {places}"
    a, b = places[0]
    h = ec.content_hash(body.splitlines()[a - 1 : b])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `{path}#{anchor}@{h}` |\n"
    )
    return (a, b)


# --- the anchor resolves ----------------------------------------------------


def test_a_symbol_anchor_resolves_through_ast(repo):
    assert ec.resolve("src/service.py", "handler", SERVICE) == [(4, 6)]
    assert ec.resolve("src/service.py", "Box", SERVICE) == [(9, 11)]
    assert ec.resolve("src/service.py", "Box.open", SERVICE) == [(10, 11)]


def test_a_decorator_is_part_of_the_span(repo):
    """A decorator carries behaviour. A row anchored to the function it wraps
    has to notice one being added, so the span starts at the decorator."""
    text = "import functools\n\n\n@functools.cache\ndef f():\n    return 1\n"
    assert ec.resolve("x.py", "f", text) == [(4, 6)]


def test_a_file_that_will_not_parse_yields_no_symbols(repo):
    """The row then falls to the text rule rather than a false OK.

    None, not `{}`: the two callers diverge on exactly this. A file that
    cannot be parsed falls back to the generic rule; a file that parses and
    simply lacks the symbol is BROKEN — conflating them anchored rows to
    leftover call sites (round 4, 🔴 2)."""
    assert ec.py_spans("def broken(:\n") is None


def test_an_ambiguous_anchor_is_broken_and_says_where(repo):
    """Two places to look is not a measurement. Reporting OK would be a claim
    about whichever one the code happened to reach first."""
    (repo / "notes.md").write_text("same line\n\nmiddle\n\nsame line\n")
    (repo / ".specseal" / "map" / "f.md").write_text(
        '# frag\n\n| CLAUSE | `notes.md#"same line"@00000000` |\n'
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "ambiguous" in r.stdout, r.stdout
    assert "2 places" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_a_missing_anchor_is_broken(repo):
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(SERVICE.replace("def handler", "def gone"))
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "locator not found" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


# --- the hash notices -------------------------------------------------------


def test_a_change_inside_the_region_drifts(repo):
    write_row(repo, "src/service.py", "handler")
    assert "1 ok" in run(["."], str(repo)).stdout
    (repo / "src" / "service.py").write_text(SERVICE.replace("x + 1", "x + 2"))
    r = run(["."], str(repo))
    assert "1 drifted" in r.stdout, r.stdout
    assert r.returncode == 1, r.stdout


def test_moving_the_region_does_not_drift_it(repo):
    """What the line-number scheme got wrong, and the reason for the change.

    Inserting a line above a cited region moved every coordinate below it, so
    the row pointed at the wrong lines while still reading OK. Here the row
    reads OK because the CONTENT is untouched, and the region it prints is the
    current one.
    """
    before = write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text("# inserted at the top\n" + SERVICE)
    r = run(["."], str(repo))
    assert "1 ok" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout
    after = ec.resolve(
        "src/service.py", "handler", (repo / "src" / "service.py").read_text()
    )
    assert after == [(before[0] + 1, before[1] + 1)], after


def test_the_hash_ignores_trailing_whitespace_and_blank_lines(repo):
    a = ["def f():", "    return 1"]
    b = ["def f():   ", "", "    return 1\t"]
    assert ec.content_hash(a) == ec.content_hash(b)


def test_the_hash_does_not_ignore_indentation(repo):
    """Indentation is content in Python — a dedent moves a statement out of the
    block it belonged to. A hash that normalised it away would go quiet exactly
    where the edit matters most, which is the failure this repository has
    called a finding in every round of this branch."""
    inside = ["def f():", "    if x:", "        go()"]
    outside = ["def f():", "    if x:", "    go()"]
    assert ec.content_hash(inside) != ec.content_hash(outside)


# --- the region is right ----------------------------------------------------


def test_a_markdown_heading_owns_its_section(repo):
    """Down to the next heading at its level OR ABOVE — a DEEPER one is part
    of the section, not the end of it.

    The level comparison survived a mutation to `k is not None` because this
    case had no nested heading to tell the two apart. Found by mutating, which
    is the only way a fixture's blind spot shows.
    """
    text = (
        "# Top\n\nintro\n\n## A\n\nbody of A\n\n"
        "### A1\n\nnested body\n\n## B\n\nbody of B\n"
    )
    assert ec.resolve("d.md", '"## A"', text) == [(5, 12)]
    assert ec.resolve("d.md", '"### A1"', text) == [(9, 12)]
    assert ec.resolve("d.md", '"# Top"', text) == [(1, 15)]  # nothing above it


def test_a_hash_in_python_is_a_comment_not_a_heading(repo):
    """Found by migrating this repository's own ledger rather than by
    reasoning: a 23-line comment block resolved to its first line alone,
    because `#` was read as a markdown heading. The heading rule is
    markdown-only, and a comment block is an ordinary contiguous run."""
    text = "x = 0\n\n# comment one\n# comment two\n# comment three\nVOCAB = 1\n"
    # In Python the run is a comment block plus the statement it introduces.
    assert ec.resolve("s.py", '"# comment one"', text) == [(3, 6)]
    # The same bytes in markdown ARE three H1 headings, so the first owns only
    # itself. That contrast is the whole point: the file type decides.
    assert ec.resolve("s.md", '"# comment one"', text) == [(3, 3)]


def test_a_text_anchor_owns_its_contiguous_block(repo):
    text = "one\ntwo\nthree\n\nfar away\n"
    assert ec.resolve("d.txt", '"two"', text) == [(1, 3)]


def test_an_escaped_pipe_matches_a_real_one(repo):
    """A row anchored to a markdown table line has to escape its pipes or it
    splits the table it lives in. The checker unescapes before matching."""
    assert ec.unescape("a \\| b") == "a | b"
    text = "| Target SHA | value |\n"
    assert ec.resolve("t.md", '"| Target SHA | value |"', text) == [(1, 1)]


# --- two levels: a major unit and an optional minor anchor -----------------


BRACE = (
    "export const OTHER = 1;\n"
    "\n"
    "export function handler(input: string): number {\n"
    "  const y = input.length;\n"
    "  if (y > 3) {\n"
    "    return y;\n"
    "  }\n"
    "  return 0;\n"
    "}\n"
    "\n"
    "class Box {\n"
    "  open(): number {\n"
    "    return 1;\n"
    "  }\n"
    "}\n"
)


def test_the_major_unit_resolves_without_a_parser(repo):
    """`ast` exists for `.py` only, and a project adopting this skill is mostly
    code that is not Python. Falling back to text anchors there would hand
    those projects the brittle version of this design.

    The rule needs no parser and no dependency: the name followed by `(`, `{`
    or `:`, then the block to the next line at the same or lower indentation.
    That closes a suite in an indentation language and lands on the closing
    brace in a brace language, because the brace sits at the declaration's own
    indent.
    """
    assert ec.resolve("svc.ts", "handler", BRACE) == [(3, 8)]
    assert ec.resolve("svc.ts", "Box", BRACE) == [(11, 14)]
    assert ec.resolve("svc.ts", "open", BRACE) == [(12, 13)]


def test_a_unit_the_generic_rule_cannot_find_is_broken(repo):
    """Loud and honest beats a per-language parser nobody maintains."""
    assert ec.resolve("svc.ts", "missing", BRACE) == []
    (repo / "svc.ts").write_text(BRACE)
    (repo / ".specseal" / "map" / "f.md").write_text(
        "# frag\n\n| CLAUSE | `svc.ts#missing@00000000` |\n"
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "locator not found" in r.stdout, r.stdout
    assert r.returncode == 2


def test_a_brace_language_unit_drifts_on_a_change_inside_it(repo):
    (repo / "svc.ts").write_text(BRACE)
    h = ec.content_hash(BRACE.splitlines()[2:8])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `svc.ts#handler@{h}` |\n"
    )
    assert "1 ok" in run(["."], str(repo)).stdout
    (repo / "svc.ts").write_text(BRACE.replace("y > 3", "y > 4"))
    r = run(["."], str(repo))
    assert "1 drifted" in r.stdout and r.returncode == 1, r.stdout


def test_a_minor_anchor_that_matches_several_places_widens(repo):
    """Several matches is not a place, so it widens like a stale one rather
    than becoming a second way to report BROKEN.

    `y` is both assigned and returned inside `handler`, which is two innermost
    statements.
    """
    assert ec.minor_region("src/service.py", SERVICE, (4, 6), "y") == []


def test_a_stale_minor_anchor_widens_to_drifted_rather_than_broken(repo):
    """The joining rule, and the property this design turns on.

    BROKEN says *I cannot find it, go edit the ledger* — the bookkeeping this
    redesign removes. DRIFTED says *it changed, go re-read the claim* — the
    work the ledger exists for. A minor anchor that stopped matching means
    that place changed, so the row widens to its unit and reports DRIFTED.
    """
    body = (repo / "src" / "service.py").read_text()
    inside = ec.minor_region("src/service.py", body, (4, 6), '"y = x + 1"')
    a, b = inside[0]
    h = ec.content_hash(body.splitlines()[a - 1 : b])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f'# frag\n\n| CLAUSE | `src/service.py#handler>"y = x + 1"@{h}` |\n'
    )
    assert "1 ok" in run(["."], str(repo)).stdout

    # The anchored statement is gone entirely.
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("    y = x + 1\n    return y", "    return x + 1")
    )
    r = run(["."], str(repo))
    assert "BROKEN" not in r.stdout, (
        f"a stale minor anchor reported BROKEN, which sends someone to edit "
        f"the ledger:\n{r.stdout}"
    )
    assert "DRIFTED" in r.stdout and "anchored statement is gone" in r.stdout, r.stdout
    assert r.returncode == 1, r.stdout


def test_widening_does_not_swallow_a_real_broken(repo):
    """The failure mode of the widening: if the UNIT is also gone, the row
    must still be BROKEN. A widen that answered DRIFTED for a deleted function
    would report `go re-read` about something nobody can open."""
    body = (repo / "src" / "service.py").read_text()
    inside = ec.minor_region("src/service.py", body, (4, 6), '"y = x + 1"')
    a, b = inside[0]
    h = ec.content_hash(body.splitlines()[a - 1 : b])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f'# frag\n\n| CLAUSE | `src/service.py#handler>"y = x + 1"@{h}` |\n'
    )
    (repo / "src" / "service.py").write_text(SERVICE.replace("def handler", "def gone"))
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "locator not found" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_a_minor_anchor_is_resolved_by_what_it_references(repo):
    """Not by the characters of its line. Renaming a local on that line then
    changes nothing; renaming the thing it calls does, and widening to the
    unit with a DRIFTED is the right answer there too."""
    text = (
        "def f(a):\n    # compute the total\n    total = compute(a)\n    return total\n"
    )
    # The comment names `compute` too, so a character search finds two places
    # and a reference search finds the one statement that actually calls it.
    # That difference is what this case exists to hold: found by mutation,
    # because a fixture without the comment passes either way.
    assert ec.minor_region("x.py", text, (1, 4), "compute") == [(3, 3)]
    assert ec.literal_statements(text.splitlines(), (1, 4), "compute") != [(3, 3)]

    renamed = text.replace("total", "sum_")
    assert ec.minor_region("x.py", renamed, (1, 4), "compute") == [(3, 3)], (
        "renaming a local broke a minor anchor that names what it calls"
    )


def test_a_markdown_locator_is_a_heading_path(repo):
    """A sentence anchor breaks on any rewording. A heading is the document's
    own structure and survives the prose beneath being rewritten."""
    text = "# Top\n\n## A\n\nbody\n\n### Deep\n\nmore\n\n## B\n\nlast\n"
    # A section runs to the line before the next heading at its level or
    # above, trailing blank included — the hash normalises blanks away.
    assert ec.resolve("d.md", '"## A"', text) == [(3, 10)]
    assert ec.resolve("d.md", '"## A / ### Deep"', text) == [(7, 10)]


def test_only_a_real_heading_opens_a_section(repo):
    """A line with the same text that is NOT a heading must not match.

    Found by mutation: treating any matching line as a level-1 heading left
    every heading case green, because no fixture had a look-alike line.
    """
    # An INDENTED `## B` — inside a code block or a list — normalises to the
    # same text as the heading but is not one. That is the case the guard is
    # for, and a look-alike that differs in text never reaches it.
    text = "## A\n\n    ## B\n\n## B\n\nreal\n"
    assert ec.heading_level("    ## B") is None
    assert ec.resolve("d.md", '"## B"', text) == [(5, 7)]


def test_the_generic_rule_needs_a_declaration_not_a_mention(repo):
    """`handler(x)` called somewhere is not `handler`'s declaration.

    Found by mutation: dropping the `(`/`{`/`:` requirement left every brace
    case green, because no fixture mentioned a name away from its declaration.
    """
    text = (
        "// handler is described here\n"
        "const r = handler(1);\n"
        "\n"
        "function handler(x) {\n"
        "  return x;\n"
        "}\n"
    )
    # `const r = handler(1);` is a CALL: what precedes the name contains `=`,
    # so it is not a declaration line. The region stops AT the closing brace
    # rather than including it — the brace sits at the declaration's own
    # indent and carries no claim.
    assert ec.resolve("svc.js", "handler", text) == [(4, 5)]
    plain = "// handler is described here\n\nfunction handler(x) {\n  return x;\n}\n"
    assert ec.resolve("svc.js", "handler", plain) == [(3, 4)], (
        "a bare mention in a comment was read as a declaration"
    )


def test_a_constant_is_a_unit_too(repo):
    """A module-level constant has no `def` to hang on, and citing one is
    common — this plugin's own ledger cites three. Without `=` in the
    declaration rule every constant in every adopting project falls to a
    literal text anchor, which is the brittle form the rule exists to avoid.

    The colon is stricter than the other delimiters for the reason measured
    here: `if review not in REVIEW_ANSWERS:` ends in a colon and is a USE, so
    a colon only declares when the name opens the line.
    """
    text = (
        "OTHER = 0\n"
        "\n"
        "REVIEW_ANSWERS = (\n"
        "    CHAIN,\n"
        "    DIRECT,\n"
        ")\n"
        "\n"
        "def check(review):\n"
        "    if review not in REVIEW_ANSWERS:\n"
        "        return None\n"
    )
    # (3, 6), closing paren included: since round 4's 🔴 2 a parsing `.py`
    # never falls to the generic rule, and `ast` spans the whole assignment
    # statement. The generic rule still stops before the paren — that half of
    # the pin lives in the `.ts` fixture above.
    assert ec.resolve("r.py", "REVIEW_ANSWERS", text) == [(3, 6)]
    # A YAML key is the same shape, and there the colon DOES declare.
    assert ec.resolve("c.yml", "jobs", "name: x\njobs:\n  a: 1\n  b: 2\nz: 3\n") == [
        (2, 4)
    ]


def test_a_repeated_heading_is_disambiguated_by_its_parent(repo):
    """Rather than by a line number, which is the thing being removed."""
    text = "## A\n\n### Same\n\none\n\n## B\n\n### Same\n\ntwo\n"
    assert len(ec.resolve("d.md", '"### Same"', text)) == 2
    assert ec.resolve("d.md", '"## B / ### Same"', text) == [(9, 11)]


# --- the rename hint ---------------------------------------------------------


def test_a_renamed_unit_is_named_in_the_broken_report(repo):
    """The checker already computed every unit's span; when a locator is gone
    and exactly one other unit carries the row's RECORDED hash, say so. The
    verdict stays BROKEN and the exit code stays 2 — the row still needs a
    person, this hands them the answer.
    """
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler(", "def total_price(")
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "locator not found" in r.stdout, r.stdout
    assert "identical content at #total_price" in r.stdout, r.stdout
    assert "renamed?" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_renamed_and_edited_prints_no_hint(repo):
    """The comparison is on the RECORDED hash, never a recomputed one. If the
    content changed AND moved there is nothing trustworthy to point at, and
    the plain BROKEN is the honest answer."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler(", "def total_price(").replace("x + 1", "x + 2")
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "locator not found" in r.stdout, r.stdout
    assert "identical content" not in r.stdout, (
        f"a hint was printed for content that also changed:\n{r.stdout}"
    )
    assert r.returncode == 2, r.stdout


def test_two_identical_units_are_counted_not_named(repo):
    """A guess is not a measurement. With two units holding the recorded
    content, the report says how many and names none."""
    twin = "def alpha(x):\n    return x + 1\n\n\ndef beta(x):\n    return x + 1\n"
    (repo / "src" / "twin.py").write_text(twin)
    # The row records what a `gamma` unit WOULD hash to: reconstruction
    # substitutes each candidate's name with the locator before comparing,
    # so both alpha and beta reconstruct to exactly this.
    h = ec.content_hash(["def gamma(x):", "    return x + 1"])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `src/twin.py#gamma@{h}` |\n"
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "locator not found" in r.stdout, r.stdout
    assert "identical content at 2 units" in r.stdout, r.stdout
    assert "#alpha" not in r.stdout and "#beta" not in r.stdout, (
        f"one of the two was named, which is a guess:\n{r.stdout}"
    )
    assert r.returncode == 2, r.stdout


def test_a_renamed_markdown_heading_is_named_too(repo):
    """The same machinery covers a document: a section whose heading was
    renamed still holds the recorded content."""
    doc = "## Old name\n\nthe body stays put\n"
    (repo / "notes.md").write_text(doc)
    h = ec.content_hash(doc.splitlines())
    (repo / ".specseal" / "map" / "f.md").write_text(
        f'# frag\n\n| CLAUSE | `notes.md#"## Old name"@{h}` |\n'
    )
    assert "1 ok" in run(["."], str(repo)).stdout
    (repo / "notes.md").write_text(doc.replace("## Old name", "## New name"))
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout, r.stdout
    assert 'identical content at #"## New name"' in r.stdout, r.stdout


def test_reverify_re_anchors_a_row_whose_content_provably_moved(repo):
    """The hint's condition is strong enough to fix, not just to point.

    Exactly one unit carrying the row's RECORDED hash is a proof the content
    moved intact — deterministic, no guess — so `--reverify` rewrites the
    locator and leaves the hash alone, identical content being the
    precondition. The plain check keeps printing BROKEN with the hint:
    reading never rewrites.
    """
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler(", "def total_price(")
    )
    ledger = repo / ".specseal" / "map" / "f.md"
    before = ledger.read_text()
    assert run(["."], str(repo)).returncode == 2
    assert ledger.read_text() == before, "the plain check rewrote the ledger"

    r = run(["--reverify", "."], str(repo))
    assert "#handler -> #total_price" in r.stdout, r.stdout
    after = ledger.read_text()
    assert "#total_price@" in after and "#handler@" not in after, after
    # The hash follows the locator. It cannot stay: the name is part of the
    # unit's own hashed region, so the recorded hash is of the OLD spelling
    # and keeping it would leave the re-anchored row DRIFTED with nothing to
    # re-read — this assertion held the first version of the feature red.
    assert after.split("@")[1][:8] != before.split("@")[1][:8]
    assert run(["."], str(repo)).returncode == 0, "the re-anchored row is not OK"


def test_reverify_does_not_touch_a_renamed_and_edited_row(repo):
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler(", "def total_price(").replace("x + 1", "x + 2")
    )
    ledger = repo / ".specseal" / "map" / "f.md"
    before = ledger.read_text()
    r = run(["--reverify", "."], str(repo))
    assert "0 rows re-verified" in r.stdout, r.stdout
    assert ledger.read_text() == before, "an unprovable move was rewritten"
    assert run(["."], str(repo)).returncode == 2


def test_reverify_does_not_choose_between_two_identical_units(repo):
    twin = "def alpha(x):\n    return x + 1\n\n\ndef beta(x):\n    return x + 1\n"
    (repo / "src" / "twin.py").write_text(twin)
    h = ec.content_hash(["def gamma(x):", "    return x + 1"])
    ledger = repo / ".specseal" / "map" / "f.md"
    ledger.write_text(f"# frag\n\n| CLAUSE | `src/twin.py#gamma@{h}` |\n")
    before = ledger.read_text()
    run(["--reverify", "."], str(repo))
    assert ledger.read_text() == before, "reverify picked one of two matches"


def test_a_move_to_another_file_is_named_with_its_path(repo):
    """hash AND name matching in another file proves the unit moved intact."""
    write_row(repo, "src/service.py", "handler")
    body = (repo / "src" / "service.py").read_text()
    (repo / "src" / "service.py").write_text(
        body.replace(SERVICE[: SERVICE.index("class")], "import os\n")
    )
    (repo / "src" / "moved.py").write_text(
        "def handler(x):\n    y = x + 1\n    return y\n"
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout, r.stdout
    assert "identical content at src/moved.py#handler (moved?)" in r.stdout, r.stdout

    rr = run(["--reverify", "."], str(repo))
    assert "src/service.py#handler -> src/moved.py#handler" in rr.stdout, rr.stdout
    ledger = (repo / ".specseal" / "map" / "f.md").read_text()
    assert "`src/moved.py#handler@" in ledger, ledger
    assert run(["."], str(repo)).returncode == 0, run(["."], str(repo)).stdout


def test_renamed_and_moved_is_still_provable_by_content(repo):
    """hash alone, unique across the scan — content identity is the proof,
    the same as the same-file rename."""
    write_row(repo, "src/service.py", "handler")
    body = (repo / "src" / "service.py").read_text()
    (repo / "src" / "service.py").write_text(
        body.replace(SERVICE[: SERVICE.index("class")], "import os\n")
    )
    (repo / "src" / "moved.py").write_text(
        "def total_price(x):\n    y = x + 1\n    return y\n"
    )
    r = run(["."], str(repo))
    assert "identical content at src/moved.py#total_price (renamed?)" in r.stdout, (
        r.stdout
    )
    rr = run(["--reverify", "."], str(repo))
    assert "-> src/moved.py#total_price" in rr.stdout, rr.stdout
    assert run(["."], str(repo)).returncode == 0


def test_a_name_alone_is_a_labelled_fact_and_never_a_fix(repo):
    """`main`, `resolve`, `check` collide across files as a matter of course.
    Content differing means the checker does not know it is a rename, so it
    says exactly what it measured and touches nothing."""
    write_row(repo, "src/service.py", "handler")
    body = (repo / "src" / "service.py").read_text()
    (repo / "src" / "service.py").write_text(
        body.replace(SERVICE[: SERVICE.index("class")], "import os\n")
    )
    (repo / "src" / "other.py").write_text("def handler(x):\n    return x * 99\n")
    r = run(["."], str(repo))
    assert "same name at src/other.py (content differs)" in r.stdout, r.stdout
    assert "renamed" not in r.stdout, r.stdout

    ledger = repo / ".specseal" / "map" / "f.md"
    before = ledger.read_text()
    rr = run(["--reverify", "."], str(repo))
    assert "0 rows re-verified" in rr.stdout, rr.stdout
    assert ledger.read_text() == before, "a name-alone match was rewritten"


def test_a_hash_match_outranks_a_name_alone_match(repo):
    """The grade order. When content identity proves where the unit went, a
    name collision elsewhere is noise and must not be reported."""
    write_row(repo, "src/service.py", "handler")
    body = (repo / "src" / "service.py").read_text()
    (repo / "src" / "service.py").write_text(
        body.replace(SERVICE[: SERVICE.index("class")], "import os\n")
    )
    (repo / "src" / "moved.py").write_text(
        "def total_price(x):\n    y = x + 1\n    return y\n"
    )
    (repo / "src" / "decoy.py").write_text("def handler(x):\n    return x * 99\n")
    r = run(["."], str(repo))
    assert "identical content at src/moved.py#total_price" in r.stdout, r.stdout
    assert "same name at" not in r.stdout, (
        f"a name-alone line was printed although the hash match decides:\n{r.stdout}"
    )


def test_the_same_unit_in_two_files_is_counted_not_rewritten(repo):
    """Same name AND identical content in two files: two units, no names, no
    rewrite. Uniqueness is judged across the whole scan."""
    write_row(repo, "src/service.py", "handler")
    body = (repo / "src" / "service.py").read_text()
    (repo / "src" / "service.py").write_text(
        body.replace(SERVICE[: SERVICE.index("class")], "import os\n")
    )
    unit = "def handler(x):\n    y = x + 1\n    return y\n"
    (repo / "src" / "a.py").write_text(unit)
    (repo / "src" / "b.py").write_text(unit)
    r = run(["."], str(repo))
    assert "identical content at 2 units" in r.stdout, r.stdout
    ledger = repo / ".specseal" / "map" / "f.md"
    before = ledger.read_text()
    run(["--reverify", "."], str(repo))
    assert ledger.read_text() == before, "reverify picked one of two files"


def test_a_whole_file_rename_heals_mechanically(repo):
    """Every row on the old path goes BROKEN, and each finds its unit in the
    new file by hash and name. This replaces the old known limit that a file
    rename was a by-hand search-and-replace on the ledger."""
    body = (repo / "src" / "service.py").read_text()
    h1 = ec.content_hash(body.splitlines()[3:6])
    h2 = ec.content_hash(body.splitlines()[8:11])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| A | `src/service.py#handler@{h1}` |\n"
        f"| B | `src/service.py#Box@{h2}` |\n"
    )
    (repo / "src" / "renamed.py").write_text(body)
    (repo / "src" / "service.py").unlink()

    before = run(["."], str(repo))
    assert before.returncode == 2
    # The hint fires from the FILE-not-found branch, which is its own path:
    # the row's file is gone entirely, not just its locator. Found by
    # mutation — nothing else pinned this branch's scan.
    assert "identical content at src/renamed.py#handler (moved?)" in before.stdout, (
        before.stdout
    )
    rr = run(["--reverify", "."], str(repo))
    assert "2 rows re-verified" in rr.stdout, rr.stdout
    after = run(["."], str(repo))
    assert after.returncode == 0, after.stdout
    assert "2 ok" in after.stdout, after.stdout


def test_past_the_file_cap_the_scan_degrades_and_says_so(repo):
    """The clean path stays the 114 ms tool; the broken path stays bounded.
    Past the cap the scan degrades to the row's own file and the line says
    so, because a silently narrowed search reads as a search that found
    nothing."""
    write_row(repo, "src/service.py", "handler")
    body = (repo / "src" / "service.py").read_text()
    (repo / "src" / "service.py").write_text(
        body.replace(SERVICE[: SERVICE.index("class")], "import os\n")
    )
    (repo / "src" / "moved.py").write_text(
        "def handler(x):\n    y = x + 1\n    return y\n"
    )
    # `zfiller` sorts AFTER `src`, so the match sits inside the first
    # SCAN_FILE_CAP files the walk meets. A mutant that fills the list past
    # the cap but ignores the capped flag would therefore still find it —
    # which is exactly what has to go red. Found by mutation: with the filler
    # walked first, the truncation itself hid the match and the flag was
    # never load-bearing.
    (repo / "zfiller").mkdir()
    for i in range(ec.SCAN_FILE_CAP + 1):
        (repo / "zfiller" / f"f{i:04}.py").write_text("pass\n")
    r = run(["."], str(repo))
    assert "repo-wide scan skipped" in r.stdout, r.stdout
    assert "moved.py" not in r.stdout, (
        f"the scan found a cross-file match past the cap:\n{r.stdout}"
    )


# --- the 0.1.0 format ---------------------------------------------------------


OLD_LEDGER = (
    "# map\n\n"
    "| Baseline commit | `9829412277fa11f81b61df7850183ae3fa9d8a05` (2026-08-31) |\n\n"
    "| CLAUSE | `src/service.py:4-6` | read | 2026-08-31 `9829412` | notes |\n"
    "| OTHER | `src/service.py:10-11` | read | 2026-08-31 | notes |\n"
)


def test_an_old_format_ledger_is_loud_never_invisible(repo):
    """The release blocker, pinned as it was measured: a 0.1.0 ledger —
    `path:line` coordinates, `date \`sha\`` stamps — read `0 ok · 0 drifted ·
    0 broken`, exit 0. Every row silently ignored, green light. A user
    updating the plugin lost their whole ledger's coverage without one
    printed word — quiet-where-it-used-to-complain, aimed at every adopting
    repository at once.

    An old-format row gets its own verdict and FAILS the run, `--strict` or
    not: a red build saying "run the migrator" beats a green build checking
    nothing.
    """
    (repo / ".specseal" / "map" / "f.md").write_text(OLD_LEDGER)
    r = run(["."], str(repo))
    assert "OLD-FORMAT" in r.stdout, f"today's silent pass, verbatim:\n{r.stdout}"
    assert "src/service.py:4-6" in r.stdout, r.stdout
    assert "--migrate" in r.stdout, "the report does not name the remedy"
    assert r.returncode == 2, r.stdout


def test_the_pre_0_2_address_is_covered_too(repo):
    """`docs/**/_evidence.md` is read by the same globs and carries the same
    old rows."""
    d = repo / "docs" / "policies" / "demo"
    d.mkdir(parents=True)
    (d / "_evidence.md").write_text(OLD_LEDGER)
    r = run(["."], str(repo))
    assert "OLD-FORMAT" in r.stdout and r.returncode == 2, r.stdout


def test_a_quoted_anchor_naming_an_old_coordinate_is_not_old_format(repo):
    """A text locator may legitimately quote a line that contains `file.py:12`.
    New-format anchors are blanked before the old-format scan, or such a row
    would read OLD-FORMAT forever with nothing for the migrator to fix."""
    (repo / "notes.md").write_text("the row cited hooks/gate.py:12 back then\n")
    body = (repo / "notes.md").read_text()
    h = ec.content_hash(body.splitlines())
    (repo / ".specseal" / "map" / "f.md").write_text(
        f'# frag\n\n| CLAUSE | `notes.md#"the row cited hooks/gate.py:12 back then"@{h}` |\n'
    )
    r = run(["."], str(repo))
    assert "OLD-FORMAT" not in r.stdout, r.stdout
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_migrate_rewrites_an_old_row_to_its_enclosing_unit(repo):
    (repo / ".specseal" / "map" / "f.md").write_text(OLD_LEDGER)
    r = run(["--migrate", "."], str(repo))
    assert "2 rows migrated" in r.stdout, r.stdout
    after = (repo / ".specseal" / "map" / "f.md").read_text()
    assert "src/service.py#handler@" in after, after
    assert "src/service.py#Box.open@" in after, after
    assert "src/service.py:4-6" not in after, after
    # The stamp drops, the date stays.
    assert "2026-08-31 `9829412`" not in after, after
    assert "2026-08-31" in after, after
    check = run(["."], str(repo))
    assert check.returncode == 0 and "2 ok" in check.stdout, check.stdout


def test_migrate_leaves_what_it_cannot_prove_and_says_why(repo):
    """Beyond EOF, a file that is gone — LEFT and reported, never guessed."""
    (repo / ".specseal" / "map" / "f.md").write_text(
        "# map\n\n"
        "| A | `src/service.py:999` | | 2026-08-31 |\n"
        "| B | `src/gone.py:3` | | 2026-08-31 |\n"
    )
    r = run(["--migrate", "."], str(repo))
    assert "0 rows migrated" in r.stdout and "2 left" in r.stdout, r.stdout
    assert "src/service.py:999" in r.stdout, r.stdout
    assert "src/gone.py:3" in r.stdout, r.stdout
    # Left rows keep failing the plain check, so the loop closes on a person.
    assert run(["."], str(repo)).returncode == 2


def test_a_row_migrate_can_only_half_prove_is_left_whole(repo):
    """All-or-nothing per row. One coordinate resolvable and one not: a
    partial rewrite would strand half a cell in each format and drop the
    stamp off a row that still fails — the report stays per-row readable, and
    the row stays exactly as the person left it. Found by mutation: no
    fixture carried two coordinates in one row."""
    row = "| X | `src/service.py:5` and `src/gone.py:2` | 2026-08-31 `9829412` |\n"
    (repo / ".specseal" / "map" / "f.md").write_text("# map\n\n" + row)
    r = run(["--migrate", "."], str(repo))
    assert "1 left" in r.stdout, r.stdout
    after = (repo / ".specseal" / "map" / "f.md").read_text()
    assert row in after, f"the row was partly rewritten:\n{after}"


def test_migrate_twice_is_a_no_op(repo):
    (repo / ".specseal" / "map" / "f.md").write_text(OLD_LEDGER)
    run(["--migrate", "."], str(repo))
    once = (repo / ".specseal" / "map" / "f.md").read_text()
    r = run(["--migrate", "."], str(repo))
    assert "0 rows migrated" in r.stdout, r.stdout
    assert (repo / ".specseal" / "map" / "f.md").read_text() == once


# --- the verdicts -----------------------------------------------------------


def test_a_missing_file_is_broken_not_external(repo):
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").unlink()
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "file not found" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_a_cross_repo_path_is_external_without_a_map(repo):
    """EXTERNAL is a claim about another repository, and only declared intent
    — a parity config, `--map`, `--default-repo` — says this project has one.
    Without the declaration this read EXTERNAL too, which made deleting a
    directory a green build (round 4, 🔴 3)."""
    (repo / ".specseal" / "parity.md").write_text("# parity\n")
    (repo / ".specseal" / "map" / "f.md").write_text(
        "# frag\n\n| CLAUSE | `legacy/src/old.py#handler@00000000` |\n"
    )
    r = run(["."], str(repo))
    assert "EXTERNAL" in r.stdout, r.stdout
    assert r.returncode == 0, "EXTERNAL is exempt from the failing codes"


def test_a_mapped_cross_repo_row_is_checked_like_any_other(repo, tmp_path):
    """Round 2's 🟡 6 cannot recur: there is no baseline for a cross-repo row
    to be missing, so it needs no second header and reads like a local one."""
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    (other / "src" / "old.py").write_text(SERVICE)
    h = ec.content_hash(SERVICE.splitlines()[3:6])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `legacy/src/old.py#handler@{h}` |\n"
    )
    r = run(["--map", f"legacy={other}", "."], str(repo))
    assert "1 ok" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout


def test_strict_turns_drift_into_the_broken_code(repo):
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(SERVICE.replace("x + 1", "x + 2"))
    assert run(["."], str(repo)).returncode == 1
    assert run(["--strict", "."], str(repo)).returncode == 2


def test_an_ok_row_prints_the_regions_current_lines(repo):
    """The line number is an output for a reader to open, never an input. It
    is what the row citing a symbol gives up nothing to have."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text("# inserted\n" + SERVICE)
    r = run(["."], str(repo))
    assert "1 ok" in r.stdout
    findings = ec.check_ledger(
        str(repo / ".specseal" / "map" / "f.md"), str(repo), {}, None
    )
    assert findings == [("OK", "src/service.py#handler", "5-7")], findings


# --- re-verifying -----------------------------------------------------------


def test_reverify_rewrites_a_drifted_hash_and_says_so(repo):
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(SERVICE.replace("x + 1", "x + 2"))
    assert run(["."], str(repo)).returncode == 1
    r = run(["--reverify", "."], str(repo))
    assert "1 row re-verified" in r.stdout, r.stdout
    assert "->" in r.stdout, "the rewrite did not name what it changed"
    assert run(["."], str(repo)).returncode == 0


def test_the_check_never_rewrites_on_its_own(repo):
    """A check that refreshed what it was checking would report OK forever.
    Re-verifying is a person saying they re-read the code, so it is a separate
    command and the ordinary run must leave the file alone."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(SERVICE.replace("x + 1", "x + 2"))
    ledger = repo / ".specseal" / "map" / "f.md"
    before = ledger.read_text()
    run(["."], str(repo))
    run(["--strict", "."], str(repo))
    assert ledger.read_text() == before, "the check rewrote the ledger"


def test_reverify_leaves_an_unresolvable_row_alone(repo):
    """It refreshes what it can see. A row whose unit is gone WITHOUT a
    provable move is a row somebody has to look at, and silently renaming its
    hash would hide it. The fixture edits the body as well as the name,
    because a pure rename is now provable and gets re-anchored instead."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler", "def gone").replace("x + 1", "x + 9")
    )
    ledger = repo / ".specseal" / "map" / "f.md"
    before = ledger.read_text()
    r = run(["--reverify", "."], str(repo))
    assert "0 rows re-verified" in r.stdout, r.stdout
    assert ledger.read_text() == before
    assert run(["."], str(repo)).returncode == 2


# --- this repository --------------------------------------------------------


def test_no_ledger_row_carries_a_line_number_or_a_commit(repo):
    """The point of the change, checked against the real ledgers.

    A `path:line` coordinate or a `<date> <sha>` stamp surviving anywhere means
    the mechanism came back — and both were what every rule this branch spent
    three review rounds on existed to manage.
    """
    import glob
    import re

    old_coord = re.compile(r"[A-Za-z0-9_./-]+\.(?:py|md|yml|yaml|sh|toml):\d+")
    stamp = re.compile(r"\b\d{4}-\d{2}-\d{2}\s+`?[0-9a-f]{7,40}`?")
    for path in sorted(
        glob.glob(os.path.join(ROOT, ".specseal", "map.md"))
        + glob.glob(os.path.join(ROOT, ".specseal", "map", "*.md"))
    ):
        for n, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
            if not line.strip().startswith("|"):
                continue
            rel = os.path.relpath(path, ROOT)
            assert not old_coord.search(line), f"{rel}:{n} cites a line number"
            assert not stamp.search(line), f"{rel}:{n} carries a commit stamp"


def test_the_checker_asks_git_for_nothing(repo):
    """The squash and rebase class is gone rather than handled: the CHECK
    path has no git to be wrong about.

    Round 4's 🟡 10 drew the boundary rather than moving it: no-git is the
    CHECKER's property, not a one-shot writer's. `--migrate` rewrites rows on
    the strength of line numbers recorded long ago, and the old stamp's
    commit is the only evidence that can say whether those numbers still mean
    anything — so git may appear in exactly two functions, `content_at` and
    `migrate`, and nowhere a plain check or a `--reverify` can reach.
    """
    import ast as ast_mod

    source = open(SCRIPT, encoding="utf-8").read()
    tree = ast_mod.parse(source)
    # Reaching for the tool means using `subprocess` (prose and messages may
    # say "git"; code may not run it). Only `content_at` may, and only
    # `migrate` may call `content_at` — a call from anywhere else would put
    # git back on a path a plain check or a --reverify can reach.
    reaching, calling = set(), set()
    for node in ast_mod.walk(tree):
        if not isinstance(node, (ast_mod.FunctionDef, ast_mod.AsyncFunctionDef)):
            continue
        for inner in ast_mod.walk(node):
            if isinstance(inner, ast_mod.Name) and inner.id == "subprocess":
                reaching.add(node.name)
            if (
                isinstance(inner, ast_mod.Call)
                and isinstance(inner.func, ast_mod.Name)
                and inner.func.id == "content_at"
            ):
                calling.add(node.name)
    assert reaching == {"content_at"}, (
        f"the check path reaches for the shell: {sorted(reaching)}"
    )
    assert calling <= {"migrate"}, (
        f"content_at is reachable outside --migrate: {sorted(calling)}"
    )
    # And the runtime proof: a plain check with no git on PATH still answers.
    write_row(repo, "src/service.py", "handler")
    r = subprocess.run(
        [sys.executable, SCRIPT, "."],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PATH": ""},
    )
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout + r.stderr


# --- round 4: the resolution and heal fixes ---------------------------------


def test_a_call_after_a_statement_keyword_is_not_a_declaration(repo):
    """`return render(y);` is the commonest shape in every brace language, and
    the rule read it as a second declaration of `render` — an ordinary
    one-declaration-one-call file was `BROKEN locator is ambiguous`, exit 2
    (round 4, 🔴 1). The existing mention pin covered `const r = handler(1);`,
    where the `=` already blocks the match; a statement keyword carries none.
    """
    text = (
        "function render(x) {\n"
        "  return x;\n"
        "}\n"
        "\n"
        "function page(y) {\n"
        "  return render(y);\n"
        "}\n"
    )
    assert ec.resolve("app.js", "render", text) == [(1, 2)]
    for kw in ("return", "throw", "yield", "await", "if", "while", "case", "not"):
        lines = ["function render(x) {", "  return x;", "}", "", f"{kw} render(y);"]
        assert ec.generic_units(lines, "render") == [(1, 2)], kw
    # Declaration modifiers are NOT statement keywords: nothing here narrows
    # what `export async function f(` and friends already match.
    decl = ["export async function render(x) {", "  return x;", "}"]
    assert ec.generic_units(decl, "render") == [(1, 2)]


def test_a_gone_symbol_in_a_parsing_python_file_is_broken_with_the_hint(repo):
    """`.py` fell back to the generic text rule whenever `ast` found no
    symbol — including when the parse SUCCEEDED and the unit is simply gone.
    A function moved out with a bare call left behind read DRIFTED, and
    `--reverify` then anchored the row to the call site permanently, with the
    true heal unreachable (round 4, 🔴 2). A successful parse means ast's
    answer is the whole answer."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        "import os\n\n\ndef caller(x):\n    handler(x)\n    return x\n"
    )
    (repo / "src" / "lib.py").write_text(
        "def handler(x):\n    y = x + 1\n    return y\n"
    )
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "DRIFTED" not in r.stdout, r.stdout
    assert "identical content at src/lib.py#handler (moved?)" in r.stdout, r.stdout
    rr = run(["--reverify", "."], str(repo))
    assert "src/service.py#handler -> src/lib.py#handler" in rr.stdout, rr.stdout
    ledger = (repo / ".specseal" / "map" / "f.md").read_text()
    assert "`src/lib.py#handler@" in ledger, ledger
    assert run(["."], str(repo)).returncode == 0


def test_a_syntax_error_still_falls_back_to_the_text_rule(repo):
    """The fallback survives for the one thing it was for: a file ast cannot
    read at all."""
    text = "def handler(x):\n    return x + 1\n\ndef broken(:\n"
    assert ec.py_spans(text) is None
    assert ec.resolve("bad.py", "handler", text) == [(1, 2)]


def test_a_module_constant_resolves_through_ast_in_a_parsing_file(repo):
    """Round 4's 🔴 2 fix must not cost the constants: with the generic
    fallback gone for parsing files, `ast` itself carries module- and
    class-level assignments — this repository's ledger cites three. A local
    assignment stays a local, not a unit."""
    text = (
        "LIMIT = 12\n"
        "\n"
        "\n"
        "class Cfg:\n"
        "    RETRIES = 3\n"
        "\n"
        "\n"
        "def use():\n"
        "    n = LIMIT\n"
        "    return n\n"
    )
    assert ec.resolve("c.py", "LIMIT", text) == [(1, 1)]
    assert ec.resolve("c.py", "Cfg.RETRIES", text) == [(5, 5)]
    assert ec.resolve("c.py", "n", text) == []
    assert ec.resolve("c.py", "use.n", text) == []


def test_a_renamed_directory_is_broken_with_the_hint_not_external(repo):
    """Renaming `pkg/` to `lib/` turned every row citing it EXTERNAL — "not
    in this repo; pass --map" — and `--strict` exited 0 while `--reverify`
    happily healed the same rows: two commands disagreeing about one row
    (round 4, 🔴 3). Without cross-repo intent declared anywhere, a missing
    file is a broken citation whatever directory it sat in, and the same
    scan that heals a renamed file heals a renamed directory."""
    (repo / "pkg").mkdir()
    (repo / "pkg" / "mod.py").write_text("def handler(x):\n    return x * 3\n")
    write_row(repo, "pkg/mod.py", "handler")
    (repo / "pkg").rename(repo / "lib")
    r = run(["."], str(repo))
    assert "EXTERNAL" not in r.stdout, r.stdout
    assert "BROKEN" in r.stdout and r.returncode == 2, r.stdout
    assert "identical content at lib/mod.py#handler (moved?)" in r.stdout, r.stdout
    rr = run(["--reverify", "."], str(repo))
    assert "-> lib/mod.py#handler" in rr.stdout, rr.stdout
    assert run(["."], str(repo)).returncode == 0


def test_a_deleted_directory_fails_the_build_without_cross_repo_intent(repo):
    """Deletion leaves nothing for the scan to find, so there is no hint —
    but the build goes red instead of green (round 4, 🔴 3)."""
    import shutil

    (repo / "pkg").mkdir()
    (repo / "pkg" / "mod.py").write_text("def handler(x):\n    return x * 3\n")
    write_row(repo, "pkg/mod.py", "handler")
    shutil.rmtree(repo / "pkg")
    r = run(["."], str(repo))
    assert "EXTERNAL" not in r.stdout, r.stdout
    assert "BROKEN" in r.stdout and "file not found" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_reverify_reads_default_repo(repo, tmp_path):
    """`reverify()` took `default_repo` and never read it: a migration
    ledger's drifted rows answered `0 rows re-verified`, silently (round 4,
    🔴 4)."""
    orig = tmp_path / "orig"
    (orig / "apps").mkdir(parents=True)
    (orig / "apps" / "svc.py").write_text("def handler(x):\n    return x + 1\n")
    (repo / ".specseal" / "map" / "f.md").write_text(
        "# frag\n\n| CLAUSE | `apps/svc.py#handler@00000000` |\n"
    )
    r = run(["--reverify", "--default-repo", str(orig), "."], str(repo))
    assert "1 row re-verified" in r.stdout, r.stdout
    check = run(["--default-repo", str(orig), "."], str(repo))
    assert "1 ok" in check.stdout and check.returncode == 0, check.stdout


def test_reverify_never_scans_this_repo_for_a_row_it_cannot_place(repo, tmp_path):
    """Worse than the dead parameter: the row's file was absent from root, so
    the graded scan searched THIS repository and re-anchored a cross-repo row
    onto a local unit whose content happened to reconstruct (round 4, 🔴 4).
    With intent declared and the file in neither checkout, there is no
    repository the scan can honestly search — so it searches none."""
    orig = tmp_path / "orig"
    orig.mkdir()
    h = ec.content_hash(["def fetch(x):", "    return x + 1"])
    (repo / "src" / "copycat.py").write_text("def grab(x):\n    return x + 1\n")
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `apps/svc.py#fetch@{h}` |\n"
    )
    before = (repo / ".specseal" / "map" / "f.md").read_text()
    r = run(["--reverify", "--default-repo", str(orig), "."], str(repo))
    assert "0 rows re-verified" in r.stdout, r.stdout
    assert (repo / ".specseal" / "map" / "f.md").read_text() == before
    check = run(["--default-repo", str(orig), "."], str(repo))
    assert "grab" not in check.stdout, check.stdout


def test_two_rows_at_one_coordinate_with_different_hashes_are_both_checked(repo):
    """The dedup key was the coordinate without the hash, so a second row
    citing the same unit at a different time — one of the two necessarily
    stale — was silently skipped: a two-row fixture read `1 ok`, exit 0
    (round 4, 🟡 5)."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / ".specseal" / "map" / "f.md"
    ledger.write_text(
        ledger.read_text() + "| STALE | `src/service.py#handler@00000000` |\n"
    )
    r = run(["."], str(repo))
    assert "1 ok" in r.stdout and "1 drifted" in r.stdout, r.stdout
    assert r.returncode == 1, r.stdout


def test_old_format_reaches_the_totals_line(repo):
    """The build failed red while the summary read all zeros (round 4, 🟡 6 —
    the totals half was measured here during the --migrate demo before the
    round reported it)."""
    (repo / ".specseal" / "map" / "f.md").write_text(OLD_LEDGER)
    r = run(["."], str(repo))
    # Both summary lines, pinned separately: the per-ledger counts and the
    # grand total each read all zeros before, and either one alone still
    # sends a reader hunting for why the build is red.
    assert "  0 ok · 0 drifted · 0 broken · 0 external · 2 old-format" in r.stdout, (
        r.stdout
    )
    assert (
        "total: 0 ok · 0 drifted · 0 broken · 0 external · 2 old-format" in r.stdout
    ), r.stdout
    assert r.returncode == 2, r.stdout


def test_a_heading_path_locator_still_gets_the_rename_hint(repo):
    """Reconstruction substituted the candidate's first line with the WHOLE
    locator string, but a heading path's recorded region starts at its LAST
    part's heading line — so the parent-qualified form the skill recommends
    was the one form that could never be healed (round 4, 🟡 8)."""
    doc = "## A\n\n### B\n\nbody stays put\n\n## C\n\ntail\n"
    (repo / "notes.md").write_text(doc)
    h = ec.content_hash(doc.splitlines()[2:6])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f'# frag\n\n| CLAUSE | `notes.md#"## A / ### B"@{h}` |\n'
    )
    assert "1 ok" in run(["."], str(repo)).stdout
    (repo / "notes.md").write_text(doc.replace("### B", "### D"))
    r = run(["."], str(repo))
    assert 'identical content at #"### D" (renamed?)' in r.stdout, r.stdout
    rr = run(["--reverify", "."], str(repo))
    assert '-> #"### D"' in rr.stdout, rr.stdout
    assert run(["."], str(repo)).returncode == 0


def test_a_failed_write_never_tears_the_ledger(repo, monkeypatch):
    """`--migrate` truncated the ledger and then wrote, so a crash mid-write
    left a torn file whose only recovery was the dirty guard's committed
    baseline. The write goes to a temp file and lands by rename: a crash
    leaves the old text in place (round 4, 🟡 14)."""
    import builtins

    ledger = repo / ".specseal" / "map" / "f.md"
    ledger.write_text(OLD_LEDGER)
    real_open = builtins.open

    class Refusing:
        def __init__(self, f):
            self.f = f

        def __enter__(self):
            return self

        def __exit__(self, *a):
            self.f.close()
            return False

        def write(self, s):
            raise OSError("disk full")

    def refusing_open(path, mode="r", *a, **k):
        if str(path) == str(ledger) and "w" in str(mode):
            return Refusing(real_open(path, mode, *a, **k))
        return real_open(path, mode, *a, **k)

    monkeypatch.setattr(builtins, "open", refusing_open)
    try:
        ec.migrate([str(ledger)], str(repo))
    except OSError:
        pass
    monkeypatch.undo()
    text = ledger.read_text()
    assert text == OLD_LEDGER or "#handler@" in text, f"torn ledger:\n{text!r}"


def test_an_unreadable_ledger_is_reported_not_a_traceback(repo):
    """A ledger `read()` returning None crashed `check_ledger`, `migrate` and
    `reverify` — swallowed under dispatch, a traceback in CI (round 4,
    🟡 14)."""
    write_row(repo, "src/service.py", "handler")
    (repo / ".specseal" / "map" / "bad.md").mkdir()
    r = run(["."], str(repo))
    assert "Traceback" not in r.stderr, r.stderr
    assert "1 ok" in r.stdout, r.stdout
    m = run(["--migrate", "."], str(repo))
    assert "Traceback" not in m.stderr, m.stderr
    v = run(["--reverify", "."], str(repo))
    assert "Traceback" not in v.stderr, v.stderr


# --- round 5: what closing round 4 opened ------------------------------------


def git(d, *a):
    return subprocess.run(
        ["git", "-C", str(d), *a],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def test_migrate_proves_a_row_against_the_file_under_its_own_root(tmp_path):
    """`git show <sha>:<rel>` resolves `<rel>` against the repository TOP
    LEVEL, not against `-C`. Run `--migrate` from a subdirectory and the
    since-the-stamp proof read a same-named file elsewhere in the repo: an
    untouched row was refused forever, and a row whose look-alike happened to
    match was rewritten and stamped as proved (round 5, 🔴 A).
    """
    top = tmp_path / "repo"
    (top / "src").mkdir(parents=True)
    (top / "sub" / "src").mkdir(parents=True)
    (top / "sub" / ".specseal" / "map").mkdir(parents=True)
    # Same path, different content: the decoy the top-level resolution reads.
    (top / "src" / "service.py").write_text(
        "import os\n\n\ndef handler(x):\n    return 999\n"
    )
    (top / "sub" / "src" / "service.py").write_text(SERVICE)
    git(top, "init", "-q")
    git(top, "config", "user.email", "t@example.com")
    git(top, "config", "user.name", "t")
    git(top, "add", "-A")
    git(top, "commit", "-qm", "base")
    sha = git(top, "rev-parse", "HEAD").stdout.strip()

    ledger = top / "sub" / ".specseal" / "map" / "f.md"
    ledger.write_text(
        f"# frag\n\n| CLAUSE | `src/service.py:4-6` | 2026-08-31 `{sha}` |\n"
    )
    r = run(["--migrate", "."], str(top / "sub"))
    assert "1 row migrated · 0 left" in r.stdout, r.stdout
    assert "without the since-the-stamp proof" not in r.stdout, r.stdout
    assert "#handler@" in ledger.read_text(), ledger.read_text()


def test_migrate_still_proves_a_row_at_the_top_level(tmp_path):
    """The other half of 🔴 A's fix: `./` must not break the ordinary case."""
    top = tmp_path / "repo"
    (top / "src").mkdir(parents=True)
    (top / ".specseal" / "map").mkdir(parents=True)
    (top / "src" / "service.py").write_text(SERVICE)
    git(top, "init", "-q")
    git(top, "config", "user.email", "t@example.com")
    git(top, "config", "user.name", "t")
    git(top, "add", "-A")
    git(top, "commit", "-qm", "base")
    sha = git(top, "rev-parse", "HEAD").stdout.strip()

    ledger = top / ".specseal" / "map" / "f.md"
    ledger.write_text(
        f"# frag\n\n| CLAUSE | `src/service.py:4-6` | 2026-08-31 `{sha}` |\n"
    )
    r = run(["--migrate", "."], str(top))
    assert "1 row migrated · 0 left" in r.stdout, r.stdout
    assert "without the since-the-stamp proof" not in r.stdout, r.stdout


def test_write_atomic_writes_through_a_symlink_and_keeps_the_mode(repo, tmp_path):
    """`os.replace(tmp, path)` targets the LINK, so a symlinked ledger was
    replaced by a regular file while the real one behind it stayed stale, and
    every ledger was demoted 0644 → 0600 by `mkstemp` (round 5, 🔴 D)."""
    from conftest import symlink_or_skip

    real = tmp_path / "real.md"
    real.write_text("old\n")
    os.chmod(str(real), 0o664)
    link = repo / ".specseal" / "map" / "linked.md"
    symlink_or_skip(str(real), str(link))

    ec.write_atomic(str(link), "new\n")
    assert os.path.islink(str(link)), "the symlink was replaced by a regular file"
    assert real.read_text() == "new\n", "the file behind the link is stale"
    assert stat.S_IMODE(os.stat(str(real)).st_mode) == 0o664, "the mode was demoted"


def test_write_atomic_keeps_a_plain_ledgers_mode(tmp_path):
    plain = tmp_path / "plain.md"
    plain.write_text("old\n")
    os.chmod(str(plain), 0o644)
    ec.write_atomic(str(plain), "new\n")
    assert plain.read_text() == "new\n"
    assert stat.S_IMODE(os.stat(str(plain)).st_mode) == 0o644, "the mode was demoted"


def test_a_declaration_whose_modifier_is_a_keyword_elsewhere_still_resolves(repo):
    """C# `public new void Render(int x)` and Swift `case loading(String)` are
    declarations whose modifiers are statement keywords in another language.
    The blocklist refused both — real code, BROKEN, exit 2 (round 5, 🔴 C).
    It may now only NARROW a set of candidates, never empty it."""
    cs = ["public new void Render(int x) {", "  return;", "}"]
    assert ec.generic_units(cs, "Render") == [(1, 2)]
    swift = ["enum State {", "  case loading(String)", "}"]
    assert ec.generic_units(swift, "loading") == [(2, 2)]


def test_a_bare_call_statement_is_not_a_declaration(repo):
    """`render(1);` has nothing before the name, so no keyword blocked it and
    the fix for round 4's 🔴 1 left it reading as a second declaration —
    output identical to the pre-fix code (round 5, 🔴 C)."""
    text = "function render(x) {\n  return x;\n}\n\nrender(1);\n"
    assert ec.resolve("app.js", "render", text) == [(1, 2)]


def test_the_recorded_hash_breaks_a_tie_between_two_places(repo):
    """Two real declarations of one name — an overload — is a tie no keyword
    list can break. The row's own recorded content breaks it: the place that
    reconstructs the hash is the row's unit (questions.md §Q3)."""
    text = (
        "void render(int x) {\n  log(x);\n}\n\nvoid render(string s) {\n  send(s);\n}\n"
    )
    (repo / "src" / "app.cs").write_text(text)
    h = ec.content_hash(["void render(int x) {", "  log(x);"])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `src/app.cs#render@{h}` |\n"
    )
    r = run(["."], str(repo))
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout


def test_a_tie_no_place_reconstructs_is_still_broken(repo):
    """The tie-break rests on the row's own evidence and nothing else: where
    no place holds the recorded content, the ambiguity is real and loud."""
    text = (
        "void render(int x) {\n  log(x);\n}\n\nvoid render(string s) {\n  send(s);\n}\n"
    )
    (repo / "src" / "app.cs").write_text(text)
    (repo / ".specseal" / "map" / "f.md").write_text(
        "# frag\n\n| CLAUSE | `src/app.cs#render@00000000` |\n"
    )
    r = run(["."], str(repo))
    assert "ambiguous" in r.stdout and r.returncode == 2, r.stdout


def test_a_map_declaration_does_not_turn_the_scan_off_for_a_local_row(repo, tmp_path):
    """`cross_repo_intent` was true for the whole RUN, so one `--map` turned
    the rename scan off for every unplaceable row, cross-repo or not. A row
    whose prefix is not among the declared maps is a local row (round 5,
    🟡 F)."""
    other = tmp_path / "legacy"
    other.mkdir()
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").unlink()
    (repo / "src" / "moved.py").write_text(SERVICE)
    r = run(["--map", f"legacy={other}", "."], str(repo))
    assert "identical content at src/moved.py#handler" in r.stdout, r.stdout


def test_reverify_says_identical_content_and_not_moved_intact(repo):
    """Round 4's 🟡 7 wording had no pin at all: reverting it passed every
    case in four files (round 5, 🟢)."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("def handler(", "def total_price(")
    )
    r = run(["--reverify", "."], str(repo))
    assert "(identical content)" in r.stdout, r.stdout
    assert "moved intact" not in r.stdout, r.stdout


NO_GIT_CLAIM = re.compile(r"git for nothing|git 을[^.\n]{0,24}부르")


def test_no_document_claims_the_checker_never_calls_git(repo):
    """Round 4's 🟡 10 put a git call in the file — one, in `--migrate` — and
    four documents kept saying the checker calls git for nothing at all. The
    exception belongs in the same paragraph as the claim (round 5, 🟡 H)."""
    for rel in ("CLAUDE.md", "README.md", "README.ko.md"):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            paragraphs = f.read().split("\n\n")
        claiming = [p for p in paragraphs if NO_GIT_CLAIM.search(p)]
        assert claiming, f"{rel} stopped stating the no-git property at all"
        for p in claiming:
            assert "--migrate" in p, f"{rel} claims no git with no exception:\n{p}"


def test_the_advisory_docstring_names_what_it_prints(repo):
    """The same commit taught the advisory OLD-FORMAT and left its docstring
    saying only BROKEN is printed (round 5, 🟡 H)."""
    import ast as ast_mod

    path = os.path.join(ROOT, "hooks", "evidence-advisor.py")
    doc = ast_mod.get_docstring(ast_mod.parse(open(path, encoding="utf-8").read()))
    assert "OLD-FORMAT" in doc, "the docstring still says BROKEN is the whole filter"


def test_known_limits_names_what_this_round_added_to_them(repo):
    """A constant became a scan candidate and collides far more readily than a
    function (round 5, 🟡 G); a nested `def` is anchored by its qualified name
    alone (round 5, 🟢). Neither was in Known limits."""
    with open(
        os.path.join(ROOT, "skills", "evidence-check", "SKILL.md"), encoding="utf-8"
    ) as f:
        limits = f.read().split("## Known limits")[1].split("\n## ")[0]
    assert "constant" in limits, "the twin limit does not name constants"
    assert "nested" in limits, "the qualified-name anchor is unrecorded"


def test_a_row_cannot_read_outside_the_repository_it_is_placed_in(repo, tmp_path):
    """`ANCHOR_RE`'s path class admits `.` and `/`, and `place()` did no
    containment check, so `../outside/creds.py#secret` was read from above the
    root — and `--reverify` wrote back a hash of what it found, turning the
    ledger into a confirmation oracle for a file the project does not contain
    (round 5, 🔴 I).

    Present in the released 0.1.0 checker too, in the `path:line` form, so the
    guard is new rather than a regression close. It bites where a repository
    is checked out but not trusted: the plain check, and the session-start
    hook running `--migrate` without anybody asking.
    """
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "creds.py").write_text("def secret():\n    return 'SENTINEL'\n")
    ledger = repo / ".specseal" / "map" / "f.md"
    ledger.write_text("# frag\n\n| CLAUSE | `../outside/creds.py#secret@00000000` |\n")
    before = ledger.read_text()

    r = run(["."], str(repo))
    assert "escapes the repository" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout

    v = run(["--reverify", "."], str(repo))
    assert ledger.read_text() == before, "reverify rewrote a row it read outside"
    assert "0 rows re-verified" in v.stdout, v.stdout

    ledger.write_text("# frag\n\n| CLAUSE | `../outside/creds.py:1-2` | 2026-08-31 |\n")
    before = ledger.read_text()
    m = run(["--migrate", "."], str(repo))
    assert "escapes the repository" in m.stdout, m.stdout
    assert ledger.read_text() == before, "migrate rewrote a row it read outside"


def test_a_mapped_prefix_still_reaches_its_own_checkout(repo, tmp_path):
    """The containment test is against the repository `place()` RETURNED. A
    `--map` prefix legitimately resolves into another checkout, and testing
    against the root would refuse every cross-repo row."""
    other = tmp_path / "legacy"
    (other / "src").mkdir(parents=True)
    (other / "src" / "service.py").write_text(SERVICE)
    h = ec.content_hash(SERVICE.splitlines()[3:6])
    (repo / ".specseal" / "map" / "f.md").write_text(
        f"# frag\n\n| CLAUSE | `legacy/src/service.py#handler@{h}` |\n"
    )
    r = run(["--map", f"legacy={other}", "."], str(repo))
    assert "1 ok" in r.stdout and r.returncode == 0, r.stdout

    # And the prefix is not a way back out of the checkout it names.
    (repo / ".specseal" / "map" / "f.md").write_text(
        "# frag\n\n| CLAUSE | `legacy/../outside/creds.py#secret@00000000` |\n"
    )
    (tmp_path / "outside").mkdir()
    (tmp_path / "outside" / "creds.py").write_text("def secret():\n    return 'S'\n")
    r = run(["--map", f"legacy={other}", "."], str(repo))
    assert "escapes the repository" in r.stdout, r.stdout
