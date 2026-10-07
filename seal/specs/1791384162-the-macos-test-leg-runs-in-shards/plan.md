# Implementation Plan: the macOS test leg runs in shards (#864)

<!-- seal/specs/1791384162-the-macos-test-leg-runs-in-shards/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved. -->

## Summary

Two phases. Phase 1 writes the three macOS shard entries, the one reading of
the matrix that the shard test and three other cases then import, and every
sentence that said macOS was one job; it ends at a commit the session pushes
and dispatches, because the smith cannot (`agents/smith.md`, contract §6).
Phase 2 reads that run — the count stays at three if its slowest macOS shard
is at or under the inherited 12 minutes, and goes to four for one more run if
not — sets each macOS shard's budget from the measured figure by the
inherited rule, and writes the records: the phase files, the ledger fragment
with its re-reads and one correction, the changelog entry, the closed
overview.

The frame is #841's, one leg over: the same plugin, the same file, the same
two inherited numbers, and the same way of measuring (the leg's own jobs,
read with `gh`). What is new is the argument that one Windows-measured file
divides the suite the same way on every leg, because collection is identical,
so the only thing macOS has to measure is the balance, and a run gives it.

**Each phase fits one spawn.** Phase 1 is one workflow edit, one helper with
its fixture cases, four call sites, one function rename, three documents'
sentences, and the narrow runs of the modules that read `test.yml`. Phase 2
is reads of one run, one or two workflow edits, and the records. The CI run
between them is not the smith's clock.

## Technical context

**The legs, measured from the Actions API** (`executed` 2026-10-07 by this
frame, `gh run view <id> --json jobs`, `startedAt` to `completedAt`; the
Windows column is groups 1 to 4 in order):

| Run | What it ran | macOS | ubuntu | Windows shards |
|---|---|---|---|---|
| 37535781870 | #841's pull request, 2026-10-06 | 20 m 29 s | 8 m 58 s | 10 m 03 s · 9 m 36 s · 10 m 58 s · 10 m 12 s |
| 37560524126 | #854's pull request | 15 m 34 s | 7 m 51 s | 9 m 19 s · 6 m 17 s · 10 m 01 s · 11 m 41 s |
| 37576998008 | #832's pull request | 16 m 52 s | 8 m 34 s | 11 m 19 s · 6 m 43 s · 8 m 44 s · 12 m 42 s |
| 37577753583 | the 0.20.0 fragments, pull request #861 | 20 m 30 s | 8 m 09 s | 9 m 15 s · 8 m 13 s · 6 m 28 s · 12 m 15 s |
| 37579688353 | the release pull request | 15 m 25 s | 8 m 15 s | 9 m 40 s · 10 m 01 s · 10 m 53 s · 9 m 56 s |
| 37580460950 | `main` after the merge | 17 m 27 s | 8 m 29 s | 10 m 42 s · 8 m 57 s · 10 m 12 s · 11 m 59 s |

The slowest macOS job on record is 20 m 52 s, run 37469595104, the base the
current 35 was set from (`test.yml`'s comment, `read`). Inside the 20 m 30 s
job of 37577753583 pytest reported 12,730 passed and 89 skipped in
1,204.74 s, so about 25 s of a macOS job is outside pytest (checkout, Python,
the pip install) — against 37 s plus 25 s to the first case on Windows
(#841's `phases/phase-3.md`). The same run's Windows shards reported 517,
460, 364 and 698 s of pytest time: 2,039 s for a leg that ran 1,974 s
unsharded, so a shard's own start-up inside pytest is about 16 s, and the
slowest shard is 1.37 times the mean by pytest time. That spread is the
file's age showing: the division is equal in the file's own seconds (below),
and the cases the file does not know take the mean.

**One file divides every leg the same way** (`executed` 2026-10-07). The
three legs collect the same cases — 12,819 at 5623d728 on macOS (12,730 +
89), on ubuntu (12,739 + 80) and across the four Windows shards (2,734 +
6,742 + 1,120 + 2,223), and 12,819 from `--collect-only` on this tree. The
division is `pytest-split`'s default, `duration_based_chunks` (NAME NOT IN TREE: it is the plugin's, read from the 0.11.0 wheel):
collection order, cut into contiguous groups of equal summed duration, a
case the file does not name given the mean of the ones it does. Reproduced
over this tree's collection order and the committed file (this frame's
probe, in the session's scratch directory and not the tree; the figures are
here):

| N | Windows seconds per group | cases per group | the shell oracle's group | macOS top-50 seconds per group (of 410.8) |
|---|---|---|---|---|
| 2 | 3,768.9 · 3,765.3 | 9,465 · 3,354 | 1 | 278.8 · 132.0 |
| 3 | 2,513.0 · 2,516.5 · 2,504.7 | 6,173 · 3,698 · 2,948 | 2 | 108.6 · 177.3 · 124.9 |
| 4 | 1,884.1 · 1,884.8 · 1,885.3 · 1,880.0 | 2,525 · 6,940 · 1,024 · 2,330 | 2 | 103.4 · 175.4 · 47.3 · 84.8 |
| 5 | 1,508.3 · 1,507.2 · 1,507.1 · 1,507.0 · 1,504.5 | 1,857 · 5,412 · 2,380 · 1,547 · 1,623 | 2 | 92.9 · 167.3 · 25.7 · 40.1 · 84.8 |

The file holds 13,042 entries summing to 7,530 s; 504 collected cases are
not in it and 727 of its entries are no longer collected. The shell oracle
(`tests/test_one_heredoc_shape_agrees_with_the_shell.py`, ten cases) is
1.00 s in the file, because `conftest.shell_probe` skips it on Windows, and
113.2 s of calls in the macOS top 50 of run 37577753583 — the one cost the
file cannot see, and it lands whole in one group at every N because a
contiguous cut keeps a module together. The last column is a hint and not a
sum: the top 50 are 410.8 of roughly 3,400 macOS worker-seconds.

**The arithmetic, in #841's form.** A macOS shard's job is about 25 s
outside pytest, about 20 s of start-up inside it, and the leg's case time
divided by N times the group's share. The case time is 1,185 s on
37577753583's pace and 1.02 times that on 37469595104's. For the share: the
oracle alone makes one group about 1.08 times its siblings at N = 3 (113 s
on roughly 1,130 s), and the file's age shows as 1.37 on Windows today;
1.45 is taken as the factor for the slowest group.

| N | at balance, the faster pace | the slowest group at 1.45, the slower pace |
|---|---|---|
| 2 | 45 + 592 = 637 s, 10.6 min | 45 + 604 × 1.45 = 921 s, 15.4 min |
| 3 | 45 + 395 = 440 s, 7.3 min | 45 + 403 × 1.45 = 629 s, 10.5 min |
| 4 | 45 + 296 = 341 s, 5.7 min | 45 + 302 × 1.45 = 483 s, 8.1 min |
| 5 | 45 + 237 = 282 s, 4.7 min | 45 + 242 × 1.45 = 396 s, 6.6 min |

**N is 3.** Two misses the inherited 12 minutes on the slower pace with any
imbalance at all. Three meets it with a minute and a half to spare at the
factor taken. Four meets it with four to spare and buys a run nothing: the
run's critical path is its Windows shards, 9 m 56 s to 12 m 42 s on the runs
above, and ubuntu at 7 m 51 s to 9 m 03 s — a macOS shard under 10 minutes
is already off it. What four costs is a fourth macOS job per run. GitHub's
limits page (`read` 2026-10-08) caps concurrent macOS jobs at 5 on the Free,
Pro and Team plans and at 50 on Enterprise, shared across every hosted
runner size; `gh api user` returns no plan for this account, and a public
repository under a user account is on one of the first three unless told
otherwise. Eleven 0.21.0 work items push in parallel, and the runs above
overlapped two and three at a time, so each macOS job a run adds is a job
that waits on another run's. The argument does not rest on what the page
says happens past the cap; it rests on the cap being five and a job being a
job.

**The measurement decides, not the arithmetic.** The factor 1.45 is an
estimate from two sources, and the issue asks for the macOS balance to be
measured. Phase 2 reads the first sharded run; three stands if its slowest
shard is at or under 12 minutes, and four replaces it for one more run if
not (`questions.md` Q2). Nothing here needs a person, because both outcomes
are written down with what each does.

**What the workflow's readers pin** (`read`; the eight modules that name
`test.yml`, by `grep`). `tests/test_arm_check.py` counts the `pytest` job by
its pytest line through `jobs`, which the shards do not touch.
`tests/test_release_hygiene.py` takes the floor from every `python:` in the
file, and three new entries carry `"3.12"`.
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py` reads the pip
line and the job's `python:` values. `tests/test_a_slow_case_names_itself.py`
wants `timeout: N }` on every `- { os:` line, so the three entries carry one
from the first commit.
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`,
`tests/test_the_gate_names_every_step_ci_runs.py` and
`tests/test_deferral_check.py` read other jobs or lines. Only the shard
module asserts that a non-Windows entry carries no split, and that is the
assertion this work widens. Two more modules matter without naming the file:
`tests/test_ci_gives_the_checks_what_they_need.py` reads every workflow
through `jobs`, and `tests/test_a_workflow_is_read_the_one_way.py` drives
`conftest.py`'s readers over fixtures, which is the pattern the new helper's
cases follow.

**The ledger.** `seal/releases/0.20.0.md` is frozen. S1, S2 and S8 anchor
`.github/workflows/test.yml#pytest@f453cc43` (S8 also
`tests/test_a_slow_case_names_itself.py#test_every_pytest_leg_has_a_timeout_and_the_job_reads_it@b32fe58d`,
S2 the floor case and the pins case of the cheap-twice module), and S4
anchors the shard module's three cases. Editing the job drifts the first
three, which `evidence-check --reverify --into seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md --checked <date>`
re-reads into this item's fragment; renaming S4's first case moves an
anchor, which a `Corrected ·` row re-points, carrying every coordinate S4
still rests on (`docs/the-evidence-ledger.md` §*A released row is read again
in the branch's fragment*). Between phase 1's commit and phase 2's fragment,
`evidence-check .` reads DRIFTED on those rows and nothing BROKEN, and the CI
`ledger` job warns and does not fail.

**What breaks in six months.** The file goes on ageing: every case added
takes the mean, every case removed leaves a dead entry, and the groups drift
apart on both legs until a shard meets its budget — the budget names the
leg, `CONTRIBUTING.md` names the refresh, and this item adds no second file
to keep fresh. The second thing is the three-entry matrix growing to four or
five by hand: the shard module refuses a count whose groups are not exactly
1 to K, so a fifth macOS entry naming group 3 twice is red, and a
block-style entry someone writes for a longer `split` is refused by the
reader rather than silently not counted. The failure direction everywhere is
*block more*.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Two macOS shards | 15.4 minutes predicted for the slowest shard on the slower pace: over the inherited 12 with any imbalance, and macOS stays the leg a run waits on | Rejected |
| B. Three macOS shards | 10.5 predicted; if the measurement says over 12, the count goes to four for one more run (Q2). A third macOS job per run against a cap of five | **Chosen** |
| C. Four macOS shards | 8.1 predicted and no shorter run, since the Windows shards take 10 to 12.7 minutes; a fourth macOS job per run against the cap, and 45 s more of macOS runner time per run for nothing a run waits on | The fallback phase 2 takes if three misses |
| D. A second durations file measured on macOS (`--durations-path`) | two files ageing apart, two refresh runs and two recipes; the division is the same on every leg already, and the imbalance today is the file's age, which a second file inherits | Rejected; the next design only if four misses, as its own issue |
| E. `least_duration` (NAME NOT IN TREE: the plugin's other algorithm) instead of contiguous chunks | spreads a module across shards, so each shard builds the module's session fixtures again — #841 chose chunks for that reason and the Windows shards run on it | Rejected, inherited |
| F. Keep each test's private slice of the job and change only the shard test's assertion | a fifth reader of one judgment in a suite #834 counted four in, each a guess over YAML text, and a block-style entry invisible to the one that reads entries | Rejected; the brief's rule and #834's numbers |
| G. The entries helper in `tests/conftest.py`, beside the step readers | `conftest.py` cannot import `jobs` from a test module without a cycle, and the job split already lives beside `jobs`, where `tests/test_arm_check.py` imports it; moving `jobs` is #835's or #867's kind of consolidation | Rejected; the helper lives beside `jobs` |
| H. Rename the shard module as well as its first case | three released anchors move for a name, when the file's sentence is still true and its docstring can say what it holds | Rejected |
| I. A provisional macOS shard `timeout` from the arithmetic (15) before the measurement | the measuring run goes red on a guessed budget and measures nothing; 35 can only be too loose, for one run | Rejected; 35 until phase 2 |
| J. Measure the balance locally on a macOS machine and skip the CI loop | a laptop under other suites ran one case at four times its CI figure (#841's `phases/phase-5.md`); the issue asks for the leg's own figure, and the runner image is `macos-26-arm64` | Rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The shards and the one reading.** `test.yml`: three `macos-latest` entries with `split: "--splits 3 --group k"` and `timeout: 35` each; the comment above the entries saying the three carry the unsharded leg's budget until phase 2 measures; the Windows block's paragraph widened to both sharded legs with the collection argument and the probe's figures; the two *`split` is empty* sentences rewritten for ubuntu alone. `tests/test_ci_gives_the_checks_what_they_need.py`: `pytest_matrix` (NAME NOT IN TREE: this phase plants it) beside `jobs`, its docstring naming the input class and what it refuses, and its fixture cases (a flow entry parsed with quotes off; a commented entry not counted; a block-style item refused naming the line). The four slice sites moved onto `jobs` and the helper. The shard module widened to a table of sharded systems, its first case renamed, its docstring rewritten; `test_a_slow_case_names_itself.py` reads entries through the helper. The `PYTEST_SPLIT` comment in `run_tests.py` and `CONTRIBUTING.md`'s three sentences. Every new or changed case seen red (§15) — the shard case under each of S1's four matrix breaks, the helper's cases with the refusal deleted and with a commented entry counted, the timeout case with a macOS `timeout` removed — and the reds listed in `phases/phase-1.md`. One commit; the hand-back names the push and the dispatch | Locally: `bin/test` over the eight modules that name `test.yml`, `tests/test_ci_gives_the_checks_what_they_need.py` and `tests/test_a_workflow_is_read_the_one_way.py`, exit read directly (§1); `grep -rn 'index("  pytest:")' tests/` empty; `evidence-check .` reads DRIFTED on 0.20.0's S1, S2, S4, S8 and nothing BROKEN, exit 1 read directly. **Needs a CI run** the session starts: `git push`, then `gh workflow run test.yml --ref chore/864-the-macos-test-leg-runs-in-shards` while no pull request is open, the push alone once the draft is | |
| 2 | **The measurement, the budget and the records.** Read the run: each macOS job's `startedAt` to `completedAt` and its summary line, ubuntu's summary line, the shards' `--durations=50` heads (Q1). S1: the three sums equal ubuntu's. S2: the slowest at or under 12 minutes — then each macOS entry's `timeout` is 1.5 times it rounded up to 5, the comment names the run, and `CONTRIBUTING.md`'s count sentence says three; over — `--splits 4`, a fourth entry, the shard table's count 4, the sentence four, one more run, and the budget from that run (Q2). `phases/phase-2.md`: every shard's time, count and head, the sum, the rule applied. `seal/ledger/1791384162-the-macos-test-leg-runs-in-shards.md`: one row per scenario with the run id; the `Re-read ·` rows for 0.20.0's S1, S2 and S8 by `--reverify --into`; the `Corrected ·` row re-pointing S4 to the renamed case with every coordinate S4 still rests on. `changelog.md`: one `### Changed` entry — the macOS leg's 15 m 25 s to 20 m 52 s before, the slowest shard after, run ids and dates, three jobs where there was one, and what a contributor refreshing the file now does. `overview.md` closed, its `## Not verified` table naming the sealer for the whole suite | **Needs a CI run** for the figure, and the pull request's run at the final SHA confirms the job reads the budget. Locally: the modules of phase 1 again; `evidence-check --strict .` exit 0 read directly | |

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
`seal/specs/1791384162-the-macos-test-leg-runs-in-shards/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes. **Re-read the Status
column after any rebase**: a squash orphans these commits in every clone but
the one that wrote them.

## Operational impact

- **CI only.** No migration, no environment variable, no new package:
  `pytest-split` is already pinned and on the pip line. `hooks/` and
  `skills/` are untouched; the local runner never passes `--splits`.
- **Three macOS jobs per run instead of one**, each about 45 s of fixed
  cost, against GitHub's cap of five concurrent macOS jobs on every plan but
  Enterprise (`read`). A run alone waits about ten minutes less on the macOS
  leg; two runs at once share the cap.
- **A contributor refreshing `.test_durations`** replaces the four Windows
  entries with the one `store` entry as before and leaves the three macOS
  entries in place; the recipe says so. The shard module goes red on that
  branch for the Windows leg, which is the `always()` the recipe already
  explains.
- **A new red a contributor can meet**: a macOS shard over its budget fails
  at GitHub, as the unsharded leg did at 35; a block-style matrix entry is
  refused by the suite with its line. Both *block more*; the prompt budget
  is zero.
