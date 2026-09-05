# 1788501054-a-check-reports-clean-while-something-is-missing — phase 13

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-13.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: round 10's fixes are work
the plan did not contain, and the phase row was added beside them, the way
phases 6 through 12 were. -->

| Field | Value |
|---|---|
| Phase | 13 |
| Commit | 3b684a7 |
| Ran by | orchestrator on fable-5.1 — no smith was spawned, on the repository owner's standing instruction for this run's fixes; the model is the one the session was switched to mid-run, which the session knows because it was told |

## What this phase was asked

Round 10's 🔴 and three 🟡, with the standing instruction that the
orchestrator carries them out — and with a line drawn in the record that
commissioned them: if round 11 opens anything, the orchestrator stops and
brings it to the owner rather than fix again.

- **🔴 1** — `stopping_floor`'s refusal said *none of them saying the run
  reopened and none closing on a fix*, where the walk breaks AT the record
  that reopened or closed on a fix, that record included — so with two
  counted, the second is one of those, and the message denied the stop that
  fired. The reopen clause dated from `f187b39`; the fix clause was round 9's.
- **🟡 2** — the spec's exits-table row carried the same quantifier.
- **🟡 3** — the narrowed pin's `Needs a fix` assertion was a whole-file
  search over a phrase the protocol uses eleven times.
- **🟡 4** — the case's docstring said six carriers fifty lines below the
  constant's comment saying eight; `phase-11.md:20` said six once more.

## What this phase found

**A quantifier over a counted set is false the moment the set includes its
own stopping element, and this walk always includes it.** `counted += 1`
precedes the `break`, so the record the walk stops at is in the count, and
any sentence of the form *none of the counted records did X* is false
whenever the walk stopped for X. Two of the rule's eight carriers used that
form — the two round 9's fix touched — and six state it exactly. The refusal
now says what the count reached, where the walk stops, and that the record
before the stop was the round too many, which is the fault the reader has to
find. Pinned by a case seen red against the old message; round 9's case is
re-anchored on the rule's exact statement rather than on the clause that
was wrong.

**An existing pin decided the spec row's wording.**
`test_the_document_states_what_each_refusal_does` holds the phrase *with two
or more later round records* in the spec, and the first rewrite dropped it —
the narrow run went red on that case and the row was rewritten to keep the
phrase and correct the meaning. That is a pin doing its job on the fix pass
that would have broken it, and it cost one extra edit rather than a round.

**The pin's other half was the same class one assertion over.** Round 9
narrowed the carrier tuple to where the second-stop search was live and left
the first assertion — `"Needs a fix" in text` — as a whole-file search that
could never fail. It anchors on the rule's own sentence now. `agent-contract`
§12 names this exactly: the coordinate was narrowed and the class inside the
case was not enumerated.

**`Contract changes` names `stopping_floor` again, for the same reason as
phase 12.** The message is a string inside the returned error tuple; an AST
comparison of `ff151db` against `3b684a7` with docstrings stripped finds
`stopping_floor` the one changed unit, nothing added or removed. Six anchors
moved — `stopping_floor` in three rows, the spec's floor subsection and
review-arm section, and the two cases whose text changed — and each row
carries a clause saying so.

**The prompt budget is zero and there is no OS boundary.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The *none of them …* quantifier from the refusal message and the spec's exits row | The same two places, stating the count and the stop; `test_the_floors_refusal_does_not_deny_the_stop_that_fired`, which refuses the old wording by name |
| `"Needs a fix" in text` as the narrowed pin's first assertion | The same case, anchored on the count rule's own sentence in the protocol |
| *six carriers* in the case's docstring and in `phase-11.md:20` | *eight*, with each place saying it used to say six |
