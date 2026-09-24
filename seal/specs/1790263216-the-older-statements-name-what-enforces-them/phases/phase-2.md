# 1790263216-the-older-statements-name-what-enforces-them — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 48a6d6a3 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`docs/round-record-spec.md`'s 16 statements without an `Enforced by:`
line, 2 of them also without a bold opening. The subjects are the
round-record generator and `chain_check.py`'s reading of the records. The
document stays at or under 945 lines. The quoted anchor
`"**Five values can stand in the reach half, and only the first is a unit"`
in `seal/releases/0.8.2.md` is not reworded.

## What this phase found

The format is phase 1's.

| # | Statement | Rule | Breaking edit | Target | Seen |
|---|---|---|---|---|---|
| D17 | §`Fixes checked by` · `1788212517` | the draft excuse does not reach this row | `chain_check` dropping the row's errors for a draft pull request | `test_a_draft_pull_request_is_excused_the_pass_and_not_this`, `test_a_round_cannot_check_its_own_fixes` | mutated (M5) |
| D18 | §The fix surface · `1788272986` | `Contract changes` and `New units` are read on every record | `chain_check` passing a record that lacks either row | `test_a_record_without_the_contract_row_fails`, `test_a_record_without_the_new_units_row_fails` | read: each plants a record without its row and asserts exit 1 naming it |
| D19 | §The record generator · `1788597030` | a record is derived, not typed | `new` writing a table the report did not carry, or returning without running `chain_check` | `test_the_three_tables_are_copied_row_for_row`, `test_the_exit_code_is_chain_checks_and_the_record_stays` | read: the second asserts the generator's exit is the check's exit 1 |
| D20 | same § · `1788844127` | `new` reads the report from where the reviewer left it | `--report` required again, or read from somewhere else | `test_the_default_reads_the_report_the_reviewer_left` | read |
| D21 | same § · `1789338080` | a script a shipped document names is reachable by a command | a document naming a script with no wrapper and no classification | `test_every_script_a_shipped_document_names_is_wrapped_or_classified`, `test_a_document_naming_a_wrapped_script_says_how_to_reach_it` | read: the first enumerates every shipped document and every script it names |
| D22 | §What it refuses · `1788789985` | a below-floor interpreter is refused at entry | `below_floor` letting every version through | `round_record.py::below_floor`, `test_the_script_refuses_at_entry_on_a_below_floor_interpreter`, `test_the_floor_is_the_number_the_runner_and_the_linter_hold` | mutated (M6) |
| D23 | same § · `1788817290` | a finding id is a bare integer in both tables | `R2-1` accepted in either table; a duplicate quoted once | `test_a_round_prefixed_verdict_id_is_refused_naming_the_format`, `test_a_round_prefixed_fix_table_id_is_refused_naming_the_format`, `test_a_duplicate_verdict_id_quotes_both_rows` | read |
| D24 | same § · `1789356180` | a row that commissions nothing takes no fix row | `close` counting a `❓` row open and writing a verdict word over it | `test_a_scope_marker_keeps_its_own_word`, `test_six_rows_with_no_id_stand_beside_one_finding_and_commission_nothing` | read: asserts the marker survives `close` and `Pass` is ticked |
| D25 | same § · `1789296200` | `new` says when the target is not HEAD | `head_moved` returning nothing | `test_a_round_whose_fixes_already_landed_is_told_which_commits` | mutated (M8) |
| D26 | §What it copies · `1788749195` | the record carries the paste-ready fixes, and a copied pipe keeps the row | the paste-ready section dropped; a copied bare pipe splitting a cell | `test_a_paste_ready_fix_reaches_the_record`, `test_a_bare_pipe_in_a_grounds_cell_keeps_the_row_at_its_header_width` | read |
| D27 | same § · `1788873610` | every record is asked the hider question, in the one writer | a second function opening a record for writing | `test_every_record_this_writes_is_read_back_before_it_is_written`, `test_a_comment_that_crosses_a_fence_names_the_comment` | read: the first walks the module's AST for write-mode `open` calls |
| D28 | same § · `1788668335` | a fence closing after a later heading is refused, naming it | the swallowed-heading refusal removed | `test_a_fence_closed_after_the_deferred_table_is_refused` | read |
| D29 | same § · `1789347354` | a wrapped terminal line is one value; the join stops at a blank line | the join stopping at a line end, or running past a blank line | `test_a_terminal_line_that_wraps_is_one_value`, `test_prose_below_the_terminal_block_is_not_swallowed` | read |
| D30 | §What `close` derives · `1789621028` | a record is read against the tree | `chain_check` not comparing the `Fix range` count with the tree | `test_a_fix_range_the_tree_contradicts_is_named` | read: plants 7 commits where the tree holds 1 |
| D31 | same § · `1789455558` | where two rows share a coordinate, the forward map takes the first | the map built by plain assignment, so the last row wins | `test_a_repeated_coordinate_resolves_to_one_row_on_both_sides` | mutated (M7) |
| D32 | same § · `1789425391` | a checker's own cases have to be able to fail | a case planted without anybody seeing it red | nothing (case 1): seeing a case fail is a session's act; the phase record reports it and review reads it **Corrected in round 1's fix pass:** the line now names `test_each_section_holds_its_rule`, the pin on the contract's §15. | — |

Fifteen decisions name targets, and one says `nothing`, of case 1.

**Mutations, each restored from kept bytes and executed 2026-09-25 on top
of `48a6d6a3`:**

| # | Mutation | Case run | Result |
|---|---|---|---|
| M5 | `chain_check` extends `errors` with `checked_by`'s only when `strict` | `test_a_draft_pull_request_is_excused_the_pass_and_not_this` | red, 1 failed |
| M6 | `round_record.py`'s `below_floor` returns None for every version | `test_the_script_refuses_at_entry_on_a_below_floor_interpreter` | red, 1 failed |
| M7 | `close`'s map of the table as it stands assigns instead of `setdefault` | `test_a_repeated_coordinate_resolves_to_one_row_on_both_sides` | red, 1 failed |
| M8 | `head_moved` returns None always | `test_a_round_whose_fixes_already_landed_is_told_which_commits` | red, 1 failed |

**The two bold openings.** Both bold an existing sentence rather than write
a new one. For D17 it is the first sentence, *The draft excuse does not
reach this row*, and it is what the long statement's table then details.
For D18 the first sentence had no verb (*Two more rows, read on every
record …*). It gained *are* so that it reads as a rule, and no other word
moved. No ledger anchor quotes either line. The line `seal/releases/0.8.2.md`
quotes, *Five values can stand in the reach half …*, is untouched, and the
row still resolves.

**The `nothing` for D32 is case 1 and not case 4.** A check cannot see
whether somebody watched a case fail before planting it. What would come
closest is a mutation run over every case, which is a different tool and
not a check of this rule.

**What the common checks returned** (executed 2026-09-25):

- `bin/fold-check --shape-from 0` went from 125 problem lines to 107: 16
  missing lines and 2 bold openings. No line names
  `docs/round-record-spec.md`. **83 statements remain** without the line.
- `bin/fold-check` exits 0. The document is 942 lines, under its 945
  budget.
- `bin/evidence-check .` named one drifted row: 0.9.1's R4, anchored on
  §*The fix surface*. Its claim is about the hole paragraph, which is
  unchanged. It carries a `Re-read 2026-09-25` note and was re-stamped with
  `--ledger seal/releases/0.9.1.md --reverify`.
- 38 modules ran in one command: 1935 passed, 7 skipped. They are the 14
  that name `round-record-spec`, the 7 that read the review-chain document
  set through `conftest.review_chain_text` (overlapping), the 18 ledger and
  `docs/` walkers phase 1 ran, and the modules holding the targets. The 7
  skips are all parametrisations of D21's target,
  `test_every_script_a_shipped_document_names_is_wrapped_or_classified`,
  for scripts no shipped document names; the case as a whole runs, so the
  target holds. (Corrected in round 1's fix pass: this sentence said none of
  the skips was a target, and round 1 ran them with `-rs`.)

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
