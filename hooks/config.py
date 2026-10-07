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

Everything here fails toward "nothing is declared" -- except where a written
row would be read as absent. A file that is there and cannot be read, and a
row written twice, are refused by `config_text` and `config_value` rather than
read as nothing (#867); a hook reads a refusal as nothing it can act on and
says nothing, and a command prints it and exits 2. `config_text`'s docstring
says which caller is which kind.
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

    **The walk is `indexed_config_rows` below, and this is its rows without
    their places** (#759). The pact reader needs to know WHICH line each row
    came from, and a second walk written for that question would be a second
    stop rule to keep in step with this one.
    """
    return [(item, value) for _index, item, value in indexed_config_rows(text)]


def indexed_config_rows(text):
    """`config_rows`' rows as (index, item, value), the index being the row's
    line in `text.splitlines()`. `config_rows` is this walk's projection, and
    its docstring is where the stop rule's reasoning lives.

    The index is what lets `pact_lines_not_read` tell a line this walk took
    as a row from every other line of the file (#759).
    """
    found, seen_header = [], False
    for index, line in unfenced(text.splitlines(), text):
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
                index,
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


def config_text(home):
    """(text, refusal) for `<home>/config.md` — the one place the file is
    opened, and the one place an absent file is told from an unreadable one.

      (None, None)     there is no file at that name: nothing is declared
      (text, None)     the file, read as UTF-8
      (None, refusal)  the file is there and cannot be read as text -- a
                       directory of that name, a permission this process
                       does not have, bytes that do not decode -- and
                       REFUSAL is a sentence naming the path and why

    **Two states, and only the second is refused** (#867). An absent file is
    what every repository had before it wrote a row, so it declares nothing,
    everywhere. A file that is there and will not read is not a repository
    that answered nothing: it is one whose answer nobody can read. What a
    caller does with that is its own kind's call, and every caller asks this
    reader rather than opening the file a second time to find out:

      - a hook that may not stop -- `hooks/mode-gate.py`,
        `hooks/evidence-advisor.py` -- reads a refusal as nothing it can act
        on and says nothing, because a gate that refuses wrongly is an outage
        nobody can get past (`CONTRIBUTING.md` §*What a change to a gate must
        carry*);
      - a command a person runs prints the sentence and exits 2 with nothing
        judged, the shape a non-numeric `Ledger frozen from` already takes
        (`templates/config.md` §*The ledger freeze*), because a command that
        reads a written row as absent turns the freeze off on a decode error.

    HOME is the seal root; a falsy one is no file. A name that `lexists` but
    will not open -- a symbolic link to nowhere -- is the second state: the
    name is there."""
    if not home:
        return None, None
    path = config_path(home)
    if not os.path.lexists(path):
        return None, None
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read(), None
    except (OSError, ValueError) as exc:
        return None, unreadable_config(path, exc)


def unreadable_config(path, exc):
    """The sentence `config_text` refuses an unreadable PATH in. It opens
    with the path and ends with no full stop, so it reads after a command's
    own prefix."""
    why = exc.strerror if isinstance(exc, OSError) and exc.strerror else str(exc)
    return (
        f"{path} is there and cannot be read as UTF-8 text ({why}), so no row "
        "of it can be read — a config that is absent declares nothing, and "
        "one that will not read is refused rather than read as absent"
    )


def doubled_row(item, count):
    """The sentence `config_value` refuses a row written COUNT times in. It
    is the sentence `pact_declaration` has refused a doubled `Pact notify`
    in since round 1 of PR #756, made the one sentence for every item."""
    return f"`{item}` appears {count} times — one value"


def config_value(text, item):
    """(value, refusal) for ITEM in the `| Item | Value |` table of TEXT —
    the one answer every reader of one config row gives (#867).

      (None, None)     no row names ITEM, or TEXT is None (no file)
      (value, None)    one row: its value, stripped and unescaped as
                       `config_rows` returns it, "" where it is empty
      (None, refusal)  ITEM is written more than once, and REFUSAL says so

    **A row written twice has no value**, not its first and not its last.
    `pact_declaration` refused a doubled `Pact notify` with *its first row is
    not the answer* (round 1 of PR #756, yellow 2) and `docs/the-pact.md`
    ratified it; every other reader here took the first, the checker took
    the last, and `seal mode` wrote the first. Three answers to one file is a
    file a person edits on the row they see while another one answers. So
    the one answer is a refusal, and what a caller does with it is its own
    kind's -- `config_text` says which kind does which.

    The rows are `config_rows`', so a row is a row only where that walk takes
    it: one written below the table's end, in a fence or in a closed comment
    is not counted, which is what keeps a fenced example from doubling the
    live row."""
    if text is None:
        return None, None
    return value_of(config_rows(text), item)


def value_of(rows, item):
    """`config_value` over ROWS already walked, as `(item, value)` pairs --
    the rule itself, for a caller that holds the rows and would otherwise
    walk the file once per item (`pact_declaration`)."""
    values = [value for found, value in rows if found == item]
    if len(values) > 1:
        return None, doubled_row(item, len(values))
    return (values[0], None) if values else (None, None)


def declared_value(home, item):
    """(value, refusal) for ITEM in `<home>/config.md`: `config_text`, then
    `config_value`, so an unreadable file and a doubled row reach the caller
    the same way -- as a refusal it acts on by its own kind."""
    text, refusal = config_text(home)
    if refusal is not None:
        return None, refusal
    return config_value(text, item)


def declared_mode(home):
    """(kind, value) for the `Mode` row — what the repository SAYS it wants.

      "none"     nothing is declared: no file, no such row, an empty value,
                 or a file that does not parse as that table. Four spellings
                 of one state, the same four the pull-request-language row
                 has for not naming a language
      "mode"     `local` or `shared`, lowercased
      "unknown"  a row is there and its value is not a mode — a claim nobody
                 can act on, which is not the same as no claim
      "refused"  the file is there and will not read, or the row is written
                 more than once; VALUE is `declared_value`'s sentence

    **There is no default.** Every other item in `config.md` falls back to
    what every repository got before the row existed; for the mode that is
    *the folder decides*, so an absent row is filled in from the folder by
    `seal mode` rather than assumed here. A default of `shared` would report
    every undeclared local-mode repository as lying.

    **`refused` is not `none`** (#867). An unreadable file used to fold into
    `none`, and `hooks/mode-gate.py` opened the file a second time to tell
    the two apart. A doubled row was read first-wins here and by the writer.
    Now the reader tells them apart once: the gate says nothing on a refusal,
    and `seal mode` prints it and writes nothing, because writing a row into
    a file whose rows disagree, or that nobody can read, cannot make it
    agree.
    """
    value, refusal = declared_value(home, ROW_ITEM)
    if refusal is not None:
        return "refused", refusal
    lowered = (value or "").lower()
    if not lowered:
        return "none", ""
    return ("mode", lowered) if lowered in MODES else ("unknown", value)


# --- the reference roots (#688) -------------------------------------------
#
# A project may have kept its own `specs/` before the plugin arrived. The
# plugin writes only to its own root and reads every other directory named
# `specs` as history: a REFERENCE ROOT, read when a change touches what it
# describes and never moved, edited, absorbed or deleted. The checks that read
# a record ask `under_reference_root` before they read a path, so none of them
# carries a test of its own (`templates/config.md` §*Reference specs*).

REFERENCE_ROW = "Reference specs"
NO_REFERENCE = "none"
# The directory name the default reads as a reference root at any depth.
REFERENCE_NAME = "specs"
# The plugin's own root in the tree, `hooks/optin.py#HOME`. Spelled here so
# this reader needs no second sibling, and held equal to that one by
# `tests/test_a_reference_root_is_read_and_never_taken.py`.
HOME = "seal"


def inside_the_root(rel):
    """True when the `/`-joined repository-relative `rel` is the plugin's own
    root or under it — never a reference root, whatever a row says."""
    return rel == HOME or rel.startswith(HOME + "/")


def reference_roots(home):
    """The repository-relative directories `<home>/config.md`'s
    `Reference specs` row names, as a tuple; `()` for `none`; or None, the
    default — every directory named `specs` outside the plugin's root.

    The value is comma-separated prefixes, each with or without a trailing
    `/` or a leading `./`. No file, no such row, an empty value or a file
    that will not read all mean the default, which is what every repository
    got before the row existed. A prefix naming the plugin's own root or
    anything under it is dropped: a reference root is outside the root by
    definition, and the root's records are read whatever the row says.

    **No root at either place is `()`, no reference root at all** — not the
    default. A reference root is defined against the plugin's root, and a
    repository with none has not opted in: the one layout the plugin ever
    read without a root is 0.3.x, whose top-level `specs/` was the plugin's
    own, and the survivor sweep's pool and range and `unverified-check` still
    read that spelling as its records — `survivor_check.py#WORK_ITEM_DIR`
    alone no longer does, so a top-level `specs/<x>/` is never a retired
    work item there. A person
    joining a project runs the bootstrap, which creates the root, before any
    check reads the tree.

    **A refusal reads as the default** (#867): a file that will not read, as
    before, and a `Reference specs` row written twice, which `config_value`
    gives no value. Its two callers, `unverified-check` and the survivor
    sweep, are not among the commands `config_text` names as refusing: what
    a refusal costs them is the reading every repository had before the row
    existed, and no record is written or lost on it."""
    if not home:
        return ()
    value, refusal = declared_value(home, REFERENCE_ROW)
    if refusal is not None or not value:
        return None
    if value.lower() == NO_REFERENCE:
        return ()
    out = []
    for entry in value.split(","):
        prefix = entry.strip().replace("\\", "/")
        while prefix.startswith("./"):
            prefix = prefix[2:]
        prefix = prefix.strip("/")
        if prefix and not inside_the_root(prefix) and prefix not in out:
            out.append(prefix)
    return tuple(out)


def under_reference_root(rel, roots):
    """True when the repository-relative path `rel` is a reference root or
    under one. `roots` is `reference_roots`' answer: None reads the default —
    any directory named `specs` on the path, outside the plugin's root — and
    a tuple reads its prefixes alone.

    A predicate on a TREE path, so local mode needs no arm of its own: its
    root is under the git directory and never in the tree, and every `specs`
    the tree holds is outside it."""
    parts = [p for p in rel.replace("\\", "/").split("/") if p and p != "."]
    if not parts or inside_the_root(parts[0]):
        return False
    if roots is None:
        return REFERENCE_NAME in parts
    joined = "/".join(parts)
    return any(joined == p or joined.startswith(p + "/") for p in roots)


# --- the pact a signer declares (#647) -------------------------------------
#
# A work item can commit in more than one repository, and where those
# repositories keep one contract together, the one copy of it is the PACT:
# `seal/pact.md` in the repository that holds it. Every repository of such a
# work item is a SIGNER, the pact's repository included. A signer other
# than the pact's repository names the pact here, by the origin remote URL of
# the repository that holds it, and the pact's repository needs no row: it is
# identified by holding `seal/pact.md` (`docs/the-pact.md`).
#
# Two readers ask these rows and they ask THIS reader:
# `skills/code-review/scripts/chain_check.py`, which prints the relationship
# at a signer's pull request and refuses nothing, and
# `skills/evidence-check/scripts/pact_check.py`, which reads every signer
# from the pact's repository and refuses what will not parse. One reader, so
# the print and the refusal are about the same rows.

PACT_ROW = "Pact"
PACT_NOTIFY_ROW = "Pact notify"
# The separator `Over the ceiling` already uses between its entries.
PACT_SEPARATOR = ";"
# What a signer asks to be told about a change to the pact: which of its
# re-reads `evidence-check --reverify` records as pact changes, and which of
# those `pact-check` reads (#647, steps C and D; `docs/the-pact.md`).
NOTIFY_ALWAYS = "always"
NOTIFY_TOUCHED = "when the pact is touched"
NOTIFY_NEVER = "never"
NOTIFY_VALUES = (NOTIFY_ALWAYS, NOTIFY_TOUCHED, NOTIFY_NEVER)
# #647 recommended it and decided nothing; the frame took it, and
# `docs/the-pact.md` states it.
NOTIFY_DEFAULT = NOTIFY_TOUCHED
# A pact's name in an anchor, `pact:<name>/"<heading path>"@<hash>`: the last
# path segment of the pact's repository's normalised origin URL. The class is
# `evidence_check.py#PACT_NAME`'s, which reads the anchor.
PACT_NAME_RE = re.compile(r"[A-Za-z0-9_.-]+")
# The word a line names a pact by: the letters `p`, `a`, `c`, `t` in that
# order, any case, with any run of characters that are not letters between
# two of them, and no letter before the `p` (#759). "Not letters between" is
# what reads emphasis, a code span, a character reference, a format
# character or a pipe inside the word as nothing, without parsing any of
# them; the look-behind is what keeps `impact` and `compact` silent.
# `evidence_check.py#PACT_WORD` is its copy, held equal by
# `tests/test_a_signer_declares_its_pact.py`.
PACT_WORD = re.compile(r"(?<![^\W\d_])p[\W\d_]*a[\W\d_]*c[\W\d_]*t", re.I)
# An HTML table cell's opening tag, `<td` or `<th`, any case. GFM passes raw
# HTML through and a renderer shows such a cell, which carries a value with
# no `|` beside it, so in a file holding one every line naming a pact is read
# without the pipe condition (round 1 of PR #793, yellow 2). A token, not a
# grammar: it fails closed, refusing more where it is wrong.
# `evidence_check.py#HTML_CELL` is its copy, held equal by
# `tests/test_a_signer_declares_its_pact.py`.
HTML_CELL = re.compile(r"<t[dh][\s/>]", re.I)
# A line GFM may read as the delimiter row under a table's header, wider than
# `DELIMITER_ROW` on purpose and fail-closed: block-quote markers and any
# whitespace before it, a vertical tab or form feed where a space stands,
# and no pipe at all, because a one-column table needs none. A run of
# dashes alone is a setext underline or a thematic break and is left out.
# The line directly above one is a header, whose cells carry the values
# below them, so it is read whole and needs no `|` (round 3 of PR #793).
# `evidence_check.py#UNDER_A_HEADER` is its copy, held equal by
# `tests/test_a_signer_declares_its_pact.py`, which holds both readers to
# every table cmark-gfm renders over a constructed delimiter row.
UNDER_A_HEADER = re.compile(
    r"^(?![ \t>]*-+[ \t]*$)[\s>]*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$"
)


def names_a_pact(text, piped=True):
    """True where TEXT names a pact: `PACT_WORD` finds the word in TEXT as
    written, or in TEXT decoded -- `html.unescape`, then NFKC. Where PIPED,
    TEXT must also hold a `|`, as written or decoded.

    **Both readings, as a union, so the decode can only add.** It decodes
    more than CommonMark does (a legacy name with no `;`), and that costs
    nothing here: `Pact&notify` names a pact as written, whatever the decode
    makes of it (round 4 of PR #784, yellow 3).

    **The pipe is the one structural condition, and it is not a grammar.** A
    GFM table row's cells are separated by pipes, so a line with none is one
    cell at most and carries no value: a pact row with no value is the
    default this reader already reads. cmark-gfm was measured to give such a
    line an empty second cell (Q2 of the work item). So a signer may name
    its pact in prose or a comment of its own `config.md` and is not refused.

    `evidence_check.py#names_a_pact` is its copy, held equal by
    `tests/test_a_signer_declares_its_pact.py`. The two imports are here
    rather than at the top because a `PreToolUse` hook loads this module and
    never reads a pact."""
    import html
    import unicodedata

    decoded = unicodedata.normalize("NFKC", html.unescape(text))
    if piped and "|" not in text and "|" not in decoded:
        return False
    return bool(PACT_WORD.search(text) or PACT_WORD.search(decoded))


def normalise_remote(url):
    """A remote URL reduced to host and path, so two spellings of one
    repository compare equal.

    `git@example.com:org/repo.git` and `https://example.com/org/repo` are one
    repository, and ssh at one machine with https at another is the ordinary
    case — comparing the strings would refuse every real import.

    The scheme goes, a `user@` prefix goes, the scp-style `host:path` colon
    becomes `/` **only where there was no scheme** (so the port in
    `https://example.com:8443/x` is left alone), a trailing `.git` and `/` go,
    and the result is lowercased.

    Wrong in the accepting direction would need two different repositories to
    reduce to the same host and path, which is the same repository. Wrong in
    the refusing direction costs a message naming `--allow-other-repo`. That
    asymmetry is why this is done at all.

    Anything that is not text reduces to "", because one caller passes a field
    out of a manifest another machine wrote. `read_manifest` checks that the
    manifest is an object and that its `format` is one this build reads; every
    other field is whatever the zip says, and a list here used to reach the
    console as an `AttributeError`.

    **It lives here and `skills/implement/scripts/seal.py` re-exports it**
    (#647), the arrangement this module's docstring records for the `Mode`
    reader. The `Pact` reader below needs it, and this module cannot import
    `seal.py`: that file imports this one, and a hook must not load a
    two-thousand-line command to read a row. One normaliser, reached by the
    name each caller already spells.
    """
    if not isinstance(url, str):
        return ""
    text = url.strip()
    if not text:
        return ""
    schemed = "://" in text
    if schemed:
        text = text.split("://", 1)[1]
    authority = text.split("/", 1)[0]
    if "@" in authority:
        text = text.split("@", 1)[1]
    if not schemed and ":" in text:
        text = text.replace(":", "/", 1)
    text = text.rstrip("/")
    if text.endswith(".git"):
        text = text[: -len(".git")]
    return text.lower()


def pact_name(remote):
    """The name a pact anchor gives the pact held at REMOTE: the last path
    segment of its normalised URL, or "" where it has no path."""
    normalised = normalise_remote(remote)
    if "/" not in normalised:
        return ""
    return normalised.rsplit("/", 1)[1]


def remote_entries(entries, empty, named):
    """(parsed, refusals) for ENTRIES, each a remote URL as somebody wrote
    it: `parsed` as `(as written, normalised, name)` in order, and one
    sentence per entry refused, EMPTY being the sentence for an empty one.

    NAMED is true where the name is what an anchor will carry -- the
    `Pact` row's entries -- so a name outside `PACT_NAME_RE`, and two entries
    sharing a name, are refused as well. A pact's `Signer` table lists
    repositories nobody cites by name, and two of them may end in one
    segment. Two entries naming one repository are refused either way.
    """
    parsed, refusals, seen, names = [], [], {}, {}
    for entry in entries:
        written = entry.strip()
        if not written:
            refusals.append(empty)
            continue
        if any(ch.isspace() for ch in written):
            refusals.append(f"`{written}` holds a space — one remote URL per entry")
            continue
        normalised = normalise_remote(written)
        name = pact_name(written)
        if not name:
            refusals.append(
                f"`{written}` is not a remote URL — it reduces to no host and "
                "path, so no repository can be found by it"
            )
            continue
        if normalised in seen:
            refusals.append(f"`{written}` and `{seen[normalised]}` are one repository")
            continue
        if named and not PACT_NAME_RE.fullmatch(name):
            refusals.append(
                f"`{written}` ends in `{name}`, which a pact anchor cannot "
                "name — the name takes letters, digits, `_`, `.` and `-`"
            )
            continue
        if named and name in names:
            refusals.append(
                f"`{written}` and `{names[name]}` both end in `{name}`, so an "
                f"anchor `pact:{name}/…` cannot say which pact it cites"
            )
            continue
        seen[normalised] = names[name] = written
        parsed.append((written, normalised, name))
    return parsed, refusals


def pact_declaration(text):
    """(pacts, notify, refusals) for the `Pact` rows of a config.md's TEXT.

      pacts     [(as written, normalised, name)] for every entry of the
                `Pact` row that parsed, in the order the row lists them;
                [] where no row names a pact
      notify    the `Pact notify` value, lowercased; `NOTIFY_DEFAULT` where a
                `Pact` row stands with no `Pact notify`; None where no
                `Pact` row does, because the notify row is then ignored, and
                None where the row is refused, outside the vocabulary or
                written more than once, and None where a line naming a pact
                is not a pact row in the one spelling read
      refusals  one sentence per thing that would not parse, naming it

    **It refuses in sentences and stops nothing.** The two callers differ on
    exactly that, and the difference is #647's decision 2: a signer's CI
    prints a refusal as a notice and its exit status does not move, while
    `pact-check`, run at the pact's repository, exits 2 on one.

    No row, an empty value, and a file with no table are one state, *no pact
    is held elsewhere* — the direction everything in this module fails in. A
    value that is there and does not parse is not that state, and it is
    refused rather than read as absent: a signer that wrote a row and is
    read as having written none is the silence this reader exists to end.

    **A pact row is read in one spelling, and every other line naming a pact
    is refused** (#759). A `| Pact notify | always |` written where the
    table walk does not take it was read as the default, and under `always`
    `evidence-check --reverify` then re-stamped a moved row citing no clause
    with no record -- the re-stamp clears the drift that was the only
    trigger for the record. `pact_lines_not_read` names every such line, and
    each is refused with `notify` None. This reader alone refuses where the
    others fail silent, and only for these two rows: no other row's default
    loses a record that cannot be recovered.
    """
    rows = indexed_config_rows(text)
    pairs = [(item, value) for _i, item, value in rows]
    # A row written twice has no value, by `value_of`'s rule and in its
    # sentence (#867): the first row is not the answer, so a caller that read
    # it would rule `always` in or out on a row the signer also contradicted
    # (round 1 of PR #756, yellow 2) -- and a doubled `Pact` lists no pact.
    value, doubled_pact = value_of(pairs, PACT_ROW)
    written, doubled_notify = value_of(pairs, PACT_NOTIFY_ROW)
    refusals = [doubled_pact] if doubled_pact else []
    not_read = pact_lines_not_read(text, rows)
    # Where a line is refused only because the file holds an HTML table
    # cell's tag, the sentence says so (round 2 of PR #793, yellow 2).
    cell = HTML_CELL.search(text) is not None
    refusals.extend(
        pact_line_refusal(line, cell and not names_a_pact(line)) for line in not_read
    )
    if not value:
        return [], None, refusals
    pacts, refused = remote_entries(
        value.split(PACT_SEPARATOR),
        f"`{PACT_ROW} | {value}` holds an empty entry — one remote URL between "
        f"each `{PACT_SEPARATOR}`",
        named=True,
    )
    refusals.extend(refused)
    if doubled_notify:
        refusals.append(doubled_notify)
        return pacts, None, refusals
    notify = " ".join((written or "").split()).lower()
    if not notify:
        notify = NOTIFY_DEFAULT
    elif notify not in NOTIFY_VALUES:
        refusals.append(
            f"`{PACT_NOTIFY_ROW} | {written}` is not one of "
            + ", ".join(f"`{v}`" for v in NOTIFY_VALUES)
        )
        notify = None
    if not_read:
        # The line this reader does not read may be the one that says
        # `always`, so no value read from the table is the answer (#759).
        notify = None
    return pacts, notify, refusals


def pact_lines_not_read(text, rows):
    """Every line of TEXT that names a pact and is not a pact row in the one
    spelling read, as written and in file order. ROWS is
    `indexed_config_rows(text)`.

    **A line is one GFM line** (`blocks.gfm_lines`), the coarsest cut any
    reader here makes, so a word can only be whole on it where it is whole on
    a finer one. Each line is one of two cases:

      - **the walk took it whole as a row**: it holds no character only
        `str.splitlines` ends a line at, and its one piece is a row of ROWS.
        Its ITEM alone is read. `Pact` and `Pact notify`, byte for byte, are
        the spelling read; any other item that names a pact is refused,
        piped or not. Its value is not read, so a `Broad gate` row running
        `-k pact` stays silent;
      - **every other line**: read whole, and refused where it names a pact
        and holds a `|` (`names_a_pact`). That is a line below the table's
        end, in a second table, a block quote, a fence or a comment, and a
        line a `str.splitlines`-only character cuts, even where each of its
        pieces would be a row. In a file holding an HTML table cell
        (`HTML_CELL`) the `|` is not asked for, because such a cell carries
        a value with no pipe beside it, and nor is it of a line directly
        above one `UNDER_A_HEADER` matches: a table's header, whose value
        stands in the row below (round 3 of PR #793).

    **Fences and comments are read through, on purpose.** Exempting them
    would make the refusal depend on `hidden_lines` matching GFM's block
    grammar, which is the modelling this reader gave up, and an unclosed
    fence there hides everything below it. An example there refuses, which is
    the loud direction: the person deletes the example. The walk still does
    not read it, so it is refused and never read.

    **No GFM is modelled.** #784 emulated what GFM renders as the item, and
    four review rounds each found spellings the emulation missed. Here
    nothing is rendered: a line names a pact or it does not.
    """
    taken = {index: item for index, item, _value in rows}
    piped = HTML_CELL.search(text) is None
    found, first = [], 0
    wholes = blocks.gfm_lines(text, keepends=True)
    for at, whole in enumerate(wholes):
        pieces = len(whole.splitlines())
        index, first = first, first + pieces
        line = whole.rstrip("\r\n")
        under = wholes[at + 1].rstrip("\r\n") if at + 1 < len(wholes) else ""
        header = UNDER_A_HEADER.match(under) is not None
        if pieces == 1 and index in taken:
            item = taken[index]
            if item not in (PACT_ROW, PACT_NOTIFY_ROW) and names_a_pact(
                item, piped=False
            ):
                found.append(line)
        elif names_a_pact(line, piped and not header):
            found.append(line)
    return found


def pact_line_refusal(line, cell=False):
    """The sentence a line `pact_lines_not_read` names is refused in. It
    quotes LINE stripped, with every whitespace character other than a space
    and every format character (Unicode category Cf) shown as its code
    point, because the character that cut the line or spelled the item
    another way is otherwise invisible in the sentence that names it. It
    opens lower-case and ends with no full stop, so it reads after each
    caller's prefix: `chain-check`'s, `pact-check`'s `REFUSED` line, and the
    writer's `LEFT` line. CELL is true where LINE holds no `|` and is refused
    only because the file holds an HTML table cell's tag (`HTML_CELL`), and
    then the sentence names that cause, because the line alone shows none
    (round 2 of PR #793, yellow 2)."""
    import unicodedata

    shown = "".join(
        f"<U+{ord(ch):04X}>"
        if (ch.isspace() and ch != " ") or unicodedata.category(ch) == "Cf"
        else ch
        for ch in line.strip()
    )
    return (
        f"`{shown}` names a pact and is not a `{PACT_ROW}` or "
        f"`{PACT_NOTIFY_ROW}` row in the one spelling read: write it as "
        f"`| {PACT_ROW} | … |` or `| {PACT_NOTIFY_ROW} | … |` inside the "
        "`| Item | Value |` table, or take it out of this file"
    ) + (
        "; this file holds an HTML table cell's tag, so a line with no `|` is "
        "refused too"
        if cell
        else ""
    )


def declared_pacts(home):
    """`pact_declaration` over `<home>/config.md`, or None where that file
    is there and will not read.

    **Not the rule the other readers here keep**, and on purpose (round 1 of
    #647, white 5). They answer an unreadable file as no row, because a gate
    that refuses wrongly stops a session with nobody able to get past it.
    This reader's caller is `pact-check`, run by a person at the pact's
    repository, and a signer whose written rows read as absent is the
    silence `pact_declaration` exists to end. So no file is no row, and a
    file that will not read is None, which `pact-check` refuses as
    `UNREADABLE`.

    Since #867 every command reading a row takes this reader's side, and
    `config_text` is where the two states are told apart for all of them;
    this is that answer in the shape `pact-check` has always read."""
    text, refusal = config_text(home)
    if refusal is not None:
        return None
    if text is None:
        return [], None, []
    return pact_declaration(text)


# --- one GFM table walker (#647, steps C and D) -----------------------------
#
# Three tables are read out of markdown by name: the pact's `| Signer |`,
# a signer's record of pact changes, and the pact's record of pact
# reviews. One walker reads all three, because three walkers are three break
# lists to keep in step, and round 3 of #735 measured exactly that drift in
# the one there was: an autolink row ended the table, and a signer written
# as one was read by nobody at exit 0.
#
# **It reads what cmark-gfm renders, or refuses.** It is held to the renderer
# by `tests/test_one_table_walker_reads_what_gfm_renders.py`, a property case
# over a corpus enumerated from the CommonMark and GFM block kinds: on every
# shape the walker's cells equal cmark-gfm's, or the walker refuses. So every
# arm below is one of two kinds. An END is a line the renderer was measured to
# end the table at; a ROW is a line written `| … |` with the header's width.
# Anything else is refused, with what it is, because a line the renderer reads
# as a row and the walker reads as an end is a row nobody reads.

# A line that ends a GFM table, after at most three spaces of indentation (a
# fourth column is an indented code block, which ends it too). The HTML block
# starts are CommonMark 4.6's seven kinds, measured against cmark-gfm one tag
# name at a time; an autolink, `<https://…>`, is not one of them, and the
# renderer reads it as one of the table's rows.
ATX_HEADING = re.compile(r"#{1,6}(?:[ \t]|$)")
THEMATIC_BREAK = re.compile(r"(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
BLOCK_QUOTE = re.compile(r">")
LIST_ITEM = re.compile(r"(?:[-+*]|[0-9]{1,9}[.)])(?:[ \t]|$)")
HTML_KINDS = (
    # 1: a raw-text element, ended by its closing tag.
    (
        re.compile(r"<(?:script|pre|style|textarea)(?:[ \t>]|$)", re.I),
        re.compile(r"</(?:script|pre|style|textarea)>", re.I),
    ),
    # 2-5: a comment, a processing instruction, a declaration, CDATA.
    (re.compile(r"<!--"), re.compile(r"-->")),
    (re.compile(r"<\?"), re.compile(r"\?>")),
    (re.compile(r"<![A-Za-z]"), re.compile(r">")),
    (re.compile(r"<!\[CDATA\["), re.compile(r"\]\]>")),
    # 6: a block-level tag name, open or closing; ended by a blank line.
    (
        re.compile(
            r"</?(?:address|article|aside|base|basefont|blockquote|body|caption"
            r"|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset"
            r"|figcaption|figure|footer|form|frame|frameset|h1|h2|h3|h4|h5|h6"
            r"|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem"
            r"|nav|noframes|ol|optgroup|option|p|param|section|source|summary"
            r"|table|tbody|td|tfoot|th|thead|title|tr|track|ul)(?:[ \t>]|/>|$)",
            re.I,
        ),
        None,
    ),
    # 7: any other whole open or closing tag alone on its line.
    (
        re.compile(
            r"(?:<[A-Za-z][A-Za-z0-9-]*"
            r"(?:[ \t]+[A-Za-z_:][A-Za-z0-9_.:-]*"
            r"(?:[ \t]*=[ \t]*(?:[^ \t\"'=<>`]+|'[^'\n]*'|\"[^\"\n]*\"))?)*"
            r"[ \t]*/?>|</[A-Za-z][A-Za-z0-9-]*[ \t]*>)[ \t]*$"
        ),
        None,
    ),
)
# A delimiter row: one `:?-+:?` per cell, a pipe somewhere in it (a bare `---`
# under a line is a setext heading, and GFM renders no table there), at most
# three spaces of indentation and no tab before it.
DELIMITER_ROW = re.compile(
    r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$"
)
# A row written `| … |`, at most three spaces in; its cells are split by
# every pipe `CELL` does not hold, so an escaped pipe stays inside its cell.
TABLE_ROW = re.compile(rf"^ {{0,3}}\|(?P<cells>(?:{CELL}|\|)*)\|[ \t]*$")
CELL_PIPE = re.compile(rf"((?:{CELL})*)(\|?)")
# A pipe after an even run of backslashes: `CELL` reads the backslashes in
# pairs and splits there, and cmark-gfm does not, because its cell scanner
# reads `\|` as an escaped pipe wherever it stands (round 1 of PR #749,
# white 6). A line holding one is no row this walker reads.
EVEN_ESCAPED_PIPE = re.compile(r"(?<!\\)(?:\\\\)+\|")


def table_cells(line):
    """The cells of LINE as a tuple, each stripped and with `\\|` reduced to a
    pipe, where LINE is written `| … |`; otherwise None, which is also the
    answer for a line holding a pipe after an even run of backslashes, which
    cmark-gfm splits differently (`EVEN_ESCAPED_PIPE`)."""
    match = TABLE_ROW.match(line)
    if not match or EVEN_ESCAPED_PIPE.search(line):
        return None
    cells = []
    for piece in CELL_PIPE.finditer(match.group("cells")):
        cells.append(unescaped(piece.group(1).strip()))
        if not piece.group(2):
            break
    return tuple(cells)


def html_start(content):
    """`(kind, end)` for the HTML block CONTENT begins -- CONTENT being the
    line past its indentation -- where `kind` is CommonMark 4.6's condition
    number and `end` the pattern that ends the block, None for the two kinds
    a blank line ends; `(None, None)` where CONTENT begins none."""
    for number, (start, end) in enumerate(HTML_KINDS, 1):
        if start.match(content):
            return number, end
    return None, None


def table_end(line):
    """Why LINE ends a GFM table above it, or None where cmark-gfm reads it as
    one of the table's rows (or the walker cannot say which, and refuses)."""
    if not line.strip():
        return "a blank line"
    if blocks.columns(line) >= 4:
        return "an indented code block"
    content = line.lstrip(" ")
    if ATX_HEADING.match(content):
        return "a heading"
    if THEMATIC_BREAK.match(content):
        return "a thematic break"
    if BLOCK_QUOTE.match(content):
        return "a block quote"
    if LIST_ITEM.match(content):
        return "a list item"
    if html_start(content)[0]:
        return "an HTML block"
    return None


def raw_html_open(lines):
    """True where an HTML block of CommonMark 4.6's kinds 1-5 -- the kinds no
    blank line ends -- is still open after LINES, so everything under it is
    the block's raw text and GFM renders no table there (round 1 of PR
    #749, yellow 5)."""
    end = None
    for line in lines:
        if end is not None:
            if end.search(line):
                end = None
            continue
        if blocks.columns(line) >= 4:
            continue
        content = line.lstrip(" ")
        number, closer = html_start(content)
        if number is not None and number <= 5 and not closer.search(content, 1):
            end = closer
    return end is not None


def a_list_above(lines):
    """True where a list item stands in LINES since the last heading or
    thematic break at the start of a line, so an indented header under it
    can be more of that item: a blank line does not end a list item, and the
    header's indent decides (round 2 of PR #749, yellow 15). The two
    patterns are matched on the line as written, so a heading indented into
    an item is the item's content and resets nothing."""
    seen = False
    for line in lines:
        if blocks.columns(line) >= 4:
            continue
        content = line.lstrip(" ")
        if ATX_HEADING.match(line) or THEMATIC_BREAK.match(line):
            seen = False
        elif LIST_ITEM.match(content):
            seen = True
    return seen


def gfm_table(text, header):
    """(rows, refusals) for the first GFM table in TEXT whose header row's
    cells are HEADER, a tuple of names.

      rows      [(line number, cells)] for every body row read, each cells a
                tuple as wide as HEADER, in order
      refusals  one sentence per thing that stopped the walk, naming it

    A header is a line written `| a | b |`, at most three spaces in; the line
    under it must be a delimiter row of the same width. Each line after that
    is one of three things, and the walk takes none of them on guesswork:

      an end       a blank line, a gap (`unfenced` hid a fence or a comment
                   block there), a heading, a thematic break, a block quote,
                   a list item, an HTML block, or a line four columns in. GFM
                   ends the table there; a line written `| … |` after it and
                   before the next heading is a row nobody reads, and is
                   refused
      a row        written `| … |` with the header's width
      anything     refused, saying what it is: a delimiter row out of place,
        else       a row of another width or without its outer pipes, or a
                   line with no pipe, which GFM reads as one of the rows

    **A header with a line directly above it is refused**, with the
    blank-line remedy, whether or not `unfenced` hides that line, because
    whether GFM renders a table there depends on block state no reader here
    tracks -- a paragraph, a list item's lazy paragraph, a table above, a
    setext underline, an HTML block, a fence inside one -- and the first
    walker, which mirrored those rules line by line, read tables GFM does not
    render (round 1 of PR #749, yellow 5; round 2, yellow 15). Judging
    the line as written closes the limit this docstring used to name, a
    fence `unfenced` hides inside an HTML block of kinds 6 and 7, because a
    header inside such a block always has a non-blank line above it. So is a
    header indented under a list item since the last heading or thematic
    break (`a_list_above`), which a blank line does not end -- the shape the
    list-item limit named here, `- x`, a blank line, then the header, is now
    refused -- and a header under an HTML block of kinds 1-5 left open above
    it (`raw_html_open`), which no blank line ends. **What this cannot see**
    is block state none of those three carries; round 2's generator found
    none over 600,000 documents.

    Each refusal reads after a noun naming the file, as both callers of
    `pact_signers` print it after "the pact ".
    """
    name = " | ".join(header)
    width = len(header)
    shape = "a one-cell row" if width == 1 else f"a {width}-cell row"
    written = "`|" + " … |" * width + "`"
    lines = text.splitlines()
    shown = list(unfenced(lines, text))
    at = next(
        (k for k, (_i, line) in enumerate(shown) if table_cells(line) == header),
        None,
    )
    if at is None:
        return [], [f"holds no `| {name} |` table"]
    head_index = shown[at][0]
    # The line as written, hidden or not: a line `unfenced` hides directly
    # above the header is a line GFM may read the header into -- a fence
    # inside an HTML block of kinds 6-7, or a list item the fence-only reading
    # hid (round 2 of PR #749, yellow 15).
    above = lines[head_index - 1] if head_index > 0 else ""
    if shown[at][1][:1] == " " and a_list_above([ln for _i, ln in shown[:at]]):
        return [], [
            f"has a `| {name} |` header indented under a list item, which GFM "
            "reads as more of that item where the indent reaches its text — "
            "write the header at the start of its line"
        ]
    if above.strip():
        return [], [
            f"has a `| {name} |` header directly under `{above.strip()}`, "
            "and GFM renders a table under a line only in some of the shapes "
            "that line can take — leave a blank line above the header"
        ]
    if raw_html_open([line for _i, line in shown[:at]]):
        return [], [
            f"has a `| {name} |` header inside an HTML block opened above it "
            "and never closed, so GFM renders no table there — close the block"
        ]
    delimiter = shown[at + 1] if at + 1 < len(shown) else None
    if (
        delimiter is None
        or delimiter[0] != head_index + 1
        or not DELIMITER_ROW.match(delimiter[1])
        or "|" not in delimiter[1]
    ):
        return [], [
            f"has a `| {name} |` header with no delimiter row under it, so "
            "GFM renders no table there"
        ]
    cells = delimiter[1].strip().strip("|").count("|") + 1
    if cells != width:
        return [], [
            f"has a `| {name} |` header over a delimiter row of {cells} "
            "cells, so GFM renders no table there"
        ]
    rows, stray, ended, previous = [], None, False, delimiter[0]
    for index, line in shown[at + 2 :]:
        if not ended and (index != previous + 1 or table_end(line)):
            ended = True
        if ended:
            if ATX_HEADING.match(line.lstrip(" ")) and blocks.columns(line) < 4:
                break
            if line.lstrip().startswith("|"):
                stray = (
                    f"has a `{name}` table that ends above `{line.strip()}`, "
                    "a row the walk never reaches — it and every row below it "
                    "would go unread"
                )
                break
            continue
        previous = index
        if DELIMITER_ROW.match(line):
            stray = _stops_at(name, line, "a delimiter row out of place")
            break
        found = table_cells(line)
        if found is not None and len(found) == width:
            rows.append((index + 1, found))
            continue
        if "|" in line:
            stray = _stops_at(name, line, f"which is not {shape} written {written}")
        else:
            stray = (
                f"has a `{name}` table that continues with `{line.strip()}`, "
                "a line with no pipe that GFM reads as one of its rows — write "
                f"it as {written}"
            )
        break
    return rows, [stray] if stray is not None else []


def _stops_at(name, line, why):
    return (
        f"has a `{name}` table that stops at `{line.strip()}`, {why} — every "
        "row below it would go unread"
    )


# The pact's own table: every OTHER signer, by origin remote URL, one per
# row under a `| Signer |` header (`templates/pact.md`).
SIGNER_HEADER = ("Signer",)


def read_table(text, header):
    """(rows, refusals, header read) for the table of TEXT headed HEADER,
    or, where TEXT holds none, headed as HEADER was written before 0.19.0
    (`renamed_header`). A text holding a HEADER table is read from it alone,
    and an old header it also holds is refused, wherever that table stands:
    its rows would otherwise go unread at exit 0 (round 1 of #822, yellow 1).
    The refusal is not added where the walk's stray-row refusal already names
    the old header, compared by the cells the refusal quotes, so a header
    written without its spaces is named once too (round 2 of #822, white 5).
    An old header with no blank line above it is one of the HEADER table's
    rows as GFM renders it; that row is not read, so it is named as the old
    header and not also as an entry (#830), quoted as the line is written so
    a person searching the file for it finds it (#831).
    Where neither is there, the refusal names HEADER and the
    header read is None, so a caller tells the old header from the new one
    without reading the text again (#822)."""
    rows, refusals = gfm_table(text, header)
    old = renamed_header(header)[0]
    old_rows, old_refusals = gfm_table(text, old) if old else ([], [])
    holds_old = old is not None and not (
        old_refusals and old_refusals[0].startswith("holds no ")
    )
    if not (refusals and refusals[0].startswith("holds no ")):
        named = f"`| {' | '.join(old)} |`" if old else None
        glued = [
            text.splitlines()[line - 1].strip()
            for line, cells in rows
            if holds_old and cells == old
        ]
        if holds_old:
            # An old header with no blank line above it is one of this
            # table's rows to GFM; it is the old header, named below or by
            # the walk's stray-row refusal, never an entry (#830).
            rows = [(line, cells) for line, cells in rows if cells != old]
        if holds_old and not any(
            table_cells(quoted) == old
            for r in refusals
            for quoted in re.findall(r"`([^`]*)`", r)
        ):
            new = f"`| {' | '.join(header)} |`"
            refusals = [
                *refusals,
                (
                    f"holds a `{glued[0]}` line inside its {new} table, the word "
                    f"before {RENAMED_IN}, which GFM reads as one of that "
                    "table's rows — delete the line"
                )
                if glued
                else (
                    f"also holds a {named} header, the word before {RENAMED_IN}, "
                    f"and nothing under it is read while the {new} table "
                    "stands — move its rows into that table and delete it"
                ),
            ]
        return rows, refusals, header
    if holds_old:
        return old_rows, old_refusals, old
    return rows, refusals, None


def pact_signers(text):
    """(signers, refusals, header) for the `| Signer |` table of a pact's
    TEXT. `signers` is `remote_entries`' parsed list, and a table that is
    absent or empty is a refusal, because a pact nobody signs is not a pact.
    `header` is the header the table was read under, `SIGNER_HEADER` or the
    one 0.18.x wrote (`read_table`), or None where the text holds neither;
    every refusal names the header it was read under.

    The table is read by `gfm_table`, so it is read as cmark-gfm renders it
    or refused, and no signer is dropped while the table reads as complete
    (round 3 of #735). On top of the walk: a row with an empty cell is
    refused by `remote_entries`, and so is every entry that is not one
    remote URL.
    """
    rows, refusals, header = read_table(text, SIGNER_HEADER)
    if header is None:
        return [], [refusals[0] + ", so it names no signer"], None
    values = [cells[0] for _line, cells in rows]
    # Both callers print each refusal after "the pact ", so an entry's own
    # sentence gets a lead-in that reads after those words (round 2 of #647,
    # white 14); `remote_entries` keeps the sentences the `Pact` row prints.
    signers, entry_refusals = remote_entries(values, "an empty row", named=False)
    word = header[0]
    out = [f"has a `{word}` entry that will not read: {r}" for r in entry_refusals]
    out.extend(_signer(refusal) for refusal in refusals)
    if not values and not any("renders no table" in r for r in refusals):
        out.append(f"has a `{word}` table that lists nobody")
    return signers, out, header


# --- the record of pact changes a signer keeps (#647, step C) ---------------
#
# `seal/pact-changes/<work-item-id>.md` in a signer: one row per ledger row
# whose code moved under a pact clause it cites, written by
# `evidence-check --reverify` and read by `pact-check` at the pact's
# repository. Permanent, one file per work item, never folded, never edited
# by hand (`docs/the-pact.md`).
PACT_CHANGES = "pact-changes"
PACT_CHANGE_HEADER = ("Clause", "Row", "Code", "Checked")
# The `Clause` cell of a row recorded under `always` that cites no clause.
NO_CLAUSE = "—"
CHECKED_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def pact_changes(text):
    """(rows, refusals) for a record of pact changes, read through
    `gfm_table`: `rows` as `(line, clause, row, code, checked)`, one per row
    whose four cells are filled and whose `Checked` is a date, and one
    sentence per row that is not, reading after "the record "."""
    rows, refusals = gfm_table(text, PACT_CHANGE_HEADER)
    out = []
    for line, (clause, row, code, checked) in rows:
        if not (clause and row and code):
            refusals.append(f"has a row at line {line} with an empty cell")
            continue
        if not CHECKED_DATE.fullmatch(checked):
            refusals.append(
                f"has a row at line {line} whose `Checked` is `{checked}`, not "
                "a date written YYYY-MM-DD"
            )
            continue
        out.append((line, clause, row, code, checked))
    return out, refusals


# --- the record of pact reviews the pact's repository keeps (#647, step D) --
#
# `seal/pact-reviews/<work-item-id>.md` at the pact's repository, begun from
# `templates/pact-review.md`: one row per signer's record of pact changes
# a pact review takes, naming the signer, the record as `<work-item-id>@
# <content hash>`, and the verdict.
PACT_REVIEWS = "pact-reviews"
PACT_REVIEW_HEADER = ("Signer", "Change", "Verdict")
VERDICT_HOLDS = "holds"
VERDICT_AMENDED = "amended"
VERDICTS = (VERDICT_HOLDS, VERDICT_AMENDED)


def pact_reviews(text):
    """(rows, refusals, header) for a record of pact reviews, read through
    `gfm_table`: `rows` as `(line, signer, change, verdict)` for every row
    whose three cells are filled, and one sentence per row that is not,
    reading after "the record ". `header` is the header read, as
    `pact_signers` returns it: a record a pact review wrote in 0.18.x is
    permanent and keeps its header (`read_table`). Whether a row can be
    true -- the signer listed, the record held, the verdict one of two -- is
    `pact-check`'s, which has the pact and the signers to ask."""
    rows, refusals, header = read_table(text, PACT_REVIEW_HEADER)
    out = []
    for line, (signer, change, verdict) in rows:
        if not (signer and change and verdict):
            refusals.append(f"has a row at line {line} with an empty cell")
            continue
        out.append((line, signer, change, verdict))
    return out, refusals, header


def _signer(refusal):
    """A walk refusal, in the words `pact-check` has always printed for the
    pact's table: a row it leaves unread is a signer."""
    return refusal.replace("every row below it", "every signer below it")


# --- the word 0.18.x wrote (#822) ------------------------------------------
#
# Until 0.19.0 every repository of a work item that keeps a pact had another
# name, and two headers carried it into files nobody regenerates: the pact's
# one-column table and every pact review record, which is permanent. Both
# still read (`read_table`), and both commands print the sentence below where
# they read one. This unit is the one place the old word is written, which is
# what lets `tests/test_one_word_one_meaning.py` refuse it everywhere else and
# exclude this unit by name (`docs/the-pact.md` §*The words*).
RENAMED_IN = "0.19.0"


def renamed_header(header):
    """(old, sentence) for HEADER: the header as written before
    `RENAMED_IN`, and the sentence naming the rename, reading after a file's
    name. (None, None) for a header the rename never touched."""
    if "Signer" not in header:
        return None, None
    old = tuple("Signatory" if cell == "Signer" else cell for cell in header)
    return old, (
        f"heads its table `| {' | '.join(old)} |`, the word before "
        f"{RENAMED_IN} — `| {' | '.join(header)} |` is the header now; rename "
        "it when the file is next edited"
    )
