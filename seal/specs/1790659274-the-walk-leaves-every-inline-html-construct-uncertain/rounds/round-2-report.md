# 1790659274 — round 2 report (warden)

| Field | Value |
|---|---|
| Target | round 1's fixes, `git diff c0d9045b..c041b5ed` (2 commits), read at branch HEAD `db4707b5` |
| Kind | verifying round: the fix diff, not the branch |
| Earlier rounds | round 1 (`round-1.md`, `round-1-report.md`), read for coordinates |
| Where it ran | a `git clone --no-local` of the orchestrator's tree at `db4707b5`, under `<scratchpad>/1790659274/round-2/` |

## How the findings relate

- **Round 1's three verdicts hold.** The list-marker shape it reported now
  counts right (finding 1), each new S4 assertion goes red under the mutant
  it targets (finding 2), and the cost measurement behind the answer to
  finding 3 reproduces.
- **But the new helper overcorrects, and that is this round's 🟡 1.**
  `_behind_markers` reads a list marker on every line it is handed. Only the · NAME NOT IN TREE
  paragraph's first line can carry one. On a later line, a `*` or a `2.`
  standing alone is paragraph text that the parser's strip keeps, and the
  helper skips it as if it were a marker. Every inline HTML line after it is
  then counted one line late. When the HTML line is the paragraph's last,
  the property goes red on a document the walk reads right.
- **The markers the prompt asked about are all counted right on the first
  line (executed), and five of the branches that handle them are pinned by
  no case (⬜ 2).**
- **The oracle does not agree with the walk by construction.** It still
  imports `markdown_it` alone (the import case is green), and the helper is
  its own reading of CommonMark 5.1 and 5.2. That independence is why it can
  be wrong in a way the walk is not.

## 🟡 1 · A later line of only `*` or `2.` is counted as a marker, so the oracle places inline HTML one line late

`tests/commonmark_oracle.py:76` (`_behind_markers`), called from · NAME NOT IN TREE
`tests/commonmark_oracle.py:125` in `_inline_html_lines`.

The count-back loop hands the helper each line from `inline.map[0]` onward
while the line reads blank behind its markers. Only the first of those lines
opens the paragraph. A later line of the same paragraph carries no list
marker, because a list item that could interrupt a paragraph would have
ended it. An empty item cannot interrupt a paragraph, and neither can an
ordered item that does not start at 1 (CommonMark 5.2). So on a later line
`*`, `+`, `1.`, `2.`, `2)`, `10)` or `2. ` plus a no-break space is text. The
parser keeps it: on `[NBSP, "*", "x <? a", "b ?>", "", "text"]` the paragraph's
inline content is `'*\nx <? a\nb ?>'` (executed). The helper returns the
offset past that `*`, the line reads blank, and the loop skips it.

Executed at `db4707b5`:

- `oracle.hidden([NBSP, "*", "x <? a", "b ?>", "", "text"])` gives
  `{4: 'inline html'}`. A renderer hides line 3, where `b ?>` begins inside
  the processing instruction; the mark method (`_starts_in_inline_html` at
  each line start) says the same, `True` at line 3 alone. Line 4 is the
  blank line after the paragraph.
- The property's own `disagreements` on that document is
  `[(4, 'live', True)]`: the walk claims the blank line live, which is
  right, and the oracle says it is hidden. The same holds with `2.` in place
  of `*` and a row after the blank line, and with two such lines (`*`, `+`)
  the count is two lines late.
- Nine continuation shapes (`*`, `+`, `1.`, `2.`, `2)`, `2. ` plus NBSP,
  `10)`, `*` plus a tab, `2.` plus two spaces) and two inside containers
  (`> *` in a quote, `  2.` in a list item) all put the HTML line one late.
  In a quote, `["> " + NBSP, "> 2.", "> x <? a", "> b ?>"]` gives `{}`: the
  late index falls past the document and is dropped, so the oracle hides
  nothing where a renderer hides line 3.

**Why it matters.** This is the same class as round 1's finding 1, a
miscount of the lines `str.strip` dropped, now in the other direction. When
the HTML line sits inside the paragraph, the walk is uncertain on every line
after the opener, so the late line costs nothing. When it is the paragraph's
last line, the late index lands on the next block, and a line the walk
rightly claims live reads as hidden. That is a false red, and the edit it
invites is a change to the walk toward a wrong oracle, which is the cost
round 1 named. `ALPHABET` holds no line that is only a marker today, so the
seeded corpus does not reach it. The first person to add `"*"` or `"2."` to
the alphabet meets it. It does not lose a record, and nothing reading the
repository's files runs the oracle.

**The fix.** A list marker is read only on the line that opens the
paragraph. On later lines only a quote's `>` is a marker, since a `>` in
paragraph text would have opened a quote. Applied in the clone: all 37 probe
shapes correct (the 22 that were right stay right and the 15 that were
wrong come right), the two new rows below red with the oracle at HEAD
(`2 failed, 21 passed`) and green with the fix, and the property module
exit 0, 80 passed. The helper still imports nothing, so
`test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys` holds.

## ⬜ 2 · Five of the helper's branches are pinned by no case

`tests/commonmark_oracle.py:84-96`. The four rows round 1's fix planted pin
the `-` bullet, the `.` delimiter, the quote branch and the space-after
check. These mutations of `_behind_markers` each leave the property module · NAME NOT IN TREE
green (exit 0, 78 passed, executed one at a time and restored):

| Mutant | Exit |
|---|---|
| bullets are `-` only (`+` and `*` dropped) | 0 |
| ordered delimiter is `.` only (`)` dropped) | 0 |
| no nine-digit bound on an ordered number | 0 |
| a tab not skipped before a marker | 0 |
| a tab not accepted after a marker | 0 |

The behaviour itself is right at HEAD. Executed: `+ `, `* `, `1) `, `2) `,
`123456789. `, `  - `, `   1. `, `-\t`, `-   `, `- - `, `1. - `, `- 1) `,
`> > - `, `>- `, `- > `, `>\t* `, `  > + `, and `- ` with U+3000, each
followed by a Unicode space and then the inline HTML lines, all give the
line a renderer hides. So nothing ships wrong if this stands. It is the
same gap round 1's finding 2 named in `hooks/blocks.py`, here in test code:
an edit that narrows the bullet set turns nothing red. Rows are listed under
*Regression tests to plant*; they were not run as cases.

## What the account asserted, and what I found

| Claimed | Where | What I found |
|---|---|---|
| The oracle's line count reads past list and quote markers, pinned by four rows | `round-1.md`, 🟡 1's grounds; ledger R1-1 | **True for the first line, executed** (20 first-line shapes correct). **False as a general statement**: later lines are read the same way, and a lone marker there is text (🟡 1) |
| R1-1: each of five mutations alone red (the old `lstrip(" >")`, and the quote, bullet, ordered and space-after branches removed) | ledger fragment, R1-1 | Not re-run as a set. Read against the four rows: each named branch is exercised by one of them. The branches it does not name survive (⬜ 2, executed) |
| S4 gained three assertions, each red under its own mutant, green at HEAD | ledger fragment, P2-1's re-read | **Confirmed, executed.** Under m1 (closer searched from the text's start) the `instruction` and `early` shapes both read `[False, False]`; under m2 (the instruction's own `?` closes it) `instruction` does; under m3 (single quotes not followed) `single` does. HEAD reads `[False, True]` on all three, and the module fails at line 653 under m1 and m2 and at line 659 under m3 |
| ⬜ 3 answered: 583 tracked `.md` files in 0.158 s at HEAD against 0.133 s at the base, the slowest 7.6 ms | `round-1.md`, ⬜ 3's grounds | **Reproduced, executed**: 583 files, best of three, 0.169 s at HEAD and 0.145 s with `hooks/blocks.py` from `3fc0c5bd`, the slowest 8.6 ms. Same order, same conclusion |
| New units are `_behind_markers` (depth 1) | `round-1.md`, `New units` | **Confirmed by the diff.** The four rows and three assertions are the cases that pin it and the S4 readings; judged as code above · NAME NOT IN TREE |
| The ledger fragments check clean | commit `c041b5ed` | **Executed**: `bin/evidence-check --ledger` on this work item's fragment and on `1790645290`'s, exit 0 each |

Carried, not re-established: round 1's fuzz result (0 half-1 and 0 half-2
failures over 240,000 documents with the fix) and its ❓ on Windows, which CI's
`windows-latest` leg answers at the pull request. The fix diff does not touch
`hooks/`, so neither rests on anything this round changed.

## Regression tests to plant

- `tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides`:
  the two rows of 🟡 1. Executed: red with the oracle at `db4707b5`, green
  with the fix.
- The same case, for ⬜ 2 (read, not run as cases): a `+` and a `*` bullet, a
  `1)` number, and a tab after the marker, each as
  `[<marker> + NBSP, "x <? a", "b ?>", "c"]` with `{2: "inline html"}`.

## Facts for the evidence ledger

- A list marker stands only on a paragraph's opening line. On any later line
  of the paragraph a lone `*`, `+`, `1.`, `2.` or `2)` is text that
  markdown-it-py 4.2.0 keeps in the inline content, and a `>` is always a
  quote's marker. Executed: the paragraph over `[NBSP, "*", "x <? a", "b ?>"]`
  has content `'*\nx <? a\nb ?>'`. R1-1 states the count-back reads markers
  on every line, so the fix drifts its anchor and corrects its claim.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_behind_markers` reads a list marker on every line the count-back hands it, but only the paragraph's opening line can carry one; a later line of only `*`, `+`, `1.`, `2.` or `2)` is text the parser keeps, so it is skipped and every inline HTML line after it is placed one line late | `tests/commonmark_oracle.py:76` | open | executed: `[NBSP, "*", "x <? a", "b ?>", "", "text"]` gives `{4: ...}` where a renderer hides line 3, and the property's `disagreements` is `[(4, 'live', True)]`; 15 of 37 probe shapes wrong at HEAD, 0 with the fix · NAME NOT IN TREE |
| ⬜ 2 | Five branches of `_behind_markers` are pinned by no case: `+` and `*`, the `)` delimiter, the nine-digit bound, a tab before a marker, a tab after one | `tests/commonmark_oracle.py:90` | open | executed: each mutant exit 0, 78 passed; the behaviour is right at HEAD on all 20 first-line shapes · NAME NOT IN TREE |
| 🟢 | round 1's finding 1 is closed for the shape it reported — a list item whose first line holds only a Unicode space | `tests/commonmark_oracle.py:125` | confirmed | executed: `["- " + NBSP, "x <? a", "b ?>", "c"]` and 19 more first-line shapes give line 2; the four rows are green. The new unit's own defect is 🟡 1 above |
| 🟢 | round 1's finding 2 is closed — S4 pins `<?>` not closing, a closer before its opener, and a `>` inside a single-quoted value | `tests/test_the_hooks_hide_what_a_renderer_hides.py:651` | confirmed | executed: each assertion's shape reads `[False, False]` under its own mutant and `[False, True]` at HEAD; the module fails under each of m1, m2 and m3 |
| 🟢 | round 1's finding 3 is answered on grounds that reproduce | `hooks/blocks.py:233` | confirmed | executed: 583 tracked `.md` files, 0.169 s at HEAD against 0.145 s at the base, the slowest 8.6 ms |
| 🟢 | The fix pass's ledger rows check clean | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | confirmed | executed: `bin/evidence-check --ledger` exit 0 on both fragments the fix commit touched |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` at `db4707b5` | exit 0, 78 passed |
| Probe: `oracle.hidden` and the property's `disagreements` on 20 first-line marker shapes, 1 item with two blank-looking lines, 12 continuation shapes, and 4 with the HTML line last in its paragraph | at HEAD: 22 correct; 15 wrong, 3 of them red in `disagreements` |
| The paragraph's inline content, and `_starts_in_inline_html` at each line start, on the `*` and the quoted `2.` shapes | content keeps `*` and `2.`; the mark is inside HTML at line 3 alone in both |
| 🟡 1's fix and two rows applied in the clone, then the probe and the module | probe: 37 of 37 correct; module exit 0, 80 passed |
| The two new rows with the oracle at HEAD | exit 1, 2 failed, 21 passed |
| m1, m2 and m3 of `hooks/blocks.py`, one at a time, restored from kept bytes, against the S4 case; and each new shape evaluated under each mutant | each exit 1; failing line 653 (m1, m2) and 659 (m3); the matrix reads `[False, False]` only where the mutant targets the shape |
| Five mutants of `_behind_markers` (⬜ 2), one at a time, restored, against the property module | each exit 0, 78 passed · NAME NOT IN TREE |
| `walk_text` over the 583 tracked `.md` files, best of three, HEAD against `hooks/blocks.py` from `3fc0c5bd` | 0.169 s against 0.145 s; slowest file 8.6 ms against 7.4 ms |
| `bin/evidence-check --ledger` on the two fragments `c041b5ed` touched | exit 0 each |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet — no run has been made, and it is the sealer's once the rounds settle |

## Paste-ready fixes

### 🟡 1

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

Needs a fix: yes — 🟡 1 (the oracle reads a list marker on a paragraph's later lines, where a lone `*` or `2.` is text, and places inline HTML one line late)
Loses a record or crashes: no

Nothing here is a 🔴. 🟡 1 sits inside a unit round 1's fixes created, so it
is the branch's to fix. Once it is fixed or answered with grounds, nothing
this round found stays open, and what comes due is the sealer's spawn.

## Proof block

Files opened in this round, in the clone at `db4707b5` unless noted:

- `tests/commonmark_oracle.py` (55-330)
- `tests/test_the_hooks_hide_what_a_renderer_hides.py` (22-470, 630-670)
- `hooks/blocks.py` (205-275), and the same file at `3fc0c5bd` (loaded for the timing)
- `bin/test`
- the diffs `c0d9045b..c041b5ed` (all four files) and `c041b5ed..db4707b5`
- this work item's `rounds/round-1.md` and `rounds/round-1-report.md`, in the orchestrator's tree

Every probe file, the clone and the scratch directory were removed after this
report was written.
