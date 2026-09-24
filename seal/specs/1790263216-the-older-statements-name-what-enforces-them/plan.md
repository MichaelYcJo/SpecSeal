# Implementation Plan: the older statements name what enforces them (#565)

<!-- seal/specs/1790263216-the-older-statements-name-what-enforces-them/plan.md
     HOW, in phases. Reading this plan and spawning `smith` is the approval. -->

Approved 2026-09-25 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.
Q1 builds on its default.

## Summary

Give each of the 115 statements `fold-check --shape-from 0` names a single
`Enforced by:` line, chosen by `spec.md` §*What a decision is*, and a bold
opening where one of the 26 lacks it. Then lower `Fold shape from` to `0`,
so that the suite's real-tree case holds every statement from then on. Six
phases take the documents in subject groups, so the code behind each group
is read once. The seventh flips the cutoff, and it can only pass when
nothing is left.

## Technical context

**What the build reads with, all on this branch from the stacked item:**

- `skills/settle/scripts/fold_check.py#shape_problems`, `#names_targets`,
  `#target_problem`, `#numbered_statements`, `#enforced_lines` — the shape,
  what counts as a target line, how a target resolves, where a statement's
  span ends, and which lines the wrap limit skips. `bin/fold-check` runs it.
- `tests/test_a_folded_statement_names_what_enforces_it.py#test_every_bound_statement_in_docs_has_the_shape`
  — the real-tree case, at the configured cutoff. After phase 7 it binds
  all 136.
- `tests/test_a_document_has_room_for_the_next_fold.py#prose_disagreements`
  — reads ``from work item `(\d+)` on`` and ``at or under ([\d,]+) lines``
  out of `docs/the-evidence-ledger.md` §*The fold …*.
- `tests/test_both_editions_carry_the_same_folds.py` — pairs heading
  levels and marker multisets per heading position; phase 6 extends it.
- `tests/test_docs_line_wrap.py#prose_lines` — 88 columns over `COVERED`,
  skipping lines `enforced_lines` returns.

**How a target is found, per statement** — cheapest source first, stopping
at the first that names a unit which catches the breaking edit:

1. The statement's own grounds. Many already name the script, the case or
   the issue (`the-broad-gate`'s statements name their tests by file).
2. The marker's work item, through history. The marker holds the whole
   directory name, and the fold deleted that directory, so
   `c=$(git -C <wt> log --format=%h --diff-filter=D -1 -- seal/specs/<marker>/spec.md)`
   finds the fold's commit, and `git -C <wt> show "$c^:seal/specs/<marker>/spec.md"`
   gives the spec as it stood — its scenarios and their *Verifiable how*
   column, which usually names the case. Executed 2026-09-25 on three
   markers from three folds (`1788302682-…`, `1790076060-…`,
   `1788331011-…`): each spec came back, naming 3, 8 and 10 test or
   scenario lines. A work item that wrote no `spec.md` has no rule by
   `docs/the-evidence-ledger.md`'s own statement and carries no marker, so
   a marker should have one; where the command returns nothing, go to 3.
3. `grep -rn` for the script or function the rule is about, across
   `tests/`, to find the case that plants the violation.

Then, for each statement, write one row of the phase record:
`| Statement (doc §heading · marker) | Its rule, short | The edit that breaks it | Target, or nothing-case 1–4 | Executed? |`.
Keep the rows as they are settled and write the document's lines in one
edit pass per document (`implement` §2, *draft as you go*), not one edit
per line.

**Failure scenario of the chosen approach, six months out.** A target keeps
resolving after the case it names is rewritten to assert something else.
`fold-check` checks resolution only, so nothing notices. The line then
claims an enforcement that stopped. This is accepted rather than solved: the
same is true of the 21 lines already bound, and whether a target really
enforces is review's by `settle` §2. What the design does catch is the
commoner rot — a renamed or deleted case or function — because at cutoff
`0` the real-tree case fails on the next suite run. The second accepted
cost: `nothing — no case reads it yet` lines can accumulate. They are
listed by `grep -rn 'Enforced by: nothing' docs/`, in the document a
reader is already in, the way a `# RIDER:` is.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Keep the cutoff at `1790154761` after the retrofit | A later edit deletes a retrofitted line and nothing notices. The prose sentence *one folded before it has not* is false the moment the retrofit lands | rejected |
| Delete the `Fold shape from` row | Absent means *not declared*, which turns the shape check off for all 136, including the 21 bound today | rejected |
| Bind per document, or step the cutoff down as phases close | The cutoff is an id comparison, and ids do not follow documents. Per-document binding is a new config shape, which is mechanism this item does not need | rejected |
| One phase per document (14) | Fourteen phase records and boundaries, and the code behind a subject is re-read for each of its documents | rejected |
| One phase for everything | No calibration. The criteria meet 106 decisions at once, and a wrong reading of them is found by review after all 106 | rejected |
| Split a long statement into several, each with a marker | Adds markers, which changes the multiset the editions test pairs and the count the fold record holds, and rewrites ratified structure for a ticket that asks for a decision | rejected |
| Write a case for every rule nothing reads | Turns 115 decisions into an unknown number of new checks and review rounds. #565 asks what enforces each statement; `nothing — <why>` answers that honestly | rejected |
| A ledger row per decision | A second copy of what the `Enforced by:` line already records, in the document, and `fold-check` already resolves | rejected |
| Leave the Korean lines unpaired | Nine lines no reader compares, in a mirror `CONTRIBUTING.md` already says drifts one edit at a time | rejected |
| **Six subject-grouped phases, then the cutoff to `0`** | See *Failure scenario* above | **chosen** |

## Phases

Each phase is one vertical slice: its documents come out of
`fold-check --shape-from 0`'s output, their named cases run and pass, and
the ledger rows their edits drift are re-stamped. **Every phase's Verified
by includes the common checks below, and names only what it adds.**

**Common checks, run at every phase boundary** — one command each, not
repeated per document:

- `bin/fold-check --shape-from 0 2>&1 | grep -E '^docs/(<the phase's documents>)'`
  prints nothing, and the total problem count dropped by exactly the
  phase's statements plus its bold openings.
- `bin/fold-check` exits 0 (the 21 bound statements still hold, and no
  document is over 1000 lines).
- `bin/test <every test node id the phase named as a target> tests/test_docs_line_wrap.py tests/test_a_folded_statement_names_what_enforces_it.py -q`
  in one command: every target is collected and passes.
- `bin/evidence-check .`: every row it names DRIFTED is re-read against the
  edit and re-stamped in the file it is in, with a dated `Re-read` note, and
  the run after that names none. A BROKEN row means a quoted anchor line was
  reworded, which `spec.md` §*Data & interfaces* forbids: restore the line.
- At least three mutations recorded in `phases/phase-N.md` — break the rule
  the way the row says, see the target go red, restore — plus one for every
  decision whose tie the builder could not state in one sentence.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **`docs/the-evidence-ledger.md`**, 16 statements. The calibration phase: the fold's own subject, whose code (`fold_check.py`, `settle.py`, `unverified_check.py`, `evidence_check.py`) the builder reads first anyway. Its phase record fixes the per-decision table's shape for the phases after it. The first statement of §*The fold …* is already bound and is phase 7's | common checks; `bin/test tests/test_a_document_has_room_for_the_next_fold.py -q` still passes, since this section holds the pin's text | 5beeaa90 |
| 2 | **`docs/round-record-spec.md`**, 16 statements, 2 bold openings. The round-record generator and `chain_check.py`'s record reading | common checks; the document is at most 945 lines | 48a6d6a3 |
| 3 | **`docs/review-chain-spec.md`** (9, 2 bold) **and `docs/commit-review-gate-spec.md`** (8, 4 bold). The review cycle and the commit gate, read together because the second was split out of the first (#526) | common checks; `review-chain-spec.md` is at most 963 lines | 03265a16 |
| 4 | **`docs/review-handoff-protocol.md`** (4, 3 bold), **`docs/measuring-a-run.md`** (10), **`docs/the-agent-set.md`** (6). Agents, handoffs and measurement, where cases 1 and 3 of `nothing` are most likely | common checks; the `0.8.2` quoted anchor into `review-handoff-protocol.md` still resolves | 4138dac5 |
| 5 | **`docs/the-broad-gate.md`** (11), **`docs/release-checklist.md`** (6, 2 bold), **`docs/branch-and-release.md`** (4, 2 bold). The gate, the release and the branch rules; case 2 of `nothing` (the rulesets) lives here | common checks; the `0.4.0` quoted anchor into `branch-and-release.md` still resolves | f0f99da4 |
| 6 | **`docs/issues-and-milestones.md`** (5, 3 bold), **`docs/worktree-guard-spec.md`** (2, 2 bold), **`docs/one-root-by-lifetime.md` and `.ko.md`** (9 and 9, 3 bold each), and **the editions test compares `Enforced by:` values** (`spec.md` §*Scope* item 4). The Korean lines copy the English targets byte for byte; a `nothing` reason is Korean | common checks over all four documents; the new case shown red first, by a planted pair whose targets differ, and the real-tree case passes; `bin/test tests/test_both_editions_carry_the_same_folds.py -q` | 4856c2cf |
| 7 | **The cutoff is `0`.** `seal/config.md`'s `Fold shape from` row, `docs/the-evidence-ledger.md` §*The fold …*'s first two statements, and the two test docstrings, in one commit (`spec.md` §*Scope* item 3). Then `bin/fold-check --shape-from 0` over the whole tree | S1, S2: `bin/fold-check` and `bin/fold-check --shape-from 0` both exit 0, reading 136 and binding 136. S3: `bin/test tests/test_a_document_has_room_for_the_next_fold.py tests/test_a_folded_statement_names_what_enforces_it.py -q`. S4: one retrofitted line deleted, `test_every_bound_statement_in_docs_has_the_shape` seen red, restored. `bin/evidence-check .` clean, including the stacked fragment's rows | 835268a4 |

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

## Operational impact

- **Nothing a plugin user runs changes.** `fold_check.py`, the templates and
  the skills are untouched. What changes is this repository's `docs/`, one
  config row, and three test modules (two docstrings, one new comparison).
- **The suite gets stricter.** After phase 7 the real-tree case binds all
  136 statements, so a later branch that deletes an `Enforced by:` line or
  renames a function one names goes red. That is the point of phase 7.
- **Stacked branch.** This branch sits on
  `fix/566-the-fold-checks-run-only-as-this-repositorys-tests` (PR #587).
  When #587 squashes into `release/v0.15.3`, this branch takes the release
  branch by a merge and not a rebase: a rebase orphans the Status column's
  commits, as the caveat above says.
- **Sibling chains C, D, E and F** edit documents and functions this branch
  names (`spec.md` §*Data & interfaces*, *Siblings*). After any merge of the
  release branch into this one, `bin/fold-check --shape-from 0` runs again
  over the merged tree. A target a sibling renamed is repointed to the new
  name after re-reading, never replaced by `nothing`.
- **Changelog.** `seal/specs/1790263216-the-older-statements-name-what-enforces-them/changelog.md`,
  one entry: every folded statement names what enforces it, and the shape
  now binds all of them.
