# 1790263216-the-older-statements-name-what-enforces-them — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | f0f99da4 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`docs/the-broad-gate.md` (11 statements), `docs/release-checklist.md` (6, 2
bold openings) and `docs/branch-and-release.md` (4, 2 bold openings): the
gate, the release and the branch rules, where case 2 of `nothing` (the
rulesets) was expected. The `0.4.0` quoted anchor into
`branch-and-release.md`, `"**The fold refuses while a verified fact has not
reached the ledger.** A"`, still resolves.

## What this phase found

The format is phase 1's.

| # | Statement | Rule | Breaking edit | Target | Seen |
|---|---|---|---|---|---|
| D70 | broad-gate §One act, one owner · `1789002694` | the broad gate belongs to one agent | a second definition assigning the gate, or the prohibition leaving the contract | `test_only_one_definition_assigns_the_broad_gate`, `test_the_prohibition_itself_has_one_home_and_it_is_the_contract` | read |
| D71 | same § · `1789034970` | a shared rule is settled against the agents that exist | the contract losing its universal-only statement, or a definition not receiving it | `test_the_contract_says_it_is_universal_only`, `test_every_definition_opens_with_the_contract_line` | read |
| D72 | §What the gate runs · `1789985781` | every CI step is mirrored by an arm or excluded with a reason | a workflow step classified nowhere | `test_every_step_the_workflow_runs_is_classified`, `test_every_entry_of_the_partition_names_a_step_the_workflow_has` | mutated (M17) |
| D73 | same § · `1789956662` | the gate and CI ask about one range, resolved once | a check handed the local ref's commit; the raw base read twice | `test_every_check_is_handed_the_commit_the_remote_tracking_ref_names`, `test_the_gate_reads_the_given_base_exactly_once` | read |
| D74 | same § · `1789445605` | a configured command that breaks the criterion is refused before anything runs | a wrapped row run as written | `test_the_wrapped_row_that_would_have_seal_a_red_suite_is_refused`, `test_a_refused_row_runs_no_check_and_adds_no_worktree` | read |
| D75 | same § · `1789721571` | a fenced example is not a config row | a fenced `Broad gate` line read as the row, or called absent | `test_a_broad_gate_line_only_inside_a_fence_is_named_and_not_called_absent` | read |
| D76 | §What the runner owes · `1788632199` | the suite's command is cheap the second time | the environment rebuilt on every call | `test_a_built_environment_is_reused_and_never_rebuilt`, `test_a_missing_environment_is_built_once` | read |
| D77 | same § · `1788691941` | every runner failure is a sentence | an unwritable environment raising a traceback | `test_an_unwritable_venv_leaves_the_refusal_a_sentence`, `test_a_failing_build_step_is_a_sentence` | read |
| D78 | §A check that cannot fail · `1788936260` | a module's arms are enumerated and mutated, and the unkilled ones reported | `arm_check.py` skipping a node type or not reporting a survivor | `skills/verify/scripts/arm_check.py`, `test_a_watched_arm_is_killed_and_an_unwatched_one_survives`, `test_every_ast_constructor_is_classified` | read |
| D79 | same § · `1789540097` | a check named for a property observes it | a check that cannot see its own property | nothing (case 1): a session's judgment, read by review one check at a time | — |
| D80 | same § · `1789996775` | a document the work item's own fixes disproved is corrected in that work item | the correction left for later | nothing (case 1): a session's act, read by review in the same pull request | — |
| D81 | checklist §2 · `1788326734` | the preparation commit gathers and folds both kinds of fragment | a release leaving a ledger fragment unfolded | `test_check_fails_while_a_fragment_is_left`, `test_the_release_pull_request_runs_the_check`, `.github/workflows/hygiene.yml` | read |
| D82 | checklist §3 · `1789687448` | a sweep over a git listing judges what remains | a scope listing paths from git with no guard | `test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard`, `test_declining_raises_the_skip_carrying_that_reason` | read |
| D83 | checklist §What a release pull request is not · `1788890000` | the survivor step passes on a release range and says why | the guard removed, or turned into a silent job-level skip | `test_the_workflow_step_skips_a_release_range_and_says_why`, `.github/workflows/hygiene.yml` | read |
| D84 | same § · `1788735085` | a loaded file naming an untagged version at or above the running one is a timer | such a version written into a loaded document | `test_no_loaded_file_names_a_version_at_or_above_the_running_one` | read |
| D85 | same § · `1789919879` | a contributor whose base is wrong is told so | the refusal not naming a wrong base; the procedure not first | `test_the_refusal_names_the_wrong_base_as_one_of_the_two_causes`, `test_the_procedure_is_the_first_section_of_the_guide` | read |
| D86 | checklist §6 · `1788789330` | an update notice names the move it costs | the notice leaving out the reload | `test_the_warning_names_the_cheap_move_before_the_expensive_one`, `test_the_warning_names_both_commands_in_order` | mutated (M18) |
| D87 | branch §Cutting a release · `1788302682` | a release pull request that changes what ships moves the version | a shipped root dropped from the watch pattern | `test_every_shipping_root_is_watched`, `test_the_refusal_still_fails_the_run`, `.github/workflows/hygiene.yml` | mutated (M16) |
| D88 | same § · `1790076050` | every act after the merge belongs to a machine or a command | the note workflow firing on something other than the tag; the label acts moved to the tag | `test_the_workflow_fires_on_the_tag_and_writes_nothing_else`, `test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag` | read |
| D89 | branch §Work accumulates · `1788826000` | a rider stamp names content, and `Target SHA` is what still names a commit | a rider stamp written as `Verified … at <sha>` | `test_no_rider_stamp_names_a_commit`, `test_every_rider_stamp_resolves_and_reproduces_its_hash` | read |
| D90 | same § · `1790076050` | a plugin directory pins a commit of this repository | — | nothing (case 3): a measured fact. The rule it supports, that anything reaching `main` is a merge commit, is held by the `main` ruleset outside the tree (case 2) | — |

Eighteen decisions name targets, and three say `nothing`: 2 of case 1 and
1 of case 3. D90's reason names a case-2 enforcement for the rule it
supports, which is the only place a ruleset appears in this phase.

**Mutations, each restored from kept bytes and executed 2026-09-25 on top
of `f0f99da4`:**

| # | Mutation | Case run | Result |
|---|---|---|---|
| M16 | `hygiene.yml`'s shipped-root pattern drops `bin` | `test_every_shipping_root_is_watched` | red, 1 of 3 |
| M17 | `hygiene.yml` gains a step no partition entry names | `test_every_step_the_workflow_runs_is_classified` | red, 1 failed |
| M18 | `hooks/version-check.py`'s notice loses its reload sentence | `test_the_warning_names_the_cheap_move_before_the_expensive_one` | red, 1 failed |

**D89: the statement was false, and Q1's default for a lagging document
applied.** The folded sentence read *two things point at those commits by
SHA: the `Verified … at <sha>` stamp on every `# RIDER:` comment, and the
`Target SHA` field*. Work item `1788826000` is the marker on that sentence.
Its own spec moved every rider stamp to an anchor and a hash and kept
`Target SHA`, and `test_no_rider_stamp_names_a_commit` holds the stamps to
that today. So the document lagged the decision of the work item whose
marker it carries. The sentence was corrected to the code:

- the stamp names content;
- `Target SHA` is what still names a commit;
- the measured incident is kept as history.

The marker had split its paragraph mid-sentence. The prose before it now
ends its own sentence, so the statement can open with its bold rule. No
marker moved.

- **What stays imprecise.** D90's statement still opens *A third reader
  points at those commits now*. It counts the two readers the old sentence
  named, and only one of those, `Target SHA`, still names a commit. The
  word is D90's bold opening. It was not reworded, because it is a measured
  record (case 3) and its claim about the plugin directory holds. It is in
  the overview's *Not done*.
- **`CLAUDE.md` carries the same false sentence.** Its §*the merge method
  is fixed per direction* says *two things point at those commits by SHA:
  the `Verified … at <sha>` stamp on every `# RIDER:` comment, and the
  `Target SHA` in every `round-N.md`*. This work item does not edit
  `CLAUDE.md`; the sentence is named in the hand-back and in the overview.

**The four bold openings.**

- D81's statement opens with a fence, so its bold sentence sits on the line
  before the fence. It restates what the section's commands do.
- D82's rule sentence was third. It moved first, and its *the first of
  them* became *the first tracked file the disk lacks*, because the words
  it pointed back to now follow it. The rest of the paragraph was rewrapped
  after `test_docs_line_wrap.py` found one line at 102 columns.
- D87's statement had no rule sentence, only a description of two checks.
  One was written that restates what they enforce.
- D89's is the corrected sentence above.

**What the common checks returned** (executed 2026-09-25):

- `bin/fold-check --shape-from 0` went from 61 problem lines to 36: 21
  missing lines and 4 bold openings. **25 statements remain.**
- `bin/fold-check` exits 0.
- `bin/evidence-check .` named six drifted rows: 0.11.1's S9, 0.15.0's P1c,
  0.12.1's R5, and 0.15.1's P3, C1 and D1. Each was re-read and noted
  `Re-read 2026-09-25`. The notes were appended by a script that asserted
  each row's line number and tail before writing, because two rows in one
  file end in the same words. Each file was re-stamped with `--reverify`.
  No claim was made false. P1c's note says the squash paragraph changed
  beside the closer's paragraph it cites. The next run is 2089 ok and 0
  drifted.
- 43 modules ran in one command: 1951 passed, 7 skipped. The wrap module
  had failed once on the rewrapped paragraph before that and passed after
  the fix.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the false half of `branch-and-release.md`'s rider sentence (a stamp naming a commit) | corrected in place; `test_no_rider_stamp_names_a_commit` already held the true half |
