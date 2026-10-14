# worktree-guard — behavior spec

Authority for `hooks/worktree-guard.py`. A change to the hook that diverges
from this document changes one of them knowingly — update both.

## Premise

Worktrees exist to keep CONCURRENT work from mixing in one folder. Single-
stream work uses plain `git switch` on the shared tree. The guard enforces
both directions of that rule from one signal: how many work streams are
actually live on the tree.

## Decision matrix

### A. Branch switch (`git switch` / branch-form `checkout`)

| Tree state | Decision |
|---|---|
| ACTIVE session present | deny — steer to a worktree; one destination, no choice |
| only IDLE sessions | **choice** — switch here, or split into a worktree; each session listed with its last-activity age. Under the `automation` press, a deny on every attempt (§Choice sites, *Under the press*) |
| detection unusable (can't see even our own process) | **choice** — the same two, and under the press the same deny |
| single stream, tracked changes present | ask — do the uncommitted changes ride along? Under the press, a deny (*The tracked-changes row has two readers too*) |
| single stream, clean | allow silently |

`[shared-tree-ok]` silences the two **choice** rows (§Choice sites); a dirty
tree then reaches the tracked-changes row, whose reason opens with the token's
lead.

**The tracked-changes row has two readers too.** Under the `automation` press
it is a `deny` to the model: nobody can answer, and "commit first" is not a
button. The press is read by the stop's reader at the session's own root.
Without the press it is the `ask`, word for word; `[shared-tree-ok]` reaches
neither.

**The deny states what the guard read and predicts nothing about git**: the
`ask`'s lead, changes and index-residue note, the press sentence, and `git
commit` and `git stash` as `LEAVES_THE_TREE` commands that pass issued alone.
No question tool, no switch option, one text for every switch form; a plain
retry meets the same refusal. The press moves no other verdict.
Enforced by: tests/test_the_guard_asks_once_per_session.py::test_under_the_press_the_dirty_row_is_a_deny_to_the_model, tests/test_the_guard_asks_once_per_session.py::test_the_token_does_not_reach_the_dirty_row_under_the_press_either, tests/test_the_guard_asks_once_per_session.py::test_a_compound_stash_and_switch_meets_the_deny, tests/test_the_guard_asks_once_per_session.py::test_the_plain_retry_meets_todays_rows, tests/test_the_guard_asks_once_per_session.py::test_the_ways_on_pass_the_guard, tests/test_the_guard_asks_once_per_session.py::test_a_creation_on_the_dirty_line_is_stopped_with_it, tests/test_the_guard_asks_once_per_session.py::test_the_press_is_read_from_the_sessions_own_root, tests/test_the_guard_asks_once_per_session.py::test_one_text_for_every_switch_form, tests/test_worktree_guard.py::test_the_dirty_tree_row_names_what_was_measured

**Which commands reach these rows.** The guard does not predict whether a
command switches a branch. It reads each git segment of the frozen reading
(§*Which tree*) as one of three shapes, from its words alone:

- **listed** — a subcommand in `LEAVES_THE_TREE` (the git subcommands this
  repository's recorded runs hold whose plain form leaves HEAD's branch, each
  with its count), or a `checkout` with a path after its `--`. A listed shape
  is silent in every tree state and spawns no git. `worktree` and `stash` are
  listed unless the first word bash hands git after them is `add` or `branch`.
  A `rebase` is listed unless it has two words that are not options, or
  `--root` and one (`git rebase main feature/x`). A lone `-` is a word, and so
  is every word after a `--` or an `--end-of-options`. git takes an
  unambiguous prefix of `--root` (`--ro`) as `--root`, and so does the guard.
- **a switch** — `git switch`, whatever its words. It takes the rows above,
  in the tree its segment names.
- **unrecognised** — every other git: a `checkout` with no path after `--`, a
  subcommand the list lacks, and a git the frozen reading does not read as one
  — in a string handed to a shell (`sh -c`, `eval`, `env -S`), in a `$( … )`,
  backtick or `<( … )` body not all listed, behind a redirection or a zsh
  precommand word, or in a command that would not split.

**An unrecognised shape stops only where the tree matters**: another session
ACTIVE or IDLE in its segment's tree, detection unusable, or tracked changes.
In a clean tree nobody else is in, row 5 says nothing of a switch, and nothing
is said of a shape that might be one. The reason quotes each shape with its
plain spelling (`git switch <branch>`, `git switch --detach <rev>`, `git
restore <path>`, the git alone, `git -C <dir>`, `git commit -F <file>`).

**The stop has two readers.** Under the press it is a `deny` to the model,
which rewrites in the plain spelling and meets the rows above on the retry, and
no person is asked. In a dirty, IDLE or unusable tree that retry meets the
press's deny. Otherwise it is an `ask`, except where another session is
ACTIVE: row 1 denies a branch-form `checkout` with nobody asked, so the stop is
a `deny` whoever is at the keyboard.

**Approving the `ask` would run every segment.** A creation on the same line is
judged first. A `git switch` on the same line makes the stop a `deny` whoever is
at the keyboard. The consent record is never read for the stop.

**Each shape is judged in the tree its segment names**, first one first and
each tree once, an `&`-cut or redirected git by its own `-C`. Every tree on the line is read before the stop
is taken: one ACTIVE tree makes it a `deny` describing the ACTIVE trees alone,
and otherwise the reason names each tree that matters and why. A reason that
describes one tree calls it "this tree", whichever tree it is.

**The failure direction.** Every unrecognised shape stops where the tree
matters; a creation only a hidden spelling holds, in a clean tree nobody else
is in, goes unjudged (§*Known limits*; work item 1791270162,
`phases/phase-3.md`).
Enforced by: tests/test_worktree_guard.py::test_a_listed_shape_is_silent_in_every_tree_and_spawns_nothing, tests/test_worktree_guard.py::test_an_unrecognised_shape_stops_where_the_tree_matters, tests/test_worktree_guard.py::test_the_same_shapes_are_silent_in_a_clean_single_stream_tree, tests/test_the_guard_asks_once_per_session.py::test_under_the_press_the_stop_is_a_deny_to_the_model, tests/test_the_guard_asks_once_per_session.py::test_the_consent_record_is_not_the_press, tests/test_guard_resolves_the_tree_it_judges.py::test_no_redirection_makes_a_moving_verb_listed_wherever_it_stands, tests/test_guard_resolves_the_tree_it_judges.py::test_a_shape_in_a_clean_tree_takes_no_stop_from_one_in_a_dirty_tree, tests/test_worktree_guard.py::test_no_approval_runs_a_line_past_an_active_tree, tests/test_worktree_guard.py::test_a_rebase_naming_a_branch_is_unrecognised, tests/test_worktree_guard.py::test_no_listed_form_moves_head_under_git, tests/test_worktree_guard.py::test_the_stop_names_each_tree_that_matters_in_both_languages, tests/test_worktree_guard.py::test_a_cut_group_is_judged_in_the_tree_its_own_c_names

### B. Worktree creation (`git worktree add`, or Agent/Task `isolation: "worktree"`)

| Tree state | Decision |
|---|---|
| **consent: this session already created a worktree in this clone, or its person pressed `automation` on the routing question** | **allow** where the call is worktree creation and nothing else · **silent** where it does more, and on the Agent/Task path. Read before every row below — §Creation consent |
| ACTIVE session present | ask — separation justified, creation still needs a human |
| only IDLE sessions | **choice** — create it, or switch in the shared tree. Under the press, reached only in a clone without the press or this session's record: a deny on every attempt, naming no way on |
| detection unusable | **choice** — the same two, and under the press the same deny |
| `[worktree-ok]` given (Bash only) | ask — the token is a confirmation coming back; declining withdraws it |
| single stream, **Bash** | deny — steer to `git switch`; `[worktree-ok]` in a retry reaches the row above |
| **Agent/Task**, no consent, any tree state | ask — concurrent by construction; declining cancels the spawn |

The Bash rows are decided before the command runs (*Decided before git runs*).

#### Why the Agent path counts nothing, asks once, and reads no token

**An isolated agent is concurrent work by construction, so the Agent path does
not count sessions**: its tool calls renew the parent's lease with no id of
their own, so a count would steer it into the parent's tree.

**With consent the path is silent, never an allow; without it, it asks, once
per session**: consent answers the creation half, not the agent.

**It reads no token, because it has no command line**: a prompt the model
writes that documents `[worktree-ok]` would switch the guard off, so the
verdict does not depend on the prompt.
Enforced by: tests/test_worktree_guard.py::test_an_isolated_agent_asks_without_counting_sessions, tests/test_worktree_guard.py::test_the_agent_verdict_does_not_depend_on_the_prompt

## Creation consent — the first creation is the question, not every one

<!-- specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session -->
**The first worktree creation in a session is the question, and a later one in
the same session is allowed — and where the person pressed `automation`, not
even the first is asked.**
A question per creation stops an unattended run at its first worktree, which
`CONTRIBUTING.md`'s prompt-budget rule has no room for. `[worktree-ok]` is not
consent: whoever issues the command writes it (`has_token`).

**The consent record is written after the answer**, by
`hooks/worktree_consent.py` on `PostToolUse` for a `git worktree add` the
harness permitted and ran, so no command text forges it.

**The routing answer is the second consent, and it covers the creation the
record cannot: the first.** The harness writes the `AskUserQuestion` result
from the person's click; the model writes the question, never the press.
Neither consent is forged by habit, only by editing a file on purpose.

**A `routing.md` is not read, not even as a fallback**: a file the model writes
is `[worktree-ok]`'s standing under another name.

**What exactly is read**; every way of failing it is *no consent*:

1. **This session's own main transcript** — `transcript_path` named
   `<session-id>.jsonl`, else `~/.claude/projects/*/<session-id>.jsonl`; a
   subagent reaches its parent's by id. No other session's, no `subagents/`.
2. **A harness-written `AskUserQuestion` result**: a `user` entry whose
   `tool_result` names an earlier `AskUserQuestion` by `tool_use_id`, read from
   `toolUseResult.answers`, `isSidechain` exactly `false`. A Bash echo of *The
   user answered: "automation"* has no such link.
3. **The routing question**: the single-select question whose options' leading
   phrases are exactly `automation`, `per axis` and `no work item`
   (`skills/implement/orchestration.md` §*Question 1 — single-select*), answered
   with the label `automation` verbatim, so a typed `Other` is not consent. A
   `multiSelect` question is skipped, so the boxes neither give nor take back
   the press. A leading phrase is the label casefolded
   and cut at the first ` (`, ` —` or ` -` (`automation (Recommended)`).
4. **The same clone**: the result entry's own `cwd` resolves to the same common
   git directory as the creation's repository.
5. **The last answer stands**: a later `per axis` or `no work item` from that
   clone takes the press back, for this guard and the commit gate, and a later
   press gives it back. **A record already written stands**: it is read first.

**A `per axis` answer is not read, even with its first box ticked**, because box
labels get reworded. A read that raises is no consent (`hooks/dispatch.py`
skips a raising gate). The record is read first, the transcript only without
one.

**The record is an empty file at
`<git-common-dir>/specseal-worktree-consent/<session-id>`**:

- **Not the choice marker**, which means *the question was put* and fails the
  other way (unwritable is **already asked**; an unwritable record, **no
  consent**).
- **In the common git directory**: a linked worktree is the same clone.
- **The clone the guard judged.** The writer places a creation by the guard's
  own placement, `hooks/worktree_consent.py#place`, through the same
  tokenizing adapter.
- **No expiry**; **a failed `git worktree add` records too**, since the
  approval happened; **an unwritable record leaves none**, silently.

**Why the allow is bounded.** `permissionDecision: "allow"` bypasses the user's
permission settings for the **whole** tool call, so the guard allows only a
command that is worktree creation and nothing else, and is **silent** for
anything more or anything the lexer gave up on.

**A segment is worktree creation only when its command word is exactly the word
`git` and no token carries `$`, a backtick, `<` or `>`.** A basename is not an
identity: `./git` would let one approved creation run any executable past
`permissions.deny`. The class is every quoting the lexer hands back as `git`
(`'git'`, `g'i't`). A glob, a `~` argument and a trailing `&` are left alone.

**Outside that class nothing reaches `allow`, and with consent the guard is
silent**: a path, a wrapper or assignment (`sudo git`, `VAR=1 git`), `$GIT`,
another case, a trailing slash. Without consent, what `cmdline.parse_git` reads
as git (a path, an assignment, a wrapper, a `cmdline.RUNNERS` program such as
`nice`) meets the ladder, and a last path component that is not `git` as
written, or `uv run`, is not git and passes silent.
`test_the_command_word_class_is_what_the_allow_covers` pins each group.

**A creation behind a redirection, a zsh precommand word or a spaced
`--config-env` is an unrecognised shape** (§A, §*Which tree*), under consent
too.

**The creation ladder is reached whatever segment comes first**, because the
writer records a creation anywhere in a command that ran.

**So the creation is judged between the ladder's two halves, whichever of the
two is written first**, and the switch ladder keeps every verdict.

| Switch-ladder row | Order | Why |
|---|---|---|
| ACTIVE session | above the creation | the one unconditional deny; it stops the whole command |
| only IDLE · detection unusable | **both**, and the branch decides | the [choice](#choice-sites) deny stops the whole line; its `ask` would run every segment, so it yields to the creation through `choose`'s `before_ask` |
| **the creation** | | |
| tracked changes present | below | it protects no tree, and approving it would create the worktree unquestioned |
| single stream, clean | below | says nothing |

**The walk keeps the first switch and the first creation, in either order**,
with the same decision and reason, never weaker than either alone; the early
exit at `if not top` falls through too.

**For a session with no consent, the guard denies or asks about the creation
wherever the writer would record.**

**What does not change.** Without the record or the routing answer the guard
asks at every site. The switch direction reads neither.

**The prompt budget.** Zero under the press in the clone it was given in
(another clone: §Choice sites, *Under the press*); one per session otherwise.
With consent a compound, an expansion, a redirection, a wrapper or a
**path-qualified command word** gets silence, not an allow.
Enforced by: tests/test_the_guard_asks_once_per_session.py::test_the_first_creation_is_still_a_question, tests/test_the_guard_asks_once_per_session.py::test_a_second_creation_in_the_same_session_is_allowed, tests/test_the_guard_asks_once_per_session.py::test_the_measured_automation_run_is_not_stopped, tests/test_the_guard_asks_once_per_session.py::test_a_result_not_linked_to_an_ask_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_automation_on_another_question_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_an_answer_given_in_another_clone_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_the_labels_match_the_routing_question_the_orchestrator_asks, tests/test_the_guard_asks_once_per_session.py::test_a_typed_answer_that_qualifies_the_preset_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_question_1_alone_and_the_boxes_beside_it_read_the_same_press, tests/test_the_guard_asks_once_per_session.py::test_the_boxes_asked_alone_neither_give_nor_take_back_the_press, tests/test_the_guard_asks_once_per_session.py::test_a_shape_the_reader_did_not_expect_keeps_the_guards_deny, tests/test_the_guard_asks_once_per_session.py::test_a_switch_written_after_a_creation_is_judged, tests/test_the_guard_asks_once_per_session.py::test_the_order_of_a_switch_and_a_creation_does_not_decide, tests/test_the_guard_asks_once_per_session.py::test_a_command_with_both_is_never_weaker_than_either_alone, tests/test_the_guard_asks_once_per_session.py::test_the_command_word_class_is_what_the_allow_covers, tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records, tests/test_guard_resolves_the_tree_it_judges.py::test_the_consent_writer_files_a_creation_where_bash_runs_it, tests/test_guard_resolves_the_tree_it_judges.py::test_the_writer_files_under_the_clone_the_guard_judged, tests/test_guard_resolves_the_tree_it_judges.py::test_the_consent_writer_composes_the_creations_own_dash_c

### Decided before git runs (#692)

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**A worktree creation is decided before git runs, in every clone, one
carrying this plugin's git hooks included.**
A hook after git cannot undo all of a creation: `-B <existing>` resets the
branch first, `--no-checkout` and `--orphan` run no `post-checkout`, a
`--lock`ed tree survives one `remove --force`. So §B decides through the
frozen reading (§*Which tree*), a refused creation buys no consent, and this
plugin installs no `post-checkout`.
Enforced by: tests/test_a_creation_is_judged_before_git_runs.py::test_a_refused_dash_capital_b_leaves_the_branch_where_it_was, tests/test_a_creation_is_judged_before_git_runs.py::test_a_creation_git_runs_no_undo_for_is_refused_before_it, tests/test_a_creation_is_judged_before_git_runs.py::test_a_bash_creation_under_the_harness_path_buys_no_consent, tests/test_a_creation_is_judged_before_git_runs.py::test_no_git_hook_judges_a_creation, tests/test_the_hook_surface_git_offers.py::test_what_a_take_back_cannot_undo

<!-- specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text -->
**A creation the guard lets through is recorded from the command that ran.**
The `PostToolUse` writer files the record in every clone, and `[worktree-ok]`
is read by the guard itself, never carried to a git hook.
Enforced by: tests/test_a_creation_is_judged_before_git_runs.py::test_an_answered_creation_runs_and_the_record_follows_it, tests/test_a_creation_is_judged_before_git_runs.py::test_the_old_token_puts_the_creation_to_the_person_before_it_runs

## Choice sites

**A site where declining leaves more than one command this session could
issue denies, with a reason instructing an AskUserQuestion naming both**: an
approve/decline prompt shows the user neither destination. Elsewhere options
would be invented. The reason tells a choice deny from the ACTIVE-session one.

**Only the deny branch protects anything.** The deny stops the WHOLE command;
the fallback `ask` runs every segment when approved. So `choose` takes a
`before_ask`, a judgment run on the `ask` branch alone, which is how the
switch's choice rows decide nothing about a creation on the same line.

**Once per session per direction**, not per site, at
`<git-dir>/specseal-worktree-choice/{create,switch}/<session-id>`, the id cut
to its basename: one budget would let a creation spend a switch's answer. The
marker, written by `PreToolUse`, means *the question was put*, never consent.

**An unwritable marker counts as already asked**, since a missed question beats
an endless deny; a later attempt, or one with no session id, gets the `ask`.

**Under the press all four choice sites deny on every attempt; the switch's
two name the split into a worktree as the way on where its creation is
consented, and the creation's two name none.** Consent is the press in its own
clone or this session's record (§Creation consent), and the reason names which
and the split: `git worktree add <wt_root>/<branch> <branch>` or `git worktree
add <wt_root>/<name> -b <branch> origin/main`, then `git -C` on it.

**Under the press no choice reason names a question tool, `[worktree-ok]` or
`[shared-tree-ok]`**; each says a plain retry meets the same refusal, and the
creation's says the press consents only in its own clone. The press is read at
the session's root only where a choice row fires, at most once per switch and
twice per creation, and no marker is written. The tokens and the attended text
are unchanged.
Enforced by: tests/test_a_creation_in_another_clone_asks_nobody.py::test_under_the_press_a_creation_row_denies_every_attempt, tests/test_a_creation_in_another_clone_asks_nobody.py::test_an_unbalanced_quote_under_the_press_names_no_token, tests/test_a_creation_in_another_clone_asks_nobody.py::test_attended_an_unbalanced_quote_keeps_the_quote_note, tests/test_a_creation_in_another_clone_asks_nobody.py::test_a_record_in_the_other_clone_outranks_the_rows, tests/test_a_creation_in_another_clone_asks_nobody.py::test_the_token_still_reaches_its_own_row, tests/test_a_creation_in_another_clone_asks_nobody.py::test_the_press_is_read_from_the_sessions_own_root, tests/test_a_creation_in_another_clone_asks_nobody.py::test_a_creation_behind_a_cd_meets_the_same_deny, tests/test_a_creation_in_another_clone_asks_nobody.py::test_the_transcript_is_read_at_most_twice_per_creation, tests/test_worktree_guard.py::test_the_attended_creation_choice_rows_are_the_bases, tests/test_the_idle_session_rows_ask_nobody.py::test_under_the_press_a_choice_row_denies_every_attempt, tests/test_the_idle_session_rows_ask_nobody.py::test_the_token_still_reads_as_it_does_attended, tests/test_the_idle_session_rows_ask_nobody.py::test_the_way_on_passes_the_guard, tests/test_the_idle_session_rows_ask_nobody.py::test_a_creation_on_the_same_line_is_stopped_with_it, tests/test_the_idle_session_rows_ask_nobody.py::test_the_plain_retry_after_the_stop_meets_the_deny, tests/test_the_idle_session_rows_ask_nobody.py::test_the_press_is_read_at_most_once_per_command, tests/test_the_idle_session_rows_ask_nobody.py::test_the_press_is_read_from_the_sessions_own_root, tests/test_the_idle_session_rows_ask_nobody.py::test_a_switch_into_another_clone_names_no_split_it_cannot_consent, tests/test_the_idle_session_rows_ask_nobody.py::test_a_clone_this_session_already_split_is_named_the_split, tests/test_worktree_guard.py::test_the_attended_choice_rows_are_the_bases_in_korean

**Retry tokens are matched as bare words of the command, never substrings**,
the whole command tokenized first. A quoted sentence never matches; unquoted
prose is a residual (`echo the [shared-tree-ok] token is documented`).

**Where the token is read from.** The command, and only the command. Not
from a here-document body, since #780: a token counts only where the command
as written and the command with its here-document bodies taken out both carry
it (`hooks/tokens.py#without_bodies`), also where `hooks/cmdline.py` cannot
load. The Agent/Task path reads no token (§B).

| Token | Answer it carries | Effect |
|---|---|---|
| `[worktree-ok]` | create the worktree | the site asks — creation always takes a confirmation, so this direction's floor is `ask` |
| `[shared-tree-ok]` | switch in the shared tree | the two switch **choice** rows go silent — the guard's own verdict there is *cannot tell* |

**The token check runs right after the ACTIVE-session row**, and each choice
hands back the other direction's token (`git worktree add … # [worktree-ok]`,
`git switch … # [shared-tree-ok]`), so an answer is not asked again.

**`[shared-tree-ok]` reaches neither the ACTIVE-session row nor the dirty
row**: it is not another session's consent, and the dirty row asks otherwise.

**A token is an audit trail, not an authorization**: nothing verifies who typed
it, the standing `[no-review]` has.

Never guarded: file restores, non-`add` worktree subcommands, and sessions in
linked worktrees (already isolated).

## Declared work streams — leases beat every heuristic

The signals below INFER liveness and miss a session hosted outside a terminal
or working from another cwd, so every repo-touching tool call DECLARES: the
`session-lease` hook stamps `<git-dir>/specseal-leases/<session-id>` for the
repo touched (an edit's file, Bash's cwd). A lease fresher than the idle
threshold is an active work stream; leases older than a day are pruned, and a
failure is silent.

## Activity: what makes a session ACTIVE (heuristics, for sessions without a lease)

<!-- specs/1788846800-an-exited-session-reads-as-live-for-five-minutes -->
**Active = ANY signal within `WORKTREE_GUARD_IDLE_MIN` minutes (default 5):**

| Signal | Detects | Grounds |
|---|---|---|
| tty atime (keystrokes) | human at the keyboard | forgotten tabs are hours stale |
| tty mtime (screen writes) | session streaming its progress | an idle prompt does not repaint |
| transcript last ACTIVE event | autonomous turns and **background agents** (`~/.claude/projects/<slug>/<session-id>/subagents/*.jsonl`) | written long after the last keystroke |

Five minutes is safe only because of the second and third signals: input alone
cannot tell "forgotten" from "autonomous turn in progress".
Enforced by: tests/test_worktree_guard_signals.py::test_fresh_active_event_counts, tests/test_worktree_guard_signals.py::test_transcript_scan_reaches_background_agents

### Passive-event filtering

A fresh transcript mtime is confirmed against the last 64KB, because idle
sessions receive passive `attachment` appends: only `user` / `assistant` /
`tool_use` / `tool_result` / `progress` events count, by their own timestamps.
A stale mtime is trusted as-is.

### What a blocking prompt must show (identification)

Every listed session shows:

- **host app**, by the ANCESTOR process chain, never siblings;
- **disaggregated signals** — terminal input/output age and transcript
  active-event age apart; an unidentified session prints its one signal's kind
  and age (*lease declaration 4.7h ago*) and nothing after;
- the project's newest OTHER transcript's **last user message snippet**.

### Unknowns resolve conservatively

**No readable tty AND no readable transcript → active.** Detection that cannot
find our own process → `reliable=False` → the **choice** rows, whose second
attempt is the `ask`: a deny on EVERY switch would be an outage on hosts the
heuristics never satisfy, not the cost of a wrong deny (a prompt) against a
wrong allow (another session's tree). Under the press those rows deny every
attempt; the way on, a worktree per branch made with `-b`, needs no switch and
no person, which keeps it a cost.

### Which tree, when the command walks to it

**The tree judged is the one the command acts on, by every row of §A, the
tracked-changes row included**: its `git -C <path>`, or where an earlier `cd`
moved the shell.

**The whole command is read the way the release base `86256492` read it**:
which segments are git, each one's `-C`, where every `cd` lands. Nothing is
read past the frozen base's words: a shape is its subcommand and, for
`checkout`, `worktree` and `stash`, one deciding word; no name is looked up.
The guard and the consent writer read through `hooks/cmdline_base.py`, that
commit's `hooks/cmdline.py` byte for byte, and choose no segment, slot or
directory through `hooks/cmdline.py`: the guard takes one answer, which a
wider reading could make a failed `cd`.

**The guard asks `hooks/cmdline.py` only what the frozen reading does not read
as git** — a shell's string, an `eval`, a substitution body, a git behind a
redirection or a zsh word, a group an `&` cut apart — and each answer is an
unrecognised shape, its `-C` composed onto the segment's frozen directory. The
consent read also has it take here-document bodies out.

**The cost is what the frozen reading does not read**: a `cd` with a
redirection among its words (`cd W 2>/dev/null`, `2>&1 cd W`) moves neither the
judged tree nor the consent clone, and a git behind a redirection or zsh's
`noglob`, `nocorrect`, `repeat N`, `for i (…)`, `foreach i (…)` is filed by no
writer and read as an unrecognised shape.

**§A asks one question of every git: is this command known to leave the branch
where it is?** Rules answering *does this command switch a branch?* do not
converge.

**A broken reader costs a stop where the tree matters, never a silence.** If
`hooks/cmdline.py` fails to load or raises, the bare word `git` in a string, a
body, a hidden position, an unsplittable command or either side of an `&` the
splitter cut is the finding.
Enforced by: tests/test_worktree_guard.py::test_a_broken_wider_reader_costs_a_stop_never_a_silence, tests/test_worktree_guard.py::test_a_broken_reader_leaves_no_cut_group_silent, tests/test_worktree_guard.py::test_a_broken_reader_judges_a_cut_in_the_tree_before_it, tests/test_guard_resolves_the_tree_it_judges.py::test_a_git_only_the_wider_reading_finds_stops_where_its_tree_matters, tests/test_guard_resolves_the_tree_it_judges.py::test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer

**The command's text is read on every git, permanently** (#692): no git refuses
a switch before its tree moves, and no hook undoes a creation (*Decided before
git runs*). `tests/test_the_frozen_reading_never_grows.py` pins
`hooks/cmdline_base.py` below its rider to `86256492:hooks/cmdline.py`, and
`tests/test_guard_resolves_the_tree_it_judges.py` holds the base's answers.

**The advice follows the same tree**: a command a reason gives carries `git -C
<root>` where the shell is elsewhere, and the note's root-relative `git
restore` always.

**Two destinations fall back to the session's own directory**: one that cannot
be computed (a variable, a glob, a subshell, a bare `cd -`), and one that holds
**no repository**, since `cd /no/such/dir ; git switch x` switches where the
shell started. A `git -C` naming no repository is silent: git refuses it. The
commit gate stops there instead: an unjudged commit is unreviewed.

## Known limits

**A word the shell builds before git runs — a brace expansion, a substitution
that spells `git`, a here-string or heredoc handed to a shell, a git spelled
past the splitter (`g""it` in a line it cannot close) — is not read**, so `git
rebase {main,feature/x}`, `git rebase --ro{,} feature/x`, `git stash {branch,}
y` and `git worktree {add,} ../wt f` are listed and silent in every tree, and
the class is decided in #886. A reader imitating bash misses the next spelling.
`test_a_shell_built_word_is_the_named_limit` and the braced half of
`test_no_listed_form_moves_head_under_git` (`tests/test_worktree_guard.py`) pin
it.

**A switch into a worktree the same command creates is judged in the session's
own tree** (`git worktree add ../x -b x && cd ../x && git switch y`): `../x`
does not exist yet. `git -C ../x switch y` avoids the stop.

**A switch whose tree the guard cannot place is judged in the session's own
tree**, silent where that is clean and single-stream: `builtin cd w`, `command
cd w`, `time cd w`, `pushd w`, `noglob cd w`, an unset `cd "$W"`, `2>&1 cd w`,
each before `&& git switch …`. Asking would stop recorded commands (work item
1790993140, `phases/phase-3.md`). `git -C <dir>` or a plain `cd <dir>` is read.

**Two more spellings reach that fallback.** One is `cd w 2>&1` before the
switch: the frozen splitter cuts it at its `&`. The other is a cut git inside an
`if` body after `cd w`. `test_a_switch_tree_the_guard_cannot_place_is_judged_as_its_own`
(`tests/test_guard_resolves_the_tree_it_judges.py`) pins both.

**`LEAVES_THE_TREE` holds only subcommands this repository's recorded runs
hold.** A git subcommand this repository never ran stops where the tree matters
until a release adds it, and under the press it cannot be rewritten, so the
reason names the list. `test_no_listed_form_moves_head_under_git` runs one
form per row against git.

**A creation only a hidden spelling holds** (`git 2>&1 worktree add …`) **is
unrecognised**: silent in a clean tree nobody else is in, unread by §B, filed
by no writer.

**A `rebase` is listed, and detaches HEAD while it runs**; the guard reads no
window. Its words are read without an option table, so `git rebase --onto main
x` stops too.

**A body or an unsplittable command is judged in the session's own tree**:
`cd W && F=$(git checkout x)` with only `W` dirty says nothing.

**A string handed to a shell (`sh -c`, `bash -c`, `eval`) is judged in the
tree its segment names**, its own `-C` and `cd` unread: `sh -c 'git -C W switch
x'` with only `W` dirty says nothing.

**With the wider reader broken, a git an `&` cut split is judged in the tree
the part before the cut names**, so `2>&1 git -C W switch x` is judged where it
was typed; loaded, in `W`.

**The frozen splitter has taken the quotes off before a word is read**, so a
quoted `>` is a redirection, `git status>/dev/null` reads its redirection as
the subcommand, and `git --config-env k=v switch x` reads `k=v`. Each stops,
naming the wrong word; none goes silent.

**On Windows the count of other sessions is always unusable** (Git for
Windows' `ps` takes no `-o`), so every state is *detection unusable*, a second
Bash creation meets the confirmation, and every unrecognised shape stops there,
in every tree. Under the press every switch without `[shared-tree-ok]` is row
2's deny, and a Bash creation in a clone without the press or a record is §B's
detection-unusable deny; Windows-only cases in
`tests/test_the_idle_session_rows_ask_nobody.py` and
`tests/test_a_creation_in_another_clone_asks_nobody.py` hold the two.

**The `automation` press is this session's, on this machine** (§*Creation
consent*, rule 1). A new session has no press until question 1 is put again
(`skills/implement/orchestration.md` §*Orchestrator: how the work is routed*),
and `routing.md`, which the model writes, is not read; `claude --resume` and
compaction keep the press.

**Under the press a model that does not take the split loops on §A's choice
rows' deny**, bounded by the reason's text (work item 1791781864,
`questions.md` M1).

**Transcript activity is per-project, not per-pid**: one working session marks
every session of the project active.

**tty atime also refreshes on in-turn stdin reads**, so the prompt says
"terminal input/output"; either way it is live.
