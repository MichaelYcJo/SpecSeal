# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ddbd24b9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 1: the cmark-gfm oracle, pinned and test-only and held the way
`MARKDOWN_IT` is; one header-tuple walker in `hooks/config.py`, with
`pact_signatories` on it; the corpus enumerated by construction from the
CommonMark and GFM block kinds, every verdict cmark-gfm's and never a
hand-written expectation; round 3's `TABLE_ENDS` entries; the census comment
(⬜ 21); the docstring table rewritten to the walker's actual rules. Verified
by the property case red with `TABLE_BREAK`'s `<` arm restored and with the
indentation rule removed, `bin/mutation-check` over every arm, and the five
pact modules and the census module green. The spawn added: every file read
and write passes `encoding="utf-8"`; answer Q12, Q13 and Q17 here.

## What this phase found

**The frame holds.** Its one wrong fact is round 3's, not the frame's: a row
indented by a tab is not read by cmark-gfm 2025.10.22, it ends the table as an
indented code block (`questions.md` Q13). The walker follows the renderer.

**The corpus: 16,364 shapes, and 656 of the `Signatory` pass's 5,454 were
wrong at `2b1dcb1f`.** 213 line kinds, each at five positions (before the
header, after it, after the delimiter, between rows, after the last row) and
five indentations, plus 125 indentation combinations of the table's own lines
and six delimiter spellings, for each of three headers. The kinds were taken
section by section: CommonMark 0.29 §4.1–§4.9 and §5.1–§5.2 with each near
miss the section states, all 62 tag names of HTML condition 6 open and bare,
the interruption rules of §4.6 and §5.2 as two-line kinds, the GFM table,
task-list and autolink extensions, and the inline shapes a line can open with.
Of the 656 wrong at the base, 44 drop a row cmark-gfm renders (the autolink
family, `< ` and a URL, `<search`, an unfinished tag, a backtick line that is
not a fence) and the rest read a table cmark-gfm does not render at all,
because a list item, a block quote or an open HTML block above the header
takes the header into itself. That second family was outside round 3's 21
shapes and is the position the frame did not name; it is now refused, naming
the line that took the header.

**Equal-or-refuse is a property a walker that refuses too much also passes.**
The first mutation pass left six arms standing, every one of them an arm that
stops a refusal, and the property cannot see those. Two cases close it: above
the header the walker reads every table cmark-gfm renders, and every delimiter
spelling cmark-gfm accepts is read. They killed all six, and found two real
over-refusals with a false cause (`* * *` read as a list item; an HTML block
closed two lines up still read as open), which is why the look-back reads the
lines above the header top to bottom rather than one line.

**Mutation: 38 distinct breaks, each red at the end** — every end arm, the
restored `<` arm and the removed indentation rule (both named by the plan),
each HTML condition's boundary, every look-back rule, the gap and blank stops,
the stray-row rule, the width checks, the `Signatory` sentences.

**What the walker cannot see**, stated in its docstring: a header lazily taken
into a list item two blocks up (`- x`, a blank line, an indented paragraph,
the header). It needs the container nesting no table reader here tracks.

**Q17**: only `pact_check.py#check` and `chain_check.py#pact_notices` call
`pact_signatories`, and neither changed.

**What the next phase needs**: `gfm_table(text, header)` returns `(line,
cells)` rows, so a record reader can name a row's line; its refusals read
after a noun naming the file; `pact_signatories` turns *every row below it*
into *every signatory below it*, and a record reader can do the same for its
own noun.

**Ledger**: P8 in #735's fragment named `TABLE_BREAK`, which is gone, and was
corrected in place with a dated note. R3 and W3 in #718's fragment were
re-stamped in place with notes; W4 there, drifted at the base already, was
left as it stood. Nine released rows the pin drifted (CONTRIBUTING.md and
`run_tests.py`) were re-read into this item's fragment. The nine rows and the
four record lines naming `SELF_ANCHOR_RE` that are drifted or refused at
`805013c2` belong to the integration branch that re-stamps them, and were not
touched.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/config.py`'s `TABLE_BREAK`, `SIGNATORY_ROW`, `SIGNATORY_DELIMITER`, `HEADING_LINE` and the `Signatory` walk inside `pact_signatories` | `hooks/config.py#gfm_table` and its arms; the record lines naming the removed constants carry the marker · NAME NOT IN TREE |
