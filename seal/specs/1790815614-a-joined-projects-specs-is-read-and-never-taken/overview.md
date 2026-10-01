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

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the broad gate over the finished branch | the orchestrator, through the sealer |

## Not done

nothing

## Fed back into the spec

none
