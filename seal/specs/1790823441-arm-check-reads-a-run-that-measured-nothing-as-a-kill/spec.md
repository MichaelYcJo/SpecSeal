# Feature Specification: arm-check reads a run that measured nothing as a kill

<!-- seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Milestone 0.17.0, #703. Found by round 1 of work item `1790815610` (#641,
PR #698), which built `mutation-check` and met the same two defects there:
one it fixed in its own file, one it read in `arm_check.py` and could not
touch (its constraint C2 kept `arm_check.py` unedited). This branch is cut
from `release/v0.17.0` at `a340221b`.

**The class: a verdict read from an exit code with nothing to compare it
against.** `skills/verify/scripts/arm_check.py#run_arms` writes a mutation,
runs `--tests`, and records `by_operator[operator] = run.returncode != 0`.
Nothing runs the command against the module as it is first, so any command
that cannot succeed at all records every arm as `killed`:

- a `-k` that selects no case (pytest exits 5);
- a module path that does not exist (pytest exits 4);
- a case that already fails before anything is mutated (exit 1).

Each prints `killed` beside every arm, `0 watched by no case`, exit 0. That
is the best possible report out of a run that measured nothing, and it is
read by an agent as permission to hand over. A `killed` is only a
measurement when the same command was green against the unmutated module.

**The second defect is in the same file and the same loop.**
`arm_check.py#clear_bytecode_cache` reads `PYTHONPYCACHEPREFIX` (or
`sys.pycache_prefix`) and joins the prefix as given. CPython joins it as
given too (`importlib._bootstrap_external.cache_from_source`, read on
3.14.4: `_path_join(sys.pycache_prefix, head.lstrip(path_separators),
filename)`), so a relative prefix resolves against the cwd of the process
that imports. The cases run in `--cwd`; the clear runs in `arm-check`'s own
cwd. With a relative prefix and a `--cwd` that is not the shell's directory,
the two mirrors differ and the stale `.pyc` stays where the cases read it,
which is the defect the whole function exists to prevent (`seal/releases/0.9.5.md`
row *A mutation loop's verdict can be decided by cached bytecode*).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #703 (the ticket) | The two defects, the three shapes, and the three boxes: a baseline before mutating with each shape seen red first; the relative prefix resolved against the cases' directory, seen red first; `mutation-check` stays green |
| `skills/verify/SKILL.md` §*`arm-check` asks condition 2 of a whole module, one arm at a time* | The documented behaviour this changes. Its last paragraph says *report-only, exit 0 either way — whether an unwatched arm should fail a run is an open decision*. That decision is about a **survivor**, and this item does not touch it: exit 0 whether or not an arm survived stays. A run refused before any mutation is a different fact, and the section already has one — `main`'s `--timeout` guard exits 2 through `parser.error` (pinned by `tests/test_arm_check.py#test_a_negative_bound_is_refused_rather_than_measured`). The section gains the baseline sentence and the second exit |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | §12: the class is *a verdict read with nothing to compare against*, and its members in this file are enumerated in §*Scope*. §14: the verdict word, the `Nothing was written` sentence, the `--timeout` help, the SKILL section and `bin/arm-check`'s header change what a person reads, so each is pinned in the same commit. §15: every new case is seen red against `a340221b`'s script, and the hand-back says how |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `arm-check` is report-only and not a gate (the judgment work item `1790690762` recorded in its `spec.md` §Grounding, inherited here). The failure direction is stated anyway: the change makes the command **refuse more**, and §*Failure direction* says why that is the cheaper mistake. Prompt budget: zero — nothing here asks anybody anything |
| `CLAUDE.md` §*The goal a design is chosen against* | Between refusing a non-green baseline and asking whether to continue, refusing is the design that runs unattended. A person learns the cause from the printed output and re-runs once |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* and §*An anchor degrades to DRIFTED* | New rows go to `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md`. The edit drifts rows in `seal/releases/0.9.5.md` and `seal/releases/0.15.1.md` (§*Data & interfaces*); each is re-read against the edit, its claim corrected in place where the edit made it false, and re-stamped with a dated note. Nothing is appended to a release file |
| `docs/the-broad-gate.md` §*A check that cannot fail is not a check* (the `arm-check` statement) | Still true after this item — arms are enumerated, mutated, and the survivors reported — and its `Enforced by:` line names `test_a_watched_arm_is_killed_and_an_unwatched_one_survives`, which stays green unchanged (S6). No `docs/` edit |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR`, `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one`, `ruff.toml` | `arm_check.py` stays loadable on a 3.9 `python3` (its own comment at `_node_arms` says it is measured there): no `zip(` with `strict=`, no `.UTC`, no three-part version token, ruff-clean |
| `.github/workflows/test.yml`, job `arm-check-grammar` | `tests/test_arm_check.py` is run on 3.13 and 3.14 with `pip install pytest` alone. Every new case drives the command through `sys.executable` and a probe under `tmp_path`, never through `bin/test` or uv |
| Work item `1790815610`, `rounds/round-1-report.md` 🔴 1 and ⬜ 7, `rounds/round-2-report.md` 🟡 10 and ⬜ 12, commit `a4ab9dc0` (on branch `perf/641-129-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout`, unmerged) | The sibling's verdict (`no baseline`, exit 2, nothing written, the baseline bounded by the same `--timeout`), what its reviewer found unpinned afterwards (the bound, the *Nothing was written* sentence, the dropped exit code), and the deferral that is this ticket. Read, not re-argued: §*Judgments the tree answered* in `questions.md` says where this item follows it and where `arm-check`'s shape wants its own answer |

## What was measured before the frame, and by whom

| # | Fact | Label |
|---|---|---|
| M1 | With `PYTHONPYCACHEPREFIX=relprefix`, Python 3.14.4 reports `sys.pycache_prefix == 'relprefix'` and `importlib.util.cache_from_source('/Users/x/proj/m.py') == 'relprefix/Users/x/proj/m.cpython-314.pyc'` — a relative path, resolved by the importing process against its own cwd. `cache_from_source`'s body absolutises the **source** head and joins the prefix as given | executed by the framer: a `python3 -c` that read the standard library and wrote nothing |
| M2 | `arm_check.py:783-790` reads the prefix from `sys.pycache_prefix` or the environment and does `os.path.join(prefix, tail.lstrip(os.sep).lstrip("/"))`; `os.path.isdir(root)` then resolves a relative `root` against the process's cwd, never against `run_arms`'s `cwd` argument, which the function does not receive | read by the framer |
| M3 | `arm_check.py:899` is `by_operator[operator] = run.returncode != 0`, and no call of `subprocess.run` in `run_arms` precedes the first write of a mutation. `main` has no `except` at all, and its only non-zero exit is argparse's 2 from the `--timeout` guard | read by the framer |
| M4 | The three shapes printed `red … (exit 5/4/1)`, exit 0, for `mutation-check` at `6b01b184` of #641's branch, which has the same `returncode != 0` rule | executed by #641's round-1 reviewer (its report §*Executed probes*); **not re-run by the framer**, and not run against `arm-check` by anybody. S1–S3 are what runs it |
| M5 | Five existing cases in `tests/test_arm_check.py` count or sequence the `subprocess.run` calls of one `run_arms` call, or hand it a command that never succeeds, so a baseline run shifts each one: `test_a_spawn_failure_keeps_the_verdicts_already_measured` (fails from the third call, expects four), `test_no_arm_runs_while_cached_bytecode_for_the_module_exists` (`len(seen) == 4`), `test_no_verdict_is_taken_after_a_restore_that_did_not_land` (`len(ran) == 1`), `test_a_pair_whose_command_ran_and_answered_nothing_is_not_called_unasked` (times out the second call), and `test_a_command_that_never_returns_is_recorded_as_unmeasured` together with `test_the_report_does_not_call_a_mutated_arm_unmutated` over `NO_VERDICT_COMMANDS` (NAME NOT IN TREE since phase 1; a command that always hangs or never spawns). `test_the_checker_is_report_only_and_exits_zero_over_the_real_module` has a green baseline and is untouched | read by the framer |
| M6 | Ledger rows whose anchors this item moves: `seal/releases/0.9.5.md` the `clear_bytecode_cache@add61f44` row (also pinned at `test_no_arm_runs_while_cached_bytecode_for_the_module_exists@5d9cbee6`) and the `run_arms@8995285a` row (also pinned at `test_a_command_that_never_returns_is_recorded_as_unmeasured@5c1a7bcb` and `test_a_spawn_failure_keeps_the_verdicts_already_measured@a307a59c`); `seal/releases/0.15.1.md` N2, anchored on the SKILL section's heading and on `run_arms@8995285a`. No row in `seal/ledger.md` or `seal/ledger/*.md` cites either file | executed by the framer: `grep -o` over the three ledger locations |
| M7 | #641's branch (`53659481`, 8 commits past `cd24f516`) edits three files this item edits: `tests/test_arm_check.py` (a `monkeypatch` parameter and one `setattr` in each of the two cache cases, lines 1046–1130), `skills/verify/SKILL.md` (73 lines inserted at line 124, directly after the *report-only, exit 0 either way* paragraph this item rewrites), and `seal/releases/0.9.5.md` (the same `clear_bytecode_cache` row, re-stamping the test anchor's hash). Its `0.15.1.md` edit is row N1, not N2 | executed by the framer: `git diff --stat` and `git diff` on that worktree |
| M8 | `mutation_check.py` loads `arm_check.py` by path and binds `clear_bytecode_cache` and `restore` from it (its lines 141–143), and calls `clear_bytecode_cache(path)` three times with no `cwd`. The file is not in this branch's tree | read by the framer, in #641's worktree |

## Scope

**In.**

1. **A baseline run in `run_arms`.** With `--tests` given, the command runs
   once against the module as it is, after the arms are enumerated and
   before anything is written, with the bytecode cache cleared before it, in
   `cwd`, with the same environment and the same `timeout` as an operator's
   run. The run is green when it exits 0. Anything else — a non-zero exit, a
   timeout at the bound, a spawn failure — is **`no baseline`**: `run_arms`
   raises `NoBaseline` carrying the cause and the command's captured output,
   nothing is written, no arm is measured. It runs on every `--tests` call,
   `--only` or not, and exactly once.
2. **`main` prints the refusal and exits 2.** One line opening with the
   verdict word `no baseline:`, naming the cause as the command gave it
   (`exit 5`, `did not return within 0.3s`, `OSError: …`), saying a failure
   under a mutation would say nothing about the mutation, and ending with
   the sentence *Nothing was written and no arm was measured.* Then the
   command's captured output, so a reader sees pytest's own *no tests ran*
   or *file not found* without re-running. The three pieces a person acts on
   — the word, the cause, the sentence — are pinned (§14).
3. **The sentences that describe the run, made true in the same commit**:
   `run_arms`'s docstring, the `--timeout` help (the bound also covers the
   run against the unmutated module; the two phrases
   `test_the_help_says_the_bound_reaches_the_command_and_not_its_children`
   pins stay verbatim), `bin/arm-check`'s header comment (its step list and
   *exit 0 whether or not an arm survived*), and the SKILL section's closing
   paragraph, which keeps the survivor sentence and gains the baseline and
   the exit.
4. **`clear_bytecode_cache(path, cwd=None)`.** A relative prefix is joined to
   `cwd` — the directory the cases import from — before the mirror is
   built; an absolute prefix and no prefix behave as today. `None` keeps
   today's behaviour (the process's cwd) for a caller that passes nothing,
   which is what #641's `mutation_check.py` does until it is changed
   (`questions.md` Q1). `run_arms` passes its `cwd` at all three call sites,
   including the new baseline's. The docstring names which directory a
   relative prefix is read against and why.
5. **The five shifted cases (M5) rewritten, keeping every assertion they
   make.** The call-counting ones move their count or their failing call by
   one for the baseline. The two that hand `run_arms` a command that never
   succeeds get a probe that is green against the unmutated module and
   hangs only on a mutated one, so the per-arm timeout path they pin is
   still the path they reach; the spawn-failure parameter is driven by a
   `subprocess.run` that raises from the second call on. The timeout, the
   spawn failure and the restore-that-did-not-land are still per-arm facts
   the report has to carry, and nothing in this item retires them.
6. **New cases in `tests/test_arm_check.py`**, each seen red against the
   script at `a340221b` before it is committed: S1–S5, S8, S9 below.
7. **The records**: this item's ledger fragment and changelog fragment
   (`### Fixed`); the three release rows M6 names, re-read and re-stamped
   with a dated note, their claims corrected in place where the edit made one
   false (the `run_arms` row's *un-asked* narrative and the
   `clear_bytecode_cache` row's *clearing the cache around every mutation*
   are what to re-read); `overview.md` closed.

**Out, each with its grounds.**

- **#312, #313, #314, #687.** Each is a different class in the same file:
  loss on a signal no `finally` sees, a bound that reaches the direct child
  only, a guard that refuses the sign and not `nan`/`inf`, a CI-leg reader
  that counts a job running no case. None is *a verdict read with nothing to
  compare against*, and the ticket keeps them out. #313's bound is the one
  the baseline inherits, so the baseline's timeout has the same reach #313
  describes — stated in the help text, not fixed here.
- **`main` catching every other exception and exiting 2** (mutation-check's
  🟡 3). In `mutation-check` exit 1 is `SURVIVED`'s code, so a traceback read
  as a verdict. In `arm-check` exit 1 is no documented verdict — a survivor
  exits 0, a refusal 2 — so a traceback does not read as one. The cost of
  adding it is a decision about every exception class the loop can raise
  (`UnknownNodeType`, `RuntimeError` from `restore`), which is not this
  defect.
- **`mutation_check.py`'s three `clear_bytecode_cache(path)` calls gaining
  `cwd=cwd`.** The file is on an unmerged branch and not in this tree. The
  one-line change belongs to whichever branch lands second (`questions.md`
  Q1, `plan.md` §*Operational impact*).
- **A prefix the parent got from `-X pycache_prefix` rather than the
  environment.** `clear_bytecode_cache` reads `sys.pycache_prefix` first, and
  a child spawned from `--tests` inherits only the environment, so a parent
  started with `-X` clears a mirror its children never use. Nobody has met
  it and it is a different cause (the two processes see different prefixes,
  not the same prefix from different directories).
- **Printing the command's output on a kill or a survival**, and any change
  to the report's arithmetic. The baseline's output is printed because it is
  the one run whose cause a person has to read to act; a kill's output is a
  case failing as intended.
- **Whether a survivor should fail the run.** The SKILL section calls it an
  open decision and `test_the_checker_is_report_only_and_exits_zero_over_the_real_module`
  pins today's answer. S7 keeps it green.
- **Writing arm-check's and mutation-check's exit tables as one table in
  `skills/verify/SKILL.md`.** The second table is on #641's branch; merging
  the prose is the merge's act.

## Failure direction

The change makes `arm-check` **refuse more**: a `--tests` that is not green
against the unmutated module used to produce a report and now produces a
refusal. A wrong refusal costs one re-run with a corrected command, and the
cause is printed. A wrong kill ships a false *watched by a case* into a
record an agent hands over on, which is the direction the whole checker
exists to prevent. The cost in the ordinary case is one extra run of the
command per invocation (61 mutations become 61 plus one on
`hooks/review-history-guard.py`), and a hang that does not depend on a
mutation now lands in the baseline, under the same bound, before anything is
written — which is why the baseline's bound is pinned (S4).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · a command that selects nothing refuses the run | Given the `two_arms` fixture and a `--tests` probe that exits 5 whatever the module holds, when `main` runs with `--tests`, then stdout opens with `no baseline:`, names `exit 5`, carries *Nothing was written and no arm was measured*, prints no `killed`/`SURVIVED` line and no `arms measured` line, the exit is 2, the module is byte-identical, and no `.pyc` for it exists | `tests/test_arm_check.py`, a parametrised case over exit 5, exit 4 and exit 1. **Red at `a340221b`**: `killed` beside both arms, exit 0 |
| S2 · a command that cannot start its run (pytest's usage error) | The same, with the probe exiting 4 | the same parametrised case |
| S3 · a case that already fails against the original | Given a probe that imports the module and asserts something false of the **unmutated** `classify`, then `no baseline` naming `exit 1`, and the same byte-identical module | the same case, plus one parameter that fails through an import rather than a bare `sys.exit`, because that is the shape a person meets |
| S4 · the baseline is bounded by `--timeout` | Given a command that sleeps 30 s against the unmutated module and `timeout=0.3`, when `run_arms` runs, then it raises `NoBaseline` within about a second, the reason names the bound (`did not return within 0.3s`), and nothing was written | `tests/test_arm_check.py`. **Red at `a340221b`**: two arms refused after 1.2 s, no exception. Red again with the baseline's `timeout` replaced by `None` (#641's round 2 found exactly this unpinned in the sibling) |
| S5 · a command that cannot be spawned at the baseline | Given `--tests` naming a command that does not exist, then `no baseline` with the `OSError` text, exit 2, nothing written | `tests/test_arm_check.py`. **Red at `a340221b`**: two arms in the no-verdict list, exit 0 |
| S6 · a green baseline changes no verdict and costs one run | Given `two_arms`, when `run_arms` runs, then the verdicts are `[('host == "example.com"', True), ("flag", False)]` as today, `refused == []`, and `subprocess.run` was called exactly five times (one baseline, four pairs), the first before any write | `test_a_watched_arm_is_killed_and_an_unwatched_one_survives` unchanged and green; a new counting case. **Red** with the baseline deleted (four calls) and with it placed after the first write |
| S7 · report-only for survivors stands | `test_the_checker_is_report_only_and_exits_zero_over_the_real_module` unchanged and green: a run with a survivor still exits 0 | that case, executed |
| S8 · every sentence a person reads says what the command now does | `--help` names the run against the unmutated module under the bound and still carries the two phrases already pinned; the SKILL section's closing paragraph states the baseline and the exit beside the survivor sentence; `bin/arm-check`'s header lists the run and says exit 0 is for survivors and 2 for a run that measured nothing | the help case extended; the SKILL and wrapper text read in review (no document is pinned by substring — `seal/releases/0.15.1.md` N2's note says why) |
| S9 · the cache under a relative prefix is cleared where the cases read it | Given a module under `tmp_path`, a directory `other/` that is not the process's cwd, a relative `PYTHONPYCACHEPREFIX` in the environment, and a `.pyc` planted at `other/<prefix>/<module's absolute dir without its leading separator>/<stem>.<tag>.pyc` — the path `cache_from_source` gives for that module when imported from `other/` — when `clear_bytecode_cache(path, cwd="other")` runs, then it removes that file and returns its path; and when `run_arms(..., cwd="other")` runs with the `SEES_CACHE`-style probe looking under that mirror, no arm runs while the file exists. Given an absolute prefix instead, the same, with `cwd` irrelevant | `tests/test_arm_check.py`, parametrised over a relative and an absolute prefix. **Red at `a340221b`** for the relative parameter: the file is left in place and `removed == []`. The absolute parameter is green today and pins what the relative one joins |
| S10 · `arm_check.py` still loads on the floor and below, and the module runs on CI's two grammar legs | `tests/test_a_script_says_which_interpreter_it_needs.py` and `tests/test_release_hygiene.py` green; `arm-check-grammar (3.13)` and `(3.14)` green on the pull request | executed narrow runs by the build; the two CI legs by the pull request |
| S11 · `mutation-check` stays green on the merged tree | When #641's branch and this one are both on `release/v0.17.0`, `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` is green: `clear_bytecode_cache`'s new parameter defaults to today's behaviour, so an unchanged caller sees no change | **verifiable only on the merged tree.** Who answers it: the orchestrator of whichever branch lands second, with that module's narrow run. Recorded `unverified` in this item's `overview.md` until then |

## Data & interfaces

- `arm_check.py#NoBaseline(Exception)` — new; carries `reason: str` and
  `output: str`. Raised from `run_arms` before any write. The one new name
  the module exports.
- `arm_check.py#run_arms` — signature unchanged. New behaviour: one
  `subprocess.run` of `tests` before the loop, in `cwd`, with `env`, under
  `timeout`, after `clear_bytecode_cache(path, cwd=cwd)`. Every
  `clear_bytecode_cache` call in the function passes `cwd=cwd`.
- `arm_check.py#clear_bytecode_cache(path, cwd=None)` — one keyword
  parameter added, default keeps today's behaviour. Return type unchanged.
- `arm_check.py#main` — catches `NoBaseline`, prints the verdict line and
  the output, returns 2. Exit 0 for every measured run stays, survivor or
  not.
- CLI flags unchanged. Exit codes: 0 measured (as today), 2 refused before
  measuring — the `--timeout` guard's code today, now also `no baseline`.
- Ledger anchors that drift: M6's three rows. New rows go in
  `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md`.
- Files #641 also edits (M7): `tests/test_arm_check.py`,
  `skills/verify/SKILL.md`, `seal/releases/0.9.5.md`. The merge resolves
  these hunk by hunk (`CLAUDE.md` §*When a ledger file conflicts*).

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. Its head lists the
judgments the tree answered (J1–J12), so nobody reopens them.

Framed 2026-10-01 by framer, before the build.
