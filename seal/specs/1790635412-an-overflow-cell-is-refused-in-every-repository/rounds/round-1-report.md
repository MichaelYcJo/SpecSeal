# Round 1 report — 1790635412-an-overflow-cell-is-refused-in-every-repository

Reviewer: warden. Target: `feat/585-an-overflow-cell-is-refused-in-every-repository`
at `6670eb6f`, against `release/v0.16.0` at `551c7967`, the whole branch.
Read and run in a `git clone --no-local` at the target SHA, never in the
orchestrator's tree. No earlier round exists, so nothing was carried.

## What this round found, in one view

The branch does what the spec says. The verdict, its grading, the notice,
`--reverify`, the advisor and every page that states the grading agree with
`exit_code`, and this repository's ledgers stay true. One defect sits in the
new walk that everything else reads through:

```
ledger_table_rows splits lines where GFM does not            (🟡 1)
  ├─ a split row can go unnamed                   (false negative, a regression
  │                                                against the removed case)
  ├─ every later row is reported one line off     (the coordinate is the verdict's
  │                                                only pointer)
  └─ work item C is promised "1-based, into the text as given", which is not true
```

Two ⬜ observations follow from the same walk and are pre-existing in the
`MALFORMED` arm. They are recorded so the next reader of this surface knows
they are there, and nothing needs to change for them.

## Spec compliance

Every acceptance row A1 to A15 was checked against the code rather than the
phase records. The executed ones are in the probes table below; the read ones
are said to be read.

- **The three interface names match `spec.md` *Data & interfaces*.**
  `LEDGER_COLUMNS` is the template's five header cells, `ledger_table_rows`
  yields `(line_number, header, cells)` with `header` None under no header,
  and `overflow_rows` returns the `(status, coord, detail)` shape. Read at
  `skills/evidence-check/scripts/evidence_check.py:1609`, `:1698` and `:1832`.
  The one clause that does not hold is the line-number promise (🟡 1).
- **`grounds_cells` keeps its yield.** Read: the old `column = 1` fallback is
  now `LEDGER_COLUMNS.index(CODE_GROUNDS)`, which is 1, and the header reset
  sits on the same non-row lines as before. Executed: the two `MALFORMED`
  modules are green at the tip.
- **The grading is `MALFORMED`'s everywhere it is stated.** `exit_code` puts
  `OVERFLOW` in the exit-1 branch below `BROKEN` (`:2892`), the notice names
  it, and the flag row, reader table, verdict row, `evidence-ci` step 4, the
  vendored template comment and the CI warning all say exit 1 lenient and
  exit 2 strict. The lenient-notice module holds each against `exit_code`, and
  it is green.
- **`--reverify` does what the verdict row claims.** The claim that the row's
  hashes are still rewritten had no case behind it, so it was probed: a
  placeholder hash in an overflowing fragment row was rewritten to the
  anchor's hash, the row got its `LEFT` line naming the ledger and line, and
  the run exited 1.
- **The advisor names the row with its ledger.** Read at
  `hooks/evidence-advisor.py:148`; the A10 case in `tests/test_dispatch.py` is
  green. Its Windows leg is CI's, as `overview.md` already says.
- **The ledger stays true.** `bin/evidence-check .` over the clone exited 0 with
  `0 drifted · 0 broken · 0 malformed · 0 overflow` on the total line and 0
  refused in the records arm. `correction-check` over the branch exited 0.
  C2 and L1 are gone from `seal/releases/0.15.1.md` and `seal/releases/0.15.3.md`
  and stand in this work item's fragment. I read the two `Corrected
  2026-09-29` notes (in `seal/releases/0.11.3.md` and
  `seal/releases/0.15.5.md`, the notice-quoting row and S4), and each corrected claim now matches `LENIENT_NOTICE` and the case that
  loops over three verdict words.
- **The README rows and the escaped pipes are right, by reading.** Both
  READMEs' `evidence-check` rows state what the code does. In a GFM table the
  table rule unescapes `\|` before inline parsing, so `` `\|` `` renders as a
  pipe and `` `\\|` `` as a backslash and a pipe, which is what the verdict row
  and reader-table cell mean. Read, not rendered.

## A split row is missed when a line separator GFM ignores follows the pipe (🟡 1)

`ledger_table_rows` builds its rows with `unquoted(text).splitlines()`
(`skills/evidence-check/scripts/evidence_check.py:1714`). Python's
`str.splitlines` ends a line at LF, CR and CRLF, and also at U+2028, U+2029,
NEL (U+0085), form feed, vertical tab and three separator controls. GFM ends
a line at LF, CR and CRLF only, so GitHub renders such a row as one row.

Two effects follow, and both were executed against the tip:

- **A split row goes unnamed.** With the stray `|` before a U+2028, NEL or form
  feed in the same row, the walk sees a short first half and a second half that
  is not a row. `overflow_rows` returns nothing. The removed implementation in
  `tests/test_release_hygiene.py` split on `\n` and counted the same row as six
  cells, so for this input the branch softens this repository's own pull-request
  check as well as shipping the gap.
- **Every row after such a character is one line off, and misdescribed.** A
  U+2028 inside any earlier cell moves a real split on editor line 4 to
  `line 5`, and because the cut row breaks the table, the detail says "no header
  above it" for a row that sits under a 5-cell header. The line is the verdict's
  only coordinate, so the person is sent to the wrong row.

This matters beyond the verdict because `spec.md` states the walk's contract for
work item C as "Line numbers are 1-based, into the text as given", and C is
about to build on it. The characters are rare in a ledger. They do arrive by
paste, and the cost of the rare case is a silent pass.

The fix is at the walk, so `MALFORMED` (which reads the same walk and had the
same split before this branch) is corrected by the same edit. With it applied in
the clone, the proposed case passed and the three modules that drive both arms
stayed green (228 passed). Reverted, the proposed case failed on all three
characters. The class (§12): `old_format_rows` (`:1563`) splits rows the same
way and is outside this diff; the fence reading in `unquoted` (`:275`) does too,
and fence reading is work item B's. Both are listed under *Deferred*, and the
fix block notes that the first can take the same constant in this branch.

## One stray pipe in the first cell draws two verdicts with opposite remedies (⬜ 2)

A pipe in the Clause cell shifts the coordinate one column right. The row is
named `OVERFLOW`, correctly, and also `MALFORMED` with "cites no coordinate …
write `path#anchor@hash` in the Code grounds cell", which is not true of the
row: it cites one, one column over. Executed, with and without a header.

This was already the case before the branch (the `MALFORMED` line alone), so
the branch improves it by adding the right remedy beside it. The advisor prints
both blocks on the commit. Nothing ships wrong that did not before. If the smith
wants it tidy, `grounds_cells` could skip a row wider than its header, since
`OVERFLOW` already fails that row at the same grade. Location:
`skills/evidence-check/scripts/evidence_check.py:1798`.

## A row GFM keeps in a wide table breaks the walk's table (⬜ 3)

`split_row` requires a leading `|`. GFM does not, so a row written without one
stays in the table on GitHub, but the walk treats it as a non-row line and
resets `header` (`:1722`). In a ledger file holding a seven-column table, every
row after such a line is then counted against five columns and named `OVERFLOW`
with "no header above it". Executed. The same reset already sent `grounds_cells`
to column 1 there, so `MALFORMED` misfired on it before this branch.

Every ledger this plugin writes starts each row with `|`, so this is a limit of
the shared row rule rather than a defect of the arm. A line in `SKILL.md`'s
*Known limits* would make it findable, and it is the smith's call whether to
add one.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `ledger_table_rows` splits lines with `str.splitlines`, which ends a line where GFM does not: a split row with U+2028, NEL or a form feed after the stray pipe is not named, and every row after such a character is reported one line off and as having no header | `skills/evidence-check/scripts/evidence_check.py:1714` | open | Executed at `6670eb6f`: three shapes each returned `[]` where the removed implementation counted six cells; a real split on editor line 4 was reported as `line 5`, "no header above it". Breaks `spec.md`'s "1-based, into the text as given" promise to work item C |
| ⬜ 2 | A stray pipe in the Clause cell draws `OVERFLOW` and also `MALFORMED` "cites no coordinate", whose remedy is wrong for that row | `skills/evidence-check/scripts/evidence_check.py:1798` | open | Executed. Pre-existing for `MALFORMED`; the branch adds the correct verdict beside it, so nothing ships worse |
| ⬜ 3 | A row with no leading `\|`, which GFM keeps in the table, resets the walk's header, so later rows of a table wider than five columns are named `OVERFLOW` with "no header above it" | `skills/evidence-check/scripts/evidence_check.py:1722` | open | Executed. Shared `split_row` rule, and pre-existing for `MALFORMED`; no ledger this plugin writes has such a row |
| 🟢 | The three interface names, the totals key, both summary lines and the `check_ledger` extension match `spec.md` *Data & interfaces* | `skills/evidence-check/scripts/evidence_check.py:1609` | confirmed | Read; the new module and the lenient-notice module executed green. The line-number clause is 🟡 1 |
| 🟢 | `--reverify` names an overflowing row, exits 1, and still rewrites the row's hashes, as the new verdict row states | `skills/evidence-check/scripts/evidence_check.py:2089` | confirmed | Executed: a placeholder hash in a split fragment row was rewritten and the row got its `LEFT` line |
| 🟢 | The ledger stays true: C2 and L1 removed and rewritten in the fragment, drifted rows re-read, two corrected claims now true | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 0 drifted and 0 overflow; `correction-check` over the branch exit 0. Read: both `Corrected 2026-09-29` notes against `LENIENT_NOTICE` |
| 🟢 | Both READMEs' command rows and the escaped pipes in `SKILL.md`'s new cells say what the code does | `README.md:270` | confirmed | Read, by GFM's table rule; not rendered |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `unquoted` finds fences on `str.splitlines` lines, so a U+2028 before a fence run can open or close a fence GFM never sees | work item B (#584), which owns fence reading this milestone | the orchestrator of milestone 49, by adding it to B's handoff; B's smith decides |
| `old_format_rows` reads rows on `str.splitlines` lines, so an old coordinate after such a character is not offered for migration | this branch, if the smith takes 🟡 1's constant into it (the fix block says how); otherwise a new issue | the smith of this work item, at the fix pass |

## Paste-ready fixes

### 🟡 1 — split on GFM's line endings in the walk

In `skills/evidence-check/scripts/evidence_check.py`, beside `RULE_CELL_RE`:

```python
RULE_CELL_RE = re.compile(r"^:?-+:?$")
# Where GFM ends a line: LF, CR or CRLF, and nowhere else. `str.splitlines`
# also ends one at U+2028, NEL, a form feed and five other characters, which
# cuts a row in two -- hiding a split that falls after the cut -- and moves
# every line number after it off the line an editor shows.
GFM_LINE_END_RE = re.compile(r"\r\n|\r|\n")
```

and in `ledger_table_rows`:

```python
    split = cell_rule()
    rows = [split(line) for line in GFM_LINE_END_RE.split(unquoted(text))]
```

The same class in `old_format_rows` (`:1563`), if taken here:

```python
    for line in GFM_LINE_END_RE.split(unquoted(text)):
```

The case, for `tests/test_a_row_wider_than_its_header_is_named.py` beside the
A3 cases. It uses that module's `HEADER`, `SPLIT` and `named`/`lines`
helpers, and was seen red against `6670eb6f` (3 failed) and green with the fix:

```python
@pytest.mark.parametrize("ch", [" ", "\x85", "\x0c"])
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

## Regression tests to plant

- `tests/test_a_row_wider_than_its_header_is_named.py`: the case in the fence
  above, for 🟡 1.

## Facts for the evidence ledger

- Once 🟡 1 is fixed, row O2's claim can add that the walk splits on GFM's
  line endings only, anchored at `ledger_table_rows` and the new case.
- Row O4's claim that the row's hashes are still rewritten had no case under
  it. It was executed in this round (see the probes table). A case in the new
  module with a placeholder hash in a split row would pin it.

Needs a fix: yes — 🟡 1, the walk splits lines where GFM does not, so a split row can go unnamed and later rows are reported one line off
Loses a record or crashes: no

The broad gate has not run. Once 🟡 1's fix is verified and a round leaves
nothing open, the sealer's spawn comes due.

## Proof block

Files opened in the clone at `6670eb6f`:
`skills/evidence-check/scripts/evidence_check.py` (lines 150–300, 1094–1140,
1340–1375, 1556–1580, 1590–1860, 2066–2225, 2835–3080),
`hooks/evidence-advisor.py` (diff), `skills/verify/scripts/unverified_check.py`
(140–215), `skills/verify/scripts/broad_gate.py` (225–240, 2030–2080),
`tests/test_a_row_wider_than_its_header_is_named.py`,
`tests/test_release_hygiene.py`, `tests/test_dispatch.py`,
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` and
`tests/test_the_ledger_fragments_fold_at_release.py` (diffs),
`skills/evidence-check/SKILL.md`, `skills/evidence-ci/SKILL.md`,
`templates/evidence-check.yml`, `.github/workflows/test.yml`, `README.md`,
`README.ko.md`, `docs/the-evidence-ledger.md` (diffs), `seal/releases/*.md`
(diff), `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md`,
and this work item's `spec.md`, `overview.md`, `questions.md`, `routing.md`,
`changelog.md`. `bin/evidence-check`, `bin/test`.
