# the commit gate inside git — behavior spec

Authority for the commit gate inside git: the `pre-commit`,
`reference-transaction` and `post-commit` stubs `hooks/hook-install.py`
writes, which commits they judge and which they leave to a person or to git,
what they cannot see, and which reading judges a commit in each state of a
repository. What a stop asks about, the two opt-in arms and the routing
declaration, is `docs/the-review-and-parity-arms.md`'s. The PreToolUse
reading that judges where git cannot, the registration of the hooks, the
review-history guard and the implementer mark are
`docs/commit-review-gate-spec.md`'s. The review run those hooks serve is
`docs/review-chain-spec.md`'s, and what the pull-request check reads of a
round record is `docs/round-record-spec.md`'s. Update spec and code together.

## The commit gate inside git (pre-commit · reference-transaction · post-commit)

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**In a clone carrying this plugin's git hooks, a commit is judged inside the
commit, in the worktree it lands in, and the command's text is an input to
nothing.**
`pre-commit` runs in the git process making the commit, with its working
directory at the root of the worktree whose index becomes the commit and the
branch `HEAD` names there. So no shell construct, present or future, routes a
commit around the decision: a command that commits reaches git, and one that
does not needs no decision. The reading this replaces predicted from the text
where a shell would run the commit, and milestone 49 found one more shape at
every round. Measured over 413 commands of the corpora, replayed through bash
and zsh (`seal/specs/1790815613-…/phases/phase-1.md`, M6): 112/115 stops on a
real commit kept, 37/44 real commits the release base missed now judged, and
70/67 stops on commands that committed nothing anywhere undeclared dropped,
the recorded run's commits into a declared worktree among them.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_s1_a_commit_lands_in_the_declared_worktree_with_no_stop, tests/test_the_commit_gate_decides_at_the_commit.py::test_s1_a_heredoc_that_ends_early_commits_into_the_main_checkout_and_is_stopped, tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**The hooks are stubs that `hooks/hook-install.py` writes, and a hooks slot
somebody else holds is never written over.**
The installer runs at session start and first in every Bash call's `pre-bash`
group, for the clone the payload's `cwd` is in, and writes `pre-commit`,
`reference-transaction` and `post-commit` into that clone's common `hooks/`
directory, which every worktree of it shares. Each stub
carries the marker line `# specseal-git-hook <version>` and the installed
plugin's absolute path, which it tests before running anything, so removing
the plugin leaves stubs that do nothing. A stub whose bytes differ from what
the running plugin would write, or that git cannot execute, is rewritten, and
until it is the clone is not one where git decides. `core.hooksPath` set at any
level, or a hook file without the marker, makes the clone foreign: nothing is
written, the plugin's own stubs there are taken out, and the session is told
once (`questions.md` P1, answer (a)). A clone that does not opt in gets
nothing and loses the stubs it had.
Enforced by: tests/test_the_hooks_are_installed_where_git_runs_them.py::test_the_stubs_land_in_the_common_hooks_directory_from_a_linked_worktree, tests/test_the_hooks_are_installed_where_git_runs_them.py::test_core_hooks_path_makes_the_clone_foreign, tests/test_the_hooks_are_installed_where_git_runs_them.py::test_a_hook_file_without_the_marker_is_never_touched, tests/test_the_hooks_are_installed_where_git_runs_them.py::test_a_clone_that_does_not_opt_in_gets_nothing_and_loses_ours, tests/test_the_hooks_are_installed_where_git_runs_them.py::test_a_stub_git_cannot_run_is_written_again_and_decides_nothing_till_then

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**A commit with no Claude session behind it is a person's own, and is not
judged.**
The session comes from `CLAUDE_CODE_SESSION_ID`, the one session variable the
harness exports to every Bash child, which git hands to its hooks; the stub's
short-cut tests that name and no other. Where it is absent, as under `env
-i`, the hook takes the lease (`hooks/session-lease.py`) whose recorded pid
is the session's `claude` process: `CLAUDE_PID` where the environment carries
it, an observed value, and else its nearest ancestor whose name is `claude`.
The lease writer records its pid by the same reader, so the lease it writes
is the one the hook finds (#868). A process is a Claude session by one test,
its executable's basename is `claude` (`hooks/hooksession.py#is_claude`),
which the worktree guard's count of other sessions uses too. Two leases
naming one pid are no session. With neither, the commit is the person's
(`questions.md` P2, answer (a)), and the stub leaves before Python starts
wherever no lease file stands in the clone. `hooks/hooksession.py` holds the
two routes and the names they read.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_s9_no_variable_and_no_lease_is_a_persons_own_commit, tests/test_the_commit_gate_decides_at_the_commit.py::test_s9_the_lease_names_the_session_when_no_variable_is_exported, tests/test_the_commit_gate_decides_at_the_commit.py::test_s9_an_emptied_environment_is_still_judged_through_the_lease, tests/test_the_hooks_are_installed_where_git_runs_them.py::test_an_emptied_lease_directory_starts_no_python, tests/test_the_commit_gate_decides_at_the_commit.py::test_the_lease_route_reads_the_exported_pid_with_no_ps_run, tests/test_the_commit_gate_decides_at_the_commit.py::test_the_one_session_variable_is_the_one_the_stub_and_the_reader_name, tests/test_lease_liveness.py::test_the_lease_records_the_process_the_hook_reads_back, tests/test_lease_liveness.py::test_the_lease_records_the_pid_the_harness_exports, tests/test_lease_liveness.py::test_the_guard_counts_the_sessions_the_one_test_names

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**The arms, the marks and the declaration are the ones
`docs/the-review-and-parity-arms.md` states, asked of
`hooks/gate.py#arms_missing`; what changes is how a stop is put.**
A git hook cannot render two buttons, so every stop is the hook's exit status
and its text on stderr, which git prints into the command's output and the
model reads. The text is the same on every attempt. Attended, it tells the
model to put the arm's options to the person with AskUserQuestion; under the
`automation` press it names no question tool. Every option names a command
that runs, the git-native waiver first: `git -c specseal.waive=review commit
…` (and `=parity`), which git hands the hook through `GIT_CONFIG_PARAMETERS`
and which inside a message is prose. The older `: '[no-review]'; git commit …`
keeps working (`questions.md` P3, answer (a)): `hooks/answer-write.py` reads
the bare word out of the Bash call, outside every heredoc body (#773), and
`hooks/answers.py` carries it to the hook for that call alone. The parent and
every subagent share one session id, so the answer is kept per call, under
the payload's `tool_use_id` with the command beside it, and given only to a
commit whose ancestry up to the `claude` process carries that command — the
Bash tool's shell holds it in its argv. Another agent's commit in the same
moment is its own command and is judged, and another agent's call starting or
ending leaves the answer alone.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_s4_under_the_press_the_refusal_names_no_question_tool, tests/test_the_commit_gate_decides_at_the_commit.py::test_s5_an_attended_session_is_told_to_ask_and_the_second_attempt_is_the_same, tests/test_the_commit_gate_decides_at_the_commit.py::test_s5_both_spellings_the_refusal_names_actually_commit, tests/test_the_commit_gate_decides_at_the_commit.py::test_s6_inside_a_message_the_waiver_is_prose, tests/test_the_commit_gate_decides_at_the_commit.py::test_an_old_spelling_waives_no_other_agents_commit, tests/test_the_old_spellings_reach_the_hook.py::test_an_answer_is_given_to_the_call_that_carried_it_and_no_other, tests/test_the_old_spellings_reach_the_hook.py::test_another_call_neither_replaces_nor_clears_an_answer, tests/test_the_old_spellings_reach_the_hook.py::test_a_token_is_a_bare_word_and_nothing_else, tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py::test_s6_neither_read_honours_a_token_the_base_did_not

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**`--no-verify` is met where the branch moves, and nothing else that moves a
branch is.**
`--no-verify` skips `pre-commit` and nothing after it, so
`reference-transaction` refuses, at `prepared`, a commit that `pre-commit`
never judged: HEAD, the index and the working tree stay as they were, with one
unreachable commit object left. What tells a commit from a merge, a reset, a
clean cherry-pick or revert, a rebase or a pull is `GIT_AUTHOR_DATE`, which
every `git commit` exports to its hooks and none of those does on git 2.34.1,
2.39.5, 2.43.0 and 2.50.1 (phase 1's M12). A commit `pre-commit` let through
carries a one-shot mark keyed by the old HEAD, the tree, that date and the
`git commit` process both hooks run under, and passes; a mark a commit left
when it aborted after `pre-commit` is another process's, and passes nothing.
A person who exports `GIT_AUTHOR_DATE` around a rebase makes it look like a
commit, and it meets the refusal: the fail direction is a stop.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_s3_no_verify_is_met_where_the_branch_moves_and_nothing_moves, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_branch_moved_by_anything_but_git_commit_is_not_judged, tests/test_the_hook_surface_git_offers.py::test_only_git_commit_hands_reference_transaction_an_author_date, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_mark_an_aborted_commit_left_passes_no_later_commit

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**A commit git makes for its own rebase, cherry-pick or revert is not judged;
a commit a shell starts while one is paused is.**
A rebase, cherry-pick or revert that stopped on a conflict, and a reword,
finish through a child `git commit`: it hands both hooks the date, runs
`pre-commit` for all but `rebase --continue`, and was refused by both until
round 1 of #692 measured it. 0.16.0's reading judged none of these commands.
What tells that child from a person's commit, on all four gits, is two facts
together: a sequencer state under the worktree's git directory (`rebase-merge`,
`rebase-apply`, `sequencer`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`), and the
`git commit` having been started by another `git` process rather than a shell.
So `git commit --no-verify` or `--amend` typed at a paused rebase is judged,
and so is an alias's commit outside a sequencer. Where `ps` cannot answer --
Windows -- the commit is judged, and the fail direction is a stop.
`GIT_REFLOG_ACTION` is no criterion: only a rebase's children carry it.
A conflicted merge is not one of them. `MERGE_HEAD` is no sequencer state
here, and `git merge --continue` runs its commit in the process the shell
started, so concluding a conflicted merge is judged whether it is typed as
`git commit` or as `git merge --continue`, where 0.16.0's reading let the
second through (round 2 of #692, executed). A merge with no conflict makes
its commit without `pre-commit` or the author date, and is not judged.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_concluding_a_conflicted_merge_is_judged, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_rebase_git_continues_is_not_judged, tests/test_the_commit_gate_decides_at_the_commit.py::test_an_interactive_rebases_reword_is_not_judged, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_pick_git_continues_is_not_judged, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_commit_typed_while_a_rebase_is_paused_is_still_met, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_commit_an_alias_starts_is_still_judged, tests/test_the_hook_surface_git_offers.py::test_a_sequencer_that_stopped_on_a_conflict_commits_with_the_date

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**Where git decides, the PreToolUse reading of
`docs/commit-review-gate-spec.md` §*commit-review-gate (PreToolUse, Bash)*
stands aside; in a clone where it cannot, the commit is judged as 0.16.0
judged it.**
P1's answer keeps a foreign clone on 0.16.0's behaviour, and for the commit
arm that behaviour is `hooks/commit-review-gate.py` reading through
`hooks/cmdline.py`, so both stay (`questions.md` P5). Each target the reader
names is asked `hooks/githooks.py#decides` first and left to git where the
stubs run. A target the reader cannot place is left to git when the session's
own clone is git-decided, because the session's directory is the stand-in it
would have been judged against. **Only a command whose shape is known plain
is left to git at all** (`hooks/tokens.py#is_plain`, `questions.md` P7);
every other command is judged by the reading wherever it lands, which is
what 0.16.0 did with it. Plain is a positive rule rather than a list of
words that step around the hooks, because three review rounds of #692 each
found spellings such a list missed. A command is plain when it splits;
every simple command's program is one of a few words measured from the
commit commands agents type (`git`, `cd`, `true`, `:`, `echo`, `printf`
with no option, `test`, `[`, and `cat`, `head`, `tail`, `grep`, `wc`,
`cut` reading output); each `git` passes only `-C` and a `-c` of
`commit.gpgsign`, `user.name`, `user.email` or `specseal.*` before
`commit`, `add`, `status`, `log`, `diff`, `show` or `rev-parse`; no
assignment stands in a command's place; output goes only to `/dev/null` or
another descriptor; nothing is parsed again (no `$( … )`, backtick, `( … )`
or `{ … }`, and no heredoc body holding a substitution behind an unquoted
delimiter); and none of the words `hooks/tokens.py#steps_around_hooks`
reads appears. A misread costs the one judgment 0.16.0 made.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_the_text_reading_stands_aside_where_git_decides, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_foreign_clone_keeps_the_text_reading, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_command_that_can_step_around_the_hooks_keeps_the_text_reading, tests/test_the_commit_gate_decides_at_the_commit.py::test_only_those_words_make_the_reading_judge_a_git_decided_clone, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_plain_agent_commit_stands_aside_and_one_word_more_is_judged, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_negative_that_is_plain_stays_plain, tests/test_the_commit_gate_decides_at_the_commit.py::test_a_negative_outside_the_allowlist_is_not_plain

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**The convergence argument is claimed for commits alone.**
No git refuses a branch switch before its tree has moved: on 2.34–2.43 a
switch reaches `reference-transaction` with no line at all, and on 2.50.1 the
line arrives after the tree and index already hold the new branch (phase 1's
M1). A worktree creation can be judged after git made it, in `post-checkout`,
but only taken back there, and round 1 of #692 found what a take-back cannot
undo: `worktree add -B` resets an existing branch first, `--no-checkout` and
`--orphan` run no `post-checkout`, and a `--lock`ed tree survives one
`--force`. On the owner's answers of 2026-10-01 (`questions.md` P4, P6) the
worktree guard's switch and creation arms both keep `86256492`'s reading on
every git, pinned so it cannot gain a rule (`docs/worktree-guard-spec.md`
§*Which tree*). Those arms still predict from text, and do not converge.
Enforced by: tests/test_the_hook_surface_git_offers.py::test_no_git_refuses_a_switch_before_the_tree_moves, tests/test_the_hook_surface_git_offers.py::test_what_a_take_back_cannot_undo, tests/test_the_frozen_reading_never_grows.py::test_the_bytes_below_the_rider_are_86256492s

### Known limits of the commit gate inside git

- **A clone no session has reached carries no stubs.** The installer writes
  them for the clone a session starts in or a Bash call's `cwd` is in, so a
  commit by `git -C` into a clone neither ever was is judged by the text
  reading in `docs/commit-review-gate-spec.md` instead. Phase 1 counted 0
  such commits in the three recorded
  runs (M8). A person's global `init.templateDir` or `core.hooksPath` would
  close it, and writing either is outside what this plugin writes.
- **A commit through a construct the reader cannot place, into a clone that
  carries no stubs, from a session whose own clone does, is judged by
  nobody.** The reader stands aside on the session's clone, and git has no
  hook to run in the other one.
- **A command that removes the stubs, or takes their execute bit, before it
  commits steps around both hooks.** `rm .git/hooks/pre-commit
  .git/hooks/reference-transaction && git commit`, and `chmod -x` on the same
  two files, landed with git alone (rounds 1 and 2 of #692, executed). Since
  P7 neither is plain, because `rm` and `chmod` are not among the plain
  programs, so the reading judges each before it runs, as 0.16.0's did. The
  installer puts the stubs and their mode back at the next Bash call.
- **`git commit-tree` with `update-ref`, and `git am`, are not commits to
  either reading.** Neither meets `pre-commit`, and round 1 of #692 executed
  both landing past the backstop, as 0.16.0's reading never read them as
  commits.
- **A commit git starts while a sequencer state is on disk is not judged,
  whoever asked for it.** An alias (`git -c alias.ci=commit ci`) and, where
  `/bin/sh` hands its last command straight to git as macOS's does, a
  `rebase --exec 'git commit …'` both run `git commit` under a `git` parent.
  During a paused rebase, cherry-pick or revert those commits pass as the
  sequencer's own.
- **On Windows** the backstop's mark is keyed without the `git commit`
  process, because each hook there runs under its own `sh.exe`, so a mark an
  aborted commit left can pass a later `--no-verify` commit with the same
  HEAD, tree and date; and no commit counts as the sequencer's, so a
  `rebase --continue` into an undeclared repository is refused.
- **The old spelling waives only where the hook can find the call's shell.**
  It needs `ps` and a `claude` process above the commit, and a shell whose
  argv carries the command, which is how the Bash tool runs one today. Where
  any of the three is missing — Windows, a commit no `claude` started, a
  harness that passes the command another way — the bare word waives
  nothing and the refusal names `git -c specseal.waive=…`, the spelling that
  belongs to its own command. The match drops everything but letters and
  digits, `\NNN` escapes included, and looks for the carried command inside
  the shell's argv, which is what lets the shell's own quoting through. So
  two agents running the same command are both waived, and so is a command
  carrying no token that contains another open call's whole command that
  way (round 2 of #692, executed).
- **Latency.** A judged commit starts one interpreter in `pre-commit`, one in
  `reference-transaction` at `prepared`, and, once it lands, one in
  `post-commit`, which has no narrowing line: 209–400 ms a commit on the
  machine phase 1 measured under load, against 57 ms with no hooks (M10). A
  ref update that is not a commit, a fetch's among them, starts none, and so
  does a person's own commit where no lease file stands in the clone. A lease
  stands for up to a day after its session's last tool call
  (`hooks/session-lease.py` prunes files older than that), and while one does
  a person's commit pays three interpreter starts, `pre-commit`,
  `reference-transaction` at `prepared` and `post-commit`, so the stub can
  look for a `claude` ancestor: round 1 of #692 measured 396 ms against 125 ms with the
  stubs and no lease and 50 ms with no stubs, and the commit was not judged.
  The installer runs first in every Bash call's `pre-bash` group, and with
  current stubs it starts two `git` processes and reads each stub: a median
  113 ms in the dispatcher's process on the machine round 1's fix pass
  measured under load, where one bare `git rev-parse` took 48 ms. That is
  paid on every Bash call in an opted-in clone, a commit or not.
- **Windows** runs the stubs through git's bundled `sh`, and #692's Windows
  pass ran them there on `windows-latest` (CI runs 37013783175 and after).
  Git for Windows' `ps` takes no `-o`, so a hook there finds no `claude`
  ancestor, and `env -i` empties `CLAUDE_PID` as it empties the session
  variable: a commit under `env -i`, which the lease names on POSIX, is a
  person's there. Read from the code, not run on Windows. A command that
  exports `LD_PRELOAD` runs no hook at all: `stdbuf` exports it as an MSYS
  path, the bundled `sh` dies loading it, and git
  commits as if every hook had passed. Neither command is plain
  (`hooks/tokens.py#is_plain`), so the PreToolUse reading judges both before
  they run, as 0.16.0's did.

### Where each state of a repository stands

| State | What judges a commit |
|---|---|
| a clone carrying the stubs | `pre-commit`, then `reference-transaction` for one that skipped it; the PreToolUse reading as well for every command whose shape `hooks/tokens.py#is_plain` does not call plain |
| a clone whose hooks slot is foreign | the PreToolUse reading in `docs/commit-review-gate-spec.md`, as 0.16.0 — said once per session |
| an opted-in clone no session has reached | the PreToolUse reading in `docs/commit-review-gate-spec.md`, until a session or a Bash call reaches it |
| a clone that opted out after the stubs arrived | nothing: each stub reads the opt-in when it runs, and the installer takes them out |
| a person's own commit, with no session behind it | nothing |
