# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — review round 2

| Field | Value |
|---|---|
| Target SHA | ec7974055bc05fb933948f5f8022e74f3336e23f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #827 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `b1f18af7914dbfc7f9b6c64e9a2dc36f227ba0d5..96832724edc66735dbf643454b4d0c50cca57af8`, 3 commits |
| Contract changes | none |
| New units | PACT_HEADER_WORD (depth 1); SWEEP_MODULE (depth 1) |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 1's fix range `d1e0b2c6..b4a5ebb4`: whether 🟡 1's refusal of a text holding both headers reaches every shape round 1 named (old table above, below past a heading, directly below) for a pact and for a pact review, without refusing a text that holds only one header or names the old word in prose; whether `pact-check` exits 2 and `chain-check` keeps its exit code on those shapes; whether the sweep's policy span now ends at its statement and `test_no_live_text_says_the_word_0_19_0_renamed` holds every tracked live file, with its exemptions as the places the old word could still return through; whether the eight units the fix pass added ship correct, and whether the ledger rows R1, P8, R5 and R6 it reworded and re-stamped say what the code now does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking-class finding is closed — a pact or pact review record holding both headers refuses the old one in every shape round 1 named, and no one-header or prose text is refused | `hooks/config.py:1326` | confirmed | executed: 17 pact and 8 review shapes through the reader; `pact-check` exit 2 on old-above-blank, new-heading-old and new-blank-old, review exit 2 on two shapes; `chain-check` exit 0/1 unchanged on three shapes; seven fix-pass cases red against d1e0b2c6's reader |
| 🟢 | round 1's white 2 is closed — the policy span ends at the next `##` heading | `tests/test_one_word_one_meaning.py:733` | confirmed | executed: the old word planted in `## When there is a pact at all` turns both sweep cases red; the class's remainder is ⬜ 6 |
| 🟢 | round 1's white 3 is closed — every tracked live file is swept | `tests/test_one_word_one_meaning.py:801` | confirmed | executed: plants in `CHANGELOG.md`, `templates/seal-README.md`, `README.md`, `chain_check.py`'s docstring, `read_table`'s docstring and above `RENAMED_IN` each turn the tree-wide case red |
| 🟢 | round 1's white 4 is closed — the overview's S4 row names every two-table shape and the function is a recorded divergence | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | confirmed | read against the reader probe's table |
| ⬜ 5 | An old header written without spaces directly below the `Signer` table is named twice, against `read_table`'s docstring and the S4 case's | `hooks/config.py:1344` | **fixed** `27b33261` | fixed at 27b33261; executed: two refusals before the fix, one after; 3447 passed with the fix |
| ⬜ 6 | The policy span stops at `##` only, so a `###` heading after the statement is exempt | `tests/test_one_word_one_meaning.py:733` | **fixed** `626a5884` | fixed at 626a5884; executed: a `### Signatory history` plant leaves both cases green; the fix turns both red and keeps the module green |
| ⬜ 7 | Five compatibility modules are exempt whole, though every use they need is the capitalised header cell; "each exception is asserted to exist" skips the record prefixes | `tests/test_one_word_one_meaning.py:816` | **fixed** `626a5884` | fixed at 626a5884; executed: a lowercase comment in `tests/test_pact_check.py` stays green; the fix turns it red and keeps the module green |
| ⬜ 8 | The review case's docstring says the old table holds a row the new one does not, and both hold the same row; the `pact-check` S4 commit message reverses which table is above | `tests/test_a_pact_review_takes_a_pact_change.py:216` | **fixed** `96832724` | fixed at 96832724; read |
| ⬜ 9 | The policy's `Enforced by:` line omits the review both-headers case and the tree-wide sweep, the cases that hold two of its clauses | `docs/the-pact.md:42` | **fixed** `96832724` | fixed at 96832724; read |
| ⬜ 10 | R5's evidence counts five `Enforced by:` targets where there are six, and P8's new clause cites no case that holds it | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:33` | answered | corrected at 96832724; paperwork correction; not counted in Needs a fix; `evidence-check --ledger` on the fragment 429 ok |
| ❓ | The full suite, lint and typecheck, and S12's `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` | the tree at ec797405 | ❓ out of verified scope | steps of the broad gate, which is the sealer's; the sealer answers it now that this round leaves nothing needing a fix |

## Paste-ready fixes

```python
        if holds_old and not any(
            table_cells(quoted) == old
            for r in refusals
            for quoted in re.findall(r"`([^`]*)`", r)
        ):
```
```python
    # Written without its spaces, the old header is quoted as written by the
    # stray-row refusal, and is still named once.
    _, refusals, _ = config.pact_signers(
        signer + "\n|Signatory|\n|---|\n|https://example.com/org/billing|\n"
    )
    assert len(refusals) == 1 and "ends above `|Signatory|`" in refusals[0], refusals
```
```python
    heading = re.search(r" #{1,6} ", rest)
    stops = [
        i
        for i in (rest.find("<" + "!--"), heading.start() if heading else -1)
        if i != -1
    ]
```
```python
# The compatibility cases need the old word only as the header cell, which is
# capitalised; their prose is swept for it in lower case.
PACT_HEADER_WORD = re.compile(r"signator(?:y|ies)|Signatories")
```
```python
    for prefix in RENAMED_RECORDS:
        assert any(p.startswith(prefix) for p in tracked), (
            f"{prefix} is excepted below and holds no tracked file"
        )
    said = []
    for rel in tracked:
        if rel.startswith(RENAMED_RECORDS) or rel == "tests/test_one_word_one_meaning.py":
            continue
```
```python
        pattern = PACT_HEADER_WORD if rel in RENAMED_COMPAT else PACT_RENAMED
        said.extend(f"{rel}: {m.group(0)}" for m in pattern.finditer(text))
```
```python
    """Round 1's yellow 1, for a pact review record. An old table above the
    new one is never read while the new one stands; read silently, a row
    only it held would be dropped and the record it took would read `NOT
    TAKEN` again with nothing saying why. It is refused at exit 2 instead."""
```
```python
    commit(world["api"], "an old table above a new one")
```
```
, tests/test_a_pact_review_takes_a_pact_change.py::test_s5_a_review_record_holding_both_headers_is_refused, tests/test_one_word_one_meaning.py::test_no_live_text_says_the_word_0_19_0_renamed
```

## Executed probes

| What was run | Result |
|---|---|
| eight modules in a `git clone --no-local` at ec797405: the six pact modules, `test_a_folded_statement_names_what_enforces_it`, `test_docs_line_wrap` | exit 0, 3514 passed |
| `pact_signers` over 17 pact shapes and `pact_reviews` over 8 review shapes | see the table under round 1's yellow 1 |
| `pact-check` end to end: old above after a blank line, old below under a heading, old directly below | exit 2 in all three, the refusal line printed, no rename line |
| `pact-check` end to end on a review record: new above with old below under a heading, old above after a blank line, new only | exit 2, exit 2, exit 0 |
| `chain-check` over new only, old above under a heading, old above after a blank line, old below under a heading, old only, with the round record passing and failing | exit 0 passing and 1 failing in every shape; the refusal as a notice on the three two-table shapes; the rename sentence on old only |
| the seven fix-pass cases with `hooks/config.py` at d1e0b2c6 | exit 1, 7 failed |
| the two sweep cases with the old word planted in nine places, one at a time | red for seven; green for a `###` heading after the statement and a lowercase comment in a compatibility module |
| ⬜ 6's fix applied, the module, then the `###` plant | 21 passed; then both cases red |
| ⬜ 7's fix applied, the module, then the lowercase plant | 21 passed; then the tree-wide case red |
| ⬜ 5's fix applied, the reader on four shapes, then the six pact modules | one refusal each; exit 0, 3447 passed |
| `bin/evidence-check --ledger seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md .` | exit 0; `total: 429 ok · 0 drifted · 0 broken` |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's broad gate, now due |
| `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` (S12) | not yet — steps of the broad gate, the sealer's |

```
PACT N new, blank, old unspaced: signers=['orders-web'] header=('Signer',) refusals=['has a `Signer` table that ends above `|Signatory|`, a row the walk never reaches — it and every signer below it would go unread', 'also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it']
```
```
REFUSED seal/pact.md — the pact also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it
pact-check: the pact `orders-api` — 1 of 1 signer read · 1 ok · 0 superseded · 0 not taken · 0 unmatched · 0 broken · 0 pact changes read · 0 taken
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
