# 1791270165-the-windows-test-leg-is-measured-and-cut — review round 1

| Field | Value |
|---|---|
| Target SHA | aacad4dd899c466b8a5d33b446d35f014487b352 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #845 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `c84ac48ed82305b55efde9dfd13ed1aa5b904434..254130b0f490913b28066608e3bbd1d685eb664a`, 3 commits |
| Contract changes | a_stopped_run → round-1-report.md, round-1.md; test_a_call_over_the_ceiling_is_named_with_its_seconds → pytest only; test_a_call_at_or_under_the_ceiling_says_nothing → pytest only |
| New units | CASE_CEILING_DEFAULT_S (depth 1); CEILING_VARIABLE (depth 1); _stopped_untouched (depth 1); _stopped_touched (depth 1); ceiling_read_by_a_fresh_import (depth 1); test_the_variable_raises_the_ceiling_for_one_run_and_unset_is_ninety (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (the hygiene survivor check is red on the branch's own range); 🟡 2 and 🟡 3 are fix or justify |
| Loses a record or crashes | no |
<!-- New units: .github/workflows/test.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1 of the chain the owner chose (`routing.md`, answered again as `automation` on 2026-10-06). The reviewer was asked to judge spec compliance first against the frame as reframed for Q10 (b), whether the cuts of phases 4a and 4b keep every claim their cases made, and whether the budget is set as Q6 (a) says from the recorded runs, reading the CI logs where a claim rests on them; then quality, over `a9d7b0e5..aacad4dd`, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the 13 changed Python files, the budget, shard, pin, arm-check and release-check modules with six neighbouring hygiene modules (607 passed) and `bin/evidence-check --strict .` (exit 0). The orchestrator had watched only the `test` workflow's runs on the pull request and missed the red `hygiene` runs the reviewer found.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The `hygiene` survivor check is red on the branch's own range: 4b removed a comment that still stands beside the move it explains | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2797` | **fixed** `af688f2e` | fixed at af688f2e; executed: hygiene runs 37465328957, 37469595060 and 37473088866 failed on it; `survivor_check.py --range a9d7b0e5...aacad4dd` exits 1 in a clone at `aacad4dd`, and exits 0 with the fenced `survivors.md` |
| 🟡 2 | The 90 s ceiling binds `bin/test` with a 2.35-times margin over the slowest local case, while the records measured local swings up to four times | `tests/conftest.py:842` | **fixed** `af688f2e` | fixed at af688f2e; read: issue table 38.30 s; `phases/phase-4.md` §*Timing*; `phases/phase-5.md` 32.6 s against 12 s; Q6 is a person's row and still ⬜ |
| 🟡 3 | The stopped-run template is built inside the first asking case's call, so `--durations` and the ceiling charge the build to that case | `tests/test_a_fix_of_a_fix_is_counted.py:511` | **fixed** `af688f2e` | fixed at af688f2e; executed (CI logs read): 17.31 s and 15.60 s of call in 37469595104 group 1, 15.03 s and 7.49 s in 37465328899; the sibling `_named_and_fixed_once` shows `6.63s setup` |
| ⬜ 4 | The docstring names 55.13 s where the constant's comment now names 55.77 s | `tests/test_a_slow_case_names_itself.py:40` | **fixed** `af688f2e` | fixed at af688f2e; read; f1ea5d6c re-based the comment |
| ⬜ 5 | "Nothing is shared between tests" is false since `a_sealed_run` | `.github/workflows/test.yml:105` | **fixed** `af688f2e` | fixed at af688f2e; read |
| ⬜ 6 | `a_sealed_run`'s docstring states the serial saving, not the per-worker one | `tests/test_the_seal_is_taken_once_by_the_sealer.py:970` | **fixed** `af688f2e` | fixed at af688f2e; read; Windows group 4 `22.70s setup` |
| ⬜ 7 | The refresh recipe has no switch to use and omits the hidden-file upload flag | `CONTRIBUTING.md:184` | **fixed** `af688f2e` | fixed at af688f2e; read; 43326715's step was removed by 340dc6fa |
| ⬜ 8 | The ceiling sees only `call`, and 4b moved prefixes into setup | `tests/conftest.py:860` | answered | the call-only ceiling is what `spec.md` Data & interfaces says; af688f2e names it as a limit in `overview.md`, the changelog fragment and `CONTRIBUTING.md`; read; matches the spec; a limit to name, not a defect |
| ⬜ 9 | Phase 5 calls run 37465328899's figures "the last run" | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/phases/phase-5.md:51` | **fixed** `af688f2e` | fixed at af688f2e; executed (logs read): 37469595104 reads 21.33 s on macOS and 24.13 s on ubuntu; a correction to the record |
| ⬜ 10 | *What the next phase needs* predates phase 3 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/overview.md:24` | **fixed** `af688f2e` | fixed at af688f2e; read; a correction to the record |
| 🟢 | The ceiling and the three timeouts are Q6 (a) applied to the slowest of the four runs | `tests/conftest.py:842`, `.github/workflows/test.yml:61` | confirmed | executed (logs read): every base figure in both comments matches the job times and `--durations` lines |
| 🟢 | S4: the shards make the whole suite | `.github/workflows/test.yml:75` | confirmed | executed (logs read): 12,838 + 208 = 13,046, ubuntu's at `98b817ad`; 13,051 at `d6587217` |
| 🟢 | The 4a sample keeps S5's contract, and the 4b cuts keep every assertion | `tests/test_guard_resolves_the_tree_it_judges.py#_sample`, `tests/test_the_seal_is_taken_once_by_the_sealer.py#a_sealed_run` | confirmed | read; the red against `94d7b2e0` is the smith's executed claim and was not re-run |
| 🟢 | The ceiling reaches nested pytest only in its own module, and fails a case correctly under xdist | `tests/conftest.py:854` | confirmed | read (fixture repositories carry no copy of the conftest) and executed (xdist probe) |

## Paste-ready fixes

```markdown
# Survivors — the Windows test leg is measured and cut

`survivor-check --range a9d7b0e5...HEAD` reported two places still carrying
wording phase 4b removed from
`test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing`, whose own move
under a spaced directory went to `a_sealed_run`. Both stand, for the reason
in each row.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | The parent first, so the move is a rename on every platform. | `test_a_run_with_no_session_says_so_and_names_the_hand_command` still moves its fixture under a spaced directory with `shutil.move`, and the comment explains that move there; 4b removed only the pipe case's copy of the move, so the sentence is true where it stands |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | it `shutil.move` falls back to a copy and an `rmtree`, which Windows | the same comment's second line, beside the same move |
```
```python
# tests/conftest.py — the constant's line, and two sentences added to its
# comment above it:
#
# A run on a machine busier than the runners it was set from may raise it
# for that run alone. Phase 4 of work item 1791270165 measured a case at up
# to four times its figure on a laptop running other sessions' suites,
# which is past this constant's margin over the slowest local case
# (38.30 s). CI sets nothing, so CI and the gate read 90 unless a person
# sets the variable on purpose.
CASE_CEILING_S = int(os.environ.get("SPECSEAL_CASE_CEILING_S", "90"))
```
```markdown
On a machine running other suites at the same time, a case can pass that
ceiling on load alone; `SPECSEAL_CASE_CEILING_S=<seconds>` raises it for one
run, and CI never sets it.
```
```python
# tests/test_a_fix_of_a_fix_is_counted.py — replaces `_stopped_runs` and
# `a_stopped_run`.


@pytest.fixture(scope="session")
def _stopped_untouched(tmp_path_factory):
    """The stopped run, built once through `new` and `close` exactly as
    `stopped` drives them, and kept as a template (#841)."""
    d = tmp_path_factory.mktemp("fix-of-a-fix-stopped") / "repo"
    _build(d)
    stopped(d, False)
    return d


@pytest.fixture(scope="session")
def _stopped_touched(tmp_path_factory):
    """The same with a code commit inside the stop's range."""
    d = tmp_path_factory.mktemp("fix-of-a-fix-stopped-touched") / "repo"
    _build(d)
    stopped(d, True)
    return d


@pytest.fixture
def a_stopped_run(request, tmp_path):
    """A copy of the stopped run in this case's own directory: the touched
    one where the case is parametrized `touched=True`. The template is
    requested here, in setup, so its build is charged to setup and never
    to the call of whichever case asks first."""
    callspec = getattr(request.node, "callspec", None)
    touched = bool(callspec and callspec.params.get("touched"))
    template = request.getfixturevalue(
        "_stopped_touched" if touched else "_stopped_untouched"
    )
    d = tmp_path / "repo"
    shutil.copytree(template, d)
    return d


# and at the five call sites:
#   repo = a_stopped_run()         ->  repo = a_stopped_run
#   repo = a_stopped_run(touched)  ->  repo = a_stopped_run
```

## Executed probes

| What was run | Result |
|---|---|
| `gh run view` on runs 37457228586, 37458654434, 37465328899, 37469595104: job start and end times, pytest summaries, `--durations` lines | every figure the phase records and the two comments cite matches |
| `gh run view --log-failed` on hygiene runs 37465328957, 37469595060, 37473088866 | each fails on the survivor check, the same two lines |
| `skills/code-review/scripts/survivor_check.py --range a9d7b0e5...aacad4dd` in a `--no-local` clone at `aacad4dd` | exit 1, two places standing |
| the same with the fenced `survivors.md` and `--exempt`, then `bin/evidence-check --strict .` | exit 0 and exit 0; the file was deleted afterwards |
| `bin/test tests/test_a_slow_case_names_itself.py tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py -q` in the clone | `8 passed`, exit 0 |
| the ceiling hook loaded into a scratch two-case suite at a 0.3 s ceiling, run with `-n 2 --junitxml` | `1 failed, 1 passed`; the sentence printed, and junit's failure message is the sentence |
| the full suite (the broad gate) | not yet run, by anyone; it is the sealer's, once, after the rounds |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The 4b cuts' yield on the Windows leg, which no run has isolated from runner swing | `overview.md` Not verified, already recorded by the build | the repository owner, if the figure is wanted; #826 reads the guard figures |
