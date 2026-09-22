# Implementation Plan: the fold ships, and the corpus is still on disk

<!-- seal/specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk/plan.md
— HOW, in phases. This is the Design Gate's artifact. -->

Approved 2026-09-22 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

Eleven phases. Two prepare (the floor inventory, then the floor repairs),
eight write prose into `docs/` grouped by **destination file**, and the last
one retires the directories and re-runs everything the removal could break.

The prose phases come after the repairs on purpose: a repair has to be green
against the corpus as it stands today **and** against the corpus the fold
leaves, and the only way to show the first is to make it before anything is
removed.

## Technical context

- `skills/settle/scripts/settle.py` — `settle` reports, `settle --retire`
  removes the directories whose marker `docs/` carries. It refuses local mode
  and needs python 3.12+.
- `skills/verify/scripts/unverified_check.py#folded_items` — the fold record
  is read from the **top level** of `docs/`, live lines only.
- `seal/ledger.md` line 78 — the one permanent row anchored into a work item
  directory (`spec.md` G3). It is why `1788184145-…` is kept.
- `.github/workflows/hygiene.yml` — the survivor step hands every
  `seal/specs/*/survivors.md` to `survivor_check.py` on every pull request
  into a release branch; the correction step reads the ledger only.
- `hooks/review-history-guard.py` is `PostToolUse` and blocks nothing, so the
  removal of 200+ round records is a reminder at worst.

**What breaks in six months.** The standing statements are written once and
read for years; a sentence folded that a later work item had already
overturned becomes a rule nobody can trace back, because the directory that
held the argument is gone. The mitigation is the newest-wins rule inside a
segment and the phase record naming what was dropped rather than folded.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| One phase per segment (38 phases) | 38 commits and 38 records for eight destination files; a reader cannot see what one document ended up saying | rejected — phases group by destination |
| One phase for all prose | the largest phase in this repository's history, with one commit covering eight `docs/` files and no reviewable seam | rejected |
| Fold the 16 ungrouped by guessing a segment from their slug | the tool declines to guess for a reason: the link from a `tests/` case to the code it pins is nowhere a machine reads | rejected — `spec.md`'s stated rule decides instead |
| Retire `1788184145-…` and drop the `seal/ledger.md` row it anchors | verified evidence for a rule that still stands is deleted, and the repository rule refuses a re-point | rejected — keep eight files |
| Lower `> 200` to `> 5` | the check becomes a comment; `skills/settle/SKILL.md` §3 names this by name | rejected |
| Delete the two `> 200` cases | they are the only sweep of the real records for a doubled close and a broken fix range | rejected — re-pointed instead |
| Take #368's checklist line here | two fix shapes, one unchosen, and a gate change needs `CONTRIBUTING.md`'s answer set | rejected — committing the retirement before the gate avoids the defect without deciding the ticket |
| Write the fold into `docs/experiments/` where a segment anchors there | `folded_items` reads the top level only, so the retirement would refuse | rejected |

## Destination map — 38 segments, 8 phases, 8 documents

| Phase | Destination | Segments (items) |
|---|---|---|
| 3 | `docs/review-chain-spec.md` | `round_record.py` (13), `bin/round-record` (1) |
| 4 | `docs/review-chain-spec.md`, `docs/review-handoff-protocol.md` | `chain_check.py` (6), `survivor_check.py` (2), `skills/code-review/orchestration.md` (1), `docs/review-handoff-protocol.md` (1) · ungrouped `1788212517`, `1788224363` |
| 5 | **new** `docs/the-evidence-ledger.md` | `evidence_check.py` (4), `correction_check.py` (2), `unverified_check.py` (2), `settle.py` (1) |
| 6 | `docs/one-root-by-lifetime.md` | `hooks/root-migrate.py` (1), `skills/implement/scripts/seal.py` (3), `hooks/mode-gate.py` (1), `hooks/config.py` (1), `skills/config/SKILL.md` (1) |
| 7 | `docs/branch-and-release.md`, `docs/release-checklist.md`, `docs/issues-and-milestones.md` | `rider_check.py` (1), `skills/commit-pr-convention/SKILL.md` (2) → branch-and-release · `docs/release-checklist.md` (1), `fold_ledger.py` (1), `release_completeness_check.py` (1), `hygiene.yml` (3), `docs/experiments/2026-09-03-…` (1) → release-checklist · `issue_claims_check.py` (1), `roll_flow_measurement_issue.py` (2), `docs/issues-and-milestones.md` (2) → issues-and-milestones · ungrouped `1788735085` |
| 8 | **new** `docs/the-gates-a-session-meets.md`, `docs/worktree-guard-spec.md` | `commit-review-gate.py` (1), `hooks/cmdline.py` (1), `implementer-notice.py` (2), `review-history-guard.py` (1) → the new file · `worktree-guard.py` (2) → the existing spec |
| 9 | **new** `docs/the-broad-gate.md` | `broad_gate.py` (6), `arm_check.py` (1), `run_tests.py` (2), `agents/sealer.md` (1) · ungrouped `1789540097` |
| 10 | **new** `docs/measuring-a-run.md`, **new** `docs/the-agent-set.md` | `session_cost.py` (7) · ungrouped `1788449488` → measuring-a-run · `skills/agent-contract/SKILL.md` (1), `agents/smith.md` (1), `skills/implement/orchestration.md` (2) → the-agent-set |

83 grouped items and 5 ungrouped, 88 directories in the retire set, 12 left
on disk.

**A destination may be wrong, and the phase that reads the specs is what finds
out.** Where reading a segment's `spec.md` files shows the statement belongs
in another top-level `docs/` file, move it and say so in the phase record.
What may not change without saying so here: no new file below `docs/`'s top
level, and no new document for an area one already covers.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | the floor inventory: `grep -rn "seal/specs" tests/` re-run, every reader classified, F1–F16 re-measured against the retire set, the answers written into `phases/phase-1.md` | the grep's own output against the table; the post-fold population computed from the retire set, not estimated | fbd5da56 |
| 2 | every floor repair — F1–F5 derived from an independent listing, F3 and F6–F8 re-pointed at fixtures, F9–F10 onto the fold record | each repaired module green **before** the fold; each new arm seen red with the arm removed (§15); `uvx ruff check` on the touched files | 5e56c675 |
| 3 | `docs/review-chain-spec.md` — the record generator's 14 items, each sentence carrying its marker | `./bin/settle` no longer lists those 14; `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py` | 21373d00 |
| 4 | `docs/review-chain-spec.md` and `docs/review-handoff-protocol.md` — the checker, the survivor sweep, the orchestrator's half, the handoff, and two ungrouped items | as phase 3 | 28e98957 |
| 5 | **new** `docs/the-evidence-ledger.md` — the ledger, its two checkers, the unverified record and `settle` itself; the file wrapped at 88 and added to `test_docs_line_wrap.COVERED` | as phase 3, plus the line-wrap case green on the new file | 91ca7125 |
| 6 | `docs/one-root-by-lifetime.md` — the root, the two modes, the config reader | as phase 3 | 2a7b571a |
| 7 | `docs/branch-and-release.md`, `docs/release-checklist.md`, `docs/issues-and-milestones.md` — the release, the tickets, the rolling log | as phase 3 | 19b7959b |
| 8 | **new** `docs/the-gates-a-session-meets.md` and `docs/worktree-guard-spec.md` — the four hooks a session meets, and the worktree guard's two | as phase 5 | 534769c0 |
| 9 | **new** `docs/the-broad-gate.md` — the gate, its arm list, the runner, the sealer, and the three checks that could not see what they were named for | as phase 5 | adea8052 |
| 10 | **new** `docs/measuring-a-run.md` and **new** `docs/the-agent-set.md` | as phase 5 | 873a75c8 |
| 11 | `settle --retire` in a commit of its own; `survivors.md` with the range-row; `changelog.md`; the post-fold re-run of F1–F16 and of A4–A9 | the acceptance table in `spec.md`, every exit code read directly | 7811c0b9 |

**Phase 11's order is fixed**, because two of its steps are the reason the
whole branch can be verified at all:

1. `./bin/settle` once more — the list of what is about to go, compared
   against the 88 the markers name, and against the 11 kept ids by name.
2. `settle --retire`, then `git add -A` and commit **immediately**. The
   deletions are in the index before any check runs, which is what keeps
   #368's defect off this branch without deciding that ticket.
3. `unverified_check.py --baseline`, `survivor-check` with the exemption,
   `chain_check.py --baseline origin/main`, `evidence_check.py --strict .`,
   then the repaired floor modules. Each exit code read directly, never
   through a pipe.
4. Only then the hand-off to the review chain. The broad gate is the
   sealer's single act and is not run in this phase.

## Operational impact

- **1,345 files leave the tree in one commit.** Nothing imports them and no
  gate refuses their absence, but every later `git log` over `seal/specs/`
  crosses this commit.
- Five new `docs/` files become ratified norms: they outrank the SDD set from
  the moment they land, and `questions.md` Q1 is where the owner can overturn
  the shape.
- `seal/ledger.md`, `seal/parity.md` and `seal/follow-up.md` are untouched.
- The fragments this branch writes — `changelog.md`, and a ledger fragment
  only if a claim is established — are gathered by the release that ships it.
