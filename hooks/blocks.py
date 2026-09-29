"""Shared reader: which lines of a markdown file does a renderer put inside a
fenced code block or an HTML comment block, and where can this module not say?

Three readers decide from a markdown file what a person declared or wrote:
`hooks/config.py` (the `| Item | Value |` table, on every Bash call through
`mode-gate` and `broad-gate`), `hooks/routing.py` (the routing declaration, on
every commit and at the pull request), and `.github/scripts/rider_check.py`
(the riders). A row quoted in a fenced example, or parked in an HTML comment,
is not a row anybody gave, and each reader used to decide that by a rule of
its own or by none (#667, #658). This is the one walk all three read.

**What it models: two block constructs, by CommonMark's own block rules.**

  1. A fenced code block (CommonMark 4.5): at most three spaces, a run of
     three or more backticks or tildes, no backtick in a backtick opener's
     info string, and a closer of the same character at least as long with
     nothing after it but spaces. `fence_opener` and `fence_closes` below are
     that rule, the same one `skills/verify/scripts/unverified_check.py#
     fence_opener` states; `tests/test_unverified_rows_close.py` holds the two
     in step.
  2. An HTML comment block (4.6, type 2): a line that begins with `<!--`, to
     the first line holding `-->`, which may be the start line itself.

They are walked in one pass, in document order, and a start is looked for
only on a line outside both. Inside a fence nothing but its closer is read;
inside a comment block nothing but `-->`. Both start conditions and both end
conditions are properties of one line, and CommonMark decides block structure
before it parses anything inline, which is why these two can be exact where
the readings before this one could not: a code span or a mid-line `<!--` can
never hide a fence line or a comment-block line.

**A construct that never closes is not a construct.** Its start line is read
as an ordinary line and the walk goes on. A renderer hides everything below
it, so below that line this walk's HIDDEN answers stand -- a renderer hides
those lines too -- and its LIVE answers are uncertain.

**Nothing inline is modelled.** A mid-line `<!--` is inline raw HTML: it may
hide text inside its own paragraph and nothing else, so the lines after it up
to the first `-->`, a blank line or a block start are uncertain, and nothing
is decided about them.

**Where the walk does not know, it says so, and it decides nothing.** Every
line carries an `uncertain` flag, and a reader reads an uncertain line exactly
as it did before this module existed -- its BASE reading. That is the whole
safety argument: on every line the reader's answer is either its old one or
the renderer's, never a third. The contexts the walk calls uncertain, and why
it cannot be exact there:

  - from the first construct-looking line that stands inside a container --
    indented, after a `>` or after a list marker -- or that starts some other
    HTML block (`<` and a letter, `/`, `?` or `!`), to the end of the file:
    a list item's end can end a construct before its delimiter, and inside
    another HTML block a fence line opens nothing, so every later pairing may
    have shifted;
  - from a construct that never closes, to the end of the file, for its live
    answers (above);
  - the paragraph lines after a mid-line `<!--` (above);
  - a line behind a container's marker (`>`, a bullet, a number), a line
    indented four columns or more, and a blank line after either: any of
    them may be part of an indented code block, and `-     code` is one
    whose indentation only the marker's column decides.

**A line is a line where GFM ends one, at LF, CR or CRLF** (#667 round 1,
🟡 1). The readers split with `str.splitlines`, which also ends a line at
U+2028, NEL, a form feed and five more characters; `walk_text` walks the
file's own lines and answers for each reader line by the line it starts in.

`tests/test_the_hooks_hide_what_a_renderer_hides.py` holds this to a
CommonMark parser that shares nothing with it: on every line the walk does
not call uncertain, over the frame's shapes and a seeded generated corpus,
the walk and the parser agree. A context is taken off the list above only
with that case green on documents that hold it.

Standard library only, and it imports nothing: it runs on the hook path,
where loading a skill module would cost every hook call.
"""

import re

# A fenced code block's delimiter line, as CommonMark spells one: up to three
# spaces of indentation, then a run of three or more backticks or three or
# more tildes, then the info string. Four or more spaces is an indented code
# block instead and never a fence. This is the pattern `hooks/config.py#FENCE`
# held until #667 moved it here; that name re-exports this one.
FENCE = re.compile(r"^ {0,3}(?P<run>`{3,}|~{3,})(?P<info>.*)$")

OPENER = "<" + "!--"
CLOSER = "-->"

LIVE, FENCED, COMMENTED = "live", "fence", "comment"

# A container's marker run in front of a line: indentation, a block quote's
# `>`, a list item's bullet or number. What follows it is what the line is.
# A list marker needs a space, a tab or the line's end after it; a block
# quote's `>` needs nothing (CommonMark 5.1: the space after it may be
# omitted), so `>` followed by a fence run is a fence inside a quote (#667
# round 1, 🟡 2).
CONTAINER = re.compile(r"^(?:[ \t]*(?:>|(?:[-+*]|\d{1,9}[.)])(?=[ \t]|$)))*[ \t]*")

# A line as GFM ends it: at LF, CR or CRLF, and nowhere else. `str.splitlines`
# also ends one at U+2028, U+2029, NEL, a form feed, a vertical tab and
# `\x1c` to `\x1e`, and a `<!--` or a fence run after one of those starts a
# line for that split and no line for a renderer (#667 round 1, 🟡 1; #664's
# class). This and `gfm_lines` are a copy of `skills/evidence-check/scripts/
# evidence_check.py#GFM_LINE_RE` and `#gfm_lines`, work item A's precedent:
# a hook imports nothing from `skills/`, and `tests/test_the_hooks_hide_what_
# a_renderer_hides.py#test_the_walks_line_rule_is_the_checkers` holds the two
# in step.
GFM_LINE_RE = re.compile(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+\Z")
# What a line that starts a block this walk does not follow looks like, once
# the container run is taken off: a fence run, or any HTML start.
BLOCK_LOOKING = re.compile(r"`{3,}|~{3,}|<")
# Another kind of HTML block (CommonMark 4.6, types 1 and 3 to 7), at the top
# level. A comment block's own `<!--` is told apart before this is asked.
OTHER_HTML = re.compile(r"<[A-Za-z/?!]")


def fence_opener(line):
    """The fence LINE opens, as `(character, length)`, or None."""
    found = FENCE.match(line.rstrip("\r\n"))
    if not found:
        return None
    run = found.group("run")
    if run[0] == "`" and "`" in found.group("info"):
        return None
    return run[0], len(run)


def fence_closes(line, opener):
    """Whether LINE closes the fence OPENER (a `fence_opener` value)."""
    found = FENCE.match(line.rstrip("\r\n"))
    return bool(
        found
        and found.group("run")[0] == opener[0]
        and len(found.group("run")) >= opener[1]
        and not found.group("info").strip()
    )


def not_spaces_after_the_run(line):
    """Whether LINE's text after its fence run is whitespace `str.strip`
    removes and CommonMark does not count -- anything but spaces and tabs."""
    found = FENCE.match(line.rstrip("\r\n"))
    info = found.group("info") if found else ""
    return not info.strip() and bool(info.strip(" \t"))


def fence_only(lines):
    """(indices inside a fenced block, index of an opener never closed or
    None) -- the fence rule alone, a block that never closes running to the
    end of the file.

    This is not the walk. It is the reading `hooks/config.py` gave every line
    before #667, and it stays because that reader's base reading is what an
    uncertain line gets: `hooks/config.py#fence_map`'s docstring says why a
    config line below a fence nobody closed stays hidden.
    """
    hidden, opener, opened_at = set(), None, None
    for index, raw in enumerate(lines):
        if opener is None:
            opener = fence_opener(raw)
            if opener is not None:
                opened_at = index
                hidden.add(index)
            continue
        hidden.add(index)
        if fence_closes(raw, opener):
            opener, opened_at = None, None
    return hidden, opened_at


def columns(line):
    """How far the line's leading spaces and tabs reach, a tab to the next
    multiple of four, as CommonMark counts indentation."""
    width = 0
    for ch in line:
        if ch == " ":
            width += 1
        elif ch == "\t":
            width += 4 - width % 4
        else:
            break
    return width


def leaves_open(text):
    """Whether TEXT ends inside an inline comment that began in it, as far as
    the delimiters alone can say: its last `<!--` has no `-->` after it.

    Nothing here knows a code span, so a `<!--` quoted in one counts. That
    errs only toward calling more lines uncertain, never toward hiding one.
    """
    at = text.rfind(OPENER)
    return at != -1 and CLOSER not in text[at + 2 :]


class Walk:
    """What `walk` found, one entry per line.

    kinds      LIVE, FENCED or COMMENTED: what the walk says the line is
    uncertain  True where the walk does not know, and a reader must read
               the line as it did before
    unclosed   the index of every fence opener that never closes, which
               the walk read as an ordinary line
    """

    def __init__(self, kinds, uncertain, unclosed):
        self.kinds = kinds
        self.uncertain = uncertain
        self.unclosed = unclosed

    def hidden(self, base=()):
        """{index: kind} of the lines a reader hides: the walk's answer where
        it knows, and where it does not, the lines of BASE -- the reader's own
        reading before #667, as {index: kind} or a set of fenced indices."""
        if not isinstance(base, dict):
            base = dict.fromkeys(base, FENCED)
        out = {}
        for index, kind in enumerate(self.kinds):
            if self.uncertain[index]:
                if index in base:
                    out[index] = base[index]
            elif kind != LIVE:
                out[index] = kind
        return out


def walk(lines):
    """The walk over LINES, which may keep their own endings."""
    text = [raw.rstrip("\r\n") for raw in lines]
    count = len(text)
    kinds = [LIVE] * count
    uncertain = [False] * count
    unclosed = []

    # The first line at or below each index that holds a closer: a comment
    # block starting at a line ends there, and an opener with none below it
    # never closes.
    next_close = [None] * (count + 1)
    for index in range(count - 1, -1, -1):
        next_close[index] = index if CLOSER in text[index] else next_close[index + 1]

    all_from, live_from = None, None
    pending, indented = False, False
    index = 0
    while index < count:
        line = text[index]
        prefix = CONTAINER.match(line).group(0)
        rest = line[len(prefix) :]
        if (prefix and BLOCK_LOOKING.match(rest)) or (
            not prefix and OTHER_HTML.match(rest) and not rest.startswith(OPENER)
        ):
            all_from = index
            break
        if not prefix:
            opener = fence_opener(line)
            if opener is not None:
                end = next(
                    (
                        below
                        for below in range(index + 1, count)
                        if fence_closes(text[below], opener)
                    ),
                    None,
                )
                if end is not None and not_spaces_after_the_run(text[end]):
                    # The one place the shared delimiter rule and CommonMark
                    # part: `str.strip` also takes a no-break space or another
                    # Unicode space after a closing run, and CommonMark takes
                    # only spaces and tabs. Where the file holds such a line,
                    # which block it closes is not certain, so nothing below
                    # the opener is claimed.
                    all_from = index
                    break
                if end is not None:
                    kinds[index : end + 1] = [FENCED] * (end + 1 - index)
                    pending, indented = False, False
                    index = end + 1
                    continue
                unclosed.append(index)
                live_from = index if live_from is None else live_from
            elif line.startswith(OPENER):
                end = next_close[index]
                if end is not None:
                    kinds[index : end + 1] = [COMMENTED] * (end + 1 - index)
                    pending, indented = False, False
                    index = end + 1
                    continue
                live_from = index if live_from is None else live_from
        if not line.strip(" \t"):
            # A blank line between two indented lines is part of the
            # indented code block they may form, so it is no surer than
            # they are.
            pending = False
            uncertain[index] = indented
        else:
            if pending:
                uncertain[index] = True
                if CLOSER in line:
                    pending = leaves_open(line[line.index(CLOSER) + len(CLOSER) :])
            elif leaves_open(line):
                pending = True
            # A line behind a container's marker -- `>`, a bullet, a number
            # -- may hold an indented code block the marker's own column
            # decides (`-     code`), and a line indented four columns or
            # more may be one. Neither is claimed, nor a blank line after it.
            indented = bool(prefix.strip(" \t")) or columns(line) >= 4
            if indented:
                uncertain[index] = True
        index += 1

    if all_from is not None:
        for below in range(all_from, count):
            kinds[below], uncertain[below] = LIVE, True
    if live_from is not None:
        for below in range(live_from, count):
            if kinds[below] == LIVE:
                uncertain[below] = True
    return Walk(kinds, uncertain, unclosed)


def gfm_lines(text, keepends=False):
    """TEXT's lines as GFM reads them, the way `str.splitlines` returns them
    otherwise: no trailing empty line, and each line's end kept only when
    KEEPENDS asks. `evidence_check.py#gfm_lines`, copied (see `GFM_LINE_RE`)."""
    lines = GFM_LINE_RE.findall(text)
    return lines if keepends else [line.rstrip("\r\n") for line in lines]


def _starts(pieces):
    out, at = [], 0
    for piece in pieces:
        out.append(at)
        at += len(piece)
    return out


def walk_text(text):
    """The walk over TEXT, answered for each line of `text.splitlines()`.

    **Every reader splits with `str.splitlines`, and the walk must not**
    (#667 round 1, 🟡 1). A reader's grammar keeps its own lines -- which
    lines form a table is not this module's question -- but whether a line
    stands in a fence or a comment is a renderer's, and a renderer ends a line
    at LF, CR and CRLF alone. So the walk reads `gfm_lines(text)`, and each
    reader line takes the answer of the GFM line it starts in: a piece of a
    hidden line is hidden, a piece of a shown line is shown unless the line
    opened an inline comment before it and left it open -- then a renderer
    hides the piece, and the walk calls it uncertain (#667 round 2) -- and a
    piece of a line the walk is not sure of keeps its reader's base reading.
    An unclosed fence opener is reported at the reader line that starts where
    it does.

    Called with LINES alone, `walk` reads them as given; every reader that
    has the text hands it here instead.
    """
    renderer = gfm_lines(text, keepends=True)
    walked = walk([line.rstrip("\r\n") for line in renderer])
    renderer_starts = _starts(renderer)
    kinds, uncertain, of = [], [], []
    line = 0
    for start in _starts(text.splitlines(keepends=True)):
        while line + 1 < len(renderer_starts) and renderer_starts[line + 1] <= start:
            line += 1
        at_start = start == renderer_starts[line]
        # A piece that starts inside an inline comment its own line opened is
        # hidden by a renderer while the line is shown (#667 round 2), so the
        # walk is not sure of it and the reader keeps its base reading. At a
        # line's start the text before the piece is empty and opens nothing.
        inside = walked.kinds[line] == LIVE and leaves_open(
            renderer[line][: start - renderer_starts[line]]
        )
        kinds.append(walked.kinds[line])
        uncertain.append(walked.uncertain[line] or inside)
        of.append((line, at_start))
    opened = set(walked.unclosed)
    unclosed = [
        index
        for index, (line, at_start) in enumerate(of)
        if at_start and line in opened
    ]
    return Walk(kinds, uncertain, unclosed)
