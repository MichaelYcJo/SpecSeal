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
CONFIG_ROW = re.compile(r"^\|\s*(?P<item>[^|]+?)\s*\|\s*(?P<value>[^|]*?)\s*\|\s*$")
CONFIG_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def config_path(home):
    return os.path.join(home, CONFIG)


def config_rows(text):
    """Every `| Item | Value |` row under the first such header, in order.

    The header and the separator are this table's own furniture ABOVE its
    first row and somebody else's table BELOW it; any other line ends the
    table. Both rules are the ones
    `tests/test_the_pull_request_language_is_the_repositorys.py#items`
    arrived at over two review rounds, and a second reader that read the
    table differently would answer a different question about the same file.
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
        found.append((match.group("item").strip(), match.group("value").strip()))
    return found


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
