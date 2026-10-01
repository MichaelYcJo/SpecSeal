# 1790815614-a-joined-projects-specs-is-read-and-never-taken — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this work item; `CLAUDE.md` §*The goal*, §*Repo rule — a change writes fragments*; `docs/one-root-by-lifetime.md` §*The change in four lines*, §*Decided after the thread*, §*What happens to the existing directories at the switch*; `docs/review-chain-spec.md` §*The survivor sweep*; `skills/implement/orchestration.md` §*Orchestrator: Bootstrap*; `templates/config.md`; `hooks/root-migrate.py`, `hooks/config.py`, `hooks/optin.py#home_at`, `#git_common_dir`; `survivor_check.py`, `unverified_check.py`, `settle.py#SPECS`, `correction_check.py`'s ledger constants, `hooks/routing.py#WORK_ITEMS`, `evidence_check.py#default_patterns`; `agents/smith.md`'s rider
· evidence: `seal/ledger/1790815614-….md` rows B1–B4, A1, F1, C1, D1, D2, D3, C2, added; 58 existing rows across fourteen `seal/releases/*.md` re-read with dated notes and re-stamped, `0.15.1.md` C2 corrected in place
· verified: executed — every new case red first (against the base or by mutation), 60 mutations across the branch each red (two survived their first run and were each answered by a sharper case, then red), the narrow modules and every module reading an edited file (2410 and 2638 cases), `evidence-check` 0 drifted · 0 broken, `survivor-check --range cd24f516..HEAD` clean; read — the README and design-record prose against the hook; unverified — the full suite, lint and broad gate

## Why this work exists

A person joining a project that keeps its own `specs/` had it read as the
0.3.x layout and moved into `seal/` unasked (#688); the plugin now writes only
its own root and reads every other `specs/` as history.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the re-point's moved set comes from (phase 1) | `spec.md` §Scope 3: "The ledger re-point (`#repoint_path`) follows the moved set, not the name pattern" · code: the set is the directories under `seal/specs/` after the moves (`moved_items`), not the units `moves` listed this run | code, as a narrowing of the spec's words | a stopped run leaves part of the move done and its rows still citing `specs/`, and a resume lists only what remains (`root-migrate.py` docstring, *a stopped move resumes*); this run's units would leave the first half's rows behind. `repoint(root)` also keeps one argument because `test_a_repoint_that_fails_after_the_moves_says_so_and_stamps_nothing` stands it in with one |
| An existing case whose premise the default overturns (phase 3) | `spec.md` §*Data & interfaces*: absent, "every directory named `specs` outside the plugin's root, at any depth" · `test_a_specs_directory_outside_the_seal_root_stays_in_the_range` asserted a deleted `docs/specs/login-flow/` is measured | the spec; the case now declares `Reference specs \| none` | the case's own docstring says what it pins: `WORK_ITEM_DIR` anchored, so `docs/specs/<name>/` is not read as a retired work item. That still holds where a repository puts its `specs/` back, which is the only place it can be observed now; under the default the directory is out of the range for a different reason, the one this work item adds |
| `hooks/config.py` spells the root's name instead of importing it (phase 3) | `spec.md` §*Data & interfaces*: the predicate answers "outside the plugin's root" · code: `config.HOME = "seal"`, not `optin.HOME` | code | `config.py` is loaded by path beside `blocks.py`; a third sibling is a new way for a copy taken alone to break (`tests/test_a_script_copied_alone_exits_2.py`). A case holds the two spellings equal |
| A repository with no `seal/` root (phase 4) | `spec.md` §*Data & interfaces*: "Absent, empty or unreadable means the default", and the default is "every directory named `specs` outside the plugin's root" — no root is not named · code: no root at either place is `()`, no reference root | code, as a reading of *outside the plugin's root* where there is no root | thirty-eight cases of `tests/test_unverified_rows_close.py` keep a work item under a top-level `specs/<id>/` in a repository with no root — the 0.3.x spelling, which `unverified_check.py` and `survivor_check.py` read as the plugin's records on purpose — and the default would have pruned every one. The only layout the plugin read without a root is that one, whose `specs/` was its own; a person joining a project runs the bootstrap, which creates the root, before a check reads the tree. The owner can overturn this; `templates/config.md` §*Reference specs* names the case in its value table |
| `unverified-check` with no `hooks/` beside it (phase 4) | `plan.md` §*Alternatives*: one resolver in `hooks/config.py`, "loaded by path" — nothing said what a copy without it does · code: it prunes nothing | code | the script loaded no sibling before, so a copy taken alone worked; a refusal would be its first break, and pruning nothing reads more, never less. The scripts held to exit 2 in `tests/test_a_script_copied_alone_exits_2.py` already loaded a sibling |
| What a mark is (round 1's fix pass, 🟡 1) | `spec.md` §Scope 1: "The marks are `routing.md` directly under the directory, or a `rounds/` directory directly under it" · code: a `routing.md` or a file under `rounds/` that git tracks (`tracked_marks`) | code, as a narrowing of the spec's words | the hook's units come from `git ls-files`, and an empty or ignored `rounds/` (or an ignored `routing.md`) on disk made a team's directory a work item with `git status` clean; round 1 executed both `rounds/` shapes moving and staging the directory. Every 0.3.x work item tracked its `routing.md`, so nothing of the plugin's is left behind. The approved `spec.md` is left as written and its sentence is listed in `survivors.md` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the broad gate over the finished branch | the orchestrator, through the sealer |
| The session-start hook over a real joined project through `hooks/dispatch.py`, not the fixture's `main()` call | the repository owner, at the next session start in such a project |
| `unverified_check.py#reference_rule`'s `top is None` guard on Windows, where a cross-volume `relpath` is the case it also keeps from being asked; only its contract is pinned here | a maintainer with a Windows machine, or the CI windows leg |
| The sealer's broad gate at `684bae49` (`NOT SEALED 684bae49 against a340221b`, 2 failed, 6438 passed) found two scopes this work item added to `tests/test_the_root_migrates_itself.py` — `test_an_id_shaped_directory_without_the_marks_stays_and_is_named` and `test_a_mark_git_does_not_track_is_not_a_mark`, each reading `git diff --cached --name-only` in its fixture — unclassified in `tests/test_a_shrunken_corpus_declines_to_judge.py`'s census, both failures `new`. The commit after `684bae49` adds both to `LISTS_A_FIXTURE`, the table for a scope that lists a repository the case built; it landed after the review run was capped, so no round read it | the orchestrator, at the sealer's next broad gate |
| PR #700's `windows-latest` leg (CI run 36819214088), after the seal at `14a1e7d2`, failed `test_a_linked_specs_holding_only_unmarked_directories_is_not_refused`: the line named nothing left. The cause is the hook, not the case: `run_moves`' cleanup `os.rmdir`s the old roots, which rested on POSIX `rmdir` refusing a symbolic link with `ENOTDIR`; Windows' `RemoveDirectoryW` removes a directory link itself, so a team's linked `specs/` was deleted from the working tree and `old_items` then listed nothing. The commit after `14a1e7d2` skips a link in that cleanup, with `test_the_cleanup_never_removes_a_linked_specs`, which gives `rmdir` Windows' semantics and was red against `14a1e7d2`. Executed on macOS only; it landed after the capped run and after the seal, so no round read it and the windows leg has not run it | CI's `windows-latest` leg on the PR, and the orchestrator |

## Not done

**No case pins the commit gate's reading of `agents/smith.md` and
`skills/implement/SKILL.md`.** Phase 5 measured that one apostrophe above
either file's waiver example flips `_hides_a_commit` over the file, and
restored the base's reading by rewording. A pin was within reach and not
taken: `tests/test_edits_go_through_the_edit_tool.py` declines on purpose to
assert `agents/smith.md`'s tripping, calling it a defect that must not be
pinned as a requirement, so which reading is right is a decision about the
gate and the rider, not about reference roots. The rider names a retired
work item's `questions.md` Q4 as the question's home, and that file is gone;
`phases/phase-5.md` holds the measurement for whoever takes it.

## Fed back into the spec

Inferred during implementation, each in `templates/config.md` §*Reference
specs* and the code, for a planner to overturn:

- A repository with no `seal/` root at either place has no reference root
  (phase 4).
- A path named on `unverified-check`'s command line inside a reference root
  is read, a file or a directory, and the base is compared by the same rule
  (phase 4).
- A prefix the row names inside `seal/` is dropped (phase 3).
