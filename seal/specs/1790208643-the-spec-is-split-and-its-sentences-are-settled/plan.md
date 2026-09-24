# Implementation Plan: the spec is split and its sentences are settled

<!-- seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-24 by the orchestrating session on the owner's `automation` answer, when `smith` was spawned; phases 3 and 6 wait for step D (#558) to squash.

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

Six phases, the split first and the sentences after it, so that nothing is
moved and then edited. Phase 1 makes the three documents, re-points the 20
shipped citations and the 23 ledger anchors, and retires the ceiling entry.
Phase 2 re-points the 28 test modules. Phase 3 writes #488's and #509's
sentences into the three ledger-rule carriers and the release checklist,
after re-reading D's landed frame. Phase 4 settles the five one-sentence
tickets in the agents' and skills' documents (#55, #316, #474 items 2 and
3, #222) and verifies #268. Phase 5 widens #466's pin. Phase 6 corrects
#474 item 1's rows and writes the records.

**This branch is built on `release/v0.15.1` after A, B, C and D have
squashed into it.** Before the first edit the smith rebases (or merges the
release branch in — never rebases a branch a sibling has already squashed
past, per the 0.15.0 lesson) and re-reads from the merged base every
section a sibling rewrote: A's `survivor_check.py` docstring, B's
`agents/warden.md` §*Where you work*, `agents/sealer.md` §*The command*,
`skills/verify/SKILL.md` §*Capture once, filter locally*, `CONTRIBUTING.md`
§*Running the checks*, `docs/release-checklist.md` §3; C's
`docs/review-chain-spec.md` §*The depth in `New units`*, `agents/warden.md`,
`skills/code-review/SKILL.md` §*Findings format*, `docs/review-handoff-protocol.md`'s
`Broad gate` row, `skills/code-review/orchestration.md`'s sealer paragraph,
`docs/release-checklist.md` §2; and D's whole diff (its frame was not
committed when this one was drawn — §*What D changes that phase 3 reads*).

## Technical context

**The source file.** `docs/review-chain-spec.md` at `9f846733`: the heading
tree with spans is in `spec.md` §*What was measured*. Lines 1922–1938
(*Which declaration applies is settled by the branch it names* … *Deleting
the routing file restores today's behavior exactly*) sit at the end of
`##### What the record carries` and are the tail of `#### The declaration`,
separated from it by the thirteen subsections that were inserted between;
the move puts them back under the declaration in the gate document.

**Where each section goes.** R = `docs/review-chain-spec.md` (the run), G =
`docs/commit-review-gate-spec.md` (new), C = `docs/round-record-spec.md`
(new). The order inside each file:

| File | Sections, in order | Level after |
|---|---|---|
| R | title and opening (rewritten to name the three files); The cycle; The review run has a bound — with its four `###` (cap, floor, verifying, leftover) and, inserted after *The last round verifies* and before *Where a leftover goes*, **The floor — `Loses a record or crashes`**, **`Needs a fix`**, **The reopening**; Two records — with **When the record was written** and **What the record carries** (its first 75 lines) beneath it; The survivor sweep and its `###`; Non-goals | the three moved bound subsections and the two record subsections become `###`; nothing else changes level |
| G | title and opening (two sentences, naming R and C); Registration; commit-review-gate — own prose, Which repository (+ `#### A cd the gate cannot read`), Why a deny, Review arm (+ `#### Where the marker goes`, `#### The declaration` own prose **plus the 17-line tail**); Parity arm; review-history-guard; implementer-mark · implementer-notice | unchanged |
| C | title and opening (two sentences, naming R and G, and that the declaration that sends a check here is G §*The declaration*); `Pass`; `Fixes checked by`; The finding id; A verdict row that commissions nothing; The fix range; The fix surface; The depth in `New units` (C's S13 sentence inside it, unchanged); What ran the round; The record generator and its three `###` | the eight `#####` become `##`; the generator's `##` and `###` unchanged |

**What the move has to reword** — each is a positional reference that dangles
in its new file, and each rewording is a sentence the sweep will report
(A's frame, judgment 7, *from a frame*), answered in `survivors.md` where a
copy elsewhere is correct:

| Where | Today | After |
|---|---|---|
| R, opening paragraph | *Authority for `hooks/commit-review-gate.py` and `hooks/review-history-guard.py`, and for the cycle contract…* | names the three files and what each is the authority for |
| R, *The floor — Loses a record…*, second paragraph | *The row is read on every record, like the two above and for the same reason* | names `Pass` and `Fixes checked by` in C |
| R, *When the record was written* | *Read on every record, like the four above* | names the four rows in C |
| R, *What the record carries* | *That is the third declaration in this document* — the other two are `New units`' depth and `Ran by`'s provenance, both in C; *the closing the arrow's and the comma's limits above already decline*; *the shape `New units`' depth and `Ran by`'s provenance already take* | each names C's section |
| G, *The declaration*, the at-pull-request table | *its last round's `Pass` checked … its `Fixes checked by` naming a checker …* | keeps the cell and adds one pointer sentence under the table: what the check reads of the record is C |
| C, *What ran the round* | *Read on every record, like the three above and for the same reason* — the three were `Fixes checked by`, the fix-surface rows and the floor, and the floor is now in R | names `Fixes checked by` and the fix-surface rows in C and the floor in R |
| C, *The depth in New units* | *the mirror of the arrow's above* — true in C (the fix surface is above) | unchanged |
| C, *The record generator* | *The sections above say what each field means* | unchanged; true in C |
| C, *The fix surface* | *the same grandfathering as above* | unchanged; `Fixes checked by` is above |
| G, *What the record carries*'s tail, now under *The declaration* | *This is a reversal, and of this document. The paragraph below the review arm's table used to say…* | unchanged; the review arm is in G |

Any further positional reference the build meets is treated the same way
and listed in `phases/phase-1.md`; a rewording not on this list is a finding
for the reviewer to weigh, not a silent edit.

**The readers of the moved text**, with the mechanism each uses:

- `skills/evidence-check/scripts/evidence_check.py#text_regions` — matches the
  heading line exactly (level included) and hashes from it to the next
  heading at or above its level; `#heading_path` for `A / B` paths.
  `--reverify` heals a row whose region moved byte-identical across files
  (`CONTRIBUTING.md` §*House rules*, the rename paragraph) and reports
  BROKEN with the destination otherwise. Hand re-point: edit the anchor's
  path and heading text, add `Re-read <date> — moved by #526's split, the
  claim unchanged` to Notes, run `--reverify`.
- `tests/test_a_document_has_room_for_the_next_fold.py` — `OVER_CEILING` and
  `FROZEN_IDS_DIGEST` keyed by path; `documents()` walks `docs/` so the new
  files are read on arrival; `test_the_evidence_ledger_states_the_values…`
  parses the ceiling bullet with three regexes (`from work item … on`, `at
  or under N lines`, `` `docs/…`, frozen at N fold markers until … ``) and
  requires the listed set to equal `OVER_CEILING` — so the rewritten bullet
  must keep the first two spellings and carry no line matching the third.
- `tests/test_docs_line_wrap.py#COVERED` — a hand list; add both new files.
- `tests/test_one_word_one_meaning.py` — the file list at `:194–226`; add
  both new files. Its `:131–135` reads the deny/ask paragraph (G); `:142–148`
  the cycle paragraph and the `## The review run has a bound` heading (R).
- `tests/test_the_rules_have_one_owner.py` — `SPEC` stays R; three cases
  (`test_the_verdict_ruling_is_against_a_vocabulary_test…`,
  `test_the_open_verdicts_boundary…`, `test_the_depth_refusal…`) read C.
  `occurrences()` walks `docs/` whole, so the count rule's phrases are
  found wherever they land — and *at most one more round record* stays in R.
- `tests/test_the_report_standard_is_one_in_three_places.py#CARRIERS` — the
  carried-closure row is in *A verdict row that commissions nothing* and C's
  S13 sentence in *The depth in `New units`*, both in C: the tuple's spec
  entry becomes C.
- `tests/test_the_reopening_is_one.py#HEADING/NEXT_HEADING/PREVIOUS_HEADING`
  (`#####` → `###`; the next heading becomes *### Where a leftover goes…*),
  `tests/test_the_record_is_held_to_the_floor_and_the_depth.py#SUBSECTIONS`
  (floor → `###` in R; depth → `##` in C), `tests/test_a_record_says_what_ran_it.py:449`
  (`##### What ran the round` → `## What ran the round`, in C),
  `tests/test_chain_hooks_hardening.py:508` (`### Review arm` / `####` — in
  G, unchanged).
- `tests/test_a_record_precedes_the_fixes_it_commissions.py:1275` and every
  other `not in` assertion over the spec: read all three files (S6).
- `skills/settle/scripts/settle.py` and `skills/verify/scripts/unverified_check.py#folded_items`
  read markers from every top-level `docs/*.md`, so a marker moved between
  the three files stays a fold record (S2).
- `.github/workflows/hygiene.yml`'s survivor step and the sealer's
  `survivors` arm read `origin/<base>...HEAD`; the move is silent to them,
  the rewordings are not (S8).
- `tests/test_no_real_identifiers.py` and `tests/test_release_hygiene.py`
  read tracked text and the `docs` directory respectively; both reach the
  new files with no edit.

**The sentence tickets' coordinates** (all at `9f846733`, read 2026-09-24):

- #488/#509: `docs/the-evidence-ledger.md` §*A row is a content anchor*
  (*Appended is the word…*) and §*A correction a merge dropped*;
  `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*;
  `CONTRIBUTING.md` §*House rules*, first bullet (*Changing cited code is the
  case the rule has to answer* and the two answers). Pinned by
  `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES`
  over `CLAUDE.md` and `CONTRIBUTING.md`, whitespace-collapsed needles.
  `docs/release-checklist.md` §0 *Squash the work items back to back* (line
  18) is where a session meets the conflict.
- #55: `agents/smith.md` phase 2, the paragraph *For a change belonging to
  no work item, `[no-review]` still waives one command…* and the rider
  beneath it, stamped `Verified 2026-09-22 against "## Phases"@72cf1e1b`.
  `tests/test_a_moved_rule_leaves_its_definition.py#WINDOW = 15`,
  `LONGEST_KEPT_APPLICATION = 10`, asserted `<=`, and the kept phrase
  *a bare word is a pathspec and git rejects it* is the pair that sets the 10.
- #316: `skills/verify/SKILL.md` §*`arm-check` asks condition 2 of a whole
  module, one arm at a time* (line 59); `skills/verify/scripts/arm_check.py#run_arms`
  docstring, `--timeout` default 900.0; `tests/test_arm_check.py` reads the
  script and not the skill.
- #474 item 2: `skills/verify/SKILL.md:355` (*the one live instance this
  repository has*) and `:360` (*Four steps of this repository's `release`
  job*). Item 3: `tests/test_the_gate_names_every_step_ci_runs.py:11–14`.
  Item 1: `seal/ledger.md` lines 2403–2404 at `9f846733` (G6, G7 of
  `1789985781`), and the four cases at `tests/test_the_gate_names_every_step_ci_runs.py:720,760,781,811`.
- #222: `skills/code-review/scripts/round_record.py#depth_two`, docstring
  ending at the #333 paragraph; the walk at `:3770`; three `seal/ledger.md`
  rows on `depth_two@8c7bfa47`.
- #466: `tests/test_the_contributor_has_a_procedure.py#CONVENTION_SURFACES`
  and the case at `:172`; `tests/test_release_hygiene.py#LOADED` and
  `#tracked`; the four standing names in `spec.md` §*Scope*.
- #268: `docs/issues-and-milestones.md` §*A keyword claims the one number
  after it*; `.github/scripts/close_issues_on_release.py:101` names #266.

**What D changes that phase 3 reads.** D's subject is the fold writing each
release to its own file and the checker's glob widening. Its committed
`spec.md` §*Data & interfaces* and §*Scope*, once on the release branch,
say whether `seal/ledger.md` keeps its name, whether a re-stamp of a released
row lands in `seal/ledger/<version>.md` or elsewhere, and which sentences of
`docs/the-evidence-ledger.md` §*A row is a content anchor*, `CLAUDE.md`
§*a change writes fragments*, `CONTRIBUTING.md` §*House rules*,
`docs/release-checklist.md` §2 and `docs/branch-and-release.md` §*The ledger
fragments fold in the same commit* it rewrote. Phase 3 writes #488's and
#509's sentences into those sections as D left them, and phase 1's 15 hand
re-points land in whichever file then holds each row.

**Failure scenario of the chosen approach, six months out.** A citation
written as `docs/review-chain-spec.md §*X*` where X now lives in another
file — a new one, or one of the 46 lines this branch left because their
section stayed. Nothing reads a `§*…*` citation against the tree
(`test_the_rules_have_one_owner.py` checks that a link string is present in
a carrier, not that the section exists), so the drift is a reviewer's
finding. What bounds it: the five owner sentences stay in the file the
links name, so the 18 link strings hold; and a moved section's heading is
unique across the three files, so a `grep` for the title finds it. The
second scenario is the record document growing past the ceiling: at about
880 lines it has room for the folds of roughly one release, after which
`settle` places the rule in the document for its own sub-subject, which is
the rule already in force.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Split along `##` headings only (the ticket's first proposal) | Leaves `## commit-review-gate` whole at 1,544 lines; the ticket says so itself | rejected |
| Two documents: the run and the gate, with the thirteen `#####` staying under the gate | The gate document lands at about 1,700 lines, over the ceiling | rejected |
| **Three documents, the thirteen subsections split between the run (the bound's three, the record's two) and the record document (eight rows and the generator)** | The record document at about 880 lines has room for about one release of folds; the run document's `## Two records` gains two `###` that are about the record rather than the mark, which its title still covers | **chosen** |
| Four documents: the record's rows apart from the generator, or the record's terminal rows apart from its tables | More room per file, at the price of a fourth name, a fourth set of citations, and a `## The record generator` whose *the sections above* sentence has to be reworded | fallback if M1 measures the record document over 1,000 lines |
| Move the floor, `Needs a fix` and the reopening to the record document with the other arms | Rule 4's owner sentence leaves the file 4 link strings name, `RULES[4]` and four carriers change, and `test_the_run_stops_at_the_last_finding.py`'s docstring (*the file that owns the cap owns the floor*) goes false | rejected — six anchors and two test constants is the cheaper edit |
| Keep every moved heading at `#####` so `--reverify` heals all 23 anchors | A document whose headings are all `#####` under a `#` title, which is the unreadability the split exists to end | rejected |
| Re-point the 15 anchors as REMOVED-and-rewritten rows in the fragment | `CLAUDE.md`'s removal rule is for a claim that went with the code; nothing went. The rename paragraph in `CONTRIBUTING.md` is the rule for a move, and it re-points | rejected |
| A `docs/review-chain-spec.md` left as a two-paragraph pointer, with all content in three new files | Every one of the 47 readers changes; the five owner rules' 18 link strings move; nothing is gained over keeping the run in the file that keeps the name | rejected |
| #331 built here as a census over the shipped documents (an n-gram walk minus the owner-rule's links) | A new instrument with a false-positive argument nobody has made, in a patch release whose rule is no design and no new gate; the ticket's own third open decision is whether the check is its own item | deferred, Q1 |
| #466's population as every tracked text file | Reaches `hooks/cmdline.py`'s `release/v0.22.0` and `bin/correction-check`; also reaches `CHANGELOG.md`, `seal/specs/` and every test fixture that builds a `release/v9.9.9` branch, which the hygiene tuple excludes for reasons the ticket says apply here too | rejected for the hygiene tuple; Q2 records the `hooks/` question |
| #55 as the three-row table copied into `agents/smith.md` (the ticket's first checkbox) | `tests/test_a_moved_rule_leaves_its_definition.py` refuses a 15-word run of §8 in any definition, and §8 already reaches the smith by mechanism | rejected — one application sentence |
| #316 pinned by a substring case in `tests/test_arm_check.py` | #310 is the standing warning against pinning a document clause by substring; the module reads the script, not the skill | W4 — the phase decides, with the default *no case, said in the phase record* |
| #488's sentence as *any touch to the shared file is permitted* | Gives back the conflict the fragments exist to remove; the ticket's own *What the answer is not* | rejected |
| #509's sentence in `docs/release-checklist.md` as a second statement of the rule | A third restatement; the checklist links to the owner in one sentence | rejected — a link |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
row is the whole task; there is no prompt per phase (`agents/framer.md`).
Each phase closes with `phases/phase-N.md` from `templates/sdd-phase.md`,
the ledger rows drafted during the phase written in one pass, a commit, and
`python3 skills/evidence-check/scripts/evidence_check.py --strict .` read
directly (contract §1). Edits go through the `Edit` tool (§9): the moves are
made with `git mv`-free file writes, so no command line carries a commit.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 0 | **The base.** `release/v0.15.1` merged in after A, B, C and D squashed; every sibling-rewritten section in §*Summary* re-read from the merged base; D's committed `spec.md` and `plan.md` read and the three ledger-rule carriers re-read as D left them; the heading walk of `spec.md` §*What was measured* re-run over the merged `docs/review-chain-spec.md` (C added one sentence to *The depth in `New units`*) and the counts in the phase record | the walk's output in `phases/phase-0.md`; `git log --oneline origin/release/v0.15.1 -6` showing the four squashes | `23d46e81` — A, B and C; D's half re-read after the merge `4a077852`, in `phases/phase-3.md` |
| 1 | **The split.** The three files written from the section map, levels as §*Where each section goes*, the 17-line tail restored under *The declaration*, the openings written, the rewordings in §*What the move has to reword* made and no others; `docs/the-evidence-ledger.md`'s ceiling bullet rewritten (*No document is over the ceiling* — keeping *at or under 1,000 lines* and the settle §2 link, carrying no `frozen at … until` line) and its `:262` citation re-pointed; the 20 shipped citations re-pointed; both READMEs' *Full decision tables* links naming G beside R; `OVER_CEILING` and `FROZEN_IDS_DIGEST` emptied (the module red on A10 first, recorded); `COVERED` and the one-word list extended; `evidence-check --reverify .` run and its heal lines quoted; the 15 hand re-points with dated notes; the marker census S2 | `bin/test tests/test_a_document_has_room_for_the_next_fold.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_release_hygiene.py tests/test_both_editions_carry_the_same_folds.py -q` — counts read directly; `evidence-check --strict .` exit 0; `bin/survivor-check --range origin/release/v0.15.1...HEAD` with its report matched line by line against the rewording table (M2); `bin/settle` exit 0 with the same *already folded* count as at phase 0; M1's three line counts | `6c5c5295` |
| 2 | **The 28 test modules.** Each module in `spec.md` §*Data & interfaces*'s list re-pointed by the section map: the tuple or path changed where a module reads one file whole; a second tuple added where a module's cases split between two; every `not in` assertion read over the three files (S6); the heading-level constants (S7) changed and each such module seen red at the old constant first; `CARRIERS`, `RULES`'s three cases | `bin/test <the 28 modules> -q` in one command, count read directly; `uvx ruff check` and `format --check` over the edited modules | `c213eb70` |
| 3 | **The ledger's two sentences** (#488, #509), into `docs/the-evidence-ledger.md` first (the owner), then `CLAUDE.md` and `CONTRIBUTING.md` as D left them; one linking sentence at the release checklist's squash step; `CONFLICT_SENTENCES` gains needles for *removes or edits* / *keeping an existing claim true*, *the side that edited*, and *after the resolution*, each seen red with the sentence absent from one guide | `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_the_contributor_has_a_procedure.py tests/test_docs_line_wrap.py -q`; `.github/scripts/claude_block.py --check` (the block above the repo rules is generated and must not have moved); `evidence-check --strict .` | |
| 4 | **Five sentences and one verification.** #55's sentence in `agents/smith.md` with the kept-phrase pin, the rider re-read and `rider_check.py --reverify`; #316's paragraph in `skills/verify/SKILL.md` (W4 decides the pin); #474 item 2's two sentences; #474 item 3's docstring; #222's paragraph in `depth_two` with the three rows re-read and re-stamped (withdrawn at the merge `4a077852`: #559, an outside contribution, closed #222 with an equivalent paragraph the owner chose, so only the corrected re-read notes stay here); #268's three greps, recorded, and an edit only where one hits; #556's two comments above `kept_broad_gate`'s calls in `close` and `seal` and `agents/sealer.md`'s seal sentence, comments and one definition sentence with no behaviour moved (added to this phase by the orchestrator at the spawn, with its `changelog.md` entry) | `bin/test tests/test_a_moved_rule_leaves_its_definition.py tests/test_arm_check.py tests/test_the_gate_names_every_step_ci_runs.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py tests/test_one_word_one_meaning.py tests/test_docs_line_wrap.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q`; `python3 .github/scripts/rider_check.py` exit 0; `uvx ruff check` over `round_record.py` and the test; `evidence-check --strict .` | `ddb580d1` |
| 5 | **#466's pin, one population wider.** The case reads `tracked(*LOADED)` from `test_release_hygiene.py` (imported, not copied), keeps the four surfaces as the loud first parameter set, allows the three history phrases by name with the reason each is history, and is seen red over a planted `skills/x/SKILL.md` in a fixture root and over this tree before `correction_check.py:23` changes; `correction_check.py:23` and `bin/correction-check:10` spell `release/vX.Y.Z`; `git log -S'release/v0.22.0'` recorded (M3) | `bin/test tests/test_the_contributor_has_a_procedure.py tests/test_release_hygiene.py tests/test_a_merge_cannot_silently_drop_a_correction.py -q` (the last reads `bin/correction-check`'s usage line); `uvx ruff` over both edited files; the two red runs in the phase record | `1ccaa24f` |
| 6 | **The records.** G6 and G7's `Code grounds` widened with a `Corrected <date>` note and `--reverify`; the fragment written in one pass; `changelog.md` (one entry per closed ticket, #331 named as deferred); `overview.md` with `## Not verified` naming the sealer for the broad gate; `survivors.md` for the rewordings the sweep still reports; `questions.md`'s W and M rows filled | `evidence-check --strict .` exit 0; `bin/survivor-check --range origin/release/v0.15.1...HEAD --exempt <this item>/survivors.md` exit 0 with every `exempt` line naming a row; `bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/` exit 0; `python3 skills/evidence-check/scripts/correction_check.py --range origin/release/v0.15.1...HEAD` exit 0; every exit read directly | |

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

- **No gate changes.** Nothing under `hooks/` or `.github/workflows/`
  changes behaviour; `CONTRIBUTING.md` §*What a change to a gate must carry*
  is not owed by any phase. Prompt budget zero throughout.
- **The document a reader opens moves.** `README.md` and `README.ko.md` link
  the gate document for the decision tables; every `§*…*` citation in a
  shipped file names the file that now holds the section. A user's own
  bookmark to `docs/review-chain-spec.md` still opens the run's spec.
- **The ceiling binds every document again.** With no over-list entry, the
  next fold into `docs/round-record-spec.md` (about 120 lines of room) or
  `docs/review-handoff-protocol.md` (839 lines, 161 of room) is the first
  to meet it.
- **`seal/ledger.md` — or the per-release file D gives it — takes 15
  re-pointed rows, two corrected rows (G6, G7) and three re-stamped rows
  (`depth_two`)**, by rename, correction and re-verification: nothing is
  appended to the shared file. A sibling branch still re-stamping the same
  rows merges hunk by hunk with both sides read.
- **The survivor sweep reports the rewordings once**, on this pull request
  and at the seal; `survivors.md` carries the grounds for any the branch
  cannot correct in its copies.
- **The rider in `agents/smith.md` drifts** on the #55 edit and is
  re-stamped after being read, which is the rider firing rather than a chore
  (`seal/follow-up.md`).
- No migration, no dependency, no environment variable, no version move.
