# 1788873620-two-in-range-values-make-one-that-is-not — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b08bab4 |
| Ran by | `claude-opus-5` — filled by the orchestrator, read from the segment transcript's own message rows. The spawn prompt named no model, which is why the segment could not source this row itself |

## What this phase was asked

Build the class #192 leaves open, by the mechanism the owner chose: *a rule
that every site converting a derived number to an int carries a guard,
checked the way this repository already checks a class — by property rather
than by list.* Not the per-operation walk, because #192's own observation is
that round 3's defect came in through a call the existing site walk had held
in its list from the start.

Two boundaries came with it. The **wrong-number** direction — a finite but
nonsensical count summed as given — stays out of this branch and stays open
on #192's body; if the property makes it cheap, that goes to `questions.md`
rather than into the diff. And **do not write the number of sites into a
document or a docstring as the completeness argument**, which is the failure
0.9.3 is named for.

The case set was named as the three measured shapes in #192's table, already
planted by round 3 of #175 as
`tests/test_session_cost.py#test_a_sum_of_entered_values_does_not_end_the_report`.

## What this phase found

**The owner's wording had two halves, and only using both keeps the check
green on the module today.** *Converting a derived number **to** an int* is
two probes, not one. The first — does the site invoke one of Python's six
integer-conversion methods on its operand — is what makes the class
name-free. On its own it classifies `math.isfinite` as a member, because
CPython converts through `__index__` before it answers, which is exactly why
`math.isfinite` on an integer with no float of its own raises `OverflowError`
(round 2 of #175's 🔴). The module has two such calls: the one in `count`,
guarded by a `try`, and the one in `token_thirds`, where `mean` is a float by
construction — `sum(part) / len(part)` or `math.inf` — so the call cannot
raise. Membership on the first probe alone therefore reddens the shipped
module at a site that is safe, and the only ways out are dead defensive code
or a provenance pass. The second probe — does the callable answer a benign
number with an exact `int` — is the owner's own second half and it settles it:
a predicate that converts in order to answer a `bool` is not a conversion to
an int. That exclusion is asserted on both halves in a case of its own, so it
stays visible rather than incidental.

**Deriving the exception set removed the one arbitrary constant in the
design.** The first draft required a `try` guard to cover `OverflowError` and
`ValueError` because a derived value can be an infinity or a `NaN`. That pair
was written down, which is the shape this release exists to replace, and it
was also wrong for `count`'s `math.isfinite` guard, which catches
`OverflowError` alone and correctly. Probing the callable with each value
`count` admits and collecting what it raises answers the same question by
measurement, and it produces a third discharge for free: a conversion that
raises nothing needs no guard.

**A `TypeError` from a probe is the probe's own filler talking.** `round(3.0,
inf)` raises `TypeError` because `ndigits` must be an index, so a derived
value in that slot reports on the filler rather than on the conversion.
Excluded, with the limit stated in the same case: the filler cuts both ways,
so for a two-argument conversion the hazards come from the slot the probe can
still reach.

**Three shapes the property does not reach**, all measured while building and
none of them discovered by reading for them: a subscript bound (converts
through `__index__`, and telling a derived bound from `len(inputs) // 3`
needs provenance the walk does not have); a true division on two derived
integers (raises, converts nothing, and the wider *raises* predicate that
would catch it also flags `share`'s `part / whole * 100`, unguarded today
with duration operands — a behaviour change outside #192); and the
`math.isfinite` shape above. The first two are `questions.md` Q1 and Q2 for
the repository owner, and `token_thirds`' docstring carries both so a next
editor of that file meets them.

**The operator dimension is a derived no.** Every operator the module writes
is unparsed from its own node — no table of symbols, so nothing can fall
behind `ast` — and probed. No numeric operator reaches an int through an
operand: `//` and `%` build integers out of integers and convert none. A
positive control shows sequence repetition does convert, and that is the one
route a numeric probe cannot see; it stays unseen on purpose, because whether
an operand is a sequence is provenance, and probing with a sequence by
default would make `2 * third` a member.

**Where the case set actually sits.** The three measured shapes of #192's
table pass at HEAD and needed nothing: they were planted by round 3 of #175
and this branch re-runs them. The spawn prompt said they *pass at
`origin/release/v0.8.3`*, which the ticket's own table contradicts — at the
base all three exit 1 with stdout empty. Read as the cases passing after the
fix, and recorded in `overview.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
