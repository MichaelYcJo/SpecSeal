# 1791019477-the-commit-gate-policy-is-cut-into-files-by-question — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `spec.md` (D1–D11, K1–K7, S1–S10), `plan.md`, `questions.md` (Q1–Q5, M1–M3, W1–W2); `docs/the-record-layout.md` §*What is decided and not built yet* (F1) and §*The size a reader takes whole*; `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* and §*A released row is read again in the branch's fragment*; `CLAUDE.md` §*a change writes fragments, never the shared file*
· evidence: `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md`: C1–C5, 2 `Corrected ·` rows, 13 `Re-read ·` rows; work item 1790993137's P11 re-stamped in place
· verified: executed — the S1 and S5 probes, a five-document reader probe, `fold-check`, `evidence-check`, `correction-check`, `survivor-check`, the narrow modules of each phase; read — every drifted row against its edit, the three preambles

## Why this work exists

The commit gate's policy was one 1,047-line document frozen over the ceiling;
cut along its headings into three, each answers one question and each takes
the next fold again.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The parent's base line count | Spec §*Data & interfaces*: "parent (1–40, 278–759, 995–1047) \| 576". The move script counted 575 base lines (40 + 482 + 53); with the rewritten preamble the parent is 586 | the measured count | the script's own `len()` over the three ranges, which asserts each boundary heading before it copies (`phases/phase-1.md`) |
| K6's crossing lines | Spec K6: "Line 91 …, 199 and 273–274 …, and 283–284" cross the cut. Line 152, *the PreToolUse reading in the next section stands aside*, crosses too: in its new file there is no next section | line 152 cited by file and section as well | K6's command was `awk` for `above`/`below`, which `next section` does not match. W1 is the row that asks for exactly this re-read (`phases/phase-1.md`) |
| Moved units' hashes | Spec D2: "Every moved unit hashes as before, so a `Corrected ·` row records the same hash at the new path". `### Known limits of the commit gate inside git` holds base line 199, a K6 line, so its hash moved from `57e93f4b` to `da878498`; the two arms' headings hash as before (`3f374912`, `4b9d8901`) | G17's `Corrected ·` row records the new hash and says which line changed | D5 requires the re-point, and the line sits inside the unit G17 anchors; the S1 probe shows it is the only line that changed there |
| K3's `Re-read ·` count for the document's own anchors | Spec K3: "2 `Re-read ·` rows for the document's own anchors" (E9 and S2). Only E9 drifted. S2's `"Authority for"` minor anchor hashes the line it names, and D4 kept that line | one `Re-read ·` row for the document's own anchors, 12 for what K5 drifted | `evidence-check` named no drift on S2 before or after the `--reverify`; M1's row carries the whole count |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

**Nine drifted rows that were already drifted at the base are left.**
`evidence-check` names them at 2b1dcb1f exactly as at this branch's tip: six
citations and one `templates/config.md` coordinate in work item 1790993138's
fragment, one `docs/branch-and-release.md` coordinate in 1790993139's, and
`seal/releases/0.5.0.md`'s `templates/config.md` row. This work drifted none
of them, and the integration of 0.18.0's first four items re-stamps them in
its own commit, so re-stamping them here would conflict with that commit at
the merge for nothing. `evidence-check --strict` fails on them until this
branch meets that commit.

## Fed back into the spec

none
