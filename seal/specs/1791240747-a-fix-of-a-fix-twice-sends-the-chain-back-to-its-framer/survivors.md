# Survivors — a fix of a fix twice sends the chain back to its framer

`survivor-check --range e66d04c0..HEAD`, run after round 1's fix pass,
reported three places still carrying wording the pass removed. One live place
was corrected: `docs/round-record-spec.md`'s sentence on which walks read the
same run now names the depth walk. The rows below stand, for the reason in
each row.

Round 2's fix pass added three rows quoting the list of what lands nowhere in
`docs/round-record-spec.md`, ledger row A1 and the owner's disclosure. The
redesign after round 3 (phase 6) re-read them: all three sentences were
rewritten around the path-only reading, none of the quoted text stands, and
the rows are gone. The redesign's own range (`9c32e7f6..HEAD`) adds the last
row.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | over every committed record whose previous `Fix range` this clone resolves | the phase-4 measurement as it was taken, kept as the record of what this clone carried; the same cell carries round 1's `Corrected 2026-10-06` note with the reviewer's resolved numbers right after it |
| `seal/releases/0.14.0.md` | of the work item holds the measurements and the residual profile | a released ledger row of another work item, which shares the phrase and not the fact; released rows are never edited |
| `tests/test_a_fix_of_a_fix_is_counted.py` | "import os\n" | the redesign: the module's `MOD` fixture, which shares three code fragments (`n return 1 n`) with the removed bare-name case's `other.py` fixture and no fact |
