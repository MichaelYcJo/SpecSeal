# 1788486395-the-roll-opens-the-next-log-with-no-body — phase 2

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/phases/phase-2.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8e87f94 |

## What this phase was asked

`.github/scripts/roll_flow_measurement_issue.py:155`, `open_issue`. It passes
`--body ""`. Give it one:

```markdown
Rolls from #<the issue just closed>. Baselines and the observations that span
versions live in #<the durable ledger>; this issue takes one comment per
segment and is closed when <version> ships.
```

The durable ledger's number is found the way the skill says a repository
declares it — by the `flow-baseline` label — not hardcoded. If none is found,
write the body without that clause rather than failing. `main` at `:173` reads
`open_issue`'s return value for its failure message; keep that contract or say
what changed. `test_one_open_issue_closes_it_and_opens_the_next:144` is the
case that grows, seen red first.

## What this phase found

**The signature change breaks three cases, not one.** The body has to name the
issue just closed, and `main` is the only caller that knows its number, so
`open_issue` takes a third argument. `plan.md` and the spawn prompt both name
`test_one_open_issue_closes_it_and_opens_the_next` as the case that grows, and
it is the case whose *assertions* grow. Two others stub `open_issue` with a
two-argument callable and raise `TypeError` the moment `main` passes three:
`test_one_open_issue_after_the_retry_succeeds:100` and
`test_close_succeeds_but_open_fails_names_both_in_the_message:202`. The first
of those now asserts the closed number reaches the stub, so the argument is
pinned by a case rather than merely tolerated by one.

**`main:173`'s contract is unchanged.** `open_issue` still returns the title
and still raises `SystemExit` from `run` on a genuine create failure, so the
recovery message that names both the closed issue and the title to open by
hand is untouched.

**A best-effort lookup needs a non-exiting `run`, and that is a second
primitive rather than a flag.** `run` calls `sys.exit` on a non-zero return,
which inside `open_issue` becomes the recovery path — correct for the create,
wrong for the ledger lookup, where a `gh` failure must cost the clause and not
the release. `try_run` is that second primitive: same call, `None` on failure.
Phase 3 is its second user, which is why it is a module function rather than a
`try/except` inside the lookup.

**`find_baseline_issue` has three ways to come back empty and they are not one
branch.** The call failed (`try_run` answers `None`), the label exists with
nothing open (`[]`), and the output is not JSON at all. The third is the one a
reader would leave out: `gh` answering with something unparseable raises
`ValueError`, and `main` catches `SystemExit` only. An uncaught `ValueError`
after a successful close is the worst failure this script has, because the
recovery message that tells an operator what to open by hand never prints.
All three answer `None`.

**The absent-ledger branch is a sentence split, not a conditional clause.**
Writing `f"... live in #{baseline_number};"` and hoping `None` never arrives
produces `live in #None`, which renders as prose and reads as a broken link.
The body is built from two halves so the ledger clause is absent rather than
empty. The two shapes, executed:

```
Rolls from #133. Baselines and the observations that span versions live in
#51; this issue takes one comment per segment and is closed when 0.9.0 ships.

Rolls from #133. This issue takes one comment per segment and is closed when
0.9.0 ships.
```

**Eight mutations, none survived** — the roll-from clause removed, the closing
version removed, the `None` guard removed, the failed-call guard answering `0`,
the empty-list guard answering `0`, the JSON guard removed, the create passing
`""` again, and `main` passing a wrong number. Each run cleared
`tests/__pycache__` and restored the file from bytes the probe kept.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `--body ""` on the create, and the case asserting the body must be empty | The same call and the same case: `open_issue` builds the body from `issue_body`, and `test_one_open_issue_closes_it_and_opens_the_next` now asserts it names the closed issue, the durable ledger, and the version it closes on |
| `open_issue`'s two-argument signature | `main`, which now passes the closed issue's number, and the three cases that call or stub it |
