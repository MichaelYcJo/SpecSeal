# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — phase 2

<!-- seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d0f9f125 |
| Ran by | unknown — the spawn prompt did not hand this value over, and the template forbids a segment to source it from its own idea of what it is; the orchestrator fills it |

## What this phase was asked

Build `plan.md`'s Phase 2: `hooks/sealer-stamp.py` at `Stop` only, silent
on `agent_id`, on another event, when not opted in and when the session's
directory is absent, drawing each undrawn file of `session_id` oldest first,
renamed and then drawn, in one `systemMessage` with the label line first;
the `stop` group in `dispatch.py` and the `Stop` entry in `hooks.json`; the
orchestrator's closing rule in `skills/code-review/orchestration.md`, kept to
the section the plan names because item C (#639) edits the verifying-round
`Target` row of the same file in a parallel branch; the **Form** bullet; the
policy paragraph with its marker, an `Enforced by:` line and a separate
`Enforced by: nothing` statement for the screen; then the ledger fragment,
the drifted rows re-read where they live — `seal/releases/0.9.3.md`'s
H1-anchored row among them, which item C drifts too — and the changelog
fragment. S17 stays in `overview.md`'s `## Not verified` with the owner as
the answerer.

## What this phase found

- **The Form bullet exposed a gap Phase 1 left.** Phase 1's gate drew on a
  terminal over any green run, `--record` or not, which is what `spec.md`
  §Scope In 2's "as today" says. Writing the bullet's *only over a written
  cell* showed the Done-when of #400 forbids it: "no other path draws one".
  The terminal now draws only over a written cell, and a terminal run without
  `--record` signals the way a pipe does. The divergence is `overview.md`'s
  one row, and `test_a_terminal_run_with_no_record_draws_nothing` pins it.
- **Nineteen hook-side mutants, one survivor.** The first run left
  `toplevel`'s walk up from `cwd` unkilled, because every case ended its turn
  at the repository root. `test_a_turn_ending_in_a_subdirectory_still_draws`
  was added for it and seen red under that mutant.
- **The class the gate's change falsified reached two more docstrings and a
  case.** `seal_stamp.py`'s module docstring and `pick_shape`'s both said an
  agent's report carries the twin, and so did the reason string of
  `test_pick_shape_is_letters_off_a_utf8_terminal`. All three now say the
  gate draws nothing on a pipe. `is_terminal`, new in Phase 1 and pinned
  there only through the gate, gained a case of its own, red under two
  mutants.
- **Twenty-seven ledger rows drifted, and one was false.** 0.10.0's S3 said a
  pipe gets letters; it was corrected in place with a `Corrected 2026-09-28`
  note. The other twenty-six were re-read, each claim true against the edit,
  and noted and re-stamped where they live. Appending those notes drifted one
  more row, 0.13.1's, which anchors a section of `seal/releases/0.4.0.md`
  itself; it was re-read and re-stamped the same way. `evidence-check
  --strict` then also refused a name in `questions.md` Q2 — `scratchpad_dir`,
  a field of the harness's payload — which now carries NAME NOT IN TREE.
- **`dispatch.py`'s event name is a table of one.** `EVENTS` maps `stop` to
  `Stop`, and `session-start` was deliberately left reporting `PostToolUse` on
  the decision path it never takes, because nothing asked for it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/verify/SKILL.md`'s *`broad-gate` prints the disc on success alone* | the same bullet: the gate draws on a terminal, the `Stop` hook elsewhere, both only over a written cell |
| The terminal drawing of a green run with no `--record` | nowhere: #400's Done-when forbids it, and the run's `SEALED` line says nothing was recorded |
| *a pipe is an agent's report, which carries the twin*, in two docstrings and a case's reason | the same places, saying the gate draws nothing on a pipe |
