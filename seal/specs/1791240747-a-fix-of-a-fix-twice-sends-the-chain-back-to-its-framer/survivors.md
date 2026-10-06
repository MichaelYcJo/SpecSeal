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
