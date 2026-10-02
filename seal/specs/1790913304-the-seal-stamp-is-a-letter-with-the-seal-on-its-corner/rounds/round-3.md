# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — review round 3

| Field | Value |
|---|---|
| Target SHA | 2fe8af6ef9a9d068d9e18f6957e878b434c4978f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 719 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `2fe8af6ef9a9d068d9e18f6957e878b434c4978f..2fe8af6ef9a9d068d9e18f6957e878b434c4978f`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is the run's last round, a verifying round at `2fe8af6e` over round 2's fix range `0bef982a..483c3770`. Round 2's `New units` reads none, so the round opened no fresh finding surface. For each of round 2's five ⬜ verdicts it was asked whether the cited commit closes it: 6 at `81e4730f`, 7 at `ea36c24f`, 8 at `2988a974`, 9 at `efe1c949`, and 10, answered as a correction to the ledger at `483c3770`. It re-ran the mutations that had survived round 2, against the new cases and against the cases at `0bef982a`. It measured the gate-failure report over every gate pair, and end to end through `hooks/dispatch.py` with two gates failing on text outside the BMP. It was told not to run `claude -p` or write a settings file, and to run only the touched test modules.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 6 is closed — the A3 case holds each turn's labels to exactly the files it claimed | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:583` | confirmed | Executed: the hook claiming every ready file turns the case red, and the case from `0bef982a` stays green under it |
| 🟢 | round 2's finding 7 is closed — oldest-first carrying and a single seal exactly at the budget are pinned | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:689` | confirmed | Executed: the floor's `break` to `continue` and `>` to `>=` each turn the ladder case red, and the case from `0bef982a` stays green under both |
| 🟢 | round 2's finding 8 is closed — `first_line` cuts at 200 UTF-16 units, so two gates write 909 whatever their text | `hooks/dispatch.py:319` | confirmed | Executed: every gate pair gives 909 and three gates 1,274, ASCII and U+1D54F alike, against 1,309 under the old cut; end to end 870 against 1,270; four mutations red, the equivalent `break` survives |
| 🟢 | round 2's finding 9 is closed — `admitted`'s docstring no longer names a scale below 0.75 | `skills/verify/scripts/seal_stamp.py:630` | confirmed | Read: `check_scale` in `drawings` refuses it first; finding 11 is the reflow's long line |
| 🟢 | round 2's finding 10 is closed — ledger B1 and B2 say what the code does, re-stamped | `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` | confirmed | Read; executed: `bin/evidence-check .` 3,521 ok, 0 drifted, 0 broken |
| ⬜ 11 | one line of `admitted`'s reflowed docstring is 113 columns, where the rest wraps under 80 | `skills/verify/scripts/seal_stamp.py:632` | deferred #721 | #721 — a rewrap in a unit this run created; does not block, and a fix would cost a verifying round the capped run has not got; Read: no check reads docstring width (`E501` is not selected); does not block, and is the branch's under the cap rule if fixed |
| ❓ | whether the harness counts a character outside the BMP as two UTF-16 units | `skills/verify/scripts/seal_stamp.py:213` | ❓ out of verified scope | Measured by round 1's fix pass with `claude -p`, which this round was told not to run; carried from round 2; the orchestrator answers it |

## Paste-ready fixes

```python
    The owner's rule of 2026-10-02 (`questions.md` Q6), which replaced one
    rung for the whole message: a seal keeps its disc rather than share a
    message without it. So the message carries as many of the oldest blocks
    as fit together WITH the disc, each at 0.75 — a scale below it is
    refused before a block reaches here — and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. The blocks past
    those are not drawn here; the hook leaves their files pending, and the
    next `Stop` draws them whole.
```

## Executed probes

| What was run | Result |
|---|---|
| pytest with `-n auto` over the three modules the fix range touched (stamp, sealer, gate failure), in the clone, with the main checkout's `.venv` | 329 passed, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone; then `--ledger` on the work item's fragment | `total: 3521 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow`, exit 0; the fragment 65 ok |
| `dispatch.describe` over every gate, every group it is in and both phases, with `first_line` of 500 ASCII and of 500 U+1D54F; the report for one, two and three gates, separator included | as fixed: 533 · 909 · 1,274 with `ModuleNotFoundError`, 539 · 921 · 1,292 with `PendingDeprecationWarning`, both texts alike; the code-point cut over U+1D54F: 733 · 1,309 · 1,874 and 739 · 1,321 · 1,892 |
| `hooks/dispatch.py pre-agent` with `worktree-guard.py` and `implementer-mark.py` raising U+1D54F text at load, then `hooks/dispatch.py stop` over one values file | two records written; the report 870 units with separator, the message 7,386; under the old cut the report 1,270, which beside `MESSAGE_BUDGET` is 10,270, past the limit |
| Eight mutations, each against the fix range's case for it | hook claims every ready file: A3 case red · floor `break` to `continue`: ladder case red · floor `>=`: ladder case red · every character one unit: cap case red · `>= 0xFFFF`: red · `units >= MESSAGE_CAP`: red · the old code-point cut: red · `first_line`'s `break` to `continue`: green, equivalent |
| The same eight against the cases at `0bef982a` | all green, so the fix range's new lines are what turn each one red |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/seal_stamp.py:647` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:643` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:229` | round 1's ⬜ 3 — answered |
| round-1 | `skills/verify/scripts/seal_stamp.py:548` | round 1's ⬜ 4 — deferred |
| round-1 | `skills/verify/scripts/seal_stamp.py:584` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2557` | round 1's 🟢 — confirmed |
| round-1 | `hooks/sealer-stamp.py:125` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:520` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:154` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.15.7.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:220` | round 1's ❓ — out of verified scope |
| round-2 | `hooks/sealer-stamp.py:142` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:619` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:227` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:469` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:593` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:658` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/seal_stamp.py:651` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:577` | round 2's ⬜ 6 — fixed |
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:679` | round 2's ⬜ 7 — fixed |
| round-2 | `skills/verify/scripts/seal_stamp.py:627` | round 2's ⬜ 9 — fixed |
| round-2 | `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` | round 2's ⬜ 10 — answered |
| round-2 | `skills/verify/scripts/seal_stamp.py:213` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 11 — one line of `admitted`'s reflowed docstring is 113 columns | #721 | the owner, through the issue |
| `record` writes an exception's type name uncapped, so a type name from outside the plugin longer than about 30 characters can pass the reserve with two gates (predates #717; the plugin's own longest is 28) | #722 | the owner, through the issue |
