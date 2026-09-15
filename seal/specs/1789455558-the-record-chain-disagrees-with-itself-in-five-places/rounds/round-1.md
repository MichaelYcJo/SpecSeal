# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — review round 1

| Field | Value |
|---|---|
| Target SHA | 4a5a32cf |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 416 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 and 🟡 2 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the run, against the whole branch — there is nothing earlier to
inherit. Spec compliance first against `spec.md`'s twelve scenarios and
`plan.md`'s seven phases, then quality.

Four of the six issues this branch answers are checks that pass for a reason
other than the one they are named for, so the round was pointed hardest at
whether the repairs are that same shape one level down — the failure the
previous work item's review found three times in three rounds, each time in
the pass that had just repaired the shape one module over.

It was also asked to check two things the build reported rather than to trust
them: the row removed from `seal/ledger.md`, and the fifteen anchor stamps the
orchestrating session refreshed after the build so the gate could reach the
ledger arm.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the second refusal arm blames the verdict word, and the word can be `open`; the vocabulary rule it states is not the rule the file enforces | `skills/code-review/scripts/chain_check.py#open_row_reason` | open | Executed: `open_row_reason("🟡 3", "open", False)` returns the *outside the vocabulary* sentence; `open_blocking` selects that row as `(5, '🟡 3', 'open', False)`; a 🟢/`verified` row quoting no 🔴 returns `[]`. Read: `check_round` holds one verdict check; `test_a_checked_pass_beside_an_open_NON_blocking_finding_passes` pins the open 🟡 as a pass |
| 🟡 2 | the sweep cannot see a bare `the seal` split across two adjacent string literals, so #406's *nothing is uncovered* is false | `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | open | Executed: three mutations of `round_record.py#seal`. One literal → sweep red. The same words across two literals → green. The pinned spelling kept plus a second anonymous instance across two literals → **86 passed** in both modules with an anonymous seal in the output |
| ⬜ 3 | `spec.md` A5's *no pair is unaccounted* is false — 48 of 124 under the shipped rule, 65 under the one A5 describes — and no divergence row names A5 | `seal/specs/1789455558-…/spec.md` §A5 | open | Executed: the predicate re-applied to the committed corpus independently, reproducing 74 / 2 / 48 / 0. Read: `overview.md`'s divergence table names §*Operational impact*, A7 and the ledger, not A5 |
| ⬜ 4 | the case-level positive assertion duplicates the fixture guard added in the same commit, so it cannot fire in the state #407 names | `tests/test_the_fixes_close_the_record.py#test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one` | open | Read: the fixture asserts the same equality on the same cell and nothing between them writes it. `phases/phase-6.md` records the same fact — the mutation had to be applied after the fixture returned |
| ⬜ 5 | the symmetric strip drops a sentence-final stop; visible whenever the reviewer's Grounds cell is empty, and disclosed only in `phase-3.md` | `skills/code-review/scripts/round_record.py#fix_table` | open | Executed: with an empty Grounds cell, `` `<sha>`. it reads the cell now. `` renders `fixed at 1cf3cac — it reads the cell now` |
| ⬜ 6 | the shared-ledger row was removed although only one of its two clauses went false; the surviving clause is now claimed by no row in either file | `seal/ledger.md` at `release/v0.12.0:2204`, superseded by `seal/ledger/1789455558-….md:13` | open | Read: `round_record.py:4060` and `:4064` still name the subcommand, so clause (a) holds; all three anchors survive, only their hashes moved; `grep` for the clause returns 0 in both files. `seal/ledger.md:1951` (S13) states the in-place criterion and this row meets it |
| ⬜ 7 | `seal/ledger.md:2201` enumerates two `reach_forward` refusals over a function that now has three, and `--reverify` re-stamped it without anyone re-reading the list | `seal/ledger.md:2201` | open | Read: the third refusal is `round_record.py:1591`. `seal/ledger.md:1945` (S6) wrote this exact failure mode down one work item ago — *a re-stamp recomputes a hash and reads nothing, so a row enumerating three refusals over a function that now has two would have passed silently*. Also: `overview.md` says `--reverify` refreshed 15 rows; 12 rows moved, carrying 15 anchor stamps |
| 🟢 | #404's first-wins holds, and the two sides agree at the cell-reading level too | `skills/code-review/scripts/round_record.py#close`, `#inherited_rows` | verified | Executed: the raw readers do disagree (`'b` helper drops b'` vs `` '`mod.py#helper`' ``), and `table_of` re-serialises through `copied_row` first, so both piped shapes round-trip to exit 0 |
| 🟢 | #405's corpus measurement is the branch's own figure, independently reproduced | `skills/code-review/scripts/round_record.py#reach_forward` | verified | Executed: 74 / 2 / 48 / 0 with 15 stopped by the standing refusal; the 48 all predate the generator, in a different section spelling |
| 🟢 | the ledger and records arms are clean at this SHA | `seal/ledger.md`, `seal/ledger/1789455558-….md` | verified | Executed: `bin/evidence-check --strict .`, exit 0 read directly — `1274 ok · 0 drifted · 0 broken`, records arm `0 refused` |
| ❓ | the broad gate — the full suite, the repository-wide lint, the typecheck | `seal/config.md` | out of verified scope | `agent-contract` §2 assigns it to `agents/sealer.md`, once, after the rounds settle. Answered by the orchestrating session's sealer spawn, which this round does not make due |

## Paste-ready fixes

```python
    named = ", ".join(f"`{word}`" for word in sorted(CLOSED_WORDS))
    return (
        "`Pass` is checked, and this row is read as open because one of its "
        "cells quotes a blocking finding an earlier round opened, while its "
        f"own verdict reads `{verdict or 'empty'}` — not one of the words "
        f"that close a row: {named}. Nothing here says the finding was "
        "closed, and an unrecognised verdict counted as closed is the "
        "tolerant read this file exists to refuse. Write one of those words, "
        f"drop the quote, or leave `Pass` unchecked: {what}"
    )
```
```python
def test_a_row_reading_open_is_not_told_its_word_is_unrecognised(repo):
    """`open` is the word `agents/warden.md` prescribes for a finding this
    round opened, and the first arm of this same function prints it back as
    `this 🔴 row reads `open``. The second arm must not tell the author the
    word is outside any vocabulary — what selected the row is the quote.

    Red against the arm as written: *…reads `open`, which is outside the
    vocabulary…* on a row whose `#` cell reads 🟡.
    """
    code, out = confirmation(repo, "open")
    assert code == 1, out
    (line,) = [ln for ln in out.splitlines() if "close a row" in ln]
    assert "outside the vocabulary" not in line, line
    assert "quotes a blocking finding an earlier round opened" in line, line
    assert "drop the quote" in line, line
```
```python
# Python joins adjacent string literals at parse time and `flat` does not, so
# a phrase split across two of them reads `... the " "seal ...` in the source
# and the sweep goes straight past it. That is the shape the output assertion
# deleted by #406 used to catch, and the reason the deletion was not
# coverage-neutral. Folding the seam here keeps ONE implementation of the rule
# reading two kinds of input, which is what the alternatives table rejected a
# second check in favour of. A seam folded where Python would not join only
# ever creates a hit, never hides one, so the error direction is the safe one.
LITERAL_SEAM = re.compile(r"([\"'])\s*(?:[fFrRbBuU]{0,2})\1")


def flat(*parts):
    text = " ".join(read(*parts).split())
    return LITERAL_SEAM.sub("", text) if parts[-1].endswith(".py") else text
```
```python
def test_the_sweep_reads_across_a_string_literal_seam():
    """The shape the deleted output pin caught and the file sweep did not.
    `round_record.py` builds every refusal out of wrapped literals, and where
    the wrap falls is decided by line length, so an anonymous instance
    straddling a seam is an ordinary edit rather than an exotic one.

    Red before the seam fold: the flattened source reads `... the " "seal ...`
    and `find("the seal")` returns -1.
    """
    seamed = ' "Spawn the verifying round first, so the " "seal covers it; " '
    assert "the seal" in LITERAL_SEAM.sub("", " ".join(seamed.split())).lower()
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py` in the clone at `4a5a32cf` | 82 passed, exit 0 |
| `bin/test` on `test_chain_check_at_the_pull_request.py`, `test_the_record_is_generated.py`, `test_one_word_one_meaning.py`, `test_the_seal_is_taken_once_by_the_sealer.py` | 299 passed, exit 0 |
| `bin/test tests/test_no_real_identifiers.py tests/test_the_rules_have_one_owner.py` | 56 passed, exit 0 |
| `bin/evidence-check --strict .` in the clone, exit read directly | exit 0 — `1274 ok · 0 drifted · 0 broken · 0 external`, records arm `0 refused` |
| `open_row_reason("🟡 3", "open", False)` | returned the *outside the vocabulary* sentence for `open` — 🟡 1 |
| `open_blocking` on a 🟡/`open` row quoting a 🔴 in its Grounds | `[(5, '🟡 3', 'open', False)]` — selected, routed to the second arm |
| `open_blocking` on a 🟢/`verified` row quoting no 🔴 | `[]` — not refused at all; the second arm's stated rule is not enforced |
| mutation A: `round_record.py#seal` reworded to `before the seal is taken`, one literal | `test_one_word_one_meaning.py` **red**, naming the module and quoting the span — phase 5's red-first reproduced |
| mutation B: the same words split across two adjacent literals | `test_one_word_one_meaning.py` **green** — the sweep cannot see the seam |
| mutation C: pinned spelling kept, second anonymous instance added across two literals | **86 passed** in both modules with an anonymous seal in the refusal's output — 🟡 2 |
| the `filled == 0` accounting re-applied to every committed `round-N`/`round-N+1` pair | 15 stopped by the standing refusal; 74 silent; 2 refused by the unconditional rule alone; **48 refused by the shipped rule**; 0 in the fourth cell |
| `close` with a verdict row carrying a raw `\|` inside a code span, and with a `\|` inside the Location cell | both round-trip; `inherited_rows` and `close`'s map name the same coordinate — hypothesis refuted |
| `close` with an empty reviewer Grounds cell and a note ending in a full stop | rendered `fixed at 1cf3cac — it reads the cell now` — ⬜ 5 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
