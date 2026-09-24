# 1790263216-the-older-statements-name-what-enforces-them — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 5beeaa90 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`docs/the-evidence-ledger.md`'s 16 statements without an `Enforced by:`
line, and no bold openings, since all 16 open with one. This is the
calibration phase. It fixes the per-decision record format below, and the
phases after it keep that format. The first statement of §*The fold …* is
already bound and is phase 7's. A target is right when the builder can name
the edit that breaks the rule and the target is what catches that edit.
Each target is opened and confirmed to go red; a target that only resolves
is not a decision. `nothing — <why>` names which of the four cases it is.
The pin on §*The fold …* keeps passing.

## What this phase found

**The record format, fixed here for phases 2 to 6.** Each decision gets one
row, numbered across the work item as D1, D2 and so on. Columns:

- **Statement**: the section and the marker's epoch prefix.
- **Rule**: the bold opening, shortened.
- **Breaking edit**: the edit to the tree that breaks the rule.
- **Target**: the unit that catches that edit, or `nothing (case N)`.
- **Seen**: `mutated` when the catch was executed as a mutation (listed
  under the table), and `read` when the case was opened and its assertion
  read against the edit.

A test node id is written as the function name alone where the file is
clear from the document line. The line in the document is the full target.

| # | Statement | Rule | Breaking edit | Target | Seen |
|---|---|---|---|---|---|
| D1 | §A row is a content anchor · `1788229400` | a coordinate names content; no line number, no commit, no git | a ledger row written as `path:line` or with a date-and-SHA stamp; the check path calling `subprocess` | `test_no_ledger_row_carries_a_line_number_or_a_commit` (real ledgers), `test_the_checker_asks_git_for_nothing` | mutated (M2) |
| D2 | same § · `1788761915` | a fragment still on disk means not shipped | `unshipped` reading the directories under `specs/` instead of the fragments | `test_a_work_item_with_a_ledger_fragment_has_not_shipped`, `test_a_work_item_whose_fragment_was_folded_away_has_shipped` | mutated (M1) |
| D3 | §What the checker refuses · `1789296100` | the lenient run says at exit 1 what the strict run would say | the exit-1 run dropping the notice | `test_a_drifted_tree_is_told_what_the_gate_would_say` | read: asserts `NOTICE` in the exit-1 output |
| D4 | same § · `1788686494` | a printed ledger name goes through one helper | a print site calling `os.path.relpath` on a ledger path | `test_no_ledger_path_reaches_relpath`; for the second bold rule, `test_a_narrowed_run_names_the_shared_ledger_it_did_not_read` | read: the first recomputes every local holding a ledger path and refuses `relpath` on it |
| D5 | same § · `1790154760` | a file many rows cite costs one parse, memoised on its text | the memo dropped (one parse per row), or keyed on the path | `test_rows_citing_one_file_cost_one_parse`, `test_a_file_edited_between_two_reads_gets_its_new_spans` | read: counts parses of one text for five rows; two same-length texts at one path |
| D6 | §A correction a merge dropped · `1789969379` | a ledger conflict is resolved hunk by hunk, never by side | a person takes `--ours` at a merge | nothing (case 1): the resolution is a person's act. `correction-check` reports a dropped marker only after the merge. **Corrected in round 1's fix pass:** the row also said the hygiene leg running `correction-check` is allowed to fail, which is false (the step carries no `continue-on-error`), and the rule's instruction is pinned; the line now names `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` | — |
| D7 | same § · `1789996780` | a bound over a corpus is stated with its instrument and moment | a count written with no instrument beside it | nothing (case 4): no case reads a census sentence for its instrument. The tie rule inside the statement is held by `test_a_tie_falls_to_the_first_parent` | — |
| D8 | §The unverified record · `1788873600` | a baseline ref is resolved once, to the merge base, for every arm | an arm reading the ref's tip instead of the merge base | `test_a_row_the_base_gained_after_the_fork_is_not_a_deletion` (row-count arm), `test_a_work_item_squashed_after_the_fork_is_not_this_branchs_removal` (removal arm) | read: the base gains a row after the fork, and the tip reading reports it as left |
| D9 | §The fold · `1790027178` | removal is the second half of the fold | `settle --retire` removing a released directory no marker records | `test_retire_removes_only_what_docs_records` | read: asserts the unmarked `beta` stays |
| D10 | same § · `1790039346` | a marker counts only on a live line | `folded_items` counting a marker inside a parked draft | `test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record`, `test_a_marker_inside_a_fenced_block_is_not_a_fold_record` | mutated (M3) |
| D11 | same § · `1790076070`, `1790138190` | a spec-less released item is retired by the rule, with no marker | the rule arm writing a marker into `docs/`, or refusing the directory | `test_the_rule_arm_removes_it_with_no_marker` | read: asserts `docs/` unchanged and the directory gone |
| D12 | same § · `1790076070`, `1790138190` | the retirement keeps a directory a ledger row anchors into | `settle --retire` removing an anchored directory | `test_a_row_anchored_inside_a_candidate_keeps_that_directory` | read: asserts `alpha` kept, `beta` removed, exit 1 |
| D13 | same § · `1790138190` | a fold opens no work item and adds no ledger row | a fold branch appending a row or opening `seal/specs/<id>/` | nothing (case 1): a session's act, reviewed at the fold's pull request (#517); no check reads a branch as a fold | — |
| D14 | same § · `1790076070`, `1790119502` | a population floor over the records is replaced, never lowered | `assert len(records) > 5` written over a sweep | nothing (case 4): no case scans the suite for a length compared with a literal | — |
| D15 | same § · `1790138190` | an empty `seal/` root reads as settled | `settle` or `unverified-check --baseline` exiting 2 on it | `test_a_settled_root_is_green_and_says_so`, `test_the_roots_own_specs_path_is_settled_when_nothing_is_under_it` | read: both parametrised shapes of the root, exit 0 |
| D16 | same § · `1790076070` | a marker on its own line is exempt from the wrap limit | `prose_lines` yielding the marker line | `test_a_fold_marker_is_skipped_and_the_line_beside_it_is_not` | mutated (M4) |

Twelve decisions name targets, and four say `nothing`: 2 of case 1 and 2
of case 4.

**Mutations, each restored from bytes kept before it and executed
2026-09-25 on top of `5beeaa90`** (`-p no:xdist`, `tests/__pycache__`
cleared around each):

| # | Mutation | Case run | Result |
|---|---|---|---|
| M1 | `unshipped` lists `specs/` instead of the fragments | `test_a_work_item_whose_fragment_was_folded_away_has_shipped` | red, 1 failed |
| M2 | `py_spans` names `subprocess` | `test_the_checker_asks_git_for_nothing` | red, 1 failed |
| M3 | `folded_items` ignores `live` | `test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record` | red, 1 failed |
| M4 | `prose_lines` drops the marker skip | `test_a_fold_marker_is_skipped_and_the_line_beside_it_is_not` | red, 1 failed |

Every decision's tie could be stated in one sentence, so the four above are
the phase's sample rather than a list of doubtful ties.

**What the common checks returned** (executed 2026-09-25):

- `bin/fold-check --shape-from 0` went from 141 problem lines to 125. No
  line names `docs/the-evidence-ledger.md`. **99 statements remain**
  without the line: 115 less this phase's 16.
- `bin/fold-check` with no flag exits 0.
- `bin/evidence-check .` named two drifted anchors, both headings of this
  document: §*A row is a content anchor* (rows D1 and E1 of
  `seal/releases/0.15.1.md`) and §*A correction a merge dropped* (row E2).
  Each claim was re-read against the edit. The edit added lines and changed
  no sentence, so each claim holds. Each row carries a `Re-read 2026-09-25`
  note and was re-stamped with
  `bin/evidence-check --ledger seal/releases/0.15.1.md --reverify .`.
- 19 test modules read a document this phase edited or name a target in
  it, and all 19 ran in one command: 997 passed. They are found by grep
  over `tests/*.py`: the modules that name `the-evidence-ledger`, the
  modules that walk tracked files or `docs/`, the modules that read the
  ledger files, and the modules holding a target.

**Where the line goes after a long statement.** Four statements in this
document run across several paragraphs. The line goes after the last
paragraph before the next marker, and it is judged against the first bold
sentence. D4 and D5 name a second target for a second bold rule, which
`spec.md` allows and does not require.

**A `nothing` reason wraps like prose.** This document is one of the six
the 88-column test covers, so each `nothing — ` line is wrapped at 88. Its
reason runs on over two more lines, and `test_docs_line_wrap.py` passes on
them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
