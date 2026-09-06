# 1788700685-two-value-shaped-odd-rows-end-the-report — review round 2

| Field | Value |
|---|---|
| Target SHA | 8c8bae7 |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 191 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1, 2, 3, 4 and 5 |
| Loses a record or crashes | yes — finding 1 ends `session_cost.py` with exit 1 and stdout empty on both the report and `--json` |

- [ ] Pass

## What this round was asked

Round 2 of work item `1788700685`. Target `8c8bae7`, base `origin/release/v0.8.3`, draft pull request #191, issue #175.

**Round 1 did not meet the floor** — it answered `Loses a record or crashes: yes` on a 🔴 that ended the report with stdout empty on both arms. So this is a **finding round**, not a verifying one: the surface is the branch, and the question is whether the floor is met now. Round 1's own verdicts were reached at `ae3fe18` and its coordinates are the agenda, not its conclusions.

Read the `New units` row round 1's `close` derived and treat whatever it names as a finding surface — those units were reviewed by nobody.

## The fixes to open first

1. **🔴 1 — a non-finite token count ended the report.** `count` now scores a value `math.isfinite` refuses as 0. **Ask:** does scoring it 0 lose something a reader needs — a transcript that genuinely carried a huge count now reads as zero with nothing said, which is the *silent* half of the very rule this file states. Ask whether the funnel is the right place or whether the report should say a value was refused. And ask what else `count` now swallows that it did not before.
2. **🟡 2 — the AST walk's node set.** Widened to cover builtin numeric consumers, and both records now state the node kinds the walk covers and what it still cannot see. The fix pass reports **three residual shapes** and says its own fix created one of them: the walk reads this module only, so a consumer inside an imported module is outside it — and this fix added `import math`. **Ask:** is that residual real and is it now reachable; are the three the class or a list; and does the corrected record state a limit a next editor can act on rather than a disclaimer.
3. **🟡 3 — the negative span.** `report` now splits zero from negative with a sentence each, and two records were corrected to stop claiming `share` is the single deciding site. **Ask:** does the negative sentence hold for every way a span can be negative; and **the fix pass reports it left the `idle` line printing on a negative span** — `idle > span_s * 0.1` is true for a negative denominator, so the report prints an idle figure beside a dash. It called that out of finding 3's scope. Judge whether that is right or whether a report that prints `idle 65.0m —` on a negative span is the same defect finding 3 named, unfixed.
4. **🟡 4 and 🟡 5 — two docstring corrections.** The mixed-zone cost, and four becoming three. **Ask** whether each corrected sentence is now true of the code as it stands, and whether any third carrier of either claim was missed — round 1's finding 1 existed because one measurement was read as a class, and finding 2 because a node set was read as complete.

## And one thing the fix pass reported about its own process

It records that adding `import math` **before** its use site made the formatter delete it as unused, turning 34 cases red, while the edit tool reported success. Ask whether anything in the tree now depends on that ordering, and whether the record it left is where the next person would meet it.

## Facts, labelled

- **executed by the orchestrator at `a4ec518`** — the three shapes that ended the report at `ae3fe18` now exit 0 on both the report and `--json`: `input_tokens` as `NaN`, `input_tokens` as `Infinity`, and one turn's `cache_read_input_tokens` as `NaN`. `./bin/test tests/test_session_cost.py -q` → 35 passed, exit 0. `uvx ruff check .` → All checks passed. `./bin/evidence-check .` unscoped → 708 ok · 2 drifted · 0 broken, the two being the base's own.
- **read** — `.venv` carries no `ruff` module; use `uvx ruff`. The suite runs through `./bin/test`.
- **unverified** — everything above; and the negative-span shape, which the orchestrator tried to build and could not: sorting by start makes a two-call transcript's span positive, so the shape needs a call whose own end precedes its own start. Confirm how the branch's fixture builds it and whether that shape is reachable from a real harness at all.

Run the ledger check unscoped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's fix for finding 1 introduced a second way to end the report and did not close the first. `math.isfinite` raises `OverflowError` on an `int` too large for a float, and `json.loads` builds such an int from any long integer literal. `output_tokens` carrying one exited 0 before the fix and exits 1 with stdout empty after it, on the report and on `--json`; `input_tokens` carrying one still exits 1. This is the residual the corrected records name — a numeric consumer reached through an import — walking in through the `math` the fix itself added | `skills/verify/scripts/session_cost.py#count` | open | 🔴. **Executed** at `ae3fe18` and `8c8bae7`, three-turn transcripts, one field written as a 401-digit integer literal, both arms each: `output_tokens` before gave exit 0 at 1281 bytes; after gives exit 1 with stdout empty and `OverflowError: int too large to convert to float`. `input_tokens` before gave exit 1 with `OverflowError: integer division result too large for a float` at `token_thirds`; after gives exit 1 at `count`. No float shape reaches this — a float literal of that size parses to infinity, which `isfinite` answers. **Reproduced independently by the orchestrator at `8c8bae7`**, both fields, both arms, same exception. Fix, verified — in `count`, wrap the finiteness question so the conversion cannot escape: take `math.isfinite(value)` inside a `try`, return 0 on `OverflowError`, and otherwise return the value when finite and 0 when not. Executed with that patch: all four shapes exit 0 on both arms, and the module suite gives 35 passed. Plant two more entries in the shapes tuple of `test_a_nan_token_count_does_not_end_the_report` — a 401-digit integer on `output_tokens` and one on `input_tokens` — seen red first against `8c8bae7` |
| 2 | The idle line still prints on a negative span, with a positive figure larger than the span, and `share` does not decide it. Round 1's finding 3 named `report` testing the non-positive predicate independently of `share`; the fix corrected the sentence and left the third independent test standing. `phases/phase-1.md`'s class table counts this site among four *closed by this phase at `share`* | `skills/verify/scripts/session_cost.py#report` (the idle guard), and the records at `seal/specs/1788700685-…/phases/phase-1.md` §*One funnel, not two*, `overview.md` divergence row *How many sites there are*, `seal/ledger/1788700685-….md` R2 Notes | open | 🟡. **Executed** at `8c8bae7`: the branch's own negative fixture prints an idle line of sixty-five minutes beside a span of minus thirty; a mixed-zone one-call transcript, call row naive-local and result row aware, prints a span of minus nine hours and an idle line of zero. The zero-span case is unaffected — at a span of zero the idle condition compares zero against zero and is false, as the records say. Fix, verified — restore the early draft's conjunct so the line prints only for a positive span. Executed with that patch: neither negative fixture prints the line, and the module suite gives 35 passed. Then correct all three records, which argue the guard is a branch no case can exercise — true at zero, false at a negative span, and the mixed transcript `parse_time`'s own new paragraph describes is how a real harness reaches one. Extend `test_a_negative_span_says_what_it_actually_saw` with an assertion that the word idle is absent, seen red first |
| 3 | The negative-span sentence is false for a negative span whose last-starting call is not its last-ending one. The span uses the last element of a list sorted by start, so that element is the last call to BEGIN | `skills/verify/scripts/session_cost.py#report` (the sentence naming the last result) | open | 🟡. **Executed** at `8c8bae7`: call `a` 10:00 to 12:00 and call `b` 10:05 to 09:00 give a span of minus sixty minutes and print *the last result predates the first call*, while the last result arrived at 12:00, two hours after the first call. Fix — say what the number is: the last call to begin ended before the first call began, which is what the arithmetic computes and is true of every negative span. Update the two assertions in `test_a_negative_span_says_what_it_actually_saw` that name the old string, and add the two-call shape above as a third arm |
| 4 | `docs/flow.md`'s #175 line still says the one open member rides as a stamped rider at `count`. The rider was removed at `a4ec518` and the member closed. Round 1's finding 1 named five carriers of the false version and this is a sixth, outside the work item's directory, so nothing in the work item's own correction pass reached it | `docs/flow.md:68` | open | 🟡. **Read** at `8c8bae7`, and a grep for the rider marker under `skills/verify/` returns nothing at `count`. `./bin/test tests/test_a_rider_reaches_its_file.py -q` gives 8 passed, exit 0, so nothing is red; the line is simply false. Fix — replace the trailing clause so it says the third member, a non-finite usage count which ended the report from `token_thirds`' rounding in every field but `output_tokens`, is closed at `count` in round 1's fix pass |
| 5 | `turn_at` builds its stamp by string interpolation into a fixed prefix, which produces an unparseable stamp for any second above 9, and re-implements the `stamp_at` the file already has | `tests/test_session_cost.py#turn_at` | open | 🟡. **Executed**: the interpolation at second 10 produces a stamp `datetime.fromisoformat` refuses, so `parse_time` returns None and `load` drops the row — a case that still asserts exit 0 while measuring one fewer turn. Fix — build both rows off the module's own clock helper, taking the call at sixty seconds per step and the result thirty seconds after it, which reproduces today's stamps exactly for the seconds now used and carries correctly past nine. Noted in the same function's case: the integer conversion in the token assertion raises rather than failing an assertion if a non-finite value ever reaches it, so the failure would read as a test error instead of the defect it pins |
| 6 | The corrected record files the residual that the 🔴 came through as *the walk sees only this module*, which points a next editor away from the fix that exists. The finiteness call IS in this module's AST — it is a `Call` whose `func` is an `Attribute`, outside the walk's NAME set, not outside the module | `seal/specs/1788700685-…/phases/phase-1.md` §*What the widened set still cannot reach* | open | ⬜ — a work-item record, so a correction rather than a fix, and not counted in `Needs a fix`. **Read** at `8c8bae7`. The other two residuals are stated correctly and are genuinely the class of a by-name walk's blind spots. Correction — say that the walk classifies calls by a bare `Name`, so a dotted call through an imported module is invisible although its call site is in this file, and that the widening is one line in the classifier: accept a `Call` whose `func` is an `Attribute` whose value is an imported module name. That is the limit a next editor can act on |
| 7 | The type/value summary table still marks the non-finite member open. Round 1's finding 1 named this coordinate among the five carriers; the correction was written as a blockquote under the NEXT heading, so a reader scanning the table meets *open* | `seal/specs/1788700685-…/phases/phase-1.md` §*Each axis then decomposes into type and value* | open | ⬜ — a work-item record, correction not fix. **Read** at `8c8bae7`. Correction — mark the cell closed at `count` in round 1's fix pass and leave the reasoning below as written, which is what the section says it is kept for |
| 8 | Round 1's findings 4 and 5, re-derived rather than inherited | `skills/verify/scripts/session_cost.py#parse_time`, `#share`, `tests/test_session_cost.py#test_a_span_of_zero_prints_what_it_can_rather_than_dividing_by_it` | answered | ⬜. **Read** at `8c8bae7`. Finding 5: three `share` call sites in `report` — command, model, idle — and both docstrings now say three. Finding 4: the mixed-zone paragraph is true, including the arithmetic, and it states the exit-0 change the old paragraph concluded away. Third carriers of the *four* claim exist in `spec.md` and `plan.md`, deliberately left as the approved contract with the divergence recorded in `overview.md` — round 1's finding 6 settled that and this round does not reopen it |

## Executed probes

| What was run | Result |
|---|---|
| Three-turn transcript, `output_tokens` as a 401-digit integer, report and `--json`, against `ae3fe18` and `8c8bae7` | before: exit 0, 1281 bytes and 1060 bytes. after: **exit 1, stdout empty, both arms** — `OverflowError: int too large to convert to float` |
| Same, `input_tokens` as a 401-digit integer | before: exit 1, stdout empty, both arms — `OverflowError: integer division result too large for a float`. after: exit 1, stdout empty, both arms, at `count` |
| The finiteness call against a 401-digit integer directly | `OverflowError: int too large to convert to float` |
| The branch's own negative-span fixture, report and `--json`, at `8c8bae7` | exit 0 both arms. Report prints a span of minus thirty minutes, the new sentence, and an idle line of sixty-five minutes |
| Mixed-zone one-call transcript — call row naive-local, result row aware — report and `--json` | exit 0 both arms. A span of minus nine hours, the negative sentence, and an idle line of zero. The negative-span family is reachable through this branch's own normalisation |
| Negative span whose last-starting call ends after the first call begins | exit 0. Prints *the last result predates the first call* while the last result is two hours later |
| Patched module — the finiteness question guarded against the conversion, and the idle line guarded on a positive span — against all five fixtures | exit 0 on every fixture, both arms; no idle line on either negative shape |
| The module suite against that patched module in a scratch tree | 35 passed, exit 0 — neither fix disturbs an existing case |
| `./bin/test tests/test_session_cost.py -q` at `8c8bae7` | 35 passed, exit 0. Reproduces the orchestrator's fact |
| `./bin/test tests/test_a_rider_reaches_its_file.py -q` at `8c8bae7` | 8 passed, exit 0 — the rider removal left nothing red |
| `./bin/evidence-check .` unscoped at `8c8bae7` | exit 1 — 708 ok · 2 drifted · 0 broken. The two are the base's own; the fragment's anchors all resolve. Reproduces the orchestrator's fact |
| The stamp interpolation at second 10 | An invalid isoformat string, so `parse_time` returns None and the row is dropped |
| Probes deleted, tree checked | scratch directory removed; the working tree is clean at `8c8bae7` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:335` | round 1's 1 — fixed |
| round-1 | `seal/specs/1788700685-…/phases/phase-1.md:120-126` and `seal/ledger/1788700685-….md` R3 | round 1's 2 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:490-494` | round 1's 3 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:68-72` | round 1's 4 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:474` and `tests/test_session_cost.py:843` | round 1's 5 — fixed |
| round-1 | `seal/specs/1788700685-…/overview.md:17-21` | round 1's 6 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, repository-wide lint and typecheck | `agent-contract` §2 reserves the broad gate; this round ran the module it reviewed and the one rider case the branch's rider removal touched, and declines to widen | the orchestrator, once the rounds settle |
| `templates/config.md#"# Repository config"` and `round_record.py#swallowed`, both DRIFTED | Confirmed present at the base and untouched by this branch; already carried in `overview.md` §Not verified with an answerer | the orchestrator, or the branch whose edits drifted them |
| The fix pass's process fact — an `import` written above its use site is deleted by the formatter as unused, the edit tool reports success, and 34 cases go red | Nowhere in the tree; the fact lives in one handover transcript. Nothing in the tree depends on the ordering, so this is a session lesson rather than a code claim, and `seal/follow-up.md` or a `learn` note is where a next person would meet it | the orchestrator |
