# Implementation Plan: the reverify writer records before it re-stamps (#647 steps C and D)

<!-- seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-10-04 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

Carry #647 C and D from `b4c9deb2` whole, without its work item's records.
Then build the three contract clauses the carried writer does not meet (W8,
W9, W10 in `spec.md`). Then rebuild the ledger for this work item against the
0.18.0 fold. Round 1 reviews everything at depth 0, which is the point of the
work item.

## Technical context

- **What exists.** `b4c9deb2`, the tip of
  `feat/647-a-signatory-records-a-pact-change-and-the-pact-is-reviewed`, holds
  the whole of C and D with round 1's and round 2's fixes. CI ran green on all
  three operating systems at that commit (`gh run view 37129036019`: pytest
  on macOS, Ubuntu and Windows, ledger, lint, arm-check-grammar; read, not
  re-run). The worktree `647-pact-cd`, beside this one in the worktrees
  directory, has it checked out.
- **The base moved only in records.** Since the old branch's merge base
  `aa7fb285`, `release/v0.18.1` (`e141980a`) changed `plugin.json`,
  `CHANGELOG.md`, `tests/test_a_record_precedes_the_fixes_it_commissions.py`,
  and folded seven fragments into `seal/releases/0.18.0.md`. None of these is
  in the carry set, so `git checkout b4c9deb2 -- <path>` is the merged content
  for every carried path.
- **The carry set** is the output of
  `git -C <old worktree> log --first-parent --no-merges --format= --name-only b9824454^..b4c9deb2 | sort -u`,
  minus everything under `seal/` except `seal/README.md`. It is 30 paths outside `seal/` plus that one at this frame: `docs/`
  (`the-pact.md`, `one-root-by-lifetime.md` and `.ko.md`), `hooks/config.py`,
  `skills/evidence-check/` (`SKILL.md`, `evidence_check.py`, `pact_check.py`),
  `skills/implement/` (`SKILL.md`, `orchestration.md`), `templates/`
  (`config.md`, `pact-review.md`, `seal-README.md`), `.github/` (`run_tests.py`,
  `test.yml`, `publish-release.yml`), `CONTRIBUTING.md`, both READMEs,
  `seal/README.md` (under `seal/` but a drawing, not a record: carry it), and
  12 files under `tests/`. Phase 1 recomputes the list and records it, rather than
  trusting this count.
- **The writer's units** are listed in `spec.md` §*Data & interfaces*.
  `main`'s reverify branch holds the transaction (`recorded_then_applied`).
- **Failure scenario of the chosen approach, in six months.** A reader opens a
  code comment citing PR #749's round 2 and finds that branch deleted. The
  comments then cite a record nobody can open. Mitigation: the branch is
  kept, and the orchestrator's close comment on #749 says why. The second
  scenario is that #746 lands a stale-`--checked` refusal inside
  `reverify_into` without keeping its family out of the moves, so a refused
  row is recorded as a pact change. W9's seam sentence is the guard, and #746's
  frame should read it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Carry the code from `b4c9deb2`; leave `1791019474`'s records on its branch; close PR #749 unmerged** | the code comments cite a closed PR's records, so a reader opens a branch rather than the tree. A reviewer at round 1 has more to read than a fix diff | **chosen** — it leaves every record on the tree true and is the only shape where `chain_check` can pass at a ready pull request (`spec.md` §*Decision 1*) |
| Merge the old branch in, records riding along | `chain_check` judges `1791019474`'s `routing.md`: last round unchecked, 🔴 10 open, `Branch` naming another branch. Closing it is refused at depth 2, and ticking it by hand is a false record | rejected |
| Merge, then `git rm` the old directory | the net diff is the carry's, so `chain_check` would pass. But round 1's range then holds 44 commits whose messages close another chain's findings, the five folded fragments still conflict, and the squash erases the history anyway | rejected — the carry's end state with a noisier range |
| Carry only the redesign's diff (`f9469ad8..b4c9deb2`) on top of an A+B base | it does not apply: the redesign replaces units round 1's fixes created, which sit on the earlier commits of the same branch | rejected |
| Re-open `1791019474` and change its depth declaration | falsifies a record, which #647's comment of 2026-10-03 names as the reason it was not done | rejected |
| Re-build C and D from scratch against this frame | spends the 44-commit build again for code that is already green on three operating systems, and the review is the same depth-0 review either way | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The carry.** Every carry-set path at its `b4c9deb2` content. The nine `docs/the-pact.md` markers name this item. The 17 `round N of #647 C and D` comments name PR #749's round. `1791019474`'s `changelog.md` becomes this item's. This item's fragment `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md` holds the claim rows W1, W2, G1, G2, C1, D1, D2 and the fact rows F1–F3, each re-read and dated the day the smith read it; their coordinates' hashes are computed from this tree. No `Re-read ·` rows yet | the five pact modules (`test_pact_check`, `test_a_signatory_declares_its_pact`, `test_one_word_one_meaning`, `test_a_signatorys_ci_prints_its_pact`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory`) plus `test_a_signatory_records_a_pact_change`, `test_a_pact_review_takes_a_pact_change`, `test_one_table_walker_reads_what_gfm_renders`, `test_every_reader_ends_a_line_where_gfm_does`, `test_release_hygiene`, `test_the_release_seal_is_drawn`, `test_the_suite_has_a_command_that_is_cheap_twice`, `test_docs_line_wrap`. Scenarios K1 and K2's commands, with output in `phases/phase-1.md` | e249d57d |
| 2 | **The writer meets W8, W9 and W10.** W8: write lines print after their file lands, and none print when the run writes no ledger. W9: a file the run writes is read strictly, and one that will not decode is `LEFT` unreadable. W10: a step-3 write failure is a `LEFT` line, the rest are written, exit 1. Add W1's step-1 stop, W2's mid-apply stop, W3's sibling case and W6's missing-file arm wherever no carried case holds them. `docs/the-pact.md` §*A signatory records a pact change* and §*What this does not see* (the power-loss limit), and `skills/evidence-check/SKILL.md`'s writer paragraph, say all of it, each sentence pinned in its commit | `tests/test_a_signatory_records_a_pact_change.py` whole, each new case seen red against the carried code (§15), recorded in `phases/phase-2.md`. `bin/mutation-check` over the units phase 2 changes | 4a9bdd06 |
| 3 | **The ledger and the closing records.** `bin/evidence-check` names the released rows this item drifts. Each is read, then re-read into this item's fragment with `--reverify --into seal/ledger/1791076833-….md --checked <date>`. A released claim the change made false gets a `Corrected ·` row instead (`evidence_check.py#CITING_VERBS`). New claim rows for W8–W10. `survivors.md` for this branch's range. `overview.md` | `bin/evidence-check --strict .` exit 0, `correction-check`, `survivor-check --range <base>...HEAD`, `unverified-check`, `chain-check --worktree --baseline origin/release/v0.18.1` (draft) | 2cfb60f3 |

**Fallback cut line: between phase 1 and phase 2.** Phase 1 and phase 3
alone ship the carried writer, which already closes 🔴 1, 🔴 10 and
🟡 11–15. It still prints write lines for a run that wrote nothing (W8), can
rewrite a non-UTF-8 byte it read leniently (W9), and leaves a traceback on an
unwritable ledger (W10). Cut there, W8–W10 become one issue with the three
scenarios as its acceptance, and `docs/the-pact.md` §*What this does not see*
names them. No cut falls inside phase 1: the deferred fixes, C and D share
units (`spec.md` §*Scope*), so any split of the carry reverts a built unit.

**Order inside the release.** #741 lands first. When it squashes into
`release/v0.18.1`, merge the release branch in (never rebase: the round
records name SHAs) and fix whatever its encoding check finds in the carry
set. #746 comes after this item and builds on W9's seam.

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
`seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
**Re-read the column after any rebase**, or it names commits that resolve in
one clone and nowhere else.

## Operational impact

- **New test-only dependency:** `cmarkgfm==2025.10.22`, pinned in
  `run_tests.py#CMARKGFM` and both workflow install lines. A plugin user
  installs nothing.
- **New files in a signatory's `seal/`:** `pact-changes/<id>.md`, written by
  `--reverify`. At the pact's repository: `pact-reviews/<id>.md`. Both are
  committed in shared mode.
- **Behaviour change for every `--reverify` user, pact or not:** W8 moves when
  the write lines print; W9 makes a non-UTF-8 ledger fragment `LEFT` rather
  than rewritten; W10 turns a traceback into a `LEFT` line and exit 1.
- **PR #749** is closed unmerged by the orchestrator after this item's pull
  request opens. Its branch is not deleted.
