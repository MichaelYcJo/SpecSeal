# 1790562540-a-resumed-agents-own-transcript-is-sliced — overview

📋 implement applied
· spec:     this work item's spec.md (Grounding, Scope, In 1–6, the class D1–D11, Out, S1–S12, Data & interfaces), plan.md (Technical context, Alternatives, phases 1–3), questions.md Q1–Q2; skills/verify/SKILL.md §*Measure the segment, and feed the flow log*; skills/verify/scripts/session_cost.py (module docstring, `#subagent_transcripts`, `#resume_cuts`, `#segment_slices`, `#measure_segments`, `#report_breaches`, `#report_segments`, `#emit`, `#main`); the 14 ledger rows `evidence-check` named; CLAUDE.md §fragments and §commit early; agent-contract §1–§3, §5, §7, §9, §12, §14, §15
· evidence: seal/ledger/1790562540-a-resumed-agents-own-transcript-is-sliced.md A1–A6 added; re-read and re-stamped where they live: seal/releases/0.11.3.md (four rows), 0.13.1.md O6 and O7, 0.15.6.md N5, 0.8.0.md F5, 0.8.2.md R3 and G5, 0.9.5.md (four rows); none corrected
· verified: executed — every new case seen red (at the base code or under the mutant equivalent to it), 14 mutants across two phases, 13 killed by the first draft and the 14th by a case added for it, the narrow modules at each phase boundary, evidence-check lenient and strict, correction-check over the range, S12 on a real resumed transcript; read — `--latest`'s ordering against the hint; unverified — the full suite, lint and format check (the sealer's)

## Why this work exists

`session-cost --segments` given a resumed agent's own transcript printed `0
segments found`, and that file is the path an orchestrator holds after a fix
pass. It now prints one row per stretch of work, with the numbers the mode
prints for that agent from the run's transcript.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which published readings the changelog names, and in which group | `spec.md` In 6: "The fix-pass readings posted as a whole resumed transcript: #577 (four passes) and #601 (ten). The ones taken from the harness's notice because `--segments` found nothing: #496, #535 and #619." Opened 2026-09-28 with `gh issue view`: #535's five fix-pass comments each say "The numbers below are the whole transcript" (or "Whole-transcript numbers below"), and six of #601's say whole transcript while its four round-2 passes quote the harness's figures | the changelog groups them as read: whole transcript in #577 (four), #535 (five) and #601 (six); the harness's figures in #496 (four) and #619 (three) | the comments themselves; contract §5, a fact from the handoff is opened before it is built on. Corrected 2026-09-28: the build counted four in #535 and round 1 (⬜ 3) found five, item A's round-2 pass being the one dropped |
| The `SKILL.md` sentences in the class | `spec.md` *The class* lists D1–D3 in the section | D1–D3, plus the *Read the counts above the table* paragraph, which says the mode prints the join counts "even when they agree" and does not for an own file | §12: the paragraph states the current behaviour, and the own-file page prints a header in their place |
| Code sentences outside the class table | `spec.md` D7 names `#measure_segments`' first line; D9 names `#emit`'s empty-branch sentence | also narrowed: `#measure_segments`' *exactly what a person running this script against that one transcript gets* (false for a slice since slicing shipped), `#emit`'s residual (*every row label is already relative*, now also a basename), and `#main`'s *The other transcripts of this run, one row each* comment | the same class; each sentence states the behaviour this change moves |
| Where the plain hint prints | `spec.md` In 4: "The condition is exactly In 1's: markers, and no transcripts beside." | In 1's condition, narrowed twice: only where the reading has a span, and only where the coordinator's messages cut the calls into two stretches or more | the line says *the span below covers every stretch … and the waits between them*; a file with no paired call prints no span for it to be about, and one whose messages fall before its first call or after its last has one stretch and no wait (round 1's 🟡 1, 328b379d) |
| `plan.md` phase 3's drifted set | "`seal/releases/0.13.1.md` (`#emit` with `test_the_posted_body_does_not_carry_the_transcripts_path`, plus two section rows)" | one section row there (O6); the other mention is prose above the table | `evidence-check` names the rows; the frame's set was a grep |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the format check | the sealer, once, after the review rounds settle |
| ✅ The hint landing after `--latest`'s `# <path>` line — read, not run: `main` prints that line before `emit` and the hint is `render()`'s first print | executed by the warden in round 1 (probe C2, `rounds/round-1.md`): `# <path>`, blank, hint, and `# <path>`, blank, own-file header; the verdict says no case is owed |

## Not done

The rows' agent name (`spec.md` *Out*): an own-file row is named by its
file. Recovering the name from `agent-<id>.meta.json` or by walking up to the
session's transcript is not built, and whether it is worth an issue is the
orchestrator's call at the pull request. Re-deriving the fix-pass readings the
changelog names is not done here, for the reason `spec.md` *Out* gives. The
walked page's resumed paragraph prints unchanged on an own-file page, as In 2
asks, including its *only the file's opening could be joined*, which is true
in general and describes nothing on a page where nothing was joined; the
legend above it says no spawn was joined.

## Fed back into the spec

Inferred during implementation, so a planner may overturn them:

- A file with transcripts beside it is walked whatever its markers, and
  never sliced as an own file (ledger A1, the case the mutation pass added).
- The plain hint is printed only where the reading has a span, and only
  where the coordinator's messages cut the calls into two stretches or more
  (ledger A5).
