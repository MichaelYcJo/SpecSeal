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

  fence        a fenced code block, its delimiter lines included
               (CommonMark 4.5)
  code         an indented code block (4.4)
  html         an HTML block of any of the seven kinds, a comment among them
               (4.6)
  inline html  inline raw HTML (6.6) that the line BEGINS inside: a comment,
               a CDATA section, a processing instruction, a declaration, an
               open tag or a closing tag -- every token the parser emits as
               `html_inline` (#673). The line where it opens begins outside
               it and is not hidden; every later line up to and including
               the one holding its closer is

All six inline kinds, and not the comment alone, because the block half
already reads that way: an HTML block of every kind is `html`, and CommonMark
6.6 renders raw HTML "without escaping" wherever it stands. Reading only the
comment let this oracle answer "shown" on the other five, which was the
walk's own answer there, so the two agreed by construction (#667 round 3,
🟡 2).

The parser is markdown-it-py's `commonmark` preset with GFM tables switched
on, because the files the hooks read are rendered as GFM, and a table changes
which lines a paragraph holds. The version is pinned in
`.github/scripts/run_tests.py#MARKDOWN_IT`.

**Where the inline HTML is, the parser says.** A token carries no source
position, so the parser's own `html_inline` rule is wrapped: the wrapper
calls it unchanged and writes down the offset the rule started and ended at,
in the inline source it was reading. Nothing about what is inline HTML is
decided here; only where the tokens the parser found lie.
"""

from markdown_it import MarkdownIt
from markdown_it.rules_inline.html_inline import html_inline

FENCE, CODE, HTML, INLINE_HTML = "fence", "code", "html", "inline html"

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


def _behind_markers(line, opens):
    """Where LINE's own text starts behind its containers' markers: a block
    quote's `>`, a bullet, an ordered number (CommonMark 5.1, 5.2), each with
    the spaces and tabs before it. A bullet or a number is a marker only
    where a space, a tab or the line's end follows it, and only on the line
    that OPENS the paragraph: on a later line of it a `*` or a `2.` is text,
    because a list item that could interrupt the paragraph would have ended
    it. A `>` on a later line is a marker, for the same reason."""
    at = 0
    while True:
        rest = line[at:]
        text = rest.lstrip(" \t")
        skip = len(rest) - len(text)
        if text.startswith(">"):
            at += skip + 1
            continue
        if not opens:
            return at
        digits = len(text) - len(text.lstrip("0123456789"))
        if text[:1] in ("-", "+", "*"):
            marker = 1
        elif 0 < digits <= 9 and text[digits : digits + 1] in (".", ")"):
            marker = digits + 1
        else:
            return at
        if text[marker : marker + 1] not in ("", " ", "\t"):
            return at
        at += skip + marker


def _inline_html_lines(inline, lines):
    """Lines of `inline`'s source that begin inside inline raw HTML in it,
    of any of the six kinds.

    Only the inline token's own children are read, not a child's children:
    an offset the wrapper kept is an offset in the source the rule was
    reading, and inside an image description that is the description, not
    the paragraph. A line that begins inside HTML nested there is a line
    after one that left HTML open, which the walk never claims.

    The inline source is the paragraph's lines joined, with Python's
    `str.strip` applied to the whole by the parser. That strip also takes a
    line holding only a no-break space or another Unicode space, which
    CommonMark reads as paragraph text, so the lines it dropped from the top
    are counted back before an offset is turned into a line. A line's
    container markers are not its text, so a list item's `- ` is skipped as
    a block quote's `>` is (#673 round 1, 🟡 1).
    """
    out = set()
    if not inline.map or not inline.children:
        return out
    first = inline.map[0]
    while (
        first < inline.map[1] - 1
        and not lines[first][
            _behind_markers(lines[first], first == inline.map[0]) :
        ].strip()
    ):
        first += 1
    src = inline.content
    starts = [0] + [n + 1 for n, ch in enumerate(src) if ch == "\n"]
    for child in inline.children:
        if child.type != "html_inline":
            continue
        span = child.meta or {}
        if "start" not in span:
            continue
        for offset, at in enumerate(starts):
            if span["start"] < at < span["end"]:
                out.add(first + offset)
    return out


def _starts(pieces):
    """Where each of PIECES, which concatenate to one text, starts in it."""
    out, at = [], 0
    for piece in pieces:
        out.append(at)
        at += len(piece)
    return out


def commonmark_lines(text):
    """TEXT's lines as CommonMark ends them, each with its own ending: at LF,
    CR or CRLF, and nowhere else (the specification's §2.1). Written from the
    specification by a scan, not taken from anything this oracle checks."""
    out, line, index = [], "", 0
    while index < len(text):
        ch = text[index]
        line += ch
        if ch == "\r" and text[index + 1 : index + 2] == "\n":
            line += "\n"
            index += 1
        if ch in "\r\n":
            out.append(line)
            line = ""
        index += 1
    if line:
        out.append(line)
    return out


def _hidden_commonmark(lines):
    """{CommonMark line index: kind} for LINES, CommonMark's own lines."""
    count = len(lines)
    out = {}
    for token in _PARSER.parse("\n".join(lines)):
        kind = BLOCK_KINDS.get(token.type)
        if kind and token.map:
            for index in range(token.map[0], min(token.map[1], count)):
                out.setdefault(index, kind)
        elif token.type == "inline":
            for index in _inline_html_lines(token, lines):
                if index < count:
                    out.setdefault(index, INLINE_HTML)
    return out


# Two marks, because no one run of characters stands everywhere inline HTML
# can hold a piece's start. Letters stand inside any of the six kinds but one
# place: between a closing tag's name and its `>`, where only whitespace may,
# so there a run of Unicode spaces is put instead. A piece starts just after
# a break, which the parser reads as whitespace, so the spaces land where one
# space already stands.
SENTINEL = "QzxSENTINELxzQ"
SPACES = chr(0x2002) + chr(0x2003) + chr(0x2002) + chr(0x2003) + chr(0x2002)


def _tokens(tokens):
    """TOKENS and every child under them, at any depth."""
    for token in tokens:
        yield token
        yield from _tokens(token.children or [])


def _starts_in_inline_html(text, offset):
    """Whether the text from OFFSET, in the middle of a CommonMark line, is
    inside inline raw HTML: the parser reads TEXT with a mark put at OFFSET,
    and an `html_inline` token it finds holds that mark.

    Tokens are read at any depth, an image description's children included,
    because the mark needs no offset. `_inline_html_lines` reads the top
    level alone for the reason its docstring gives.
    """
    for mark in (SENTINEL, SPACES):
        marked = text[:offset] + mark + text[offset:]
        for token in _tokens(_PARSER.parse(marked)):
            if token.type == "html_inline" and mark in token.content:
                return True
    return False


def hidden_text(text):
    """{index: kind} for every line of `text.splitlines()` a renderer hides.

    **The renderer reads TEXT, not a reader's split of it** (#667 round 1,
    🟡 1). `str.splitlines` also ends a line at U+2028, NEL, a form feed and
    five more characters, and CommonMark does not, so a reader's line can be a
    piece of a renderer's line. The parser is given CommonMark's lines. A
    reader line that starts a CommonMark line takes that line's answer, and so
    does a piece of a line in a block the renderer hides. **A piece of any
    other line is asked where it starts** (#667 round 2): inline raw HTML of
    any of the six kinds can open before it or close before it on the same
    line, so the line's answer is not the piece's. Mapping a piece by its
    line was the walk's own rule, and an oracle built on it agreed with the
    walk by construction; asking about comments alone did the same on the
    other five kinds (#673).
    """
    commonmark = commonmark_lines(text)
    found = _hidden_commonmark([line.rstrip("\r\n") for line in commonmark])
    renderer_starts = _starts(commonmark)
    out = {}
    line = 0
    for index, start in enumerate(_starts(text.splitlines(keepends=True))):
        while line + 1 < len(renderer_starts) and renderer_starts[line + 1] <= start:
            line += 1
        kind = found.get(line)
        if start == renderer_starts[line] or kind in (FENCE, CODE, HTML):
            if kind:
                out[index] = kind
        elif _starts_in_inline_html(text, start):
            out[index] = INLINE_HTML
    return out


def hidden(lines):
    """`hidden_text` of LINES joined with `\\n`, endings removed or not, so
    index N here is index N of that text's `splitlines()` -- LINES' own
    index wherever no line holds a break CommonMark does not honour."""
    return hidden_text("\n".join(line.rstrip("\r\n") for line in lines))


def hidden_lines(lines):
    """The indices alone."""
    return set(hidden(lines))
