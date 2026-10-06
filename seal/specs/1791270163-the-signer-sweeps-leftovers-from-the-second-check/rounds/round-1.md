# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — review round 1

| Field | Value |
|---|---|
| Target SHA | 6978d861e4471139c84f5c37bb613d294bbc38a1 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #843 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `5bc0a48f59b605a96a083aa3fafd8a920ede62d6..149ef480cd6b50d75d9c5e65ab44b5635fa812b9`, 5 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1, a table or a footnote definition directly under the statement still stays exempt from the sweep. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the chain the owner chose on 2026-10-06 (`routing.md`, answered again as `automation` on the next machine). The reviewer was asked to judge spec compliance first against `spec.md`, `plan.md` and the four findings of `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/post-review-check-2.md` this item exists to close, then quality, over `origin/release/v0.20.0..6978d861`, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the three changed Python files and the two changed test modules (2671 passed). The orchestrator confirmed 🟡 1 by reading the span regex at `tests/test_one_word_one_meaning.py:737`: no alternative ends the span at a line starting `|` or `[^`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The widened span end misses two blocks cmark-gfm starts directly under a paragraph: a table (a line over a delimiter row) and a footnote definition; the old word in either stays exempt, against the §12 class `spec.md` §*Grounding* claims | `tests/test_one_word_one_meaning.py:737` | **fixed** `5ed7503e` | fixed at 5ed7503e; executed: cmark-gfm renders `<p>` then `<table>` for three table plants and closes the paragraph at a footnote definition; all four green through the span function at base and at HEAD; the fence turns them red, keeps the continuation line and the baseline green, and the module passes (21) |
| ⬜ 2 | R6's re-read row says the span ends at the end of the paragraph, and the changelog says the check sweeps whatever follows; both are one shape short while 🟡 1 stands | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | **fixed** `6365df4b` | fixed at 6365df4b; read, with 🟡 1's plants executed; a correction to the run's paperwork, not counted in `Needs a fix` |
| ⬜ 3 | The overview's Not verified table names the broad gate's and survivor-check's answerers from the first routing answer, which `routing.md` has since replaced | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24` | **fixed** `53649c22` | fixed at 53649c22; read against `routing.md`; a correction to the run's paperwork, not counted in `Needs a fix` |
| ⬜ 4 | No case pins the glued quote for a review record, which `spec.md` S2 states | `tests/test_a_signer_declares_its_pact.py:1257` | **fixed** `6ab8fedf` | fixed at 6ab8fedf; executed: `pact_reviews` quotes `\|Signatory\|Change\|Verdict\|` as written and reads the row under it; `grep` finds no case for it |
| ⬜ 5 | The `glued` list re-splits the text per glued row and tests `holds_old` per row inside the comprehension | `hooks/config.py:1350` | answered | a cleanup with no behaviour change, left out of the fix pass by the orchestrator so that the verifying round reads only the four fixes; the comprehension stays as it is; read; cleanup, no behaviour changes |
| 🟢 | the second check's ⬜ 1 is closed for the six blocks it named | `tests/test_one_word_one_meaning.py:737` | confirmed | executed: list item, block quote, fence, `***`, `div` and `---` plants green with the base module and red at HEAD; the continuation line green both times; the remainder is 🟡 1 |
| 🟢 | the second check's ⬜ 2 is closed — the filter's position is pinned | `tests/test_a_signer_declares_its_pact.py:1278` | confirmed | executed: the S4 case fails with the filter moved inside the `if holds_old and not any(…)` branch (the glued header returns as an entry), passes at HEAD |
| 🟢 | the second check's ⬜ 3 is closed — the glued line is quoted as written | `hooks/config.py:1369` | confirmed | executed: the S4 case fails with the base reader, with the quote rebuilt from the cells, and with the strip removed; `\|Signatory\|`, an indented line and CRLF text all quote as written through `pact_signers`; the four other pact modules 776 passed |
| 🟢 | the second check's ⬜ 4 is closed — R1 corrected and R6 and P8 re-read in this item's fragment | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:2` | confirmed | executed: all fifteen of R1's code coordinates carried, none extra; `bin/evidence-check --ledger` on the fragment with `--strict`, exit 0, 21 ok; read: no file under `seal/releases/` changes in the range; R6's wording is ⬜ 2 |

## Paste-ready fixes

```python
    end = re.search(
        r"\n[ \t]*\n"  # a blank line
        r"|\n {0,3}(?:#{1,6}[ \t\n]"  # an ATX heading
        r"|(?:[-*+]|1[.)])[ \t]"  # a list item that can interrupt a paragraph
        r"|>|`{3}|~{3}|<"  # a block quote, a fence, an HTML block
        r"|\[\^[^\]\n]+\]:"  # a footnote definition
        r"|(?:[-*_][ \t]*){3,}\n|=+[ \t]*\n|-+[ \t]*\n)"  # a break or an underline
        r"|\n(?=[^\n]*\n {0,3}(?=[^\n]*\|)[|:\- \t]*-[|:\- \t]*\n)"  # a table's header
        r"|<" + "!--",
        rest,
    )
```
```python
    # A pact review record's glued old header is quoted as written too (#831).
    rows, refusals, _ = config.pact_reviews(
        "# R\n\n| Signer | Change | Verdict |\n|---|---|---|\n| a | b | holds |\n"
        "|Signatory|Change|Verdict|\n"
    )
    assert rows == [(5, "a", "b", "holds")], rows
    assert refusals == [
        "holds a `|Signatory|Change|Verdict|` line inside its `| Signer | Change "
        "| Verdict |` table, the word before 0.19.0, which GFM reads as one of "
        "that table's rows — delete the line"
    ], refusals
```
```text
R6's Re-read row, grounds, appended once 🟡 1's fix lands: a table under the
statement (a header line over a delimiter row, with and without outer pipes)
and a footnote definition, each green before and red after.
changelog.md, second entry, the list of blocks: "A list item, a block quote,
a fenced block, an HTML block, a table, a footnote definition, a thematic
break or a setext underline".
overview.md, Not verified, the broad gate's answerer: the sealer, once after
the review rounds settle (routing.md, answered again under automation).
overview.md, Not verified, survivor-check: the sealer's run, over the fix
range the review rounds leave.
```

## Executed probes

| What was run | Result |
|---|---|
| cmark-gfm over eleven plants under a three-line paragraph | a table (three shapes) and a footnote definition end the paragraph; `2.`, a link reference definition, an inline tag, an autolink and a four-space line do not; `- ` alone makes a setext heading |
| the span function at base and at HEAD over nine plants under the statement | six blocks green at base, red at HEAD; continuation green both; table and footnote green both |
| 🟡 1's fence applied in the clone: twelve plants, the baseline, then `tests/test_one_word_one_meaning.py` | ten block plants red, continuation and setext pipe line green, baseline empty; exit 0, 21 passed; the file restored |
| the S4 case at HEAD and with four reader variants (base reader, filter moved inside the branch, quote unstripped, quote from cells) | exit 0, 1 passed; then exit 1 in each of the four |
| `pact_signers` over unspaced, indented and CRLF glued shapes, `pact_reviews` over two glued shapes | quotes as written; the review row under the glued line read |
| four modules at HEAD: `tests/test_pact_check.py`, `tests/test_a_pact_review_takes_a_pact_change.py`, `tests/test_one_table_walker_reads_what_gfm_renders.py`, `tests/test_a_signers_ci_prints_its_pact.py` | exit 0, 776 passed |
| `bin/evidence-check --ledger` on this item's fragment, `--strict` | exit 0; 21 ok · 0 drifted · 0 broken |
| R1's code coordinates, released row against the fragment's `Corrected · R1` row | 15 and 15; none missing, none extra |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this round ran none of it, and the sealer answers it after the rounds |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
