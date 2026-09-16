# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 6

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-6.md -->

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `1376409` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#407. `one_finding_inside_one_earlier_unit` asserts its substitution landed,
and `test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one`
gains a positive assertion beside its two negatives. Class: all five `re.sub`
sites across `tests/test_the_fixes_close_the_record.py` and
`tests/test_the_record_is_generated.py` read, plus any the earlier phases
planted, each either guarded or recorded as already guarded.

Verified by `bin/test tests/test_the_fixes_close_the_record.py
tests/test_the_record_is_generated.py`, red-first with two mutations: break
the `New units` pattern so the substitution misses, and make round 1 name no
unit so `depth_two` returns at its guard.

**This phase was built once, reverted at a stop, and rebuilt from its own
diff against a tree two commits further on.** Both mutations were re-run
here rather than reported from the first build, because a mutation result
read off a previous tree is a claim about a tree that no longer exists.

## What this phase found

**The vacuity is real and it was executed, not argued.** With the `New units`
pattern broken so the substitution misses, and with neither the fixture guard
nor a positive assertion present, `test_a_unit_added_by_a_fix_outside_every_
earlier_unit_is_depth_one` **passes** — 1 passed, exit 0. Round 1 names no
unit, `depth_two` returns at its own guard, and both of the case's negatives
hold for a reason that has nothing to do with the finding it is named for.

**The class is five sites and one was already guarded.**

| Site | Substitutes | Before |
|---|---|---|
| `two_rounds` | `New units \| helper (depth 1)` | unguarded — **guarded** |
| `two_findings_inside_two_earlier_units` | `alpha (depth 1); beta (depth 1)` | unguarded — **guarded** |
| `one_finding_inside_one_earlier_unit` | `alpha (depth 1)` | unguarded — **guarded**, the site the issue names |
| `test_a_previous_record_whose_checker_cell_does_not_parse_is_refused` | the `Fixes checked by` cell | **already guarded**, and it is the house shape the issue says the author knew |
| `test_the_two_record_run_reads_back_through_chain_check` | `Contract changes` and `New units` to `none`, beside a `str.replace` closing the verdict | unguarded — **guarded**, both substitutions in one assertion |

Phases 1–5 planted no `re.sub` of their own, so the enumeration is closed at
five.

**Nothing in `close`'s output discriminates the two states, which is why the
assertion already in the case is not the one #407 asks for.** `New units |
beta_guard (depth 1)` is written from `measure` and `added` whether or not the
depth walk ran, so it holds in both. What is false in exactly the guard state
is round 1's own `New units` cell, read back from disk after the run — and
that is the assertion the case now carries.

**The second mutation only proves anything applied INSIDE the case.** Round 1
has to be renamed to `none` **after** the fixture returns, so the fixture's
new guard passes and the positive assertion is what goes red. Applied inside
the fixture, the guard fires first and the case is never reached, which
demonstrates the guard and says nothing about the case. Both orders were run;
the first turned the fixture red at `assert 'none — the fixes are not yet
written' == 'alpha (depth 1)'`, the second turned the case red at
`assert 'none' == 'alpha (depth 1)'` with both negatives above it holding.

**Nothing came out differently against this tree.** The two commits that
landed between the first build and the rebuild are handoff documents; the
diff applied clean, both mutations reproduced their earlier messages
verbatim, and the module count is 201 passed in both runs.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — four assertions are added and nothing is taken out of the tree | none |
