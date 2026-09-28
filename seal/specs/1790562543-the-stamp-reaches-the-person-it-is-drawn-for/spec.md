# Feature Specification: the sealer's stamp reaches the person it is drawn for

<!-- seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #400, milestone 50 (0.15.7), item D. The owner's decision of 2026-09-28
(the issue's last two comments) overrides the body and every earlier comment
where they disagree: **the gate draws nothing in a sealer; the main session
draws once, from a file the gate wrote; and the drawing is the last thing on
the screen.**

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-broad-gate.md` §*One act, one owner, and the owner is an agent* | The run stays the sealer's. The orchestrator never takes it to get a terminal, and the drawing moves while the run does not |
| `skills/agent-contract/SKILL.md` §2 | Same, from the contract. It is also why issue #400's route *the orchestrator runs the gate itself* is closed on policy as well as by measurement |
| `docs/the-broad-gate.md` §*A document that its own work item's fixes disproved is corrected in the same work item* | Four documents say where the disc is drawn, and this work makes each of them false. They are corrected here (§Scope) |
| `skills/verify/SKILL.md` §*Every agent seals what it verified, and one of them is final*, the **Form** bullet | "`broad-gate` prints the disc on success alone, so seeing the drawing means the last seal was earned." The property is kept and its mechanism changes. Only a green run with a written cell writes the values, and only those values are drawn |
| `skills/verify/SKILL.md` §*Counterfeits*, and `templates/config.md`'s refusal of a default `Broad gate` row | A drawing over no run is the counterfeit. `bin/seal-stamp`'s sample must not become the cheap way to satisfy the new rule (issue body §*The forgery this must not open*) |
| `CLAUDE.md` §*The goal a design is chosen against* | The trigger is mechanical: the gate writes, a hook draws. No session act sits between them, so the run stays unattended |
| `hooks/implementer.py` module docstring (the stance) | A mark catches a session that forgets. It does not stop an adversary. A values file somebody writes by hand is outside what this defends (§*What cannot be checked*) |
| `hooks/console.py` | Owns the stream-encoding decisions every new entry point repeats. The new hook follows it |

## What was measured before the frame, and by whom

| Fact | Label | Where |
|---|---|---|
| A tool call has no controlling terminal: `/dev/tty` fails with `device not configured`, and stdout is a UTF-8 non-tty | executed, 2026-09-15, by the owner's session | issue #400, comment *The blocking measurement* |
| A sealer's message into main renders folded behind `ctrl+o` | executed, 2026-09-15 | issue #400, comment *Second measurement* |
| A Bash result renders truecolour and folds at a few lines | executed + seen by the owner | issue #400 body, table |
| A `Stop` hook's JSON `systemMessage` renders **unfolded, in truecolour, after the turn's final text**, and before the *Waiting for N background agents* footer. The harness styles the message's **first line** as a dim label, `Stop says: <line 1>`. The drawing started on line 2 | executed 2026-09-28 by the orchestrator's probe D; read from the owner's screenshot | the probe script `…/scratchpad/probe/probe.py`, the `stop-json` mode; relayed to this framer |
| Of the four probe variants, three rendered. Which one failed was not said | read, the owner's words | relayed |
| No probe output entered the model's context in the next turn | executed/observed by the orchestrator | relayed. **Not re-measured for the D-only re-probe** (questions.md Q1) |
| A subagent's Bash environment carries `CLAUDE_CODE_SESSION_ID`, and its value is the **parent** session's id: the same id that names the parent's scratchpad directory | executed, in this framer (a subagent), Claude Code 2.1.283 | `env` in this session. The variable is **not documented**: the hooks reference says the session id arrives on stdin |
| Tool events (`PostToolUse`) fire inside subagents, and their payload then carries `agent_id` and `agent_type`. `Stop` is "when Claude finishes responding" and `SubagentStop` is "when a subagent finishes". `Stop` payloads carry `session_id` and `cwd` | read, code.claude.com/docs/en/hooks, 2026-09-28, through a summarising fetch | The fetch's paraphrase of what `systemMessage` does on `Stop` contradicted itself between two reads, so the probe governs that point and the docs do not |

## Scope

**In.**

1. **The gate signals and does not draw, where stdout is not a terminal.** On
   a sealed run with `--record`, after the cell is written, `broad_gate.py`
   writes the panel's rows to one values file and prints one `SEALED` line
   naming it. It draws no disc and no letter twin. This covers the sealer's
   run and every other piped run.
2. **A hand-run in a real terminal draws exactly once, as today.** The form is
   chosen by `pick_shape`, and no values file is left for anyone else to
   draw. This path cannot be reached from a tool call (measured above), so it
   cannot become an agent's cheap path.
3. **`seal_stamp.py` reads a values file.** A reader function and a `--from
   <file>` input draw that run's rows. Drawing claims the file first, so a
   drawn file is never drawn again. `seal-stamp` with no arguments still
   draws the sample, unchanged.
4. **A `Stop` hook draws, in the main session only.** A new hook, registered
   under a new `stop` group of `hooks/dispatch.py` and a `Stop` entry in
   `hooks/hooks.json`, draws every undrawn values file of its own session.
   It uses block form, the file's scale, and a JSON `systemMessage`. Line 1
   is a label that says what was sealed. It draws nothing when the payload
   names an `agent_id`, so the sealer's own end never draws.
5. **Scale 0.90 is the default**, as one constant in `seal_stamp.py` with the
   reason beside it and the 0.75 candidate that was passed over. Both CLIs
   (`seal-stamp` and `broad-gate`) take their `--scale` default from it.
6. **The words that the change makes false are corrected in the same work
   item**, and the rule for the orchestrator is written where closing rules
   are read:
   - `agents/sealer.md`: §*The command* (the exit-0 bullet, and the paragraph
     saying the drawing arrives as letters), and nothing in §Report. The
     issue body says §Report needs no change, and the gate's output, whole
     and unedited, now carries the `SEALED` line.
   - `skills/code-review/orchestration.md` §*Orchestrator: the pull request
     opens before round 1, and a phase is re-run*: the closing rule.
   - `skills/verify/SKILL.md` §*Every agent seals…*: the **Form** bullet.
   - `docs/the-broad-gate.md`: one new policy paragraph, carrying the spec
     marker and an `Enforced by:` line, plus a statement of what cannot be
     checked.
   - `skills/verify/scripts/broad_gate.py` module docstring (*Printed on
     success only…*, and the usage line's `--scale 1.0`).
   - `skills/verify/scripts/seal_stamp.py` module docstring (*The gate
     imports…*), and `bin/seal-stamp`'s usage comment.

**Out, and why.**

- **The failure form.** `NOT SEALED` with no picture is unchanged, and the
  issue body says it is not reopened.
- **The drawing, the palette and the chart.** The issue's §*Not this* rules
  them out.
- **An emoji form or a pull-request destination.** Both were withdrawn by the
  owner.
- **The order of `agents/sealer.md` §Report.** The 2026-09-15 comments asked
  for the stamp to come last in the report, and the body superseded that.
  The report carries no drawing now.
- **Relabelling `seal-stamp`'s sample as `SAMPLE`.** It was the cheap path
  only while the rule said *end with the stamp*. The rule now asks no session
  to draw anything, so there is nothing for the sample to counterfeit.
- **Pruning drawn values files.** They accumulate under the git common dir,
  as `specseal-implementer-notice/` markers already do. This is a named cost,
  not a defect.
- **Arming at `SubagentStop`** to close the early-draw window
  (plan.md §*Technical context*). It is deferred unless the window is
  observed.
- **Windows rendering of the block form through the hook.** No Windows
  session exists here (questions.md Q4).
- **`round_record.py` and `chain_check.py`.** The cell's format and its
  readers do not change. The values file is not a record.
- **The READMEs** (`README.md` row 43 and `README.ko.md` row 41). Checked:
  both describe the sealer as running the gate and writing the cell, and
  neither says where the stamp is drawn. The other documents that name the
  stamp's drawing were found by `git grep` for `stamp|drawing|drawn|disc`
  over `docs/`, `agents/`, `skills/*/SKILL.md`, `skills/*/orchestration.md`,
  the READMEs, `CONTRIBUTING.md` and `templates/`. They are the six in item 6.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | A sealer seals | Given a repository with a `Broad gate` row, a work item whose last record has `Pass` ticked, and `CLAUDE_CODE_SESSION_ID` set, when `broad-gate --base b --record <item>` runs with stdout a pipe and every check green, then it exits 0, the cell is written, exactly one values file exists under `<git-common-dir>/specseal-stamp/<session>/`, stdout carries exactly one line starting `SEALED` that names the tree, the base commit and that file's path, and stdout carries no disc (no half-block, no SGR sequence, no twin row) | a case driving the gate as a subprocess (the existing `run_gate` shape) |
| S2 | The file holds this run's panel | Given S1, then the file's rows equal `panel(tree, base, checks, item, workflow, gate_copy(root))` for that run: `SEALED`, tree, base, from, gate, suite, row, ledger, chain, workflow where present, and rounds. It also holds the scale the run was given | a case comparing the file against `panel` on one fixture |
| S3 | The main session's turn ends | Given one undrawn values file for session X, when the hook receives a `Stop` payload with `session_id` X and no `agent_id`, then it prints one JSON object whose `systemMessage` has line 1 as a label naming what was sealed (not blank) and, from line 2, `seal_stamp.stamp(rows, scale, shape=False)` (the block form, with SGR sequences), and the file is marked drawn | a hook case through `dispatch.py stop` |
| S4 | It draws once | Given S3 has run, when a second `Stop` arrives for X, then nothing is printed | same case, second call |
| S5 | The sealer's own end | Given an undrawn file for X, when the payload carries an `agent_id` (a subagent), or `hook_event_name` is not `Stop`, then nothing is printed and the file stays undrawn | hook case |
| S6 | Another session's run | Given an undrawn file for session Y, when a `Stop` for X arrives, then nothing is printed and Y's file is untouched | hook case |
| S7 | A red run | Given a failing check, when the gate runs, then it exits 1, prints the `NOT SEALED` form, writes no values file, and draws nothing | existing `NOT SEALED` cases, plus an assertion that no values file exists |
| S8 | A refused seal | Given `round_record.py seal` refuses, or its post-write chain check fails (exit 2 either way), then no values file is written and nothing is drawn | a case on the existing refusal fixtures |
| S9 | No record named | Given a green piped run without `--record`, then it exits 0 with no values file, no disc, and one `SEALED` line saying that nothing was recorded, so nothing will be drawn | case |
| S10 | A person's terminal | Given stdout is a UTF-8 terminal and a green `--record` run, then the gate draws the stamp **exactly once** on that terminal and leaves no undrawn values file | a pty case (POSIX; skipped where `pty` is unavailable), counting `SEALED` panels |
| S11 | Drawing a file by hand | Given an undrawn values file, when `seal-stamp --from <file>` runs, then it draws that run's rows and marks the file drawn. Run again, it refuses with one sentence and exit 2 | case |
| S12 | The sample is unchanged | `seal-stamp` with no arguments prints `SAMPLE_ROWS` exactly as before, apart from the scale default | the existing `test_the_command_piped_prints_the_twin` |
| S13 | The scale | `seal_stamp.DEFAULT_SCALE == 0.90`. Both CLIs' `--scale` defaults read it, and the constant's comment names the 0.75 candidate and why it was passed over | case, and the comment read in review |
| S14 | No session to draw it | Given a green `--record` piped run with `CLAUDE_CODE_SESSION_ID` unset, then the file is written where no hook draws it, and the `SEALED` line says so and names `seal-stamp --from <path>` | case |
| S15 | The file cannot be written | Given the values directory is unwritable, then the gate still exits 0 (the cell is written and the checks passed), and says on stderr that the values could not be written, so nothing will be drawn | case |
| S16 | The rule is where it is read | `skills/code-review/orchestration.md` says the stamp is drawn for the orchestrator at the end of its turn, that its result text comes first, and that it never draws one itself, with `seal-stamp` and a relayed sealer log both named. `agents/sealer.md` says the gate draws nothing in a sealer | document-pin cases (contract §14), each seen red with its sentence deleted (§15) |
| S17 | Seen on the person's screen | Given a real sealer run in a release, the owner sees the stamp after the orchestrator's text, unfolded and in colour, once | **Cannot be a case.** Read by the owner on the first real run (§*What cannot be checked*) |

## Data & interfaces

**The values file.** One per sealed, recorded, piped run, at
`<git-common-dir>/specseal-stamp/<session-or-none>/<epoch>-<tree>.json`.
It uses the **common** dir because the sealer's `--root` is a linked
worktree while the orchestrator's `cwd` may be the main checkout (it is,
in this very run). The common dir is the one place both resolve alike, and
`hooks/implementer.py#git_dir` shows why a built `<root>/.git` path is wrong
in a worktree. The JSON holds at least:

```json
{"tree": "<short sha>", "base": "<commit>", "from": "<ref>",
 "item": "<abs item dir>", "session": "<id or null>", "scale": 0.9,
 "rows": [["SEALED", ""], null, ["tree", "…"], …]}
```

`rows` is exactly what `panel()` returned, with `None` as `null`. It is the
source of the drawing, and nothing re-derives it.

**Drawn state.** Drawing renames `X.json` to `X.drawn.json` with
`os.replace` **before** printing. So two concurrent `Stop` hooks draw it at
most once, and a crash between the rename and the print loses that one
drawing rather than repeating it.

**The signal line** (stdout, one line, piped runs): it starts with `SEALED`,
carries `<tree> against <base commit>`, and names the file's path. Where no
session was found, it says so and names `seal-stamp --from <path>`. It
mirrors the failure form's `NOT SEALED   <tree> against <base>`. Existing
assertions of `"SEALED" in stdout` keep holding, and assertions of panel rows
on a pipe do not (plan.md Phase 1).

**The hook's output.** `{"systemMessage": "<label line>\n<stamp lines…>"}`.
The label line is styled by the harness as `Stop says: …`, so it names what
was sealed: `SEALED <tree> against <base> · <work item id>`. Several files in
one turn come out as one message, oldest first, each stamp whole.

**Registration.** `hooks/hooks.json` gains `"Stop": [{"hooks": [{"type":
"command", "command": "python3 … dispatch.py stop || py -3 … dispatch.py
stop"}]}]`, in the existing shape. `hooks/dispatch.py#GROUPS` gains
`"stop": ("sealer-stamp.py",)`.

**Ledger anchors this work drifts.** They are re-read in the files that hold
them, per `CLAUDE.md` §*a change writes fragments*:
- `broad_gate.py#gate`: `seal/releases/0.10.0.md`, `0.12.0`, `0.12.2`, `0.15.4`
- `hooks/dispatch.py#GROUPS`: `0.4.0`, `0.9.1`
- `agents/sealer.md#"## The command"`: `0.12.0`, `0.12.2`, `0.15.1`, `0.15.3`
- `seal_stamp.py#main` and `skills/verify/SKILL.md#"## Every agent seals…"`: `0.10.0`

`evidence-check` names the exact set after the edit.

## What cannot be checked, stated so nobody mistakes it for enforced

- **What the person sees.** No case, hook or CI job can observe the screen.
  The cases prove that the hook emits the right bytes under the right
  payload. The owner's screenshot of probe D proves that such bytes render.
  Whether a given run's stamp was seen is read by the owner and by nobody
  else (S17).
- **That the orchestrator's text comes first.** The hook fires at `Stop`,
  which is after the turn's final text by construction, and probe D showed
  that order. What no case can show is that the orchestrator wrote its result
  text in that turn rather than a later one. That part is an instruction
  (S16), not a check.
- **A values file written by hand** into the pending directory would be
  drawn. This is the stance in `hooks/implementer.py`: the mechanism catches
  a session forgetting, not an adversary. It costs more than typing
  `seal-stamp`, and it forges a file in the git dir rather than a line in a
  reply.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline. No row
there needs a person.

Framed 2026-09-28 by framer, before the build.
