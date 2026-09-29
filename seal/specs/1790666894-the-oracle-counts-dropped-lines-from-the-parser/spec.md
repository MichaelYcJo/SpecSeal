# Feature Specification: the oracle counts a paragraph's dropped lines from the parser (#677)

<!-- seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #677 (the ticket; it ranks below `docs/` and above the code) | Two boxes: the oracle takes the dropped-line count from the parser and the hand-written helper is gone; the report's rows are planted, each seen red |
| `seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/rounds/round-3-report.md` §*🟡 1*, §*⬜ 2*, §*Paste-ready fixes* | The executed shapes and the drafted fix this frame starts from. Its numbers (18 of 18, 91 passed, 16 red with the count forced to 0, 1 red with `lheading` unwrapped) are the reviewer's, executed in a clone this frame did not open. Phase 1 runs them again |
| `tests/commonmark_oracle.py`, module docstring: "A parser written by somebody else, from the specification, is the whole point, so no rule of this repository's is written here" and "Nothing about what is inline HTML is decided here; only where the tokens the parser found lie" | The principle the fix restores. The hand count is a rule of this repository's about containers, written into the oracle. The parser-side count reads the text the parser itself joined |
| `skills/agent-contract/SKILL.md` §12, §15 | §12: the class is every container and line shape in front of a paragraph whose top lines the parser's strip drops, enumerated below, not the report's 18 probes. §15: every new row is seen red before it is planted, and §*How each row is seen red* says against what |
| `CLAUDE.md` §*Repo rule — commit early* ("A row whose anchor a change removes is REMOVED, not re-pointed") and `docs/the-evidence-ledger.md` §*An anchor degrades to DRIFTED* | R1-1 in H's fragment goes. §*The ledger* below says why REMOVED and not narrowed |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* ("an edit drifts the row, which is re-read against that edit and re-stamped there with a dated note, its claim first corrected in place") | The new claim is a row in `seal/ledger/1790666894-the-oracle-counts-dropped-lines-from-the-parser.md`. H's P1-1 and F's P1-2 are corrected or re-read where they live |
| `skills/evidence-check/SKILL.md` §*NOT-IN-TREE* ("a record of a work item that has not shipped … names a compound backticked identifier that nothing carries outside `seal/specs/`") | H has not shipped: its ledger fragment is still in the tree. Deleting the helper makes every backticked mention of it in H's records refuse. §*H's records* below |

**Which rung of the ladder.** `skills/implement/SKILL.md` §3's top rung,
because the oracle's answer is a verdict a person reads and acts on. A false
red in the property names the walk as wrong, and the edit it invites is a
change to `hooks/blocks.py` toward a wrong oracle. That is round 3's own
*Why it matters*. The work is test code only: nothing under `hooks/` or
`.github/workflows/` moves, so `CONTRIBUTING.md` §*What a change to a gate
must carry* does not apply.

## What goes wrong today

markdown-it-py's `paragraph` and `lheading` block rules build an inline
token's source as `state.getLines(start, end, state.blkIndent, False).strip()`
(read in markdown-it-py 4.2.0, `markdown_it/rules_block/paragraph.py` and
`lheading.py`). Python's `str.strip` also drops a line holding only a
character such as a no-break space, which CommonMark reads as paragraph text.
The inline token's `map` still starts at the first source line, so an offset
in the stripped source is off by the number of whole lines the strip took.

The oracle counts those lines back itself.
`tests/commonmark_oracle.py#_inline_html_lines` walks from `inline.map[0]`,
skipping a line whose text behind its container markers is blank, and
`_behind_markers` decides where the markers end. · NAME NOT IN TREE
Three rounds found a marker shape it read wrong:

| Round | What the helper misread |
|---|---|
| 1 | a list marker on an opening line that holds only a Unicode space |
| 2 | a `*` or `2.` on a later line, which is text |
| 3 | a `>` four columns in, or behind a tab, on a later line, which is lazy-continuation text; while inside `10. >` a `>` four columns in is a real marker |

Round 3's last row is why a column count cannot fix it either: telling the
two `>` apart needs the list item's content indent, which is the block
parser's container stack. The helper would have to rebuild it.

## The fix, and why it closes the class

The parser has already consumed every container marker by the time it joins
the lines. So the count is taken from the text the parser joined:

- A wrapper around the parser's own `paragraph` and `lheading` rules, the way
  `_recording_html_inline` wraps `html_inline`. It calls the rule unchanged.
  For each `inline` token the rule pushed, it takes the same
  `state.getLines(*token.map, state.blkIndent, False)` and writes the number
  of line ends inside what `lstrip` removes from its top into the token's
  `meta`. The wrapper is named `_recording_lines`, the report's name.
- `parser` installs it with `md.block.ruler.at` for both rules.
- `_inline_html_lines` starts at `inline.map[0]` plus that number, and reads
  no source line. Its `lines` parameter goes, because nothing reads it.
- `_behind_markers` is deleted. · NAME NOT IN TREE

**Why this is the whole class and not one more instance.** The count never
reads a marker. Whatever the parser took as a container prefix is absent from
the joined text, and whatever it kept as text is present. The number of line
ends in the stripped prefix is the number of whole lines dropped, for any
character `str.strip` removes, because none of those characters is a `\n`.
What remains to show is that the parser's joined text is the text the rule
stripped, which holds because the wrapper calls `getLines` with the same
arguments right after the rule returns, before any container restores its
line marks.

**Why these two rules and no others.** In markdown-it-py 4.2.0 six places push
an `inline` token (read: `grep 'push("inline"' markdown_it/rules_block/`):

| Rule | Lines in its source | Needs the count |
|---|---|---|
| `paragraph` | one or more | yes |
| `lheading` | one or more, the underline excluded | yes |
| `heading` (ATX) | one | no: a strip cannot drop a whole line from one line |
| `table`, twice (header and body cells) | one per cell | no, for the same reason |
| `blockquote`'s alert title | a fixed word | no: alerts are off unless `options["alerts"]` is set, and the `commonmark` preset does not set it |

`Ruler.at` resets a rule's `alt` list to `[]` (read: `markdown_it/ruler.py`,
`Ruler.at`). Both rules already have `[]` in the block parser's rule table, so
wrapping them does not change which rule may interrupt which.

## Scope

**In.**

- `tests/commonmark_oracle.py`: the wrapper, two lines in `parser`, the
  deleted helper, `_inline_html_lines`' start and signature, its docstring's
  last paragraph, and one sentence in the module docstring's *Where the inline
  HTML is, the parser says* paragraph saying the parser also says where a
  paragraph's text starts.
- `tests/test_the_hooks_hide_what_a_renderer_hides.py`: one new
  parametrized case holding the class's rows (S1 to S3), one case over every
  character the strip drops (S4), and one `FOUND` document (S5). The case the
  existing marker rows sit in keeps them.
- H's records, H's and F's ledger fragments, this work item's fragment and
  its `changelog.md`, as §*The ledger* and §*H's records* say.

**Out, one line each.**

- `hooks/blocks.py` and every reader: the defect is in the oracle and shows
  only as a false red. No reader's answer moves.
- `_starts_in_inline_html`, the piece path: it puts a mark in the text and
  looks for it in a token, so it needs no offset and never used the count.
- The 13 marker rows already in `test_the_oracle_names_each_kind_it_hides`:
  they stay where they are and keep pinning the count. Moving them drifts two
  ledger rows for no change in what is checked.
- `ALPHABET`: not widened. H measured six lines pushing
  `test_the_walk_is_exact_somewhere` under its floor, and `FOUND` is where a
  shape goes.
- The markdown-it-py pin (`4.2.0` in `.github/scripts/run_tests.py`):
  unchanged. No new dependency.
- A dropped line that ends in a break `str.splitlines` makes and CommonMark
  does not (NEL, LS, PS and five more): that is `hidden_text`'s reader-split
  mapping, F's work, and S4 leaves those characters out on purpose.
- Where markdown-it-py itself departs from CommonMark on a shape below: the
  oracle follows its parser. A row pins the parser's answer by name, as the
  `past the first closer` row already does, and the walk is not changed
  toward it (Q1).
- `docs/`: no policy document describes the oracle's count. `CONTRIBUTING.md`
  §*Running the checks* names the parser and its pin, and neither changes.

## User scenarios & acceptance *(mandatory)*

The notation is the existing case's. `NBSP` is U+00A0. `"x <? a"` opens a
processing instruction and `"b ?>"` closes it, so the line holding `b ?>`
begins inside inline HTML and is the one a renderer hides. Expected answers are
CommonMark's, read from the specification by this frame and not run (Q1).

**S1. The report's shapes: a `>` on a later line that is text.** Red with the
oracle at `cd56113c`, which the report executed for the first three and for
the fourth and fifth in its probe.

| Row | Lines | Hidden |
|---|---|---|
| S1a four columns in | `[NBSP, "    >", "x <? a", "b ?>"]` | `{3}` |
| S1b behind a tab | `[NBSP, "\t>", "x <? a", "b ?>"]` | `{3}` |
| S1c four columns into an item | `["- " + NBSP, "      >", "  x <? a", "  b ?>"]` | `{3}` |
| S1d four columns into a quote | `["> " + NBSP, ">     >", "> x <? a", "> b ?>"]` | `{3}` |
| S1e two of them | `[NBSP, "    > >", "x <? a", "b ?>"]` | `{3}` |

The report planted S1a to S1c and left S1d and S1e as probes. They go in too:
they are the same false red from the other two containers.

**S2. Setext headings are joined and stripped as a paragraph is.** The rows
that pin the `lheading` wrapper.

| Row | Lines | Hidden |
|---|---|---|
| S2a level 1 | `[NBSP, "x <? a", "b ?>", "==="]` | `{2}` |
| S2b level 2 | `[NBSP, "x <? a", "b ?>", "---"]` | `{2}` |
| S2c inside a quote | `["> " + NBSP, "> x <? a", "> b ?>", "> ==="]` | `{2}` |

**S3. The class, enumerated.** Every container and line shape the hand count
had to know about, each with at least one line the strip drops.

| Row | Lines | Hidden |
|---|---|---|
| S3a a quote one column in | `[" > " + NBSP, " > x <? a", " > b ?>"]` | `{2}` |
| S3b a quote three columns in | `["   > " + NBSP, "   > x <? a", "   > b ?>"]` | `{2}` |
| S3c a quote with no space after `>` | `[">" + NBSP, ">x <? a", ">b ?>"]` | `{2}` |
| S3d a later quote marker three columns in | `["> " + NBSP, "   > x <? a", "   > b ?>"]` | `{2}` |
| S3e a quote's lazy line drops the `>` | `["> " + NBSP, "x <? a", "b ?>"]` | `{2}` |
| S3f an item continued by indentation | `["- " + NBSP, "  x <? a", "  b ?>"]` | `{2}` |
| S3g four spaces after a bullet | `["-    " + NBSP, "x <? a", "b ?>"]` | `{2}` |
| S3h nine digits are a marker | `["123456789. " + NBSP, "x <? a", "b ?>", "c"]` | `{2}` |
| S3i an item that opens on a blank line | `["-", "  " + NBSP, "  x <? a", "  b ?>"]` | `{3}` |
| S3j a quote inside an item | `["- > " + NBSP, "  > x <? a", "  > b ?>"]` | `{2}` |
| S3k an item inside an item | `["- - " + NBSP, "    x <? a", "    b ?>"]` | `{2}` |
| S3l a quote inside a quote | `["> > " + NBSP, "> > x <? a", "> > b ?>"]` | `{2}` |
| S3m a `>` four columns in that IS a marker | `["10. > " + NBSP, "    > x <? a", "    > b ?>"]` | `{2}` |
| S3n two dropped lines | `[NBSP, NBSP, "x <? a", "b ?>"]` | `{3}` |
| S3o spaces, a tab and no-break spaces mixed | `[" " + NBSP + "\t" + NBSP, "x <? a", "b ?>"]` | `{2}` |
| S3p a reference definition before the paragraph | `["[a]: /u", NBSP, "x <? a", "b ?>"]` | `{3}` |

S3m is round 3's counterexample to a column count, and the row that makes a
return to one go red. S3i and S3p are the two shapes whose paragraph does not
start on its container's first line, so they pin that the count is added to
the paragraph's own `map[0]`.

**S4. Every character the strip drops.** Computed by the case, not listed:
every code point `c` for which `c.isspace()` holds, `("a" + c + "b").splitlines()`
has one piece, and `c` is neither a space nor a tab. On Python 3.14 that is
U+001F, U+00A0, U+1680, U+2000 to U+200A, U+202F, U+205F and U+3000
(executed by this frame, a standard-library one-liner and no part of the
suite). For each, `[c, "x <? a", "b ?>"]` and `["- " + c, "x <? a", "b ?>"]`
hide `{2}`. U+001F is the one CommonMark does not call whitespace at all, so
it is the case where the count and CommonMark's own reading differ most.
Computing the set is what keeps a new Unicode version from leaving a
character out.

**S5. The false red the report executed, kept in the corpus.**
`[NBSP, "    >", "x <? a", "b ?>", "", "text"]` goes in `FOUND`. At `cd56113c`
the report executed `disagreements` on it as `[(4, 'live', True)]`, so
`test_where_the_walk_claims_to_be_exact_it_is` fails there. After the fix it
agrees.

**S6. The helper is gone and the oracle is still independent.**
`tests/commonmark_oracle.py` defines no marker-reading function, and
`test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys` stays
green: the two new imports are from `markdown_it`.

**S7. Nothing else moves.** `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py`
exits 0. The existing marker rows stay green, and so do both halves of the
property.

### How each row is seen red (§15)

| Rows | Seen red against |
|---|---|
| S1, S5 | the oracle at `cd56113c` (`git show cd56113c:tests/commonmark_oracle.py`) |
| S2 | the fix with `lheading` left unwrapped. Round 3 executed S2a green at the old helper, so this row CANNOT be red against it. The ticket's second box says each row is seen red against the hand-written helper, and for S2 that is not possible; the unwrapped rule is the sentence S2 pins |
| S3, S4 | the fix with the dropped-line count forced to 0. Every one of them has at least one dropped line, so each goes red. Which of them are also red at `cd56113c` is recorded, not required (Q2) |

## The ledger

- **H's R1-1 is REMOVED**, in
  `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md`.
  Its claim is the helper's reading of markers: "a block quote's `>` on every
  line, and on the paragraph's opening line alone a bullet or an ordered
  number". That claim goes with the helper. Its two other anchors,
  `_inline_html_lines` and `test_the_oracle_names_each_kind_it_hides`, are
  already P1-1's. Narrowing the row to them would keep a false sentence on
  true code. H itself narrowed F's rows instead, citing *"a row that keeps a
  live anchor beside the dead one loses only the dead one"*, but those rows'
  claims still held after the rename; this one's does not.
- **H's P1-1** is corrected in place. Its first `Corrected` note ends "The
  count now skips container markers by CommonMark 5.1 and 5.2
  (`_behind_markers`, R1-1)", which becomes false. A new `Corrected <date>` · NAME NOT IN TREE
  note says the count now comes from the parser's paragraph and setext rules
  and names this work item's row. Its `_inline_html_lines` and
  `test_the_oracle_names_each_kind_it_hides` anchors are re-stamped.
- **F's P1-2**, in
  `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md`,
  cites `tests/commonmark_oracle.py#parser`, which gains two lines. Its
  claim ("locating inline HTML by wrapping the parser's own `html_inline`
  rule") still holds, so it takes a `Re-read <date>` note and a re-stamp.
- **A new row** in `seal/ledger/1790666894-the-oracle-counts-dropped-lines-from-the-parser.md`:
  the oracle takes the number of whole lines the parser's strip dropped from
  its own `paragraph` and `lheading` rules, which join each line from behind
  the container markers the parser consumed. Anchored on `_recording_lines`,
  `parser`, `_inline_html_lines`, the new cases and `FOUND`.
- Whatever else `bin/evidence-check --reverify` names as drifted is re-read
  against this diff. The three rows above are what this frame found by grep
  (read); the checker's list is the measurement.

## H's records

H (`1790659274`) has not shipped, so the records arm reads its records.
Today 38 lines under its directory name the helper without the
` · NAME NOT IN TREE` marker, in six files, all under `rounds/` (grep, read).
Only a backticked mention outside a closed fence is read by the arm, so the
set that needs the marker is a subset of the 38. The builder marks exactly the
lines the arm names after the helper is deleted, in the same commit, as H did
for F's `_comment_lines`. The marker is appended to the line and nothing else · NAME NOT IN TREE
on it changes. This work item's own records carry it already where they name
the helper.

## Data & interfaces

- `tests/commonmark_oracle.py`: a module-level `_recording_lines(rule)`
  returning a wrapper with the block rule signature
  `(state, start, end, silent)`; `parser()` gains
  `md.block.ruler.at("paragraph", …)` and `md.block.ruler.at("lheading", …)`;
  `_inline_html_lines(inline)` loses `lines`, and `_hidden_commonmark`'s call
  loses the argument. An inline token from either rule carries
  `meta["dropped"]`; one from any other rule carries no such key and is read
  as 0.
- `tests/test_the_hooks_hide_what_a_renderer_hides.py`: two new cases and one
  `FOUND` entry. The builder names the cases.
- `seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/changelog.md`:
  one entry under `### Fixed`. Nothing a plugin user runs changes, so it says
  the suite's CommonMark oracle stops reporting a false disagreement with the
  hooks' walk after a line of only a Unicode space followed by an indented
  `>`, and that it now takes the count from the parser.

## Open questions → questions.md

None needs a person. Q1 to Q3 are measurements, and the phases that meet them
run them.

Framed 2026-09-29 by framer, before the build.
