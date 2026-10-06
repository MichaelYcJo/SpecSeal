# Round 1 report — 1791270163-the-signer-sweeps-leftovers-from-the-second-check

| Field | Value |
|---|---|
| Target SHA | 6978d861 |
| Base | `origin/release/v0.20.0` at a9d7b0e5 (the merge base) |
| Range | a9d7b0e5..6978d861: nine commits, three code files (`hooks/config.py`, `tests/test_one_word_one_meaning.py`, `tests/test_a_signer_declares_its_pact.py`), one ledger fragment, the work item's records |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 6978d861 under `<scratchpad>/1791270163-…/round-1/clone`, run with the worktree's existing `.venv` interpreter; the clone, the probes and the logs were removed at hand-over |

## Summary

The four leftovers of `post-review-check-2.md` are closed as that check
described them, and every red the smith reports was reproduced here. One gap
remains in the class finding 1 exists to close:

- **🟡 1 — two GFM blocks still begin under the statement and stay exempt.**
  The widened span end lists the blocks that `spec.md` §*Scope* item 1 names.
  cmark-gfm also lets a **table** and a **footnote definition** begin
  directly under a paragraph's last line, and both stay exempt at 6978d861.
  `spec.md` §*Grounding* cites §12 for this exact class ("every block GFM lets
  begin directly under a paragraph's last line ends the span"). The
  docstring's "whatever follows it" and the changelog's "again sweeps whatever
  follows" are therefore still one shape short.
- **⬜ 2 — the R6 re-read row and the changelog fragment state 🟡 1's class as
  closed.** This is paperwork. Both read true once 🟡 1's fix lands.
- **⬜ 3 — `overview.md` §*Not verified* names answerers from the first
  routing answer.** The routing was answered again (`automation`), so the
  broad gate's answerer is now the sealer after the rounds. Paperwork.
- **⬜ 4 — no case pins the review record's as-written quote**, which
  `spec.md` S2 states. The code is right (executed). Only the pin is missing.
- **⬜ 5 — `glued` is built with a guard that belongs outside it**, and it
  splits the text again for every glued row. Cleanup only.

Nothing found here loses a record or crashes. Every shape still exits as it
did. 🟡 1 is a gap in a test sweep, not in `pact-check`.

## What the account claimed, and what was found

- **Claimed (phase 1, R6's grounds):** the six block plants are green before
  the change and red after it, and a lazy continuation line is green both
  times. Executed: the same plants run through `without_the_policy_span` from
  the base module (a9d7b0e5) and from HEAD give six green and six red, and the
  continuation line is green both times. Claim holds. The same probe also put
  a table and a footnote definition under the statement. Both are green at
  base and at HEAD (🟡 1).
- **Claimed (phase 2):** the S4 case was red against the reader before the
  fix, red with the filter moved back inside the branch, and red with
  `.strip()` removed. Executed, all three. The base reader fails on the
  `|Signatory|` shape. With the filter moved, the glued header returns as an
  entry beside the stray-row refusal. Without the strip, the indented shape is
  quoted with its indent. A fourth variant, the quote rebuilt from the cells as
  before, is also red. Claim holds.
- **Claimed (phase 2, overview):** six modules, 3447 passed. Executed: the
  four pact-reading modules the orchestrator did not run (`pact-check`,
  pact-review, table walker, signers' CI) gave 776 passed, exit 0.
  776 + 2671 (the orchestrator's two modules) = 3447. Claim holds.
- **Claimed (phase 3):** the `Corrected · R1` row carries all fifteen of R1's
  coordinates. Executed: a comparison of the code coordinates in
  `seal/releases/0.19.0.md` line 31 against the fragment's row gives 15 and
  15, none missing and none extra. `bin/evidence-check --ledger` on the
  fragment with `--strict` exits 0 (21 ok, 0 drifted, 0 broken). Claim holds.
- **Claimed (spec, data and interfaces):** `text.splitlines()[line - 1]` is
  the line `gfm_table` numbered. Read: `gfm_table` enumerates
  `unfenced(lines, text)` over `lines = text.splitlines()` and appends
  `(index + 1, found)`, and `unfenced` keeps each line's index. Executed with
  CRLF line endings: the quote is `|Signatory|`. Claim holds.
- **Claimed (spec, scope item 1):** the span ends "wherever GFM ends the
  statement's paragraph". It does not for a table or a footnote definition
  (🟡 1).

## Findings from execution

### 🟡 1 — a table or a footnote definition directly under the statement stays exempt

`tests/test_one_word_one_meaning.py:737`. The new pattern ends the span at
the blocks `spec.md` §*Scope* item 1 lists. cmark-gfm (the renderer
`tests/gfm_table_oracle.py` holds the walker to) closes a paragraph at two
more. Each was planted directly under the statement's `Enforced by:` line,
rendered, and run through the span function at HEAD:

| Plant | cmark-gfm renders | span at HEAD |
|---|---|---|
| `\| Signatory \|` then `\|---\|` | `<p>` (the statement) then `<table>` | green (exempt) |
| `Signatory` then `---\|` | `<p>` then `<table>` | green |
| `a \| signatory` then `--\|--` | `<p>` then `<table>` | green |
| a footnote definition saying the word | `<p>` ends; the definition is its own block | green |

This matters because this work item exists to close exactly this class. The
spec's grounding row cites §12 for it. The docstring says the exemption ends
"whatever follows it". R6's re-read dates "to the end of its paragraph" as
true, and the changelog tells users the check "again sweeps whatever follows".
A person who adds a table under the statement and writes the old word in its
header gets no red. That is the same quiet gap as the six shapes this item
fixed.

The fix adds two alternatives. A footnote definition is a marker at the start
of a line. A table is a line with a delimiter row under it, so the cut goes
before the header line, which GFM takes out of the paragraph. Executed in the
clone: all four plants turn red, the six earlier block plants stay red, and
the continuation line stays green. A pipe line under a `---` underline also
stays green, which is right because GFM makes it part of the statement's
setext heading. The baseline stays green, and the sweep module passes with the
fix (21 passed). No line of the statement is followed by a delimiter-shaped
line, so the baseline cannot move. The pattern does not check that cell
counts match, so it errs toward sweeping more, the same stance `spec.md`
§*Out* takes for the HTML-block end.

## Findings from reading

### ⬜ 2 — R6's re-read row and the changelog fragment state 🟡 1's class as closed

`seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3`
and `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/changelog.md:10`.
R6's row says "the cited row's claim holds", and that claim is "the span ends
at the end of its paragraph". The changelog's second entry says the check
"again sweeps whatever follows" the statement. Both are one shape short while
🟡 1 stands, and both become true once its fix lands. The R6 row's grounds
should then name the table and footnote plants beside the six it lists. This
is a correction to the run's paperwork, not counted in `Needs a fix`.

### ⬜ 3 — the overview's Not verified table names answerers from the first routing answer

`seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24`.
The broad-gate row says "this segment is routed `straight to the PR` and
`stop before the pull request`, and no sealer ran", and names "the session
that opens the pull request". The `survivor-check` row says "no review round
ran". `routing.md` now reads `through the review chain` and `open the pull
request` under `automation`. The sealer answers the broad gate after the
rounds, and this round is what gives `survivor-check` a fix range. The names
in that column are what a reader acts on. `spec.md` §*Out* and `plan.md`
§*What the smith does not do* carry the same first answer, but they are the
frame as it was written and can stand. Paperwork, not counted in
`Needs a fix`.

### ⬜ 4 — the review record's as-written quote is stated by S2 and pinned by nothing

`tests/test_a_signer_declares_its_pact.py:1257`. `spec.md` S2 says
"`pact_reviews` the same for `|Signatory|Change|Verdict|`". Its
*Verifiable how* names only the S4 case, which reads a pact. No test holds the
glued sentence for a review record, spaced or not (`grep "line inside its"`
over `tests/` finds the S4 case alone). Executed: `pact_reviews` quotes
`|Signatory|Change|Verdict|` as written and reads the row under it. The
behaviour is right, and the reader is shared, so this is a gap in a pin and
not a defect. A fence is under `## Paste-ready fixes`. It has not been seen
red, so it is **unverified**, and whoever takes it answers that.

### ⬜ 5 — the `glued` comprehension re-splits the text per row and carries the branch's guard inside it

`hooks/config.py:1350`. `holds_old` is tested once per row inside the
comprehension, though the list is only read when `holds_old` is true.
`text.splitlines()` is run again for every glued row, though `gfm_table` has
already split the same text. Glued rows are rare, so the cost is negligible.
The form simply reads as if `holds_old` could change between rows. A smaller
form computes the list under the `if holds_old:` the filter already sits in.
Cleanup, no fix commissioned. The smith may answer it with grounds.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The widened span end misses two blocks cmark-gfm starts directly under a paragraph: a table (a line over a delimiter row) and a footnote definition; the old word in either stays exempt, against the §12 class `spec.md` §*Grounding* claims | `tests/test_one_word_one_meaning.py:737` | open | executed: cmark-gfm renders `<p>` then `<table>` for three table plants and closes the paragraph at a footnote definition; all four green through the span function at base and at HEAD; the fence turns them red, keeps the continuation line and the baseline green, and the module passes (21) |
| ⬜ 2 | R6's re-read row says the span ends at the end of the paragraph, and the changelog says the check sweeps whatever follows; both are one shape short while 🟡 1 stands | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | open | read, with 🟡 1's plants executed; a correction to the run's paperwork, not counted in `Needs a fix` |
| ⬜ 3 | The overview's Not verified table names the broad gate's and survivor-check's answerers from the first routing answer, which `routing.md` has since replaced | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24` | open | read against `routing.md`; a correction to the run's paperwork, not counted in `Needs a fix` |
| ⬜ 4 | No case pins the glued quote for a review record, which `spec.md` S2 states | `tests/test_a_signer_declares_its_pact.py:1257` | open | executed: `pact_reviews` quotes `\|Signatory\|Change\|Verdict\|` as written and reads the row under it; `grep` finds no case for it |
| ⬜ 5 | The `glued` list re-splits the text per glued row and tests `holds_old` per row inside the comprehension | `hooks/config.py:1350` | open | read; cleanup, no behaviour changes |
| 🟢 | the second check's ⬜ 1 is closed for the six blocks it named | `tests/test_one_word_one_meaning.py:737` | confirmed | executed: list item, block quote, fence, `***`, `div` and `---` plants green with the base module and red at HEAD; the continuation line green both times; the remainder is 🟡 1 |
| 🟢 | the second check's ⬜ 2 is closed — the filter's position is pinned | `tests/test_a_signer_declares_its_pact.py:1278` | confirmed | executed: the S4 case fails with the filter moved inside the `if holds_old and not any(…)` branch (the glued header returns as an entry), passes at HEAD |
| 🟢 | the second check's ⬜ 3 is closed — the glued line is quoted as written | `hooks/config.py:1369` | confirmed | executed: the S4 case fails with the base reader, with the quote rebuilt from the cells, and with the strip removed; `\|Signatory\|`, an indented line and CRLF text all quote as written through `pact_signers`; the four other pact modules 776 passed |
| 🟢 | the second check's ⬜ 4 is closed — R1 corrected and R6 and P8 re-read in this item's fragment | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:2` | confirmed | executed: all fifteen of R1's code coordinates carried, none extra; `bin/evidence-check --ledger` on the fragment with `--strict`, exit 0, 21 ok; read: no file under `seal/releases/` changes in the range; R6's wording is ⬜ 2 |

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

## Regression tests to plant

- 🟡 1: no new case. The two sweep cases hold it. The four plants in its table
  are the ones to see red, as the six were in phase 1.
- ⬜ 4: the fence under `## Paste-ready fixes`, at the end of the S4 case in
  `tests/test_a_signer_declares_its_pact.py`. Unverified as a committed case.

## Facts for the evidence ledger

- R6's `Re-read ·` row, once 🟡 1's fix lands: the table plant (with and
  without outer pipes) and the footnote plant are green before the fix and
  red after it, in both sweep cases.

## Paste-ready fixes

### 🟡 1

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

It replaces the `end = re.search(...)` call in the span function. The two
new lines are the footnote alternative, inside the group, and the table
alternative, outside it. The table alternative cuts before the line that sits
over a delimiter row, because cmark-gfm takes that line out of the paragraph
as the table's header. Executed in the clone as described under 🟡 1.

### ⬜ 4

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

It goes at the end of the S4 case. The strings are the ones `pact_reviews`
returned in this round's probe. The case itself was not run and has not been
seen red.

### ⬜ 2 and ⬜ 3 (the run's paperwork)

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

Needs a fix: yes — 🟡 1, a table or a footnote definition directly under the
statement still stays exempt from the sweep.
Loses a record or crashes: no

## Proof block

Files opened: `hooks/config.py` (`gfm_table`, `_stops_at`, `read_table`,
`pact_signers`, `pact_reviews`, `_signer`, `renamed_header`, the head of
`unfenced`), `tests/test_one_word_one_meaning.py` (from `PACT_RENAMED`
through `test_no_live_text_says_the_word_0_19_0_renamed`), the base version
of the same module, `tests/test_a_signer_declares_its_pact.py` (`BOTH` and
the S4 case), `tests/test_a_pact_review_takes_a_pact_change.py` (the imports
and the S5 both-headers case), `tests/gfm_table_oracle.py` (head),
`bin/test`, `.github/scripts/run_tests.py` (the venv lines), `docs/the-pact.md`
(the statement under the `1791239490` fold marker), this item's `spec.md`,
`plan.md`, `questions.md`, `overview.md`, `handoff.md`, `routing.md`,
`changelog.md`, `phases/phase-1.md` to `phase-3.md`, the ledger fragment,
`seal/releases/0.19.0.md` lines 22, 31 and 36,
`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/post-review-check-2.md`,
and the range's diff and log.
