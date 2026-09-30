# Feature Specification: the walk leaves every inline HTML construct uncertain (#673)

<!-- seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #673 (the ticket; it ranks below `docs/` and above the code) | Three boxes: a piece that starts inside any inline HTML construct is uncertain, every shape seen red first; the oracle asks every inline HTML token; the rider case's region half is restored beside the new one |
| `seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/rounds/round-3-report.md` §*Round 2's 🟡 1 is closed for the comment*, §*And the oracle cannot see it*, §*The re-pinned rider case*, §*Paste-ready fixes* | The executed shapes and the drafted fixes this frame starts from. Work item F's `spec.md` §*The acceptance property* is still the property: for every line L, `new(L)` is `base(L)` or `renderer(L)` (half 1), and every line the walk claims is classed as the oracle classes it (half 2) |
| F's `spec.md` §*What is not modelled*: "These are the **minimum** … It may never narrow what it calls uncertain without that" | Widening what the walk calls uncertain needs no oracle, and costs only claimed lines. Narrowing it needs the property green on documents that hold the context |
| F's `spec.md` §*The oracle* ("a fenced block, an indented code block, an HTML block, or an inline HTML comment. It judges nothing else") | The definition of *renderer hides* this work widens, and by exactly one step: *an inline HTML comment* becomes *inline raw HTML of any kind*. The grounds are in §*Why the line is drawn at raw HTML*. Nothing else in that definition moves (Q1) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `hooks/blocks.py` is under `hooks/`. The change carries a test seen red, a failure direction, a prompt budget and a platform note (§*Failure direction and prompt budget*) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | §12: the class is enumerated from CommonMark §6.6 and the parser's own regular expressions, not from the report's three openers. §14: `templates/config.md` states the unsure contexts to a person, so its sentence widens and is pinned in the same commit. §15: every case that claims a defect is seen red against `3fc0c5bd` |
| `docs/the-evidence-ledger.md` §*An anchor degrades to DRIFTED* and the retire guard's rule ("a row that keeps a live anchor beside the dead one loses only the dead one") | Two oracle helpers are renamed (§*Data & interfaces*). The F rows that cite them lose that one anchor and keep the rest; the renamed units' claims are new rows in this work item's fragment |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | New rows go to `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md`. F's rows P1-2, P2-1 and R1-1 in `seal/ledger/1790645290-….md` are corrected in place, because keeping an existing claim true is not appending |

## What goes wrong today

`hooks/blocks.py#walk_text` answers each `str.splitlines` piece by the GFM
line it starts in. Round 2 of F made one exception: a piece is uncertain where
the text before it on its GFM line leaves an inline comment open
(`leaves_open`, which looks for `<!--` alone). The comment is one kind of
inline raw HTML among six, and the other five hide what they hold too.

The executed shape, from the round 3 report, with `␤` standing for U+2028
(the report ran it with all eight breaks `str.splitlines` honours and
CommonMark does not):

```
x <![CDATA[ a␤```␤| Item | Value |␤|---|---|␤| Mode | shared |
]]>
```

- A renderer reads one paragraph whose CDATA section holds the table, so it
  shows no row.
- The config reader's base (`fence_only` over the reader's split) reads the
  "```" piece as a fence opener and hides every row below it.
- The walk calls the piece live and certain, so `config_rows` returns
  `[("Mode", "shared")]`. That is a third reading, which half 1 forbids.

The oracle did not see it. `tests/commonmark_oracle.py#_comment_lines` and · NAME NOT IN TREE
`#_starts_in_a_comment` keep only `html_inline` tokens whose content starts
with `<!--`. On the rest of the class the oracle answers "shown", which is the
walk's own answer, so it agrees with the walk by construction. That is the
failure F's round 2 🟡 2 named, one token kind over.

Executed by the reviewer at `8b1492aa`, which is byte-identical to this
work item's base `3fc0c5bd` under `hooks/`, `tests/`, `.github/`, `skills/`
and `templates/` (read, `git diff --stat 8b1492aa 3fc0c5bd`, empty):

- three openers × eight breaks give `[("Mode", "shared")]`;
- over 20,000 seeded documents the base walk leaves both readings for the
  config reader in 2,035 and disagrees with the widened oracle on a claimed
  line in 3,123; the drafted walk scores 0 and 0;
- the declaration form did not reproduce, because the probe's closer `>`
  stood at a line start and opened a block quote.

## The class, enumerated

**Source.** CommonMark 0.31.2 §6.6 lists what an HTML tag is: an open tag, a
closing tag, an HTML comment, a processing instruction, a declaration or a
CDATA section. markdown-it-py 4.2.0, the version pinned in
`.github/scripts/run_tests.py#MARKDOWN_IT_VERSION`, recognises the same six
in `markdown_it/common/html_re.py#HTML_TAG_RE` and emits every one of them as · NAME NOT IN TREE
the single token type `html_inline` (`rules_inline/html_inline.py`). Both were
read on 2026-09-29; the parser's source was read in an installed copy of that
exact version. The open tag is listed twice below, because what a piece inside
it can hold depends on whether it starts in a quoted value.

| # | Construct | Opens at | Ends at (§6.6) | markdown-it-py 4.2.0 | What a piece inside can hold | How the walk decides | How the oracle decides | Case |
|---|---|---|---|---|---|---|---|---|
| H1 | HTML comment | `<!--` | the first `-->`; `<!-->` and `<!--->` are whole comments | the same, except it runs past a `-->` that a `-` precedes (`--->`) | anything | unchanged: `leaves_open` (the last `<!--` has no `-->` after it), in `walk_text`'s piece check and in `walk`'s pending state | unchanged in what it finds; now under the kind `inline html` | round 2's cases stand. The `--->` divergence stays pinned by name (`test_the_oracle_names_each_kind_it_hides`, "past the first closer"), and the walk follows the specification there, as F decided |
| H2 | CDATA section | `<![CDATA[` | the first `]]>` | the same (`[\s\S]*?`, lazy) | anything, a fence run and a table row included | new `leaves_html_open`: from the opener to the first `]]>` after it | any `html_inline` token | config ×8 breaks; `FOUND` (LS) |
| H3 | Processing instruction | `<?` | the first `?>` after the opener's `?`, so `<?>` does not close | the same | anything | `leaves_html_open`: to the first `?>` after the opener | any `html_inline` | config ×8; `FOUND` (FF) |
| H4 | Declaration | `<!` and an ASCII letter | the first `>` | the same (`<![A-Za-z][^>]*>`) | anything but `>` | `leaves_html_open`: to the first `>` after the opener | any `html_inline` | config ×8, with the closer written `a>` so that no `>` starts a line and opens a block quote; `FOUND` |
| H5 | Open tag, inside a quoted attribute value | `<` and a letter, then an attribute whose value opens with `"` or `'` | the value's own quote, then the tag's `>` | the same, except whitespace inside a tag is Python's `\s`, which takes all eight breaks; CommonMark takes spaces, tabs and up to one line ending | anything but that quote | `leaves_html_open`: `TAG_END`, the first `>` outside a quoted value | any `html_inline` | config ×8 for `"` and again for `'`; `FOUND` (NEL for `"`, PS for `'`) |
| H6 | Open tag, outside a quoted value | `<` and a letter | the first `>` outside a quoted value | as H5 | attribute names and unquoted values only, so no backtick and no space: never a fence run, never a `\| a \| b \|` row | as H5 | any `html_inline` | `FOUND` only, because no reader row can start inside one (`x <span` + LS + `lang="en">`); an oracle row for a later line beginning inside one |
| H7 | Closing tag | `</` and a letter | the first `>`, with only whitespace before it | as H5 for whitespace | whitespace only | as H5 (`INLINE_HTML` takes `</` and a letter) | any `html_inline` | `FOUND` only (`x </span` + VT + `>`). No whole-line oracle row: across a line ending the `>` would start the next line and open a block quote |

**Why the walk can be trusted not to under-report on H2 to H7.** For each
construct the closer the walk looks for is the parser's closer:
the first `]]>`, the first `?>`, the first `>`, or the first `>` outside a
quoted value. Where the parser forms the construct, the walk finds the same
end. Where the walk finds an opener the parser does not honour — inside a code
span, after a backslash, at an autolink, at `<` and a letter that never
becomes a tag — the walk reports it open, which errs only toward uncertain.
That is `leaves_open`'s own argument, extended. Where two constructs nest in
the text, the walk reads left to right and skips what an earlier construct
holds, which is also what the parser does.

**Inline constructs that are not raw HTML, and how each is decided.**

| Construct | Why it is outside this work | How the walk decides | How the oracle decides |
|---|---|---|---|
| Autolink (§6.5), `<scheme:…>` and `<address@…>` | The parser's `autolink` rule runs before `html_inline` and emits a link whose text a renderer displays | its `<` and a letter count as an opener, so a piece after an autolink left open is uncertain. That errs toward the base and costs claimed pieces only | shown |
| Code span (§6.1) | A renderer displays its content, and F's frame counts it as shown (its shape C1) | the walk knows no code span; an opener inside one counts, as `leaves_open` already says | shown |
| Link destination and title, image description, link reference definition (§6.3, §6.4, §4.7) | A renderer puts their text in an attribute or emits none of it. F's definition of *renderer hides* has never counted that, at block level (a reference definition produces no token) or inline. Widening it is a change to the acceptance property, not a fix inside it | unchanged: claimed by the line the piece starts in | shown |
| HTML blocks (§4.6) | Block level, and already modelled: the walk walks a comment block exactly and leaves every other kind uncertain to the end of the file; the oracle counts all seven kinds as `html` | unchanged | unchanged |

The third row is Q1, the one row that needs a person. Until it is answered
the property keeps F's definition there.

## Why the line is drawn at raw HTML

F's oracle already counts **every** kind of HTML block as hidden (`BLOCK_KINDS`
maps `html_block` whatever its type), and CommonMark §6.6 says raw HTML is
"rendered in HTML without escaping". So a line inside `<?php … ?>` is hidden
when it stands as a block, and today it is shown when the same thing stands
inline. The comment was the only inline kind F named because it was the only
one its rounds had met. Counting all six is the inline half of a rule the
block half already follows, and it is the parser's own category: one token
type, `html_inline`, which is what the ticket asks the oracle to read.

## The reading after this work

**`walk_text`.** A piece of a live GFM line is uncertain where the text of
that line before it leaves inline raw HTML open: a comment by `leaves_open`,
as now, or any of H2 to H7 by `leaves_html_open`. A piece of a fenced or
commented line keeps its line's answer and stays claimed. A piece that starts
at its line's start is asked about nothing, because the text before it is
empty.

**`walk`.** A paragraph line after a line that leaves H2 to H7 open is
uncertain, and so is every later line of that paragraph, up to a blank line,
a fence or a comment block. The walk does not look for that construct's
closer on later lines, because a tag's closer needs its quoted values tracked
across lines. That is what the round 3 draft calls *sticky*. After a comment
the pending state ends at `-->` as it does now, and the text after that `-->`
is asked both questions again. The cost is claimed lines, which Q2 measures.

**Which readers change.** Only the config reader, and what reads through it:

| Reader | Its base on an uncertain line | What changes |
|---|---|---|
| `hooks/config.py`, and through it `seal.py#table_span` and `broad_gate.py` | the fence-only reading | a piece inside H2 to H5 after a fence run earlier on its line is read by the fence-only reading, so the rows the base fenced are no rows |
| `hooks/routing.py#table_rows` | never hidden | nothing: the walk called these pieces live, and an uncertain line is read as live |
| `.github/scripts/rider_check.py#comment_blocks` | no fence state | nothing, for the same reason |

The routing and rider rows are why no case is added for either reader. Their
property halves run over the new `FOUND` documents all the same (S6).

## Scope

**In:**

- `hooks/blocks.py`: `leaves_html_open` with its two patterns, the sticky
  pending state in `walk`, the piece check in `walk_text`, and the module
  docstring and `walk_text`'s docstring, which name the contexts the walk is
  unsure of.
- `hooks/config.py#hidden_lines`' docstring, which lists "the lines after a
  mid-line `<!--`" among them.
- `templates/config.md` §*Broad gate*, whose sentence tells a person which
  contexts are read as before ("after a `<!--` in the middle of a line"), and
  a case that pins the widened sentence (§14).
- `tests/commonmark_oracle.py`: every `html_inline` token, top-level for lines
  and at any depth for pieces, under the kind `inline html`, with the two
  helpers renamed and the docstrings rewritten.
- The cases in S1 to S5 and S10 to S11, and the `FOUND` documents in S6.
- Ledger: F's rows P1-2, P2-1 and R1-1 corrected in place; this work item's
  own fragment for the new units.

**Out:**

| What | Why it is out | Who answers what is left |
|---|---|---|
| Round 3's 🟡 3 and ⬜ 5, a rider marker after a break GFM does not honour | Filed on #664, which is open and owns the class of a region cut where `str.splitlines` breaks and GFM does not; the round record's Deferred field sends it there | the work item that takes #664 |
| Link and image attribute text, and reference definitions | §*The class, enumerated*, third table: a change to what *renderer hides* means | a person, Q1 |
| `ALPHABET` | Six alphabet lines pushed `test_the_walk_is_exact_somewhere` to 22,166 of 69,084, under its third (executed by the reviewer), and an opener without its closer never forms inline HTML to the parser, so those lines tested nothing (61 passed with the base walk). The new shapes go in `FOUND` | nothing left |
| markdown-it-py running a comment past `--->` | Pinned by F as a parser divergence the walk must not follow | nothing left |
| F's `spec.md`, `plan.md` and phase records | F's own record of what it decided and built. This spec states where it widens F's definition; it does not rewrite F's documents | nothing left |
| `docs/` and both README editions | None of them states the walk's inline rule (read: `docs/*.md`, `README.md` and `README.ko.md` by the phrases "mid-line", "in the middle of a line", "inline comment", "inline HTML" and `blocks.py`; the only hits in `docs/` are about pull-request review comments) | nothing left |
| `skills/evidence-check/SKILL.md`'s mid-line comment sentence | Another reader, with its own question, not on the walk | nothing left |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the oracle names every inline kind on whole lines | Given a paragraph whose H2, H3, H4, H5 (both quotes) or H6 construct runs past a line ending, when `oracle.hidden(lines)` reads it, then every later line up to and including the closer's is `inline html`, and the line it opens on is not | one row per construct in `test_the_oracle_names_each_kind_it_hides`, each red with the oracle from `3fc0c5bd` |
| S2 · the oracle asks where each piece starts, for every kind | Given each of H2 to H7 opened before a break and closed after it, when `oracle.hidden_text` reads it, then the piece is `inline html`; a piece past a closed one is shown | assertions in `test_the_oracle_reads_the_text_not_a_readers_split` over its eight breaks, red with the oracle from `3fc0c5bd` |
| S3 · the config reader reads no row inside inline HTML | Given `x ` + opener + brk + "```" + brk + the config table + `\n` + closer, for H2, H3, H4 (closer `a>`), H5 `"` and H5 `'`, and all eight breaks, when `config_rows` reads it, then it returns `[]` | `tests/test_the_mode_question_is_asked_once.py#test_a_piece_inside_other_inline_html_is_no_config_row`, 40 cases, red at `3fc0c5bd` per opener |
| S4 · `walk_text`'s own answer | A piece after each of H2 to H7 its line left open is uncertain; a piece after one its line closed is claimed; a piece of a fenced line stays fenced and claimed | a case beside `test_a_piece_inside_its_lines_open_comment_is_the_only_piece_unsure`, red at `3fc0c5bd` on its first half |
| S5 · `walk`'s paragraph state | Given a line that leaves H2 to H6 open and two more paragraph lines, then a blank line and one more, when `walk` reads them, then the two are uncertain and the line after the blank is claimed | a case over `walk`, red at `3fc0c5bd` on its first half |
| S6 · the property holds with the class in the corpus | Given `FOUND` plus one document per row H2 to H7 that the case column marks, when halves 1 and 2 run over the config, routing and rider readers, then no reader leaves both readings and every claimed line matches the oracle | `test_where_the_walk_claims_to_be_exact_it_is` and the three `…never_leaves_both_readings` cases. Red: the new `FOUND` documents with the base walk and the widened oracle |
| S7 · the walk is still exact somewhere | Given the corpus with the new `FOUND`, when `test_the_walk_is_exact_somewhere` counts, then claimed lines stay above a third of the total | the case itself; the count goes in the phase record (Q2) |
| S8 · no committed file changes answer | Given every tracked `.md` file, when `config_rows` reads it at `3fc0c5bd` and at HEAD, then the answers are the same; and the walk's claimed lines over the same files are the same count | a measurement recorded in the phase record (Q3). The reviewer measured 24,009 of 68,819 claimed for both walks |
| S9 · the routing and rider readers do not move | Given their case tables, when they run at HEAD, then every case passes unedited | `tests/test_routing_is_recorded.py` and `tests/test_a_rider_reaches_its_file.py` green with only S11's edit in the second |
| S10 · the template says the widened rule | Given `templates/config.md` §*Broad gate*, when a person reads which contexts are read as before, then the list names inline HTML a line leaves open, not a `<!--` alone | a case asserting the new phrase and the absence of "after a `<!--` in the middle of a line", red with the old template |
| S11 · the rider case asks the hasher its own question | Given `test_a_break_commonmark_does_not_honour_quotes_no_rider`, when it runs, then the old region half over `text` (no `RIDER:` line kept) sits beside the new half over `region` | the case; its old half red under a `region_lines` mutant that walks the reader's split, green at HEAD |

## Failure direction and prompt budget

`CONTRIBUTING.md` asks each gate change for these; they are stated once here
and repeated in the pull request.

- **The config reader reads fewer rows, in one family only.** A row in a piece
  inside H2 to H5, after a fence run earlier on its GFM line, is read by the
  fence-only reading, which hides it. That is the reader's base, and it is the
  module's own direction: *nothing is declared*. Nothing is read that was not
  read before.
- **`broad-gate`** refuses where it read such a row, and names it fenced,
  because the base that hid it is the fence reading. No new sentence.
- **`mode-gate`** asks the mode question where the only `Mode` row stood in
  such a piece. That is *nobody declared*, inside its existing budget of two
  per session per repository. No committed file holds the shape (S8).
- **The commit gate and the rider check** do not change answer (§*Which readers
  change*).
- **Platform.** String processing only. All eight breaks are cases. A CRLF
  file is read the same way, because every predicate reads a line with its
  ending removed.

## Data & interfaces

- **`hooks/blocks.py`.** New: `INLINE_HTML` (the H2 to H7 openers, the comment
  excluded), `TAG_END` (the first `>` outside a quoted value) and
  `leaves_html_open(text)`. `leaves_open` keeps its name and its behaviour.
  `walk` gains the sticky state; `walk_text`'s check asks both predicates. No
  signature changes, and `Walk` is unchanged.
- **`tests/commonmark_oracle.py`.** The kind `COMMENT = "comment"` becomes
  `INLINE_HTML = "inline html"`. `_comment_lines` becomes `_inline_html_lines` · NAME NOT IN TREE
  and keeps every top-level `html_inline` token; its offsets are the parser's
  offsets in the paragraph's inline source, which is why it stays top-level.
  `_starts_in_a_comment` becomes `_starts_in_inline_html` and looks for the · NAME NOT IN TREE
  sentinel in `html_inline` tokens at any depth, an image description's
  children included, because the sentinel needs no offset. The module
  docstring's fourth place and `hidden_text`'s docstring say *inline raw HTML*.
  The two expectations that spell `"comment"` today spell `"inline html"`.
- **`tests/test_the_hooks_hide_what_a_renderer_hides.py#FOUND`.** Seven
  documents, one per case-column entry H2 to H7, the three from the round 3
  report among them. `ALPHABET` is not touched.
- **Ledger.** In `seal/ledger/1790645290-…md`, corrected in place with a dated
  note and re-stamped: P1-2 (it says "an inline HTML comment"; the
  `_comment_lines` anchor is dropped as renamed), P2-1 (its uncertain list · NAME NOT IN TREE
  says "the paragraph lines after a mid-line opener up to its closer"; `walk`
  and `FOUND` drift) and R1-1 (it says "leaves an inline comment open"; the
  `_starts_in_a_comment` anchor is dropped as renamed; `walk_text`, · NAME NOT IN TREE
  `hidden_text` and the rider and oracle cases drift). In
  `seal/ledger/1790659274-…md`: the renamed oracle units, `leaves_html_open`
  with its patterns, the S3, S4, S5 and S10 cases.
- **Messages.** None new. `templates/config.md`'s existing sentence widens
  (S10).

## Open questions → questions.md

One row needs a person, Q1, and it does not block the build: its default is
F's definition, which this work keeps. Q2 to Q5 are measurements.

Framed 2026-09-29 by framer, before the build.
