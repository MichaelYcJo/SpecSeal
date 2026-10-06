# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | a8d3482f |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The owner and the carriers. A `###` in `skills/code-review/orchestration.md`
under *the run ends with a verifying round* stating the rule, its two against
the 3+ Fix Rule's three, the stop, the reframe and the exit; a link of at most
three lines in `docs/review-chain-spec.md` beside the `stop regardless` row;
`agents/framer.md`'s hand-back paragraph and its writes; one sentence in
`agents/warden.md`; the `spec.md` row of `skills/implement/SKILL.md` §3; the
comment in `templates/sdd-spec.md`; a row in the acts table of
`skills/implement/orchestration.md`; the rule in
`tests/test_the_rules_have_one_owner.py`; `chain: reframed` named in
`docs/issues-and-milestones.md`. `docs/review-chain-spec.md` stays at or under
1000 lines.

## What this phase found

**The rule is number 16, not 11.** `plan.md` named rule 11 in the one-owner
table; that number has belonged to *a wrapped terminal line is one value*
since #340, and rules 12 to 15 joined after it. The new row is 16, owner
`ORCH`, with five link carriers: `docs/review-chain-spec.md`,
`docs/round-record-spec.md`, `agents/framer.md`, `agents/warden.md` and
`skills/implement/SKILL.md`. Each carrier names the section with `owns that
rule`, which is the string the test reads.

**The section sits between *The cap is a ceiling* and the depth section**, so
`tests/test_a_fix_pass_may_add_a_unit.py`'s slice of the depth section, which
ends at *Then say who checked them*, does not grow to hold it.

**`tests/test_no_passage_is_pasted_into_a_second_file.py` caught two copies
this phase and phase 1 made.** The run definition stood in both the owner and
`docs/round-record-spec.md`, and the `second` value stood whole in both the
template row and the spec's value table. The owner now says what starts over
past a `second` in its own words, and the template row shows `second — <the
same>; …` and leaves the full value to the spec.

**The spec's link is three lines and the file stands at 998.** The link names
the widening (any severity, in the unit the last fix pass wrote) and the
owner, and leaves the rest to it.

**§15, shown red by mutation.** The owner's headline sentence, the framer's
and the spec's link sentences, and the acts-table heading were each broken
once with `mutation-check` against `test_the_rules_have_one_owner.py -k 16`
and `test_every_orchestrator_act_names_its_delivery.py`. All red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the full `second` value in `templates/sdd-round.md`'s `Fix of a fix` row | `docs/round-record-spec.md` §*A fix of a fix — `Fix of a fix`*, whose value table states it |
