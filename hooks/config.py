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
CELL = r"(?:[^|\\]|\\.)"
CONFIG_ROW = re.compile(
    rf"^\|\s*(?P<item>{CELL}+?)\s*\|\s*(?P<value>{CELL}*?)\s*\|\s*$"
)
CONFIG_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")

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
    """
    found, seen_header = [], False
    for line in text.splitlines():
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
    """Everything a caller with somebody to tell needs about the first line a
    person wrote as a row of this table and this reader will not take as one.

      line   the refused line as written, with its own indentation, or None
      ended  whether that line is the one that ENDED the table
      below  the rows written under it that the reader never reached

    **`ended` is a condition and not a decoration.** `config_rows` breaks on
    a line it cannot parse only once it has FOUND a row; with nothing found
    yet it steps past that line and keeps reading, so every row below still
    arrives. A refusal that says those rows were lost sends a person to
    reformat rows that were read correctly -- a true sentence about the wrong
    file, which is the shape #415 was opened about. The narrowing was
    measured in that work item and reached five records before it reached
    this walk (round 1 🟡 1).

    **It reports and it refuses nothing.** Nothing here raises, and no caller
    becomes able to deny by importing it: it answers a question two callers
    that already talk to a person want to ask, which is *why did that row not
    arrive*. `hooks/mode-gate.py` deliberately does not ask it -- a
    `PreToolUse` hook that refuses wrongly stops a session with nobody able
    to get past it, and everything in this module fails toward silence.

    A line is one of these only when it begins with a pipe once its
    indentation is stripped, which is how a person spells a row -- an
    indented row is still a row somebody wrote. A blank line or a paragraph
    of prose ends the table by the rule `config_rows` has always had, so it
    is the table's end and not a refusal. So does a second header or a stray
    separator once a row has been found, and the walk stops there too rather
    than reaching into whatever table comes next: it used to step past both
    unconditionally and could quote a line out of the table BELOW this one
    (#415 round 1, the correction).

    Before this existed the two states were indistinguishable to a caller:
    `broad_gate` reported a piped `Broad gate` row as ABSENT, which is a true
    sentence about a cause that is not the real one (#415).
    """
    lines = text.splitlines()
    seen_header, found = False, False
    for i, line in enumerate(lines):
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if found:
                return None, False, []
            continue
        if CONFIG_ROW.match(line):
            found = True
            continue
        if not line.lstrip().startswith("|"):
            return None, False, []
        return line, found, rows_under(lines[i + 1 :])
    return None, False, []


def rows_under(lines):
    """The rows a person wrote below a refused line, until the table's shape
    stops -- a blank line, prose, or a header starting somebody else's table.

    **Read more tolerantly than `config_rows` reads, deliberately.** A second
    line that will not parse is stepped over rather than ending the walk,
    because nothing acts on these values: their one use is letting a refusal
    say that a row the person wrote is sitting below the line, so that
    nobody is sent looking for a row that is already in their file (#415).
    A reader whose answers were acted on could not be this forgiving.
    """
    under = []
    for line in lines:
        if not line.strip() or CONFIG_HEADER.match(line):
            break
        if not line.lstrip().startswith("|"):
            break
        match = CONFIG_ROW.match(line)
        if match:
            under.append(
                (
                    unescaped(match.group("item").strip()),
                    unescaped(match.group("value").strip()),
                )
            )
    return under


def refused_row(text):
    """The refused line alone -- `refusal` above is the whole answer, and its
    docstring is where this one's reasoning lives."""
    return refusal(text)[0]


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
