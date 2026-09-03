# the-settings-live-in-a-file-nobody-opens — review round 4

<!-- The verifying round for round 3's fixes (target: the diff
adc3b9d..133ddf3). Nothing needing a fix, which closes the run. Written by the
review orchestrator, which implemented this work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from adc3b9d, reviewed at 133ddf3 |
| PR | none yet |
| Broad gate | a73de50 against `origin/release/v0.5.0`: `pytest tests/ -q -n auto` 1647 passed · 1 skipped; `ruff check .` clean; `ruff format --check .` 85 files; `evidence_check.py --strict .` 455 ok · 0 drifted · 0 broken; `unverified_check.py --baseline` exit 0 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |

- [x] Pass

## What this round was asked to attack

The same question a fourth time — **did this fix derive one level and leave
the next by hand?** — with four places named: every module-level string
either checker matches against a record, against the derivation; whether
round 3's three-unreachable claim holds or the patterns are built from
constants; whether any other message in `chain_check.py` spells a constant by
hand; whether the twelve move spellings are honestly described and whether
any fires on ordinary prose; and whether the two backticked emoji read
consistently elsewhere.

## The answer

Nothing to open. The twelve move spellings are honestly described — the
comment says the check is an enumeration rather than a closure, which is the
true statement about a list of strings against a class of behaviours — and
none of the twelve fires on this skill's own prose. `ditto ` is the only one
that is also an ordinary English word, and it appears in no shipped document.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r3 🟡 2 | five spellings let two moves through | `tests/…` | answered — reproduced. Twelve now, and the two that walked past are caught | reviewer ran all twelve against the skill and a near-miss scan: none hit |
| 🟢 1 | the comment's honesty about what the case buys | `tests/test_the_settings_have_a_front_door.py:76-90` | pass — *what it does not buy is proof that none did* states the limit rather than hiding it | reviewer read |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: twelve move spellings against `skills/config/SKILL.md`, plus a near-miss scan | none hit, none near |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | see the Broad gate row |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–3 | `tests/test_the_settings_have_a_front_door.py`'s two assertions | replaced in every round; closed here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| No enumeration of strings closes the move class | round 3's record, and the comment in the case | the repository owner |
| Whether the bootstrap should route its questions through this skill | `questions.md` Q2 | the repository owner |
