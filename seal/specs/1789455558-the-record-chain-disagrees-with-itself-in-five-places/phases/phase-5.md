# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 5

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `f119f72` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#406. Delete `assert "the seal" not in out` from
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, and reword the seal
refusal's exit sentence to name the sealer. Class: `grep -rn '"the seal" not
in' tests/ skills/` re-run and the enumeration recorded.

Verified by `bin/test tests/test_one_word_one_meaning.py
tests/test_the_seal_is_taken_once_by_the_sealer.py`, red-first by rewording
that sentence to leave the seal anonymous — which has to turn
`test_no_instructing_document_leaves_an_instance_anonymous` red, naming the
module and the span, because that is what proves the sweep rather than the
deleted pin is holding the rule.

## What this phase found

**The class is one member, re-measured.** `grep -rn '"the seal" not in'` over
`tests/`, `skills/`, `agents/` and `docs/` returns the one occurrence the
issue named and nothing else.

<!-- CORRECTED by round 1's 🟡 2, 2026-09-16. The claim in this paragraph is
false as written and the paragraph is left standing, because a phase record states what
was true when it was written. The sweep reads flattened SOURCE and the deleted
assertion read the run's OUTPUT; Python joins adjacent string literals where a
flattened read does not, so an anonymous instance split across two literals was
invisible to the sweep. Round 1 kept the pinned spelling, added such an
instance, and both modules stayed green. `flat` folds the literal seam now
(`20359325`), which restores the coverage inside the one check — and found a live
instance in `round_record.py` the moment it could see one. -->

**The deletion loses no coverage, and the reason is a fact this phase opened
rather than took from the issue.** `SEAL_SWEPT` in
`tests/test_one_word_one_meaning.py` lists
`("skills", "code-review", "scripts", "round_record.py")` — the module the
refusal text lives in. So the sweep already reads this sentence. What went is
a second, stricter reading of one rule, held by a check that is not the
rule's owner: the sweep skips a hit whose next character is a letter, and the
deleted assertion did not, so it refused `the sealer`.

**The two positive pins beside it stay**, and they are what keeps §14's
requirement on this refusal met inside the module a reader of it opens:
`the only value \`seal\` accepts` and `` `seal` runs with `Pass` ticked ``. A
third now joins them, `before the sealer runs`, which is the opposite
direction of #406 stated as a pin: the spelling the deleted assertion turned
red is the one the case now requires.

**The case's docstring asserted something false and it was rewritten rather
than left.** It read *this file is not swept, so the pin is what would have
kept the old wording alive* — true of the test module, and beside the point,
because what the sweep reads is `round_record.py`, where the sentence is. A
docstring is a claim like any other and this one would have argued the
deletion back in.

**The red-first run is the phase's whole evidence**, because deleting an
assertion cannot be seen red by anything. Rewording the exit to *before the
seal runs* turned the sweep red with
`skills/code-review/scripts/round_record.py says \`the seal\` and leaves the
instance anonymous`, quoting the span. That is the rule still held, by one
check instead of two.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `assert "the seal" not in out` — the second, stricter reading of the *name whose* rule | `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous`, which already sweeps `round_record.py` and is what `CLAUDE.md` names as the check for that rule |
| The docstring sentence claiming the module is not swept | The same docstring, rewritten with the `SEAL_SWEPT` membership stated |
