# Implementation Plan: the Windows test leg is measured and cut (#841)

<!-- seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `per axis` answer (smith named), when `smith` was spawned.

## Summary

Four phases remain of the five the issue gave, and the order from here is
**1 (closing), 4b, 3, 5**: the baseline run's tables into
`phases/phase-1.md`, then the other cases the Windows table names, then the
shards sized from the leg the cuts leave, then the budget. Phase 2, the
Defender step, was dropped on 2026-10-06 by the owner's answer to
`questions.md` Q10 (b); phase 4a closed at 83801eac. The shards come after
the cuts because `K` is divided from the leg that is left, not the leg that
was measured.

The measurement is the Windows leg's own `--durations` table, taken through
a `workflow_dispatch` trigger before any pull request existed (run
37429940700, named in `handoff.md`). Routing became `automation` the same
day, so a draft pull request opens at the end of the build and its CI runs
the three legs on every push; the confirming figures of phases 3 and 5 are
those runs', and the trigger stays for a SHA no pull request covers. Phases
1, 3 and 5 are verified by a CI run; phase 4 is verified locally by the
narrow run of each module it touches.

**The smith cannot push or dispatch** (`agents/smith.md`, agent-contract §6),
so each CI-verified phase ends with a commit and a hand-back line saying
which run the session has to start: `git push` of the branch, then
`gh workflow run test.yml --ref perf/841-the-windows-test-leg-tripled-in-two-weeks`
while no pull request is open, and the push alone once the draft pull
request is, since its own run is then the measurement. The smith reads the
result with `gh run view <id> --log` and `gh run download`, both reads.

**The 45-minute bound.** Phase 1 was one edit of `test.yml` (the trigger
and the flag) and one commit, and the sampler of phase 4a one module's edit
with its narrow run; both fit the bound. The Windows run itself takes 35–40
minutes today and is not the smith's clock.

This frame was drawn by `framer` running on Fable 5.1, and revised by
`framer` on Fable 5.1 on 2026-10-06, after phases 1 and 4a were built, to
fold in the owner's Q10 (b) answer and the routing change to `automation`.
The `Framed` mark at the foot of `spec.md` is unchanged: a `Reframed … after
round <N>.` line names a stop in a review run, and none has begun.

## Technical context

**The leg, measured from the Actions API on 2026-10-06 (`executed`, this
frame).** `pytest` job wall times on `main`, `startedAt` to `completedAt`:

| Run | Date | windows | ubuntu | macOS |
|---|---|---|---|---|
| 35806776524 | 2026-09-23 | 7 m 39 s | 2 m 06 s | 4 m 06 s |
| 36387281144 | 2026-09-28 | 16 m 11 s | 3 m 19 s | 6 m 39 s |
| 37082809479 | 2026-10-03 | 22 m 42 s | 4 m 51 s | 9 m 06 s |
| 37200416121 | 2026-10-04 | 29 m 58 s | 6 m 10 s | 5 m 08 s |
| 37420951690 | 2026-10-06 (0.19.0 release PR) | 39 m 34 s | 6 m 51 s | 18 m 02 s |
| 37413792861 | 2026-10-06 (#828) | 37 m 30 s | 8 m 51 s | 17 m 56 s |

Windows grew 5.2× while ubuntu grew 3.3× and the test count grew 1.35×. The
Windows leg has no `--durations` output today, so which cases carry the
difference is not known; the local macOS table in the issue's first comment
is the only per-case figure, and it is a different machine.

**Where the cost is known to sit.**

- `tests/test_guard_resolves_the_tree_it_judges.py` (2,633 lines).
  `_placed(verb)` yields `git <verb>` with every one of the 38 redirection
  operators `_redirections()` derives from `hooks/cmdline.py#_REDIRECTION`,
  at every word position, glued and spaced, target glued and spaced — on the
  order of 500 shapes per verb. `test_no_twin_is_asked_unless_an_operator_cuts_the_segment`
  walks it for every verb of `TWINS` and `DASHED_TWINS` (about sixty
  verbs) through `_read_apart`, which runs `wg.walk_command`, `wg.classify`
  per segment and `wg.wider_only_kinds`. The fixture `a_branch_and_a_file`
  patches `wg.is_ref` to a set lookup so "a sweep of the generated shapes
  spawns no git per shape" — so this case is **CPU-bound by its own
  account**, and the Windows per-spawn multiplier would not apply to it.
  Whether `wider_only_kinds` still spawns through `_refs` or `_fetched_as`
  (`hooks/worktree-guard.py:1157`, `:1176`) is `questions.md` Q4, a
  measurement, and it decides whether sampling alone brings the case to
  seconds on Windows. The sibling `test_no_constructed_switch_is_silent`
  walks the same generator over `DASHED_SWITCHES` and is not in the local
  top 5, which says the twins' extra cost is in the wider reading of a
  non-switch, not in the generator.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` (8,353 lines). Its
  `repo` fixture copies a session-scoped template, but each gate case runs
  `broad_gate.py`, which runs the fixture's `Broad gate` row —
  `SUITE_ROW = "<python> -m pytest -q -p no:cacheprovider tests"` — at the
  base and at the branch: two pytest start-ups per case, which is where
  about 10 s a case on macOS goes.
- `tests/test_a_fix_of_a_fix_is_counted.py`: a session template too; each
  case drives `round_record.py new` over a planted repository, so the git
  spawns are the script's own.
- `tests/test_one_heredoc_shape_agrees_with_the_shell.py`: 4 runs per case
  (bash, zsh × directly, through eval) over a corpus of about 150 program
  strings, each a shell spawn. Skipped on `windows-latest` by
  `conftest.shell_probe`, so it is the macOS leg's cost and out of scope.

**What the workflow's own readers pin.** `tests/test_arm_check.py:361`
counts `- run: pytest tests/ -q -n auto` as running the module (S6 reader);
an `--ignore` of a module or a `-k` on the line would stop the count.
`tests/test_release_hygiene.py:1046` takes the floor from every
`python: "<x.y>"` in the matrix. `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:39`
reads `test.yml` for the pip line's pins against `run_tests.py`'s
constants. `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:446`
reads the `ledger` job's warning line. None of them reads `on:`, so the
dispatch trigger is free; the shard arguments and a new pin are not.

**The ledger.** `seal/releases/0.18.2.md` D1 anchors five cases of the guard
module, the twins case among them at `@3e34189e`. The file is frozen
(`Ledger frozen from | 1790993141`), so the re-read is a row in this item's
fragment written by `--reverify --into`.

**What breaks in six months.** The budget's two numbers are set from one
measurement on one day's runners. A slower runner image, or a case added
at 80% of the ceiling, makes a leg red for a reason unrelated to the
change under review — the failure direction is *block more*, and a red that
fires on every run in some environment is the outage `CONTRIBUTING.md`
names. The mitigation is the rule in `questions.md` Q6 (1.5× the measured
figure, so a 50% slower day passes) and the fact that both numbers are one
constant each, beside the run id they came from. The `.test_durations` file
goes stale as cases are added; it unbalances the shards and changes
nothing about what they cover, and the budget names the leg that grew.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Measure locally on macOS and infer Windows from the 60 ms / 22 ms spawn ratio | The twins case spawns no git per shape, so the ratio does not apply to it; the issue's own comment calls this a reading, not a measurement. `CONTRIBUTING.md` §*What a change to a gate must carry* asks for platform honesty | Rejected — the Windows leg prints its own table |
| B. Open a draft pull request to get CI runs | When framed, `routing.md` said `stop before the pull request`, and a draft is a pull request; a `workflow_dispatch` trigger is one line, and the session ran it against the pushed branch for the baseline. Routing became `automation` on 2026-10-06, so the draft pull request opens at the end of the build and its runs confirm phases 3 and 5 | Rejected for the baseline; from the pull request on, both run, and the trigger stays for a SHA no pull request covers |
| C. Delete the 165 s case | It is the one case holding that a restore-shaped `checkout` is silent wherever a redirection stands, and D1 of `seal/releases/0.18.2.md` cites it. The owner's second comment refused this | Rejected |
| D. Sample the product with a seeded random generator | A red is reproducible only with the seed, and a seed changed by hand drops coverage silently. A deterministic covering sample whose coverage the module asserts has neither failure | Rejected in favour of a covering sample |
| E. Shard by a hand-kept module list (`--ignore`/paths per shard) | Deterministic and plugin-free, but the list rots as modules grow, an `--ignore` of a module on the pytest line changes what `test_arm_check.py`'s S6 reader counts, and balance is guessed rather than measured | Kept as the fallback if `pytest-split` fails a pin or has no wheel; not chosen |
| F. `pytest-split` with a committed durations file | Balanced by the leg's own figures; a stale file unbalances and never uncovers; one more pinned test-only package, held to `run_tests.py` the way `markdown-it-py` is | **Chosen** for the shards |
| G. Split the Windows suite by xdist alone (`-n` higher than the cores) | Hosted `windows-latest` has 4 cores; more workers than cores on a spawn-bound suite buys nothing a measurement has shown, and a single 165 s case is a floor no worker count lowers | Rejected |
| H. `pytest-timeout` as the per-case budget | It kills a hung case and reports a timeout, which is a different claim from "this case is over the ceiling": the case is killed mid-call, and the message is the plugin's. A conftest hook over the `call` duration fails the case after it ran, with this repository's sentence | Rejected; a conftest ceiling is chosen |
| I. `timeout-minutes` alone as the budget | A leg that goes red names no case; the person at the log opens the `--durations` table by hand | Rejected alone; chosen together with the per-case ceiling, which names the case |
| J. Run the Windows leg on `main` only, or nightly | Three Windows-only defects after round 12 of one branch (`skills/code-review/orchestration.md:559`) is why the leg is on pull requests | Rejected — the issue refuses it |
| K. Stub the sealer fixture's `Broad gate` row with a script that prints a pytest-shaped summary | Cheap, but the `collected_nothing` D1 of `seal/releases/0.18.2.md` (line 19, re-read in 0.18.3) and the cases it anchors are claims about pytest's real output under xdist. A stub is admissible only for a case whose claim is not about that output | Decided per case by the work (`questions.md` Q5), never module-wide |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The measurement, from the Windows leg itself.** `test.yml`: `on.workflow_dispatch`, bare; the `pytest` step keeps its `- run: pytest tests/ -q -n auto` head and gains `--durations=50`; the `test.yml` comment's "198 s against 24 s" paragraph says the figures are dated and points at `phases/phase-1.md`. Landed at b9435eda. The Defender step and the input that gated it, which this row once planned for the same edit, were refused (`questions.md` Q10 (b)) and are not owed. The session pushed and dispatched once (run 37429940700, `handoff.md`). **Still owed, and what closes the phase**: `phases/phase-1.md` gains the three legs' top-50 tables from that run, with run id, SHA and date, `executed`; Q2 answered | **Needs a CI run** — taken. Locally: the six `test.yml`-reading modules `phases/phase-1.md` names, exit read directly (§1). In CI: `gh run view 37429940700 --log` shows the tables (S1, S2) | |
| 2 | **Dropped 2026-10-06.** The Defender step was refused by the harness as weakening a security control (`phases/phase-1.md`) and then by the owner (`questions.md` Q10 (b)). No step, no dispatch pair, no `phases/phase-2.md`; Q3 closes as not measured and Q7 with the input gone. Nothing is owed here, and the cut rests on phases 3 and 4 | nothing — no work exists to verify | 0ba13a2a (dropped: the commit that recorded the owner's answer) |
| 3 | **The Windows shards, built after 4b.** `pytest-split` pinned in the pip line and as `PYTEST_SPLIT` (NAME NOT IN TREE: this phase plants it) in `run_tests.py` beside the three other test-only pins, with the case that holds the two lines together extended; `.test_durations` from the Windows leg's `--store-durations` (one run — a dispatch, or the draft pull request's — with `actions/upload-artifact`, downloaded with `gh run download`), committed beside `tests/`; the matrix gains `shard: [1..K]` on Windows only, `K` from phase 1's Windows table less phase 4b's cuts against Q1's target; `CONTRIBUTING.md` §*Running the checks*' "CI runs five jobs" sentence counts the shards. `phases/phase-3.md`: each shard's `passed`/`skipped` and wall time, the sum against the unsharded leg of the last run before the shards (S4) | **Needs a CI run.** Locally the six `test.yml`-reading modules of phase 1 again; in CI the shard logs | |
| 4a | **The twins case on a covering sample.** A sampler over `_placed(verb)` in `test_guard_resolves_the_tree_it_judges.py` with the coverage contract of S5 asserted by a structural case in the module; `test_no_twin_is_asked_unless_an_operator_cuts_the_segment` and `test_no_constructed_switch_is_silent` walk the sample; the red shown against `94d7b2e0`'s reading (`bin/mutation-check` or a reverted line) and recorded in `phases/phase-4.md` (§15); Q4 measured by a `test_tmp_*` probe counting `subprocess.run` calls during the case, deleted (§7), its count in the phase record; `evidence-check --reverify --into seal/ledger/1791270165-….md --checked <date>` for D1 of 0.18.2 (S6). Buildable before phase 1's run returns | `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q`, time read off pytest's summary (under 30 s on the smith's machine); `evidence-check --strict .` exit 0 | 83801eac (4a) |
| 4b | **The other cases the Windows table names, built before phase 3.** For each module in the Windows top 50 whose per-case figure the table confirms — the sealer module, `test_a_fix_of_a_fix_is_counted.py`, the two guard cases at 31 s and 38 s locally — a cut on the terms of `spec.md` Scope 4 and Q5, each named in `phases/phase-4.md` with what it keeps and what left; released rows whose anchors move re-read into the fragment (S6). A module the Windows table does not confirm is left alone and said so | The narrow run of each module touched; `evidence-check --strict .`; `git diff --stat origin/release/v0.20.0...HEAD -- seal/releases seal/ledger.md` empty | |
| 5 | **The budget.** `tests/conftest.py`: `CASE_CEILING_S` (NAME NOT IN TREE: this phase plants it) and the hook that fails a `call` over it with the S7 message, the constant's comment naming the Windows figure and run id it was set from by Q6's rule, the figure being the leg after phases 3 and 4; `timeout-minutes` on the three `pytest` jobs by the same rule, each beside its run id (S8); a `test_tmp_*` probe sleeping past the ceiling seen red and deleted (§15, §7); one confirming run — the draft pull request's, or a dispatch — whose Windows leg is under Q1's target. `changelog.md` (one `### Changed` entry: the Windows leg before and after, dated, and what a slow case now sees), `seal/ledger/1791270165-….md` with one row per scenario and the re-reads, `overview.md` closed (S9) | **Needs a CI run** for the confirming figure. Locally: `bin/test tests/test_docs_line_wrap.py -q`; `evidence-check --strict .` exit 0 read directly | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. What a phase discovers while
it is being built, and needs the next phase to know, goes to
`seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes. **Re-read the Status
column after any rebase**: a squash orphans these commits in every clone but
the one that wrote them.

## Operational impact

- **CI only.** No migration, no environment variable, nothing a plugin user
  installs. `hooks/` and `skills/` are untouched.
- **One new test-only package**, `pytest-split`, pinned on the terms the
  three existing test-only pins state; the local runner installs nothing
  new because `bin/test` never passes `--splits`.
- **A new failure a contributor can meet**: a case over the per-case
  ceiling `CASE_CEILING_S` (NAME NOT IN TREE: phase 5 plants it) fails with
  a sentence naming it, and a leg over `timeout-minutes` fails at GitHub.
  Both are *block more*; the prompt budget is zero.
- **The Windows leg's `--durations=50` table** appears in every run's log.
