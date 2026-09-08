# 1788846800-an-exited-session-reads-as-live-for-five-minutes — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e926704 |
| Ran by | `specseal:smith` — model unknown, the spawn prompt named none; the orchestrator fills this |

## What this phase was asked

Fix #256: `sessions_in_tree`'s last arm reads a fresh transcript with no
matching process as an unattached live session, and those are also exactly the
inputs of a session that exited inside `IDLE_MIN`.

The prompt settled a direction — *a live session holds its transcript open; an
exited one does not* — and required two probes **before** building on it: that
a live VS Code extension-panel session holds its own transcript open, and
whether an exited session's transcript carries a terminal marker in its tail.
The panel case at `:1135-1139` was named as one this work must not trade away.

## What this phase found

**Both probes came back negative, and the direction the ticket settled cannot
be built.**

- **No live `claude` process holds any transcript open.** `lsof` on the
  transcript of the session writing it seconds earlier returns nothing, and
  all 13 live `claude` pids on this machine hold 0 `.jsonl` descriptors. The
  ticket's probe table row *"no process holds it open — the session is gone"*
  was an uncontrolled measurement: it lacked a positive control, and the same
  result comes back for a live session. Built as specified, the discriminator
  would have answered *not held* for every session, collapsed the arm to
  always-idle, and traded the panel case away completely — the opposite of
  what the ticket intended.
- **No terminal marker exists.** Across 188 transcripts, no last-record type
  separates fresh from exited (`system` and `bridge-session` appear in both).
  `cost-state`, the nearest candidate, is absent from 127 exited transcripts
  and appears mid-file in 23, so neither its presence nor its absence decides
  anything.

**What the probes uncovered instead is that the guard already holds the
answer, one function away.** `hooks/session-lease.py` writes the owning pid
into `<git-dir>/specseal-leases/<session-id>`, and its docstring states the
purpose exactly: *extension-hosted sessions aren't named `claude` … Heuristics
infer; leases DECLARE.* The lease is the designed answer to the very case the
arm was built for.

So the defect is not a missing signal. **It is one arm re-animating a session
another arm has already buried.** Verified against the incident's own state,
still on disk in the main checkout: `fresh_leases` read session `fdbb7b51…`'s
lease, found pid `21518` gone, and retired it on positive evidence; the arm
then read that session's two-minute-old transcript and put it straight back
into `active`, which on the switch path is a hard deny.

The repair excludes transcripts of lease-proved-dead sessions. It is
subtractive, needs no new syscall, and is safe by construction: a session
lands in the dead set only on positive evidence its owner is gone, so every
unreadable answer leaves today's behaviour intact. **That is also the answer
to the ticket's first open decision** — the fail direction is not a choice the
design has to make, because the exclusion is evidence of death rather than a
liveness test that can fail.

**Two things the next phase and the reviewer need.**

- The fix belongs at **both** call sites of `transcript_idle_minutes`, not
  only the arm the ticket names (`agent-contract` §12). The per-pid site has
  the same defect with a different consequence: a live session held in
  `active` by a dead neighbour's transcript. Moving it to `idle` turns a deny
  into a question and never into a silent allow, because the pid is real and
  stays in one of the two lists.
- **Mutation testing found three cases pinning nothing**, and one of them was
  a counterfeit in the strict sense: the another-host case used pid 1, which
  is alive on every machine, so it passed with the host check deleted. The
  per-pid call site had no case at all. Nine mutants, all now killed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The unconditional trust the transcript arm placed in a fresh transcript | Replaced in the same arm by `dead_session_ids`; the arm itself stays, and the case it exists for is pinned by `test_sessions_in_tree_still_sees_an_unattached_live_session` |
| `fresh_leases`' inline git-dir resolution | Extracted to `lease_dir`, which `fresh_leases` now calls — same behaviour, one reader |
| The ticket's chosen direction (an `lsof` discriminator) | Not implemented, and the grounds are recorded in `plan.md`'s Alternatives table and in this record, so it is not re-proposed from the ticket text alone |
