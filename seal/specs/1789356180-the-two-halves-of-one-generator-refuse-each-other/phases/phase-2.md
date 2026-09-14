# 1789356180-the-two-halves-of-one-generator-refuse-each-other — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8fece68 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

What the fix pass's verdict vocabulary admits, settled once and stated in one
place. Q2's answer is (a): `docs/review-chain-spec.md` is corrected to the
spelling `agents/smith.md` already carries — verdict `answered`, correcting
commit in the Grounds cell — and
`tests/test_the_rules_have_one_owner.py#test_a_correction_row_closes_answered_and_never_fixed`,
which asserts both sentences today, is rewritten to assert one. A repair made
outside the tree gets a spelling and a document that names it (#321's comment).
`already deferred` is settled in the documents rather than in the vocabulary
(#273 part 2).

## What this phase found

**The disagreement is executed rather than read now.** `close` over a fix table
whose verdict cell reads `answered — corrected at <sha>` — the exact string
`docs/review-chain-spec.md` prescribed — exits 2 with

```
finding 1's verdict `answered — corrected at 6883bfb` is none of `fixed`,
`answered`, `deferred <home>` — the three a fix pass may hand over.
```

So both halves of #341's comment hold, and the cost is visible in the message:
a reader who followed the owner met a list of three words, one of which their
cell had begun with, and nothing said so.

**That is the one code change phase 2 needed, and the frame did not predict
it.** Q2(a) reads as a document correction, and four of the five cases planted
here were green before any edit — they pin the spelling `agents/smith.md`
already prescribed, which `fix_table` has always accepted. The live defect is
the refusal a reader meets when they type the other spelling, and `fix_table`
now has an arm for a verdict cell that BEGINS with `fixed` or `answered` and
carries a suffix. It names the two-cell shape and prints the row to write.
`deferred <home>` is handled above that arm and is untouched, because the home
is what makes a deferral readable.

**`already deferred` needed no vocabulary change and did need a sentence.**
`spec.md` §4 is right that no document tells a reviewer to put the phrase in a
Verdict cell, and that the two records which met the case wrote the two-cell
shape. What no document said is which cell it is NOT for — and a verdict cell
holding it reads OPEN, so the finding stays open, `close` demands a fix row,
and that row overwrites the reviewer's verdict. `agents/warden.md` now says it
at the paragraph that tells the reviewer to write the phrase at all.

**The rewritten case had to be narrowed twice.** The first spelling asserted
the one-cell string is absent from `docs/review-chain-spec.md` — which turned
red on the spec's own new paragraph explaining what the one cell cost. A pin
that blunt erases the history along with the rule, so it asserts the
prescribing clause is gone (`such a row closes …`) and that the correction is
present, and lets the spec name the old spelling in order to say it was wrong.

**One spelling asserted in both files is the repair, not one sentence per
file.** The case that let the two drift apart asserted a different string in
each. Both files are now checked against the same string, which is what a
later edit to either has to satisfy.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/review-chain-spec.md`'s prescription of `answered — corrected at <sha>` as one cell | the two-cell spelling, in the same section, which `agents/smith.md` already carried and `round_record.py#fix_table` already accepted |
| the half of `#test_a_correction_row_closes_answered_and_never_fixed` that asserted the one-cell spelling in the spec | the same case, asserting one spelling in both files plus the absence of the prescribing clause |
