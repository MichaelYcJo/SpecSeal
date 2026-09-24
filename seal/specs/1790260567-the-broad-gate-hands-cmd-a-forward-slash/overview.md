# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — overview

📋 implement applied
· spec:     this work item's spec.md (Scope 1–4, A1–A7, The class enumerated, Data & interfaces), plan.md (phases 1–3, Alternatives, Where each claim is executed), questions.md Q1–Q3; templates/config.md §Broad gate; CLAUDE.md §fragments, §commit early; agent-contract §2, §12–§15
· evidence: seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md A1–A4 added; seal/releases/0.10.0.md S4, three rows of seal/releases/0.12.0.md and seal/releases/0.5.0.md S8 re-read and re-stamped
· verified: executed — phase 1's modules and every module reading a document it edited, every new case seen red, a mutation pass; unverified — the full suite, lint and typecheck (the sealer's), and the `cmd.exe` half of A4 (CI's windows leg)

## Why this work exists

On Windows the broad gate handed `cmd.exe` the row `bin/test -q`, which it
runs as a command called `bin`, and a suite that never started was reported
as a suite that failed; the gate now hands `cmd.exe` `bin\test`.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many ledger rows the template edit drifts | `spec.md` §*Data & interfaces*: "`templates/config.md#"## Broad gate"` is cited by `seal/releases/0.10.0.md` S4 and by `0.12.0.md`. Editing the section drifts both rows." `evidence-check` found three rows in `0.12.0.md` on that anchor, and `0.5.0.md` S8 on the whole file's anchor | all five re-read and re-stamped | A row an edit drifts is re-read where it lives (`CLAUDE.md` §*Appended is the word*); the check names the rows, and the spec's count was a read |
| `spec.md`'s coordinate for `gate` | `spec.md` spelled the path from the file name alone, which `evidence-check` refuses as BROKEN once the work item has a fragment | corrected to `skills/verify/scripts/broad_gate.py#gate@79c16119` | The anchor and the claim are unchanged; only the path was short, and the check names where the identical content is |

## Not verified

| Item | Who must answer |
|---|---|
| `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` with the exit code and output passed through (A4, `questions.md` Q1) | CI's `windows-latest` leg at the pull request |

## Not done

nothing

## Fed back into the spec

none
