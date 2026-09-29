# 1790659274 — round 1 report (warden)

| Field | Value |
|---|---|
| Target | `fix/673-the-walk-leaves-every-inline-html-construct-uncertain` at `7a6f2d3e`, against base `3fc0c5bd` (`git diff 3fc0c5bd...7a6f2d3e`) |
| Earlier rounds | none |
| Where it ran | a `git clone --no-local` of the orchestrator's tree at `7a6f2d3e`, under `<scratchpad>/1790659274/round-1/` |

## How the findings relate

- **The walk is right.** Over 240,000 generated documents that put every
  inline HTML opener and closer at every break, the new walk claims no line
  the oracle classes otherwise. None of the three readers leaves both
  readings. The base walk fails about 3,700 documents in every 60,000 of the
  same corpus. This holds once the oracle's own defect below is fixed.
- **The oracle has one defect, and the fuzz found nothing else (🟡 1).** In a
  list item whose first line holds only a Unicode space, it counts every
  inline HTML line one line too early. The defect predates this branch, but
  this branch widened it from the comment to all six kinds. It errs loudly
  (a false red), never silently.
- **The walk is right in three places no case pins (🟡 2).** A mutant for each
  one brings back #673's exact defect, a `Mode` row neither reading shows, and
  the suite stays green.
- **A cost the old predicate did not have (⬜ 3).** Asking every tag opener
  scales with openers times line length.

## 🟡 1 · The oracle counts inline HTML lines one line early behind a list marker

`tests/commonmark_oracle.py:96`, in `_inline_html_lines`. The parser strips
the paragraph's inline source with Python's `str.strip`, which also drops a
first line holding only a no-break space, U+2028, NEL, a form feed or another
Unicode space. The oracle counts those dropped lines back by asking
`lines[first].lstrip(" >").strip()`. That skips a block quote's `>` but not a
list marker, so on `- ` followed by a Unicode space the line reads as `-` and
is not skipped. Every offset after that lands one line early.

Executed at HEAD:

- `oracle.hidden(["- " + NBSP, "x <? a", "b ?>", "c"])` gives `{1: "inline html"}`.
  A renderer hides line 2 (`b ?>` begins inside the processing instruction)
  and shows line 1, where it opens.
- The same with `1. ` in front, or `> - `, or a comment
  (`x &lt;!-- a` / `b -->`), gives `{1: ...}` too, so the comment has had this
  since F. `-` with a no-break space and no space after it is not a list
  marker, and it gives `{2: ...}` correctly.
- In the fuzz, all 12 of the new walk's half-2 disagreements over 240,000
  documents are this shape (`- ` followed by one of the eight breaks, which
  `str.strip` also takes). With the fix below applied in the clone they drop
  to 0, and the property module stays green (74 passed).

**Why it matters.** The oracle is what the walk is judged against, and here it
names the opener's line hidden and the closer's line shown. Today that is a
false red: the walk claims the opener's line live, and the property fails on
a document the walk reads right. It is not agreement by construction, because
the line the oracle wrongly shows is one the walk calls uncertain anyway.
The cost is that the first `ALPHABET` line of the form `- ` plus a Unicode
space turns the property red, and the reading that fixes it is a change to
the walk toward a wrong oracle. The paste-ready fix skips container markers
the way CommonMark 5.1 and 5.2 define them, without a new import, so
`test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys` still
holds (it asserts the imports are `{"markdown_it"}` alone).

## 🟡 2 · Three readings of `leaves_html_open` the spec states are pinned by no case

`hooks/blocks.py:231` and `:210`. The code is right in all three places
(executed: `config_rows` returns `[]` on each shape at HEAD). The spec states
each one in §*The class, enumerated*, and a mutant of each passes
`tests/test_the_hooks_hide_what_a_renderer_hides.py` and the inline, comment
and break cases of `tests/test_the_mode_question_is_asked_once.py`
(exit 0, 136 passed):

| Mutant | What the spec says | What the mutant reads, executed |
|---|---|---|
| m1: the closer is searched from the line's start (`text.find(closer)`) | H3 and H2: "the first `?>` after the opener" | `x ?> <? a` + LS + fence run + config table + `\n?>`: `[("Mode", "shared")]` |
| m2: a processing instruction's own `?` closes it | H3: "`<?>` does not close" | `x <?>` + LS + the same: `[("Mode", "shared")]` |
| m3: a `>` inside a single-quoted value ends the tag | H5: "the value's own quote, then the tag's `>`" | `x <span title='b>c` + LS + the same: `[("Mode", "shared")]` |

The S4 case pins the quoted `>` for `"` only, so m3 survives. No case holds a
`<?>`, or a closer standing before its opener on the same line. A fourth
mutant, the closing tag's `/?` dropped, fails 2 cases and is pinned.

**Why it matters.** Each mutant is one plausible edit away from the code, and
each one reads the row #673 exists to stop reading. The account claims 13
mutations of the new units, all red, and that is true of the 13 it ran
(`phases/phase-2.md`). These three are outside that list. The paste-ready fix
adds three assertions to the S4 case. Each is green at HEAD, red under its
mutant (executed, `walk_text(...).uncertain[:2]` is `[False, False]` under the
mutant and `[False, True]` at HEAD), and the oracle hides each piece.

## ⬜ 3 · Asking every tag opener costs openers times line length

`hooks/blocks.py:233`. `TAG_END.match` runs from each `<` and letter to the
first `>` outside quotes. When many openers share one far `>`, each scan runs
to it. Executed: a line of 8,000 openers (`a <b ` repeated, one `>` at the end,
40,001 characters) takes 3.1 s in `leaves_html_open`, 0.70 s at 20,001 and
0.17 s at 10,001. `walk_text` then asks `leaves_html_open` again on the prefix
before every piece of a line, which multiplies the cost by the pieces. The
`leaves_open` it sits beside is one `rfind`.

Such a line is not in any tracked file, and markdown lines are short, so this
is not a fix this round needs. If it is taken up, one pass from the right can
compute, for every index, where a tag starting there unquoted ends: a `>`
ends at itself, a quote ends where the text after its closing quote ends, and
anything else ends where the next index does. Each opener then reads one
entry. `leaves_html_open(line)` is also computed twice on the `walk` line that
enters the pending state (`hooks/blocks.py:351-352`).

## What the account asserted, and what I found

| Claimed | Where | What I found |
|---|---|---|
| Asking every opener, not a left-to-right skip, is needed, and it errs only toward uncertain | `overview.md`, first divergence row | **Confirmed, executed.** Read against markdown-it-py 4.2.0's `common/html_re.py` in the clone's `.venv`: each closer the walk looks for is the parser's (the first `]]>`, the first `?>` after `<?`, the first `>` after `<!` and a letter, the first `>` outside a quoted value, where a quote can only stand as a value's delimiter in a tag the parser forms). The fuzz found no claimed line inside inline HTML |
| A pending line is asked whole, not only after its `-->` | `overview.md`, second row | **Confirmed.** `walk` reads `sticky or leaves_html_open(line)` before `-->` is looked for (`hooks/blocks.py:344-346`); the S5 `fake` assertion covers it |
| Sticky only makes a line uncertain, and uncertain falls back to the base | spec §*The reading after this work* | **Confirmed, read and executed.** By induction over lines, the new walk's pending state is a superset of the base's, and `kinds` does not change, so every line the new walk claims is one the base walk claimed with the same kind. An uncertain line takes the fence-only reading in `hooks/config.py#hidden_lines` (through `Walk.hidden(base)`), is read as live in `hooks/routing.py`, and is never quoted in `.github/scripts/rider_check.py#quoted_lines`. `seal.py#table_span` reads through `unfenced`. The fuzz found 0 half-1 failures for all three readers |
| Two marks, letters then Unicode spaces, find every piece | `phases/phase-1.md` | **Confirmed, with one over-report that costs nothing.** Against `html_re.py`, letters stand everywhere inside the six kinds but between a closing tag's name and its `>`, and the spaces stand there because `\s` takes U+2002 and U+2003. Letters can also create a tag that is not there: on `x <a` + LS + `="b">` the parser forms no `html_inline`, and the oracle says the piece is hidden (executed). The walk calls that piece uncertain anyway, because the text before it holds `<a` with no `>`. Any tag a mark creates needs such an unclosed opener before it, so this over-report cannot fail a case the walk reads right |
| Lines are read at the top level and pieces at any depth | `tests/commonmark_oracle.py` docstrings | **Confirmed.** A line that begins inside HTML nested in an image description comes after a line that leaves that HTML open, which `walk` holds pending. The fuzz alphabet included `![x` and `](u)` |
| With the base walk, 49 of the new cases fail | `phases/phase-2.md` | **Reproduced**: `hooks/blocks.py` from `3fc0c5bd` over the new cases and the property halves, exit 1, 49 failed, 2 passed |
| The rider case's region half is the old one, byte for byte | `phases/phase-3.md` | **Confirmed**: `git show 8b1492aa^:tests/test_a_rider_reaches_its_file.py`, lines 601-603, match the restored lines |
| The ledger fragment checks clean | `phases/phase-2.md` | **Executed**: `bin/evidence-check --ledger` on this work item's fragment, exit 0 |
| Q1: link and image attribute text is not "hidden" | `questions.md`, `overview.md` §*Not done* | A person's question, not re-decided here. Neither 🟡 depends on it |

## Regression tests to plant

- `tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides`:
  the list-marker row of 🟡 1. Red at HEAD (`{1: "inline html"}`), green with
  the oracle fix (executed in the clone).
- `tests/test_the_hooks_hide_what_a_renderer_hides.py#test_a_piece_inside_other_inline_html_its_line_left_open_is_unsure`:
  the three assertions of 🟡 2, each red under its mutant.

## Facts for the evidence ledger

- `hooks/blocks.py#leaves_html_open` asks for the same closer as markdown-it-py
  4.2.0's `html_re.py` for each of the five kinds it reads. Executed: over 4
  seeds of 60,000 generated documents built from those openers and closers at
  every break, the walk claims no line the oracle, once fixed by 🟡 1, classes
  otherwise.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The oracle counts inline HTML lines one line too early in a list item whose first line holds only a Unicode space, because its count of stripped lines skips a `>` and not a list marker | `tests/commonmark_oracle.py:96` | open | executed: `["- " + NBSP, "x <? a", "b ?>", "c"]` gives `{1: ...}` where a renderer hides line 2; all 12 fuzz disagreements are this shape, and 0 remain with the fix |
| 🟡 2 | Three readings the spec states are pinned by no case: the closer after the opener, `<?>` not closing, and a `>` inside a single-quoted value | `hooks/blocks.py:231` | open | executed: mutants m1, m2 and m3 each pass both modules (exit 0) and each reads `[("Mode", "shared")]` on its shape; HEAD reads `[]` |
| ⬜ 3 | Asking every tag opener scans to the tag's end once per opener, and `walk_text` asks again for every piece | `hooks/blocks.py:233` | open | executed: 0.17 s, 0.70 s and 3.1 s at 10,001, 20,001 and 40,001 characters |
| 🟢 | The widening only adds uncertainty, and no claimed line is inside inline HTML | `hooks/blocks.py:213` | confirmed | read: pending is a superset of the base's per line; executed: 0 half-2 and 0 half-1 failures over 240,000 documents with 🟡 1's fix |
| 🟢 | Every opener asked, where the spec said left to right | `hooks/blocks.py:213` | confirmed | read against `html_re.py`, and executed by the fuzz |
| 🟢 | The rider case's region half is restored byte for byte | `tests/test_a_rider_reaches_its_file.py#test_a_break_commonmark_does_not_honour_quotes_no_rider` | confirmed | read: `8b1492aa^` lines 601-603 |
| 🟢 | 49 new cases fail with the base walk | `tests/test_the_hooks_hide_what_a_renderer_hides.py` | confirmed | executed: exit 1, 49 failed, 2 passed |
| ❓ | The eight breaks on Windows | `hooks/blocks.py` | ❓ out of verified scope | not run on Windows; CI's `windows-latest` leg at the pull request answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q -p no:xdist` at HEAD | exit 0, 74 passed |
| Fuzz probe: 4 seeds of 60,000 documents (seed 1: 5,000), one to six lines of openers, closers, code spans, backslashes, fence runs, table rows, list and quote markers and links, joined by spaces and all eight breaks; half 2 against the base walk and the new walk, half 1 for the config, routing and rider readers | new walk: 12 half-2 documents, all 🟡 1's shape; 0 half-1 failures. Base walk: 3,642 to 3,766 half-2 documents per 60,000 |
| The same four seeds with 🟡 1's oracle fix applied in the clone, then restored | new walk 0 half-2 and 0 half-1; property module exit 0, 74 passed |
| Mutants m1 to m4 of `hooks/blocks.py`, one at a time, restored from kept bytes, against the property module and the mode module (`-k "renderer or inline or comment or break"`) | m1, m2 and m3 exit 0, 136 passed; m4 exit 1, 2 failed |
| `config_rows` on each mutant's shape, under HEAD and under m1, m2 and m3 | HEAD `[]` on all three; each mutant `[("Mode", "shared")]` on its own shape (m1 on two) |
| 🟡 2's three assertions under HEAD and each mutant | `[False, True]` at HEAD; `[False, False]` under the mutant each one targets; the oracle hides each piece |
| `hooks/blocks.py` from `3fc0c5bd` over the new cases and the property halves, restored with `git checkout` | exit 1, 49 failed, 2 passed |
| `bin/evidence-check --ledger` on this work item's ledger fragment | exit 0 |
| `leaves_html_open` and `walk_text` timing on long lines | 8,000 tag openers in 40,001 characters: 3.1 s; `walk_text` over 2,000 pieces: 0.55 s |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet — no run has been made, and it is the sealer's once the rounds settle |

## Paste-ready fixes

### 🟡 1

```python
# tests/commonmark_oracle.py -- a new helper directly above `_inline_html_lines`
def _behind_markers(line):
    """Where LINE's own text starts behind its containers' markers: a block
    quote's `>`, a bullet, an ordered number (CommonMark 5.1, 5.2), each with
    the spaces and tabs before it. A bullet or a number is a marker only
    where a space, a tab or the line's end follows it."""
    at = 0
    while True:
        rest = line[at:]
        text = rest.lstrip(" \t")
        skip = len(rest) - len(text)
        if text.startswith(">"):
            at += skip + 1
            continue
        digits = len(text) - len(text.lstrip("0123456789"))
        if text[:1] in ("-", "+", "*"):
            marker = 1
        elif 0 < digits <= 9 and text[digits : digits + 1] in (".", ")"):
            marker = digits + 1
        else:
            return at
        if text[marker : marker + 1] not in ("", " ", "\t"):
            return at
        at += skip + marker


# tests/commonmark_oracle.py#_inline_html_lines -- replaces the two-line loop
    while (
        first < inline.map[1] - 1
        and not lines[first][_behind_markers(lines[first]) :].strip()
    ):
        first += 1


# tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides
# -- a row after the "between attributes" row
        # a list item whose first line holds only a Unicode space, which the
        # parser's strip drops: its marker is not text, so the lines are
        # counted from the next one
        (["- " + NBSP, "x <? a", "b ?>", "c"], {2: "inline html"}),
# -- and its id, after "between attributes"
        "behind a list marker",
```

### 🟡 2

```python
# tests/test_the_hooks_hide_what_a_renderer_hides.py#test_a_piece_inside_other_inline_html_its_line_left_open_is_unsure
# -- after the `quoted` assertion
    # `<?>` does not close a processing instruction: the `?` is the opener's
    instruction = blocks.walk_text(f"a <?>{ls}| r |\n?>\n\nd\n")
    assert instruction.uncertain[:2] == [False, True], instruction.uncertain
    # a closer before its opener closes nothing
    early = blocks.walk_text(f"a ?> <? b{ls}| r |\n?>\n\nd\n")
    assert early.uncertain[:2] == [False, True], early.uncertain
    # a `>` inside a single-quoted value does not end the tag either
    single = blocks.walk_text(f"a <span title='b>c{ls}d'>\n\ne\n")
    assert single.uncertain[:2] == [False, True], single.uncertain
```

Needs a fix: yes — 🟡 1 (the oracle's line count behind a list marker) and 🟡 2 (three readings of `leaves_html_open` no case pins)
Loses a record or crashes: no

Nothing here is a 🔴. Once 🟡 1 and 🟡 2 are fixed or answered with grounds,
nothing this round found stays open, and what comes due is the sealer's spawn.

## Proof block

Files opened in this round, at `7a6f2d3e` in the clone unless noted:

- `hooks/blocks.py` (lines 150-440), `hooks/config.py` (180-240)
- `tests/commonmark_oracle.py` (55-230), `tests/test_the_hooks_hide_what_a_renderer_hides.py` (22-62, 184-610)
- `.github/scripts/rider_check.py` (215-245), `skills/implement/scripts/seal.py` (1467-1500), `bin/test`
- markdown-it-py 4.2.0 in the clone's `.venv`: `common/html_re.py`, `rules_inline/html_inline.py`
- this work item's `spec.md`, `overview.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`, `changelog.md`, and its ledger fragment
- the whole diff `3fc0c5bd...7a6f2d3e` for `hooks/`, `tests/`, `templates/`, `seal/releases/`, `seal/ledger/1790645290-…` and work item 1790645290's records
- `tests/test_a_rider_reaches_its_file.py` at `8b1492aa^` (lines 601-603)

Every probe file, output and the clone were removed after this report was written.
