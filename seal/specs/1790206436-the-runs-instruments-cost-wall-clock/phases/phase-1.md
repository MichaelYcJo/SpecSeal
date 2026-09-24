# 1790206436-the-runs-instruments-cost-wall-clock — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | adabb0f8 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

The runner is parallel by default (#337): `.github/scripts/run_tests.py`
installs `pytest-xdist` on both build strategies and on an adopted `.venv`
lacking it; `main` adds `-n auto` unless the caller passed `-n…`,
`--numprocesses…`, `-p no:xdist` or `--pdb`; a failed install is a sentence
plus a serial run. Invert `test_it_does_not_pass_n_auto` and see it red
first. Remove the serial figures from `bin/test`, the runner docstring,
`CONTRIBUTING.md` §*Running the checks* and the test module's message;
`docs/release-checklist.md` §3's suite line becomes `bin/test -q`. Verified
by the module alone (`bin/test tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q`),
one real cold build in a scratch clone driven from Python and deleted after,
and `ruff` over the edited files. M2's `FAILED`-line probe and W1's flag
candidates are this phase's measurements.

## What this phase found

**Red first, at the frame commit `421b0c0e`.** The new module copied into a
scratch clone at that commit and run with the main checkout's interpreter:
`8 failed, 67 passed` — the inverted pin, both build-strategy cases (A1),
both adopted-environment cases (A2), the failed-install case (A3), the
narrow-form tail (A5) and the absent-figure case (A6). A4 is green at the
base by construction (the old runner added nothing either) and was shown red
by mutation instead: `caller_decided` returning `False` turns all eight
spellings red.

**Mutation, one unit at a time, restored from kept bytes** (each: `bin/test
<module> -q -p no:cacheprovider`, then `tests/__pycache__` cleared):

| Mutation | Red |
|---|---|
| drop the `-n auto` append | 4 — the inverted pin, A5, both A2 cases |
| `caller_decided` always `False` | 8 — every A4 spelling |
| pass `-n auto` after a failed install | 1 — A3 |
| `PACKAGES` without `pytest-xdist` | 2 — both A1 build cases |
| `add_xdist` never repairs (`has_xdist` short-circuited) | 3 — both A2 cases and A3 |

**The cold build, in a scratch clone at `adabb0f8`, driven from Python and
deleted after.** `uv` on PATH, so the `uv` strategy: the build printed
`+ pytest-xdist==3.8.0`, `.venv/lib/python3.13/site-packages/xdist` was
there afterwards, and the module's output opened with `bringing up
nodes...`. Cold call 1.6 s wall, warm call 0.9 s, module `75 passed in
0.81s` / `0.77s`. The runner prints the interpreter and not the command, so
`-n auto` was read off xdist's own first line and the marker directory
rather than off a printed command. 10 logical CPUs, macOS (Darwin 25.6.0),
2026-09-24. The worktree's own `.venv` was built by the same code path on its
first call: 2 s wall including the module.

**M2 — the gate's parsers keep their input under `-n auto`.** A probe module
with one failing and one passing case, written into `tests/`, run through
`bin/test <probe> -q` from Python and unlinked in `finally`: exit 1, stdout
carries `FAILED tests/test_tmp_fails_under_xdist.py::test_tmp_one_fails -
assert 1 == 2` and `1 failed, 1 passed in 0.55s`. Both the `FAILED
path::name` short-summary line `failing_files` reads and the counts line
`suite_counts` reads are present. The default the frame assumed holds; no
`questions.md` row for the owner.

**W1 — which flags belong on the withholding list.** Each candidate run once
through `bin/test <module> -q <flag>` against the built environment, so
`-n auto` was beside it: `--sw` exit 0 (75 passed), `-s` exit 0, `-x` exit
0, `--trace` exit 0, `--lf -x` exit 0 on a clean cache (one earlier run
under a stale `lastfailed` entry exited 5 with no summary line, re-run exit
0; observed and not explained). None is refused, so none joins the list.
`--pdb` is on the list and the reason the frame gave for it was half right:
pytest-xdist 3.8.0's `pytest_cmdline_main` raises its `UsageError` (`--pdb NAME NOT IN TREE
is incompatible with distributing tests`, exit 4) for `-n 2 --pdb`, and for
`-n auto --pdb` it sets `numprocesses = 0` and `dist = "no"` itself — a
failing probe under `-n auto --pdb` reached the `(Pdb)` prompt in-process
and exited 2 on the debugger quitting. Withholding the flag and passing it
reach the same serial run; the runner withholds because it is the shorter
route and the arguments then pass through exactly as typed. `caller_decided`'s
docstring and the A4 case carry the measurement.

**One existing pin moved with the default.** `test_no_arguments_runs_the_whole_suite`
asserted the command's *last* element is `tests`; with `-n auto` appended it
is `auto`. The case now asserts `tests` is the first argument after `pytest`,
which is what it was pinning.

**Where the frame's spelling was left to the phase (W2, this phase's
part):** the install-step function is `add_xdist(venv)`, called in `main`
directly after `ensure` returned; the marker is `site_packages(venv)` — one
`Lib/site-packages` on Windows, `sorted((venv/"lib").glob("python*/site-packages"))`
elsewhere — with `has_xdist` asking for an `xdist` directory under any of
them; `PACKAGES = ("pytest", "pytest-xdist")` is the one place both build
strategies read the install list from. `fake_venv` in the test module takes
`xdist=True` and grows the marker at `lib/python<FLOOR>/site-packages/xdist`
(`Lib/site-packages/xdist` on `nt`); the glob answers `python3.13` and
`python3.12` alike, which the cold build's 3.13 environment confirmed.

**The suite's own wall clock is not measured here.** The spawn prompt says
the whole suite is not this segment's to run and the sealer takes it once;
M1's first reading (the suite alone, cold, in the scratch clone) is
therefore not taken, and the second (the sealer's run over this branch) is
the orchestrator's to read off the sealer's report. The before figure the
changelog fragment carries is the ticket's and the 0.15.0 run's; the after
figure is the 0.15.0 preparation's hand run of the same flags on this
machine, which is the configuration this phase makes the default.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_it_does_not_pass_n_auto`, the pin that held the serial default in place | inverted in place as `test_the_whole_suite_runs_in_parallel_by_default`, same module; its docstring says what the old pin held |
| the serial figure *about five minutes* from `bin/test`, the runner's docstring and `CONTRIBUTING.md` §*Running the checks*; *five-minute suite* from three test docstrings and one failure message | the measured before-and-after with date and machine in `seal/specs/1790206436-the-runs-instruments-cost-wall-clock/changelog.md`; `test_no_loaded_document_states_the_serial_figure` keeps the three documents clear |
| the runner's comment `No -n auto: …` naming the workaround (*add xdist and pass it yourself*) | the comment above the same command, which now says why the flag used to be withheld |
| `docs/release-checklist.md` §3's `uv run --quiet --with pytest --with pytest-xdist pytest tests/ -q -n auto` | `bin/test -q` on the same line — the runner is the one spelling of the run |
