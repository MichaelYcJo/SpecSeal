# 1790635415-a-gate-that-fails-to-load-says-so — overview

📋 implement applied
· spec:     this work item's routing.md, spec.md (Grounding, the measured facts, Scope In 1–7 and Out, S1–S14, Data & interfaces, What a change to a gate must carry, What cannot be checked), plan.md (Technical context, Alternatives, all three phases), questions.md Q1–Q4; docs/commit-review-gate-spec.md §Registration; CONTRIBUTING.md §What a change to a gate must carry; CLAUDE.md §fragments, §commit early; templates/sdd-phase.md, sdd-overview.md; agent-contract §1–§3, §5, §7–§9, §12, §14, §15
· evidence: seal/ledger/1790635415-a-gate-that-fails-to-load-says-so.md G1–G5 added; re-read and restamped in place: seal/releases/0.4.0.md (the row citing hooks/dispatch.py#run_gate), seal/releases/0.15.7.md N8
· verified: executed — S1 red against 2dc9a970, S7 and S9 red against the phase-1 tree, 41 single mutants each killed, the modules that drive dispatch.py or read an edited file run at each phase boundary, evidence-check --strict, rider_check.py, survivor-check; read — Q1's screen; unverified — the rows below

## Why this work exists

A gate that failed to load read exactly like an allow, and nobody was told.
It is now said once per session at the end of the main session's turn, and
the call still goes ahead.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How a failure leaves `run_gate` | `plan.md` §*Technical context*: `run_gate` "will also return what failed" | `run_gate` still returns a gate's stdout, and the failure goes into the module-level `dispatch.FAILED` | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py#test_the_stop_group_reports_the_stop_event` monkeypatches `run_gate` with `lambda _gate, _payload: decision`, a function returning a string. The plan's own constraint is that no existing case be edited to make room |
| Plain text from the `stop` group | spec silent: `spec.md` §*Scope* item 4 names only the stamp's JSON and nothing | the records wait, and the text is printed as it was | plain `Stop` stdout reaches a different reader than a `systemMessage` (`plan.md`'s Alternatives, the "Also tell the model" row), so converting it would move another gate's output onto a new channel. No gate prints it today |
| A linked worktree's silent `stop` | `spec.md` §*Data & interfaces*: "it starts no process in a main checkout" | one `git rev-parse` more per turn end in a linked worktree, measured at +17 ms median | within the frame's stated cost; `questions.md` Q4 records the measurement |

## Not verified

| Item | Who must answer |
|---|---|
| Q1: the report on screen, line 1 as the dim `Stop says:` label and the stamp still whole and last when both arrive in one message | a measurement by the orchestrating session, which alone hosts `Stop` (`questions.md` Q1) |
| The Windows render of a `Stop` `systemMessage`, and this work's cases on Windows | CI's `windows-latest` leg for the cases; the owner, or whoever next runs a session on Windows, for the render |
| Two hook processes racing for one record, run for real rather than forced by blinding the existence check | nobody can run it deterministically. The exclusive create and the claim-by-rename are pinned by forcing each side of the race in-process |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

**A parser of the `.git` file.** It would make the silent `stop` in a linked
worktree process-free, by reading the `gitdir:` line and that directory's
`commondir`. Nothing asked for it, `hooks/sealer-stamp.py` pays the same
process there already, and one parser would want to serve both.

**`merge()` raises on a gate that prints a JSON array, a number or `null`.**
`classify` calls `.get` on whatever `json.loads` returned, so the dispatcher
exits 1 and every decision in the group is lost. This predates the branch,
is not one of the two `merge()` drops `spec.md` §*Scope* Out names, and no
gate prints such a value today. It needs a home that names who will act,
which is the orchestrator's to pick.

## Fed back into the spec

*Inferred during implementation*: plain text from the `stop` group is never
turned into a `systemMessage`, and pending records wait for a turn end that
can carry them. `hooks/dispatch.py#beside` holds it, and so does
`tests/test_a_gate_that_fails_says_so.py#test_plain_text_at_stop_is_left_alone_and_the_records_wait`.
A planner may overturn it.

*Inferred in round 1's fix pass* (🟡 1): a gate that failed to load is named
in every group that loads its file, and a run failure only in the group it
was seen in. `spec.md` §*Scope* item 4 was corrected to say so;
`hooks/dispatch.py#describe` and
`tests/test_a_gate_that_fails_says_so.py#test_a_gate_that_fails_to_load_names_every_group_that_loads_it`
hold it.
