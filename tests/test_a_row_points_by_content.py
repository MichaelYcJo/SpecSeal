"""A ledger coordinate names a place by content, and reports change by content.

The whole of the mechanism this replaces was compensation for one fact: a
coordinate made of a line number rots on contact. A line moves for edits that
have nothing to do with the claim, so the coordinate is re-anchored, so the
row's derived baseline resets, so a stamp is needed to clear it, so a squash
orphans the stamp. Three review rounds were spent on that chain, and half of
the branch's commits touched `.specseal/` rather than the code it describes.

An anchor plus a content hash removes the cause. There is no baseline, no
stamp, no commit SHA, and `evidence_check.py` no longer imports `subprocess`
at all — which is the shortest proof that the whole squash/rebase class is
gone rather than handled.

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
    """The row then reports BROKEN rather than a hash of something arbitrary.
    Silence here would be a false OK on a file nobody can even read."""
    assert ec.py_spans("def broken(:\n") == {}


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
    assert ec.resolve("r.py", "REVIEW_ANSWERS", text) == [(3, 5)]
    # A YAML key is the same shape, and there the colon DOES declare.
    assert ec.resolve("c.yml", "jobs", "name: x\njobs:\n  a: 1\n  b: 2\nz: 3\n") == [
        (2, 4)
    ]


def test_a_repeated_heading_is_disambiguated_by_its_parent(repo):
    """Rather than by a line number, which is the thing being removed."""
    text = "## A\n\n### Same\n\none\n\n## B\n\n### Same\n\ntwo\n"
    assert len(ec.resolve("d.md", '"### Same"', text)) == 2
    assert ec.resolve("d.md", '"## B / ### Same"', text) == [(9, 11)]


# --- the verdicts -----------------------------------------------------------


def test_a_missing_file_is_broken_not_external(repo):
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").unlink()
    r = run(["."], str(repo))
    assert "BROKEN" in r.stdout and "file not found" in r.stdout, r.stdout
    assert r.returncode == 2, r.stdout


def test_a_cross_repo_path_is_external_without_a_map(repo):
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
    """It refreshes what it can see. A row whose anchor is gone is a row
    somebody has to look at, and silently renaming its hash would hide it."""
    write_row(repo, "src/service.py", "handler")
    (repo / "src" / "service.py").write_text(SERVICE.replace("def handler", "def gone"))
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
    """The squash and rebase class is gone rather than handled, and the
    shortest proof is that there is no git to be wrong about."""
    source = open(SCRIPT, encoding="utf-8").read()
    assert "import subprocess" not in source, "the checker runs commands again"
    # Prose may discuss git; code may not reach for it. Comment and docstring
    # lines are excluded so the reasoning can stay where a reader finds it.
    code = []
    fence = False
    for line in source.splitlines():
        if line.count('"""') % 2:
            fence = not fence
            continue
        if fence or line.lstrip().startswith("#"):
            continue
        code.append(line)
    offenders = [ln for ln in code if "git" in ln and "gitignore" not in ln]
    assert not offenders, f"the checker reaches for git: {offenders}"
