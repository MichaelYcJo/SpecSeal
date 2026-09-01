# 1788276387-the-windows-step-never-reaches-its-guard — overview

## Why this work exists

`test_letting_drift_warn_takes_both_halves` has failed on the Windows CI leg
since the day it landed (PR #58), which turns every branch's checks red and
blocks every merge; the `step` helper's bash line quotes `sys.executable`
with its Windows backslashes, so bash never reaches the guard the test is
about.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| none | | | |

## Not verified

| Item | Who must answer |
|---|---|
| The fix on an actual Windows runner. Attempt 1 (forward-slashed interpreter path) did not change the failure, so the surviving hypothesis is `bash` on PATH resolving to something that fails every command with its own exit code; the test now checks that precondition by executing `bash -c "exit 7"` and skips with the reason when it does not hold. Which of the two paths the runner takes is read, not executed | CI's windows leg on this work item's pull request |

## Not done

Nothing beyond the one helper; the guard's own semantics are untouched.

## Fed back into the spec

none
