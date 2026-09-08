# Feature Specification: an exited session reads as live for five minutes

<!-- seal/specs/1788846800-an-exited-session-reads-as-live-for-five-minutes/spec.md -->

## Grounding

This repository has no `docs/policies/` tree, so the SDD set is the root of
judgment. Two ratified documents bound the work and are cited rather than
restated:

| Document | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | a test seen red, a stated failure direction, a prompt budget, platform honesty |
| `docs/worktree-guard-spec.md` §*Leases* | the lease is the declared work stream; the heuristics only infer |

## Scope

**In.** The last arm of `sessions_in_tree` (`hooks/worktree-guard.py`), which
turns a fresh transcript with no matching process into an unattached live
session. The arm resolves to active for a session that has *exited*, because
its two inputs — no process, a fresh transcript — are also exactly that
session's inputs.

**Out.**

- The verdict ladders in `guard_worktree_creation` and `judge_creation`. This
  work changes an input to them, never their arms (#237's ladder in
  particular).
- `hooks/worktree_consent.py`. Untouched.
- Whether `transcript_idle_minutes` should become per-tree instead of
  per-project. Separable, and the repair lands per-session, which is narrower
  than either. See `questions.md` Q2.

## What the measurements changed

The ticket settles a direction — *a live session holds its transcript open; an
exited one does not* — and the first probe **falsifies it**. No live `claude`
process holds any transcript open, including the session writing its own file
seconds earlier. The file-descriptor discriminator would answer *not held* for
every session and would collapse the arm to always-idle, which is the fail-open
direction `proc_cwd`'s docstring argues against.

The second probe, a terminal marker in an exited transcript's tail, is also
negative: no record type separates the two populations, and the nearest
candidate (`cost-state`) is absent from 127 exited transcripts and appears
mid-file in 23.

What both probes uncovered instead is that the guard **already holds the
answer**. `hooks/session-lease.py` writes `<git-dir>/specseal-leases/<session-id>`
carrying the owning pid, and its docstring states the purpose in as many words:
*extension-hosted sessions aren't named `claude` … Heuristics infer; leases
DECLARE.* The lease is the designed answer to the very case the arm was built
for.

In the reported incident the lease mechanism got it right and the arm overrode
it. `fresh_leases` read the exited session's lease, found its pid gone, and
retired it on positive evidence. The arm then read the same session's transcript
and resurrected it.

**So the defect is not a missing signal. It is one arm re-animating a session
another arm has already buried.**

## The repair

A transcript belonging to a session whose lease proves its owner is gone is a
record, not a signal. Excluding those transcripts fixes the incident exactly,
keeps the extension-panel case (a live panel session's lease owner is alive),
and adds no new syscall.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| **The incident** | Given a fresh transcript whose tail is active events, and a lease naming a pid that is not running · When the tree is judged · Then the session is **not** active | `test_an_exited_sessions_transcript_is_not_a_work_stream` |
| **The case that must not break** | Given a fresh transcript and **no lease at all** (a panel session that has not yet touched the repo) · When the tree is judged · Then it is still active | `test_a_transcript_with_no_lease_still_counts` |
| A live owner keeps its transcript | Given a fresh transcript and a lease whose pid **is** running · Then still active | `test_a_live_lease_owner_keeps_its_transcript` |
| Another host is not ours to judge | Given a lease from a different host · Then still active | `test_a_lease_from_another_host_does_not_retire_a_transcript` |
| A lease with no pid is not evidence | Given a lease carrying no `pid` · Then still active | `test_a_lease_without_a_pid_does_not_retire_a_transcript` |
| The subagent directory follows its session | Given `<dead-session>/subagents/*.jsonl` fresh · Then not active | `test_a_dead_sessions_subagent_transcripts_are_skipped` |
| End to end | Given the incident's shape · When `sessions_in_tree` runs · Then `active == []` | `test_sessions_in_tree_does_not_resurrect_an_exited_session` |

## Data & interfaces

No schema, no endpoint, no payload. One new module-level helper and one new
keyword argument, both internal to `hooks/worktree-guard.py`.

## Open questions → questions.md

Q1 (where an unreadable answer lands) and Q2 (per-project vs per-tree) are in
`questions.md` with the orchestrator named as answerer. Both carry a
recommendation and the work continues under it.
