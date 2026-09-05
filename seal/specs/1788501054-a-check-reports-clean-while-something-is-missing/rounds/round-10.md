# 1788501054-a-check-reports-clean-while-something-is-missing — review round 10

| Field | Value |
|---|---|
| Target SHA | ff151db |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | `ff151db`, against `origin/release/v0.8.0` — **2096 passed · 1 skipped · 0 failed**, `ruff check .` and `ruff format --check .` clean. Issue #160's four export cases passed here where they failed at `293a761` and `3937727`; recorded on #160 as intermittent. Spent by this round's fix and re-taken after it |
| Fixes checked by | round-11 |
| Contract changes | `stopping_floor` — the message inside the error tuple it returns changed again, so its set of returnable values moved while signature, arity and return shape did not → `main`, and `tests/test_chain_check_at_the_pull_request.py::test_this_repositorys_own_round_records_pass_the_per_record_checks` |
| New units | `test_the_floors_refusal_does_not_deny_the_stop_that_fired` (depth 1) → pytest only |
| Needs a fix | yes — 🔴 1, `stopping_floor`'s refusal asserts that none of the counted records reopened or closed on a fix when the record it stopped at is precisely one of those; 🟡 2, the spec's exits row states the same false quantifier; 🟡 3, the narrowed pin's `Needs a fix` assertion is a whole-file substring search that cannot fail; 🟡 4, the case's docstring says six carriers fifty lines below its own comment saying eight |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE FIFTH VERIFYING ROUND IN A ROW TO OPEN SOMETHING INSIDE THE PREVIOUS
FIX. The structure signal fired at round 9 and fires again here: 🔴 1 is a
false clause added to the refusal by round 9's fix, of the same shape as the
false clause that refusal already carried from `f187b39`. Issue #161 records
the loop with this branch's counts, and this record adds one more to them.

All four findings are prose and a test's internals, the fix adds one case
and no mechanism, and the orchestrator carries it on the owner's standing
instruction — with one line drawn in the open: **if round 11 opens anything,
the orchestrator stops and brings it to the repository owner rather than fix
it.** A sixth cycle would be the loop and not the work.

Written and committed before the fixes it commissions, so both fix-surface
rows start pending.

THE FIX SURFACE ABOVE is the reach-back, filled at `3b684a7`, and the reason
sits here rather than in the cell. `Contract changes` names `stopping_floor`
for the same reason round 9's record did: the refusal is a string inside the
error tuple the function returns, so its set of returnable values moved
while nothing else did — an AST comparison of `ff151db` against `3b684a7`
with docstrings stripped finds it the one changed unit, nothing added or
removed. The one new unit is the case pinning that the refusal names the
record before the stop as the fault, in a file that predates the run,
answering a finding in a unit that predates it — depth 1. Round 9's message
case was re-anchored in place and the carrier pin's dead assertion was
replaced in place; neither adds a definition. -->

## What this round was asked

The verifying round at `git diff 0d92f21..ff151db` — **two commits**, the
orchestrator's, given as a count the round re-took: 2.

Round 9 had found round 8's pin hollow and the refusal message stating one
stop; the owner chose to narrow the pin rather than rebuild it. This round was
asked to break six things: the narrowed pin for what it now claims, and
whether its name overclaims; the message pin, each half separately; the eight
copies as R12 lists them, opened one by one; whether naming `stopping_floor` in
`Contract changes` for a changed message is the row's meaning or an overreach;
the five re-read anchors and R12; and the terminal state and the squash, with
the refusal's own text read as it would print.

The third found 🔴 1 and 🟡 2. The first found 🟡 3 and 🟡 4.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The refusal denies the very stop that fired. The walk breaks **at** the record that reopened or closed on a fix, that record included, so whenever `counted` is 2 the second counted record IS one of those two things — and the message says *none of them saying the run reopened and none closing on a fix*. The reader who checks their own `Needs a fix: yes` is told the tool did not see it; their actual fault, the quiet round before it, is never named | `chain_check.py:2523-2524`, inside `stopping_floor` | **fixed** `3b684a7` | **Executed** by the round on three fixtures: round 3 reopening → exit 1 and *none of them saying the run reopened*; round 3 closing on a fix → exit 1 and *none closing on a fix*; three quiet records → exit 1 and true. **Orchestrator confirmed by reading the walk**: `counted += 1` precedes the break, so the stopping record is counted. The reopen clause is from `f187b39`; **the fix clause is new in `35def0f`** — round 9's fix added a second false clause of the shape it was repairing. Six of the eight carriers state the rule exactly (*stops at the first later record …, that record included*); the two that use *none of them* are the two round 9's fix touched |
| 🟡 2 | The spec's exits row states the same false quantifier as the checker's failure condition — by its wording, a sequence whose third record reopens should pass; it fails | `docs/review-chain-spec.md:743` | **fixed** `3b684a7` | **Executed** by the round, same three fixtures. Round 9's 🟡 3 named this row for omitting the second stop; the fix added the second stop and kept the quantifier, so the row is false about two conditions instead of one |
| 🟡 3 | Half of the narrowed pin is still a whole-file substring search. The second assertion is live — the protocol's second-stop sentence reverted turns it red, and an emptied tuple fires the guard — but the first, `"Needs a fix" in text`, cannot fail: the phrase occurs eleven times in the protocol | `tests/test_the_run_stops_at_the_last_finding.py:134` | **fixed** `3b684a7` | **Executed** by the round: the count rule's own sentence broken, case green. Round 9's 🔴 1 shape surviving inside the fix that closed it — the coordinate was narrowed, the class inside the case was not enumerated. This is the pinned carrier, not the four deferred ones |
| 🟡 4 | The same file says eight and six fifty lines apart: the constant's comment, rewritten by round 9's fix, says *EIGHT places*; the docstring below it, extended by the same fix, still says *three of the rule's six carriers*. `phase-11.md:20` carries the same stale six as a flat statement | `tests/test_the_run_stops_at_the_last_finding.py:113` against `:54`; `phases/phase-11.md:20` | **fixed** `3b684a7` | **Read**. The two-answers-in-one-document shape `tests/test_one_word_one_meaning.py` exists for, and the precedent round 9's 🟡 4 cited |
| 🟢 5 | The narrowed pin, for what it claims, and its name | `tests/test_the_run_stops_at_the_last_finding.py` | answered | **Executed**: protocol second stop reverted → red; `COUNT_RULE_CARRIERS = ()` → the guard fires. Spelling counts by file re-taken: the protocol is the one carrier where the search is live. The name overclaims and the docstring beneath it says so and says why the name is kept — the disclosure sits where the reader meets the name |
| 🟢 6 | The message pin, each half separately | `tests/…floor_and_the_depth.py` | answered | **Executed**: *none closing on a fix* reverted → red; *do not rewrite the row* removed → red. Both substrings occur exactly once in `chain_check.py`, so nothing but the message satisfies the case |
| 🟢 7 | The eight copies, as R12 lists them | eight coordinates | answered | **Read**, all eight opened: every one names both stops. R12's list is right and complete; a ninth statement exists as a code comment inside the walk and is precise. Two of the eight are false in a different way — 🔴 1, 🟡 2 |
| 🟢 8 | `Contract changes` naming `stopping_floor` for a changed message | `rounds/round-9.md:10` | answered | **Read**: `templates/sdd-round.md:30` names *set of returnable values* as one of the four triggers, and the message is a string inside the returned error tuple. Not an overreach. **Executed** AST walk: `stopping_floor` is called once, inside `main` |
| 🟢 9 | The five re-read anchors and R12 | three ledgers | answered | **Executed**: `evidence_check.py .` unscoped → `539 ok · 1 drifted · 0 broken`, S8 alone; R12's three anchors resolve; the fragment header says eleven and eleven were counted |
| 🟢 10 | The terminal state, and the squash | a `--no-local` clone | answered | **Executed**: `round-10.md` with `no fixes to check` / `no` / `no` / `Pass` ticked and `round-9.md`'s cell set to `round-10` → `chain_check` **exit 0**. `merge --squash ff151db` → one commit, six suites **216 passed**, identical two notices. The floor's message does not fire on this repository's own records at any point, which is why 🔴 1 needed a built fixture |
| 🟢 11 | The four unpinned carriers as a recorded limit | five places | answered | **Read**: the constant's comment, `phase-12.md`, `round-8.md`'s Deferred, `plan.md`'s phase-11 row, R12's Notes. Written where a reader meets it, with its measurement |
| ❓ 12 | `questions.md` Q2, Q3, Q4 | `questions.md` | out of verified scope | **Read**, unchanged. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 0d92f21..ff151db` | **2** |
| three fixtures through `stopping_floor`: round 3 reopens · round 3 closes on a fix · three quiet | exit 1 each; the message false for the first two, true for the third — 🔴 1 |
| the same three against `docs/review-chain-spec.md:743`'s wording | the first should pass by the row and fails — 🟡 2 |
| the protocol's count-rule sentence broken, spelling only | the narrowed pin stays green — 🟡 3 |
| protocol second stop reverted · `COUNT_RULE_CARRIERS = ()` | red · red — the live half and the guard |
| each half of the message pin reverted | red · red |
| all eight carriers opened | every one names both stops |
| AST walk for `stopping_floor`'s callers | one, inside `main` |
| `evidence_check.py .` **unscoped** | `539 ok · 1 drifted · 0 broken` — S8 |
| the terminal state with `round-10.md`, in a clone | `chain_check` **exit 0** |
| `merge --squash ff151db`, six suites | **216 passed** |
| `chain_check` at HEAD · `bin/unverified-check` · ruff on three files · four touched suites in a clone | two honest notices · exit 0 · clean · **96 passed** |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 7–10 | `chain_check.py#stopping_floor`, and specifically its refusal message | Four rounds; the walk changed once and the message three times, and each rewrite carried a clause the next round found false |
| rounds 8–10 | `tests/test_the_run_stops_at_the_last_finding.py`'s carrier pin | Written, found hollow, narrowed, found half-hollow. The next reader opens the one assertion left and asks whether it can fail |
| rounds 4–10 | the cell or sentence the orchestrator last wrote | Seven rounds running |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The line drawn.** This is the fifth verifying round to open something inside the previous fix. The orchestrator carries these four on the owner's standing instruction, and if round 11 opens anything it stops and brings it to the owner rather than fix again — a sixth cycle is the loop, not the work | this row, `overview.md` §Not done, issue #161 | the repository owner |
| The four carriers that keep a corrected sentence and lose their pin | `phases/phase-12.md`, R12 | nobody yet — #161 |
| ❓ from round 6 — a ledger coordinate with no `@hash` is counted in no bucket | `rounds/round-6.md` Deferred | the repository owner |
| `questions.md` Q2, Q3, Q4 · issues #158–#161 · the Windows leg | as before | the repository owner; the windows CI leg |
