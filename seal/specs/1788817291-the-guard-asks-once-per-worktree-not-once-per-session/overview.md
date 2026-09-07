# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `gh issue view 237`; `CONTRIBUTING.md` §*What a change to a gate must carry*; `CLAUDE.md` §*The goal a design is chosen against*; `docs/worktree-guard-spec.md` §B, §Choice sites; `skills/agent-contract/SKILL.md` §§2, 9, 12, 13, 15; `hooks/worktree-guard.py`'s module docstring and `has_token`'s; `seal/config.md` (no `Record language` row → English); `seal/follow-up.md`
· evidence: 9 rows in `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md`, all `Executed`; `hooks/dispatch.py#GROUPS` re-verified in `seal/ledger.md` (`b3d45306 -> a5e67d2c`)
· verified: executed — `tests/test_the_guard_asks_once_per_session.py` (26 cases), `test_worktree_guard.py`, `test_worktree_guard_signals.py`, `test_dispatch.py`, `test_guard_resolves_the_tree_it_judges.py`, `test_gates_do_not_fail_open.py`, `test_lint_python.py`, `test_chain_hooks_hardening.py`, `bin/evidence-check .`, and 16 single-unit mutations each seen red. Unverified — the full suite, lint and typecheck (the broad gate, the orchestrator's)

## Why this work exists

The guard had no path through it that cost zero prompts, so an unattended run
reached its first `git worktree add` and stopped; after this it stops once per
session instead of once per worktree, and the evidence it stops for is
something the model cannot write for itself.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the `PostToolUse` arm lives | The ticket says "the guard already keeps session-scoped state … so the place and the pattern exist", which reads as one file | A second file, `hooks/worktree_consent.py` | `hooks/dispatch.py` calls every gate's `main()` with the same payload and no event name, so one file wired to both events would have to sniff `hook_event_name`. `agent-contract` §13 refuses a defence resting on a platform guarantee, and where the field were absent the writer would silently never record — which reads as "nobody ever consented" and costs back every prompt this removes |
| How a consented creation gets through | The ticket says "`PreToolUse` **allows** a later creation" | `allow`, but only for a command that is worktree creation and nothing else; `ask` otherwise | `permissionDecision: "allow"` bypasses the user's own permission settings for the WHOLE tool call, and a creation is routinely one segment of a compound. The record is about worktree creation, so that is the whole of what the guard may speak for |
| The `Agent` path | The ticket says the path "shares the record", without saying what sharing produces | Silence, where Bash allows | That call is a creation PLUS an agent with a prompt. Silence is the guard withdrawing its objection, which is the whole of what the record establishes; the harness's own question about running the agent is not the guard's to remove |
| A redundant condition | `if session_id and worktree_consent.granted(top, session_id)` was written first | The `session_id and` removed | `consent_path` already answers `""` for a missing or separator-only id, so nothing could make the extra condition false — and mutation testing showed no case could pin it. A condition no case can pin is removed rather than kept |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and the typecheck | the orchestrator's broad gate, run once after the rounds settle (`agent-contract` §2) |
| Behaviour on Linux and on Windows — nothing here reads a process, but `os.makedirs`, `open`, `os.path.isfile` and `git rev-parse --git-common-dir` all run | CI's Linux and Windows legs on the pull request |
| That a hook `ask` cannot be auto-answered, and that a `PostToolUse` payload means the call ran — the two harness facts the design rests on | not observable from a test; the same standing every gate in this repository has, named under Platform honesty in `pr-notes.md` |
| Whether a `permissions.deny` rule outranks a hook `allow` — if it does not, a user who explicitly denied `git worktree add` would be overridden after their first approval | the repository owner, or a run against a settings file carrying such a rule |

## Not done

**The compound-command case is left at one prompt each.** `cd X && git worktree
add …` and `git worktree add … && echo done` get `ask` rather than `allow`,
because the allow covers the whole tool call and the record is only about the
creation. Widening it means deciding which other segments a worktree consent
may speak for, which is a different question from the one this work item
answers. The measured six creations were single-segment calls, so the budget
the ticket asks for is reached without it.

**No pruning of the record directory.** It grows one empty file per session
that created a worktree, the way `specseal-worktree-choice/` already does, and
pruning by mtime would be the time bound Q1 rejected arriving through the back
door. If the directory ever needs bounding, it wants a rule that is not a clock.

**`split_command` was not deleted.** Its rider says no production caller reaches
it; this work added two more readers and neither uses it, so the rider is still
true and still not this work item's judgment to make.

## Fed back into the spec

- `docs/worktree-guard-spec.md` gains §*Creation consent — the first creation is
  the question, not every one*, and one row at the top of §B's matrix. Inferred
  during implementation: the four decisions in it (a third directory, the clone
  as the scope, no expiry, a failed creation still records) are `questions.md`
  Q1–Q4, decided here rather than by a policy that existed first, and a planner
  may overturn any of them.
- `hooks/cmdline.py` gains `adds_a_worktree`, which makes "is this segment a
  creation" one reading rather than two. Inferred during implementation: the
  module's docstring already claims ownership of reading a command line, and
  this is the first time two gates needed the same creation test.
