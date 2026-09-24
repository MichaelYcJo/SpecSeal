# 1790260565-a-ledger-row-carries-two-readings-in-one — review round 3

| Field | Value |
|---|---|
| Target SHA | 0eb461fd2f3e8510680d793b0b6b3dca9e81fa4f |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 588 |
| Broad gate | e4d44f65 against c52e8350 |
| Fixes checked by | no fixes to check |
| Fix range | `9d314d65201f640b1b1273472135dcc6b4d7b3f8..9d314d65201f640b1b1273472135dcc6b4d7b3f8`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790260565 is the last, verifying round: the diff of round 2's fixes, 8eb70840..4a3e4635, at 0eb461fd. Round 2 closed on a fix and spent the one reopening, so this record ends the run. Its job is whether round 2's three verdicts are closed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's ⬜ 1 is closed — `CONTRIBUTING.md`'s re-stamp needle holds the act as well as the premise | `tests/test_a_merge_cannot_silently_drop_a_correction.py:754` | confirmed | Executed: needle count 1, whitespace collapsed; act deleted with premise kept → guides' case 1 failed, needle named; premise deleted → 1 failed; restored → guides' and owner's cases pass |
| 🟢 | round 2's ⬜ 2 is closed — E1 anchors `EDIT_OUTCOMES` at the final unit's hash | `seal/releases/0.15.1.md` | verified | Executed: `evidence-check` over the release file and the fragment 201 ok, 0 drifted, 0 broken; hash set to `00000000` → DRIFTED on `EDIT_OUTCOMES`. Read: 135efd8a follows d7320980 |
| 🟢 | round 2's ⬜ 3 is closed — E1's and E2's newest notes cite commit 950db9ef's message and `rounds/round-2.md` | `seal/releases/0.15.1.md` | confirmed | Read: 950db9ef's message records the red runs; round 2's first probe row records the thirteen deletions; neither note cites `rounds/round-1.md` any more |
| 🟢 | the fix range creates no new unit, as round 2's `New units` row says | `tests/test_a_merge_cannot_silently_drop_a_correction.py:747` | confirmed | Read: d7320980 edits one string of an existing entry; 135efd8a and 4a3e4635 edit ledger rows |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| A probe named with the test_tmp prefix, run once in the clone and deleted: the widened `CONTRIBUTING.md` needle counted, whitespace collapsed | 1 |
| The same probe: `evidence-check --reverify .` and its line break deleted from `CONTRIBUTING.md`, premise kept, then the guides' case | 1 failed, the widened needle named; file restored |
| The same probe: the premise *the claim still holds and you have re-read it* deleted, act kept, then the guides' case | 1 failed, the widened needle named; file restored |
| The same probe: the guides' case and the owner's case on the restored tree | 1 passed each; `git status` in the clone empty |
| The same probe: E1's `EDIT_OUTCOMES@69099dff` set to `@00000000`, then `bin/evidence-check --ledger seal/releases/0.15.1.md .` | exit 1, `EDIT_OUTCOMES` DRIFTED; file restored |
| `bin/evidence-check --ledger seal/releases/0.15.1.md --ledger` the work item's fragment `.` | 201 ok, 0 drifted, 0 broken, exit 0 |
| `bin/evidence-check .` | exit 0 |
| `bin/correction-check --range 8eb70840...0eb461fd` | exit 0: no merge commit in the range |
| `bin/test -q -p no:xdist tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py` | 108 passed, exit 0 |
| The broad gate: full suite, lint and format over the finished branch | not yet: it has not been run, and it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | round 1's ⬜ 1 — fixed |
| round-1 | `tests/test_release_hygiene.py:1296` | round 1's ⬜ 2 — fixed |
| round-1 | `tests/test_release_hygiene.py:1255` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` | round 1's ⬜ 4 — answered |
| round-1 | `seal/releases/0.9.2.md:31`, `seal/releases/0.8.2.md:145`, `seal/releases/0.9.3.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.2.md:31` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_release_hygiene.py:1233` | round 1's 🟢 — confirmed |
| round-1 | `docs/round-record-spec.md:542` | round 1's 🟢 — confirmed |
| round-1 | `seal/` | round 1's 🟢 — confirmed |
| round-2 | `tests/test_a_merge_cannot_silently_drop_a_correction.py:754` | round 2's ⬜ 1 — fixed |
| round-2 | `seal/releases/0.15.1.md` | round 2's ⬜ 2 — answered |
| round-2 | `CLAUDE.md` | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.15.1.md`, `seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
