# 1791270165-the-windows-test-leg-is-measured-and-cut — overview

📋 implement applied
· spec:     this item's routing.md, spec.md, plan.md, questions.md; `CONTRIBUTING.md` and `docs/` read only as cited by them
· evidence: seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md — 13 `Re-read ·` rows and one row per scenario (S1, S2, S4 to S9)
· verified: executed — five CI runs read (37429940700, 37457228586, 37458654434, 37465328899, 37469595104), the modules each phase touched, every new or rewritten case seen red, the Q4 and ceiling probes, `evidence-check --strict`; read — the Actions expression and dispatch rules, hosted runners' cores and one VM per job; unverified — the whole suite (the sealer)

## Why this work exists

Every pull request waits on the Windows test leg, which grew from 7 to 40
minutes in two weeks; this item measures it on Windows and cuts it.

## Where the build stands (2026-10-06, the second smith on Opus 5.5)

| Phase | State |
|---|---|
| 1 | Closed: the tables of run 37429940700 are in `phases/phase-1.md`, and Q2 is answered |
| 2 | Dropped by the owner's answer to `questions.md` Q10 (b) |
| 3 | Closed: four Windows shards; run 37465328899 ran the whole suite across them, slowest shard 10 m 03 s (`phases/phase-3.md`) |
| 4a | Closed (83801eac) |
| 4b | Built by the second smith from the Windows table: three shared prefixes in two modules, 46 cases; `phases/phase-4.md` says what each keeps and what was left alone |
| 5 | Closed: the 90 s case ceiling and the leg timeouts (ubuntu 15, macOS 35, each Windows shard 20), confirmed by run 37469595104, with macOS's timeout re-based on it (`phases/phase-5.md`) |

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
| What 4b can buy | plan.md Summary puts 4b before the shards because "`K` is divided from the leg that is left"; the issue reads "a minority of cases carry most of the growth" | 4b built, and its yield stated as bounded | the Windows table's top 50 are 9 to 12% of the leg's worker time, so 4b can take at most about 2.7 of its 30 minutes (`phases/phase-1.md`) |
| The two guard cases | plan.md 4b: "the two guard cases at 31 s and 38 s locally" are cut targets | left alone | each walks a list of distinct measured rows, and asks each twice by design, so no cut keeps the claim except dropping rows; the guard's premise is #826's (`phases/phase-4.md`) |
| The location cases | plan.md 4b cuts what the Windows table confirms per case | 35 cases cut, one of them in the table | the module is in the table with 8 cases, and the 35 share one prefix with the case the table names at 8.97 s; the others sit below the table's 8.15 s floor, so their Windows figure is inferred, not read |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ The `--durations=50` tables on all three legs, and that the dispatch runs at all | run 37429940700 at be8a4115 printed all three, read off its job logs on 2026-10-06 by the second smith; the tables are in `phases/phase-1.md` |
| ✅ `evidence-check --strict .` exit 0 (plan 4a): it exits 2 on `spec.md` line 14, whose Grounding row quotes D1's released anchor `@3e34189e`, which this build's rewrite drifts | the framer reworded `spec.md` line 14 at a321fbcb; the last two `NOT-IN-TREE` lines (`windows_defender_off` here and in `phases/phase-1.md`) were marked by the second smith, and the command exited 0, read directly, on 2026-10-06 · NAME NOT IN TREE |
| Which lookup the twins case spawns git through (194 spawns on the sample) | #826, which rewrites or retires the case; the Windows table does not name it (under 8.15 s), so phase 4b does not owe it |
| The whole suite | the sealer, once, after the rounds — none were routed |
| ✅ That the Windows leg writes `.test_durations` under xdist on the hosted runner and the artifact uploads (`include-hidden-files`, since the name starts with a dot): seen locally only, on macOS, in a scratch suite of six cases under `-n 2` | run 37458654434 uploaded `test-durations-windows-latest`; the second smith downloaded it with `gh run download` on 2026-10-06, 13,042 entries |
| What 4b's cuts buy on the Windows leg: every figure in `phases/phase-4.md` for after the cuts is from the second smith's loaded macOS machine | phase 5, if it takes several runs: phase 3 read the first run after 4b and found the runner's swing between runs of one day larger than anything 4b could move (`phases/phase-3.md`), so one run cannot answer it |
| Where one sealer gate run's 10-15 s on Windows goes, and so whether a cheaper `Broad gate` row (`plan.md` Alternatives K) is worth reading the remaining sealer cases for | the repository owner, who decides whether that measurement is wanted once phase 3 shows what the sealer module still costs a shard |

## Not done

Phase 2 was dropped by Q10 (b). macOS, now the longest leg at about 18
minutes, was not cut: the title names Windows, and its budget is its own
figure (`phases/phase-5.md`).

Phase 4b left alone the cases `phases/phase-4.md` lists under *Left alone*,
each with its grounds. The largest of them are the twelve sealer cases that
prepare a state of their own before the gate runs; whether any of them can
take a cheaper `Broad gate` row is Q5's question, case by case, and was not
read.

## Fed back into the spec

none
