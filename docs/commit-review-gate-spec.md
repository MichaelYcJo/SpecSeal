# commit-review-gate — behavior spec

Authority for `hooks/commit-review-gate.py`, `hooks/review-history-guard.py`
and the implementer mark: how the hooks are registered, which repository a
commit is judged against, the two opt-in arms, and the routing declaration
that moves the review arm's check to the pull request. The review run those
hooks serve is `docs/review-chain-spec.md`'s, and what the pull-request check
reads of a round record is `docs/round-record-spec.md`'s. Update spec and code
together.

## Registration — gates run in groups, not one process each

`hooks/hooks.json` registers `hooks/dispatch.py <group>` per event, and the
dispatcher calls each gate in that group inside one interpreter. A gate is
still a standalone script — that is how it is tested and debugged — but on a
live tool call it does not pay for its own Python startup. Adding a gate means
adding it to `GROUPS` in `dispatch.py`.

When more than one gate in a group returns a decision, the strictest wins
(deny > ask > silence) and **every** reason is kept in the merged text: a gate
that was overruled still has something the user needs to read. A gate that
raises is skipped and the rest of the group still decides — a crashing gate
must not block a tool call.

<!-- specs/1790635415-a-gate-that-fails-to-load-says-so -->
**A gate that fails is said once per session, at the end of the main
session's turn, and the call it failed on still goes ahead.** A failure is an
exception while loading the gate's file, a `SystemExit` included, or an
`Exception` from its `main()`. A `SystemExit` from `main()` is a gate
finishing. A load-time `SystemExit` used to end the whole group. The
dispatcher writes a record under `<git-common-dir>/specseal-gate-failure/`,
keyed by session and gate, in an opted-in repository, and also where
`optin.py` is itself the broken module, because that one cannot tell. The
`stop` group says each pending record once as a `systemMessage`, before the
sealer's stamp where there is one, and nothing the report adds carries a
decision. Before this, a skipped gate read exactly like an allow and nobody
was told. What it still cannot say is a failure it had nowhere to write: a
git directory it cannot write to is as silent as before.
Enforced by: tests/test_a_gate_that_fails_says_so.py::test_a_broken_gate_is_said_at_the_end_of_the_turn_and_only_once, tests/test_a_gate_that_fails_says_so.py::test_a_system_exit_at_load_does_not_take_the_group_down, tests/test_a_gate_that_fails_says_so.py::test_the_report_goes_before_the_stamp_and_the_stamp_is_unchanged

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
The session comes from `CLAUDE_CODE_SESSION_ID`, which the harness exports to
every Bash child and git hands to its hooks. Where it is absent, as under
`env -i`, the hook takes the lease (`hooks/session-lease.py`) whose recorded
pid is its nearest ancestor named `claude`. Two leases naming one pid are no
session. With neither, the commit is the person's (`questions.md` P2, answer
(a)), and the stub leaves before Python starts wherever no lease file stands
in the clone. `hooks/hooksession.py` holds the two routes.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_s9_no_variable_and_no_lease_is_a_persons_own_commit, tests/test_the_commit_gate_decides_at_the_commit.py::test_s9_the_lease_names_the_session_when_no_variable_is_exported, tests/test_the_commit_gate_decides_at_the_commit.py::test_s9_an_emptied_environment_is_still_judged_through_the_lease, tests/test_the_hooks_are_installed_where_git_runs_them.py::test_an_emptied_lease_directory_starts_no_python

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**The arms, the marks and the declaration are the ones below, asked of
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
the bare word out of the Bash call and `hooks/answers.py` carries it to the
hook for that call alone. The parent and every subagent share one session id,
so the answer is kept per call, under the payload's `tool_use_id` with the
command beside it, and given only to a commit whose ancestry up to the
`claude` process carries that command — the Bash tool's shell holds it in its
argv. Another agent's commit in the same moment is its own command and is
judged, and another agent's call starting or ending leaves the answer alone.
Enforced by: tests/test_the_commit_gate_decides_at_the_commit.py::test_s4_under_the_press_the_refusal_names_no_question_tool, tests/test_the_commit_gate_decides_at_the_commit.py::test_s5_an_attended_session_is_told_to_ask_and_the_second_attempt_is_the_same, tests/test_the_commit_gate_decides_at_the_commit.py::test_s5_both_spellings_the_refusal_names_actually_commit, tests/test_the_commit_gate_decides_at_the_commit.py::test_s6_inside_a_message_the_waiver_is_prose, tests/test_the_commit_gate_decides_at_the_commit.py::test_an_old_spelling_waives_no_other_agents_commit, tests/test_the_old_spellings_reach_the_hook.py::test_an_answer_is_given_to_the_call_that_carried_it_and_no_other, tests/test_the_old_spellings_reach_the_hook.py::test_another_call_neither_replaces_nor_clears_an_answer

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
**Where git decides, the PreToolUse reading in the next section stands aside;
in a clone where it cannot, the commit is judged as 0.16.0 judged it.**
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
  reading below instead. Phase 1 counted 0 such commits in the three recorded
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
  ancestor: the session comes from `CLAUDE_CODE_SESSION_ID` alone, and a
  commit under `env -i`, which the lease names on POSIX, is a person's
  there. A command that exports `LD_PRELOAD` runs no hook at all: `stdbuf`
  exports it as an MSYS path, the bundled `sh` dies loading it, and git
  commits as if every hook had passed. Neither command is plain
  (`hooks/tokens.py#is_plain`), so the PreToolUse reading judges both before
  they run, as 0.16.0's did.

### Where each state of a repository stands

| State | What judges a commit |
|---|---|
| a clone carrying the stubs | `pre-commit`, then `reference-transaction` for one that skipped it; the PreToolUse reading as well for every command whose shape `hooks/tokens.py#is_plain` does not call plain |
| a clone whose hooks slot is foreign | the PreToolUse reading below, as 0.16.0 — said once per session |
| an opted-in clone no session has reached | the PreToolUse reading below, until a session or a Bash call reaches it |
| a clone that opted out after the stubs arrived | nothing: each stub reads the opt-in when it runs, and the installer takes them out |
| a person's own commit, with no session behind it | nothing |

## commit-review-gate (PreToolUse, Bash)

This is the reading 0.16.0 shipped, and since #692 it judges only where git
cannot: a target in a clone without this plugin's stubs, a target it cannot
place from a session whose own clone has none, and a command whose words can
keep the hooks from judging it. The section above says when it stands aside,
and everything below describes it as it was.

The hook carries **two opt-ins, evaluated independently**. Each has its own
mark, its own waiver token and its own silence rules, and neither is nested
behind the other: one arm being satisfied never suppresses the other's prompt.

They are no longer declared independently, and that changed at 0.10 without
anyone noticing. The migration config lives at `seal/parity.md`, so
writing it creates `seal/` — the directory whose existence is the review
opt-in. A repository with a migration config and no review opt-in cannot be
built through any address the plugin documents or writes.

This paragraph used to claim the opposite, and the claim stayed true only
through the pre-0.10 `docs/parity.md`, which no user-facing document has ever
named and which nothing in the plugin has ever written. That read was removed
rather than documented, on the grounds that the address had no
users; removing it is what made the collapse visible. A repository that wants
the parity arm and not the review arm waives the review arm per command with
`[no-review]`, which is what the tests here do.

| Condition | Decision |
|---|---|
| not a `git commit` command | silent |
| neither opt-in applies | silent — a globally installed plugin must not nag unrelated repos |
| the command names a `-C` the gate cannot resolve | **stopped** — see below |
| every applicable mark equals current HEAD | allow |
| no session id in the payload | **ask** — nowhere to record that the choice was put up, and a deny would then repeat forever |
| this session's person pressed `automation` on the routing question | **deny**, every time, whose reason names the ways on that need nobody and **puts no question to anybody** — see *Why a deny, and why only once* |
| otherwise, first time this session meets it in this repo | **deny**, whose reason **instructs the model to put the choice up** with AskUserQuestion, naming both ways on for every arm that fired |
| otherwise | **ask**, which is the harness **putting two buttons to the user** — every missing mark named at once, and approving IS the waiver |

Those last two rows are different acts and the word "asks" covers both, so it
is not used for either on its own. A `deny` addresses the **model**: the hook
cannot render a dialog, so it spends its reason on instructions and hands the
turn back. An `ask` addresses the **user**: the harness renders two buttons
that the model never sees, and declining is a bare "No".

### Which repository, and what happens when it cannot be read

<!-- specs/1788305134-the-reader-stops-where-it-need-not -->
**The repository judged is the one the command commits *into*, not the one the
shell sits in.** `git -C <path> commit` moves git without moving the shell, so
the directory comes from the command and falls back to `cwd` only when the
command names none. Repeated `-C` compose. A command committing into two
repositories is judged for both.

The shell moves too, and reading only `-C` missed it. `cd <path> && git commit`
leaves the shell somewhere else before git runs, so the gate judged the
directory the session started in — measured wrong in both directions, and in
the one that matters a routing declaration found in the session's own
repository silenced a commit landing in a repository that had never given that
answer. There was no moment on that path at which anyone could
have typed a waiver or clicked a prompt. Every directory a command can commit
into is resolved from the command, `cd` included.

Which directories it reaches depends on the operator joining the segments.
`&&` and `||` are opposites: `&&` runs the commit where the `cd` arrived,
`||` runs it only if the `cd` failed, which is where the shell already was.
The pipe and background operators are a third case — they open a subshell, so
a `cd` on one side of them does not move the shell the commit runs in at all.

| The command | What is judged |
|---|---|
| `cd X && git commit` | the repository holding X |
| `cd X ; git commit` | both — `;` runs the commit whether the `cd` succeeded or not, so a failed `cd` leaves it in the session's own repository |
| `cd X \|\| git commit` | both — the session's own repository and X |
| `cd X \| git commit`, `cd X \|& git commit`, `cd X & git commit` | both, and for a different reason: the commit runs in a subshell that never left the session's own repository, and a shell told to run a pipeline's last stage in the current shell (`shopt -s lastpipe`) does land in X |
| `cd N \|\| cd B && git commit` | both N and B — the second `cd` is skipped whenever the first works |
| `cd X && git commit`, where X is inside the session's own repository | that one repository, with the verdict and the prompt unchanged |

A segment joined by one of those operators may never run, so the directories
in front of it stay candidates past it. Reading only the operator that
*follows* a segment loses that: `cd N \|\| cd B && git commit` kept B alone,
and where B carried a declaration the commit went unjudged.

**Where an operator is written does not change which operator it is.** An
operator at the end of a line — the ordinary way to write a long command — put
the line break directly behind itself, and a run of shell punctuation reads as
a single token, so `cd X \|\|` and a newline arrived as one operator that
matched none of these rules. The line break is read as its own separator, the
first operator after a segment is the one that binds it, and a backslash
before a line break is a continuation whose two characters both go.

**Only what the shell would EXECUTE is read as commands.** A heredoc body is
data the shell feeds to a command on stdin, so the gate drops it before
splitting, exactly as it drops a comment. Writing a script and then committing
it is ordinary, and every newline being a separator meant a `cd` on the second
line of `cat > run.sh <<'EOF'` moved the reader's shell — the commit after the
terminator was then judged against a repository the shell never entered, with
the session's own directory absent from the candidates altogether. A `<<`
inside a comment opens nothing, `<<<` is a herestring and opens no body, and a
body whose terminator never arrives runs to the end, which is what the shell
does with one. Neither does `$((…))` open one: the `<<` in `n=$((1<<2))` is an
arithmetic left shift, and reading it as a redirect took `2))` for a delimiter
and dropped every line after it looking for a match no line makes — so a
commit written below it did not arrive misjudged, it did not arrive at all.
This is a JUDGMENT read; the scan for a waiver token still sees the command as
written.
Enforced by: tests/test_gate_judges_the_repo_it_commits_to.py::test_a_commit_aimed_elsewhere_is_judged_there, tests/test_gate_judges_the_repo_it_commits_to.py::test_a_cd_reaches_the_repository_the_commit_lands_in

<!-- specs/1788184145-the-gate-stops-the-session-editing-its-tests -->
**A file edit goes through the `Edit` tool, because a shell command that only
edits a file is still a command line this gate reads.** Dropping a heredoc
body from the walk decides where a commit lands; whether the command commits
at all is asked of every body separately, as shell, on purpose, because a
commit hidden in a body used to walk straight past (legacy #75). Two kinds of
segment count there. One is a segment whose command word is `git` with the
`commit` subcommand, so what counts is the position and never the presence of
the word: a fixture file of shell commands held in Python strings can read
clean whole, while an eight-line patch of that file trips (#34). A string a
shell would run is a position too — the one `sh -c` is handed, or the inside
of `$( … )` or a backtick pair (#670) — and this repository's own fixture
files hold commits in exactly those, so since #670 they trip whole. The other
has no
commit in it at all — an `eval` whose argument the reader cannot expand
stops the session, since nothing can tell what it reduces to without running
the shell. So a session that searched its patch for a commit and found none
has not cleared it, and an edit the `Edit` tool makes leaves no command line
to read. Skipping a body that is only being written to a file would reopen
#75, and that trade is the repository owner's to make.
Enforced by: tests/test_edits_go_through_the_edit_tool.py::test_the_rule_names_the_tool_and_pairs_its_two_reasons, tests/test_gate_judges_the_repo_it_commits_to.py::test_an_interpreter_fed_heredoc_body_that_commits_stops

<!-- specs/1788305134-the-reader-stops-where-it-need-not -->

**A failure branch waits for the operator that runs it.** `cd X && make \|\|
git commit` commits where the shell is when the `cd` fails, and that is the
directory the session started in. Reading only the operator immediately after
a segment lost it as soon as anything stood between the `cd` and the `\|\|`.
The directory a failed command leaves the shell in is carried until something
consumes it, and a failure branch nothing ever reaches is not reported — which
is what keeps `cd X && git commit` answering for X alone.

**Two operators consume one, not one.** `\|\|` runs its right side only from
the failure branch; `;` — and a newline, which is the same operator written
differently — runs it from both, which is why `cd X ; git commit` answers for
two repositories where `cd X && git commit` answers for one. Only `\|\|` was
treated as a consumer, so the session's own repository dropped out of the `;`
answer and a routing declaration in X silenced a commit that could land in
either. `bash -c 'cd /no/such/dir ; pwd'` prints the directory it started in.

**The reader enumerates what it understands, not what moves a shell.** Where
it met a construct it did not model it answered *the shell stayed where it
was*, and that is a confident answer rather than an absent one: a stop where
the session's own directory needs review, and a silence where that directory
carries a declaration and the commit lands elsewhere. Measured on seven
commands, five leaked — a `cd` inside a function body, a sourced script, an
`eval`, a `pushd`, and a loop, with `command cd X` a sixth found alongside
them. Filling the parser in is not the fix; the list of constructs that move a
shell is not one anybody finishes, and every one still missing resolves
confidently to the wrong directory.

So a segment the reader can read as a simple command — a literal command word
and its arguments — leaves the shell where the reader computed it, and every
other segment leaves it **unreadable**, which is the stop below. What is
enumerated is therefore the shell's reserved words, which are a closed and
documented part of its grammar, rather than the open list of things that
relocate a shell. The remaining error changes direction with it: a construct
nobody added to the understood set reads as not understood, and stops.

**Exclusive branches are not walked as one.** A directory reached by a branch
that succeeded is not somewhere the alternative branch then runs, so
`cd build \|\| cd dist` reaches build or dist and never `build/dist`. That
composed path is not merely extra: it exists nowhere, so it resolves to no
repository, and a target that resolves to nothing is reported as unreadable —
which returns before the real verdict is used and puts a directory the user
never typed in the prompt. Sixteen branches produced 65536 such candidates.
What is still bounded only by a bound is every shape whose reachable
directories genuinely multiply — a chain of pipe stages, one of `;`, and one
alternating `&&` and `\|\|`. Those directories are all real, so the bound
limits how much answering the reader will do rather than correcting anything;
past it the command reads as one whose directory could not be computed.

The last row is what keeps this cheap. Where every directory a command reaches
sits in one repository, the operator does not matter and neither does the `cd`:
the common `cd src && git commit` costs exactly what it cost before, compared
byte for byte against the parent commit. Prompt volume is the problem reading
the command was added to reduce.

The gate reads `tool_input.command` **before the shell expands it**. So a `-C`
whose value is a shell variable arrives as the literal characters `$WT`, names
a directory that does not exist, and resolves to no repository. A path that was
simply typed wrong looks identical from here — there is no reading of the
command that tells them apart.

That target is not a repository the gate checked and found clean. It is a
repository the gate never saw, and until the release that closed it, both
produced the same nothing. Every agent in that release session was instructed to
commit with `git -C "$VAR"`, and every one of those commits passed a gate that
had looked at nothing.

| What the gate has | What it does |
|---|---|
| a `-C` it resolved to a repository | judges that repository — its opt-in, its marks |
| a `-C` it could not resolve, in a session whose own repository opted in | **stops**: deny once per session per repository, then ask — or deny every time, where the session's person pressed `automation` |
| a `-C` it could not resolve, anywhere else | silent — the plugin has no standing in a repository that never opted in |
| no `-C`, and `cwd` is no repository | silent — there is no repository and no command naming one |

The session's own repository decides *whether* the gate speaks, never *what is
true* of the target. Judging an unresolved target against the session's marks
would answer for a repository the commit may never touch, which is the defect
`-C` parsing was added to fix.

The two ways on are ordered deliberately. The first is to write the path out,
because that is what lets the gate reach a verdict at all; `[no-review]` is
second and works exactly as everywhere else.
Enforced by: tests/test_gate_judges_the_repo_it_commits_to.py::test_a_failure_branch_survives_an_intervening_segment

#### A `cd` the gate cannot read

The rest of the shell is deliberately not implemented. A `cd` whose
destination cannot be computed is treated as one that cannot be computed,
rather than followed to a guess:

| The `cd` | Why it cannot be read |
|---|---|
| `cd "$WT"` | the command is read before the shell expands it — the same fact that leaves a `-C` variable unresolvable |
| `cd /tmp/x*`, `cd {a,b}` | names a set of paths rather than one |
| `(cd X && git commit)` | the closing parenthesis decides whether the commit runs inside the subshell or after it, and finding that reliably is a shell parser. The `git commit` itself IS read — a subshell opener is taken off the command word and a closing parenthesis off the subcommand, because `(git commit)` commits for real and used to be invisible to the gate entirely |
| `cd -` with nothing behind it | there is no previous directory to return to |

Each takes the treatment the table above gives an unresolvable `-C`: a stop
where the session's own repository opted in, silence anywhere else. It is that
same partition and not a second one. A hook that follows a construct it half
understands is back to being confidently wrong, which is the failure this
section exists to describe — and the same-root collapse is what limits what
the honesty costs, since a destination inside the right repository changes no
verdict.

`hooks/worktree-guard.py` reads a command the same way, because the parsing is
shared and a session that walks to another repository to switch a branch there
was judged against the tree it started in. Its answer for a destination it
cannot read is the opposite one: it keeps judging the session's own tree,
which is where today's answer already was. What that guard protects is a tree
two sessions would share, so stopping is not available to it and going silent
would be a fail-open.

**A commit behind a reserved word that begins a command list is a commit.**
`for d in a; do git commit -m x; done`, `while …; do git commit …; done` and
`if true; then git commit …; fi` reached the gate as no commit at all (#669):
the shell splits them at `;`, the commit arrives in a segment whose first word
is `do` or `then`, and the reader looked for `git` in that position alone. The
same commands written across lines were always judged, because there the
reserved word stands on its own line and the commit follows a segment the
reader does not understand.

So after `do`, `then`, `else`, `elif`, `if`, `while`, `until` or `{`, the next
word is read as the command word, and the segment gets the directory its
multi-line spelling has: unresolved, which is a stop wherever the session's
own repository opted in, before any declaration is read. Inside a `case` arm,
a function definition or a coprocess no position names the command word, so
the first `git` word stands in for it — a wrong one is a stop, never a
silence. `!` and `time` stand in front of a command without opening a list,
and a commit behind them is judged where the shell is. `for`, `select`, `case`
and `in` are followed by names and words rather than commands, so
`for d in git commit` reads nothing.

The reading can only have gained stops by this. Every segment the new reading
reaches began with a word at which the old one found no command, so no commit
the base read is read differently, and the directories it marks unresolved
are those segments' own. What that argument could not see is the fallback for
a command the splitter could not finish, which is not a segment: a commit
found behind `do` in a declared repository took the session's own directory
out of the judgment, until the fallback came to stand beside what was found
(round 1 of work item 1790644505, and the #670 statement below).
Enforced by: tests/test_a_commit_behind_a_reserved_word_is_judged.py

**A commit behind a wrapper, in a shell string or in a substitution is a
commit.** `exec git commit`, `nice git commit`, `timeout 5 git commit`,
`xargs git commit`, `sh -c 'git commit'` and `echo $(git commit)` each reached
the gate as no commit at all (#670): the reader knew five wrappers by name,
stopped at the first word it did not know, never read a string handed to a
shell, and never looked inside a substitution.

So three readings are added. A program that runs its operands as a command
(`cmdline.RUNNERS`, an enumeration of POSIX's, GNU coreutils', util-linux's,
the privilege tools', the tracers' and `find`, `parallel`, `watch` and
`script`) is read past: directly in front of `git` the commit is judged where
the shell is, and behind the program's own options or operands, which the
reader does not parse, the first `git` word stands in and the directory is
unresolved. A string `sh -c`, `bash -c`, `su -c`, `script -c`, `flock -c`,
`env -S` or `watch` hands to a shell is read as a command the way `eval`'s
argument already was, and a command word the shell would expand in the string
a host runs (`sh -c "$CMD"`) counts as one that might commit. `parallel`'s
arguments are read for a commit written out, and no further: placing its
command word means parsing its options (#674). That question is not
asked of a shell's positional parameters or of `watch` as a word something
else was handed, because no shell runs those (`find -exec sh -c '…' _ {}`,
`grep watch *.py`). An `eval` is found the same way `git` is, behind a
reserved word, a prefix, a runner or a subshell. The body of a `$( … )`, backticks,
`<( … )` or `>( … )` is read as a command the way a heredoc body is; a
single-quoted one is text. A commit found in a string or a substitution runs
somewhere the walk does not place, so it stops wherever the session's own
repository opted in.

What stays unread is a program whose operands are a script or a remote
command rather than a command here — `bash run.sh`, `source`, `make`, `uv
run`, `npx`, `ssh`, `docker exec` — because reading it would mean reading
files or machines, not the command. Each stays silent as it was.

The reading can only have gained stops by this, for the reason #669's change
gives, and for one more: a command the splitter could not finish is still
judged in the session's own directory when the new reading found a commit in
the part it did read. Without that, a commit found in a declared repository
took the session's directory out of the judgment (round 1 of work item
1790644505). A body nested deeper than the reader reads — `NESTING_READ`, 32
levels, or the recursion limit where that comes first — reads as one that
might commit, beside every commit already found, since a gate that raises is
skipped and a skipped gate is silence; catching the raise around the whole
reading had thrown away a commit it had found in another repository (round 2
of work item 1790644505).
Enforced by: tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py

**A program word is read where the shell reads one, whatever stands in front
of it.** `2>/dev/null git commit`, `git 2>/dev/null commit`, `2>&1 git
commit`, `(sh -c 'git commit')`, `bash -c 2>/dev/null "$CMD"` and `watch` in
a `case` arm or a function body each reached the gate as no commit at all
(#674), and bash landed every one it was given. The readers above stopped at
the first word they did not know, and a redirection, a compound command's
header and a `(` glued to the program are each such a word.

So each place a program word stands is read past what the shell takes off it:

- **A redirection** in front of the program or before git's subcommand, glued
  or spaced (`2>/dev/null`, `2> /dev/null`, `<<<w`, `<< EOF`, `{fd}>f`, zsh's
  `>!f`), is read past to the word it stands in front of. A commit there is
  judged where the shell is, as the same commit without it is. A `cd`, a
  relocator, a reserved word or an expanding word reached past one adds an
  unresolved directory beside the one the walk read without it, and never
  replaces it: `[no-review]` waives an unresolved target whole, and a session
  that is not opted in reads one as silence, so a replaced directory is a
  stop lost. The same holds for zsh's `noglob`, `nocorrect` and `repeat N`,
  for a redirection glued to a word's end (`cd>/dev/null W`), and for one the
  splitter cut (`2>&1 cd W`). A redirection after a `cd`'s operand, or glued
  to one (`cd W 2>/dev/null`, `cd W>/dev/null`), is the shell's as well. The
  landing read past any of these is added in front of the directory the walk
  read with it, and the gate judges both. The worktree guard and the consent
  writer read none of this list's additions. They take one answer where the
  gate takes all, so since #689 they read a command through a frozen copy of
  `86256492`'s reader, and for them this `cd` does not move the shell and a
  git behind a redirection or a zsh prefix is not git
  (`worktree-guard-spec.md` §*Which tree*).
- **A redirection glued to the end of a word** (`git>/dev/null commit`, `git
  commit>/dev/null`, `sh>/dev/null -c`) is cut off into a view read beside the
  segment, adding only what the segment did not find. A descriptor in front
  (`2>f`), bash 4.1's `{fd}>f` and a quoted word holding a space stay whole.
- **The operators the splitter cuts at `&` or `|`** — `2>&1`, `>&2`, `<&0`,
  `>&-`, `>|f`, and `&>f` after a word, `git>&2` among them — are glued back
  into a view the gate reads beside the segments, adding only what no segment
  found on its own. The walk asks that view too, where a `cd` behind one
  stands. The splitter itself is unchanged, because teaching it these
  operators moves every segment in both gates and in the walk.
- **zsh's precommand words and short loops** — `noglob`, `nocorrect`, `repeat
  N`, `for i (…) cmd` and `foreach i (…) cmd` — are read past as runners, the
  count and the word list as operands.
- **Inside a `case` arm, a function definition or a coprocess,** `watch` and
  the command word of a host's string are read by position, and a header
  spelling the reader does not place falls to the stand-in `git` already had.
  Behind a runner's own options inside a string, which the reader cannot tell
  from the program, a later word that expands counts. None of these three counts
  a redirection's target. Past 32 headers, one inside the next
  (`HEADERS_READ`), the program counts as one the reader does not place.
- **A host glued to a subshell's `(`** is a host, and a string picked after a
  host's flag is read past a redirection written there, and past the options
  and `--` behind that redirection (`bash -c 2>/dev/null -- "$CMD"`).

`sudo -s` and `sudo -i` are not string hosts: `man sudo` says the command
is escaped a character at a time before it reaches the shell's `-c`, so a
quoted string is one word there and not a command line. Their argument form
is `sudo` the runner's.

The reading can only have gained stops by this. Every reader asks what it
asked before first and adds what the new reading finds, `understood`'s
refusal is added beside the directory the walk read before, the walk's
reading past redirections unplaces a segment beside its directory and never
in place of it, and a generated
corpus of 11,393 commands across these positions found none silent where the
release base stopped. The one answer
replaced rather than kept is git's subcommand where it had been a redirection,
which no reader acted on. Over 6,033 commands recorded in the milestone's
runs, none changed its verdict.

That holds past the walk's `STATE_CAP` as well. Past 64 directories the walk
collapses into one it cannot read, and the directories added beside count
toward the cap, so a chain of `cd` segments reaches it sooner than the base's
walk did: nine `2>/dev/null cd W;` in a row, or a refused segment followed by
sixteen `cd W;`. So the walk carries the base's own states in a thread of
their own, with none of the additions and the same collapse at the base's
length, and every segment's directories are the walk's followed by that
thread's (question Q7 of work item 1790660768). Where the walk names none,
the base's come first. This gate judges every directory, so that order
decides none of its answers, but it is the order the deny names its targets
in. The worktree guard and the consent writer do not read this walk: they read
through a frozen copy of `86256492`'s reader (#689), so no order of the two
decides the tree they judge. The `cd` behind a redirection, the depth bound and
the cap are held by `tests/test_no_shape_the_base_stops_reads_silent.py`.
Enforced by: tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py

### Why a deny, and why only once

A hook returns allow/deny/ask and nothing else, and the harness renders an
`ask` as two buttons the model never sees. Declining is then a bare "No", and
the user who wanted the *other* way on has to retype the command themselves —
the yes/no shape `implement` §1 rejects, still present after the reason string
was made to name both continuations. Denying gives the model the turn back and
spends the reason on the question, which is the shape measured in
`hooks/review-skill-gate.py`.

Firing once per session per repository is what keeps that from being a trap.
The marker is `<git-dir>/specseal-commit-choice/<session-id>`, with the session
id reduced to its basename first — it names a file, and a malformed id with
separators in it otherwise escapes the directory. An unwritable marker counts
as already asked, since one missed question beats a deny nothing can get
past. Every attempt after the first meets the plain `ask` — which is
also the answer for an environment with nobody to ask: one extra round trip,
then today's behavior.

**Where the person said nobody would be answering, every stop is a deny.** A
session whose person pressed `automation` on the routing question was
promised that nothing stops to ask, and an `ask` is a person's prompt. So
there the sentence above is reversed: the gate denies at every stop, in both
arms and at both decision sites, and the reason names the ways on that need
nobody — a commit whose repository the gate can read, an edit through the
`Edit` or `Write` tool, the waiver only for a commit no work item owns, and
otherwise handing the commit back. It names no question tool, and says that
re-issuing the command unchanged meets the same refusal.

Measured in the milestone-49 run (#662, #665): four stops reached the person
as prompts. The main checkout's one deny had been spent by the orchestrator's
own loop, and the marker is keyed on the git directory and the session id
alone. A subagent's call carries its parent's session id, so every later stop
in that repository, from every agent in the run, was an `ask`.

The press is the one `docs/worktree-guard-spec.md` §*Creation consent* reads,
through the same reader, `hooks/worktree_consent.py#automation_answered`, and
it stands for the same reason: the harness writes it from the click, and the
model writes the question and never which option was pressed. It is read
against the session's own repository, which is where standing to speak comes
from, and only once a stop is decided, so what the gate stops does not move.
A `per axis` answer and a `routing.md` `Automation` row are not read, for the
reasons that section gives, and such a run still meets the ask. The last
answer to the routing question from this clone is the one that stands, so a
later `per axis` takes an earlier press back.

This blocks more and never allows more. Where the base asked, a click let the
commit through; a deny never does. Every way of not reading the press — no
session id, no transcript, a shape the reader refuses, a reader that raises —
is the answer above, because a gate that raises is skipped, and a skipped gate
is silence. A wrong refusal costs the model a turn. The bound on a model that
re-issues the same command is the reason's text alone, and whether it holds is
a measurement owed at the next automation run.
Enforced by: tests/test_an_automation_run_meets_no_commit_prompt.py

**Two readings that prompted that run stay as they are.** `cd X && x` on one
line and `git commit` on the next reaches the session's own directory whenever
the `cd` fails, which is *Two operators consume one, not one* above (#662). A
heredoc body is read as shell for whether it commits, which is *A file edit
goes through the `Edit` tool* above (#665). Work item `1790635415` narrowed
both — trusting an existing `cd` target not to fail, and reading a body fed
to a known interpreter as data — and its rounds 2 and 3 found commands the
narrowed gate read silent where the base stopped them, and a real bash ran the
commit for every one it was given: a flag after the `<<`, a bundled `-Bc`, a
`$(…)` or `${…;…}` moving the boundary, a `#` glued to the delimiter, and an
earlier segment or an assignment prefix moving the `cd` target. Each fix
narrowed further than its proof, so the reading stays where it was, and what
changed is who a stop is put to. The changes to the reading are the two
stricter ones above: a commit behind a reserved word (#669), and one behind a
wrapper, in a shell string or in a substitution (#670). Every one of those
commands still stops, with the press and without.
Enforced by: tests/test_no_shape_the_base_stops_reads_silent.py

**Both arms, one call.** When both arms fire, the reason asks for two
questions inside a single AskUserQuestion call rather than one question with
four combined options. The arms are waived independently, so combining them
makes every label carry two facts and multiplies the option count; one call
still costs one interruption.

### Review arm — opt-in: `seal/` at the repo root

| Condition | Decision |
|---|---|
| `[no-review]` in the command | silent (explicit skip, visible in history). Typed in front of it: `: '[no-review]'; git commit …` — see below |
| a `routing.md` declaration names this branch, for either answer | silent — the routing question was answered before the first edit, and CI checks the answer at the pull request. See *The declaration* below |
| `specseal-reviewed` equals current HEAD | satisfied |
| the change confined to `docs/`, `seal/` | no different from any other change — this arm reads no paths. The parity arm's silence on the same roots is that arm's alone, and the paragraph below says why |
| otherwise | contributes an ask |

<!-- specs/1790154759-the-review-arm-asks-where-no-reviewer-compares -->
**The review arm reads no paths: a change confined to `docs/` and `seal/`
meets it as any other change does, and a lighter tier is declared, never
inferred.**

**Why this arm has no document-root line.** The two arms ask different
questions. The parity arm asks whether the original was consulted, and a
`docs/` file has no original, so its silence there is right. This arm asks
whether anybody reads the change before it lands, and here `docs/` is the
policy the code conforms to and `seal/ledger.md` is the verified evidence.
#518 measured whether review finds defects there before drawing any line,
and it does. Across every round record, at least 25 fixed findings sit in
`docs/` alone and 26 in the ledger alone. #514's fold, which changed `docs/`,
`seal/` and four test files, opened seven findings a later round verified as
fixed, all in `docs/`, one of them 🔴. No reviewed work item was ever confined
to the two roots, and the seventeen docs/seal-only commits on the release
branch never reached a reviewer, so nothing measured them either way. The
parity arm's line would stop asking exactly where the reviewed findings sit,
on the strength of a population nobody measured. A documentation pass that
should reach nobody is routed that way before the first edit, by declaring
`straight to the PR`; it is never inferred from the paths it touches.

The marker is decided when the work starts, not discovered at the commit
(`implement` §1) — and until the release that added `routing.md`, nothing
recorded it, so the gate had to
re-derive the answer at every commit and could only ask. The branch that
submitted to review was interrupted at every step; the branch that skipped
review was silent. The incentive ran backwards, and it ran backwards for
exactly the work the chain exists to serve.

Approving is still per commit and the marker still per command. What changed
is that the routing answer now has somewhere to live, and the check it
silences now happens at the pull request instead. See below.
Enforced by: tests/test_chain_hooks_hardening.py::test_the_review_arm_asks_on_a_document_only_commit

#### Where the marker goes, which is not where it is read

`has_marker` finds a bare word anywhere in the command. Where it can be *typed*
is a separate question, and the prompts answered it wrongly for three releases
After `git commit`, a bare word is a **pathspec**, so
`git commit -m x [no-review]` is rejected by git before the gate's advice can
help. The gate stopped the commit, the escape it named failed, and approving
the prompt was left as the only thing that worked — the outcome the wording
exists to offer an alternative to.

Measured in three shells:

| Form | bash | `zsh -c` | interactive zsh |
|---|---|---|---|
| `git commit -m x [no-review]` | rejected (pathspec) | rejected | rejected (unmatched glob) |
| `git commit -m x  # [no-review]` | commits | commits | **rejected** — `#` is not a comment there, so the marker globs |
| `: '[no-review]'; git commit -m x` | commits | commits | commits |

So the advised form puts the marker in front, inside a no-op `:` command. The
shell discards it, git never sees it, and the word stays in the command where
shell history keeps it — which is the whole point of a waiver that is supposed
to be visible.

`tests/test_the_waiver_can_be_typed.py` runs the advised form against real git
in every non-interactive shell present, and pins the rejected form too. The
interactive-zsh row is recorded rather than run: an interactive shell in CI
needs a tty and sources a user's rc.

#### The declaration, and where the check went instead

<!-- specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer -->
**The gate reads `seal/specs/<work-item-id>/routing.md` before it reads anything
else.** Where a declaration is in force the review arm stays silent — for
**either** answer, because the routing question was answered before the first
edit and asking for `[no-review]` as well is asking for the same answer twice.

| The declaration says | At the commit | At the pull request |
|---|---|---|
| through the review chain | silent | a committed `rounds/round-N.md` is required, every commit its `Target SHA` names being REACHABLE — an ancestor of HEAD, or of the branch `routing.md` declares — its last round's `Pass` **checked**, that claim consistent with its own verdict table, and its `Fixes checked by` naming a checker the repository can confirm. A record this pull request does not touch keeps every requirement except reachability: its commits are expected to be gone, and the review it records was enforced at the pull request that added it. A record it RESTORES byte-for-byte from the merge base's own history — the same bytes at the same path in any commit the merge base reaches — is judged the same way, because an earlier pull request added those bytes. One byte changed and the record is this pull request's claim again |
| straight to the PR | silent | the sealer's `broad-gate.md` in the work item's directory, for a work item begun at or after `chain_check.py`'s `DIRECT_GATE_FROM` — the one broad run, at a SHA the tree can see, against the base — and nothing else: the answer turns off the reviewer alone. A draft pull request is excused the file, an earlier work item is excused and prints, and the declaration is printed either way, because a decision nobody sees is not a record |
| nothing readable, or no file | today's behavior — deny once, then ask | pass, with a notice saying nothing was checked |

What the check reads of each round record under the first answer, and what
each refusal costs, is `docs/round-record-spec.md` for the record's rows, and
`docs/review-chain-spec.md` for the floor, `Needs a fix`, the reopening and
when the record was written.
Enforced by: tests/test_routing_is_recorded.py::test_a_declared_chain_item_commits_without_a_prompt, tests/test_routing_is_recorded.py::test_a_declared_direct_item_commits_without_a_prompt, tests/test_chain_check_at_the_pull_request.py::test_a_record_restored_from_the_bases_history_makes_no_reachability_claim

<!-- specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row -->
**`straight to the PR` owes the sealer's `broad-gate.md` and turns off the
reviewer alone, and `Review` has two answers, not three.**

**Two answers, and not three.** A session that wrote a change and then checked
it itself has asked for a third — *reviewed by the session* — with a record of
its own (#241). There is none, and the reason is what the chain's record is
worth: something, only because somebody other than the author wrote it.
`Fixes checked by` refuses *the session that wrote them*
(`docs/review-chain-spec.md` §*Two records, and what each of them says*),
`Ran by` is the spawning
session's row and never the agent's own, and the contract names a review that
certifies itself as what the commit gate exists to catch. What the author's own
check leaves that CI can read is what it RAN — the broad gate at a SHA against
a base — and that is the sealer's stamp, which `straight to the PR` already
owes in the row above. The reading half, *here is what I checked*, is prose,
and prose is not evidence. So a change its author checked declares `straight
to the PR` and takes the broad run; what that answer turns off is the reviewer,
and nothing else. A change belonging to no work item at all is the routing
question's third answer, `no work item`, whose recorded form is `[no-review]`
in front of each commit — there is no value meaning no enforcement anywhere.
Enforced by: skills/code-review/scripts/chain_check.py::direct_seal

<!-- specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer -->
**A declaration the pull request RETIRED is not one it made**, and neither is
one it only renamed. Both are ways a `routing.md` leaves a diff without
anybody declaring anything, and both are excluded: the rename because the
root move renames every declaration in the repository at once, the
retirement because `settle --retire` removes a released work item's directory
after a `docs/` policy has absorbed its spec, and that work item was reviewed
at its own pull request. The first fold put 88 retired declarations in one
diff, and this check failed all 88.

**The marker is what tells a retirement from a deletion**, because both leave
the file absent at `HEAD` and nothing else can. Where `docs/` carries the
work item's `<!-- specs/<work-item-id> -->` comment on a live line, the check
prints `retired: …` and reads no further; where it does not, the refusal stands —
that is a directory removed with nothing absorbing it, which is what the
refusal was written for. It is the same distinction
`unverified_check.folded_items` draws for a removed `overview.md`, and this
reader had not grown it.

**The rule is the other way a declaration is retired, and it carries no
marker.** `settle --retire` also removes a released directory that held no
`spec.md` and nothing open in its record, because a record of a moment states
no rule to fold (#517). So a declaration absent at `HEAD` whose directory is
gone is asked one more question of the merge base: did the directory hold no
`spec.md` there, and nothing open in its `overview.md` or `evidence-todo.md`?
Where it did not, the check prints `retired: by the rule — …`; where the merge
base held a spec or an open row, the refusal stands. The question is
`unverified_check.retired_by_rule`, the one predicate `settle`,
`unverified_check.py --baseline` and the survivor sweep ask too, so the four
cannot disagree about the same tree the way the marker arm once did. Asked of
the merge base rather than of the tree the branch left, and asked whether the
directory's history ever held a `spec.md`, a spec deleted in one commit — or
in an earlier pull request — and the directory in the next is still a
deletion.

Every record is read as git carries it at `HEAD`, never as the working tree
holds it: a tree that differs from `HEAD` is what CI never sees, and a local
run reading it would be the more permissive of the two. `--worktree` reads the
working tree instead, for the check `round_record.py` runs on a record before
its commit. The flag is local only, and CI keeps the default.

Which declaration applies is settled by the branch it names, looked up from
the checked-out branch. Every way that lookup can fail — a renamed branch, a
detached HEAD, two declarations naming one branch, a file that will not parse
— resolves to *no declaration*, and therefore to **asking**. There is no path
from a missing or ambiguous declaration to silence: a fail-open here would be
a gate that a corrupt file switches off, and a failed read is not a decision
anyone made.

**This is a reversal, and of this document.** The paragraph below the review
arm's table used to say there is deliberately no standing waiver, because
"a gate that can be turned off for a session has nothing left to do but stay
quiet". That was correct while the commit was the only place a check could
live: with one enforcement site, recording the answer necessarily removes the
check.

A waiver removes a check; a routing record moves it. Both answers stay
enforced — the chain at the pull request against the round record, the direct
route by `[no-review]` in every commit command, unchanged. There is no third
value meaning "no enforcement anywhere". What makes the reversal possible is
the second site, which did not exist when that paragraph was written:
`gh pr create` passed no gate at all, so enforcement sat entirely on every
commit and was absent at the moment the work actually left.

What it costs, stated rather than buried:

- A commit on an unreviewed branch is no longer stopped as it is typed.
  Between the declaration and the pull request, nothing local blocks.
- A branch that declares the chain and never opens a pull request is checked
  by nothing. Today the gate would have stopped every commit. The
  destination axis is what turns that from an accident into a state someone
  declared and can be shown.
- A repository that adopts the declaration and not the workflow has traded a
  prompt for a convention, and the plugin cannot detect that state.
- Deleting the routing file restores today's behavior exactly, because the
  fallback for a missing declaration is today's decision table.

Enforced by: tests/test_chain_check_at_the_pull_request.py::test_a_declaration_this_branch_retired_is_not_one_it_made, tests/test_chain_check_at_the_pull_request.py::test_a_declaration_the_rule_arm_retired_is_not_one_it_made

### Parity arm — opt-in: `seal/parity.md` at the repo root

Ported behavior follows the original where policy is silent, so a commit that
changes code should carry a record that the original was consulted. Mark:
`<git-dir>/specseal-parity`, written by the `legacy-parity` skill after an
actual comparison.

| Condition | Decision |
|---|---|
| `[no-parity]` in the command | silent (explicit skip, visible in history). Same placement as `[no-review]` |
| the change confined to `docs/`, `seal/` | silent — nothing there can be compared against an original, and a gate that fires where no comparison was possible teaches people to click through it |
| `specseal-parity` equals current HEAD | satisfied |
| otherwise | contributes an ask |

"The change" there is every path the commit would carry, not the index alone:
`changed_paths()` reads the staged diff, and also what `-a` and a trailing
pathspec pick up, because two of the three forms never touch the index. A
document-root row that said *staged* would describe a narrower silence than
the gate actually keeps, and a reader would expect a prompt where none comes.

The mark says a comparison was recorded, not that it was a good one. Writing
it for work nobody compared converts "nobody checked" into "someone checked
and it was fine" — the one claim the parity methodology exists to keep honest.

`ask` was chosen over `deny` here originally, on these grounds: the gate
cannot know whether the user already accepted the risk, and *a deny with no
override path forces workflow contortions* (measured on the worktree guard's
earlier design). That reasoning stands — it is the override path that changed,
so the premise no longer holds:

| The old worry | What answers it now |
|---|---|
| a deny repeats, and the user cannot get past it | the question fires once per session per repository; every attempt after it is the same `ask` as before |
| the gate cannot know the user already accepted the risk | it no longer has to guess — the deny's reason puts the choice to the user, and their answer comes back as `[no-parity]` (or the comparison itself) |
| nowhere to record the risk being accepted | the marker, and the token in the command, which stays visible in shell history |

What the deny buys is the half the `ask` could never deliver: the reason
string could *name* both ways on, but only the model can put them up as
options, and an `ask` never gives the model the turn.

## review-history-guard (PostToolUse, Bash)

<!-- specs/1788844300-the-guards-cases-cannot-observe-what-they-guard -->
**A session that posts a review is reminded to write the round record, and
one that reads a review is reminded to read the record first.**
Two branches with **opposite conditions** — the failure modes differ:

| Trigger | Condition | Reminder |
|---|---|---|
| review posted (`gh pr review/comment`, `gh api -X POST …/pulls/N/(reviews\|comments)`) | the work item's `rounds/` holds **no** `round-*.md` | write `rounds/round-N.md`, and `tests-todo.md` and `evidence-todo.md` beside `rounds/` rather than inside it, now — the posting session is the only one that still holds its verdicts and probe results |
| review read (`gh pr view --json …comments`, `gh api …/pulls/N/(comments\|reviews)` without POST) | a round record **exists** | read it before acting on inline comments — the todo lists may not be in the comments at all |

Which work item: the one whose `seal/specs/<id>/routing.md` names the checked-out
branch — the same key the commit gate reads. The records used to be keyed by
the pull request number, at `.specseal/handoff/PR-<n>/`, and that directory
was never once created in this repository: the number does not exist while the
rounds that would fill it are running. One key instead of two costs this
reminder the case where `gh pr merge` runs from a branch that declared
nothing. What replaced the deadline is the pull-request check in CI, not this.

Reminder-only (PostToolUse cannot block). Same `seal/` opt-in as the gate.
Enforced by: tests/test_chain_hooks.py::test_history_guard_reminds_posting_without_record, tests/test_chain_hooks.py::test_history_guard_reminds_reading_with_record

## implementer-mark · implementer-notice (PreToolUse Agent|Task · PostToolUse Bash)

<!-- specs/1788310269-the-implementer-leaves-a-mark -->
**A `framer` or `smith` spawn leaves a mark, and a commit on a branch whose
declaration names that agent, with no mark standing, gets one line saying so.**
The routing declaration has two axes that name an agent — `Planning`, who
draws the frame, and `Implementation`, who builds the work item — each
answered by that agent's name or by `the session`, and until these two hooks
existed the answers were written down and read by nothing. Two hooks, sharing
one address module (`hooks/implementer.py`), so the writer and the reader
cannot spell the path two ways — and one module for both axes, because a
second one beside it would differ by a constant:

| | Fires | Does | Prompt budget |
|---|---|---|---|
| `implementer-mark` (`pre-agent`) | an Agent/Task spawn whose `subagent_type` is `framer` or `smith` | writes the checked-out branch name to `<git-dir>/specseal-planner` or `<git-dir>/specseal-implementer`, one per axis. Prints nothing | zero — it cannot deny or ask |
| `implementer-notice` (`post-bash`) | a command that actually invokes `git commit` | where the declaration for this branch names an agent on either axis and no mark of that axis stands for this branch, prints one line naming the file — one line naming both axes where both are unfulfilled, never one line each; silent for an axis whose mark stands, whose row is absent or outside its vocabulary, or which answers `the session` | zero — a reminder, once per session per repository, never a decision |

A mark is keyed on the **branch**, not on HEAD as `specseal-reviewed` is: a
work item commits many times and neither the framer nor the implementer
changes when it does. It is keyed on the **axis** too, because the two marks
share a directory and `smith` is spawned on nearly every work item — one mark
answering for both would go silent in exactly the state the notice reports.
It lives in the git dir and CI never sees it, which is why nothing at the pull
request reads either axis — neither agent produces a committed artifact a
session could not also write. Everything fails toward "no mark", which is toward a
reminder: a mark gate that quietly stops running turns the notice on, not off,
so a dead gate produces a line somebody reads rather than a silence nobody
does. The commit gate's decision is byte-identical with the row and without it.
Enforced by: tests/test_the_implementer_is_recorded.py::test_spawning_smith_leaves_a_mark, tests/test_the_implementer_is_recorded.py::test_a_declared_smith_with_no_mark_is_noticed_after_a_commit
