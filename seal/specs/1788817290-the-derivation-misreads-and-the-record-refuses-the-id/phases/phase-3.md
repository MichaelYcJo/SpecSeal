# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 58c7ce2 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#194, with its design decision already made by the repository owner and
closed to reopening: **literal-set comparison plus a stated hole.** Flag a
unit whose set of returned constant literals changed, and write the shape
this does NOT catch — a changed input→value mapping — into
`docs/review-chain-spec.md` as a paragraph. Documentation alone had been
refused as a floor rather than an answer. The paragraph must not stand in for
the check, and the check must not be quietly widened to try to cover the hole:
a stated hole is the deliverable.

The handoff also required the class to be enumerated by construction — derive
by AST the set of units whose returnable literals changed across a real diff,
and check that against what the implementation reports.

## What this phase found

**The row's own template had already promised this half.**
`templates/sdd-round.md` describes `Contract changes` as *signature, return
arity, return type, or set of returnable values*, and so do
`skills/code-review/SKILL.md`, `chain_check.py`'s header and
`docs/review-handoff-protocol.md`. Four documents promised the fourth thing
and the derivation delivered two. That reframes the change: it closes a gap
between the documents and the code rather than adding a rule to both.

**Literals have to be keyed by type as well as value, and nothing in the
ticket says so.** Python hashes `0` and `False` into one key, and `1` and
`True` likewise, so a plain set of values reads a unit that swapped a count
for a flag as unchanged. `(type name, repr)` costs one tuple and keeps them
apart; three of the 21 constructed pairs exist for exactly that.

**A real instance the old contract missed, found by the probe the handoff
asked for.** Across `v0.8.0..v0.8.3`,
`skills/code-review/scripts/chain_check.py#read_record` began returning an
explicit `None` — literals `{}` → `{None}` — with signature and arity
unchanged. The old two-element contract read it as unchanged; the new one
reports it. Two other real spans held no member, and containment on those
proves nothing, which is why only the first is cited.

**The cross-check is two halves, and only one of them is independent.**
Round 1's finding 4 is that this paragraph used to call both halves a second
implementation. The whole-tree comparison runs `literals_of` over every
top-level def in every tracked `.py` file, and `literals_of` is the shipped
`return_literals` loop character for character apart from the order of one
assignment — two copies of one algorithm agree by construction, so what that
half catches is a later edit to one of them, not a blind spot in both. It
also asserts how many units carry a literal at all, so a derivation that
always answered the empty set could not pass it.

The half that could have caught a blind spot is the 21 constructed pairs,
whose expectation column is a hand-written statement of what should be
reported per shape rather than a reading of the code, and it is where the
nested-scope boundaries and the bare `return` are pinned. That is the half
the eight measured instances of a class enumerated by reading argue for.

**The hole is pinned as a hole.** `test_the_hole_is_a_hole_and_not_a_claim`
rebuilds `is_a_record_of_a_moment` from its two ends and asserts the contract
is UNCHANGED — so the case goes red the day somebody widens the check and
leaves the paragraph standing. That is the only way a stated limit can be
kept honest by a machine rather than by a reader's memory.

**One surviving mutation is equivalent and is not a gap.** Dropping the
`n.value is not None` guard changes nothing: `isinstance(None, ast.Constant)`
is false, so the loop adds no literal either way. The guard stays for what it
says rather than for what it does.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the two-element contract tuple `(signature, return arities)` | nowhere it was read from outside `measure`, which compares it whole; the third element is additive and every case that passed on signature or arity alone still passes, pinned by `test_the_signature_and_arity_halves_are_untouched` |
| the standing gap between four documents promising *set of returnable values* and a derivation that compared two things | into the code. What is left in its place is the opposite kind of statement — a limit the documents now carry that the code cannot reach, in `docs/review-chain-spec.md` and `docs/review-handoff-protocol.md`, so a conforming tool is not promised more than any implementation can give |
