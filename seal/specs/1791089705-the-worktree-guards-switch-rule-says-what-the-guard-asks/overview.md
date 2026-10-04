# 1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*; this item's `spec.md`, `plan.md`, `questions.md`; round 3's report of 1791019475 (§*Findings* 🟡 9 and ⬜ 10, §*Paste-ready fixes*); `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; agent contract §12, §14, §15
· evidence: `seal/ledger/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks.md` — G1 added; `Re-read ·` rows for M2 (0.16.0), K5 and K7 (0.18.0)
· verified: executed — the pin red then green, three `KINDS` mutants red, the rule-case mutant surviving before C3 and red after, the narrow modules, `survivor-check`, `evidence-check --strict` (exit 2, every drifted row the wave-one squashes' and none this item's: this fragment reads 11 ok, 0 drifted; #766 re-reads the ten); read — the sentence against `switch_kind` clause by clause

## Why this work exists

The sentence that tells a person when the worktree guard asks now names the
words the guard actually reads. A test pins the sentence, and three rows bind
the code to the three words it used to get wrong.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A7's range | `spec.md` A7: "`bin/survivor-check --range e141980a...HEAD`". After the merge of `origin/release/v0.18.1`, that range also holds #756–#758 | `origin/release/v0.18.1...HEAD` and the build range `807fe9e7..f5dc2aa2` | the merge is not this item's removal of wording; both ranges report three removed sentences and no survivor (`phases/phase-1.md`) |
| K7's stamp in `spec.md` | `spec.md` *Data & interfaces* quoted K7's coordinate with the heading shortened to "Which tree…", which `evidence-check`'s records arm refuses as `BROKEN` once the ledger fragment exists | the heading written out in full, the hash kept | a locator nothing resolves fails the strict run; the full heading is what K7 cites, and the stamp now reads `DRIFTED`, which a live item's records may (`skills/evidence-check/SKILL.md` §*The records arm*) |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, lint and typecheck over the repository | the sealer, after the review rounds settle |

## Not done

The glued short-option shapes (`switch -cfoo`, `checkout -bfoo`) stay out.
They are filed as #764, as the spawn said. `Re-read · C4` and `Re-read · S8`,
which the narrowed `--reverify` also wrote, were removed unread. They are
wave-one drift, and a parallel chore is re-reading them.

## Fed back into the spec

none
