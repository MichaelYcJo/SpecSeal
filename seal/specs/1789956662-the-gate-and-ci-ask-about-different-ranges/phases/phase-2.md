# 1789956662-the-gate-and-ci-ask-about-different-ranges — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c674ac26 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`gate()` resolves once and all six consumers take the resolved commit.
`args.base` is read exactly once in the file. A1 and A2 end to end on a
behind-base fixture, red against the gate as it stands; A3 —
`tests/test_the_seal_is_taken_once_by_the_sealer.py` green with nothing
edited in it; A10 still green; and the structural case counting the reads of
`args.base`.

## What this phase found

**`args.base` was read seven times, not six.** `spec.md` §*The class,
enumerated by construction* enumerates six CONSUMERS and the count is of
READS — the seventh is the refusal sentence for a base that does not resolve,
which quotes the spelling rather than consuming it. The table is right about
the consumers and the number is not the table's number. The case asserts one
read, which is the property that matters, and the refusal now quotes
`base.given` from the resolver instead.

**A3 did not hold whole, and the one case that moved is a defect this work
repairs rather than a cost it pays.** The `Broad gate` cell's base half was
the ref AS TYPED:

```
old   2cc9f1a against base
new   2cc9f1a against b9cdec0
```

`spec.md` §*Out, and why each* says of that cell *The cell already names
commits, which is the property #423's comment asks for* — true of the tree
half and false of the base half, which is the half #423's comment is about.
So `test_the_gate_with_record_seals_the_item_and_counts_its_rounds` asserted
the ref and now asserts the commit. Everything else in that module is
untouched: 119 of its 121 cases never went red at all, and the second failure
was my own — `panel` was still being handed the `Base` object.

**Neither parser of that cell sees the change.** `chain_check.broad_gate`
takes `SHA_RE.findall(cell)[0]`, and `round_record.py seal` refuses a cell
with no SHA-shaped word. Both read the FIRST one, which is the tree, so the
base half moving from a word to a hash is invisible to them. Measured by
running both modules, not inferred.

**The base comparison is pinned by the count and by nothing behavioural.**
`compare_at_base` runs only when the repository's command fails AND names
failing test files, so no case reaches it with a behind base. Routing it back
to `args.base` turns exactly one case red — the structural count — which is
what `spec.md` means by *the closure is structural, not a list*. Worth
knowing before somebody reads that single red as a weak pin.

**`not_sealed` took the resolved commit in this phase although A7 is phase
3's row**, because `base` is a `Base` from the resolution onward and the
failure form needs a string. A7's case is therefore written in phase 3 and
shown red by mutating that one argument back, rather than against the
pre-phase tree.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the six unresolved reads of `args.base` in `gate()` | `resolve_base`, at the one read that remains — and the count case is what keeps them from coming back |
| the `Broad gate` cell's base written as a ref | the same cell, now the commit; `phases/phase-2.md` above and `overview.md` carry why |
