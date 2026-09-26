# 1790381329-the-deferred-sentences-and-pins — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. Opened at phase 3 and kept as the work goes; closed at phase 7. -->

📋 implement applied
· spec:     spec.md, plan.md, questions.md of this work item; `CLAUDE.md` (fragments, ledger rows); `skills/agent-contract/SKILL.md` §12, §14, §15; `docs/the-evidence-ledger.md` §*A correction a merge dropped*; issues #610, #611, #612, #613, #615, #616
· evidence: C1–C5 in `seal/ledger/1790381329-the-deferred-sentences-and-pins.md`; re-read and re-stamped rows in `seal/releases/0.4.0.md`, `0.5.0.md`, `0.8.0.md`, `0.8.1.md`, `0.9.3.md`, `0.10.0.md`, `0.11.4.md`, `0.12.0.md`, `0.13.0.md`, `0.13.1.md`, `0.14.0.md`, `0.15.0.md`, `0.15.3.md`, `0.15.4.md`; corrected in place: 0.13.0 S1, 0.15.4 S1 ×2
· verified: executed — each phase's narrow modules, every new case seen red, mutations on the #610 units, the Q1 probe, `as_cmd_expands` run directly, `evidence-check`, `survivor-check`; read — the enumerations' non-twin judgments; unverified — the full suite (the sealer's) and `cmd.exe`'s resume point (Windows)

## Why this work exists

Six items 0.15.4's capped rounds deferred — two scripts that died with a
traceback when copied alone, a settle heading the skill did not name, the
sentences placing CI's `--baseline` comparison at the fork point, a docstring
that missed *at a ready pull request*, the survivor sweep's statement of what
it leaves silent, and the broad gate's `%CD%` precedence — each fixed as a
class and pinned on its own example.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `payload_meter.py`'s case invocation (Q4) | questions.md Q4's default: *`--calibrate <an existing empty file>`*; the row passes a transcript path that need not exist | the path that need not exist | `calibration_of` calls `_session_cost()` before `spawns_in` opens the transcript, and an existing file would have meant editing `test_a_script_copied_alone_exits_2_and_names_what_it_misses`, which 0.15.4's M1 anchors (`phases/phase-1.md`) |
| #613's class | spec.md: the frame judged the class to be `fix_surface`'s docstring alone; `round_record.py#landing_values` said *the check refuses `Pass` beside `nobody` there* with no timing | fixed in phase 4 with the same qualifier | it is a statement of when the check refuses, which is the class #613 corrects (`phases/phase-4.md`) |
| #615's class | spec.md: the three silent-set statements; the id count's direction was also written *as many rows* in four more places, which reads as the equality the new case kills | the four say *at least as many* | the new case pins `>=`, so a sentence reading as `==` states the mutation (`phases/phase-5.md`) |
| #612's class | spec.md's table listed `unverified_check.py`'s module docstring paragraph; its bold heading *not the ref's tip* was false in CI too | the heading reads *not the ref* | the merge base IS the ref's tip in CI (`phases/phase-3.md`) |
| #616's pins | spec.md: the round's defined-`CD` case and the reader needle; `templates/config.md` now also states the substring bound, a person-read line | a third row in the variable case pins the bound | contract §14: a changed sentence a person acts on is pinned in the same commit (`phases/phase-6.md`) |
| `docs/release-checklist.md` in the documents case (#612) | spec.md: the case *gains a second assertion per file*, and also lists the checklist as *Out*, true at both places | the checklist row carries no tip phrase | spec.md §*Out of scope*: its sentence is true on a branch checkout and at the merge ref, so it names neither place and is not edited |

## Not verified

| Item | Who must answer |
|---|---|
| where `cmd.exe` resumes scanning after an undefined `%NAME%`, and whether `broad_gate.py#as_cmd_expands` agrees; the docstring says it is not modelled and claims nothing either way (`questions.md` Q2) | a Windows run of `cmd.exe` — whoever next changes the broad gate's `cmd.exe` path (#616's *Who acts*) |

## Not done

- **S4 is not pinned as silent** (#615): a row whose id lost its sibling
  and whose every anchor was renamed goes silent, and a case asserting exit
  0 would lock that gap in. spec.md's *Out* holds the grounds.
- **No new case for #613**: a docstring is outside contract §14's list, and
  the rule's behaviour is held by the draft and ready cases.
- **No Windows-only case for where `cmd.exe` resumes after an undefined
  name** (#616): its first run would be at the pull request, unattended,
  for a question the docstring leaves open truthfully (plan.md's
  Alternatives). The *Not verified* row above names who answers it.

## Fed back into the spec

none
