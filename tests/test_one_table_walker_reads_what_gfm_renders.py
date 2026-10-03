"""One table walker, held to cmark-gfm over an enumerated corpus (#647, C and D).

`hooks/config.py#gfm_table` reads three tables out of markdown: the pact's
`| Signatory |`, a signatory's record of pact changes, and the pact's record
of pact reviews. This module holds it to GitHub's renderer, `cmarkgfm`, through
`tests/gfm_table_oracle.py`, and the property is S1 of the work item's
`spec.md`: **on every shape, the walker's cells equal cmark-gfm's, or the walker
refuses.** No shape yields cells cmark-gfm does not render.

**The corpus is enumerated by construction, not from examples.** Round 3 of
#735 found the walk's silent drop (an autolink row) with 21 shapes its author
had not written, after the walk had passed 14 its author had. So the line kinds
below are every block start CommonMark 0.29 lists in §4 (leaf blocks) and §5
(container blocks), taken section by section, with the near misses each
section states beside its starts; the GFM extensions' own line shapes (a
table's delimiter and rows, a task list item, an extended autolink); and the
inline shapes a line can open with that read as a block start to a careless
eye (an autolink, an scp-style autolink, `<` and a space). Each kind is put at
every position a table has, and at each of five indentations, 0-3 spaces and a
tab, applied to every line of the kind. Each of the three headers takes its
own pass.

What the enumeration leaves out, and why:

  - containers two blocks deep (a list item, a blank line, its indented
    paragraph, then the header): `gfm_table`'s docstring names it as what the
    walker cannot see, because telling it apart needs container nesting;
  - inline markup inside a row's cells (emphasis, a code span, an entity):
    the walker returns a cell's source and the renderer its text, so the two
    differ by design. The rows here are plain, and a cell's content is the
    reader's to judge, not the walk's;
  - a line ending other than LF: `tests/test_every_reader_ends_a_line_where_
    gfm_does.py` holds where a line ends, for every reader.
"""

import ast
import os
import random
import re

import gfm_table_oracle as oracle
import pytest
from conftest import load_hook_module

HERE = os.path.dirname(os.path.abspath(__file__))
config = load_hook_module("config.py", "config_for_the_table_walker")

HEADERS = {
    "signatory": ("Signatory",),
    "pact change": ("Clause", "Row", "Code", "Checked"),
    "pact review": ("Signatory", "Change", "Verdict"),
}

# CommonMark 0.29 §4.6, HTML block start condition 6: the block-level tag
# names, written out from the specification rather than from the walker.
TYPE_6 = [
    "address",
    "article",
    "aside",
    "base",
    "basefont",
    "blockquote",
    "body",
    "caption",
    "center",
    "col",
    "colgroup",
    "dd",
    "details",
    "dialog",
    "dir",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "frame",
    "frameset",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hr",
    "html",
    "iframe",
    "legend",
    "li",
    "link",
    "main",
    "menu",
    "menuitem",
    "nav",
    "noframes",
    "ol",
    "optgroup",
    "option",
    "p",
    "param",
    "section",
    "source",
    "summary",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "title",
    "tr",
    "track",
    "ul",
]

# Every kind is a list of lines. The comment before each group is the section
# of the specification it is taken from.
KINDS = {
    # §4.1 thematic breaks, each character, spaced and not, and a near miss.
    "break ***": ["***"],
    "break ---": ["---"],
    "break ___": ["___"],
    "break * * *": ["* * *"],
    "break - - -": ["- - -"],
    "break _ _ _": ["_ _ _"],
    "not a break **": ["**"],
    # §4.2 ATX headings, the widest and the empty one, and two near misses.
    "heading #": ["# h"],
    "heading ######": ["###### h"],
    "heading, empty": ["#"],
    "not a heading #######": ["####### h"],
    "not a heading #h": ["#h"],
    # §4.3 setext underlines (`---` is above).
    "setext ===": ["==="],
    "setext =": ["="],
    # §4.4 indented code, and indented code that holds a container's marker,
    # which four columns make code rather than a container.
    "indented code": ["    code"],
    "indented code, a list marker": ["    - x"],
    "indented code, a quote marker": ["    > q"],
    # §4.5 fenced code: closed, unclosed, and a backtick info string.
    "fence ```": ["```", "x", "```"],
    "fence ~~~": ["~~~", "x", "~~~"],
    "fence ```, unclosed": ["```"],
    "fence ~~~, unclosed": ["~~~"],
    "not a fence ```a`b": ["```a`b"],
    # §4.6 HTML blocks, the seven start conditions.
    "html 1 <script>": ["<script>"],
    "html 1 <pre>": ["<pre>"],
    "html 1 <style>": ["<style>"],
    "html 1 <textarea>": ["<textarea>"],
    "html 1 closed": ["<pre>x</pre>"],
    "html 1 over lines": ["<pre>", "x", "</pre>"],
    "html 2 closed": ["<!-- c -->"],
    "html 2 open": ["<!--"],
    "html 2 over lines": ["<!--", "c", "-->"],
    "html 3 closed": ["<? x ?>"],
    "html 3 open": ["<?"],
    "html 4 closed": ["<!DOCTYPE html>"],
    "html 4 open": ["<!X"],
    "html 5 closed": ["<![CDATA[ x ]]>"],
    "html 5 open": ["<![CDATA["],
    **{f"html 6 <{n}>": [f"<{n}>"] for n in TYPE_6},
    **{f"html 6 <{n}": [f"<{n}"] for n in TYPE_6},
    "html 6 </div>": ["</div>"],
    "html 6 <div/>": ["<div/>"],
    # A name CommonMark 0.31 added to condition 6, after cmark-gfm's 0.29.
    "html 6? <search": ["<search"],
    # The near miss condition 6 states: the name must end where a listed
    # name ends, so a longer name a listed one begins is not a block start.
    "not html 6, <divx": ["<divx"],
    "not html 6, <pattern": ["<pattern"],
    "html 7 <span>": ["<span>"],
    "html 7 </span>": ["</span>"],
    'html 7 <a href="x">': ['<a href="x">'],
    "html 7 <a href=x y>": ["<a href=x y>"],
    "html 7 <custom-tag/>": ["<custom-tag/>"],
    "not html 7, text after": ["<span>x</span> y"],
    "not html 7, unfinished": ["<span"],
    "not html 7, unquoted": ['<a href="x"'],
    # What may interrupt a paragraph, which decides whether a line above the
    # header leaves a block open: §4.6 says the seventh kind may not, and
    # §5.2 that a list item may only with text after a bullet or the number 1.
    "after a paragraph, html 7": ["text", "<span>"],
    "after a paragraph, html 6": ["text", "<div>"],
    "after a paragraph, list -": ["text", "- x"],
    "after a paragraph, list 1.": ["text", "1. x"],
    "after a paragraph, list 2.": ["text", "2. x"],
    "after a paragraph, list -, empty": ["text", "-"],
    "after a paragraph, quote": ["text", "> q"],
    "after a list item, a break": ["- x", "***"],
    "after a list item, a comment": ["- x", "<!-- c -->"],
    "after a list item, a fence": ["- x", "```", "x", "```"],
    # §4.7 a link reference definition.
    "link reference": ["[x]: https://example.com"],
    # §4.8 a paragraph line.
    "paragraph": ["text"],
    # §4.9 blank lines (the indentation makes the whitespace-only ones).
    "blank": [""],
    # §5.1 block quotes.
    "quote > q": ["> q"],
    "quote >": [">"],
    "quote >q": [">q"],
    # §5.2 list items, each marker, the widest number, empty ones, near misses.
    "list -": ["- x"],
    "list +": ["+ x"],
    "list *": ["* x"],
    "list 1.": ["1. x"],
    "list 2)": ["2) x"],
    "list 123456789.": ["123456789. x"],
    "not a list 1234567890.": ["1234567890. x"],
    "list -, empty": ["-"],
    "list 1., empty": ["1."],
    "not a list -x": ["-x"],
    # GFM: a task list item, an extended autolink, a bare URL.
    "task list": ["- [ ] x"],
    "task list, done": ["- [x] x"],
    "extended autolink": ["www.example.com"],
    "bare url": ["https://example.com/org/x"],
    # GFM tables: a delimiter out of place, and rows written wrong.
    "table delimiter": ["|---|"],
    "table row, two cells": ["| x | y |"],
    "table row, no closing pipe": ["| x"],
    "table row, no opening pipe": ["x |"],
    "table row, empty": ["|  |"],
    # Inline shapes a line can open with.
    "autolink": ["<https://example.com/org/x>"],
    "autolink, scp-style": ["<git@example.com:org/x.git>"],
    "autolink, email": ["<x@example.com>"],
    "< and a space": ["< https://example.com/org/x"],
}

INDENTS = ("", " ", "  ", "   ", "\t")
POSITIONS = (
    "before the header",
    "after the header",
    "after the delimiter",
    "between rows",
    "after the last row",
)
CLAUSE = ["", "## Order response shape", "", "x"]


def row(header, n):
    return (
        "| "
        + " | ".join(f"https://example.com/org/r{n}c{c}" for c in range(len(header)))
        + " |"
    )


def document(header, kind_lines, position, indent):
    """The base table -- a header, its delimiter and two rows, then a clause
    -- with KIND_LINES, each indented by INDENT, put at POSITION."""
    head = "| " + " | ".join(header) + " |"
    delimiter = "|" + "---|" * len(header)
    parts = [head, delimiter, row(header, 1), row(header, 2)]
    at = {
        "before the header": 0,
        "after the header": 1,
        "after the delimiter": 2,
        "between rows": 3,
        "after the last row": 4,
    }[position]
    kind = [indent + line for line in kind_lines]
    lines = ["# Pact", "", *parts[:at], *kind, *parts[at:], *CLAUSE]
    return "\n".join(lines) + "\n"


def delimiters(header):
    """Every spelling of HEADER's delimiter row the GFM tables extension
    states: both outer pipes, one, or none, padded or not, aligned or not --
    and, for one column, the bare `---` that is a setext underline instead."""
    n = len(header)
    cells = ["---"] * n
    aligned = [":-:"] * n
    return [
        "|" + "|".join(cells) + "|",
        "| " + " | ".join(cells) + " |",
        "|" + "|".join(aligned) + "|",
        "|" + "|".join(cells),
        "|".join(cells) + "|",
        "|".join(cells),
    ]


def plain(header, indents, delimiter=None):
    """The base table with its header, delimiter and rows indented by
    INDENTS, the indentation axis on the table's own lines (⬜ 22), and the
    delimiter spelled DELIMITER."""
    head = indents[0] + "| " + " | ".join(header) + " |"
    delimiter = indents[1] + (delimiter or "|" + "---|" * len(header))
    rows = [indents[2] + row(header, n) for n in (1, 2)]
    return "\n".join(["# Pact", "", head, delimiter, *rows, *CLAUSE]) + "\n"


def corpus(header):
    """Every document of HEADER's pass, de-duplicated, in a stable order."""
    seen, out = set(), []
    for kind, lines in KINDS.items():
        for position in POSITIONS:
            for indent in INDENTS:
                text = document(header, lines, position, indent)
                if text not in seen:
                    seen.add(text)
                    out.append(((kind, position, indent), text))
    for a in INDENTS:
        for b in INDENTS:
            for c in INDENTS:
                text = plain(header, (a, b, c))
                if text not in seen:
                    seen.add(text)
                    out.append((("plain", a, b, c), text))
    for spelled in delimiters(header):
        text = plain(header, ("", "", ""), spelled)
        if text not in seen:
            seen.add(text)
            out.append((("delimiter", spelled), text))
    return out


def disagreement(header, text):
    """None where the walker agrees with cmark-gfm on TEXT or refuses it;
    otherwise what each said."""
    want = oracle.rows_under(text, header)
    rows, refusals = config.gfm_table(text, header)
    if refusals:
        return None
    got = [cells for _line, cells in rows]
    if want is not None and got == want:
        return None
    return f"walker {got}, cmark-gfm {want}"


# --- the oracle is independent ---------------------------------------------


def imported_roots(path):
    with open(path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            roots.add((node.module or "").split(".")[0] if not node.level else ".")
    return roots


def test_the_oracle_imports_the_renderer_and_nothing_of_this_repositorys():
    """The oracle shares no code with the walk it checks, as
    `tests/commonmark_oracle.py` shares none with the hook readers (#667)."""
    assert imported_roots(oracle.__file__) == {"cmarkgfm", "html"}
    with open(oracle.__file__, encoding="utf-8") as handle:
        source = handle.read()
    for reach in ("sys.path", "importlib", "hooks/", "skills/", ".github/"):
        assert reach not in source.split('"""', 2)[-1], reach


def test_the_oracle_reads_a_table_and_a_row_gfm_adds():
    """The two facts round 3 of #735 executed, read through the oracle: an
    autolink line under a table is one of its rows, and a thematic break
    ends it."""
    head = "| Signatory |\n|---|\n| https://example.com/org/a |\n"
    assert oracle.rows_under(
        head + "<https://example.com/org/b>\n", ("Signatory",)
    ) == [
        ("https://example.com/org/a",),
        ("https://example.com/org/b",),
    ]
    assert oracle.rows_under(head + "***\n| x |\n", ("Signatory",)) == [
        ("https://example.com/org/a",)
    ]


# --- S1: on every shape, equal or refused ----------------------------------


@pytest.mark.parametrize("which", sorted(HEADERS))
@pytest.mark.parametrize("kind", sorted(KINDS))
def test_the_walker_reads_what_cmark_gfm_renders_or_refuses(which, kind):
    header = HEADERS[which]
    wrong = []
    for position in POSITIONS:
        for indent in INDENTS:
            text = document(header, KINDS[kind], position, indent)
            said = disagreement(header, text)
            if said:
                wrong.append(f"{position}, indent {indent!r}: {said}\n{text}")
    assert not wrong, "\n".join(wrong)


@pytest.mark.parametrize("which", sorted(HEADERS))
def test_a_table_indented_as_gfm_permits_is_read_and_not_refused(which):
    """S3 (⬜ 22 of #735's round 3). Where cmark-gfm renders the table, the
    walker reads it exactly, refusing nothing; where it renders none (a tab
    before the header or the delimiter), the walker refuses."""
    header = HEADERS[which]
    wrong = []
    for a in INDENTS:
        for b in INDENTS:
            for c in INDENTS:
                text = plain(header, (a, b, c))
                want = oracle.rows_under(text, header)
                rows, refusals = config.gfm_table(text, header)
                got = [cells for _line, cells in rows]
                if want is None:
                    ok = bool(refusals)
                elif c == "\t":
                    # GFM ends the table above a row a tab indents; the walk
                    # refuses that row as one it never reaches.
                    ok = bool(refusals) or got == want
                else:
                    ok = not refusals and got == want
                if not ok:
                    wrong.append(f"{(a, b, c)!r}: walker {got} {refusals}, GFM {want}")
    assert not wrong, "\n".join(wrong)


@pytest.mark.parametrize("which", sorted(HEADERS))
def test_every_delimiter_gfm_accepts_is_read(which):
    """Every spelling of the delimiter row: where cmark-gfm renders the
    table, the walker reads it exactly and refuses nothing; where it renders
    none (a bare `---` under one column is a setext underline), the walker
    refuses."""
    header = HEADERS[which]
    wrong = []
    for spelled in delimiters(header):
        text = plain(header, ("", "", ""), spelled)
        want = oracle.rows_under(text, header)
        rows, refusals = config.gfm_table(text, header)
        got = [cells for _line, cells in rows]
        ok = bool(refusals) if want is None else (not refusals and got == want)
        if not ok:
            wrong.append(f"{spelled!r}: walker {got} {refusals}, GFM {want}")
    assert not wrong, "\n".join(wrong)


@pytest.mark.parametrize("which", sorted(HEADERS))
def test_a_line_directly_above_the_header_is_refused(which):
    """Whether cmark-gfm renders a table under a line depends on the block
    state above it, which the walker does not track, so a non-blank line the
    walk is shown directly above a header is refused with the blank-line
    remedy (round 1, yellow 5). This reverses the build's first choice,
    which mirrored cmark-gfm's interruption rules line by line and was found
    reading tables cmark-gfm does not render in shapes the corpus did not
    reach. A kind whose last line `unfenced` hides, or a blank line, leaves
    a gap or a blank above the header and is not this rule's."""
    header = HEADERS[which]
    for kind, lines in KINDS.items():
        for indent in INDENTS:
            text = document(header, lines, "before the header", indent)
            split = text.splitlines()
            head = split.index("| " + " | ".join(header) + " |")
            shown = dict(config.unfenced(split, text))
            above = shown.get(head - 1)
            if above is None or not above.strip():
                continue
            _rows, refusals = config.gfm_table(text, header)
            assert refusals and "blank line above the header" in refusals[0], (
                kind,
                indent,
                refusals,
            )


def test_the_shapes_round_1_measured_are_refused():
    """Round 1's measured shapes, each a table cmark-gfm does not render and
    the walker read: a table directly above, a setext `-` that makes the
    next line a list, a seventh-kind tag after a list item, and an HTML
    block of kinds 1-5 left open across a blank line."""
    u = "https://example.com/org/a"
    opener = "<" + "!-- old list, being retired"
    for text in (
        f"| Name |\n|---|\n| x |\n| Signatory |\n|---|\n| {u} |\n",
        f"Intro\n-\n2. second\n| Signatory |\n|---|\n| {u} |\n",
        f"1) one\n<a>\n___\n>\n| Signatory |\n|---|\n| {u} |\n",
        f"# Pact\n\n{opener}\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<pre>\nexample\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<?php\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<![CDATA[\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<!DOCTYPE\n\n| Signatory |\n|---|\n| {u} |\n",
    ):
        assert oracle.rows_under(text, ("Signatory",)) is None, text
        _rows, refusals = config.gfm_table(text, ("Signatory",))
        assert refusals, text


def test_an_html_block_closed_above_the_header_leaves_the_table(oracle_check=True):
    """The other side of the open-block refusal: a kind 1-5 block closed on
    a later line, a blank line, then the table, renders, and is read."""
    u = "https://example.com/org/a"
    for text in (
        f"<pre>\nx\n</pre>\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<?php\nx\n?>\n\n| Signatory |\n|---|\n| {u} |\n",
    ):
        assert oracle.rows_under(text, ("Signatory",)) == [(u,)], text
        rows, refusals = config.gfm_table(text, ("Signatory",))
        assert refusals == [] and [c for _l, c in rows] == [(u,)], text


# --- an independent generator (round 1, yellow 5) ---------------------------
#
# The corpus puts one kind at a time at each position; round 1 found the
# walker's line-above mistakes with random documents instead. This is that
# generator, held small and seeded so it runs in a few seconds: documents of
# 2-9 lines drawn from a vocabulary of line kinds and table lines, judged by
# cmark-gfm. Its one tolerated disagreement is `unfenced`'s limit, named in
# `gfm_table`'s docstring: a fence line `unfenced` hides that cmark-gfm reads
# inside an HTML block, which a blank line has not yet ended.

GENERATOR_SEED = 647
GENERATOR_DOCUMENTS = 3000
FENCE_LINE = re.compile(r"^ {0,3}(?:`{3,}|~{3,})")
HTML_LINE = re.compile(r"^ {0,3}<[A-Za-z!?/]")


def vocabulary(header):
    lines = [ln for kind in KINDS.values() for ln in kind]
    head = "| " + " | ".join(header) + " |"
    delimiter = "|" + "---|" * len(header)
    table = [head, delimiter, row(header, 1), row(header, 2), "| x |", "|---|"]
    return sorted(set(lines)) + table * 6 + ["", "", "", "text"]


def inside_html_fence(text):
    """True where a fence line stands under an HTML block start with no
    blank line between: the limit `unfenced` shares with `config_rows`."""
    opened = False
    for line in text.splitlines():
        if not line.strip():
            opened = False
        elif HTML_LINE.match(line):
            opened = True
        elif opened and FENCE_LINE.match(line):
            return True
    return False


@pytest.mark.parametrize("which", sorted(HEADERS))
def test_random_documents_are_read_as_cmark_gfm_renders_them_or_refused(which):
    header = HEADERS[which]
    words = vocabulary(header)
    pick = random.Random(f"{GENERATOR_SEED}-{which}")
    head = "| " + " | ".join(header) + " |"
    wrong = []
    for _n in range(GENERATOR_DOCUMENTS):
        lines = [pick.choice(words) for _k in range(pick.randint(2, 9))]
        if head not in lines:
            lines.insert(pick.randint(0, len(lines)), head)
        text = "\n".join(lines) + "\n"
        said = disagreement(header, text)
        if said and not inside_html_fence(text):
            wrong.append(f"{said}\n{text}")
    assert not wrong, f"{len(wrong)} disagreements:\n" + "\n".join(wrong[:5])


def test_round_3s_shapes_are_inside_the_corpus():
    """Round 3 of #735 compared 21 shapes and named their kinds; each falls
    inside the enumeration, so they are not listed separately (spec item 1).
    Written here as round 3 wrote them, against the `Signatory` header."""
    header = HEADERS["signatory"]
    texts = {text for _key, text in corpus(header)}
    named = [
        ("autolink", "after the last row", ""),
        ("autolink, scp-style", "after the last row", ""),
        ("< and a space", "after the last row", ""),
        ("break ***", "after the last row", ""),
        ("break ---", "after the last row", ""),
        ("break ___", "after the last row", ""),
        ("html 6 <div>", "between rows", ""),
        ("list 1.", "between rows", ""),
        ("blank", "between rows", ""),
        ("paragraph", "after the last row", ""),
        ("heading ######", "between rows", ""),
        ("fence ```", "between rows", ""),
        ("html 2 closed", "between rows", ""),
        ("quote > q", "between rows", ""),
        ("list -", "between rows", ""),
        ("table delimiter", "between rows", ""),
        ("table row, two cells", "after the last row", ""),
        ("table row, no closing pipe", "after the last row", ""),
        ("table row, no opening pipe", "after the last row", ""),
        ("table row, empty", "after the last row", ""),
    ]
    for kind, position, indent in named:
        assert document(header, KINDS[kind], position, indent) in texts, kind
    for indents in (("   ", "", ""), ("", "   ", ""), ("", "", "   "), ("", "", "\t")):
        assert plain(header, indents) in texts, indents


def test_the_corpus_is_counted():
    """The size the phase record states, so a kind that silently stops
    generating shapes is a red case rather than a smaller number nobody
    reads."""
    sizes = {which: len(corpus(header)) for which, header in HEADERS.items()}
    assert sizes == {"signatory": 5454, "pact change": 5455, "pact review": 5455}, sizes


def test_a_half_written_tag_does_not_hide_the_table_from_the_oracle():
    """`<h1` with no `>` above a table: cmark-gfm renders the table, and an
    oracle printing raw HTML handed `html.parser` a tag that swallowed the
    `<table>` after it, so the oracle said no table."""
    text = "<h1\n\n| Signatory |\n|---|\n| https://example.com/org/a |\n"
    assert oracle.rows_under(text, ("Signatory",)) == [("https://example.com/org/a",)]


@pytest.mark.parametrize(
    "above",
    [
        "text\n```\nx\n```\n",
        "text\n<!-- c -->\n",
        "<div>\n\n",
        "<pre>x</pre>\n\n",
        "<? x ?>\n\n",
        "<!DOCTYPE html>\n\n",
    ],
    ids=[
        "a closed fence directly above, under a paragraph",
        "a closed comment directly above, under a paragraph",
        "a kind-6 block a blank line ends",
        "a kind-1 block closed on its own line",
        "a kind-3 block closed on its own line",
        "a kind-4 block closed on its own line",
    ],
)
def test_a_table_under_a_block_that_has_ended_is_read(above):
    """The refusals reach no further than they must: a block `unfenced` hides
    leaves a gap rather than a line above, a blank line ends a kind-6 block,
    and a kind 1-5 block closed on its opening line is closed. cmark-gfm
    renders each table, and the walker reads it."""
    u = "https://example.com/org/a"
    text = f"# Pact\n\n{above}| Signatory |\n|---|\n| {u} |\n"
    assert oracle.rows_under(text, ("Signatory",)) == [(u,)], text
    rows, refusals = config.gfm_table(text, ("Signatory",))
    assert refusals == [] and [c for _l, c in rows] == [(u,)], (text, refusals)


@pytest.mark.parametrize(
    "cell", ["a \\\\| b", "a \\\\\\\\| b"], ids=["two backslashes", "four backslashes"]
)
def test_a_pipe_after_an_even_run_of_backslashes_is_refused(cell):
    """cmark-gfm reads `\\|` as an escaped pipe wherever it stands, so a pipe
    after an even run of backslashes does not split its cell; `CELL` read
    the backslashes in pairs and split there, and a three-cell row read as
    four (round 1, white 6). Such a row is refused rather than guessed."""
    header = HEADERS["pact change"]
    text = (
        "| Clause | Row | Code | Checked |\n|---|---|---|---|\n"
        f"| {cell} | c | 2026-10-04 |\n"
    )
    assert oracle.rows_under(text, header) != [("a \\", "b", "c", "2026-10-04")]
    rows, refusals = config.gfm_table(text, header)
    assert rows == [] and refusals, (rows, refusals)
