# Survivors — the spec is split and its sentences are settled

`bin/survivor-check --range origin/release/v0.15.1...HEAD`, run at phase 6
(`4b25160c`), reported two places carrying the exception sentence #488 widened.
`skills/evidence-check/SKILL.md` §*`correction-check`* was a fourth carrier of
the rule, and it is corrected in the same phase. Correcting it put one more
place in the report at `8a5591b0`, `correction_check.py`'s module docstring,
which is the row below. The other was `CLAUDE.md`, whose quote the
orchestrator's paste at `233d1a13` removed, so its exemption row was removed
in round 1's fix pass rather than left excusing nothing.

| Path | Quote | Grounds |
|---|---|---|
| `skills/evidence-check/scripts/correction_check.py` | because a branch that falsifies what a row claims must repair it in the shared file | The docstring narrates #424, the incident the checker was built for, and in that incident the row stood in the shared file and the repair was a correction of a falsified claim. The sentence says what that branch was required to do then, which stays true; the rule as it stands now, *removes or edits*, in *the file the row is in*, is the evidence-ledger policy's, and the docstring does not restate it |
