# 1790206437-a-second-fold-writes-a-second-heading — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | dea6f051 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The convention (#366, second half): one sentence in `agents/warden.md`,
`skills/code-review/SKILL.md` §Findings format and
`docs/review-chain-spec.md` §The depth in `New units` — a finding whose
coordinates sit at two depths is written as two findings, one depth each —
held in one constant and pinned in
`tests/test_the_report_standard_is_one_in_three_places.py`, red with the
sentence deleted from any one carrier; no `.py` under
`skills/code-review/scripts/` touched in this phase. Q1 arrived answered by
the owner before this phase: convention only.

## What this phase found

**The frame holds.** The three carriers had the paragraphs the spec named
(`agents/warden.md`'s verifying-round item on the previous record's
`New units` surface, the skill's id paragraphs under §Findings format, the
spec's *declared wrong* paragraph), and each took the sentence beside the
paragraph it extends. The pin is `SPLIT_AT_TWO_DEPTHS`, one text, and
`REVIEWER_CARRIERS` names the three files rather than slicing `CARRIERS`,
as the plan asked; the template is not a carrier (judgment 7).

**The sentence is lowercase in every carrier on purpose.** The pin is
case-sensitive, so each carrier leads into it with a clause (*Write one
depth per finding:*, *One depth per finding:*, *The declaration is per
finding as well as per entry:*) rather than starting a sentence with it.
Each carrier then says what the reviewer needs from where it stands: the
warden and the skill say `round_record.py close` keys the refusal on the
finding's `Location`, the spec says the refusal names the finding to split
next round.

**Red first, executed.** `bin/test tests/test_the_report_standard_is_one_in_three_places.py -q -k split_a_finding`
at `b9cec50f`, no carrier holding the sentence: 1 failed, exit 1, naming
`agents/warden.md`. Then, with all three holding it, the sentence deleted
from each carrier in turn by a script restoring kept bytes: 1 failed, exit
1 each time, naming the carrier it was deleted from. Bytes identical to the
kept copies after each.

**Green, executed.** `bin/test tests/test_the_report_standard_is_one_in_three_places.py
tests/test_docs_line_wrap.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py -q`:
114 passed in 66.83 s, exit 0. `bin/test tests/test_the_rules_have_one_owner.py
tests/test_one_word_one_meaning.py tests/test_a_moved_rule_leaves_its_definition.py
tests/test_a_corrected_sentence_survives_elsewhere.py -q`: 314 passed, exit 0
— a sentence stated in three files is what the one-owner module exists to
refuse for the rules it lists, and it does not list this one. `uvx ruff
check` and `uvx ruff format --check` over the test module: exit 0.
`git diff --stat` for the phase: the three carriers and the test module,
no `.py` under `skills/code-review/scripts/`.

**The ledger: eight rows re-read.** Three document sections moved
(`agents/warden.md#"## Role"`, `skills/code-review/SKILL.md#"## Findings
format"`, `docs/review-chain-spec.md#"##### The depth in `New units`"`) and
one enclosing one with them (`docs/review-chain-spec.md#"### Review arm —
opt-in: `seal/` at the repo root"`, which spans 668–1945 and drifts on any
edit inside it). Seven rows were re-stamped by `--reverify` and each got a
`Re-read 2026-09-24` note; the eighth, `1788331011`'s row hashing its own
`###` section, drifted because one of the seven stands inside that section,
and took a second `--reverify` pass and its own note — the shape its Notes
cell already described from the last time. `evidence-check --strict .`:
`1662 ok · 0 drifted · 0 broken`, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
