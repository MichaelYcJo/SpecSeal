# 1791128260-a-pact-row-is-read-in-one-plain-spelling — review round 3 report

Ran by: specseal:warden on claude-opus-5-5
Target SHA: 958de65f9f0548ca4b56eb03f2c55983fffab304 (PR #793, draft)
Base: `release/v0.18.2` at 94d7b2e0
Round 2's fix range: `ec5d3237..e6173ed6`, three commits; New units
`DELIMITER_ROW`, `DELIMITERS`, `WALKER_DELIMITERS`, `IN_A_CELL_FILE`; contract
change in `pact_line_refusal`
Kind of round: verifying, and the round cap. The target is round 2's fix diff.

## What this round was asked

Open round 2's fixes and judge whether each closes its finding with no
regression. For yellow 1: whether the 320-line delimiter construction's axes
are complete for GFM delimiter rows, whether a delimiter row the walker
accepts can sit under a header line the vendored copy does not see as
row-shaped and slip, and the widened property (a rendered `always` under a
rendered `Pact notify` means the copy is blind) re-run. For yellow 2: the
template and document sentences on `HTML_CELL` and the refusal's new cause
clause. Whites 3 and 4. The template copied whole must stay silent in both
readers.

## How the round was run

The repository was cloned with `git clone --no-local` into this round's
scratch directory and checked out at 958de65f; every probe ran there, through
the repository's own runner and its `cmarkgfm` oracle,
`tests/gfm_table_oracle.py`. Executed and read findings are labelled apart
below.

The implementer's account was read in full: round 2's record and report, the
three fix commits' messages, and the ledger fragment's diff. Its claims were
checked against the code or a probe. One could not be reproduced: the smith's
widened fuzz is not in the tree, and on this round's own fragment set the
property it reports as holding at the head does not hold (🟡 1, 🟡 2).

## Summary

Round 2 closed what it named, and the class is still open on two axes the
construction did not have.

1. Round 2's construction varied the delimiter row along five axes, all under
   one header shape, `| Mode | Pact notify |` written at the start of its own
   line. cmark-gfm renders a table on more delimiter rows than that: with a
   vertical tab or form feed where a space stands, and under a header that
   lazily continues a block quote. Under each the vendored copy is not blind,
   and its writer re-stamps a moved row with no record. This is 🟡 1. The
   plugin refuses all of them, because the header line holds a pipe.
2. The header axis the construction left out matters more. A one-column
   table needs no pipe anywhere: `Pact notify` over `:-:` over `always`
   renders a table that says `always`. Neither reader asks anything of a line
   with no pipe, so both read the default, and the plugin's own writer
   re-stamps a moved row with no record at exit 0. This is 🟡 2. It predates
   round 2 and is the transposed-table class of round 1's yellow 3, which
   round 1 and round 2 checked only for a two-cell header.
3. Round 2's yellow 2 and both whites are closed. The template copied whole
   is silent in both readers, before and after the fix proposed here.

One patch closes both findings. The two readers take one new predicate,
"the line under this one is a delimiter row GFM may read", which is wider
than the walker's `DELIMITER_ROW` on purpose. A line standing over one is a
table's header, so it is read whole and needs no pipe.

## 🟡 1 — Under a delimiter row with a vertical tab or form feed, or a header continuing a block quote, the vendored copy still re-stamps unrecorded

`skills/evidence-check/scripts/evidence_check.py:3808` decides that a line is
a table's header with `DELIMITER_ROW.match(under) and "|" in under`. That is
the walker's rule, and the walker's rule is narrower than what cmark-gfm
renders. Executed through the oracle, each of these renders a second table
with `Pact notify` over `always`:

- `---\x0b|---`, `---\x0c|---`, `|---|---|\x0b` and `|---|---|\x0c` under
  `| Mode | Pact notify |`. cmark-gfm's delimiter scanner takes a vertical tab
  and a form feed as spaces; `DELIMITER_ROW` takes a space and a tab only.
- `> x`, then `| Mode | Pact notify |` at the start of its line, then
  `> ---|---`. The header is a lazy continuation of the block quote's
  paragraph, and the delimiter row is inside the block quote. `> > `,
  `>` with no space, and `   > ` before the delimiter row render too.

In each case the header line matches `CONFIG_ROW_RE`, is read by its item
`Mode` alone, and names no pact, so `notify_may_be_always` returns False.
Executed end to end with the S9 fixture: the vendored writer exits 0,
re-stamps the moved row citing no clause, and writes no `seal/pact-changes/`
under `---\x0b|---`, `|---|---|\x0c` and the block-quote shape. The plugin's
writer exits 1 with a `LEFT` line on all three.

This is the same loss round 2's yellow 1 named, one axis over. The
construction in `tests/test_a_signatory_declares_its_pact.py` varies indent,
outer pipes, cell count, cell spelling and padding, with padding a space or
nothing. It has no axis for the whitespace class and none for a container
prefix. It also holds the copy to the walker, so a delimiter row cmark-gfm
renders and the walker does not read cannot appear in it at all.

The other half of the question asked has a clean answer. A header line the
copy does not see as row-shaped (an indented one, one with no outer pipe, one
inside a block quote) is read whole by `names_a_pact`, and it slips only where
it holds no pipe. That case is 🟡 2.

## 🟡 2 — A one-column table with no pipe says `always`, and both readers read the default

`hooks/config.py:938` refuses a line the walk did not take where it names a
pact and holds a `|`, unless the file holds an HTML table cell. The copy does
the same at `skills/evidence-check/scripts/evidence_check.py:3812`. The pipe
condition rests on "a line with no `|` has no value cell"
(`docs/the-pact.md:92`). That is false of a table's header. Executed through
the oracle: `Pact notify` over `:-:`, `:--`, `--:`, `-|`, `|-`, `|---|`,
` :-: `, `---\x0c` or `:-:\x0b`, over `always`, renders a one-column table
with header `Pact notify` and body `always`. A plain `---` does not, because
it is a setext underline.

Executed: under a `Pact` value, `pact_declaration` returns the default
`when the pact is touched` with no refusal, and `notify_may_be_always`
returns False. End to end, the plugin's writer and the vendored writer each
exit 0, re-stamp a moved row citing no clause, and write no
`seal/pact-changes/`.

Why it matters: this is the failure #759 exists to end. A person reading the
rendered config sees `Pact notify` set to `always`, and the plugin's own
writer re-stamps a moved row with no pact change, which clears the drift that
was the only trigger for the record. Round 1 graded the same loss through an
HTML table row as yellow 2, and this is graded the same way.

It predates round 2's fixes. It sits in units this branch built for #759, so
the branch owns it (see *What this round's verdicts mean for the run*).

The template stays silent under the fix. Executed: `templates/config.md`
whole gives `([], None, [])` and copy False, and `always` with the copy blind
once filled. This repository's `seal/config.md` is silent too. The two
sentences that promise a pipe-less sentence is free, `docs/the-pact.md:92`
and `templates/config.md:432`, each gain a clause and a pin in the patch.

## The widened property, re-run

The smith's fuzz is not in the tree, so this round wrote its own. It draws
60,000 configs, each a `Pact` value in the table and one to six fragment
lines below it, from 39 fragment entries (37 distinct, the blank line
weighted three times). Those include the transposed headers, a
pipe-less `Pact notify`, the delimiter rows above, the block-quote prefixes
and the body rows. Every config was rendered through cmark-gfm.

| | At 958de65f | With the patch below |
|---|---|---|
| configs cmark-gfm renders with `always` under `Pact notify` | 613 | 613 |
| of those, the plugin reads the default | 18 | 0 |
| of those, the copy is not blind | 38 | 0 |
| the plugin reads `always` and the copy is not blind | 0 | 0 |

The last row is round 1's property, and it still holds. It is too weak to
catch either finding, because in each the plugin refuses or reads the default
rather than `always`. The account's "0 at the head" for the widened property
holds only for the smith's fragment set, which this round could not see.
Classified, the head's 38 copy misses are all one of the two findings: a
pipe-less one-column header, or a vertical tab or form feed in the delimiter
row.

## Round 2's findings, answered

- **Yellow 1, closed for the spellings it named.** Executed: all 320
  `DELIMITERS` hold the copy blind exactly where the walker reads a delimiter
  row, and the `---|---` vendored writer case leaves the row. The class is
  open on two more axes, which is 🟡 1 and 🟡 2 of this round.
- **Yellow 2, closed.** Executed at the target: the template with a `<td>` in
  a comment gives 32 refusals, all 32 with the cause clause, and `notify`
  None. A piped line in the same file is refused without the clause. Read:
  `cell and not names_a_pact(line)` attaches the clause exactly where the
  pipe condition alone would not refuse, a decoded pipe included. Read: the
  template sentence spells the tag without its `<`, and the template whole is
  silent (executed). The new template pin fails against 8c33fad3's template
  (executed).
- **White 3, closed.** Read: the YAML sentence now says a line of it naming a
  pact is refused only where it holds a `|`. That is exact outside a file
  holding an HTML table cell, whose exception the same document states at
  line 93. Under the patch below, a line over a delimiter row is a second
  exception, which the patch's sentence at line 92 states.
- **White 4, answered.** Executed: S12 has 13 parameters at the target, as O3
  now says. Read: O2 states the cause clause, the C1 `Corrected ·` row states
  the header rule as round 2 wrote it, and the 16 re-stamped coordinates
  across eight rows are the units the fix range touched. `evidence-check
  --strict` exits 0 at the target (executed). Under the patch below, C1's
  parenthesis naming `DELIMITER_ROW` stops being true of the copy and has to
  be reworded in the closing commit. That is paperwork, and the patch's
  ledger note says so.
- **Rounds 1 and 2's green verdicts.** Carried. The patch leaves `PACT_WORD`,
  `names_a_pact`, the walk and `HTML_CELL` untouched. The two pact modules,
  the census module, the docs wrap test, the identifier test and the
  pull-request-language test pass with it (2490, executed).

## What this round's verdicts mean for the run

This is round 3 with no 🔴 open, so it is the round cap
(`docs/review-chain-spec.md` §*The review run has a bound, and an end*). It
opens two 🟡 findings that need a fix and answers `yes` to the floor, so no
record of this run has met the floor yet. The reopening bound is therefore
not engaged. The bound that stops the run here is the round cap.

Under §*The cap bounds rounds, and not the fixes of the round it stopped*,
the run may still write fixes for what the branch owns. Both findings are
the branch's.

- 🟡 1's coordinate is the header test round 2's fix wrote into
  `notify_may_be_always` around its new unit `DELIMITER_ROW`.
- 🟡 2's coordinates are `hooks/config.py#pact_lines_not_read` and the copy's
  pipe condition, both built by this branch for #759 (b0207eaa, 5efdea16).

So both are fixed on the branch rather than filed. This record's `Fixes
checked by` will read `round-4`. One verifying round then reads the fix diff
and ends the run whatever it finds, with `no fixes to check`. Whatever that
round opens takes the filing ladder, because three rounds is the only bound
a 🟡 gets.

## Regression tests to plant

All are in the patch below. Each was seen red at 958de65f: 11 cases failed
with the patch's tests and the target's code, and every case that existed
before passed (2161). The two new S12 pins were seen red against the
target's `docs/the-pact.md` and `templates/config.md`.

- `tests/test_a_signatory_declares_its_pact.py`: an S9 case that builds 256
  lines under a header by construction (block-quote prefix, outer pipes, one
  or two cells, `---` or `:-:`, padding of nothing, a space, a vertical tab
  or a form feed) under three header shapes. Wherever cmark-gfm renders
  `always` under `Pact notify`, it asserts the plugin refuses and the copy is
  blind. It also asserts more than 20 such configs per shape, so the case
  cannot pass on an empty set.
- The same module: three `STRAY_WAYS` rows for the pipe-less one-column
  table; S9 (b) relaxed from *exactly the walker* to *at least the walker*;
  S10 holding the new predicate equal across the two readers; two S12 pins.
- `tests/test_a_signatory_records_a_pact_change.py`, the vendored S9 writer
  case: three rows, for the vertical tab, the block quote and the one-column
  table.

## Facts for the evidence ledger

- cmark-gfm renders a one-column table from a header line with no pipe over
  `:-:`, `|---|`, `-|` or `---` followed by a form feed, but not over a plain
  `---`, which is a setext underline. Executed 2026-10-05 through
  `tests/gfm_table_oracle.py`.
- cmark-gfm's delimiter row takes a vertical tab and a form feed where a
  space stands, and is read under a header line that lazily continues a block
  quote. Executed 2026-10-05.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Round 2's header test is the walker's `DELIMITER_ROW`, narrower than cmark-gfm: under `---\x0b\|---`, `\|---\|---\|\x0c`, or a header lazily continuing a block quote over `> ---\|---`, the vendored copy reads the header by its item alone, is not blind, and its writer re-stamps a moved row at exit 0 with no pact change | `skills/evidence-check/scripts/evidence_check.py:3808` | open | executed: cmark-gfm renders each with `Pact notify` over `always`; copy False on each; vendored writer exit 0, re-stamped, no `seal/pact-changes/` on three; plugin writer exit 1 on three. The construction has no whitespace-class axis and no container axis, and it holds the copy to the walker rather than to cmark-gfm. With the patch: zero copy misses over 60,000 rendered configs |
| 🟡 2 | A line with no pipe over a delimiter row is a one-column table's header: `Pact notify` over `:-:` over `always` renders `always`, and both readers read the default, so the plugin's own writer and the vendored writer re-stamp a moved row at exit 0 with no pact change; `docs/the-pact.md:92` and `templates/config.md:432` say such a line carries no value | `hooks/config.py:938` | open | executed: oracle renders nine pipe-less delimiter spellings as a one-column table; `pact_declaration` gives the default with no refusal and the copy False; both writers exit 0, re-stamped, no record. 18 of 613 rendered-`always` fuzz configs read as the default by the plugin at the head, 0 with the patch; template and this repository's config still silent |
| 🟢 | round 2's yellow 1 is closed for the outer-pipe spellings it named | `skills/evidence-check/scripts/evidence_check.py:3808` | confirmed | executed: all 320 constructed delimiter lines hold the copy blind exactly where the walker reads one; the `---\|---` vendored writer row leaves. The class's other axes are this round's yellow 1 and 2 |
| 🟢 | round 2's yellow 2 is closed — the template and the pact say a cell tag anywhere refuses a pipe-less sentence, and the refusal names the cause only where the pipe condition alone would not refuse | `templates/config.md:432` | confirmed | executed: template plus a commented `<td>` gives 32 refusals, all with the clause; a piped line in the same file gets none; template whole silent and `always` when filled; the new template pin red against 8c33fad3 |
| 🟢 | round 2's white 3 is closed — the YAML sentence states when a line of front matter is refused | `docs/the-pact.md:347` | confirmed | read; exact outside a file holding an HTML table cell, the exception stated at line 93 |
| 🟢 | round 2's white 4 is closed — O3 counts the pins it rests on, O2 and C1 state the round-2 rules | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:14` | confirmed | executed: S12 has 13 parameters; `evidence-check --strict` exit 0 at the target. Read: the 16 re-stamped coordinates across eight rows are the units the fix range touched |
| carried | rounds 1 and 2's confirmations: the #784 spellings, the must-not set, the walk-index mapping, the HTML shapes, the template rewrite, the survivors rows | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried: the patch touches neither the word, the walk nor `HTML_CELL`; the touched modules pass at the target and with the patch (executed) |

## Executed probes

| What was run | Result |
|---|---|
| cmark-gfm through `tests/gfm_table_oracle.py` on 19 delimiter, container and one-column shapes, against both readers | vertical tab or form feed in or after the delimiter row, and a block-quote lazy header: rendered `always`, plugin refuses, copy False. Pipe-less one-column header: rendered `always`, plugin default with no refusal, copy False. A list-item lazy header, CRLF, CR, tabs around pipes: copy blind |
| cmark-gfm on a pipe-less `Pact notify` over 11 delimiter spellings, and on eight container shapes | one-column table on all but a plain `---` and `> :-:` outside a block quote; table under `> > `, `>`, `   > `, `- > ` and `> - ` prefixes |
| Both writers end to end, a moved row citing no clause, four shapes | one-column pipe-less: plugin and vendored exit 0, re-stamped, no record. Vertical tab, form feed, block quote: vendored exit 0, re-stamped, no record; plugin exit 1 with a `LEFT` line |
| 60,000 random configs over 39 fragment entries, rendered through cmark-gfm, at the target and with the patch | 613 render `always`; plugin default 18 then 0; copy not blind 38 then 0; plugin `always` with copy not blind 0 and 0 |
| The head's copy misses classified by header line and the line under it | all are a pipe-less one-column header or a vertical tab or form feed in the delimiter row |
| Template whole, with a commented `<td>`, filled; a piped line in a cell file; this repository's config — at the target and with the patch | silent and copy False; 32 refusals, 32 with the clause; filled `always`, copy blind; piped line without the clause; repository config silent. Same both times |
| The patch's tests against the target's code | 11 failed (the three `STRAY_WAYS` rows, two of the new S9 case's three shapes, S9 (a), S10, three vendored writer rows), 2161 passed |
| The patch whole: the two pact modules, the census module, the docs wrap test, the identifier test, the pull-request-language test | 2490 passed; ruff check and format clean on the four Python files |
| The two new S12 pins with the target's `docs/the-pact.md` and `templates/config.md` | 2 failed, 13 passed |
| Round 2's template pin with 8c33fad3's `templates/config.md` | 1 failed, 12 passed |
| `evidence-check --strict` at the target; with the patch | exit 0; exit 2 with DRIFTED on the units the patch touches, which the fix pass re-reads |
| The full suite, the repository-wide lint and the typecheck | not yet. That is the sealer's single run after the rounds settle, and nothing in this round stands in for it |

## Paste-ready fixes

```diff
# 🟡 1 and 🟡 2 — one patch, because the two readers take one new predicate.
# Applies with `git apply` at 958de65f. Executed: 2490 passed across the two
# pact modules, the census, the docs wrap, identifier and PR-language tests;
# ruff clean. The ledger re-reads it drifts are in the next block.
diff --git a/docs/the-pact.md b/docs/the-pact.md
--- a/docs/the-pact.md
+++ b/docs/the-pact.md
@@ -89,7 +89,10 @@ holds a `|`: a row written below the table's end, in a second table, in a block
 quote, inside a code fence or an HTML comment, or cut by a character only
 Python ends a line at. An example kept in a fence or a comment is refused too,
 because telling it from a live row would mean modelling GFM; delete it. A line
-with no `|` has no value cell, so the pact can be named in prose. In a file
+with no `|` has no value cell, so the pact can be named in prose. A line
+standing directly over a table's delimiter row is that table's header, and a
+one-column table needs no pipe anywhere, so such a line naming a pact is
+refused with or without a `|`, inside a block quote too. In a file
 that holds an HTML table cell's tag, `<td>` or `<th>`, anywhere, a code span, a
 fence or a comment included, a line naming a pact is refused with or without a
 `|`, because such a cell carries a value with no pipe beside it; take the tag
diff --git a/hooks/config.py b/hooks/config.py
--- a/hooks/config.py
+++ b/hooks/config.py
@@ -664,6 +664,17 @@ PACT_WORD = re.compile(r"(?<![^\W\d_])p[\W\d_]*a[\W\d_]*c[\W\d_]*t", re.I)
 # `evidence_check.py#HTML_CELL` is its copy, held equal by
 # `tests/test_a_signatory_declares_its_pact.py`.
 HTML_CELL = re.compile(r"<t[dh][\s/>]", re.I)
+# A line GFM may read as the delimiter row under a table's header, wider than
+# `DELIMITER_ROW` on purpose: block-quote markers and any whitespace before
+# it, a vertical tab or form feed where a space stands, and no pipe, because
+# a one-column table needs none. A run of dashes alone is a setext underline
+# and is left out. The line above one is a header, whose cells carry the
+# values below them, so it is read whole and needs no `|` (round 3 of PR
+# #793). `evidence_check.py#UNDER_A_HEADER` is its copy, held equal by
+# `tests/test_a_signatory_declares_its_pact.py`.
+UNDER_A_HEADER = re.compile(
+    r"^(?![ \t>]*-+[ \t]*$)[\s>]*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$"
+)
 
 
 def names_a_pact(text, piped=True):
@@ -909,7 +920,9 @@ def pact_lines_not_read(text, rows):
         line a `str.splitlines`-only character cuts, even where each of its
         pieces would be a row. In a file holding an HTML table cell
         (`HTML_CELL`) the `|` is not asked for, because such a cell carries
-        a value with no pipe beside it.
+        a value with no pipe beside it, and nor is it of a line directly
+        above one `UNDER_A_HEADER` matches, a table's header, whose value
+        stands in the row below (round 3 of PR #793).
 
     **Fences and comments are read through, on purpose.** Exempting them
     would make the refusal depend on `hidden_lines` matching GFM's block
@@ -925,17 +938,20 @@ def pact_lines_not_read(text, rows):
     taken = {index: item for index, item, _value in rows}
     piped = HTML_CELL.search(text) is None
     found, first = [], 0
-    for whole in blocks.gfm_lines(text, keepends=True):
+    wholes = blocks.gfm_lines(text, keepends=True)
+    for at, whole in enumerate(wholes):
         pieces = len(whole.splitlines())
         index, first = first, first + pieces
         line = whole.rstrip("\r\n")
+        under = wholes[at + 1].rstrip("\r\n") if at + 1 < len(wholes) else ""
+        header = UNDER_A_HEADER.match(under) is not None
         if pieces == 1 and index in taken:
             item = taken[index]
             if item not in (PACT_ROW, PACT_NOTIFY_ROW) and names_a_pact(
                 item, piped=False
             ):
                 found.append(line)
-        elif names_a_pact(line, piped):
+        elif names_a_pact(line, piped and not header):
             found.append(line)
     return found
 
diff --git a/skills/evidence-check/scripts/evidence_check.py b/skills/evidence-check/scripts/evidence_check.py
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ -3744,13 +3744,14 @@ PACT_WORD = re.compile(r"(?<![^\W\d_])p[\W\d_]*a[\W\d_]*c[\W\d_]*t", re.I)
 # table cell's opening tag, in whose file a line naming a pact needs no `|`
 # (round 1 of PR #793, yellow 2).
 HTML_CELL = re.compile(r"<t[dh][\s/>]", re.I)
-# `hooks/config.py#DELIMITER_ROW`, copied for a copy with no `hooks/`: a GFM
-# delimiter row, its outer pipes each optional, at most three spaces in. The
-# GFM table walker reads a line as one where this matches and a pipe stands
-# in it, and so does `notify_may_be_always` (round 2 of PR #793, yellow 1);
-# `tests/test_a_signatory_declares_its_pact.py` holds the two equal.
-DELIMITER_ROW = re.compile(
-    r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$"
+# `hooks/config.py#UNDER_A_HEADER`, copied for a copy with no `hooks/`: a
+# line GFM may read as the delimiter row under a table's header, block-quote
+# markers, a vertical tab or form feed and a one-column row without a pipe
+# included, a run of dashes alone left out. That comment says why (round 3
+# of PR #793); `tests/test_a_signatory_declares_its_pact.py` holds the two
+# equal.
+UNDER_A_HEADER = re.compile(
+    r"^(?![ \t>]*-+[ \t]*$)[\s>]*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$"
 )
 
 
@@ -3785,11 +3786,11 @@ def notify_may_be_always(said):
     (`HTML_CELL`), which carries a value with no pipe (#759; round 1 of PR
     #793, yellow 2).
 
-    **A table's header is read whole.** A row-shaped line directly above a
-    delimiter row, read as the plugin's GFM walker reads one (`DELIMITER_ROW`
-    and a pipe, the outer pipes each optional), is a header, and a transposed table names the item there
-    and puts the value in the row below, so its item alone says nothing
-    (round 1 of PR #793, yellow 3).
+    **A table's header is read whole, and needs no pipe.** A line directly
+    above one `UNDER_A_HEADER` matches is a header, and a transposed table
+    names the item there and puts the value in the row below, so its item
+    alone says nothing (round 1 of PR #793, yellow 3), and a one-column
+    table's header holds no `|` (round 3 of PR #793).
 
     Where the plugin refuses and this copy does not, nothing can mean
     `always`: a plain `Pact` row outside the table, a plain row with no
@@ -3805,11 +3806,11 @@ def notify_may_be_always(said):
     piped = HTML_CELL.search(said) is None
     for at, line in enumerate(lines):
         under = lines[at + 1] if at + 1 < len(lines) else ""
-        header = DELIMITER_ROW.match(under) and "|" in under
+        header = UNDER_A_HEADER.match(under) is not None
         plain = line.splitlines() == [line] and not header
         match = CONFIG_ROW_RE.match(line) if plain else None
         if match is None:
-            if names_a_pact(line, piped):
+            if names_a_pact(line, piped and not header):
                 return True
             continue
         item = match.group("item").replace("\\|", "|")
diff --git a/templates/config.md b/templates/config.md
--- a/templates/config.md
+++ b/templates/config.md
@@ -433,7 +433,8 @@ table. A sentence with no pipe in it may name the pact freely, which is why
 this section is written without one: this file can be copied whole. A file
 that also holds an HTML table cell's tag, a `td` or `th` opened with a `<`,
 anywhere, a comment or a code span included, refuses such a sentence too, so
-keep that tag out of this file.
+keep that tag out of this file. So does a line of dashes and colons directly
+under the sentence, which makes it a one-column table's header.
 
 ## The fold's values
 
diff --git a/tests/test_a_signatory_declares_its_pact.py b/tests/test_a_signatory_declares_its_pact.py
--- a/tests/test_a_signatory_declares_its_pact.py
+++ b/tests/test_a_signatory_declares_its_pact.py
@@ -20,6 +20,7 @@ import os
 import sys
 import unicodedata
 
+import gfm_table_oracle as oracle
 import pytest
 from conftest import load_hook_module
 
@@ -431,6 +432,17 @@ STRAY_WAYS = [
         )
         for d in WALKER_DELIMITERS
     ),
+    # Round 3 of PR #793, yellow 2: a one-column table needs no pipe, so its
+    # header names the item with none and the value stands below it.
+    *(
+        (
+            f"a one-column table with no pipe over {d!r}",
+            CONFIG + f"\nPact notify\n{d}\nalways\n",
+            ["Pact notify"],
+            ORDERS,
+        )
+        for d in (":-:", "|---|", "---\x0c")
+    ),
 ]
 
 
@@ -794,15 +806,69 @@ def test_s9_the_vendored_copy_reads_the_silent_set_as_the_table_says():
     )
     assert ec.notify_may_be_always(None) is True
     # Round 2 of PR #793, yellow 1: the copy reads a line as a table's header
-    # exactly where the plugin's walker reads the line under it as a
-    # delimiter row.
-    for d in DELIMITERS:
+    # wherever the plugin's walker reads the line under it as a delimiter
+    # row; round 3 widened it, so this is at least, not exactly.
+    for d in WALKER_DELIMITERS:
         text = CONFIG + f"\n| Mode | Pact notify |\n{d}\n| shared | always |\n"
-        assert ec.notify_may_be_always(text) is (d in WALKER_DELIMITERS), repr(d)
+        assert ec.notify_may_be_always(text) is True, repr(d)
     with open(os.path.join(ROOT, "seal", "config.md"), encoding="utf-8") as f:
         assert ec.notify_may_be_always(f.read()) is False
 
 
+# Round 3 of PR #793, yellows 1 and 2: the lines under a header by
+# construction, each axis a way cmark-gfm renders a table `DELIMITER_ROW`
+# does not read -- a block quote the header continues lazily, a vertical tab
+# or form feed where a space stands, a one-column row with no pipe -- under
+# a two-cell header, a one-cell header and a one-cell header with no pipe.
+UNDERS = sorted(
+    {
+        quote + left + "|".join([f"{pad}{cell}{pad}"] * cols) + right
+        for quote in ("", "> ", ">", "   > ")
+        for left in ("", "|")
+        for right in ("", "|")
+        for cols in (1, 2)
+        for cell in ("---", ":-:")
+        for pad in ("", " ", "\x0b", "\x0c")
+    }
+)
+
+
+def _rendered_always(text):
+    """True where cmark-gfm renders `always` in a `Pact notify` column."""
+    for head, rows in oracle.tables(text):
+        if "Pact notify" in head:
+            k = head.index("Pact notify")
+            if any(len(r) > k and r[k] == "always" for r in rows):
+                return True
+    return False
+
+
+@pytest.mark.parametrize(
+    "header, body",
+    [
+        ("| Mode | Pact notify |", "| shared | always |"),
+        ("| Pact notify |", "| always |"),
+        ("Pact notify", "always"),
+    ],
+    ids=["two cells", "one cell", "one cell, no pipe"],
+)
+def test_s9_a_header_gfm_renders_is_read_whole_by_both_readers(header, body):
+    """S9. Wherever cmark-gfm renders `always` under a `Pact notify` header,
+    the plugin's reader refuses and a copy with no `hooks/` is blind, so
+    neither re-stamps a moved row the rendered table says is `always`."""
+    shown = 0
+    for under in UNDERS:
+        quote = under[: len(under) - len(under.lstrip(" >"))]
+        lazy = "> x\n" if quote else ""
+        text = CONFIG + f"\n{lazy}{header}\n{under}\n{quote}{body}\n"
+        if not _rendered_always(text):
+            continue
+        shown += 1
+        assert config.pact_declaration(text)[1] is None, repr(under)
+        assert ec.notify_may_be_always(text) is True, repr(under)
+    assert shown > 20, shown
+
+
 @pytest.mark.parametrize(
     "ch", SPLITLINES_ONLY, ids=[f"U+{ord(c):04X}" for c in SPLITLINES_ONLY]
 )
@@ -834,7 +900,7 @@ def test_s10_the_reader_and_the_vendored_copy_read_one_word():
         ec.HTML_CELL.pattern,
         ec.HTML_CELL.flags,
     )
-    assert config.DELIMITER_ROW.pattern == ec.DELIMITER_ROW.pattern
+    assert config.UNDER_A_HEADER.pattern == ec.UNDER_A_HEADER.pattern
     lines = {line for text in S2_TEXTS for line in text.splitlines()}
     lines |= {line for below, _ in SILENT for line in (CONFIG + below).splitlines()}
     lines |= set(OTHER_ITEMS)
@@ -943,6 +1009,18 @@ def test_the_blind_side_is_read_as_no_line(item, gap):
             "with a `<`, anywhere, a comment or a code span included, refuses such a "
             "sentence too, so keep that tag out of this file.",
         ),
+        (
+            ("docs", "the-pact.md"),
+            "A line standing directly over a table's delimiter row is that table's "
+            "header, and a one-column table needs no pipe anywhere, so such a line "
+            "naming a pact is refused with or without a `|`, inside a block quote "
+            "too.",
+        ),
+        (
+            ("templates", "config.md"),
+            "So does a line of dashes and colons directly under the sentence, which "
+            "makes it a one-column table's header.",
+        ),
     ],
     ids=[
         "the pact: the rule",
@@ -958,6 +1036,8 @@ def test_the_blind_side_is_read_as_no_line(item, gap):
         "template: the Absent cell",
         "template: no pipe",
         "template: an HTML table cell's tag, round 2 of PR #793",
+        "the pact: a table's header, round 3 of PR #793",
+        "template: a table's header, round 3 of PR #793",
     ],
 )
 def test_s12_the_documents_say_a_pact_row_is_read_in_one_spelling(parts, sentence):
diff --git a/tests/test_a_signatory_records_a_pact_change.py b/tests/test_a_signatory_records_a_pact_change.py
--- a/tests/test_a_signatory_records_a_pact_change.py
+++ b/tests/test_a_signatory_records_a_pact_change.py
@@ -1627,6 +1627,9 @@ SPLITLINES_ONLY = ["\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", " ", "\u
         "\n<table><tr><td>Pact notify</td><td>always</td></tr></table>\n",
         f"\n| Pact | Pact notify |\n|---|---|\n| {PACT_URL} | always |\n",
         "\n| Mode | Pact notify |\n---|---\n| shared | always |\n",
+        "\n| Mode | Pact notify |\n---\x0b|---\n| shared | always |\n",
+        "\n> x\n| Mode | Pact notify |\n> ---|---\n> | shared | always |\n",
+        "\nPact notify\n:-:\nalways\n",
     ],
     ids=[
         "below the table",
@@ -1650,6 +1653,9 @@ SPLITLINES_ONLY = ["\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", " ", "\u
         "round 1 of PR #793, yellow 2: an HTML table row",
         "round 1 of PR #793, yellow 3: a transposed table",
         "round 2 of PR #793, yellow 1: a delimiter row with no outer pipes",
+        "round 3 of PR #793, yellow 1: a vertical tab in the delimiter row",
+        "round 3 of PR #793, yellow 1: a header a block quote continues",
+        "round 3 of PR #793, yellow 2: a one-column table with no pipe",
     ],
 )
 def test_s9_a_vendored_copy_leaves_where_the_plugin_refuses_a_pact_line(
```

```markdown
🟡 1 and 🟡 2 — the closing commit's paperwork, not code.
seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md: the patch
drifts the coordinates `evidence-check --strict` names (pact_lines_not_read,
notify_may_be_always, the two documents' sections, the template's "## Pact"
and "# Repository config", S9, S10, S12). Re-read them with
`--reverify --into`. In the C1 `Corrected ·` row, replace

  unless it stands directly above a delimiter row as the GFM walker reads one
  (`DELIMITER_ROW` and a pipe, the outer pipes each optional), where it is a
  table's header and is read whole,

with

  unless it stands directly above a line GFM may read as a delimiter row
  (`UNDER_A_HEADER`: block-quote markers, a vertical tab or form feed, and a
  one-column row with no pipe included), where it is a table's header and is
  read whole with no `|` asked,

and in the O1 or O3 row that states the pipe condition, add that a line over
such a row is refused without a `|` (round 3 of PR #793).
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (the vendored copy re-stamps unrecorded under a
delimiter row with a vertical tab or form feed, or a header continuing a block
quote), 🟡 2 (a one-column table with no pipe says `always` and both readers
read the default)

Loses a record or crashes: yes — under 🟡 2 the plugin's writer and the
vendored writer, and under 🟡 1 the vendored writer, re-stamp a moved row
citing no clause at exit 0 and record no pact change, where the rendered table
says `Pact notify` is `always` (executed)

The broad gate has not come due: this round leaves two findings open. Once
round 4 reads the fix diff and the run ends, what comes due is the sealer's
spawn.

## Proof block

Files opened at 958de65f in the clone, or in the repository under review
read-only:

- `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/rounds/round-2.md`
  and `round-2-report.md`
- the fix-range diff `ec5d3237..e6173ed6` of `hooks/config.py`,
  `skills/evidence-check/scripts/evidence_check.py`, `templates/config.md`,
  `docs/the-pact.md`, `tests/test_a_signatory_declares_its_pact.py`,
  `tests/test_a_signatory_records_a_pact_change.py` and the ledger fragment;
  the three commits' messages
- `hooks/config.py` lines 650-1300 (`PACT_WORD`, `HTML_CELL`, `names_a_pact`,
  `pact_declaration`, `pact_lines_not_read`, `pact_line_refusal`,
  `DELIMITER_ROW`, `table_cells`, `gfm_table`)
- `skills/evidence-check/scripts/evidence_check.py` lines 365-400, 3305-3345
  and 3735-3840
- `docs/the-pact.md` lines 80-100 and 318-358
- `skills/evidence-check/SKILL.md` lines 330-345
- `templates/config.md` lines 415-440
- `tests/test_a_signatory_declares_its_pact.py` lines 1-40, 188-260, 400-440,
  620-720, 770-845 and 975-1030
- `tests/test_a_signatory_records_a_pact_change.py` lines 1540-1690
- `tests/test_every_reader_ends_a_line_where_gfm_does.py` lines 676-700
- `tests/gfm_table_oracle.py`
- `skills/code-review/orchestration.md` lines 120-240
- `docs/review-chain-spec.md` lines 41-136 and 373-420
- `bin/test` and `CONTRIBUTING.md` lines 120-160

The probes, their fixtures, the trial patch and the clone were removed at the
end of the round.
