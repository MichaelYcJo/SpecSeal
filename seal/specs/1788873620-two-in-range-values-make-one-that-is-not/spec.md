# Feature Specification: two in-range values make one that is not

<!-- seal/specs/1788873620-two-in-range-values-make-one-that-is-not/spec.md -->

Issue #192, release 0.9.3. Round 3 of #175 closed one site; what is left is
the class.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §12 — *a defect belongs to a class, enumerate the class* | The one site is already fixed. The deliverable is the enumeration, and §12 is why a second coordinate fix is not an answer |
| `CLAUDE.md` §*The goal a design is chosen against* | The check runs unattended in the suite, so a new unguarded site is refused by CI rather than by whoever notices |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test that can fail somebody's pull request is a gate: a case seen red, a stated failure direction, a prompt budget |
| `docs/flow.md` §*0.9.3 — the enumeration was done by reading* | The release's own sentence: replace enumeration by reading with enumeration by construction. A count is not a property |

## Scope

**In.** Every site in `skills/verify/scripts/session_cost.py` that converts a
number to an `int`, enumerated from the module's own source, with membership
decided by execution rather than by a list of names, and each member required
to be discharged — by a guard, or by an operand that cannot be a derived
number.

**Out, and each for a stated reason.**

- **The wrong-number direction** — a finite but nonsensical count summed as
  given. #192's own body keeps it open and the owner's routing answer keeps it
  out of this branch.
- **A per-operation walk** asking, per operator, whether finite operands can
  make a non-finite result. The owner chose the int-conversion property over
  it; #192 records why — round 3's defect came in through a call the existing
  site walk had held in its list from the start.
- **#200 and #202**, the two instrument defects scheduled into 0.9.4. Nothing
  here pins either behaviour as correct.
- **The two shapes the chosen property does not reach**, both stated in the
  checker's own docstring and in `questions.md` rather than left to be found:
  a subscript bound, and a true division that raises on two derived integers.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The class is enumerated from the source, not from a list | Given the module, when the walk runs, then every call and operator site in its syntax tree is examined, checked against a second independent reading | `test_the_walk_examines_every_call_and_operator_site` |
| Membership is decided by what a site does, not by what it is called | Given a converter with a name nobody could have listed — a local `def`, an aliased import, a `from`-import — when the walk runs, then it is a member | `test_the_guard_shapes_are_decided_by_what_they_catch`, the rows naming a local function, an alias and a `from`-import |
| A predicate that converts in order to answer something else is not a member | Given `math.isfinite`, which consumes its operand through `__index__` and answers a `bool`, when the walk runs, then it is not a member — asserted on both halves | `test_a_predicate_that_converts_but_answers_a_bool_is_not_a_member` |
| Both halves of membership are load-bearing | Given a function answering with an integer it never converted, when the walk runs, then it is not a member and is not asked for a guard | `test_a_callable_that_yields_an_int_without_converting_is_not_a_member` |
| What a conversion raises is measured, not written down | Given each conversion, when it is probed with the values `count` admits, then a `try` must cover what was seen and a `TypeError` from the probe's own filler is not a hazard | `test_a_type_error_is_not_a_hazard_the_guard_has_to_cover` |
| The shipped module has no undischarged member | Given `session_cost.py` as it stands, when the property runs, then no site is reported | `test_every_int_conversion_in_the_module_is_discharged` |
| A new unguarded site is caught by the checker | Given the module with one unguarded `int(...)` added, when the property runs, then that site is named with its unit and line | `test_an_unguarded_conversion_added_to_the_module_is_named` |
| The guard shapes the module uses are the shapes the checker accepts | Given the constructed shapes, when each is classified, then the guarded ones pass and the unguarded ones fail — including the two measured refusals | `test_the_guard_shapes_are_decided_by_what_they_catch` |
| The operator dimension's answer is derived, with a positive control | Given every operator the module writes, when each is unparsed from its own node and probed, then none converts — and sequence repetition, which does, shows the answer is a measurement | `test_the_operator_half_is_probed_and_says_what_it_cannot_see`, `test_no_operator_in_this_module_converts_a_number_to_an_int` |
| The residual has one shape a next editor can act on | Given the sites the walk cannot resolve, when they are listed, then every one is a name the module binds inside a function or an expression with no name — never a name it binds nowhere | `test_the_unresolved_callees_are_runtime_receivers`, `test_the_residual_check_names_a_callee_the_module_binds_nowhere`, `test_a_call_on_a_literal_receiver_resolves` |
| A next editor of the module meets the rule | Given `token_thirds`, when someone opens it, then its docstring names the class, the checker and the two shapes the property does not reach | `test_the_module_states_the_rule_and_the_two_shapes_it_misses` |

## Data & interfaces

No interface changes. `session_cost.py` gains docstring text in
`token_thirds`; nothing it prints or returns moves. The new checker is
`tests/test_a_derived_number_reaching_an_int_carries_a_guard.py`, which reads
the module's source and never its output.

Existing evidence this builds on: `seal/ledger.md` §*What the cost meter can
read*, rows for `#count` and `#token_thirds`.

## Open questions → questions.md

Two, both about widening, both for the repository owner. Neither blocks: the
class the owner chose is buildable and complete over its own predicate
without either answer.
