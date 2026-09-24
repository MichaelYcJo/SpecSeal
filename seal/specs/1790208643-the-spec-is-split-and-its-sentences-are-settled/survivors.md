# Survivors — the spec is split and its sentences are settled

`bin/survivor-check --range origin/release/v0.15.1...HEAD`, run at phase 6
(`4b25160c`), reported two places carrying the exception sentence #488 widened.
`skills/evidence-check/SKILL.md` §*`correction-check`* was a fourth carrier of
the rule, and it is corrected in the same phase. Correcting it put one more
place in the report at `8a5591b0`, `correction_check.py`'s module docstring,
which is the row below. The other was `CLAUDE.md`, whose quote the
orchestrator's paste at `233d1a13` removed, so its exemption row was removed
in round 1's fix pass rather than left excusing nothing.

Round 1's fix pass (⬜ 6) reworded the record document's *this document's
`blocks more` default*, which dangled after the split. The sweep then named
two places that say *this file's `blocks more` direction* about
`chain_check.py`. There *this file* is the checker the sentence sits in, and
every other refusal in it does block more, so the two rows below exempt them.

| Path | Quote | Grounds |
|---|---|---|
| `skills/evidence-check/scripts/correction_check.py` | because a branch that falsifies what a row claims must repair it in the shared file | The docstring narrates #424, the incident the checker was built for, and in that incident the row stood in the shared file and the repair was a correction of a falsified claim. The sentence says what that branch was required to do then, which stays true; the rule as it stands now, *removes or edits*, in *the file the row is in*, is the evidence-ledger policy's, and the docstring does not restate it |
| `skills/code-review/scripts/chain_check.py` | exception to this file's `blocks more` direction.** Every other refusal here treats what it cannot read as the failing case | *This file* is `chain_check.py` itself, in `says_not_yet`'s docstring, and the claim is about that file's refusals, every other one of which treats an unreadable value as failing. The sentence #526's fix pass reworded dangled because the record document holds no such default; this one names the file it stands in, and it is true there |
| `tests/test_a_record_precedes_the_fixes_it_commissions.py` | The deliberate exception to this file's `blocks more` direction. | The case's docstring names the direction of the checker it tests, the same fact as the row above in the file that pins it; *this file* is read with the checker's name the module docstring gives, and the sentence is true of it |
| `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/spec.md` | the anchor's hash belongs to exactly one side — the side that edited the anchored unit; | the frame's #509 row, a record of the rule as it was asked for; round 1 found it false where both sides edited the unit, the carriers state the corrected rule, and the row carries a dated `Corrected 2026-09-24 (round 2's ⬜ 3)` note beside the sentence. Excused by the orchestrator at the close of round 2 |
