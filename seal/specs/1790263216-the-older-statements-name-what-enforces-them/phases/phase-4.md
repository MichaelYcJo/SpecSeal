# 1790263216-the-older-statements-name-what-enforces-them — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 4138dac5 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`docs/review-handoff-protocol.md` (4 statements, 3 bold openings),
`docs/measuring-a-run.md` (10) and `docs/the-agent-set.md` (6): agents,
handoffs and measurement, where cases 1 and 3 of `nothing` were expected to
be most common. The `0.8.2` quoted anchor into `review-handoff-protocol.md`,
`"- **A runner the repository ships is found, not typed into every
prompt.**"`, still resolves.

## What this phase found

The format is phase 1's.

| # | Statement | Rule | Breaking edit | Target | Seen |
|---|---|---|---|---|---|
| D50 | handoff §Ran by · `1788491830` | a record's `Ran by` row names what executed its segment | `chain_check` passing a record with no `Ran by` row | `test_an_absent_row_fails_after_the_cutoff`, `test_the_row_is_read_on_every_record_not_only_the_last` | mutated (M15) |
| D51 | handoff §The handoff before round 1 · `1788224363` | the orchestrator hands coordinates rather than prose | the requirements dropped from the protocol, or the implementer's documents no longer routed to it | `test_the_protocol_carries_the_handoff_before_round_one`, `test_the_implementer_documents_point_at_the_section` | read: pins *coordinates rather than prose*, the three labels, *an aggregate is not a coordinate*, and the route from `agents/smith.md` and the implement skill |
| D52 | handoff §After the run · `1788277657` | the bar depends on the segment kind | a bar dropped or made a refusal threshold | `test_the_protocol_names_a_bar_per_segment_kind`, `test_the_bars_and_the_run_level_table_judge_different_things` | read |
| D53 | handoff §Where each half went · `1788873630` | a section marked for one role reaches that role only | an agent's `skills:` list preloading an `Orchestrator:` section | `test_no_agent_preloads_a_section_marked_for_the_orchestrator` (real tree), `test_a_marked_heading_in_an_injected_skill_names_agent_file_and_heading` | read |
| D54 | measuring §The unit is a segment · `1789296300` | a segment is measured from its own transcript, joined by assertion | a join made outside the tolerance | `test_each_spawned_segment_is_named_by_the_spawn_it_opened_at`, `test_a_segment_opening_outside_the_tolerance_is_named_by_nobody` | read |
| D55 | same § · `1788908215` | the delegated interval is not the orchestrator's model time | the subagent's interval charged to the orchestrator | `test_the_subagents_own_interval_is_not_charged_to_the_orchestrator`, `test_two_spawns_are_two_cycles_each_naming_what_it_spawned` | read |
| D56 | same § · `1788613827` | a run's report is one comparison table, tokens summed over every subagent | the token line summing the parent alone; a row dropped from the run-level table | `test_the_token_line_sums_the_run_not_just_the_transcript_it_was_given`, `test_the_run_level_table_carries_every_row` | read |
| D57 | §What a measurement must survive · `1788700685` | a degenerate reading is reported, never divided by | a division by a zero span; a naive stamp ending the report | `test_a_span_of_zero_prints_what_it_can_rather_than_dividing_by_it`, `test_a_naive_stamp_does_not_end_the_report` | read |
| D58 | same § · `1788873620` | every int conversion is enumerated from the source and discharged | an unguarded conversion added | `test_every_int_conversion_in_the_module_is_discharged`, `test_an_unguarded_conversion_added_to_the_module_is_named` | read |
| D59 | same § · `1788904490` | a published reading is still wrong after publication | a correction that does not say which readings it affects | nothing (case 1): a session's act, written by the correcting work item and read by review | — |
| D60 | same § · `1788926756` | a refusal names the cut its row ends at | the refusal naming a spawn's result as the cause | `test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result` | read: asserts *outlived the cut its row ends at* and not *outlived a spawn's result* |
| D61 | §Where a reading goes · `1788449488` | a measurement nobody posted is one nobody has | the verify skill's instruction to measure and post dropped | `test_the_section_says_it_happens_without_asking`, `test_the_section_names_the_post_command` | read |
| D62 | same § · `1790076080` | posting a reading is one command | `--post` accepted without `--says`; a state that opens an issue | `test_one_open_posts_once_to_that_issue`, `test_post_without_says_refuses_and_says_where_the_reading_comes_from`, `test_no_state_ever_opens_an_issue` | mutated (M13) |
| D63 | same § · `1790076080` | a network write only typing starts is not a hook | `session-cost --post` wired into `hooks/hooks.json` | nothing (case 4): no case reads the hook list for it. The no-path rule inside the statement is held by `test_the_posted_body_does_not_carry_the_transcripts_path` | — |
| D64 | agent-set §One contract · `1788433011` | the universal rules live in one file every agent receives unasked | a definition dropping the contract line, or naming it outside `skills:` | `test_every_definition_opens_with_the_contract_line`, `test_a_bare_name_is_delivered_by_the_frontmatter` | read |
| D65 | same § · `1789081272` | the party that draws a contract is not the one that executes it | a framer-declared work item reaching the pull request with no frame, or an unmarked one | `test_a_declared_framer_with_no_spec_is_refused`, `test_a_spec_with_no_mark_is_refused` | read |
| D66 | agent-set §What each party writes · `1788445862` | a build phase leaves a record | the smith no longer told to write it; the template losing a section | `test_smith_is_told_to_write_the_phase_record`, `test_all_three_sections_exist_outside_comments` | read |
| D67 | same § · `1789100139` | a transition document is deleted when the transition is over | a transition document left standing | nothing (case 1): a session's act, read by review | — |
| D68 | agent-set §What a spawn costs · `1788993115` | a spawn's payload is measurable | the meter failing on the real tree, or not counting per file | `test_the_real_tree_runs_and_names_every_shipped_agent`, `test_the_composition_table_counts_bytes_and_chars_per_file_and_in_total` | read |
| D69 | same § · `1790076080` | the orchestrator's acts are counted against their delivery | an `Orchestrator:` act with no row in the table | `test_every_orchestrator_act_names_its_delivery`, `test_an_act_with_no_row_is_named` | mutated (M14) |

Seventeen decisions name targets, and three say `nothing`: 2 of case 1 and
1 of case 4.

**Mutations, each restored from kept bytes and executed 2026-09-25 on top
of `4138dac5`:**

| # | Mutation | Case run | Result |
|---|---|---|---|
| M13 | `session_cost.py` never refuses `--post` without `--says` | `test_post_without_says_refuses_and_says_where_the_reading_comes_from` | red, 1 failed |
| M14 | the Bootstrap row removed from `skills/implement/orchestration.md`'s act table | `test_every_orchestrator_act_names_its_delivery` | red, 1 failed |
| M15 | `chain_check.py`'s `ran_by` skips its absent-row branch | `test_an_absent_row_fails_after_the_cutoff` | red, 1 failed |

**The three bold openings.** D52 bolds its existing first sentence. D50 and
D51 had no sentence stating the rule first, so each gained one that
restates. D50's restates the heading (*A record's `Ran by` row names what
executed its segment*). D51's restates the rule the section already bolds
mid-paragraph, *coordinates rather than prose*. The quoted line
`seal/releases/0.8.2.md` anchors into D51's statement is untouched and
resolves.

**Which rules take a text pin and which take `nothing`.** A rule a session
follows takes the pin on the instruction it reads, where one exists. That
is D51, D52, D61 and D66, and D33 and D36 in phase 3. A rule with no
instruction pinned anywhere takes case 1: D59 and D67. D65 is neither. The
split between framer and builder is held at the pull request, where a
framer-declared work item with no marked frame is refused.

**What the common checks returned** (executed 2026-09-25):

- `bin/fold-check --shape-from 0` went from 84 problem lines to 61: 20
  missing lines and 3 bold openings. **46 statements remain.**
- `bin/fold-check` exits 0. `review-handoff-protocol.md` is 845 lines, under
  its 848 budget.
- `bin/evidence-check .` named four drifted rows, each re-read, noted
  `Re-read 2026-09-25` and re-stamped where it lives:
  - `seal/ledger.md`'s handoff row;
  - 0.4.0's bars row;
  - 0.8.2's R4;
  - 0.6.0's L3.

  The next run is 2089 ok, 0 drifted and 0 broken, so the quoted `0.8.2`
  anchor resolves.
- 60 modules ran in one command: 2871 passed. They are the modules that name
  one of the three documents or `seal/ledger.md`, the base set, and the
  modules holding the targets.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
