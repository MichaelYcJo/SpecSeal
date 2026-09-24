# Survivors — a second fold writes a second heading

`bin/survivor-check --range 0c72d956..bc186868`, run in the round-1 fix
pass after ⬜ 3's rewording of `docs/review-chain-spec.md`'s sealer
sentence, reported three places carrying its removed wording. One was a
tenth carrier of the replaced rule — `chain_check.py#broad_gate`'s docstring
— and is corrected in the same pass. The two below are records of the
release that shipped the rule as it then stood, and are not rewritten.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | so a re-seal records a second run instead of erasing the first; a first seal is byte-identical to before, and the reader still takes the first SHA as the run | The released 0.15.0 entry, in a shipped section, describing the cell's rule as that release wrote it — one entry per run, a re-seal keeping the first. The same-commit-same-base replace is 0.15.0's own round-2 narrowing and 0.15.1's wording of it; a released entry is a record of its release and is not rewritten by a later one, as `1790173209`'s `survivors.md` already holds for the entry above it |
| `seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/changelog.md` | so a re-seal records a second run instead of erasing the first; a first seal is byte-identical to before, and the reader still takes the first SHA as the run | The fragment that entry was gathered from, byte for byte the same sentence; it is already in `CHANGELOG.md` under its marker, and `settle` retires it with its work item. Rewriting the fragment after the gather would leave the two copies of one entry disagreeing |
