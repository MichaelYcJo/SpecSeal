# 1788501054-a-check-reports-clean-while-something-is-missing — phase 11

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-11.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: round 8's fixes are work
the plan did not contain, and the phase row was added beside them, the way
phases 6 through 10 were. -->

| Field | Value |
|---|---|
| Phase | 11 |
| Commit | cd4fec2 |
| Ran by | orchestrator on fable-5.1 — no smith was spawned, on the repository owner's standing instruction for this run's fixes; the model is the one the session was switched to mid-run, which the session knows because it was told |

## What this phase was asked

Round 8's 🔴 and two 🟡, with the standing instruction that the orchestrator
carries them out:

- **🔴 1** — the floor's count rule was written in six places by `f187b39`;
  round 7 updated three and `phase-10.md`'s removal table named those three
  as the whole set. `docs/review-handoff-protocol.md:318-319`, the normative
  document, still said a conforming tool stops at one condition where the
  checker stops at two, and both of `chain_check.py`'s own docstrings — the
  module's at `:208` and `stopping_floor`'s at `:2353`, in bold four lines
  above the walk — stated the old rule as the whole rule.
- **🟡 2** — `round-7.md`'s `Contract changes` named `check_round` as
  `stopping_floor`'s caller; `main` is the only one.
- **🟡 3** — `round-7.md`'s `Fixes checked by` reason was false at HEAD.

`agent-contract` §14 governs the first: a changed line a person reads gets a
test that pins it, and nothing had pinned the protocol or the docstrings.

## What this phase found

**The class is the pin's, not the sentence's.** Round 7 corrected three
copies and believed it had corrected them all because the pass enumerated by
memory, not by grep — `phase-10.md`'s removal table is the record of that
belief. What would have caught it is not a fourth careful reading but a case
whose carrier tuple lists every copy. `tests/test_the_run_stops_at_the_last_finding.py`
pins the FLOOR in four carriers and had pinned the COUNT rule in two;
`COUNT_RULE_CARRIERS` lists five, and the protocol and `chain_check.py` are
among them because the protocol says what a conforming tool does and a
docstring above a walk is what a reader of the walk opens.

**Seen red on the protocol first, and the loop stops there.** The case
iterates the carriers in order and the protocol is fourth, so the first red
names it; the two docstrings would have been named in turn. All three were
corrected in one commit and the case is green.

**The second stop has three spellings, and pinning them is an enumeration.**
`SECOND_STOP` holds *closed on a fix*, *verdicts say `fixed`* and *`fixed`
verdict* — the spec's, the template's and the skill's own words. `docs/review-chain-spec.md`
declines an enumeration over an unbounded domain twice; this one is over this
repository's own five sentences, bounded and named in the constant's comment,
and a sixth copy written in a fourth spelling would go red for the right
reason — it would fail the `Needs a fix` half or be added to the tuple.

**The reach was misread, and the cell says so.** `grep` found the one call to
`stopping_floor` at line 2860 and the orchestrator read it as inside
`check_round`, which ends at 2641. The corrected cell names `main` and its
trailing comment records the misreading rather than quietly becoming right —
the eighth instance on this branch of the orchestrator's prose about a record
being wrong, and the first about a record's own reach.

**`Contract changes` is `none` by measurement.** An AST comparison of
`293a761` against `cd4fec2` with docstrings stripped finds `chain_check.py`
identical. The three anchors on `stopping_floor` drifted by docstring alone —
R11, F1 and F9 — and each carries a re-read clause saying exactly that.

**The prompt budget is zero and there is no OS boundary**: a docstring, a
protocol paragraph, a test module and a record.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The count rule stated with one stop as the whole rule, in `docs/review-handoff-protocol.md` and in both `chain_check.py` docstrings | The same three places, each now naming both stops; and `test_every_carrier_of_the_count_rule_states_both_stops`, which refuses the next copy left behind |
| `check_round` as `stopping_floor`'s named reach in `round-7.md` | `main`, in the same cell, with the misreading recorded in the trailing comment |
