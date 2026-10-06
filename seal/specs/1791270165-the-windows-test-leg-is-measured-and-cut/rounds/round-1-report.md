# Round 1 report — the Windows test leg is measured and cut (#841)

Reviewer: warden on Opus 5.5. Target `aacad4dd`, range `a9d7b0e5..aacad4dd`
(the branch's own; `origin/release/v0.20.0` has since moved to `275a7ce0`
and is not merged in). Spec compliance first, then quality. This is a first
round, so no earlier round's coordinates were carried; every verdict below
is this round's own.

## Summary

The frame's premise (a few heavy cases) did not hold, and the build recorded
that rather than hiding it. The shards carry the cut, and the CI runs bear
the build's figures out: I read each run's job times and pytest summaries
against the phase records, and every one matches. The budget follows Q6 (a)
to the number. The 4a sampler and the 4b cuts keep every assertion their
cases made.

One thing blocks the pull request today. The `hygiene` workflow has been red
at `98b817ad`, `d6587217` and `aacad4dd`, and no record of the work item
mentions it. Two smaller findings are about the budget: how far the ceiling
can be trusted on a busy local machine, and one template build that lands in
a case's measured call.

## Findings

### 🔴 1 — the `hygiene` workflow is red on this branch's own removal

*Executed* (CI logs read, and the check re-run here). `hygiene` concluded
`failure` on runs 37465328957 (`98b817ad`), 37469595060 (`d6587217`) and
37473088866 (`aacad4dd`). The failing step is *wording this branch removed
is not still standing elsewhere*. Phase 4b moved the pipe case's relocation
under a spaced directory into `a_sealed_run`, and with it deleted the
two-line comment that explained `shutil.move`'s rename. The same comment
still stands in `test_a_run_with_no_session_says_so_and_names_the_hand_command`
at `tests/test_the_seal_is_taken_once_by_the_sealer.py:2797-2798`, and
`survivor_check.py` reports it as wording the range removed that still
stands.

Re-run in a clone at `aacad4dd`, `survivor_check.py --range
a9d7b0e5...aacad4dd` exits 1 with the same two places. So this is the
branch's own range and not the moved base. The pull request cannot pass its
checks until this is answered. `overview.md` and the phase records say
nothing about it.

The comment is still true where it stands, because the no-session case still
moves its fixture with `shutil.move`. So the remedy is the one the checker
names: a row in this work item's `survivors.md`. The fenced file below was
run in the clone. With `--exempt` it exits 0 (`every survivor is excused by
a row above (2)`), and `bin/evidence-check --strict .` still exits 0 with
it in place.

### 🟡 2 — the 90 s ceiling binds `bin/test` with a smaller margin than the record measured local load to need

*Read*, with figures from the records and the issue. `CASE_CEILING_S`
(`tests/conftest.py:842`) is 1.5 times the slowest Windows call, 55.77 s,
rounded up to 90. The spec has it bind `bin/test` too, and so the sealer's
broad gate on a laptop. There the slowest case after the twins cut is
`test_no_shape_the_base_stops_reads_silent` at 38.30 s (the issue's local
table under `-n auto`), which leaves a margin of 2.35 times. The build's own
records measured local swings larger than that:

- `phases/phase-4.md` §*Timing* says that on the second smith's machine,
  running other sessions' suites, "one figure can move by a factor of four
  from one run to the next".
- `phases/phase-5.md` §*The ceiling also binds `bin/test`* records one
  sealer case at 32.6 s locally that ran in 12 s on Windows.

Running parallel chains on one machine is how this repository's runs are
normally driven. A broad-gate run under that load can therefore fail a case
that passes alone. The gate then reruns the failing file at the base, where
it passes, and reads the failure as the branch's own. The result is a false
refusal at the one broad run. The spec chose *block more* as the failure
direction. But Q6's 1.5 margin was derived from runner swing in CI, and
`phases/phase-5.md` §*What this says about the rule* notes that the rule
holds only while it is re-applied to the slowest run measured. No local run
was among the runs measured.

Q6 is a person's row and still reads ⬜, so the margin is the repository
owner's to set. Fix or justify. The fence below is one fix that keeps CI and
the gate reading 90 unless someone sets the variable on purpose. The other
fix is the owner answering Q6 for the local half.

### 🟡 3 — the stopped-run template is built inside a case's call, so `--durations` and the ceiling charge the build to whichever case asks first

*Executed* (CI durations read). `_stopped_runs`
(`tests/test_a_fix_of_a_fix_is_counted.py:500`) returns a closure, and the
template is built when a case calls `a_stopped_run()` in its body, which is
the call phase. The Windows tables show the effect. In group 1 of run
37469595104,
`test_a_reframed_record_is_written_and_starts_the_count_at_no[True]` takes
17.31 s and `test_a_record_after_an_unreframed_second_is_refused` takes
15.60 s of call, while the same cases' own steps cost a few seconds once the
template exists. Run 37465328899 shows the same pattern at 15.03 s and
7.49 s.

This item made `--durations` the reading surface and had the ceiling name
the case. Here both name the wrong case, and a later cut, or #826 reading
these figures, would chase two cases whose own work is small. The sibling
`_named_and_fixed_once` builds in setup, and its build shows up honestly as
`6.63s setup` in the same table. It also explains why phase 4b's
`if touched not in built:` → `if True:` mutation SURVIVED: the closure's
cache is invisible to every case. The fence below builds both templates as
setup-time fixtures and picks one from the case's own `touched` parameter,
so the build is charged to setup and the cache goes away.

### ⬜ 4 — a docstring still names the first base

`tests/test_a_slow_case_names_itself.py:40` says
`test_the_ceiling_is_the_one_q6_set` is "1.5 times 55.13 s". f1ea5d6c
re-based the constant's comment on 55.77 s (run 37469595104), and the value
is unchanged. The docstring should name 55.77 s to match the comment it
pins.

### ⬜ 5 — `test.yml`'s comment says nothing is shared between tests

`.github/workflows/test.yml:105` still reads "Nothing is shared between
tests -- each builds its own repository under `tmp_path`". `a_sealed_run`
now hands one repository to six cases. That is safe, because under xdist a
module fixture lives in one worker and those cases only read. But the
sentence that justifies running cases in parallel is now false as written. A
clause saying that shared fixtures are read-only and per worker would keep
it true.

### ⬜ 6 — `a_sealed_run`'s docstring states the serial saving

`tests/test_the_seal_is_taken_once_by_the_sealer.py:970` says "what left is
five identical runs". Under `-n auto` the module fixture is built once per
worker that draws one of the six cases. The Windows group 4 table shows the
build as `22.70s setup`, and each worker that draws a case pays it again.
`phases/phase-4.md` states the xdist caveat. The docstring does not.

### ⬜ 7 — CONTRIBUTING's refresh recipe for `.test_durations` cannot be followed as written

`CONTRIBUTING.md:184` says to "run the Windows leg once unsharded with
`--store-durations`, upload the file as an artifact". The workflow has no
switch for an unsharded store run, so a contributor has to edit `test.yml`.
The upload needs `include-hidden-files: true`, because the file name starts
with a dot and current `upload-artifact` skips such files by default. Phase
3 needed that flag (`overview.md` Not verified), and the step that had it,
43326715's, was removed by 340dc6fa. `phases/phase-3.md:132` names that
commit. CONTRIBUTING does not. A stale file only unbalances the shards, so
nothing ships broken, but the paragraph should name the commit whose step to
restore, or carry the step itself.

### ⬜ 8 — the ceiling sees only the call phase, and 4b moved cost into setup

`pytest_runtest_makereport` (`tests/conftest.py:860`) returns for every
report but `call`. The spec says call, so this matches the spec. Still, 4b's
three cuts each moved a prefix into a session or module fixture's setup. The
largest is `a_sealed_run`'s `22.70s setup` in Windows group 4, and a fixture
that grows past 90 s will never be named. The changelog's sentence says
"whose call runs longer", so it is accurate. I am recording this as a known
limit of the ceiling, not a defect.

### ⬜ 9 — a phase 5 sentence calls an earlier run "the last run"

`phases/phase-5.md:51` says "the highest call on macOS and ubuntu in the
last run is 18.76 s and 13.90 s". Those are run 37465328899's figures. The
confirming run 37469595104, the last one, reads 21.33 s on macOS and
24.13 s on ubuntu (logs read). The conclusion still holds, since the
ceiling binds on Windows first. This is a correction to the record, not to
the tool.

### ⬜ 10 — `overview.md`'s *What the next phase needs* is from before phase 3

`overview.md:24` still says the draft pull request's run "is the
measurement phase 3 starts from". Phases 3 and 5 are closed, and the table
above that paragraph says so. This is a correction to the record.

## What was confirmed

- **Q6 (a) is applied to the number.** I read every figure in the
  `CASE_CEILING_S` comment and the `timeout` comment from the logs of runs
  37457228586, 37458654434, 37465328899 and 37469595104, and each matches:
  - Windows' slowest call: 55.13, 52.49, 33.70 (with
    `test_no_shape_the_base_stops_reads_silent` at 29.91) and 55.77 s.
  - Job wall times: ubuntu 6 m 40 s, 7 m 58 s, 5 m 40 s and 9 m 03 s;
    macOS 19 m 52 s, 16 m 27 s, 17 m 38 s and 20 m 52 s; Windows group 3
    10 m 03 s and 10 m 34 s.
  - 1.5 times each base, rounded up: 83.7 s to 90; 13.6 min to 15; 31.3
    min to 35; 15.9 min to 20.
- **S4 holds.** The four shards of 37465328899 sum to 12,838 passed and 208
  skipped (13,046), which equals ubuntu's total at the same SHA. That is
  13,042 plus the four cases `98b817ad`'s range added. In 37469595104 they
  sum to 13,051.
- **The 4a sample keeps S5's contract.** `_sample`'s cover is asserted by
  `test_the_sample_covers_every_placement_and_every_verb`, which reads
  placements off the tuples rather than through the sampler's helper, so a
  dropped axis cannot hide on both sides. The per-verb two-sided pick is
  there. What left, per verb and per placement, is named in
  `phases/phase-4.md`. The red against `94d7b2e0`'s reading is the smith's
  `executed` claim, and I did not re-run it.
- **The 4b cuts keep every assertion.** I read the six `a_sealed_run`
  cases: none writes to the shared tree (one runs `git status`). Their
  environment is safe because `sealed_values` hands every script
  `env_without_a_pull_request()`, and the suite's empty `GIT_TEMPLATE_DIR`
  means no hook in the fixture reads the ambient variables that the
  module-scoped build sees. The fix-of-a-fix templates build the same
  prefix in the same order, and the prefix's own assertions (`code != 2`,
  round 3 reads `second`) still run, once, at the build.
- **Nested pytest.** The ceiling reaches a nested run only where a case
  loads this repository's `conftest.py` into it. The only such case is the
  deliberate one in `test_a_slow_case_names_itself.py`: the fixture
  repositories of the sealer and gate modules carry their own one-file
  suites and no copy of the conftest, and no case runs pytest in-process.
  An outer case's call includes its nested runs, and the sealer cases peak
  at about 17 s on Windows. Under xdist the hook still fails the case with
  the pinned sentence, and junit carries it as the failure message (probe
  below).

## Regression tests to plant

None owed by a 🔴. For 🟡 3, the fix leaves the cases' assertions unchanged.
The existing `[True]` assertion that only the touched copy carries
`return 1000` already pins which template a case gets
(`tests/test_a_fix_of_a_fix_is_counted.py`).

## Facts for the evidence ledger

- The `hygiene` survivor check at `aacad4dd` over `a9d7b0e5...aacad4dd`
  reports the two comment lines at
  `tests/test_the_seal_is_taken_once_by_the_sealer.py:2797-2798`. Executed
  2026-10-06. This belongs in the fragment only if 🔴 1's fix adds a
  `survivors.md`, which then carries it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The `hygiene` survivor check is red on the branch's own range: 4b removed a comment that still stands beside the move it explains | `tests/test_the_seal_is_taken_once_by_the_sealer.py:2797` | open | executed: hygiene runs 37465328957, 37469595060 and 37473088866 failed on it; `survivor_check.py --range a9d7b0e5...aacad4dd` exits 1 in a clone at `aacad4dd`, and exits 0 with the fenced `survivors.md` |
| 🟡 2 | The 90 s ceiling binds `bin/test` with a 2.35-times margin over the slowest local case, while the records measured local swings up to four times | `tests/conftest.py:842` | open | read: issue table 38.30 s; `phases/phase-4.md` §*Timing*; `phases/phase-5.md` 32.6 s against 12 s; Q6 is a person's row and still ⬜ |
| 🟡 3 | The stopped-run template is built inside the first asking case's call, so `--durations` and the ceiling charge the build to that case | `tests/test_a_fix_of_a_fix_is_counted.py:511` | open | executed (CI logs read): 17.31 s and 15.60 s of call in 37469595104 group 1, 15.03 s and 7.49 s in 37465328899; the sibling `_named_and_fixed_once` shows `6.63s setup` |
| ⬜ 4 | The docstring names 55.13 s where the constant's comment now names 55.77 s | `tests/test_a_slow_case_names_itself.py:40` | open | read; f1ea5d6c re-based the comment |
| ⬜ 5 | "Nothing is shared between tests" is false since `a_sealed_run` | `.github/workflows/test.yml:105` | open | read |
| ⬜ 6 | `a_sealed_run`'s docstring states the serial saving, not the per-worker one | `tests/test_the_seal_is_taken_once_by_the_sealer.py:970` | open | read; Windows group 4 `22.70s setup` |
| ⬜ 7 | The refresh recipe has no switch to use and omits the hidden-file upload flag | `CONTRIBUTING.md:184` | open | read; 43326715's step was removed by 340dc6fa |
| ⬜ 8 | The ceiling sees only `call`, and 4b moved prefixes into setup | `tests/conftest.py:860` | open | read; matches the spec; a limit to name, not a defect |
| ⬜ 9 | Phase 5 calls run 37465328899's figures "the last run" | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/phases/phase-5.md:51` | open | executed (logs read): 37469595104 reads 21.33 s on macOS and 24.13 s on ubuntu; a correction to the record |
| ⬜ 10 | *What the next phase needs* predates phase 3 | `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/overview.md:24` | open | read; a correction to the record |
| 🟢 | The ceiling and the three timeouts are Q6 (a) applied to the slowest of the four runs | `tests/conftest.py:842`, `.github/workflows/test.yml:61` | confirmed | executed (logs read): every base figure in both comments matches the job times and `--durations` lines |
| 🟢 | S4: the shards make the whole suite | `.github/workflows/test.yml:75` | confirmed | executed (logs read): 12,838 + 208 = 13,046, ubuntu's at `98b817ad`; 13,051 at `d6587217` |
| 🟢 | The 4a sample keeps S5's contract, and the 4b cuts keep every assertion | `tests/test_guard_resolves_the_tree_it_judges.py#_sample`, `tests/test_the_seal_is_taken_once_by_the_sealer.py#a_sealed_run` | confirmed | read; the red against `94d7b2e0` is the smith's executed claim and was not re-run |
| 🟢 | The ceiling reaches nested pytest only in its own module, and fails a case correctly under xdist | `tests/conftest.py:854` | confirmed | read (fixture repositories carry no copy of the conftest) and executed (xdist probe) |

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

Every leaving was removed: the clone, the scratch suite and the downloaded
logs.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The 4b cuts' yield on the Windows leg, which no run has isolated from runner swing | `overview.md` Not verified, already recorded by the build | the repository owner, if the figure is wanted; #826 reads the guard figures |

## Paste-ready fixes

### 🔴 1

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

Saved as `seal/specs/1791270165-the-windows-test-leg-is-measured-and-cut/survivors.md`.

### 🟡 2

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

In `CONTRIBUTING.md`, after "Make it cheaper, split it, or sample what it
walks.":

```markdown
On a machine running other suites at the same time, a case can pass that
ceiling on load alone; `SPECSEAL_CASE_CEILING_S=<seconds>` raises it for one
run, and CI never sets it.
```

### 🟡 3

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

Needs a fix: yes — 🔴 1 (the hygiene survivor check is red on the branch's
own range); 🟡 2 and 🟡 3 are fix or justify
Loses a record or crashes: no

## Proof

Files opened: `spec.md`, `plan.md`, `questions.md`, `overview.md`,
`routing.md`, `handoff.md`, `changelog.md`, `phases/phase-4.md`,
`phases/phase-5.md`, and the S4 section of `phases/phase-3.md` and the
failure section of `phases/phase-1.md` (all under this work item);
`.github/workflows/test.yml`; `.github/scripts/run_tests.py` (the diff);
`CONTRIBUTING.md` (the diff); `tests/conftest.py`;
`tests/test_a_slow_case_names_itself.py`;
`tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`;
`tests/test_a_fix_of_a_fix_is_counted.py`;
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the six shared-run
cases, `sealed_values`, `run_gate`, `settled_item`, the generator helpers
and the autouse fixtures); `tests/test_guard_resolves_the_tree_it_judges.py`
(the diff); the ledger fragment
`seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md`; and an
earlier work item's `survivors.md` from history, for the format.
