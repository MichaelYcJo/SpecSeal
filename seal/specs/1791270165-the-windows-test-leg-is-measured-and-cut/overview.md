# 1791270165-the-windows-test-leg-is-measured-and-cut — overview

📋 implement applied
· spec:     this item's routing.md, spec.md, plan.md, questions.md; `CONTRIBUTING.md` and `docs/` read only as cited by them
· evidence: seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md — one `Re-read · D1` row (0.18.2)
· verified: executed — the six test.yml-reading modules, the guard module, two mutation reds, the Q4 probe, `evidence-check` lenient and strict; read — the Actions expression and dispatch rules below

## Why this work exists

Every pull request waits on the Windows test leg, which grew from 7 to 40
minutes in two weeks; this item measures it on Windows and cuts it.

## Handoff — where the build stopped (2026-10-06, smith on Opus 5.5)

| Phase | State |
|---|---|
| 1 | Workflow edit committed (b9435eda); local checks pass. **Open**: the dispatch run and its three tables in `phases/phase-1.md` |
| 2 | **Blocked on the owner** (`questions.md` Q10): the Defender step was refused by the harness, so there is nothing to measure |
| 3 | Not started; waits on phase 1's figures |
| 4a | Closed (83801eac) |
| 4b | Not started; waits on phase 1's Windows table |
| 5 | Not started; waits on phases 2–4 |

**Next step:** the session pushes and dispatches once (below), reads the
three `--durations=50` tables off the run's log, and a smith writes them into
`phases/phase-1.md` with the run id, SHA and date, which closes phase 1 and
answers Q2. Then phase 4b reads the Windows table; phase 3 needs it as well.

**CI commands owed (the session's, not the smith's):**

    git -C /Users/michael/Documents/GitHub/SpecSeal-worktrees/841-windows-ci-time push -u origin perf/841-the-windows-test-leg-tripled-in-two-weeks
    gh workflow run test.yml --ref perf/841-the-windows-test-leg-tripled-in-two-weeks
    gh run list --workflow test.yml --branch perf/841-the-windows-test-leg-tripled-in-two-weeks --limit 1
    gh run view <id> --log

There is no `-f windows_defender_off=…`: the input is gone with the step.
One dispatch, not the plan's two, until Q10 is answered.

**If `gh workflow run` answers HTTP 422** ("does not have 'workflow_dispatch'
trigger"), the cause is that `main`'s copy of `test.yml` has no such trigger
and GitHub reads the default branch's file to decide whether a workflow can
be dispatched at all. This is from GitHub's documentation and was not run.
The way past is not this smith's to choose: a `push` trigger naming this
branch, or a draft pull request, which the routing refuses. Each is a change
to what `test.yml` runs on, so it goes to the owner.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The Defender step in phase 1's edit | plan.md phase 1: "the Defender step of phase 2 lands in this same edit"; the code has no such step | not written | the harness refused the write as weakening a security control; `questions.md` Q10 |
| The dispatch input | spec.md Data & interfaces: "`on.workflow_dispatch` with one boolean input … (`windows_defender_off`, default `true`)"; the trigger is bare | bare trigger | the input gated only the refused step |
| The step's `if:` | plan.md: `inputs.windows_defender_off == 'true'` | the input read bare, if the step is ever written | a boolean input compared with a string is always false (`phases/phase-1.md`) |
| Phase 1's local check | plan.md names four modules | six | two more modules read `test.yml` |

## Not verified

| Item | Who must answer |
|---|---|
| The `--durations=50` tables on all three legs, and that the dispatch runs at all | the orchestrating session — the owed dispatch above |
| `evidence-check --strict .` exit 0 (plan 4a): it exits 2 on `spec.md` line 14, whose Grounding row quotes D1's released anchor `@3e34189e`, which this build's rewrite drifts | the framer, or the owner — `spec.md` is not the smith's to edit |
| Which lookup the twins case spawns git through (194 spawns on the sample) | phase 4b, if the Windows table still names the case |
| The whole suite | the sealer, once, after the rounds — none were routed |

## Not done

Phase 2, 3, 4b and 5 were not started: 2 waits on Q10, and the others on
CI figures, as the spawn ordered.

## Fed back into the spec

none
