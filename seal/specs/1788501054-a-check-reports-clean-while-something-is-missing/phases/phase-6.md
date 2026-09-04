# 1788501054-a-check-reports-clean-while-something-is-missing — phase 6

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-6.md
— what this phase of the build did, written by the implementer when the phase
closes. Not in `plan.md`'s original four: round 2's fixes are work the plan did
not contain, and the phase row was added beside them. -->

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | <the commit that closed this phase> |
| Ran by | specseal:smith on opus |

## What this phase was asked

Round 2's five open 🟡, and then a sixth the orchestrator handed back after
closing its own half of it:

- **🟡 4** — `added_on_branch`'s summary line still says *first added* while
  its body says the opposite twenty-six lines down.
- **🟡 5** — the case docstring and the spec both still say *oldest commit
  that touched*, and both are false by measurement: dropping
  `--diff-filter=A` turns two cases red, not one.
- **🟡 8** — the inode fold goes silent where `st_ino` is 0.
- **🟡 9** — the bound sentence's pointer names the wrong row.
- **🟡 10** — R6 claims no column can distinguish a re-read that happened
  from one that did not, and the same commit disproved it four times.
- **🟡 6**, reassigned mid-phase from *weigh it* to *build it*: this branch
  made a record's fix surface start out provisional and required no second
  step, so a verifying round reading the record alone sees no finding
  surface. The orchestrator's message named `Fixes checked by` as the
  discriminator and set two things to settle rather than assume — which
  reasons mean *not yet*, and whether the arm reaches `Contract changes` too
  — and one thing it must not do: refuse the honest mid-run state.

Constraints: unscoped `evidence_check.py .` for reading, no unscoped
`--reverify`, and the depth checked rather than assumed.

## What this phase found

**The `allow` direction is the whole design of 🟡 6's refusal, and it is this
file's only one.** Three keys were weighed. Refusing any `none` that carries a
reason is the widest and it refuses `none — the fixes deleted a line`, which
is honest. Keying on a phrase is prose matching, the enumeration over an
unbounded domain the arrow's and the comma's limits already decline. What made
the third defensible is that the phrase is not arbitrary prose: it is what
`templates/sdd-round.md` prints, so it lives in `chain_check.py` as `NOT_YET`
and a case ties the two files together. The cost is stated rather than buried
— a reworded cell escapes, so *this record passed* means *its cell does not
carry the template's own pending words*, never *its fix surface is complete*.

**The discriminator needed no new source of truth, and that is what made it
worth building at round 2.** `Fixes checked by` already says whether a later
round opened these fixes. While it reads `nobody`, *not yet written* may be
true; once it names a `round-N`, the fixes exist and the cell contradicts its
own file two rows above it. That is the third instance of the
contradiction-inside-one-file shape `chain_check.py` already refuses twice.

**Two mutations survived the first battery and both were coverage gaps rather
than noise.** Dropping the `OSError` fallback and letting `os.stat` raise left
every case green — nothing had ever handed the checker a path it could find
and not stat. A broken symlink is how that arrives through the CLI, because
`glob` returns one for a literal pattern and `os.stat` then raises. And keying
the pending arm to `SURFACE_FROM` instead of `ORDER_FROM` left everything
green, because every fixture sat below both cutoffs or above both: the case
that separates them is a work item begun BETWEEN the two, which owes the rows
and not this arm. Both cases were written and both mutations now die.

**A case read the file it lives in and its own needle satisfied it.** The
pin for 🟡 5 asserts that *oldest commit that touched* appears in neither the
spec nor this test file — and spelled as a literal, the assertion line is
itself an occurrence, so the case passed whatever the docstring said. The
needle is built from two pieces now, with the reason beside it. That is the
shape `seal/ledger.md` records as a case green against its own mutation, met
from the inside for the first time.

**Round 2's `--diff-filter=A` measurement is what makes 🟡 5 a defect rather
than a stale sentence.** Under the earliest add the flag was separable only by
a base that moves under a long branch; under the latest add the newest
commit that merely TOUCHED a record is its verdict update, which descends from
the fix. So the flag now protects the ordinary record, and the case docstring
claimed the mutation does not reach the ordinary case. Both descriptions are
corrected and the docstring now says what the flag carries.

**🟡 10's repair is a convention, and the row that claimed otherwise is the
one this phase rewrote.** R6 said no column can distinguish a re-read that
happened from one that did not. The Notes column can, and the round-1 fix pass
had already used it on four of the eight rows. All eight now carry a
`Re-read 2026-09-04` clause naming what the re-read found, so the trace lives
in `seal/ledger.md`, which is permanent, rather than in `phases/phase-4.md`,
which the release removes.

**The branch's own two records pass the new arm, checked rather than
argued.** `round-1.md` has its rows filled and `round-2.md`'s read *not yet
written* while `Fixes checked by` says `nobody` — the honest mid-run state.
Running the checker on this tree fires the arm on neither; what remains is the
unchecked `Pass` on the last record, which is what a run in progress looks
like.

**The depth question again does not bite.** `says_not_yet` and `NOT_YET` sit
beside `says_none` and `fix_surface`, which predate this work item entirely,
so they are depth 1 under every reading — no unit was added inside anything
the round-1 fix pass created.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Three descriptions of the earliest-add rule — the function's summary line, the case docstring's *oldest-touching* paragraph, and the spec's table row | The corrected copies, plus a case asserting the phrase appears in neither the spec nor the test file. `phases/phase-3.md` keeps its copy on purpose: it is a record of what was true at its own moment |
| R6's claim that no column can show a re-read | R6 itself, rewritten to say which column can, plus the `Re-read` clause on all eight rows of `seal/ledger.md` |
