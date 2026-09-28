# 1790635412-an-overflow-cell-is-refused-in-every-repository — review round 1

| Field | Value |
|---|---|
| Target SHA | 6670eb6fee85ec8368e3bb8ad786d0af610ce2c2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #659 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `6bf504c3e9181791c45598b64a227dd0d55ff4ad..0659e395510378c72c7c63485bc56223456c3797`, 2 commits |
| Contract changes | none |
| New units | GFM_LINE_RE (depth 1); gfm_lines (depth 1); NOT_A_LINE_END (depth 1); test_a_character_gfm_does_not_end_a_line_at_does_not_cut_a_row (depth 1); test_a_character_gfm_does_not_end_a_line_at_does_not_open_a_fence (depth 1); test_an_old_coordinate_after_such_a_character_is_still_offered (depth 1); test_migrate_reads_the_fence_where_gfm_reads_it (depth 1); test_a_record_line_after_such_a_fence_run_is_read (depth 1) |
| Needs a fix | yes — 🟡 1, the walk splits lines where GFM does not, so a split row can go unnamed and later rows are reported one line off |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first finding round, over the whole branch `551c7967...6670eb6f`. Asked to review the shipped `OVERFLOW` arm against the frame and the owner's pre-edit answer (ship it), with the contract of `LEDGER_COLUMNS` and `ledger_table_rows` named as a surface worth attention, because work item C builds on it after this squashes.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `ledger_table_rows` splits lines with `str.splitlines`, which ends a line where GFM does not: a split row with U+2028, NEL or a form feed after the stray pipe is not named, and every row after such a character is reported one line off and as having no header | `skills/evidence-check/scripts/evidence_check.py:1714` | **fixed** `17e8f667` | fixed at 17e8f667 — with the rows it drifted re-read in `0659e395`. The class was fixed across every table or fence walk in `evidence_check.py` (`unquoted`, `old_format_rows`, `ledger_table_rows`, `migrate`, the records arm); the `splitlines` calls feeding `content_hash` stay, since changing them moves every hash; Executed at `6670eb6f`: three shapes each returned `[]` where the removed implementation counted six cells; a real split on editor line 4 was reported as `line 5`, "no header above it". Breaks `spec.md`'s "1-based, into the text as given" promise to work item C |
| ⬜ 2 | A stray pipe in the Clause cell draws `OVERFLOW` and also `MALFORMED` "cites no coordinate", whose remedy is wrong for that row | `skills/evidence-check/scripts/evidence_check.py:1798` | answered | The one-line fix changes `MALFORMED`'s reading, which `spec.md` In 2 and A7 hold unchanged, and would drop a true `MALFORMED` where the split is in the Notes cell. It predates the branch; `OVERFLOW` now prints the right remedy beside it, and escaping the pipe clears both; Executed. Pre-existing for `MALFORMED`; the branch adds the correct verdict beside it, so nothing ships worse |
| ⬜ 3 | A row with no leading `\|`, which GFM keeps in the table, resets the walk's header, so later rows of a table wider than five columns are named `OVERFLOW` with "no header above it" | `skills/evidence-check/scripts/evidence_check.py:1722` | answered | The reset comes from the shared reader's `split_row`, which the arm asks through `cell_rule()` and the spec keeps the arm off rewriting. The misreading is loud, predates the branch for `MALFORMED`, and no ledger this plugin writes has such a row; Executed. Shared `split_row` rule, and pre-existing for `MALFORMED`; no ledger this plugin writes has such a row |
| 🟢 | The three interface names, the totals key, both summary lines and the `check_ledger` extension match `spec.md` *Data & interfaces* | `skills/evidence-check/scripts/evidence_check.py:1609` | confirmed | Read; the new module and the lenient-notice module executed green. The line-number clause is 🟡 1 |
| 🟢 | `--reverify` names an overflowing row, exits 1, and still rewrites the row's hashes, as the new verdict row states | `skills/evidence-check/scripts/evidence_check.py:2089` | confirmed | Executed: a placeholder hash in a split fragment row was rewritten and the row got its `LEFT` line |
| 🟢 | The ledger stays true: C2 and L1 removed and rewritten in the fragment, drifted rows re-read, two corrected claims now true | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 0 drifted and 0 overflow; `correction-check` over the branch exit 0. Read: both `Corrected 2026-09-29` notes against `LENIENT_NOTICE` |
| 🟢 | Both READMEs' command rows and the escaped pipes in `SKILL.md`'s new cells say what the code does | `README.md:270` | confirmed | Read, by GFM's table rule; not rendered |

## Paste-ready fixes

```python
RULE_CELL_RE = re.compile(r"^:?-+:?$")
# Where GFM ends a line: LF, CR or CRLF, and nowhere else. `str.splitlines`
# also ends one at U+2028, NEL, a form feed and five other characters, which
# cuts a row in two -- hiding a split that falls after the cut -- and moves
# every line number after it off the line an editor shows.
GFM_LINE_END_RE = re.compile(r"\r\n|\r|\n")
```
```python
    split = cell_rule()
    rows = [split(line) for line in GFM_LINE_END_RE.split(unquoted(text))]
```
```python
    for line in GFM_LINE_END_RE.split(unquoted(text)):
```
```python
@pytest.mark.parametrize("ch", ["
", "\x85", "\x0c"])
def test_a_character_gfm_does_not_end_a_line_at_does_not_cut_a_row(ch):
    """GFM ends a line at LF, CR and CRLF only; `str.splitlines` also ends
    one at these. Cut there, a split after the cut went unnamed and every
    later row was one line off and read as under no header."""
    c = "x.py#f@00000000"
    hidden = f"| a | `{c}` | ran `a | b` more{ch}text | 2026-01-01 | n |\n"
    assert lines(HEADER + hidden) == [3]
    before = f"| a | `{c}` | b{ch}c | 2026-01-01 | n |\n"
    text = HEADER + before + SPLIT.format(c=c)
    assert lines(text) == [4]
    assert "under a 5-cell header" in named(text)[0][1]
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the new module, the lenient-notice module, the fold module, the two new or changed `test_dispatch.py` cases and the two `test_release_hygiene.py` cases | exit 0, 114 passed |
| `bin/test` over `test_a_folded_statement_names_what_enforces_it.py`, `test_a_document_has_room_for_the_next_fold.py`, `test_one_word_one_meaning.py`, `test_a_row_points_by_content.py`, `test_evidence_check.py`, `test_no_real_identifiers.py` | exit 0, 289 passed |
| `bin/evidence-check .` in the clone at `6670eb6f` | exit 0; total `2661 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow`; records arm 0 refused |
| `bin/correction-check --range 551c7967...6670eb6f` | exit 0, no merge commit in range |
| probe file test_tmp_overflow.py (deleted): `overflow_rows` and `malformed_rows` over U+2028, NEL, form feed and FS shapes, a Clause-cell pipe, a row with no leading pipe in a seven-column table, a comment line inside it, a trailing empty cell, CRLF, adjacent tables | 🟡 1, ⬜ 2 and ⬜ 3 as described; CRLF counted exactly; adjacent tables keep their own headers |
| `--reverify` over a one-row fragment whose split row holds `@00000000` | the hash was rewritten, a `LEFT … OVERFLOW` line printed, exit 1 |
| 🟡 1's fix applied in the clone, then the proposed case (test_tmp_gfm.py, deleted) and three modules | case 3 passed; new module, `test_a_row_points_by_content.py` and `test_evidence_check.py` 228 passed |
| the same case after reverting the fix | 3 failed, so the case is red against `6670eb6f` |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet run by anyone; `unverified`, answered by the sealer after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `unquoted` finds fences on `str.splitlines` lines, so a U+2028 before a fence run can open or close a fence GFM never sees | work item B (#584), which owns fence reading this milestone | the orchestrator of milestone 49, by adding it to B's handoff; B's smith decides |
| `old_format_rows` reads rows on `str.splitlines` lines, so an old coordinate after such a character is not offered for migration | this branch, if the smith takes 🟡 1's constant into it (the fix block says how); otherwise a new issue | the smith of this work item, at the fix pass |
