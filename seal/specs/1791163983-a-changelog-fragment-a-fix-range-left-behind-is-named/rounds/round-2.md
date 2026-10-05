# 1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named — review round 2

| Field | Value |
|---|---|
| Target SHA | 9863be79e85c1cf7cd49cc16b7eb4cc59db61b66 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #802 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `c13039fa115d58789832ddaba2f4efcdd166ed51..71c7303768fb8e1fac1656bff6fe221e5a85b35d`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round over round 1's fixes (f96ea9a2..65ff34c6): did each fix close its finding (round 1's probes re-run, the own-branch probe on CI's merge ref), did the range introduce a regression; `walk_tip` judged by construction over the merge shapes HEAD can be, including a shallow clone; `--no-renames` on moves both ways and a renamed fragment; the owner section and `changelog.md` against the code; the exit status never moving.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding is closed — on CI's merge ref the walk starts at the pull request's own head, so the item's fix is named and a sibling's squash is not | `skills/code-review/scripts/chain_check.py:4176` | confirmed | executed: probes A, B, C, F and the own-branch probe against an unmoved and a moved base; the four merge-ref cases red with `tip = "HEAD"` |
| 🟢 | round 1's second finding is closed — a move lists both of its paths | `skills/code-review/scripts/chain_check.py:4218` | confirmed | executed: six moves in both directions under default and `copies` rename settings; a fragment renamed into place still counts; the two move cases red without `--no-renames` |
| 🟢 | round 1's third finding is closed — the owner section and the fragment name all three attributions | `docs/the-record-layout.md:100` | confirmed | read; `changelog.md:9-10` carries the same three |
| 🟢 | the notice never changes the exit status after the fix range | `skills/code-review/scripts/chain_check.py:4295` | confirmed | executed: every probe compared the exit code with the arm patched out, all equal |
| 🟢 | a shallow checkout leaves the arm silent, and this repository's CI is not shallow | `.github/workflows/hygiene.yml:30` | confirmed | executed: probe I at depth 1 is silent with exit unchanged; the job checks out with `fetch-depth: 0` |
| carried | round 1's confirmations — the ancestor guard's silent state, the first `Target SHA`, the RIDER re-stamp, the owner links and `RULES` row | `skills/code-review/scripts/chain_check.py:4291` | confirmed | the fix range leaves the guard, the SHA choice and `agents/` unchanged; rule 15's cases pass in the module run (236 passed); probe G silent |
| ⬜ 1 | `walk_tip` asks only HEAD's parents, so a merge made from the base side below HEAD sends the walk down the base: the sibling is named and the fix is lost | `skills/code-review/scripts/chain_check.py:4194` | deferred #805 | #805 — no party in this process makes a base-side merge below HEAD, and the arm only prints; the ancestry-path remedy gives up first-parent order and is a design call, filed; executed, probe H. No party in this process makes that merge, and the arm only prints, so it ships no defect. Not listed under the docstring's *WHAT IT CANNOT SEE* |
| ⬜ 2 | the fragment says a sibling's squash is *never* named, which ⬜ 1's shape contradicts, and line 13 is left unwrapped | `seal/specs/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named/changelog.md:13` | answered | corrected at 71c73037: the fragment and the S1 ledger row say a sibling's squash is not named on a branch checkout or CI's merge ref, and name the base-side merge below HEAD as #805; the line is wrapped; read; a correction to the run's paperwork; the ledger's S1 row carries the same *never* |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q tests/test_a_fragment_left_behind_is_named.py tests/test_the_rules_have_one_owner.py tests/test_chain_check_at_the_pull_request.py` at 9863be79 | 236 passed |
| the seven new cases with `tip = "HEAD"` and without `--no-renames`, in the clone, then restored | 6 failed, 1 passed (the merge-on-the-branch case, which pins the HEAD side) |
| probe A — lagging fix, base unmoved; branch, then CI's merge ref | both name the fix in round 1's fix range |
| probe B — as A, with a sibling's squash on the base, merge ref | the fix named; the sibling not named |
| probe C — fragment brought along, sibling on the base, merge ref | silent |
| probe D — moves `hooks/x.py` to `tests/x.py` and to `seal/x.py`, and `tests/t.py` to `hooks/t.py`, each under default and `diff.renames=copies`; a fragment renamed into place after a fix | every move named by its behaviour path; the renamed fragment silent |
| probe F — the branch merges the base (with a sibling), one own commit, the base moves again, merge ref | branch: the fix named, sibling not; merge ref: the fix and the own commit named, neither sibling |
| probe G — the branch rebased onto a moved base, merge ref | silent |
| probe H — a merge made from the base side, then one own commit | HEAD at the merge: the fix named; one commit on top: the sibling named *after the last round*, the fix not named |
| probe I — CI's merge ref cloned at depth 1 | silent, exit 0 with and without the arm |
| probe K — an octopus of base, a side branch descending from the target, and the branch | the fix and the side commit named; the sibling not |
| own-branch probe — this item's records at 9863be79, then a late commit to `chain_check.py`, on the branch, on a merge into `origin/release/v0.18.3`, and on a merge into that base moved by one sibling commit | at 9863be79: silent (the fragment was brought along in 65ff34c6); late commit on the branch and on both merge refs: the late commit named *after the last round*, the sibling not; exit 1 with and without the arm |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle (contract §2); nothing this round leaves open, so the sealer's spawn has come due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/chain_check.py:4187` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:4184` | round 1's 🟡 2 — fixed |
| round-1 | `docs/the-record-layout.md:97` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:4255` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py:4253` | round 1's 🟢 — confirmed |
| round-1 | `agents/smith.md:122` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_rules_have_one_owner.py:296` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
