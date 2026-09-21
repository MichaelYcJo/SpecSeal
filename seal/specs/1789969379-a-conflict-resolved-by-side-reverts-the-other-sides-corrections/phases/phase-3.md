# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 99948792 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Fragments, and the empty case. A4 and A5, with A5 asserting that the cheap
path says it looked at no merges, so the common case cannot silently pass by
doing nothing.

## What this phase found

**A4 and A5 were already green when this phase opened, and that is not the
same as being held.** Fragments were watched from the first commit — the plan
said to, and building it the other way would have meant taking it out again —
and the report's empty-range branch was written in phase 2. So what this
phase actually delivers for both rows is the case, and each was driven red by
a mutation of the thing it is about: the glob renamed away from
`seal/ledger/`, and the empty-range sentence emptied. Without those two
mutations the rows would have shipped asserted and unproven, which is exactly
what `agent-contract` §15 says has happened three work items running.

**The mutation sweep found a real pass this had not earned.** `read_blobs`
returns a blob it could not decode — over the size cap, or holding a NUL byte
— as ABSENT rather than as the empty string, and the docstring said why. But
nothing downstream acted on the difference: an absent result blob read as a
ledger with no rows, every row then failed the survival test, and the run
printed *no correction marker was dropped at a merge*. A ledger too big to
read was a pass, which is `skills/verify/SKILL.md` §*The Seal Test* exactly.

The repair is that the listing is now **per rev** rather than a union. A path
a rev does not carry and a path whose blob did not come back are different
facts, and only the union collapses them. A path listed at a rev whose blob
is missing is named under `not judged` with the revs it could not be read at,
and the case lowers `SIZE_CAP` to drive it.

**`not judged` prints and does not refuse.** The same line now carries two
causes — a merge whose parents share no history, and a blob that could not be
read — and neither exits non-zero. Refusing the whole run over one unreadable
blob would turn a check about corrections into a check about file sizes, and
the precedent is `survivor_check.py`'s `unresolved` rows, which print and
silence nothing. What keeps that honest is that the line is printed at all:
the failure this is about is silence, not a wrong exit code.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `ledger_paths`, which returned the union of every rev's ledger paths | `ledger_listing`, which returns the same paths per rev — the union is still taken, one line later, and the per-rev listing is what the unreadable-blob report needs |
