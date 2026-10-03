# Implementation Plan: the commit gate's policy is cut into files by question (#727)

<!-- seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

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

`docs/commit-review-gate-spec.md` (1,047 lines) is cut along its headings into
three files, as `docs/the-record-layout.md` F1 decided. The moved text moves
byte for byte. What follows the move is everything that reads the text: the
fold freeze in `seal/config.md` and its prose pin, 14 test files, the
references in other files that `spec.md` K5 lists, and the ledger. `spec.md` §*The classes,
enumerated* lists each class by the command that produces it. This plan says
in which order they move and how each step is shown.

## Technical context

**What this builds on, every line read at 2b1dcb1f.**

- **The cut lines.** `docs/commit-review-gate-spec.md` headings at 41, 194,
  268 (inside git), 278 (PreToolUse), 760, 805, 833, 955 (arms) and 995, 1018
  (guards).
- **The freeze.** `seal/config.md` row 13 freezes the document at 18 markers,
  digest `cb5d441b51a4`.
- **What fails while the two disagree.** `skills/settle/scripts/fold_check.py#ceiling_problems`
  fails a listed file that is back under the ceiling.
  `tests/test_a_document_has_room_for_the_next_fold.py#prose_disagreements`
  holds `docs/the-evidence-ledger.md` §*The fold, and what tells it from a
  deletion* equal to the row.
- **How a heading's unit ends.** `skills/evidence-check/scripts/evidence_check.py`'s
  heading walk gives a heading everything down to the next heading at its
  level or above. That is why E9's `## commit-review-gate (PreToolUse, Bash)`
  drifts when the `###` arms leave from under it, while G5's `## Registration`
  and the `#### A \`cd\`` rows do not.
- **What survivor-check subtracts.** `skills/code-review/scripts/survivor_check.py#corrected`
  subtracts what the range added, so a verbatim move reports nothing and only
  the reworded lines can.

**The failure scenario of the chosen approach, six months on.** The parent is
the largest part, at about 585 lines, and the PreToolUse reading is where
#716-style fixes keep landing. A few more folds take it back toward the
ceiling. When they do, the next cut follows its own headings (§*Which
repository, and what happens when it cannot be read*, §*Why a deny*) and this
work's preamble index takes one more line. What does not break is the move
itself. Every anchor that moved is re-pointed by a row the checker reads, and
every citation names the file that holds its heading.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Move verbatim at the original heading levels, add an H1, an `Authority for` paragraph and, in the arms file, one `##` wrapper (D2, D3) | The arms file reads H1 → `##` (new) → `###` (moved). That is a little deeper than the file needs, and nothing checks heading depth | **chosen** |
| Promote the arms headings to `##` and reflow the moved paragraphs | Every moved unit's hash changes, so a `Corrected ·` row can no longer show that the content is the same. `tests/test_chain_hooks_hardening.py` and `tests/test_the_reopening_is_one.py` slice on `### Review arm`, `#### The declaration …` and `### Parity arm`, and would need new markers. Survivor-check reads every reworded heading as a correction to chase | rejected |
| Re-point only the `§*…*` citations and leave bare path mentions | `hooks/routing.py` would still say the parent *refuses to build* a standing waiver that the parent no longer mentions. A reader opens the wrong file, and the next split makes it two hops. #526's S2 rule is that the holder is cited | rejected (D6) |
| Leave stub headings in the parent saying *moved to …* | The old ledger anchors resolve to the stub and read DRIFTED, not BROKEN. The tool then asks for a re-read where a re-point is owed, and the move goes invisible to the one reader built to see it. Two files would also carry one heading | rejected |
| Delete the `Over the ceiling` row instead of writing `none` | An absent row is *not declared*, and `fold-check` stops checking that half, saying so in one line. #526 kept the listing, empty | rejected (D8) |
| Land the move and the config row in separate commits | Between them, `fold-check` fails the entry, or the moved document is over the ceiling unlisted, and the K2 tests read text that has left. No intermediate commit stands on its own | rejected |
| A permanent `§*…*` citation resolver as a test | It is new mechanism, which is outside a move's scope. #526 verified its citations with a one-off script | rejected (D11) |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The cut, in one commit.** (a) Write `docs/the-commit-gate-inside-git.md` and `docs/the-review-and-parity-arms.md` from base lines 41–277 and 760–994 with a script that asserts each boundary line's text before it copies (the heading at the first line of each range, and the heading just past its end). Take the lines out of the parent the same way. (b) Add the H1s, the `Authority for` paragraphs, and the arms file's `## The two arms of the commit gate` (D3). Rewrite the parent's preamble as its index, before `## Registration` (D4). (c) Turn the six K6 crossing lines (91, 199, 273, 274, 283, 284) into citations (D5). (d) Set `seal/config.md` `Over the ceiling` to `none`, and rewrite `docs/the-evidence-ledger.md`'s fold statement to list nothing and to record the #727 split (D8). Update the history in `tests/test_a_document_has_room_for_the_next_fold.py`'s docstring. (e) Make every K2 site follow its text: `REVIEW_CHAIN_DOCS` to five, the two sweep lists, the `DIRECT_REQUIRES` key, `GATE_SPEC`, the waiver, hardening and two-answers paths, and the `VERSIONS_OF_ANOTHER_PRODUCT` keys (D10) | **executed**: one narrow command over the K2 modules, `tests/test_a_document_has_room_for_the_next_fold.py` and `tests/test_docs_line_wrap.py`; `bin/fold-check` exits 0 with 18 markers across the three files; the S1 `test_tmp_*` probe shows the moved blocks equal to `git show 2b1dcb1f:docs/commit-review-gate-spec.md` except at the K6 lines, then is deleted | |
| 2 | **Every reference follows (K5), and the record layout says F1 is built.** Re-point each K5 row whose subject moved: the agent contract's §9 and §17, both READMEs (the citation and the documents list), `docs/round-record-spec.md` and `docs/review-chain-spec.md` preambles, `docs/the-evidence-ledger.md` 477, the hook and checker comments, and the four test comments. Then make `docs/the-record-layout.md` match D9 | **executed**: the S5 `test_tmp_*` probe resolves every `§*…*` naming one of the three files against the cited file's headings and finds no moved heading cited by the parent's path; its count goes in `phases/phase-2.md`, then it is deleted. A narrow command over the modules that read the touched files, found by `git grep -l` of each touched path in `tests/` (at least `tests/test_the_agent_contract_holds_the_universal_rules.py`, `tests/test_the_ledger_rules_have_one_home.py`, `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_one_word_one_meaning.py`, `tests/test_docs_line_wrap.py`) | |
| 3 | **The ledger, the entry and the sweep.** (a) Run `bin/evidence-check` and read every BROKEN and DRIFTED row it names. (b) Write the two `Corrected ·` rows by hand in `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md`: G17 with all five coordinates, and *two opt-in headings* with both, each citing the released row by content as `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* shows. (c) After reading each drifted row, run `bin/evidence-check --reverify --into seal/ledger/1791019477-….md --checked <date>` for the `Re-read ·` rows, narrowed with `--ledger` to what was read. Re-stamp any other work item's fragment row in place. (d) Add this item's own rows: the three files and their preambles, the freeze lifted, and the K2 pins re-pointed. (e) Write `changelog.md`. (f) Run `bin/survivor-check --range 2b1dcb1f...HEAD` over the whole branch, and correct each survivor or exempt it in `survivors.md` with its quote (K7) | **executed**: `bin/evidence-check` nothing BROKEN or DRIFTED; `bin/correction-check --range 2b1dcb1f...HEAD` passes, with no released file changed; `bin/survivor-check --range 2b1dcb1f...HEAD` exits 0, or 1 with every line exempted | |

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

**Notes for the builder, which are this work's and no template's.**

- **Files.** Every file read and write passes `encoding="utf-8"`. No
  `git stash`. Commit with `git -C <worktree>` in a command of its own.
- **Phase 1 is one commit on purpose.** The `Alternatives` row about separate
  commits says why. Phases 2 and 3 may commit as often as each step stands on
  its own.
- **The move script is a probe.** It lives in the scratchpad, not the tree,
  and asserts each boundary heading's text before it copies, so a miss fails
  loudly (contract §9).
- **The broad gate is the sealer's.** The full suite, the repository-wide lint
  and the typecheck are not this work's to run (contract §2). Hand over with
  the suite labelled `unverified` and the sealer named.

## Operational impact

None for a deployer: no migration, no environment variable, no dependency. An
installed copy gets two new documents and a narrower parent. The agent
contract's §9 and §17 cite a different file for the same section. A link to
`docs/commit-review-gate-spec.md` at an older tag keeps resolving at that tag.
A link to one of its moved sections at the current tip lands on the parent's
index, which names the file that holds it.
