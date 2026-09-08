# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | db58253 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#211: `Contract changes` reads `no call site found` for a pytest test
function, where `pytest only` is the value that exists for it. The ticket
proposed the repair itself — *`call_sites` recognising a `def` under `tests/`
whose name begins with `test_`* — and left one question in its own *Not
verified* section: whether other unit kinds reach `no call site found` for the
same reason.

## What this phase found

**That open question has an answer, and taking the ticket's proposed repair
would have shipped half a fix.** `call_sites` was run over every top-level def
under `tests/` at `ba22b28` rather than reasoned about: 1892 of 1947 `test_*`
defs read `no call site found`, and so did **8 of 42 fixtures**. A fixture is
injected by parameter name, so a fixture whose only consumers are tests has no
`name(` anywhere in the tree — the same cause, one kind over. A `conftest`
hook is a third member by the same construction, and this repository holds
none, which is why its case is built in a repository the test creates.

**One unit under `tests/` reads `no call site found` correctly, and it is
what bounds the rule.** `tests/test_the_reopening_is_one.py#floor_record` is
passed by name as a value at five sites and never called. A rule reading
*anything under `tests/`* would say *the runner covers this* about a unit
nothing covers — #211's own false sentence pointing the other way — so the
rule is the three pytest constructions and a case refuses the wider one.

*Corrected by round 2's fix pass.* That was true of the tree this phase ran
against and is not true of the branch. `floor_record` stopped reading `no call
site found` at `824bfca`, where round 1's record and report landed quoting its
`def` line — the walk greps every tracked file, so a committed record that
quotes code invents a call site for the unit it quotes. The unit bounding the
rule at HEAD is `tests/test_the_records_can_be_carried_out_and_in.py#timed_out`,
which the merge of `release/v0.9.1` brought in. What the phase decided is
unchanged; only the example moved.

**One limit is recorded rather than closed, and it was a surviving mutation
that forced the decision.** The hook arm reads `conftest.py` alone; pytest
also registers collected test modules as plugins, so a `pytest_generate_tests`
in a test module really is dispatched and really has no call site — and still
reads `no call site found`. Widening the arm would catch it and would also
catch any helper somebody named `pytest_something`. The narrower rule with the
limit written down is the trade, in the spec section and in a case.

**No reach value was added, which is why this phase moved no vocabulary.**
`PYTEST_ONLY` already meant *the runner is the reach*, so
`docs/review-chain-spec.md`'s five-value enumeration and
`test_the_fixes_name_their_surface.py`'s derivation of that vocabulary from
`call_sites`' own source both stayed green. What DID need writing is that the
section defined `pytest only` by its CALLERS, and a collected test function
has none — a reader checking the row against the section found the value
undefined for the case it now appears in.

Phase 3 needs one thing from here: `call_sites` is now reached for more units,
because phase 3 widens what enters `Contract changes`. The cost is one
`git grep` per newly-admitted unit, and `runner_reached` adds one `git show`
per unit whose reach comes back empty.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing | — the phase adds two units and one branch; the sentence in `docs/review-chain-spec.md` defining `pytest only` by its callers alone is widened rather than replaced, and still stands for the case it was written for |
