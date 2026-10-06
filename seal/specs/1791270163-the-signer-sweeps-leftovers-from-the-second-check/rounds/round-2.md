# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — review round 2

| Field | Value |
|---|---|
| Target SHA | a374154b71abf8bcd1015fb753c92f4872543ba1 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #843 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `f649a21baf5158f82a2b9bd9896f2a864a53be7e..e3c9bc9d215b57c9474c7fff6e09a552d881515e`, 4 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | first — 🟡 1 at tests/test_one_word_one_meaning.py#without_the_policy_span, a unit round-1's fixes changed |
| Needs a fix | yes — 🟡 1, an ordered list item written `01.` or `001)` directly under the statement still stays exempt from the sweep. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round for round 1's fixes at `5bc0a48f..149ef480`. The reviewer was asked to open each fix and judge whether it closes its finding without opening a new one, inheriting round 1's verdicts, then anything else in `origin/release/v0.20.0..a374154b`, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the two changed test files and the two changed test modules (2671 passed). The orchestrator accepted 🟡 1 on CommonMark's rule that an ordered list interrupts a paragraph only when its start number is 1, which `01.` and `001)` are.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An ordered list item with leading zeros (`01.`, `001)`) directly under the statement starts at 1, so cmark-gfm ends the statement's paragraph there, but the span's list alternative accepts only a bare `1`, so the old word in it stays exempt | `tests/test_one_word_one_meaning.py:749` | **fixed** `1ffe9e75` | fixed at 1ffe9e75; executed: cmark-gfm renders `<p>` then `<ol>` for three leading-zero plants; all three green through the span function at 5bc0a48f and at HEAD; the fence turns them red, agrees with cmark-gfm on thirteen plants, keeps the baseline green, and the module passes (21) |
| ⬜ 2 | The overview says the fix pass's `survivor-check` run left no removed wording standing; three places stand, excused in `survivors.md` | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:26` | **fixed** `cdee5dfe` | fixed at cdee5dfe; executed: `survivor-check` over `5bc0a48f..149ef480` exits 1 with three standing places, and exits 0 with `--exempt`; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | round 1's yellow 1 is closed for the table and the footnote definition | `tests/test_one_word_one_meaning.py:753` | confirmed | executed: two table shapes, a delimiter row under the statement's last line and a footnote definition, each rendered outside the paragraph by cmark-gfm, green at 5bc0a48f and red at HEAD; continuation and baseline green; the leading-zero list item is this round's yellow 1 |
| 🟢 | round 1's white 2 is closed — R6's re-read row and the changelog name the table and the footnote definition | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | confirmed | read: the row's grounds and the changelog's list name both blocks; executed: the plants the row describes behave as it says; the fragment checks `--strict`, exit 0, 21 ok |
| 🟢 | round 1's white 3 is closed — the overview names the sealer and each fix pass | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24` | confirmed | read against `routing.md` and `agents/smith.md` §*Phases* item 3; the survivor sentence beside it is this round's white 2 |
| 🟢 | round 1's white 4 is closed — the review record's glued quote is pinned | `tests/test_a_signer_declares_its_pact.py:1292` | confirmed | executed: the S4 case passes at HEAD and fails with the quote rebuilt from the cells for a multi-cell header, a mutation only the new `pact_reviews` assertion can see |
| 🟢 | round 1's white 5 stays answered — the comprehension is unchanged | `hooks/config.py:1350` | confirmed | read: `hooks/config.py` is not in the fix range, so the answer's grounds stand as written |

## Paste-ready fixes

```python
        r"|(?:[-*+]|0{0,8}1[.)])[ \t]"  # a list item that can interrupt a paragraph
```
```text
overview.md, Not verified, the survivor-check row: "round 1's fix pass ran
it over its whole fix range from 5bc0a48f; three places still carry the
wording it removed, each excused in survivors.md, and it exits 0 with that
file as its exemption".
R6's Re-read row, grounds, appended once 🟡 1's fix lands: an ordered list
item starting at 1 with leading zeros (01., 001)) under the statement, green
in both sweep cases before and red after; 02. and a ten-digit marker, which
cmark-gfm keeps in the paragraph, green both times.
```

## Executed probes

| What was run | Result |
|---|---|
| cmark-gfm, plain and with footnotes, over eleven plants under the statement's last line; each also through the span function at 5bc0a48f and at HEAD | tables (outer pipes, two cells, a delimiter row directly under the statement) and the footnote definition outside the paragraph, green then red; `01.`, `001)` and the indented `01.` outside the paragraph, green both; `02.` and the continuation inside, green both; `1.` red both; a footnote label with a space stays in the paragraph and is swept at HEAD, which errs toward sweeping more; baseline green |
| the S4 case at HEAD, then with the glued quote rebuilt from the cells for a header of more than one cell | exit 0, 1 passed; then exit 1, 1 failed; `hooks/config.py` restored, clone clean |
| 🟡 1's fence applied in the clone: thirteen plants through cmark-gfm and the fenced span function, the baseline, then `tests/test_one_word_one_meaning.py` | all thirteen agree with cmark-gfm; baseline green; exit 0, 21 passed; the file restored, clone clean |
| `bin/evidence-check --ledger` on this item's fragment, `--strict` | exit 0; 21 ok · 0 drifted · 0 broken |
| `bin/survivor-check --range 5bc0a48f..149ef480`, with and without `--exempt` pointing at `survivors.md` | exit 1, three standing places, without it; exit 0, all three excused, with it |
| `bin/round-record new` over this report, in a second scratch clone, then the clone removed | the record written with all seven verdict rows, both fences and both fields; `Fix of a fix` reads `first`, keyed on `without_the_policy_span`; its chain-check exits 2 only because the clone carries no `origin/release/v0.20.0` |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this round ran none of it, and the sealer answers it once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_one_word_one_meaning.py:737` | round 1's 🟡 1 — fixed |
| round-1 | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | round 1's ⬜ 2 — fixed |
| round-1 | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24` | round 1's ⬜ 3 — fixed |
| round-1 | `tests/test_a_signer_declares_its_pact.py:1257` | round 1's ⬜ 4 — fixed |
| round-1 | `hooks/config.py:1350` | round 1's ⬜ 5 — answered |
| round-1 | `tests/test_a_signer_declares_its_pact.py:1278` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:1369` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:2` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
