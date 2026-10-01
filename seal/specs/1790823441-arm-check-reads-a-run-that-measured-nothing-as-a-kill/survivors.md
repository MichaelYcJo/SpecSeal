# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — survivors

Places `survivor-check` reports that still carry wording a range removed,
judged and kept.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` | stem = os.path.splitext(os.path.basename(module))[0] | #641's `SEES_CACHE`, the twin of the `arm-check` probe this branch changed. That change was owed because `arm-check`'s new first run cleared the one planted cache before any arm, so the clear before each arm had no witness. `mutation-check` gives each of its three removals a case of its own, and two of those probes write a `.pyc` themselves (`WRITES_CACHE`): removal before the baseline, `test_no_bytecode_for_the_mutated_file_exists_while_the_cases_run`; between the write and the mutated run, `test_bytecode_the_baseline_wrote_is_gone_before_the_mutated_run`; after the restore, `test_bytecode_the_cases_wrote_for_the_mutant_is_not_left_behind`. Executed 2026-10-01 at `a5d4749a` with `mutation-check` against that module: deleting each removal in turn read `red`, each on its own case |
