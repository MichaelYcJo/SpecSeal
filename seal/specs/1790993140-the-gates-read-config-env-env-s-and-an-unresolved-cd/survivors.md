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
