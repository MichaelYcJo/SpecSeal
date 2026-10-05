# 1791128260-a-pact-row-is-read-in-one-plain-spelling — review round 4 report

Ran by: specseal:warden on claude-opus-5-5
Target SHA: a3808f8197872f321690a22aa939348b7dfae879 (PR #793, draft)
Base: `release/v0.18.2` at 94d7b2e0
Round 3's fix range: `72b290c6..56558074`, four commits; New unit
`UNDER_A_HEADER` (depth 1), shared by both readers and held equal by S10
Kind of round: verifying, after the round cap, and the last round of this
run. The target is round 3's fix diff.

## What this round was asked

Open round 3's fixes and judge whether each closes its finding with no
regression. The questions were these:

- whether the construction's axis set is complete for what cmark-gfm renders
  as a table header over a delimiter row;
- whether `UNDER_A_HEADER` refuses anything that must stay silent;
- the rendered-cell 60,000-config fuzz, re-run;
- whether the test module's import cost is acceptable or should move into the
  test bodies.

Rounds 1 to 3's confirmations are inherited, and only what the fixes touch is
re-checked.

## How the round was run

The repository was cloned with `git clone --no-local` into this round's
scratch directory and checked out at a3808f81. Every probe ran there, through
the repository's own runner (`bin/test`) and its oracle,
`tests/gfm_table_oracle.py`, which is cmark-gfm pinned at 2025.10.22.
Findings from reading and findings from execution are labelled apart below.

The implementer's account was read in full: round 3's record and report, the
fix commits' messages, the ledger and overview diffs, and the orchestrator's
spawn prompt. Each claim was checked against the code or a probe. One claim
did not hold, about where the import cost comes from (⬜ 1).

## Summary

Round 3's two findings are closed, and the predicate is the right shape. The
three findings this round opens are all ⬜. None of them changes what either
reader decides.

1. **Both readers held on every table this round could construct.** The
   construction this round built is wider than the one in the tree: 31
   containers, 6 header styles, 10 padding characters, escaped pipes in the
   delimiter row, and a delimiter row wider than its header. It gave 112,530
   configs, and cmark-gfm rendered `always` under `Pact notify` in 36,424 of
   them. The plugin read none of those as the default without a refusal, and
   the vendored copy was blind on every one (executed). Against the code
   before the fix, the same construction finds 7,087 plugin misses and 7,408
   copy misses, so it can fail.
2. **Nothing that must stay silent is refused.** That covers the template
   copied whole, this repository's config, a setext heading at the margin, in
   a list and in a block quote, the thematic breaks, and YAML front matter
   (executed).
3. **The fuzz holds.** Over 60,000 random configs, 4,637 render `always`.
   Neither reader misses at the target, and at the code before the fix 10
   are missed (executed).
4. **The import cost is not the oracle (⬜ 1).** The smith's note says the
   module renders the oracle about 2,400 times at import, for about 3 s per
   worker. The renders are 2,520 and take 0.11 s. The 2.43 s is
   `DELIMITERS`, which scans all of Unicode once for each of its 60 outer
   combinations. Making the padding tuple once brings the import from 2.76 s
   to 0.41 s, with the same 1,680 rows. Moving the oracle into the test
   bodies would leave that cost where it is.
5. **The oracle-kept rows have no floor (⬜ 2).** Round 3's proposed case
   asserted more than 20 rendered configs per shape, and the landed
   construction dropped that. If the oracle filter keeps nothing, S2 and S9
   pass over an empty set (executed).
6. **The template's new sentence overstates (⬜ 3).** It says "a line of
   dashes and colons" refuses, but a line of dashes alone does not.

## Round 3's findings, answered

### Yellow 1 — closed

The vertical tab, the form feed and a header lazily continuing a block quote
are now covered. Read: `hooks/config.py:677` and
`skills/evidence-check/scripts/evidence_check.py:3753` hold one pattern, and
S10 holds them equal. Both readers take it at the line under each line
(`hooks/config.py:949`, `skills/evidence-check/scripts/evidence_check.py:3809`).

Executed:

- In the tree's construction, 793 rows are kept under `STRAY_WAYS`. Margin
  261, three block-quote forms and the list item 111 each, three spaces in
  88. Four spaces and a tab give none, which is right, because each is a code
  block.
- `test_s9_a_vendored_copy_leaves_where_the_plugin_refuses_a_pact_line`, 31
  passed. Its three new rows are a vertical tab in the delimiter row, a
  header a block quote continues, and a pipe-less one-column table.
- Two mutations show the cases can fail. With `[\s>]*` narrowed to `\s*` (no
  block-quote marker), 20 cases fail. With every `\s` narrowed to `[ \t]`,
  12 fail.

### Yellow 2 — closed

A pipe-less line over a delimiter row is a header in both readers:
`names_a_pact(line, piped and not header)` at `hooks/config.py:956` and
`skills/evidence-check/scripts/evidence_check.py:3813`.

Executed: when the pipe condition was put back on the plugin's header line,
45 cases failed. When a pipe was required in the delimiter row, 45 failed.
The `docs/the-pact.md:93` sentence matches the code as far as the probes
reached, and S12 pins it. The ledger's C1 `Corrected ·`, O1 and O3 rows state
`UNDER_A_HEADER` (read). `evidence-check --strict` exits 0 at the target
(executed).

### The setext exclusion — pinned, and seen red

Executed: with the lookahead `(?![ \t>]*-+[ \t]*$)` removed from both copies,
two cases fail and nothing else does:

- `test_s4_a_line_that_is_not_a_pact_row_in_another_spelling_is_silent[a setext heading naming a pact]`
- `test_s9_the_vendored_copy_reads_the_silent_set_as_the_table_says`

## The construction's axis set, judged

The prompt asked about six axes beyond the ones in the tree. Each was built
and rendered through cmark-gfm, then run against both readers. All executed.

| Axis | What cmark-gfm renders | Both readers |
|---|---|---|
| A backslash-escaped pipe in the delimiter row, between two cells, after one cell, and inside outer pipes | no table | nothing to hold |
| A delimiter row wider than its header (four cells under three) | no table | nothing to hold |
| Header with trailing spaces, a trailing backslash, an escaped pipe in a cell, outer pipes that differ from the delimiter row's | a table wherever the delimiter row is one | 0 misses |
| Nested containers: `> > `, `>>`, `>  `, `>` then a tab, `   > `, `> - `, `- > ` | a table | 0 misses |
| List items: `-`, `*`, `+`, `1.`, `1)`, `10.`, a wide `-   `, `-` then a tab; a lazy header in a list | a table under the content indent; none where the delimiter row is lazy | 0 misses |
| A paragraph line above the header with no blank line, at the margin, in a block quote, in a list, and a heading above | a table, the last line being the header | 0 misses |
| Padding of no-break space, em space, ideographic space, U+001C and U+0085 | no table: only tab, vertical tab and form feed are taken | wider than cmark-gfm, which is the fail-closed direction |

So the predicate is complete over every axis tried. The construction in the
tree is narrower than this one in three ways:

- only spaces pad a delimiter row behind a container;
- the header's outer pipes always copy the delimiter row's;
- there are no nested containers, no ordered-list markers and no paragraph
  line above.

None of those reaches a branch the predicate does not already take. Its
container part is one class, `[\s>]*`, and the mutations above show the tree's
construction already fails when that class narrows. This is not a finding.

## Breadth: what `UNDER_A_HEADER` refuses that must stay silent

Executed, with the prose line "This repository signs the orders pact" over
each line below:

- **Silent in both readers, as they must be.** `---`, `--- `, `  ---`,
  `----------`, `-`, `- - -`, `***`, `___`, `===`, `> ---`, `---` then a
  tab, a tab then `---`, `-- -`. A setext heading in a list item and in a
  block quote. YAML front matter, including `Pact notify: always` in it and
  a closing `--- ` with a trailing space. A thematic break after a blank
  line. The template copied whole, with no pact in the plugin and the copy
  `False`. This repository's `seal/config.md`, the same.
- **Refused, and cmark-gfm renders a one-column table, so correct.** `:-`,
  `---` with a vertical tab after it, a vertical tab before `---`.
- **Refused where cmark-gfm renders no table.** These are the two places
  the predicate is wider than GFM:
  - a no-break space before `---`, where cmark-gfm renders a paragraph;
  - `|---|---|` under a one-cell line, where the column counts differ and
    cmark-gfm renders a paragraph.

  Both are fail-closed. The refusal names the line, and a person meets it
  only by writing one of these two lines directly under prose that names the
  pact. Neither is a shape this repository writes, so this is not a finding.

## The fuzz, re-run

Round 3's fuzz is not in the tree, so this round wrote its own. It draws
60,000 configs, each the test module's `CONFIG` with a `Pact` value, plus one
to six fragment lines below it. Seed 793. There are 53 fragment entries, the
blank line counted three times:

- pact rows in both spellings;
- transposed headers and pipe-less `Pact notify` lines;
- delimiter rows with tabs, vertical tabs and form feeds;
- block-quote, list-item and ordered-list prefixed headers, delimiters and
  bodies;
- prose naming the pact, an HTML comment, a heading, YAML-like lines, and a
  header with trailing spaces or a backslash.

The property counts a config as rendering `always` when cmark-gfm renders
any of three things:

- `always` in a `Pact notify` column;
- `always` as the header cell after `Pact notify`;
- a body row `Pact notify` / `always`.

| | At 72b290c6 (code before round 3's fixes) | At a3808f81 |
|---|---|---|
| configs rendered with `always` | 4,637 | 4,637 |
| the plugin reads something other than `always` with no refusal | 10 | 0 |
| the copy is not blind | 10 | 0 |
| both | 9 | 0 |

## ⬜ 1 — The import cost is a Unicode scan repeated 60 times, not the oracle

`tests/test_a_signatory_declares_its_pact.py:241`. The padding tuple inside
`DELIMITERS` is a generator over every code point, written in the
comprehension's innermost `for` clause. Python evaluates that clause once per
outer combination: 2 left × 2 right × 3 column counts × 5 cells, which is 60
scans of 1,114,112 characters.

Measured (executed):

| What | Time |
|---|---|
| the whole module import | 2.74 to 2.81 s |
| `DELIMITERS` as written | 2.43 s |
| the same set with the tuple made once | 0.041 s, the same set |
| 2,520 oracle renders | 0.11 s |
| the module import with the tuple made once | 0.41 s, 1,680 delimiter rows and 840 `STRAY_WAYS` rows as before |
| the module under the patch | 2646 passed |

**Why it matters.** Every pytest-xdist worker collects this module. So the
2.4 s is paid by each worker, on every full-suite run and on every narrow run
of this module. Moving the oracle into the test bodies, as the smith's note
offers, would save about 0.1 s of it.

**Judgement.** The cost does not need to move into the test bodies. With the
tuple made once, the oracle filter at import costs about 0.15 s and can
stay where it is. The release ships no defect either way, so this is ⬜.

## ⬜ 2 — The oracle-kept rows have no floor, so S2 and S9 can pass over nothing

`tests/test_a_signatory_declares_its_pact.py:490`. `STRAY_WAYS` keeps a
constructed row only where `oracle.rows_under(text, cells)` returns rows
under exactly the header the row was built with. If a later edit stops the
oracle rendering that header, the filter keeps nothing and both
`test_s2_every_way_the_walk_passes_a_pact_row_by_is_refused` and
`test_s9_the_vendored_copy_cannot_rule_always_out_on_any_s2_text` stay green.
Such an edit could be the header text, the joiner, or the `CONFIG` prefix.
Round 3's proposed case asserted `shown > 20` per shape for this reason, and
the landed construction dropped it.

Executed: `rows_under` was called with a header no row has, which empties
the filter. The module then ran 1852 passed with no failure. With the case
below added, that case failed alone. At the target it passes.

The renderer cannot move, because `cmarkgfm` is pinned, so nothing ships
broken today. This is ⬜.

## ⬜ 3 — The template says a line of dashes and colons refuses; a line of dashes alone does not

`templates/config.md:436` reads: "So does a line of dashes and colons
directly under the sentence, which makes it a one-column table's header."
S12 pins it.

Executed above: `---` under a pact-naming sentence is a setext underline,
and both readers stay silent. The sentence is also silent about pipes,
though `|---|` refuses. Both errors are in the safe direction. A person who
believes it avoids a heading that would have been fine, and a refusal names
the line it refuses.

The behaviour is right, and the sentence overstates the rule in the one case
a person is most likely to write, a heading over the sentence. This is ⬜. A
wording that keeps the template free of pipes:

> So does a line directly under the sentence that GFM reads as a table's
> delimiter row, such as `:-:` or `---:` (dashes alone are a heading's
> underline and refuse nothing), which makes the sentence a one-column
> table's header.

The S12 pin would change with it.

## What this round's verdicts mean for the run

This is the verifying round after the cap, and the run ends here. It opens
nothing at 🔴 or 🟡, so `Needs a fix` is `no`. The three ⬜s go through the
filing ladder. Their coordinates sit in units this branch owns: the test
module's construction and the template sentence it added. The release ships
no defect if they stand.

The broad gate has now come due. What comes due is the sealer's spawn, not
a run for the session reading this.

## Regression tests to plant

None is owed: no 🔴 or 🟡 is open. If ⬜ 2 is taken, its case is in the
fenced patch below, at `tests/test_a_signatory_declares_its_pact.py`. It was
seen red with the oracle filter emptied: 1 failed, and it was the only
failure.

## Facts for the evidence ledger

- cmark-gfm renders no table for a delimiter row holding an escaped pipe
  (`---\|---`), or for a delimiter row with more cells than its header.
  Executed 2026-10-05 through `tests/gfm_table_oracle.py`.
- cmark-gfm takes only tab, vertical tab and form feed as padding in a
  delimiter row. A no-break space, an em space, an ideographic space, U+001C
  and U+0085 give no table. Executed 2026-10-05.
- cmark-gfm renders a table under a header behind `> > `, `> - `, `- > `,
  `*`, `+`, `1.`, `1)` and `10.` containers when the delimiter row sits at
  the content indent. It renders none when the delimiter row is a lazy line
  under a list item, or under a header that lazily continues a block quote
  with the delimiter row unprefixed. Executed 2026-10-05.
- A paragraph line directly above a header does not stop the table: the
  paragraph's last line is the header. Executed 2026-10-05.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `DELIMITERS` re-scans all of Unicode for each of its 60 outer combinations, which is 2.43 s of the module's 2.76 s import, paid by every xdist worker; the oracle renders cost 0.11 s, so the cost is not the oracle's and need not move into the test bodies | `tests/test_a_signatory_declares_its_pact.py:241` | open | executed: hoisting the padding tuple gives the same 1,680 rows, the import drops to 0.41 s, and the module still passes 2646; no reader changes |
| ⬜ 2 | The oracle-kept `STRAY_WAYS` rows have no floor: emptied, S2 and S9 pass over nothing; round 3's `shown > 20` guard was not landed | `tests/test_a_signatory_declares_its_pact.py:490` | open | executed: with `rows_under` given a header no row has, the module passed 1852 with no failure; the proposed per-container floor fails alone there and passes at the target |
| ⬜ 3 | The template says a line of dashes and colons under a pact sentence refuses; a line of dashes alone does not, and `\|---\|` does without being named | `templates/config.md:436` | open | executed: `---` under the sentence is silent in both readers; `:-` and `\|---\|` refuse; the error is in the safe direction |
| 🟢 | round 3's yellow 1 is closed — a vertical tab or form feed in the delimiter row and a header continuing a block quote are headers to the copy, and the plugin refuses them | `skills/evidence-check/scripts/evidence_check.py:3809` | confirmed | executed: 793 oracle-kept rows pass; the three vendored-writer rows pass; narrowing the block-quote class fails 20 cases and narrowing `\s` to `[ \t]` fails 12 |
| 🟢 | round 3's yellow 2 is closed — a pipe-less line over a delimiter row is a header to both readers, and the pact and template say so | `hooks/config.py:956` | confirmed | executed: putting the pipe condition back on a header line fails 45 cases; `evidence-check --strict` exit 0; read: C1, O1 and O3 state `UNDER_A_HEADER` |
| 🟢 | The predicate is complete over every axis the prompt named and more: escaped pipes, wider delimiter rows, header trailing spaces and backslashes, nested containers, list markers, a paragraph line above | `hooks/config.py:677` | confirmed | executed: 112,530 constructed configs, 36,424 rendered `always`, 0 misses in either reader; at 72b290c6, 7,087 and 7,408 |
| 🟢 | `UNDER_A_HEADER` refuses nothing that must stay silent: the template whole, this repository's config, setext headings, thematic breaks, YAML front matter | `hooks/config.py:677` | confirmed | executed: each silent in both readers; the two wider shapes (a no-break space before dashes, a two-cell delimiter under a one-cell line) refuse loudly and are not written here |
| 🟢 | The rendered-cell property holds over 60,000 random configs | `skills/evidence-check/scripts/evidence_check.py:3813` | confirmed | executed: 4,637 rendered `always`, 0 plugin and 0 copy misses; 10 and 10 at 72b290c6 |
| 🟢 | The setext exclusion is pinned and was seen red | `tests/test_a_signatory_declares_its_pact.py:715` | confirmed | executed: without the lookahead, exactly the new S4 case and S9 (b) fail |
| carried | rounds 1 to 3's confirmations: the #784 spellings, the must-not set, the walk-index mapping, the HTML shapes, the template rewrite, the survivors rows, round 2's yellow 2 and whites 3 and 4 | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried, not re-derived: round 3's fixes touch neither `PACT_WORD`, `HTML_CELL`, the walk nor the cell-file rule; the must-not set was re-run here anyway and is silent |
| ❓ | round 1's question: whether github.com's rendering of YAML front matter as a table is a spelling the rule owes a refusal | `docs/the-pact.md:91` | ❓ out of verified scope | carried from round 1; round 3's fixes leave front matter silent (executed: the closing `---` falls under the setext exclusion); github.com's rendering is not reachable from this round; the orchestrator answers it, as round 1 named |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_signatory_declares_its_pact.py -p no:xdist`, at the target | 2645 passed in 10.41 s |
| `bin/test` on the records module's vendored-writer S9 case, at the target | 31 passed |
| The module's import, timed and split | 2.74 to 2.81 s whole; `DELIMITERS` 2.43 s; 2,520 oracle renders 0.11 s; the padding tuple made once 0.041 s, the same set |
| A construction of 31 containers × 6 header styles × the delimiter rows (10 paddings, escaped pipes, a wider delimiter row) through cmark-gfm, against both readers, at the target and at 72b290c6's code | 112,530 configs, 36,424 rendered `always`; misses 0 and 0 at the target; 7,087 plugin and 7,408 copy at 72b290c6 |
| The breadth set, prose naming a pact over 16 underline shapes, plus setext in a list and a block quote, YAML front matter three ways, the template whole and filled, this repository's config, and CR and CRLF one-column tables | silent where cmark-gfm renders no table, except the two wider shapes named above; refused where it renders one; template filled reads `always` with the copy blind |
| 60,000 random configs over 53 fragment entries, seed 793, rendered through cmark-gfm, at the target and at 72b290c6's code | 4,637 rendered `always`; plugin 0 and copy 0 at the target; 10 and 10 at 72b290c6 |
| Five mutations of `UNDER_A_HEADER` and the header pipe condition in both readers, the pact module and the vendored-writer S9 case run under each | setext lookahead removed: 2 failed; block-quote class removed: 20; `\s` narrowed to `[ \t]`: 12; pipe condition kept on the header: 45; a pipe required in the delimiter row: 45 |
| The ⬜ 1 and ⬜ 2 patch, the module run under it, ruff check and format | 2646 passed; import 0.41 s; ruff clean |
| The ⬜ 2 case with the oracle filter emptied | 1 failed (the new case), 1852 passed |
| `evidence-check --strict`, at the target | exit 0 |
| The full suite, the repository-wide lint and the typecheck | not yet. That is the sealer's single run, and nothing in this round stands in for it |

## Paste-ready fixes

```diff
# ⬜ 1 and ⬜ 2 — optional, test-only. Applies with `git apply` at a3808f81.
# Executed: tests/test_a_signatory_declares_its_pact.py 2646 passed, import
# 0.41 s; ruff check and format clean. The new case fails alone when the
# oracle filter keeps nothing.
diff --git a/tests/test_a_signatory_declares_its_pact.py b/tests/test_a_signatory_declares_its_pact.py
--- a/tests/test_a_signatory_declares_its_pact.py
+++ b/tests/test_a_signatory_declares_its_pact.py
@@ -230,7 +230,18 @@ def refused(line, cell=False):
 # character Python calls whitespace that does not end a GFM line -- every
 # one, so cmark-gfm, not a list, says which a delimiter row may hold. The
 # plugin's GFM walker reads one as a delimiter row where `DELIMITER_ROW`
-# matches and a pipe stands in it.
+# matches and a pipe stands in it. The padding is one scan of the code
+# points, made once: written inside the comprehension, it is made again for
+# every outer combination, sixty scans and most of this module's import
+# (round 4 of PR #793).
+PADS = (
+    "",
+    *(
+        ch
+        for ch in map(chr, range(sys.maxunicode + 1))
+        if ch.isspace() and ch not in "\r\n"
+    ),
+)
 DELIMITERS = sorted(
     {
         left + "|".join([f"{pad}{cell}{pad}"] * cols) + right
@@ -238,14 +249,7 @@ DELIMITERS = sorted(
         for right in ("", "|")
         for cols in (1, 2, 3)
         for cell in ("-", "---", ":--", "--:", ":-:")
-        for pad in (
-            "",
-            *(
-                ch
-                for ch in map(chr, range(sys.maxunicode + 1))
-                if ch.isspace() and ch not in "\r\n"
-            ),
-        )
+        for pad in PADS
     }
 )
 WALKER_DELIMITERS = [
@@ -493,6 +497,26 @@ STRAY_WAYS = [
 ]
 
 
+def test_s2_cmark_gfm_renders_a_table_behind_every_container_that_takes_one():
+    """S2's oracle-kept rows are not an empty set. They are kept only where
+    cmark-gfm renders `always` under the header the row was built with, so
+    an edit to the construction that the oracle stops rendering would leave
+    S2 and S9 passing over nothing (round 4 of PR #793)."""
+    kept = [w[0] for w in STRAY_WAYS if w[0].startswith("a table cmark-gfm renders")]
+    for where in (
+        "at the margin",
+        "in a block quote",
+        "in a block quote with no space",
+        "continuing a block quote lazily",
+        "in a list item",
+        "three spaces in",
+    ):
+        shown = sum(
+            k.startswith(f"a table cmark-gfm renders, {where} over") for k in kept
+        )
+        assert shown > 20, (where, shown)
+
+
 @pytest.mark.parametrize(
     "text, lines, pacts", [w[1:] for w in STRAY_WAYS], ids=[w[0] for w in STRAY_WAYS]
 )
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — the module's import repeats a Unicode scan 60 times | not placed by this round; the filing ladder decides | the 0.18.2 run's orchestrator, who places it; the patch above is ready to apply as it stands |
| ⬜ 2 — the oracle-kept rows have no floor | not placed by this round; the filing ladder decides | the 0.18.2 run's orchestrator, who places it; the patch above is ready to apply as it stands |
| ⬜ 3 — the template's dashes-and-colons sentence overstates | not placed by this round; the filing ladder decides | the 0.18.2 run's orchestrator, who places it; the wording is in the ⬜ 3 section, and the S12 pin moves with it |

Needs a fix: no

Loses a record or crashes: no

## Proof block

These files were opened at a3808f81 in the clone, or read-only in the
repository under review:

- `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/rounds/round-3.md`
  and `round-3-report.md` (outline, summary, the widened property, run
  consequences, regression tests, ledger facts, the paste-ready patch,
  deferred, proof block); `round-1.md` and `round-2.md`, their verdict rows
- the fix-range diff `72b290c6..56558074` of `hooks/config.py`,
  `skills/evidence-check/scripts/evidence_check.py`, `templates/config.md`,
  `docs/the-pact.md`, `tests/test_a_signatory_declares_its_pact.py`,
  `tests/test_a_signatory_records_a_pact_change.py`, the ledger fragment
  and `overview.md`; the messages of the commits from 72b290c6 to a3808f81
- `hooks/config.py` lines 664-710 and 919-962, plus a search for
  `DELIMITER_ROW` (`names_a_pact`, `UNDER_A_HEADER`, `pact_lines_not_read`,
  `pact_declaration`'s docstring)
- `hooks/blocks.py` lines 372-377 (`gfm_lines`)
- `skills/evidence-check/scripts/evidence_check.py` lines 3744-3830
- `tests/gfm_table_oracle.py`, whole
- `tests/test_a_signatory_declares_its_pact.py` lines 188-262, 490-506 and
  812-870
- `tests/conftest.py` lines 543-547
- `docs/the-pact.md` lines 89-102 and 325-340
- `skills/evidence-check/SKILL.md` lines 334-345
- `templates/config.md` lines 425-440
- `bin/test`, and `.github/scripts/run_tests.py`, a search for `CMARKGFM`

The probe files, their logs, the trial patch and the clone were removed at
the end of the round.
