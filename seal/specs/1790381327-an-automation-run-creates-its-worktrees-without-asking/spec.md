# Feature Specification: an automation run creates its worktrees without asking (#604, #8)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask a person is the more expensive. The owner pressed `automation` precisely so nothing else asks; a guard prompt one call later is the failure the goal names |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Four things the build owes: a test seen red, a stated failure direction, a prompt budget, platform honesty. This spec states the direction and the budget below so the pull request inherits them rather than inventing them |
| `docs/worktree-guard-spec.md` §*Premise* | The guard counts **work streams**, not sessions: "how many work streams are actually live on the tree". This is what settles #8 — an `isolation: "worktree"` Agent is a second stream by construction |
| `docs/worktree-guard-spec.md` §*Creation consent* | The consent record's standing — written after the answer, not before the question — is the bar a new consent source has to meet. Its threat model is a session writing consent by habit (`[worktree-ok]` typed on the first attempt), not an adversary editing files: the record itself is one `touch` away |
| `docs/worktree-guard-spec.md` §*Choice sites*, last paragraphs | `[worktree-ok]` and `[shared-tree-ok]` are "an audit trail, not an authorization". Whatever the model writes has that standing, and a `routing.md` is something the model writes |
| `skills/implement/orchestration.md` §*Orchestrator: how the work is routed* | Fixes question 1's three labels — `automation`, `per axis`, `no work item` — which is what makes the owner's answer recognisable in the transcript at all |
| `hooks/routing.py` module docstring, `AUTOMATION` comment | "Nothing gates on it and nothing can". This design keeps that true: the guard reads the person's answer in the transcript, never the `Automation` row of `routing.md` |
| `skills/agent-contract/SKILL.md` §13 | The transcript's shape is a harness fact. Every way of not finding the answer must land on the guard's old behaviour, never on silence |

## The decision this frame makes

### What counts as consent the model cannot forge

Three candidates, judged by who writes the bytes and when. The table extends
the one in `docs/worktree-guard-spec.md` §*Creation consent*.

| | `[worktree-ok]` | `routing.md` reading `Automation \| yes` + `Answer pressed \| automation` | the consent record | the `AskUserQuestion` answer in the transcript |
|---|---|---|---|---|
| written by | the model, in the command | **the model**, with `Write`, then committed by the model | the `PostToolUse` hook | **the harness**, from the person's click |
| written when | before the question | after the answer — but the answer it records is typed by the model | after a creation ran | at the moment the person answers |
| present at the measured moment (2026-09-26, and #604's 2026-09-25) | yes | **no** — the worktrees were created first so each branch could carry its own `routing.md` | no — no creation had run yet | **yes** |
| forgeable by habit | yes | yes: `Answer pressed` is the model's account of a click, and a copied file carries it | no | no: the model writes the question and its options, never which one was pressed |
| forgeable by deliberate file editing | — | — | yes (`touch`) | yes (append to the `.jsonl`) — the same standing as the record |

**The transcript answer is chosen.** It is the only candidate that is both
present when the first `git worktree add` arrives and written by something
other than the model. `routing.md` fails on both counts: it is authored by the
session (committing it changes where it is, not who wrote it), and the
measured order puts the worktrees before the file. Requiring both would
reinstate the prompt for exactly the measured run.

### What exactly is read

An answer counts when **all** of these hold. Each one is a place the reading
can fail, and every failure means *no consent*, which is today's behaviour.

1. **This session's own main transcript.** Resolved as: the payload's
   `transcript_path` when its basename is `<session_id>.jsonl`; otherwise the
   one file matching `~/.claude/projects/*/<session_id>.jsonl`. A subagent's
   tool call carries the parent's `session_id` (#8's measurement), so a
   subagent reaches its parent's answer through the second form. Nothing else
   is scanned — no other session's file, no `subagents/` file.
2. **A harness-written `AskUserQuestion` result.** A `type: "user"` entry whose
   `tool_result` block's `tool_use_id` names an earlier assistant `tool_use`
   with `name: "AskUserQuestion"`, read from the entry's structured
   `toolUseResult.answers`. A Bash result that echoes *The user answered:
   "automation"* has no such link and no `answers` object.
3. **The routing question's shape.** One single-select question in that result
   whose options' leading phrases are exactly `automation`, `per axis` and
   `no work item`, and whose answer's leading phrase is `automation`. The
   leading phrase is the label casefolded and cut at the first ` (`, ` —` or
   ` -`, then stripped.
4. **The same clone.** The result entry's own `cwd` resolves, through
   `optin.git_common_dir`, to the same common git directory as the creation's
   repository. An absent or unresolvable `cwd` is no consent.

Measured 2026-09-26 with a throwaway script over the local transcripts (the
guard itself was not run): across the 38 SpecSeal transcripts (190 MB), the
10 routing answers found all pass rule 3 — seven bare `automation`, and one
each of `automation (권장)`, `automation (Recommended)` and
`automation — 안 멈추고 끝까지`. That scan, with a substring prefilter, took
0.37 s for all 38 files together. Across all 68 local transcripts the largest
file is 17.3 MB and the median 3.7 MB.

### Where it sits in the ladder

Beside the consent record, at row 0 of `guard_worktree_creation`, and with
exactly the record's effect on both entry points:

| Entry point | record **or** automation answer present |
|---|---|
| Bash, command is worktree creation and nothing else | `allow` |
| Bash, command does more | silent |
| Agent/Task `isolation: "worktree"` | silent |

The record is read first because it is one `stat`; the transcript is scanned
only when there is no record. Once the first creation runs, the `PostToolUse`
writer records it, so the scan is paid at most until then.

The switch direction reads neither. An answer that the run should not stop
says nothing about taking another session's branch out from under it — the
same sentence §*Creation consent* already says of the record.

### #8 — the Agent path is judged as concurrent, not counted

An `isolation: "worktree"` Agent runs beside its parent, and the parent's tree
is not switched, so the call is two streams by construction. The session count
cannot see that (a subagent renews its parent's lease and has no id of its
own), and the answer the guard gives on that path today — *call the Agent again
without isolation* — would put the agent in the parent's tree while the parent
works there, which is the mixing the guard exists to prevent.

So the Agent path stops calling `sessions_in_tree` and stops reaching the
choice sites. It has two outcomes:

| Agent/Task `isolation: "worktree"` | Decision |
|---|---|
| record or automation answer present | silent (unchanged for the record) |
| otherwise | `ask` — the first creation of a session is still one confirmation (#237's invariant, untouched). The reason says the agent runs beside this session, so a separate tree is the right shape, and that declining cancels the spawn. It no longer says *single-stream* and no longer recommends dropping `isolation` |

This changes what the guard **measures** on that path, not the confirmation
floor. Lowering the floor for supervised sessions is not asked for by either
issue, and #237's invariant stays whole.

## Scope

**In**

- `hooks/worktree_consent.py`: one reader, beside `granted`, for the
  automation answer, so one module answers *what is consent*.
- `hooks/worktree-guard.py`: row 0 reads record-or-answer; `main` passes the
  payload's `transcript_path`; the Agent path is judged by the two-row table
  above; the `[worktree-ok]` row's first sentence names what was measured
  (*no other Claude session is working in this tree*) instead of asserting
  *single-stream work*, because a worktree a subagent chain will use is
  concurrent work the count cannot see.
- The two riders this touches, both of which say *decide this first if you
  are here*:
  - `main`'s `# RIDER:` on the Agent path (#8's open question) is answered and
    removed.
  - `guard_worktree_creation`'s `# RIDER:` on the unreachable `ask` tail of
    row 0: the tail is removed and `consented` takes only `allow` or `silent`.
    Row 0 is being edited, the rider asks for that decision, and the
    repository's rule is that a branch nothing can make true is a branch no
    case can pin.
- `docs/worktree-guard-spec.md`: §B's table, §*Why the Agent path ends at
  `ask`* (rewritten for the new rule), §*Creation consent* (the fourth column
  above, the prompt budget), §*Choice sites*' "where the token is read from"
  sentence, each new clause with an `Enforced by:` line.
- Tests in `tests/test_the_guard_asks_once_per_session.py` and
  `tests/test_worktree_guard.py`: the Agent-path cases pinned to the old
  steering are rewritten, and the new cases below are added, each seen red.
- The ledger rows these edits drift, re-read and re-stamped in place:
  `seal/releases/0.9.1.md` (`guard_worktree_creation`, `main`) and
  `seal/releases/0.9.4.md` S3/S4. New claims go to
  `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md`.
- `seal/specs/<this item>/changelog.md` fragment.

**Out, with the reason**

- **`per axis` with the first box ticked.** The tree says it is the same
  promise (`Automation` = `yes`), but the box label is not recognisable: in
  4 of 4 measured per-axis answers the orchestrator had reworded or translated
  it (`멈추지 않고 끝까지 실행`, `End to end`, …), while the preset matched
  10 of 10. Excluding it keeps today's one prompt for those runs and makes
  nothing worse. Q1 in `questions.md`.
- **The `routing.md` reading.** Rejected above; not a fallback either,
  because a fallback the model can satisfy by writing a file is the
  `[worktree-ok]` standing under another name.
- **`permission_mode` in the payload** (auto or bypass mode as consent). It is
  the person's setting, but it answers *who judges permissions*, not *may this
  run split the clone*; it would silence the guard in every auto-mode
  session, supervised ones included. In `plan.md`'s Alternatives.
- **A switch written after a creation in one command is never judged.** `main`'s
  walk sets `reason` from the first classifying segment and skips later
  non-creating segments, so `git worktree add … && git switch x` goes silent
  whenever consent is present — including over another session's ACTIVE tree.
  This predates this work (it holds for every session with a record since
  #257, `seal/releases/0.9.4.md` S3), and its fix belongs to the walk, not to
  what counts as consent. This work widens the population that reaches it to
  the first creation of an automation session, so it is named here and in
  `questions.md` (Q3) for the orchestrator to file.
- **`CLAUDE.md` and `templates/claude-md-block.md`** say *concurrent
  sessions*. The hook's authority is `docs/worktree-guard-spec.md`, whose
  Premise says streams; rewording the block every install copies is the
  owner's call. Q2.
- **The single-stream `deny` text on the Bash path**, the choice sites, the
  `[shared-tree-ok]` direction, leases and the activity heuristics: untouched.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the measured run | Given a session transcript holding a routing `AskUserQuestion` result answered `automation (Recommended)` from this clone's `cwd`, no consent record, a clean single-stream tree · When one Bash call runs two `git worktree add` lines and a `git switch -c` ending in `# [worktree-ok] …` · Then the guard emits nothing | test: fixture transcript copied from the measured entry's shape; raw stdout empty; seen red against the current code (which answers `ask`) |
| S2 bare creation | Same transcript, `git worktree add ../wt -b x` alone · Then `allow` | test, seen red (current: `deny`) |
| S3 Agent path with the answer | Same transcript, Agent `isolation: "worktree"` · Then silent | test, seen red (current: `ask`) |
| S4 no answer, Agent path | No record, no answer, any tree state (single-stream, idle, unreliable, active) · Then `ask`, the reason names the agent running beside the session, contains neither *single-stream* nor an instruction to drop `isolation`, and `sessions_in_tree` is not called | test over the four states, seen red (current: choice deny at idle/unreliable, *single-stream* text) |
| S5 no answer, Bash | No record, no answer · Then every Bash row is exactly as today | the existing suite for `test_worktree_guard.py` and `test_the_guard_asks_once_per_session.py` passes unchanged except the cases listed as rewritten |
| S6 forged by the model | Transcript where the only *automation* text is (a) an assistant message, (b) a Bash `tool_result` echoing *The user answered: "automation"*, (c) an `AskUserQuestion` result answered `per axis`, (d) one answered `automation` to a question whose options are not the routing three · Then no consent in all four | test, four cases; (b) and (d) seen red by weakening the id link and the option-set check respectively |
| S7 other session, other clone | The answer sits in another session's transcript, or in this session's but with a `cwd` in a different clone · Then no consent | test |
| S8 unreadable | No transcript, unreadable file, malformed JSON lines, a `toolUseResult` without `answers` · Then no consent and no traceback; stdout carries the old verdict | test |
| S9 switch direction | Answer present, `git switch x` in a tree with an ACTIVE session · Then `deny` exactly as today | test |
| S10 messages | The `[worktree-ok]` row's reason starts from what was counted, and the Agent `ask` reason is pinned, in both `LANG`s | test pins the new text (§14) |

## Data & interfaces

- Hook payload field read, new to this repository: `transcript_path`
  (PreToolUse). Its absence is handled by rule 1's second form. Whether a
  subagent's payload carries the parent's path or its own is `questions.md`
  Q4, and either answer lands on rule 1's second form.
- Transcript entry fields read, shape measured on 2026-09-26 in
  `~/.claude/projects/-Users-yc-Documents-GitHub-SpecSeal/b78a324d-861d-4c95-bae1-286a9cb2f052.jsonl`
  (the orchestrator's own session): assistant `message.content[]` items of
  `type: "tool_use"` with `id`, `name`; user entries with
  `message.content[]` items of `type: "tool_result"` with `tool_use_id`,
  plus top-level `cwd`, `toolUseResult.questions[]` (`question`,
  `options[].label`, `multiSelect`) and `toolUseResult.answers`
  (`{question text: chosen label}`; a multi-select answer is the chosen labels
  joined by `, `, measured in four other transcripts).
- No file format of this repository changes; no new record is written.

## Open questions → questions.md

Four rows, none of which blocks the build: two for a person (Q1, Q2) with
defaults the build proceeds on, one for the work that the orchestrator files
as an issue (Q3), and one measurement the design does not depend on (Q4).

Framed 2026-09-26 by framer, before the build.
