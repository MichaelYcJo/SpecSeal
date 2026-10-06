# Round 3 report — 1791239490-a-repository-that-keeps-a-pact-is-a-signer

| Field | Value |
|---|---|
| Target SHA | cfd823ba8bee4bf61254d554be701878d2b25edc |
| Base | `origin/release/v0.19.0` |
| Pull request | #827 (draft) |
| Round kind | verifying, and the run's last — round 2's fix range `b1f18af7..96832724` |
| Ran by | specseal:warden on claude-opus-5-5 |

HEAD did not move during the review: `cfd823ba` at spawn and at hand-over.

## Summary

Round 2's six findings are closed as recorded. The fix for white 5 names an
old header once when a blank line stands above it, in every spelling the
walker can parse. The policy span now ends at any ATX heading. The
compatibility modules are swept for a lowercase spelling. The review
case's docstring, the `pact-check` S4 commit message, the `Enforced by:`
line and ledger rows R1, P8, R5 and P11 say what the code does.
`evidence-check` reads the fragment at 432 ok.

Three of the closures leave part of their class behind. None of the gaps
ships a defect, so all five findings below are ⬜:

1. White 5's class, one shape further on (⬜ 11). With no blank line
   above it, GFM reads the old header as a row of the `Signer` table. The
   reader then names that one line twice: once as an entry that is not a
   remote URL, and once as the old header. The orchestrator measured this
   shape. This round reproduced it for a pact, end to end, and for a pact
   review record at the reader.
2. White 7's class, one spelling further on (⬜ 12). `PACT_HEADER_WORD` is
   case-sensitive, so `SIGNATORY` and `SIGNATORIES` in a compatibility
   module stay green. Its comment says every other spelling is swept.
3. White 6's class, one heading form further on (⬜ 13). A setext heading
   after the policy statement does not end the span.
4. Two records describe the old reach (⬜ 14, ⬜ 15). These are paperwork:
   `overview.md`'s S4 row, and R6's "the capitalised header cell".

Each fix below was applied in the scratch clone. With all of them applied,
the six pact modules ran green, and each new assertion or plant was seen
red without its fix.

## Findings from execution

### ⬜ 11 — an old header glued under the `Signer` table is named twice

`hooks/config.py:1346`. Round 2's fix compares the walk's refusals by the
cells they quote. That reaches every shape where the walk's stray-row
refusal is what names the old header. It does not reach the shape where
there is no blank line between the `Signer` table and `|Signatory|`. There
the walk reads the old header as one of the table's rows. GFM does the same.

In that shape `pact_signers` runs `remote_entries` over the row and refuses
`Signatory` as an entry that is not a remote URL. `read_table` also adds
its "also holds a `| Signatory |` header" sentence, so one line gets two
REFUSED lines. With the old delimiter row under it, a third line refuses
`|---|` as a delimiter row out of place. That line is correct. It is what
says the rows under it go unread.

For a pact review record (`pact_reviews`), the glued header comes back as
a row `('Signatory', 'Change', 'Verdict')` that `pact-check` then judges as a
review row. The reader output for that shape is in the probe table. This
round did not run it end to end.

The S4 case's docstring
(`tests/test_a_signer_declares_its_pact.py:1222`) says that directly below
with no heading, the stray-row refusal names the old header and it is not
named twice. That holds after a blank line and not without one.

Why it matters: the exit is 2 either way and both sentences are true. A
person still reads two refusals about one line, which is what white 5 was
filed against. The fix filters the old header out of the rows where the
refusal names it. The line is then refused once, as the old header, which
carries the rename and the remedy.

### ⬜ 12 — `PACT_HEADER_WORD` lets an all-caps spelling through

`tests/test_one_word_one_meaning.py:807`. `PACT_RENAMED` is
`re.IGNORECASE`, and `PACT_HEADER_WORD`, which replaces it for the five
compatibility modules, is not. The comment above it (line 804) says their
prose "is still swept for every other spelling". Planted in
`tests/test_pact_check.py`, `SIGNATORY_URL = 'x'` and `# SIGNATORIES` each
leave the tree-wide case green. An upper-case constant is the form the old
word would most likely come back in inside a test module. The rename
touched identifiers, and the compatibility modules spell their constants
in capitals (`SIGNER_URL`, `PACT_URL`).

The fix exempts only the exact capitalised singular, and keeps the unit's
name, so the ledger anchor stays put (its hash moves).

### ⬜ 13 — a setext heading does not end the policy span

`tests/test_one_word_one_meaning.py:733`. The span now ends at ` #{1,6} `
in the flattened text, which is every ATX heading. A setext heading
(`Signatory history` over a `-----` underline) planted after the statement
leaves both sweep cases green. The span then runs on to the next `##`. R6
and the docstring say "a heading of any level". This repository's docs use
ATX headings, so the gap is narrow. The fix stops at an underline run of
two or more `=` or `-` as well. Stopping too early is the safe direction,
because whatever the span stops covering gets swept. The six modules stay
green with it.

## Findings from reading

### ⬜ 14 — the overview's S4 row says the stray-row refusal covers "directly below with no heading" (paperwork)

`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18`
says the old table directly below with no heading is named by "the walk's
stray-row refusal, which already names it". That is the blank-line shape.
With no blank line it is ⬜ 11's shape, and the row should name it. This
is a correction to the run's records and does not count toward `Needs a fix`.

### ⬜ 15 — R6 says "the capitalised header cell" where the sweep exempts the capitalised word (paperwork)

`seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34`,
R6: "sweeps the five compatibility modules for every spelling but the
capitalised header cell (`PACT_HEADER_WORD`)". The pattern exempts
`Signatory` anywhere in those modules, in prose as well. A planted
`# Signatory repositories read the pact.` stays green, which is the design
and is already true in quoted prose there. At the target it also exempts
the all-caps spellings (⬜ 12). Once ⬜ 12 is fixed, the claim should say
"every spelling but the capitalised singular `Signatory`". This is a
correction to the run's records.

## What round 2's findings came to

- **White 5**: closed for the shapes it named. The S4 case's new assertion
  fails against the reader at `b1f18af7`. Across 16 pact shapes and 6
  review shapes, every shape with a blank line, a heading, extra spaces, a
  tab, a missing trailing pipe or a two-space indent names the old header
  exactly once. The glued shape is ⬜ 11.
- **White 6**: closed for ATX headings. A planted `### Signatory history`
  turns both cases red. The setext remainder is ⬜ 13.
- **White 7**: closed for lowercase and for `Signatories`. A planted
  `# a signatory's checkout` turns the tree-wide case red. The record
  prefixes are asserted to exist (read at lines 825-828). The all-caps
  remainder is ⬜ 12.
- **White 8**: closed. The review case's docstring now matches its fixture,
  where the old table sits above under `## Since 0.19.0` and both tables
  hold one row. The `pact-check` S4 commit message reads "an old table above
  a new one", which matches its fixture.
- **White 9**: closed. The `Enforced by:` line carries eight targets, the
  review both-headers case and the tree-wide sweep among them, and the
  folded-statement case resolves them.
- **White 10**: closed. R5 says eight targets, and there are eight. P8 cites
  the S4 case for the both-headers clause, and that case holds it.
- **New units**: `SWEEP_MODULE` ships correct. It is asserted tracked and
  is the one module skipped whole. `PACT_HEADER_WORD` is ⬜ 12.
- **Ledger rows R1, P8, R5, P11**: they say what the code does at the
  target, and their hashes are current. R6 is ⬜ 15.

## Regression tests to plant

- `tests/test_a_signer_declares_its_pact.py`, inside
  `test_s4_a_pact_holding_both_tables_reads_signer_and_refuses_the_old_one`:
  the glued old header, with and without its delimiter row, named once (the
  ⬜ 11 fence). It was executed: red against the target's reader, green with
  the fix.
- A review-record twin of that assertion through `pact_reviews`, beside it.
  Not written and not run, so it is **unverified**. Whoever writes ⬜ 11's
  fix answers it.
- No new case for ⬜ 12 or ⬜ 13. The tree-wide and pact-text cases hold
  both once fixed, and the plants above were seen red with each fix.

## Facts for the evidence ledger

- R1 and P8 cite `read_table`, and ⬜ 11's fix moves its hash. Re-read them
  against the fix, and add to R1's claim that an old header GFM reads as a
  row of the new table is refused once and is not read as a row.
- R6 cites `PACT_HEADER_WORD` and `without_the_policy_span`, and ⬜ 12's
  and ⬜ 13's fixes move both hashes. Reword it as ⬜ 15 says, and add
  "an ATX or setext heading" for the span's end.
- `overview.md` S4 row: ⬜ 14.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's white 5 is closed — an old header after a blank line is named once whatever its spacing | `hooks/config.py:1346` | confirmed | executed: the S4 case red against `b1f18af7`'s reader, green at the target; 16 pact and 6 review shapes through the readers; the glued shape is ⬜ 11 |
| 🟢 | round 2's white 6 is closed — an ATX heading of any level ends the policy span | `tests/test_one_word_one_meaning.py:733` | confirmed | executed: a `### Signatory history` plant turns both sweep cases red; the setext remainder is ⬜ 13 |
| 🟢 | round 2's white 7 is closed — the compatibility modules are swept for the lowercase and plural spellings | `tests/test_one_word_one_meaning.py:807` | confirmed | executed: a lowercase plant turns the tree-wide case red; read: the record-prefix assertion; the all-caps remainder is ⬜ 12 |
| 🟢 | round 2's white 8 is closed — the review case's docstring and the S4 commit message match their fixtures | `tests/test_a_pact_review_takes_a_pact_change.py:216` | confirmed | read against both fixtures |
| 🟢 | round 2's white 9 is closed — the `Enforced by:` line names the eight cases that hold the statement | `docs/the-pact.md:42` | confirmed | read: eight targets; executed: the folded-statement and line-wrap modules, 67 passed |
| 🟢 | round 2's white 10 is closed — R5 counts eight targets and P8 cites the case that holds its clause | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:33` | confirmed | read; executed: `evidence-check --ledger` on the fragment, 432 ok |
| 🟢 | `SWEEP_MODULE`, a unit round 2's fixes created, ships correct | `tests/test_one_word_one_meaning.py:808` | confirmed | read: asserted tracked, the one module skipped whole; executed: the module green |
| 🟢 | ledger rows R1, P8, R5 and P11 say what the code does at the target | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:29` | confirmed | read against `read_table`, `pact_signers` and `docs/the-pact.md`; executed: 432 ok |
| ⬜ 11 | An old header with no blank line above it is read as a row of the `Signer` table and named twice, as an entry that is not a remote URL and as the old header; a review record returns it as a row | `hooks/config.py:1346` | open | executed: three REFUSED lines from `pact-check` at exit 2, two naming the old header; the fix names it once in every shape and keeps the six pact modules green |
| ⬜ 12 | `PACT_HEADER_WORD` is case-sensitive, so `SIGNATORY` and `SIGNATORIES` in a compatibility module are not swept, though its comment says every other spelling is | `tests/test_one_word_one_meaning.py:807` | open | executed: both plants green at the target and red with the fix; the module green with the fix |
| ⬜ 13 | A setext heading after the policy statement does not end the span | `tests/test_one_word_one_meaning.py:733` | open | executed: the plant green at the target and red in both cases with the fix |
| ⬜ 14 | The overview's S4 row says the stray-row refusal names the old header "directly below with no heading", which holds only after a blank line | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | open | paperwork correction; not counted in Needs a fix |
| ⬜ 15 | R6 says the sweep exempts "the capitalised header cell"; it exempts the capitalised word anywhere and, at the target, the all-caps spellings | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34` | open | paperwork correction; not counted in Needs a fix |
| ❓ | The full suite, lint and typecheck, and S12's `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` | the tree at cfd823ba | ❓ out of verified scope | steps of the broad gate, which is the sealer's; the sealer answers it once the orchestrator settles this round's findings |

## Paste-ready fixes

### ⬜ 11

```python
        if holds_old and not any(
            table_cells(quoted) == old
            for r in refusals
            for quoted in re.findall(r"`([^`]*)`", r)
        ):
            # An old header with no blank line above it is one of this
            # table's rows to GFM; the refusal below names it, so it is not
            # read as a row and named a second time.
            rows = [(line, cells) for line, cells in rows if cells != old]
            refusals = [
```
```python
    assert len(refusals) == 1 and "ends above `|Signatory|`" in refusals[0], refusals
    # With no blank line above it, GFM reads the old header as a row of the
    # `Signer` table; it is named once, as the old header, and not also as an
    # entry that is not a remote URL (round 3 of #822).
    for under in ("|Signatory|\n|---|\n|https://example.com/org/billing|\n", "| Signatory |\n"):
        signers, refusals, _ = config.pact_signers(signer + under)
        assert [s[2] for s in signers] == ["orders-web"], signers
        assert sum("Signatory" in r for r in refusals) == 1, refusals
        assert BOTH in refusals, refusals
```
```python
    above it with only a blank line between. Its rows hold signers, and a
    signer nobody reads at exit 0 is what the table walker exists to end.
    Directly below after a blank line, the walk's stray-row refusal already
    names it; with no blank line GFM reads it as one of the `Signer` rows,
    and it is named as the old header rather than as an entry. It is never
    named twice."""
```

### ⬜ 12

```python
# The compatibility cases need the old word only as the header cell, which is
# capitalised and singular; their prose is still swept for every other
# spelling, upper case included (round 2 of #822, white 7; round 3, white 12).
# The sweep's own module stays exempt whole: its pattern, a retired
# identifier and a work item's id name the word.
PACT_HEADER_WORD = re.compile(r"(?!Signatory)(?i:signator(?:y|ies))")
```

### ⬜ 13

```python
    heading = re.search(r" (?:#{1,6}|={2,}|-{2,}) ", rest)
```

### ⬜ 14

```
directly below after a blank line (the walk's stray-row refusal, which already names it), and directly below with no blank line, where GFM reads it as a row of the `Signer` table (one refusal naming the old header, the row not read)
```

### ⬜ 15

```
and sweeps the five compatibility modules for every spelling but the capitalised singular `Signatory` (`PACT_HEADER_WORD`), upper case included
```

## Executed probes

| What was run | Result |
|---|---|
| four modules in a `git clone --no-local` at cfd823ba: the signer, sweep, `pact-check` and pact-review modules | exit 0, 2760 passed |
| `test_a_folded_statement_names_what_enforces_it`, `test_docs_line_wrap` | exit 0, 67 passed |
| the S4 signer case with `hooks/config.py` at b1f18af7 | exit 1, 1 failed |
| `pact_signers` over 16 pact shapes, `pact_reviews` over 6 review shapes, at the target | every shape names the old header once, except the glued shapes C, C2, D (twice) and RC, RC2 (once, with the old header returned as a row) |
| `pact-check` end to end on the glued shape, from a `test_tmp_` probe run once and deleted | exit 2, three REFUSED lines, two naming the old header |
| sweep plants at the target, one at a time: `###` heading, setext heading, lowercase, all-caps constant, all-caps plural, capitalised prose | `###` red in both cases, lowercase red; setext, the two all-caps and capitalised prose green |
| ⬜ 11, ⬜ 12 and ⬜ 13's fixes applied, then the readers over the same shapes | every shape names the old header once; no review returns the old header as a row |
| the same fixes, six pact modules (the four above, the signers' CI module, the table-walker module) | exit 0, 3447 passed |
| ⬜ 11's new S4 lines against the target's reader | exit 1, 1 failed |
| with ⬜ 12 and ⬜ 13's fixes, plants: all-caps constant, all-caps plural, lowercase, `Signatories`, setext, `###` | every one red |
| `bin/evidence-check --ledger seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md .` | exit 0; `total: 432 ok · 0 drifted · 0 broken` |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's broad gate |
| `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` (S12) | not yet — steps of the broad gate, the sealer's |

### ⬜ 11

```
EXIT 2
REFUSED seal/pact.md — the pact has a `Signer` entry that will not read: `Signatory` is not a remote URL — it reduces to no host and path, so no repository can be found by it
REFUSED seal/pact.md — the pact has a `Signer` table that stops at `|---|`, a delimiter row out of place — every signer below it would go unread
REFUSED seal/pact.md — the pact also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it
pact-check: the pact `orders-api` — 1 of 1 signer read · 1 ok · 0 superseded · 0 not taken · 0 unmatched · 0 broken · 0 pact changes read · 0 taken
```
```
RC new,old unspaced as row: rows=[(3, 'orders-web', 'w@abc', 'holds'), (4, 'Signatory', 'Change', 'Verdict')] n_refusals=2 naming_old=1
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, all at cfd823ba:

- `hooks/config.py`: lines 1090-1500 (`table_cells`, `gfm_table`, `read_table`, `pact_signers`, `pact_reviews`, `renamed_header`)
- `tests/test_one_word_one_meaning.py`: lines 690-860
- `tests/test_a_signer_declares_its_pact.py`: lines 1216-1266
- `tests/test_pact_check.py`: lines 1-30, 70-101, 240-285
- `tests/test_a_pact_review_takes_a_pact_change.py`: lines 205-250
- `docs/the-pact.md`: the section from `## The words` through the `Enforced by:` line
- `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md`: rows R1, R5, R6, P8 and P11
- `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md`: the S4 row
- `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/rounds/round-2.md` and `round-2-report.md`
- `bin/test`
- the diff `b1f18af7..96832724`
