# Survivors — MALFORMED is graded like DRIFTED, and rule (a) reads prose as prose

`survivor-check --range origin/release/v0.15.5...HEAD`, run at `353224c2`
after the build's three phases, reported one place. It shares its wording
with the docstring of the renamed malformed case, which said `MALFORMED`
exits 2 "as OLD-FORMAT does". The standing sentence is about `OLD-FORMAT`,
which this work item leaves at exit 2 under both readings.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` | OLD-FORMAT exits 2 with or without the flag, so both readers already agree and the remedy the run names is the migrator. | `test_an_old_format_row_is_silent`'s docstring; `OLD-FORMAT`'s grading did not move (`spec.md` §*Out*), so the sentence is true and the case beneath it still passes |
