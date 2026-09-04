# 1788486395-the-roll-opens-the-next-log-with-no-body — phase 3

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/phases/phase-3.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <pending> |

## What this phase was asked

The same `gh issue create` call adds `--label measurement` and
`--milestone "log: measurement"`.

**Neither may fail the release.** A milestone is repository state: it can be
renamed or deleted, and `gh issue create --milestone` fails outright on a name
it cannot resolve. The invariant this script protects is *exactly one open
`flow-measurement` issue*, which neither argument touches. So: attempt them,
and when one fails, say so in the body of the issue just created — that is the
one artifact a person opens; a line in a workflow log is not read.

## What this phase found

**Tolerating a failure means retrying the create, and a retry is how this
script would break its own invariant.** The task frames the two arguments as
best-effort, which reads as *do not exit*. Getting the argument off the call
means calling `gh issue create` again without it, and a create that fails
after the mutation lands — a network drop between GitHub's write and the
client's read — would then open a second issue. Two open `flow-measurement`
issues is the reading the module docstring says is *never a lag artifact and
always the invariant broken*, and this script would be its author.

So a failed attempt re-reads `list_open_issues` before it retries, and a
reading that is no longer empty ends the ladder with the issue that landed.
The cost is one extra `gh issue list` per failed attempt, which happens only
on a path that is already failing. `plan.md`'s *failure direction: allows
more* is about the two arguments; it was never a licence for the retry to
break the one-open rule, and the divergence is recorded in `overview.md`.

**The last rung is `run`, not `try_run`, and that is what keeps the recovery
message reachable.** Three rungs: both arguments, the index label alone,
neither. The first two tolerate failure; the third does not, so a create that
fails all the way down still raises `SystemExit` into `main`'s handler, which
names the already-closed issue and the title to open by hand. Mutating that
rung to `try_run` is one of the nine mutations below, and
`test_every_attempt_failing_still_exits_loudly` is what killed it.

**Each rung drops the argument the rung above could not set, rather than
retrying it.** A fallback that keeps the failing argument is not a fallback;
`test_a_milestone_that_cannot_be_set_does_not_fail_the_release` asserts
`--milestone` is absent from the second attempt, and the mutation that puts it
back was killed.

**Which argument failed is inferred from the rung, not from `gh`.** A first
attempt that fails for an unrelated reason — a network blip — produces a
second attempt whose body says the milestone could not be set. The note is
written to survive that: it says the milestone *could not be set*, names the
three reasons, and asks a person to set it by hand *if it still exists*. What
it never does is assert the milestone is gone. Distinguishing the causes would
mean parsing `gh`'s stderr, which is a string this repository does not own.

**`INDEX_LABEL` and `INDEX_MILESTONE` are constants for the reason `#109`'s
own row learned.** They are this repository's names and the module docstring
now says why they may live here and not in the skill:
`tests/test_the_release_check_watches_what_ships.py` classifies `.github/` as
staying home, and phase 1's
`test_the_shipped_skill_names_no_repository_specific_tracker_state` holds the
other half from the skill's side.

**Nine mutations, none survived** — the index label removed from the first
rung, the milestone removed entirely, the fallback retrying the milestone, the
fallback's note dropped, the last rung's notes dropped, the landed-create
guard removed, the last rung switched to `try_run`, `LABEL` dropped from the
create, and `issue_body` ignoring its notes.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `open_issue`'s single unconditional `run(... "gh", "issue", "create" ...)` | `create_args`, which builds the argument tuple, and the three-rung loop in `open_issue` that calls it. The last rung is still `run`, so the failure path the module docstring describes is unchanged |
