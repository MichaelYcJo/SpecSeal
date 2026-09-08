# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | c05044d |
| Ran by | specseal:smith on claude-opus-5[1m] — the harness's own model identifier; the spawn prompt named none |

## What this phase was asked

#204, in two halves and in this order. First write the argument for
`VERSION_TOKEN`'s leading `(?<![\w.])` beside the constant, covering both
characters — the `\w` half and the `.` half, which does a different job and is
load-bearing on its own. Then decide the uppercase hole against that argument:
an uppercase `V` is a version prefix rather than a preceding word, so the
argument does not reach it and `v?` widens to `[vV]?`. Narrow neither
lookaround. Re-execute the measurement the ticket carries rather than taking
it.

## What this phase found

**The ticket's measurement is stale, and the re-execution is what showed it.**
#204 records, executed at `7349afc`, that `git grep -E 'V[0-9]+\.[0-9]+\.[0-9]+'`
over the loaded set returns nothing, so no instance of the invisible shape
exists. One exists now: `docs/flow.md:101` writes `an uppercase V0.9.0 is
invisible` — the line the orchestrator added to the 0.9.2 list describing this
very work item. Enumerated over all 64 loaded files, the widening admits
exactly that one token and loses none.

It is still not an offender, and for two independent reasons rather than the
ticket's one: `docs/flow.md` is in `RECORDS_OF_A_MOMENT`, and `0.9.0` is below
the running `0.9.1` and so is history either way. The offender list is empty
before and after the widening, which is the claim that actually mattered.

**What the next phase needs from this one.** `as_release` was left alone
deliberately. Its `lstrip("v")` does not strip an uppercase `V`, and nothing
hands it one — `timers_in` passes `match.group(1)`, the bare token, and the
`VERSIONS_OF_ANOTHER_PRODUCT` lookup is string equality on `match.group(0)`.
Widening it would be speculative and would drift a ledger anchor for a claim
nobody is making. A reviewer looking for the uppercase class elsewhere in the
module should land there and find this sentence.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
