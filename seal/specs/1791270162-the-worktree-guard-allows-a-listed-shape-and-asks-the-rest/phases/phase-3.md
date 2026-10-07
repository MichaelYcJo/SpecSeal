# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 377026d8 |
| Ran by | smith on Opus 5.5 (named by the spawn prompt) |

## What this phase was asked

Resume at phase 3 by `plan.md`, after `origin/release/v0.20.0`, which holds
#841's twins sampling (PR #845, squash 86cbd9a2), was merged into the branch.
Retire the twins case after #841's sampled version; write the one `Corrected
·` row for D1 of 0.18.2 in this item's ledger fragment, never the released
file; re-measure the corpus with phase 1's definition through a deleted
`test_tmp_*` probe, and list the subcommands phase 2's probe saw that phase
1's table lacks (`check-ref-format`, `hash-object`, `cherry`, `version`) as
candidates under P1 (a); settle the 48 failing cases of
`tests/test_guard_resolves_the_tree_it_judges.py`, each retired with its
subject or rewritten to the new reading, recorded case by case here.
`survivor-check --range a9d7b0e5...HEAD` reported 5 places: correct each or
excuse it in this item's `survivors.md`, and run it over the whole range at
each phase boundary. P5 stays as phase 2 built it. Run only the slices the
plan names; no full suite, no broad gate, no push, no pull request.

## What this phase found

**The merge the spawn named had not carried #845.** `9c03ae85` merged
`origin/release/v0.20.0` as the local ref stood, `275a7ce0`, before #845
landed. A fetch moved the ref to `86cbd9a2`, and `d822128e` merges it. The
twins case retired here is the sampled one, so W4 closes as its default
said: #841 landed first.

**Settling the 48 cases instead of deleting them found three gaps in phase
2's build, each a silence where the tree matters.** The class each belongs
to was enumerated and closed here, because each is this branch's own:

- **A redirection could hide the word `worktree` and `stash` are listed
  by.** `worktree` was listed unless the frozen `adds_a_worktree` read an
  `add`, and `stash` unless its first plain word was `branch`. A
  redirection in front of that word, glued to it, or cut away with an `&`
  hid it: `git worktree 2>/dev/null add ../wt b`, `git worktree
  add>/dev/null ../wt b`, `git worktree &>/dev/null add ../wt b`, `git
  stash 2>/dev/null branch x`. bash creates the worktree or takes the
  branch; the build said nothing in a dirty tree. Over every operator at
  every position, glued and spaced, 208 of the 2,356 placed shapes of five
  moving verbs were silent at `9c03ae85` (a deleted probe), 104 each of
  `worktree add` and `stash branch`. `_hidden_mover` reads the first word
  bash hands git (`_plain_words`) against the frozen one, and a group an
  `&` cut is read again whole where its git part is listed. The other
  direction is pinned too: a listed verb with a redirection after its own
  words stays listed, which 24 shapes at `9c03ae85` did not (a path glued
  to its redirection after `--` read as no path).
- **Only the first unrecognised shape's tree was read.** `git checkout
  README.md && cd w && 2>/dev/null git switch x`, with the session's tree
  clean and `w` dirty, was silent: the `checkout` decided, in a tree that
  matters to nobody. Candidate C asked about it at the base. Each shape is
  judged in its own tree now, first one first, each tree looked up once.
- **A git only the wider reader reads carried a `-C` nothing applied.**
  `2>/dev/null git -C W switch x` was judged in the tree it was typed from.
  `_finding_tree` composes the wider reading's `-C` for such a segment,
  onto the directory the frozen walk placed it in. This reads one thing
  past the frozen walk, and `overview.md` records it as a divergence.

**The cases, settled one by one.** "Red at" names the hooks a case failed
against before it went green here; a rewrite that keeps a property the base
already held is green at both and says so.

| Case (parameters) | Verdict | Grounds |
|---|---|---|
| `test_what_only_the_wider_reading_finds_is_put_to_the_person` (15) | rewritten as `test_a_git_only_the_wider_reading_finds_stops_where_its_tree_matters` | candidate C's tree-less question is gone; each shape stops in the dirty `w` its segment names. The two `--config-env` commands gained `cd w &&`, since in the clean session tree an unrecognised shape says nothing. Red at `a9d7b0e5` on all 15, and at `9c03ae85` on the two hidden `worktree add`s · NAME NOT IN TREE |
| `test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer` (5) | rewritten | the stop in `w`, a `deny` because a session is ACTIVE there (P5), naming the plain spelling; the consent writer's half is unchanged. Red at `a9d7b0e5` on all 5 |
| `test_a_segment_the_base_reads_no_git_in_does_not_take_the_first_slot` (5) | rewritten | the stub now puts the ACTIVE session in `w` only: the hidden shape in the clean tree says nothing and the frozen switch keeps the slot and is denied in `w`. Green at `a9d7b0e5` too, its property being the base's |
| `test_a_redirection_word_is_not_read_as_a_branch_name` (6) | retired | its subject was C's views reading a redirection word as a name · NAME NOT IN TREE |
| `test_a_switch_wherever_its_redirection_stands_meets_the_dirty_tree_row` (5 of 6) | rewritten as `..._is_stopped_in_a_dirty_tree` | R0-R4 are a `checkout` without `-- <path>`, stopped before the ladder; both texts name the uncommitted changes. Green at `a9d7b0e5`, where the ladder asked · NAME NOT IN TREE |
| `test_a_restore_wherever_its_redirection_stands_stays_silent` (3) | rewritten as `test_a_restore_with_its_dashes_stays_silent_wherever_its_redirection_stands` | the same three restores carry their `--` now; without it they are unrecognised, which S3 holds · NAME NOT IN TREE |
| `test_a_restore_before_a_hidden_switch_does_not_silence_the_question` (2) | rewritten as `test_a_shape_in_a_clean_tree_takes_no_stop_from_one_in_a_dirty_tree` | the second gap above. Red at `a9d7b0e5` and at `9c03ae85` · NAME NOT IN TREE |
| `test_a_newly_read_checkout_in_front_takes_no_question_away` (2 of 4) | rewritten in place | the property outlived #790's lookups; the two whose switch only the wider reading reads, through its own `-C`, red at `9c03ae85` (the second and third gaps) |
| `test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard` (1) | rewritten as `test_a_git_only_the_reading_past_redirections_finds_stops_in_its_segments_tree` | the stop asks in `w` and quotes the shape. Red at `a9d7b0e5` (C asked with no tree) · NAME NOT IN TREE |
| `test_a_creation_only_the_wider_reading_finds_is_silent_under_consent` (1 of 4) | rewritten as `..._stops_whatever_the_consent_record` | the stop reads no consent record (#734). Red at `a9d7b0e5` on all 4, and at `9c03ae85` on the two hidden `worktree add`s · NAME NOT IN TREE |
| `test_the_question_names_both_kinds_and_says_it_in_korean` (1) | retired | C's text is gone; W1's pin in `tests/test_worktree_guard.py` holds the stop's text in both languages · NAME NOT IN TREE |
| `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` (1) | retired | its subject was C's per-view subtraction; `cd w && git checkout README.md` is unrecognised and stopped, which S3 holds · NAME NOT IN TREE |
| `test_a_message_search_over_a_dirty_tree_is_asked` (1) | rewritten in place | both searches stop in the dirty tree now, the one git refuses included, and the stop names `git switch --detach <rev>`. Red at `a9d7b0e5`, where the refused search was silent |
| `test_an_untokenizable_segment_is_not_a_switch` | rewritten as `test_an_untokenizable_command_holding_git_is_a_finding_of_its_own` | the segment is a switch, and the command is P4's untokenizable finding. Red at `a9d7b0e5` · NAME NOT IN TREE |
| `test_a_file_restore_inside_a_subshell_stays_silent` | rewritten as `test_a_restore_inside_a_subshell_is_listed_by_its_dashes_alone` | read by `shape_of`, no tree. Red at `a9d7b0e5` · NAME NOT IN TREE |
| `test_a_wider_reader_that_exits_at_load_costs_only_the_question` | rewritten as `..._leaves_the_guard_reading` | asserts the shapes the guard keeps without the wider reader. Red at `a9d7b0e5` · NAME NOT IN TREE |
| `test_a_hidden_switch_behind_a_judged_one_adds_no_question`, `test_a_hidden_creation_behind_a_judged_one_adds_no_question` | kept, docstrings rewritten | each passes for the new reason: the hidden shape's tree is clean and single-stream |
| `test_classify_follows_the_chdir_when_resolving_a_ref`, `test_a_subshell_checkout_resolves_the_branch_it_names`, `test_a_branch_ending_in_a_parenthesis_answers_inside_a_subshell_too` | retired | the ref lookup and its `)` peel · NAME NOT IN TREE |
| `test_candidate_c_finds_what_only_the_wider_reading_finds`, `test_candidate_c_reports_nothing_the_frozen_reading_found`, `test_candidate_c_reads_a_redirection_glued_to_git`, `test_a_switch_behind_an_ampersand_led_operator_is_candidate_cs`, `test_a_broken_wider_reader_costs_only_the_question` | retired | candidate C; the broken-reader property is `test_a_broken_wider_reader_costs_a_stop_never_a_silence` · NAME NOT IN TREE |
| `RESTORES`, `_shapes`, `_after_the_subcommand`, `_placement`, `_sample`, `test_no_restore_is_asked_whatever_the_redirection_and_wherever_it_stands`, `POLICY_RULE`, `ASKABLE`, `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`, `HIDDEN_FILE_CHECKOUTS` and its case | retired | candidate C's generators and rule, #841's sampler with them; `_redirections` and `_placed` stay and feed the two new property cases · NAME NOT IN TREE |
| `test_the_guard_policy_says_a_hidden_file_checkout_is_asked`, `test_the_guard_policy_says_what_it_reads_past_the_base` | retired | the policy pins on #745's rule and on the two rules read past the base; phase 4 rewrites §*Which tree* and pins the new sentences (S12) · NAME NOT IN TREE |
| `KINDS`, `test_switch_kind_reads_the_words_alone`, `CREATING`, `VALUED`, `_spellings`, `CREATIONS`, `SWITCHES`, `TWINS`, `_dashed`, `_git_switches`, `DASHED`, `DASHED_SWITCHES`, `DASHED_TWINS`, `a_branch_and_a_file`, `_read_apart`, `_kinds_read` and the eight cases over them, among them `test_no_constructed_switch_is_silent`, `test_no_twin_is_asked_unless_an_operator_cuts_the_segment` (#841's sampled form) and `test_the_sample_covers_every_placement_and_every_verb` | retired | `spec.md` In 6 retires these generators and every case over them with `switch_kind`, `classify` and the option table · NAME NOT IN TREE |
| `USAGE`, `_usage`, `test_the_option_table_binds_the_installed_git`, `test_the_reduction_takes_out_every_redirection_the_reader_names`, `test_a_process_substitution_target_goes_with_its_operator`, `test_a_word_holding_whitespace_is_not_cut`, `test_a_long_option_named_exactly_wins_over_the_ones_it_begins`, `test_an_ambiguous_long_prefix_takes_nothing` | retired | the option table and the reduction · NAME NOT IN TREE |
| #790's section: `_git`, `_commit`, `a_history`, `CARRIERS`, `MOVES`, `GUESSED`, `REFUSED`, `MOVING_SHAPES`, the base's lookup, and the cases over names git resolves, refuses, guesses or reads as a range, `test_nothing_the_base_read_as_a_switch_goes_quiet` and `test_the_first_newly_read_checkout_is_the_one_judged` among them | retired | every name lookup and the slot rule they fed are removed · NAME NOT IN TREE |
| `tests/test_worktree_guard.py`: `reason_for`, `test_classify`, `test_classify_checkout_of_existing_file_is_restore`, `test_classify_checkout_dwim_remote_branch`, the two `-C` cases | rewritten to `shape_of` (`test_shape_of`, `test_a_checkout_restores_by_its_dashes_and_not_by_the_tree`); the DWIM case retired | `classify` is removed; the splitting and quoting properties those cases held are read through `shape_of`, with no repository · NAME NOT IN TREE |
| new: `test_no_redirection_makes_a_moving_verb_listed_wherever_it_stands`, `test_a_redirection_after_a_listed_verbs_words_keeps_it_listed`, `test_each_tree_is_placed_once_however_many_shapes_it_holds` | planted | red at `9c03ae85` on 208 and 24 shapes; the third survived a break of the per-tree dedupe until it was written, then red |

**Mutation, through `bin/mutation-check`, every unit this phase added or
changed, one break at a time, each red:** `_DECIDED_BY` without `stash`;
`_hidden_mover` never hiding, and hiding a plain mover; `_plain_words`
dropping glued heads, keeping the `&`, keeping a number or a `{name}`
descriptor, and keeping a spaced target; the merged re-read skipped, taking
no finding, and skipping a listed part; `main` reading only the first tree;
`_finding_tree` dropping the wider `-C`, and placing a body in a segment's
tree. **Two survived.** The per-tree dedupe, until
`test_each_tree_is_placed_once_however_many_shapes_it_holds` was written
(then red). And `_finding_tree` reading the wider `-C` for a segment the
frozen reading reads as git too: an equivalent mutant, because for such a
segment `judgeable` has already composed the same `-C` onto the same
directory. A third unit, the merged re-read's `switch`/`creation` branch,
could not be reached (the group's subcommand is the listed part's own) and
was removed rather than shipped untested; so was `_plain_words`' whitespace
guard, which changed no reading.

**The corpus, re-read on phase 1's definition.** Its record does not say
which `cwd` a pair took, so a deleted probe reproduced its cut-1 figures
first: a pair is (command, the entry's own `cwd`), and that gives 31,193
pairs and 8,960 holding git, phase 1's numbers exactly. The first cwd of
each transcript gives 31,191. Cut 2 ends at the end of 2026-10-06 (+09:00);
it reads 33,239 pairs where phase 1 read 33,220, the difference being runs
recorded on that day after phase 1's probe. Phase 2's 22,628 is no
definition tried here, and its probe is gone. Through the build's own
readers, tree-blind:

| | Cut 1 | Cut 2 |
|---|---|---|
| pairs | 31,193 | 33,239 |
| pairs holding a git segment the frozen reading yields | 8,960 | 9,707 |
| pairs the build stops, by an unrecognised shape | 315 | 333 |
| of them, a `checkout` without `-- <path>` | 280 | 297 |
| an unlisted subcommand | 14 | 14 |
| a string handed to a shell | 13 | 13 |
| an untokenizable command | 5 | 5 |
| a substitution body | 3 | 3 |
| a redirection read as the subcommand | 1 | 2 |
| pairs today's guard stops, at its maximum, switches only | 379 | 401 |
| pairs the build stops that today's guard does not | 55 | 57 |
| pairs today's guard stops that the build neither stops nor sends to the ladder | 0 | 0 |
| **M3: an unlisted subcommand, its own plain spelling** | **14** | **14** |

M3's 14 are `update-ref` (13 pairs), `symbolic-ref` (1) and one subcommand
held in a variable, `$d`, some pairs holding two. Today's maximum is
`a9d7b0e5`'s `classify` per segment with every name lookup answering True,
plus candidate C's switches; it reads below phase 1's 439/465 because
creations are left out here. The string class reads 13 where phase 1 read 0:
phase 2 reads a shell's string with `reparsed_texts`, which returns every
word that might be the string, where phase 1's probe used `command_strings`.
Every count is tree-blind, so an upper bound on stops where the tree
matters.

**P1 (a)'s candidates: none becomes a row.** On phase 1's definition the
frozen reading yields `check-ref-format`, `hash-object`, `cherry` and
`version` as a subcommand in neither cut. Their occurrences sit inside
here-documents, `python3` scripts, shell strings and `git --version`, and
the one recorded subcommand off the list is `2>/dev/null`, the redirection
shape. Under P1 (a) a row is a recorded subcommand, so `LEAVES_THE_TREE`
does not change.

**M4, after.** `bin/test tests/test_guard_resolves_the_tree_it_judges.py
tests/test_the_frozen_reading_never_grows.py -q --durations=10 -p no:xdist`:
112 passed in 7.83 s, slowest call 0.31 s, against the 164.87 s, 24.88 s
and 203.0 s #841's body carries for the base (read, not re-run) and the
17.7 s #841 measured for the module after sampling.

**The ledger.** `seal/ledger/1791270162-….md` holds 18 `Corrected ·` rows,
one per released row whose claim rested on a unit or case this phase
removed, D1 of 0.18.2 among them, each correcting its family's last
correction where there was one; and 7 `Re-read ·` rows, written by
`evidence-check --reverify --ledger seal/releases/0.18.3.md --into …` for
the families whose `main` coordinate moved and whose claims were read
against `main` first and hold (A4, A5, W2, W4, W7, W9, and 0.9.1's writer
row). Two things the strict check still reports are #841's and not this work
item's to write: its fragment's S5 row cites
`test_the_sample_covers_every_placement_and_every_verb` and · NAME NOT IN TREE
`test_no_twin_is_asked_unless_an_operator_cuts_the_segment`, both retired
(BROKEN); and its spec, plan, questions, phase and round records name
`_sample`, `DASHED_*` and the other retired helpers (NOT-IN-TREE). A · NAME NOT IN TREE
`Corrected ·` row cannot cite a fragment row, so S5 is repaired in place or
not at all.

**Survivors.** At the start, at `9c03ae85` and before #845 was merged,
`survivor-check --range a9d7b0e5...HEAD` reported 6 places, not the
handoff's 5; why the two differ was not measured. After this phase
it reports 113, because the range now deletes four shipped readings whose
sentences stand, by design, in the released ledger and in the records of
the work items that built them. Two were this phase's to correct, comments
in the test module, and are corrected. Of the rest, `docs/worktree-guard-
spec.md` holds the ones that are defects, and phase 4 rewrites that
document; `hooks/cmdline.py:40-58` describes that module's own redirection
reader, which stands; the others are released rows, earlier work items'
records and phrase coincidences. The whole-range row in `survivors.md` waits
until phase 4 has corrected the policy, so it never excuses a defect.

**Two shapes the stop reads imprecisely, in the safe direction.** `git
--config-env k=v switch x` stops as the unlisted subcommand `k=v`, because
the frozen reading takes the value for the subcommand; the stop is right
and its plain spelling is not. A redirection glued to a listed subcommand
(`git status>/dev/null`) stops as phase 2's redirection shape. Phase 4's
§*Known limits* can name both.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| candidate C (`wider_only_kinds`, `_bare_words`, `ask_what_only_the_wider_reading_finds`) · NAME NOT IN TREE | the unrecognised-shape stop (`stop_unrecognised`, phase 2); K5, N1, M1, M2 and W10's `Corrected ·` rows |
| `switch_kind`, the option table and its reader (`SWITCH_OPTIONS`, `_Options`, `_long_option`, `read_switch_words`, `handed_words`, `_redirection_width`, `_REDIRECTION`) · NAME NOT IN TREE | `shape_of`, `_restores`, `_plain_words`, `_hidden_mover`; G1, D1, D2 and D3's `Corrected ·` rows |
| `classify`, its lookups and guesses (`is_ref`, `_verified`, `_commit_named`, `_object_named`, `_one_merge_base`, `_OBJECT_NAME`, `tracked_in_any_remote`, `_refs`, `_fetched_as`, `_the_bases_lookup`, `_no_guess`) · NAME NOT IN TREE | nothing looks a name up; R1-R6 and W1's `Corrected ·` rows |
| the cases in the table above marked retired | their subject left with them; the `Corrected ·` rows name them |
| §*Which tree*'s sentences on the readings, and their pins | the pins are gone; the sentences are phase 4's to rewrite |
