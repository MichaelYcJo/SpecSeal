# Survivors — a cd row's failing path is measured under its own directory

Round 1's fix pass rewrote `compare_at_base`'s second docstring paragraph,
which said every present file reads `new?`, never `new`, where no prefix
prints pytest's summary. A file run alone now reads `new` from a run that
collected nothing. The place below states the same rule for the work item
that wrote it, and stays as that work item recorded it.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/spec.md` | **Where no prefix prints a pytest summary, every present file reads | #747's frame, the scope that work item was asked to build and shipped in 0.18.1; it records what was asked then, and another work item's frame is not this pass's to edit. `templates/config.md` rule 3, the rule's one home, carries the sentence as it now holds |
| `seal/releases/0.18.1.md` | `verdicts_at_base` reads that run: `failing on base too` where a `FAILED` or `ERROR` line names the file | B3 as it shipped in 0.18.1, which is frozen; this item's fragment supersedes it with `Corrected · B3`, which round 2's fix pass rewrote to read pytest's own lines only. The same row's coordinate list (`verdicts_at_base@8fed3ba4`, `MEASURED_ENDINGS@588d1907`) is the released reading the correction re-stamps, not a sentence to correct |
