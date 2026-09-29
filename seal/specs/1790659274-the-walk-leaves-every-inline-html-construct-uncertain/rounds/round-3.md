# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — review round 3

| Field | Value |
|---|---|
| Target SHA | ce0f1f94381d2962787ff1f58aed8c6307cfb696 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #676 |
| Broad gate | eaf3043a against 86256492 |
| Fixes checked by | no fixes to check |
| Fix range | `ce0f1f94381d2962787ff1f58aed8c6307cfb696..9b4db624d5ae5ea819aa3ce4ada6439966ea50dd`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a `>` four columns in on a paragraph's later line is text, and the oracle reads it as a quote marker and places inline HTML one line late) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening. Target round 2's fix diff `ceff5460..43b81e3f` at HEAD `ce0f1f94`, with the new rows as a finding surface: does `_behind_markers` match CommonMark on a paragraph's opening line and every later one, and is the oracle still independent of the walk.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `>` four columns in, or behind a tab, on a paragraph's later line is lazy-continuation text the parser keeps; `_behind_markers` reads it as a quote marker, and every inline HTML line after it is placed one line late | `tests/commonmark_oracle.py:89` | deferred #677 | #677 — The run is capped. The oracle's hand-read markers misread a third shape; #677 replaces `_behind_markers` with the parser's own dropped-line count in this release, after this lands; executed: 5 of 18 shapes wrong at HEAD; `[NBSP, "    >", "x <? a", "b ?>", "", "text"]` gives `disagreements` `[(4, 'live', True)]`. The unit is round 1's `New units` row, which round 2's fix edited, so it is the branch's; the run ends here, so its home is the orchestrator's ladder |
| ⬜ 2 | Ledger row R1-1 says the count reads a block quote's `>` on every line, which finding 1 shows false | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | deferred #677 | #677 — R1-1 is REMOVED with the helper when #677 lands; a correction to the run's records; the row is REMOVED if finding 1's fix deletes its anchor |
| 🟢 | round 2's finding 1 is closed — a bullet or a number on a paragraph's later line is text again | `tests/commonmark_oracle.py:92` | confirmed | executed: a later-line `*` in a list item right; removing the guard fails the two new rows alone, and moving it before the quote branch fails the quote row alone |
| 🟢 | round 2's finding 2 is closed — every branch round 2 named has a row that goes red without it | `tests/test_the_hooks_hide_what_a_renderer_hides.py:127` | confirmed | executed: five mutants, each exit 1, each failing its own row |
| 🟢 | The oracle is still independent of the walk | `tests/commonmark_oracle.py:50` | confirmed | executed: the import case is green at HEAD and with finding 1's fix |
| 🟢 | The fix pass's ledger rows check clean | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | confirmed | executed: `bin/evidence-check --ledger` exit 0 on both fragments `43b81e3f` touched |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/commonmark_oracle.py:96` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/blocks.py:231` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/blocks.py:233` | round 1's ⬜ 3 — answered |
| round-1 | `hooks/blocks.py:213` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_rider_reaches_its_file.py#test_a_break_commonmark_does_not_honour_quotes_no_rider` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_hooks_hide_what_a_renderer_hides.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/blocks.py` | round 1's ❓ — out of verified scope |
| round-2 | `tests/commonmark_oracle.py:76` | round 2's 🟡 1 — fixed |
| round-2 | `tests/commonmark_oracle.py:90` | round 2's ⬜ 2 — fixed |
| round-2 | `tests/commonmark_oracle.py:125` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_hooks_hide_what_a_renderer_hides.py:651` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
