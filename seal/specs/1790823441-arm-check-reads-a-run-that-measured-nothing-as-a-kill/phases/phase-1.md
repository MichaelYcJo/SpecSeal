# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a3da8e87 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The baseline. `NoBaseline`; one run of `--tests` in `run_arms` against the
module as it is, before any write, under `timeout`, after a cache clear;
`main` printing `no baseline: <cause> … Nothing was written and no arm was
measured.` and the command's output, exit 2. Cases S1 to S3 (exit 5, 4, 1
and an import-shaped failure), S4 (the bound), S5 (cannot spawn), S6 (five
calls, the first before any write), each seen red against `a340221b`. The
cases spec M5 names rewritten, every assertion kept. The texts of spec
§Scope 3 in the same commit: `run_arms`' docstring, the `--timeout` help
with its case extended, `bin/arm-check`'s header, the SKILL section's
closing paragraph. S7 untouched and green. The spawn added: read #641's
baseline handling first and do not repeat its round findings (a read-only
target, the interrupt sentence, an unpinned baseline bound); Q2 measured.

## What this phase found

**The frame holds, with one aggregate wrong and one measurement that did not
yet exist.** Spec M5 and §Scope 5 say *five existing cases* and name six
functions. After the baseline landed exactly those six went red, seven items
with the parametrise, and nothing else in the module did. The list was right
and the count was not.

**The first run sits before the outer `try`, and that is what makes three of
#641's round findings unreachable here.** Inside it, a refusal would reach
the `finally` that restores the module, so *Nothing was written* would be a
sentence about a restore. A read-only target would then turn the refusal into
a `PermissionError` from that restore, which is the sibling's 🟡 9 shape. An
interrupt during the first run would leave through the same restore. Outside
it, a refusal and an interrupt both leave before the first write, with
nothing owed. A byte comparison cannot show this, because a restore writes
the same bytes, so S1, S4 and S5 set the module's mtime to 2001 and assert
it is unchanged. Mutation M3 (a restore before the raise) turns all four S1
items red on that assertion alone. No interrupt sentence was written: `main`
has no `KeyboardInterrupt` arm, and none is in scope.

**`text=True` came off the first run.** With it, `subprocess.run` decodes
strictly in the locale's encoding, so a suite printing a non-UTF-8 byte would
turn a refusal into a `UnicodeDecodeError` traceback. Without it, every
capture is bytes or `None` (`TimeoutExpired` carries `None` when nothing was
read, on POSIX), and `_text` decodes with replacement. The pairs keep
`text=True`; their output is never shown, and changing them is not this
defect.

**Two units the plan did not name got a case each, because a mutation left
them green.** Dropping `cwd=cwd` from the first run, and making the refusal
conditional on there being an arm (`plan.md` §Alternatives L), both survived
S1 to S6. `test_the_first_run_is_taken_where_the_pairs_are` runs a probe that
exists only under `cwd`. `test_the_first_run_is_taken_whatever_the_arms_are`
covers a module with no arms and an `--only` matching none. A third, the
timeout's partial output, is pinned by `test_a_first_run_that_timed_out_carries_what_it_printed`
through a `subprocess.run` that raises at once, because a real command's
output before a 0.3 s bound depends on how fast its interpreter starts.

**The two rewritten timeout cases wait 1.0 s a pair, not 0.3 s.** Their
command now has to pass against the unmutated module inside the same bound
before any pair is asked. `HANGS_ON_A_MUTATION` compares bytes with a copy
(Q5's default), runs with `-S`, and the case takes about 4 s against 1.2 s
before. 0.3 s is an interpreter start-up on a loaded Windows runner, and the
full suite runs this module on Windows.

**Q2:** `bin/test` propagates pytest's exit code. The documented wrapper form
with a `-k` that selects nothing printed `no baseline: exit 5. …`, then
pytest's `no tests ran in 0.71s`, exit 2, and `hooks/review-history-guard.py`'s
sha256 unchanged. **Q4:** the whole output, stdout then stderr, after the
verdict line; no line on a passing first run.

**How each case was seen red** (executed). S1 to S3, S5 and S6 against the
script at `a340221b`: `killed` beside both arms at exit 0 for the four S1
items, both arms in the no-verdict list for S5, four calls for S6. S4 and the
two cases above went red on `NoBaseline` not existing, and their right-reason
red is the mutation list. Nineteen mutations, one at a time, each restored
from bytes kept in the scratchpad with the sha256 compared and
`__pycache__` cleared beside the script and the cases:

| # | Mutation | Red |
|---|---|---|
| M1 | the first run's `timeout=timeout` removed | S4, after 33 s |
| M2 | a mutant of arm one written before the first run | S6, through `NoBaseline` |
| M2b | a mutant of the unwatched arm written before it | S6, on *the first run has to be against the module as it is* |
| M3 | a restore before the exit's raise | all four S1 items, on the mtime |
| M4 | the non-zero check disabled | the four S1 items and both no-arms items |
| M5 | the timeout's output dropped | the timeout-output case |
| M6 | strict decode | the timeout-output case |
| M7 | `_text`'s `None` guard removed | S4 (POSIX: a real timeout with nothing read carries `None`) |
| M8 | the `OSError` arm re-raises | S5 |
| M9 | `main` returns 0 on a refusal | the four S1 items and S5 |
| M10 | the output not echoed | the four S1 items |
| M11 / M11b | stderr / stdout dropped from the output | the import item / the three print items |
| M12 | the clear before the first run removed | the cache-observation case |
| M13 | `env=env` removed from the first run | the import item, on the `.pyc` pin |
| M14 | `cwd=cwd` removed from the first run | the cwd case |
| M15 | the refusal only when there is an arm | both no-arms items |
| M16 | `NoBaseline` keeps no output | the four S1 items and the timeout-output case |
| M17 | *Nothing was written…* removed from the line | the four S1 items and S5 |
| M18 / M19 | the bound's / `--tests`'s new help sentence removed | the help case |

M13's red depends on the caller's own environment not already setting
`PYTHONDONTWRITEBYTECODE`; with it set, the child inherits it either way and
the mutation is equivalent there.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `NO_VERDICT_COMMANDS`, the two `(label, command, timeout)` rows the report case was parametrised by | `NO_VERDICT_DOORS` and the case body: the hang is `hangs_on_a_mutation`, the spawn failure a `subprocess.run` that spawns a missing command from its second call |
| `text=True` on the first run (never shipped; removed inside this phase) | `_text`, which decodes with replacement |
