# the-settings-live-in-a-file-nobody-opens — review round 2

<!-- The verifying round for round 1's fixes (target: the diff
9a28262..2b9f43b), reviewed with #106 on one branch. Both of round 1's
findings were closed at their coordinates and both fixes were still
satisfiable with the claim false. Round 3 verifies. Written by the review
orchestrator, which implemented this work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from 9a28262, reviewed at 2b9f43b |
| PR | none yet |
| Broad gate | not yet — round 3 verifies these fixes |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none — two assertions replaced |
| Needs a fix | yes — 🟡 5 (the move assertion no longer detects a move), 🟡 6 (the absent-rows assertion survives its own negation) |

- [x] Pass

## What this round was asked to attack

Whether round 1's two replacements are still satisfiable with the claim false,
mutated in ways round 1 did not use.

## The answer, and it is the shape worth keeping

**A presence assertion cannot see an addition.** Round 1 found
`assert "mv " not in text` blind to a `cp -a` rewrite and replaced it with
`assert "Do not do any of that by hand" in text`. That answers a different
question: appending a paragraph telling the session to move the root another
way leaves the prohibition sitting there, present and true, while the file now
contains a move.

The class: **every claim of the form *the file does not grow X* needs an
absence half.** A presence assertion pins what the file says; only an absence
assertion pins what it does not.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🟡 8 | two assertions satisfied by words the file had for another reason | `tests/…` | answered at the coordinates, and both replacements are this round's findings | reviewer ran six mutations |
| r1 🟡 9 | the template-copy branch could not fire | `skills/config/SKILL.md` | answered — reproduced | reviewer read the stub `seal mode` writes |
| 🟡 5 | the presence assertion cannot see a move added elsewhere: a `cp -a` paragraph left it green, and so did re-scoping the prohibition to `…by hand when editing a language row`, which keeps the substring and guts the rule | `tests/test_the_settings_have_a_front_door.py` | fixed at adc3b9d — an absence half over five spellings of a move, and the prohibition pinned with its full stop | reviewer executed both mutations; the orchestrator reproduced each and confirmed both now redden |
| 🟡 6 | `"including the ones the file does not carry"` is a fragment, so `never including…` leaves it green with the instruction inverted | `tests/…` | fixed at adc3b9d — the whole clause with its polarity | reviewer executed the inversion |
| 🟢 7 | the skill spells no move of its own and `seal mode`'s output matches what it describes | — | pass | reviewer ran the whole sequence in a scratch repository |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: six mutations of `skills/config/SKILL.md` | two red, four green — 🟡 5 and 🟡 6 |
| orchestrator: a `cp -a` paragraph, the re-scoped prohibition, the inverted instruction | each reddens its own case |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | 1642 passed · 1 skipped; clean; 455 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `tests/test_the_settings_have_a_front_door.py`'s two assertions | replaced in both rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the bootstrap should route its questions through this skill | `questions.md` Q2 | the repository owner |
