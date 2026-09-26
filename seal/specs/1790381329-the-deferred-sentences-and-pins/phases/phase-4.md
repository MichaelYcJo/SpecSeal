# 1790381329-the-deferred-sentences-and-pins — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | de59906b |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#613. The round's paste-ready lines in `chain_check.py#fix_surface`'s
docstring, adding *at a ready pull request* to the `nobody` refusal on the
last record. Enumerate first for twins that state the check's timing without
that qualifier. Re-read each `@dd0a5d68` row against the edit and re-stamp it
in its release file with a dated note; no new case, because a docstring is
outside contract §14's list.

## What this phase found

- **The frame missed one twin: `round_record.py#landing_values`.** Its
  docstring says *the check refuses `Pass` beside `nobody` there* of a capped
  run's last record, with no timing. That is a statement of when the check
  refuses, the same as `fix_surface`'s, so it gains *at a ready pull
  request* in the same phase. Three 0.8.1/0.10.0/0.11.4 rows anchor it and
  were re-read.
- **The enumeration and its judgments.** Searched at the build tip over
  `docs/ skills/ agents/ templates/ hooks/ .github/ README.md README.ko.md
  CONTRIBUTING.md`: *beside a checked `Pass`*, *refuses it on the LAST*,
  *fails beside*, *carrying `nobody`*, *`nobody` beside*, *beside `nobody`*,
  *`Pass` beside*, *`Pass` 가 체크*, *`Pass` 옆*, *`nobody` 옆*, and any line
  pairing `nobody` and `Pass` with *fail*, *refus*, *red*, *거부* or *실패*.
  Beyond the two fixed:
  - already say *a ready pull request*: `docs/round-record-spec.md:46,63,584`,
    `docs/review-chain-spec.md:314,638,908`, `chain_check.py:124,152`,
    `skills/code-review/orchestration.md:295,520`,
    `skills/implement/orchestration.md:547`, `agents/smith.md:301`,
    `README.md:611`, `README.ko.md:211,606`.
  - not a statement of the check's timing: `docs/round-record-spec.md:96`
    and `docs/review-handoff-protocol.md:274` (the frame's grounds hold);
    `chain_check.py:2206` (says what makes the refusal reachable, and the
    next paragraph states the draft half); `chain_check.py:519,2172`
    (name the refusal).
  - a different pair: `docs/round-record-spec.md:62,906`,
    `chain_check.py:1215,2292`, `templates/sdd-round.md:258` (`Pass` beside
    an open 🔴, which fails at every stage).
- **The count.** Seven rows anchor `fix_surface@dd0a5d68` (0.4.0 ×3, 0.8.0
  ×3, 0.15.0 ×1), as the frame said; three more anchor `landing_values`.
  None of the ten claims quotes the edited sentence, so each got a dated
  `Re-read` note and a re-stamp, and none a correction.
- **Seen red.** No new case: the rule's behaviour is held by the draft and
  ready cases in `tests/test_the_last_rounds_fixes_are_checked.py` and
  `tests/test_chain_check_at_the_pull_request.py`, which this phase leaves
  green.
- **Verified by (executed, 2026-09-26):** `tests/test_chain_check_at_the_pull_request.py`,
  `tests/test_the_last_rounds_fixes_are_checked.py`,
  `tests/test_the_fixes_close_the_record.py` and
  `tests/test_the_rules_have_one_owner.py`, 386 passed. `evidence-check .`
  after the re-stamps: 0 drifted, 0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
