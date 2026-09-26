# Implementation Plan: an automation run creates its worktrees without asking (#604, #8)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-26 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

The worktree guard gains a second consent source beside the consent record:
the person's `automation` answer to the routing question, read from this
session's own transcript, where the harness wrote it. Row 0 of
`guard_worktree_creation` reads record-or-answer, with the record's existing
effect on both entry points. Separately, the Agent `isolation: "worktree"`
path stops counting sessions (#8): it is concurrent by construction, so it
asks once per session or is silent under consent, and never steers the agent
into the parent's tree. `spec.md` holds the decision table and the reading
rules; this file holds the order and the alternatives.

## Technical context

Code this builds on, by content anchor (a line number moves for unrelated
edits):

- `hooks/worktree-guard.py#guard_worktree_creation` — row 0 is the
  `worktree_consent.granted(top, session_id)` block; the unreachable `ask` tail
  under its `# RIDER:` is removed here. The `[worktree-ok]` row (`if user_ok:`)
  gets its first sentence reworded.
- `hooks/worktree-guard.py#main` — the `if tool in ("Agent", "Task"):` block
  carries #8's `# RIDER:` and is rewritten to the two-row rule; the Bash path
  passes `data.get("transcript_path", "")` down through `judge_creation`.
- `hooks/worktree-guard.py#judge_creation` — gains the transcript argument and
  nothing else.
- `hooks/worktree_consent.py#granted` — the new reader sits beside it and
  resolves the clone through `optin.git_common_dir`, the way `consent_path`
  does.
- `hooks/worktree-guard.py#last_user_snippet`, `#transcript_idle_minutes` —
  existing transcript readers; they locate files by `project_slug(cwd)`, which
  is wrong for a session whose cwd is a linked worktree. The new reader does
  not reuse that lookup (spec rule 1).
- `skills/implement/orchestration.md` §*Question 1 — single-select* — the three
  labels the reader matches. A test pins the reader's constants against that
  table, so relabelling the question turns a case red instead of quietly
  bringing the prompt back.

Constraints the build must respect:

- `CONTRIBUTING.md` §*What a change to a gate must carry* — every new case seen
  red; the PR body carries the failure direction and prompt budget below.
- `skills/agent-contract/SKILL.md` §13 — every way of not finding the answer
  lands on today's verdict. §14 — the two reworded messages are pinned in the
  same commit as the change.
- The riders: both `# RIDER:` comments this work reaches are resolved and
  deleted, not re-stamped. `rider_check.py` reads what remains.

**Failure direction, for the PR body.** The change allows more, in two
places: a creation in a session whose person pressed `automation`, and the
Agent path no longer denying once at the two choice sites. Both are the cheap
direction here. A wrong allow on worktree CREATION produces a folder and a
branch; it touches no existing tree. The direction whose wrong allow breaks
another session's tree is the switch, and neither consent source reaches it.

**Prompt budget, for the PR body.** A session whose person pressed
`automation`: zero guard prompts for worktree creation, from one per session.
Any other session: one per session on the Bash path, as today; one per
session on the Agent path, from one plus a choice-site deny round trip in the
idle and detection-unusable states.

**What breaks in six months.** The harness renames `toolUseResult` or
`answers`, or moves transcripts. The reader then finds nothing and the prompt
comes back — once per session, the pre-change cost — and nothing turns red,
because the fixture pins the shape measured today rather than the harness's.
The one drift the tree can catch is its own: the orchestration doc relabelling
question 1, which the label pin catches.

**Platform honesty.** Transcript location is `~/.claude/projects/` through
`os.path.expanduser`, plus the payload's `transcript_path`. Measured on macOS
only. Windows and Linux are unverified; the answerer is the CI matrix for the
fixture cases, and nobody for a live Windows transcript.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. The `AskUserQuestion` answer in this session's transcript** (chosen) | The harness changes the transcript shape; the prompt returns at the old cost. Deliberate editing of the `.jsonl` forges it — the same standing as `touch`ing the consent record | Chosen: the only source both present at the measured moment and written by something other than the model |
| B. A committed `routing.md` reading `Automation \| yes` and `Answer pressed \| automation` | The model writes every byte of it, so it is `[worktree-ok]` in a file. And in both measured runs the worktrees came first, so each branch could carry its own `routing.md`: the file was absent when the guard asked. Which branch's file would authorise a creation made from the release branch is a question with no answer | Rejected |
| C. Require both A and B | Reinstates the prompt for exactly the measured order | Rejected |
| D. Accept either A or B | B's half is satisfiable by the model writing a file, so the guard is as strong as its weaker half | Rejected |
| E. `permission_mode` (auto or bypass) as consent | It says who judges permissions, not whether this run may split the clone. It would silence the guard in every auto-mode session, supervised ones included, and its values are unmeasured here | Rejected. NAME NOT IN TREE: a harness payload field this repository never reads |
| F. The orchestrator asks one more question, *may this run create worktrees?* | A second click for an answer already given; `automation`'s description says nothing stops to ask again, and adding a box breaks question 2's four-option ceiling | Rejected |
| G. A `PostToolUse` hook on `AskUserQuestion` writes the consent record when the answer is `automation` | Structurally tidy: no transcript scan, the guard reads only `granted()`. But the `PostToolUse` payload's `tool_response` shape for `AskUserQuestion` has never been captured in this repository, and a subagent has no `AskUserQuestion`, so `smith` cannot capture it or see a case red against it. It also makes the record mean two things | Rejected for this work. Worth revisiting once a real payload is on disk; the transcript shape is measured today |
| #8-i. Keep counting sessions on the Agent path | Keeps telling the model to drop `isolation`, which would put the agent in the parent's tree while the parent works — the mixing the guard exists to stop | Rejected |
| #8-ii. The Agent path is always silent | Lowers #237's floor (*the first creation of a session takes one confirmation*) for supervised sessions. Neither issue asks for that | Rejected |
| **#8-iii. Concurrent by construction: ask once per session, silent under consent** (chosen) | A supervised session still pays one prompt for its first isolated agent, which is today's floor | Chosen: it changes what is measured, not the floor |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The reader, in `hooks/worktree_consent.py`: spec rules 1–4, fail-closed on every unreadable shape. A fixture builder in the test file producing transcript lines shaped like the measured entry. The projects root is one module constant the tests point at a temporary directory, so no case can read a real transcript on the machine running it. The label pin against `orchestration.md`'s Question 1 table | spec S6, S7, S8 as unit cases on the reader; (b) seen red by dropping the `tool_use_id` link, (d) by dropping the option-set check, S7 by dropping the clone check; the label pin seen red by editing a constant | d94793bc |
| 2 | Row 0 reads record-or-answer on both entry points; `main` and `judge_creation` carry `transcript_path`; the unreachable `ask` tail and its rider are removed and `consented` takes `allow` or `silent` only. `docs/worktree-guard-spec.md` §B row 1 and §*Creation consent* (the fourth column, the budget) updated with `Enforced by:` lines | S1, S2, S3, S9 through `wg.main()`, each seen red against the phase-1 tree; S5 is the two guard test files passing with no edit outside the cases this phase rewrites | e7a7d643 |
| 3 | #8: the Agent path's two-row rule, no `sessions_in_tree` call, new `ask` reason; #8's rider removed. The `[worktree-ok]` row's first sentence reworded. `docs/worktree-guard-spec.md` §B's Agent rows and §*Why the Agent path ends at `ask`* rewritten; §*Choice sites*' "Where the token is read from" sentence re-pointed. The Agent-path cases in `tests/test_worktree_guard.py` that pin the old steering (`test_the_agent_prompt_names_the_way_on_an_agent_has` and neighbours) rewritten to the new text | S4 over four tree states, seen red against the phase-2 tree; S10 pins both reasons in both `LANG`s; `test_the_agent_verdict_does_not_depend_on_the_prompt` still passes unchanged | 484326f3 |
| 4 | Ledger: re-read and re-stamp the drifted rows in `seal/releases/0.9.1.md` and `seal/releases/0.9.4.md` (S3, S4; row 142's *the Agent path still asks* stays true and is re-read, not corrected); new claims in `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md`; `changelog.md` fragment | `evidence-check` on the ledger files; `rider_check.py` shows the two riders gone and nothing new | |

The broad gate is not in this table: it is the sealer's, once, after the
review rounds settle.

## Operational impact

- No new dependency, environment variable or file format; no record is written
  that was not written before.
- A new payload field is read (`transcript_path`), and its absence is handled.
- Cost: one transcript scan, only for a creation with no consent record, and
  only until the first creation runs and the writer records it. Measured: a
  prefiltered scan of 38 transcripts (190 MB together) took 0.37 s; the
  largest single local transcript is 17.3 MB.
- Behaviour change a user sees: after pressing `automation`, no guard prompt
  for worktree creation; an isolated Agent is never told to drop `isolation`.
