# Implementation Plan: folded statements pile into one spec (#520)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-23 by the orchestrating session, under the owner's `automation` preset, when `smith` was spawned.

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

The work writes three rules into the fold's procedure, and adds three
repository tests that read them. The Korean design record gets the one section
and ten markers it is missing. Nothing in the existing 101 folded statements is
rewritten, and the chain spec is not split. `spec.md` §Scope carries what is in
and out, and the home of each deferral.

## Technical context

- **The marker reader is shared.**
  `skills/verify/scripts/unverified_check.py#FOLD_MARKER` and `#live_lines`
  are the one rule for a live marker, which
  `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*
  requires. `#folded_items` shows the walk: the top level of `docs/`, `*.md`
  only, live lines only. The three new tests import these rather than defining
  a regex of their own.
- **There is a precedent for a paired-edition case.**
  `tests/test_settle_reads_before_it_removes.py#test_both_editions_took_the_same_decisions`
  compares a cell count, and it stays. The new pairing test is the general
  form, and that case is one section's content-level pin.
- **There is a precedent for a cutoff by work-item id.** Fold 1's phase 2
  (`f51e634d`, #504) made the cutoff constants F9 and F10 traceable. Work-item
  ids are epoch-prefixed, so `int(id.split("-")[0]) >= 1790154761` is the
  whole comparison.
- **There is a precedent for an exception list that cannot outlive its
  reason.** `tests/test_no_document_names_the_old_roots.py#KEEP` asserts that
  each entry still occurs. `OVER_CEILING` does the same with "still exceeds".
- **The failure scenario of the chosen approach, six months out.** The
  over-list is still there because nobody split the chain spec, so the chain
  spec is frozen at 29 markers. Each fold then places chain rules into smaller
  documents it creates for sub-subjects, and `docs/` fragments by fold rather
  than by design. The mitigation is that the split issue is filed before phase
  3 and is the over-list entry's home. Removing the entry is the only way the
  count moves, so the fragmentation is visible at every fold's pull request
  rather than silent.
- **A second failure scenario: `Enforced by: nothing — …` becomes the
  default.** A folder can always write it. The check makes the choice visible
  and greppable, and it cannot make the choice correct. The standing text says
  so, and a reviewer reads those lines first.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Split `docs/review-chain-spec.md` now, along the issue's four axes | The `commit-review-gate` section (lines 431–1,860) holds the record field rules and has no inner `##` to split on, so it stays at about 1,430 lines. The 47-file surface collides with 12 files of open PR #525, and with any sibling that cites the chain spec. The split also holds nothing: the next fold piles into whichever piece is nearest | rejected for 0.14.0 and deferred with a home. The ceiling does the holding |
| Freeze the chain spec's **line** count instead of its marker count | #525 adds 14 lines to it and is not a fold, so a line freeze turns an unrelated sibling red. The marker is what only a fold adds | rejected |
| Give the shape check a git baseline (`--baseline origin/<base>`, new markers only) | This needs a workflow step and a base ref, and a test run outside CI has no base. It also adds a second mode to a reader #525 is rewriting | rejected in favour of the id cutoff, which needs no git |
| Grandfather the 101 markers with an explicit list of 92 ids | A 92-entry list is one more thing to keep in step, and the ids already carry their order | rejected |
| Retrofit `Enforced by:` onto all 101 statements now | This is 101 enforcer judgments, 29 of them in a file #525 edits, and it is the size of a fold | deferred to the split issue as a second item |
| Retire `docs/one-root-by-lifetime.ko.md` | Five test modules pin it. `CONTRIBUTING.md` puts Korean in human-facing documents. The owner kept it through 2026-09-22, and PR #525 extends both editions by hand today. Retiring content a person reads is the owner's call, and the tree points the other way | rejected by the tree. questions.md Q1 records it as the owner's to overturn |
| Pair the editions on the number of headings only | A marker can move to a different section in one edition and the counts still match | rejected. The check pairs per heading position |
| Ship the checks as a `settle --check` mode or a new `bin/` command | `settle.py` is +468 lines in #525. A new command brings a wrapper, README rows and release-check listing | deferred to the split issue. The tests ship now |

## Phases

Each phase ends with its tests executed narrowly, and the broad gate is the
sealer's. Each phase commits as soon as it stands on its own.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The editions are paired.** `tests/test_both_editions_carry_the_same_folds.py`: for every top-level `docs/X.ko.md` with a `docs/X.md`, the sequences of live-heading levels are equal, and each heading position has the same multiset of fold-marker ids. It asserts at least one pair was read. Seen red at the base (10 ids against 0) before any prose. Then `docs/one-root-by-lifetime.ko.md` gains a Korean §*What the repository decides for itself, and how it is read*, at the English position between §*순서* and §*범위 밖*, with its 5 markers, plus the other 5 markers at their matching headings. `CONTRIBUTING.md`'s *Both READMEs move together* widens to any document with a `.ko.md` edition and names the new test | the new module, executed red then green, and `test_settle_reads_before_it_removes`, `test_first_setup_asks_once`, `test_no_document_names_the_old_roots`, `test_unverified_rows_close`, `test_release_hygiene`, `test_docs_line_wrap`, all executed narrowly | e491b63e |
| 2 | **A folded statement has a shape.** `skills/settle/SKILL.md` §2 gains the shape rule: bold rule sentence, then grounds, then one `Enforced by:` line naming paths or `path::name`, or `nothing — <why>`. It says a stacked marker group shares one statement, that the plugin ships no checker for it, and that a contradiction between two statements is review's to find. `tests/test_a_folded_statement_names_what_enforces_it.py`: for markers with id ≥ `SHAPE_CUTOFF = 1790154761`, a bold opening line, exactly one live `Enforced by:` line, and every target resolves (the file exists, and `::name` is a `def` or `class` in it, found by `ast`). The fixture cases are A4–A6, each seen red, and A7 runs over the real `docs/` | the new module, executed, with each fixture case shown red by deleting the line it pins. `test_settle_reads_before_it_removes` is executed, because it reads settle's text || c43ffedf |
| 3 | **A document has a ceiling.** Before the phase starts, the orchestrator files the split issue (Q3) and hands over its number. Settle §2 gains the placement rule: one subject, one document, and a document the repository has put over its ceiling takes no new statement, so the fold splits it along its own headings or places the rule in the sub-subject's document. `docs/the-evidence-ledger.md` §*The fold…* links to settle §2 and states `LINE_CEILING = 1000`, the over-list with its home, and `SHAPE_CUTOFF`. `tests/test_a_document_has_room_for_the_next_fold.py` covers A8–A10, and one case pins the prose values against the constants. If #525 has merged, rebase onto `release/v0.14.0` first | the new module, executed, A8–A10 seen red, the prose-against-constants pin seen red by editing the number. `test_the_rules_have_one_owner` and `test_docs_line_wrap` executed || 24a001f1 |
| 4 | **The work item closes.** `changelog.md` fragment, `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md` rows (the three test modules' units, settle §2, the evidence-ledger paragraph, the Korean section), and `overview.md` with `## Not verified` (the broad gate, answered by the sealer) | `evidence-check --strict .` executed on the fragment, and `unverified-check` executed on the overview | |

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

- **The 0.14.0 fold is the first one bound by these rules.** It cannot add a
  marker to `docs/review-chain-spec.md`. The release checklist's fold step
  needs no edit, because settle §2 is what the folder reads.
- **Work items created after `1790154761` fold with an `Enforced by:` line.**
  Two 0.14.0 siblings have smaller ids and fold without one: #515
  (`1790134781`) and #517 (`1790138190`). #518 and #519 have no branch yet,
  so a work item opened for either one gets a larger id and folds under the
  shape. That is intended.
- **No new dependency, command, environment variable or workflow step.** The
  three tests run inside `bin/test`, which CI already runs.
