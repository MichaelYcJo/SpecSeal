# 1791934661-every-doc-states-the-current-rule-only — overview

📋 implement applied
· spec:     `spec.md` §*The problem, measured*, §*Targets*, §*Scope*, §*Which case reaches which doc*, S1–S5, S10, §*Removes*; `plan.md` phase 1, §*Dependency*, §*Technical context*; `questions.md`; #923's `spec.md` §*The shape of a compact file*, §*Non-inferiority, proved per phase*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*
· evidence: none — the orchestrator deferred the released-row re-reads to the owner (`phases/phase-1.md`)
· verified: executed — `measure.py` before and after, the narrow modules, three `mutation-check` runs on the re-pointed pins and one on the dropped `BASELINE` entry, `fold-check`, `evidence-check` strict and lenient, `--reverify` without `--into`, `survivor-check`; read — the 79 released rows' claims against the new text

## Why this work exists

`docs/` sits at its ceiling because changes appended the story of each rule;
each file is rewritten to the rules alone so a reader pays for rules only.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Quoted-line anchors in phase 1 | `plan.md` phase 1: "the 3 quoted-line anchors corrected" / the 103 anchors are all heading paths | nothing to correct | `spec.md`'s own table and `measure.txt` say 0; `phases/phase-1.md` |
| Released rows answered in phase 1 | `spec.md` S2: one `Re-read ·` or `Corrected ·` row per row, in the phase / none written | none written | the orchestrator's instruction of 2026-10-14: the owner decides how released rows into rewritten docs are handled |
| The two consent comparison tables in `docs/worktree-guard-spec.md` §*Creation consent* | `spec.md` §*Removes* names no phase-1 removal / both tables left, their content folded into three sentences | folded | a format the frame did not list; every property the tables held is stated in *The routing answer is the second consent* and *A `routing.md` is not read* |

## Not verified

| Item | Who must answer |
|---|---|
| The 19 released family roots phase 1 drifted — 18 anchoring `docs/worktree-guard-spec.md` (79 rows, 103 anchors) and its two re-pointed test units, one `BASELINE`: `evidence-check --strict` exits 2 until each is re-read or corrected; three read as `Corrected ·` (`phases/phase-1.md`) | the owner, deciding how the step runs; then whoever runs it |
| `survivor-check` over `origin/release/v0.22.0...HEAD` names 410 places carrying wording phase 1 removed, so the hygiene step fails at the pull request | the orchestrator — per-place rows, a range row, or another answer (`phases/phase-1.md`) |
| The `bytes:` and `history:` rows for `docs/worktree-guard-spec.md` (34,973 and 0), and that #923's checker reads the file at 0 history | the rebase onto #923 phase 1, which is the orchestrator's |
| The full suite, the repository-wide lint and the typecheck over this branch | the sealer, once the rounds settle |

## Not done

Phase 2 onward, by the spawn's order.

## Fed back into the spec

none
