# 1791384154-a-records-finding-closes-once-at-the-runs-end — review round 3

| Field | Value |
|---|---|
| Target SHA | fe3480d26d257d521e40b0aeb86e2159fee9192a |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 879 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 3 of round 2's fixes: be3c452a..b0e52bb2 (23f22eb4, wording only with the value NOTES_FROM = 1791384163 kept; b0e52bb2, two survivors rows), plus f8f8b85a and the close at fe3480d2. It was announced as the run's last record. The job was the answers to round 2's three verdicts. The spawn asked three things: whether the five carriers state the same assumption truly and nothing wider; whether the two survivors are true where they stand; and whether ⬜ 3's answer holds under the PR's release job. Facts arrived labelled. Read by the orchestrator: the owner's scope answer 7. Read from the smith: the five carriers, survivor-check and chain-check at exit 0, 553 passed, and rider_check and evidence-check.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `NOTES_FROM`'s comment says the owner fixed the release's scope at the batch; the owner's answer 7 declined to split the release, the release also carries #834's build (1791382684, before the batch), and #871 to #874 sit unframed in its milestone | `skills/code-review/scripts/chain_check.py:861` | open | read: the #834 handoff, answer 7 and question 7; executed: the milestone holds 26 open issues. The value and the assumption are right; only the grounds overstate |
| ⬜ 2 | PR #879's body names the cutoff `1791384154`, which round 1 moved, and calls this review the first run under the new rule | `PR #879 body:19` | open | read: `gh pr view 879`; executed: the squash message is COMMIT_MESSAGES, so the body does not reach git history. A GitHub write, the orchestrator's |
| ⬜ 3 | `overview.md`'s *Not verified* row hands the real-run check to this item's own rounds, which all closed with the installed 0.20.0 generator | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/overview.md:29` | open | read: `round-2-fixes.md` carries rows for two notes, which this branch's `close` refuses; a correction, not counted by `Needs a fix` |
| 🟢 | round 2's should-fix finding 1 is closed — the five carriers state one assumption, no item of the release framed after the batch, and one remedy, and none says more | `skills/code-review/scripts/chain_check.py:868` | confirmed | read: the five side by side; executed: no work-item id at or past 1791384163 in any local ref, #860's reframe keeps 1791384160, and the siblings' fix-word notes are three and two |
| 🟢 | round 2's note 2 is closed — the changelog names the eleven items and what moves the cutoff | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/changelog.md:21` | confirmed | read |
| 🟢 | round 2's note 3 is closed — the `release` job is green at the head and nothing names `round-1.md` | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/rounds/round-1.md:36` | confirmed | read: CI `release` passes at `fe3480d2`, judged as draft; executed: `chain_check.py` at the head and over the merge, draft exit 0, ready exit 1 on `Broad gate` and `Pass` beside `nobody` only |
| 🟢 | the two survivors b0e52bb2 adds are true where they stand | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/survivors.md:12` | confirmed | executed: `survivor-check` names exactly those two and exits 0 with the exemptions; read: `REOPEN_FROM` is 1788597030, the item that added the reopening |

## Paste-ready fixes

```python
# WHAT IT ASSUMES: that no item of that release is framed after the batch.
# On 2026-10-08 the owner kept the release at the batch and #834's build
# (1791382684, framed before it) instead of splitting it, while #871-#874
# sit in its milestone unframed. An item framed later for the same release
```
```
| `chain-check` | — | fails a ready pull request over an open note, and, for a work item begun at or after `1791384163` (one past 0.21.0's batch, whose rounds run under 0.20.0's `close`; an item framed later for this release moves it), over a note closed `fixed` |
```
```
This pull request's rounds ran under the installed 0.20.0 `close`, so the first run under the new rule is the first work item reviewed after 0.21.0 is installed. #860 and #866 edit neighbouring lines of `close` and `chain_check.py` (`overview.md` §*Not verified*).
```
```
| `notes`, `close`'s carried note and the two `chain-check` arms on a real run, through a warden's report rather than a fixture. This item's rounds closed with the installed 0.20.0 generator, so none of them ran under the rule | the orchestrator of the first work item reviewed after 0.21.0 is installed |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_a_note_closes_once_at_the_runs_end.py`, `tests/test_docs_line_wrap.py` and `tests/test_the_rules_have_one_owner.py`, in the clone at `fe3480d2` | 134 passed, exit 0 |
| `survivor-check --range be3c452a..fe3480d2`, bare | exit 1; two places, `routing.md:17` and `chain_check.py:739` |
| the same with `--exempt` over this item's `survivors.md` | exit 0; both excused |
| `survivor-check --range origin/release/v0.21.0...fe3480d2` with the same exemptions | exit 0; one excused, `agents/smith.md:199` |
| `chain_check.py --baseline origin/release/v0.21.0` at `fe3480d2`, draft and ready event payloads | draft exit 0, a notice for `Pass` beside `nobody` on `round-2.md`; ready exit 1, `Broad gate` at `not yet` and `Pass` beside `nobody`, both on `round-2.md`; nothing on `round-1.md` |
| a probe merge of `fe3480d2` into `d712a632` (the base tip GitHub reports), then the same two runs | the same exits and the same messages |
| the notes rows of #858's and #864's records on `origin/release/v0.21.0` | #858 round 1: notes 6 to 8 `fixed`; #864 round 1: notes 3 and 4 `fixed`; every other note `answered` |
| work-item directories on the release, #834 and #860 branches | highest 1791384162; #860's is 1791384160 |
| `gh pr checks 879`, read and not run by this round | at `fe3480d2`: `release`, `ledger`, `lint` and `arm-check-grammar (3.13)` pass; the pytest legs and `arm-check-grammar (3.14)` were still pending when read |
| `gh api` reads: PR #879's base and merge, the release branch tip, the repository's squash setting, milestone 58 | base tip `d712a632`; squash message COMMIT_MESSAGES; 26 open issues |
| the full suite, repository-wide lint and typecheck (the sealer's broad gate) | not yet: no run has happened at any SHA of this branch. The sealer answers it, and its spawn is now due |

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
| round-2 | `skills/code-review/scripts/chain_check.py:863` | round 2's 🟡 1 — fixed |
| round-2 | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/changelog.md:21` | round 2's ⬜ 2 — answered |
| round-2 | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/rounds/round-1.md:36` | round 2's ⬜ 3 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2626` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_note_closes_once_at_the_runs_end.py:644` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:19` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_note_closes_once_at_the_runs_end.py:566` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
