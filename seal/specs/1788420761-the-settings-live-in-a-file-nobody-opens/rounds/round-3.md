# the-settings-live-in-a-file-nobody-opens — review round 3

<!-- The verifying round for round 2's fixes (target: the diff
2b9f43b..adc3b9d). The absence half arrived and was a subset. Round 4
verifies. Written by the review orchestrator, which implemented this work
item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from 2b9f43b, reviewed at adc3b9d |
| PR | none yet |
| Broad gate | not yet — round 4 verifies these fixes |
| Fixes checked by | round-4 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 2 (five spellings of a move let two through) |

- [x] Pass

## What this round was asked to attack

One question: **round 2 found a fix deriving one level and leaving the next by
hand. Did this fix do it again?** Then five places — `VERDICT_COLUMN` as a
real contract change in a checker; whether `ROUND_RECORD_FIELDS` is itself
hand-written and checked against anything; whether any literal's backticked
form is a substring of another; a sixth way the skill could grow a move; and
whether case-folding the strip introduces a false positive.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 🟡 5 | the presence assertion could not see an addition | `tests/…` | answered — the absence half is there, and it is a subset, which is 🟡 2 | reviewer inserted six moves: four caught, two through |
| r2 🟡 6 | the fragment survived its own negation | `tests/…` | answered — reproduced | reviewer inverted the instruction: red |
| 🟡 2 | the five spellings let `cp -r` and `shutil.copytree` through, while the failure message reads *the skill spells a move of its own* — a general claim over a specific check, which invites the next reader to believe the class is closed | `tests/test_the_settings_have_a_front_door.py` | fixed at 133ddf3 — twelve spellings, and a comment saying it is an enumeration rather than a closure | reviewer executed both; orchestrator reproduced three and confirmed each reddens |
| 🟢 3 | the skill still spells no move of its own | — | pass | reviewer read |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: six moves inserted into the skill | `cp -r` and `shutil.copytree` green, four red |
| orchestrator: `cp -r`, `shutil.copytree` and `os.rename` inserted | each reddens |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | 1647 passed · 1 skipped; clean; 455 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–2 | `tests/test_the_settings_have_a_front_door.py`'s two assertions | replaced in every round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| No enumeration of strings closes the move class | this record, and the comment in the case | the repository owner |
| Whether the bootstrap should route its questions through this skill | `questions.md` Q2 | the repository owner |
