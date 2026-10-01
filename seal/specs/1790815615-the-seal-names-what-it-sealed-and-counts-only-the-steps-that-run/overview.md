# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md` (S1–S6, A1–A18, §Grounding, §*What was measured*), `plan.md` (Phases 1–4, Alternatives, Operational impact), `questions.md` (Q1–Q5); `docs/the-broad-gate.md` §*What the gate runs*, §*Where the stamp is drawn*; `skills/verify/SKILL.md` §*A seal says what it did not answer*, §*What the count does not say*; `agents/sealer.md` §*The command*; `skills/code-review/orchestration.md` §*The stamp is drawn for you*
· evidence: `seal/ledger/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run.md`, rows added per phase
· verified: per phase, in `phases/phase-N.md`; the full suite, lint and the broad gate are not run here (below)

## Why this work exists

The sealer's stamp and its two lines named two commits and never the branch, the base's ref or the work item they sealed, and the `workflow` row counted CI steps that never run for the base; after this a reader matches a stamp to its work by name and the count is the one CI will ask.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A repository with no remote does not collapse the ref | `spec.md` A3: *"Given `--base <sha>` or a repository with no remote, then the head reads `against <commit>` once"*. In a repository with no remote, `resolve_base` step 3 returns the ref **as given** (`base`), which is a branch name and not the commit | The head reads `against base @ <commit>` there; only a ref spelled in hex that is a prefix of the commit (or the reverse) collapses | `broad_gate.py#resolve_base` docstring step 3 (*"the ref as given"*); S1's own reason for the collapse is *"so no line reads `1e2bed9 @ 1e2bed9`"*, and `base @ 1e2bed9` repeats nothing. Phase 1 |
| The commit-the-cell line asks git before it prints | S2: *"On a sealed run with `--record`, one line follows the `SEALED` line"* | The line prints where `git status --porcelain` names the file the cell went into, which on every recorded seal in practice is always | A line saying *not committed* over a file that matches HEAD would be false on its face; asked rather than assumed, so it is true wherever it prints. Phase 1 |
| The line also follows a stamp drawn on a terminal | S2 names only the `SEALED` line, which a terminal run does not print | It prints after the drawn stamp too, on the same stream | The cell is written on that path as well and CI reads HEAD either way; the terminal case's `screen.count("SEALED") == 1` still holds because the line does not carry the word. Phase 1 |

## Not verified

| Item | Who must answer |
|---|---|
| Q3: the installed 0.16.0 `Stop` hook draws a values file this gate writes (rows labelled `""`, two extra keys) unchanged, under its old label, on the owner's screen | the repository owner, on the first real seal of the 0.17.0 run |
| The full suite, the repository-wide lint and the broad gate over this branch | the orchestrator, through the sealer after the review rounds settle |

## Not done

nothing

## Fed back into the spec

none
