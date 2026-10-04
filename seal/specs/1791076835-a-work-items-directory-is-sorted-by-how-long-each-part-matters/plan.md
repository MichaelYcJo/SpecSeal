# Implementation Plan: a work item's directory is sorted by how long each part matters (#729)

<!-- seal/specs/1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

A work item's directory keeps its paths. What changes is when its process
record leaves: `settle --retire-process` removes `rounds/`, `phases/`,
`survivors.md` and the other files written only for a pull request from every
released work item, without waiting for the fold, while `routing.md` and the
SDD set stay until the fold retires the directory (spec D1–D5). The documents
that state how long a work item's records stay are brought into line, and
`docs/the-record-layout.md` marks F3 built (D6).

## Technical context

- `skills/settle/scripts/settle.py` — `released` (the directory is present at
  `--released-at`), `open_items` (evidence-todo guard, via
  `unverified_check.py#todo_open_rows`), `anchored_rows`, `citations`,
  `retire` (the shape of a removal arm: candidate set read from the tree,
  per-directory guards, `removed …` lines, a closing count, exit 1 when
  anything was kept), `report` (the dry run's sections), `main` (the flags).
  The new arm is a sibling of `retire`, not a branch inside it.
- `skills/code-review/scripts/survivor_check.py#records_a_past_state` — the
  class the arm removes three members of. The arm does not import it to
  decide what to remove (a destructive allow-list is spelled where it acts),
  but a case pins that the two agree on those three members, so neither can
  drift alone.
- `skills/code-review/scripts/chain_check.py#changed_routing` — selects items
  by a changed `routing.md` only; the reason a drop range judges nothing.
- `skills/verify/scripts/unverified_check.py` `--baseline` — counts
  `overview.md` rows; the drop removes none.
- Existing cases to build beside: `tests/test_settle_reads_before_it_removes.py`
  (scratch-repository builders for released items, the local-mode refusal,
  the anchored-row guard).
- The branch merges `origin/release/v0.18.1` in (merge, never rebase) before
  building, after the wave-1 branches squash. #728 edits
  `docs/the-record-layout.md` in parallel: touch only the F3 paragraph and the
  one line under the `seal/specs/<work-item-id>/` table.

**What breaks in six months.** A new file kind starts being written into a
work item for its pull request (a new todo, a new mirror). The allow-list does
not name it, so the arm keeps it and prints it under *not a process record*
on every run. That is the loud direction on purpose: the line is the prompt
to add it to the list in the same change that introduced it, and a file that
was in fact durable is never lost.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Regroup the process record under one subdirectory (`run/`) | Every reader and 57 test files move with no fallback (the protocol forbids a dual read); the gain is a listing that `rounds/` and `phases/` already give | Rejected (D1) |
| One file per run | 41 of 53 runs exceed the 64 KB a reader takes whole; `Fixes checked by` names a `round-N` file | Rejected (D2) |
| Leave everything to the fold (no change; document the lifetimes only) | The fold has not run since 2026-09-24; 525 files that no reader needs wait seven releases on a judgment they do not need | The fallback cut, not the plan |
| Drop the process record in the release-preparation commit (step 2) | That commit is gather, fold and bump only, and #728 is reshaping it this release; and dropping a release's own records before its pull request into `main` fails `chain_check` and empties `release_seal`'s counts | Rejected |
| Drop at merge into the release branch | Same: the release pull request and the release seal still read the records | Rejected |
| A hook or CI job that drops automatically | `settle` is invoked, never triggered (`skills/settle/SKILL.md` §*When it runs*) | Rejected |
| Fold `--retire-process` into `--retire` | `--retire` is "the second half of the fold and never its own act"; one flag with two meanings makes that sentence false | Rejected: a flag of its own |
| Drop `routing.md` with the process record | `chain_check#main` refuses a removed `routing.md` beside a standing `spec.md` unless folded or retired by the rule | Rejected (D4) |
| A cutoff exempting the 55 released items, by the ledger freeze's precedent | The freeze's grounds (anchored citations, parallel re-stamps) do not hold for round records; `--retire` has no cutoff | Rejected (D5) |
| **`settle --retire-process`, at step 2b, every released item, allow-list, `--retire`'s guards** | A new pull-request-only file kind is printed as kept until it is listed | **Chosen** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `settle --retire-process` (spec D3, D4; S1–S4, S8, S9) and the dry-run section (S10), with `skills/settle/SKILL.md`'s section for the arm, its output and its guards, in the same commit as the strings it pins | new cases in `tests/test_settle_reads_before_it_removes.py` (or a sibling file), each seen red against the unbuilt flag or with the pinned sentence removed; that module run alone | d6753af8 |
| 2 | The readers accept a drop (S5–S7): a scratch repository whose range removes a released item's process record passes `chain_check.py`, `survivor_check.py --range` and `unverified_check.py --baseline`; the variant that also removes `routing.md` fails `chain_check`. A case pins that the arm's leave-list and `records_a_past_state` agree on `rounds/`, `phases/` and `survivors.md`. Any reader that refuses is fixed here | the new cases and the modules of the three checkers' own tests | |
| 3 | The carriers of spec D6: `docs/the-record-layout.md` (F3 built; the lifetime line), `docs/release-checklist.md` §2b, `docs/review-handoff-protocol.md`, `docs/one-root-by-lifetime.md` and `.ko.md` (one appended *Decided when* section), `skills/implement/SKILL.md`, `agents/framer.md`, `survivor_check.py`'s two docstrings, `seal/README.md`; the pins that follow any test-pinned sentence; `changelog.md` fragment and `seal/ledger/1791076835-….md` rows | S11's `grep` over D6's phrases returns only the new wording; the tests that pin the edited documents, run by module | |

**The fallback cut line.** If the review run nears its cap with phase 1 or 2
unsettled, the arm is withdrawn whole and phase 3 ships in its minimal form:
`docs/the-record-layout.md` states the two lifetimes as they hold today (the
process record leaves with the directory when `settle --retire` takes it),
F3 reads *decided: the paths stay; the process record leaves with the
directory*, and the early drop is filed as a follow-up issue naming this
spec's D3–D5. Nothing in the tree then claims a command that does not exist.
Phases 1 and 2 are not separable from each other: a drop the readers have not
been shown to accept is not shipped.

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

- A new flag on a shipped command (`settle --retire-process`); `bin/settle`
  needs no change. No new dependency, no config row, no template change.
- A repository that updates the plugin gains a release-checklist act that
  removes files. Nothing runs it automatically, and `settle` with no flag
  shows what it would remove first.
- The first run in this repository (0.18.1's step 2b or later) removes about
  525 files from 55 directories in its own `[no-review]` pull request. It is
  not part of this work item.
