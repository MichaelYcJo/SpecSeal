# an exited session reads as live for five minutes — overview

📋 implement applied
· spec:     `CLAUDE.md` (repo + user), `CONTRIBUTING.md` §What a change to a gate must carry · §Running the checks, `docs/flow.md` §0.9.2 · §0.9.3, `seal/config.md`, `seal/follow-up.md`, `seal/ledger.md` §Coordinates, this item's `routing.md` · `spec.md` · `plan.md` · `questions.md`, `agent-contract` §§1–3 · 7 · 9 · 12 · 14 · 15, issues #256 and #257
· evidence: `seal/ledger/1788846800-…md` — 4 rows added (S1 · S2 for #256, S3 · S4 for #257), 15 coordinates, `--strict` exit 0
· verified: **executed** — both probes, the acceptance cases seen red then green, 14 mutations across two loops with 0 survivors, `bin/test` on 8 modules, `rider_check.py` exit 0, `evidence_check.py --strict` exit 0, `ruff check`/`format`. **Read, not executed** — the harness's permission flow for a call the hook declines to decide. **Not run** — the full suite, lint over the whole tree, and the Linux and Windows legs (see *Not verified*)

## Why this work exists

Ending a session made the tree read as concurrent for five minutes, so `git
switch` was denied and work was pushed into worktrees nobody needed (#256);
and batching commands into one call cost a confirmation the previous release
had already removed (#257). Both were found by using the guard on this
repository's own 0.9.2 release run.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The discriminator for a live session | #256 settles it: *"A live session holds its transcript open; an exited one does not. Use the open file descriptor as the discriminator on this arm."* | The lease record's owning pid, which the guard already writes and already probes | **Measured false.** `lsof` on the transcript of the session writing it seconds earlier returns nothing (exit 1), and all 13 live `claude` pids hold 0 `.jsonl` descriptors. Built as settled, the arm would have answered *not held* for every session and collapsed to always-idle — trading the extension-panel case away instead of keeping it, which is the one thing the ticket forbade. The ticket's supporting probe had no positive control: its row *"no process holds it open — the session is gone"* is a true reading of a fact that is equally true of a live session |
| Where the fix lands | The ticket names one coordinate, `:1140-1143` | Both call sites of `transcript_idle_minutes` | `agent-contract` §12 — the finding names an instance, the fix is owed to the class. The per-pid site has the same defect: a live session held in `active` by a dead neighbour's transcript. Moving it to `idle` turns a deny into a question and never into a silent allow, because the pid is real and stays in one of the two lists |
| The cheaper alternative the ticket asked me to check | *"whether an exited session's transcript carries a terminal marker in its tail. If one exists it is cheaper than `lsof`"* | Not used — none exists | Across 188 transcripts no last-record type separates the populations; `system` and `bridge-session` appear in both. `cost-state`, the nearest candidate, is absent from 127 exited transcripts and mid-file in 23 |
| Where the leftover from #257 is filed | The prompt and `plan.md` both said `seal/follow-up.md` | A `# RIDER:` at the branch itself | `seal/follow-up.md`'s own rules: *"Anything tied to a coordinate is a `# RIDER:` comment at the line it is about"*, because nobody greps a follow-up list before editing a message block. Corrected in the ledger row and in `phases/phase-2.md`, which had both named the wrong home |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint, and the typecheck — `agent-contract` §2 reserves these for the orchestrator, run once after the rounds settle | the orchestrator |
| That a live VS Code extension-panel session is still counted. No panel session could be produced in this environment, so the case is pinned by construction rather than by observation: a live panel session's lease owner is alive and a session with no lease is not proved dead, so neither reaches the dead set | the orchestrator, or anyone who can open a panel session and run `.github/scripts/` against it |
| That the harness applies its normal permission flow to a call the hook declines to decide — #257's whole argument for `silent` over `ask`. The half that lives in this repository IS executed (the hook emits an empty stream, asserted on the raw stream); the half that lives in the harness cannot be executed by any test in this tree | the orchestrator |
| The Linux and Windows legs. Everything here ran on macOS. `dead_session_ids` adds no platform-specific call — a `listdir`, a `json.load`, and the existing `lease_owner_alive` — but the pid-type guard it relies on is only observable on Windows, where `tasklist /FI "PID eq {pid}"` interpolates a string happily | CI |

## Not done

**The per-project read was left per-project** (#256's second open decision).
The over-reporting the ticket measured is per-*session* and the repair lands
per-session, which is finer than either option on offer, so this fix does not
need it. Narrowing to per-tree would separately discard a real signal — another
worktree of the same project being worked in — and that is a behaviour change
owed its own ticket.

**The process scan was not widened to match on argv.** It would find an
extension-panel host that `comm` cannot see, and it complements this fix
rather than competing with it — but it does not touch the defect, since the
incident had no process to find at all, and it could not be measured here for
the same reason the panel case could not. Named in `plan.md`'s Alternatives
table so it is not lost.

**The unreachable else branch in `guard_worktree_creation`'s consent message
was left standing**, with the `consented` parameter's `ask` default. Removing
it was outside the bound #257 was given. It carries a rider at the line.

**No pull request was opened and no reviewer was spawned**, per the handoff.
The branch is committed and unpushed; `release/v0.9.3` does not exist yet, so
there is nothing to open it against.

## Fed back into the spec

**One clause, inferred during implementation, and it is in the ledger as S2
rather than here**: the two liveness discriminators #256 proposes do not
exist. It is recorded as a row because the falsified direction is written down
in the issue, which is where a later reader looks first, and it would
otherwise be re-proposed from that text with the measurement lost.
