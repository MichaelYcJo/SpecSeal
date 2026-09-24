# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — overview

📋 implement applied
· spec:     this work item's spec.md (Scope 1–4, A1–A7, The class enumerated, Data & interfaces), plan.md (phases 1–3, Alternatives, Where each claim is executed), questions.md Q1–Q3; templates/config.md §Broad gate; agents/sealer.md §The command; CONTRIBUTING.md §Running the checks; CLAUDE.md §fragments, §commit early; agent-contract §2, §12–§15
· evidence: seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md A1–A6 added; re-read and re-stamped where they live: seal/releases/0.10.0.md S4 and S1, four rows of seal/releases/0.12.0.md, seal/releases/0.12.2.md R7, seal/releases/0.15.1.md G3, N1 and P3, seal/releases/0.8.2.md R3 and R4, seal/releases/0.5.0.md S8
· verified: executed — each phase's modules and every module reading a document it edited (26, 53 and 58 modules), every new case seen red, a mutation pass per phase, the Q2 probe, evidence-check; read — Q3's grep, the static list of gh callers; unverified — the full suite, lint and typecheck (the sealer's), the `cmd.exe` half of A4 (CI's windows leg), and whether any case in the tree reaches a live gh (the sealer's run and the three CI legs)

## Why this work exists

On Windows the broad gate handed `cmd.exe` the row `bin/test -q`, which it
runs as a command called `bin`, and a suite that never started was reported
as a suite that failed; the gate now hands `cmd.exe` `bin\test`, says when a
failing suite printed no summary, and this repository's suite runs with `gh`
logged out so a case reaching a live `gh` fails locally as it does on CI.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many ledger rows the template edit drifts | `spec.md` §*Data & interfaces*: "`templates/config.md#"## Broad gate"` is cited by `seal/releases/0.10.0.md` S4 and by `0.12.0.md`. Editing the section drifts both rows." `evidence-check` found three rows in `0.12.0.md` on that anchor, and `0.5.0.md` S8 on the whole file's anchor | all five re-read and re-stamped | A row an edit drifts is re-read where it lives (`CLAUDE.md` §*Appended is the word*); the check names the rows, and the spec's count was a read |
| `spec.md`'s coordinate for `gate` | `spec.md` spelled the path from the file name alone, which `evidence-check` refuses as BROKEN once the work item has a fragment | corrected to `skills/verify/scripts/broad_gate.py#gate@79c16119` | The anchor and the claim are unchanged; only the path was short, and the check names where the identical content is |

## Not verified

| Item | Who must answer |
|---|---|
| `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` with the exit code and output passed through (A4, `questions.md` Q1) | CI's `windows-latest` leg at the pull request |
| No case in the tree reaches a live `gh` now that the suite runs logged out (`spec.md` §*The class, enumerated*) | the sealer's one broad run, then the three CI legs |
| No child process in `tests/` builds its environment through a helper Q3's grep could not see | the three CI legs, which are logged out whatever the environment says |
| A `gh` login kept in the OS keyring is not reached under the suite's environment, because `GH_TOKEN` is set first (round 1's 🟡 1; read from upstream `cli/cli`) | `test_the_token_gh_would_send_is_not_a_login` run on a machine whose `gh` login is in the keyring — not this builder's machine, whose login is in `hosts.yml`, and not CI, which has none |

## Not done

nothing

## Fed back into the spec

none
