# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — phase 5

<!-- seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | dace4e34 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 5, the depth bound (`spec.md` decision 4).
`NESTING_READ = 32` goes in `hooks/commit-review-gate.py`, `_hides_a_commit`
answers True past it, and the `RecursionError` catch stays. For S9: the call
count is a case, red at `86256492`. The time for 4000 and 6000 nested `<(`,
`$(` and backticks beside a commit is measured at `86256492` and after, and
recorded in this record and the PR body. The §13 run with a lowered recursion
limit is made once in a subprocess and recorded. Q1, the harness hook
timeout, is the orchestrator's and is left to it.

## What this phase found

**The bound is a depth counter around `_reads_a_commit`.** Past `NESTING_READ`
levels, `_hides_a_commit` returns True without reading. A `finally` gives the
level back, so a deep read in one part of a command does not leave the next
part pre-answered. The mutant with no decrement shows what that costs: every
control in a declared repository then stops.

**Measured**, the gate's `main()` in-process on a commit into an undeclared
repository beside a nesting, from a declared session directory, with
`_reads_a_commit` counted. The third kind is a backtick around each `$(`.
Nested backticks need escaping, and the reader does not unescape them, so
only this form nests with backticks at all.

| Depth | Kind | `86256492` | Head (`6e4e0de5`) |
|---|---|---|---|
| 4000 | `$(` | deny, 249 calls, 12.62 s | deny, 32 calls, 2.32 s |
| 4000 | `<(` | deny, 249 calls, 12.98 s | deny, 32 calls, 2.07 s |
| 4000 | `` `$( `` | deny, 744 calls, 13.98 s | deny, 95 calls, 2.51 s |
| 6000 | `$(` | deny, 249 calls, 24.57 s | deny, 32 calls, 4.39 s |
| 6000 | `<(` | deny, 249 calls, 50.19 s | deny, 32 calls, 3.89 s |
| 6000 | `` `$( `` | deny, 744 calls, 62.10 s | deny, 95 calls, 4.33 s |

The base figures are larger than round 3's 30.8 s and 31.4 s. The counting
wrapper and the rest of this build's readers each rescan the body once more
per level. What the table compares is the same wrapper at both SHAs. The
remaining 2 to 4 seconds are the outer readers scanning the whole
6000-level string once each, and not the recursion.

**§13, once, in a subprocess.** With `sys.setrecursionlimit(120)`, below what
32 levels need, `RecursionError` fired at 29 levels and every row still denied
(29, 29 and 84 calls, 1.8 to 2.2 s). The catch is what answers there, and
it answers the same way.

**The case asks for the bound exactly.** `len(calls) == NESTING_READ`. A
count below it means the recursion limit answered first, and a count above it
means the bound did not hold. The first version asked for at most
`NESTING_READ + 1`, and a mutant raising the bound to 1000 passed it: the
recursion limit, some 250 levels down, answered in its place. The equality is
what kills that mutant.

**Seen red.** At `86256492` the same count is 249 per chain (the probe
above), not 32. The planted case fails there on the missing name before it
reaches the count.

**Mutants.** Each ran alone under `PYTHONDONTWRITEBYTECODE=1` and was restored
from saved bytes. The tree was clean after each run.

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | no bound | `test_a_deep_nesting_is_read_to_a_bound` |
| 2 | the bound answers False | the same |
| 3 | no increment | the same |
| 4 | no decrement | the controls in a declared repository |
| 5 | a bound of 1000 | the same case, once it asks for equality |

The `except RecursionError` is the base's and was not mutated. With the
default limit the bound answers first, so no case in the suite can tell the
catch is there. The §13 run above is what shows it still answers.

**Verification.** Executed at `dace4e34`: the 26 modules, 1475 passed and 1
skipped, exit 0. S7 passed.
`test_a_commit_found_before_a_nesting_too_deep_still_stops`, round 2's case,
passed.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.**

- *A test seen red.* The call count is 249 per chain at `86256492` against
  32, and every changed branch has a mutant a case kills.
- *Failure direction.* Past 32 levels a body counts as one that might commit,
  which only adds a stop. The catch stays behind it.
- *Prompt budget.* No command a person writes nests 32 levels. The
  commit-message form is two. A nesting of 32 or more with no commit in it is
  a new stop (`spec.md` (c)). The time for the pathological case drops from
  12 to 62 seconds to 2 to 4, measured.
- *Platform honesty.* Measured on macOS under CPython 3.14.4, at its default
  recursion limit and a lowered one. The suite ran under the repository's
  3.13.9. Q1, whether the harness cuts off a hook that runs
  long, is still the orchestrator's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
