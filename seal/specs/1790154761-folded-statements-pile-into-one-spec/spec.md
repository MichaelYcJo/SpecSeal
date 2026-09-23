# Feature Specification: folded statements pile into one spec (#520)

<!-- seal/specs/1790154761-folded-statements-pile-into-one-spec/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Record language: English (`seal/config.md` carries no `Record language` row).

## What was measured, and against what

Every number below was re-measured on 2026-09-23 in this worktree at
`9b18172a` (release/v0.14.0 at `f8f1c9de` plus this item's `routing.md`), with
the reader the checkers use: `FOLD_MARKER = ^<!-- specs/(\S+) -->$`
(`skills/verify/scripts/unverified_check.py#FOLD_MARKER`), top level of
`docs/` only.

| File | Lines | Fold markers | Distinct ids |
|---|---|---|---|
| `docs/review-chain-spec.md` | 2,159 | 29 | 26 |
| `docs/the-evidence-ledger.md` | 221 | 13 | 10 |
| `docs/the-broad-gate.md` | 126 | 11 | 11 |
| `docs/one-root-by-lifetime.md` | 675 | 10 | 10 |
| `docs/measuring-a-run.md` | 122 | 10 | 9 |
| `docs/issues-and-milestones.md` | 361 | 6 | 6 |
| `docs/release-checklist.md` | 294 | 6 | 6 |
| `docs/the-agent-set.md` | 105 | 6 | 6 |
| `docs/branch-and-release.md` | 363 | 4 | 3 |
| `docs/review-handoff-protocol.md` | 839 | 4 | 4 |
| `docs/worktree-guard-spec.md` | 448 | 2 | 2 |
| `docs/one-root-by-lifetime.ko.md` | 586 | **0** | 0 |
| total | — | **101** | 92 |

The issue's numbers hold: 101 markers, 29 in the chain spec, 10 against 0 in
the two editions. The chain spec is 141,638 of `docs/`'s 406,832 bytes (35%).
Every existing marker id is below this work item's id `1790154761`; the
largest is `1790076080-every-orchestrator-rule-is-a-sentence`.

Four facts the issue does not state, each opened:

- **The Korean edition's drift predates both folds.** The English edition
  has 22 headings and the Korean 21, title included, with fenced blocks
  skipped. A heading needs `#` and then a space, because each edition has one
  prose line that begins `#<number>`. The missing one is §*What the repository
  decides for itself, and how it is read*, which the first fold created
  (`f51e634d`, #504) and which carries 5 of the 10 markers. The other 5 sit on
  sections both editions share (§*The change in four lines*, §*The opt-in
  signal…*, §*What first setup asks*, §*Shared or local*).
- **The repository already reads `CONTRIBUTING.md` as pairing this document.**
  `tests/test_settle_reads_before_it_removes.py#test_both_editions_took_the_same_decisions`
  says so in its docstring and compares one section's cell count across the
  editions. Five test modules pin text in the Korean edition, and PR #525
  (#517, open, draft) adds a dated section to both editions by hand on
  2026-09-23.
- **The split the issue proposes leaves a 1,430-line piece.** The chain spec's
  `## commit-review-gate` runs from line 431 to 1,860 and holds every record
  field rule. The four axes the issue names (record, cap and ladder, verifying
  round, pull request) do not divide it along a heading that exists.
- **The split's surface is 47 files, and 12 of them are in PR #525's diff.**
  `review-chain-spec` is named 87 times in 24 test modules, 55 times in
  shipped files (skills, agents, templates, hooks and the two READMEs), and
  by 18 rows of `seal/ledger.md`. The 12 shared with #525 include
  `skills/code-review/scripts/chain_check.py`, `seal/ledger.md` and five test
  modules.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | a rule a check reads beats a rule a reviewer has to remember. Each of the three rules below comes with the check that reads it |
| `skills/settle/SKILL.md` §2 *Write one standing statement per segment* | the fold's own procedure. After #525 lands it is also the fold's spec, because a fold opens no work item. The shape rule and the placement rule are stated here, and nowhere else is their owner |
| `tests/test_the_rules_have_one_owner.py` (the convention it pins) | one carrier states a rule and every other carrier links to it. `docs/the-evidence-ledger.md` links to settle §2 and holds only this repository's own values |
| `CONTRIBUTING.md` §*Both READMEs move together* | the pairing rule already exists for the READMEs. It is widened to any document with a `.ko.md` edition, and this is its owner |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* | markers are read on live lines at the top level of `docs/`. The new checks read markers the same way and reuse the same reader |
| `skills/implement/SKILL.md` §*Document layout* | a work item creates no `docs/` document, so the new standing text goes into existing documents |
| `docs/issues-and-milestones.md` §*A release is sized by what has to be in effect…* | the next fold runs at 0.14.0's release. The rules it has to follow need to be in effect before it, and the split does not |
| `docs/review-chain-spec.md` §*Where a leftover goes — the ladder…* | every deferral below names a home and a party |

## Scope

**One line: the next fold meets three written rules, and a check reads each
one.** The rules say where a folded statement may land, what shape it takes,
and that both editions of a document carry the same folds. Nothing in the
existing 101 statements is rewritten except the Korean edition's missing
section.

### In

1. **The editions are paired, and a check holds them.** The Korean edition
   gains a translation of §*What the repository decides for itself, and how it
   is read* and the 10 markers, each under the heading that matches its English
   position. A new test compares every top-level `docs/X.ko.md` with its
   `docs/X.md`. Both editions must have the same sequence of heading levels,
   and for each heading position the same multiset of fold-marker ids beneath
   it. Marker ids are language-neutral, so this comparison needs no
   translation. `CONTRIBUTING.md`'s README rule widens to cover any document
   with a `.ko.md` edition.
2. **A folded statement has a fixed shape, and a check reads it.** A statement
   opens with a bold rule sentence, is followed by its grounds, and carries
   exactly one line `Enforced by: <target>[, <target>…]` or
   `Enforced by: nothing — <why>`. A target is a repository path, optionally
   followed by `::<name>` for a `def` or `class` in that file. The check
   resolves every target. Consecutive marker lines share the statement below
   them. A statement ends at the next marker, the next heading or the end of the
   file. **The shape binds only markers whose id is `≥ 1790154761`**, this work
   item's id. Ids are epoch-prefixed, so the cutoff is a comparison rather than
   a list, and all 101 existing markers are below it.
3. **A document has a ceiling, and the chain spec takes no new fold until it
   is split.** Every top-level `docs/*.md` stays at or under **1,000 lines**,
   except files in a named over-list. Each over-list entry records a frozen
   fold-marker count and the issue that retires it. For
   `docs/review-chain-spec.md` that count is 29 and the issue is the deferred
   split. The check fails when a file outside the list passes the ceiling. It
   fails when a listed file gains a marker. It also fails when a listed file no
   longer exceeds the ceiling, so an entry cannot outlive the split. This
   check is what holds placement: the 0.14.0 fold cannot add a chain rule to
   the chain spec, so it has to place the rule in a document for the rule's
   own sub-subject or do the split first.
4. **The rules are written where their owner is.** Settle §2 states the shape
   and the placement rule in general form, because a consumer repository's fold
   follows them too. `docs/the-evidence-ledger.md`'s fold section links to
   settle §2 and states this repository's ceiling, its over-list and the
   cutoff. It does not state the rules again.

### Out, and where each one goes

| Item | Why it is out | Home |
|---|---|---|
| Splitting `docs/review-chain-spec.md` | The proposed axes leave the 1,430-line `commit-review-gate` section whole, so the split needs a design of its own. Its 47-file surface overlaps 12 files of open PR #525. The ceiling in item 3 keeps the pile from growing meanwhile, so nothing forces the split into 0.14.0. #265's split of `skills/code-review/SKILL.md` along its own headings is the precedent to follow | a new issue in `backlog: docs drift`, filed by the orchestrator before phase 3. Its number becomes the over-list entry's home (questions.md Q3) |
| Retrofitting the shape onto the 101 existing statements | This is 101 judgments about which check enforces each rule, across every `docs/` file, including 29 in a file #525 edits. That audit is valuable, and #516's false sentence is the kind it would find, but it is a work item of its own | the same new issue, as a second checklist item |
| Shipping the shape and ceiling checks as plugin commands | #525 changes `settle.py` by 468 lines. A new command also brings a `bin/` wrapper and README cheat-sheet rows that `tests/test_chain_hooks_hardening.py` derives. The checks ship as repository tests. Settle §2 says the plugin carries no checker for them, the same way it already says so for *only what is still true* | the same new issue |
| A check that two statements contradict | No reader can tell that without semantics. #516's finding 2 was found by review, and the placement rule narrows where a reviewer has to look (one subject, one document) | nothing. The spec says so rather than implying a check covers it |
| Moving folds out of `docs/one-root-by-lifetime.md` | `tests/test_no_document_names_the_old_roots.py#DESIGN_RECORD` classifies the file as a record of a moment, yet the first fold wrote an undated standing section into it. Once the editions are paired the mirror drift is closed either way, so whether a design record may take folds changes no code here | questions.md Q4, for the owner |
| `README.md` / `README.ko.md` pairing | They are not under `docs/`. The hygiene workflow already warns about them, and their content-level pins live in `tests/test_chain_hooks_hardening.py` | unchanged |
| `docs/experiments/*.ko.md` | below the top level, which the fold never reads (`docs/the-evidence-ledger.md` §*The fold…*) | unchanged |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The Korean edition drifts | Given `docs/X.md` gains a fold marker under heading position k, when `docs/X.ko.md` is not changed, then the pairing test fails, naming the file, the heading position and the missing id | the new test, seen red at `9b18172a` (10 ids against 0) before phase 1's prose lands |
| A2 | The editions agree | Given this branch's `docs/one-root-by-lifetime{,.ko}.md`, then heading-level sequences are equal and each position's marker multiset is equal | the new test, executed green |
| A3 | A heading added to one edition only | Given one extra `##` in the English edition, then the pairing test fails on the level sequence | a planted case in the new test module, seen red |
| A4 | A new fold without the shape | Given a marker with id ≥ `1790154761` whose statement has no `Enforced by:` line, or two of them, then the shape test fails, naming the marker | fixture cases in the shape test, each seen red |
| A5 | A statement names an enforcer that does not exist | Given `Enforced by: tests/test_x.py::test_gone`, where the file or the name is absent, then the shape test fails, naming the target | fixture case, seen red |
| A6 | An unenforced rule says so | Given `Enforced by: nothing — <why>`, then the shape test passes. The same line with an empty reason fails | fixture cases |
| A7 | The existing 101 statements | Given the real `docs/`, then the shape test passes, and it asserts it read at least one marker, so a broken reader cannot pass on an empty walk | executed over the tree |
| A8 | A fold adds to the chain spec | Given `docs/review-chain-spec.md` with 30 markers, then the ceiling test fails, naming the over-list entry and its home issue | fixture or planted case, seen red |
| A9 | A document grows past the ceiling | Given any top-level `docs/*.md` outside the over-list above 1,000 lines, then the ceiling test fails | planted case, seen red |
| A10 | The split happens | Given the chain spec drops to 1,000 lines or fewer, then the ceiling test fails until the over-list entry is removed | planted case, seen red |
| A11 | The rules have one owner | Settle §2 states the shape and placement rules. `docs/the-evidence-ledger.md` links to it by section name and holds the values. `CONTRIBUTING.md` owns the edition rule | read. Where the rule texts are pinned, the pins live in the new test modules |
| A12 | Nothing else regresses | the modules that pin either edition, settle's text or the fold reader stay green: `test_settle_reads_before_it_removes`, `test_first_setup_asks_once`, `test_no_document_names_the_old_roots`, `test_unverified_rows_close`, `test_release_hygiene`, `test_docs_line_wrap` | executed per phase (narrow). The broad gate is the sealer's |

## Data & interfaces

- **The `Enforced by:` line.** It is a line of its own, starting at column 0
  with `Enforced by: `. It is followed by a comma-separated list of targets,
  or by `nothing — ` and a non-empty reason. A target is `path` or
  `path::name`, where `path` is relative to the repository root. The check
  reads it on a live line, so a quoted example in a fence does not count. The
  field name is read by a checker, so it stays English in every edition
  (`skills/implement/SKILL.md` §*The language the records are written in*).
  The Korean edition pairs markers only, and it carries no `Enforced by:` lines
  of its own until a marker at or above the cutoff reaches it.
- **A heading** is a live line matching `^#{1,6} `. The space is required,
  because `docs/one-root-by-lifetime.md` has a line beginning `#458 settled`
  and the Korean edition has one beginning `#79 만`. Neither is a heading, and
  a reader without the space counts both.
- **Three constants** live in the tests and nowhere else. `SHAPE_CUTOFF =
  1790154761` and `LINE_CEILING = 1000` are two of them. The third,
  `OVER_CEILING = {"docs/review-chain-spec.md": (29, "#<split issue>")}`, is
  keyed by path, holds the frozen count and the home, and is asserted to still
  exceed the ceiling. `docs/the-evidence-ledger.md` states the values in prose,
  and one case pins the prose against the constants, so the two cannot
  disagree.
- **Markers are read with the shared reader.** The checks use
  `unverified_check.live_lines` and `FOLD_MARKER` rather than a second regex,
  as `docs/the-evidence-ledger.md` §*The fold…* requires ("one function decides
  what live means").
- **Ledger.** New rows go to `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`.
  Nothing in `seal/ledger.md` moves, because nothing anchored there is removed.

## Overlap with PR #525 (#517), named

| File | #525 changes | This work changes | Expected conflict |
|---|---|---|---|
| `skills/settle/SKILL.md` | adds §*A fold is not a work item*, and rewrites §1, §4 and §*What a fold branch owes* | §2 only | none by hunk. After #525, §2 is the fold's spec, which is why the rules go there |
| `docs/one-root-by-lifetime.md` / `.ko.md` | appends a dated section, with no markers, to both | inserts the translated section and 10 markers into the Korean edition | none by hunk. The pairing test must pass on both orders of merge, and #525's section adds one heading to each edition |
| `docs/the-evidence-ledger.md` | rewrites the fold section's last three paragraphs (lines 171–224) | adds paragraphs to the same section | likely. Phase 3 rebases first if #525 has merged, and otherwise places its paragraphs directly after the *top level of `docs/`* paragraph |
| `docs/review-chain-spec.md` | +14 lines, no markers | none. The count is frozen at 29 | none. #525 adds no marker |

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

Framed 2026-09-23 by framer, before the build.
