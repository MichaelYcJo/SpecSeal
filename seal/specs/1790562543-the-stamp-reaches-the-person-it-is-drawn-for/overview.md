# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — overview

📋 implement applied
· spec:     this work item's spec.md (Grounding, measurements, Scope In 1–6 and Out, S1–S17, Data & interfaces, What cannot be checked), plan.md (Technical context and its three failure scenarios, Alternatives, both phases), questions.md Q1–Q7; issue #400's body (§*The size, and why it is 0.90*, §*What to build*, §*Done when*) and its 2026-09-28 comments; docs/the-broad-gate.md; skills/verify/SKILL.md §*Every agent seals what it verified*; agents/sealer.md §*The command*; skills/code-review/orchestration.md §*Orchestrator: the pull request opens before round 1*; templates/sdd-phase.md, sdd-overview.md; CLAUDE.md §fragments and §commit early; agent-contract §1–§3, §5, §7–§9, §12, §14, §15
· evidence: seal/ledger/1790562543-the-stamp-reaches-the-person-it-is-drawn-for.md N1–N9 added; 0.10.0 S3 corrected in place; re-read and re-stamped where they live: seal/releases/0.4.0.md (three rows), 0.9.1.md, 0.9.3.md (the H1-anchored row), 0.10.0.md (five rows beside S3), 0.11.5.md, 0.12.0.md (three), 0.12.2.md (five), 0.13.1.md, 0.15.1.md (four), 0.15.3.md, 0.15.4.md (three)
· verified: executed — every new case seen red (S1 against the gate at 30d75220; the rest under 40 single mutants, 19 in phase 1 and 21 in phase 2, each killed, the one first survivor killed by a case added for it), the modules that drive the gate, the stamp or the hook and every module naming a file either phase edited, run at each phase boundary, evidence-check --strict; read — the Q2 reading (executed by the orchestrating session, relayed); unverified — S17 and Q1, Q3, Q4 below, and the full suite, lint and typecheck (the sealer's)

## Why this work exists

The sealer's stamp was drawn into a pipe nobody saw unfolded. It is now drawn
once in the session that spawned the sealer, after that turn's text, from a
file the gate writes only over a green run with a written cell.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A green run WITHOUT `--record` on a terminal | `spec.md` §Scope In 2: "A hand-run in a real terminal draws exactly once, as today" — today draws on any green run. The first build drew there without a cell | the terminal draws only over a written cell; without `--record` it prints the `SEALED` line saying nothing was recorded, as a pipe does (S9) | issue #400 §*Done when*: "Drawing a stamp requires the gate's exit 0 and the written cell; no other path draws one." `plan.md`'s Alternatives row for the piped no-record run cites the same sentence, and S10, the terminal scenario, is stated for "a green `--record` run". Nothing names a terminal as the exception. Pinned by `test_a_terminal_run_with_no_record_draws_nothing` |

## Not verified

| Item | Who must answer |
|---|---|
| S17: on a real sealer run, the stamp appears after the orchestrator's text, unfolded, in colour, once | the owner, on the first real sealer run after this merges. The installed plugin is 0.15.6, so the new hook cannot fire in the session that built it |
| Q1: whether a `Stop` hook's `systemMessage` enters the model's context on the next turn | a measurement, after the first real draw: search the session's transcript `.jsonl` for the label line |
| Q3: whether the early-draw window occurs, a stamp drawn above the text it belongs under | a measurement, by the orchestrator on the next release run |
| Q4: the block form through the hook on Windows (Windows Terminal, and a cp949 console) | the owner, or whoever next runs a session on Windows |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

A hook running under an interpreter below `seal_stamp.py`'s 3.12 floor draws
nothing and says nothing. The hook runs under whatever `python3` the harness
finds, which is 3.9 on a stock macOS, and `seal_stamp.py` refuses at import
there. Nothing was built around it: the frame's hook is silent on every
failure, the `SEALED` line in the sealer's report still names the file and
`seal-stamp --from`, and changing the floor is a decision about every script
that copies it. The hook's docstring states it.

`dispatch.py` now names the `Stop` event for the `stop` group, as `plan.md`
asked. `session-start` still reports `PostToolUse` on the decision path it
never takes; correcting it was not asked for.

## Fed back into the spec

none — the divergence row above carries the one rule this work settled that
`spec.md` did not state.
