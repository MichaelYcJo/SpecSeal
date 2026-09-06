# 1788613827-a-runs-report-carries-one-comparison-table — overview

📋 implement applied
· spec:     CLAUDE.md §The goal a design is chosen against, §a change writes fragments never the shared file, §no real identifiers; seal/specs/1788613827-…/spec.md, plan.md, questions.md, routing.md and phases/phase-1.md, phase-2.md, phase-3.md; skills/agent-contract/SKILL.md §2, §3, §4, §9, §12, §14, §15; skills/implement/SKILL.md §2, §3, §4; skills/writing-style/SKILL.md; templates/sdd-overview.md, templates/ledger.md, templates/sdd-phase.md; docs/flow.md §0.8.2; seal/config.md (no `Record language` row, so English)
· evidence: `seal/ledger/1788613827-a-runs-report-carries-one-comparison-table.md`, five rows (R1–R5), every hash stamped by `evidence-check --reverify` scoped to the fragment; plus seven rows in `seal/ledger.md` whose anchors phases 2 and 3 moved, re-read and re-stamped with a note each (`## The handoff before round 1`, `### After the run — the per-segment bars`, `## Pull request bodies` ×4, `## Measure the segment, and feed the flow log`)
· verified: executed — phase 4's own modules (`test_chain_hooks_hardening`, `test_the_set_a_work_item_always_has`, `test_unverified_rows_close`, `test_a_row_points_by_content`, `test_evidence_check`, `test_the_ledger_fragments_fold_at_release`, `test_the_changelog_is_gathered_at_release`, `test_no_real_identifiers`, `test_docs_line_wrap`) and `evidence-check` over the whole ledger, output in `phases/phase-4.md`; phases 1–3 as their own records label them, each re-run by the orchestrator at its close. read — the three phase records' findings, the four documents this phase's rows cite. **unverified** — the full suite, the repository-wide lint and the typecheck; see below

## Why this work exists

Two runs of the same chain were unreadable side by side because each report
picked its own rows, and the one row nobody can produce by hand — what the run
spent — was summed by a script written for that occasion; from here the rows
are fixed and the tokens come out of one command.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What verifies phase 4 | `plan.md` row 4, Verified by: *`uv run pytest tests/ -q` once, plus `uvx ruff check .` and `evidence-check`*. This phase ran `evidence-check` and the nine modules that read what it wrote, and declined the other two | code | `skills/agent-contract/SKILL.md` §2: *the broad gate — the full suite, the repository-wide lint, the typecheck — is the orchestrator's, run once, after the review rounds settle*, and §3 says a spawn prompt cannot widen that. A round is edits already scheduled, so a broad run taken here is spent by the first fix. The three declined checks are rows of §Not verified with the orchestrator named |
| Which modules verify phase 3 | `plan.md` row 3, Verified by: *`uv run pytest tests/test_the_handoff_before_round_one.py tests/test_docs_line_wrap.py -q` plus the new pins for both sentences*. Phase 3 added a third module, `tests/test_the_chain_section_has_one_shape.py` | code | `phases/phase-3.md`: the pull request pin fits neither module the plan's own §Technical context named — `tests/test_the_pull_request_language_is_the_repositorys.py` is about the language row in every one of its cases, and `tests/test_a_segment_feeds_the_flow_log.py` pins the table's owner rather than its carriers. `spec.md`'s acceptance row for that scenario allows *or a new module*, so the plan's verification cell is the half that was narrower than the spec |
| The table's `Location` buckets and its share row | #170 §*The rule* states both cells verbatim: `\| Findings by `Location`: record · code or tests · docs · ledger \| the `Location` column \|` and `\| Records' share of the diff \| `git diff --numstat` against the base, `seal/specs/**` apart \|`. `docs/review-chain-spec.md` §*A finding located in a record is a correction, not a round* says the opposite of both: *"A finding whose `Location` is under `seal/specs/`, `seal/ledger/` or `seal/ledger.md` is about the run's own paperwork rather than about the tool"* | the policy | `skills/implement/SKILL.md` §1: **a ticket is a request, not an authority** — it ranks above the code as it happens to be and below the documents that were ratified. The two readings are not academic: measured on this branch at `4d277f1`, `seal/specs` 729 lines · `seal/ledger*` 39 · everything else 831, so the share row reads **45 %** as the issue wrote it and **48 %** under the policy. A table exists to make two runs comparable, and one that can be filled two ways is not one. Round 1's finding 3 |
| Where the run-level reading goes | `spec.md` §Scope, in-item 2, asks the measurement section to state the table. It does not say the table shares the segment readings' destination; `skills/verify/SKILL.md` now says *it is **not a third destination**: the table goes to the rolling log named above* | code | a second home for a reading is a second place to look for one, and the section already names where a segment's reading goes. `docs/review-handoff-protocol.md`'s pointer was then written not to contradict it (`phases/phase-2.md`'s note to phase 3, honoured at `8887abc`) |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ The full suite, the repository-wide lint and the typecheck | run once at `15ab83d` after the rounds settled: 2287 passed, 2 skipped, 4 failed — exactly #160's four macOS export cases, reproduced identically at the base `a9a827b` in a clean clone. `uvx ruff check .` and `ruff format --check .` clean |
| ✅ `subagent_transcripts` and `newest` on the Windows leg | the leg passed on PR #173 in 5 m 03 s, run 33980610140, with every case this work item planted in it |
| ✅ The table as a thing a person actually fills — every row of it, for one real run, beside another run's | filled for this run in PR #173's chain section and posted to the rolling flow log, #172's comment of 2026-09-06. Findings 3 and 4 of round 1 are what the first filling hit, exactly as round 1 predicted. Whether the rows hold for a run this branch did not build is still open, and the next three 0.8.2 items are the readings |
| ✅ Whether this run meets the target 0.8.2 measures against | it does not, and it was never the run to measure it: 4 h 07 min over 2,477 changed lines, where the target is three hours for a change under three hundred code lines. This branch is the ruler, so #156, #155 and #169 are the first readings — recorded in #172's comment |

## Not done

**A checker that refuses a report with no table.** The owner's call of
2026-09-05, recorded as `questions.md` Q3 and as the first *Out* of
`spec.md` §Scope. The table's sources are a pull request body and an issue
comment, and CI reads neither, so a gate over it would either fetch them or
open on a failed fetch. Reopen it with a measurement rather than a
preference.

**Reading a verdict from the numbers.** The table makes two runs comparable
and stops there. `skills/verify/SKILL.md` says so in its own paragraph, and
what a row meant on one branch goes in the prose beside it.

**Widening `tools_per_turn`'s denominator to the token line's turn count.**
The per-segment bars in `docs/review-handoff-protocol.md` are calibrated
against the ratio as it stands, so moving it would move a published threshold
with nothing saying it had moved. Two counters, and `token_totals`' docstring
says which is which and why.

**The table as a file under `templates/`.** A template is copied into a work
item's directory; this table is written into a pull request body and an issue
comment, neither of which the work item holds (`questions.md` assumption 7).

**Re-stamping `templates/config.md#"# Repository config"` in `seal/ledger.md`.**
The unscoped `evidence-check` reported five drifted rows; four are anchors
phases 2 and 3 moved, and those seven ledger rows were re-read and re-stamped
with a note each. The fifth is not this branch's: `templates/config.md` and
`seal/ledger.md` are both byte-identical to `main` at `a9a827b`, so that row
was already drifted there, and re-stamping it here would put another branch's
change into this diff under this branch's name. `.github/workflows/test.yml`
turns drift into a `::warning::` and fails only at exit 2 or above, so nothing
is blocked by leaving it. The repository owner decides whether it rides along.

**A `Broad gate` cell that can hold more than one entry — #174.** Round 1's
finding 4 was two halves. The narrow one is fixed: the table's row asked for
`how many times, at what SHA` from a cell `round_record.py` replaces rather
than appends, and it now asks for what the cell carries. The wide one would
change `templates/sdd-round.md` and the checker that writes it, which is
mechanism a fix pass may not add (`skills/code-review/SKILL.md`), so it is an
issue for the repository owner.

**#156, #155 and #169** — 0.8.2's other three items, and the first three
readings taken under the table this work item builds (`questions.md` Q1).

## Fed back into the spec

Every item below is *inferred during implementation*, and a planner may
overturn it.

- **The token line's printed shape.** `spec.md` §Data & interfaces fixes the
  JSON object and names the fields; the four printed lines — a `tokens`
  header carrying the transcript and turn counts, then `output`, `cache
  write` and `cache read` right-aligned in fifteen columns — are phase 1's,
  chosen so the three magnitudes line up for a reader comparing two runs
  (`phases/phase-1.md`).
- **The transcript count is the line's own cross-check.** Nothing in the spec
  asked for it to be printed. `plan.md` §*What breaks in six months* named
  the silent-shrink failure, and the count is the mitigation: a line reading
  `1 transcript` for a run that spawned six is wrong to the only reader who
  can tell, and the same report's `Agent` call count is the number to hold it
  against.
- **A refusal list of another file's strings needs a case holding it to its
  owner.** `tests/test_the_chain_section_has_one_shape.py` refuses three row
  labels in `skills/commit-pr-convention/SKILL.md`, and
  `test_the_pinned_rows_are_the_owners_own` asserts those three are still
  rows of the table in `skills/verify/SKILL.md`. Without it a renamed row
  leaves a green case guarding a string nobody would paste
  (`phases/phase-3.md`).
- **A case red because its subject does not exist has not been seen red for
  its own reason.** Phase 2 stated it after two of nine assertions were
  invisible in the first red run, and phase 3 applied it to nine of its
  eleven mutations. `skills/agent-contract/SKILL.md` §15 asks for the red and
  does not distinguish the two reds; this work item's records do.
