# 1791270165-the-windows-test-leg-is-measured-and-cut — overview

📋 implement applied
· spec:     this item's routing.md, spec.md, plan.md, questions.md; `CONTRIBUTING.md` and `docs/` read only as cited by them
· evidence: seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md — one `Re-read · D1` row (0.18.2)
· verified: executed — the six test.yml-reading modules, the guard module, two mutation reds, the Q4 probe, `evidence-check` lenient and strict; read — the Actions expression and dispatch rules below

## Why this work exists

Every pull request waits on the Windows test leg, which grew from 7 to 40
minutes in two weeks; this item measures it on Windows and cuts it.

## Where the build stands (2026-10-06, the second smith on Opus 5.5)

| Phase | State |
|---|---|
| 1 | Closed: the tables of run 37429940700 are in `phases/phase-1.md`, and Q2 is answered |
| 2 | Dropped by the owner's answer to `questions.md` Q10 (b) |
| 3 | Not started; it is next, and it needs the next CI run (below) |
| 4a | Closed (83801eac) |
| 4b | Being built by the second smith from the Windows table |
| 5 | Not started |

**What the next phase needs.** Routing is `automation` now, so the
orchestrator pushes the branch and opens the draft pull request. That pull
request's CI run is the measurement phase 3 starts from: the Windows leg
after 4b, which is "the last run before the shards" of S4.

**The dispatch worked where the first smith expected a refusal.** It wrote
here that `gh workflow run` might answer HTTP 422 because `main`'s copy of
`test.yml` has no `workflow_dispatch` trigger. The session's dispatch of
2026-10-06 was accepted and ran (run 37429940700), so that reading of
GitHub's documentation did not hold for this repository.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The Defender step in phase 1's edit | plan.md phase 1: "the Defender step of phase 2 lands in this same edit"; the code has no such step | not written | the harness refused the write as weakening a security control; `questions.md` Q10 |
| The dispatch input | spec.md Data & interfaces: "`on.workflow_dispatch` with one boolean input … (`windows_defender_off`, default `true`)"; the trigger is bare | bare trigger | the input gated only the refused step · NAME NOT IN TREE |
| The step's `if:` | plan.md: `inputs.windows_defender_off == 'true'` | the input read bare, if the step is ever written | a boolean input compared with a string is always false (`phases/phase-1.md`) |
| Phase 1's local check | plan.md names four modules | six | two more modules read `test.yml` |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ The `--durations=50` tables on all three legs, and that the dispatch runs at all | run 37429940700 at be8a4115 printed all three, read off its job logs on 2026-10-06 by the second smith; the tables are in `phases/phase-1.md` |
| ✅ `evidence-check --strict .` exit 0 (plan 4a): it exits 2 on `spec.md` line 14, whose Grounding row quotes D1's released anchor `@3e34189e`, which this build's rewrite drifts | the framer reworded `spec.md` line 14 at a321fbcb; the last two `NOT-IN-TREE` lines (`windows_defender_off` here and in `phases/phase-1.md`) were marked by the second smith, and the command exited 0, read directly, on 2026-10-06 · NAME NOT IN TREE |
| Which lookup the twins case spawns git through (194 spawns on the sample) | #826, which rewrites or retires the case; the Windows table does not name it (under 8.15 s), so phase 4b does not owe it |
| The whole suite | the sealer, once, after the rounds — none were routed |

## Not done

Phase 2, 3, 4b and 5 were not started: 2 waits on Q10, and the others on
CI figures, as the spawn ordered.

## Fed back into the spec

none
