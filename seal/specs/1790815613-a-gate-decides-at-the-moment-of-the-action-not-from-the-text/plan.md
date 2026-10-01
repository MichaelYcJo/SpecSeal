# Implementation Plan: a gate decides at the moment of the action, not from the text (#692)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-01 by the repository owner, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. -->

## Summary

The commit gate, the worktree guard's two arms and the consent writer stop
reading a Bash command's text to predict where it acts, and decide inside
git instead: `pre-commit` judges a commit in the worktree it lands in (with a
`reference-transaction` backstop for `--no-verify`), `post-checkout` records
a creation in the clone it ran in, and the switch and creation refusals move
to `reference-transaction prepared` where phase 1 shows git refuses there
cleanly, or to a `post-checkout` undo where it does not. The hooks are stubs
an installer writes into each opted-in clone's hooks directory at session
start and at the first Bash call in a repository. Session identity comes from
the environment the harness exports to every Bash child
(`CLAUDE_CODE_SESSION_ID`, measured) with the lease's pid as the second
route; the automation press and the routing declaration are read the way
they are read today, by session id and by the real branch. The text readers
(`hooks/cmdline.py`'s walk, the gate's PreToolUse path, the guard's Bash walk,
`creation_directory`) are deleted; what stays a text read is a bare-word
token translator whose misread can only cost a refusal. Below the git floor
and in a clone whose hooks slot is foreign, the frozen 0.16.0 reading stays,
byte-identical and pinned, and never gains a rule.

## Technical context

Existing code this builds on, all `read` at `cd24f516`:

- `hooks/commit-review-gate.py#judge` (the two arms, the declaration through
  `routing.declared(cwd, top)`, the marks through `read_mark`), `#automation_pressed`,
  `#AUTOMATION_WAYS`, `#automation_reason`, `#question_reason`, `#ask_reason`,
  `#waiver_form`, `#commit_shape`, `#changed_paths`, `#touches_code`,
  `#DOC_ROOTS`. These move into `hooks/gate.py` with their substance intact;
  what goes is everything that reads a command — `commit_invocations`,
  `commit_targets`, `is_git_commit`, `names_a_directory`, `unreadable_reason`,
  `UNREADABLE_STATE`, `UNREADABLE_CONSTRUCT`, `already_asked`,
  `CHOICE_DIR` — because in a hook there is one target, git's, and no `ask`.
  Inside `pre-commit` the index git will commit is the one `GIT_INDEX_FILE`
  names, for `-a` and a pathspec too, so `changed_paths` collapses to one
  `git diff --cached --name-only` (M2 confirms the three forms).
- `hooks/worktree-guard.py#sessions_in_tree`, `#fresh_leases`,
  `#dead_session_ids`, `#tracked_changes`, `#phantom_entries`,
  `#fmt_sessions`, `#fmt_snippet`, `#steer_to_switch`, `#steer_to_shared`,
  `#git_at`, `#guard_worktree_creation`'s ladder texts, `#ancestors`,
  `#proc_cwd`. The counting and the texts are reused with one input changed:
  the tree is the hook's own working directory. What goes is
  `walk_command`, `split_command`, `judgeable`, `segment_cwd`, `classify`,
  `only_creates_a_worktree`, `ELSEWHERE`, `judge_creation`, `choose`'s
  `before_ask`, `already_asked` and `main`'s Bash walk; the Agent/Task arm of
  `main` stays.
- `hooks/worktree_consent.py#automation_answered`, `#transcript_for`,
  `#consent`, `#granted`, `#record`, `#consent_path` reused by the hooks;
  `#creation_directory` goes; `#main`'s Agent arm stays or goes with M5.
- `hooks/session-lease.py#owner_pid` and its record `{"ts","host","pid"}`
  under `<git-dir>/specseal-leases/<session>` — the second route to a
  session id (executed: this subagent's `CLAUDE_PID` equals that `pid`).
- `hooks/optin.py#home_at`, `#git_common_dir`, `#repo_root`, `SCRATCH`;
  `hooks/routing.py#declared`, `#current_branch`; `hooks/dispatch.py#GROUPS`
  and its failure channel (`record`, `draw`) for the installer's say-once
  message; `hooks/implementer-notice.py` (moves to `post-commit`).
- `hooks/cmdline_base.py` — `86256492`'s reader, kept only where P4 keeps
  it; `tests/test_what_the_reader_understands.py#test_the_guard_reads_the_same_answer`
  is the pin to retarget to bytes.
- Real-git test precedents: `tests/test_the_waiver_can_be_typed.py` (git
  init in `tmp_path`, every shell present), `tests/test_the_reader_agrees_with_bash.py`
  (one bash process as the oracle, guarded by `conftest.usable_bash`),
  `tests/test_a_gate_that_fails_says_so.py` (the dispatcher's groups).
- Constraints: hooks run from the installed cache, so a stub embeds the
  installed version's path (spec §*What the tree answered*, 9); Python 3.9
  on stock macOS (`dispatch.py`'s own note), `python3 || py -3` as
  `hooks.json` spawns; `CLAUDE_PLUGIN_ROOT` is absent from a Bash child's
  environment (executed).

**Failure scenario of the chosen approach — what breaks in six months.**
A git release changes a hook's contract or the symref support (phase 1's
table is version-keyed and CI runs the floor and the newest). The harness
renames the session variable (the lease route stands; S9 is the test that
removes the variable). A project adopts husky or pre-commit after the stubs
are in (the installer finds a foreign slot at the next session start, says
so, falls back — P1). Somebody adds one rule to the frozen fallback (S11
compares bytes against `git show 86256492:hooks/cmdline.py`). A clone no
session ever entered carries no hook (stated as a known limit; M8 counts
it).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. git-native, pure** | below the git floor a switch and a creation have no "before" to refuse at (M1, M3); a clone whose hooks slot is foreign (P1) or that no session entered (M8) carries no hook; a harness that exports no session variable (S9) | chosen for every action git can decide; the rest is C′ |
| **A′. A plus an advisory PreToolUse fast path** (the ticket's own wording for A) | the text reader lives on to produce the advisory; the model gets two messages for one commit and reads the advisory's misreading as a fact; `hooks/cmdline.py` cannot be deleted | rejected — spec §*What the tree answered*, 8 |
| **B. static, fail-closed** | every segment `understood` refuses and every unresolved `cd` becomes a stop for every consumer: the guard gains 36–78 asks per 4,380 commands (`seal/specs/1790745049-…/rounds/round-1-report.md`), the recorded run keeps all 14 commit-gate stops (each a correct reading of text), and the next shell construct is a new stop with no bound on "not understood" | rejected — it converges onto the person's keyboard, which is the cost `CLAUDE.md`'s first goal weighs against |
| **C. hybrid as the ticket writes it** — A where git decides, B for what never reaches git | "two mechanisms to keep in step", the failure the ticket names; a B that grows is milestone 49 again | rejected in that form |
| **C′. A everywhere git decides; the frozen 0.16.0 reading, never edited, where git cannot** — below the floor (P4) and in a foreign-slot clone (P1) | one rule added to the fallback (S11 pins its bytes, so the rule has to delete a test first); the fallback's own silences — #686's spellings — stay below the floor, and the policy states that as the floor's cost | **chosen** |
| **U. undo after the fact** for every switch and creation (`post-checkout` reverts what the ladder would have refused) | a dirty tree carried twice; another session's tree moved for a window of seconds; a reverted `-b` creation leaves its branch; reversible, but not prevention | kept as the switch arm's own answer only where M1 shows refusing at `prepared` is unclean; rejected as the general design |
| **R. `reference-transaction` alone for the commit gate** (no `pre-commit`) | fires at `prepared`, `committed` and `aborted` for every ref update — fetch, push, tag — so three interpreter starts per update (M10); refusing at `prepared` leaves an orphaned commit object and git's own lock error in front of the gate's text; the parity arm's diff has to be rebuilt from the ref rather than read from the index | rejected as the primary; kept as the `--no-verify` backstop (M2) |
| **W. the waiver as a commit-message trailer read by `commit-msg`** | a waiver inside the message is the prose-versus-consent confusion `has_marker` exists to avoid, and it lands in history as part of the commit's text | rejected; `git -c specseal.waive=<arm>` (M11) is read from the command and visible in shell history, as `: '[no-review]';` was meant to be |
| **P. one more rule for the text reading** | the stopped class: #674's three rounds, Q7's cap, #689's round 1, and the abandoned `fix/689-past-the-cap-…` plan's four ordering rows; more than 24 hours and no criterion for done | refused — the owner's decision of 2026-09-30, `routing.md` §*Why this way* |
| **T. a global `init.templateDir` or user-level `core.hooksPath`** so every clone carries the stubs | writes a person's git configuration outside any repository, and chains with their own hooks on every repository on the machine | out of scope; reopened only with M8's number |

**The chosen approach, and the paragraph a reviewer can attack.** Every
decision runs inside the git process performing the action, in the worktree
git resolved and on the branch `HEAD` names there, and the model's command
text is an input to none of them; so there is no shell construct, present or
future, that can route a commit, a switch or a creation around the decision,
because a command that performs the action reaches git and one that does
not needs no decision. What can step around a git hook is git's own list —
`--no-verify`, which skips `pre-commit` and `commit-msg` and nothing else, so
`reference-transaction` backstops it; a re-pointed `core.hooksPath` or a
removed stub, which the installer re-checks at every session start and
every Bash call in the repository and says once rather than falls silent on;
and a git version lacking the hook, which is a floor a version-keyed test
pins — and that list is finite, documented, and changes only with a git
release. The one text read that stays is of consent tokens, and a token
misread costs one refusal naming the git-native spelling, never a silent
pass. Where this argument does not reach — below the floor, in a foreign
slot — the design does not reason about shell at all: it keeps `86256492`'s
reader byte for byte, which has one known behaviour and gains no rule.

## Phases

Vertical slices — each phase ends with something runnable and verified. A
phase marked **real git** drives `git` itself in `tmp_path` repositories, the
way `tests/test_the_waiver_can_be_typed.py` does; CI runs those on the git
floor phase 1 names and on the newest git, and the Windows leg runs phase 2's.
Narrow runs per phase are the named modules through `bin/test`, `ruff check`
and `ruff format --check` on the changed Python, `bin/evidence-check --strict .`
where a ledger moves. The broad gate is the sealer's, once, after the rounds.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The hook surface and the corpora, measured** (real git). M1–M3, M5, M10, M11 answered by `test_tmp_` probes on the git here (2.50.1) and on the oldest git CI can install, deleted after; M6 and M7 counted (the corpora's generators replayed through real bash in sandbox repositories carrying throwaway stubs, against an exported `86256492` tree's PreToolUse verdicts; the three transcripts classified); M8 grepped. The spec's comparison table re-stated with numbers in `phases/phase-1.md`, the git floor named for P4, and one version-keyed case pinning M1–M3's table. No file under `hooks/` changes | `tests/test_the_hook_surface_is_what_the_design_assumes.py` (new; real git; skips below the floor, naming it); the phase record's tables, each row `executed` with the probe's command | fc873413 |
| 2 | **The installer and the stubs** (real git). `hooks/hook-install.py` in `GROUPS["session-start"]` and `GROUPS["pre-bash"]`; `hooks/git/{pre-commit,reference-transaction,post-checkout,post-commit}.py` as entry points that exit 0; the stub shape (marker line, embedded installed path, `python3 || py -3`, `-f` test so an uninstalled plugin leaves a stub that exits 0); ownership and version rewrite; P1's answer for a foreign slot, said once through the dispatcher's failure channel; removal from a clone that opted out; S12, S13 | `tests/test_the_hooks_are_installed_where_git_runs_them.py` (new; real git; every message pinned, §14); `tests/test_a_gate_that_fails_says_so.py` and `tests/test_dispatch.py` for the new group members | d06f5e25 |
| 3 | **The commit gate at the commit** (real git). `hooks/gate.py` with the judgment moved from `hooks/commit-review-gate.py#judge`; `pre-commit` deciding in the worktree git commits into: session id from the environment then the lease (W3), P2's answer when neither, the press through `automation_answered`, the declaration through `routing.declared`, both arms, `-c specseal.waive=` (M11), the refusal texts (W1, W2) with the old spelling named where P3 keeps it; `reference-transaction` as the `--no-verify` backstop (M2); `implementer-notice.py` moved to `post-commit`; `commit-review-gate.py` removed from `GROUPS["pre-bash"]` in this same phase so the two never run together; S1–S6, S9 | `tests/test_the_commit_gate_decides_at_the_commit.py` (new; real git; the four recorded commands verbatim); `tests/test_an_automation_run_meets_no_commit_prompt.py`, `tests/test_the_waiver_can_be_typed.py`, `tests/test_gate_judges_the_repo_it_commits_to.py`, `tests/test_no_shape_the_base_stops_reads_silent.py`, `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`, `tests/test_a_commit_behind_a_reserved_word_is_judged.py` retargeted from PreToolUse payloads to real commits with bash as the oracle (S2), reader-based assertions deleted with a note; `tests/test_the_implementer_is_recorded.py`; `tests/test_routing_is_recorded.py` | 4388e73d |
| 4 | **Creation consent and the creation ladder at git** (real git). `post-checkout` writes the record in the clone the worktree belongs to, keyed by session (S7); the creation refusal at `reference-transaction prepared` where M3 says the new `HEAD` is a transaction, else the post-hoc path P4 settles (S8); the Agent/Task arm kept or retired by M5; the token translator for `[worktree-ok]` and `git -c specseal.answer=worktree-ok` (P3, W6); `creation_directory` deleted; `hooks/worktree-guard.py`'s creation arm reads the hook's tree | `tests/test_the_guard_asks_once_per_session.py` retargeted (writer half to `post-checkout`, reader half to the refusal), `tests/test_worktree_guard.py`'s creation rows, `tests/test_worktree_guard_signals.py` and `tests/test_lease_liveness.py` unchanged and green | |
| 5 | **The switch at git** (real git). The three switch rows as refusals at `prepared` or as `post-checkout` undo per M1 (S10); `[shared-tree-ok]` and `-c specseal.answer=shared-tree-ok`; the dirty-tree row as a refusal naming `-c specseal.answer=carry-changes`; P4's fallback wired for the switch and creation arms alone below the floor, through `hooks/cmdline_base.py` as it stands (S11); the guard's Bash walk deleted above the floor | `tests/test_the_switch_is_judged_where_git_switches.py` (new; real git; version-keyed), `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py` with its frozen-reader rows kept under the fallback marker only, `tests/test_what_the_reader_understands.py#test_the_guard_reads_the_same_answer` retargeted to bytes | |
| 6 | **Deletion, policy, contract, ledger**. `hooks/cmdline.py` reduced to `hooks/tokens.py` (W5); `hooks/commit-review-gate.py` deleted; `hooks/cmdline_base.py` deleted unless P4 keeps it; the two policy documents rewritten around the action (spec §*Scope* 7, the migration table from spec §*Migration*, the #689 whites closed by deletion); contract §9 and §17, `agents/smith.md`, `skills/implement/SKILL.md` §1, `templates/sdd-routing.md`'s comment, `README.md`, `README.ko.md` and this repository's `CLAUDE.md` rewritten to what is true; the ledger rows anchored on removed units REMOVED in their files, the new claims in `seal/ledger/1790815613-….md`, drifted rows re-read (W4); the changelog fragment with its operational note; S14, S15 | `bin/survivor-check`, `bin/evidence-check --strict .`, `bin/unverified-check`, `tests/test_the_hooks_hide_what_a_renderer_hides.py`'s enforced-by walk, `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, `tests/test_edits_go_through_the_edit_tool.py` rewritten to the new reason, `tests/test_a_rider_reaches_its_file.py`, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` | |

This table is also where the work records how far it got. There is no
separate task list.

**Status is empty, or the commit that closed the phase.** Re-read the column
after any rebase.

What a phase discovers while it is being built, and needs the next phase to
know, goes to `phases/phase-N.md` from `templates/sdd-phase.md` when the
phase closes. Phase 1's record is the one every later phase reads first: it
holds the floor, the M-answers and the numbers.

## Operational impact

- **Files written into a person's clone.** Four stubs under
  `<git-common-dir>/hooks/` of every opted-in clone a session enters, each
  carrying a marker line and the installed plugin's absolute path; said once
  per session when written. `core.hooksPath` is never written. A foreign slot
  is never overwritten (P1). A plugin uninstall leaves stubs that test the
  path and exit 0.
- **Compatibility.** The PreToolUse commit gate is gone, so a commit on an
  undeclared branch is refused by git with a non-zero exit instead of the
  harness's two buttons; a `;`-joined command runs its later parts after a
  refused commit, where a `deny` used to stop the whole line. The old waiver
  spellings keep working only if P3 keeps the translator; the git-native
  spelling is the one every refusal names. Below the git floor the switch and
  creation arms behave exactly as 0.16.0.
- **CI.** A git-version matrix leg (the floor and the newest) for the
  real-git modules; the Windows leg runs phase 2's module.
- **Dependencies and environment.** None new. The hooks read
  `CLAUDE_CODE_SESSION_ID`, `CLAUDECODE`, `CLAUDE_PID` and git's own
  `GIT_DIR`/`GIT_CONFIG_PARAMETERS`; they set nothing.
- **Latency.** One interpreter start per judged action, and none where the
  stub exits before Python (`CLAUDECODE` unset under P2's default; a
  `reference-transaction` state other than `prepared`). M10's numbers go into
  the policy the way `hooks/dispatch.py`'s docstring carries its own.
