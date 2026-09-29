# Survivors — the commit gate stops asking about commits that are not there

Phase 5's sweep (`survivor-check --range 768377bf..130f8010`) reported one
place. It is a record of phase 1's own measurement, dated by the phase it
names, and it already carries the correction that says what changed after it.

| Path | Quote | Grounds |
|---|---|---|
| `docs/commit-review-gate-spec.md` | Every segment the new reading reaches began with a word at which the old one found no command, so no commit the base read is read differently | round 1's fix pass (`survivor-check --range 3006eb85..b93cb50`). Still true of segments, which round 1 confirmed by reading `command_word` against the base's loop; the sentences after it in the same paragraph now say what it could not see, the unparsed fallback, and the corrected #670 argument it shares two phrases with is about the same gap |
| `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/overview.md` | Executed: `commit_invocations` returns no invocation for `do git commit`, `then git commit` | phase 1's divergence row, recording what it executed at `release/v0.16.0`; the row's `Corrected 2026-09-29 by phase 4` note follows it and says the hole became #669 and is fixed. The removed sentence it shares a phrase with was the phase-4 *Not done* bullet about wrappers, which phase 5 closed; the two are about different shapes |
