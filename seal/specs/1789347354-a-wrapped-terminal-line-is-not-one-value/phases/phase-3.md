# 1789347354-a-wrapped-terminal-line-is-not-one-value — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 02e4436 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#340: put the conformance statement — a wrapped terminal line is one value,
and here is where the join stops — in the file Q3 names as its owner, link it
from the other carriers, and give `templates/sdd-round.md` the sentence in the
**prose** about the same fields, never in the `Needs a fix` row
`seal/ledger.md:89` quotes as an anchor. A case in
`tests/test_the_rules_have_one_owner.py`'s shape, both halves seen red;
`evidence-check --strict` reporting 0 broken and the template row's hash
unchanged.

## What this phase found

**Q3's answer and the plan's acceptance criterion pull in different
directions, and the reading taken is written here rather than sent back.** Q3
option (b) closes with *neither needs a registry row*; `plan.md` phase 3 and
`spec.md` §*User scenarios* both ask for a case in
`tests/test_the_rules_have_one_owner.py`'s shape, *the owner states it, every
other carrier links it* — which is that file's registry.

The reading: *neither needs a registry row* means neither needs a row to
**reconcile the two rules**, because they are not one rule. The conformance
rule taken alone is one owner and two links, which is exactly what `RULES`
models, so it is entered as rule 11 with `PROTOCOL` as owner and `TEMPLATE`
and `WARDEN` as links. The operative rule gets no row; what keeps the two
apart is a second case,
`test_the_wrap_rule_is_two_rules_and_the_warden_keeps_the_operative_one`,
which asserts that the warden carries the blank-line instruction, that the
protocol carries the narrowing sentence, and that **the warden carries neither
the owner's sentence nor its enumeration of the three stops**. That third
assertion is what makes the split falsifiable rather than a claim in a
docstring.

**The template row `seal/ledger.md:89` anchors on is byte-identical.**
`evidence-check .` reports `1181 ok · 0 drifted · 0 broken`, exit 0, after the
prose addition. The new paragraph sits below the field prose, eleven lines
down from the row, inside the same HTML comment block the template's other
guidance lives in.

**Both halves were seen red by stashing, not asserted.** Six sentence-level
mutations, each turning exactly one case red: the protocol's owner sentence
(rule 11's owner case), the protocol's narrowing sentence (the split case),
the template's link and the warden's link (rule 11's link case, once each),
the warden's blank-line instruction, and putting the enumeration back into the
warden (the split case, both).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase only adds | none |
