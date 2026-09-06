# 1788700685-two-value-shaped-odd-rows-end-the-report — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | <the commit that closes this phase> |
| Ran by | <the orchestrator fills this — the spawning session is the only party that knows> |

## What this phase was asked

The records and the ledger, and no code. Five things, of which the first is a
judgment the phase was told not to take on the issue's word.

1. **#170's ledger row in `seal/ledger.md`.** Its guarantee is stated over the
   whole class — *one odd row must not end the report* — and its enumeration
   ran on the **type** axis alone. Judge first whether the row is **falsified**
   (a removal, per this repository's rule) or **under-specified** (the axis
   named in place), and say which and on what grounds.
2. **This work item's own fragment**, for the claims phase 1 established: the
   normalisation, the non-positive-span guard, and the enumeration's two axes.
3. **`count`'s residual has to survive this phase.** It is on #170's own axis,
   so whatever is written about that row has to leave room for it rather than
   closing it by wording. Check the rider is still there and still stamped.
4. **The records** — the changelog fragment, this file, `plan.md`'s Status
   cell, and `overview.md`, whose `## Not verified` section is read by a
   machine and has one shape.
5. **`docs/flow.md`** — the row for #175 only, ticked; #180 and #182 are other
   branches' to write.

And: correct the record where phase 1 measured the issue wrong. Two of its
findings contradict documents now in the tree — the naive stamp raises on an
**ordering** rather than on a subtraction, and the counts are six subtractions
and three divisions rather than four of each — and both belong in
`overview.md`'s divergence table with both sides quoted.

## What this phase found

### #170's row is under-specified, and the grounds are a measurement rather than a reading

The instruction was not to take the issue's word for it, so the deciding fact
was measured. `seal/ledger.md`'s R6 records the construction that grounds its
guarantee: *every field the two readers read, taken from `grep '\.get('` rather
than from memory, crossed with all seven types JSON can carry AND with the
field being absent — 288 variants*. A probe ran that construction on the one
field the naive stamp lives in, against the module R6 was stamped against
(`6863669`, byte-identical to 0.8.2's):

| `timestamp` written as | Old module |
|---|---|
| a non-ISO string · a number · `true` · `false` · `null` · an array · an object · the field removed | **exit 0**, 296 bytes, all eight |
| a valid ISO stamp with no zone, one call | exit 1, stdout empty, `TypeError: can't subtract offset-naive and offset-aware datetimes` |
| a valid ISO stamp with no zone, two calls | exit 1, stdout empty, `TypeError: can't **compare** offset-naive and offset-aware datetimes` |
| two stamps that are equal | exit 1 after **36 bytes**; `--json` on the same file, exit 0, 491 bytes |

That is the whole judgment. The enumeration's axis closes at exit 0 on every
one of its own eight variants, and the two shapes that end the report are
values of the type the field already carries — a naive ISO stamp is a `str`
exactly as an aware one is. They are outside the cross product **by
construction**, not members it missed.

So the three tests point one way:

- **Are the anchors gone?** No. `evidence-check` unscoped reports 0 broken and
  every anchor R6 cites resolves. This repository's removal rule fires when a
  change takes an anchor's code out of the tree; nothing was removed.
- **Is the mechanism false?** No. The four funnels still type-check, and phase
  1 ADDED to two of them — `parse_time` gained the normalisation, `count`
  gained the rider.
- **Is the reach over-stated?** Yes, and only that. *No shape a harness can
  write ends the report* was false as a universal on the day it was written,
  which the middle rows above measure directly.

A claim whose grounds are sound and whose scope is stated wider than those
grounds is under-specified. The repair is the axis named where the row is, and
the row now says which axis its 288 variants ran and what a value of an
already-correct type does instead — with the second axis pointed at this work
item's fragment.

**Removal would have destroyed the useful half.** R6's durable content is the
method — *the enumeration is what turns "I looked and found no more" into a
number a later session can re-run and compare* — and that method is exactly
what phase 1 re-ran to find these two. A row deleted for being narrow would
take its own reproduction instructions with it.

### The residual survives the wording, on purpose

`count`'s rider stands at `skills/verify/scripts/session_cost.py`, stamped
`Verified 2026-09-06 at b0e4859`, and `tests/test_a_rider_reaches_its_file.py`
passes at 8. `NaN` and `Infinity` are `float` values of a field whose JSON type
is a number — the value half of the same axis R6 was narrowed to the type half
of. So the narrowed row does not touch them: it now claims the type axis, and
names the open member explicitly rather than leaving a reader to infer that
*no member survived* has an exception. Had the row instead been re-asserted
over the class with two more members ticked off, the rider would have been
contradicted by the document a reader reaches first.

### The two axis vocabularies sit at different levels, and the fragment says so

`phases/phase-1.md`'s decomposition table files naive-beside-aware under the
**type** sub-axis, because a `datetime` carries its zone in its type. R6's
enumeration ran one level up, over the JSON type each **field** carries, where
a naive stamp and an aware one are both `str`. Both are correct at their own
level and a row saying only "the type axis" would be read at whichever level
the reader arrived from, so the corrected row names *the type each field
carries* and the fragment's header comment states the two-level reading
outright.

### The ledger read, before and after

`./bin/evidence-check .` unscoped, at `e8ef34d` before any edit: **677 ok · 4
drifted · 0 broken**, exit 1. The four are `templates/config.md#"# Repository
config"`, `session_cost.py#count`, `session_cost.py#parse_time`, and
`round_record.py#swallowed`.

After: **708 ok · 2 drifted · 0 broken**, exit 1 — the fragment's 7 rows added
and the two anchors this branch drifted re-stamped. **The remaining two are
not this branch's and were left alone.** They predate it by construction: phase
1's only code commit touches `session_cost.py` and `tests/test_session_cost.py`
and neither of those files, and the first unscoped run above already carried
them. Whether their claims are still true is a re-reading somebody else owes;
it is in `overview.md`'s Not verified with an answerer.

Neither was re-stamped by the scoped write, because `--reverify` narrows to a
file and `seal/ledger.md` holds two anchors nobody here has read. Instead the
two hashes this branch owed were taken from the tool's own output for the SAME
anchors in this work item's fragment, where R1 and R3 cite them —
`parse_time` `37cc8192` and `count` `a29bae9b`. The method is checkable rather
than asserted: the fragment also cites `load`, and the value the tool computed
for it there, `d7f90cd4`, is the value `seal/ledger.md` already carried for
that anchor from before this branch existed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| R6's claim to the whole class — *no shape a harness can write ends the report* — narrowed to the axis its own enumeration ran | The second axis is `seal/ledger/1788700685-two-value-shaped-odd-rows-end-the-report.md` R3, which carries the decomposition and the one member left open; the open member itself is the stamped `# RIDER:` at `count` |
