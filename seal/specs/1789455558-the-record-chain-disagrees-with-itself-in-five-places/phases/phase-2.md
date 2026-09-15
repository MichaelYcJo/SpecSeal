# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 2

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `38521a2` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#405. The unconditional silence at `filled == 0` becomes a refusal where
round N+1's inherited table does not account for every coordinate of round N,
naming the unaccounted ones, with nothing written to either record. Q3's
corpus measurement runs **first** and decides the predicate: unconditional if
the corpus produces no unaccounted pair, narrowed to `filled == 0` if it
produces any, with the shape that forced the narrowing recorded.

Verified by `bin/test tests/test_the_fixes_close_the_record.py`, red-first by
deleting the accounting, with
`test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused`
re-run green in the opposite direction and both records asserted
byte-identical after the refused run.

## What this phase found

**Q3, measured 2026-09-15 at `14b617c`, over every committed
`round-N`/`round-N+1` pair under `seal/specs/`.** 139 pairs are readable on
both sides. The accounting applied to **every** run would refuse **65 of
them**, so the measurement's own rule decides it: **narrowed to
`filled == 0`**, which is what shipped.

The split is what makes the narrowing a decision rather than a retreat.
Leaving out the 15 pairs the standing *a coordinate round N's table lacks*
refusal already stops:

| Shape | Pairs | Unconditional | Narrowed |
|---|---|---|---|
| `filled > 0`, every coordinate accounted | 74 | silent | silent |
| `filled > 0`, some coordinate unaccounted | 2 | **refused** | silent |
| `filled == 0`, some coordinate unaccounted | 48 | refused | refused |
| `filled == 0`, every coordinate accounted | 0 | silent | silent |

**The two pairs are the whole difference, and both are the shape the plan's
alternatives table predicted.** `1788272986` round 2 and `1788433011` round 2
each have a next round whose `## Inherited coordinates` was written **by
hand** — one row, `| round-2 | … | closed this round |`, where the round
before it carried three coordinates. The row is correct as far as it goes and
the section was never truncated; it was simply never generated. Refusing that
is the reader sent to correct a table that is not wrong, which is the failure
the removed refusal was removed for.

**The 48 are refused under either rule, so they do not discriminate**, and
they are worth naming anyway: every one of them has a next round whose
section predates the generator, in a different spelling entirely
(`| round 1 🔴 1 | \`chain_check.py\` \`verdict_of\` | … |`). Nobody re-runs
`close` against a merged record, so the compatibility break is narrower than
the count reads — but a live run that meets a hand-written section with no
row from round N in it will now be refused, and that is indistinguishable
from the truncation #405 is about. Recorded rather than designed around.

**The fourth row is zero, and that is the surprise.** The shape the silence
was introduced for — a re-review round whose every coordinate an earlier
round already claimed — **appears in no committed pair at all**. The case
that pins it (`…_claimed_is_not_refused`) is the only place it exists, which
is one more reason the narrowing had to keep it: the corpus could not have
caught a regression there.

**The accounting reads the whole `Coordinate` column, not the `round-N`
rows.** `inherited_rows` is first-seen-wins across rounds, so round N's own
coordinates sit under round N or under whichever earlier round claimed them
first. A phase that read only the `round-N` rows would have refused every
re-review round, which is the state this work is repairing away from.

**A divergence from `plan.md` §Operational impact, and it is the narrowing's
shadow.** That section says a table *edited or truncated since `new` wrote
it* now exits 2 where it exited 0. What shipped is narrower: a table that
lost rows **and** names no row from round N at all. A table that lost some of
its rows and kept one of round N's still passes. That is the 2-pair row of
the table above, traded away on purpose.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `reach_forward` docstring's claim that an empty fill is silent because it is the re-review shape — the claim is now conditional on the accounting | The same docstring, in the paragraph beneath it, and the comment at the `if not filled` arm |
