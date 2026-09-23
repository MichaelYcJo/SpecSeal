# Feature Specification: the review arm asks where no reviewer compares

<!-- Skeleton written first; filled as the frame is read. -->

## Grounding

(pending)

## Scope

(pending)

## User scenarios & acceptance *(mandatory)*

(pending)

## Data & interfaces

(pending)

## The measurement the issue asked for

Issue #518 says one number has to be taken before any line is drawn: how many
review rounds on docs/seal-only changes found a real defect. It was taken from
the tree on 2026-09-23 against `origin/release/v0.14.0` at `f8f1c9de`, by three
scripts that read `git log` and the round records' `## Verdicts` tables. Every
figure below is **executed** unless it says otherwise.

**M1. No reviewed work item was ever confined to `docs/` and `seal/`.** Of the
88 work items with a round record on the release branch, the commit that added
each one's `round-1.md` touched a path outside those two roots in all 88. The
one apparent exception, `1788184145-the-gate-stops-the-session-editing-its-tests`,
is a pre-squash commit that recorded a round separately from the code it
reviewed, and that round's findings sit in `agents/`.

**M2. The seventeen docs/seal-only commits were never reviewed.** Of 175
non-merge commits on the release branch, 17 are confined to `docs/` and
`seal/`, the same count the issue took from `main`. None of them added a round
record. Thirteen of the seventeen touch `docs/flow.md`, which no longer exists
in the tree. Four touch `docs/one-root-by-lifetime.md` and its Korean edition,
the design record for the document roots.

**M3. The nearest thing to a docs/seal-only item is the second fold, and its
review found real defects in every round that had fixes.**
`1790119502-four-shipped-work-items-wait-unfolded` (#514, squashed as
`f2943c04`) changed `docs/`, `seal/` and four test files. Its three rounds
opened seven findings a later round verified as fixed, and all seven are
located in `docs/`:

| Round | New findings fixed | Severity | Where |
|---|---|---|---|
| 1 | 4 | one 🔴, one 🟡, two ⬜ | `docs/branch-and-release.md`, `docs/the-evidence-ledger.md`, `docs/the-agent-set.md`, `docs/review-chain-spec.md` |
| 2 | 3 | one 🟡, two ⬜ | `docs/review-chain-spec.md`, `docs/release-checklist.md`, `docs/branch-and-release.md` |
| 3 | 0 | — | verified the fixes |

The 🔴 was a folded policy sentence that gave three release acts to the tag
push when two of them fire on the merge to `main`. That is the defect the issue
predicts for a fold: *whether a folded sentence is true lives entirely in
`docs/`*.

**M4. Across every round record, a fixed finding located only in `docs/` or
`seal/` is common.** 279 round records carry a `## Verdicts` table. Of their
fixed, non-🟢 findings, those whose every cited location is under one root:

| Location | Fixed findings |
|---|---|
| a shipped path (`skills/`, `agents/`, `hooks/`, `templates/`, `bin/`, `.claude-plugin/`) | 372 |
| elsewhere outside the two roots (`tests/`, `.github/`, `README.md`, …) | 278 |
| `docs/` only | 25 |
| `seal/ledger.md` or `seal/ledger/` only | 26 |
| `seal/` otherwise — the work item's own records | 48 |
| `docs/` and `seal/` together | 2 |

The 25 `docs/`-only findings come from 14 different work items. The counts are
a lower bound: a finding whose Location cell cites no backticked path is not
counted, and neither is a verdict other than `fixed`.

**What the measurement decides.** The number the issue asked for is not zero,
and it is not small where it matters. Every docs/seal-only change that reached a
reviewer produced real defects in `docs/`, and the changes that never reached
one were planning bookkeeping in a file that has since been retired. So a line
drawn at `docs/` and `seal/`, the parity arm's line, would have exempted the
only population that measured positive and bought nothing on the population
that measured empty. The measurement refuses that line.

## Open questions → questions.md

Framed 2026-09-23 by framer, before the build.
