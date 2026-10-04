"""One heredoc shape, matched byte for byte, and the command with its body
taken out (#739, #763).

The commit gate reads every heredoc body as shell and asks whether it commits,
because a body a shell runs is a command. A body that is only the text of a
file, or a Python program read from stdin, is not, and reading it as shell
stopped whole Bash calls for a body that only MENTIONED a commit. #760 tried
to tell the two apart through `hooks/cmdline.py`'s body boundaries, and four
review passes each found a place where that splitter and the shell disagree
about where a body starts or ends. Every one was a silent commit.

So this reader trusts nothing it did not write. It admits ONE shape, given in
`docs/commit-review-gate-spec.md` and as clauses A-F below, and everything
else is `None`: the gate then reads the command exactly as it did before.
There is no shell lexer here, no quote tracking and no import from the
splitter. What it does is a regular grammar over the command's first line, a
split of the rest on newlines, an exact comparison and a count.

  A. No carriage return, no NUL and no backslash followed by a newline,
     anywhere in the command, body included.
  B. The first line is exactly `[cd WORD && ]CONSUMER <<'D'`, one space
     between tokens, nothing before or after. CONSUMER is a sink -- `cat >
     WORD`, `cat >> WORD`, `tee WORD`, `tee -a WORD` -- or the program
     `python3 -` followed by zero or more WORDs. D is `[A-Za-z0-9_]+`. WORD is
     a plain word or one single-quoted word.
  C. The body ends at the first later line exactly equal to D. No line equal
     to D, no match. Nothing is stripped before the comparison.
  D. Outside the body, `<<` occurs exactly once.
  E. After a sink's terminator, nothing but newlines. After the program's,
     anything: that suffix is read the base's way.
  F. The reduced text is the first line without ` <<'D'`, then, where the
     program has a suffix that is more than newlines, a newline and the
     suffix.

Each clause closes a row of `spec.md`'s disagreement table in the work item
`1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data`, and
`tests/test_one_heredoc_shape_agrees_with_the_shell.py` runs every admitted
string of a generated corpus through the real bash and zsh to show they cut
the body where this does. Widening the grammar reopens a row: a LEAD that
assigns, a target that is a parameter or a program after a sink each needs a
reader that proves line 1 closed, which is the splitter this module exists not
to trust.
"""

import re

# Clause B's slots. ASCII alone, so a line equals D as text exactly when it
# equals it as bytes (row 8).
_D = r"[A-Za-z0-9_]+"
_PLAIN = r"[A-Za-z0-9_./][A-Za-z0-9_./-]*"
_QUOTED = r"'[^'\n]+'"
_WORD = rf"(?:{_PLAIN}|{_QUOTED})"
_LEAD = rf"cd {_WORD} && "
_SINK = rf"(?:cat > {_WORD}|cat >> {_WORD}|tee {_WORD}|tee -a {_WORD})"
_PROGRAM = rf"python3 -(?: {_WORD})*"

_OPENER = re.compile(
    rf"(?P<head>(?:{_LEAD})?(?:(?P<sink>{_SINK})|{_PROGRAM})) <<'(?P<d>{_D})'"
)

# Clause A: each byte where a reader and some shell were measured or can be
# shown to disagree.
_BANNED = ("\r", "\0", "\\\n")


def _match(command):
    """(reduced text, body) for a command of the one shape, else None.

    The body is what the reader says the consumer receives: every line before
    the terminator, each with the newline that ends it. The agreement test
    compares it with what a real shell wrote, which is why it is returned at
    all: the gate needs the reduced text alone.
    """
    if not isinstance(command, str) or any(b in command for b in _BANNED):
        return None
    first, newline, rest = command.partition("\n")
    if not newline:
        return None
    opener = _OPENER.fullmatch(first)
    if opener is None:
        return None
    lines = rest.split("\n")
    try:
        end = lines.index(opener.group("d"))
    except ValueError:
        return None
    body = "".join(line + "\n" for line in lines[:end])
    after = "\n".join(lines[end + 1 :])
    if (first + "\n" + opener.group("d") + "\n" + after).count("<<") != 1:
        return None
    if not after.strip("\n"):
        return opener.group("head"), body
    if opener.group("sink") is not None:
        return None
    return opener.group("head") + "\n" + after, body


def reduce(command):
    """The command with its one heredoc body taken out, or None.

    None means the command is not the one shape this module admits, and the
    caller reads the command as written. A string means it is, and nothing
    below the caller is asked where a body is: the reduced text has none.
    """
    found = _match(command)
    return None if found is None else found[0]
