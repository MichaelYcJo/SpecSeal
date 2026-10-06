# Survivors — a fix of a fix twice sends the chain back to its framer

`survivor-check --range e66d04c0..HEAD`, run after round 1's fix pass,
reported three places still carrying wording the pass removed. One live place
was corrected: `docs/round-record-spec.md`'s sentence on which walks read the
same run now names the depth walk. The two below stand, for the reason in
each row.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | over every committed record whose previous `Fix range` this clone resolves | the phase-4 measurement as it was taken, kept as the record of what this clone carried; the same cell carries round 1's `Corrected 2026-10-06` note with the reviewer's resolved numbers right after it |
| `seal/releases/0.14.0.md` | of the work item holds the measurements and the residual profile | a released ledger row of another work item, which shares the phrase and not the fact; released rows are never edited |
| `docs/round-record-spec.md` | a prose file, a module-level line, a `Location` nothing places | round 2's fix pass (`survivor-check --range 01b1f966..HEAD`): the list of what lands nowhere is still true; the docstring it was matched against reworded the same list around `names_a_file`, and the spec's next sentence carries the tracked-file rule |
| `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | a 🟢, ❓ or ⬜ row, a prose file, a module-level line | round 2's fix pass: the same still-true list, in ledger row A1, whose next clause states the tracked-file and carrier rules |
| `skills/code-review/orchestration.md` | a landing it cannot place counts as none — a prose file, a module-level line | round 2's fix pass: the owner's disclosure of what the reading cannot see, still true; the detail is the spec's |
