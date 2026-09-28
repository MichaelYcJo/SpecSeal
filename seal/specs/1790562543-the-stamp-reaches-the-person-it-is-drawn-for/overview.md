# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — overview

📋 implement applied
· spec:     pending — written when the build closes
· evidence: pending — written when the build closes
· verified: pending — written when the build closes

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
