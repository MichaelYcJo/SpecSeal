# 1788501054-a-check-reports-clean-while-something-is-missing — review round 11

| Field | Value |
|---|---|
| Target SHA | 72774d5 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | `72774d5`, against `origin/release/v0.8.0` — **2097 passed · 1 skipped · 0 failed**, `ruff check .` and `ruff format --check .` clean. Spent by whatever fix closes 🔴 1 |
| Fixes checked by | nobody — round 12 is the round that opens these fixes and it is not written yet; this cell becomes `round-12` the moment that record is committed |
| Contract changes | `stopping_floor` — the message inside the error tuple it returns changed a third time, so its set of returnable values moved while signature, arity and return shape did not → `main`, and `tests/test_chain_check_at_the_pull_request.py::test_this_repositorys_own_round_records_pass_the_per_record_checks` |
| New units | none |
| Needs a fix | yes — 🔴 1, the refusal's new clause blames the verifying round the rule allows — *the record before it was a round too many* — and contradicts its own sentence three clauses later, where a second record is the one too many; 🟡 2, the spec's exits row carries the same blame in *the quiet round in first*; 🟡 3, `round-9.md`'s `Fixes checked by` is stale at HEAD, so `chain_check` prints three lines where `plan.md`'s phase-13 row claims two |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE ORCHESTRATOR STOPS HERE, as `round-10.md` said it would. This is the
sixth verifying round in a row to open something inside the previous fix,
and the 🔴 is the third consecutive rewrite of one sentence — the floor's
refusal — each rewrite carrying a clause the next round found false. Round
9's fix added a false quantifier; round 10's fix removed it and added a
false blame; and round 10's own case hid the blame by giving its floor
record `Needs a fix: no`, the one shape where no verifying round is
warranted and the blamed record happens to be excess anyway.

🟡 3 is the fourth consecutive stale reach-back, and the orchestrator's own
check missed it by counting only the newest record's lines.

The fixes are small and prose, as every fix since round 6 has been, and
that is exactly why the orchestrator does not write them: issue #161's loop
is not closed by one more small fix, and the record that commissioned this
round said so. What the owner decides is below, in Deferred.

THE OWNER ANSWERED: the orchestrator writes these three and takes one more
verifying round. THE FIX SURFACE ABOVE is that reach-back, filled at
`1623c3e`, and the reason sits here rather than in the cell. `Contract
changes` names `stopping_floor` a third time for the same reason as rounds
9 and 10 — the refusal is a string inside the tuple it returns — and an AST
comparison of `72774d5` against `1623c3e` with docstrings stripped finds it
the one changed unit, nothing added or removed. `New units` is `none`:
round 10's case was rebuilt in place on the fixture that can tell the
difference, and round 9's case re-anchored in place; neither adds a
definition. -->

## What this round was asked

The verifying round at `git diff 257a7f2..72774d5` — **two commits**, the
orchestrator's, given as a count the round re-took: 2.

Round 10 had found the refusal denying the very stop that fired; the fix
rewrote the message to name the count, the stop, and the record before the
stop as the fault, pinned by a new case. This round was asked to break six
things: the new refusal read as a person would, against the three fixtures
round 10 used; the three pins on the message, each clause reverted
separately; the narrowed pin's new anchor; the spec row and the phrase an
existing case holds; every copy of the count rule one last time; and the
terminal state and the squash.

The first found 🔴 1 — with a fourth fixture the fix's own case did not
build: a floor record that answered `Needs a fix: yes`, so that a verifying
round was warranted.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The refusal blames the verifying round and contradicts its own next sentence. *The record before it was a round too many* names the first later record — which the same message, three clauses later, calls *the verifying round* the floor allows. The record one too many is the second, the one the walk stopped at | `chain_check.py:2521-2526`, inside `stopping_floor`; pinned as correct by `tests/…floor_and_the_depth.py:583` | **fixed** `1623c3e` | **Executed** by the round on five fixtures: with round 1 `Needs a fix: yes` and rounds 2–3 quiet — this branch's own shape — the message names r2, the verifying round at r1's fix diff. In two of the five shapes the walk ended because `later` ran out, so *before it* has no referent at all. **Orchestrator re-read the twelve lines**: the clause and the contradiction are both there. Every other carrier states it the right way round — *one later record is the verifying round; a second is the run carrying on*. The fix's own case gave round 1 `Needs a fix: no`, the one shape where r2 is excess anyway, which is how a false clause came to be pinned as true |
| 🟡 2 | The spec's exits row carries the same blame — *a reopening in second place does not excuse the quiet round in first* — in a cell that calls the round in first the verifying round | `docs/review-chain-spec.md:743`, the clause round 10's fix appended | **fixed** `1623c3e` | **Read**. Nothing about the first record needs excusing; the second is still a second |
| 🟡 3 | `round-9.md`'s `Fixes checked by` still reads `nobody — round 10 … not written yet` at HEAD, beside `round-10.md` committed at `257a7f2` with `**fixed**` four times. The fourth consecutive stale reach-back — round 7's 🟡 2, round 8's 🟡 3, round 9's 🟡 5, and now this | `rounds/round-9.md:9` | **fixed** `1623c3e` | **Executed**: `chain_check --baseline origin/release/v0.8.0` at HEAD prints **three** lines, and `plan.md:49` claims *down to `round-10.md`'s honest pair*. **Orchestrator re-ran it**: `round-9.md` 1, `round-10.md` 2. The orchestrator's own verification counted only `round-10.md`'s lines, which is how the third line went unseen |
| 🟢 4 | The three pins on the message, each clause reverted separately | `tests/…floor_and_the_depth.py` | answered | **Executed**, five mutations in a clone, baseline 79 passed: each clause dropped or re-added turns exactly one assertion red and nothing else. One pin per clause — the pins are right; the clause one of them pins is wrong |
| 🟢 5 | The narrowed pin's new anchor | `tests/test_the_run_stops_at_the_last_finding.py` | answered | **Executed / read**: the anchored sentence occurs exactly once in the flattened protocol, verbatim; `Needs a fix` eleven times, which is the dead assertion it replaced. The wrap `test_docs_line_wrap` enforces is safe under `flat()` |
| 🟢 6 | The spec row against all five fixtures | `docs/review-chain-spec.md:743` | answered | **Executed**: the row's condition is true of all five and correctly lets `r1 quiet · r2 reopens` pass. It reads as one rule with the counting method as an appositive. Only the trailing clause is wrong — 🟡 2 |
| 🟢 7 | Every copy of the count rule, one last time | eight coordinates | answered | **Read**, all eight opened: every one states the stop and its inclusiveness, and **no *none of them* quantifier survives anywhere** — grep over `*.md` and `*.py` hits only the two negative assertions and past round records. The ninth statement, the code comment inside the walk, is precise |
| 🟢 8 | Six→eight, and the arithmetic | three places | answered | **Read**: 3 + 3 + 2 = 8, consistent with R12 and the plan rows |
| 🟢 9 | The terminal state | a `--no-local` clone | answered | **Executed**: `round-11.md` with `no fixes to check` / `no` / `no` / `Pass` ticked and `round-10.md`'s cell set to `round-11` → `chain_check` **exit 0**. The only line left is `round-9.md`'s stale cell — 🟡 3 |
| 🟢 10 | The squash | a `--no-local` clone | answered | **Executed**: `merge --squash 72774d5`, six suites **173 passed**, `chain_check` there on the unchecked `Pass` plus the two notices, as expected before round 11 is written |
| 🟢 11 | The ledgers | three ledgers | answered | **Executed**: `evidence_check.py .` unscoped → `540 ok · 1 drifted · 0 broken`, S8 alone; R12's four anchors resolve; `bin/unverified-check` exit 0 |
| ❓ 12 | `questions.md` Q2, Q3, Q4 | `questions.md` | out of verified scope | **Read**, unchanged. Q4 is the one 🟡 3 touches: the pending arm keys on `Fixes checked by`, so a stale cell prints and is never refused. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 257a7f2..72774d5` | **2** |
| five fixtures through `stopping_floor`, the message read verbatim | the clause names r2 in four of five; in two, *before it* has no referent — 🔴 1 |
| five clause mutations of the refusal, in a clone | one assertion red per clause, nothing spurious |
| the protocol's anchored sentence, counted | once; `Needs a fix` eleven times |
| the spec row against the five fixtures | true of all five; the trailing clause false — 🟡 2 |
| all eight copies opened; grep for *none of them* | every copy exact; no quantifier survives |
| `chain_check --baseline origin/release/v0.8.0` at HEAD | **three** lines — `round-9.md` 1, `round-10.md` 2 — 🟡 3. Orchestrator re-ran and counted per record |
| the terminal state with `round-11.md`, in a clone | `chain_check` **exit 0**, one stale notice left |
| `merge --squash 72774d5`, six suites | **173 passed** |
| `evidence_check.py .` **unscoped** · `bin/unverified-check` | `540 ok · 1 drifted · 0 broken` — S8 · exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 7–11 | `chain_check.py#stopping_floor`'s refusal message | Three rewrites in three rounds, each carrying a clause the next round found false. The next writer opens every other carrier first and copies the direction they agree on |
| rounds 7–11 | the `Fixes checked by` cell of the second-newest record | Stale four rounds running. The next check counts `chain_check`'s lines per record, not the newest record's alone |
| rounds 4–11 | the cell or sentence the orchestrator last wrote | Eight rounds running |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **Who writes these three fixes, and whether round 12 reads them.** 🔴 1 blocks merge and cannot be answered with grounds — it names the wrong record. The fixes are prose, a fixture cell and a reach-back; the reader they owe is a verifying round, because `nobody` beside a ticked `Pass` fails the pull request by design. The orchestrator stops here as `round-10.md` said, because this is the sixth cycle of the loop #161 records and a seventh small fix is the loop, not the work | this row, `overview.md` §Not done, issue #161 | **the repository owner** — who answered: the orchestrator writes them, copying the direction the other carriers agree on rather than inventing a fourth sentence, and round 12 reads that diff. Phase 14 is that pass |
| The pending arm keys on `Fixes checked by`, so a stale reach-back prints and is never refused — four times on this branch | `questions.md` Q4 | the repository owner |
| The four carriers that keep a corrected sentence and lose their pin | `phases/phase-12.md`, R12 | nobody yet — #161 |
| ❓ from round 6 — a ledger coordinate with no `@hash` is counted in no bucket | `rounds/round-6.md` Deferred | the repository owner |
| `questions.md` Q2, Q3 · issues #158–#161 · the Windows leg | as before | the repository owner; the windows CI leg |
