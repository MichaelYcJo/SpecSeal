# 1789356180-the-two-halves-of-one-generator-refuse-each-other — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 853f65a |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

A verdict row that commissions nothing. A row with no finding id is copied
into the record, never keyed, and never asked for a closure; a row whose
verdict reads `❓ out of verified scope` is treated the same way; and a refusal
for a malformed id names every offending row rather than the first. The rule is
stated in `agents/warden.md`, `templates/sdd-round.md`,
`skills/code-review/SKILL.md` and `docs/review-chain-spec.md` §*The finding id*
in the same commit. Q1's answer is (a) with (b) kept for the rows that do carry
an id — so the validation also lands at `new`, where today it lands only at
`close`.

## What this phase found

**A row with no id needs no spelling of its own, and the corpus is what
decides it.** `plan.md` left this open. The discriminator is whether the cell
carries a digit anywhere in it: of the 253 cells today's rule refuses, 199
carry digits and were reaching for an id and missed (`R2-1`, `1b`, `round 2's
finding (🟡 4)`), and 51 carry none. Requiring one sentinel — an empty cell,
say — would refuse the shapes reviewers already reach for and buy nothing: a
reviewer who forgets an id writes an empty cell just as readily as a word.

<!-- CORRECTED 2026-09-14 by round 1's 🟡 2, which re-derived this population
through the module's own `table_body`. The sentence that stood here said the
51 "carry none and were never an id (`✅`, `carried`, `🟢 fix-surface`, `—`)"
and that "the two populations do not overlap on anything a reviewer writes".
The count is right and the reading of it was not. **44 of the 51 are a
severity marker and a single LETTER** — `🔴 A` through `🟢 O` — which is a
finding id in the wrong alphabet, and only 7 are the shape this rule admits.
Neither `✅` nor a bare em dash occurs in a committed record at all; the 21
bare em dashes are in reviewers' REPORTS, a different corpus. So the evidence
for the admission is 7 rows rather than 51, and the dominant no-digit shape is
a finding id — which is what round 1's 🔴 1 then found the rule admitting with
`Pass` ticked over it. The severity arm is that repair, and the corrected
grounds are in `docs/review-chain-spec.md` §*A verdict row that commissions
nothing* and in this work item's ledger fragment, row 1. The conclusion this
paragraph reaches — no sentinel of its own — is unchanged and is still right;
its grounds were wrong. -->

**The corpus counts the frame read are three of them wrong, and one badly.**
Re-derived by executing the module's own patterns over the 207 committed
records that parse, on 2026-09-14:

| What was counted | `spec.md` §6 read | Executed here |
|---|---|---|
| verdict body rows | 1,992 | **1,989** |
| refused, carrying digits | 199 | **199** |
| refused, no digit at all | 54 | **51** |
| bare `—` `#` cells in reports | 21 | **21** |
| Grounds cell reduced to its home | 66 | **66** |
| `fixed at <sha> — ` then an empty code span | 103 | **210** |

The last row is the one that matters: the frame's 103 is low by more than
half, and phase 3's acceptance re-measures it. The three small divergences do
not move any argument — one row in thirty-seven is still one row in
thirty-seven.

**The scope marker could not be closed from the `#` column at all.** #84's
finding 15 carries an id (`15`), so phase 1's `#`-cell mechanism never reaches
it. It is closed from the Verdict column instead: `out of verified scope` joins
`chain_check.CLOSED_WORDS` and neither `FIX_WORDS` nor `HOME_WORDS`. That is
the split `spec.md` predicted between the two columns, arriving one phase
earlier than the table there puts it.

**A severity marker leads a verdict cell and `verdict_of` did not know it.**
Every committed scope-marker row reads `❓ out of verified scope`, marker
included, and `verdict_of` matched the vocabulary as a prefix of the whole
cell. Stripping a leading run of non-word characters is the same rule
`FINDING_ID_RE` applies one column over, and it was measured before it was
taken: over all 1,989 committed verdict rows it changes the reading of
**exactly one cell**, which is the one this release is adding. Nothing else
this repository has ever written begins a verdict cell with punctuation that a
strip would carry into a vocabulary word.

**`new` validates the ids through `verdict_rows`, not through a new call
site.** `tests/test_a_finding_id_is_a_bare_integer.py#test_the_rule_is_one_constant_both_tables_read`
asserts one `FINDING_ID_RE.match` site and exactly three `finding_number(`
occurrences. The report's verdict table carries the same heading under the
same header as the record's — that is what lets `table_of` copy one into the
other — so `build` calls `verdict_rows` on the report's own lines and gets
both the validation and the keying for free. The case's numbers are unchanged.

**That second use fixed a disagreement nobody had listed.** `build` derived
`Pass` and `landing_values` from `verdict_words` over every copied row. A
confirmation row reads `verified` in its verdict cell, which is in no
vocabulary and therefore OPEN — so `new` would tick no box for a round that
opened nothing while `close` ticked one. The two halves refusing each other is
this work item's own title, met inside it.

**Four existing cases had their refusal move, and each keeps both halves.**
`new` refusing a malformed id does not retire the reading at `close`, because a
record is a file somebody can edit — so `test_a_hand_edited_record_still_meets_the_rule_at_close`
was added and `test_every_shape_the_corpus_holds_is_refused_by_name` lost `A`
and `carried` to a new companion case that asserts they are admitted.

**Q5 and Q6 are phase 3's and phase 4's and are untouched here.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `A` and `carried` as refused `#` cells — `tests/test_a_finding_id_is_a_bare_integer.py#test_every_shape_the_corpus_holds_is_refused_by_name`'s parameter list | `#test_every_no_digit_shape_the_corpus_holds_is_admitted`, which asserts the opposite for the same two shapes plus `✅`, `🟢 fix-surface` and `—` |
| the `close`-path assertion in four cases whose refusal moved to `new` | `#test_a_hand_edited_record_still_meets_the_rule_at_close` keeps the `close` reading pinned; the `new` reading is pinned by `#test_a_malformed_id_is_refused_at_new_where_the_author_is` |
| `verdict_words` as `build`'s source of verdict words | `verdict_rows`, in `build`. The function keeps its other caller, `inherited_rows`, and is not removed |
