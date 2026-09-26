# 1790381329-the-deferred-sentences-and-pins — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | ae66911f |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#615. Re-count the anchored ledger rows carrying no id `ROW_ID` reads
(questions.md Q1), then the round's three paste-ready texts with the measured
figure: `survivor_check.py`'s module docstring, `removed_ledger_rows`' last
docstring paragraph, and `docs/review-chain-spec.md`'s sentence after *every
anchor it kept.* Enumerate the silent-set statement by meaning first. Plant
`test_a_claim_split_into_two_rows_as_it_is_corrected_stays_measured`, seen
red with `>=` changed to `==`.

## What this phase found

- **Q1: 289 of 833 anchored live rows (34.7%)**, counted at `a31ad5bf` by a
  one-shot probe (`test_tmp_row_ids.py` in the session's scratch directory,
  run once and deleted) that loaded `ROW_ID` from `survivor_check` and
  `ANCHOR_RE` and `live_lines` through `survivor_check`'s own `evidence()`
  and `reader()`, over `seal/ledger.md`, `seal/releases/*.md` and
  `seal/ledger/*.md`. The round had 280 of 800 at its tip; the 33 more rows
  are within 0.15.4's fold (32 anchored rows in `seal/releases/0.15.4.md`)
  plus this work item's fragment (3). The statements say *about 35%*, and
  `removed_ledger_rows` gives *289 of the 833*.
- **The class was wider than the silent set: the count guard's direction
  was stated four more times as *as many rows*.** `>=` is what the new case
  pins, and *as many* reads as equality, the mutation that case exists to
  kill. So the `ROW_ID` comment, the module docstring's id sentence,
  `removed_ledger_rows`' id paragraph, the inline comment above the guard,
  and the docstring of `test_a_removed_row_sharing_one_live_anchor_with_another_row_takes_the_exit`
  now say *at least as many*. The `ROW_ID` comment adds why: a correction
  may split a row, never merge two away.
- **The enumeration and its judgments.** Searched over `docs/ skills/
  agents/ templates/ hooks/ .github/ README.md README.ko.md CONTRIBUTING.md`
  and the survivor tests: *goes silent*, *stays silent*, *silent when*,
  *silent only*, *four shapes*, *about 35%*/*37%*, *298*, *280 of*, *falls
  back to its anchors*, *the id does not name*, *lost a sibling*, *id-like*,
  *as many rows*, *id stands*, *corrected in place*, *removed ledger row*,
  Korean *조용*, *침묵*. Beyond the three statements and the four *as many*
  places: the hooks' and gates' *stays silent* (a gate printing nothing),
  `broad_gate.py:824` and three test files' *four shapes* (other shapes),
  `tests/test_a_corrected_sentence_survives_elsewhere.py:3108,3148` (the
  floor's silence), `tests/test_settle_reads_before_it_removes.py:1438`
  (README section row counts), and the Korean hits (unrelated). None is a
  twin. `seal/specs/1790297084-*/` was read and not rewritten.
- **The paste-ready texts applied with the figure replaced**; the module
  docstring's re-wrapped id sentence keeps under 80 columns.
- **Seen red (§15).** The new case passes with the guard as built, because
  it pins shipped behaviour; with `named[path][key] >= held[key]` changed to
  `==` it failed (exit 0, no place), and the file was restored from a copy
  kept before the mutation.
- **One 0.15.4 row drifted**, P3 (`removed_ledger_rows` and the neighbour
  case), re-read with a dated note; its claim already said an id carried
  fewer times names no row, so it holds. C4 in this work item's fragment
  carries the direction and the figure.
- **Verified by (executed, 2026-09-26):** `tests/test_a_corrected_sentence_survives_elsewhere.py`
  whole and `tests/test_docs_line_wrap.py`, 184 passed. `evidence-check .`:
  0 drifted, 0 broken, 0 records refused.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *four shapes* list in `removed_ledger_rows`' docstring, which missed S4 and called S1–S3 and S5 silent | the paragraph stating both conditions together |
| *about 37%* and *298 of about 800* | *about 35%* and *289 of the 833*, measured at `a31ad5bf` |
