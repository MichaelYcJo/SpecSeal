"""Which tables cmark-gfm renders out of a markdown document, and their cells.

This is the oracle `hooks/config.py#gfm_table` is held to (#647, steps C and
D). It answers one question -- what does GitHub's own renderer put in each
table -- and nothing else. Which table a reader wants, and what it refuses,
is the reader's grammar and is not asked here.

**It shares nothing with what it checks.** It imports `cmarkgfm` and the
standard library, and nothing from `hooks/`, `skills/` or `.github/scripts/`;
`tests/test_one_table_walker_reads_what_gfm_renders.py` reads this file's own
imports to hold that, the arrangement `tests/commonmark_oracle.py` keeps
(#667). A table rule written by somebody else is the whole point: round 3 of
#735 found the walk's silent drop by comparing it with cmark-gfm, and the walk
had been checked only against a list of shapes its own author wrote.

**Why cmark-gfm and not markdown-it-py**, which the suite already pins: GitHub
renders these files with cmark-gfm, and markdown-it-py's table rule is a
reimplementation of it. The version is pinned in
`.github/scripts/run_tests.py#CMARKGFM`, so the renderer cannot move under the
suite.

The document is rendered with GitHub's extensions and raw HTML left out, and
the HTML is read back with `html.parser`. **Left out, not kept**: the
renderer parses an HTML block exactly the same either way and only changes
what it prints for it, `<!-- raw HTML omitted -->`. Kept, a half-written tag
such as `<h1` lands in the output verbatim, `html.parser` reads it as a tag
that swallows the `<table>` after it, and the oracle reported no table where
cmark-gfm rendered one (round 1 of PR #749, measured while closing
yellow 5). A cell is the text inside its
`<th>` or `<td>`, stripped, with character references decoded: the text a
person sees in the rendered table.
"""

import html.parser

import cmarkgfm
from cmarkgfm.cmark import Options


class _Tables(html.parser.HTMLParser):
    """Every `<table>` in rendered HTML, as `(header cells, body rows)`."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.in_head = False
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tables.append([(), []])
        elif tag == "thead":
            self.in_head = True
        elif tag == "tbody":
            self.in_head = False
        elif tag == "tr" and self.tables:
            self.row = []
        elif tag in ("th", "td") and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None:
            self.row.append("".join(self.cell).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.in_head:
                self.tables[-1][0] = tuple(self.row)
            else:
                self.tables[-1][1].append(tuple(self.row))
            self.row = None
        elif tag == "table":
            self.in_head = False

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def rendered(text):
    """TEXT as GitHub renders it, raw HTML left out (see the module's
    docstring for why)."""
    return cmarkgfm.github_flavored_markdown_to_html(
        text, options=Options.CMARK_OPT_DEFAULT
    )


def tables(text):
    """`[(header cells, [body row cells, ...]), ...]` for every table cmark-gfm
    renders out of TEXT, in document order, each row a tuple of strings."""
    reader = _Tables()
    reader.feed(rendered(text))
    reader.close()
    return [(tuple(head), list(rows)) for head, rows in reader.tables]


def rows_under(text, header):
    """The body rows of the first table whose header cells are HEADER, or
    None where cmark-gfm renders no such table."""
    for head, rows in tables(text):
        if head == tuple(header):
            return rows
    return None
