# 1791270165-the-windows-test-leg-is-measured-and-cut — questions for the planner

<!-- seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

Framed by `framer` on Fable 5.1, 2026-10-06, and revised by the same on the
same day after Q10 was answered. Nothing below blocks a phase: phase 2 was
dropped with Q10 (b), and Q1 and Q6 carry defaults the build proceeds on.

## Judgments the ticket left open that the tree answered

Listed so nobody reopens them. Each one's grounds are in `spec.md` or in
`plan.md`'s Alternatives table.

| Judgment | Answer | Where the grounds are |
|---|---|---|
| Whether the Windows leg stays on pull requests | Yes. Three Windows-only defects arrived after round 12 of one branch; the issue refuses dropping it | `spec.md` Grounding, last row; `plan.md` Alternatives J |
| Whether the 165 s case can be deleted | No. It is the one case holding the restore-wherever-the-redirection-stands property and `seal/releases/0.18.2.md` D1 cites it. It is sampled here and rewritten or retired in #826 | the owner's second comment on #841; `plan.md` Alternatives C |
| Which measurement is shared with #826 and who owns it | This item owns per-case durations (CI `--durations` per leg, the local table); #826 owns the stop count over the 27,351 recorded pairs and reads this item's guard-module figures instead of re-timing them | `spec.md` Scope 1 |
| How the Windows leg is measured before a pull request exists | `workflow_dispatch` on `test.yml`, run by the session against the pushed branch; the baseline was taken that way. Routing became `automation` on 2026-10-06, so from the draft pull request on its own runs measure, and the trigger stays for a SHA no pull request covers | `plan.md` Alternatives B |
| Whether the Windows figure may be inferred from macOS | No. The twins case spawns no git per shape (`a_branch_and_a_file`), so the per-spawn ratio does not apply to it; platform honesty is a contribution rule | `plan.md` Alternatives A; `CONTRIBUTING.md` §*What a change to a gate must carry* |
| Whether the heredoc shell oracle is in scope | No. `conftest.shell_probe` finds no usable shell on `windows-latest`, so the module is skipped there; it is the macOS leg's cost | `spec.md` Scope, Out |
| Whether "a repository built once and copied" is still to build | It exists: `tests/conftest.py#_repo_template` (used by about 50 modules through `repo`) and the sealer module's `_template`. Remaining per-case `git init` is touched only where the Windows table names the module | `spec.md` Scope 4, third bullet |
| How the product is sampled | A deterministic covering sample whose coverage the module asserts, never a seeded random one | `plan.md` Alternatives D; `spec.md` S5 |
| How the suite is sharded | `pytest-split` with a committed durations file from the Windows leg; the by-module list is the fallback | `plan.md` Alternatives E, F |
| What the budget is made of | `timeout-minutes` per leg and a per-case ceiling in `conftest.py` that fails the case with a sentence naming it; not `pytest-timeout`, which kills and reports a timeout | `plan.md` Alternatives H, I |
| Where the measured figures live | In `phases/phase-N.md` and `overview.md`, dated with run ids; `CONTRIBUTING.md` keeps saying the figure is recorded in the work item that measured it | `spec.md` Grounding, third row |
| Fragments under the freeze | New rows in `seal/ledger/1791270165-….md`; D1 of 0.18.2 and any other moved anchor re-read with `evidence-check --reverify --into`; no released file changes | `spec.md` Grounding, fifth row |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What is the Windows `pytest` leg's target wall time after this item, at the 0.20.0 branch's size? The issue states the history (7–12 min two weeks ago, 34–40 min now) and asks for a budget "decided from the measurement", but names no number, and the number decides the shard count `K` in phase 3 and the leg's `timeout-minutes` in phase 5. The tree cannot answer it: it is a value somebody waits on | a person — the repository owner | (a) **back to the 7–12 min band**: `K` is whatever the phase 1–2 figures divide to under 12 min, likely 3–4 shards; (b) **under the ubuntu leg × 2** (about 14 min today): fewer shards, a looser budget; (c) **no leg target, only the per-case ceiling**: `K` chosen as the smallest that halves the leg, and the budget is the ceiling alone | (a): the slowest shard at or under 12 min; `K` from the measurement | ⬜ |
| Q2 | Which cases carry the Windows leg's time, by the leg's own `--durations=50` table on each of the three legs, at the branch's SHA? | a measurement — phase 1's dispatch run, `gh run view <id> --log` | The table decides which modules phase 4b touches; a module not in the Windows top 50 is left alone | none; phase 1 answers it | ✅ run 37429940700 at be8a4115: the Windows top 50 are led by the guard's three corpus cases (36, 25 and 23 s), then 8 fix-of-a-fix cases (125 s) and 18 sealer cases (202 s); together the 50 are about a tenth of the leg's worker time, so the leg's minutes are spread across the suite (`phases/phase-1.md`, the second smith, 2026-10-06) |
| Q3 | How much does `Set-MpPreference -DisableRealtimeMonitoring $true` shorten the Windows `pytest` job? | a measurement — two dispatches at one SHA, `windows_defender_off` (NAME NOT IN TREE: removed with the step) true and false | Shorter: the step stays, unconditional. Not shorter, or the cmdlet fails on the hosted image: the step goes, and the phase record says what it printed | none; phase 2 answers it | ✅ not measured: Q10 was answered (b), so the step that Q3 measures is never written |
| Q4 | Does `test_no_twin_is_asked_unless_an_operator_cuts_the_segment` spawn a process per shape despite `a_branch_and_a_file` patching `wg.is_ref`? `wider_only_kinds` may reach `hooks/worktree-guard.py#_refs` (`:1157`) or `#_fetched_as` (`:1176`), which run git | a measurement — a `test_tmp_*` probe wrapping `subprocess.run` with a counter for that one case, run once, deleted | Zero or near zero: the case is CPU-bound and sampling alone brings it to seconds on every leg. Thousands: the fixture also patches the lookups the sweep reaches, on the same terms `is_ref` is patched, and the phase record says which | sampling alone; the count decides whether the fixture grows | ✅ 194 spawns over the 870-shape sample, 0 over the first three verbs' 1,268 product shapes; sampling alone kept (`phases/phase-4.md`, smith, 2026-10-06) |
| Q5 | For each sealer and fix-of-a-fix case the Windows table confirms, which cut keeps the claim: a module-scoped shared gate run for cases that only read a verdict, a cheaper `Broad gate` row for cases whose claim is not about pytest's output, or none? the `collected_nothing` D1 of `seal/releases/0.18.2.md` and the cases it anchors are claims about pytest's real output under xdist and keep the real runner | the work — phase 4b, case by case, each named in `phases/phase-4.md` | A cut that drops a claim is refused; a case left alone is listed with its figure | each case keeps the real runner until its claim is read | ✅ by the work in 4b: the six sealer cases that only read one sealed run share it, and five plus 35 fix-of-a-fix cases copy the prefix they repeated; no case got a cheaper `Broad gate` row, so every sealer case keeps the real runner, and the twelve other sealer cases in the Windows table are left alone, listed with their figures (`phases/phase-4.md`, the second smith, 2026-10-06) |
| Q6 | What are the per-case ceiling `CASE_CEILING_S` (NAME NOT IN TREE: phase 5 plants it) and the three `timeout-minutes` values? They are values a contributor is limited by, so a person is accountable for them; the issue says to decide them from the measurement | a person — the repository owner, who may overturn the rule below | (a) **a rule**: ceiling = 1.5 × the slowest remaining case on the Windows leg after phases 3 and 4, rounded up to 30 s; `timeout-minutes` = 1.5 × each leg's measured wall time after phases 3 and 4, rounded up to 5 min; (b) **fixed numbers** the owner names; (c) **no per-case ceiling**, only the leg timeouts (Alternatives I says why a case should name itself) | (a), applied by phase 5 with the run id written beside each constant | ⬜ |
| Q7 | Does the `windows_defender_off` dispatch input (NAME NOT IN TREE: removed with the step) outlive phase 2? | the work — phase 2 | Kept: a lever for the next measurement, one more input in `on:`. Removed: the trigger stays bare and the step's fate is in the file | removed; the trigger stays | ✅ removed with the step (Q10 (b)); the trigger stays bare |
| Q8 | What does the Windows leg measure after all five phases, at the branch's last SHA? The changelog entry states a before and an after with dates | a measurement — phase 5's confirming dispatch | The after figure goes in `changelog.md`, `overview.md` and `phases/phase-5.md`; a figure over Q1's target is reported, not hidden, with what is left to cut | none; phase 5 answers it | ✅ run 37465328899 at 98b817ad, the last measured: slowest Windows shard 10 m 03 s, against 33-36 minutes on this branch before the shards; macOS 17 m 38 s is now the longest leg. The confirming run of phase 5's push is the orchestrator's (`phases/phase-5.md`, the second smith, 2026-10-06) |
| Q9 | Does adding `pytest-split` to the pip line and the shard matrix to `test.yml` trip `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`'s pins or `tests/test_arm_check.py`'s S6 reader, and what is the smallest extension of those cases that holds the new line to `run_tests.py`? | the work — phase 3, by the narrow run of the two modules | Trips: the pin case is extended for a fourth constant the way the third was. Holds: nothing to do. If `pytest-split` has no wheel on one leg, Alternatives E is taken and the phase record says so | the pin case is extended | ✅ it trips nothing: `${{ matrix.split }}` holds no selection option, so S6's reader still counts the job; `test_ci_installs_the_parser_the_runner_pins` was extended for `PYTEST_SPLIT`, kept out of `PACKAGES`, and `pytest-split` 0.11.0 is a pure-Python wheel (`phases/phase-3.md`, the second smith, 2026-10-06) |
| Q10 | Does the Windows leg get a step turning Defender real-time scanning off (`Set-MpPreference -DisableRealtimeMonitoring $true`)? Phase 1 tried to write it gated on a dispatch input, and the harness's permission classifier refused the write as weakening a security control (`phases/phase-1.md`). Q3 and phase 2 measure nothing until the step exists | a person — the repository owner | (a) **allow it**: the owner writes the step, or grants the permission, and phase 2 runs its two dispatches; read the input bare in `if:`, since `== 'true'` against a boolean input is always false; (b) **refuse it**: phase 2 is dropped, Q3 closes as not measured, and the cut rests on phases 3 and 4 | none; phase 2 waits | ✅ (b), refused: phase 2 is dropped, Q3 closes as not measured, and the cut rests on phases 3 and 4 — the repository owner, asked by the next session on another machine, 2026-10-06 |

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
