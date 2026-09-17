# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 2f35376e |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The bootstrap asks for the row in the same question as the mode.
`skills/implement/orchestration.md` §*Orchestrator: Bootstrap* step 1 carries
a second question in the one `AskUserQuestion`: candidates read off the
repository and offered, never guessed (the parity-setup shape), a decline that
says what it costs, and the criterion named by pointer. The row is written
after `seal mode`, the way `/specseal:config` step 3 already writes one — the
row **and its section**. Red first by reverting the Bootstrap edit.

## What this phase found

**Q4, answered, and the answer has an order.** Four sources, and the first is
the one the plan did not name: `.github/workflows/*.yml`. What CI already
refuses a pull request for is the repository's own answer to this question,
written down before anybody asked it, and it beats a `Makefile` target for the
same reason a measurement beats a guess. Then a runner under `bin/`, then a
package manifest, then a `Makefile`. Each candidate is offered **with the file
it came from**, which is what makes it correctable — a proposal whose source
is not named is a guess with better manners.

**Where nothing is findable, the answer is to say so.** The floor is at least
one derived candidate *where one is findable*, and offering a plausible
command with an invented source is worse than offering none: it is exactly the
row nobody chose that `templates/config.md` §*Broad gate* argues against by
name. The section says this rather than leaving it to be inferred.

**The question count is what changed, not the call count.** The bootstrap
still opens exactly one `AskUserQuestion`; it now carries two questions. A
case asserts `boot.count("AskUserQuestion") == 1`, because a second call after
the first is a second wait for one decision, and a new prompt owes
`CONTRIBUTING.md`'s budget an argument. This owes none: the prompt budget is
unchanged and the number of new interruptions is zero.

**The decline writes nothing at all, and the asymmetry with the mode row is
argued rather than asserted.** The mode row records its answer because #151
measured what its absence costs — a never-asked repository got shared mode
*silently*. Nothing about this row is silent: a repository that declined and
one that was never asked meet the same refusal at the same moment and are told
the same correct thing, so a trace would separate two states nothing treats
differently, and would add a writer and a way for that writer to go stale.

**Ten mutations, all red — after one was not.** The loop's needles are
literal, and three of them span a hand-wrap, which is a trap for any later
session driving the same kind of check: `lands after\n   the review rounds
have settled` matches where the flat phrase does not. The case itself reads
through `flat()` and is unaffected.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the Bootstrap gains a question and the recording step gains a paragraph | none |
