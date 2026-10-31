# Closing memo: 1793457435-replay-targets-reads-both-layouts

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and format check at the work item's head: phases 1 and 2, and the build of the folded scope item 4 (31da1258, db1d502b), each ran its phase-boundary set and checked its changed files alone (contract rule 2) | the orchestrator, by `seal gate` after the review rounds settle |
| Scenario 5's regeneration of the four seeded cases after 31da1258. It was not run again. The commit moved `seed_defects.py#main`'s write loop under `elif held` and left its calls and their arguments as they were (read) | the proofer of the next round, or the sealer when it samples the crafters' claims |
| Scenario 5's regeneration of the eight committed cases after round 3's fix pass. It was not run. The fix changes which `--case` names `main` reads and the exit of a `--case` run, and each of the eight names is in its generator's `CASE_NAME` form (executed: `fullmatch` over the names under `evals/behaviour/proofer/`), so each is read and matched as before (read) | the sealer, when it samples the crafters' claims |
| Scenario 4's clone run over v0.27.0 and v0.26.0 after round 1's fix pass. It was not run again. The fix pass changes `blocked` only for a record in which the parser accepts no `seal` block, and round 1 found that each of the 10 records holding a `seal` opener at any release tag parses (read, not executed) | the sealer, when it samples the crafters' claims |

## Not done

`seed_defects.py --case` still prints its empty-read line where no named commit holds a round 1 record. `replay_targets.py --case` prints only the names in that run. Dropping the line under `--case` was within reach and not taken. Scope item 4 of `frame/design.md` gives `seed_defects.py` that line wherever no commit it read holds a round 1 record. The two generators also read a name in different units. `replay_targets.py` reads records, so a named work item with no record is a name nothing answers. `seed_defects.py` reads commits, so a named commit with no round 1 record is listed as `left out: holds no round 1 record`, and the empty-read line is what says that the read found nothing. So a run that names its cases now answers each name alike in both generators, and only `seed_defects.py` adds the empty-read line after the names.
