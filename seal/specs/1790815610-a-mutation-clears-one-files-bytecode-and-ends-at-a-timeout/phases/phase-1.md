# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 09ba83c3 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

`plan.md`'s phase 1, in the order its six steps give: `mutation_check.py`
with the replace, both bytecode halves, the restore and the verdicts, bounded
for now by a plain `subprocess.run`; the wrapper pair; S1, S2, S3, S4, S7 and
S8 seen red before the change that turns each green; S1's second red with the
glob swapped for `cache_from_source`; and the xdist measurement for
`questions.md` Q1. Before any of it, smith.md phase 1: say whether the frame
holds.

## What this phase found

**The frame holds, except for one coordinate it builds on.** Spec M7 says
no shipped script imports a sibling and that `from arm_check import ...`
resolves because a script's own directory is first on `sys.path`. The second
half is true only while the script is run by its path with `PYTHONSAFEPATH`
unset; a case that loads the script by an `importlib` spec meets neither
condition, and the plan's own *How the sibling import resolves* paragraph
already had to work around that. Nine shipped scripts reach another file,
and every one does it by path through `importlib.util.spec_from_file_location`
(`survivor_check.py`, `chain_check.py`, `settle.py`, `round_record.py`,
`fold_check.py`, `payload_meter.py`, `evidence_check.py`, `broad_gate.py`,
`correction_check.py`). So `mutation_check.py` loads `arm_check.py` the same
way, registered in `sys.modules` first because `arm_check`'s dataclasses
need it, and the two functions are still the ledgered originals rather than
a copy. The test module needs no path set-up as a result.

**A mutated run's cases inherit `PYTHONDONTWRITEBYTECODE=1`, and a case that
plants a cache by import then plants nothing.** Found while mutating this
command with itself. The first sweep reported S1 red under every mutation,
and two of those reds were counterfeit: the outer run set the variable, the
pytest it started inherited it, and S1's import-made plant wrote no `.pyc`,
so the case failed on its own precondition whatever had been mutated. The
class, enumerated over every module under `tests/` naming `__pycache__`, has
three members: this module's S1, and two cases in `tests/test_arm_check.py`
(`test_a_stale_bytecode_cache_cannot_decide_an_arms_verdict`,
`test_no_arm_runs_while_cached_bytecode_for_the_module_exists`). Both of
those were already red under `arm-check` mutating `arm_check.py`, since
`run_arms` sets the same variable, so the class predates this branch. The new
command adds a second way in. Fixed in all three: S1 plants with
`py_compile` and takes the variable out of its own environment before it
asks whether the command set it; the two `arm-check` cases switch
`sys.dont_write_bytecode` off for the plant alone, so their plants are still
made by a real import. Both were shown red under the variable with the edit
stashed, and green with it. `seal/releases/0.9.5.md`'s row anchored on
`test_no_arm_runs_while_cached_bytecode_for_the_module_exists` drifts with
that edit and is re-read in phase 4, with the rest of the ledger work.

**S2 is deterministic rather than timing-dependent.** The spec's form, an
import of the unmutated module just before the mutation, makes the stale
read happen only when both writes land in one mtime second. The case plants
an unchecked-hash `.pyc` instead, which CPython loads without consulting the
source. Without the removal, the cases run the cached `VALUE = 15` on every
run, and S2 reads SURVIVED. This diverges from the spec's wording and keeps
its claim; `overview.md` records it.

**The formatter hook strips an import that nothing uses yet.** The first
write of the test module imported `py_compile` ahead of the case that used
it, and the hook removed the line. So S2's first red was a `NameError` and
not the stale read. It was retaken: green with the removal, red without it.
A later phase that writes an import before its user meets the same thing.

**Q3, the shape chosen.** `mutation-check <path> --replace OLD NEW --tests
"<command>" [--timeout S] [--cwd DIR]`, as the spec suggested. The verdict
is the first line, `<word>: <detail> (<elapsed>s)`, and the words are `red`
(exit 0), `SURVIVED` (1), `timed out`, `could not start`, `refused` and `not
restored` (all 2). Four refusals were added beyond the spec's count rule,
because each one would otherwise print a verdict nobody measured: an empty
OLD, a NEW identical to OLD (SURVIVED every time), a file that is not UTF-8
text (a lenient decode would restore different bytes), and a `--tests` that
names no command.

**The bytecode removal is not gated on the file's extension.** It is
`arm_check.clear_bytecode_cache` unchanged, which removes `<stem>.*.pyc`
beside any file. For `notes.md` beside `notes.py`, that removes a valid cache
and costs one recompile. Gating on `.py` would instead miss an extensionless
script loaded through `importlib`, which does get a cache, and a missed cache
is a stale read rather than a cost.

**Q1, measured.** Apple M3 Pro, 12 cores, macOS 26.5, the worktree's `.venv`
at 3.13.9, 2026-10-01. One warm-up run, then three alternating runs of each
form.

| Module and cases | `-n auto` (bin/test's default) | `-p no:xdist` |
|---|---|---|
| `tests/test_the_handoff_before_round_one.py -k smith`, 2 cases at 0.02 s | 0.81, 0.74, 0.84 s; mean 0.80 s | 0.18, 0.17, 0.18 s; mean 0.18 s |
| `tests/test_arm_check.py -k "cache or restore or never_returns"`, 7 cases at 1.6 s | 1.96, 1.89, 2.02 s; mean 1.96 s | 1.66, 1.73, 2.12 s; mean 1.84 s |

Worker start-up is about 0.6 s per run. On a handful of fast cases, that is
most of the run, and on a handful that already takes 1.6 s the parallelism
pays it back. So the answer is *faster*. Phase 3's example carries `-p
no:xdist`, and the SKILL section says it is for a handful of cases.

**Mutated, each with the command itself, every one red.** The bytecode step
four ways: the removal before the run, the variable, the removal after the
restore, and the glob replaced by `cache_from_source` (the last red only on
the planted foreign tag, which is spec M4 pinned). Then thirteen units: the
empty-OLD, identical and count refusals, the UTF-8 refusal, the
`NotRestored` mapping, the exit-code rule for red, the `OSError` arm, the
negative-bound and empty-command refusals, the exit table, the output echo,
the restore call and the replacement itself. The wrapper's case was red with
the executable bit removed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
