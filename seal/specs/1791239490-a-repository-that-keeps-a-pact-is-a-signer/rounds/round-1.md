# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — review round 1

| Field | Value |
|---|---|
| Target SHA | 91aeafacb7db8c34d621a9fe9d80e887a8ce9044 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #827 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `d1e0b2c615df9b003bbc54604ac881a150b50518..b4a5ebb4cfbcb3f60cf91638a4105fc3c4389089`, 3 commits |
| Contract changes | none |
| New units | test_s5_a_review_record_holding_both_headers_is_refused (depth 1); BOTH (depth 1); test_s4_a_pact_holding_both_tables_reads_signer_and_refuses_the_old_one (depth 1); without_the_policy_span (depth 1); RENAMED_RECORDS (depth 1); RENAMED_COMPAT (depth 1); test_no_live_text_says_the_word_0_19_0_renamed (depth 1); test_s4_a_pact_holding_both_tables_is_exit_2_naming_the_old_one (depth 1) |
| Needs a fix | yes — 🟡 1, a pact or pact review record holding both headers drops the old table's rows with no refusal |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Spec compliance first against `spec.md` (every live text says `signer`; a pact and a pact review written with `| Signatory |` still read, with one line naming the rename that changes no exit code; a broken `| Signer |` table is refused rather than covered by an old one; the sweep in `tests/test_one_word_one_meaning.py` refuses the old word outside its two named spans; released records keep their word), then quality: every path that reads a pact's or a pact review's table, enumerated and attacked with both headers, neither, both at once, and a broken new one; the printed lines of `pact-check` and `chain-check` and their exit codes; the sweep's exemptions, as a place the old word could return through; the ledger fragment's 28 `Corrected ·` and 39 `Re-read ·` rows against the claims they re-point, with the released files untouched; the overview's four divergences from the plan.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A file holding both headers is read from the `Signer` table, and the old table's rows go unread with no refusal where it stands above the new one, or below it under a heading; two cases pin that silence | `hooks/config.py:1326` | **fixed** `34a195cc` | fixed at 34a195cc; executed: `pact-check` read 0 of 1 signer with two old-table signers never named, and `chain-check` said "lists 1 signer"; the fix flips exactly the four cases that pin the drop |
| ⬜ 2 | The sweep's policy exemption runs past the statement into the next section's heading | `tests/test_one_word_one_meaning.py:736` | **fixed** `5fd4c203` | fixed at 5fd4c203; executed: the old word planted in `## When there is a pact at all` leaves the case green |
| ⬜ 3 | The sweep reaches only `pact_texts()`, so S11's property has no standing check over the other files spec item 1 renamed | `tests/test_one_word_one_meaning.py:722` | **fixed** `5fd4c203` | fixed at 5fd4c203; executed: five plants outside the set stay green, and one inside turns it red; spec item 8 scopes the sweep this way |
| ⬜ 4 | The overview's S4 row omits one silent shape and does not say the "above" shapes are outside S4; the spec's "module constants" became a function with no divergence row | `seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/overview.md:18` | answered | corrected at b4a5ebb4; paperwork correction; not counted in Needs a fix |
| 🟢 | A pact and a pact review record headed the 0.18.x way read as the new header does, with one rename line each and no exit change | `hooks/config.py:1326`, `skills/evidence-check/scripts/pact_check.py:692` | confirmed | executed: reader probe and the S2/S5 cases in the slice |
| 🟢 | A broken `\| Signer \|` table is refused and not covered by the old one | `hooks/config.py:1333` | confirmed | executed: no delimiter row and a line directly above both refuse with the header read as `Signer` |
| 🟢 | `chain-check` counts signers, carries the rename sentence on the old header, and its exit does not move | `skills/code-review/scripts/chain_check.py:4085` | confirmed | executed: four shapes, all exit 0 |
| 🟢 | Every `Corrected ·` row carries every coordinate its released row rests on, and the released files are byte-identical to the base | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md` | confirmed | executed: coordinate comparison script, `evidence-check --ledger` on the fragment (423 ok), empty `git diff --stat` |
| ❓ | S12's `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD`, and the full suite, lint and typecheck | the tree at 91aeafac | ❓ out of verified scope | both commands are steps of the broad gate (`skills/verify/scripts/broad_gate.py`), which is the sealer's; the sealer answers it once the rounds settle |

## Paste-ready fixes

```python
def read_table(text, header):
    """(rows, refusals, header read) for the table of TEXT headed HEADER,
    or, where TEXT holds none, headed as HEADER was written before 0.19.0
    (`renamed_header`). A text holding a HEADER table is read from it alone,
    and an old header it also holds is refused: the rows under it would
    otherwise go unread at exit 0, wherever that table stands. Where neither
    is there, the refusal names HEADER and the header read is None, so a
    caller tells the old header from the new one without reading the text
    again (#822)."""
    rows, refusals = gfm_table(text, header)
    old = renamed_header(header)[0]
    old_rows, old_refusals = gfm_table(text, old) if old else ([], [])
    holds_old = old is not None and not (
        old_refusals and old_refusals[0].startswith("holds no ")
    )
    if not (refusals and refusals[0].startswith("holds no ")):
        if holds_old and not any(f"`| {' | '.join(old)} |`" in r for r in refusals):
            refusals = refusals + [
                f"also holds a `| {' | '.join(old)} |` header, the word before "
                f"{RENAMED_IN}, and nothing under it is read while the "
                f"`| {' | '.join(header)} |` table stands — move its rows into "
                "that table and delete it"
            ]
        return rows, refusals, header
    if holds_old:
        return old_rows, old_refusals, old
    return rows, refusals, None
```
```python
BOTH = (
    "also holds a `| Signatory |` header, the word before 0.19.0, and nothing "
    "under it is read while the `| Signer |` table stands — move its rows into "
    "that table and delete it"
)


def test_s4_a_pact_holding_both_tables_reads_signer_and_refuses_the_old_one():
    """S4 of #822. A `| Signer |` table is read alone, and an old table
    anywhere else in the file is refused rather than left unread: above it,
    below it under a heading, or above it with only a blank line between.
    Directly below with no heading, the walk's stray-row refusal already
    names it."""
    signer = "# Pact\n\n| Signer |\n|---|\n| https://example.com/org/orders-web |\n"
    old = "| Signatory |\n|---|\n| https://example.com/org/billing |\n"
    for text in (
        signer + "\n## Before\n\n" + old + "\n## A\n\nx\n",
        f"# Pact\n\n{old}\n## Now\n\n" + signer.split("\n\n", 1)[1],
        f"# Pact\n\n{old}\n" + signer.split("\n\n", 1)[1],
    ):
        signers, refusals, header = config.pact_signers(text)
        assert [s[2] for s in signers] == ["orders-web"], (text, signers)
        assert refusals == [BOTH] and header == ("Signer",), (text, refusals)
    _, refusals, header = config.pact_signers(signer + "\n" + old)
    assert header == ("Signer",)
    assert refusals == [
        "has a `Signer` table that ends above `| Signatory |`, a row the walk "
        "never reaches — it and every signer below it would go unread"
    ], refusals
```
```python
    signers, refusals, header = config.pact_signers(both)
    assert header == ("Signer",), (both, header)
    assert [s[0] for s in signers] == [v], (both, signers)
    assert len(refusals) == 1 and "also holds a `| Signatory |` header" in refusals[0], (
        both,
        refusals,
    )
```
```
A file holding no table under the new header is read under the old one
exactly as it would be under the new; a file holding one is read from it
alone, and an old header beside it is refused, because its rows would
otherwise go unread.
```
```python
            head, marker, rest = text.partition(span)
            assert marker, f"{where}: the excluded span `{span}` is gone"
            # The statement ends at the next heading or the next fold marker,
            # whichever comes first; `flat` has put both on one line.
            stops = [i for i in (rest.find("<" + "!--"), rest.find(" ## ")) if i != -1]
            assert stops, (
                f"{where}: the excluded span is the last statement in the file, "
                "so this exclusion now removes everything after it"
            )
            text = head + rest[min(stops) :]
```

## Executed probes

| What was run | Result |
|---|---|
| `pact_signers` and `pact_reviews` over 14 pact and 5 review shapes, in a `git clone --no-local` at 91aeafac | see 🟡 1's table; every single-header and neither shape behaves as the spec says |
| `pact-check` end to end: old table (orders-web, orders-mobile), heading, `\| Signer \|` (orders-tablet) | exit 1, `0 of 1 signer read`, the two old-table signers never named |
| `chain-check` over the old header, both (old above), neither, broken new + old | exit 0 in all four; the rename sentence only on the old header; "lists 1 signer" on both |
| the sweep case with the old word planted in eight places, one at a time | red only for a string constant of `pact_check.py`; green for the seven outside the swept set or inside the policy span |
| a script comparing each `Corrected ·` row's coordinates with its released row | 27 of 28 parsed, every released coordinate carried; P8 compared by hand |
| `evidence_check.py --ledger seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md .` | exit 0; `total: 423 ok · 0 drifted · 0 broken` |
| `git diff --stat e6d5a055...HEAD -- seal/ledger.md seal/releases changelog` | empty |
| six pact modules: `test_one_word_one_meaning`, `test_a_folded_statement_names_what_enforces_it`, `test_pact_check`, `test_a_signer_declares_its_pact`, `test_a_pact_review_takes_a_pact_change`, `test_a_signers_ci_prints_its_pact` | exit 0, 2797 passed |
| 🟡 1's fix applied in the clone, then the pact modules with the walker module | exit 1, 3440 passed, 4 failed: the S4 case and the walker case's three parametrizations, each asserting the silent drop |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |
| `evidence-check --strict .` and `correction-check --range origin/release/v0.19.0...HEAD` (S12) | not yet — steps of the broad gate, the sealer's |

```
NOT FOUND https://example.com/org/orders-tablet — no checkout of it was found on this machine: add `| https://example.com/org/orders-tablet | <the path of its checkout> |` to ~/.claude/specseal/pact-paths.md
pact-check: the pact `orders-api` — 0 of 1 signer read · 0 ok · 0 superseded · 0 not taken · 0 unmatched · 0 broken · 0 pact changes read · 0 taken
```
```
old above, heading, new below -> (['also holds a `| Signatory |` header, the word before 0.19.0, and nothing under it is read while the `| Signer |` table stands — move its rows into that table and delete it'], ('Signer',))
old above, blank, new below   -> (same refusal, ('Signer',))
new above, heading, old below -> (same refusal, ('Signer',))
new above, blank, old below   -> (['has a `Signer` table that ends above `| Signatory |`, a row the walk never reaches — it and every signer below it would go unread'], ('Signer',))
signer only                   -> ([], ('Signer',))
signatory only                -> ([], ('Signatory',))
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
