# Implementation Plan: two in-range values make one that is not

<!-- seal/specs/1788873620-two-in-range-values-make-one-that-is-not/plan.md -->

## Summary

A checker that enumerates the int-conversion sites of `session_cost.py` from
the module's own syntax tree and refuses one that is not discharged. Nothing
about the shipped behaviour moves; what the branch adds is a rule that fails
in CI when a new site arrives without a guard.

**The predicate is the whole design.** Two questions have to be answered
without a list, because a list is what #192 exists to replace:

- **Is this site an int conversion?** Answered by the language's own
  integer-conversion protocol. Python reaches an `int` through exactly six
  operand methods — `__int__`, `__index__`, `__trunc__`, `__round__`,
  `__floor__`, `__ceil__` — so the checker passes an operand that records
  which of them is invoked and calls the site's own callable. `round`, `int`,
  `math.floor` and a locally written `def to_int(v): return int(v)` all answer
  the same way, and no name appears in the checker.
- **Is this member discharged?** Either its operand cannot be a derived
  number — an integer literal, or integer arithmetic over integer literals —
  or a guard dominates it: a finiteness test on the same operand, or a `try`
  whose handlers catch what the conversion raises. *Finiteness test* is
  decided by probing too: a callable that answers truthily for a benign float
  and falsily for both non-finite ones. *Catches what it raises* is decided by
  `issubclass`, so an aliased or tupled exception classifies correctly.

That is why the checker has no name list and no count anywhere in it, and why
its failure message names the property rather than a total.

## Technical context

- `skills/verify/scripts/session_cost.py#token_thirds` — the one member today.
  `means.append(round(mean) if math.isfinite(mean) else 0)`: the conversion is
  the `round`, and the guard is the finiteness test in the enclosing
  conditional expression, not the `try` above it, which wraps the division.
- `skills/verify/scripts/session_cost.py#count` — the funnel for values that
  ENTER. It answers per value; nothing answered for a sum, which is #192.
- `tests/test_a_new_returnable_value_is_a_contract_change.py` — the shape this
  follows: enumerate a class from a module's own source, cross-check the
  derivation rather than trusting one reading, and assert the check is not
  vacuous.
- `tests/test_session_cost.py#test_a_sum_of_entered_values_does_not_end_the_report`
  — the three measured shapes of #192's table, already planted by round 3 of
  #175. This branch adds no transcript case; those three are the case set and
  they are re-run.

**What breaks in six months.** The probe CALLS the callables the module calls.
Every one of them is enumerated from the source, and the operand it is handed
answers no protocol but the six — so a callable that is not a numeric consumer
raises `TypeError` on the spot and nothing reaches a filesystem. What a future
edit could do is call something whose mere invocation matters, and the probe
would invoke it. The bound on that is the operand: with an object that has no
path, no string value and no arithmetic, a destructive call has nothing to act
on. Stated in the checker's docstring, because it is the cost of deciding
membership by execution instead of by a list.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A per-operation walk: per operator, can finite operands make a non-finite result | #192 measured it — round 3's defect arrived through a call the walk had held in its list from the start. A site enumeration answers which operations exist, not what they make of two values that passed | Rejected by the owner in `routing.md` |
| Membership by name list (`int`, `round`, `math.floor`, …) | The list is the failure mode this release is named for. Round 3 of #175 already recorded the two forms a name list misses — a `from`-import and an alias — and closing them means widening a list and building an alias table | Rejected; resolving the binding and probing the object closes both for free |
| Membership by *raising*: any site that raises on a value `count` admits | Strictly wider, and it flags `share`'s `part / whole * 100`, which is unguarded today and whose operands are seconds. Closing it means changing behaviour #192 did not ask about, on a site nobody has measured a failure at | Rejected; recorded as Q2 for the owner |
| Include subscript and slice bounds, which convert through `__index__` | Whether a bound is a derived number cannot be decided without provenance: `by_family[key][0]` indexes with a local name, and exempting it needs a rule that either lets a derived bound through or reddens the module today | Rejected; recorded as Q1 for the owner and stated in the checker |
| Widen the walk over the whole tree | Every `round(` in every script becomes a member and the diff stops being about #192. The module is the one whose operands come out of a transcript | Rejected; the scope is stated rather than assumed |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The checker — the walk, the probes, the discharge analysis, the cases — **and** `token_thirds`' docstring naming the class, the check and the shapes the property does not reach | `./bin/test tests/test_a_derived_number_reaching_an_int_carries_a_guard.py tests/test_session_cost.py -q` | b08bab4 |
| 2 | The mutation battery, and what it changed: five units gained the case that exercises them, `integer_shaped` stopped excluding `bool`, and the cannot-raise discharge gained a shape | 44 mutations one at a time, 43 caught; the survivor recorded in `Converted`'s docstring | 1ccfbb9 |
| 3 | The records: ledger fragment, the one re-read row in `seal/ledger.md`, changelog fragment, questions, phase records, overview, and the `#192` box in `docs/flow.md` | `evidence_check.py --reverify`, then the two test modules unchanged | ae0c238 |

The docstring was planned as phase 2 and shipped inside phase 1: the
checker's last case pins it, so splitting them would have shipped a red case.
The mutation battery took the freed number because it changed code rather than
only measuring it — `overview.md`'s divergence table carries both.

## Operational impact

None. No migration, no new environment variable, no new dependency: the
checker uses `ast`, `builtins`, `contextlib`, `io` and `math` from the
standard library. Nothing a deployer touches.

**The prompt budget is zero.** The check runs in the suite and in CI and puts
no question in front of anybody; its failure is a red case naming a
coordinate.

**The failure direction is toward blocking.** A `try` guard is accepted only
when its handlers catch both `OverflowError` and `ValueError`, because a
derived value can be an infinity or a `NaN` and the two raise differently — so
a site guarded against one of them is refused. That is the cheaper mistake
here: a wrong refusal is a red case with a coordinate in it, and a wrong pass
is the report ending with stdout empty, which is the outcome #175 spent four
rounds on.
