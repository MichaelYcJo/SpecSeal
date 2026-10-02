# 1790835051-the-preflight-asks-seals-own-refusals — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` §*The goal a design is chosen against*, §*Repo rule — a change writes fragments*; `skills/agent-contract/SKILL.md` §1, §7, §8, §9, §12, §14, §15; `docs/review-chain-spec.md` via `skills/code-review/scripts/round_record.py#seal`'s docstring; `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run*; `skills/verify/SKILL.md` §*The broad gate*; `templates/config.md` §*Broad gate*; this work item's `routing.md`, `spec.md` S1–S12, `plan.md` phases 1–4, `questions.md` Q1–Q4; `seal/follow-up.md`; #702's body
· evidence: `seal/ledger/1790835051-the-preflight-asks-seals-own-refusals.md` R1–R9 added; 48 rows in 15 files (35 drifted coordinates) re-read against the edits and re-stamped `--checked 2026-10-01`, none corrected (every claim still held); the frame's three short-path coordinates in `spec.md` and `plan.md` corrected in place. Round 1's fix pass: R3 corrected, R10 and R11 added, a dated `Re-read 2026-10-01 by work item 1790835051 (#702), phase 4` note on each of the 48 rows (⬜ 2), and the 26 rows on `seal` and `gate` re-read again against the fixes and re-stamped `--checked 2026-10-02`
· verified: executed — every new case seen red first, 9 mutations each red (2, 4 and 3 by phase), the modules each phase's `Verified by` cell names, `evidence-check --strict .` over the whole ledger, `survivor-check` over the branch, Q3 timed once; read — `seal/follow-up.md` (nothing waits on this work), both READMEs and `docs/` (none names the preflight); unverified — the full suite, repository-wide lint and the broad gate (the sealer's)

## Why this work exists

Three refusals of `round_record.py seal` still cost the sealer a whole suite
after #638's preflight; the preflight now asks them through `seal --check`,
so they arrive before the spawn.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The preflight's tail | spec §Scope: "`PREFLIGHT_TAIL` says what the run did: the record arms and `seal`'s refusals". The code reads "the record arms, and `seal`'s refusals where a work item is declared for the branch" | the code | On an undeclared branch nothing is asked, and the spec's wording would be false on every such run. The tail is one constant for every run (`phases/phase-2.md`) |
| `seal_record`'s return | `plan.md` §*Technical context* left `(code, text)` or the `Check` to the phase. Returning the `Check` turned `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` red | `(code, text)`, unchanged | spec S10: that case stays "green unchanged". The preflight builds the `Check` from `<keep>/seal.txt`, `run`'s path for a check named `seal` |
| A detached HEAD | spec S8 names none and two declarations. A detached HEAD reaches the same skip, and the S8 line would read "declares a detached HEAD" | `PREFLIGHT_DETACHED` and a third case | contract §14: a printed line is pinned by a case |
| Two declarations' exit | spec S8: "The same line and exit for two declarations naming `feature`" | the line and no `seal.txt` are asserted; the exit is left to the chain arm | the chain arm's handling of two declarations is not this work's, and `seal` is asserted absent from the failures |
| S5's fixture | `plan.md`: "a commit made on a side branch from HEAD and handed to `generate(..., target=X)`" | the same, then `git reset --soft HEAD~1` | `generate` commits the record, which moves HEAD past the commit the target descends from (`questions.md` Q2) |
| Units the plan did not count | `plan.md` §*The ledger* names 26 rows in eleven files on `seal`, `seal_record` and `gate` | 48 rows in 15 files re-read and re-stamped (35 drifted coordinates; **Corrected 2026-10-02** by round 1's fix pass, which counted the rows: this cell said 35 rows) | the build also edited `sealed_record`'s docstring, `main`'s `--preflight` help and `PREFLIGHT_RECORD`, and four document sections whose rows anchor on the whole section or the whole file. The plan's count is corrected in place with a dated note |
| The frame's coordinates | `spec.md` §Scope and `plan.md` §*The ledger* wrote three coordinates with short paths and their `e83db346` hashes | corrected in place to full paths without a hash, with a dated note | the records arm of `evidence-check --strict .`, the preflight's own `ledger` arm, read all six as BROKEN from the frame commit on, so the branch could not preflight green whatever the build did |
| Where #638's changelog sentence went | spec §Scope: "One sentence is appended to that fragment" | inserted at the end of the paragraph it answers, not at the end of the file | the file ends under `### Changed`, and the sentence answers one in `### Added` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the broad gate over this branch. Each phase ran the modules its `Verified by` cell names | the orchestrator, through the sealer |
| Q4: how many sealer runs over 0.17.0's successors are refused at `round_record.py seal` after a suite. The target is 0 | the flow-log sweep that follows 0.17.0 (`questions.md` Q4) |
| PR #714's `windows-latest` leg on `04d8bfd7`, after the seal at `3e9af52c`, failed `test_the_generated_unread_fixes_fail_the_preflight_at_seal`, `test_a_settled_item_preflights_green_and_names_the_record_it_asked` and `test_a_direct_item_preflights_green_and_names_the_work_item_it_asked`: the ask's stderr line named `seal\specs\…`. The cause is the gate, not the cases: `gate` formatted `PREFLIGHT_ASKED` with `os.path.relpath` as it came, and `seal --check`'s `CHECKED` lines did the same, which S2 missed on Windows because it computed its expectation with `os.path.relpath` too. The commits after `04d8bfd7` format both lines through `preflight_asked_line` and `checked_line`, which take the path module and write `/`; `test_the_asked_line_names_its_home_with_slashes_on_windows` and `test_the_checked_line_names_its_home_with_slashes_on_windows` pass them `ntpath` and were red against `04d8bfd7`'s formatting, and `test_each_line_naming_a_home_is_formatted_only_by_its_line_function` holds the call sites. Executed on macOS only; it landed after the seal, so no round read it and the windows leg has not run it | CI's `windows-latest` leg on the PR, and the orchestrator |

## Not done

#638's `overview.md` carries an open `## Not verified` row, answerer the
repository owner, saying the preflight does not ask `seal`'s refusals and
naming alternative E. This work closes the gap that row describes. The row is
#638's record, and this work touches nothing of #638's but its changelog
fragment, so the row is left open for its answerer to mark.

`agents/sealer.md` is untouched (S12): `git diff e83db346 -- agents/sealer.md`
is empty.

Q3 is answered and no case asserts a time, as the spec asked. Measured once
on 2026-10-01 on an Apple M3 Pro: on the sealer's fixture the ask added about
1 s to a preflight (medians 9.23 s against 8.17 s), and `seal --check` alone
took 0.72 s there and 0.57 s on this repository's own work item
(`phases/phase-2.md`).

On this branch today the preflight fails at `seal`: the declaration names the
review chain and `rounds/` is empty, which `seal_home` refuses. That is the
right answer before round 1, because the preflight is the step after the
rounds settle.

## Fed back into the spec

- *Inferred during implementation:* the preflight's tail is true of every run,
  asked or not, rather than of an asked one (`phases/phase-2.md`).
- *Inferred during implementation:* a detached HEAD is named on its own line,
  `PREFLIGHT_DETACHED`, rather than as a branch no declaration names.
