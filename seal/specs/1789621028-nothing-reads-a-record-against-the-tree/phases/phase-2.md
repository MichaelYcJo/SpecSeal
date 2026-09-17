# 1789621028-nothing-reads-a-record-against-the-tree — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 34730974 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Close #427's write half. Ahead of the write at `round_record.py:3771`, `close`
refuses to prefix a `Grounds` cell it has already prefixed — for all three
verdict words, naming the finding and saying to restore the `Grounds` cell as
well, with nothing written to disk when it fires. Three cases, one per verdict
word, each seen red with the guard deleted; the #427 reproduction refused; and
the byte-identical doubled row reproduced with the guard removed. Exits read
directly, never through a pipe.

## What this phase found

**Q4 is answered: it refuses, ahead of the write, and refusing does not block
the documented way out.** `questions.md` Q4 defaulted to refusing and made the
phase measure whether that blocks correcting a record and re-closing it. It
does not, and the reason is the shape of the repair: the guard fires on the
HALF-restored record — `Verdict` back to `open`, `Grounds` left as `close`
wrote it — and stays silent on the fully restored one.
`test_the_documented_repair_still_closes` is that measurement, and it closes
green with the second row byte-identical to the first. So refusing costs the
author one more restore and tells them which half is still half-repaired,
where overwriting would have discarded the reviewer's sentence silently — the
thing the join at that line was written for.

**The guard has two arms, because one of them closes the instance and not the
class (§12).** #427's own reproduction re-runs `close` with the SAME fix
table, so the cell already begins with the exact text this run would write and
`old.startswith(grounds)` sees it. That arm covers all three words, since all
three reach the join. It does not cover a fix pass that amended its commit
between two closes, or a row reopened and re-closed under another word: the
text changed, so the comparison sees nothing while the cell still carries a
close prefix. The second arm reads the SHAPE, and that shape is
`chain_check.CLOSE_PREFIX_RE` — the same pattern phase 3's reader uses, held
in the checker so the writer and the reader cannot drift apart about what a
close prefix looks like.

**One of the three words has a shape a reader can recognise after the fact,
and this is what bounds phase 3.** `fixed` writes `fixed at <sha>`. `answered`
and `deferred` write the author's own words into the cell, so a standing
duplicate of either is indistinguishable from prose that repeats itself. The
generator's guard catches all three at the moment of writing; only the `fixed`
shape survives into a committed record for a checker to find. Phase 3 is
therefore a reader of that one shape, and saying so is better than a reader
that pretends to cover three.

**Nothing reaches disk when it fires, and that is a property of where it
sits.** `write_record` runs after the loop the guard raises in, so a refusal
leaves the half-restored record exactly as it stood — which is what makes the
refusal's instruction possible to follow. Each refusal case asserts the record
text is unchanged, not only that the exit was 2.

**The measurements, executed 2026-09-17.** Exit codes read from
`subprocess.run().returncode`; the generator mutated from bytes kept in the
driver and restored from those bytes; `tests/__pycache__` cleared between runs.

| Run | Exit | What it printed |
|---|---|---|
| `tests/test_the_fixes_close_the_record.py`, whole module | **0** | 88 passed |
| The five new cases, guard in place | **0** | 6 passed, 82 deselected |
| Guard deleted | **1** | the three word cases and the changed-commit case failed; 4 failed, 2 passed |
| Guard widened to `if old:` | **1** | `test_the_documented_repair_still_closes` failed — the case that pins the direction which must stay open |
| `FIXED_AT` respelled as its own literal | **1** | `test_the_generator_and_the_checker_spell_the_close_prefix_once` failed |
| Neighbouring modules — `test_the_record_is_generated`, `test_chain_check_at_the_pull_request`, `test_the_fixes_name_their_surface`, `test_gates_do_not_fail_open`, `test_one_word_one_meaning` | **0** | 313 passed |
| `uvx ruff check` over the two scripts and the case module | **0** | |

Two of the five cases cannot be reddened by deleting the guard, and that is
correct rather than a gap: one pins the ABSENCE of a refusal and the other
pins that there is one spelling of the prefix. Each was shown red against the
mutation it is actually about, in the table above.

**The doubled cell, reproduced.** A probe (`test_tmp_*`, run once and deleted,
§7) closed a fixture record, restored its `Verdict` cell alone, and closed
again with the guard removed:

| | Cell |
|---|---|
| First close | `fixed at 891bfcf; executed` |
| Second close, guard removed | `fixed at 891bfcf; fixed at 891bfcf; executed` |
| Second close, guard in place | `fixed at 891bfcf; executed`, unchanged, exit 2 |

The guardless second close exited **1**, and on the unrelated `Pass` /
`Fixes checked by` notice — saying nothing about the duplication. That is
#427's account of the real incident, reproduced in a fixture.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `round_record.py`'s own `FIXED_AT = "fixed at"` literal | `chain_check.CLOSE_PREFIX`, which the generator now aliases. A case counts the literals so a second spelling cannot come back |
