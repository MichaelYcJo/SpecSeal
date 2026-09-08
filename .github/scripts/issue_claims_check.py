#!/usr/bin/env python3
"""Report which issues a pull request body CLAIMS and which it only mentions.

PR #162's body wrote `Closes #153 and #150`. At the 0.8.0 release,
`close_issues_on_release.py` closed #153 and left #150 open, and somebody
closed it by hand afterwards.

**Nothing malfunctioned.** A closing keyword claims the one number that follows
it and nothing else -- GitHub reads it that way, and the sibling script says so
in a comment two lines above its own regex. The sentence claimed #153 and said
nothing about #150.

So the repair is not a wider regex. Widening `CLOSING` would make this
repository close issues GitHub does not, and the two would then disagree about
what a body means, which is worse than the loss it repairs. The repair is that
somebody is TOLD, at the pull request, while the author is still looking.

This is the same shape as the defect the release workflow itself exists for:
an answer was written and nothing acted on it. The rule is already written
down, in the one file whose author needs it least at the moment the prose is
written -- the session writing a pull request body is not reading
`close_issues_on_release.py`.

  issue_claims_check.py                    reads `PR_BODY` from the environment
  issue_claims_check.py --body-file BODY   reads a file (local runs and tests)

**It reports; it never fails a pull request.** A check that goes red on prose
stops a release for a false positive, and a check people learn to scroll past
is a check that is not there. One occurrence has been measured; that does not
buy a gate.

Exit codes: **0** for every body it read, whatever it found. **2** only when it
was handed no body at all -- neither `PR_BODY` in the environment nor
`--body-file`. That one is a misconfigured workflow, and the alternative is a
step that is green having examined nothing.

**What GitHub does not read is defined once, next door.** `KEYWORDS`,
`CLOSING`, `FENCE` and `SPAN` are imported from `close_issues_on_release.py`
rather than restated here, so widening one moves both. Two lists of what a
closing keyword is would drift apart the first time either was edited.

## What a sentence is

The check turns on *another `#N` within the same sentence*, and segmenting
prose that holds `#150.`, `e.g.`, `0.9.2` and fenced code is where it would be
wrong. A segment ends at the first of:

  1. `.`, `!`, `?` or `;` followed by whitespace or the end of the text;
  2. a blank line;
  3. the start of a new markdown block -- a line whose first non-space
     character is `-`, `*`, `+`, `#`, `>`, `|`, or a `1.`-style list marker.

**A single newline is not a boundary.** Every body in this repository is
hard-wrapped, so one sentence spans lines routinely and `Closes #1 and\\n#2` is
this defect wrapped at column 88. Measured on #162's own body: its `Closes`
sentence runs across three lines.

What that gives up, in the one direction it is allowed to: `e.g.` and `i.e.`
end a segment, because nothing here can tell an abbreviation from a full stop.
Splitting early can only put two numbers in different segments, so the check
under-reports rather than inventing a warning. `0.9.2` and a trailing `#150.`
are safe, because a full stop inside a token is not followed by whitespace.

Only a number AFTER the claim is a candidate. `Part of #1, and this closes #2`
is not the shape and says nothing, which is where the false-positive budget
goes.

A closing keyword inside a fenced block or an inline code span is invisible,
the way it is to GitHub and to the sibling script -- this repository's own
documents carry `Closes #88` in a fence as the example to copy, and its bodies
quote its documents routinely. The masking here replaces code CHARACTER FOR
CHARACTER with spaces, where the sibling collapses each match to one space:
a fence collapsing to a single space would join the line above it to the line
below, and this module segments by line structure.
"""

import argparse
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "hooks"))

import console  # noqa: E402
from close_issues_on_release import CLOSING, FENCE, KEYWORDS, SPAN  # noqa: E402

# Every `#N` a body writes, claimed or not. `#L45` and `#anchor` do not match:
# a digit has to follow the hash immediately.
ISSUE_REF = re.compile(r"#(\d+)\b")

# Rule 1. A full stop inside `0.9.2` is not followed by whitespace, so it is
# not a boundary; `#150.` at the end of a sentence is.
SENTENCE_END = re.compile(r"[.!?;](?=\s|$)")

# Rule 3. A line that opens a new markdown block ends the segment before it,
# even with no blank line between them -- consecutive list items are the case
# that matters, and they are written without one.
#
# Every marker that CommonMark requires a space after asks for one here. A
# bare `[-*+>|#]` class reads `#22` at the start of a line as a heading, and
# `#22` at the start of a line is this defect hard-wrapped -- which is the one
# thing this module exists to see. `*bold*` opening a line is the same trap
# one marker over. `>` and `|` take no space in the markdown either.
BLOCK_START = re.compile(r"^[ \t]*(?:[-*+](?=\s)|\#{1,6}(?=\s|$)|\d+[.)](?=\s)|[>|])")


def prose_only(body):
    """`body` with fenced blocks and code spans blanked, length preserved.

    Same two patterns the release closer uses, and a different substitution:
    every masked character becomes a space and every newline is kept, so the
    offsets this module reports and the line structure it segments by both
    survive. Collapsing a fence to one space -- which is right for a `findall`
    and wrong here -- would splice the line above it onto the line below.
    """

    def blank(m):
        return "".join("\n" if c == "\n" else " " for c in m.group(0))

    return SPAN.sub(blank, FENCE.sub(blank, body))


def segments(text):
    """`(start, end)` for each sentence-ish run of `text`, in order.

    Empty runs are dropped. The boundaries are the three rules in the module
    docstring; everything between two of them is one segment, newlines
    included, because a hard-wrapped sentence is still one sentence.
    """
    cuts = {0, len(text)}
    for m in SENTENCE_END.finditer(text):
        cuts.add(m.end())
    at = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if not stripped or BLOCK_START.match(line):
            cuts.add(at)
        at += len(line)
    return [(a, b) for a, b in itertools.pairwise(sorted(cuts)) if text[a:b].strip()]


def claimed_spans(text):
    """`(number, digit-start, digit-end)` for every closing keyword + number.

    The digit span, not the whole match: it is what tells a claimed `#153`
    apart from a bare `#150` sitting in the same sentence.
    """
    return [(m.group(1), m.start(1), m.end(1)) for m in CLOSING.finditer(text)]


def read(body):
    """`(claimed, mentioned, warnings)` for one pull request body.

    `claimed` and `mentioned` are issue numbers as strings, deduplicated, in
    the order the body writes them. A number that is claimed anywhere is not
    also reported as mentioned -- `Closes #1` and a later `see #1` is one
    claim, not a claim and a doubt.

    A warning is `(claimed number, unclaimed number, the sentence)`, one per
    unclaimed `#N` that follows a claim inside the same segment. The claimed
    number named is the NEAREST claim before it, which is the one whose
    keyword the author was reusing.

    A number the body claims SOMEWHERE is never warned about, wherever else it
    also appears: `Closes #1 and #2 ... closes #2` loses nothing, and a
    warning there would be the false positive this check spends its whole
    budget avoiding.
    """
    text = prose_only(body)
    claims = claimed_spans(text)
    claimed_at = {start for _, start, _ in claims}

    claimed, mentioned, warnings = [], [], []
    for number, _, _ in claims:
        if number not in claimed:
            claimed.append(number)
    for m in ISSUE_REF.finditer(text):
        number = m.group(1)
        if m.start(1) in claimed_at or number in claimed or number in mentioned:
            continue
        mentioned.append(number)

    for start, end in segments(text):
        here = [c for c in claims if start <= c[1] < end]
        if not here:
            continue
        # Quoted from the ORIGINAL body, not the masked copy: the author has
        # to recognise the sentence they wrote, and a code span blanked out of
        # it reads as a different sentence. The masking is length-preserving,
        # so these offsets index the body as written.
        sentence = " ".join(body[start:end].split())
        for m in ISSUE_REF.finditer(text, start, end):
            if m.start(1) in claimed_at or m.group(1) in claimed:
                continue
            before = [c for c in here if c[1] < m.start(1)]
            if before:
                warnings.append((before[-1][0], m.group(1), sentence))
    return claimed, mentioned, warnings


def report(claimed, mentioned, warnings, out=print):
    """Print the split and any warning. Returns nothing; the exit code is 0."""
    out(f"claimed (closed when the release reaches `main`): {_list(claimed)}")
    out(f"mentioned only (nothing closes these): {_list(mentioned)}")
    for kept, lost, sentence in warnings:
        out(
            f"::warning::this sentence claims #{kept} and NOT #{lost}: "
            f'"{_short(sentence)}" -- a closing keyword claims the one number '
            f"that follows it, so #{lost} stays open. Write "
            f"`closes #{lost}` in front of it, or move it out of the "
            f"sentence if it was never a claim."
        )
    if not warnings:
        out("no sentence claims one number and names another beside it")


def _list(numbers):
    return ", ".join("#" + n for n in numbers) if numbers else "none"


def _short(sentence, limit=160):
    return sentence if len(sentence) <= limit else sentence[: limit - 1] + "…"


def body_from(args, env):
    """The body to read, or None when nothing was handed over.

    An EMPTY `PR_BODY` is a body -- a pull request opened with no description
    is ordinary, and reporting nothing for it is the right answer. An ABSENT
    one is a workflow that forgot to pass it, which is the only thing here
    worth an exit code.
    """
    if args.body_file:
        with open(args.body_file, encoding="utf-8", errors="replace") as f:
            return f.read()
    return env.get("PR_BODY")


def main(argv=None, env=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--body-file",
        help="read the body from this file instead of the PR_BODY environment variable",
    )
    args = parser.parse_args(argv)
    body = body_from(args, os.environ if env is None else env)
    if body is None:
        sys.stderr.write(
            "no body to read: neither --body-file nor PR_BODY. A step that "
            "examined nothing must not be green.\n"
        )
        return 2
    report(*read(body))
    return 0


if __name__ == "__main__":
    console.to_utf8()
    raise SystemExit(main())


# `KEYWORDS` is imported for the docstring's claim that this module and the
# release closer share one definition, and re-exported so a reader who lands
# here can see the vocabulary without opening the sibling.
__all__ = ["CLOSING", "FENCE", "ISSUE_REF", "KEYWORDS", "SPAN", "main", "read"]
