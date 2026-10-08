# 1791384162-the-macos-test-leg-runs-in-shards — questions for the planner

<!-- seal/specs/1791384162-the-macos-test-leg-runs-in-shards/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

Framed by `framer` on Fable 5.1, 2026-10-08. No row blocks the build: none
is a person's. One is a measurement a CI run gives, and two are the work's.

## Judgments the issue left open that the tree answered

Listed so nobody reopens them. Each one's grounds are in `spec.md` or in
`plan.md`'s Alternatives table.

| Judgment | Answer | Where the grounds are |
|---|---|---|
| How many macOS shards | Three, the smallest count whose slowest shard the arithmetic puts under 12 minutes on the slowest measured pace; four is the fallback the measurement can choose | `plan.md` §*Technical context*, Alternatives A–C |
| What a sharded leg's target is | 12 minutes for its slowest shard, inherited from #841's Q1 (a), which the owner left at its default and 0.20.0 shipped on (S4) | `spec.md` Grounding |
| How the budget is set | 1.5 times the slowest measured job, rounded up to 5 minutes, beside its run id — #841's Q6 (a), inherited; 35 stands until the first sharded run | `spec.md` Grounding, Scope 2; `plan.md` Alternatives I |
| Whether macOS gets its own durations file | No. Collection is identical on the three legs, so the Windows file divides every leg the same way; only each case's price differs, and that is measured, not stored | `spec.md` Scope 1 and Out; `plan.md` Alternatives D |
| How the macOS balance is measured | From the sharded run's own jobs, `startedAt` to `completedAt`, and each job's summary line — never from the file or a laptop | `spec.md` S2; `plan.md` Alternatives J |
| What the shards' union is checked against | ubuntu's `passed` plus `skipped` at the same SHA, as 0.20.0's S4 did for Windows, because the three legs collect the same cases | `spec.md` Scope 1, S1 |
| Which tests change | The shard module, the timeout case, the two cheap-twice cases that sliced the job, and the new reader beside `jobs`; nothing else asserts the shape of a non-Windows entry | `plan.md` §*Technical context*, the readers paragraph |
| Where the one reading lives | Beside `jobs` in `tests/test_ci_gives_the_checks_what_they_need.py`, not in `conftest.py` | `plan.md` Alternatives G |
| What is renamed | The shard module's first case, for its name; not the module file | `spec.md` Scope 4 and Out; `plan.md` Alternatives H |
| Whether `.test_durations` is refreshed here | No. It is stale (504 collected cases unknown to it, 727 dead entries) and that is today's imbalance on both legs, but the refresh is a dedicated Windows run the owner starts by `CONTRIBUTING.md`'s recipe; the report names it as a leftover | `spec.md` Out |
| Whether macOS-heavy cases are cut | No; #841 left the shell oracle and the rest of the table to the owner, and the issue asks for shards | `spec.md` Out |
| Whether the READMEs or `docs/` change | No; neither names the CI legs (`grep`) | `spec.md` Out |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What do the three macOS shards measure on the first sharded run — each job's time `startedAt` to `completedAt`, its `passed` and `skipped`, and the sum of the three against ubuntu's at the same SHA? | a measurement — the run the session dispatches after phase 1's push; `gh run view <id> --json jobs`, and each job's log for its summary line | the slowest at or under 12 minutes: the budget is set from it and three stands; over: Q2; a sum that is not ubuntu's: a group is missing or doubled, which the shard case should have caught first | none; phase 2 answers it | ✅ measured 2026-10-08 in run 37700567455 at 3a946dd0: 5 m 22 s, 6 m 24 s and 6 m 56 s; 6,164 + 9, 3,630 + 75 and 2,945 + 4, which is 12,827, ubuntu's 12,747 + 80. Three stands and the budget is 15 (`phases/phase-2.md`) |
| Q2 | If three shards' slowest is over 12 minutes, does the count go to four, and what if four misses too? | the work — phase 2, from Q1's figure | four: a fourth entry, the shard table's count, the count sentence, one more run, the budget from it; four also over: this item ships four with its measured figure and says so, and a macOS-measured durations file is the next design as its own issue | three holds, by the arithmetic in `plan.md` (10.5 minutes at a 1.45 factor on the slowest pace) | ✅ answered by the work 2026-10-08 in phase 2: not reached. The slowest of three shards took 6 m 56 s, so the count stays three |
| Q3 | Has #835's registry of readers landed on `release/v0.21.0` when phase 1 builds, so the new reader's input class is a row there rather than a sentence in its docstring alone? | the work — phase 1, by reading the release branch at its start | landed: the row, in the shape the registry asks; not: the docstring names the class (*owned*) and what it refuses, and `phases/phase-1.md` names the seam for #835's build to add the row | the docstring | ✅ answered by the work 2026-10-08 in phase 1: not landed. `origin/release/v0.21.0` read 5623d728 at the phase's start, and #835 sits unmerged on `feat/835-a-reader-declares-its-input-class`. `matrix_include_entries`'s docstring (the reader's name since round 1's fix) names the class (*owned*) and what it refuses; `phases/phase-1.md` names the seam |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
