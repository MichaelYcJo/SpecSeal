# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `fcf53fd` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

#342. `close --round N-1` reaches forward into `round-N.md`'s
`## Inherited coordinates` and brings the rows inherited from round N-1 to the
words that round's verdict cells now carry, printing what it filled the way it
already prints `Contract changes` and `New units`. It refuses rather than
guesses where the record is unreadable or the rows are absent, and says nothing
where round N does not exist yet. A two-record fixture: close N-1, read N,
assert the words agree — red against the tree today.

## What this phase found

**The reach is built before either write, and that is not a detail.** Every
refusal in `close` lands with nothing on disk changed, and a reach that wrote
round N-1 first and then refused over round N would break that sentence for the
one refusal a reader is most likely to meet. So the forward pass is computed
from `rows` and `words` — which `close` already holds — validated, and only then
are the two records written, round N-1 first because round N's rows are only
true once it has landed.

**What the caller hands over is `{Location cell: (`#` cell, verdict word)}`,
not the record.** Re-reading round N-1 from disk to recompute the words would
give the reach a second source of truth for the thing it is copying, which is
the property that makes the whole defect possible one file over.

**Three refusals were considered and two were taken.** A next record with no
readable `## Inherited coordinates`, and a row naming a coordinate round N-1's
verdict table does not hold — both refuse. The third, *round N+1 exists and its
table names no row from round N*, also refuses: `new` writes one row per
`Location` cell of every earlier record, so a table with nothing from round N in
it is one this round's verdicts cannot be carried into. Each says *no cell was
written*, which is true because nothing has been.

**Silence is the fourth state and it is the common one.** In every ordinary run
the fix pass comes first and the verifying round is spawned after it, so
`round-{N+1}.md` does not exist. A reach that refused there would stop the run
it exists to keep truthful, and its case is the one that says so.

**A case here could not assert an exit code, and the reason is worth writing
down.** `test_the_reach_forward_says_nothing_where_the_next_round_does_not_exist`
runs `close` over a one-record run whose fixes no later round has read, which
`chain_check` refuses on its own grounds at exit 1. That verdict is a different
question with its own cases, so the case asserts the printed line — that `close`
wrote its record, said nothing about the reach, and refused nothing. Written as
`assert code in (0, 1)` it would have been the hedge round 4's 🟡 4 objected to;
asserting the line is the narrower claim.

**§14 reached the template rather than the spec.** The `Why` cell is now
written twice by two commands, and the second is not the command that owns the
section — so `templates/sdd-round.md`'s `## Inherited coordinates` comment says
who fills it the second time, what the two refusals are, and that it is silent
where round N does not exist. `docs/review-chain-spec.md` carries no description
of this section at all, which is why the sentence went to the template.

**Q4's answer for this phase.** One anchor drifted, `round_record.py#close`,
carried by `seal/ledger.md` R2 and by this work item's own fragment. R2 holds:
its sentence is *every refusal comes before any cell is written*, and both of
the reach's refusals are built before either write. `evidence-check --strict`
exit 0 at 1254 ok · 0 drifted · 0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Nothing. The reach adds a pass and two refusals and takes nothing out — `inherited_rows` still writes the row, `reach_back` still sets `Fixes checked by`, and the `Why` cell's format is unchanged | — |
