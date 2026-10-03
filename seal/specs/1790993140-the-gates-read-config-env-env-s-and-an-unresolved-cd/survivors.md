# Survivors — the gates read `--config-env`, `env -S`, and an unresolved `cd`

Round 1's fix pass (`survivor-check --range 25e5b01a..HEAD`) reported one
place. It is M1's original claim in `seal/releases/0.16.0.md`, from #689. The
ledger keeps a corrected claim's original words and puts the correction after
them in the same cell, so the standing text is the claim the correction is
about, not wording the range forgot. The range narrowed that correction
(round 1, white 7); the original stays by the ledger's own rule.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.16.0.md` | so the guard's decision, the kinds it recognises, the tree it judges, each segment's directories and the clone consent is filed under are `86256492`'s | M1's original claim, kept by the correct-in-place rule; the two `Corrected` notes after it in the same cell, 2026-09-30 and 2026-10-03, say what changed |
| `tests/test_guard_resolves_the_tree_it_judges.py` | Round 1 of 1790993140, yellow 3. | a case's citation of the round finding it pins; round 2's fix pass reworded the guard's docstring that cited the same finding, and this case still pins it |
| `tests/test_guard_resolves_the_tree_it_judges.py` | Round 1 of 1790993140, yellow 3: the subtraction is per view, so a restore both readings parse alike adds no question | the same citation, on the case pinning the per-view subtraction; it still holds, because the restore's own segment is where the frozen parser reads its kind |
