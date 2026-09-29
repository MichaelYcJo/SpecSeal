"""Shared reader: what does this repository say about itself?

`config.md` sits in the root `hooks/optin.py` resolves, in the same shape as
`parity.md` -- a markdown table of `| Item | Value |`. Every row in it is
optional and every absent row has a default, which is what every repository
got before that row existed.

`Mode` is the exception that proves it, and it is why this module exists. What
every repository got before that row was *the folder decides*, which is not a
value, so an absent one has no default at all -- it is filled in from where the
folder actually is, by `seal mode`. Until somebody runs that command, a root
exists that nobody chose a mode for, and #151 is what that costs: a monorepo
was opted into shared mode, with its review records committed, without the
question ever being put to anyone.

Two callers need the row and they need the SAME answer.
`skills/implement/scripts/seal.py` writes it, and `hooks/mode-gate.py` reads it
to decide whether the question still has to be asked. A file that one of them
parses and the other does not is a gate that stays quiet about a row the
command believes it wrote. The parser lived in `seal.py`, which is a
two-thousand-line command that a `PreToolUse` hook must not import -- so the
READER moved here and the writer stayed there, and `seal.py` re-exports these
names rather than keeping a second copy.

**Not in `optin.py`, deliberately.** That module's docstring says there is no
config key and everything in it fails toward *not opted in*; the root's
existence is the opt-in and `docs/one-root-by-lifetime.md` §*The opt-in signal
is the root itself* is the clause. The `Mode` row decides nothing about opting
in -- it RECORDS an answer -- and putting it in that module would read as the
clause being softened.

Everything here fails toward "nothing is declared". A file that cannot be read
is not an answer somebody gave.
"""

import os
import re
import sys

# `hooks/blocks.py` is a sibling, found by this file's own directory, so the
# callers that load this module by path -- `broad_gate.py#load`, `seal.py` --
# find it too. `hooks/routing.py` reaches `optin.py` the same way.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import blocks
except ImportError as missing:
    # A sentence rather than a bare `ModuleNotFoundError`, and an exception
    # rather than an exit, because this is a module other code imports: a
    # `PreToolUse` gate that raises is skipped for that call and said at the
    # end of the turn (`hooks/dispatch.py`, #28), and a script that loads this
    # file by path catches the error or names the file first
    # (`skills/implement/scripts/seal.py#HOOK_PURPOSES`).
    raise ImportError(
        "cannot read "
        + os.path.join(os.path.dirname(os.path.abspath(__file__)), "blocks.py")
        + ", and it is the walk this reader reads config.md through, which "
        "tells a live row from one quoted in a fence or parked in a comment. "
        "This file ships beside it under `hooks/`; a copy of one taken on its "
        "own is not a plugin"
    ) from missing

CONFIG = "config.md"
ROW_ITEM = "Mode"

# The two modes, spelled the way every document in this repository spells
# them. Read case-insensitively, written lowercase.
LOCAL, SHARED = "local", "shared"
MODES = (LOCAL, SHARED)

# The `| Item | Value |` table, read exactly as `templates/parity.md` and the
# pull-request-language row are read.
CONFIG_HEADER = re.compile(r"^\|\s*Item\s*\|\s*Value\s*\|\s*$")

# A CELL is any run of characters that are neither a pipe nor a backslash, or
# a backslash followed by anything. The second half is markdown's own escape,
# and this file is markdown: `\|` is how a cell of a markdown table carries a
# literal pipe, and `templates/config.md` already writes its own cells that
# way. Without it a cell ended at the first `|`, so a `Broad gate` row holding
# a pipe stopped being a row -- and `config_rows`'s stop rule then took every
# row written below it, silently (#415).
#
# A bare pipe is still a cell boundary, deliberately. Making it part of the
# value needs a greedy last cell, and a greedy last cell reads the rows of a
# THREE-column table written under this one as rows of this one --
# `templates/config.md` ships three-column tables.
#
# **This narrows in exactly one shape, and it is not a defect to repair.** A
# backslash standing immediately against a cell-ending pipe used to be a
# plain character followed by the delimiter; it is now one escaped pipe, so
# `| Broad gate | C:\Users\x\tools\|` is no longer a row. It cannot be both:
# the escape is what the rest of this comment is for. Nothing becomes
# unwritable, because `config_rows` strips each cell -- a space before the
# closing pipe returns the same value byte for byte. Found by round 1 of
# #415, where `plan.md` asserted that a widened pattern can only make MORE
# lines into rows; `spec.md` §*What this repair cannot see* now names it.
CELL = r"(?:[^|\\]|\\.)"
CONFIG_ROW = re.compile(
    rf"^\|\s*(?P<item>{CELL}+?)\s*\|\s*(?P<value>{CELL}*?)\s*\|\s*$"
)
CONFIG_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")

# A fenced code block's delimiter line, as CommonMark spells one: up to three
# spaces of indentation, then a run of three or more backticks or three or
# more tildes, then the info string. Four or more spaces is an indented code
# block instead and never a fence, which is why the bound is written into the
# pattern rather than checked after it.
#
# **Three or more, and tildes as well as backticks, is a decision with
# grounds.** This repository's own records wrap a fenced example in FOUR
# backticks -- #429's body and `rounds/round-3-report.md` both do -- and that
# is exactly the text somebody would paste into `config.md` to document the
# format. A rule that knew three backticks only would read the inner fence as
# the outer one's close and leave the live table inside a fence.
#
# The pattern lives in `hooks/blocks.py` since #667, which the routing reader
# and the rider check read as well; this name is that one.
FENCE = blocks.FENCE

# The one escape this reader undoes, spelled as the two characters it is.
ESCAPED_PIPE = "\\|"


def unescaped(cell):
    """CELL with markdown's escaped pipe reduced to one literal pipe.

    **Exactly those two characters, and no other backslash is touched.** A
    general unescape -- `re.sub(r"\\\\(.)", r"\\1", cell)` -- turns
    `C:\\Python\\python.exe -m pytest` into `C:Pythonpython.exe -m pytest`,
    and that row reads back with its path intact today, on a repository
    already synced across operating systems. Widening this would break a
    value nobody was asking us to change, to serve an escape markdown only
    needs for the pipe.

    The reduction happens HERE, before any caller sees the value, so a shell
    -- `/bin/sh` or `cmd.exe` -- is handed a plain `|` and never meets the
    backslash at all.
    """
    return cell.replace(ESCAPED_PIPE, "|")


def config_path(home):
    return os.path.join(home, CONFIG)


def fence_map(lines, text=None):
    """([(index, line)] outside every fenced block, the index of an opener
    that was never closed or None) -- the one fence rule, computed once.

    `unfenced` below is the generator form all three walks read the file
    through, and this is the same walk with the state it ENDS in kept. A fence
    that runs to the end of the file is the one thing about a fence a caller
    with somebody to tell has to be able to say: `broad-gate` quoting a live
    `| Broad gate |` row back as *written inside a code fence* and telling the
    person to move it into a table it is already in is a true sentence about a
    cause that is not the real one, which is the failure #429 was opened about
    arriving one shape over. A second fence rule written for that question is
    the split this module exists to prevent.

    Nothing here refuses and nothing acts on the second value. It is a fact
    about the file, for the one caller that has somebody to tell --
    `skills/verify/scripts/broad_gate.py#fence_left_open` -- exactly as
    `refusal` below is a fact about the table for the same caller.

    **The lines it hides are `hidden_lines`' below**, which reads the file
    through `hooks/blocks.py`'s walk (#667): a closed fence, and now a
    line-start HTML comment block that closes, hide their lines, and a line
    the walk cannot be sure of keeps the reading this function gave it before
    -- the fence rule alone. The name stays because every caller spells it,
    and "outside every fenced block" now means "outside every block this
    reader hides". TEXT is `hidden_lines`' argument of the same name.
    """
    hidden, opened_at = hidden_lines(lines, text)
    shown = [
        (index, raw.rstrip("\r\n"))
        for index, raw in enumerate(lines)
        if index not in hidden
    ]
    return shown, opened_at


def hidden_lines(lines, text=None):
    """({index: "fence" or "comment"} for every line of LINES no walk of the
    table is shown, the index of a fence opener never closed or None).

    **TEXT is the file LINES were split from, and every caller that has it
    passes it** (#667 round 1, 🟡 1). The readers split with
    `str.splitlines`, which ends a line at U+2028, NEL, a form feed and five
    more characters where a renderer does not; the walk reads TEXT where
    GFM breaks it (`blocks.walk_text`), so a `<!--` after such a character
    hides nothing. LINES alone is read as given, which is right for a list
    of lines nobody split from a file.

    **Two readings, and every line takes one of them** (#667, #658). Where
    `hooks/blocks.py#walk` is sure, the line is hidden exactly where a
    CommonMark renderer hides it: inside a fenced block or a line-start HTML
    comment block that closes. Where the walk is not sure -- a construct
    inside a list item, another kind of HTML block, the lines after inline
    raw HTML a line leaves open (a mid-line `<!--`, CDATA, a processing
    instruction, a declaration or a tag) and a piece of a line that starts
    inside it, everything below a construct that never closes -- the
    line keeps this reader's reading from before #667, the fence rule alone,
    `blocks.fence_only`. So on every line the answer is either the old one or
    the renderer's, and never a third; `tests/test_the_hooks_hide_what_a_
    renderer_hides.py` holds that over a generated corpus.

    What it means in a file:

      - a row parked in a comment that closes, above the table or inside it,
        is not a row (`COMMENTED_OLD_ROW`, `COMMENTED_OLD_TABLE`), which is
        the direction this module fails in: *nothing is declared*;
      - a fence line inside such a comment opens no fence, so a header
        comment quoting a fence no longer hides the live table under it;
      - **a fence that is never closed still hides everything below it**,
        because that is what it did before and a line below it is one the
        walk is not sure of. `broad-gate` names that fence
        (`broad_gate.py#fence_left_open`), and `seal mode` asks again;
      - a `<!--` nobody closed hides nothing it did not hide before, and
        switches off no fence below it: it is not a construct at all.

    **The second value** is the fence a caller has somebody to tell about:
    the first opener that never closes, on a line where the walk is not sure
    -- where the old reading, the one that runs such a fence to the end, is
    the one in force. A fence line inside a closed comment opens nothing, so
    it is never named.
    """
    walked = blocks.walk(lines) if text is None else blocks.walk_text(text)
    base, base_opened = blocks.fence_only(lines)
    hidden = walked.hidden(base)
    candidates = list(walked.unclosed)
    if base_opened is not None and walked.uncertain[base_opened]:
        candidates.append(base_opened)
    return hidden, min(candidates) if candidates else None


def unfenced(lines, text=None):
    """(index, line) for each of LINES that is outside every fenced code
    block and every HTML comment block that closes, with the line's own
    ending removed and its index kept. `hidden_lines` below is the rule and
    says which lines those are (#667); this paragraph and the ones after it
    were written for the fence half, and hold for the comment half word for
    word.

    **One fence rule, in front of all three walks of this table.** A line
    inside a fenced code block is not part of any `| Item | Value |` table:
    not a header, not a separator, not a row, and not a line somebody wrote as
    a row. `config_rows`'s walk below, `refusal`'s walk below that, and
    `skills/implement/scripts/seal.py#table_span` -- the WRITER's walk, which
    finds the line `with_row` overwrites -- all read the file through this
    one generator. A fence rule that landed in one of them and not another
    would leave the reader and the writer disagreeing about which row is the
    row, which is the file two rows deep that `table_span`'s own comment says
    no command can bring into agreement (#429).

    **Why a table inside a fence is not the table.** `config.md`'s header
    comment points its reader at `templates/config.md`, a document of EXAMPLE
    tables, and `skills/config/SKILL.md` §*Procedure* step 3 tells a session
    to copy a block of that template -- one holding a fenced
    `| Broad gate | ... |` row -- into the repository's own file, naming no
    position for it. So a fenced example above the live table, or above a
    table that has no parseable row yet, is a shape this plugin's own
    documented procedure produces; before this rule the example's rows were
    the rows every gate got, and the sealer's seal was taken over a command
    nobody chose.

    **It yields positions, not surviving text alone.** `table_span` returns
    indices into its caller's own `lines` and `with_row` overwrites one of
    them, so a helper handing back text could not serve that walk, and a
    second fence rule written for it is the split this module exists to
    prevent.

    **It takes either spelling of a line.** `config_rows` and `refusal` walk
    `text.splitlines()` and `table_span` walks `text.splitlines(keepends=True)`;
    the ending is stripped here, so all three get the same answer about the
    same file whether it is written with LF or CRLF.

    The edge cases past `spec.md`'s rule are resolved toward *not a fence*,
    which is the direction that keeps a live table readable:

      - a BACKTICK fence's info string may not itself hold a backtick
        (CommonMark 4.5), so ``` `x` ``` on its own line opens nothing and is
        an ordinary line of prose here. A tilde fence's info string is
        unrestricted, which is CommonMark's rule and not an exception to this
        one;
      - a closing run may be LONGER than the one that opened the block and
        may carry nothing after it but spaces. A run of the other character,
        or a run carrying an info string, is content inside the block;
      - an unclosed fence runs to the end of the file, so what it swallows
        lands on *nothing is declared* -- the direction everything in this
        module fails in, and loud where it matters: `broad-gate` exits 2 with
        a message and `seal mode` asks the mode question.

    A fence opens wherever its line stands, INCLUDING between two rows of a
    table, because this walk answers a question about the file and not about
    any one caller's state. The three walks hold different state at the same
    line, so a fence rule that consulted it would give them three answers.

    **The walk itself is `fence_map` above**, and this is its surviving lines.
    One walk rather than two: the caller that needs to know whether a fence
    was left open asks that function, and every walk of the table asks this
    one, and neither reads the file by a rule of its own. TEXT is
    `hidden_lines`' argument of the same name.
    """
    yield from fence_map(lines, text)[0]


def config_rows(text):
    """Every `| Item | Value |` row under the first such header, in order.

    The header and the separator are this table's own furniture ABOVE its
    first row and somebody else's table BELOW it; any other line ends the
    table. Both rules were arrived at over two review rounds of #82, in the
    copy of this loop that used to live in
    `tests/test_the_pull_request_language_is_the_repositorys.py` and now
    calls this one. Round 1 🟡 6: a row of a different SHAPE was skipped as
    though it were not there, so a `| a | b | c |` between two two-cell rows
    let the row after it be read as part of this table. Round 2 🟡 5: a
    header and a separator were stepped past wherever they appeared, so a
    stray separator or a second `| Item | Value |` header let the rows
    behind it be read as more of this one. A second reader that read the
    table differently would answer a different question about the same file,
    which is what this module exists to prevent.

    Each cell comes back with `\\|` reduced to one literal pipe and nothing
    else changed; `unescaped` above says why it is those two characters
    alone. The stop rule is unchanged, so a line a person wrote as a row
    still ends the table when it will not parse -- `refused_row` below is
    what names such a line, for a caller that has somebody to tell.

    **`unfenced` filters in FRONT of this walk and neither half of the stop
    rule moves.** Both halves were arrived at over those two rounds, and a
    repair that reached into the `if found: break` arms to special-case a
    fence is the regression this docstring predicts. What changed is which
    lines the walk is shown: a line inside a code fence is not shown to it at
    all, so an example table pasted above the live one is no longer this
    reader's table (#429).
    """
    found, seen_header = [], False
    for _index, line in unfenced(text.splitlines(), text):
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if found:
                break
            continue
        match = CONFIG_ROW.match(line)
        if not match:
            if found:
                break
            continue
        found.append(
            (
                unescaped(match.group("item").strip()),
                unescaped(match.group("value").strip()),
            )
        )
    return found


def refusal(text):
    """Everything a caller with somebody to tell needs about the lines a
    person wrote as rows of this table and this reader will not take as ones.

      refused  every such line, in order, each as (line, reached): the line
               as written with its own indentation, and whether the reader
               got that far before it stopped
      below    the rows written under the STOPPING line, which never arrived
      stopper  the refused line that ENDED the table, or None where no line
               ended it that way

    **Every value here is a fact about the TABLE, and that is the contract.**
    This used to hand back ONE line and a flat `ended` saying whether THAT
    line stopped the reader, and both callers then built sentences about the
    table out of it. The first refused line and the stopping line are the
    same line only while there is one of them. With two, the reader stops at
    the second while the answer describes the first, and #415's own defect
    came back in the unit that closed it, in both directions at once: the
    rows below were lost and the refusal said they were read, and a
    `Broad gate` row sitting under the second line was reported ABSENT
    (round 2 🟡 1). `refused` is a list for the same reason -- the line a
    caller is asking about may be neither the first nor the stopping one.

    **`stopper` is where the reader stopped and nothing else is.**
    `config_rows` breaks on a line it cannot parse only once it has FOUND a
    row; with nothing found yet it steps past that line and keeps reading,
    so every row below still arrives. A refusal that says those rows were
    lost sends a person to reformat rows that were read correctly -- a true
    sentence about the wrong file, which is the shape #415 was opened about
    (round 1 🟡 1). So `stopper` is None for a file whose refused lines all
    sit above its first parsed row, and `reached` is what tells a caller
    which side of the stopping place its own line is on.

    **It reports and it refuses nothing.** Nothing here raises, and no caller
    becomes able to deny by importing it: it answers a question two callers
    that already talk to a person want to ask, which is *why did that row not
    arrive*. `hooks/mode-gate.py` deliberately does not ask it -- a
    `PreToolUse` hook that refuses wrongly stops a session with nobody able
    to get past it, and everything in this module fails toward silence.

    **The walk is `config_rows`'s, and the one difference is that it reads
    ON past the stopping line**, because what lies under that line is
    exactly what a caller has to be told about. Nothing acts on those
    values, which is what lets the walk be that tolerant; a reader whose
    answers were acted on could not be.

    A line is a refusal only when it begins with a pipe once its indentation
    is stripped, which is how a person spells a row -- an indented row is
    still a row somebody wrote. A blank line or a paragraph of prose is the
    table's end rather than a refusal, and ABOVE the first parsed row it is
    neither: `config_rows` steps past it and reads on, so this walk does too,
    and it used to give up there instead -- which reported a refused row
    written under a line of prose as an absent row (#415 round 2, the
    correction). A second header or a stray separator ends the table once a
    row has been found, and the walk stops there rather than reaching into
    whatever table comes next (#415 round 1, the correction).

    Before this existed the two states were indistinguishable to a caller:
    `broad_gate` reported a piped `Broad gate` row as ABSENT, which is a true
    sentence about a cause that is not the real one (#415).

    **A fenced line is not a line somebody wrote as a row of this table.**
    This walk reads what `unfenced` shows it, exactly as `config_rows` above
    does, so a pipe-line inside a code fence reaches neither `refused` nor
    `below` and never becomes `stopper` -- which is what stops `broad-gate`'s
    refusal from quoting a line out of an example block back at a person as
    their own malformed row (#429). A caller that needs to speak about a
    fenced line asks its own question of the file; `broad_gate.py#fenced_row`
    is the one that does. A line inside an HTML comment block that closes is
    the same (#667): a malformed pipe-line somebody commented out is not
    quoted back as theirs, and `broad_gate.py#commented_row` is the question
    about it.
    """
    seen_header, found = False, False
    refused, below, stopper = [], [], None
    for _index, line in unfenced(text.splitlines(), text):
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if found:
                break
            continue
        match = CONFIG_ROW.match(line)
        if match:
            found = True
            if stopper is not None:
                below.append(
                    (
                        unescaped(match.group("item").strip()),
                        unescaped(match.group("value").strip()),
                    )
                )
            continue
        if not line.lstrip().startswith("|"):
            if found:
                break
            continue
        refused.append((line, stopper is None))
        if found and stopper is None:
            stopper = line
    return refused, below, stopper


def refused_row(text):
    """The first refused line alone -- `refusal` above is the whole answer,
    and its docstring is where this one's reasoning lives."""
    refused = refusal(text)[0]
    return refused[0][0] if refused else None


def declared_mode(home):
    """(kind, value) for the `Mode` row — what the repository SAYS it wants.

      "none"     nothing is declared: no file, no such row, an empty value,
                 or a file that does not parse as that table. Four spellings
                 of one state, the same four the pull-request-language row
                 has for not naming a language
      "mode"     `local` or `shared`, lowercased
      "unknown"  a row is there and its value is not a mode — a claim nobody
                 can act on, which is not the same as no claim

    **There is no default.** Every other item in `config.md` falls back to
    what every repository got before the row existed; for the mode that is
    *the folder decides*, so an absent row is filled in from the folder by
    `seal mode` rather than assumed here. A default of `shared` would report
    every undeclared local-mode repository as lying.
    """
    try:
        with open(config_path(home), encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, ValueError):
        # Unreadable is one of the four, not a failure: `IsADirectoryError`
        # and a file this locale cannot decode both land here, and neither is
        # a reason to stop answering where the folder is.
        return "none", ""
    for item, value in config_rows(text):
        if item == ROW_ITEM:
            lowered = value.lower()
            if not lowered:
                return "none", ""
            return ("mode", lowered) if lowered in MODES else ("unknown", value)
    return "none", ""
