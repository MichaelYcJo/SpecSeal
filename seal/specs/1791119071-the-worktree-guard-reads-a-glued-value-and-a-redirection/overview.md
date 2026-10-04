# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/worktree-guard-spec.md` §*A. Branch switch*, §*Unknowns resolve conservatively*, §*Which tree, when the command walks to it*, §*Known limits*; this item's `spec.md`, `plan.md`, `questions.md`; `seal/specs/1790815613-…/questions.md` P4 (as `spec.md` quotes it); `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `CONTRIBUTING.md` §*Running the checks*; agent contract §7, §12, §14, §15
· evidence: `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md` — D1–D4 added; `Corrected · G1` (0.18.1); `Re-read ·` rows for M2 (0.16.0), K5, K6, K7, N1 and `Corrected · G17` (0.18.0)
· verified: executed — M1 under bash with git 2.54.0, the base's and the build's generated sweeps, the corpus before and after, the module against the base guard (67 red) and the build (green), 39 + 4 mutation breaks, the plan's seven narrow modules, ruff on the touched Python, `evidence-check --strict`, `survivor-check`, `test_no_real_identifiers.py`; read — the rewritten sentence against `switch_kind` clause by clause

## Why this work exists

The worktree guard let `git checkout -bNAME`, `git switch --cre NAME`, `git
checkout feature/x>/dev/null` and their kind switch a shared or dirty tree
unasked. It now reads a checkout's and a switch's words as git and bash hand
them, and a file restore keeps its silence because the tree still decides.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The corpus | `spec.md` A11: "the corpus 1790993140's phase 3 fixed (27,351 distinct command and directory pairs …)" | the 25,741 pairs still on disk, before and after alike | at least one transcript D1 read is gone from this machine (main transcripts 34 → 33), and nothing restores it (`phases/phase-1.md`) |
| A5's rule past an `&` cut | `spec.md` A5: "where one does, the question follows §*Which tree*'s rule" | only candidate C's half is held to the rule there; the frozen loop's half is named in §*Known limits* | the frozen segment holds the words before the cut alone, so `git checkout feature/x <&1 -- README.md` is judged a switch, as at `94d7b2e0` (32 generated shapes); not this change's, and fixing it means teaching the frozen splitter, which P4 keeps |
| `--no-` negation | `spec.md` In 1: "a long word resolves by exact name, then by unique prefix, `--no-` negating" | no negation rule | a negation reads exactly as a word git refuses (takes nothing, creates nothing), no long name begins with `no-`, and no case could tell the two apart (`phases/phase-2.md`) |
| A8's red | `spec.md` A8: "red with one operator removed from the local list" | red with `<>` removed; `&>` removed stays green | a glued `&` is cut and dropped before the operator is read, so `&>` in the list is redundant for this reduction (`phases/phase-2.md`) |
| `checkout -U 3 feature/x` | `spec.md` Axis 2 lists `-U 3 N` as a V shape that switches | read as a switch to `feature/x`, and named in §*Known limits* | git refuses `-U` without `-p` (M1); the loud direction on a shape git refuses, and teaching the reader `-U` needs `-p` is a rule nobody asked for |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, lint and typecheck over the repository | the sealer, after the review rounds settle |
| A7 against any git but 2.54.0 (CI's ubuntu, macOS and Windows gits) | CI's run of `test_the_option_table_binds_the_installed_git` on the pull request |

## Not done

The R& shapes stay candidate C's, which reads no tree (`spec.md` *Out*,
Alternative F), and a cut before `--` stays the frozen loop's misreading. The
`worktree` arm, `-p`/`--pathspec-from-file`, aliases and a quoted `>` stay
out as `spec.md` *Out* says. `plan.md` line 81 gained `NAME NOT IN TREE` on
`_names_anew`, a name round 3's unmerged fence held, because the records arm · NAME NOT IN TREE
of `evidence-check` refused it.

## Fed back into the spec

none
