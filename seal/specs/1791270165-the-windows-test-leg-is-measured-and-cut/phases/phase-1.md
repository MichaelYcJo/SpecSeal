# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b9435eda (the workflow edit; the phase closes when the dispatch tables below are recorded) |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The `test.yml` edit of `plan.md` phase 1 and its local checks: a
`workflow_dispatch` trigger with a boolean `windows_defender_off` input
(default `true`), `--durations=50` on the `pytest` line with its
`- run: pytest tests/ -q -n auto` head kept, the phase 2 Defender step in the
same edit gated on the input, and the "198 s against 24 s" comment dated and
pointed here. No push and no dispatch: the session runs those, and this
record gains the three legs' top-50 tables from the dispatch run.

## What this phase found

**The Defender step is not in the tree.** Writing the step
(`Set-MpPreference -DisableRealtimeMonitoring $true`, `shell: pwsh`, gated
on `runner.os == 'Windows'`) was refused by the harness's permission
classifier as weakening a security control. The refusal covers the outcome,
so the step was not written by any other route. Its input had no other use,
so `workflow_dispatch` landed bare. Whether the step goes in is the
repository owner's decision (`questions.md` Q10); until it is, phase 2 has
nothing to measure and one dispatch measures phase 1.

**The plan's `if:` would never have run the step on a dispatch.** It read
`inputs.windows_defender_off == 'true'`. The `inputs` context keeps a
boolean input a boolean, and an Actions expression compares unlike types as
numbers, where `'true'` is NaN, so the comparison is false for both
answers. The step, if the owner allows it, reads the input bare. This is
`read` from the Actions expression documentation and not `executed`: no
dispatch has run.

**Six modules read `test.yml`, not four.** `tests/test_the_gate_names_every_step_ci_runs.py`
and `tests/test_deferral_check.py` name the file too, so the local check ran
all six:

    bin/test tests/test_arm_check.py tests/test_release_hygiene.py
      tests/test_the_suite_has_a_command_that_is_cheap_twice.py
      tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py
      tests/test_the_gate_names_every_step_ci_runs.py
      tests/test_deferral_check.py -q

`322 passed, 2 skipped in 8.96s`, exit 0 read directly (`executed`,
2026-10-06, at the tree of b9435eda).

**The tables.** Owed by the dispatch run named in `overview.md`. Each leg's
top-50 table goes here with the run id, the SHA and the date.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `test.yml` sentence "That is the whole of why the windows leg took 198s against ubuntu's 24s" as a present-tense claim | the same comment, now dated, pointing at this record |
