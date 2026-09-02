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
| ✅ The fix on an actual Windows runner | executed: this PR's windows leg went green at c888075, 1091 passed · 17 skipped — one more skip than before, which is the guard test taking the precondition path (bash there fails the `exit 7` probe). Attempt 1's forward-slash-only change had not moved the failure, which is what narrowed the cause to bash itself. Session of 2026-09-02 |

## Not done

Nothing beyond the one helper; the guard's own semantics are untouched.

## Fed back into the spec

none
