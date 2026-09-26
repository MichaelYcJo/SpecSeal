# 1790381329-the-deferred-sentences-and-pins — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. Opened at phase 3 and kept as the work goes; closed at phase 7. -->

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
| `docs/release-checklist.md` in the documents case (#612) | spec.md: the case *gains a second assertion per file*, and also lists the checklist as *Out*, true at both places | the checklist row carries no tip phrase | spec.md §*Out of scope*: its sentence is true on a branch checkout and at the merge ref, so it names neither place and is not edited |

## Not verified

| Item | Who must answer |
|---|---|
| where `cmd.exe` resumes scanning after an undefined `%NAME%`, and whether `broad_gate.py#as_cmd_expands` agrees; the docstring says it is not modelled and claims nothing either way (`questions.md` Q2) | a Windows run of `cmd.exe` — whoever next changes the broad gate's `cmd.exe` path (#616's *Who acts*) |

## Not done

nothing yet

## Fed back into the spec

none
