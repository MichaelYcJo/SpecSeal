# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d1921115 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

`plan.md`'s phase 2: the bound. The platform-chosen strategy, the POSIX
session and group kill, the `KeyboardInterrupt` path and the Windows verdict
text, with S5 and S6 seen red on phase 1's `subprocess.run` form (S5's
grandchild still alive) before they turn green, and `tests/test_arm_check.py`
unchanged by it.

## What this phase found

**S5's red on phase 1's form is #313's measurement, re-taken on the new
command.** With `subprocess.run(timeout=1)` the verdict arrived promptly and
the wrapper's child was still alive five seconds later. On POSIX `run`
waits rather than communicating after the kill, so the direct child's pipe
was not what held the run back; the child simply outlived it.

**Ending the group raises a second hang, one step later.** After the kill,
the output is collected, and the collection waits for every holder of the
pipe. A process that started a session of its own is outside the group, so
the kill does not reach it and it holds the pipe for as long as it runs.
That is the 32-minute shape again, moved past the bound. So the collection
is bounded too, `REAP_TIMEOUT` (5 s; NAME NOT IN TREE since round 1's fix pass, which moved the wait onto the process and removed it), after which the pipe is closed and the
process reaped. The GROUP verdict text was overclaiming that case (*nothing
it started outlives this line*), and now names the exception. A case pins
both halves, with the bound shortened to 0.5 s so it does not cost five
seconds. Mutated to an unbounded collection, it waits the escaped child's
30 s and goes red on the elapsed time.

**The interrupt is a `KeyboardInterrupt` here and nowhere else.** The
session that makes the group kill possible also takes the cases out of the
terminal's foreground group, so Ctrl-C reaches this process alone. The case
delivers the interrupt by replacing `_wait`, the one wait, once the
wrapper's child is known to be running. It asserts the child is dead, the
file restored and the verdict `interrupted` with exit 2. Mutated so the
interrupt arm only re-raises, the child survives and the case goes red.

**A race the bound can lose is handled and pinned.** The command can finish
between the bound expiring and the kill, and `killpg` then raises
`ProcessLookupError` for a group that no longer exists. The arm that
swallows it has its own case, driven on a process already reaped.

**What stays unverified: the Windows path on Windows.** `strategy("nt")` and
its verdict text are pinned from this machine (S6, contract §13). The
`proc.kill()` arm and `bin/mutation-check.cmd` have been run by nobody on
Windows, which is the state `bin/arm-check.cmd` is in too. `overview.md`
names who answers it.

**Mutated, each with the command, every one red.** Ten units: the session
flag, the group kill, the interrupt arm's kill, the platform chooser, the
Windows text, `main`'s interrupt arm (whose escaping `KeyboardInterrupt`
interrupted the inner pytest, exit 2, with the case listed failed), the
verdict line's joint, the bounded collection, the escape sentence, and the
`ProcessLookupError` arm.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| phase 1's `subprocess.run(..., timeout=)` bound in `run_cases` | replaced in place by `Popen` with `start_new_session` and `_end`; nothing else carried it |
