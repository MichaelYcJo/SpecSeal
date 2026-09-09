# 1788912166-red-for-following-the-documents-green-for-ignoring-one — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `13fbc4d` |
| Ran by | `specseal:smith on claude-opus-5` — filled by the spawning session, which is the only participant that knows what it spawned |

## What this phase was asked

The fragments, and the four `CONTRIBUTING.md` answers written where the pull
request will carry them. Verified by `evidence-check` and the narrow modules.

## What a change to a gate must carry

This phase changes no gate — it writes the records the other three owe. The
four answers per arm are in `phases/phase-1.md`, `phases/phase-2.md` and
`phases/phase-3.md`, and the pull request body carries them from there. Where
this phase touched behaviour at all, it is the prose a person reads, which is
answered below rather than as a gate change.

## What this phase found

**One of the three documents that had to be corrected was documenting the
defect as expected behaviour.** `skills/code-review/orchestration.md` said the
`release` leg *"is red from the draft's opening until round 1's record
commits … and that is the window's expected state, not a failure to chase"*,
and a case in `test_the_rules_have_one_owner.py` pinned that sentence, on the
grounds that no carrier had said the window was expected. #296 removes the
window, so the sentence and its case were both asserting something false. The
case is rewritten to require the correction and to assert **both** halves — the
state prints on a draft, and nothing that can reach `main` is exempt — because
a case requiring only the first would go green over a document that had
quietly turned the draft into a permanent exemption.

**The second window's sentence was reworded by accident and put back.** The
same paragraph carries a second red window, from `close` ticking `Pass` until
the verifying round's record commits, with its own case pinning its wording.
That window is untouched by this branch, so its sentence had no business
changing; the original phrasing is restored rather than the case updated. A
case going red is not automatically a case to edit — the question is which of
the two the change was entitled to move.

**Corrected after round 1's ⬜ 5: it was put back one word short, so this was
an edit and not a restoration.** The original ended *"and that window is
expected too"* and it now ends *"and that window is expected."* The dropped
`too` pointed at the FIRST red window, which #296 closes, so with that window
gone the word refers to nothing and dropping it is right. What was wrong is
this paragraph calling the result a restoration. The sentence stands as
edited, deliberately, and
`test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits`
now asserts the clause through its final word. It reached only as far as
*record commits* before, which is why nothing caught the missing one.

**The fixture class from phase 2 was larger than the static enumeration
found, and the extra member is a different shape.** Phase 2 enumerated every
`specs/<id>` literal in `tests/` and fixed six modules' hand-built records.
`test_the_fixes_close_the_record.py` then failed anyway: it names no work-item
id at all, it imports the harness from `test_the_record_is_generated.py`, and
its record comes from `round_record.py new` rather than from a string in the
file. So the class is not *hand-built fixtures* — it is **any case that puts a
record for an item above the cutoff in front of a READY `chain_check`**, and a
generated record says `not yet` until the broad gate runs. Re-enumerated on
the id itself rather than on the path prefix: two distinct ids at or above
`GATE_FROM` across `tests/`, one of them this work item's own constant. The
one case in that module that runs the check ready now passes `--broad-gate`
to `close`, with the correction commit as the value, because the gate runs
after the fixes — a SHA the record's `Target SHA` descends from would fail as
the run spent before the round it sealed. That is the real sequence, so the
case now models it.

**A version-shaped number in an example is a timer.** The whole-range row's
docstring example was written as `origin/release/v0.9.5...HEAD`, and
`test_release_hygiene.py` refuses any loaded file naming a version at or above
the running one: such a line goes red on the day that version ships, on the
release's own preparation commit, after the broad gate has already run. The
example reads `origin/release/vX.Y.Z...HEAD`.

**Eleven ledger rows drifted and none of their claims did.** Every one is a
row whose anchor covers a region this branch edited for a different reason —
`chain_check.py#main`, the anchored constant block, `templates/sdd-round.md`'s
field table, `agents/smith.md#"## Phases"`, three `orchestration.md` regions,
and `survivor_check.py#read_exemptions`. Each claim was re-read against what
actually moved and each holds, so each row carries a re-read note saying which
edit moved its region and that the claim stands. The one worth naming is S5,
the exemption anchor: `read_exemptions` gained the range shape and a second
return value, and the contiguous-run matching S5 is about lives in `exempted`,
which was not edited and whose hash did not move. The whole-range row is a new
claim in this work item's own fragment rather than a change to that one.

**One rider stamp re-stamped, after reading the rider.** `agents/smith.md:60`
carries the design-gate rider about the waiver example, and its stamp anchors
on `## Phases` — the section this phase added a paragraph to. The rider asks
for a trade that is the repository owner's (`questions.md` Q2 of another work
item), not something this branch may settle, so the answer is a re-stamp and
not a repair.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `orchestration.md`'s claim that the `release` leg's first red window is *the window's expected state, not a failure to chase* | the same paragraph, rewritten to say the window is closed and why, and `test_the_rules_have_one_owner.py#test_the_release_leg_is_no_longer_red_until_round_ones_record_commits` — renamed from `..._is_red_...` — pins the correction and both of its halves |
| the case name `test_the_release_leg_is_red_until_round_ones_record_commits` — NAME NOT IN TREE, which is the point of the row | the renamed case above; its docstring keeps the ⬜ 8 history and records that #296 closed the window the finding asked somebody to document |
