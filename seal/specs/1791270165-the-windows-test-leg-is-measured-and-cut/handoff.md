# 1791270165 — handoff

Written 2026-10-06 by the orchestrating session (Opus 5.5) when the 0.20.0 run moved to another machine. Read this first, then `overview.md` §*Handoff*.

## Where it stands

- Framed by `framer` on Fable 5.1 (93e764e1). Built by `smith` on Opus 5.5: b9435eda, 597cc5f7, ca6bf8a1, 83801eac, be8a4115.
- **Phase 4a is closed.** The twins case walks a covering sample of 870 of its 20,832 shapes and went from 165 s to 2.85 s locally. Its module reported 426 passed, and the smith saw each new helper fail under `bin/mutation-check`.
- **Phase 1 is open.** `test.yml` has a `workflow_dispatch` trigger and `--durations=50`. The branch was pushed and the workflow dispatched once from the old machine: run https://github.com/MichaelYcJo/SpecSeal/actions/runs/37429940700. GitHub accepted the dispatch, though `main`'s `test.yml` has no `workflow_dispatch`. Its three `--durations` tables close phase 1 and answer Q2.
- No pull request is open (routing: stop before the pull request).

## Two things a person decides

1. **Q10, the Defender step.** The harness's permission classifier refused the smith's `Set-MpPreference -DisableRealtimeMonitoring $true` step as a security weakening. Nothing produced it another way. The dispatch input that toggled it was removed with it. Phase 2 waits on the owner: write it themselves, or drop the Defender lever and go straight to shards. An agent must not write it around the refusal.
2. **`evidence-check --strict .` exits 2** because `spec.md:14`'s Grounding table quotes D1's old coordinate (`…@3e34189e`), which this build's edit to the twins case drifts. That sentence is the framer's. Reword it to the "at hash `…`" form, as #831's smith did, or have a framer do it.

## Next

1. Read run 37429940700's `pytest` job logs (`gh run view 37429940700 --log`) and record the three tables in `phases/phase-1.md`. That closes phase 1.
2. Phase 4b from the Windows table. Then phase 3, shards with `pytest-split` and K from Q1's default (slowest shard ≤ 12 min). Then phase 5, the budget, with Q6's default.
3. #826 phase 3 rebases onto this item's twins sampling (W4 there), so land this first.
4. Take the owner's answer for the `Review` and `Destination` rows. `routing.md` records "for now, framer + smith".
