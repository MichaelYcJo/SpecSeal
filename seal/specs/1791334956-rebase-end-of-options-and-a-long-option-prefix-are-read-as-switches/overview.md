# 1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     `spec.md` and `plan.md` of this work item; round 3's report of work item 1791270162 (verdicts, probes, Paste-ready fixes); `docs/worktree-guard-spec.md` §A and §*Known limits*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file*
· evidence: `seal/ledger/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches.md` R1–R4; F3, F4, F5, F7, F8, S12, K7 and the K6 and G17 re-reads in 1791270162's fragment re-stamped in place after reading each
· verified: executed — git 2.50.1 on every rebase spelling the class holds, the new cases red at `3d78c220` and green after, `bin/mutation-check` on each changed unit, the guard modules' slices, `bin/evidence-check --strict .`; read — `git rebase -h`, the drifted rows' claims

## Why this work exists

`git rebase --ro <branch>` and `git rebase --end-of-options <upstream> <branch>` switch HEAD before they rebase, and the guard let both through in a tree another session was working in; it now stops them as it stops every rebase that names a branch.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which prefixes of `--root` count | Round 3's paste-ready fix reads `w.startswith("--r") and "--root".startswith(w)`, so `--r` counts / the code reads from `--ro` | `--ro` | Executed on git 2.50.1: `git rebase --r feature/x` exits 129, "ambiguous option: r (could be --reschedule-failed-exec or --reapply-cherry-picks)", and HEAD stays. Reading `--r` as `--root` stops a command git refuses; the guard now reads exactly what git reads, and `git rebase --r feature/x` is a listed case |
| Where `--root` is read from | `spec.md` Data & interfaces: "a prefix of `--root` counts as `--root`" / the code also reads it off the words bash hands git rather than off `args` | off the plain words | Same class: `git rebase --root>/dev/null feature/x` hands git `--root feature/x` and switches, and the base read `"--root" in args`, which the redirection hid. Red under the old reading through `bin/mutation-check` |
| What pins ⬜ 2 and ⬜ 3 | `spec.md` S5: "the policy pin cases" / the build also added a behaviour case for each | both | §14 of the agent contract: the sentences describe what a person meets, so the behaviour they describe is pinned too — `test_a_one_tree_reason_calls_the_tree_it_judges_this_tree`, and two rows of `UNPLACED` |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds settle |
| The git-binding case's new forms under CI's gits: a branch named `-x` made by `update-ref`, and `--end-of-options`, which git has read since 2.24 | CI on Ubuntu, macOS and the Windows shards at the pull request |

## Not done

Every other subcommand on `LEAVES_THE_TREE` is out of scope (`spec.md` Out): round 3 judged them, and the git-binding case holds them. `questions.md` P5 of 1791270162 stays as built. F3 in 1791270162's fragment was re-stamped and left as written: its claim still holds and R1 here carries the two new spellings.

## Fed back into the spec

- Inferred during implementation: `--root` is the only long option of `git rebase -h` (git 2.50.1) that changes how many words name a branch; every other option either takes no value or has its value counted as a word. R1 holds it.
- Inferred during implementation: the guard reads `--root` off the words bash hands git, so a redirection glued to it hides nothing. `docs/worktree-guard-spec.md` §A does not name this spelling; R1 and the function's docstring do.
