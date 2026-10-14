# 1791934661-every-doc-states-the-current-rule-only — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | the commit that adds this record, which `plan.md`'s Status cell names; the rewrite is `574f010f`, and the budget rows below are written at the rebase |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

Rewrite both editions of `docs/one-root-by-lifetime` to what still rules, on
one outline: English ≤ 22,000 B, Korean ≤ 27,000 B. The design narrative and
the dated decision sections leave, by the owner's answer to #923 Q1; the three
cases pinning the dated sections are removed. Keep the rule census (old rule →
new coordinate) with no ledger rows, no survivors rows, and one-line removal
summaries. Before it, close phase 1's items as the orchestrator answered them:
the docstring fix in a commit of its own, the dead `VERSIONS_OF_ANOTHER_PRODUCT`
entry removed, the released rows and the survivor sweep recorded as #944's.

## What this phase found

**Before and after** (`measure.py`, `executed`, at `431c6754` and `574f010f`).

| Measure | English before → after | Korean before → after |
|---|---|---|
| Bytes | 52,013 → 19,422 | 63,111 → 23,684 |
| Lines | 728 → 316 | 700 → 313 |
| History lines, #930 marks · widened | 39 · 33 → 0 · 0 | 33 · 25 → 0 · 0 |
| Headings | 23 → 12 | 23 → 12, the same levels |
| Fold markers · `Enforced by:` lines | 10 · 9 → 10 · 9, the targets unchanged | the same |
| Pin modules (literals found verbatim) | 32 (53) → 16 (33) | 30 (39) → 13 (20) |
| `BASELINE` pairs | 3 (12 runs) → 0, entries removed | — |

Budget rows owed at the rebase: `bytes:` 19,422 and 23,684, `history:` 0 and 0.

**Two more cases pinned the dated decision table than the plan named.**
`tests/test_first_setup_asks_once.py`'s `test_the_scratch_row_moved_from_left_open_to_decided`
and `test_the_decided_table_carries_this_work_items_rows` read *Decided after
the thread*. Their needles are rules, so they were re-pointed rather than
removed: `test_the_scratch_opt_out_is_stated_with_the_opt_in` and
`test_first_setup_states_what_each_answer_creates_and_installs` read the
sections that state them now, each seen red through `mutation-check` with its
needle broken in either edition (`executed`, five `red`).

**Both exemptions left.** Neither edition names an old root outside the
`KEEP` phrases, so `DESIGN_RECORD` is gone from
`tests/test_no_document_names_the_old_roots.py`, and neither names a version, so
the pair's two `RECORDS_OF_A_MOMENT` entries are gone; the exact-path shape of
that list is held by an entry the case writes in. Each scan now reaches the
pair: red with `.specseal/map.md` written into the Korean edition and with
`0.99.0` written into the English (`executed`, two `red`).

**Citations.** Every outside `§` into the pair names a heading that stands
(`read`), except `hooks/root-migrate.py`'s, which named *What happens to the
existing directories at the switch* and now names *The change in four lines*.
`docs/the-record-layout.md` §*docs/*'s row says what the pair answers now.

**Phase 1's docstring fix moved a unit off the reader census.**
`hooks/worktree_consent.py#automation_answered` changed hash, so
`tests/test_a_reader_declares_its_input_class.py` refused it; it now carries a
`Reads:` line and its census line is gone (`e6052447`).

**What left, in one summary per section.** *The problem, as measured* and its
SDD-set line: #74's counts, and a line `docs/the-record-layout.md` owns. *What
happens to the existing directories at the switch*: the one-time move, now one
sentence of *The change in four lines*. *What it touches in this repository*,
*Order*, *Out of scope*, *Decisions left open*: 0.4.0 planning, #74. *What does
not change*: each item stated in the section that owns it. *Decided after the
thread* and the four dated sections: each rule moved to its owning section or
to the file that already owns it (`skills/settle/SKILL.md`,
`docs/the-record-layout.md`, `skills/implement/orchestration.md`); the dates,
measurements and "what it corrects above" cells left with them. Inside kept
sections: the thread's arguments, "recommended", the owner's corrected summary
of the modes, and the retention measurement.

**Census: 43 rules and 27 decision rows. 55 stand in the new text; 15 leave
this file — 11 with `spec.md` §*Removes* (the 0.4.0 narrative, the dated
sections), 4 to the file that already owns them.** Every kept row is `not
exercisable — no agent case opens this file; held by` the node ids named. A Korean rule maps to the same
coordinate as its English twin, by heading position.

| # | Old rule | New coordinate | Exercised by |
|---|---|---|---|
| 1 | *The change in four lines* **After this change one root…** | same section, **One root the plugin owns holds everything…** | not exercisable — no agent case opens this file; held by tests/test_no_document_names_the_old_roots.py::test_no_shipped_document_names_the_old_roots, tests/test_optin_home.py::test_the_legacy_directory_is_not_an_opt_in |
| 2 | *The problem, as measured* **Things with different lifetimes share a folder…** | *The proposed tree*, the lifetime table | not exercisable — no agent case opens this file; held by tests/test_the_ledger_fragments_fold_at_release.py::test_every_row_reaches_the_ledger_byte_for_byte_and_the_fragment_is_gone |
| 3 | *The proposed tree* **What the names say** | unchanged | not exercisable — no agent case opens this file; held by tests/test_one_word_one_meaning.py::test_the_owner_states_that_one_seal_is_final |
| 4 | *What happens at a release* step 1 | step 1 | not exercisable — no agent case opens this file; held by tests/test_the_ledger_fragments_fold_at_release.py::test_every_row_reaches_the_ledger_byte_for_byte_and_the_fragment_is_gone, tests/test_the_ledger_fragments_fold_at_release.py::test_folding_twice_finds_nothing_and_writes_nothing |
| 5 | step 2 | step 2 | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_states_the_destination_rule |
| 6 | step 3, the guard | step 3 | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_an_open_evidence_todo_row_skips_that_item_and_names_it, tests/test_the_ledger_fragments_fold_at_release.py::test_an_open_evidence_todo_row_refuses_the_fold_and_touches_nothing |
| 7 | *The dependency rule* **Anything that must outlive a release may not read…** | unchanged | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer |
| 8 | **Already safe** | **Safe** | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer |
| 9 | **Would break on removal…** | **The two readers a removal reached** | not exercisable — no agent case opens this file; held by tests/test_unverified_rows_close.py::test_the_documents_state_the_merge_base_footing, tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer |
| 10 | **Kept on purpose** | unchanged | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_an_open_evidence_todo_row_skips_that_item_and_names_it |
| 11 | **The wider rule behind it: nothing may need to be found and updated…** | **Nothing may need to be found and updated when something else moves** | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_states_the_destination_rule |
| 12 | **What keeps `settle` light** | unchanged, with the fold-is-not-a-work-item bullet | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_says_who_judges_and_who_reads, tests/test_settle_reads_before_it_removes.py::test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row |
| 13 | *The opt-in signal* **A repository is opted in when `seal/` exists…** | unchanged | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_new_home_opts_in, tests/test_optin_home.py::test_the_git_directory_is_the_second_place, tests/test_optin_home.py::test_the_shared_root_wins_when_both_exist |
| 14 | **What the thread proposed instead…** | the same paragraph, its why-sentence | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_new_home_opts_in |
| 15 | *What first setup asks* **The one moment this project allows a question…** | **…and it asks one: shared or local** | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_a_repository_with_the_root_at_either_place_is_never_asked, tests/test_first_setup_asks_once.py::test_the_two_options_are_named_in_order_with_shared_as_the_default |
| 16 | **shared** | **shared** | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_each_option_says_what_it_creates_and_what_it_installs, tests/test_first_setup_asks_once.py::test_first_setup_states_what_each_answer_creates_and_installs |
| 17 | **local** | **local** | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_each_option_says_what_it_creates_and_what_it_installs |
| 18 | *Shared or local* **The question is not "commit the folder or not"…** | unchanged | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore |
| 19 | **`seal/config.md`'s `Mode` row is not that key…** | **…is not a key…**, and **Local mode installs no hygiene workflow…** | not exercisable — no agent case opens this file; held by tests/test_the_mode_is_a_row_and_a_command.py::test_two_mode_rows_are_refused_naming_both_lines, tests/test_first_setup_asks_once.py::test_the_record_no_longer_says_the_checks_would_refuse |
| 20 | **Why local mode is under `.git/` and not gitignored** | **Local mode lives under `.git/`…** | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore |
| 21 | **Local records can be copied to another clone by hand** | **Local records can be copied by hand, and a copy is not a sync** | not exercisable — no agent case opens this file; held by tests/test_the_records_can_be_carried_out_and_in.py::test_into_shared_creates_the_committed_root |
| 22 | **A copy is not a sync, and the modes convert into each other** | the same paragraph as 21, and the table's *Switching later* row | not exercisable — no agent case opens this file; held by tests/test_the_mode_is_a_row_and_a_command.py::test_shared_to_local_moves_stages_and_writes_the_row, tests/test_the_mode_is_a_row_and_a_command.py::test_local_to_shared_moves_stages_and_writes_the_row |
| 23 | **The mode is not a one-way door; the history is** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_mode_is_a_row_and_a_command.py::test_the_way_back_it_names_actually_walks_back |
| 24 | **Local mode gets an export/import pair** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_records_can_be_carried_out_and_in.py::test_the_import_asks_nothing_and_names_the_next_command, tests/test_the_records_can_be_carried_out_and_in.py::test_the_reminder_is_one_line_and_writes_nothing |
| 25 | *Naming* **Product name, recommended…** | **Product name: SpecSeal…** | not exercisable — no agent case opens this file; held by tests/test_one_word_one_meaning.py::test_the_owner_states_that_one_seal_is_final |
| 26 | **Root name, recommended…** | **Root name: `seal/`…** | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_new_home_opts_in |
| 27 | **Sub-directory name, recommended…** | **Sub-directory name: `seal/specs/<id>/`** | not exercisable — no agent case opens this file; held by tests/test_no_document_names_the_old_roots.py::test_no_shipped_document_names_the_old_roots |
| 28 | **English stays for every shipped artifact** | **English is the language of every shipped artifact** | not exercisable — no agent case opens this file; held by tests/test_the_pull_request_language_is_the_repositorys.py::test_the_skill_names_the_file_and_the_row |
| 29 | *What happens to the existing directories* **Every work item in `specs/`** moves whole | `spec.md` §*Removes*, the 0.4.0 design narrative | removed — the move ran at 0.4.0; #74 |
| 30 | **The move is done by the session-start hook, once** | *The change in four lines* | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_an_unmoved_old_layout_is_not_asked_but_told |
| 31 | the old ledger paths become `seal/ledger*` | `spec.md` §*Removes*, the 0.4.0 design narrative | removed — #74 |
| 32–38 | *Order*, its seven items | `spec.md` §*Removes*, the 0.4.0 design narrative | removed — 0.4.0's planning, #74 |
| 39 | *What the repository decides* **A setting nobody can find…** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_settings_have_a_front_door.py::test_the_skill_names_every_row_the_template_ships, tests/test_the_settings_have_a_front_door.py::test_the_skill_shows_rows_that_are_absent |
| 40 | **What language this plugin writes in…** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_pull_request_language_is_the_repositorys.py::test_the_skill_names_the_file_and_the_row, tests/test_the_pull_request_language_is_the_repositorys.py::test_the_mirror_is_named_for_its_own_language |
| 41 | **Two rows, because one cannot express the middle answer** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_pull_request_language_is_the_repositorys.py::test_the_template_is_one_item_value_table_whose_first_row_is_the_language, tests/test_the_pull_request_language_is_the_repositorys.py::test_every_document_that_names_a_language_row_names_the_shipped_one |
| 42 | **A cell may carry an escaped pipe…** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_mode_question_is_asked_once.py::test_an_escaped_pipe_is_one_row_and_the_rows_below_it_still_arrive |
| 43 | **A git call that fails is not a git call that answered "nothing"** | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_records_can_be_carried_out_and_in.py::test_an_unreadable_remote_here_refuses_the_import |
| 44 | *Decided after the thread*: the opt-in signal; the directory's lifetime; the dependency stance; where the folded record lives | *The opt-in signal*; *What happens at a release*; *The dependency rule*; *What "spec" means after this* | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_new_home_opts_in, tests/test_settle_reads_before_it_removes.py::test_the_implement_skill_names_the_one_writer_of_docs |
| 45 | the first-setup question's shape; what shared mode installs; the migration hook's stamp | *What first setup asks* | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_first_setup_states_what_each_answer_creates_and_installs |
| 46 | how a session finds the root | *The proposed tree*, **Every `seal/…` path means…** | not exercisable — no agent case opens this file; held by tests/test_the_agent_contract_holds_the_universal_rules.py |
| 47 | the `scratch` opt-out | *The opt-in signal*, its `.git/specseal-scratch` sentence | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_the_scratch_opt_out_is_stated_with_the_opt_in |
| 48 | *Decisions left open*, its three rows | *Naming*, the three names as decided | not exercisable — no agent case opens this file; held by tests/test_one_word_one_meaning.py::test_the_owner_states_that_one_seal_is_final |
| 49 | *Decided when `settle` was built*: what `settle` is; where the fold record lives; who may write in `docs/` | *What keeps `settle` light*; step 2; *What "spec" means after this* | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_says_who_judges_and_who_reads, tests/test_settle_reads_before_it_removes.py::test_the_implement_skill_names_the_one_writer_of_docs |
| 50 | what groups; what a removal breaks | `skills/settle/SKILL.md`, which owns both; *The dependency rule* names the two readers as they stand | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer |
| 51 | whether the mechanism's own release folds | `spec.md` §*Removes*, the four dated sections | removed — overturned by the next row, #517 |
| 52 | *Decided when the fold stopped being a work item*: whether a fold is a work item | *What keeps `settle` light*, its last bullet, linking `skills/settle/SKILL.md` | not exercisable — no agent case opens this file; held by tests/test_settle_reads_before_it_removes.py::test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row |
| 53 | a released work item that wrote no `spec.md`; a ledger row inside a retiring directory | `skills/settle/SKILL.md`, which owns both | removed from this file — held there; #517 |
| 54 | what a fold owes the survivor sweep | `spec.md` §*Removes*, the four dated sections | removed — the sweep is retired by #944 |
| 55 | *Decided when a joined project's `specs/` was read and never taken*: what the 0.3.x layout means | *The change in four lines*, linking `skills/implement/orchestration.md` §*Orchestrator: Bootstrap — create what's missing* | not exercisable — no agent case opens this file; held by tests/test_first_setup_asks_once.py::test_an_unmoved_old_layout_is_not_asked_but_told |
| 56 | whose a `specs/` outside the root is | *The change in four lines*, the reference-root sentence | not exercisable — no agent case opens this file; held by tests/test_optin_home.py::test_the_legacy_directory_is_not_an_opt_in |
| 57 | *Decided when the process record stopped waiting for the fold*: when the process record leaves | *What happens at a release*, **The process record leaves after the release…** | not exercisable — no agent case opens this file; held by tests/test_settle_retires_the_process_record.py::test_the_design_records_dated_section_says_no_check_reads_it |
| 58 | what the process record is; whether the two halves move apart on disk | `docs/the-record-layout.md` §*seal/specs/<work-item-id>/*, linked from the same paragraph | removed from this file — held there; #729 |

Rows 32–38 are seven rules in one row; rows 44–58 hold the 27 decision rows,
grouped by the section that holds them now.
