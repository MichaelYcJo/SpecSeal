# 1791128260-a-pact-row-is-read-in-one-plain-spelling — review round 4

| Field | Value |
|---|---|
| Target SHA | a3808f8197872f321690a22aa939348b7dfae879 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #793 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `b9aa4a14f65ae86e6dedbf7e5ccc80abd62d9012..b9aa4a14f65ae86e6dedbf7e5ccc80abd62d9012`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4 of the #759 redesign (PR #793), the verifying round after the round cap and the run's last, at a3808f81: open round 3's fixes (range 72b290c6..56558074) and judge whether each closes its finding with no regression — `UNDER_A_HEADER` shared by both readers with its setext exclusion, held to cmark-gfm on a constructed set; whether that construction's axes are complete; whether its breadth refuses anything that must stay silent; the rendered-cell fuzz; and the cost of rendering the oracle at import.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `DELIMITERS` re-scans all of Unicode for each of its 60 outer combinations, which is 2.43 s of the module's 2.76 s import, paid by every xdist worker; the oracle renders cost 0.11 s, so the cost is not the oracle's and need not move into the test bodies | `tests/test_a_signatory_declares_its_pact.py:241` | deferred #794 | #794 — Round 4 is the run's last; the import cost goes to #794 in milestone 54, closed by a post-review fix on this pull request; executed: hoisting the padding tuple gives the same 1,680 rows, the import drops to 0.41 s, and the module still passes 2646; no reader changes |
| ⬜ 2 | The oracle-kept `STRAY_WAYS` rows have no floor: emptied, S2 and S9 pass over nothing; round 3's `shown > 20` guard was not landed | `tests/test_a_signatory_declares_its_pact.py:490` | deferred #794 | #794 — The missing floor on the oracle-filtered rows goes to #794, closed by a post-review fix on this pull request; executed: with `rows_under` given a header no row has, the module passed 1852 with no failure; the proposed per-container floor fails alone there and passes at the target |
| ⬜ 3 | The template says a line of dashes and colons under a pact sentence refuses; a line of dashes alone does not, and `\|---\|` does without being named | `templates/config.md:436` | deferred #794 | #794 — The template sentence goes to #794, closed by a post-review fix on this pull request; executed: `---` under the sentence is silent in both readers; `:-` and `\|---\|` refuse; the error is in the safe direction |
| 🟢 | round 3's yellow 1 is closed — a vertical tab or form feed in the delimiter row and a header continuing a block quote are headers to the copy, and the plugin refuses them | `skills/evidence-check/scripts/evidence_check.py:3809` | confirmed | executed: 793 oracle-kept rows pass; the three vendored-writer rows pass; narrowing the block-quote class fails 20 cases and narrowing `\s` to `[ \t]` fails 12 |
| 🟢 | round 3's yellow 2 is closed — a pipe-less line over a delimiter row is a header to both readers, and the pact and template say so | `hooks/config.py:956` | confirmed | executed: putting the pipe condition back on a header line fails 45 cases; `evidence-check --strict` exit 0; read: C1, O1 and O3 state `UNDER_A_HEADER` |
| 🟢 | The predicate is complete over every axis the prompt named and more: escaped pipes, wider delimiter rows, header trailing spaces and backslashes, nested containers, list markers, a paragraph line above | `hooks/config.py:677` | confirmed | executed: 112,530 constructed configs, 36,424 rendered `always`, 0 misses in either reader; at 72b290c6, 7,087 and 7,408 |
| 🟢 | `UNDER_A_HEADER` refuses nothing that must stay silent: the template whole, this repository's config, setext headings, thematic breaks, YAML front matter | `hooks/config.py:677` | confirmed | executed: each silent in both readers; the two wider shapes (a no-break space before dashes, a two-cell delimiter under a one-cell line) refuse loudly and are not written here |
| 🟢 | The rendered-cell property holds over 60,000 random configs | `skills/evidence-check/scripts/evidence_check.py:3813` | confirmed | executed: 4,637 rendered `always`, 0 plugin and 0 copy misses; 10 and 10 at 72b290c6 |
| 🟢 | The setext exclusion is pinned and was seen red | `tests/test_a_signatory_declares_its_pact.py:715` | confirmed | executed: without the lookahead, exactly the new S4 case and S9 (b) fail |
| carried | rounds 1 to 3's confirmations: the #784 spellings, the must-not set, the walk-index mapping, the HTML shapes, the template rewrite, the survivors rows, round 2's yellow 2 and whites 3 and 4 | `tests/test_a_signatory_declares_its_pact.py` | confirmed | carried, not re-derived: round 3's fixes touch neither `PACT_WORD`, `HTML_CELL`, the walk nor the cell-file rule; the must-not set was re-run here anyway and is silent |
| ❓ | round 1's question: whether github.com's rendering of YAML front matter as a table is a spelling the rule owes a refusal | `docs/the-pact.md:91` | ❓ out of verified scope | carried from round 1; round 3's fixes leave front matter silent (executed: the closing `---` falls under the setext exclusion); github.com's rendering is not reachable from this round; the orchestrator answers it, as round 1 named |

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `templates/config.md:389` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/config.py:922` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3781` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/SKILL.md:339` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:5` | round 1's ⬜ 5 — answered |
| round-1 | `docs/the-pact.md:337` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_a_signatory_declares_its_pact.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:686` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3757` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:913` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-pact.md:91` | round 1's ❓ — out of verified scope |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3798` | round 2's 🟡 1 — fixed |
| round-2 | `templates/config.md:432` | round 2's 🟡 2 — fixed |
| round-2 | `docs/the-pact.md:347` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md:14` | round 2's ⬜ 4 — answered |
| round-2 | `hooks/config.py:666` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3761` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/survivors.md` | round 2's 🟢 — confirmed |
| round-3 | `skills/evidence-check/scripts/evidence_check.py:3808` | round 3's 🟡 1 — fixed |
| round-3 | `hooks/config.py:938` | round 3's 🟡 2 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — the module's import repeats a Unicode scan 60 times | not placed by this round; the filing ladder decides | the 0.18.2 run's orchestrator, who places it; the patch above is ready to apply as it stands |
| ⬜ 2 — the oracle-kept rows have no floor | not placed by this round; the filing ladder decides | the 0.18.2 run's orchestrator, who places it; the patch above is ready to apply as it stands |
| ⬜ 3 — the template's dashes-and-colons sentence overstates | not placed by this round; the filing ladder decides | the 0.18.2 run's orchestrator, who places it; the wording is in the ⬜ 3 section, and the S12 pin moves with it |
