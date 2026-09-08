# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `gh issue view 237`; `CONTRIBUTING.md` §*What a change to a gate must carry*; `CLAUDE.md` §*The goal a design is chosen against*; `docs/worktree-guard-spec.md` §B, §Choice sites; `skills/agent-contract/SKILL.md` §§2, 9, 12, 13, 15; `hooks/worktree-guard.py`'s module docstring and `has_token`'s; `seal/config.md` (no `Record language` row → English); `seal/follow-up.md`
· evidence: 9 rows over 7 coordinates in `seal/ledger/1788817291-the-guard-asks-once-per-worktree-not-once-per-session.md`, all `Executed`; `hooks/dispatch.py#GROUPS` re-verified in `seal/ledger.md` (`b3d45306 -> a5e67d2c`)
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
| What *nothing else* is asked of | The build asked it of the COMPOUND — is every segment a `git worktree add` | Asked of the SEGMENT too: `git` is its own command word, and no token carries `$`, a backtick, `<` or `>` | Round 1 executed eleven single-segment shapes that were allowed anyway, two of them in a real shell where the substitution created its marker and the redirection truncated a file. The docstring already claimed this bound; the code did not enforce it |
| Which verdict a command holding both a switch and a creation gets | Round 1's paste-ready fix makes the creation OUTRANK the earlier verdict | The switch ladder keeps its three concurrency verdicts, and the creation is judged below them and above the two rows that protect no tree — the tracked-changes `ask` and the silent single-stream exit — plus the earlier `if not top` | Outranking turns a switch denied under an ACTIVE session into an `ask` about the creation — the branch is still taken out from under that session, one approval later. Pinned by `test_the_switch_ladder_keeps_every_verdict_it_had`, which goes red under the alternative (executed). Where the fall-through SITS was found the same way: placed at the ladder's end it left row 3 in front of it, and approving *the uncommitted changes will follow you* created the worktree — so a dirty tree decided whether the creation was questioned. `test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned` pins that, and goes red with the fall-through moved back to the end |
| Two checks from round 1's paste-ready fix | `cmdline.understood(tokens)` and an `Unresolved` in `wheres` | Neither kept | Mutation-tested one at a time: deleting either left every case green. The command-word test subsumes both and is strictly stronger — `understood` answers True for `time git worktree add …` where the command-word test answers False, and an `Unresolved` cannot occur at all, because a segment that would produce one is not a creation and fails `adds_a_worktree` first. This repository removes a condition no case can pin (the row above) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and the typecheck | the orchestrator's broad gate, run once after the rounds settle (`agent-contract` §2) |
| Behaviour on Linux and on Windows — nothing here reads a process, but `os.makedirs`, `open`, `os.path.isfile` and `git rev-parse --git-common-dir` all run | CI's Linux and Windows legs on the pull request |
| That a hook `ask` cannot be auto-answered, and that a `PostToolUse` payload means the call ran — the two harness facts the design rests on. `--dangerously-skip-permissions` exists today, so the first half is a question about the present, not about a future harness | **the repository owner**, against the harness. It closed with *the same standing every gate in this repository has*, which names nobody — and this is the row that least tolerates that, because the two facts in it are the whole foundation of the change (round 1, finding 5) |
| Whether a `permissions.deny` rule outranks a hook `allow` — if it does not, a user who explicitly denied `git worktree add` would be overridden after their first approval. Round 1 widened what rides on this: findings 1 and 3 were about how much else an `allow` was covering | **the repository owner**, or a run against a settings file carrying such a rule. `pr-notes.md` §4 says what the guard does if the answer is the unfavourable one |

## Not done

**A creation carrying an expansion, a redirection or a wrapper is left at one
prompt each too.** `git worktree add <path> $(…)`, `… > <file>`, `sudo git
worktree add …` and the eight other shapes round 1 found now answer `ask`
rather than `allow`. Widening any of them means deciding what else a worktree
consent may speak for, which is the same question the paragraph below leaves
open. Nobody writes a worktree creation in those shapes, so the budget is
unaffected.

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

**Four red cases in `tests/test_the_records_can_be_carried_out_and_in.py` were
left alone**, because they are red at the base commit too. Executed: at
`86e140f`, detached, the module reports `4 failed, 74 passed` —
`test_a_link_at_the_partial_name_refuses_the_export`,
`test_a_file_at_the_partial_name_survives_the_refusal`,
`test_the_export_refuses_the_link_where_o_excl_does_not_catch_it` and
`test_a_broken_link_at_the_zips_own_name_is_not_a_free_name`. They are about
`seal` export/import and nothing here touches it. It is a follow-up for the
orchestrator to file rather than a defect for this branch to chase, and fixing
it here would be scope this work item did not ask for.

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
