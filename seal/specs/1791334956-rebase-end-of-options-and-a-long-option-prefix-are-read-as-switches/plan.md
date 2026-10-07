# Implementation Plan: rebase's --end-of-options and a long-option prefix are read as switches (#854)

<!-- seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-07 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

Apply round 3's paste-ready fix for 🟡 1 and close its class. Plant the cases that show it red first. Correct §A and §Known limits for ⬜ 2 and ⬜ 3. One phase.

## Technical context

- `hooks/worktree-guard.py#_rebase_names_a_branch` reads a rebase's words. Its option-end set is `--` today, and it reads `--root` by its full spelling only.
- `tests/test_worktree_guard.py` holds the rebase cases, `SWITCHING`, and `test_no_listed_form_moves_head_under_git`, which binds `LEAVES_THE_TREE` to git.
- **Failure scenario of the chosen approach:** a future git adds a long option to `rebase` whose prefix collides with `--root`, such as `--ro…`. The prefix reading then mis-reads it. The git-binding case catches that on the CI git, as long as the new option has a form in it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Read `--end-of-options` and every unambiguous prefix of `--root` (round 3's fix) | a future colliding option, caught by the git-binding case | chosen |
| Read every `rebase` with any long option as unrecognised | `git rebase --rebase-merges main`, which leaves HEAD on its branch, would stop in a dirty tree | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | 🟡 1 fixed with its class enumerated against `git rebase -h`, ⬜ 2 and ⬜ 3 in the policy with their pins, S1–S5, the changelog fragment and ledger rows | each new case red at 3d78c220 and green after; `bin/mutation-check` red on each changed unit; the guard modules; `bin/evidence-check --strict .`; `survivor-check --range origin/release/v0.20.0...HEAD` | |

## Operational impact

`git rebase --ro <branch>` and `git rebase --end-of-options <upstream> <branch>` now stop in a tree where a switch matters. Every other rebase reads as before.
