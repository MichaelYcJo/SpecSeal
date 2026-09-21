# 1789996780-the-census-and-the-tie-that-nothing-holds — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ecca19b9 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#471. Plant `test_a_tie_falls_to_the_first_parent` from round 3's paste-ready
text, beside `test_the_parent_named_is_the_one_that_lost_the_most`. Green on
shipped code, red on the mutation that walks the parents in reversed order,
both runs recorded (A8, `agent-contract` §15).

## What this phase found

**The mutation reproduces round 3's measurement digit for digit.** Round 3
reported that rebuilding `carried` in any other order leaves 48 of 48 green.
Changing `for parent in kin:` to `for parent in reversed(kin):` in `examine`
reddened exactly the new case — `48 passed, 1 failed` — and the failure
printed the second parent's SHA where the first parent's was asserted. That is
the whole of the finding: the module had 48 cases and none of them could tell
which of two SHAs a reader is sent to open.

**The tie is not produced by an even loss count alone; the fixture has to make
both parents carry the marker.** The shipped case above it gives `ours` the
marker in two cells and `theirs` in one, so the two sides lose different
amounts and `max` has a winner on the merits. Round 3's fixture gives both
sides one occurrence each and differs only in the last cell, so `by_parent`
holds two entries of length one and `max` falls through to insertion order.
That last-cell difference is load-bearing: without it the two parents' texts
are identical, git finds no conflict, and the fixture stops constructing the
shape the case is about.

**The tie behaviour is a property of `max` over a dict, not of anything
written down in the module.** `by_parent` is built by iterating `kin`, and
`max` returns the first of equal keys in iteration order. Nothing in the code
names the first parent; the comment above it does. That is exactly the shape
`agent-contract` §14 is about — a sentence a person reads and acts on, held by
an implementation detail of a builtin — and it is why the case asserts the
negative (`from parent <second>` **not** in the output) as well as the
positive.

**Restored from bytes kept outside git.** The module was copied to the
scratchpad before the mutation and restored with `cp`, never `git checkout`,
and both hashes were compared (`af6ea4f4…`). `tests/__pycache__` was cleared
on both sides of the mutation.

## What this phase removes

Nothing. The phase adds one case and changes no shipped sentence; the two
clauses of the parent-naming rule both stand, and this is the second of them
acquiring something that holds it.
