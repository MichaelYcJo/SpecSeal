#!/usr/bin/env python3
"""unverified-check — read what an overview recorded as unverified, and fail
on a record that cannot be read.

`verify` condition 4 lets a claim go out unproven as long as the row names who
answers it. Nothing ever read those rows again. The measured failure: a row in
`seal/specs/1787495842-verify-the-unverified/overview.md` said nobody had seen the
gates render in an interactive TUI and named the user as the answerer. Months
later the user hit exactly that, from the other side, and asked why every gate
renders as yes/no. The record was accurate and no procedure ever closed it.

So this reads every `## Not verified` section and reports what is still open.
It does **not** fail because items are open. Dozens were open the day it was
written, and a build that goes red for an honest `unverified` row teaches
people to write none, which voids the condition it is defending. Counting them
is what `unverified-check specs/` is for; no number is repeated in prose here,
because a number in a comment is right for one commit and nobody recounts it.

It fails for what the author can always fix:

  malformed   a section that cannot be read. A tolerant parser reports zero
              here, and zero reads as "everything has been closed" — the worst
              available failure, because it is indistinguishable from success
  fewer rows  a table that lost rows against the base, or an `overview.md`
              that was there and is not (`--baseline REF`) — unless the work
              item's fold is recorded in `docs/`, which is `settle` retiring
              a released spec rather than this branch deleting a record. Such
              a directory is named as folded and counted apart. So is one the
              rule arm retired (#517): the whole directory is gone, and at
              the merge base it held no `spec.md` and nothing open in its
              record, which `retired_by_rule` answers for every reader
  no baseline the ref itself does not resolve, or it shares no history with
              HEAD. That is exit 2, not a pass: a comparison against nothing
              is not a comparison

**The base is the merge base, not the ref's tip.** `--baseline REF` names the
branch a pull request merges into, and that branch moves: the moment one work
item squashes into it, every sibling branch cut before that squash has the
squashed item's `overview.md` at the base and never had it at all. So the ref
is resolved once, to `git merge-base REF HEAD`, and every read below uses that
commit. A row present at the fork point and absent here was removed by THIS
branch, which is the only claim this makes; a row that arrived on the base
after the fork is not this branch's business. `merge_base` carries what the
old footing cost (#272).

An item is closed by marking it, never by deleting it: prefix the Item cell
with the check mark and say in the second cell what closed it. Anything
unmarked counts open, so the silent direction is always "still open".

Deliberately a text scan of markdown, not a parser library: the gates here are
stdlib-only, and the format it accepts is one line long. That format is strict
on purpose — see `check_file`.

Exit codes: 0 the record is readable (open items are reported, not punished) ·
1 a section could not be read, or rows were deleted · 2 the path or arguments
were unusable, which includes a scan that found no overview at all — except
under a `seal/` root's own `specs` path holding no work item, empty or absent,
which is the state a complete fold ends in and exits 0 saying so
(`settled_root`).
"""

import argparse
import os
import re
import subprocess
import sys

OVERVIEW = "overview.md"
HEADING = "## Not verified"
HEADER = ("Item", "Who must answer")
CLOSED = "✅"
PLACEHOLDER = re.compile(r"^<[^>]*>$")
# Characters that occupy no width: the two variation selectors, the zero-width
# family, and the byte-order mark. None of them make a marker into a claim.
INVISIBLE = "\ufe0f\ufe0e\u200b\u200c\u200d\u2060\ufeff"
SEPARATOR = re.compile(r"^:?-+:?$")
# Where a fold records itself, and the one line-anchored shape it takes. A
# released work item's directory is removed by `settle` once its SDD set has
# been folded into `docs/`, and the fold's record is the provenance comment
# the folded prose carries there — the same marker
# `.github/scripts/fold_ledger.py#marker` and
# `.github/scripts/gather_changelog.py#marker` write. A record derived from
# the destination cannot disagree with the destination, which is why there is
# no second file for this to read.
#
# Line-anchored, for the reason `fold_ledger.py#is_marked` already pays for:
# every document that describes the convention quotes the marker's shape
# inline, and a substring test would read that prose as a fold and excuse a
# removal nothing absorbed.
#
# **The line anchor is not the whole of it, and a fence is the other half.**
# It says the marker stands alone on its line; it never says the line is
# prose. `skills/settle/SKILL.md` §2 — the one document a session reads before
# it folds — shows the marker inside a fenced block with a REAL released work
# item id, so a session copying that example into the policy it is writing
# hands `settle --retire` a real directory to delete. Measured 2026-09-22:
# `folded_items` over a `docs/` holding a copy of that skill returns
# `1788302682-the-release-check-never-watched-bin`, and the retirement removed
# it at exit 0. And a commented-out draft is the other way a line stops being
# live, which round 2 of the same chain found still open. So every read below
# goes through `live_lines`, the one rule for whether a line is live: one scan
# carrying fence, comment and code-span state together, read by
# `settle.py#coordinates` through the same function, because a second copy of
# any part of it is the duplicated-reader shape `check_text`'s docstring spent
# three review rounds closing and round 3 found once more. It was three passes
# in sequence for four rounds; `live_lines`'s docstring says why a sequence
# could not answer this and what each formulation got wrong.
#
# `readable()` is NOT what this uses, although it is the pair `check_text`
# takes. It blanks HTML comments too, and the marker IS one, so it would erase
# every fold record there is.
DOCS = "docs"
FOLD_MARKER = re.compile(r"^<!-- specs/(\S+) -->$", re.M)
# The two delimiters of an HTML comment. `live_lines` scans for them directly:
# it holds the comment state itself, so neither is looked for while it is
# inside a fence or a code span, and nothing blanks either one out of the text.
OPENER = "<!--"
CLOSER = "-->"
# A run of backticks. `live_lines` needs it as it scans for code spans.
BACKTICKS = re.compile(r"`+")
# A fence delimiter line, as CommonMark 4.5 spells one: at most three spaces
# of indentation, a run of three or more backticks or three or more tildes,
# then the info string. `fence_opener` and `fence_closes` below are the rule
# the ledger readers and the record readers ask — `fence_opener`'s docstring
# lists them, and the readers that still keep a rule of their own — and this
# pattern is only their first half.
#
# **Three spaces, not `\\s*`.** Four is an indented code block, or a lazy
# continuation line inside an open paragraph. Reading one as a delimiter does
# not merely park lines — it INVERTS the fence state for the rest of the file,
# so a real fenced block's content reads live and its delimiters read as
# content, and a fold marker quoted inside a fenced example becomes a fold
# record. `skills/settle/SKILL.md` §2 shows the marker inside a fence with a
# real released id, which is the quotation this would have read (round 6,
# finding 1; executed on a throwaway git repository, `settle --retire` at
# exit 0 with the directory removed). `blank_fences` used to keep an
# unbounded spelling of its own, and #491 is what that cost: the bound had
# landed here and not one function over in the same file.
FENCE_RE = re.compile(r"^ {0,3}(?P<run>`{3,}|~{3,})(?P<info>.*)$")
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
# The heading matcher for a base revision. There is one reader; only how it
# finds the section is an argument, because a base commit may spell the
# heading the way this corpus did before it was normalized. Everything else —
# how a cell is read, where a fence ends, how a path resolves — is shared, and
# that sharing is what stopped one fix from opening the next gap.
LOOSE_HEADING = re.compile(r"^#{2,3}\s.*not verified", re.I)


def split_row(line):
    """Cells of one markdown table row, or None if the line is not a row.

    `\\|` inside a cell is an escaped pipe, not a column break."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def is_separator(cells):
    return bool(cells) and all(SEPARATOR.match(c) for c in cells)


def is_header(cells):
    return bool(cells) and cells[0].strip().lower() == "item"


def visible(s):
    """`s` without characters that take no space on screen.

    Many keyboards emit U+2705 followed by U+FE0F, and a zero-width space
    pastes in from anywhere. Either one makes `| \u2705 | done |` survive a
    plain `.strip()` while looking exactly like a bare check mark, which is
    the one row shape this refuses."""
    return s.translate({ord(c): None for c in INVISIBLE}).strip()


def comment_scan(lines):
    """`(the line began outside a comment, its text outside comments)`, each.

    One scanner, because two readers of this file want two different things
    out of the same walk and a second copy of the walk is what
    `check_text`'s docstring spent three review rounds undoing. `strip_comments`
    wants the text; `opens_outside_a_comment` wants the state the line STARTED
    in, which the text cannot answer — a fold marker IS a comment, so a
    genuine one and one sitting inside a commented-out draft both come back
    with nothing kept.
    """
    inside = False
    for line in lines:
        began = not inside
        rest, kept = line, ""
        while rest:
            if inside:
                end = rest.find("-->")
                if end == -1:
                    rest = ""
                else:
                    rest, inside = rest[end + 3 :], False
            else:
                start = rest.find("<!--")
                if start == -1:
                    kept, rest = kept + rest, ""
                else:
                    kept, rest, inside = kept + rest[:start], rest[start + 4 :], True
        yield began, kept


def strip_comments(lines):
    """The same lines with HTML comment content blanked out, indices intact.

    A template explains a section in a comment beside it, and an overview keeps
    that comment. The guidance is not rows, and it is not prose where a table
    belongs."""
    return [kept for _, kept in comment_scan(lines)]


def fence_opener(line):
    """The fence `line` opens, as `(character, length)`, or None.

    **The fence delimiter rule, and the one place it is written** (#491,
    #444). CommonMark 4.5: at most three spaces of indentation, then three or
    more backticks or three or more tildes. A BACKTICK opener's info string
    may not itself hold a backtick, so ``` ```x` ``` on its own line opens
    nothing; a tilde opener's info string is unrestricted. `fence_closes`
    below is the other half.

    The readers below ask these two functions rather than a pattern of their
    own, because five spellings of this rule is what five readers had. **It
    is not every fence walk in the repository.** `hooks/config.py#FENCE` is a
    deliberate copy, below. `payload_meter.py#FENCE`,
    `.github/scripts/fold_ledger.py#demote`,
    `.github/scripts/close_issues_on_release.py`,
    `skills/evidence-check/scripts/correction_check.py#rows` and the other
    readers #584 names still keep their own, and #584 is where each is
    brought here or answered. The readers that ask it: `fence_spans` and
    through it
    `blank_fences` and `closed_fence_lines`, and `_liveness` and
    `_paragraph_ends_at`, all in this module, and `todo_open_rows` through
    `closed_fence_lines` — which `settle.py#open_rows` and
    `.github/scripts/fold_ledger.py#open_rows` both are; and
    `skills/evidence-check/scripts/evidence_check.py#quoted_lines`, which
    the checker's four ledger walks read through, and `#claim_lines`, the
    records arm's walk, both by way of its `fence_rule`; and
    `hooks/root-migrate.py#repoint` through `evidence_check.py#unquoted`.
    `skills/code-review/scripts/round_record.py#fenced_after` applies the
    closer rule and the backtick-info rule by its own pattern and keeps a
    wider opener on purpose, so a fix fenced inside a list item still
    reaches the record. That file keeps a vendored copy of these two functions for the copy
    `evidence-ci` puts alone in a user repository, where this module is not
    beside it. **A new reader that decides by
    line whether it stands inside a fence belongs on this list**, and a
    reviewer of one has this docstring to check it against — nothing else
    can reach a reader that does not exist yet.

    `hooks/config.py#FENCE` is a deliberate copy: it runs on the
    hook path, where loading a skill module would cost every hook call.
    `tests/test_unverified_rows_close.py#test_the_fence_rule_agrees_with_the_config_reader`
    holds the two in step, shape by shape.
    """
    m = FENCE_RE.match(line.rstrip("\r\n"))
    if not m:
        return None
    run = m.group("run")
    if run[0] == "`" and "`" in m.group("info"):
        return None
    return run[0], len(run)


def fence_closes(line, opener):
    """Whether `line` closes the fence `opener` (a `fence_opener` value).

    CommonMark 4.5: the same character as the opener, a run at least as
    long, the same three-space bound, and nothing after the run but spaces
    or tabs. So ```` ```python ```` inside an open ```` ``` ```` block is
    content, and so is ```` ``` ```` inside a ```` ```` ```` block.
    """
    m = FENCE_RE.match(line.rstrip("\r\n"))
    return bool(
        m
        and m.group("run")[0] == opener[0]
        and len(m.group("run")) >= opener[1]
        and not m.group("info").strip()
    )


def fence_spans(lines):
    """`[(first, last)]` for each fenced block in `lines`, delimiters
    included, with `last` None for a block that is never closed.

    The walk for a reader with no comment or code-span state of its own. A
    reader that has either — `_liveness`, `claim_lines` — walks with
    `fence_opener` and `fence_closes` directly, because whether a line can
    open a fence at all depends on the state it began in.

    **An unclosed block is reported, not decided.** `blank_fences` blanks it
    to the end, because a gate reading a record treats it as quoted and
    `round_record.py` refuses the record with a named message. A reader of a
    line that HOLDS something — a ledger anchor, an open row — reads it,
    because only a block that closes is certainly a quotation
    (`docs/the-evidence-ledger.md` §*A marker counts only on a live line*).
    """
    spans, opener, first = [], None, None
    for n, line in enumerate(lines):
        if opener is None:
            opener = fence_opener(line)
            if opener is not None:
                first = n
        elif fence_closes(line, opener):
            spans.append((first, n))
            opener = None
    if opener is not None:
        spans.append((first, None))
    return spans


def closed_fence_lines(lines):
    """The indices of `lines` inside a fenced block that CLOSES, delimiters
    included — the lines a reader of something a line holds may skip."""
    lines = list(lines)
    return {
        n
        for first, last in fence_spans(lines)
        if last is not None
        for n in range(first, last + 1)
    }


def blank_fences(lines):
    """The same lines with fenced blocks blanked out, indices intact.

    A skill or an overview quoting this very format must not read as rows or
    as a second section. Blanking rather than truncating matters: the working
    tree and the base revision have to agree about where the table is, or
    adding an example reads as a deletion and rows after an example read as
    absent. A block that is never closed is blanked to the end, and the
    delimiter rule is `fence_opener`'s."""
    lines = list(lines)
    out = list(lines)
    for first, last in fence_spans(lines):
        for n in range(first, len(lines) if last is None else last + 1):
            out[n] = ""
    return out


def _liveness(lines, spans_cross_lines):
    """Whether each line BEGINS live, under one of the two span readings.

    `spans_cross_lines` is the only thing that differs between them, and it is
    the one question markdown cannot answer without a block model: a backtick
    run with no partner on its own line is literal text if the paragraph ends
    before its partner, and a code span if it does not. `live_lines` runs this
    twice rather than deciding.

    Everything else is shared and is not a guess. Inside a fence nothing is
    read but the closing fence; inside a comment nothing is markdown, so
    backticks there are ordinary characters; inside a code span no comment
    delimiter is a delimiter. A fence is decided before the rest of its line
    because a fence opener owns the whole line, and after that whichever of a
    comment opener and a backtick run comes first in the text wins.
    """
    fence, comment, span = None, False, None
    out = []
    for n, line in enumerate(lines):
        out.append(fence is None and not comment and span is None)

        if fence is not None:
            if fence_closes(line, fence):
                fence = None
            continue
        if not comment and span is None:
            fence = fence_opener(line)
            if fence is not None:
                continue

        pos = 0
        while pos < len(line):
            if comment:
                at = line.find(CLOSER, pos)
                if at == -1:
                    break
                pos, comment = at + len(CLOSER), False
            elif span is not None:
                closer = next(
                    (
                        m
                        for m in BACKTICKS.finditer(line, pos)
                        if m.end() - m.start() == span
                    ),
                    None,
                )
                if closer is None:
                    break
                pos, span = closer.end(), None
            else:
                opener = line.find(OPENER, pos)
                run = BACKTICKS.search(line, pos)
                if opener != -1 and (run is None or opener < run.start()):
                    pos, comment = opener + len(OPENER), True
                elif run is None:
                    break
                else:
                    width = run.end() - run.start()
                    closer = next(
                        (
                            m
                            for m in BACKTICKS.finditer(line, run.end())
                            if m.end() - m.start() == width
                        ),
                        None,
                    )
                    if closer is not None:
                        pos = closer.end()
                    elif spans_cross_lines and _partner_ahead(lines, n + 1, width):
                        span = width
                        break
                    else:
                        pos = run.end()
    return out


def _paragraph_ends_at(line):
    """Whether this line ends the paragraph above it.

    Each rule is the format's own: a blank line (CommonMark 4.8), an ATX
    heading (4.2), a fence delimiter (4.5), a thematic break (4.1), a block
    quote marker (5.1), a bullet or an ordered list that may interrupt a
    paragraph (5.2, 5.3), a setext underline (4.3), and a table row, which
    GFM parses cell by cell.

    **Being incomplete here is CHEAP, not safe, and the difference is a line
    the format parks.** This bounds one half of a disagreement rather than
    the answer, and a missing stop USUALLY only lets `_partner_ahead` reach
    further, which makes the crossing reading believe in a span the format
    would not, which parks a line — a fold reported as a deletion, at exit 1,
    which a person sees. Usually, not always: reaching further also changes
    which runs pair with which, and a run that consumes a partner early
    leaves a later run with none, so a later line goes live rather than
    parked. Measured 2026-09-22 with the setext underline missing, which it
    was until round 6: `["text `", "===", "text `", "plain prose", "text `"]`
    read its last two lines live where the format parks them. The rule round
    5 removed decided the answer by itself, so its missing stops removed a
    directory; this one only leans, but it leans in both directions. **Add a
    stop when the format has one, and stop nowhere the format does not** — an
    over-stop shortens the reach, which is the direction that goes live.
    """
    s = line.strip()
    if not s:
        return True
    indent = len(line) - len(line.lstrip(" "))
    # `|` is a deliberate over-stop — GFM parses a table row's cells
    # independently and it is what keeps three work items' coordinates.
    # `>` is the format's own rule (CommonMark 5.1).
    if s.startswith(("|", ">")):
        return True
    # CommonMark 4.2: at most three spaces of indentation, then one to six
    # hashes, then a space, a tab or end of line. `s.startswith("#")` alone
    # stopped on `#hello` and on `####### seven`, which are paragraph text —
    # and on the issue references this repository writes constantly, 944
    # lines of them (round 6, finding 4). Four spaces is paragraph text too,
    # a lazy continuation line, and the oracle
    # `tests/test_unverified_rows_close.py#block_ends_at` has bounded it all
    # along (#491's round-7 comment).
    if indent <= 3 and s.startswith("#"):
        n = len(s) - len(s.lstrip("#"))
        if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
            return True
    # Only an OPENER interrupts a paragraph, and `fence_opener` is the rule.
    if fence_opener(line) is not None:
        return True
    if s[0] in "*-_" and len(s) >= 3 and set(s.replace(" ", "")) == {s[0]}:
        return True
    if s[:2] in ("- ", "* ", "+ "):
        return True
    # CommonMark 4.3: a setext underline is a run of `=` under a paragraph.
    # The `-` form is already a thematic break above.
    if set(s) == {"="}:
        return True
    # CommonMark 5.3: an ordered list interrupts a paragraph only when it
    # starts with 1. `3. an item` inside a paragraph is paragraph text, and
    # stopping there shortens the crossing reading's reach.
    return s[:2] in ("1.", "1)") and len(s) > 2 and s[2] in " \t"


def _partner_ahead(lines, start_line, width):
    """Whether a backtick run of exactly `width` arrives before the paragraph
    the run opened in has ended.

    This is one half of a disagreement, not an answer: it asks how far a span
    COULD reach, and `live_lines` pairs it with the reading where an unclosed
    run reaches nowhere at all. A true span's partner lies inside its own
    paragraph, so this finds the very same partner; everywhere the two differ
    this reading parks a line the format would have read live, which is the
    direction that keeps a work item's directory.
    """
    for i in range(start_line, len(lines)):
        if _paragraph_ends_at(lines[i]):
            return False
        for m in BACKTICKS.finditer(lines[i]):
            if m.end() - m.start() == width:
                return True
    return False


def live_lines(lines):
    """`(the line, it begins live)` for each line — both readings, ANDed.

    **The one rule for whether a line is live, and every reader of the fold
    record and of the ledger sections asks it here** — `folded_items` below
    and both loops of `skills/settle/scripts/settle.py#coordinates`. A line
    begins live when it begins outside a fenced block, outside an HTML
    comment and outside a code span. The line is handed back unchanged; what
    a caller reads out of it — a marker, a coordinate — lives inside
    backticks, and the flag beside it is the whole of the judgment.

    **The one question markdown will not answer without a block model, and
    what is done about it.** A backtick run with no partner on its own line
    is literal text if the paragraph ends before its partner arrives, and a
    code span if it does not. Knowing which needs to know where the block
    ends, and every rule this reader has had for that was a guess:

    - Reading A: the run is **not** a span. It is literal, and comment
      delimiters after it on later lines are real delimiters.
    - Reading B: the run **is** a span, reaching to the next run of equal
      length wherever that falls.

    **A line is live only where both readings call it live.** Nothing decides
    where a block ends, because neither reading is chosen — both are computed
    and the disagreement is resolved toward keeping a work item's directory.
    Where the two agree, that is the answer; where they differ, the line is
    read as quoted and its marker is not a fold record. The cost is a fold
    reported as a deletion, which a person sees at exit 1 and can act on.

    **This is what five review rounds cost.** Rounds 1 to 4 each guessed at
    the comment state from a stateless pass; the scan that replaced them
    guessed instead at markdown's block structure, and round 5 found the
    shape that guess got wrong — a paragraph carrying an unclosed backtick,
    a draft opener on the next line, the closing backtick after it, and a
    marker below, which read live and took `settle --retire` to exit 0 with
    the directory removed. A guess at a block model fails for the same reason
    a guess at the comment state did, one level down. Computing both readings
    is what ends the class: there is no third thing to be wrong about.
    `plan.md` §*Alternatives considered* carries the four formulations of the
    pre-pass and this one's own predecessor.

    **What it reads, and what it does not model.** Inside a fence nothing is
    read but the closing fence; inside a comment nothing is markdown, so
    backticks there are ordinary characters; inside a code span no comment
    delimiter is a delimiter. A fence is decided before the rest of its line,
    then whichever of a comment opener and a backtick run comes first wins.
    Reference definitions, link destinations, raw HTML blocks and entity
    references are not modelled and none can hold a fold marker on a line of
    its own. Markdown's indented code block is the one deliberate omission
    with a shape that could: `skills/settle/scripts/settle.py#coordinates`
    names it and
    `tests/test_settle_reads_before_it_removes.py#test_an_indented_example_row_is_counted_and_the_reader_says_so`
    pins the decision.

    **What this may not touch.** `comment_scan`, `strip_comments`,
    `blank_fences` and `readable` serve the other gates — `check_text`,
    `round_record.py`, `chain_check.py`, the review-history guard — and
    `seal/ledger.md` pins `strip_comments`'s exact output while
    `tests/test_chain_hooks.py#reader_blanking_passes` pins the passes
    `readable` makes. None of them is on this path. What this scan and
    `blank_fences` DO share is the fence delimiter, `fence_opener` and
    `fence_closes`, because two spellings of it is what #491 found: the
    three-space bound had landed here and not one function over.

    No `zip`. Ruff's B905 requires the strictness keyword on every such call,
    that keyword arrived in python 3.10, and this script carries no
    interpreter guard — so writing one here is the traceback on somebody's
    3.9 `python3` that
    `tests/test_a_script_says_which_interpreter_it_needs.py` keeps out of the
    tree. That module reads TEXT rather than an AST, so even naming the
    construct here reddens it, which is why this sentence goes the long way
    round.
    """
    lines = list(lines)
    literal = _liveness(lines, spans_cross_lines=False)
    crossing = _liveness(lines, spans_cross_lines=True)
    for n, line in enumerate(lines):
        yield line, literal[n] and crossing[n]


def readable(text):
    """The lines a reader should judge: no comment text, no fenced blocks.

    Every read starts here — the working tree and the base revision alike —
    which is what keeps the two sides of the comparison counting the same
    table."""
    return blank_fences(strip_comments(text.splitlines()))


def headings(lines):
    """(index, text) for every heading in already-`readable` lines."""
    return [(i, line.rstrip()) for i, line in enumerate(lines) if line.startswith("#")]


def parse_section(body, offset, strict_header=True):
    """(open, closed, errors) for the body lines of one section.

    `offset` is the file line number of body[0], so every error carries a
    coordinate the author can open."""
    errors, open_rows, closed_rows = [], [], []
    content = [(offset + i, ln) for i, ln in enumerate(body) if ln.strip()]

    if not content:
        errors.append(
            (offset, "the section is empty — write the table, or `none — <why>`")
        )
        return open_rows, closed_rows, errors

    first_no, first = content[0]
    if first.strip().lower().startswith("none"):
        for line_no, line in content[1:]:
            if line.strip().startswith("|"):
                errors.append((line_no, "`none` and a table in the same section"))
                break
        return open_rows, closed_rows, errors

    cells = split_row(first)
    if cells is None:
        errors.append(
            (
                first_no,
                "expected `| Item | Who must answer |`, found prose. Prose "
                "belongs under `## Not done`; this section is read by a machine",
            )
        )
        return open_rows, closed_rows, errors
    if (tuple(cells) != HEADER) if strict_header else not is_header(cells):
        errors.append(
            (
                first_no,
                f"header is |{'|'.join(cells)}|, and the one this reads is "
                f"|{'|'.join(HEADER)}|",
            )
        )
        return open_rows, closed_rows, errors
    if len(content) < 2 or not is_separator(split_row(content[1][1]) or []):
        errors.append((first_no, "the header row is not followed by a separator row"))
        return open_rows, closed_rows, errors

    rows = content[2:]
    if not rows:
        errors.append(
            (first_no, "a table with no rows says nothing — write `none — <why>`")
        )
    for line_no, line in rows:
        cells = split_row(line)
        if cells is None:
            errors.append((line_no, "a line inside the table that is not a table row"))
            continue
        if len(cells) != 2:
            errors.append((line_no, f"{len(cells)} cells, expected 2"))
            continue
        item, who = cells
        # One normalization for every judgment below. Reading the raw cell in
        # one place and the normalized cell in another is how a zero-width
        # space turned a separator into an unverified item and a blank row
        # into an open one.
        seen = [visible(c) for c in cells]
        if is_separator(seen) or is_header(seen):
            errors.append(
                (
                    line_no,
                    "a second header or separator row inside the section — it "
                    "holds one table, and a repeated one counts `|---|---|` "
                    "as an unverified item",
                )
            )
            continue
        if not seen[0] or not seen[1]:
            errors.append(
                (line_no, "an empty cell — every row names an item and its answerer")
            )
            continue
        if PLACEHOLDER.match(seen[0]) or PLACEHOLDER.match(seen[1]):
            errors.append((line_no, "the template's placeholder is still in the row"))
            continue
        if seen[0].startswith(CLOSED):
            rest = visible(seen[0][len(CLOSED) :])
            if not rest:
                errors.append(
                    (
                        line_no,
                        f"a bare {CLOSED} — the row keeps the item's text, and "
                        "the second cell says what closed it",
                    )
                )
                continue
            closed_rows.append((line_no, rest, who))
        else:
            open_rows.append((line_no, item, who))
    return open_rows, closed_rows, errors


def check_file(path):
    """(open, closed, errors) for one overview.

    Exactly one `## Not verified` section, spelled that way. Tolerating other
    spellings is what makes an unknown one report zero, and this corpus had
    more than one of them."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as exc:
        return [], [], [(0, f"cannot be read: {exc}")]
    return check_text(text)


def sections(lines, heading):
    """Where the section starts, under the matcher this read was given.

    The canonical heading always wins when the file has one. Without that, a
    base revision holding both `## Not verified` and a heading that merely
    mentions the phrase would be counted differently from the working tree,
    and the file would be reported as having lost rows nobody removed."""
    if isinstance(heading, str):
        return [i for i, text in headings(lines) if text.strip() == heading]
    exact = [i for i, text in headings(lines) if text.strip() == HEADING]
    return exact or [i for i, text in headings(lines) if heading.match(text)]


def check_text(text, heading=HEADING, strict_header=True):
    """The reader. One of it, for the working tree and for a base revision.

    There used to be two, and while both existed every property added to one
    had to be added to the other by hand. Four pairs drifted apart across
    three review rounds — which section is counted, how a cell is normalized,
    where a fence ends, how a path resolves — and each fix on one side opened
    a gap on the other.

    Three of those four are now shared outright. The fourth is these two
    arguments, and they say the same thing twice: a base revision may be
    written the way the corpus was before this normalization. Measured here,
    the files that changed did not only change the heading — they renamed the
    second column from `Who` to `Who must answer` — so relaxing the heading
    alone would still have stopped comparing them.

    Nothing else relaxes. A legacy header still has to be a two-cell row whose
    first column is `Item`, and every row below it is read exactly as the
    working tree's rows are. The relaxation ends when every base carries the
    canonical wording."""
    lines = readable(text)

    found = sections(lines, heading)
    if not found:
        near = [(i, text) for i, text in headings(lines) if LOOSE_HEADING.match(text)]
        hint = (
            f" (found `{near[0][1].strip()}` at line {near[0][0] + 1})" if near else ""
        )
        return [], [], [(1, f"no `{HEADING}` section{hint}")]
    if len(found) > 1:
        at = ", ".join(str(i + 1) for i in found)
        return (
            [],
            [],
            [(found[1] + 1, f"more than one `{HEADING}` section: lines {at}")],
        )

    start = found[0]
    end = len(lines)
    for i, _ in headings(lines):
        if i > start:
            end = i
            break
    return parse_section(lines[start + 1 : end], start + 2, strict_header)


def overviews(paths):
    """Every overview.md under the given paths, in a stable order."""
    found = []
    for p in paths:
        # The argument is resolved once, and nothing below it is. `ls-tree`
        # lists a tracked symbolic link under its own path, so resolving each
        # file made a link that is right there read as deleted.
        p = real(p)
        if os.path.isfile(p):
            found.append(p)
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            if OVERVIEW in files:
                found.append(os.path.join(root, OVERVIEW))
    return sorted(dict.fromkeys(found))


def real(path):
    """`path` with symbolic links resolved.

    Every path this compares has to come through here. `git rev-parse
    --show-toplevel` answers with links already resolved, so a caller who
    reaches the tree through one — `/tmp` on macOS is a link to `/private/tmp`,
    and a code directory linked from home is the same shape — produced a
    repo-relative path like `../link/specs`, which matches no line of
    `ls-tree`. Both comparisons then found nothing to do and the run passed:
    the state the ref check above exists to prevent, reached by another
    door."""
    return os.path.realpath(path)


def git_path(path):
    r"""`path` as git spells it: forward slashes, whatever `os.sep` is here.

    Every repo-relative path in this file is built by `os.path.relpath` and
    then handed to git — as a `show` argument, or compared against what
    `ls-tree` printed. git answers and accepts `/` on every platform, so on
    Windows the two sides were built by two rules: `specs\x\overview.md`
    against `specs/x/overview.md`. `show` returned None and the row check
    quietly compared nothing; the presence check matched no path and reported
    every tracked overview as deleted.

    A no-op where `os.sep` already is `/`, rather than branching on `os.name`:
    the substitution has to be on the path Linux CI runs, or the Windows half
    is proven by nothing. It also must not run there — a backslash is a legal
    character in a POSIX filename, and rewriting it would corrupt a real name.
    """
    return path if os.sep == "/" else path.replace(os.sep, "/")


def repo_relative(path, root):
    r"""`path` as a repo-relative git path, or None when it has no relative form.

    The composition `git_path(os.path.relpath(...))` is not safe on its own:
    `relpath` raises across drives, and the four sites that hand a path to git
    were left holding that raise while the two reporting sites got
    `display_path`. Measured: the run printed one row and then died mid-report
    with the very `ValueError` the helper beside this one exists to prevent.

    None rather than a fallback, because these four are asking git a question
    about a path INSIDE a repository. A path on another volume is not inside
    this one -- a working tree cannot span drives -- so there is no answer to
    degrade to, and inventing one is the quiet zero this tool refuses.
    `main` rejects that case up front; this is what makes the rejection
    total rather than a promise.
    """
    try:
        return git_path(os.path.relpath(path, root))
    except ValueError:
        return None


def display_path(path, start):
    r"""`path` relative to `start`, or absolute when there is no relative form.

    `os.path.relpath` raises `ValueError` on Windows when the two are on
    different drives, and this is the reporting footing for every line the
    tool prints. Running `unverified-check D:\repo\specs` from `C:\` is
    an ordinary thing to do, and it died with a traceback before printing a
    single row. The absolute path is a worse answer than a relative one and a
    far better one than no output at all.
    """
    try:
        return os.path.relpath(path, start)
    except ValueError:
        return os.path.abspath(path)


def nearest_existing(path):
    """`path`, or the closest ancestor of it that exists.

    A deleted directory still has to name the repository it was in."""
    p = os.path.abspath(path)
    while not os.path.exists(p) and os.path.dirname(p) != p:
        p = os.path.dirname(p)
    return p


def unique_by_target(paths):
    """One path per real file, first in sort order.

    A tracked symbolic link and the file it points at are one record and two
    paths. Counting both doubles its open items. Presence is a different
    question and keeps every path — `ls-tree` lists the link under its own
    name, so dropping it here would report a file that is right there as
    deleted."""
    seen, out = set(), []
    for p in paths:
        target = os.path.realpath(p)
        if target in seen:
            continue
        seen.add(target)
        out.append(p)
    return out


def repo_root(path):
    here = path if os.path.isdir(path) else (os.path.dirname(path) or ".")
    r = subprocess.run(
        ["git", "-C", here, "rev-parse", "--show-toplevel"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout.strip() if r.returncode == 0 else None


def commit_of(root, ref):
    """The commit `ref` names in `root`, or None.

    One reader for two questions — whether a ref resolves at all, and which
    commit it is. `resolves` below used to ask rev-parse itself and answer only
    the first; the second is what `base_label` needs, and asking twice is the
    duplicated-reader shape `check_text` above spent three review rounds
    closing."""
    r = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def resolves(root, ref):
    """Whether `ref` names a commit in `root`.

    Asked before anything is compared. An unresolvable ref used to make every
    comparison return "no base version", which is the same silence as a file
    that is genuinely new — so a CI checkout too shallow to hold the base
    branch turned the deletion check off and reported success.

    `chain_check.py` loads this module and calls this by name, which is why it
    stays a predicate rather than becoming `commit_of` at its call sites."""
    return commit_of(root, ref) is not None


def merge_base(root, ref):
    """The last commit `ref` and `HEAD` agreed on, or None.

    This is the revision every comparison below reads, and `ref` is not. The
    baseline a caller passes is the branch the pull request merges into, and
    that branch MOVES: the moment one work item squashes into it, every
    sibling branch cut before that squash has the squashed item's `overview.md`
    at the base and never had it at all. On the release that found this, three
    of four branches were refused for exactly that, and the refusal was right
    about what it measured and wrong about what happened (#272).

    The merge base is the fork point, so a file present there and absent here
    was removed by THIS branch — which is the only claim this tool makes. A
    file that arrived on the base after the fork is not this branch's business.

    None for two states, and both are exit 2 rather than a degraded pass:
    unrelated histories (exit 1, empty output) and a `HEAD` that names no
    commit (exit 128). A shallow clone whose base ref resolves while their
    common ancestor sits beyond the graft lands in the first."""
    r = subprocess.run(
        ["git", "-C", root, "merge-base", ref, "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def base_label(ref, ref_commit, base):
    """How a report names the revision it compared against.

    The shortest form that is TRUE, which is one rule and not a special case.
    Where the merge base IS the ref's own commit the ref names it exactly, and
    that is the ordinary run: `--baseline HEAD` locally, and CI, whose checkout
    on a `pull_request` event is the merge of the head into the base. Where the
    base has moved past the fork, naming the ref alone would send a reader to a
    commit this run never opened."""
    if base == ref_commit:
        return ref
    return f"the merge-base of {ref} and HEAD ({base[:7]})"


def overviews_at(root, ref, prefixes):
    """Repo-relative `overview.md` paths present at `ref` under `prefixes`.

    The scan walks the tree as it is now, so a file deleted wholesale never
    enters it and its rows leave without a word. Deleting the file was
    therefore cheaper and quieter than deleting one row from it, which is the
    behaviour the row check exists to make expensive."""
    r = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", ref],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        return []
    out = []
    for rel in r.stdout.splitlines():
        if os.path.basename(rel) != OVERVIEW:
            continue
        # The same skip list the scan walks with. Built by a different rule,
        # a tracked overview.md under build/ or node_modules/ would be absent
        # from every scan and so reported as deleted on every run — a red
        # build the author can only clear by renaming the directory.
        if set(os.path.dirname(rel).split("/")) & SKIP_DIRS:
            continue
        if any(p == "." or rel == p or rel.startswith(p + "/") for p in prefixes):
            out.append(rel)
    return out


def folded_items(root):
    """Work item ids whose SDD set has been folded into `docs/`.

    The removal of a released work item's directory is `settle`'s last act,
    and until this read existed the arm below could not tell it from a branch
    deleting a record. It is not a distinction the removal itself carries:
    both shapes are a directory present at the fork point and absent here.
    What tells them apart is whether a policy document absorbed the item, and
    the marker is that, written where the prose landed.

    Nothing outside `docs/` is read. `docs/` is where the fold writes, by
    `docs/one-root-by-lifetime.md` §*What happens at a release* step 2, and
    widening the scan to the whole tree would let a marker anywhere — a round
    record, a changelog fragment, the removed directory's own files at the
    base — excuse a removal nothing absorbed. A repository with no `docs/`
    folds nothing and gets an empty set, which is the state every repository
    was in before `settle` shipped.

    **The top level of `docs/` and no deeper**, for the same reason one step
    in. `spec.md` G2 and `skills/settle/SKILL.md` §2 fix the destination as a
    flat `docs/` — merge into a document that exists, create one only for a
    new area, and no `docs/policy/` directory — so a fold never writes below
    this level and a marker below it is somebody's notes. This repository's
    own `docs/experiments/` is four scratch files, and a quoted marker in one
    of them excused a removal nothing absorbed (measured 2026-09-22). The
    docstring above argued that scope for the tree and then did not apply it
    inside `docs/`.

    **A line has to be live, and `live_lines` is the one rule for it.** A
    fenced block is a quotation and a commented-out draft is a parked one;
    round 1 closed the first and round 2 found the second still open, with
    the same outcome both times — a directory removed at exit 0 with nothing
    having absorbed it. Round 3 then found the rule spelled here in full and
    in `settle.py#coordinates` by half, so neither reader spells it any more:
    both ask `live_lines`, which also blanks inline code spans before it asks
    the comment state, because a document that quotes `<!--` inside backticks
    would otherwise park every marker below it. The constant's own comment
    carries the measurements.
    """
    found = set()
    top = under_root(root, DOCS)
    if not os.path.isdir(top):
        return found
    for name in sorted(os.listdir(top)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(top, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        for line, live in live_lines(text.splitlines()):
            if live:
                found.update(FOLD_MARKER.findall(line))
    return found


# A released work item that wrote no `spec.md` states no rule, and the rule
# arm retires it with no marker: #517's owner decision D3, narrowed by one
# condition the frame recorded as a judgment the owner may overturn — nothing
# in its record may still be open. These are the files the arm reads.
SPEC = "spec.md"
EVIDENCE_TODO = "evidence-todo.md"
# The evidence-todo rule's two row shapes. `SEPARATOR` above reads one cell;
# these read a whole line, which is what the evidence-todo reader walks.
TODO_SEPARATOR_RE = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
DRAINED_RE = re.compile(r"^[\s*_]*drained\b", re.IGNORECASE)


def todo_open_rows(text):
    """Table body rows of an evidence-todo file that are still open.

    The rule, so a person can apply it by hand: a LIVE line outside a table
    whose first word is `drained` closes the whole file; otherwise every body
    row is open unless its first cell begins with ✅, and a row inside a
    fenced block that closes is an example and is not a row. A table is a run
    of lines starting with `|`; its first line is the header when the second
    is a separator, and neither is a body row.

    **The two halves read by opposite rules, and that is the direction rule**
    (#487). `drained` EXCUSES a file, so it counts only on a line
    `live_lines` calls live: one quoted in a fence, in an HTML comment or in
    a code span closes nothing, because closing a file on a quotation is the
    silent direction for a guard. A row HOLDS something, so it is skipped
    only when it is certainly quoted, which for a line is a fenced block that
    closes (`closed_fence_lines`). A row in a fence nobody closed, or in a
    comment, is read: a parked row is still somebody's open fact.

    Split on `\\n` alone: `splitlines()` also breaks on U+2028, U+0085 and
    form feed, so a cell holding one of those followed by `drained` closed the
    file — the silent direction for a guard.

    **It lives here because the rule arm's predicate reads it, and it is the
    one spelling there is.** `skills/settle/scripts/settle.py#open_rows` asks
    this function, and so does `.github/scripts/fold_ledger.py#open_rows`,
    which loads this module by path the way `.github/scripts/rider_check.py`
    loads the shipped checker. That script used to keep a copy on the ground
    that release automation and a shipped script may not depend on each
    other; `rider_check.py` had already taken that direction, and nothing
    held the two copies in step (#487).
    """
    lines = text.split("\n")
    live = [flag for _, flag in live_lines(lines)]
    quoted = closed_fence_lines(lines)
    rows = []
    n = 0
    while n < len(lines):
        line = lines[n]
        if n in quoted or not line.lstrip().startswith("|"):
            if live[n] and DRAINED_RE.match(line):
                return []
            n += 1
            continue
        table = []
        while n < len(lines) and n not in quoted and lines[n].lstrip().startswith("|"):
            table.append(lines[n])
            n += 1
        if len(table) >= 2 and TODO_SEPARATOR_RE.match(table[1].strip()):
            table = table[2:]
        for row in table:
            if TODO_SEPARATOR_RE.match(row.strip()):
                continue
            first = row.strip().strip("|").split("|", 1)[0].strip()
            if not first.startswith(CLOSED):
                rows.append(row)
    return rows


def tree_at(root, ref, directory):
    """Repo-relative paths under `directory` at `ref`; the disk when `ref` is
    None. `directory` is `/`-joined, and so is every path returned.

    Public because `survivor_check.py` asks it whether a directory is gone at
    the right end of its range, which keeps that module's own path-listing
    call sites at the count its case holds them to."""
    if ref is None:
        top = under_root(root, directory)
        out = []
        for here, dirs, files in os.walk(top):
            dirs.sort()
            for name in sorted(files):
                rel = os.path.relpath(os.path.join(here, name), root)
                out.append(git_path(rel))
        return out
    r = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", ref, "--", directory],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout.splitlines() if r.returncode == 0 else []


def _text_at(root, ref, rel):
    """What `rel` held at `ref`, or on disk when `ref` is None; None if absent."""
    if ref is not None:
        return show(root, ref, rel)
    try:
        with open(under_root(root, rel), encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def open_record_rows(root, ref, directory):
    """`[(file, what is open)]` for a work item's record at `ref`.

    The rows the rule arm refuses to take with a directory: every open item in
    `overview.md`'s `## Not verified`, and every open row of
    `evidence-todo.md`. Each is a claim with an answerer rather than a rule,
    and #514's frame measured the loss this prevents — the only record that a
    production workflow was red sat in a retiring overview (its L2).

    An overview whose section cannot be read is one entry saying so, never
    zero rows: a count this cannot read is not a count of nothing, which is
    the rule `check_text` above is written to. A base revision is read with
    the same relaxations the `--baseline` comparison gives it.
    """
    found = []
    overview = _text_at(root, ref, f"{directory}/{OVERVIEW}")
    if overview is not None:
        if ref is None:
            rows, _, errors = check_text(overview)
        else:
            rows, _, errors = check_text(
                overview, heading=LOOSE_HEADING, strict_header=False
            )
        if errors:
            found.append((OVERVIEW, f"cannot be read ({errors[0][1]})"))
        for _, item, _who in rows:
            found.append((OVERVIEW, item))
    todo = _text_at(root, ref, f"{directory}/{EVIDENCE_TODO}")
    if todo is not None:
        for row in todo_open_rows(todo):
            found.append((EVIDENCE_TODO, row.strip()))
    return found


def retired_by_rule(root, ref, directory):
    """Whether the rule arm may retire `directory` as it stood at `ref`.

    **The one predicate, and every reader of a retirement asks it here**:
    `settle` of the working tree (`ref` None), and `--baseline` below,
    `chain_check.py --baseline` and `survivor_check.py --range` of the
    merge-base they already compute. `plan.md` §*What breaks in six months*
    is why it is not spelled in each: the next condition added to it would
    land in one reader and not the others, and the first sign would be a fold
    pull request red in CI after `settle --retire` said the removal was fine.

    True when the directory existed at `ref`, held no `spec.md` there, and
    its record there held no open row (`open_record_rows`). Released-ness is
    not asked, because it is `settle`'s question about a ref this does not
    know; a CI reader's merge-base is by construction a commit the removal
    happened after.

    **A spec is asked of history, not of the tree at `ref` alone**
    (`wrote_a_spec`), so a `spec.md` deleted in one commit, or in an earlier
    pull request that has already merged, and the directory in the next still
    reads as a deletion. That is what makes this a rule about what the work
    item was, rather than about what it was left looking like.
    """
    paths = tree_at(root, ref, directory)
    if not paths:
        return False
    if f"{directory}/{SPEC}" in paths or wrote_a_spec(root, ref, directory):
        return False
    return not open_record_rows(root, ref, directory)


def wrote_a_spec(root, ref, directory):
    """Whether any commit reachable from `ref` (HEAD when None) touched
    `directory/spec.md`.

    D3 names a work item that WROTE no spec, which is a question about
    history rather than about one tree. Asked of the merge base alone, a spec
    deleted by an earlier merged pull request read as never written, and the
    next pull request retired the directory with no marker while every reader
    passed both (round 1's finding 3).

    A git failure answers *wrote one*, which keeps the directory. A shallow
    clone cut short of the deletion answers *never*, which is the reading
    before this existed; the CI checkout fetches the whole history.
    """
    r = subprocess.run(
        [
            "git",
            "-C",
            root,
            "log",
            # Without it, a merge commit whose result matches one parent for
            # this path is followed down that parent alone, and a spec added
            # and dropped on the other side is pruned. Every release reaches
            # `main` through such a merge, so the next release read a spec
            # its predecessor dropped as never written (round 2's finding 6).
            "--full-history",
            "-1",
            "--format=%H",
            ref or "HEAD",
            "--",
            f"{directory}/{SPEC}",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode != 0 or bool(r.stdout.strip())


def settled_root(path):
    """Whether `path` is a `seal/` root's own `specs` directory with no work
    item under it — empty on disk, or absent while the root is there.

    That is the state a complete fold reaches (#517, `spec.md` G7), and it is
    two states: the tree that ran `settle --retire` holds an empty
    `seal/specs/`, and a fresh checkout of the commit holds none, because git
    keeps no empty directory. Every pull request after the fold hands this
    tool `--baseline origin/<base> seal/specs/`, the shipped
    `templates/hygiene.yml` included, and reading that as a typo turned every
    one of them red. Only this one path is settled: any other path that is
    missing is still refused, which is what keeps `specs/ spces/` from
    passing in silence.
    """
    p = os.path.abspath(path)
    parent = os.path.dirname(p)
    if os.path.basename(p) != "specs" or os.path.basename(parent) != "seal":
        return False
    if not os.path.isdir(parent):
        return False
    if not os.path.isdir(p):
        return True
    return not any(os.path.isdir(os.path.join(p, n)) for n in os.listdir(p))


SETTLED = (
    "unverified-check: {path} holds no work item and its `seal/` root is "
    "there — the state a complete fold ends in, so there is nothing to read "
    "and nothing left the record without being closed"
)


def under_root(root, rel):
    """The disk path of a `/`-joined repository-relative path."""
    return os.path.join(root, *rel.split("/"))


def work_item_of(rel):
    """The work item id a repo-relative record path belongs to.

    The directory that holds the record, which is how every other reader of
    this layout names a work item — `gather_changelog.py#fragments` takes the
    same basename for the same reason.
    """
    return os.path.basename(os.path.dirname(rel))


def show(root, ref, rel):
    r = subprocess.run(
        ["git", "-C", root, "show", f"{ref}:{rel}"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout if r.returncode == 0 else None


def annotate(kind, path, line, message):
    """A GitHub annotation in CI, a plain line anywhere else."""
    if os.environ.get("GITHUB_ACTIONS"):
        # An annotation is matched against the diff by path, and GitHub spells
        # those the way git does. Every caller passes `display_path` output,
        # which is `os.sep`-spelled on purpose -- right for a line a person
        # reads, wrong for this. Unreachable while `hygiene.yml` pins
        # `ubuntu-latest`; live the moment these tools run on the Windows leg,
        # which is what the decision in `seal/ledger.md` points at.
        where = f" file={git_path(path)},line={line}" if path else ""
        return f"::{kind}{where}::{message}"
    return f"{path}:{line}  {message}" if path else message


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="unverified-check",
        description="Report open `## Not verified` items; fail on a record "
        "that cannot be read.",
    )
    ap.add_argument("path", nargs="*", default=["."])
    ap.add_argument(
        "--baseline",
        metavar="REF",
        help="the branch this pull request merges into. Also fail when a "
        "table holds fewer rows than it did where this branch forked from "
        "REF, or when an overview.md that existed there is gone — an item "
        "leaves by being marked closed, not by the row or the file being "
        "deleted. The comparison is against `git merge-base REF HEAD`, so a "
        "work item squashed into REF after this branch forked is not this "
        "branch's removal. Nor is a work item whose fold `docs/` records with "
        "its `<!-- specs/<id> -->` marker: that is `settle` retiring a "
        "released spec a policy document has absorbed, and it is named as "
        "folded rather than reported as a deletion. Nor is a directory "
        "removed whole that held no spec.md and nothing open at the merge "
        "base: `settle` retires that by the rule, with no marker, and it is "
        "named as retired by the rule",
    )
    args = ap.parse_args(argv)

    missing = [p for p in args.path if not os.path.exists(p) and not settled_root(p)]
    if missing and not args.baseline:
        print(f"unverified-check: no such path: {missing[0]}", file=sys.stderr)
        return 2
    # With a baseline, a path that is gone may be the thing being asked about:
    # the workflow runs `--baseline origin/<base> specs/`, and a change that
    # deletes specs/ used to be told it had mistyped an argument. A path that
    # held nothing at the base either is still a typo, and saying so is what
    # keeps `specs/ spces/` from passing in silence. That check needs the
    # repository, so it waits until the baseline block below has resolved one.

    # Resolved before the scan, because deleting every overview.md is the one
    # case where the scan finds nothing AND something has to be reported. It
    # used to exit 2 saying "nothing was checked", which reads as a bad
    # argument — and in a repository with one work item, deleting a single
    # file is that case.
    # `base` is the commit every comparison below reads and `named` is how a
    # report spells it. Resolved ONCE, here, because all three of the reads
    # below used to take `args.baseline` and a repair applied at any one of
    # them would leave two arms of one refusal reading two revisions.
    root = base = named = None
    if args.baseline:
        root = repo_root(real(nearest_existing(args.path[0])))
        if root is None:
            print(
                f"unverified-check: --baseline {args.baseline} needs a git "
                f"repository, and {args.path[0]} is not in one — nothing was "
                "compared",
                file=sys.stderr,
            )
            return 2
        ref_commit = commit_of(root, args.baseline)
        if ref_commit is None:
            print(
                f"unverified-check: --baseline {args.baseline} does not resolve "
                f"in {root} — nothing was compared. A shallow checkout or a "
                "renamed base branch lands here, and passing it would report "
                "a deletion check that never ran",
                file=sys.stderr,
            )
            return 2
        base = merge_base(root, args.baseline)
        if base is None:
            print(
                f"unverified-check: --baseline {args.baseline} and HEAD "
                f"share no history in {root} — nothing was compared. What "
                "this asks is what THIS branch removed, and without a commit "
                "they agree on there is no such question to answer",
                file=sys.stderr,
            )
            return 2
        named = base_label(args.baseline, ref_commit, base)
        # Every argument is compared against ONE repository, the one the FIRST
        # argument is in. That was always the rule and nothing stated it, so on
        # Windows a second argument on another drive reached `os.path.relpath`
        # and aborted the run mid-report. Said here instead: a path with no
        # relative form to `root` is not in `root`, because a working tree
        # cannot span volumes.
        outside = [
            p
            for p in args.path
            if repo_relative(real(nearest_existing(p)), root) is None
        ]
        if outside:
            print(
                f"unverified-check: {outside[0]} is not in {root} — nothing "
                "was compared. Every path is read against the repository the "
                "first one is in, and this one is on another volume",
                file=sys.stderr,
            )
            return 2

    if missing and args.baseline:
        typos = [
            p
            for p in missing
            if not overviews_at(
                root,
                base,
                [repo_relative(real(p), root)],
            )
        ]
        if typos:
            print(
                f"unverified-check: no such path: {typos[0]} — and nothing "
                f"under it at {named} either, so there is nothing to "
                "compare it against",
                file=sys.stderr,
            )
            return 2

    files = overviews(args.path)
    cwd = os.getcwd()
    total_open = total_closed = 0
    bad, deleted, uncompared, settled, ruled = [], [], [], [], []
    for path in unique_by_target(files):
        rel = display_path(path, cwd)
        open_rows, closed_rows, errors = check_file(path)
        total_open += len(open_rows)
        total_closed += len(closed_rows)
        for line_no, message in errors:
            bad.append(annotate("error", rel, line_no, message))
        if not errors and (open_rows or closed_rows):
            print(f"  {rel}  {len(open_rows)} open · {len(closed_rows)} closed")
            for _, item, who in open_rows:
                print(f"      open  {item}  —  {who}")

        if args.baseline and not errors:
            # An unreadable section returns zero rows, and comparing that zero
            # told the author to restore rows that never left.
            base_text = show(root, base, repo_relative(path, root))
            if base_text is None:
                continue
            base_open, base_closed, base_errors = check_text(
                base_text, heading=LOOSE_HEADING, strict_header=False
            )
            if base_errors:
                # Never a silent zero: a base this cannot read is a file whose
                # count is unknown, and saying so is the whole point of the
                # tool. It is not an error either — the author cannot edit a
                # commit that already happened.
                uncompared.append(
                    annotate(
                        "notice",
                        rel,
                        1,
                        f"not compared: the section at {named} could "
                        f"not be read ({base_errors[0][1]})",
                    )
                )
                continue
            was = len(base_open) + len(base_closed)
            now = len(open_rows) + len(closed_rows)
            if now < was:
                deleted.append(
                    annotate(
                        "error",
                        rel,
                        1,
                        f"{was} rows at {named}, {now} here. An item leaves "
                        f"this table by being marked {CLOSED} with what closed it, "
                        "never by being deleted",
                    )
                )

    if args.baseline:
        prefixes = sorted({repo_relative(real(p), root) for p in args.path})
        here = {repo_relative(f, root) for f in files}
        folded_ids = folded_items(root)
        for rel in overviews_at(root, base, prefixes):
            if rel not in here and work_item_of(rel) in folded_ids:
                # A fold, not a deletion. Named rather than passed over in
                # silence: a removal this arm stops reporting is one the
                # reader has to be able to see it decided about.
                settled.append(
                    annotate(
                        "notice",
                        display_path(os.path.join(root, rel), cwd),
                        1,
                        f"folded: `{DOCS}/` carries "
                        f"<!-- specs/{work_item_of(rel)} -->, so what this "
                        "recorded as unverified was absorbed by a policy "
                        "document before the directory was removed",
                    )
                )
                continue
            directory = os.path.dirname(rel)
            if (
                rel not in here
                and not os.path.isdir(under_root(root, directory))
                and retired_by_rule(root, base, directory)
            ):
                # The rule arm (#517 D3): the directory is gone, and at the
                # merge-base it held no `spec.md` and nothing open, which is
                # exactly what `settle --retire` removes without a marker. A
                # memo removed from a directory that stays is not this — a
                # retirement takes the whole directory.
                ruled.append(
                    annotate(
                        "notice",
                        display_path(os.path.join(root, rel), cwd),
                        1,
                        f"retired by the rule: at {named} the directory held "
                        f"no `{SPEC}` and nothing open in its record, so "
                        "it states no rule for a policy document to absorb "
                        "and nothing unverified left with it",
                    )
                )
                continue
            if rel not in here:
                # Relative to the caller's directory, like every other line
                # this prints. The two deletion reports used to answer on
                # different footings, which only agreed when the command ran
                # from the repository root.
                deleted.append(
                    annotate(
                        "error",
                        display_path(os.path.join(root, rel), cwd),
                        1,
                        f"present at {named} and not here. Whatever it "
                        "recorded as unverified left with it — a renamed "
                        "directory reads the same way, and says so out loud "
                        "rather than dropping the rows",
                    )
                )

    if not files and not deleted and not settled and not ruled:
        if all(settled_root(p) for p in args.path):
            print(SETTLED.format(path=", ".join(args.path)))
            return 0
        print(
            f"unverified-check: no {OVERVIEW} found under "
            f"{', '.join(args.path)} — nothing was checked",
            file=sys.stderr,
        )
        return 2

    print(
        f"\n{len(unique_by_target(files))} overviews · {total_open} open"
        f" · {total_closed} closed"
        f" · {len(bad)} unreadable"
        + (f" · {len(uncompared)} not compared" if uncompared else "")
        + (f" · {len(settled)} folded" if settled else "")
        + (f" · {len(ruled)} retired by the rule" if ruled else "")
    )

    if settled:
        print(f"\nfolded into {DOCS}/ and removed, not deleted from the record:")
        for line in settled:
            print(line)

    if ruled:
        print(
            f"\nretired by the rule — no `{SPEC}` and nothing open at the base, "
            "so no marker is owed:"
        )
        for line in ruled:
            print(line)

    if uncompared:
        print(f"\nnot compared against {named}:")
        for line in uncompared:
            print(line)

    if bad:
        print("\nthe record could not be read as it stands:")
        for line in bad:
            print(line)
        print(
            "\nThis is not a report of zero open items. A section this cannot "
            "read is a section whose count is unknown."
        )
    if deleted:
        print("\nrows left the record without being closed:")
        for line in deleted:
            print(line)
        print(
            "\nRe-add the row with " + CLOSED + " and what closed it. Deleting "
            "and verifying have to look different, or they are the same edit."
        )
    if bad or deleted:
        return 1

    if total_open == 0:
        print(f"open: 0 — every recorded item carries {CLOSED} and what closed it.")
    return 0


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
