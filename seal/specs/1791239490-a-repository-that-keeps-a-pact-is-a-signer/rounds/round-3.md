# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — review round 3

| Field | Value |
|---|---|
| Target SHA | cfd823ba8bee4bf61254d554be701878d2b25edc |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #827 |
| Broad gate | 1d33dc8b against e6d5a055 |
| Fixes checked by | no fixes to check |
| Fix range | `cfd823ba8bee4bf61254d554be701878d2b25edc..cfd823ba8bee4bf61254d554be701878d2b25edc`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 2's fix range `b1f18af7..96832724`, which ends the run: whether ⬜ 5's comparison of quoted cells names an old header once in every shape it can stand in, including `|Signatory|` written as a row of the `Signer` table with no blank line above it, which the orchestrator measured at two refusals (an entry that is not a remote URL, and an old header that GFM reads as a row rather than a header); whether the policy span now ends at a heading of any level and the five compatibility modules are swept for every spelling but the header cell; whether `PACT_HEADER_WORD` and `SWEEP_MODULE` ship correct; whether the `Enforced by:` line, the review case's docstring, and ledger rows R1, P8, R5, R6 and P11 say what the code now does.

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
| ⬜ 11 | An old header with no blank line above it is read as a row of the `Signer` table and named twice, as an entry that is not a remote URL and as the old header; a review record returns it as a row | `hooks/config.py:1346` | deferred #830 | #830; executed: three REFUSED lines from `pact-check` at exit 2, two naming the old header; the fix names it once in every shape and keeps the six pact modules green |
| ⬜ 12 | `PACT_HEADER_WORD` is case-sensitive, so `SIGNATORY` and `SIGNATORIES` in a compatibility module are not swept, though its comment says every other spelling is | `tests/test_one_word_one_meaning.py:807` | deferred #830 | #830; executed: both plants green at the target and red with the fix; the module green with the fix |
| ⬜ 13 | A setext heading after the policy statement does not end the span | `tests/test_one_word_one_meaning.py:733` | deferred #830 | #830; executed: the plant green at the target and red in both cases with the fix |
| ⬜ 14 | The overview's S4 row says the stray-row refusal names the old header "directly below with no heading", which holds only after a blank line | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | deferred #830 | #830; paperwork correction; not counted in Needs a fix |
| ⬜ 15 | R6 says the sweep exempts "the capitalised header cell"; it exempts the capitalised word anywhere and, at the target, the all-caps spellings | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34` | deferred #830 | #830; paperwork correction; not counted in Needs a fix |
| ❓ | The full suite, lint and typecheck, and S12's `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` | the tree at cfd823ba | ❓ out of verified scope | steps of the broad gate, which is the sealer's; the sealer answers it once the orchestrator settles this round's findings |

## Paste-ready fixes

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
```python
# The compatibility cases need the old word only as the header cell, which is
# capitalised and singular; their prose is still swept for every other
# spelling, upper case included (round 2 of #822, white 7; round 3, white 12).
# The sweep's own module stays exempt whole: its pattern, a retired
# identifier and a work item's id name the word.
PACT_HEADER_WORD = re.compile(r"(?!Signatory)(?i:signator(?:y|ies))")
```
```python
    heading = re.search(r" (?:#{1,6}|={2,}|-{2,}) ", rest)
```
```
directly below after a blank line (the walk's stray-row refusal, which already names it), and directly below with no blank line, where GFM reads it as a row of the `Signer` table (one refusal naming the old header, the row not read)
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/config.py:1326` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_one_word_one_meaning.py:736` | round 1's ⬜ 2 — fixed |
| round-1 | `tests/test_one_word_one_meaning.py:722` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | round 1's ⬜ 4 — answered |
| round-1 | `hooks/config.py:1326`, `skills/evidence-check/scripts/pact_check.py:692` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:1333` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py:4085` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md` | round 1's 🟢 — confirmed |
| round-1 | the tree at 91aeafac | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_one_word_one_meaning.py:733` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_one_word_one_meaning.py:801` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py:1344` | round 2's ⬜ 5 — fixed |
| round-2 | `tests/test_one_word_one_meaning.py:816` | round 2's ⬜ 7 — fixed |
| round-2 | `tests/test_a_pact_review_takes_a_pact_change.py:216` | round 2's ⬜ 8 — fixed |
| round-2 | `docs/the-pact.md:42` | round 2's ⬜ 9 — fixed |
| round-2 | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:33` | round 2's ⬜ 10 — answered |
| round-2 | the tree at ec797405 | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
