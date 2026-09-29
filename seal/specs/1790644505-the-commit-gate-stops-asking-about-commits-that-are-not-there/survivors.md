# Survivors — the commit gate stops asking about commits that are not there

Phase 5's sweep (`survivor-check --range 768377bf..130f8010`) reported one
place. It is a record of phase 1's own measurement, dated by the phase it
names, and it already carries the correction that says what changed after it.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/overview.md` | Executed: `commit_invocations` returns no invocation for `do git commit`, `then git commit` | phase 1's divergence row, recording what it executed at `release/v0.16.0`; the row's `Corrected 2026-09-29 by phase 4` note follows it and says the hole became #669 and is fixed. The removed sentence it shares a phrase with was the phase-4 *Not done* bullet about wrappers, which phase 5 closed; the two are about different shapes |
