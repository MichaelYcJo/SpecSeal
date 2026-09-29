# 1790659274-the-walk-leaves-every-inline-html-construct-uncertain — review round 2

| Field | Value |
|---|---|
| Target SHA | db4707b5cebd49800362c56a9ea75a06f35331f6 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #676 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `ceff5460b967b441fc79c5b795ffced05a63b159..43b81e3f13aaf63c2195da563b48618db9567976`, 3 commits |
| Contract changes | _behind_markers → round-1-report.md, round-1.md, round-2-report.md, round-2.md, pytest |
| New units | none |
| Needs a fix | yes — 🟡 1 (the oracle reads a list marker on a paragraph's later lines, where a lone `*` or `2.` is text, and places inline HTML one line late) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, verifying, over round 1's fix diff `c0d9045b..c041b5ed` at HEAD `db4707b5`. Asked whether each verdict round 1 closed is closed, with `_behind_markers` and its pins as a finding surface: does it count behind every marker CommonMark allows, and does it agree with the walk by construction.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_behind_markers` reads a list marker on every line the count-back hands it, but only the paragraph's opening line can carry one; a later line of only `*`, `+`, `1.`, `2.` or `2)` is text the parser keeps, so it is skipped and every inline HTML line after it is placed one line late | `tests/commonmark_oracle.py:76` | **fixed** `37dadb8d` | fixed at 37dadb8d — with `717ba0bb` pinning that `>` stays a marker on later lines: `_behind_markers` reads a bullet or a number only on the paragraph's opening line; executed: `[NBSP, "*", "x <? a", "b ?>", "", "text"]` gives `{4: ...}` where a renderer hides line 3, and the property's `disagreements` is `[(4, 'live', True)]`; 15 of 37 probe shapes wrong at HEAD, 0 with the fix |
| ⬜ 2 | Five branches of `_behind_markers` are pinned by no case: `+` and `*`, the `)` delimiter, the nine-digit bound, a tab before a marker, a tab after one | `tests/commonmark_oracle.py:90` | **fixed** `37dadb8d` | fixed at 37dadb8d — one row per unpinned branch — `+`, `*`, `1)`, a tab after and a tab before a marker, the ten-digit non-marker; executed: each mutant exit 0, 78 passed; the behaviour is right at HEAD on all 20 first-line shapes |
| 🟢 | round 1's finding 1 is closed for the shape it reported — a list item whose first line holds only a Unicode space | `tests/commonmark_oracle.py:125` | confirmed | executed: `["- " + NBSP, "x <? a", "b ?>", "c"]` and 19 more first-line shapes give line 2; the four rows are green. The new unit's own defect is 🟡 1 above |
| 🟢 | round 1's finding 2 is closed — S4 pins `<?>` not closing, a closer before its opener, and a `>` inside a single-quoted value | `tests/test_the_hooks_hide_what_a_renderer_hides.py:651` | confirmed | executed: each assertion's shape reads `[False, False]` under its own mutant and `[False, True]` at HEAD; the module fails under each of m1, m2 and m3 |
| 🟢 | round 1's finding 3 is answered on grounds that reproduce | `hooks/blocks.py:233` | confirmed | executed: 583 tracked `.md` files, 0.169 s at HEAD against 0.145 s at the base, the slowest 8.6 ms |
| 🟢 | The fix pass's ledger rows check clean | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | confirmed | executed: `bin/evidence-check --ledger` exit 0 on both fragments the fix commit touched |

## Paste-ready fixes

```python
# tests/commonmark_oracle.py -- replaces the head of `_behind_markers`
def _behind_markers(line, opens):
    """Where LINE's own text starts behind its containers' markers: a block
    quote's `>`, a bullet, an ordered number (CommonMark 5.1, 5.2), each with
    the spaces and tabs before it. A bullet or a number is a marker only
    where a space, a tab or the line's end follows it, and only on the line
    that OPENS the paragraph: on a later line of it a `*` or a `2.` is text,
    because a list item that could interrupt the paragraph would have ended
    it. A `>` on a later line is a marker, for the same reason."""
    at = 0
    while True:
        rest = line[at:]
        text = rest.lstrip(" \t")
        skip = len(rest) - len(text)
        if text.startswith(">"):
            at += skip + 1
            continue
        if not opens:
            return at
        digits = len(text) - len(text.lstrip("0123456789"))
        # ... the rest of the body unchanged


# tests/commonmark_oracle.py#_inline_html_lines -- the loop's condition
    while (
        first < inline.map[1] - 1
        and not lines[first][
            _behind_markers(lines[first], first == inline.map[0]) :
        ].strip()
    ):
        first += 1


# tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides
# -- two rows after "a dash that is no marker"
        # a later line of the paragraph carries no list marker: a `*` or a
        # `2.` there is text, since an item that could interrupt would have
        # ended the paragraph, and the parser's strip keeps it
        ([NBSP, "*", "x <? a", "b ?>", "c"], {3: "inline html"}),
        (["> " + NBSP, "> 2.", "> x <? a", "> b ?>"], {3: "inline html"}),
# -- and their ids
        "a star on a later line is text",
        "a number on a later quoted line is text",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` at `db4707b5` | exit 0, 78 passed |
| Probe: `oracle.hidden` and the property's `disagreements` on 20 first-line marker shapes, 1 item with two blank-looking lines, 12 continuation shapes, and 4 with the HTML line last in its paragraph | at HEAD: 22 correct; 15 wrong, 3 of them red in `disagreements` |
| The paragraph's inline content, and `_starts_in_inline_html` at each line start, on the `*` and the quoted `2.` shapes | content keeps `*` and `2.`; the mark is inside HTML at line 3 alone in both |
| 🟡 1's fix and two rows applied in the clone, then the probe and the module | probe: 37 of 37 correct; module exit 0, 80 passed |
| The two new rows with the oracle at HEAD | exit 1, 2 failed, 21 passed |
| m1, m2 and m3 of `hooks/blocks.py`, one at a time, restored from kept bytes, against the S4 case; and each new shape evaluated under each mutant | each exit 1; failing line 653 (m1, m2) and 659 (m3); the matrix reads `[False, False]` only where the mutant targets the shape |
| Five mutants of `_behind_markers` (⬜ 2), one at a time, restored, against the property module | each exit 0, 78 passed |
| `walk_text` over the 583 tracked `.md` files, best of three, HEAD against `hooks/blocks.py` from `3fc0c5bd` | 0.169 s against 0.145 s; slowest file 8.6 ms against 7.4 ms |
| `bin/evidence-check --ledger` on the two fragments `c041b5ed` touched | exit 0 each |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet — no run has been made, and it is the sealer's once the rounds settle |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
