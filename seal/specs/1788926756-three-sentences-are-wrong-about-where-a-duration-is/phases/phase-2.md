# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `be5bc18` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Items 1 and 2 — the refusal names the cut its row ends at, and prints both
sums rather than their difference — **re-read against phase 1's rule and
taken from #145's round-3 report where it still holds.** Verified by the
report's own case, seen red first, and the `outside == 0` boundary case still
green.

The prompt was explicit that pasting the report's text unchanged is the
failure: both prior fix passes on this file correctly refused to paste a
reviewer's text, twice, and the record kept both refusals.

## What this phase found

**What I took from the report, unchanged.** Both halves of the fix itself.
Naming *the cut its row ends at* rather than *a spawn's result* is still
right — phase 1 did not touch `spawn_cuts`, so the head row's cut is still
the first spawn's start. Printing the two sums rather than their difference
is still right — `minutes` is still one decimal, so the rounding is
untouched. The report's case for item 1 also survives intact: its numbers
(`sum to 0.2m against the run's own 0.2m`) are identical under both rules,
which I recomputed rather than assumed.

**What I refused, and why.** The report's grounds for not naming the figure
an overlap:

> `analyse` takes a span as the last call TO BEGIN's end minus the first
> call's start, so an outliving call shortens the RUN's span too and the
> difference carries both errors.

Phase 1 removed that. The run's span is now correct, so the difference no
longer carries the span's own error. The conclusion survives on new grounds:
a row's span and the run's both end at the last call to end, so **every row's
interval is a subinterval of the run's**, and the difference is the gaps
between the rows *minus* their overlap. A negative one is the overlap net of
the gaps. On the pinned fixture the head row covers the whole run, so there
are no gaps and the 987s does equal the overlap — which is precisely why
naming it the overlap would be a claim that holds on that fixture and fails
in general.

**One consequence nothing had named: the refusal can no longer fire on one
row.** It used to — the head row's span reached 1000s against a run of 995s,
so a single row passed the whole run by itself. With every row's interval
inside the run's, a sum past the run requires two rows covering the same
seconds. That is the prompt's *strictly less often*, now with the reason
under it.

**Two numbers moved and both are in the report's text.** The pinned shape's
run span is 16.7m rather than 16.6m and the magnitude 16.4m rather than
16.5m, so the report's paste-ready assertion
`"the rows' spans sum to 33.1m against the run's own 16.6m"` is wrong by one
decimal place. Anything copied from that report has to be recomputed.

**The exact-cover boundary the spec names had no case.** `spec.md`'s third
scenario cites *the existing boundary case, still green*; the only existing
one covers the positive branch at `outside == 304`. The `>= 0` versus `> 0`
choice — an exact cover reading as the partition agreeing rather than as a
refusal — was unpinned, and #145's round 3 had only probed it. Planted as
`test_an_exact_cover_reads_as_the_partition_agreeing` and seen red under
`> 0`.

**One departure from `plan.md`'s phase boundaries, and it is deliberate.**
The plan puts all of `skills/verify/SKILL.md` in phase 3. Item 1's clause
lives in that file too, and leaving a sentence there naming a cause the code
had stopped naming would put a false sentence in the tree across a phase
boundary — the class this work item exists to close. The clause moved in this
phase; the span's own disclosure is still phase 3's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The printed clause *a call outlived a spawn's result*, in `session_cost.py#report_spawns` and again in `skills/verify/SKILL.md` | Replaced in both by *a call outlived the cut its row ends at*, with the head row's cut named in each |
| The printed phrase *the rows' spans SUM PAST the run's own N by M* | Replaced by the two sums, *sum to N against the run's own M*. Its assertion in `test_a_call_that_outlives_a_cut_prints_no_between_the_rows_figure` moved with it |
| The grounds *an outliving call shortens the RUN's span too*, carried in the module comment, the case's comment and #145's ledger fragment row | The module comment and the case's comment now carry the subinterval grounds. **The ledger fragment row is phase 3's** — it is one of the six rows this work item re-stamps |
| `skills/verify/SKILL.md`'s instruction *leave the between-the-rows share out of the reading rather than substituting the sum* | Kept and widened to *either sum*, since two are printed now. The report's paste-ready text dropped the whole instruction; that would have lost the one actionable sentence a person taking a reading needs |
