# 1791270165 — handoff

Written 2026-10-06 by the orchestrating session (Opus 5.5) when the 0.20.0 run moved to another machine. Read this first, then `overview.md` §*Where the build stands*.

## Where it stands

- Framed by `framer` on Fable 5.1 (93e764e1). Built by `smith` on Opus 5.5: b9435eda, 597cc5f7, ca6bf8a1, 83801eac, be8a4115.
- **Phase 4a is closed.** The twins case walks a covering sample of 870 of its 20,832 shapes and went from 165 s to 2.85 s locally. Its module reported 426 passed, and the smith saw each new helper fail under `bin/mutation-check`.
- **Phase 1 is open.** `test.yml` has a `workflow_dispatch` trigger and `--durations=50`. The branch was pushed and the workflow dispatched once from the old machine: run https://github.com/MichaelYcJo/SpecSeal/actions/runs/37429940700. GitHub accepted the dispatch, though `main`'s `test.yml` has no `workflow_dispatch`. Its three `--durations` tables close phase 1 and answer Q2. The second smith, on the new machine, recorded them in `phases/phase-1.md`, which closes the phase.
- Draft pull request #845 into `release/v0.20.0` is open: the owner's second answer on 2026-10-06 was `automation` (`routing.md`), and the orchestrator opened it after phase 4b. Its CI runs the three legs on every push, and the build has closed (`overview.md`).

## Two things a person decided

Both were open when this file was written and both were settled on the new machine the same day.

1. **Q10, the Defender step.** The harness's permission classifier refused the smith's `Set-MpPreference -DisableRealtimeMonitoring $true` step as a security weakening, and nothing produced it another way. The owner answered (b): the step is dropped, and with it phase 2 (`questions.md` Q10, 0ba13a2a).
2. **`evidence-check --strict .` exited 2** because `spec.md:14`'s Grounding table quoted D1's old coordinate (`…@3e34189e`), which this build's edit to the twins case drifts. The framer reworded it at a321fbcb.

## Next

1. Read run 37429940700's `pytest` job logs (`gh run view 37429940700 --log`) and record the three tables in `phases/phase-1.md`. That closes phase 1. Done by the second smith.
2. Phase 4b from the Windows table (built by the second smith; `phases/phase-4.md`). Then phase 3, shards with `pytest-split` and K from Q1's default (slowest shard ≤ 12 min). Then phase 5, the budget, with Q6's default.
3. #826 phase 3 rebases onto this item's twins sampling (W4 there), so land this first.
4. The owner answered the `Review` and `Destination` rows on 2026-10-06 by pressing `automation`: the `warden` rounds, the sealer, and a draft pull request into `release/v0.20.0`, with nothing stopping to ask. `routing.md` records both answers.
