# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — review round 1

| Field | Value |
|---|---|
| Target SHA | c575695ee6a0b88c721f2477560682f9bc62b102 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 608 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, the three copies of the `Pass`-beside-`nobody` rule that still say it fails at every stage |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790297083 reviews the build at c575695e against spec.md and plan.md (frame 8c7569a0, approved 97d0d2a7). It covers a record restored byte for byte from the fork's history (#598 instance 1), Pass beside nobody printing on a draft (#598 instance 4), and added_on_branch finding the latest add across a merge and a skewed clock (#529). The classes are every way a pull request's own new record could read as restored (the unsafe direction), every PR state the draft arm reads, every merge shape the history queries walk, and every document stating the Pass-beside-nobody rule.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | three copies still say `Pass` beside `nobody` on the last record fails the pull request, with no draft exception | `skills/code-review/orchestration.md:295`, `templates/sdd-round.md:119`, `README.md:609` | open | read. The same class Scope 4 enumerated. Line 519 of the same orchestration file now says the opposite for a draft |
| ⬜ 2 | the handoff protocol's no-claim sentence names the untouched record and not the restored one | `docs/review-handoff-protocol.md:190` | open | read. Incomplete, not false |
| ⬜ 3 | `written_late` docstring: "an ordinary record pays no extra `git log`" is true only of a record naming no fix | `skills/code-review/scripts/chain_check.py#written_late` | open | read. `phases/phase-2.md` carries the right qualifier |
| ⬜ 4 | `written_late`'s restoration exit reaches untouched records whose add is still in range; right answer, unnamed shape | `skills/code-review/scripts/chain_check.py#written_late` | open | executed, probe 3 Q2 |
| ⬜ 5 | changelog says "three records" for three shapes | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md:1` | open | read |
| 🟢 | `--find-object` walks both parents without `--full-history`; dropping the flag from `restored_from` is safe | `skills/code-review/scripts/chain_check.py#restored_from` | confirmed | executed, probe 1 (a)(b)(c), including the second-parent-treesame shape that a plain log simplifies |
| 🟢 | no route found by which a pull request's own new record reads as restored | `skills/code-review/scripts/chain_check.py#restored_from` | confirmed | executed, probe 3 Q1 and M1. read: same path plus same bytes in the fork's history is required, and the fork is the base tip in CI |
| 🟢 | `--topo-order` gives the late add under a skewed clock | `skills/code-review/scripts/chain_check.py#added_on_branch` | confirmed | executed, probe S7, M5 and M6 |
| 🟢 | the draft excuse reaches only `Pass` beside `nobody`; ready and unknown still fail | `skills/code-review/scripts/chain_check.py#checked_by` | confirmed | executed, M3 and M4. read: `strict = state != "draft"` |
| 🟢 | the C4 divergence's grounds hold: `run_check` judges `close` as a draft unless `gh` says ready | `skills/code-review/scripts/round_record.py#run_check` | confirmed | read, lines 2348–2367 and 988–1010. No document states `close`'s exit code in the window |
| 🟢 | the replaced orchestration sentence and its renamed pin are accurate and complete | `skills/code-review/orchestration.md:519` | confirmed | read. The pin asserts the whole sentence and the absence of the old ending |

## Paste-ready fixes

```
| `nobody — <why>` | the gap, written down. It prints on every CI run, and on the run's **last** record beside a checked `Pass` it fails a ready pull request — a review cannot have passed while its own fixes went unread. On a draft that pair prints and names the verifying round, because the draft is where it stands between `close` and that round's record, and *Ready for review* re-runs the check. Work items begun before the rule landed are excused and only print |
```
```
`nobody` prints on every run. On the run's LAST record it also FAILS a ready
pull request when `Pass` is checked beside it, because that pair is the review
claiming to have passed while its own fixes went unread. On a draft the pair
prints and names the verifying round, because that is where it stands between
`close` and the verifying round's record, and *Ready for review* re-runs the
check. Work items begun before the rule landed are excused and only print. The
way out costs no round: one verifying round at the diff of those fixes, and a
round that opens nothing needing a fix does not consume the cap.
```
```
- **`Fixes checked by: nobody` prints everywhere and fails in one place.** On
  the run's last record, beside a checked `Pass`, it fails a ready pull
  request: a review cannot have passed while the fixes that closed its
  findings went unread. On a draft that pair prints and names the verifying
  round, and *Ready for review* re-runs the check. Anywhere else it only
  prints. Work items begun before this rule landed are excused entirely,
  because a check whose first act is red on merged history nobody can repair
  is a check people learn to skip. The way out costs no round — one verifying
  round at the diff of those fixes.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the five touched modules (`test_chain_check_at_the_pull_request.py`, `test_a_record_precedes_the_fixes_it_commissions.py`, `test_the_last_rounds_fixes_are_checked.py`, `test_the_fixes_close_the_record.py`, `test_the_rules_have_one_owner.py`) at c575695e | 442 passed, exit 0 |
| probe 1: `git log --find-object` with and without `--full-history`, shapes (a), (b), (c) | identical lists in all three. In (c), plain `git log -- r.md` lists only `sideZ, addX`, and `restored_from` finds `mainY` |
| probe 2: `added_on_branch` on S1, S7, and the parallel add in both date orders | the late add every time |
| probe 3: a branch's own record squashed into the base; Q1 without merging the base back, Q2 after | Q1: in the diff, `restored_from` None. Q2: not in the diff, `restored_from` names the squash, while `added_on_branch` still names the branch's own add |
| eight mutations of `chain_check.py`, one at a time, each run against its modules and then restored (M1 predicate walks HEAD; M2 `written_late` skips the predicate; M3 `main` omits `strict`; M4 excuse at every stage; M5 no `--topo-order` in `added_on_branch`; M6 no `--full-history` there; M7 no `--topo-order` in the predicate; M8 `refs` ignores `restored`) | every mutation red: 34, 1, 1, 3, 1, 2, 1 and 5 failures. The clone was clean after restoring |
| `evidence_check.py .` in the clone | 2241 ok, 0 drifted, 0 broken |
| cost of one `restored_from` walk on this repository | 25 ms |
| the broad gate: full suite, lint, typecheck | not yet. Owed to the sealer, once, after the rounds settle; this round ran none of it |

```
1c result Z
1c no-full ['dfd33c6… mainBackX', '1d4f53c… mainY']
1c full    ['dfd33c6… mainBackX', '1d4f53c… mainY']
1c plain log no-full ['sideZ', 'addX']
1c restored_from 1d4f53ce3afa3d35c7c85456cb5ec981029d6008
```
```
3 Q1 (branch never merged base): touched? True restored_from: None
3 Q2 (branch merged base in): touched? False restored_from: ecd05c0 added_on_branch: 906ee6f f1: 906ee6f
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
