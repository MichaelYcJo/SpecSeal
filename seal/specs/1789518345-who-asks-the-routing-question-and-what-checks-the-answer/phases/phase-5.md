# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | d177df33 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`round_record.py seal` writes `seal/specs/<id>/broad-gate.md` when `rounds/`
holds no record, and the last-record path is unchanged where one does.
`chain_check.py`'s `straight to the PR` arm reads that cell instead of printing
*nothing required* and returning.

It also decides `questions.md` Q4: can the `broad-gate.md` cell reuse the
existing cell reader, or does it need its own?

## What this phase found

**Q4 — one reader, and the surrounding record degrades correctly rather than
having to be worked around.** `chain_check.broad_gate` reads the cell out of
whatever file it is handed: `read_record` → `table_rows` → `field`. The only
thing it asks of the record around the cell is `Target SHA`, for the
premature-run comparison, and a `broad-gate.md` carries none — so
`SHA_RE.findall("")` is empty, the comparison loop never runs, and the
function falls through to its passing branch. **That absence is not a gap
being tolerated; it is the right answer.** With no round there is no reviewed
commit for a run to have been spent before. No field forced a split, so the
`plan.md` row stands as written and no second spelling of the cell exists.

**What the one reader could NOT answer is the file being absent**, and that is
the one thing the direct arm most needs. `read_record` returning None is
`broad_gate`'s *no claim* answer — correct for a record this pull request does
not touch, and silence for a seal that was never taken. So `direct_seal` is
the absence check and the delegation, nothing more.

**The cutoff `plan.md` gave only to phase 6 is needed here too, and the
measurement is the same shape.** 16 declarations in this tree answer `straight
to the PR` and not one carries a `broad-gate.md`, because the file did not
exist. A release pull request carries every work item the release adds, so an
arm with no cutoff refuses a release for work nobody could have sealed.
`DIRECT_GATE_FROM` is this work item's id, matching `GATE_FROM`'s spelling.
**This is scope phase 5 took that its plan row did not name**, and it is
recorded rather than left: shipping one arm with the mechanism and its twin
without it is the near-identical-copy-missing-one-half failure this repository
keeps recording.

**`item_began` answered None for the new path, which is the grandfathered
answer — so the cutoff would have been off for the whole arm, silently.** It
reads `parts[-3]`, which is the work item's id in
`<item>/rounds/round-N.md` and the literal string `specs` in
`<item>/broad-gate.md`. Measured directly: the first run of the `not yet` case
above the cutoff exited 0 with the notice quoting **1788912166**, the chain
path's constant, on a work item begun at 1789518345. The repair is
`item_began_at(item)`, the rule one level up, with `item_began` delegating to
it — one rule, two depths — and `broad_gate` taking `began`, `floor` and
`excused` as parameters rather than reading a constant it cannot know the
right one of.

**The sentinel for `began` is `False`, not `None`.** `None` is a legal value
that MEANS grandfathered — a repository naming its work items some other way
has no date to compare — so `None` cannot also mean *derive it yourself*.
Collapsing the two is the same failure one layer down from the one above.

**Three refusals in `seal` are questions about a round that ran, and a work
item that ran none answers all three by having no round.** `Pass`, `Fixes
checked by` and `Target SHA` are skipped where `n is None`. The pair below
them is NOT skipped — the cell must still carry a SHA-shaped word and that SHA
must still resolve here — because those are about the RUN rather than about
the review. That split is what keeps the new home from being a cheaper way to
write an unverifiable cell.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `chain_check.py`'s *straight to the PR — declared, nothing required* and the `continue` that followed it | the same arm, which now prints that no ROUND RECORD is required and then reads the seal. The sentence was true about the reviewer and false about the sealer, and the `continue` is what made the falsehood unobservable |
| `seal`'s unconditional `last_record` call | `seal_home`, which picks the home from what exists. `last_record` itself is kept and still raises: a work item whose rounds are running and whose records are not written yet is a different state, and the two cannot be told apart from inside this function |
| `item_began`'s `parts[-3]` read and its `len(parts) < 3` guard | `item_began_at(item)`, with `item_began` delegating. One rule, two depths — and the guard's job is done by the last segment not being a number, which is what it was really testing |
