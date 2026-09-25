# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — review round 3

| Field | Value |
|---|---|
| Target SHA | 1aea54ae8068b127fa2d5e5c75d0f8eb2737c295 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 608 |
| Broad gate | 97dc4247 against c4797ae1; earlier run: 76fd4340 against 7b557144 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790297083 is the verifying round after the run's one reopening. It reads round 2's fixes (e58b62d3..bc6f4a4c) and the closing commit's record correction at 1aea54ae, and ends the run whatever it finds. For round 2's two findings and the three places the fix pass widened to, it asks whether each is closed. It searches the rule's wording once more in English and Korean, and reads PR #608's CI at that tip.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `fix_surface`'s docstring says `checked_by` refuses `nobody` beside `Pass` on the last record without "at a ready pull request", while its twin in the round-record spec was widened by the fix pass | `skills/code-review/scripts/chain_check.py:2623` | deferred #613 | read. True at ready, and the module states the draft half at `:123`, `:152` and `:2210`, so no defect ships. Survivor-check does not reach it (executed). Deferred because the run is capped. The branch did not create the unit, and #598 owns the draft/`nobody` state (instance 4) |
| 🟢 | round 2's 🟡 1 is closed — `agents/smith.md` states the draft half | `agents/smith.md:301` | verified | read against `checked_by`'s `strict` branch. The semicolon join keeps the meaning, and `tests/test_a_fix_pass_may_add_a_unit.py` passes (executed) |
| 🟢 | round 2's ⬜ 2 is closed — `seal`'s refusal says "a ready pull request", pinned twice | `skills/code-review/scripts/round_record.py:4496` | verified | read. Executed: both pinning cases pass at the target and fail at the new assertion with the `e58b62d3` message (§15) |
| 🟢 | the widening to the module docstring's cell table is correct | `skills/code-review/scripts/chain_check.py:124` | verified | read against `checked_by` |
| 🟢 | the widening to the round-record spec's fix-surface section is correct | `docs/round-record-spec.md:585` | verified | read |
| 🟢 | the widening to the review-chain spec's floor section is correct | `docs/review-chain-spec.md:315` | verified | read. The other refusal it names reads no `strict`, which matches the unchanged half |
| 🟢 | the seventeen drifted ledger rows are re-read and re-stamped, and the rider is re-stamped | `seal/releases/` (11 files), `agents/smith.md:116` | verified | read, each added row carries the dated note. Executed: `evidence_check.py --strict .` exit 0; rider module 29 passed |
| 🟢 | the record correction in `round-2-report.md` drops a hash that would be stale again after the fix | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/rounds/round-2-report.md:96` | verified | read. The ledger rows now carry `@cede28c2`, so a hash in the report prose would be wrong either way |
| ❓ | PR #608's `pytest (windows-latest, 3.12)` leg at `1aea54ae` | PR #608 checks | ❓ out of verified scope | still pending at this round's last read; the other five legs pass. The orchestrator answers it, from `gh pr checks 608` before the sealer's seal is taken |

## Paste-ready fixes

```
      `checked_by` prints a notice for it on every record and refuses it on
      the LAST record beside a checked `Pass` at a ready pull request. A
      non-terminal record carrying it is false by construction — a later
      record exists, and round N+1 reviews round N's fixes — and nothing
      refuses that today
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_fix_pass_may_add_a_unit.py` and the two `seal` refusal cases of `tests/test_the_seal_is_taken_once_by_the_sealer.py`, at `1aea54ae`, in the round's clone | 11 passed, exit 0 |
| the same two `seal` refusal cases with `round_record.py` replaced by its `e58b62d3` version, then restored | 2 failed, each at `assert "fails a ready pull request" in out`; the clone was clean afterwards |
| `bin/test tests/test_a_rider_reaches_its_file.py` at `1aea54ae` | 29 passed, exit 0 |
| `evidence_check.py --strict .` at `1aea54ae` | exit 0; 0 drifted, 0 refused |
| `survivor-check --range e58b62d3..bc6f4a4c` | exit 0, no removed wording standing. It does not reach ⬜ 1 |
| `git grep` for the rule's English and Korean wordings over every tracked file outside `tests/`, `CHANGELOG.md` and `seal/`, each hit read in context | every copy states the draft half or sits beside a full statement; ⬜ 1 is the one twin the widening left |
| `gh pr checks 608` at `1aea54ae` | lint, ledger, release, pytest ubuntu and pytest macos pass; pytest windows pending |
| `round_record.py new --round 3` over this report, inside the clone | exit 0; the record parsed with every verdict row, `Needs a fix` no, run noted `capped`; the clone was then deleted |
| the broad gate: full suite, lint, typecheck | not yet. It is the sealer's, once, after this round; this round ran none of it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/orchestration.md:295`, `templates/sdd-round.md:119`, `README.md:609` | round 1's 🟡 1 — fixed |
| round-1 | `docs/review-handoff-protocol.md:190` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py#written_late` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md:1` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py#restored_from` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py#added_on_branch` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py#checked_by` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py#run_check` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/orchestration.md:519` | round 1's 🟢 — confirmed |
| round-2 | `agents/smith.md:301` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:4496` | round 2's ⬜ 2 — fixed |
| round-2 | `README.md:213`, `README.md:610`, `README.ko.md:210`, `README.ko.md:605`, `skills/code-review/orchestration.md:295`, `skills/implement/orchestration.md:547`, `agents/sealer.md:113`, `templates/sdd-round.md:119` | round 2's 🟢 — verified |
| round-2 | `docs/review-chain-spec.md` restoration row | round 2's 🟢 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1, `fix_surface`'s docstring twin of the widened spec paragraph | #613, filed with the paste-ready fix below, because #598 closes with this pull request | the orchestrator of this run, who posts the comment before the release closes #598, or files a `from-review` issue instead if the change should outlive that close |
