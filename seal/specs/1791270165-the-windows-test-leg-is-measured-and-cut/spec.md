# Feature Specification: the Windows test leg is measured and cut (#841)

<!-- seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Every pull request waits on the slowest leg, and a release waits on it twice. A leg at 35–40 minutes is a cost paid against the first goal on every run, which is why the owner marked the issue urgent. Nothing here may add a question to a person: the whole change runs in CI and in the suite |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `.github/workflows/test.yml` decides whether a pull request proceeds, so a change to it carries the four items: a test seen red, a stated failure direction, a prompt budget (zero here, and the pull request body says so), and platform honesty — the Windows figures come from the Windows leg itself, never from a macOS run multiplied by a per-spawn ratio |
| `CONTRIBUTING.md` §*Running the checks* | States "CI runs five jobs" and that the suite's cost is "a figure with a date and a machine, recorded in the work item that measured it, not here". A sharded Windows leg and a budget change the first sentence; the figures this item measures go in its phase records and `overview.md`, dated, and not into `CONTRIBUTING.md` |
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true* | `broad_gate.py#PARTITION` mirrors `hygiene.yml`'s steps, not `test.yml`'s, and `seal/config.md`'s `Broad gate` row is `bin/test -q`. Sharding in `test.yml` adds no arm and changes no partition; a per-case ceiling planted in `tests/conftest.py` reaches `bin/test` and CI alike, so the gate and CI keep saying the same thing |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* and `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | `seal/releases/0.18.2.md` row D1 (the worktree guard) anchors `tests/test_guard_resolves_the_tree_it_judges.py#test_no_twin_is_asked_unless_an_operator_cuts_the_segment` and four sibling cases, the twins case at hash `3e34189e` when framed. Rewriting that case moves the anchor; the re-read is written by `evidence-check --reverify --into seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md --checked <date>`, and no released file changes. Phase 4a wrote that `Re-read · D1` row on 2026-10-06, and a later cut of the same case re-reads it again · NAME NOT IN TREE |
| `skills/agent-contract/SKILL.md` §2, §7, §15 | The smith runs the modules it touches and never the whole suite, so every whole-leg figure in this item is CI's (§2). A duration probe is a `test_tmp_*` file, run once and deleted (§7). The sampled twins case and the ceiling are each seen red before they are committed (§15) |
| `skills/code-review/orchestration.md` §*the opening of the pull request before round 1* (line 559) and `docs/review-chain-spec.md` line 482 | Three Windows-only defects arrived on one branch after round 12. That is why the Windows leg stays on pull requests, and why this item cuts cases rather than legs |

## Scope

**In.** Four of the five things the issue asks for, numbered as the issue
gives them; the second was refused and keeps its number only so the plan's
references to Scope 1, 4 and 5 stay true. The whole of it is
`.github/workflows/test.yml`, `tests/conftest.py`, test modules, and this
work item's records. No file under `hooks/` or `skills/` changes.

1. **The measurement, read off the Windows leg itself.** The `pytest` job
   prints `--durations=50` on every leg, and `test.yml` gains a
   `workflow_dispatch` trigger so a pushed branch can be measured before any
   pull request exists. The first dispatch at the branch's SHA is the
   baseline; its three legs' top-50 tables, with the run id and the date, go
   in `phases/phase-1.md`. Routing was `stop before the pull request` when
   this was framed and became `automation` on 2026-10-06 (`routing.md`): a
   draft pull request opens at the end of the build, and from then on its
   CI runs the three legs on every push, so the confirming figures of items
   3 and 5 are the pull request's own. The trigger stays, because the
   baseline was taken through it (run 37429940700, named in `handoff.md`)
   and a SHA no pull request covers is still measured that way. The
   local macOS table in the issue's first comment (12,958 passed in 456 s;
   165 s for the twins case) is `executed` by the orchestrator on 2026-10-06
   and is cited, not re-measured.

   **Which measurement is shared with #826, and who owns it.** Two items meet
   at the worktree guard's corpus cases. The split is: **this item owns the
   per-case duration measurement** — `--durations` on each CI leg and the
   local table above — and #826 reads this item's figures for
   `tests/test_guard_resolves_the_tree_it_judges.py`,
   `tests/test_the_guard_asks_once_per_session.py` and
   `tests/test_no_shape_the_base_stops_reads_silent.py` instead of timing
   them again. **#826 owns the stop-count measurement** over the 27,351
   recorded command and directory pairs (the count `test_guard_resolves…`
   line 944 already cites from work item 1790993140 phase 3), and this item
   neither runs nor cites it. The 165 s case is cut here by sampling its
   product (below) and is **rewritten or retired in #826**, as the owner's
   second comment on #841 decided; this item does not decide that.

2. **No Defender step.** The issue's second item, a step turning real-time
   scanning off on the Windows runner, is out of this work: the harness
   refused to write it as weakening a security control (`phases/phase-1.md`),
   and the owner refused it on 2026-10-06 (`questions.md` Q10 (b)). Nothing
   measures it (Q3 closed unmeasured), no dispatch input gates it (Q7
   closed with the input gone), and the cut rests on items 3 and 4 below.

3. **The Windows suite split across shards.** `K` Windows jobs, each running
   a disjoint subset whose union is the whole suite, `K` decided from phase
   1's Windows table less item 4's cuts against the target in `questions.md`
   Q1, which is why the shards are built after the cuts. The union is
   verifiable: the shards' `passed + skipped` counts sum to one unsharded
   leg's. The ubuntu and macOS legs stay one job each unless their measured
   time says otherwise.

4. **The heaviest cases cut at the source, keeping what each holds.**
   - `test_no_twin_is_asked_unless_an_operator_cuts_the_segment` keeps its
     property and samples the product: every redirection operator at every
     position (glued and spaced, target glued and spaced) appears at least
     once across the sample, and every twin verb appears with at least one
     redirection; the sample is deterministic, so a red reproduces by name.
     The same sampler serves `test_no_constructed_switch_is_silent`, which
     walks the same `_placed` generator over `DASHED_SWITCHES`. · NAME NOT IN TREE
   - The other modules the measurement names — `test_the_seal_is_taken_once_by_the_sealer.py`
     (13 cases in the local top 40, about 10 s each), `test_a_fix_of_a_fix_is_counted.py`
     (7, about 12 s each), the two guard cases at 31 s and 38 s — are cut
     only where the Windows table confirms them and only in a way that
     leaves the case's claim exercised: a shared run for cases that only
     read a verdict, a cheaper fixture command where the claim is not about
     pytest's output, a smaller corpus where the claim is a property over a
     product. Each cut names what it keeps and what it drops in its phase
     record.
   - A repository built once and copied is already the suite's shape:
     `tests/conftest.py#_repo_template` and the sealer module's `_template`
     are session-scoped and copied per case. The remaining `git init` per
     case (61 modules call it through other helpers) is touched only where
     the Windows table names the module.

5. **A budget, decided from the measurement.** Two halves, both cheap and
   both unattended. The leg's half is `timeout-minutes` on each `pytest`
   job, set from the leg measured after phases 3 and 4 by the rule in
   `questions.md` Q6; GitHub fails the leg that exceeds it. The case's half
   is a per-case ceiling in `tests/conftest.py`: a case whose call phase
   runs longer than `CASE_CEILING_S` (NAME NOT IN TREE: phase 5 plants it)
   fails with a message naming the case and its seconds, so a case that
   pushes a leg past its budget names itself in the log rather than hiding
   in a wall-clock total. `--durations` stays on every run as the reading
   surface.

**Out**, each with its reason.

- **Dropping the Windows leg from pull requests, or running it only on
  `main`.** The issue refuses it and the grounding row says why.
- **Any change to `hooks/worktree-guard.py` or to what the guard asks.**
  That is #826's premise change; this item changes test cost only.
- **The Defender step.** Refused twice: by the harness, which would not
  write a step weakening a security control, and by the owner on 2026-10-06
  (`questions.md` Q10 (b)). Q3 closes as not measured, and no phase record
  carries a figure for it.
- **Rewriting or retiring the twins case.** #826's, by the owner's comment.
- **The heredoc shell oracle (`test_one_heredoc_shape_agrees_with_the_shell.py`,
  109 s locally).** `conftest.shell_probe` finds no usable `bash` or `zsh`
  on `windows-latest` (its `bash` is the WSL launcher), so the module is
  skipped there and costs the Windows leg nothing. It costs the macOS leg;
  the per-case ceiling of phase 5 will name it if it is over, and cutting it
  is a follow-up for the repository owner, not this item.
- **The macOS leg's own time (18 minutes on the 0.19.0 release run).** Named
  by the measurement and bounded by the budget, not cut here; the title
  names Windows.
- **`bin/test` and `.github/scripts/run_tests.py`.** The local runner is
  unchanged; the ceiling reaches it through `conftest.py`.
- **#834's inventory of checks that never leave.** The cost side of this
  item, scheduled for 0.21.0.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the Windows leg is measured on Windows | Given the branch pushed, when the session dispatches `test.yml` at its SHA, then each of the three `pytest` legs prints a `--durations=50` table, and `phases/phase-1.md` holds the three tables with the run id, the SHA and the date, labelled `executed` | `gh run view <id> --log` shows the tables; the phase record cites the id |
| S2 · the workflow still says what the pinning tests read | Given the `workflow_dispatch` trigger, the `--durations` flag and later the shard matrix, when the suite's own readers run, then `tests/test_arm_check.py#test_a_job_counts_only_where_its_pytest_line_selects_this_module`'s S6 reader still counts the `pytest` job as running `tests/test_arm_check.py`, `tests/test_release_hygiene.py#test_the_python_floor_is_the_same_number_everywhere` still finds the floor in the matrix, and `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`'s pins on the pip line still hold | the narrow run of those three modules, exit code read directly |
| S3 · withdrawn — the Defender step is not measured | Withdrawn 2026-10-06 under `questions.md` Q10 (b): no step, no dispatch pair, no `phases/phase-2.md`. S9's one row per scenario excludes this one | `test.yml` carries no such step; Q3 and Q10 read ✅ in `questions.md` |
| S4 · the shards cover the suite | Given `K` Windows shards, when they finish, then their `passed` and `skipped` counts sum to the unsharded Windows leg's from the last run before the shards (phase 4b's closing SHA), any difference being a case phase 3 itself adds and names, and the slowest shard's wall time is at or under Q1's target | the counts read off the three logs and written in `phases/phase-3.md` |
| S5 · the twins case keeps its property on a sample | Given the sampler, when the case runs, then every operator of `_redirections()` appears at every position with each glued/spaced choice at least once across the sample, every verb of `TWINS` and `DASHED_TWINS` appears with at least one redirection, the sample is the same on every run, and the case still goes red against a guard that reads `-b` after `--` as a creation (`94d7b2e0`'s reading) | a structural assertion inside the module over the sample's coverage; the red shown with `bin/mutation-check` or a reverted reading in the phase record; `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` under 30 s on the smith's machine, time read off pytest's summary · NAME NOT IN TREE |
| S6 · a cut keeps the claim | Given a case the Windows table names, when it is cut, then its phase record says what the case held, what it holds after, and what left (a shape, a runner, a repetition), and the released ledger row that anchors it is re-read into this item's fragment | `evidence-check --strict .` exit 0 read directly; `git diff --stat origin/release/v0.20.0...HEAD -- seal/releases seal/ledger.md` empty |
| S7 · a slow case names itself | Given `CASE_CEILING_S` in `tests/conftest.py` (NAME NOT IN TREE: phase 5 plants it), when a `test_tmp_*` probe sleeps past it, then the probe fails with a message holding its node id and its seconds, and a case under the ceiling is untouched; the probe is deleted | the probe's red shown in `phases/phase-5.md` (§15), the deletion stated (§7) |
| S8 · a leg over budget fails by itself | Given `timeout-minutes` on each `pytest` job, when a leg exceeds it, then GitHub fails the job with no step of this repository's involved | the three values in `test.yml`, each beside a comment naming the measured figure and run id they were set from |
| S9 · the records say what shipped | Given the build closed, then `changelog.md` holds one `### Changed` entry a reader of the release notes can act on (the Windows leg's before and after, dated, and what the budget does on a slow case), `seal/ledger/1791270165-….md` holds one row per scenario above and the re-reads S6 owes, the `test.yml` comment block's "198 s against 24 s" paragraph carries the new dated figures or points at `phases/phase-1.md`, and `CONTRIBUTING.md` §*Running the checks*' "CI runs five jobs" sentence counts the shards | `evidence-check --strict .`; `tests/test_docs_line_wrap.py`; the fragment present |

## Data & interfaces

- **`.github/workflows/test.yml`.** `on.workflow_dispatch` bare, with no
  input: the one the frame planned gated only the Defender step, and both
  went together (Q10 (b), Q7). The `pytest` step's line keeps
  the shape `- run: pytest tests/ -q -n auto …` so the S6 reader in
  `tests/test_arm_check.py` keeps counting it; shard selection is passed as
  arguments after it, never as `--ignore` of a module. The matrix keeps
  `python: "3.12"` on every include. The three `timeout-minutes` values are
  this item's and each carries the run id it was set from.
- **`tests/conftest.py`.** Two units phase 5 plants, so neither is in the
  tree yet: `CASE_CEILING_S` and `pytest_runtest_makereport` · NAME NOT IN TREE.
  The constant carries a comment naming the measured figure it was set
  from; the hook (or an equivalent one) fails a `call` report whose
  duration exceeds it, with a message `"<nodeid> ran <s> s, over the <CASE_CEILING_S> s ceiling
  (#841)"`. The ceiling applies on every platform at one value; a platform
  factor is not introduced until a measured case needs one.
- **`tests/test_guard_resolves_the_tree_it_judges.py`.** A sampler over
  `_placed(verb)` whose coverage the module itself asserts (S5). Its name
  and shape are the work's; its coverage contract is this spec's.
- **Sharding.** `pytest-split` (`--splits K --group N`), pinned in the pip
  line and in `run_tests.py` the way the three other test-only packages
  are, with a `.test_durations` file produced by the Windows leg's own
  dispatch run (`--store-durations`, uploaded as an artifact, downloaded
  with `gh run download`) and committed beside `tests/`. A stale file
  unbalances the shards and never changes what they cover. The by-module
  alternative is in `plan.md`.
- **Nothing a plugin user runs changes.** `hooks/` and `skills/` are
  untouched; the packages added are test-only, on the terms
  `CONTRIBUTING.md` §*Running the checks* states for `markdown-it-py`.

## Open questions → questions.md

`questions.md` carries three person's rows — Q1 with a default (the Windows
target), Q6 with a rule (the ceiling and the timeouts), and Q10, answered
(b) on 2026-10-06 — four measurement rows, of which Q3 closed unmeasured
with Q10, and three the work decides, of which Q7 closed the same way.
Nothing in it blocks any phase.

Framed 2026-10-06 by framer, before the build.
