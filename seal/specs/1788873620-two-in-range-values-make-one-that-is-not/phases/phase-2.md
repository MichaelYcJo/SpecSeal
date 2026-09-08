# 1788873620-two-in-range-values-make-one-that-is-not — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 1ccfbb9 |
| Ran by | unknown — the spawn prompt named no model, and a segment must not source this row from its own idea of what it is; the orchestrator fills it |

## What this phase was asked

Mutation-test every unit the branch adds, one at a time — break it, run the
cases that cover it, watch one go red, restore from bytes kept rather than
from HEAD, and clear `tests/__pycache__` between mutations. The checker in
particular had to be **seen red against an unguarded site introduced into the
real module and then removed**.

## What this phase found

**Forty-four mutations, and the first pass left five survivors that were each
a unit no case exercised.** That is the whole argument for doing this rather
than reading the file again: every one of the five looked covered, because
the module was green and the unit was called on every run.

| Survivor | Why nothing caught it | What now covers it |
|---|---|---|
| the resolver's literal-receiver branch | `" ".join(...)` is the only such call, and losing it moved the site into the residual, where the stray filter skips a callee with no root name | `test_a_call_on_a_literal_receiver_resolves`, which also refuses the case as vacuous if the module stops calling a method on a literal |
| `root_name` | no stray existed either way, so the residual check passed with the function returning nothing at all | `test_the_residual_check_names_a_callee_the_module_binds_nowhere` — a constructed module whose callee the module binds nowhere, which is the shape the residual promise refuses |
| the consumes-an-integer half of membership | nothing in the module both fails that probe and yields an exact int, so making it always true changed no verdict | `test_a_callable_that_yields_an_int_without_converting_is_not_a_member` — a function answering with an integer it never converted, which cannot raise and must not be asked for a guard |
| the operator probe (`operator_forms`, `operator_raised`) | the operator answer is structurally *no* under numeric probing, so a broken probe returns the same no | `test_the_operator_half_is_probed_and_says_what_it_cannot_see`, with sequence repetition as a positive control |
| the finiteness predicate's own benign answer | every refused shape in the table failed for a different reason first | a shape whose predicate is falsy for a benign number too |

**Two more survivors were code rather than missing cases, and both are worth
recording as judgments.**

- `integer_shaped` excluded `bool`, copied from `count`'s reasoning without
  the reasoning. `count` excludes `bool` because `True + 1` is a wrong number
  in a token column; the question here is only whether a transcript could
  have derived the operand, and a literal `True` derives from one no more
  than a literal `7` does. Keeping the exclusion refuses `round(True)`, which
  cannot raise. Removed, with a shape pinning it.
- the cannot-raise discharge had no shape behind it. A converter that guards
  itself internally is now one of the constructed shapes, which is also the
  shape that shows detection surviving a callable that swallows `Exception`
  around its own `int()`.

**One survivor is being kept, and the docstring now says so instead of
overclaiming.** `Converted` derives from `BaseException` so a probed callable
cannot swallow the signal — but `_recorder` records *before* it raises, so
detection never depended on who catches it, and no case can tell
`BaseException` from `Exception`. What the base class actually buys is
stopping the callable at the conversion rather than letting it run on. The
alternative to recording this was a case that pins the class statement to
itself, which proves nothing.

**Final count: 43 of 44 caught.** Both mutations of the shipped module are
caught by name — the finiteness guard removed from `token_thirds`, and a new
unguarded `int(sum(spans))` added in a unit nobody thought to look at, each
reported with its unit and line. Deleting the subscript residual from
`token_thirds`' docstring is caught too, which is what keeps a stated limit
from being silently unstated.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `integer_shaped`'s `bool` exclusion | nowhere — it was `count`'s reason applied where it does not hold, and the reason stays with `count`. The judgment is recorded above and in the checker's own docstring |
| the hardcoded `(OverflowError, ValueError)` pair a `try` guard had to cover | `raised_by`, which probes what each conversion actually raises; the ledger fragment's second row carries the claim |
