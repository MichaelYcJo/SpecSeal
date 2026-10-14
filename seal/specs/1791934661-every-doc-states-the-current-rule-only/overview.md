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
| Released rows answered per phase | `spec.md` S2: one `Re-read ·` or `Corrected ·` row per row, in the phase / none written | none written, in any phase | the orchestrator's decision of 2026-10-14: #944 retires the released ledger files |
| Survivor rows | `spec.md` §*Removes*: `survivor-check` reads every removed sentence / no `survivors.md` row | none | the orchestrator's decision of 2026-10-14: the survivor sweep is retired by #944 |
| The two consent comparison tables in `docs/worktree-guard-spec.md` §*Creation consent* | `spec.md` §*Removes* names no phase-1 removal / both tables left, their content folded into three sentences | folded | a format the frame did not list; every property the tables held is stated in *The routing answer is the second consent* and *A `routing.md` is not read* |
| Pins on the one-root pair's dated sections | `plan.md` phase 6: "the three dated-section cases removed" / two more cases in `tests/test_first_setup_asks_once.py` read *Decided after the thread* | the three removed; the two re-pointed at the sections that state their rules | their needles are rules that still hold; `phases/phase-6.md` |
| Files outside `docs/` in phase 6 | `spec.md` §*Scope*: every file outside `docs/` is #940's or #923's / `hooks/root-migrate.py`'s citation and `hooks/worktree_consent.py`'s `Reads:` line edited | edited | the same §*Scope* edits a citing file in the phase that removes its heading; the `Reads:` line repairs the census phase 1's docstring fix broke |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ The 19 released family roots phase 1 drifted — 18 anchoring `docs/worktree-guard-spec.md` (79 rows, 103 anchors) and its two re-pointed test units, one `BASELINE`: `evidence-check --strict` exits 2 until each is re-read or corrected; three read as `Corrected ·` (`phases/phase-1.md`) | answered by the orchestrator on 2026-10-14: not re-read or corrected, because #944 retires the released ledger files; `--strict` stays 2 on this branch until #944 lands |
| ✅ `survivor-check` over `origin/release/v0.22.0...HEAD` names 410 places carrying wording phase 1 removed, so the hygiene step fails at the pull request | answered by the orchestrator on 2026-10-14: the survivor sweep is retired by #944, and no `survivors.md` row is written |
| The `bytes:` and `history:` rows for `docs/worktree-guard-spec.md` (34,973 and 0), and that #923's checker reads the file at 0 history | the rebase onto #923 phase 1, which is the orchestrator's |
| The `bytes:` and `history:` rows for `docs/one-root-by-lifetime.md` (19,422 and 0) and its `.ko.md` (23,684 and 0) | the rebase onto #923 phase 1, which is the orchestrator's |
| The full suite, the repository-wide lint and the typecheck over this branch | the sealer, once the rounds settle |

## Not done

Phases 2–5 and 7–10, by the spawns' order; phases 1 and 6 are built.

## Fed back into the spec

none
