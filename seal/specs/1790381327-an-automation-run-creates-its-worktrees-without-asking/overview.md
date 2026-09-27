# 1790381327-an-automation-run-creates-its-worktrees-without-asking — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `docs/worktree-guard-spec.md` §Premise, §B, §*Creation consent*, §*Choice sites*; `skills/implement/orchestration.md` §*Question 1 — single-select*; `docs/the-evidence-ledger.md` §*Appended is the word*; `CLAUDE.md` §*a change writes fragments*
· evidence: A1–A5 in `seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md`; six rows of `seal/releases/0.9.1.md` and S3, S4 of `seal/releases/0.9.4.md` re-read and re-stamped, six claims corrected in place
· verified: executed — the guard's and the consent writer's test modules, the doc-shape cases, `evidence-check --strict`, `rider_check.py`, `survivor-check`, and every seen-red and mutation run the phase records list; read — the harness transcript shape, from the orchestrator's own transcript; unverified — the rows below

## Why this work exists

A person who pressed `automation` was stopped by the worktree guard one call
later, and an isolated agent was told to move into its parent's tree. After
this work the guard reads that answer as consent, and it judges an isolated
agent as concurrent work.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| One `Enforced by:` line per new clause | `plan.md` phase 2: "updated with `Enforced by:` lines" / the new cases were added to §*Creation consent*'s one existing line | code | `tests/test_a_folded_statement_names_what_enforces_it.py`: "the statement under [...] carries 2 `Enforced by:` lines, not one". A marked statement runs to the next heading and carries exactly one |
| S9 seen red against the phase-1 tree | `plan.md` phase 2: "S1, S2, S3, S9 through `wg.main()`, each seen red against the phase-1 tree" / S9 seen red by mutation | code | S9 pins a deny the phase-1 tree already gives. A case that must not move cannot be red before the change, so the switch ladder was made to exit on consent, and the case went red |
| Row 142 re-read, not corrected | `plan.md` phase 4: "row 142's *the Agent path still asks* stays true and is re-read, not corrected" / corrected | code | That half does stay true. The row's premise, "With no record, single-stream Bash still denies", is false once the `automation` answer is present |
| The Agent-path cases live in two test files | `spec.md` §Scope names `tests/test_the_guard_asks_once_per_session.py` and `tests/test_worktree_guard.py` / a third, `tests/test_worktree_guard_signals.py`, carried a case that asserted the old ACTIVE listing | code | That case went red at phase 3 and was rewritten |
| `guard_worktree_creation` keeps its parameters | spec silent / `single_stream`, `shared_option`, `shared_steer` removed (NAME NOT IN TREE after phase 3) | code | spec silent. Once the Agent path stopped calling the function, no caller could set them; the rule the phase-2 rider stated applies |
| The answer's leading phrase (round 1, finding 1) | `spec.md` rule 3: "whose answer's leading phrase is `automation`" / the answer must also equal one of the question's option labels verbatim | code | A typed `Other` answer, *automation - but ask me before each worktree*, was read as the preset. 184 of 184 pressed answers on disk equal a label, so the stricter rule loses no measured case |
| A sidechain entry (round 1, ❓) | spec silent / a result marked `isSidechain: true` is refused | code | spec silent. A subagent has no `AskUserQuestion`, and 0 local main transcripts hold such an entry; the orchestrator answered the reviewer's question this way |
| §B row 1 and the allow-bound paragraph | the doc said a compound gets `ask` / the code has answered `silent` since #257 | code | `seal/releases/0.9.4.md` S3, and `test_a_consent_record_buys_silence_for_a_compound_not_a_second_prompt` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck across the repository | the sealer, once, after the review rounds settle |
| Whether a subagent's `PreToolUse` payload carries its parent's `transcript_path` or its own `subagents/…` path (`questions.md` Q4). Either answer lands on the reader's glob fallback, which a case covers | a measurement: a session whose installed hook is this branch's copy |
| That a live harness still writes `toolUseResult.questions`, `answers` and a top-level `cwd` in the shape the fixtures pin. Measured on 2026-09-26 in the orchestrator's transcript only | nobody in this repository can pin the harness; the prompt returns at the old cost if the shape moves |
| Transcript location on Windows and Linux | the CI matrix, for the fixture cases; nobody, for a live Windows transcript |

## Not done

Q1 (a `per axis` answer with its first box ticked) and Q2 (`CLAUDE.md` and
`templates/claude-md-block.md` saying *concurrent sessions*) stay on their
defaults, (a) each, so the build reads no question-2 box and edits neither
file. Q3 is #620: a switch written after a creation in one command goes
unjudged when consent is present. It predates this work, and this work widens
who reaches it to the first creation of an automation session. The Bash
path's single-stream `deny` text is untouched, as the spec's Out list says.

## Fed back into the spec

Inferred during implementation, and a planner may overturn each:

- Any matching routing answer in the transcript counts, not only the latest.
  A later `per axis` does not revoke an earlier `automation`, the same
  standing the record has (A1's note).
- `multiSelect` must be `False` rather than absent (A1's note).
- The `allow` reason names which consent it read, so a person can tell the
  record from the answer (A3).
- The answer must be one of the option labels verbatim, and a sidechain entry
  is refused (A1, after round 1).
