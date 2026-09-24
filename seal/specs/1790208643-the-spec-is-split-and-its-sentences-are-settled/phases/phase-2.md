# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c213eb70 |
| Ran by | specseal:smith on Claude Opus 5.5 (1M context) — the agent as the spawn prompt's first line names it, the model as the commit trailer it prescribes names it |

## What this phase was asked

Re-point the test modules that read `docs/review-chain-spec.md` by the section
map: change the tuple or path where a module reads one file whole, add a
second tuple where a module's cases split between two, read every `not in`
assertion over the three files (S6), change the heading-level constants (S7)
and see each such module red at the old constant first, and re-point
`CARRIERS` and `RULES`'s three cases.

## What this phase found

**The population is 30 modules, not 28** (executed, `grep -rln
review-chain-spec tests/`). The two the frame did not count are
`tests/test_a_corrected_sentence_survives_elsewhere.py`, A's (#550), and
`tests/test_docs_line_wrap.py`, whose only mention is phase 1's own `COVERED`
comment. The first names `docs/review-chain-spec.md:1418` inside
`RELEASE_RANGES`, a line of the 0.15.0 squash commit `576fe39d` as that
commit's tree holds it. The name is right for that commit and is not
re-pointed.

**Red before the edit, at the phase-1 tree** (executed: all 30 modules in one
`bin/test` command, exit 1, `50 failed, 1430 passed, 1 skipped`). The S7
modules were red at their old constants.
`test_the_reopening_is_one.py` had 14 failures (`##### The reopening`),
`test_the_record_is_held_to_the_floor_and_the_depth.py` 9 (the four
`SUBSECTIONS`, `DEPTH_FROM`, the recorded limits, the refusal table), and
`test_a_record_says_what_ran_it.py` 3 (`##### What ran the round`). One
failure is not the split's:
`test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
names this work item, which had a `spec.md` and no `overview.md`. The overview
is opened in this phase, at the build's first divergences, as
`skills/implement/SKILL.md` §4 says, rather than at phase 6.

**Green after** (executed: the same 30 modules, `1 failed, 1479 passed,
1 skipped`, the one failure being the overview case). That case is green
once `overview.md` exists (`-k overview`, `1 passed`). The run-stops module
and the hook module were run again after the revert below (`67 passed`).
`uvx ruff check tests/` exit 0, `uvx ruff format --check tests/` exit 0.

**How the re-points were made.** One conftest reader serves the absence
half: `tests/conftest.py#REVIEW_CHAIN_DOCS` (the three paths) and
`#review_chain_text` (each file whitespace-collapsed, joined with newlines so
no phrase can straddle two files). What each module now reads:

- The gate document: `test_one_word_one_meaning`'s deny/ask case,
  `test_chain_hooks_hardening`'s review-arm case, `test_handoff_outlives_the_merge`,
  `test_the_direct_answer_owes_the_sealers_record` (both cases),
  `test_waiver_decided_at_start` (both), and `test_the_reopening_is_one`'s
  `--worktree` case, whose slice ends at `### Parity arm` now.
- The record document: `test_a_finding_id_is_a_bare_integer`,
  `test_a_new_returnable_value_is_a_contract_change`,
  `test_a_runner_reached_unit_reads_pytest_only`,
  `test_the_fixes_name_their_surface`, `test_a_record_says_what_ran_it` (two
  of its three cases), `test_the_report_standard_is_one_in_three_places`
  (`CARRIERS` and `REVIEWER_CARRIERS`), `test_the_rules_have_one_owner`'s
  three cases, now under a `RECORD_SPEC` constant,
  `test_a_record_precedes_the_fixes_it_commissions`'s three fix-surface cases,
  and `test_the_last_rounds_fixes_are_checked`'s vocabulary case.
- Split by the section each case reads:
  `test_the_record_is_held_to_the_floor_and_the_depth`. `SUBSECTIONS`
  carries each subsection's file: the floor, `Needs a fix` and the reopening
  in the run document, closing at `### Where a leftover goes`, and the depth
  in the record document, closing at `## What ran the round`. The cutoff case
  is parametrised with its file (`FLOOR_FROM` in the run document,
  `DEPTH_FROM` in the record document), and the refusal-table case reads all
  three.
- The heading constants (S7): `test_the_reopening_is_one` reads
  `### The reopening`, between `### `Needs a fix`` and
  `### Where a leftover goes — the ladder`. Its ordering case is renamed
  `…_between_needs_a_fix_and_the_ladder`, which no ledger row anchors (read).
  `test_a_record_says_what_ran_it` reads `## What ran the round`.
- Docstrings and comments naming a section that moved are re-pointed in
  `test_what_the_reader_understands`, `test_release_hygiene`,
  `test_gate_judges_the_repo_it_commits_to`, `test_ci_gives_the_checks_what_they_need`
  and `test_the_fixes_close_the_record` (three).
- Left alone, because the section each reads stays in the run document:
  `test_a_release_is_sized_by_a_criterion`, `test_a_segment_feeds_the_flow_log`,
  `test_the_broad_gate_cell_keeps_every_run`, `test_the_record_is_generated`,
  `test_the_run_stops_at_the_last_finding`, `test_the_seal_is_taken_once_by_the_sealer`,
  and the cycle and cap cases of `test_chain_hooks_hardening` and
  `test_one_word_one_meaning`.

**S6, the absence assertions: 12 cases widened to all three documents.** One is in
`test_one_word_one_meaning` (`## The cycle has a bound`) and one in
`test_the_direct_answer_owes_the_sealers_record` (the carrier's gone half,
where the carrier is one of the three). Three are in
`test_the_rules_have_one_owner`: the one-cell prescription, *The verdict word
cannot do this job*, and `UNLESS`, whose loop now runs over all three. One is
in `test_a_record_says_what_ran_it`: the whole needle set reads all three,
because the *three malformed states* count is one copy in the floor's
subsection and one in `Ran by`'s, now in two files. Two are in
`test_a_record_precedes_the_fixes_it_commissions`: the stale *oldest commit
that touched* and *the third style above*. Four are in
`test_the_last_rounds_fixes_are_checked`: the three backwards tuples wherever
the carrier is one of the three, and *There is no third case to run away*.
The run-stops
module's absence was widened and then reverted in this phase:
`ONLY_ENDING` holds no review-chain document, so the widened branch could
never run. A unit that cannot run cannot be seen red, and it was taken back
out.

**Each widened absence seen red** (executed, a probe: bytes of the gate
document and the run document kept in the scratchpad, every forbidden
sentence appended to the GATE document — a sibling, not the file each case
used to read — and the direct-answer's gone sentence to the run document).
The six modules gave `12 failed, 249 passed`, and each of the 12 is one
planted sentence: `test_the_spec_separates_the_cycle_from_the_review_run`,
`test_each_carrier_says_what_the_direct_answer_requires[parts0]`,
`test_a_correction_row_closes_answered_and_never_fixed`,
`test_the_verdict_ruling_…`, `test_the_count_rules_sentence_…` (`UNLESS`),
`test_the_spec_states_the_two_halves_and_the_unknown_answer`,
`test_every_description_of_which_add_is_read_says_the_latest`,
`test_the_spec_points_at_the_row_it_means`, the three last-rounds tuples'
cases, and `test_the_spec_says_the_verifying_round_cannot_loop`. Both files
were restored from the kept bytes, and `git status --short docs/` printed
nothing.

**The ledger** (executed). 11 anchors on the edited cases drifted, in 13 rows.
Each row was re-read and noted *Re-read 2026-09-24 — #526's split
re-pointed the anchored case … and widened any absence it asserts … to all
three documents; the claim unchanged*. `evidence-check --reverify .`
re-stamped 13 rows, then `evidence-check --strict .` exit 0 with
`1767 ok · 0 drifted · 0 broken`.

**What `CLAUDE.md` needs: nothing from this phase.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_the_reopening_is_one.py#test_the_subsection_sits_between_needs_a_fix_and_the_depth`, by name | the same case as `…_and_the_ladder`, which is what it now asserts |
