# Implementation Plan: an exited session reads as live for five minutes

<!-- seal/specs/1788846800-an-exited-session-reads-as-live-for-five-minutes/plan.md -->

## Summary

Stop the transcript arm of `sessions_in_tree` from counting a transcript whose
session a lease has already proved dead. The lease record already carries the
owning pid, `lease_owner_alive` already probes it, and `fresh_leases` already
retires the lease on that evidence — the transcript scan is simply not told.

The change is subtractive. It only ever *removes* liveness, and only on the
positive evidence `fresh_leases` demands: this host, a recorded pid, and that
pid no longer running. Every other lease shape — another host, no pid, an
unprobeable owner, no lease at all — leaves the transcript counted exactly as
it is counted today.

## Technical context

- `hooks/worktree-guard.py:1136-1143` — the arm. Fires only when `active` is
  empty, which is after both the process scan and `fresh_leases` have run.
- `hooks/worktree-guard.py:953-1074` — `fresh_leases`, whose docstring states
  the rule this change reuses: *A lease is dropped ONLY on positive evidence
  that its owner is gone.*
- `hooks/worktree-guard.py:905` — `lease_owner_alive(pid)` → True / False / None.
- `hooks/worktree-guard.py:854` — `transcript_idle_minutes(cwd, own_session_id)`,
  which scans `<session-id>.jsonl` and `<session-id>/subagents/*.jsonl`. The
  session id is in the filename, which is what makes the exclusion addressable.
- `hooks/session-lease.py:1-28` — the lease writer, and the statement that
  leases exist precisely because extension-hosted sessions are not named
  `claude`.

**The incident, replayed against the code.** At the denial, pid 22255 was the
guard's own session, so `pids - mine` was empty and `active` was `[]`.
`fresh_leases` read the lease of session `fdbb7b51…`, found its recorded pid
`21518` no longer running, and retired it — correctly. The arm then read that
same session's transcript, saw two minutes, and appended it to `active`, which
on the switch path is a hard deny. *(Lease and process states verified on disk;
the pid is still recorded gone.)*

**What breaks in six months.** If Claude Code ever stops writing leases, or
moves the lease directory, the exclusion set goes empty and the arm reverts to
today's behaviour — over-reporting, not under-reporting. That is the safe
direction, and it is the same failure mode the arm already has.

The second-order risk is a session whose lease pid is reused by an unrelated
process after the session exits. Then `lease_owner_alive` says alive, the
transcript is counted, and we over-report. Again the safe direction, and
`fresh_leases` already carries that exposure unchanged.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The open file descriptor** (the ticket's direction) — `lsof` the transcript; a live session holds it open | **Measured false.** No live `claude` holds any transcript open, including one writing its own file seconds earlier; all 13 live pids hold 0 `.jsonl` fds. The discriminator would answer *not held* for every session, collapsing the arm to always-idle — the fail-open direction | **Rejected on measurement** |
| **A terminal marker in the tail** — a record type written at session end | **Measured false.** Across 188 transcripts no last-record type separates fresh from old (`system`, `bridge-session` appear in both). `cost-state`, the nearest candidate, is absent from 127 exited transcripts and mid-file in 23 | **Rejected on measurement** |
| **Sample the transcript twice** — a live session's file grows | A live-but-waiting panel session does not grow either, so the case the arm exists for breaks in its most common state. Also puts a sleep in a hook | Rejected |
| **Widen the process scan to argv** — find the panel host by command line, not `comm` | Reasonable and complementary, but it does not touch the defect: the incident had *no* process to find. It would also be an unmeasured widening, since no panel session was available to measure against | Rejected for this work item; noted in `seal/follow-up.md` |
| **Drop the arm entirely** — the lease already covers the panel case | Correct for a panel session that has touched the repo, wrong for one that has only written transcripts. The arm's residual case is real, and dropping it is a fail-open change | Rejected |
| **Exclude transcripts of lease-proved-dead sessions** | Only fires on positive evidence of death; every unreadable answer leaves today's behaviour intact | **Chosen** |

## The two decisions, with recommendations

**Q1 — where an unreadable answer lands.** The chosen design makes this
question mostly moot, which is its main argument. The exclusion is *additive
evidence of death*, not a liveness test that can fail: `lsof` is never called,
and the only probe is `os.kill(pid, 0)`, which `lease_owner_alive` already
wraps and which returns `None` — not `False` — when it cannot answer. A `None`
leaves the session out of the dead set and therefore still counted as active.
**Recommendation: fail toward active**, which here means *do nothing*, and is
the same rule `fresh_leases` states for itself. Implemented that way.

**Q2 — per-project or per-tree.** **Recommendation: leave alone**, and the
repair is a reason rather than a deferral. The over-reporting the ticket
measured is per-*session*, and the exclusion lands per-session, so it corrects
the fault at a grain finer than either option. Narrowing to per-tree would
separately discard a real signal — another worktree of the same project being
worked in — and that is a behaviour change with its own failure direction,
owed its own ticket.

## Failure direction, prompt budget, platform honesty

*(the three `CONTRIBUTING.md` §What a change to a gate must carry demands
beyond the red test, which is in the Phases table)*

- **Direction: the gate allows more, in exactly one shape** — a session whose
  lease proves its owner exited. A wrong allow here cannot move another
  session's branch, because the evidence is that no such session exists. Every
  other shape is untouched, so the change cannot widen an allow it was not
  aimed at.
- **Prompt budget: strictly fewer, never more.** On the switch path the
  incident's shape went `deny`; it now falls through to allow. On the creation
  path it went `ask`; it now falls through. No shape gains a prompt. Against
  this project's first goal — verification that runs unattended — the change
  removes a denial that fired for five minutes after every session in the
  project ended.
- **Platform honesty.** `lease_owner_alive` is already the platform-aware
  probe and is unchanged. The new code adds no platform-specific call: a
  `listdir`, a `json.load`, and `lease_owner_alive`. **Executed on macOS
  only.** Linux and Windows are unexercised by me and go to the handover
  labelled `unverified`; CI runs the suite on all three.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `dead_session_ids` + `lease_dir`, and `transcript_idle_minutes` skipping them | the seven cases in `spec.md`, each seen red first | |
| 2 | Records: changelog fragment, ledger fragment, `docs/flow.md` row, overview | `evidence_check.py --strict --ledger …`, `bin/test` on the two modules | |

## Operational impact

None. No migration, no new environment variable, no new dependency, no
compatibility break. The lease format is read exactly as `fresh_leases`
already reads it, including the pre-upgrade bare-timestamp form, which parses
to an empty record and therefore never lands in the dead set.
