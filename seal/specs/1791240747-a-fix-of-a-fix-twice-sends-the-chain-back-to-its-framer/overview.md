# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — overview

📋 implement applied
· spec:     pending — filled when the build closes
· evidence: pending — filled when the build closes
· verified: pending — filled when the build closes

## Why this work exists

A fix pass whose fix is itself the next round's finding, twice in one run, now stops the fix passes mechanically and sends the work item back to its framer, where it used to run on until a person noticed.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the unit's AST is kept | `plan.md` phase 1: "`top_units` keeps enough of each node to compare ASTs between ends" / the code adds `round_record.py#unit_dumps`, a separate reading keyed to the same names | code | `top_units`' value is a three-tuple a dozen call sites unpack; a fourth element moves all of them for a reading only `fix_pass_units` makes |
| Whether `New units` is read | `spec.md` §*The reading*: "that unit is named by round K-1's `New units`, or is present at both ends … with a different AST" / the code derives the added units from the range's two ends and does not read the row | code | `close` writes `New units` from exactly the units present at `b` and absent at `a`; the ends give the same set with the path the row lacks, so a name two files share cannot land in the wrong file. The two differ only for a hand-edited row (inferred during implementation) |
| The arm's signature | `spec.md` §Data & interfaces: "`fix_of_a_fix(reader, root, rel, earlier, later)`" / the code takes `(reader, root, rel, earlier, stopped)` | code | none of the gate table's eight rows reads the records after this one, and the resumption row needs the `second` the run began after |

## Not verified

| Item | Who must answer |
|---|---|
| pending — filled when the build closes | the smith, at phase 4 |

## Not done

Pending — filled when the build closes.

## Fed back into the spec

Pending — filled when the build closes.
