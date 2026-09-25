# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — review round 2

| Field | Value |
|---|---|
| Target SHA | e36888e3383bbde779d07ebaa134ed10f7b7550e |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 608 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `e58b62d3d32459ebf99fac349edebb390edc8be6..bc6f4a4ce62c2a18074a6e97a3976fd27072d408`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, the ninth copy of the `Pass`-beside-`nobody` rule in `agents/smith.md` that still says it fails the pull request at every stage |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790297083 is the verifying round over round 1's fixes (1f21376f..8decc62c) at e36888e3. For each round-1 verdict closed as fixed or answered, it asks whether it is actually closed. For 🟡 1 in particular, it asks whether each of the eight copies the fix pass widened to says what chain_check.checked_by does, and whether a ninth copy stands in a shipped document or message that the widening missed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the ninth copy of the `Pass`-beside-`nobody` rule says the pair fails the pull request with no draft exception; round 1's 🟡 1 class, missed by the widening | `agents/smith.md:301` | **fixed** `bc6f4a4ce62c2a18074a6e97a3976fd27072d408` | fixed at bc6f4a4ce62c2a18074a6e97a3976fd27072d408; read. Contradicts `checked_by`'s `strict` branch and the eight fixed copies. Worded differently, so survivor-check could not match it. Found by the enumerating grep (executed) |
| ⬜ 2 | `seal`'s refusal says the orchestration document fails a pull request, without "ready" | `skills/code-review/scripts/round_record.py:4496` | **fixed** `bc6f4a4ce62c2a18074a6e97a3976fd27072d408` | fixed at bc6f4a4ce62c2a18074a6e97a3976fd27072d408; read. The refusal and its instruction are right in either state, so ⬜. A change needs a pin (§14) |
| 🟢 | round 1's 🟡 1: the eight copies it names or widened to now match the code | `README.md:213`, `README.md:610`, `README.ko.md:210`, `README.ko.md:605`, `skills/code-review/orchestration.md:295`, `skills/implement/orchestration.md:547`, `agents/sealer.md:113`, `templates/sdd-round.md:119` | verified | read, each against `chain_check.checked_by`'s `strict` branch. Executed: 14 draft and `nobody` cases passed. The class stays open through 🟡 1 of this round |
| 🟢 | round 1's ⬜ 2 is closed: the handoff protocol names the restored record | `docs/review-handoff-protocol.md:190` | verified | read |
| 🟢 | round 1's ⬜ 3 is closed: the `written_late` qualifier is the true one | `skills/code-review/scripts/chain_check.py#written_late` | verified | read, the early return on empty `commissioned_fixes` precedes `restored_from` |
| 🟢 | round 1's ⬜ 4 is answered in spec.md and the review-chain spec row, and the code matches | `docs/review-chain-spec.md` restoration row | answered | read. The code has no touched-check before `restored_from`. Round 1's probe 3 Q2 carried, not re-run |
| 🟢 | round 1's ⬜ 5 is closed: the changelog counts shapes | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md:1` | verified | read |

## Paste-ready fixes

```
last fixes nobody opened. That pair, `nobody` beside a checked `Pass` on the
last record, **fails a ready pull request** for any work item begun after the
rule landed. On a draft it prints and names the verifying round, and *Ready
for review* re-runs the check. The way out is the verifying round above,
which costs no round.
```
```
**Re-read 2026-09-25 by work item 1790297083's round 2 fix pass (#598).** One sentence of `## Phases` gained the draft half of the `Pass`-beside-`nobody` rule. Nothing this row claims moved, so the claim holds.
```
```
            "`skills/code-review/orchestration.md` fails a ready pull request "
            f"whose last record reads `{chain.NOBODY}` beside a checked "
            "`Pass`. "
```
```
    assert "fails a ready pull request" in out, out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_last_rounds_fixes_are_checked.py -k "draft or nobody"` at `e36888e3`, in the round's clone | 14 passed, exit 0 |
| `evidence_check.py .` at `e36888e3`, in the round's clone | exit 0; every ledger file reports 0 drifted and 0 broken |
| `git grep` over every tracked file outside `tests/`, `CHANGELOG.md` and `seal/` for the rule's wording, English and Korean, then each hit read in context | nine copies state the rule without leaning on a nearby full statement. Eight are correct and one (`agents/smith.md:301`) is 🟡 1. A message copy is ⬜ 2 |
| `git grep` of the ledger for anchors into `agents/smith.md` | four rows at `#"## Phases"@12c56e52`, which 🟡 1's fix drifts |
| the broad gate: full suite, lint, typecheck | not yet. The sealer's, once, after the rounds settle; this round ran none of it |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
