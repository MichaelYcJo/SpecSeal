# 1790562540-a-resumed-agents-own-transcript-is-sliced — overview

📋 implement applied
· spec:     this work item's spec.md, plan.md, questions.md; skills/verify/SKILL.md §*Measure the segment, and feed the flow log*; skills/verify/scripts/session_cost.py (module docstring, `#subagent_transcripts`, `#resume_cuts`, `#segment_slices`, `#measure_segments`, `#report_breaches`, `#report_segments`, `#emit`, `#main`); CLAUDE.md §fragments and §commit early; agent-contract §1–§3, §5, §9, §12, §14, §15
· evidence: filled at phase 3
· verified: filled at phase 3

## Why this work exists

`session-cost --segments` given a resumed agent's own transcript printed `0
segments found`, and that file is the path an orchestrator holds after a fix
pass. It now prints one row per stretch of work, with the numbers the mode
prints for that agent from the run's transcript.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which published readings the changelog names, and in which group | `spec.md` In 6: "The fix-pass readings posted as a whole resumed transcript: #577 (four passes) and #601 (ten). The ones taken from the harness's notice because `--segments` found nothing: #496, #535 and #619." Opened 2026-09-28 with `gh issue view`: #535's four fix-pass comments each say "The numbers below are the whole transcript" (or "Whole-transcript numbers below"), and six of #601's say whole transcript while its four round-2 passes quote the harness's figures | the changelog groups them as read: whole transcript in #577 (four), #535 (four) and #601 (six); the harness's figures in #496 (four) and #619 (three) | the comments themselves; contract §5, a fact from the handoff is opened before it is built on |
| The `SKILL.md` sentences in the class | `spec.md` *The class* lists D1–D3 in the section | D1–D3, plus the *Read the counts above the table* paragraph, which says the mode prints the join counts "even when they agree" and does not for an own file | §12: the paragraph states the current behaviour, and the own-file page prints a header in their place |
| Two code sentences outside the class table | `spec.md` D7 names `#measure_segments`' first line; D9 names `#emit`'s empty-branch sentence | also narrowed: `#measure_segments`' *exactly what a person running this script against that one transcript gets* (false for a slice since slicing shipped), `#emit`'s residual (*every row label is already relative*, now also a basename), and `#main`'s *The other transcripts of this run, one row each* comment | the same class; each sentence states the behaviour this change moves |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the format check | the sealer, once, after the review rounds settle |

## Not done

Filled at phase 3.

## Fed back into the spec

Filled at phase 3.
