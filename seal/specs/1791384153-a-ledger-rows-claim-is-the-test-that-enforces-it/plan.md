# Implementation Plan: a ledger row's claim is the test that enforces it

<!-- seal/specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

A ledger row may name the test that holds its claim, in pytest's own
spelling, instead of a hash over the code. Such a row never drifts: the
checker reads that the test exists, the suite reads that it passes, and
`--reverify` leaves it alone. A released row moves onto its test by one
`Corrected ·` row in the branch's fragment, written on demand where a
`Re-read ·` row would otherwise be owed, and never by a bulk pass from a
feature branch. `fold_check.py`'s own resolver of `Enforced by:` targets is
removed in favour of the ledger's. `spec.md` holds the decisions D1–D8 and
the fourteen scenarios; this file holds the order they are built in.

## Technical context

Coordinates at 5623d728, all `read` by the framer.

- `skills/evidence-check/scripts/evidence_check.py#malformed_rows` (:2049)
  refuses a grounds cell that *cites no coordinate*: its second branch fires
  when `ANCHOR_RE` and `OLD_COORD_RE` both miss and another cell is not
  empty. A node-id-only cell is exactly that today. `#refused_coordinate`
  (:1930) does not refuse `path::name` — it partitions on `#` and `@`, and a
  node id has neither — so the token is prose to the present reader.
- `#grounds_cells` (:2019) is the one table walk over Code grounds cells,
  with the fragment's column index from `LEDGER_COLUMNS` (:1896). D3's
  reader goes through it.
- `#resolve_unit` (:614): for a `.py` path, `py_spans(text).get(locator, [])`;
  `#parsed_spans` (:479) keys a method as `Class.method`, which is why a
  node id's parts after the path join with `.`.
- `#check_ledger` (:1568) assembles the findings of one file: the body walk,
  the family findings, `old_format_rows`, `malformed_rows`, `overflow_rows`.
  The node-id findings join that list.
- `#family_view` (:2451): `superseded` is every root a `Corrected ·` row
  cites; a superseded family's coordinates are not graded; the correcting
  row's own line is graded as its own family, citation excluded
  (`if cite is not None and m.span() == cite.span(): continue`). A
  `Corrected ·` row with no code coordinate therefore has nothing to grade.
  `#left_alone` (:3064) keeps `--reverify` off a superseded family. Phase 2
  verifies both by a case rather than trusting this reading.
- `#reverify_into` (:4196) writes the `Re-read ·` rows and the summary.
- `#exit_code` (:5653): BROKEN → 2; MALFORMED → 1 leniently, 2 under
  `--strict`. Unchanged.
- `skills/settle/scripts/fold_check.py#target_problem` (:262) resolves an
  `Enforced by:` target with its own `ast.walk`; `#load` (:145) is how the
  module already loads `unverified_check.py`, `hooks/config.py` and
  `hooks/optin.py`. `tests/test_a_folded_statement_names_what_enforces_it.py`
  pins the detail text *no def or class named test_gone* (:161).
- `tests/test_evidence_check.py#vendored_copy` (:345) copies the checker
  alone into `tools/`; S12 runs there.
- `docs/the-evidence-ledger.md` is 547 lines against a 1,000-line ceiling;
  `#heading_path` (:567) ends a section at the next heading of its level or
  higher, so a section inserted between two changes neither region.

**Failure scenario of the chosen approach, in six months.** A test is
reworded to assert something weaker and its row's prose still describes the
stronger claim; nothing in the tree notices, because nothing holds the prose
to the test. That is the trade the issue asks for and the one `Enforced by:`
has run under since #565 with no issue filed. What catches it is review, and
what bounds it is that the test is named in the row, so a reader opens one
file. The other direction — a test deleted — is BROKEN at the next run.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A test node id alone in the grounds cell (chosen) | The reader of a row has to open the test to find the code; a test that names nothing is a bad test rather than a bad row | taken |
| A test plus a hash-less code anchor for the reader | `path#unit` with no `@hash` is MALFORMED under `refused_coordinate` today, so it is a grammar change in #867's five copies; a pointer that resolves but never drifts still breaks on a rename and owes a `Corrected ·` row, which is the bookkeeping coming back by another door | refused |
| A test plus a hashed code anchor, drift of the anchor reported as information | The row owes a re-read on every edit exactly as now; nothing is saved | refused |
| A third citing verb (`Held ·`) for the migration | A new copy of the supersede judgment in `family_view`, `correction_check.py`, `survivor_check.py` and `settle.py`, each of which reads `Corrected` today; the brief refuses a new copy where a reader exists | refused |
| `--reverify --into` writing the `Corrected ·` test row itself where the released row cites exactly one test unit | The tool guesses which of a row's grounds is the enforcer; a row may cite a test as one ground among several. The brief prefers a reader that refuses to one that guesses. The option is printed, not written | refused |
| A bulk pass over the 1,042 released rows citing a test, in this work item | Eleven branches in 0.21.0 edit the units those rows cite; two `Corrected ·` rows on one released row are each DRIFTED at the fold, so a bulk pass from a feature branch collides with every sibling | refused; `questions.md` Q1 |
| `evidence-check` running the named test | A 1.7 s per-commit advisor becomes a test run; a consuming repository's suite is its own job | refused |
| Any `def` or `class` accepted as the enforcer, as `fold-check` accepts | A row naming a unit that exists is a claim nothing checks, the state *cites no coordinate* already refuses | refused; the ledger accepts a test, `fold-check` keeps its wider acceptance |
| A mixed row allowed, its hashes graded as today | A row reads as migrated while still owing re-reads | refused |
| Editing §*A released row is read again…* to carry the rule | 9 released rows cite that section and would drift for prose | refused; a new section is inserted after it |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
new test module's file name is the build's to choose; `spec.md`'s
scenarios call it *the new module*.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The reader: one new function in `evidence_check.py` that reads node ids from the Code grounds cell through `grounds_cells`, resolves each through `resolve_unit`'s Python branch with the parts joined by `.`, and grades OK / BROKEN / MALFORMED as D2 says; `malformed_rows` no longer refuses a node-id-only cell and refuses a mixed one (D4); `malformed_remedy` names the two forms; `check_ledger` adds the findings. S1–S6, S8 (the `--reverify` half), S11, S12 | the new module, each case seen red against the unfixed checker and the way it was shown recorded in `phases/phase-1.md`; `tests/test_evidence_check.py` and `tests/test_a_released_row_is_read_again_in_a_fragment.py` green unchanged | |
| 2 | The migration path: S7 as a case (a `Corrected ·` row with citation and node id supersedes, an edit to the root's unit produces no finding, `--reverify --into` writes no `Re-read ·` row for it), and S9's one summary sentence in `reverify_into`, pinned. If S7 needs a change in `family_view` or `left_alone`, the change is one branch and `phases/phase-2.md` says which | the cases, red with the superseding removed and with the sentence deleted | |
| 3 | One resolver: `fold_check.py#target_problem` loads `evidence_check.py` through `load` and asks it; the `ast.walk` branch is removed; S10's method spelling; the pins in `tests/test_a_folded_statement_names_what_enforces_it.py` updated in the same commit; the 451 targets under `docs/` measured green by `fold-check` | that module red with the old resolver restored; `fold-check` over the tree green | |
| 4 | The documents (D7): the new section in `docs/the-evidence-ledger.md` with `Enforced by:` lines naming phases 1–3's cases, `templates/ledger.md`'s two forms, the two sections of `skills/evidence-check/SKILL.md`, and `skills/evidence-ci/SKILL.md` §*Updating later*; a pin per changed sentence; the text hygiene modules green | `fold-check`; the pins red with the sentence removed; `tests/test_docs_line_wrap.py` and the five text hygiene modules green | |
| 5 | This item's records (D8): the fragment's test rows for S1–S13, the citing rows for every released row phases 1–4 drifted — per row the `Corrected ·` test row or the `Re-read ·` row, chosen by reading (Q3) — `changelog.md`, and `overview.md` | `evidence-check --strict .` 0 drifted, exit 0, executed and its output in `phases/phase-5.md` | |

**Order, and why.** Phase 1 before 2 because S7's `Corrected ·` row holds a
node id the reader must accept first. Phase 3 after 1 because it imports
what 1 writes. Phase 4 after 3 because its `Enforced by:` lines name cases
that must exist. Phase 5 last because it reads the hashes phases 1–4 leave.

**Sequencing with the siblings.** #867 and #870 edit `evidence_check.py`;
`spec.md` §*The seam* names the units this item changes and the ones it
only reads. Whichever of the three lands second in `release/v0.21.0` merges
the release branch in and re-runs phase 5's `--strict`; the conflict
surface is `malformed_rows` and `check_ledger`, which #867 may touch for the
grammar and #870 should not.

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

- **No migration of any released file.** The freeze stands; released rows
  move onto their tests one `Corrected ·` row at a time, on demand.
- **A consuming repository changes nothing** until it writes a test row,
  and then it updates its vendored `tools/evidence_check.py` first, or the
  older copy refuses the row as MALFORMED (`skills/evidence-ci/SKILL.md`
  §*Updating later*). No new environment variable, no new dependency.
- **What a gate prints changes in two places**, each pinned: the new
  MALFORMED and BROKEN details for a node id, and one summary sentence of
  `--reverify --into`.
- **Prompt budget: zero.** Nothing here asks a person anything; every new
  verdict is a refusal a person reads at exit 1 or 2.
- **Failure direction: blocks more**, on rows that do not exist in any
  ledger today (measured: no Code grounds cell holds a `path::name` token).
