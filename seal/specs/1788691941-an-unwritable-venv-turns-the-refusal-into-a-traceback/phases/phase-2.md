# 1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback — phase 2

<!-- seal/specs/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 3bf5c6d |

<!-- The phase's substantive work is `d210bac` (the derived case) and
`3bf5c6d` (the two ledger judgments); the Commit row and `plan.md`'s Status
cell carry the second, which is the one that closed the phase's argument. The
records and the mutation loop's repair follow it. -->

| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The second and last phase of the build: the two closings phase 1 left, and
this work item's records.

1. **R2's caveat, in `seal/ledger.md`.** Its claim reads *the virtualenv is
   invisible to git on every exit of `ensure`*, and phase 1 makes that false
   in a new way on one path: the exit is now reached, the ignore is still not
   written, and the runner says so instead of raising. The fragment rule keeps
   a branch out of the shared ledger and its own text carves out this case —
   *a branch that removes code an existing `seal/ledger.md` row cites must
   touch that file to leave the ledger true*. Judge whether R2 is
   **falsified** (a removal, and the new claim goes in this work item's own
   fragment) or **under-specified** (a caveat in place); say which and on what
   grounds, and do not take the issue's word for it. Re-stamping the rows this
   branch never opened is not this phase's — say what drifted and leave those.
2. **The reach-vocabulary case.**
   `tests/test_the_fixes_name_their_surface.py#test_the_section_names_the_words_the_writer_can_put_in_a_reach`
   reads three constants out of `round_record.py` and goes red when one is
   renamed or its value changes — measured, three ways. What it cannot see is
   a **sixth** value added to `call_sites`, which is the drift the paragraph
   it guards exists against: the document would go stale and the suite would
   stay green. The document is correct today, so nothing ships broken. #177's
   *Done when* offers two closings — the case notices a value `call_sites` can
   return that the document does not name, **or** the limit is written down
   beside it. Pick one and argue it. If the first: the returnable set has to
   be derived from the function rather than listed beside it, or the case has
   the same defect one level up.
3. **The records.** The ledger fragment, the changelog fragment (never
   `CHANGELOG.md`), this file, `plan.md`'s Status cell, and `overview.md`,
   whose `## Not verified` section is read by a machine and has one shape.
4. **`docs/flow.md`.** The 0.8.3 section has no row for #177 — the four items
   0.8.2's work opened were never written in. Add the row for #177 only,
   ticked. #175, #180 and #182 are each another branch's to write.

Handed over as **unverified**: that phase 1 edited two of R2's anchors.

## What this phase found

**The handoff's unverified fact was one anchor too many, and measuring it is
what settled the judgment below.** Phase 1 edited exactly one of R2's nine
anchors. The unscoped read before any edit named three drifted rows in the
whole repository and only one of them is R2's — `hide_from_git`. `ensure` was
untouched (phase 1's diff is the module docstring and that one function), and
the six cases R2 cites are untouched because an anchor is a unit and phase 1
added functions beside them rather than editing them. The other two drifted
rows, `templates/config.md` and `round_record.py#swallowed`, belong to edits
this branch never opened and are left exactly as they were.

**R2 is under-specified, and the test that decides it is whether code the row
cites was removed.** `CLAUDE.md` states the removal rule over the anchor — *a
row whose anchor a change removes is REMOVED, not re-pointed; its claim went
with the code* — and this branch removed nothing. `hide_from_git`, `ensure`'s
`finally`, `build`'s own `finally` and all six cases stand, and every one of
them is green.

Which leaves the harder half: is the CLAIM false? It is not, and the reason is
that the claim is about a mechanism rather than about an outcome the write can
fail to produce. What R2 says is that the ignore is owed to a function's exits
instead of to a list of remembered paths, and its three recorded tidy-ups are
all attacks on that mechanism — delete the function, move the call back onto
the successful path, turn the `finally` back into a list. Phase 1 touched none
of them; the guard is what keeps the mechanism working on a path where it
previously raised.

**The outcome half had always been conditional, and #177 is what made the
condition visible rather than what created it.** On an unwritable `.venv` the
directory was not invisible to git before this branch either — the write
raised through the `finally`, so R2 was false on that path in the worse of the
two ways, with a traceback replacing the refusal that had already printed. A
caveat that states a precondition which was there all along is a row repaired
in place. Removing it would delete a claim that is true, and take the three
tidy-ups' guards with it.

So the shape is: the caveat and the re-stamp on R2 in `seal/ledger.md`, and
the guard's own evidence — the two cases, the fixture, the exit code, the
`git status` line — as a new row in this work item's fragment, which is where
the fragment rule puts a new claim.

**`--reverify` cannot narrow below a file, so R2's anchor was re-stamped by
hand.** The scoped write form takes `--ledger <glob>` and nothing finer, and
`seal/ledger.md` holds two drifted anchors this branch never read. Running it
there would re-stamp them on behalf of a session that never opened them, which
is the one thing the handoff said was not this phase's. The hash was computed
the way the tool computes it — `resolve_unit` for the region, `content_hash`
over those lines — and written into the row directly: `63e2d9b9` → `08f18fc6`,
one place, not resurrected, which is the branch `reverify` itself would have
taken. The scoped run on the fragment then produced `08f18fc6` for the same
anchor independently, so the hand value is confirmed by the tool rather than
merely asserted. The unscoped read went 3 drifted → 2, and the two that remain
are the two this branch never read.

**The vocabulary case took the first closing, and the project's own goal is
what decides between them.** A written limit and a derived case do not catch
the same defect: the limit tells a future reader the drift is possible and
stops nothing, while the derivation refuses the commit that causes it. The
goal statement at the top of `CLAUDE.md` ranks these explicitly — between two
designs, the one that stops to ask a person is the more expensive — and the
tie-break only applies where both catch the defect, which here they do not.
`RECORDED_LIMIT` in the same module is the house form for the second closing
and it was declined for a reason the second closing itself states: it exists
where closing the limit would mean enumerating an unbounded domain, and this
domain is not unbounded.

**The set is derivable because the values that can go stale are fixed in the
function's source.** `call_sites` returns module-level string constants named
in a `return`, and the two open-ended categories the document names as
categories — the enclosing top-level unit, the file's basename — which are the
reviewed repository's own names. `reach_values` walks the function's `return`
statements for names that resolve to module-level string constants, plus
string literals written into one, so a fourth constant joins the derived set
with nobody editing the test file.

**Both cases are kept, and that is a decision rather than an oversight.**
Neither covers the other. A constant added to `call_sites` is invisible to the
named form, and the mutation run shows it — `1 failed, 1 passed`.

<!-- CORRECTED in round 1's fix pass (finding 1). This paragraph also claimed
a constant renamed with its value untouched is caught by the named form
alone. It is not: the derived case builds its floor from the same three
constants by attribute name, so a rename and a reword redden BOTH. The named
case's real unique catch is `only the first is a unit name`, which the derived
case never reads. The **Executed** label below covers the addition mutation,
which is the half this phase's run measured; the other three were measured in
the fix pass and are in `rounds/round-1.md`. -->

Their docstrings say which is which, where a reader would type the deletion.

**The derivation's own vacuous pass is guarded before the loop.** A derivation
that stops finding anything leaves the assertion loop with nothing to iterate
and the case green, which is `agent-contract` §15's failure built into the
case rather than found in it. The count is asserted first, and `call_sites`
being found exactly once is asserted inside `reach_values`.

**What the derivation does not reach is recorded rather than closed**, in
`reach_values`' docstring: a value another function hands back, and one
formatted at run time. Closing those means resolving a call across functions,
which is the enumeration `RECORDED_LIMIT` declines two screens up for the same
reason.

<!-- CORRECTED in round 2's fix pass (finding 10): this describes the recorded
limit as phase 2 wrote it, and the derivation was rebuilt twice afterwards.
The docstring now records five under-reach shapes, six more that are one
branch away, and TWO over-reaches rather than none; `formatted at run time`
is in neither list, because an f-string is a fixture expecting an empty set.
`rounds/round-1.md` and `rounds/round-2.md` carry the current shape. The
paragraph stays because it is phase 2's record of what phase 2 built. -->


**R8 is R2's shape one document over, so it is repaired the same way.** Its
claim ended *so the document cannot drift from the generator*, and reading
three constants by name is three ways of catching a rename and no way of
catching a fourth. The claim is narrowed to those three, its Notes carry the
measurement, and the wider claim is a second row in the fragment. Its anchors
did not move, because the existing case was not edited — the derived case is a
new function beside it.

**The derivation's literal arm was unreachable, and only the mutation loop
found it.** `call_sites` names a constant in every one of its returns and
writes no string literal into one, so against the real module the arm that
reads a literal cannot execute: deleting it left the whole module green. That
is an arm no case can kill, planted by the very phase that was closing #177's
*the list would be the thing going stale* — the same defect one level down.
`reach_values` takes the generator's text as a parameter now, defaulting to
the real module, and seven fixtures exercise both arms, both type checks, and
the two halves of the recorded limit. Six mutations, one at a time, each dead
and each named. The parameter is the first thing that will read as test-only
machinery, so the row says what it buys where the deletion would be typed.

<!-- CORRECTED in round 1's fix pass (finding 4): this said six fixtures where
`DERIVATIONS` had seven. The count moved again in that pass — the derivation
became `handed_back`, one arm per way an expression carries a value outward,
and the fixtures were re-enumerated over those arms and over the
over-collection shapes round 1 measured. The round records carry the current SHAPE, and
no number here or there should be read as current: round 2's fix pass added four
more fixtures without touching this marker, which is round 3's finding 8. The
numbers in this record are phase 2's, at `3bf5c6d`. -->

**The "six mutations" figure above is a mutation count and stays correct.**
Only the fixture count was wrong.

**The vacuous-pass guard was a bare count and is now a floor with content.**
`len(values) >= 3` is a number anybody can lower without noticing; the derived
set is required to contain the three constants the named case reads, so the
guard fails by naming what went missing and dies under the mutation that
empties the derivation.

**The format hook removes an import added in a call of its own.** `import ast`
was added before its caller existed, the `PostToolUse` formatter stripped it
as unused, and the next run failed with `NameError`. Nothing was lost, but the
edit order matters here: add the import in the same call as the code that uses
it, or expect to add it twice.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

## Runs

**The unscoped ledger read, before any edit, executed** —
`./bin/evidence-check .` → exit `1`, read directly:

```
seal/ledger.md
  DRIFTED  templates/config.md#"# Repository config"  content changed at 1-147 — re-verify
  DRIFTED  .github/scripts/run_tests.py#hide_from_git  content changed at 116-164 — re-verify
  DRIFTED  skills/code-review/scripts/round_record.py#swallowed  content changed at 431-553 — re-verify
  678 ok · 3 drifted · 0 broken · 0 external · 0 old-format
total: 688 ok · 3 drifted · 0 broken · 0 external · 0 old-format
```

**The same read after, executed** — exit `1`, and the exit is the two rows
this branch never opened:

```
seal/ledger.md
  DRIFTED  templates/config.md#"# Repository config"  content changed at 1-147 — re-verify
  DRIFTED  skills/code-review/scripts/round_record.py#swallowed  content changed at 431-553 — re-verify
  679 ok · 2 drifted · 0 broken · 0 external · 0 old-format
seal/ledger/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback.md
  6 ok · 0 drifted · 0 broken · 0 external · 0 old-format
total: 695 ok · 2 drifted · 0 broken · 0 external · 0 old-format
```

**Red, executed**, against a sixth value in `call_sites`' returnable set —
`NO_TRACKED_FILE = "not a tracked file"` added at module level and returned
beside `NO_SITE`. Both reach cases were run under the mutation, and the split
is the finding:

```
=== MUTATED: a sixth value in call_sites' returnable set ===
--- exit: 1
.F
E   AssertionError: the section does not name `not a tracked file`
1 failed, 1 passed, 33 deselected in 0.07s
```

The one that passed is `test_the_section_names_the_words_the_writer_can_put_in_a_reach`,
which is what #177 reports. The mutation was restored from bytes kept before
it — never from `HEAD`, which would have taken the uncommitted work in the
tree with it — and the restore was verified byte for byte:

```
=== RESTORED ===
--- exit: 0
2 passed, 33 deselected in 0.05s
restore verified byte for byte
```

**Six mutations over `reach_values`, one at a time, executed.** Each was
applied to a kept copy, run, and restored before the next; `tests/__pycache__`
was cleared between them. The first run left one alive:

```
DEAD      the named-constant arm deleted                    exit 1
DEAD      the literal arm deleted                           exit 1
SURVIVED  the string check on a literal dropped             exit 0
DEAD      the return-only filter dropped                    exit 1
DEAD      the one-definition guard weakened to any          exit 1
DEAD      the derivation emptied                            exit 1
```

The survivor is the finding: no fixture put a non-string literal inside a
`return`, so dropping the type check on that arm changed nothing any case
could see. One fixture closes it, and the loop re-run reads six DEAD with the
killing case named for each — `test_the_derivation_reads_both_shapes_a_return_can_fix`
for the arms and the type checks, `test_a_second_call_sites_is_refused_rather_than_picked_from`
for the guard, and `test_the_section_names_every_reach_value_the_generator_fixes`
for the return-only filter and the emptied derivation. Restored byte for byte
and green.

**Green, executed.** `./bin/test tests/test_the_fixes_name_their_surface.py -q`
→ `43 passed in 7.90s`, exit `0` read directly rather than through a pipe.
(`35 passed` at `d210bac`, before the derivation fixtures.)

`uvx ruff check` and `uvx ruff format --check` on
`tests/test_the_fixes_name_their_surface.py`: exit `0` and `1 file already
formatted`. The `.venv` carries no `ruff` module, so `uvx ruff` is the form.

## What the review round must know

- **The suite is unverified**, labelled per `agent-contract` §2 with the
  orchestrator as its answerer. Two modules were run:
  `tests/test_the_fixes_name_their_surface.py` in this phase and
  `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` in phase 1.
  Nothing else on this branch has been executed since.
- **The two drifted rows in `seal/ledger.md` are left deliberately** and are
  not this branch's to close. They are named in `overview.md`'s
  `## Not verified` with an answerer.
- **The judgment to attack first is R2's under-specified reading.** It rests
  on the claim being about a mechanism, and a reviewer who reads the claim as
  being about the outcome — *invisible to git* — reaches the opposite verdict
  and a removal. Both readings are in the row's own text; the grounds for
  taking the first are in R2's Notes and above.
