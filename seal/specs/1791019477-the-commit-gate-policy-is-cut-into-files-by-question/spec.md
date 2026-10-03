# Feature Specification: the commit gate's policy is cut into files by question (#727)

<!-- seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/spec.md
WHAT this work delivers and how we will know. The policy documents in docs/
outrank this file; it cites them and does not restate them. Every line number
below was read at 2b1dcb1f, the branch's base; the heading lines there are the
same as the ones `docs/the-record-layout.md` §*What is decided and not built
yet* records at 233f0455 (41, 194, 268, 278, 760, 955, 995). -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-record-layout.md` §*What is decided and not built yet*, F1 | The cut itself: which headings go to `docs/the-commit-gate-inside-git.md`, which to `docs/the-review-and-parity-arms.md`, and what stays in `docs/commit-review-gate-spec.md` with an index naming the other two. Fold markers go across whole, and the `Over the ceiling` row goes away in the same change. This is ratified policy, so the frame follows it and does not reopen the file names or the cut |
| `docs/the-record-layout.md` §*The size a reader takes whole* | Each file stays at or under 1,000 lines and 64 KB. The bullet naming this document as over target goes, because after the cut it is not |
| #715's frame, `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/spec.md` D7 | The same cut, decided first. D7 also says *each is under 500 lines*; the parent is not (see *Data & interfaces*), and the frame corrects the figure rather than building to it |
| `skills/settle/SKILL.md` §*2. Write one standing statement per segment* | A document over its ceiling is split *along the headings it already has*. That is why the cut follows headings and moves text rather than rewording it |
| `templates/config.md` §*The fold's values*; `skills/settle/scripts/fold_check.py#ceiling_problems` | An `Over the ceiling` entry fails once its file is back under the ceiling ("Remove its entry; <home> was its home"). So the row and the cut must land in one commit, and the frozen marker count (18, digest `cb5d441b51a4`) must be conserved across the three files |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* (marker `1790208643`) and `tests/test_a_document_has_room_for_the_next_fold.py#test_the_evidence_ledger_states_the_values_the_config_rows_hold` | The prose states the `Over the ceiling` list and a pin holds it equal to the config row. The statement changes in the same commit as the row |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from` = `1790993141` | This item, `1791019477`, is above the cutoff. No released ledger file is edited. A released row whose anchor moves is re-pointed by a `Corrected ·` row in this item's fragment carrying every coordinate its claim still rests on; a row whose anchor stays but drifts gets a `Re-read ·` row; a row in another work item's unreleased fragment is re-stamped in place |
| `seal/releases/0.15.1.md` §*1790208643-the-spec-is-split-and-its-sentences-are-settled*, rows S2 and S3 (#526, the precedent) | S2: each document opens saying what it is the authority for and naming its siblings, and **a section moved to a sibling is cited there by the file that holds it**. S3: a sentence a case forbids is forbidden in every sibling, through one reader (`tests/conftest.py#review_chain_text`). Both carry over to this cut |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | The changelog entry goes in `seal/specs/1791019477-…/changelog.md`; ledger rows go in `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` |

## Scope

**In.**

1. `docs/commit-review-gate-spec.md` is cut into three files along its own headings, as F1's table says:
   - `docs/the-commit-gate-inside-git.md` takes lines 41–277: `## The commit gate inside git (pre-commit · reference-transaction · post-commit)` with `### Known limits of the commit gate inside git` and `### Where each state of a repository stands`.
   - `docs/the-review-and-parity-arms.md` takes lines 760–994: `### Review arm — opt-in: …` with its two `####` subsections, and `### Parity arm — opt-in: …`.
   - `docs/commit-review-gate-spec.md` keeps lines 1–40, 278–759 and 995–1047: the preamble, `## Registration`, `## commit-review-gate (PreToolUse, Bash)` through `### Why a deny, and why only once`, `## review-history-guard`, and `## implementer-mark · implementer-notice`.
2. The moved lines move verbatim (decision D2). The only words that change inside them are the positional references that would point across the cut (D5).
3. Each new file opens with its own H1 and an `Authority for …` paragraph naming the parent and the siblings, in the shape the three #526 documents already use. The parent's preamble names what it still holds and indexes the two new files (D3, D4).
4. `seal/config.md`'s `Over the ceiling` row goes from the entry for this document to `none` (D8). `docs/the-evidence-ledger.md`'s fold statement says no document is listed, in the same commit.
5. Every reference into the document that names a moved section, or whose subject moved, is re-pointed to the file that holds it (D6). The full list is in *The classes, enumerated* below.
6. Tests that read the document follow the text they pin (D10).
7. The ledger follows the move under the freeze (D7): two `Corrected ·` rows, and `Re-read ·` rows for what the edits drift.
8. `docs/the-record-layout.md` marks F1 built, lists the two new files in its `docs/` table, drops this document from the over-target list, and corrects the *under 500 lines* figure (D9).

**Out, each with its reason.**

| Left out | Why |
|---|---|
| Rewording, reflowing or re-levelling any moved sentence or heading | A move that rewords cannot be read as a move. The ledger hashes, the tests that slice on `### Review arm`, `#### The declaration, and where the check went` and `### Parity arm`, and survivor-check all depend on the bytes staying the same (D2) |
| Splitting the PreToolUse section further (482 lines, the parent's largest part) | F1 decides three files and the parent; the parent sits near 585 lines, under the ceiling. A fourth file is a decision F1 did not make |
| Every record under `seal/specs/*/` other than this item's, every released ledger file, and `CHANGELOG.md` | They record a moment, and the freeze forbids editing released ledger files. 83 files under `seal/specs/` name the old path (`git grep -l commit-review-gate-spec -- seal/specs`); none is a live instruction |
| `docs/the-evidence-ledger.md` line 302's history sentence, which names `docs/commit-review-gate-spec.md` as one of #526's three products | It is still true. Only line 305–310's present-tense *one document is listed over the ceiling now* becomes false, and that one changes |
| A permanent test or checker that resolves every `§*…*` citation repository-wide | No such check exists today; building one is mechanism, not a move. #526 verified its 36 citations with a one-off script, and this work does the same with a `test_tmp_*` probe (contract §7), recorded in the phase record (questions Q4) |
| Bare references whose subject stays in the parent | They still resolve and still point at the right file. Editing them only drifts ledger rows (D6) |
| Any edit #737 needs in this document | #737 runs in parallel and plans none; if it comes to need one, the orchestrator sequences it after this squash |
| F2, F3, F4 of the record layout | Their own issues: #728, #729, #730 |

## The classes, enumerated

Each class is listed by the command that produces it, with what follows the move. Counts were taken at 2b1dcb1f and are labelled **read** unless said otherwise.

### K1. Fold markers and `Enforced by:` lines

- **Command.** `grep -n '^<!-- specs/' docs/commit-review-gate-spec.md` and `grep -n '^Enforced by:' docs/commit-review-gate-spec.md`.
- **Count.** 18 live markers (line 888's backticked `<!-- specs/<work-item-id> -->` is prose, not a marker) and 23 `Enforced by:` lines.
- **By part.** Parent: markers at 25, 323, 384, 406, 997, 1020 (6), `Enforced by:` 11. Inside git: markers at 43, 60, 78, 90, 111, 128, 151, 179 (8), `Enforced by:` 8. Arms: markers at 770, 835, 853, 876 (4), `Enforced by:` 4.
- **How it follows.** A statement runs from its markers to the next marker or heading (`fold_check.py#numbered_statements`), so a cut on headings carries every statement whole. The moved `Enforced by:` lines name test targets that do not move. The 18-marker total is conserved, which is what the freeze digest counted. After the cut no file is listed, so the digest is not recomputed; it leaves with the row.

### K2. Tests that read the document's text

- **Commands.** `git grep -n "commit-review-gate-spec" -- tests` (14 files) and `git grep -n "review_chain_text\|REVIEW_CHAIN_DOCS" -- tests` (8 files).
- **How each literal was placed.** A scratch script parsed each referencing test function, took every string literal, and located it in the whitespace-collapsed document by line, then by part. **Executed** once, read-only, under the scratchpad.

| Site | What it reads | Part the text lives in after the cut | Follows by |
|---|---|---|---|
| `tests/conftest.py` `REVIEW_CHAIN_DOCS` (23) and `review_chain_text` | the absence reader over the review-chain documents | all | Extend the tuple to five: add `docs/the-commit-gate-inside-git.md` and `docs/the-review-and-parity-arms.md`, and say five in the comment and docstring (S3's rule) |
| `tests/test_chain_hooks_hardening.py#test_the_review_arms_missing_path_line_is_written_where_it_is_met` (507) | `### Review arm` … `####` slice | arms | Path |
| `tests/test_the_direct_answer_owes_the_sealers_record.py` `DIRECT_REQUIRES` key (41) | "the sealer's `broad-gate.md`" at 844, 854 | arms | Key re-pointed. The absence half then reads all five through `review_chain_text`, because the arms file is in `REVIEW_CHAIN_DOCS` |
| same file, `test_the_specification_says_why_two_answers_and_not_three` (116) | 857, 864 | arms | Path |
| `tests/test_the_reopening_is_one.py` `GATE_SPEC` (51, used at 640) | `#### The declaration, and where the check went` … `### Parity arm` | arms | Path |
| `tests/test_waiver_decided_at_start.py` (856, 862) | 926, 800, 920 | arms | Path (856's "per command" also stands at 301 in the parent; 926's "no standing waiver" does not, so the arms file is the one that must hold both) |
| `tests/test_release_hygiene.py` `VERSIONS_OF_ANOTHER_PRODUCT` (135–138) | git versions 2.34.1, 2.39.5, 2.43.0, 2.50.1 at 119–120, 182 | inside git | The four keys re-pointed |
| `tests/test_a_gate_that_fails_says_so.py` (896) | `## Registration` up to the next `\n## ` | parent | Nothing, provided the index is placed before `## Registration` (D4) |
| `tests/test_one_word_one_meaning.py#test_the_two_prompts_are_named_by_who_they_address` (134) | 312–318 | parent | Nothing |
| `tests/test_handoff_outlives_the_merge.py` (291) | `.specseal/handoff` at 1009 | parent | Nothing |
| `tests/test_one_word_one_meaning.py` sweep list (215) | instructing documents | all | Add both new files beside the parent, under the comment that already explains why #526's products joined |
| `tests/test_docs_line_wrap.py` `COVERED` (189) | wrapped documents | all | Add both new files. The moved lines were already held to the wrap, so they enter wrapped; the new preambles are written wrapped |
| `tests/test_a_document_has_room_for_the_next_fold.py` module docstring (16) | history | n/a | Its last sentence says the split is #715's; it becomes the record that #727 split it and the listing stayed, empty |
| prose mentions: `tests/test_chain_hooks_hardening.py` 460 (§*Review arm*), `tests/test_release_hygiene.py` 1900 (standing waiver), `tests/test_the_commit_gate_decides_at_the_commit.py` 439 and 594 (§*Known limits …*) | citations | arms, arms, inside git, inside git | Re-pointed (K5) |
| prose mentions whose subject stays: `tests/test_chain_hooks_hardening.py` 377, `tests/test_gate_judges_the_repo_it_commits_to.py` 1076 and 1213, `tests/test_what_the_reader_understands.py` 16 | citations | parent | Nothing |

The other `REVIEW_CHAIN_DOCS` consumers (`test_a_record_precedes_the_fixes_it_commissions.py`, `test_a_record_says_what_ran_it.py`, `test_one_word_one_meaning.py` 151, `test_the_last_rounds_fixes_are_checked.py`, `test_the_record_is_held_to_the_floor_and_the_depth.py`, `test_the_rules_have_one_owner.py`) read the reader or iterate the tuple. Extending the tuple widens their absence checks to the new files, which is the point, and changes no presence check.

### K3. Ledger rows anchored in the document

- **Command.** `git grep -n -o 'docs/commit-review-gate-spec.md#"[^"]*"' -- seal/ledger.md seal/releases seal/ledger`.
- **Count.** 12 coordinates in 10 rows. `seal/ledger.md` holds none.
- **What changes, by row.** Moves are by heading text, and a heading owns everything down to the next heading at its level or above (`evidence_check.py#heading_level` and the walk beside it).

| Row | Coordinate(s) | What the cut does | Follows by |
|---|---|---|---|
| `seal/releases/0.17.0.md` G17 (line 86) | `### Known limits of the commit gate inside git`@57e93f4b plus four coordinates in tests and `docs/worktree-guard-spec.md` | moves to `docs/the-commit-gate-inside-git.md` | **`Corrected ·` row**, carrying all five coordinates with the moved one at its new path |
| `seal/releases/0.4.0.md` *the review-chain specification's two opt-in headings…* (line 259) | `### Review arm — …`@3f374912, `### Parity arm — …`@4b9d8901 | both move to `docs/the-review-and-parity-arms.md` | **`Corrected ·` row**, both coordinates re-pointed. Its claim names *the review-chain specification*, which has not been the file for some time; the corrected claim names the arms document |
| `seal/releases/0.16.0.md` E9 (line 113) | `### Why a deny, and why only once`@1aa757b8, `## commit-review-gate (PreToolUse, Bash)`@e60b3b8c | the `##` unit stays but loses the Review arm and Parity arm, which sat under it | **`Re-read ·` row**. The claim (the automation row, the reversal, #662/#665) lives in the part that stays |
| `seal/releases/0.15.1.md` S2 (line 96) | `# commit-review-gate — behavior spec`>`"Authority for"`@b920d5fb, and the two sibling preambles | the parent's `Authority for` paragraph is rewritten (D4) | **`Re-read ·` row**, if the claim still holds after the rewrite, which D3 and D4 are written to keep. Where `docs/review-chain-spec.md`'s and `docs/round-record-spec.md`'s preambles are also edited (K5), the same row covers them, one row per released row |
| `seal/releases/0.16.0.md` G5 (line 80) | `## Registration — …`@38cf4f2a | stays, untouched | nothing |
| `seal/releases/0.16.0.md` lines 103, 107, 194, 250 | `#### A \`cd\` the gate cannot read`@529cc11c | stays, untouched | nothing |
| `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` line 12 (#716's fragment, unreleased) | the same `#### A \`cd\`` heading | stays, untouched | nothing. Were it to drift, it is re-stamped in place, because a citation into a fragment is refused |

**The count the prompt asked for: 2 `Corrected ·` rows, re-pointing 3 coordinates, and 2 `Re-read ·` rows for the document's own anchors.** That is cheap. The larger share of the ledger work comes from K5's edits to other files, which drift units that other rows anchor; see M1 in `questions.md`. Its upper bound, read off the anchors, is about 13 more released rows: `hooks/commit-review-gate.py#main` (6 rows), `#touches_code` (1, `0.14.0.md` line 61), `#DOC_ROOTS` in both hook files (1, `0.4.0.md` line 230), `chain_check.py#restored_from` (1), `tests/conftest.py` (1, `0.15.1.md` line 97), `tests/test_docs_line_wrap.py#COVERED` (2 released, plus one row in work item `1790993137`'s fragment, re-stamped in place), and `skills/agent-contract/SKILL.md` §17 (1). Whether a module-level comment counts inside the next assignment's unit is something only `evidence-check` can say.

### K4. `# RIDER:` comments

- **Commands.** `grep -n RIDER docs/commit-review-gate-spec.md` returns nothing, and `.github/scripts/rider_check.py#RIDER_ROOTS` is `(".github", "agents", "hooks", "skills", "templates", "tests")`, so no rider can live under `docs/`. A rider's stamp hashes a region of the file it stands in (`rider_check.py#region_hash`), never a document elsewhere.
- **Count.** 0. **How it follows.** Nothing to do. A rider whose comment text names the old path would have shown up in K5's grep, and none does.

### K5. Cross-references from other files

- **Command.** A scratch script over `git ls-files`, excluding `seal/specs/`, `seal/releases/`, `seal/ledger*` and `CHANGELOG.md`, collapses each file's whitespace so a wrapped `§*…*` is still one string. It lists every mention of `commit-review-gate-spec.md` with the `§*…*` that follows it, and every `*<moved heading>` that appears with no path in front. **Executed**, read-only. `git grep -n "commit-review-gate-spec" -- ':!seal/specs' ':!seal/releases' ':!seal/ledger' ':!CHANGELOG.md'` gives the same sites line by line.
- **The rule (D6).** A reference that names a moved heading, or whose subject now lives in a moved part, is cited by the file that holds it. A reference whose subject stays is left alone.

| Site | Reference | Subject now in | Follows by |
|---|---|---|---|
| `skills/agent-contract/SKILL.md` 251 (§9) and 356 (§17) | §*The commit gate inside git* | inside git | Re-point |
| `README.md` 190, `README.ko.md` 189 | `§The commit gate inside git` | inside git | Re-point |
| `README.md` 185, `README.ko.md` 184 | the documents list | n/a | Add links to the two new files beside the parent |
| `docs/round-record-spec.md` 7 | §*The declaration, and where the check went instead* | arms | Re-point |
| `docs/the-evidence-ledger.md` 477 | *The declaration, and where the check went instead* | arms | Re-point |
| `docs/the-evidence-ledger.md` 305–310 | *one document is listed over the ceiling now* | n/a | Rewritten with D8 |
| `docs/review-chain-spec.md` 7 | names the parent as the authority for the hooks | parent and two siblings | Name the two new siblings too (S2's shape) |
| `docs/the-record-layout.md` 43, 88, 160–174 | over-target bullet, `docs/` table, F1 | n/a | D9 |
| `hooks/commit-review-gate.py` 634 (comment above `DOC_ROOTS`) and 649 (`touches_code` docstring) | §*Review arm* | arms | Re-point |
| `hooks/gate.py` 60 (comment above `DOC_ROOTS`) | §*Review arm* | arms | Re-point |
| `hooks/gate.py` 14 (module docstring) | *the two arms, as … defines them* | arms | Re-point |
| `hooks/mode-gate.py` 63, `hooks/routing.py` 27 | the standing waiver the document refuses (arms, line 926) | arms | Re-point |
| `hooks/commit-review-gate.py` 1333 (in `main`) | *the known limit … states* (a commit in a clone with no hooks) | inside git, §*Known limits* | Re-point |
| `skills/code-review/scripts/chain_check.py` 3094 (`restored_from`) | a restored record was enforced at its earlier pull request (877–910) | arms | Re-point |
| `tests/test_chain_hooks_hardening.py` 460; `tests/test_release_hygiene.py` 1900; `tests/test_the_commit_gate_decides_at_the_commit.py` 439, 594 | see K2 | arms, arms, inside git, inside git | Re-point |
| `hooks/commit-review-gate.py` 454; `hooks/cmdline.py` 2234, 2384; `hooks/cmdline_base.py` 1692, 1772; `tests/test_chain_hooks_hardening.py` 377; `tests/test_gate_judges_the_repo_it_commits_to.py` 1076, 1213; `tests/test_what_the_reader_understands.py` 16 | an unresolvable target, `Unresolved`, the subshell case, parity declared through `seal/` | parent | Nothing |
| `seal/config.md` 13 | the `Over the ceiling` entry | n/a | D8 |

### K6. Positional references inside the document that cross the cut

- **Command.** `awk` over the document printing every line holding `above` or `below` with its part (25 lines). Each was read for its target.
- **Crossing.** Line 91 (*the ones below*, meaning the arms and the declaration), 199 and 273–274 (*the PreToolUse reading below*), and 283–284 (*The section above says when it stands aside*). They become citations by file and section (D5).
- **Internal.** The other 19 point within their own part, or are not positional at all (192 is an `Enforced by:` line, 229 is *a `claude` process above the commit*). The builder re-reads each one against the cut as it lands, because a word like *above* is only verifiable once the file exists (W1).

### K7. What survivor-check will see

- **Why it matters.** `skills/code-review/scripts/survivor_check.py#corrected` counts a sentence as corrected when a file holds it fewer times at the tip, and subtracts the n-grams of the sentences the range added.
- **What that means here.** A verbatim move removes a sentence from one file and adds it to another, so the move cancels itself out. What survivor-check can report is the wording changed: the positional sentences (K6), the parent's preamble, the record-layout and evidence-ledger sentences, and each re-pointed citation. Where the old wording still stands in a file that should keep it (a released ledger row quoting it, for one), it is exempted in this item's `survivors.md` with the quote; anything else is corrected.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the cut follows the headings | Given the base, when the branch lands, then `docs/the-commit-gate-inside-git.md` holds base lines 41–277 byte for byte, `docs/the-review-and-parity-arms.md` holds 760–994 byte for byte, and the parent holds 1–40, 278–759 and 995–1047, except for the K6 lines and the preambles | **executed**: a `test_tmp_*` probe compares each moved block against `git show 2b1dcb1f:docs/commit-review-gate-spec.md`, listing every differing line, which must be K6's alone; deleted after |
| S2 each file is under the ceiling | Each of the three is at most 1,000 lines and 64 KB (about 585, 250 and 250 lines; 39 KB, 21 KB and 17 KB) | **executed**: `tests/test_a_document_has_room_for_the_next_fold.py` and `bin/fold-check` |
| S3 the freeze lifts | `seal/config.md`'s `Over the ceiling` row reads `none`; `docs/the-evidence-ledger.md`'s fold statement lists no document, and the pin holds the two equal | **executed**: same module, `test_the_evidence_ledger_states_the_values_the_config_rows_hold` |
| S4 every statement keeps its shape | 18 markers across the three files (6, 8, 4), each statement with its one `Enforced by:` line, every target resolving | **executed**: `bin/fold-check` exits 0 |
| S5 every citation resolves | Every `§*X*` naming `docs/commit-review-gate-spec.md`, `docs/the-commit-gate-inside-git.md` or `docs/the-review-and-parity-arms.md`, in the live tree K5 covers, names a heading the cited file holds; no moved heading is cited by the parent's path | **executed**: a `test_tmp_*` probe, run once, its count recorded in the phase record and deleted (contract §7) |
| S6 each file opens saying what it holds | Each of the three opens with `Authority for …`, naming its siblings; the parent's preamble indexes the two new files ahead of `## Registration` | **read** by the warden; `tests/test_a_gate_that_fails_says_so.py#test_the_registration_section_says_a_failure_is_said_and_names_its_case` **executed** shows Registration's slice unchanged |
| S7 the tests follow their text | Every K2 site reads the file that holds its text, and `REVIEW_CHAIN_DOCS` names five documents | **executed**: the K2 modules, run as one narrow command |
| S8 the ledger follows under the freeze | No released ledger file changes. The two K3 `Corrected ·` rows and every `Re-read ·` row stand in this item's fragment; `evidence-check` reports nothing BROKEN or DRIFTED | **executed**: `bin/evidence-check`, and `bin/correction-check --range 2b1dcb1f...HEAD` |
| S9 the record layout marks F1 built | `docs/the-record-layout.md` lists the two files in its `docs/` table, no longer names this document over target, and marks F1 built with the corrected line counts | **read** by the warden; `tests/test_docs_line_wrap.py` **executed** if the file is in its list |
| S10 nothing survives unexplained | `bin/survivor-check --range 2b1dcb1f...HEAD` reports nothing, or each survivor is exempted in this item's `survivors.md` with its quote | **executed** by the builder before hand-back |

## Data & interfaces

**The parts' sizes at 2b1dcb1f, executed by a scratch script** (`wc`-style counts over the line ranges):

| Part | Lines | Bytes |
|---|---|---|
| parent (1–40, 278–759, 995–1047) | 576 | 38,990 |
| inside git (41–277) | 237 | 20,247 |
| arms (760–994) | 235 | 15,868 |

D7 and `docs/the-record-layout.md` both say *each is under 500 lines*. The parent is 576 before its index. The ceiling, 1,000, is the requirement, and all three meet it. The *500* is an aggregate nobody measured, and it is corrected where the record layout states it (D9).

**Decisions, with grounds.**

- **D1. The file names and the cut are F1's.** `docs/the-record-layout.md` is policy, which outranks this spec. The frame follows it.
- **D2. The moved lines move verbatim, at their own heading levels.** `### Known limits …`, `### Review arm …` and the others keep their `#` count and their text.
  - *What it keeps.* Every moved unit hashes as before, so a `Corrected ·` row records the same hash at the new path, and that sameness can be checked. The three tests that slice on heading markers change only their path. Survivor-check sees the move as a move (K7).
  - *What it costs.* The arms file has `###` sections under an H1. D3 adds a `##` above them, so there is no level gap.
- **D3. Each new file opens with an H1 in the siblings' style**, `# the commit gate inside git — behavior spec` and `# the review and parity arms — behavior spec`. Then comes an `Authority for …` paragraph, which names the parent, the other new file, `docs/review-chain-spec.md` and `docs/round-record-spec.md`, and ends *Update spec and code together*, as the three #526 documents do. The arms file adds one wrapper heading, `## The two arms of the commit gate`, above `### Review arm`. A heading added above a `###` changes nothing inside it.
- **D4. The parent keeps its H1 and rewrites its `Authority for` paragraph in place.** The paragraph keeps its opening words, so S2's minor anchor still finds it. It names what the parent still decides (registration, the PreToolUse reading, the review-history guard, the implementer mark) and indexes the two new files, one line each, by the question each answers (what git decides; what each arm wants). All of it sits before `## Registration`, so G5's anchor and S14's slice are untouched. The paragraph today claims *the two opt-in arms, and the routing declaration*, which after the cut belong to the arms file. Leaving that claim in would be false, which is why the paragraph is rewritten rather than appended to.
- **D5. A positional reference that crosses the cut becomes a citation** by file and section, in the shape `` `docs/commit-review-gate-spec.md` §*commit-review-gate (PreToolUse, Bash)* ``. No other word inside a moved block changes.
- **D6. A reference whose subject moved is cited by the file that holds it, bare or `§`-qualified, in docs, skills, READMEs, hooks and tests alike.** One rule, because an exception list is what rots. The cost is ledger drift on the code units those comments sit in (K3's upper bound), and each drift is a comment-only change re-read in one pass. A reference whose subject stays is not touched, because editing it buys nothing and drifts a row.
- **D7. The ledger follows the freeze**, as K3 says. No released file is edited.
- **D8. `Over the ceiling` becomes `none`, not a deleted row.**
  - *Grounds.* #526 left *the listing … empty* (`tests/test_a_document_has_room_for_the_next_fold.py`'s docstring). `templates/config.md` reads an absent row as *not declared*, and that turns the check off with one printed line, which is a different state from *declared, nothing listed*.
  - *Reading the task's words.* *The row for it is removed* is read as the entry removed and the row kept.
- **D9. `docs/the-record-layout.md`.**
  - F1 keeps its heading and table, which record the cut and the lines at 233f0455, and is marked built by #727.
  - *Four parts … decided here and built by their own issues* becomes three not yet built, with F1 built.
  - The `docs/` table narrows the parent's question and adds a row for each new file.
  - The over-target list drops its third bullet and says two kinds.
  - *Each is under 500 lines* becomes the measured counts.
- **D10. Tests follow their text, and the absence reader covers all five documents** (S3's rule). No pin is loosened. A pin that read a moved sentence reads it in the file that now holds it.
- **D11. No new test or checker.** Verification of S1 and S5 is by `test_tmp_*` probes run once and deleted (contract §7), as #526's citation check was. This work alters text that people and agents read, so it sits on the ladder's top rung. It adds no behaviour that a planted case would pin, beyond what K2's existing pins already hold.

## Open questions → questions.md

Every question a person would decide is decided by this frame, with its grounds above and its row in `questions.md`. The measurements and the work's own questions are listed there with who answers each.

Framed 2026-10-03 by framer, before the build.
