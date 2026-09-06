# 1788700685-two-value-shaped-odd-rows-end-the-report — review round 1

| Field | Value |
|---|---|
| Target SHA | ae3fe18 |
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

Round 1 of work item `1788700685`, target `ae3fe18`, base `origin/release/v0.8.3`, draft pull request #191, issue #175.

Attack these first, in this order. Each is a specific claim this branch makes.

1. **The judgement that #170's row is under-specified rather than falsified, and the eight measurements it rests on.** The branch re-ran the row's own recorded method — *every field × seven JSON types × field absent* — against the `timestamp` field at the commit the row was stamped at, and reports all eight variants exit 0 while a naive stamp and an equal-stamp pair exit 1. From that it concludes the two shapes are **values of the field's own type** and therefore structurally outside the product rather than members it missed. **It measured 8 of 288 and inferred the rest from the row's stated construction.** That is the place to overturn the judgement. Re-run what you need to, and say whether *outside the product* survives contact — in particular whether any of the other four fields' variants can produce the same shape, and whether the row's method as recorded actually generates what the branch says it generates.
2. **`parse_time` normalising rather than dropping.** A naive stamp is read as UTC. Ask what that does to a transcript whose stamps are naive **local** time — the span stays right and an absolute time does not, which the branch says nothing here prints. Check that. And ask whether normalising at `parse_time` closes every site: the branch reports six subtractions and two ordering comparisons, and that a two-call transcript dies in `load`'s `calls.sort` before `analyse` is entered. Confirm the count and confirm no operand reaches an arithmetic site from a source `parse_time` does not funnel.
3. **`share(part, whole)` and the non-positive guard.** It returns a percentage when the span is positive and an em dash otherwise. Ask: is `share` the only place deciding what a non-positive span means, or does a second site still decide it independently — the branch says it removed an early draft's separate idle guard for exactly that reason, so check the removal is complete. Ask what a NEGATIVE span prints end to end, and whether the explanation line under the span is true for a negative span as well as a zero one, since it says *every call shares one timestamp*.
4. **The `--json` asymmetry, which the branch uses as an argument for where the guard lives.** Measured: a zero span exits 0 under `--json` and 1 under the report. Verify it, and verify the corollary — that `--json`'s numbers for a zero-span transcript are actually correct rather than merely emitted.
5. **The `NaN` / `Infinity` residual, left open on purpose.** It prints `nan` and exits 0, so it is out of this spec. Ask whether the narrowed row and the rider together leave it genuinely open — a reader meeting the row first must not read it as closed — and whether `nan` reaching a *comparison* or a `max`/`sort` does something worse than printing.
6. **The AST enumeration.** 56 arithmetic and ordering sites, classified; the first walk returned 42 and missed `AugAssign` and `UnaryOp`. Ask whether 56 is now complete: what about a comparison inside a comprehension's condition, a `sorted(key=...)`, a `%` or f-string format of a transcript value, a `divmod`, a `round`, `statistics.mean`, or an operand reaching a builtin through a variable. Judge the METHOD, not the count.
7. **The re-stamping.** Four rows drifted; the branch re-stamped them by taking the tool's own computed values at the same coordinates rather than by hand, and cross-checked the method against a value `seal/ledger.md` already carried. Verify the four stamps resolve and that nothing this branch never opened was touched.
8. **The two spec divergences left in `overview.md` rather than back-fitted.** `spec.md` and `plan.md` still say `analyse`'s subtractions and name four of each. Judge whether leaving the approved contract unedited and recording the divergence is right here, or whether a document that is now false in the tree should be corrected.

Facts, labelled:

- **executed by the orchestrator at `ae3fe18`** — `./bin/test tests/test_session_cost.py tests/test_a_rider_reaches_its_file.py -q` → 41 passed, exit 0. `./bin/evidence-check .` unscoped → 708 ok · 2 drifted · 0 broken, the two being `templates/config.md#"# Repository config"` and `round_record.py#swallowed`, both the base's and neither opened by this branch. `./bin/unverified-check --baseline origin/release/v0.8.3` → exit 0.
- **read** — `.venv` carries no `ruff` module; use `uvx ruff`. The suite runs through `./bin/test`.
- **unverified** — everything in the eight items above.

Run the ledger check unscoped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `NaN` or `Infinity` in `input_tokens` or `cache_read_input_tokens` ends the report — exit 1, stdout empty, on the report AND `--json` — so the residual the branch deferred as "exits 0" is inside `spec.md`'s own In scope. Five documents state the false version: the `# RIDER:` at `count`, `phases/phase-1.md:166`, `overview.md:33-38`, fragment R3, `changelog.md` | `skills/verify/scripts/session_cost.py:335` | open | 🔴. Executed at `ae3fe18`, three tool-call turns: `input_tokens` as `NaN` raises `ValueError: cannot convert float NaN to integer` at `token_thirds`; `Infinity` raises `OverflowError`; one turn's `cache_read_input_tokens` as `NaN` raises the same `ValueError`. `output_tokens` is the only usage field that does NOT reach `token_thirds`, and it is the only one the branch measured. **Reproduced independently by the orchestrator at `ae3fe18`**, same three shapes, same exits, both arms. Fix — the rider's own one-liner, which closes it at the funnel: import `math` beside the existing imports, then in `count` return the value only when `math.isfinite` accepts it and `0` otherwise. Then correct the five documents and plant `test_a_nan_token_count_does_not_end_the_report` — three tool-call turns with `input_tokens` non-finite, a second arm with `Infinity`, both arms exiting 0 — seen red first |
| 2 | The AST walk's node set omits builtin numeric consumers, and `round` at line 335 is the one site outside it — where finding 1 lives. The walk is recorded as "complete rather than merely larger" | `seal/specs/1788700685-…/phases/phase-1.md:120-126` and `seal/ledger/1788700685-….md` R3 | open | 🟡. Executed: re-derived the walk at `ae3fe18` with phase 1's stated node set — arithmetic `BinOp`, `AugAssign`, `UnaryOp`, ordering `Compare`, and the five walked calls — giving 22 + 10 + 5 + 10 + 13 = 60 sites, consistent with 56 pre-fix. Adding a class for builtin numeric consumers returns exactly one more: `round` at line 335. Fix — extend the walk with a set of builtin and stdlib numeric consumers (`round`, `int`, `float`, `abs`, `divmod`, `pow`, `mean`, `median`, `fsum`, `isqrt`, `ceil`, `floor`), re-classify, and correct both records to state the node set the walk covers rather than claiming completeness over operations |
| 3 | A negative span prints *every call shares one timestamp*, which is false for it; and `report` decides the non-positive predicate independently of `share`, contradicting the record's claim that `share` is the single such place. No case pins the shape | `skills/verify/scripts/session_cost.py:490-494` | open | 🟡. Executed at `ae3fe18` over a two-call transcript with four distinct stamps whose second call ends before the first begins: it prints a negative span and then the shared-timestamp sentence. A grep for the word negative in `tests/test_session_cost.py` returns nothing. Fix — split the branch so the sentence matches the shape: keep the current sentence for a span of exactly zero, and for a negative span print that the last result predates the first call, so the span is negative and there is no share to take of it. Plant `test_a_negative_span_says_what_it_actually_saw`, seen red first. Correct fragment R2 and `phases/phase-1.md:108-112`, which both say `share` is the only site |
| 4 | `parse_time`'s docstring names the assumption's cost as an absolute time and says every number the file prints is safe, but a MIXED transcript — one aware stamp beside a naive local one, the shape the fix exists for — now yields a span wrong by the harness's offset at exit 0, where it used to raise | `skills/verify/scripts/session_cost.py:68-72` | open | 🟡. Read, against the branch's own fixture: `mixed-pair` asserts a ten-second span for an aware stamp paired with a naive one; at UTC+9 the true span is minus nine hours. The docstring's own condition — *whenever the two share a zone* — is not met by that case and the paragraph concludes nothing is lost. Not a request to reverse `plan.md`'s accepted alternative. Fix — after that condition, add that where the two do NOT share a zone, which is the shape this normalisation was written for, the difference is wrong by that harness's offset and it is now wrong at exit 0 where it used to raise |
| 5 | Two new docstrings say four lines of `report` divide by the span. There are three, which this branch measured and recorded | `skills/verify/scripts/session_cost.py:474` and `tests/test_session_cost.py:843` | open | 🟡. Read. `phases/phase-1.md:75` states the correction in the branch's own words and the `overview.md` divergence table quotes it. Confirmed against the code: three `share` call sites. Fix — in both docstrings, four becomes three |
| 6 | Leaving `spec.md` and `plan.md` unedited with the divergence recorded in `overview.md` is right | `seal/specs/1788700685-…/overview.md:17-21` | answered | ⬜. Read. `plan.md` is the approved contract; both sides of each divergence are quoted with the measurement behind the correction. Not a finding. Noted only: `spec.md` §Scope's sentence about `analyse`'s subtractions stays false in the tree, which is the convention's cost rather than this branch's |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/evidence-check .` unscoped at `ae3fe18` | exit 1 — 708 ok · 2 drifted · 0 broken. The two are `templates/config.md#"# Repository config"` and `round_record.py#swallowed`, both the base's. The fragment's rows all resolve. Reproduces the orchestrator's fact |
| `./bin/deferral-check` | exit 0 — `tests: resolves` |
| Synthetic transcript, negative span (four distinct stamps, second call ends before first begins), report and `--json` | Both exit 0. The report prints a negative span followed by the shared-timestamp sentence. `--json` gives a negative span and a negative command time |
| Synthetic transcript, zero span, report and `--json` | Both exit 0. The report carries the span line, the sentence, three dashes, the token block and the family table. `--json` gives a zero span, zero command and model time, one call, one call turn, one tool per turn and a zero mean gap — all correct for that transcript, not merely emitted |
| Synthetic transcript, `output_tokens` non-finite | exit 0 both arms, prints `output nan`. Reproduces the branch's measurement |
| Synthetic transcript, three tool-call turns, `input_tokens` as `NaN` | **exit 1, stdout empty, report AND `--json`** — `ValueError: cannot convert float NaN to integer` at `session_cost.py:335` |
| Synthetic transcript, three tool-call turns, `input_tokens` as `Infinity` | **exit 1, stdout empty, both arms** — `OverflowError: cannot convert float infinity to integer` at the same line |
| Synthetic transcript, three turns, one `cache_read_input_tokens` as `NaN` | **exit 1, stdout empty, both arms** — same `ValueError` |
| AST re-derivation of phase 1's walk at `ae3fe18`, plus a class for builtin numeric consumers | 60 sites in phase 1's node set (22 BinOp, 10 AugAssign, 5 UnaryOp, 10 Compare, 13 walked calls); exactly 1 outside it — `round` at line 335. 16 f-string format targets listed and checked; none raises on a non-finite value |
| `./bin/test tests/test_session_cost.py -q -k "zero or naive"` in a `--no-local` clone at `ae3fe18` | 3 passed, 30 deselected |
| Mutation 1 — revert `parse_time`'s normalisation | exit 1, 1 failed — `test_a_naive_stamp_does_not_end_the_report` killed it |
| Mutation 2 — revert `share` to a plain division | exit 1, 1 failed — the zero-span case killed it |
| Mutation 3 — delete the non-positive-span explanation print | exit 1, 1 failed — the sentence is pinned by name |
| Clone restored, probes deleted, main tree checked | Clone status clean before removal; main tree clean at `ae3fe18` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, repository-wide lint and typecheck | `agent-contract` §2 reserves the broad gate; not run, and this round declines to widen | the orchestrator, once the rounds settle |
| `templates/config.md#"# Repository config"` and `round_record.py#swallowed`, both DRIFTED | Already carried in `overview.md` §Not verified with an answerer; confirmed present at the base and untouched by this branch | the orchestrator, or the branch whose edits drifted them |
