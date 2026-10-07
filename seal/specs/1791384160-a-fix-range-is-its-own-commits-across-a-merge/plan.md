# Implementation Plan: a fix range is its own commits across a merge (#860, #805)

<!-- seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

One reading of *the commits a range owns* — `git log --ancestry-path
--no-merges a..b` — lives in `chain_check.py` and is imported by every reader
of a range in the two scripts. `round_record.py close` measures the fix
surface at the range's two ends as today and keeps only the units an owned
commit added or changed. The fragment notice walks the owned commits from
round 1's target to HEAD and drops `walk_tip`. Three git listings gain `-z`.
The rule has one home in `docs/the-record-layout.md`, and the two scripts
and the orchestration link it.

## Technical context

Coordinates are at `1d935529` (the branch's routing commit, tree equal to
main `5623d728`).

- `skills/code-review/scripts/round_record.py`: `parse_range` :3273,
  `touched` :3305, `measure` :3469, `tracked_at` :3966, `call_sites` :3615,
  `unit_dumps` :2308, `fix_pass_units` :2331, `landings` :2360 (calls
  `fix_pass_units`; not edited), `unit_adders` :4060, `depth_two` :4094
  (takes the filtered `added`; not edited), `close` :4244 — the `fixed`
  guard at :4319–:4325, `paths = touched(root, a, b)` at :4326 and the
  `measure` call at :4327.
- `skills/code-review/scripts/chain_check.py`: `range_ends` :4442,
  `last_round_end` :4461, `walk_tip` :4482, `commits_after` :4507,
  `fragment_left_behind` :4543 (the `rev-list` calls at :4617 and :4626),
  the module docstring's fragment row :48–:54, `is_ancestor` :1434.
- Tests that read these: `tests/test_the_fixes_close_the_record.py` (its
  `close` helper :117 runs the generator with `--range`; its `_build` :85
  makes `base` and `feature`), `tests/test_a_fragment_left_behind_is_named.py`
  (`integrate` :386 and `ci_merge_ref` :433 are the merge shapes already
  planted; `judged` :175 pins that the arm never moves the exit status),
  `tests/test_the_fixes_name_their_surface.py`,
  `tests/test_a_fix_of_a_fix_is_counted.py`,
  `tests/test_the_rules_have_one_owner.py` (rule 15 is the fragment rule's
  entry and the model for the new one).
- Policy: `docs/the-record-layout.md` §*A commit after the build brings its
  changelog fragment along* :82–:117 states the first-parent walk and
  `walk_tip`'s CI case in prose; `docs/round-record-spec.md` §*The fix range*
  :308; `skills/code-review/orchestration.md` §*And name the fix surface*
  :364–:371 says *every top-level Python unit the range touches*.
- Released ledger rows that anchor on what moves: `seal/releases/0.18.3.md`
  :113 (`S1, S5, S8, S10`, anchors `walk_tip@a591b279` and
  `fragment_left_behind@ae5436fc`), :114 (`S2, S3, S4, S6`, anchors
  `commits_after@f603407e`), `seal/releases/0.19.0.md` :81 (`A1`, the `Fix
  of a fix` derivation). `seal/config.md` declares `Ledger frozen from
  1790993141`, so each is a citing row in this item's fragment.
- Document ceiling: `seal/config.md` `Document line ceiling | 1000`, `Over
  the ceiling | none`; `docs/round-record-spec.md` is at 994 lines and
  `docs/review-chain-spec.md` at 999. The rule's home therefore goes in
  `docs/the-record-layout.md` (279 lines), which already owns the fragment
  rule, and the fix-range section links it in one sentence.
- Measured in the frame, in the `832` worktree where `1791270164`'s squashed
  commits still resolve: `99bcad40..092004bb` is 9 commits, 5 owned; the
  two-ends diff lists 74 paths, the owned commits 9; in one of those 9 files
  the two-ends diff adds 22 top-level names and the owned commits 2. `git
  grep -n -z` emits `<rev>:<path>\0<line>\0<text>`.

**What breaks in 6 months.** A behaviour change made only inside a merge
commit's conflict resolution is in neither reader's view, as it was not
before; the home states it, and a `fixed` row that names the merge is refused
with that reason rather than measured on nothing. A range whose start does
not reach its end owns nothing; `close` refuses it, `new` counts no landing
from it (the permissive direction `landings` documents), and the notice is
silent on it as it already is for a target HEAD does not descend from.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. `--ancestry-path --no-merges` as the one reading, surface filtered per unit** | a change inside a merge's conflict resolution is invisible to both readers; a range whose start does not reach its end is empty. Both are stated and the first is today's declared limit | chosen |
| B. `--first-parent --no-merges` for both readers, `walk_tip` kept and taught to look below HEAD | #805 recurs one level deeper at each extension; the reading rests on parent order, which `git merge` sets for whoever ran it and no party here controls — the inventory's *guess* class | rejected |
| C. the two-ends diff with each merge's second-parent side subtracted (#860's second option) | a path both sides changed is either dropped, losing the own change, or kept whole, keeping the sibling's units; the measurement found exactly that file, 22 against 2 | rejected |
| D. the two-ends diff restricted to the owned commits' paths, no per-unit filter | the same file: 22 units at the ends, 2 owned | rejected, and S2 is the case that keeps it rejected |
| E. a per-commit measure only, the parent-to-commit surfaces unioned | `depth_two` and `call_sites` need the range's ends parsed (`at_a`, `at_b`), so the ends are parsed anyway; a unit added and removed inside the range is listed though absent at the end; a contract changed and changed back is listed | rejected; A keeps the ends' meaning and adds the ownership filter |
| F. for the notice's *since the fragment last changed*, the position of the fragment's last change in `--topo-order` | where history branches inside the item, whether a side commit is named depends on git's tie-break between two commits neither of which descends from the other, and no rule a person can state predicts it | rejected; the descent rule gives the same answer on a linear history and a statable one on a branched one |
| G. keep `walk_tip` and list #805's shape under *WHAT IT CANNOT SEE* (#805's second option) | the notice names a sibling's squash as the item's and misses the item's fix for a shape nothing refuses; the inventory's *let the unknown through* | rejected |
| H. the `Fix range` count becomes the owned-commit count | every record since `RANGE_FROM` disagrees with the checker and a new cutoff is needed; the count's job, a moved end, is served by git's `a..b` on both sides | rejected; one sentence in the home says the row's count and the surface read the range two ways |
| I. a `*_FROM` cutoff for the new derivation | nothing re-reads a written row against git, so it would gate nothing; the generator has no grandfathering by policy | rejected |
| J. the `fixed` guard keeps its two `is_ancestor` tests | a `fixed` row naming the merge, or a sibling's commit, passes the guard while the surface below is measured on none of it, so the guard's own sentence becomes false | rejected |
| K. the rule's home in `docs/round-record-spec.md` beside the fix-range row | the file is six lines under the ceiling; the section would cost lines elsewhere in the same file | rejected for the ceiling; the fix-range section links the home instead |
| L. leave the three `-z` readers to #866/#867 | `touched` is rewritten here anyway and gets `-z` for free; the other two are one token each in the same class and share one red fixture; splitting them leaves two guesses standing beside a corrected third | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `chain_check.py#own_commits`, the one reading, with its parse measured first (Q1). `fragment_left_behind` walks it from round 1's target to HEAD, takes each record's range and *after the last round* from it, and names a commit when no owned fragment-changing commit descends from it (Q2); `walk_tip` and `commits_after` removed; the module docstring's fragment row rewritten. S7 and S9 seen red first; S8's three cases re-documented. The rule's home written in `docs/the-record-layout.md` and the fragment section there rewritten to say the owned-commit walk; `docs/round-record-spec.md` §*The fix range* links it | `tests/test_a_fragment_left_behind_is_named.py` whole (S7, S8, S9, and `judged`'s exit-status pin on every case); `tests/test_chain_check_at_the_pull_request.py` at the boundary | |
| 2 | `round_record.py`: `touched` reads `own_commits`; `own_units` per owned commit; `close` filters `measure`'s `added` and `changed` to owned units before `depth_two` and `call_sites`; `fix_pass_units` the same filter; `unit_adders` reads `own_units` for the `fixed` commits; `parse_range` refuses a start that does not reach its end; the `fixed` guard asks `own_commits` and its message is rewritten. S1–S6 seen red first. `skills/code-review/orchestration.md` §*And name the fix surface* links the home; `tests/test_the_rules_have_one_owner.py` gains the rule's entry (Q5) | `tests/test_the_fixes_close_the_record.py`, `tests/test_the_fixes_name_their_surface.py`, `tests/test_a_fix_of_a_fix_is_counted.py` whole; `tests/test_the_rules_have_one_owner.py` | |
| 3 | `-z` in `tracked_at` and in `call_sites`' parse (two partitions on NUL, one on the first `:`), with `touched` already verbatim through phase 1. S10's fixture seen red against each of the three | the close module's new case; `tests/test_a_runner_reached_unit_reads_pytest_only.py` at the boundary (it reads `call_sites`) | |
| 4 | the records: `changelog.md`, the ledger fragment with the new claims, the `Corrected ·` rows for 0.18.3's two anchoring rows and the re-read of 0.19.0's `A1`, `overview.md`'s divergences and *Not verified*; the five text-hygiene modules the brief names | `bin/evidence-check` green on the branch (S13); the hygiene modules | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Seams with the siblings that touch the same two files

| Sibling | Units it changes | Where this item meets it | How the build is sequenced |
|---|---|---|---|
| #866 (`1791384155`) | `landings` (the `Location` reading), `location_units`, `depth_two`, `fix_table`, `terminal_value`, `pull_request_is_ready`, `stopping_floor`/`floor_and_fixes`, `runs_of`/`current_run`, `broad_gate`/`seal`, `doubled_grounds`, `field`/`field_index` | `close` — #866 at its `doubled_grounds` and `field_index` calls, this item at the `fixed` guard :4319–:4325 and the surface at :4326–:4335; `depth_two` — #866 inside it, this item only in what it is handed; `tracked_at` — this item's one token, #866's callers unaffected since they test membership | different lines of one function; whichever lands second merges the release branch in and resolves text, not meaning |
| #837 (`1791384154`) | the open-rows and verdict handling in `new` and `close`, `checked_by`/`fix_of_a_fix` and the run cut in `chain_check`, `skills/code-review/orchestration.md`'s fix-pass sections | `close` as above; `landings`' `COMMISSIONS_NOTHING` filter (#837) against `fix_pass_units`' result (this item) — two inputs to one function, neither edits the other's; `orchestration.md` — #837 the fix-pass rules, this item one sentence in §*And name the fix surface* | no shared line is expected; the merge of the release branch is the check |
| #835 (`1791384152`) | the registry test reading #834's table | `own_commits` is a new reader and declares its class in `spec.md`; where #835's registry lands first, this item adds its rows there | this item after #835, or the row added at the integration merge |

## Operational impact

- No migration, no new environment variable, no new dependency. Bare
  `--ancestry-path` is git 1.6 or later; the CI legs run 2.x.
- Compatibility: records already written read the same; `close` gains two
  refusals at the keyboard (S5, S6), each at exit 2 with nothing written and
  the shape named. Direction: `close` blocks more on two shapes nobody
  intends; the surface rows name fewer units, which is the true surface; the
  notice names different commits and never refuses. Prompt budget: zero —
  nothing here asks a person anything.
- The released 0.18.3 and 0.19.0 ledger rows are not edited; the fragment
  carries their corrections and the fold moves them at the release.
