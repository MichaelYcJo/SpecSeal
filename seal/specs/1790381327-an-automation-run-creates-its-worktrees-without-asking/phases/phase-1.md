# 1790381327-an-automation-run-creates-its-worktrees-without-asking — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d94793bc |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The reader, in `hooks/worktree_consent.py`: spec rules 1–4, failing closed on
every unreadable shape. A fixture builder in the test file that writes
transcript lines in the measured shape. The projects root as one module
constant the tests point at a temporary directory. The label pin against
`skills/implement/orchestration.md`'s Question 1 table. Verified by S6, S7 and
S8 as unit cases on the reader, with (b) seen red by dropping the
`tool_use_id` link, (d) by dropping the option-set check, S7 by dropping the
clone check, and the label pin by editing a constant.

## What this phase found

**Does the frame hold? Mostly, with four gaps the build absorbs rather than
routes back.**

- The frame names two test files for the Agent-path rewrite.
  `tests/test_worktree_guard_signals.py` is a third one:
  `test_agent_isolation_worktree_concurrent_asks` asserts that the Agent
  path's reason lists the ACTIVE session, which phase 3 removes because that
  path stops calling `sessions_in_tree`. Phase 3 rewrites it with the others.
- `docs/worktree-guard-spec.md` §B row 1 says the guard answers **ask** where
  a command does more than create a worktree. The code has answered `silent`
  since #257 (`seal/releases/0.9.4.md` S3). The module docstring of
  `hooks/worktree-guard.py` carries the same stale `ask`. Phase 2 edits that
  row anyway, so it corrects both.
- `seal/releases/0.9.1.md`'s `judge_creation` row cites a unit phase 2 changes
  (it gains the transcript argument). The plan names the `guard_worktree_creation`
  and `main` rows and not this one. Phase 4 re-reads it with the others.
- The frame says the Agent path passes `single_stream="ask"` and the two
  `shared_*` arguments. Once phase 3 stops routing the Agent path through
  `guard_worktree_creation`, no caller passes any of the three, so they become
  parameters nothing can set. Phase 3 removes them for the rule the rider
  already states: a branch nothing can make true is a branch no case can pin.

**The constant alone does not keep a case off real transcripts.** The guard
imports `worktree_consent` by its plain name, so the copy it reads is
`sys.modules["worktree_consent"]`. A test's own `load_hook_module` copy is a
different module object. `tests/conftest.py` gained an autouse fixture that
points the `sys.modules` copy at an empty directory for every in-process case.
Cases that run a hook as a subprocess still see the real `~/.claude/projects`,
and none of them uses a session id that names a real transcript (`me`, `ag`,
`s-intact` and similar).

**Two strictness choices, both fail-closed.** `multiSelect` must be `False`,
not merely absent, because an absent field is a shape nobody measured. The
`tool_use` must come before its result, which the single pass enforces by
construction; there is no separate check for it, so it has no mutation of its
own.

**Any matching answer counts, not the latest.** The spec says an answer counts
when all four rules hold, and a later `per axis` answer does not revoke an
earlier `automation`. That matches the record's standing: once written, it is
never revoked either.

**Seen red.** Against the pre-change module (`a0eaeea9`) all 17 new cases fail
(16 errors at fixture setup, where `PROJECTS_ROOT` does not exist, and the
label pin failing on the missing constant). Then one mutation at a time on the
new module, each turning exactly its case red:

| Mutation | Red case |
|---|---|
| drop the `tool_use_id in asked` link | `test_a_result_not_linked_to_an_ask_is_not_consent` |
| drop the option-set check | `test_automation_on_another_question_is_not_consent` |
| clone check always true | `test_an_answer_given_in_another_clone_is_not_consent` |
| `per axis` → `per-axis` in `ROUTING_LABELS` | `test_the_labels_match_the_routing_question_the_orchestrator_asks` |
| no decoration cut in `leading_phrase` | `test_the_routing_preset_is_consent` |
| first of many glob matches | `test_two_transcripts_for_one_session_are_none` |
| ignore the payload's `transcript_path` | `test_the_payloads_transcript_path_is_read_when_it_names_this_session` |
| drop the `multiSelect` check | `test_a_multi_select_routing_shape_is_not_consent` |

**A hazard for the next phase.** This session's `PostToolUse` formatter runs
after every edit and removed `import glob`, added one edit before its first
use. Add an import in the same edit as its first use.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
