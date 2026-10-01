# 1790815614-a-joined-projects-specs-is-read-and-never-taken — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     filled at the close of the build
· evidence: filled at the close of the build
· verified: filled at the close of the build

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

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the broad gate over the finished branch | the orchestrator, through the sealer |

## Not done

nothing

## Fed back into the spec

none
