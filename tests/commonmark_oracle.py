"""Which lines of a markdown document a CommonMark renderer hides (#667).

This is the oracle the hook readers are held to. It answers one question per
line -- does a renderer show this line as markdown text, or does it put it
inside something that is not -- and nothing else. Which lines form a table is
each reader's own grammar and is not asked here.

**It shares nothing with what it checks.** It imports markdown-it-py and the
standard library, and nothing from `hooks/`, `skills/` or `.github/scripts/`;
`tests/test_the_hooks_hide_what_a_renderer_hides.py` reads this file's own
imports to hold that. The work item before this one built its oracle out of
the readers' shared functions, and round 3 of it found the gap that
arrangement cannot see: "The oracle cannot catch this, because it is built
the same way." A parser written by somebody else, from the specification,
is the whole point, so no rule of this repository's is written here.

A line is hidden when the parser puts it in one of four places:

  fence    a fenced code block, its delimiter lines included (CommonMark 4.5)
  code     an indented code block (4.4)
  html     an HTML block of any of the seven kinds, a comment among them
           (4.6)
  comment  an inline HTML comment (6.6) that the line BEGINS inside. The line
           where the comment opens begins outside it and is not hidden;
           every later line up to and including the one holding its `-->`
           is

The parser is markdown-it-py's `commonmark` preset with GFM tables switched
on, because the files the hooks read are rendered as GFM, and a table changes
which lines a paragraph holds. The version is pinned in
`.github/scripts/run_tests.py#MARKDOWN_IT`.

**Where the inline comment is, the parser says.** A token carries no source
position, so the parser's own `html_inline` rule is wrapped: the wrapper
calls it unchanged and writes down the offset the rule started and ended at,
in the inline source it was reading. Nothing about what is a comment is
decided here; only where the one the parser found lies.
"""

from markdown_it import MarkdownIt
from markdown_it.rules_inline.html_inline import html_inline

FENCE, CODE, HTML, COMMENT = "fence", "code", "html", "comment"

BLOCK_KINDS = {"fence": FENCE, "code_block": CODE, "html_block": HTML}


def _recording_html_inline(state, silent):
    """The parser's own rule, with where its token started and ended kept."""
    start = state.pos
    found = html_inline(state, silent)
    if found and not silent:
        state.tokens[-1].meta = {"start": start, "end": state.pos}
    return found


def parser():
    md = MarkdownIt("commonmark").enable("table")
    md.inline.ruler.at("html_inline", _recording_html_inline)
    return md


_PARSER = parser()


def _comment_lines(inline, lines):
    """Lines of `inline`'s source that begin inside an HTML comment in it.

    The inline source is the paragraph's lines joined, with Python's
    `str.strip` applied to the whole by the parser. That strip also takes a
    line holding only a no-break space or another Unicode space, which
    CommonMark reads as paragraph text, so the lines it dropped from the top
    are counted back before an offset is turned into a line.
    """
    out = set()
    if not inline.map or not inline.children:
        return out
    first = inline.map[0]
    while first < inline.map[1] - 1 and not lines[first].lstrip(" >").strip():
        first += 1
    src = inline.content
    starts = [0] + [n + 1 for n, ch in enumerate(src) if ch == "\n"]
    for child in inline.children:
        if child.type != "html_inline" or not child.content.startswith("<!--"):
            continue
        span = child.meta or {}
        if "start" not in span:
            continue
        for offset, at in enumerate(starts):
            if span["start"] < at < span["end"]:
                out.add(first + offset)
    return out


def hidden(lines):
    """{index: kind} for every line of `lines` a renderer hides.

    `lines` is a list of lines as a reader splits them, endings removed or
    not; they are joined with `\\n`, so index N here is index N there.
    """
    lines = [line.rstrip("\r\n") for line in lines]
    count = len(lines)
    out = {}
    for token in _PARSER.parse("\n".join(lines)):
        kind = BLOCK_KINDS.get(token.type)
        if kind and token.map:
            for index in range(token.map[0], min(token.map[1], count)):
                out.setdefault(index, kind)
        elif token.type == "inline":
            for index in _comment_lines(token, lines):
                if index < count:
                    out.setdefault(index, COMMENT)
    return out


def hidden_lines(lines):
    """The indices alone."""
    return set(hidden(lines))
