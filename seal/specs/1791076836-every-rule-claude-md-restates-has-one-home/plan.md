# Implementation Plan: every rule CLAUDE.md restates has one home (#730)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
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

The work runs in two phases.
- **Phase 1** gives the three rules one home each. Their `CLAUDE.md` rows become link rows in the shape of spec D2, and so does the goal section's batch sentence. Four code comments are repointed, and the per-rule pin is added.
- **Phase 2** ships the method. It adds a repository-wide verbatim ratchet whose baseline is measured on phase 1's tree, rewrites `docs/the-record-layout.md`'s F4 paragraph to say F4 is built, and writes the closing records.

Phase 1 has to come first because it removes one of the pairs the baseline would otherwise record: `CLAUDE.md` ↔ `docs/branch-and-release.md`.

## Technical context

- **Before building:** run `git -C <worktree> fetch origin`, then `git -C <worktree> merge origin/release/v0.18.1`. Merge, never rebase. Do this after the wave-1 branches of 0.18.1 have squashed. #728 and #729 edit `docs/the-record-layout.md` in this release. Read that file after the merge, so that the F4 paragraph is edited as it then stands.
- **The homes, at e141980a:**
  - merge: `docs/branch-and-release.md` §*Work accumulates on a release branch*, the *Which button, for each direction* table (lines 117–135);
  - identifiers: `CONTRIBUTING.md` §*House rules*, the *No real identifiers* bullet (lines 261–263);
  - cadence: `skills/implement/SKILL.md` §*2. Implement, and feed evidence back where you verified it*, at *Commit at the smallest step…* (line 299 onward).
- **Constraints the build must keep:**
  - `tests/test_the_ledger_rules_have_one_home.py::test_the_two_first_reads_link_each_rule_to_its_home` reads `CLAUDE.md`'s *Commit freely* paragraph and its fragment row. Both stay word for word.
  - `CLAUDE.md`'s generated region is not touched. `claude_block.py --check` holds it.
  - The three repo-local row headings in `CLAUDE.md` keep their text, because they are cited by heading. The only exception is a heading whose rewording the warden asks for.
  - `tests/test_a_moved_rule_leaves_its_definition.py`'s `WINDOW` gets one source.
- **What breaks in six months.**
  - *The ratchet.* It holds copies at their current count and no lower. If the remainder issue is never worked, the baseline stays at 99 pairs for good, and the check only stops new pastes. That is still its purpose, and the pairs stay visible in the module.
  - *The link rows.* A change to a rule's *values* (a seventh merge direction, a second fixture domain) has to update both the home and the row. Only the home's sentences are pinned, so a stale value in a row is caught by a reviewer and not by a check (spec D2). That gap is narrower than the one D1 measured, because a value in one sentence is easier to see than a whole table that has drifted.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Link row = path + section only** | A session that holds only `CLAUDE.md` has no trigger and no act. It merges or writes a fixture without opening the home, which is exactly the moment the rule was written for. | Rejected. Spec D2 takes path + trigger + one act sentence |
| **Keep the restatements, and pin each copy against its home** | #715's docstring: a pin that holds two copies equal *kept them equal and kept them both*. D1 shows the merge copy has already gone stale where nothing pinned it. | Rejected |
| **Extend `test_the_ledger_rules_have_one_home.py` with the three rules** | Its name and docstring say *ledger and fragment rules*. Adding the merge method makes the module describe itself falsely. | Rejected. Sibling module in the same shape (D4) |
| **One-off sweep only, with the result recorded** | The list rots on the day it is written (contract §7). The next paste lands green, as #107, #292, #715 and D1's merge table did. | Rejected as the *only* answer. It is kept for the paraphrase half (D6) |
| **Semantic similarity as a check** | At any threshold that catches a paraphrase, it also matches links against their headings and table rows against their prose. Each false red needs a person's judgment. Recall on #730's own three rules was 0 of 3. | Rejected. It runs once (D6) |
| **Zero-tolerance verbatim check, after this work fixes all 219 runs** | About 50 files of rewording under the review cap, most of it in the review-chain documents, where choosing which copy is the rule is a substantive decision. It conflicts with every sibling branch of the release. | Rejected. Ratchet + remainder issue (D5, D7) |
| **Exact baseline: the check fails when a count drops and the baseline is not lowered** | Every branch that touches a duplicated passage has to edit the one baseline table, which is the shared-file conflict the fragment rule exists to stop. | Rejected. Fail on increase only. The slack is stated in D5 |
| **Baseline as one repository-wide total** | A drop in one pair hides a paste in another. | Rejected. Per pair |
| **Chosen: verbatim ratchet per file pair at `WINDOW` = 15, link rows in D2's shape, paraphrase pass recorded once, one remainder issue** | It does not catch a paraphrase (1 of 3 known restatements is a verbatim copy). A pair that has drained can take a later copy up to its old count. | Chosen |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **Three rules, one home each.** After the merge-in, `CLAUDE.md`'s merge, identifiers and commit rows become link rows (spec D2, D3), and the goal section's batch sentence folds into its §1 link (Scope 4). `CONTRIBUTING.md`'s *No real identifiers* bullet gains the history-rewrite reason. The four code comments from Scope 2 cite `CONTRIBUTING.md` §*House rules*. The sibling pin module (D4) is added, and its needles come from the homes as they stand after the edit. | `bin/test` on the D4 module, `tests/test_the_ledger_rules_have_one_home.py`, `tests/test_the_claude_md_block_has_one_source.py`, `tests/test_no_real_identifiers.py`, and the four modules whose comments moved. The D4 module is seen red with a needle planted in `CLAUDE.md`, and seen red with a link removed. `python3 .github/scripts/claude_block.py --check` exits 0. S5's grep is empty. | 9e2dbbdf |
| 2 | **The method ships.** The ratchet module (D5) has its corpus, normalisation (wrapped section names included), `WINDOW` from one source, the baseline measured on phase 1's tree with the sanctioned preamble marked, and a failure message that names the act. The F4 paragraph of `docs/the-record-layout.md` is rewritten (D8), with *the remainder issue* left as a placeholder until the orchestrator gives it a number. Then the closing records: ledger fragment rows, `changelog.md`, `overview.md`, and the `phases/phase-N.md` files. | `bin/test` on the ratchet module. It is seen red against a planted paste, and it stays green against a planted deletion (S6, S7). Its measured counts are printed beside the baseline and are equal to it (S8). `tests/test_docs_line_wrap.py`, `tests/test_a_document_has_room_for_the_next_fold.py` and `bin/fold-check` run on the touched document. `git diff <base> -- docs/the-record-layout.md` stays inside the F4 paragraph (S9). | |

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

- **One new CI failure mode.** A contributor whose pull request pastes 15 or more words from one rule document into another gets a red test. The message names the pair and the act. No `CONTRIBUTING.md` bullet announces it (spec O6).
- No hook, workflow, config row, dependency or install change. `CLAUDE.md`'s distributed block is untouched, so nothing changes for installed users.
- The orchestrator files one issue, the remainder (spec D7), from the clusters and the paraphrase table in `spec.md`, and gives its number to the F4 paragraph before the pull request is marked ready.
