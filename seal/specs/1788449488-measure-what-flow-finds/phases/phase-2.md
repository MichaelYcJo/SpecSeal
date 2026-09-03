# 1788449488-measure-what-flow-finds — phase 2

<!-- seal/specs/1788449488-measure-what-flow-finds/phases/phase-2.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | ff7f292 |

## What this phase was asked

Build phase 2 only, of the 3-phase table in `plan.md`: a new
`.github/scripts/roll_flow_measurement_issue.py` — a pure
`next_version(current: str) -> str` function (minor bump, patch reset to 0:
`"0.7.0"` → `"0.8.0"`, `"0.7.3"` → `"0.8.0"`), tested directly with no
`gh`/`git` calls; a `main()` that reads `.claude-plugin/plugin.json`'s
version, lists open `flow-measurement` issues via `gh issue list --label
flow-measurement --state open --json number,title`, fails loudly
(`sys.exit`) if the count is not exactly 1, else closes that issue and opens
a new one titled `chore: flow measurement — <next_version>`, labelled
`flow-measurement`, empty body. Wire
`.github/workflows/close-issues-on-release.yml` to run this script as a
second step (same trigger, same checkout, same `GH_TOKEN`/`REPO` env already
set for the neighbouring step).

Explicit instruction carried from phase 1's own finding, not from `plan.md`'s
phase 2 row itself: build in a bounded retry (one retry after a short sleep)
on the label lookup before treating "zero open" as the fail-loud invariant
violation, so a false "zero open" reading right after some other action does
not cause the wrong branch to fire — an implementation-robustness addition on
top of the plan, to be recorded as a plan divergence in `overview.md` (phase
3's job).

New test module, name chosen by this phase, following
`tests/test_release_hygiene.py:225-355`'s `monkeypatch`-on-`subprocess.run`
pattern: `next_version` cases (pure function, no mocking); the
exactly-one-open invariant (0 open after retry → fails loudly, 2 open → fails
loudly, 1 open → closes it and opens the next, with the right title and empty
body) via mocked `subprocess.run`/`gh` calls, never hitting the real network.
Every new case shown red first.

Do not start phase 3. Fill `plan.md`'s Phase 2 Status cell with the commit
that closes this phase. Run
`uvx --with pytest python3 -m pytest <new test module> -q` (fresh output,
exit code read directly) before calling this phase done. Write this file
from `templates/sdd-phase.md`. Mutation-test every new unit before handing
over.

## What this phase found

**The retry is asymmetric by design, and that asymmetry is itself
mutation-tested.** A search-index lag (phase 1's finding) can only ever
produce an undercount — GitHub had written the label but the search index had
not caught up, so the lookup returned fewer results than the true state, never
more. So the retry fires only on a zero reading; a reading of two or more is
never a lag artifact and is never retried — `test_two_open_issues_fails_
loudly_without_retrying` pins that a two-open reading exits without calling
`time.sleep` at all, not just that it eventually exits.

**Plan divergence, carried forward from phase 1's own note (spec.md's
acceptance table already treats "exactly one open" as the invariant to
enforce, not as a check that must be instantaneous after a label write, so
this needed no design change — only the retry itself, which the plan's own
phase 2 row did not spell out).** `plan.md`'s phase 2 row describes the
exactly-one-open invariant as a direct fail-loud check with no retry
language. The retry-once hardening is additive robustness on top of that row,
not a redesign of it: a zero reading still fails loudly, just after one more
look rather than on the first. Recorded here per phase 1's own instruction to
flag it now so phase 3's `overview.md` has it; phase 3 is the one that
carries it into the closing memo's own divergence section, since this file's
own job (per `templates/sdd-phase.md`) is what the phase discovered, not the
closing account.

**Mutation testing surfaced a bytecode-cache gap the contract's own
instruction did not anticipate for this case.** §Verify's mutation step says
to clear `tests/__pycache__` between mutations, because the earlier work item
that wrote that instruction was mutating code the test files import directly
from the repository's normal package layout. This phase's test module loads
the script under test with `importlib.util.spec_from_file_location` from
`.github/scripts/`, a directory Python also caches bytecode for, under
`.github/scripts/__pycache__` — a location the contract's instruction does
not name. One mutation (making `read_version` ignore its `root` parameter)
was restored correctly on disk, byte-for-byte, but a stale `.pyc` from the
mutated run was still picked up by the *next* isolated test invocation,
because only `tests/__pycache__` had been cleared between mutations and not
`.github/__pycache__`. The batch run across all eight mutations happened to
not surface it (each mutation ran in its own subprocess close enough in time
that the loader's mtime check re-read source), but a later standalone rerun
of the full suite caught it directly: `test_read_version_reads_plugin_json`
failed, asserting `9.9.9 == 0.6.0` — the mutated "ignore root, always read
the real repository's own `plugin.json`" behavior, resurrected from cache
after the source was already restored. Fixed by clearing both
`tests/__pycache__` and every `__pycache__` under `.github/` before each
mutation and before the final confirmation run; the final run was rerun after
that fix and passed clean (6 passed, exit 0), matching the earlier passing
run byte-for-byte since the source file was never actually different.
Worth carrying into `agent-contract`'s own mutation-testing instruction: "clear
`tests/__pycache__`" should read "clear `tests/__pycache__` and any
`__pycache__` next to the module under test" wherever the module under test
lives outside the normally-imported tree — flagged here as a phase finding,
not acted on, since editing the plugin's own shipped contract is out of this
work item's scope (`spec.md`'s Out section: no change to gate/refusal logic,
and this is not that, but it is still not this branch's file to edit).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
