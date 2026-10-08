# 1791384154-a-records-finding-closes-once-at-the-runs-end — review round 2

| Field | Value |
|---|---|
| Target SHA | 636beccedfadcecd610732e920ac7d9a796c6ba7 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 879 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `be3c452aa09d6934f057337151bf63201702953b..b0e52bb2111c338140026742a58544728d9dc592`, 2 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | first — 🟡 1 at skills/code-review/scripts/chain_check.py#NOTES_FROM, a unit round-1's fixes changed |
| Needs a fix | yes — 🟡 1 (the cutoff holds for the batch, not for a 0.21.0 work item framed after it) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: e10a7c35..38696bb0, plus the fix table at e03b8a54 and the close at 636becce, which was written with the installed 0.20.0 round_record.py. The job was the answers to round 1's eight verdicts. Round 1's three new units were a finding surface. The spawn also named the smith's flag that 🟡 3's fix may add a rule in a fix pass. It also asked whether NOTES_FROM and the new arms turn #858's or #864's merged records red once this branch lands; the reviewer ran this branch's chain-check over a clone with the release branch merged in. Facts arrived labelled. Read from the smith: the rider re-measured, the cutoff moved past the batch, 1,241 passed and 9 mutations red. Read: the release branch holds #858 and #864.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The cutoff's premise, that the first records held to it are written under the rule, is false for any 0.21.0 work item framed after the batch: its id passes 1791384163 while its rounds run under 0.20.0's `close`, which admits a ⬜ closed `fixed`; round 1's finding 2 is closed for #858 and #864 only | `skills/code-review/scripts/chain_check.py:863` | **fixed** `23f22eb4` | fixed at 23f22eb4 — the value stays `1791384163`, right for the release the owner scoped on 2026-10-08 (the eleven framed items plus #834's build, all below it); `NOTES_FROM`'s comment, the owner file's sentence, the test's constant and the ledger's N2 now say what it assumes — no item of that release framed after the batch — and that whoever frames one moves the cutoff past its own id in the same change. The far-future value was not taken: it would switch the rule off for every item framed after the release ships, which is the case the rule is for; executed: `date +%s` is 1791432483; the merged clone shows #858 and #864 closed five ⬜ rows `fixed` between them under 0.20.0. Read: milestone 0.21.0 has about ten open issues with no work item |
| ⬜ 2 | The changelog fragment says every 0.21.0 work item is before the cutoff and prints | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/changelog.md:21` | answered | corrected at `23f22eb4` — the changelog fragment names the eleven items framed with this one as before the cutoff, and says a later one moves it; read; false for the first item framed from the open milestone |
| ⬜ 3 | A carried confirmation in round 1's record quotes a blocking glyph in its Finding cell, so the `release` check fails at 636becce now that `close` ticked `Pass` | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/rounds/round-1.md:36` | answered | cleared by round-2.md being the last record, as the finding says: at `b0e52bb2`, executed, `chain_check.py --baseline origin/release/v0.21.0` names nothing on round-1.md, judged ready or draft (draft exit 0); no edit taken; executed: this branch's `chain_check.py` errors on line 36 as draft and as ready. Read: CI `release` fails on the same line; it clears when round-2.md is the last record |
| 🟢 | round 1's blocking finding is closed — the rider on smith's Phases section is re-measured and re-stamped | `agents/smith.md:87` | confirmed | executed: rider module passes; a probe gives 1, 1 and True at `5623d728` and at HEAD. Read: CI rider cases pass |
| 🟢 | round 1's finding 2 is closed for the merged siblings — #858 and #864 print and do not fail | `skills/code-review/scripts/chain_check.py:863` | confirmed | executed: chain-check over the merge, baselines `release/v0.21.0` and `main`; five notices, no sibling error. The class is finding 1 of this round |
| 🟢 | round 1's finding 3 is closed — `new` refuses the redesign's first record over the stopped run's open note | `skills/code-review/scripts/round_record.py:2626` | confirmed | executed: the case is red with the refusal disabled and green restored. Read: not the mechanism the fix-pass section refuses (see the prose) |
| 🟢 | round 1's finding 4 is closed — the policy sends a record-located note to `notes` and never to a fix word | `docs/review-chain-spec.md:246` | confirmed | read; executed: the line-wrap module passes |
| 🟢 | round 1's finding 5 is closed — the five `notes` refusals are pinned | `tests/test_a_note_closes_once_at_the_runs_end.py:644` | confirmed | executed: each of five sentence mutations red, restored green |
| 🟢 | round 1's finding 6 is closed — `Corrected · S10` and `Corrected · S13` replace the re-reads | `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:19` | confirmed | read; CI `ledger` passes |
| 🟢 | round 1's finding 7 is closed — warden.md excepts a carried note from the answer every earlier finding needs | `agents/warden.md:348` | confirmed | read |
| 🟢 | round 1's finding 8 is closed — the owner file and the policy both read *a ⬜ like any other* | `skills/code-review/orchestration.md:196` | confirmed | read |
| 🟢 | round 1's new units read correctly and pin what they claim | `tests/test_a_note_closes_once_at_the_runs_end.py:566` | confirmed | read; executed: both new cases red under mutation |
| ❓ | The merge with #860 and #866, which edit `close` and `chain_check.py` beside these lines | `skills/code-review/scripts/round_record.py:4401` | ❓ out of verified scope | neither is in `release/v0.21.0` yet; the orchestrator answers it when it integrates them |

## Paste-ready fixes

```python
# Where a note closed on a fix word becomes an error, as the unix second in a
# work item's directory name. NOT the id of the work item that added the rule,
# which is what the other cutoffs use: every work item framed before the
# release that ships this rule is installed runs its rounds under the
# installed 0.20.0 `close`, which demands a fix-table row for a ⬜ and admits
# `fixed` -- #858's round 1 closed three that way and #864's two. That moment
# is the release's tag, which no id known today names, so the cutoff is held
# past anything this release can frame (round 2's 🟡 1 of #837). The
# reasoning is otherwise `STRICT_FROM`'s. Measured 2026-10-07: 35 ⬜ rows of
# 14 committed records closed `fixed` before it, and they print.
NOTES_FROM = 1798761600
```
```python
# Past anything 0.21.0 can frame: its items run under 0.20.0's `close`
# (round 2's 🟡 1 of #837).
AT_THE_CUTOFF = "seal/specs/1798761600-an-item-under-the-rule"
BEFORE_THE_CUTOFF = "seal/specs/1798761599-an-item-before-the-rule"
```
```
word is an error for a work item begun at or after `1798761600` — past
anything the release that ships the rule can frame, since every item framed
before it is installed runs its rounds under the previous `close` — and a
notice before it, and a ⬜ still open on a record of the run is an error at a
ready pull request and a notice on a draft.
```
```
  an open note and, for a work item begun at or after `1798761600`, over a
  note closed `fixed` — every work item framed before this release is
  installed is before that and prints. A record whose only open rows are notes now reads
```
```
| 🟢 | The landing leaves only open notes out: an open blocking or should-fix finding still holds `nobody`, and `Pass` is derived from every word | `skills/code-review/scripts/round_record.py:2595` | confirmed | read: `build` and `close` filter by `carried_ids`, which takes only `note_rows`' open notes |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight modules the spawn named, in the clone at 636becce | 435 passed, exit 0 |
| this branch's `chain_check.py --baseline origin/release/v0.21.0` at 636becce, draft and ready event payloads | exit 1 both; the error is round-1.md:36; ready adds `Broad gate` and `Pass` beside `nobody` |
| a probe merge of `origin/release/v0.21.0` (d712a632) into 636becce, then `chain_check.py` with baseline `release/v0.21.0` (draft, ready) and `main` (ready) | exit 1 each, on this item's three errors only; #858's ⬜ 6–8 and #864's ⬜ 3–4 closed `fixed` print as notices |
| a probe re-measuring the rider: `commit_invocations` over line 77 alone and with everything above, and `_hides_a_commit` over the file, at `5623d728` and HEAD | 1, 1, True at both |
| a probe changing each of the five `notes` refusal sentences, then disabling the redesign refusal, each followed by its case | all six red (exit 1); both cases green after restore |
| `gh pr checks 879`, read and not run by this round | at 636becce: every pytest leg, lint, ledger and arm-check-grammar pass; `release` fails on round-1.md:36 |
| work-item ids across every fetched branch and pull-request head | highest is 1791384162; none at or above 1791384163 |
| the full suite, repository-wide lint and typecheck (the sealer's broad gate) | not yet: no run has happened at any SHA of this branch. The sealer answers it after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `agents/smith.md:87` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:856` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:4855` | round 1's 🟡 3 — fixed |
| round-1 | `docs/review-chain-spec.md:246` | round 1's 🟡 4 — fixed |
| round-1 | `tests/test_a_note_closes_once_at_the_runs_end.py:450` | round 1's 🟡 5 — fixed |
| round-1 | `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:17` | round 1's ⬜ 6 — answered |
| round-1 | `agents/warden.md:348` | round 1's ⬜ 7 — answered |
| round-1 | `skills/code-review/orchestration.md:196` | round 1's ⬜ 8 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:2595` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py:4610` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py:3867` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py:4401` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
