# 1790659274 — round 3 report (warden)

| Field | Value |
|---|---|
| Target | round 2's fixes, `git diff ceff5460..43b81e3f` (3 commits), read at branch HEAD `ce0f1f94` |
| Kind | verifying round after the one reopening: the fix diff, not the branch, and the run ends here |
| Earlier rounds | round 1 and round 2 (`round-N.md`, `round-N-report.md`), read for coordinates |
| Where it ran | a `git clone --no-local` of the orchestrator's tree at `ce0f1f94`, under `<scratchpad>/1790659274/round-3/` |

## How the findings relate

- **Round 2's two verdicts are closed.** A bullet or a number on a
  paragraph's later line is text again, and each of the helper's branches
  now has a row that goes red when that branch is removed (executed, seven
  mutants).
- **The shapes the prompt named all count right.** Lazy continuation lines,
  a quote whose later line drops the `>`, a list item continued by
  indentation, a setext heading, and the round-2 shapes inside containers
  give the line a renderer hides (executed, 13 shapes).
- **But one marker is still read where the parser reads text, and that is
  🟡 1.** The fix states that a `>` on a later line is always a quote marker.
  A `>` indented four columns or more, or behind a tab, is a lazy
  continuation line's text, and the parser keeps it. The helper skips it and
  places inline HTML one line late.
- **This is the third instance of one class in three rounds.** Round 1 read
  too few markers on the opening line, round 2 too many on later lines, and
  round 3 finds a `>` that is not one. Each fix aimed at the coordinate the
  finding named. The paste-ready fix below takes the count from the parser's
  own state instead of re-deriving it, so the class goes and not the
  instance.
- **The oracle is still independent of the walk.** It imports `markdown_it`
  alone, and the proposed fix keeps it that way.

## 🟡 1 · A `>` four columns in on a paragraph's later line is text, and the oracle reads it as a quote marker

`tests/commonmark_oracle.py:89` (the `>` branch of `_behind_markers`),
called from `tests/commonmark_oracle.py:131` in `_inline_html_lines`.

Round 2's fix returns before the list-marker branches on a later line, but
keeps the `>` branch for every line. Its docstring gives the reason: *"A `>`
on a later line is a marker, for the same reason."* That holds only where the
`>` stands at most three columns into its container. CommonMark 5.1 allows a
block quote marker 0–3 spaces of indentation. On a paragraph's later line a
`>` further in is a lazy continuation, because an indented code block cannot
interrupt a paragraph. markdown-it-py agrees: its paragraph rule takes any
line indented more than three columns as a continuation, and on
`[NBSP, "    >", "x <? a", "b ?>"]` the paragraph's inline content is
`'>\nx <? a\nb ?>'` (executed). The helper strips every leading space and tab
without counting columns, reads the `>`, finds nothing behind it, and skips
the line as blank.

Executed at `ce0f1f94`, the probe gives `{}` where a renderer hides line 3 on
five shapes:

- `[NBSP, "    >", "x <? a", "b ?>"]`, a `>` four spaces in at the top level;
- `[NBSP, "\t>", ...]`, the same behind a tab;
- `["- " + NBSP, "      >", "  x <? a", "  b ?>"]`, four columns into a list item;
- `["> " + NBSP, ">     >", "> x <? a", "> b ?>"]`, four columns into a quote;
- `[NBSP, "    > >", ...]`, two of them.

The late index falls past the document and is dropped, so the oracle hides
nothing. With a blank line and a row after the HTML line, the late index
lands on the blank line instead: `[NBSP, "    >", "x <? a", "b ?>", "", "text"]`
gives `{4: 'inline html'}`, and the property's `disagreements` is
`[(4, 'live', True)]`. The same holds for the tab and the list-item shapes.

**Why it matters.** It is the false red round 2's 🟡 1 described, from the
other marker. The walk rightly claims the blank line live, the oracle says
hidden, and the edit it invites is a change to the walk toward a wrong
oracle. `ALPHABET` holds `"    code"` and `"\tcode"` but no line that is an
indented `>`, so the seeded corpus does not reach it. It does not lose a
record, and nothing that reads the repository's files runs the oracle.

**Why the fix is not a column count.** Counting columns before the `>` is not
enough on its own. A `>` inside a list item may stand as far in as the item's
content indent plus three, and the helper does not know that indent: on
`10. > a` followed by `    > b`, the `>` four columns in is a real marker,
and the parser's inline content is `'a\nb'` (executed).
The helper would have to rebuild the block parser's container stack, which is
what three rounds have been doing one marker at a time.

**The fix.** The parser already knows the lines it joined. Its `paragraph`
and `lheading` block rules build the inline source as
`state.getLines(*map, state.blkIndent, False).strip()`, where each line is
taken from behind the container markers the parser itself consumed. The fix
wraps those two rules the way the module already wraps `html_inline`, and
counts the whole lines that strip removed from the top of that same text.
`_behind_markers` is deleted. The approach fits the module's own principle,
*"Where the inline HTML is, the parser says"*, and imports only from
`markdown_it`.

Executed in the clone:

- the five wrong shapes and the 13 right ones all correct (18 of 18);
- the property module with the fix and four new rows: exit 0, 91 passed;
- the three `>` rows against the oracle at HEAD: exit 1, 3 failed, 88 passed,
  each of the three by id;
- the fix with the dropped-line count forced to 0: exit 1, 16 failed,
  covering the 15 marker rows, the setext row and
  `test_where_the_walk_claims_to_be_exact_it_is`;
- the fix with `lheading` left unwrapped: exit 1, 1 failed, the setext row
  alone. That is why the setext row is in the fix: without it, nothing pins
  the second wrapper.

**Where it goes.** The run ends at this round, so which home this finding
takes is the orchestrator's ladder. The fact the ladder turns on is this:
`_behind_markers` is round 1's `New units` row, and round 2's fix edited it,
so the unit is the branch's.

## ⬜ 2 · Ledger row R1-1 states the claim 🟡 1 shows false

`seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md`,
row R1-1. The fix commit `43b81e3f` rewrote it to say the oracle counts back
behind *"a block quote's `>` on every line"*. A `>` four columns in on a later
line is not a marker (🟡 1, executed). This is a correction to the run's
records and not a defect in the tool. If 🟡 1's fix lands, the row's
`_behind_markers` anchor is removed, so the row is REMOVED and the new claim
is written as a new row. If it does not land, the sentence needs the
three-column bound.

## Round 2's findings

**Round 2's finding 1 is closed.** `_behind_markers` now returns before the
list-marker branches on every line after the paragraph's opening one
(`tests/commonmark_oracle.py:92`). Executed: a `*` on the later line of a
list item's paragraph gives the line a renderer hides. Where a lazy `*`
follows a list item, or a lazy `2.` follows a quote, the parser ends the
container there, and the oracle follows the parser's tokens and is right
too. With the new guard removed, the two new rows
go red (`a star on a later line is text`, `a number on a later quoted line
is text`) and nothing else does. With the guard moved in front of the quote
branch, `a quote marker on a later line` goes red alone.

**Round 2's finding 2 is closed.** Each of the five branches round 2 named now
has a row that fails when the branch is removed (executed, one mutant at a
time, restored):

| Mutant | Rows that fail |
|---|---|
| bullets are `-` only | `behind a plus`, `behind a star`, `a tab before a marker` |
| the delimiter is `.` only | `behind a parenthesis` |
| no nine-digit bound | `ten digits are no marker` |
| a tab not skipped before a marker | `a tab before a marker` |
| a tab not accepted after a marker | `a tab after a marker` |

## What the account asserted, and what I found

| Claimed | Where | What I found |
|---|---|---|
| `_behind_markers` reads a bullet or a number only on the paragraph's opening line | commit `37dadb8d`, the helper's docstring | **Confirmed, executed**: a later-line `*` in a list item right, and the guard's two rows red without it |
| *"A `>` on a later line is a marker, for the same reason"* | `tests/commonmark_oracle.py:83` | **False for a `>` four columns in or behind a tab** (🟡 1, executed on five shapes) |
| R1-1: the count reads *"a block quote's `>` on every line"* | ledger fragment, R1-1 | False for the same shapes (⬜ 2) |
| Six rows pin the helper's other branches | commit `37dadb8d` | **Confirmed, executed**: each of the five branch mutants turns at least its own row red |
| The `>` on a later line stays a marker, pinned by a row | commit `717ba0bb` | **Confirmed, executed**: the row fails only when the quote branch is skipped on later lines |
| The ledger fragments check clean after P1-1, R1-1 and P1-2 were re-read | commit `43b81e3f` | **Executed**: `bin/evidence-check --ledger` exit 0 on both fragments, 0 drifted |
| The oracle imports nothing of this repository's | `tests/test_the_hooks_hide_what_a_renderer_hides.py`, S1 | **Executed**: green in the module run (87 passed). The fix keeps `imported_roots` at `{"markdown_it"}`, green in the 91-passed run |

## Regression tests to plant

In `tests/test_the_hooks_hide_what_a_renderer_hides.py`,
`test_the_oracle_names_each_kind_it_hides`, after
`ten digits are no marker`: the four rows in the second fence below. The three
`>` rows were run red against the oracle at HEAD and green with the fix. The
setext row is green at HEAD and was run red with the `lheading` wrapper
removed from the fix.

## Facts for the evidence ledger

- R1-1 goes REMOVED when 🟡 1's fix deletes `_behind_markers`. The new claim
  is a new row in this work item's fragment: the oracle takes the number of
  lines the parser's strip dropped from the parser's own paragraph and
  setext-heading rules, which join each line from behind the container
  markers the parser consumed.
- P1-1's `_inline_html_lines` anchor drifts under the same fix and is re-read
  against it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `>` four columns in, or behind a tab, on a paragraph's later line is lazy-continuation text the parser keeps; `_behind_markers` reads it as a quote marker, and every inline HTML line after it is placed one line late | `tests/commonmark_oracle.py:89` | open | executed: 5 of 18 shapes wrong at HEAD; `[NBSP, "    >", "x <? a", "b ?>", "", "text"]` gives `disagreements` `[(4, 'live', True)]`. The unit is round 1's `New units` row, which round 2's fix edited, so it is the branch's; the run ends here, so its home is the orchestrator's ladder |
| ⬜ 2 | Ledger row R1-1 says the count reads a block quote's `>` on every line, which finding 1 shows false | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | open | a correction to the run's records; the row is REMOVED if finding 1's fix deletes its anchor |
| 🟢 | round 2's finding 1 is closed — a bullet or a number on a paragraph's later line is text again | `tests/commonmark_oracle.py:92` | confirmed | executed: a later-line `*` in a list item right; removing the guard fails the two new rows alone, and moving it before the quote branch fails the quote row alone |
| 🟢 | round 2's finding 2 is closed — every branch round 2 named has a row that goes red without it | `tests/test_the_hooks_hide_what_a_renderer_hides.py:127` | confirmed | executed: five mutants, each exit 1, each failing its own row |
| 🟢 | The oracle is still independent of the walk | `tests/commonmark_oracle.py:50` | confirmed | executed: the import case is green at HEAD and with finding 1's fix |
| 🟢 | The fix pass's ledger rows check clean | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | confirmed | executed: `bin/evidence-check --ledger` exit 0 on both fragments `43b81e3f` touched |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` at `ce0f1f94` | exit 0, 87 passed |
| Probe: `oracle.hidden` and the paragraph's inline content on 18 shapes (indented `>` on a later line, lazy continuation, a quote dropping `>`, an item continued by indentation, setext), and `disagreements` on three with the HTML line last | at HEAD: 13 correct, 5 wrong; `disagreements` `[(4, 'live', True)]` on all three |
| Seven mutants of `_behind_markers`, one at a time, restored from kept bytes, against the property module | each exit 1; failing ids as in the table under *Round 2's findings*; `git diff --quiet` exit 0 after |
| 🟡 1's fix applied in the clone, then the 18-shape probe and the module | probe 18 of 18 correct; module exit 0, 87 passed |
| The four new rows with the oracle at HEAD, with the fix, with the fix's dropped-line count forced to 0, and with `lheading` unwrapped | exit 1 (3 failed); exit 0 (91 passed); exit 1 (16 failed); exit 1 (1 failed, the setext row) |
| `bin/evidence-check --ledger` on the two fragments `43b81e3f` touched | exit 0 each, 0 drifted |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet — no run has been made; it comes due now, as the sealer's spawn |

## Paste-ready fixes

### 🟡 1

```python
# tests/commonmark_oracle.py -- the imports
from markdown_it import MarkdownIt
from markdown_it.rules_block.lheading import lheading
from markdown_it.rules_block.paragraph import paragraph
from markdown_it.rules_inline.html_inline import html_inline


# tests/commonmark_oracle.py -- a wrapper after `_recording_html_inline`,
# and two lines in `parser`
def _recording_lines(rule):
    """A block rule of the parser's that joins lines into an inline token's
    source, with the number of whole lines its strip dropped from the top
    kept on that token. The joined text is the parser's own: each line is
    taken from behind the container markers the parser itself consumed, so
    no marker is read here (#673 round 3, 🟡 1)."""

    def recorded(state, start, end, silent):
        count = len(state.tokens)
        found = rule(state, start, end, silent)
        if found and not silent:
            for token in state.tokens[count:]:
                if token.type == "inline" and token.map:
                    joined = state.getLines(*token.map, state.blkIndent, False)
                    dropped = joined[: len(joined) - len(joined.lstrip())]
                    token.meta = {"dropped": dropped.count("\n")}
        return found

    return recorded


def parser():
    md = MarkdownIt("commonmark").enable("table")
    md.inline.ruler.at("html_inline", _recording_html_inline)
    md.block.ruler.at("paragraph", _recording_lines(paragraph))
    md.block.ruler.at("lheading", _recording_lines(lheading))
    return md


# tests/commonmark_oracle.py -- `_behind_markers` is deleted whole.


# tests/commonmark_oracle.py#_inline_html_lines -- the docstring's last
# paragraph, and the count that replaces the while loop
    The inline source is the paragraph's lines joined, with Python's
    `str.strip` applied to the whole by the parser. That strip also takes a
    line holding only a no-break space or another Unicode space, which
    CommonMark reads as paragraph text, so the lines it dropped from the top
    are counted before an offset is turned into a line. The parser's own
    block rule counts them, from the lines it joined behind the markers it
    consumed: three rounds read those markers here, and each missed a
    different one (#673 rounds 1 to 3).
    """
    out = set()
    if not inline.map or not inline.children:
        return out
    first = inline.map[0] + (inline.meta or {}).get("dropped", 0)
    src = inline.content
```

```python
# tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides
# -- four rows after "ten digits are no marker"
        # a `>` four columns in, or behind a tab, on a paragraph's later line
        # is lazy-continuation text the paragraph keeps, not a quote marker
        ([NBSP, "    >", "x <? a", "b ?>"], {3: "inline html"}),
        ([NBSP, "\t>", "x <? a", "b ?>"], {3: "inline html"}),
        (["- " + NBSP, "      >", "  x <? a", "  b ?>"], {3: "inline html"}),
        # a setext heading's text is joined and stripped as a paragraph's is
        ([NBSP, "x <? a", "b ?>", "==="], {2: "inline html"}),
# -- and their ids
        "a > four columns in is text",
        "a > behind a tab is text",
        "a > four columns into an item is text",
        "a setext heading counts as a paragraph does",
```

Needs a fix: yes — 🟡 1 (a `>` four columns in on a paragraph's later line is text, and the oracle reads it as a quote marker and places inline HTML one line late)
Loses a record or crashes: no

## Proof block

Files opened in this round, at `ce0f1f94` in the clone unless marked:

- `tests/commonmark_oracle.py`
- `tests/test_the_hooks_hide_what_a_renderer_hides.py` (lines 1–180, 180–520)
- `seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/rounds/round-2.md`
- `seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/rounds/round-2-report.md` (to its account table)
- `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` and `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` (the rows `43b81e3f` changed)
- `docs/review-chain-spec.md` (the cap, the reopening and the ladder sections)
- markdown-it-py 4.2.0's paragraph and lheading block rules, `StateBlock.getLines`, the block parser's rule table and `Ruler.at`, in the clone's virtual environment
