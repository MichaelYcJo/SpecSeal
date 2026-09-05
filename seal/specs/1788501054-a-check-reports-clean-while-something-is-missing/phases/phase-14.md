# 1788501054-a-check-reports-clean-while-something-is-missing — phase 14

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-14.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: round 11's fixes are work
the plan did not contain, and the phase row was added beside them, the way
phases 6 through 13 were. -->

| Field | Value |
|---|---|
| Phase | 14 |
| Commit | 1623c3e |
| Ran by | orchestrator on fable-5.1 — no smith was spawned. `round-10.md` had drawn the line that the orchestrator would not fix what round 11 opened; round 11 opened a 🔴, the orchestrator stopped and brought it to the repository owner, and the owner chose that the orchestrator write these three and take one more verifying round |

## What this phase was asked

Round 11's 🔴 and two 🟡, after the owner's answer to the stopped run:

- **🔴 1** — round 10's rewrite of the floor's refusal blamed *the record
  before it* — the first counted record — which is the verifying round the
  floor allows, as the same message says three clauses later and every
  other carrier of the rule agrees. The one too many is the stopping record
  and every counted record after the first.
- **🟡 2** — the spec's exits row carried the same blame, *the quiet round
  in first*.
- **🟡 3** — `round-9.md`'s reach-back was stale at HEAD, the fourth in a
  row, and the orchestrator's own check missed it by counting only the
  newest record's `chain_check` lines.

## What this phase found

**The fixture hid the finding, and that is the whole of how a false clause
got pinned as true.** Round 10's case gave its floor record `Needs a fix:
no` — the one shape where no verifying round is warranted, so the record
before the stop happened to be excess as well and the clause read as true.
With the floor record answering `yes`, the record before the stop is the
reader it is owed, and the clause blamed it. The case now builds that shape
and asserts round 3 is named and round 2 is not; seen red against the
message that blamed the wrong record. §15 is not only *see it red* — it is
*see it red on the fixture that can tell the difference*.

**The direction was copied, not invented.** Six carriers already said *one
later record is the verifying round; a second is the run carrying on*. The
refusal now says the same, and names the excess records by file — `later[1:
counted]`, which is empty when the count is one and so never prints on a
legal run. Three rewrites of this sentence in three rounds each carried a
clause the next round found false; this one carries the sentence the other
carriers agreed on.

**The reach-back check counts per record now.** `chain_check`'s output at
HEAD is grouped by record and counted, not grepped for the newest record's
name — the check that let `round-9.md`'s stale cell through for a round.
Round 10's cell was set in the commit that added `round-11.md`, so it is not
the fifth.

**`Contract changes` names `stopping_floor` a third time, for the same
reason**, and an AST comparison of `72774d5` against `1623c3e` with
docstrings stripped finds it the one changed unit. Five anchors moved —
`stopping_floor` in three rows, the spec's floor subsection and review-arm
section, and both message cases — and the three ledger clauses that had
repeated round 10's blame now say what round 11 found rather than being
quietly corrected.

**No new unit.** Round 10's case was rewritten in place — fixture, assertions
and docstring — and round 9's case re-anchored on the one phrase every
rewrite kept. #161's first rule, kept for a fourth pass.

**The prompt budget is zero and there is no OS boundary.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *the record before it was a round too many* from the refusal, and *the quiet round in first* from the spec's exits row | The same two places, naming the stopping record and every counted record after the first as the ones too many; `test_the_floors_refusal_does_not_deny_the_stop_that_fired`, rebuilt on the fixture that can tell the difference |
| Round 10's fixture with `Needs a fix: no` on the floor record | The same case, with `yes`, so a verifying round is warranted and the blame is testable |
| Three ledger clauses repeating round 10's blame — R12, F1, F9 | The same clauses, saying what round 11 found and keeping what was believed |
