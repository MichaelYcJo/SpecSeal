# Round 2 report — a changelog fragment a fix range left behind is named (#797)

| Field | Value |
|---|---|
| Round | 2, the verifying round over round 1's fixes |
| Target SHA | 9863be79 |
| Fix range read | f96ea9a2..65ff34c6, 4 commits |
| Base | `release/v0.18.3` at a3aa139a |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 9863be79, in the session scratchpad under the work item id and `round-2/`, removed after the round |

## Summary

All three of round 1's findings are closed, and the fix range opened nothing
that needs a fix.

- **Round 1's blocking finding is closed.** On CI's merge ref the walk now
  starts at the pull request's own head (`walk_tip`), so the item's own fix
  is named and a sibling's squash on the base is not. Executed: round 1's
  probes A, B and C re-run, and the own-branch probe re-run on this item's
  real history, against both an unmoved and a moved base.
- **Round 1's second finding is closed.** With `--no-renames` a move lists
  both of its paths. Executed in both directions, out of and into what ships,
  under the default `diff.renames` and under `diff.renames=copies`. A
  fragment renamed into place still counts as brought along.
- **Round 1's third finding is closed.** The owner section and the fragment
  now name all three attributions (read).
- **Two ⬜, neither a release defect.** `walk_tip` asks only HEAD's own
  parents. A merge made from the base side, sitting below HEAD, still sends
  the walk down the base (executed). No party in this process makes that
  merge. The fragment's sentence *a sibling's squash on the base is never
  named* overstates by that one shape, and the same line is left unwrapped.

The notice still never changes the exit status. Every probe compared the
check's exit code with the arm patched out, and the two were equal in every
case.

## Findings

### ⬜ 1 — below HEAD, a merge whose first parent is the base still sends the walk down the base

`skills/code-review/scripts/chain_check.py:4194`.

`walk_tip` looks at HEAD's parents alone. That covers CI's merge ref, which
is always HEAD. It does not cover the same parent order one commit deeper. On
a branch whose history holds a merge made from the base side (first parent
the base, second the branch), followed by one more commit, the first-parent
walk from HEAD passes that merge and runs down the base.

Executed (probe H): a lagging fix, a sibling's squash on the base, the branch
reset to the base and the old branch merged into it, then one more own
commit. With HEAD at that reversed merge, the fix is named, because
`walk_tip` handles it. With one commit on top, the notice names the sibling's
squash as *after the last round* and the item's fix is not named. That is
round 1's blocking failure, one commit lower.

Why this is ⬜ and not 🟡: no party in this process makes that merge. `git
merge` and `git pull` run on the branch put the branch first, and the
integration commit `docs/the-record-layout.md` §*A commit after the build
brings its changelog fragment along* names is a merge of the release branch
made from the branch. Probe F covers that shape and is right. The arm only
prints, so the cost of the rare shape is one wrong notice line, never a stop.
The docstring's *WHAT IT CANNOT SEE* does not list the shape, though.

If the orchestrator wants the shape closed rather than written down, the
general form is to drop `walk_tip` and restrict the walk to the commits that
descend from round 1's target, with `git log --ancestry-path`. A sibling's
squash never descends from the target, whatever the parent order. That
remedy is read, not executed. It also gives up first-parent order for
history that branches inside the item, so it is a design choice for an
issue, not a fix for this round.

### ⬜ 2 — the fragment says a sibling's squash is *never* named, and the line is unwrapped

`seal/specs/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named/changelog.md:13`.

*so a sibling's squash on the base is never named* is true for every shape
the process makes, and false for the shape in ⬜ 1. The ledger's S1 row
carries the same words. The owner section (`docs/the-record-layout.md:98`)
makes the narrower claim, that the walk starts at the pull request's own
head, and that claim is exact. Line 13 also runs to about 130 characters
where the rest of the fragment wraps near 78. The release gathers the
fragment verbatim, so the long line reaches `CHANGELOG.md` as it stands. Both
halves sit under `seal/specs/`, so this is a correction to the run's
paperwork.

## Answers to what the round was asked

**Round 1's verdicts, inherited and checked.**

| Round 1 | This round | How |
|---|---|---|
| 🔴 1, the walk follows the base in CI | closed | executed: probes A, B, C, F and the own-branch probe; the four new merge-ref cases red with `tip = "HEAD"` restored |
| 🟡 2, a move under `tests/` or `seal/` is not named | closed | executed: probe D, six moves; the two move cases red with `--no-renames` removed |
| ⬜ 3, two attributions where the notice writes three | closed | read: `docs/the-record-layout.md:100-102` and `changelog.md:9-10` name all three |
| 🟢 silent state for a target HEAD does not descend from | carried | the guard at `chain_check.py:4291` is unchanged by the fix range; probe G (rebase inside a merge ref) silent |
| 🟢 first SHA of a two-SHA `Target SHA` | carried | unchanged by the fix range; its case passes in the module run |
| 🟢 `agents/smith.md` RIDER re-stamp | carried | the fix range does not touch `agents/` |
| 🟢 owner section, links, `RULES` row | carried | the section was edited; rule 15's cases pass in the module run |

**`walk_tip` by construction.** Its result depends on three facts: whether
HEAD is a merge, whether HEAD's first parent descends from round 1's target,
and which later parent descends from it. Each shape the round named, with
what the walk reads:

| Shape of HEAD | `walk_tip` returns | Notice | Evidence |
|---|---|---|---|
| branch checkout, no merge | HEAD | the item's commits | executed, probe A branch and own-branch 2 |
| merge of the release branch on the branch (first parent descends) | HEAD; the merge is skipped and the sibling stays behind its second parent | the item's commits, sibling not named | executed, probe F branch; new case at test line 482 |
| CI merge ref, base unmoved | the second parent, the pull request head | the item's commits | executed, probe A merge ref and own-branch 3 |
| CI merge ref, base moved | the second parent | the item's commits, sibling not named | executed, probe B and own-branch 4 |
| CI merge ref over a head that itself merged the base, base moved again | the second parent | the item's commits including one after its own merge; neither sibling named | executed, probe F merge ref |
| octopus of base, an unrelated head, the branch | the first later parent that descends | the item's commits | executed, the new case at test line 514 |
| octopus where two later parents descend | the first of them | that parent's first-parent line; a commit only on the other is not walked | executed, probe K; no process makes this shape |
| merge where no parent descends from the target | not reached: HEAD does not descend, the ancestor guard at `:4291` returns first | silent | read; probe G |
| rebased branch inside a merge ref | not reached, same guard | silent | executed, probe G |
| HEAD equal to round 1's target, a merge itself | HEAD, since neither parent descends | silent, the range is empty | read |
| shallow clone, `fetch-depth: 1` | not reached: round 1's target does not resolve | silent, exit status unchanged | executed, probe I. This repository's CI is not shallow: `.github/workflows/hygiene.yml:28-30` checks out with `fetch-depth: 0`, so the target resolves there |
| a merge made from the base side, below HEAD | HEAD | the sibling named, the fix lost | executed, probe H; ⬜ 1 |

The two mutants the ledger records as equivalent are equivalent (read).
`len(parents) > 1` as `> 0` differs only for a one-parent HEAD whose parent
does not descend from the target. Past the ancestor guard that HEAD is the
target itself, and the loop over the later parents is then empty. `<end>..HEAD`
for `<end>..<tip>` asks the same question of every commit the walk lists,
because each listed commit is an ancestor of the tip.

**`--no-renames`, both directions.** A move out of what ships (`hooks/` into
`tests/` or `seal/`) is now named by its source. A move into what ships
(`tests/` into `hooks/`) was named before and still is, by its destination.
Under `diff.renames=copies` every one of those reads the same. A fragment
renamed into place after a fix counts as the fragment's change, so the fix
before it is not named. All executed, probe D.

**The owner section and `changelog.md` against the code.** The owner section
(`docs/the-record-layout.md:93-108`) matches the code. It says that a move
lists both paths, that CI's walk starts at the pull request's own head, and
that there are three attributions. Its silent states are the four the guards
implement. The fragment matches the code except for the *never* in ⬜ 2.

**The notice and the exit status.** Unchanged in every probe. Each scratch
probe ran the check twice, once with the arm patched out, and asserted the
codes equal. The own-branch probe on this item's real records returned exit 1
with and without the arm, from the other arms of a ready pull request whose
`Broad gate` reads `not yet`.

**The smith's account, checked.** The ledger says the merge-ref and move
cases were red before the fix. I restored `tip = "HEAD"` and removed
`--no-renames` in the clone. Six of the seven new cases went red. The
seventh, the merge-on-the-branch case, stays green under that mutant by
design, because it pins the side where HEAD is the right tip. The other 23
mutations the ledger reports are the smith's account, not re-run.

## Regression tests to plant

None required. If ⬜ 1 is closed rather than written down, the case is probe
H as a test in `tests/test_a_fragment_left_behind_is_named.py`: a reversed
merge, one own commit, and an assert that the fix is named and the sibling is
not. It is red at 9863be79 (executed).

## Facts for the evidence ledger

- `walk_tip` handles a merge at HEAD only. The S1 row's *so a sibling's
  squash on the base is never named* holds for every merge shape the process
  makes, and not for a merge made from the base side below HEAD (⬜ 1, ⬜ 2).
- `.github/workflows/hygiene.yml` checks out with `fetch-depth: 0`. A
  repository that keeps the `actions/checkout` default of depth 1 gets
  silence from this arm, through the existing silent state *a round 1
  `Target SHA` this repository cannot see*.

## Carried, not re-established

- `bin/evidence-check --strict .` exit 0 at the fix head is the
  orchestrator's run, not re-run here.
- The 298 passed across the three narrow modules and three hygiene modules
  is the orchestrator's. I ran the three narrow modules alone: 236 passed.
- What `main` passes to the arm and when it runs are carried from round 1;
  the fix range does not touch `main`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding is closed — on CI's merge ref the walk starts at the pull request's own head, so the item's fix is named and a sibling's squash is not | `skills/code-review/scripts/chain_check.py:4176` | confirmed | executed: probes A, B, C, F and the own-branch probe against an unmoved and a moved base; the four merge-ref cases red with `tip = "HEAD"` |
| 🟢 | round 1's second finding is closed — a move lists both of its paths | `skills/code-review/scripts/chain_check.py:4218` | confirmed | executed: six moves in both directions under default and `copies` rename settings; a fragment renamed into place still counts; the two move cases red without `--no-renames` |
| 🟢 | round 1's third finding is closed — the owner section and the fragment name all three attributions | `docs/the-record-layout.md:100` | confirmed | read; `changelog.md:9-10` carries the same three |
| 🟢 | the notice never changes the exit status after the fix range | `skills/code-review/scripts/chain_check.py:4295` | confirmed | executed: every probe compared the exit code with the arm patched out, all equal |
| 🟢 | a shallow checkout leaves the arm silent, and this repository's CI is not shallow | `.github/workflows/hygiene.yml:30` | confirmed | executed: probe I at depth 1 is silent with exit unchanged; the job checks out with `fetch-depth: 0` |
| carried | round 1's confirmations — the ancestor guard's silent state, the first `Target SHA`, the RIDER re-stamp, the owner links and `RULES` row | `skills/code-review/scripts/chain_check.py:4291` | confirmed | the fix range leaves the guard, the SHA choice and `agents/` unchanged; rule 15's cases pass in the module run (236 passed); probe G silent |
| ⬜ 1 | `walk_tip` asks only HEAD's parents, so a merge made from the base side below HEAD sends the walk down the base: the sibling is named and the fix is lost | `skills/code-review/scripts/chain_check.py:4194` | open | executed, probe H. No party in this process makes that merge, and the arm only prints, so it ships no defect. Not listed under the docstring's *WHAT IT CANNOT SEE* |
| ⬜ 2 | the fragment says a sibling's squash is *never* named, which ⬜ 1's shape contradicts, and line 13 is left unwrapped | `seal/specs/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named/changelog.md:13` | open | read; a correction to the run's paperwork; the ledger's S1 row carries the same *never* |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened: `seal/specs/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named/rounds/round-1.md`
and `round-1-report.md`; `changelog.md` of the same work item; the diff
f96ea9a2..65ff34c6 whole (`skills/code-review/scripts/chain_check.py`,
`docs/the-record-layout.md`, the work item's ledger fragment under
`seal/ledger/`, `changelog.md`, `tests/test_a_fragment_left_behind_is_named.py`);
`chain_check.py` lines 4100-4360 (`behaviour_path`, `range_ends`,
`last_round_end`, `walk_tip`, `commits_after`, `fragment_left_behind`), and
`git`, `is_ancestor`, `resolves_to`; `tests/test_a_fragment_left_behind_is_named.py`
lines 1-260 and the new cases; `docs/the-record-layout.md` lines 80-115;
`.github/workflows/hygiene.yml` lines 1-35 and 150-215; the checkout lines of
the other workflows by search; `ruff.toml` head; `bin/test`.
Not opened: `spec.md`, `overview.md`, `plan.md`, the phase records, `main`
in `chain_check.py`, `agents/smith.md`.
